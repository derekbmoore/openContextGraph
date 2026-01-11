# 4-Layer Security Context

## Layer 1: SecurityContext (Identity)

- user_id, tenant_id, roles, scopes

## Layer 2: EpisodicContext (Conversation)

- conversation_id, messages, channel

## Layer 3: SemanticContext (Knowledge)

- facts, entities, graph_nodes

## Layer 4: OperationalContext (Runtime)

- current_agent, tool_calls, budgets

## Implementation

See: `backend/core/context.py`

## TODO

- [ ] Add RBAC matrix
- [ ] Document scope patterns
- [ ] Add multi-tenant isolation examples
