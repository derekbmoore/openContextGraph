"""
API Middleware Package - openContextGraph

Provides middleware for:
- Authentication (OIDC/JWT)
- RBAC (Role-based access control)
"""

from api.middleware.auth import (
    get_current_user,
    require_roles,
    require_scopes,
    OIDCAuth,
)

__all__ = [
    "get_current_user",
    "require_roles",
    "require_scopes",
    "OIDCAuth",
]
