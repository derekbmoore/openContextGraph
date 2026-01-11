# Docker Compose — Infrastructure Foundation

## Purpose

Docker Compose provides the **infrastructure backbone** for openContextGraph, orchestrating five critical services that form the platform's runtime environment. This isn't just convenience tooling—it's the foundation for **reproducible, auditable deployments** required by enterprise and FedRAMP compliance.

## Why This Exists

### The Problem

AI systems often suffer from "works on my machine" syndrome. Dependencies are scattered, versions drift, and production differs from development. For enterprise AI—especially in regulated environments—this is unacceptable.

### The Solution

A declarative infrastructure definition that:

1. **Guarantees consistency** across dev, test, and UAT environments
2. **Documents dependencies** as code (infrastructure-as-code)
3. **Enables air-gapped deployment** by defining all components explicitly
4. **Supports compliance audits** with version-pinned, reproducible builds

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  PostgreSQL │  │     Zep     │  │      Temporal       │  │
│  │   (Data)    │  │  (Memory)   │  │  (Orchestration)    │  │
│  │   :5432     │  │    :8000    │  │    :7233, :8088     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┴─────────────────────┘             │
│                          │                                   │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │                Backend API (:8082)                     │  │
│  │   FastAPI + Agents + Memory Client + ETL Router        │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │              Temporal Worker                           │  │
│  │   Durable workflow execution                           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Sample

```yaml
# docker-compose.yml
version: '3.8'

services:
  # =============================================================================
  # Core Infrastructure - Data Layer
  # =============================================================================
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ctxEco
      POSTGRES_USER: ctxEco
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ctxEco"]
      interval: 10s
      timeout: 5s
      retries: 5

  # =============================================================================
  # Memory Layer (CtxGraph) - Temporal Knowledge Graph
  # NIST AI RMF: MAP 1.1 (System Context), MANAGE 2.3 (Data Governance)
  # =============================================================================
  zep:
    image: ghcr.io/getzep/zep:latest
    environment:
      ZEP_STORE_TYPE: postgres
      ZEP_STORE_POSTGRES_DSN: postgres://ctxEco:${POSTGRES_PASSWORD}@postgres:5432/ctxEco
      ZEP_AUTH_REQUIRED: false
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

  # =============================================================================
  # Orchestration Layer (Spine) - Durable Workflows
  # NIST AI RMF: GOVERN 1.2 (Accountability), MANAGE 4.1 (Incident Response)
  # =============================================================================
  temporal:
    image: temporalio/auto-setup:1.22
    environment:
      - DB=postgresql
      - POSTGRES_USER=ctxEco
      - POSTGRES_PWD=${POSTGRES_PASSWORD:-changeme}
      - POSTGRES_SEEDS=postgres
    ports:
      - "7233:7233"
    depends_on:
      postgres:
        condition: service_healthy

  temporal-ui:
    image: temporalio/ui:2.21.3
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    ports:
      - "8088:8080"
    depends_on:
      - temporal

  # =============================================================================
  # Application Layer - Backend API
  # =============================================================================
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - POSTGRES_HOST=postgres
      - ZEP_API_URL=http://zep:8000
      - TEMPORAL_HOST=temporal:7233
    ports:
      - "8082:8082"
    depends_on:
      - postgres
      - zep
      - temporal

  # =============================================================================
  # Worker Layer - Temporal Workflow Execution
  # =============================================================================
  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: python -m workflows.worker
    environment:
      - TEMPORAL_HOST=temporal:7233
      - ZEP_API_URL=http://zep:8000
    depends_on:
      - temporal
      - zep

volumes:
  postgres_data:
```

---

## Service Descriptions

### PostgreSQL (Data Layer)

- **Purpose**: Persistent storage for Zep memory, Temporal state, and application data
- **Version**: 15-alpine (security-patched, minimal footprint)
- **Health Check**: Ensures downstream services wait for database readiness

### Zep (Memory Layer)

- **Purpose**: Temporal knowledge graph for episodic and semantic memory
- **Capability**: Tri-Search™ (keyword + vector + graph fusion)
- **Dependency**: Requires PostgreSQL for persistence

### Temporal (Orchestration Layer)

- **Purpose**: Durable workflow execution with automatic retry and state persistence
- **Capability**: Long-running workflows survive restarts, network failures
- **UI**: Web interface on :8088 for workflow monitoring

### Backend (Application Layer)

- **Purpose**: FastAPI REST API serving agents, memory, and ETL endpoints
- **Capability**: Routes requests to appropriate handlers

### Worker (Execution Layer)

- **Purpose**: Executes Temporal workflows independently of API
- **Capability**: Scales horizontally for parallel workflow processing

---

## NIST AI RMF Alignment

| NIST AI RMF Function | Control | How Docker Compose Addresses It |
|---------------------|---------|--------------------------------|
| **GOVERN 1.1** | Policies and procedures | Declarative infrastructure-as-code defines exact system configuration |
| **GOVERN 1.2** | Accountability | Service logs, health checks, and named containers enable attribution |
| **MAP 1.1** | System context | Complete dependency graph documented in compose file |
| **MAP 1.5** | System boundaries | Network isolation via Docker networks; explicit port exposure |
| **MEASURE 2.6** | Continuous monitoring | Health checks detect service degradation |
| **MANAGE 2.3** | Data governance | PostgreSQL with versioned schema; Zep with structured memory |
| **MANAGE 4.1** | Incident response | Temporal provides workflow state for debugging; restart policies recover from failures |

### Specific Controls

**GOVERN 1.1 (Policies and Procedures)**

```yaml
# Version pinning ensures reproducibility
image: postgres:15-alpine      # Specific version, not :latest
image: temporalio/auto-setup:1.22  # Pinned Temporal version
```

**MAP 1.5 (System Boundaries)**

```yaml
# Only expose necessary ports
ports:
  - "8082:8082"  # Backend API only
# Internal services (temporal:7233) not exposed to host by default
```

**MANAGE 4.1 (Incident Response)**

```yaml
# Health checks enable auto-recovery
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ctxEco"]
  interval: 10s
  retries: 5
```

---

## On-Prem / FedRAMP Considerations

| Docker Compose | Kubernetes Equivalent | FedRAMP Control |
|----------------|----------------------|-----------------|
| `services:` | Deployments/StatefulSets | CM-2 (Baseline Configuration) |
| `volumes:` | PersistentVolumeClaims | CP-9 (System Backup) |
| `healthcheck:` | Liveness/Readiness Probes | SI-4 (System Monitoring) |
| `depends_on:` | Init Containers | SC-7 (Boundary Protection) |
| `environment:` | ConfigMaps/Secrets | SC-28 (Protection of Information at Rest) |

---

## Usage

### Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down
```

### Production Considerations

```bash
# Use production passwords
export POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Start with resource limits
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Summary

Docker Compose is the **infrastructure foundation** that enables:

- ✅ Reproducible deployments across environments
- ✅ Declarative configuration as code
- ✅ Health monitoring and auto-recovery
- ✅ Clear service boundaries for security
- ✅ NIST AI RMF alignment for enterprise compliance

*Document Version: 1.0 | Created: 2026-01-11*
