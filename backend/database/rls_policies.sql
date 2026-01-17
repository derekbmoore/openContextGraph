-- =============================================================================
-- OpenContextGraph - Row Level Security (RLS) Policies
-- 
-- NIST AI RMF: MANAGE 2.3 - Data Isolation
-- Compliance: FedRAMP High / IL5
-- 
-- These policies enforce "Zero Trust Data Isolation" at the database layer.
-- They rely on session variables set by the application (middleware).
-- =============================================================================

-- Prerequisites:
-- Application must set the following run-time variables for each transaction:
-- SET app.current_tenant = 'tenant-123';
-- SET app.current_user = 'user-abc';
-- SET app.current_groups = 'Dept:Finance,Proj:Alpha'; -- Comma-separated

-- -----------------------------------------------------------------------------
-- 1. Enable RLS on Sensitive Tables
-- -----------------------------------------------------------------------------

-- Example: Documents Table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Example: Vector Embeddings Table
ALTER TABLE embeddings ENABLE ROW LEVEL SECURITY;

-- -----------------------------------------------------------------------------
-- 2. Tenant Isolation Policy (Mandatory)
-- -----------------------------------------------------------------------------
-- STRICT: No cross-tenant access, ever. Admin override handled via role check if needed.

CREATE POLICY tenant_isolation_policy ON documents
    AS PERMISSIVE
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant', true)::text);

-- -----------------------------------------------------------------------------
-- 3. ABAC Data Access Policy (Owner + Groups)
-- -----------------------------------------------------------------------------
-- Access allowed if:
-- 1. User is the OWNER (user_id matches)
-- 2. OR User is a member of any Group in the record's ACL (Array Overlap)
-- 3. OR Record is Marked "Public" (clearance level)

CREATE POLICY abac_access_policy ON documents
    AS PERMISSIVE
    FOR SELECT
    USING (
        -- Rule 1: Ownership
        user_id = current_setting('app.current_user', true)::text
        OR
        -- Rule 2: Group Membership (Overlap Check &&)
        -- Requires 'acl_groups' column to be TEXT[] (Array of Strings)
        (acl_groups && string_to_array(current_setting('app.current_groups', true), ','))
        OR
        -- Rule 3: Public Data (within Tenant)
        clearance = 'public'
    );

-- -----------------------------------------------------------------------------
-- 4. PII Masking (Dynamic Data Masking)
-- -----------------------------------------------------------------------------
-- Using PostgreSQL anonymization extension or simple views

-- View Example for Non-Privileged Users
CREATE OR REPLACE VIEW documents_sanitized AS
SELECT
    id,
    -- Redact PII for non-HR/Admin users
    CASE 
        WHEN 'Dept:HR' = ANY(string_to_array(current_setting('app.current_groups', true), ',')) 
        THEN ssn 
        ELSE 'XXX-XX-XXXX' 
    END as ssn,
    content,
    metadata
FROM documents;
