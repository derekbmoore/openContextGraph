-- Migration: Foundry Governance (user_threads, tool_invocations)
-- Description: Creates tables for tracking Foundry Agent state and auditing tool usage for incident response.

-- 1. User Threads (Persistence & Retention)
-- Tracks the mapping between internal users and external Foundry Thread IDs.
-- Includes 'expires_at' for strict retention enforcement.
CREATE TABLE IF NOT EXISTS user_threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    thread_id TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_user_threads_lookup ON user_threads(tenant_id, user_id, agent_id);
CREATE INDEX IF NOT EXISTS idx_user_threads_expiry ON user_threads(expires_at);

-- 2. Tool Invocations (Audit & Incident Response)
-- Logs every tool execution with identity context and policy decision.
-- Designed for "Who did what?" analysis.
CREATE TABLE IF NOT EXISTS tool_invocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id TEXT NOT NULL,          -- Foundry Run ID
    tool_call_id TEXT NOT NULL,    -- Foundry Tool Call ID (Stable)
    tenant_id TEXT NOT NULL,
    user_id TEXT,                  -- Human Subject (if known)
    agent_id TEXT NOT NULL,        -- Confgiured Agent Name
    actor_object_id TEXT,          -- Service Principal or User OID
    actor_type TEXT,               -- 'autonomous' or 'user_obo'
    tool_name TEXT NOT NULL,
    resource_scope TEXT,           -- Target Resource (e.g. repo name)
    decision TEXT,                 -- 'ALLOW' or 'DENY'
    policy_rule TEXT,              -- ID of rule triggering the decision
    inputs_hash TEXT,              -- Redacted/Hashed inputs
    outputs_hash TEXT,             -- Redacted/Hashed outputs
    duration_ms INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_tool_invocations_run ON tool_invocations(run_id);
CREATE INDEX IF NOT EXISTS idx_tool_invocations_audit ON tool_invocations(tenant_id, agent_id, created_at);

-- 3. RLS Policies (Draft - to be refined)
-- Ensure isolation so tenants cannot query each other's audit logs
ALTER TABLE user_threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE tool_invocations ENABLE ROW LEVEL SECURITY;

-- Simple isolation policy (assumes app passes tenant_id config, similar to existing pattern)
-- CREATE POLICY tenant_isolation_threads ON user_threads
--     USING (tenant_id = current_setting('app.current_tenant', true));

-- CREATE POLICY tenant_isolation_tools ON tool_invocations
--     USING (tenant_id = current_setting('app.current_tenant', true));
