# Runbook: Stalwart Recovery (P2)

Procedures for recovering from Stalwart mail server failures.

## Symptoms

- Users unable to send/receive mail.
- Web UI returning connection timeout or 502/504 errors.
- SMTP/IMAP ports not responding.

## Recovery Steps

### 1. Check Service Status

```bash
docker compose -f infra/10-communication/mail/docker-compose.yml ps
```

### 2. Inspect Logs

Look for authentication failures, database errors, or certificate issues.

```bash
docker logs stalwart
```

### 3. Certificate Mismatch

If you see TLS errors, verify that the certificates in `../../../../secrets/certs` are valid and correctly mounted.

```bash
ls -l secrets/certs
```

### 4. Restart Service

If the process is hung or unresponsive to healthchecks:

```bash
docker compose -f infra/10-communication/mail/docker-compose.yml restart stalwart
```

## Escalation

- Check `infra_net` connectivity.
- Verify host disk space in `${DEFAULT_COMMUNICATION_DIR}`.
