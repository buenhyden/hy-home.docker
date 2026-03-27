# Laboratory (11-laboratory) Operations Policy

> 실험 및 관리 서비스의 노출 기준과 통제 정책 정의.

---

## Overview (KR)

이 문서는 `11-laboratory` 티어 서비스들의 운영 정책을 정의한다. 실험적 도구들이 시스템 안정성과 보안을 해치지 않도록 서비스 노출 범위(Exposure)와 인증 기준을 규정한다.

## Policy Scope

관리용 UI 및 실험적 어플리케이션의 런타임 정책 및 보안 가드레일.

## Applies To

- **Systems**: [Portainer](./portainer.md), [RedisInsight](./redisinsight.md), [Homer](./dashboard.md), [Dozzle](./dozzle.md)
- **Agents**: AI-Ops Agents
- **Environments**: Production-Management Area

## Controls

- **Required**:
  - 모든 UI 서비스는 Traefik `sso-auth` 미들웨어를 통해 보호되어야 한다.
  - 관리 데이터 볼륨(`.management_dir`)은 정기적으로 백업되어야 한다.
- **Allowed**:
  - 로컬 네트워크 환경에서의 임시 테스트용 비보안 노출 (단, `lab` 프리픽스 사용 필수).
- **Disallowed**:
  - `/var/run/docker.sock`을 외부(Internet-facing) 망에 직접 노출하는 행위.
  - 인증 없는 데이터베이스 GUI 노출.

## Exceptions

- 초기 부트스트래핑 단계에서의 일시적 비인증 접근은 1시간 이내로 제한한다.

## Verification

- Traefik 대시보드에서 `sso-auth` 미들웨어 적용 여부 확인.
- `infra/11-laboratory` 하위 `docker-compose.yml` 파일의 레이블 리뷰.

## Review Cadence

- Quarterly (매 분기 보안 감시 기록과 함께 리뷰)

## Related Documents

- **ARD**: `[../../02.ard/03-security.md]`
- **Portainer Policy**: `[./portainer.md]`
- **RedisInsight Policy**: `[./redisinsight.md]`
- **Dozzle Policy**: `[./dozzle.md]`
- **Dashboard Policy**: `[./dashboard.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/README.md]`
