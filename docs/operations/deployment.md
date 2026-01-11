# Deployment Guide

## Local Development

```bash
docker-compose up -d
cd backend && uvicorn api.main:app --reload
cd frontend && npm run dev
```

## On-Prem (Kubernetes)

```bash
helm install ctxEco ./infra/helm/ctxEco
```

## Prerequisites

- PostgreSQL 15+
- Kubernetes 1.28+
- 16GB RAM minimum

## TODO

- [ ] Add production hardening steps
- [ ] Document backup/restore
- [ ] Add rollback procedures
