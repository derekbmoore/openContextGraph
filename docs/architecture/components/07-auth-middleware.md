# Auth Middleware — OIDC Integration

## Purpose

Auth Middleware provides **identity verification and access control** at the API edge. It supports both enterprise OIDC providers (Azure AD, Keycloak) and development modes, ensuring every request has a verified `SecurityContext`.

## Why This Exists

### The Problem

AI systems without proper authentication:

- **Cannot attribute actions** to users
- **Cannot enforce multi-tenancy**
- **Cannot meet compliance requirements**
- **Cannot implement RBAC**

### The Solution

JWT-based authentication middleware that:

1. **Validates tokens** from OIDC providers
2. **Extracts identity claims** into SecurityContext
3. **Enforces RBAC** through decorators
4. **Supports multi-tenant** isolation

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Client Request                             │
│   Authorization: Bearer <JWT>                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Auth Middleware                            │
├─────────────────────────────────────────────────────────────┤
│  1. Extract JWT from Authorization header                    │
│  2. Validate signature (JWKS)                                │
│  3. Verify claims (issuer, audience, expiry)                 │
│  4. Extract identity (user_id, tenant_id)                    │
│  5. Map roles and scopes                                     │
│  6. Create SecurityContext                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              SecurityContext (Layer 1)                       │
│  user_id, tenant_id, roles, scopes, email, display_name     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                     [Protected Route Handler]
```

---

## Code Sample

```python
# backend/api/middleware/auth.py
"""
OIDC Authentication Middleware

Provides:
- JWT token validation from OIDC providers
- User identity extraction
- Role-based access control (RBAC)
- Multi-tenant support

Supports:
- Azure AD / Entra ID
- Keycloak
- Any OIDC-compliant provider

NIST AI RMF Alignment:
- GOVERN 1.2: Accountability through verified identity
- MAP 1.5: System boundaries via tenant isolation
- MANAGE 1.3: Access control through RBAC
"""

import logging
import os
from typing import Optional
from datetime import datetime, timezone

import httpx
from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core import SecurityContext, Role

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
    """Decoded JWT token payload from OIDC provider."""
    sub: str                      # Subject (user identifier)
    oid: Optional[str] = None     # Object ID (Azure AD specific)
    tid: Optional[str] = None     # Tenant ID
    preferred_username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    roles: list[str] = []
    scp: Optional[str] = None     # Scopes
    aud: str                      # Audience
    iss: str                      # Issuer
    exp: int                      # Expiration
    iat: int                      # Issued at


class OIDCAuth:
    """
    OIDC Authentication Handler.
    
    Validates JWT tokens from any OIDC-compliant provider.
    
    NIST AI RMF: GOVERN 1.2 - Verified identity for accountability
    """
    
    def __init__(self):
        """Initialize from environment variables."""
        self._issuer_url = os.getenv("OIDC_ISSUER_URL")
        self._client_id = os.getenv("OIDC_CLIENT_ID")
        self._audience = os.getenv("OIDC_AUDIENCE", self._client_id)
        self._jwks: Optional[dict] = None
        self._jwks_uri: Optional[str] = None
    
    @property
    def issuer_url(self) -> str:
        return self._issuer_url
    
    @property
    def client_id(self) -> str:
        return self._client_id
    
    async def get_jwks(self) -> dict:
        """
        Fetch and cache JWKS (JSON Web Key Set).
        
        JWKS contains the public keys used to verify JWT signatures.
        """
        if self._jwks is not None:
            return self._jwks
        
        # Discover JWKS URI from well-known endpoint
        if not self._jwks_uri:
            async with httpx.AsyncClient() as client:
                discovery_url = f"{self.issuer_url}/.well-known/openid-configuration"
                response = await client.get(discovery_url)
                response.raise_for_status()
                config = response.json()
                self._jwks_uri = config.get("jwks_uri")
        
        # Fetch JWKS
        async with httpx.AsyncClient() as client:
            response = await client.get(self._jwks_uri)
            response.raise_for_status()
            self._jwks = response.json()
        
        return self._jwks
    
    async def validate_token(self, token: str) -> TokenPayload:
        """
        Validate a JWT token from the OIDC provider.
        
        NIST AI RMF Controls:
        - GOVERN 1.2: Validates token signature
        - MAP 1.5: Extracts tenant_id for isolation
        
        Args:
            token: JWT token string
        
        Returns:
            TokenPayload with decoded claims
        
        Raises:
            HTTPException if validation fails
        """
        try:
            # Get JWKS for signature verification
            jwks = await self.get_jwks()
            
            # Decode and validate the token
            payload = jwt.decode(
                token,
                jwks,
                algorithms=["RS256"],
                audience=self._audience,
                issuer=self.issuer_url,
                options={"verify_exp": True}
            )
            
            return TokenPayload(**payload)
            
        except JWTError as e:
            logger.warning(f"Token validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def map_roles(self, token_roles: list[str]) -> list[Role]:
        """
        Map OIDC roles to application roles.
        
        Supports both direct and prefixed role names:
        - "admin" → Role.ADMIN
        - "App.Admin" → Role.ADMIN
        """
        role_mapping = {
            "admin": Role.ADMIN,
            "analyst": Role.ANALYST,
            "pm": Role.PM,
            "viewer": Role.VIEWER,
            "developer": Role.DEVELOPER,
        }
        
        mapped = []
        for role in token_roles:
            # Handle prefixed roles (e.g., "App.Admin")
            role_name = role.split(".")[-1].lower()
            if role_name in role_mapping:
                mapped.append(role_mapping[role_name])
        
        return mapped
    
    def extract_scopes(self, token: TokenPayload) -> list[str]:
        """Extract scopes from token."""
        if token.scp:
            return token.scp.split(" ")
        return []


# Global auth instance
_auth: Optional[OIDCAuth] = None


def get_auth() -> OIDCAuth:
    """Get or create the auth instance."""
    global _auth
    if _auth is None:
        _auth = OIDCAuth()
    return _auth


def _get_auth_required() -> bool:
    """Check if authentication is required."""
    return os.getenv("AUTH_REQUIRED", "true").lower() == "true"


_AUTH_REQUIRED = _get_auth_required()


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> SecurityContext:
    """
    FastAPI dependency to get the current authenticated user.
    
    CRITICAL: This is the entry point for all authentication.
    
    NIST AI RMF Controls:
    - GOVERN 1.2: Every request attributed to a user
    - MAP 1.5: Tenant isolation enforced
    - MANAGE 1.3: Roles extracted for RBAC
    
    Usage:
        @router.get("/protected")
        async def protected_route(user: SecurityContext = Depends(get_current_user)):
            return {"user": user.user_id}
    """
    # Development mode - return POC user
    if not _AUTH_REQUIRED:
        logger.debug("Auth disabled, returning POC user")
        return SecurityContext(
            user_id="poc-user",
            tenant_id="poc-tenant",
            roles=[Role.ADMIN],
            scopes=["*"],
            email="poc@example.com",
            display_name="POC User",
        )
    
    # Production mode - validate token
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth = get_auth()
    token = await auth.validate_token(credentials.credentials)
    
    # Build SecurityContext from token claims
    return SecurityContext(
        user_id=token.oid or token.sub,
        tenant_id=token.tid or "default",
        roles=auth.map_roles(token.roles),
        scopes=auth.extract_scopes(token),
        email=token.email or token.preferred_username,
        display_name=token.name,
        token_expiry=datetime.fromtimestamp(token.exp, tz=timezone.utc),
    )


def require_roles(*required_roles: Role):
    """
    Decorator/dependency to require specific roles.
    
    NIST AI RMF: MANAGE 1.3 - Role-based access control
    
    Usage:
        @router.get("/admin")
        async def admin_route(
            user: SecurityContext = Depends(require_roles(Role.ADMIN))
        ):
            return {"admin": True}
    """
    async def role_checker(
        user: SecurityContext = Depends(get_current_user),
    ) -> SecurityContext:
        for role in required_roles:
            if user.has_role(role):
                return user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Required roles: {[r.value for r in required_roles]}",
        )
    
    return role_checker


def require_scopes(*required_scopes: str):
    """
    Decorator/dependency to require specific scopes.
    
    Usage:
        @router.get("/project/{project_id}")
        async def project_route(
            project_id: str,
            user: SecurityContext = Depends(require_scopes("projects:read"))
        ):
            return {"project": project_id}
    """
    async def scope_checker(
        user: SecurityContext = Depends(get_current_user),
    ) -> SecurityContext:
        for scope in required_scopes:
            if not user.has_scope(scope):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required scope: {scope}",
                )
        return user
    
    return scope_checker
```

---

## Supported Providers

### Azure AD / Entra ID

```env
OIDC_ISSUER_URL=https://login.microsoftonline.com/{tenant-id}/v2.0
OIDC_CLIENT_ID=your-client-id
OIDC_AUDIENCE=your-client-id
```

### Keycloak

```env
OIDC_ISSUER_URL=https://keycloak.example.com/realms/ctxEco
OIDC_CLIENT_ID=ctxEco-backend
OIDC_AUDIENCE=ctxEco
```

### Development Mode

```env
AUTH_REQUIRED=false
```

---

## NIST AI RMF Alignment

| Function | Control | Implementation |
|----------|---------|----------------|
| **GOVERN 1.2** | Accountability | Every request has verified `user_id` |
| **MAP 1.5** | Boundaries | `tenant_id` enables isolation |
| **MANAGE 1.3** | Access Control | `require_roles()`, `require_scopes()` |
| **MEASURE 2.7** | Monitoring | Token validation logged |

---

## Summary

Auth Middleware provides:

- ✅ OIDC-based JWT validation
- ✅ SecurityContext creation from claims
- ✅ Role-based access control
- ✅ Multi-tenant isolation
- ✅ NIST AI RMF compliance

*Document Version: 1.0 | Created: 2026-01-11*
