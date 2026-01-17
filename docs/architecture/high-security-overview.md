# OpenContextGraph: High-Security Architecture Overview

**Security Level:** FedRAMP High / IL5 Ready
**Philosophy:** Zero Trust Data Isolation via Contextual Provenance

## 1. Executive Summary

This document details how **OpenContextGraph** ("ctxEco") achieves compliance with strict federal and enterprise security requirements (NIST AI RMF, FedRAMP High). Unlike standard RAG implementations, ctxEco treats security as a **metadata-driven dimension** of the data itself, not just a gateway check.

The system implements a **Defense-in-Depth** strategy across four layers: Identity, Ingestion, Memory, and Storage.

---

## 2. Core Security Pillars

### A. Zero Trust Identity (ABAC + RBAC)

* **Legacy RBAC:** Standard Roles (`Admin`, `Analyst`) provide functional access.
* **Modern ABAC (Attribute-Based Access Control):** Data access is governed by **Claims** (Attributes) carried in the user's opaque token.
  * **Mechanism:** `SecurityContext` extracts `groups` from OIDC tokens.
  * **Taxonomy:** Access is granted via strict Group membership (`Dept:Finance`, `Proj:Manhattan`).
  * **Agent Identity:** AI Agents (Elena, Marcus, Sage) are **Service Principals** in Azure AD, bound by the same restrictions as human users.
    * *Example:* `Agent:Marcus` (Engineering) cannot see data tagged `Dept:Finance`.

### B. Ingestion Provenance (The "Antigravity" Layer)

Data is secured *before* it enters the system.

* **Antigravity Router:** Automatically tags content based on classification rules.
  * **Class A (Truth):** Strict OCR (Docling) + High Classification.
  * **Class C (Ops):** Structured Data + granular ACLs.
* **ACL Injection:** Every vector chunk carries an immutable Access Control List (ACL) in its metadata (`acl_groups`).
  * *Example:* A financial report is ingested with `metadata.acl_groups = ['Dept:Finance']`.

### C. Memory Isolation (The "Zep" Layer)

We enforce mandatory filtering at the retrieval layer. No vector search can execute without scoping.

* **Tri-Search Security:** The `search_memory` function constructs a mandatory JSONPath filter:

    ```sql
    WHERE (tenant_id = :tenant)
    AND (
        (user_id = :user) -- Private memory
        OR
        (acl_groups && :user_groups) -- Departmental memory
    )
    ```

* **Result:** A query for "Quarterly Revenue" by an Engineer yields **0 results**, even if the vector similarity is 1.0.

### D. Database Hardening (Row-Level Security)

PostgreSQL enforces the final line of defense.

* **RLS Policies:** Defined in `backend/database/rls_policies.sql`.
* **Mechanism:** Even if the API application logic fails, the database rejects queries that attempt to read rows outside the user's Tenant or Group set.

---

## 3. Compliance Mapping (NIST AI RMF)

| NIST Control | Feature Implementation |
| :--- | :--- |
| **MANAGE 1.3** | **Access Control:** Full integration with Entra ID Service Principals and Groups. |
| **MANAGE 2.3** | **Data Isolation:** Metadata-driven ACLs on every vector chunk. |
| **MEASURE 2.1** | **System Integrity:** Provenance ID links every answer back to a specific file version. |
| **GOVERN 1.2** | **Auditability:** Agent actions are logged with their Service Principal ID. |

---

## 4. Why This Exemplifies "Context Ecology"

In a "Context Ecology," information is not static; it is alive and bound to its environment. Security is the "Gravity" that keeps sensitive data grounded to its owners. By implementing these features, we ensure that **Context never leaks** across boundaries—it exists only where it is permitted to exist.
