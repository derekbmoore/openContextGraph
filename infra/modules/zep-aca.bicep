@description('Location for all resources.')
param location string = resourceGroup().location

@description('ID of the Container Apps Environment.')
param acaEnvId string

@description('Name of the Container Apps Environment (for certificate parenting).')
param acaEnvName string

@description('Whether to enable custom domain with managed certificate.')
param enableCustomDomain bool = false

@description('Custom domain name for Zep.')
param customDomainName string = 'zep.ctxEco.work'

@description('Binding type: Disabled (HTTP only) or SniEnabled (HTTPS with Cert).')
param customDomainBindingType string = 'SniEnabled'

@description('Name of the Zep container app.')
param appName string = 'zep'

@description('PostgreSQL FQDN for Zep storage.')
param zepPostgresFqdn string

@description('PostgreSQL admin user for Zep.')
param zepPostgresUser string = 'cogadmin'

@description('PostgreSQL admin password for Zep.')
@secure()
param zepPostgresPassword string

@description('PostgreSQL database name for Zep.')
param zepPostgresDb string = 'zep'

@description('Key Vault URI (e.g. https://myvault.vault.azure.net/). When set with identityResourceId, Zep reads Postgres DSN from secret zep-postgres-dsn and picks up password changes after restart.')
param keyVaultUri string = ''

@description('User-assigned identity resource ID for Key Vault access (required if keyVaultUri is set).')
param identityResourceId string = ''

@description('User-assigned identity client ID (for reference).')
param identityClientId string = ''

@description('Zep API key (optional, for authentication).')
@secure()
param zepApiKey string = ''

@description('Container image for Zep.')
param zepImage string = 'ghcr.io/getzep/zep:latest'

@description('Container registry server for Zep image.')
param registryServer string = 'ghcr.io'

@description('Registry username (optional, if image is private).')
param registryUsername string = ''

@description('Registry password (optional, if image is private).')
@secure()
param registryPassword string = ''

@description('Azure AI Services API key.')
@secure()
param azureAiKey string

@description('Azure AI Services Endpoint.')
param azureAiEndpoint string

@description('Azure OpenAI LLM deployment name.')
param azureOpenAiLlmDeployment string = 'gpt-5-chat'

@description('Azure OpenAI Embedding deployment name.')
param azureOpenAiEmbeddingDeployment string = 'text-embedding-ada-002'

// Zep API Key Secret (only if provided)
var zepSecret = empty(zepApiKey) ? [] : [
  {
    name: 'zep-api-key'
    value: zepApiKey
  }
]

// Azure AI Key Secret (only if provided)
var azureAiSecret = empty(azureAiKey) ? [] : [
  {
    name: 'azure-ai-key'
    value: azureAiKey
  }
]

var zepApiEnv = empty(zepApiKey) ? [] : [
  {
    name: 'ZEP_API_KEY'
    secretRef: 'zep-api-key'
  }
]

var zepRegistrySecret = empty(registryUsername) ? [] : [
  {
    name: 'zep-registry-password'
    value: registryPassword
  }
]

var zepRegistries = empty(registryUsername) ? [] : [
  {
    server: registryServer
    username: registryUsername
    passwordSecretRef: 'zep-registry-password'
  }
]

@description('Tags to apply to all resources.')
param tags object = {
  Project: 'CtxEco'
  Component: 'Zep'
}

// When Key Vault is used, DSN comes only from KV (env ZEP_STORE_POSTGRES_DSN). Config file must not set store.postgres.dsn so env wins.
var useKvForDsn = !empty(keyVaultUri) && !empty(identityResourceId)
var zepDsn = 'postgresql://${zepPostgresUser}:${zepPostgresPassword}@${zepPostgresFqdn}:5432/${zepPostgresDb}?sslmode=require'
// KV path: no dsn in config — Zep uses ZEP_STORE_POSTGRES_DSN from Key Vault ref. Inline path: dsn in config for single-source simplicity.
var llmServerBlock = 'llm:\n  service: openai\n  azure_openai_endpoint: ${azureAiEndpoint}\n  azure_openai:\n    llm_deployment: ${azureOpenAiLlmDeployment}\n    embedding_deployment: ${azureOpenAiEmbeddingDeployment}\nserver:\n  host: 0.0.0.0\n  port: 8000\n  web_enabled: false\nlog:\n  level: debug\nauth:\n  required: false\n'
var zepConfigContent = useKvForDsn ? 'store:\n  type: postgres\n${llmServerBlock}' : 'store:\n  type: postgres\n  postgres:\n    dsn: "${zepDsn}"\n${llmServerBlock}'

// Get reference to existing ACA environment for parenting the cert
resource acaEnv 'Microsoft.App/managedEnvironments@2022-03-01' existing = {
  name: acaEnvName
}

// Create Managed Certificate for Custom Domain (Only if SniEnabled)
resource certificate 'Microsoft.App/managedEnvironments/managedCertificates@2024-03-01' = if (enableCustomDomain && customDomainBindingType == 'SniEnabled') {
  parent: acaEnv
  name: '${appName}-cert'
  location: location
  properties: {
    subjectName: customDomainName
    domainControlValidation: 'CNAME'
  }
}

// Key Vault secret ref and env so Zep reads DSN from KV at runtime (no baked password in config when useKvForDsn).
var kvDsnSecret = useKvForDsn ? [
  {
    name: 'zep-postgres-dsn'
    keyVaultUrl: '${keyVaultUri}secrets/zep-postgres-dsn'
    identity: identityResourceId
  }
] : []
var kvDsnEnv = useKvForDsn ? [
  { name: 'ZEP_STORE_TYPE'
    value: 'postgres' }
  { name: 'ZEP_STORE_POSTGRES_DSN'
    secretRef: 'zep-postgres-dsn' }
] : []

// Zep Container App
resource zepApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: appName
  location: location
  tags: tags
  identity: useKvForDsn ? {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identityResourceId}': {}
    }
  } : null
  properties: {
    managedEnvironmentId: acaEnvId
    configuration: {
      ingress: {
        external: true  // Now public for MCP client access via zep.ctxEco.work
        targetPort: 8000
        transport: 'http'
        allowInsecure: false
        customDomains: enableCustomDomain ? [
          {
            name: customDomainName
            certificateId: customDomainBindingType == 'SniEnabled' ? certificate.id : null
            bindingType: customDomainBindingType
          }
        ] : []
      }
      dapr: {
        enabled: false
      }
      secrets: concat([
        {
          name: 'zep-postgres-password'
          value: zepPostgresPassword
        }
        {
          name: 'zep-config-yaml'
          value: zepConfigContent
        }
      ], kvDsnSecret, zepSecret, azureAiSecret, zepRegistrySecret)
      registries: zepRegistries
    }
    template: {
      volumes: [
        {
          name: 'zep-config-volume'
          storageType: 'Secret'
          secrets: [
            {
              secretRef: 'zep-config-yaml'
              path: 'config.yaml'
            }
          ]
        }
      ]
      containers: [
        {
          name: 'zep'
          image: zepImage
          command: ['/app/zep']
          args: ['--config', '/config/config.yaml']
          volumeMounts: [
            {
              volumeName: 'zep-config-volume'
              mountPath: '/config'
            }
          ]
          env: concat([
            {
              name: 'ZEP_OPENAI_API_KEY'
              secretRef: 'azure-ai-key'
            }
          ], kvDsnEnv, zepApiEnv)
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          probes: [
            {
              type: 'Startup'
              httpGet: {
                port: 8000
                path: '/healthz'
              }
              initialDelaySeconds: 60   // KV + Postgres can be slow on cold start
              periodSeconds: 10
              failureThreshold: 36     // 60 + (36 * 10) = 420s total startup window
            }
            {
              type: 'Readiness'
              httpGet: {
                port: 8000
                path: '/healthz'
              }
              initialDelaySeconds: 10
              periodSeconds: 10
              failureThreshold: 6
            }
            {
              type: 'Liveness'
              httpGet: {
                port: 8000
                path: '/healthz'
              }
              initialDelaySeconds: 60
              periodSeconds: 30
              failureThreshold: 5
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1  // Scale-to-zero disabled for POC verification (Warm Start)
        maxReplicas: 2
        rules: [
          {
            name: 'http-scale'
            http: {
              metadata: {
                concurrentRequests: '10'
                cooldownPeriod: '1800'  // 30 minutes before scaling down
              }
            }
          }
        ]
      }
    }
  }
}

// Outputs
// For external ingress with custom domain, use HTTPS custom domain
// For internal/default, use internal FQDN with port 8000
output zepFqdn string = zepApp.properties.configuration.ingress.fqdn
output zepApiUrl string = enableCustomDomain ? 'https://${customDomainName}' : 'https://${zepApp.properties.configuration.ingress.fqdn}'
