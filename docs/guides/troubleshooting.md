---
title: 'Troubleshooting Guide'
layer: 'guides'
---

# Troubleshooting Guide

This guide covers common issues encountered when bootstrapping or operating the `hy-home.docker` stack.

## 1. Secrets & Authentication

### Placeholder secrets are still present

- **Symptom**: Integrations fail authentication; secret files contain `CHANGE_ME_*`.
- **Cause**: Bootstrap generated placeholders for manual values.
- **Fix**: Run `bash scripts/bootstrap-secrets.sh --env-file .env --strict` and replace placeholders in `secrets/`.

## 2. Infrastructure & Docker

### Certificate generation fails

- **Symptom**: `generate-local-certs.sh` exits with `mkcert is not installed`.
- **Fix**: Install `mkcert` and rerun the script.

### Compose validation fails

- **Symptom**: `bash scripts/validate-docker-compose.sh` returns interpolation errors.
- **Fix**: Check `.env` for missing values or invalid YAML in includes. Run `docker compose config` to debug.

### Preflight reports missing directories

- **Symptom**: Mount path errors in `preflight-compose.sh`.
- **Fix**: Ensure directories defined in `.env` exist. Default baseline:

  ```bash
  mkdir -p /home/hy/volumes/{auth,data,message_broker,obs}
  ```

### Host ports already in use

- **Symptom**: `port is already allocated` bind error.
- **Fix**: Update the conflicting `*_HOST_PORT` in `.env`.

## 3. Network

### Optional external networks missing

- **Symptom**: Warnings for `project_net` or `kind`.
- **Fix**: Create them manually if needed: `docker network create project_net`.
