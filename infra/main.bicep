// Main Bicep file for Student Advisor Chatbot with Azure AI Services
targetScope = 'resourceGroup'

@description('Azure region for deployment')
param location string = resourceGroup().location

@description('Base name for all resources')
param baseName string = 'studentadvisor'

@description('Environment name (dev, test, prod)')
param environment string = 'dev'

@description('The name of the OpenAI model to deploy')
param modelName string = 'gpt-4.1'

@description('The model format')
param modelFormat string = 'OpenAI'

@description('The version of the model')
param modelVersion string = '2025-04-14'

@description('The SKU name for the model deployment')
param modelSkuName string = 'GlobalStandard'

@description('The capacity of the model deployment in TPM')
param modelCapacity int = 40

@description('Deployment timestamp for unique suffix generation')
param deploymentTimestamp string = utcNow('yyyyMMddHHmmss')

// Variables
var uniqueSuffix = substring(uniqueString('${resourceGroup().id}-${deploymentTimestamp}'), 0, 4)
var aiServicesName = toLower('${baseName}${uniqueSuffix}')
var projectName = 'project'
var storageAccountName = 'st${take(uniqueSuffix, 18)}'
var keyVaultName = 'kv${take(uniqueSuffix, 10)}'
var appInsightsName = '${baseName}-ai-${environment}-${uniqueSuffix}'
var logAnalyticsName = '${baseName}-la-${environment}-${uniqueSuffix}'

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// Storage Account
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
  }
}

// Azure AI Services Account
resource aiAccount 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: aiServicesName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: toLower(aiServicesName)
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: true
  }
}

// Diagnostic Settings for AI Services (connects to Application Insights)
resource aiDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'AppInsightsDiagnostics'
  scope: aiAccount
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        category: 'Audit'
        enabled: true
      }
      {
        category: 'RequestResponse'
        enabled: true
      }
      {
        category: 'Trace'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// Azure AI Project (child resource of AI Services)
resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: aiAccount
  name: projectName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: 'Student Advisor Chatbot Project'
    displayName: 'Student Advisor'
  }
}

// Model Deployment
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: aiAccount
  name: modelName
  sku: {
    capacity: modelCapacity
    name: modelSkuName
  }
  properties: {
    model: {
      name: modelName
      format: modelFormat
      version: modelVersion
    }
  }
}

// Outputs
output accountName string = aiAccount.name
output projectName string = aiProject.name
output accountEndpoint string = aiAccount.properties.endpoint
output resourceGroupName string = resourceGroup().name
output location string = location
output appInsightsName string = appInsights.name
output appInsightsConnectionString string = appInsights.properties.ConnectionString
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output logAnalyticsWorkspaceId string = logAnalytics.id
