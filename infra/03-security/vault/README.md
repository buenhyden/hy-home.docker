# Vault Secret Management

> Identity-based secrets management and encryption-as-a-service for `hy-home.docker`.

## Overview

HashiCorp Vault는 `hy-home.docker` 플랫폼의 중앙 비밀 관리 엔진이다. 모든 인프라 계층(Gateway, Auth, Data, App)에서 사용하는 API 키, 데이터베이스 자격 증명, 인증서 등을 안전하게 보관하고 수명 주기(Lifecycle)를 관리한다. 현재 구현은 단일 노드 Raft 통합 스토리지와 Vault Agent 서비스로 구성되며, 향후 HA 확장을 위한 전환 절차는 정책/런북에서 관리한다.

## Audience

이 README의 주요 독자:

- **SRE / DevOps**: 클러스터 구성, 백업(Snapshot), 버전 업그레이드 담당
- **Security Engineers**: ACL 정책 설계 및 인증 방식(Keycloak OIDC, AppRole) 관리
- **AI Agents**: 자동화된 봉인 해제(Unseal) 감지 및 비밀 렌더링 검증 수행

## Scope

### In Scope

- **Server Configuration**: `vault.hcl`을 통한 Raft 스토리지 및 리스너 설정
- **Agent Configuration**: `vault-agent.hcl`을 통한 자동 인증(Auto-auth) 및 템플릿 처리
- **Healthcheck Protocol**: `wget` 기반의 정밀 상태 점검 로직
- **Connectivity**: Traefik L7 라우팅 및 내부망(`infra_net`) 통신 구성

### Out of Scope

- 하위 네트워크(VLAN/Subnet) 방화벽 및 커널 보안 설정
- 개별 애플리케이션의 비즈니스 로직 및 비밀 데이터의 내용물 생성
- HSM(Hardware Security Module) 연동 (SW 기반 봉인 관리 사용)

## Structure

```text
vault/
├── config/             # Vault & Agent configuration files
│   ├── templates/      # Secret rendering templates (.ctmpl)
│   ├── vault.hcl       # Server configuration (Raft, Listener)
│   └── vault-agent.hcl # Agent configuration (AppRole, Templating)
├── docker-compose.yml  # Container orchestration & Healthcheck
└── README.md           # This file
```

## Tech Stack

| Category    | Technology      | Notes                  |
| ----------- | --------------- | ---------------------- |
| Platform    | Vault (Go)      | `hashicorp/vault:2.0.3` |
| Persistence | Raft            | Single-node integrated storage |
| Sidecar     | Vault Agent     | Auto-auth & Templating |
| Runtime     | Official container image | Root compose profile service |

## Implementation Details

### Healthcheck Protocol

Vault의 헬스체크는 봉인(Sealed) 상태나 초기화되지 않은 상태에서도 클러스터 준비도를 판단할 수 있도록 파라미터를 조정함:

```yaml
healthcheck:
  test: ["CMD-SHELL", 'wget -q -O- "http://127.0.0.1:8200/v1/sys/health?standbyok=true&sealedcode=200&uninitcode=200" >/dev/null 2>&1 || exit 1']
```

### Configuration Highlights

- **Storage**: Raft 스토리지를 `/vault/data`에 마운트하여 데이터 지속성 보장.
- **Listener**: 내부/infra_net에서는 `tls_disable = 1`로 설정하여 성능을 높이고, 외부 접근은 Traefik이 TLS를 종료함.

## Testing

```bash
# Validate the root security profile and 03-security hardening contract
HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 03-security

# Runtime-only checks after the security profile is already running
docker compose --profile security exec vault vault operator raft list-peers
docker compose --profile security exec vault vault status
docker compose --profile security exec vault-agent ls -la /vault/out
```

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. **Sealed Status Check**: 모든 API 작업 전 `vault status`를 통해 `Sealed: false`임을 확인한다.
2. **Template Path Verification**: `.ctmpl` 파일 수정 시 `vault-agent.hcl`의 `template` 섹션과 경로가 일치하는지 확인한다.
3. **AppRole ID Access**: 자동화 작업 시 `/vault/agent/role_id` 및 `secret_id` 파일을 통해 토큰을 획득한다.

## Validation

- Run `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh 03-security` before marking documentation ready.
- Verify Vault seal status in runtime sessions with `docker compose --profile security exec vault vault status` and confirm the seal state is `false`.
- Confirm secret paths are accessible by checking `docker compose --profile security logs vault --tail=200 | grep -i 'error\|warn'` after policy changes.
- Verify token authentication by confirming dependent services can retrieve their secrets on startup.

## Troubleshooting

- Start with `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh` to confirm root-context Vault mounts, ports, and network placement.
- Check `vault` status and logs, then follow the linked security runbook for sealed or initialization failures.

## Related Documents

- **System Guide**: [vault.md](../../../docs/05.operations/guides/03-security/vault.md)
- **Technical Spec**: [spec.md](../../../docs/03.specs/03-security/spec.md)
- **Ops Policy**: [vault.md](../../../docs/05.operations/policies/03-security/vault.md)
- **Runbook**: [vault.md](../../../docs/05.operations/runbooks/03-security/vault.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Vault Secret Management service leaf in `03-security`; services: `vault`, `vault-agent`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/03-security/vault/docker-compose.yml` |
| Config files | `docker-compose.yml`, `config`, `config/templates/app_env.ctmpl`, `config/templates/grafana_admin_password.ctmpl`, `config/templates/grafana_client_secret.ctmpl`, `config/templates/grafana_db_password.ctmpl`, `config/templates/keycloak_admin_password.ctmpl`, `config/templates/keycloak_admin_username.ctmpl`, `config/templates/keycloak_db_password.ctmpl`, `config/templates/oauth2_proxy_client_secret.ctmpl`, plus 3 more |
| Config values | env keys: `VAULT_ADDR`, `VAULT_API_ADDR`, `VAULT_CLUSTER_ADDR`, `SKIP_SETCAP`, `SKIP_CHOWN`; profiles: `core`, `security`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/03-security/vault/docker-compose.yml` |
| Networks | `k3d-hyhome`, `infra_net` |
| Volumes | `vault-data:/vault/data`, `./config/vault.hcl:/vault/config/vault.hcl:ro`, `./config/vault-agent.hcl:/vault/config/vault-agent.hcl:ro`, `./config/templates:/vault/config/templates:ro`, `vault-agent-data:/vault/agent`, `vault-agent-out:/vault/out`, `vault-data`, `vault-agent-data`, plus 1 more |
| Ports | `${VAULT_PORT:-8200}`, `${VAULT_CLUSTER_PORT:-8201}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.vault.rule`, `traefik.http.routers.vault.entrypoints`, `traefik.http.routers.vault.tls`, `traefik.http.routers.vault.middlewares`, `traefik.http.services.vault.loadbalancer.server.port` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `vault`, `vault-agent` |
| Operations | [Guide](../../../docs/05.operations/guides/03-security/vault.md), [Policy](../../../docs/05.operations/policies/03-security/vault.md), [Runbook](../../../docs/05.operations/runbooks/03-security/vault.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with root profile validation, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
