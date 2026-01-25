# Domain Memory Quick Start

## What is Domain Memory?

Domain Memory solves the "Green Intern" problem: AI agents that forget project context between sessions. This file (`.ctxeco/domain-memory.md`) stores project-specific knowledge that agents need to remember.

## How It Works

1. **Research Phase**: Agents read this file before making changes
2. **Implementation**: Agents make changes following established patterns
3. **Update Phase**: Agents update this file with new decisions/patterns
4. **Auto-Ingestion**: Updates are automatically ingested into Zep for long-term memory

## For Developers

### Reading Domain Memory

Agents automatically read this file via the `read_domain_memory` MCP tool. You can also:
- Open `.ctxeco/domain-memory.md` in any IDE (Cursor, VS Code, Antigravity)
- Search for patterns, decisions, or known issues
- Review project evolution

### Updating Domain Memory

**Option 1: Via Agent**
Ask an agent to update Domain Memory after making a decision:
> "After fixing the CORS issue, update Domain Memory with this solution."

**Option 2: Manual Edit**
Edit `.ctxeco/domain-memory.md` directly, then commit to git. The file will be ingested on next sync.

### MCP Tools Available

- `read_domain_memory` - Read current Domain Memory
- `update_domain_memory` - Update Domain Memory with new knowledge
- `scan_commit_history` - Analyze git logs for decisions/patterns

## Examples

See `docs/research/domain-memory-implementation-example.md` for complete workflow examples.

## Learn More

- [Domain Memory Integration Design](../docs/research/domain-memory-integration.md)
- [Implementation Examples](../docs/research/domain-memory-implementation-example.md)
- [Implementation Plan](../docs/research/domain-memory-implementation-plan.md)
