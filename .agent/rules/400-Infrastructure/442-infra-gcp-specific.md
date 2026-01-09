---
trigger: always_on
glob: "**/*"
description: "GCP: IaC, Service Accounts, Cloud Run, and Firestore Best Practices."
---
# Google Cloud Platform (GCP) Standards

## 1. Infrastructure as Code (IaC)

- **Terraform**: Use Terraform for ALL resource provisioning.
- **State**: Store state in remote buckets (GCS) with locking (DynamoDB/GCS).
- **Service Accounts**: Never create resources via Console manually.

## 2. Serverless (Cloud Run / Functions)

- **Idempotency**: Functions must be safe to retry.
- **Cold Starts**: Use global scope for initialization (DB connections, secrets).
- **Billing**: Use instance-based billing if doing background work after response.

### Example: Cold Start

**Good**

```python
# Initialized once per instance
db_client = firestore.Client()
secret = access_secret_version("my-secret")

def handler(request):
    # Reuses client and secret
    return db_client.collection("users").add(...)
```

**Bad**

```python
def handler(request):
    # Connection created on EVERY request - slow and expensive
    db_client = firestore.Client() 
    ...
```

## 3. Security

- **Service Accounts**: Create dedicated SAs with least privilege.
- **No Keys**: Avoid downloading JSON keys. Use Workload Identity Federation.
- **Secrets**: Use Secret Manager. Never env vars for secrets.

## 4. Firestore

- **No Sequential IDs**: Avoid `item1`, `item2`. Use UUIDs or auto-ID.
- **Indexing**: Exempt fields that cause write hotspots or high costs.
- **Pagination**: Use cursors (`start_after`), NOT `offset`.

### Example: Pagination

**Good**

```python
query = db.collection('items').order_by('created').start_after(last_doc).limit(20)
```

**Bad**

```python
query = db.collection('items').offset(1000).limit(20) # Bills 1020 reads!
```
