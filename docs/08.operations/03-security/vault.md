# Vault Operations Policy

> Operational and security policies for the Vault authentication and secrets management layer in `hy-home.docker`.

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 보안 심장부인 Vault의 운영 정책을 정의한다. Unseal Key의 관리 체계, 토큰 수명(TTL), 그리고 보안 감사(Audit Logging) 절차를 규정하여 시스템의 무결성과 기밀성을 보장한다.

## Policy Scope

Vault 서버(`vault`) 및 에이전트(`vault-agent`)의 런타임 보안 설정, 인증 방식(AppRole, OIDC), 그리고 비밀 보관 주기를 규정한다.

## Applies To

- **Systems**: Vault Raft Cluster, Vault Agent Sidecars
- **Agents**: AI Agents (Automated unsealing & monitoring)
- **Environments**: Production (Strict), Staging (Standard)

## Controls

- **Required**:
  - 초기화 시 생성된 5개의 Unseal 키는 독립된 3명 이상의 관리자 또는 보안 스토리지에 분산 보관해야 함.
  - 모든 Vault API 요청은 `/vault/logs/audit.log`에 JSON 형태로 기록되어야 함.
- **Allowed**:
  - 내부망(`infra_net`)에서의 HTTP(L7) 통신 (Traefik이 외부 TLS 종료).
  - AppRole을 통한 애플리케이션 서비스의 자동 인증 및 토큰 갱신.
- **Disallowed**:
  - Root Token의 운영 환경 상시 보관 및 사용 (부트스트래핑 후 즉시 파기 권고).
  - Unseal 키의 일반 텍스트 파일 저장 또는 Git 저장소 포함.

## Exceptions

- 초기 구축 및 복구 단계에서의 임시 Root Token 사용 (SRE 파트장 승인 필요).
- 테스트용 Dev 모드 Vault 실행 (운영 데이터 접근 금지).

## Verification

- `vault audit list` 명령을 통해 감사 로그 활성화 상태를 매월 점검함.
- `vault token lookup`을 통해 AppRole 토큰의 TTL 준수 여부를 확인함.

## Review Cadence

- **Quarterly**: 실무자 권한 복기 및 Unseal 키 보관 상태 점검.

## Related Documents

- **ARD**: [spec.md](../../04.specs/03-security/spec.md)
- **Runbook**: [vault.md](../../09.runbooks/03-security/vault.md)
- **Guide**: [vault.md](../../07.guides/03-security/vault.md)
