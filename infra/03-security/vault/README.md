# Vault Secret Management

> Identity-based secrets management and encryption-as-a-service for `hy-home.docker`.

## Overview

HashiCorp Vault는 `hy-home.docker` 플랫폼의 중앙 비밀 관리 엔진이다. 모든 인프라 계층(Gateway, Auth, Data, App)에서 사용하는 API 키, 데이터베이스 자격 증명, 인증서 등을 안전하게 보관하고 수명 주기(Lifecycle)를 관리한다. Raft 통합 스토리지를 통해 별도의 데이터베이스 없이 고가용성 클러스터를 구성하며, Vault Agent Sidecar를 통해 애플리케이션에 비밀을 투명하게 주입한다.

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
| Platform    | Vault (Go)      | v1.21.4 (Official)     |
| Persistence | Raft            | Integrated Storage     |
| Sidecar     | Vault Agent     | Auto-auth & Templating |
| OS          | Alpine          | Minimal Footprint      |

## Implementation Snippet

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
# Verify Raft cluster status
docker exec vault vault operator raft list-peers

# Check unseal & init status
docker exec vault vault status

# Rendered secrets check (Vault Agent)
docker exec vault-agent ls -la /vault/agent/
```

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. **Sealed Status Check**: 모든 API 작업 전 `vault status`를 통해 `Sealed: false`임을 확인한다.
2. **Template Path Verification**: `.ctmpl` 파일 수정 시 `vault-agent.hcl`의 `template` 섹션과 경로가 일치하는지 확인한다.
3. **AppRole ID Access**: 자동화 작업 시 `/vault/agent/role_id` 및 `secret_id` 파일을 통해 토큰을 획득한다.

## Related Documents

- **System Guide**: [vault.md](../../../docs/07.guides/03-security/vault.md)
- **Technical Spec**: [spec.md](../../../docs/04.specs/03-security/spec.md)
- **Ops Policy**: [vault.md](../../../docs/08.operations/03-security/vault.md)
- **Runbook**: [vault.md](../../../docs/09.runbooks/03-security/vault.md)
