# Graph Knowledge Security & Isolation Features

**Status:** Implemented (v1.0)
**Date:** January 17, 2026
**Component:** OpenContextGraph (Backend/Frontend)

## 1. Overview

The Graph Knowledge system (`/memory/graph`) is the visual interface for the organization's "Context Ecology." Because this graph contains sensitive intellectual property and operational memory, we enforce a **Strict Zero Trust Isolation Model** by default.

This document details the security features implemented to ensure data sovereignty, tenant isolation, and future-proof department visibility.

## 2. Core Security Features

### 2.1 Multi-Tenant Isolation

**Enforcement:** Hard Boundary via `tenant_id`.

Every interaction with the Memory Graph is scoped to the specific Azure AD Tenant ID of the caller.

* **Implementation:** The Backend API extracts `tid` (Tenant ID) from the OIDC Token.
* **Verification:** `ZepMemoryClient.list_sessions(..., tenant_id=user.tenant_id)` is called for every request.
* **Result:** A user in Tenant A (e.g., Zimax) can **never** access or visualize nodes from Tenant B (e.g., Customer X), even if they share the same physical database.

### 2.2 Strict User Privacy (Default View)

**Enforcement:** Private-by-Default via `user_id`.

Currently, the Knowledge Graph is scoped to the **Authenticated User**.

* **Visualization:** When you load `/memory/graph`, you see **only** the Episodes you participated in and the Facts derived from them.
* **Logic:** The API queries Zep for sessions where `owner_id == current_user.oid`.
* **Why:** This prevents accidental leakage of sensitive "HR" or "Finance" discussions to the broader organization before explicit sharing policies are configured.

### 2.3 Security Context Tagging (The "Stamp")

**Enforcement:** Write-time Metadata Injection.

To enable future "Department-wide Knowledge" (e.g., *Engineering Team sees all Tech Specs*), we must verify the *provenance* of every memory.

We have implemented automatic **Security Context Stamping** in the Chat/Ingestion pipeline (`/api/v1/chat`).

**Every new memory session is stamped with:**

```json
{
  "metadata": {
    "tenant_id": "8888-xxxx-xxxx-xxxx",    // The Organization
    "user_id": "user-123",                 // The Owner
    "project_id": "proj-alpha",            // The Project Context (if set)
    "groups": ["group-engineering", "group-admins"], // The Owner's Departments
    "classification": "internal"           // Default sensitivity
  }
}
```

**Strategic Value:**
Even though the current UI shows a "Private View," the underlying data is already "Dept-Aware." We can simply update the read-policy (Search Query) to include `"groups" CONTAINS "group-engineering"` to unlock shared knowledge, without needing to migrate or re-tag data.

## 3. Architecture Diagrams

### 3.1 Data Visibility Flow

```mermaid
graph TD
    User[User (Engineering)] -->|Token {groups: ['eng']}| API[API Gateway]
    API -->|Extract Claims| Guard[Security Guard]
    Guard -->|1. Enforce Tenant| Zep[Zep Memory]
    Guard -->|2. Enforce User/Group| Graph[Graph Builder]
    
    subgraph "Isolation Barriers"
        Zep -->|Filter: tenant_id| Data[Raw Data]
        Data -->|Filter: owner == user OR group IN user.groups| Nodes[Visible Nodes]
    end
    
    Nodes --> Graph
    Graph -->|JSON| UI[Frontend Graph]
```

## 4. Verification

To verify these controls:

1. **Isolation:** Log in as User A. Chat with Sage. Log in as User B. User B's graph should **not** show User A's new nodes.
2. **Tagging:** Inspect the Zep Session Metadata (via `/api/v1/memory/sessions`). New sessions will contain the `groups` and `project_id` fields.

---
*Implementation in `backend/api/routes/chat.py` and `backend/api/routes/graph.py`.*
