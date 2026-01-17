# Security Architecture: Isolation & Controls (FedRAMP High)

## 1. Executive Summary

This document defines the security architecture for OpenContextGraph to meet **NIST AI RMF**, **FedRAMP High**, and **IL5** requirements. The core objective is **Zero Trust Data Isolation**: ensuring that irrespective of the authentication method (CIAM vs. Local Tenant), a user can *only* access data explicitly authorized for their **Security Groups** (Department/Project).

## 2. Identity & Authorization (AuthN/AuthZ)

We move beyond simple "Tenant Isolation" to **Attribute-Based Access Control (ABAC)**.

### 2.1 The Usage of Claims

The OIDC Token (from Entra ID or CIAM) must include a `groups` or `wids` claim.

* **Tenant ID (`tid`)**: Hard boundary. Data never leaks across tenants.
* **Security Groups (`groups`)**: Soft boundaries. Maps to Departments (e.g., `Dept:HR`, `Dept:Engineering`) and Projects (e.g., `Proj:Alpha`).

### 2.2 Security Context Propagation

The `SecurityContext` object in `core/context.py` will be expanded:

```python
class SecurityContext:
    user_id: str
    tenant_id: str
    roles: List[Role]       # Admin, Viewer (Functional)
    groups: List[str]       # "group-id-123", "group-id-456" (Data Access)
    clearance: str          # "public", "confidential", "secret"
```

### 2.3 Tenant Configuration Requirements (Phase 0)

To support this model, the Customer Tenant (Azure AD) must be provisioned with a standard Group Taxonomy.

**Standard Roles (Functional):**

* `OpenContext:Admin` - Platform administrators.
* `OpenContext:Analyst` - Power users who can see "Internal" data.
* `OpenContext:User` - Standard consumers.

**Data Access Groups (ABAC Attributes):**

* **Departments:** `Dept:[Name]` (e.g., `Dept:Finance`, `Dept:HR`, `Dept:Engineering`).
* **Projects:** `Proj:[Codename]` (e.g., `Proj:Alpha`, `Proj:Manhattan`).

*Scripts provided: `scripts/setup_tenant_groups.sh` will automate this provisioning.*

## 3. Data Classification & Ingestion

All data entering the "Context Ecology" via `AntigravityRouter` must be tagged with an **Access Control List (ACL)**.

### 3.1 Classification Levels

1. **Public:** Access within Tenant.
2. **Internal:** Access restricted to Employee role.
3. **Confidential:** Access restricted to specific Department Groups.
4. **Restricted:** Access restricted to specific Project Groups + Individuals.

### 3.2 Ingestion Tagging (The "Stamp")

When `antigravity_router.ingest(file)` is called, it must accept an ACL:

```json
{
  "provenance_id": "CLASS-A-uuid",
  "tenant_id": "tenant-abc",
  "acl_groups": ["dept-engineering", "proj-apollo"],
  "classification": "confidential"
}
```

## 4. Storage & Retrieval Controls

### 4.1 Vector Store (Zep) - "ABAC Filter"

Every search query **MUST** apply a mandatory filter intersection.

* **Query:** "Show me the budget."
* **User Context:** `groups=["dept-finance"]`
* **Effective Filter:**

    ```json
    {
      "where": {
        "and": [
          {"jsonpath": "$.system.tenant_id == 'tenant-abc'"},
          {"or": [
             {"jsonpath": "$.custom.acl_groups ?| array['dept-finance']"},
             {"jsonpath": "$.custom.owner_id == 'user-123'"}
          ]}
        ]
      }
    }
    ```

### 4.2 Relational DB (Postgres) - "Row Level Security (RLS)"

We will enable native Postgres RLS.

```sql
CREATE POLICY "tenant_isolation" ON documents
    USING (tenant_id = current_setting('app.current_tenant'));

CREATE POLICY "group_access" ON documents
    USING (acl_groups && current_setting('app.current_groups')::text[]);
```

## 5. PII Masking & Obfuscation

Sensitive columns will use **Dynamic Data Masking** based on Role.

| Data Element | Role: Analyst | Role: Admin | Role: System |
|--------------|---------------|-------------|--------------|
| `email` | `s*****@company.com` | `sarah@company.com` | `sarah@company.com` |
| `ssn` | `***-**-****` | `***-**-****` | `123-45-6789` |
| `credit_card` | `XXXX-1234` | `XXXX-1234` | `Encrypted` |

**Implementation:** `postgresql-anonymizer` extension or specific View layers.

## 6. Audit Logging (NIST AU-3)

Every "Read" access to a Class A (Truth) document is logged to an immutable ledger (Blob WORM storage or Log Analytics), recording:

* *Who* (User ID)
* *What* (Provenance ID)
* *Why* (Justification/Query)
* *When* (Timestamp)
