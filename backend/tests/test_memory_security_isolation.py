"""
Security isolation tests for memory access.

Tests to verify that memory access is properly isolated by:
- Tenant (users from different tenants cannot see each other's data)
- User (users within a tenant cannot see each other's personal memories)
- System memories (accessible only to authorized roles)
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from api.main import app
from core.context import Role, SecurityContext
from api.middleware.auth import get_current_user


@pytest.fixture
def user_tenant_a_alice():
    """Tenant A, User Alice"""
    return SecurityContext(
        user_id="user-alice",
        tenant_id="tenant-acme",
        roles=[Role.ANALYST],
        scopes=["*"],
        session_id="session-alice-1",
    )


@pytest.fixture  
def user_tenant_a_bob():
    """Tenant A, User Bob - SAME tenant as Alice"""
    return SecurityContext(
        user_id="user-bob",
        tenant_id="tenant-acme",
        roles=[Role.ANALYST],
        scopes=["*"],
        session_id="session-bob-1",
    )


@pytest.fixture
def user_tenant_b_charlie():
    """Tenant B, User Charlie - DIFFERENT tenant"""
    return SecurityContext(
        user_id="user-charlie",
        tenant_id="tenant-bigco",
        roles=[Role.ANALYST],
        scopes=["*"],
        session_id="session-charlie-1",
    )


@pytest.fixture
def admin_tenant_a():
    """Tenant A Admin"""
    return SecurityContext(
        user_id="admin-acme",
        tenant_id="tenant-acme",
        roles=[Role.ADMIN],
        scopes=["*"],
        session_id="session-admin-1",
    )


@pytest.fixture
def client_alice(user_tenant_a_alice):
    """Client authenticated as Alice (Tenant A)"""
    async def override():
        return user_tenant_a_alice
    app.dependency_overrides[get_current_user] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def client_charlie(user_tenant_b_charlie):
    """Client authenticated as Charlie (Tenant B)"""
    async def override():
        return user_tenant_b_charlie
    app.dependency_overrides[get_current_user] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestCrossTenantIsolation:
    """Tests to verify cross-tenant data isolation."""
    
    @pytest.mark.skip(reason="Integration test - requires live Zep connection")
    def test_user_in_tenant_a_cannot_see_tenant_b_episodes(self, client_alice, client_charlie):
        """User Alice (Tenant A) should not see Charlie's (Tenant B) episodes."""
        # Client Alice lists episodes
        resp_alice = client_alice.get("/api/v1/memory/episodes")
        assert resp_alice.status_code == 200
        episodes_alice = resp_alice.json()["episodes"]
        
        # Client Charlie lists episodes  
        resp_charlie = client_charlie.get("/api/v1/memory/episodes")
        assert resp_charlie.status_code == 200
        episodes_charlie = resp_charlie.json()["episodes"]
        
        # Verify no cross-contamination (if both have data)
        alice_ids = {e["id"] for e in episodes_alice}
        charlie_ids = {e["id"] for e in episodes_charlie}
        
        if alice_ids and charlie_ids:
            assert alice_ids.isdisjoint(charlie_ids), \
                f"Cross-tenant episode leakage detected! Common IDs: {alice_ids & charlie_ids}"
    
    @pytest.mark.skip(reason="Integration test - requires live Zep connection")
    def test_search_respects_tenant_boundary(self, client_alice, client_charlie):
        """Search results should be tenant-scoped."""
        query = {"query": "test", "limit": 100}
        
        resp_alice = client_alice.post("/api/v1/memory/search", json=query)
        resp_charlie = client_charlie.post("/api/v1/memory/search", json=query)
        
        assert resp_alice.status_code == 200
        assert resp_charlie.status_code == 200
        
        # Results should be different (tenant-scoped)
        results_alice = {r["id"] for r in resp_alice.json()["results"]}
        results_charlie = {r["id"] for r in resp_charlie.json()["results"]}
        
        if results_alice and results_charlie:
            assert results_alice.isdisjoint(results_charlie), \
                f"Cross-tenant search leakage! Common IDs: {results_alice & results_charlie}"


class TestCrossUserIsolation:
    """Tests to verify cross-user data isolation within same tenant."""
    
    def test_user_alice_cannot_see_user_bob_private_memories(
        self, 
        user_tenant_a_alice, 
        user_tenant_a_bob
    ):
        """Alice should not see Bob's personal memories (same tenant)."""
        from memory.access_policy import MemoryAccessPolicy
        
        # Bob's personal memory
        bobs_memory = {
            "user_id": "user-bob",
            "metadata": {"tenant_id": "tenant-acme"},
            "content": "Bob's secret project notes"
        }
        
        # Alice should NOT be able to access Bob's memory
        can_access = MemoryAccessPolicy.can_access_memory(
            user_tenant_a_alice,
            memory_user_id=bobs_memory["user_id"],
            memory_tenant_id=bobs_memory["metadata"]["tenant_id"]
        )
        
        assert not can_access, "Alice should NOT be able to access Bob's personal memory!"
    
    def test_admin_can_see_any_user_in_same_tenant(
        self, 
        admin_tenant_a, 
        user_tenant_a_alice
    ):
        """Admin should be able to access any user's memories in their tenant."""
        from backend.memory.access_policy import MemoryAccessPolicy
        
        # Alice's memory
        alices_memory = {
            "user_id": "user-alice",
            "metadata": {"tenant_id": "tenant-acme"},
        }
        
        can_access = MemoryAccessPolicy.can_access_memory(
            admin_tenant_a,
            memory_user_id=alices_memory["user_id"],
            memory_tenant_id=alices_memory["metadata"]["tenant_id"]
        )
        
        assert can_access, "Admin should be able to access any user's memory in their tenant"


class TestSystemMemoryAccess:
    """Tests for system-ingested memory access control."""
    
    def test_analyst_can_access_system_memories(self, user_tenant_a_alice):
        """Analyst should be able to access system memories."""
        from backend.memory.access_policy import MemoryAccessPolicy
        
        can_access = MemoryAccessPolicy.can_access_system_memories(user_tenant_a_alice)
        assert can_access, "Analyst should be able to access system memories"
    
    def test_viewer_cannot_access_system_memories(self):
        """Viewer role should NOT be able to access system memories."""
        from backend.memory.access_policy import MemoryAccessPolicy
        
        viewer = SecurityContext(
            user_id="user-viewer",
            tenant_id="tenant-acme",
            roles=[Role.VIEWER],
            scopes=[],
            session_id="session-viewer-1",
        )
        
        can_access = MemoryAccessPolicy.can_access_system_memories(viewer)
        assert not can_access, "Viewer should NOT be able to access system memories"
    
    def test_system_memory_requires_same_tenant(self, user_tenant_a_alice):
        """System memory access requires same tenant."""
        from backend.memory.access_policy import MemoryAccessPolicy
        
        # System memory from a different tenant
        other_tenant_system_memory = {
            "user_id": "system",
            "metadata": {"tenant_id": "tenant-bigco"},
        }
        
        can_access = MemoryAccessPolicy.can_access_memory(
            user_tenant_a_alice,
            memory_user_id="system",
            memory_tenant_id="tenant-bigco"  # Different tenant!
        )
        
        assert not can_access, "Cannot access system memory from different tenant"


class TestGlobalSearchSecurity:
    """Tests for global search security hardening."""
    
    @pytest.mark.asyncio
    async def test_global_search_requires_user_id(self):
        """Global search should fail without user_id."""
        from memory.client import ZepMemoryClient
        
        client = ZepMemoryClient()
        
        # Mock the HTTP client to avoid actual API calls
        with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = []
            
            # Global search without user_id should return empty
            results = await client.search_memory(
                session_id="global-search",
                query="test",
                user_id=None,  # No user_id!
                tenant_id="tenant-acme",
            )
            
            assert results["results"] == [], "Global search without user_id should return empty"
    
    @pytest.mark.asyncio
    async def test_global_search_requires_tenant_id(self):
        """Global search should fail without tenant_id."""
        from backend.memory.client import ZepMemoryClient
        
        client = ZepMemoryClient()
        
        with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = []
            
            # Global search without tenant_id should return empty
            results = await client.search_memory(
                session_id="global-search",
                query="test",
                user_id="user-alice",
                tenant_id=None,  # No tenant_id!
            )
            
            assert results["results"] == [], "Global search without tenant_id should return empty"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
