targetScope = 'resourceGroup'
param location string = resourceGroup().location
param suffix string = uniqueString(resourceGroup().id)
param tags object = { workload: 'm-and-a-technology-integration-factory', evidence: 'deployment-contract' }

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-newco-${suffix}'
  location: location
  tags: tags
  properties: {
    addressSpace: { addressPrefixes: ['10.70.0.0/16'] }
    subnets: [
      { name: 'shared-services', properties: { addressPrefix: '10.70.1.0/24' } }
      { name: 'migration', properties: { addressPrefix: '10.70.2.0/24' } }
    ]
  }
}

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'law-newco-${suffix}'
  location: location
  tags: tags
  properties: { retentionInDays: 30 }
}

resource vault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-newco-${suffix}'
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: { family: 'A', name: 'standard' }
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    publicNetworkAccess: 'Enabled'
  }
}

output vnetId string = vnet.id
output workspaceId string = logs.id
output keyVaultId string = vault.id

