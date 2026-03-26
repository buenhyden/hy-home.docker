<!-- [ID:09-tooling:terraform] -->
# Runbook: Terraform Recovery (P2)

> Procedures for resolving common Terraform execution errors and state lock issues.

## Symptoms

- "Error acquiring the state lock".
- "Error: Failed to load state: State data is corrupted".
- "Error: No valid credentials found".
- "Error: Error refreshing state: AccessDenied".

## Diagnostic Steps

### 1. Check Execution Context
Ensure you are running the command from the correct directory:
```bash
cd ${DEFAULT_TOOLING_DIR}/terraform
```

### 2. Verify Backend Access
If using a remote backend, verify that MinIO/S3 is up:
```bash
# Check MinIO status if applicable
cd ${DEFAULT_DATA_DIR}/minio
docker compose ps
```

## Recovery Procedures

### 1. Force Unlocking State

If a previous execution crashed and left the state locked:

1. Identify the **Lock ID** from the error message.
2. Run the force-unlock command:
   ```bash
   docker compose run --rm terraform force-unlock <LOCK_ID>
   ```

> [!CAUTION]
> Only force-unlock if you are 100% sure that no other person or process is currently modifying the infrastructure.

### 2. Handling Corrupted Local State

If the `.tfstate` file is unreadable:

1. Check for the `terraform.tfstate.backup` file.
2. If the backup exists and is valid, swap it:
   ```bash
   mv terraform.tfstate terraform.tfstate.corrupted
   cp terraform.tfstate.backup terraform.tfstate
   ```
3. Run `terraform plan` to verify consistency.

### 3. Resolving Provider Credential Failures

If credentials expired or are invalid:

1. Verify the host mounts in `docker-compose.yml` point to valid directories.
2. Refresh tokens on the host:
   ```bash
   # For AWS
   aws sso login --profile <your-profile>
   ```
3. Re-run `terraform init`.

## Escalation Policy

- **P1**: Corrupted remote state with no backup -> Notify Infrastructure Architect immediately.
- **P2**: Stuck state lock or transient network error -> Follow manual recovery steps.

## Related References

- **Infrastructure**: [Terraform Tool](../../../infra/09-tooling/terraform/README.md)
- **Guide**: [Terraform System Guide](../../07.guides/09-tooling/terraform.md)
- **Operation**: [IaC Operations Policy](../../08.operations/09-tooling/terraform.md)
