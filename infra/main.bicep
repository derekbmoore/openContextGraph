@description('Location for all resources.')
param location string = resourceGroup().location

@description('Name of the environment (used for resource naming).')
param envName string = 'ctxEco-env'

@description('Environment type: staging, dev, test, uat, or prod.')
@allowed(['staging', 'dev', 'test', 'uat', 'prod'])
param environment string = 'staging'

var isProd = environment == 'prod'
@description('Enable authentication requirement for API endpoints.')
param authRequired bool = false  // Disabled for POC testing - enable for UAT/prod later

@description('Azure AD tenant ID for Entra External ID authentication.')
param azureAdTenantId string = ''

@description('Azure AD client ID for frontend app (from Entra External ID app registration).')
param azureAdClientId string = ''

@description('Whether using Entra External ID (CIAM) vs Workforce identity.')
param azureAdExternalId bool = false

@description('Entra External ID tenant domain (e.g., ctxEcoai for ctxEcoai.ciamlogin.com).')
param azureAdExternalDomain string = ''

@description('Enable Azure AD authentication for Postgres (recommended for uat/prod).')
param enablePostgresAad bool = false

@description('Object ID of the AAD admin for Postgres (user or group).')
param postgresAadAdminObjectId string = ''

@description('Tenant ID for AAD admin (defaults to current tenant).')
param postgresAadAdminTenantId string = tenant().tenantId

@description('Enable Private Link for Blob, Postgres, Key Vault (off for staging POC).')
param enablePrivateLink bool = false

@description('Postgres Admin Password')
@secure()
param postgresPassword string

// param adminObjectId string

@description('Container image for backend API.')
param backendImage string = 'ghcr.io/derekbmoore/opencontextgraph/backend:latest'

@description('Container image for worker.')
param workerImage string = 'ghcr.io/derekbmoore/opencontextgraph/worker:latest'

@description('Container image for Zep (memory).')
param zepImage string = 'ghcr.io/getzep/zep:latest'

@description('AKS node size (prod).')
param aksNodeSize string = 'Standard_D4s_v3'

@description('AKS node count (prod).')
param aksNodeCount int = 3

@description('AKS min node count (prod).')
param aksNodeMinCount int = 3

@description('AKS max node count (prod).')
param aksNodeMaxCount int = 10

@description('Enable private cluster for AKS (prod).')
param enableAksPrivateCluster bool = true
// param azureOpenAiKey removed
// param azureSpeechKey removed

@description('Azure AI Services APIM Gateway endpoint or direct Foundry endpoint.')
param azureAiEndpoint string = 'https://zimax-gw.azure-api.net/zimax'



@description('Azure AI Services project name.')
param azureAiProjectName string = ''

@description('Azure AI Model Router deployment name (recommended for intelligent routing).')
param azureAiModelRouter string = 'model-router'

@description('Azure AI Services API key for Foundry.')
@secure()
param azureAiKey string = ''

@description('Registry username.')
param registryUsername string

@description('Registry password.')
@secure()
param registryPassword string

@description('Zep API key (stored in Key Vault and used by backend/worker).')
@secure()
param zepApiKey string = ''

@description('Azure AI Foundry Agent Service endpoint.')
param azureFoundryAgentEndpoint string = ''

@description('Azure AI Foundry Agent Service project name.')
param azureFoundryAgentProject string = ''

@description('Azure AI Foundry Agent Service API key (optional, uses Managed Identity if not provided).')
@secure()
param azureFoundryAgentKey string = ''

@description('Elena Foundry Agent ID.')
param elenaFoundryAgentId string = ''

@description('Anthropic API Key.')
@secure()
param anthropicApiKey string = ''

@description('Gemini API Key.')
@secure()
param geminiApiKey string = ''

@description('GitHub Personal Access Token.')
@secure()
param githubToken string = ''

@description('Azure/Zimax VoiceLive API Key.')
@secure()
param voiceliveApiKey string = ''

@description('Endpoint for VoiceLive Service (Default: Zimax SaaS).')
param azureVoiceLiveEndpoint string = 'https://zimax.services.ai.azure.com'

@description('Azure Speech Service Key for Avatar.')
@secure()
param azureSpeechKey string = ''

@description('Azure Speech Service Region (e.g., westus2 for Avatar).')
param azureSpeechRegion string = 'westus2'



@description('Postgres SKU Name (e.g., Standard_B2ms, Standard_D4ds_v4).')
param postgresSku string = 'Standard_B2s'

@description('Postgres Storage Size in GB.')
param postgresStorageGB int = 32

@description('Postgres High Availability Mode (Disabled, ZoneRedundant).')
param postgresHighAvailability bool = false

// ...

var postgresTier = contains(postgresSku, '_B') ? 'Burstable' : (contains(postgresSku, '_E') ? 'MemoryOptimized' : 'GeneralPurpose')
var finalPostgresSku = {
  name: postgresSku
  tier: postgresTier
}

var postgresHaMode = postgresHighAvailability ? 'ZoneRedundant' : 'Disabled'

var enableAadForEnv = enablePostgresAad || environment == 'prod' || environment == 'uat'

// var postgresBackupDays = environment == 'prod' ? 35 : (environment == 'uat' ? 14 : 7)
// var postgresGeoRedundant = environment == 'prod' ? 'Enabled' : 'Disabled'



@description('Number of Postgres Read Replicas.')
param postgresReadReplicas int = 0

@description('Blob Storage Redundancy (Standard_LRS, Standard_GRS).')
param blobStorageRedundancy string = 'Standard_LRS'

@description('Log Analytics Retention Days.')
param logRetentionDays int = 30

@description('Enable Backup for Postgres.')
param enableBackup bool = true

@description('Backup Retention Days.')
param backupRetentionDays int = 7

@description('Number of Temporal History Shards.')
param temporalHistoryShards int = 512

@description('Deploy AKS Cluster (Prod only).')
param deployAks bool = false

@description('Enable Temporal Codec Server.')
param enableCodecServer bool = false

// Enhanced tagging schema for enterprise data-plane split
var baseTags = {
  Project: 'CtxEco'
  Environment: environment
  Component: ''  // Set per resource
  Plane: ''  // record (Blob) or recall (Zep/Postgres)
  Owner: 'zimax-ctxEco-team'
  CostCenter: 'ctxEco-platform'
  DataClass: 'internal'  // internal, confidential, restricted (set per resource)
}

@description('Tags to apply to all resources.')
param tags object = {}

// Merge base tags with overrides
var mergedTags = union(baseTags, tags)

// =============================================================================
// Log Analytics
// =============================================================================
var logAnalyticsTags = union(mergedTags, {
  Component: 'LogAnalytics'
  DataClass: 'internal'
})

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: '${envName}-logs'
  location: location
  tags: logAnalyticsTags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: logRetentionDays
  }
}

// =============================================================================
// Container Apps Environment
// =============================================================================
var acaEnvTags = union(mergedTags, {
  Component: 'ContainerAppsEnvironment'
  DataClass: 'internal'
})

resource acaEnv 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: '${envName}-aca'
  location: location
  tags: acaEnvTags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// =============================================================================
// AKS (Prod only)
// =============================================================================
module aksCluster 'modules/aks.bicep' = if (isProd && deployAks) {
  name: 'aksCluster'
  params: {
    location: location
    aksName: '${envName}-aks'
    dnsPrefix: '${envName}-aks'
    nodeSize: aksNodeSize
    nodeCount: aksNodeCount
    nodeMinCount: aksNodeMinCount
    nodeMaxCount: aksNodeMaxCount
    enablePrivateCluster: enableAksPrivateCluster
    enableAzurePolicy: true
    tags: union(mergedTags, { Component: 'AKS' })
  }
}

// =============================================================================
// PostgreSQL Flexible Server (Temporal + Zep storage)
// =============================================================================
var postgresTags = union(mergedTags, {
  Component: 'PostgreSQL'
  Plane: 'recall'  // System of recall (memory/knowledge graph)
  DataClass: 'internal'
})

// Postgres SKU selection based on environment


// var postgresBackupDays = environment == 'prod' ? 35 : (environment == 'uat' ? 14 : 7)
// var postgresGeoRedundant = environment == 'prod' ? 'Enabled' : 'Disabled'

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: '${envName}-db'
  location: location
  tags: postgresTags
  sku: finalPostgresSku
  properties: {
    administratorLogin: 'cogadmin'
    administratorLoginPassword: postgresPassword
    version: '16'  // Use PG16 for pgvector support
    storage: {
      storageSizeGB: postgresStorageGB
    }
    authConfig: {
      activeDirectoryAuth: enableAadForEnv ? 'Enabled' : 'Disabled'
      passwordAuth: 'Enabled'
      tenantId: postgresAadAdminTenantId
    }
    backup: {
      backupRetentionDays: backupRetentionDays
      geoRedundantBackup: 'Disabled' // Default to disabled, use redundancy param if needed
    }
    highAvailability: {
      mode: postgresHaMode
    }
  }

  resource allowAzureServices 'firewallRules' = {
    name: 'AllowAzureServices'
    properties: {
      startIpAddress: '0.0.0.0'
      endIpAddress: '0.0.0.0'
    }
  }

  // Enable required PostgreSQL extensions for Temporal and Zep
  resource azureExtensions 'configurations' = {
    name: 'azure.extensions'
    properties: {
      value: 'btree_gin,vector,pg_trgm,uuid-ossp'
      source: 'user-override'
    }
  }
}

resource postgresAadAdmin 'Microsoft.DBforPostgreSQL/flexibleServers/administrators@2022-12-01' = if (enableAadForEnv && !empty(postgresAadAdminObjectId)) {
  parent: postgres
  name: 'ActiveDirectory'
  properties: {
    principalName: 'aad-admin'
    principalType: 'User'
    tenantId: postgresAadAdminTenantId
  }
}

// =============================================================================
// Storage Account (System of Record - raw artifacts)
// =============================================================================
var storageTags = union(mergedTags, {
  Component: 'BlobStorage'
  Plane: 'record'  // System of record (raw docs, artifacts, provenance)
  DataClass: 'internal'
})

resource storage 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: replace('${envName}store', '-', '')
  location: location
  tags: storageTags
  kind: 'StorageV2'
  sku: {
    name: contains(blobStorageRedundancy, 'Standard_') ? blobStorageRedundancy : 'Standard_${blobStorageRedundancy}'
  }
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    networkAcls: {
      defaultAction: enablePrivateLink ? 'Deny' : 'Allow'  // Deny public access when Private Link enabled
      bypass: 'AzureServices'
    }
  }
}

// =============================================================================
// File Share for Persistence (Docs/Graph)
// =============================================================================
resource fileService 'Microsoft.Storage/storageAccounts/fileServices@2021-09-01' = {
  parent: storage
  name: 'default'
}

resource docsShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2021-09-01' = {
  parent: fileService
  name: 'docs'
  properties: {
    accessTier: 'TransactionOptimized'
    shareQuota: 5120
  }
}

// Link File Share to ACA Environment
resource acaDocsStorage 'Microsoft.App/managedEnvironments/storages@2022-03-01' = {
  parent: acaEnv
  name: '${toLower(envName)}-docs'
  properties: {
    azureFile: {
      accountName: storage.name
      accountKey: storage.listKeys().keys[0].value
      shareName: 'docs'
      accessMode: 'ReadWrite'
    }
  }
}

// RBAC: grant blob contributor to backend/worker identities
// RBAC: grant blob contributor to backend/worker identities
resource storageBlobContributorBackend 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, backendIdentity.name, 'blob-contrib-backend')
  scope: storage
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor
    principalId: backendIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource storageBlobContributorWorker 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, workerIdentity.name, 'blob-contrib-worker')
  scope: storage
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalId: workerIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// =============================================================================
// Managed Identities (User Assigned)
// =============================================================================
var identityTags = union(mergedTags, {
  Component: 'ManagedIdentity'
  DataClass: 'internal'
})

resource backendIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2018-11-30' = {
  name: '${envName}-backend-id'
  location: location
  tags: union(identityTags, { Component: 'ManagedIdentity-Backend' })
}

resource workerIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2018-11-30' = {
  name: '${envName}-worker-id'
  location: location
  tags: union(identityTags, { Component: 'ManagedIdentity-Worker' })
}

// =============================================================================
// Key Vault
// =============================================================================
module keyVaultModule 'modules/keyvault.bicep' = {
  name: 'keyVault'
  params: {
    location: location
    // Match manually created Key Vault name 'ctxecokv'
    keyVaultName: '${toLower(replace(envName, '-', ''))}kv'
    enableSoftDelete: true
    enablePurgeProtection: isProd || environment == 'uat'
    enablePrivateLink: enablePrivateLink
    tags: union(mergedTags, { Component: 'KeyVault', DataClass: 'confidential' })
  }
}

// Seed required secrets (postgres, zep, azure-ai, foundry)
module keyVaultSecrets 'modules/keyvault-secrets.bicep' = {
  name: 'keyVaultSecrets'
  params: {
    keyVaultName: keyVaultModule.outputs.keyVaultName
    postgresPassword: postgresPassword
    zepApiKey: zepApiKey
    azureAiKey: azureAiKey
    azureFoundryAgentEndpoint: azureFoundryAgentEndpoint
    azureFoundryAgentProject: azureFoundryAgentProject
    azureFoundryAgentKey: azureFoundryAgentKey
    elenaFoundryAgentId: elenaFoundryAgentId
    anthropicApiKey: anthropicApiKey
    geminiApiKey: geminiApiKey
    githubToken: githubToken
    voiceliveApiKey: voiceliveApiKey
    azureSpeechKey: azureSpeechKey
  }
}

// =============================================================================
// Role Assignments (Key Vault Access for Managed Identities)
// =============================================================================
// Key Vault Secrets User (4633458b-17de-408a-b874-0445c86b69e6)
var keyVaultSecretsUserRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')

module backendKvRole 'modules/role-assignment.bicep' = {
  name: 'backend-kv-role'
  params: {
    principalId: backendIdentity.properties.principalId
    roleDefinitionId: keyVaultSecretsUserRole
    nameSeed: 'backend-kv'
  }
}

module workerKvRole 'modules/role-assignment.bicep' = {
  name: 'worker-kv-role'
  params: {
    principalId: workerIdentity.properties.principalId
    roleDefinitionId: keyVaultSecretsUserRole
    nameSeed: 'worker-kv'
  }
}

// =============================================================================
// Temporal Container App
// =============================================================================
module temporalModule 'modules/temporal-aca.bicep' = {
  name: 'temporal'
  params: {
    location: location
    acaEnvId: acaEnv.id
    acaEnvName: acaEnv.name
    // Include environment in app name to avoid cross-environment collisions
    appName: '${envName}-temporal'
    enableCustomDomain: false
    postgresFqdn: postgres.properties.fullyQualifiedDomainName
    postgresUser: 'cogadmin'
    postgresPassword: postgresPassword
    postgresDb: 'temporal'
    tags: union(mergedTags, { Component: 'Temporal' })
  }
}

// =============================================================================
// Zep Self-hosted Deployment
// =============================================================================
// Create Zep database on Postgres
resource zepDb 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2021-06-01' = {
  parent: postgres
  name: 'zep'
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// Create Temporal database on Postgres
resource temporalDb 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2021-06-01' = {
  parent: postgres
  name: 'temporal'
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// Create Temporal visibility database on Postgres
resource temporalVisibilityDb 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2021-06-01' = {
  parent: postgres
  name: 'temporal_visibility'
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// Enable pgvector extension on Zep database
// Note: This requires azure.extensions parameter to include 'vector' in Postgres server config
// The extension is created via init script or manual setup after deployment

var zepTags = union(mergedTags, {
  Component: 'Zep'
  Plane: 'recall'  // System of recall (memory/knowledge graph)
  DataClass: 'internal'
})

module zepModule 'modules/zep-aca.bicep' = {
  name: 'zep'
  params: {
    location: location
    acaEnvId: acaEnv.id
    acaEnvName: acaEnv.name
    enableCustomDomain: true
    customDomainBindingType: 'SniEnabled' // Stage 2: Enable Cert
    customDomainName: 'zep.ctxeco.com'
    appName: '${envName}-zep'
    zepPostgresFqdn: postgres.properties.fullyQualifiedDomainName
    zepPostgresUser: 'cogadmin'
    zepPostgresPassword: postgresPassword
    zepPostgresDb: 'zep'
    zepApiKey: zepApiKey
    zepImage: zepImage
    registryServer: 'ghcr.io'
    registryUsername: registryUsername
    registryPassword: registryPassword
    azureAiKey: azureAiKey
    azureAiEndpoint: azureAiEndpoint
    tags: zepTags
  }
}

// Self-hosted Zep API URL (internal to ACA environment)
var zepApiUrl = zepModule.outputs.zepApiUrl

// =============================================================================
// Backend API Container App
// =============================================================================
module backendModule 'modules/backend-aca.bicep' = {
  name: 'backend'
  dependsOn: [
    acaDocsStorage
  ]
  params: {
    location: location
    docsStorageName: acaDocsStorage.name
    acaEnvName: acaEnv.name
    appName: '${envName}-api'
    enableCustomDomain: true
    customDomainBindingType: 'SniEnabled' // Stage 2: Enable Cert
    customDomainName: 'api.ctxeco.com'
    containerImage: backendImage
    postgresFqdn: postgres.properties.fullyQualifiedDomainName
    temporalHost: temporalModule.outputs.temporalHost

    zepApiUrl: zepApiUrl

    azureAiEndpoint: azureAiEndpoint
    azureAiProjectName: azureAiProjectName
    azureAiModelRouter: azureAiModelRouter
    azureVoiceLiveEndpoint: azureVoiceLiveEndpoint
    azureSpeechRegion: azureSpeechRegion
    registryUsername: registryUsername
    registryPassword: registryPassword
    keyVaultUri: keyVaultModule.outputs.keyVaultUri
    identityResourceId: backendIdentity.id
    identityClientId: backendIdentity.properties.clientId
    authRequired: authRequired
    azureAdTenantId: azureAdTenantId
    azureAdClientId: azureAdClientId
    azureAdExternalId: azureAdExternalId
    azureAdExternalDomain: azureAdExternalDomain
    tags: union(mergedTags, { Component: 'BackendAPI' })
  }
}

// var backendId = resourceId('Microsoft.App/containerApps', '${envName}-api')

// =============================================================================
// Worker Container App
// =============================================================================
module workerModule 'modules/worker-aca.bicep' = {
  name: 'worker'
  dependsOn: [
    acaDocsStorage
  ]
  params: {
    location: location
    docsStorageName: acaDocsStorage.name
    acaEnvId: acaEnv.id
    appName: '${envName}-worker'
    containerImage: workerImage
    postgresFqdn: postgres.properties.fullyQualifiedDomainName
    temporalHost: temporalModule.outputs.temporalHost

    zepApiUrl: zepApiUrl

    azureAiEndpoint: azureAiEndpoint
    azureAiProjectName: azureAiProjectName
    registryUsername: registryUsername
    registryPassword: registryPassword
    keyVaultUri: keyVaultModule.outputs.keyVaultUri
    identityResourceId: workerIdentity.id
    identityClientId: workerIdentity.properties.clientId
    tags: union(mergedTags, { Component: 'Worker' })
  }
}

// =============================================================================
// Static Web App
// =============================================================================
module swaModule 'static-webapp.bicep' = {
  name: 'staticWebApp'
  params: {
    location: location
    // Use the default SWA name so certificates remain bound to the intended environment
    swaName: '${envName}-web'
    enableCustomDomain: false
    backendResourceId: backendModule.outputs.backendId
  }
}

// =============================================================================
// DNS Records
// =============================================================================
// Note: Frontend uses apex domain (ctxEco.work) which is configured separately
// Deploy DNS records to the dns-rg resource group where the DNS zone exists
// module dnsModule 'modules/dns.bicep' = {
//   name: 'dns'
//   scope: resourceGroup('dns-rg')
//   params: {
//     dnsZoneName: 'ctxEco.work'
//     backendFqdn: backendModule.outputs.backendDefaultFqdn
//     temporalUIFqdn: temporalModule.outputs.temporalUIDefaultFqdn
//   }
// }

// =============================================================================
// Outputs
// =============================================================================
output acaEnvId string = acaEnv.id
output postgresFqdn string = postgres.properties.fullyQualifiedDomainName
output keyVaultUri string = keyVaultModule.outputs.keyVaultUri
output backendUrl string = backendModule.outputs.backendUrl
output swaDefaultHostname string = swaModule.outputs.swaDefaultHostname
output temporalUIFqdn string = temporalModule.outputs.temporalUIDefaultFqdn
output zepApiUrl string = zepApiUrl

output storageAccountName string = storage.name
// Output SWA Identity Principal ID for debugging/verification
output swaIdentityPrincipalId string = swaModule.outputs.swaIdentityPrincipalId

// Grant SWA Identity 'Reader' access to the Resource Group (or specific resources)
// Role: Reader (acdd72a7-3385-48ef-bd42-f606fba81ae7)
resource swaReaderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, 'swa-reader-role')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'acdd72a7-3385-48ef-bd42-f606fba81ae7')
    principalId: swaModule.outputs.swaIdentityPrincipalId
    principalType: 'ServicePrincipal'
  }
}


// =============================================================================
// Auth Fix (Post-SWA Linking)
// =============================================================================
// The SWA Linked Backend resource automatically enables "Easy Auth" and sets
// "RedirectToLoginPage" on the backend Container App. This breaks CORS for
// unauthenticated OPTIONS requests. We must reset it to "AllowAnonymous"
// AFTER the SWA module runs.
module authFixModule 'modules/auth-fix.bicep' = {
  name: 'authFix'
  dependsOn: [
    swaModule
  ]
  params: {
    containerAppName: '${envName}-api'
  }
}
