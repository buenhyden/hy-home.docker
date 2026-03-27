# Dozzle Operations Policy

> 관리 도구 로그 노출 및 접근 통제 정책.

---

## Overview (KR)

이 문서는 Dozzle 서비스의 운영 정책을 정의한다. 시스템 로그는 민감한 정보를 포함할 수 있으므로, 엄격한 인증 및 노출 범위를 규정하여 보안 사고를 예방한다.

## Policy Scope

Dozzle 서비스의 노출 범위, 인증 방식 및 리소스 접근 통제.

## Applies To

- **Systems**: Dozzle
- **Agents**: AI-Ops Agents
- **Environments**: Production-Management Area

## Controls

- **Required**:
  - 모든 UI 접근은 Traefik `sso-auth` 미들웨어를 통해 승인된 관리자만 가능해야 한다.
  - `/var/run/docker.sock`은 읽기 전용으로 연결하거나 내부 네트워크에서만 통제된 방식으로 사용되어야 한다 (Dozzle 설정 준수).
- **Allowed**:
  - 개발 및 트러블슈팅 목적의 실시간 로그 스트리밍.
- **Disallowed**:
  - 인증 없이 외부 인터넷(Public)에 Dozzle UI를 노출하는 행위.
  - 로그 데이터를 외부 서비스로 무단 반출하는 설정.

## Exceptions

- 긴급 장애 복구 상황에서 SSO 서버 장애 시, 로컬 포트 포워딩을 통한 일시적 접근을 허용하되 작업 완료 후 즉시 차단한다.

## Verification

- Traefik `Host` 룰 및 미들웨어 설정(`sso-auth`)이 `docker-compose.yml`에 올바르게 적용되었는지 정기적으로 검토한다.

## Review Cadence

- Quarterly (보안 감사 주기와 동기화)

## Related Documents

- **ARD**: `[../../02.ard/03-security.md]`
- **Guide**: `[../../07.guides/11-laboratory/dozzle.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/dozzle.md]`
