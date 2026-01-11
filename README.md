# OpenContextGraph (ctxEco)

> **Enterprise AI Context Orchestration Platform**

OpenContextGraph solves the **Memory Wall Problem** in Large Language Models through innovative context engineering. Built on the **Brain + Spine + CtxGraph** architecture pattern.

## Quick Start

### Local Development

1. **Configure environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start services**:

   ```bash
   docker-compose up -d
   ```

3. **Install dependencies**:

   ```bash
   # Backend
   cd backend && pip install -r requirements.txt
   
   # Frontend
   cd frontend && npm install
   ```

4. **Run development servers**:

   ```bash
   # From root
   docker-compose up -d  # Infrastructure
   cd backend && uvicorn api.main:app --reload --port 8082
   cd frontend && npm run dev
   ```

5. **Open browser**: `http://localhost:5173`

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   Backend (FastAPI)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Agents    │  │     ETL     │  │      Voice      │  │
│  │  (Brain)    │  │ (Antigrav.) │  │   (WebRTC)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Orchestration (Temporal - Spine)            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│          Memory (Zep + Graphiti - CtxGraph)             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Episodic   │  │  Semantic   │  │  Graph Search   │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Key Features

- 🧠 **4-Layer Security Context** — Identity, Episodic, Semantic, Operational
- 🔍 **Tri-Search™** — Keyword + Vector + Graph fusion with RRF
- 📄 **Antigravity Router** — Class A/B/C document ingestion by truth value
- 🦴 **Durable Workflows** — Temporal-based orchestration
- 💾 **CtxGraph** — Temporal knowledge graph (Zep + Graphiti)
- 🎤 **Voice & Avatar** — WebRTC-based voice interaction

## Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [Security Model](docs/security/4-layer-context.md)
- [Deployment Guide](docs/operations/deployment.md)

## License

MIT License — See [LICENSE](LICENSE)

---

*OpenContextGraph — Defying data gravity since 2026*
