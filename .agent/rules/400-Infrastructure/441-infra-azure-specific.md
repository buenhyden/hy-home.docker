---
trigger: always_on
glob: "**/*.bicep,**/*.tf"
description: "Azure: Bicep/Terraform, Managed Identity, and Naming."
---
# Azure Standards

## 1. Identity & Access

- **Managed Identity**: Use System/User Assigned Managed Identity for Service-to-Service auth.
- **Keys**: No Storage Account Keys or Service Principal Secrets in code.

### Example: Auth

**Good**

```bicep
resource appService 'Microsoft.Web/sites@2021-02-01' = {
  identity: { type: 'SystemAssigned' }
}
```

**Bad**

```json
"connectionString": "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=..."
```

## 2. Naming Convention

- **Consistency**: `[Resource]-[App]-[Env]-[Region]`.
- **Lowercase**: Azure resources are often case-insensitive but DNS is lowercase.

### Example: Naming

**Good**

```text
st-myapp-prod-eus
```

**Bad**

```text
MyStorageAccount123
```
