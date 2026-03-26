# Vault Secret Management

> Identity-based secrets management and encryption-as-a-service.

---

## Overview (KR)

HashiCorp Vault는 `hy-home.docker` 플랫폼의 중앙 비밀 관리 엔진이다. 데이터 암호화, 동적 비밀 생성, 그리고 엄격한 접근 제어 및 감사 기능을 제공한다. Raft 통합 스토리지를 사용하여 고가용성을 유지하며, Vault Agent를 통해 애플리케이션에 비밀을 안전하게 전달한다.

## Audience

- SRE (Scaling & Maintenance)
- Security Engineers (Policy & Audit)
- AI Agents (Automated unsealing & monitoring)

## Scope

### In Scope

- Vault Server 구성 (`vault.hcl`) 및 Raft 스토리지 관리
- Vault Agent 구성 (`vault-agent.hcl`) 및 템플릿 처리
- 상태 모니터링 및 `wget` 기반 헬스체크 프로토콜
- Keycloak OIDC 통합 및 AppRole 인증 체계

### Out of Scope

- 하위 네트워크 방화벽 설정
- 개별 애플리케이션 내부의 비즈니스 로직
- 비밀 내용 자체의 생성 (관리에만 집중)

## Structure

```text
vault/
├── config/             # Vault & Agent configuration files
│   ├── templates/      # Secret rendering templates (.ctmpl)
│   ├── vault.hcl       # Server configuration
│   └── vault-agent.hcl # Agent configuration
├── docker-compose.yml  # Container orchestration
└── README.md           # This file
```

## Tech Stack

| Category    | Technology      | Notes                  |
| ----------- | --------------- | ---------------------- |
| Binary      | Vault (Go)      | v1.21.4                |
| Persistence | Raft            | Integrated Storage     |
| Sidecar     | Vault Agent     | Auto-auth & Templating |
| Runtime     | Alpine          | Container Image        |

## Implementation Snippet

### Healthcheck Protocol
Vault의 헬스체크는 봉인(Sealed) 상태나 초기화되지 않은 상태에서도 클러스터 준비도를 판단할 수 있도록 설계됨:

```yaml
healthcheck:
  test: ["CMD-SHELL", 'wget -q -O- "http://127.0.0.1:8200/v1/sys/health?standbyok=true&sealedcode=200&uninitcode=200" >/dev/null 2>&1 || exit 1']
```

### Configuration Highlights
- **Storage**: Raft 스토리지를 사용하여 별도의 외부 DB 없이 클러스터링 가능.
- **Listener**: Traefik이 외부 TLS를 종료하며, 내부망(`infra_net`)에서는 고성능 HTTP 통신 수행.

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

1. **Sealed Status**: 모든 관리 작업 전 `vault status`를 통해 `Sealed: false`임을 확인해야 함.
2. **AppRole ID**: 자동화 스크립트는 `/vault/agent/role_id` 및 `secret_id` 경로를 참조하여 인증을 수행함.
3. **Rate Limiting**: Vault API 호출 시 `429` 응답에 대한 지수 백오프(Exponential Backoff) 처리가 필요함.

## Related Documents

- **Guide**: `[../../../docs/07.guides/03-security/vault.md]`
- **Spec**: `[../../../docs/04.specs/03-security/spec.md]`
- **Operation**: `[../../../docs/08.operations/03-security/vault.md]`
- **Runbook**: `[../../../docs/09.runbooks/03-security/vault.md]`
