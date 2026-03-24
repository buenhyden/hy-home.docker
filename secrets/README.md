# 🔐 Secrets Management

> Centralized repository for all sensitive environment variables and Docker secrets.

## Overview

**KR**: `hy-home.docker` 인프라에서 사용하는 모든 민감 정보(비밀번호, 키, 토큰)를 Docker Secrets 포맷(`.txt`)으로 관리하는 저장소입니다. 중앙 집중형 레지스트리와 자동화 스크립트를 통해 보안과 일관성을 유지합니다.
**EN**: Centralized repository for managing all sensitive information (passwords, keys, tokens) used in the `hy-home.docker` infrastructure in Docker Secrets format (`.txt`). It maintains security and consistency through a centralized registry and automation scripts.

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Registry** | `SENSITIVE_ENV_VARS.md` | Source of truth for all secrets mapping and metadata |
| **Auth** | `auth/` | Credentials for Traefik, Keycloak, and proxies |
| **Automation** | `automation/` | Keys and passwords for Airflow, n8n, etc. |
| **Certs** | `certs/` | Local TLS certificates (managed by mkcert) |
| **Common** | `common/` | Shared credentials like SMTP and Slack webhooks |
| **Data** | `data/` | Secrets for OpenSearch, Supabase, and AI tools |
| **DB** | `db/` | Database-specific passwords (Postgres, Valkey, NoSQL) |
| **Observability**| `observability/` | Credentials for Grafana and monitoring tools |
| **Storage** | `storage/` | MinIO root and application credentials |
| **Tools** | `tools/` | Internal secrets for SonarQube, Syncthing, etc. |

---

## 🏛️ Secret Management System

### 1. Registry (Source of Truth)

- **[SENSITIVE_ENV_VARS.md](SENSITIVE_ENV_VARS.md)**: Master list of all secrets.
- Tracks automation status, file paths, corresponding `.env` variables, and modification dates.
- For new environments, refer to **[SENSITIVE_ENV_VARS.md.example](SENSITIVE_ENV_VARS.md.example)**.

### 2. Automation Script

- **`gen-secrets.sh`**: Automatically generates password files based on the registry.
- **Key Features**:
  - Secure random password generation (16 characters).
  - `htpasswd` generation for Traefik/OpenSearch.
  - Real-time registry synchronization.

---

## ⚙️ Infrastructure / Component Details

### Standard Service Secrets (Samples)

| Service | Category | Docker Secret File | Purpose |
| :--- | :--- | :--- | :--- |
| `traefik` | Auth | `auth/traefik_admin_password.txt` | Dashboard Access |
| `keycloak` | Auth | `auth/keycloak_admin_password.txt` | IAM Admin Password |
| `postgres` | DB | `db/postgres/mng_password.txt` | Management DB Root |
| `airflow` | Automation | `automation/airflow_fernet_key.txt` | Data Encryption |
| `minio` | Storage | `storage/minio_root_password.txt` | S3 Storage Root |
| `supabase` | Data | `data/supabase_jwt_secret.txt` | JWT Signing Secret |

### Operational Commands

```bash
# Generate/Sync all missing secrets
./scripts/gen-secrets.sh

# Force regenerate all secrets (creates .bak files)
./scripts/gen-secrets.sh --force

# Update a specific secret manually
echo "new_password" > secrets/db/postgres/mng_password.txt
docker compose restart mng-postgres
```

---

## 🛡️ Security Policy

- **Git Exclusion**: All `.txt` files are ignored by Git via `.gitignore`.
- **Encryption at Rest**: Ensure the host filesystem is encrypted. Docker Secrets are mounted as in-memory files (tmpfs) within containers.
- **Backup**: `gen-secrets.sh` creates `.bak` copies before overwriting existing secrets.

---

## Extensibility & References

- [🤖 Agent Governance](/AGENTS.md)
- [🏛️ System Architecture](/ARCHITECTURE.md)
- [⚙️ Operations](/OPERATION.md)
- [📜 Secrets Registry](SENSITIVE_ENV_VARS.md)

---
*Maintained by Senior DevOps & Security Team*
