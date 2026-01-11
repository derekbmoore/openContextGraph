# Infrastructure

## Azure → On-Prem Mapping

| Azure | On-Prem |
|-------|---------|
| Container Apps | Kubernetes |
| PostgreSQL Flex | PostgreSQL |
| Key Vault | HashiCorp Vault |
| Azure Speech | Whisper + Piper |
| Azure OpenAI | vLLM / Ollama |

## Modules

See: `infra/k8s/`, `infra/helm/`

## TODO

- [ ] Create Helm charts
- [ ] Document air-gapped deployment
