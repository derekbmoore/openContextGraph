"""
Memory access policy enforcement.

Defines and enforces access control policies for memory operations,
particularly for system-ingested memories and cross-user access.
"""

from core import SecurityContext, Role


class MemoryAccessPolicy:
    """
    Policy for memory access control.
    
    Enforces:
    - Tenant isolation (users can only access their tenant's memories)
    - User isolation (users can only access their own memories by default)
    - System memory access (controlled access to user_id="system" memories)
    - Admin override (admins can access all memories in their tenant)
    """
    
    # Roles that can access system memories (user_id="system")
    SYSTEM_MEMORY_ROLES = [Role.ADMIN, Role.ANALYST, Role.PM]
    
    # Roles that can access any user's memories within their tenant
    TENANT_ADMIN_ROLES = [Role.ADMIN]
    
    @classmethod
    def can_access_system_memories(cls, user: SecurityContext) -> bool:
        """
        Check if user can access system-ingested memories.
        
        System memories (user_id="system") are typically documentation
        or organizational knowledge ingested programmatically.
        """
        return any(role in cls.SYSTEM_MEMORY_ROLES for role in user.roles)
    
    @classmethod
    def can_access_memory(
        cls, 
        user: SecurityContext, 
        memory_user_id: str, 
        memory_tenant_id: str
    ) -> bool:
        """
        Check if user can access a specific memory.
        
        Args:
            user: The authenticated user's security context
            memory_user_id: The user_id of the memory's owner
            memory_tenant_id: The tenant_id of the memory
            
        Returns:
            True if access is allowed, False otherwise
        """
        # SECURITY: Tenant isolation is mandatory
        if user.tenant_id != memory_tenant_id:
            return False
        
        # Admin can access any memory in their tenant
        if Role.ADMIN in user.roles:
            return True
        
        # Users can access their own memories
        if user.user_id == memory_user_id:
            return True
        
        # System memories are accessible per SYSTEM_MEMORY_ROLES
        if memory_user_id == "system":
            return cls.can_access_system_memories(user)
        
        # Default: deny access to other users' memories
        return False
    
    @classmethod
    def filter_accessible_memories(
        cls,
        user: SecurityContext,
        memories: list[dict],
    ) -> list[dict]:
        """
        Filter a list of memories to only those the user can access.
        
        Args:
            user: The authenticated user's security context
            memories: List of memory dicts with 'user_id' and 'metadata.tenant_id'
            
        Returns:
            Filtered list containing only accessible memories
        """
        accessible = []
        for memory in memories:
            memory_user_id = memory.get("user_id", "")
            memory_tenant_id = memory.get("metadata", {}).get("tenant_id", "")
            
            # If no tenant_id, treat as legacy (allow if user matches or is system)
            if not memory_tenant_id:
                if memory_user_id == user.user_id or memory_user_id == "system":
                    accessible.append(memory)
                continue
            
            if cls.can_access_memory(user, memory_user_id, memory_tenant_id):
                accessible.append(memory)
        
        return accessible
