---
title: "01-Gateway Traefik Operations Policy"
version: "1.2.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "operations"
artifact_id: "POL-0013"
parent_ids:
- "AD-0001"
created: "2026-05-17"
---

# 01-Gateway Traefik Operations Policy

## Overview

이 문서는 `01-gateway`의 Traefik 운영 정책을 정의한다. 런타임 모델은 `Traefik Primary`이며, 표준 하드닝 강도는 `Balanced`다.

## Scope

- `infra/01-gateway/traefik/docker-compose.yml`
- `infra/01-gateway/traefik/dynamic/middleware.yml`
- Gateway 소유 라우터(`dashboard` 등) 라벨 정책 and root `core` profile validation boundary

- **Systems**: Traefik v3 (gateway tier)
- **Environments**: Local, Dev, Stage, Production-like

## Rules

- **필수**:
  - `check-all-hardening.sh 01-gateway` 실패 0건을 유지해야 한다.
  - 인증 루프, 대량 429, dashboard 접근 장애 발생 시 즉시 런북 절차를 수행해야 한다.
  - Dashboard 라우터는 `dashboard-auth@file,gateway-standard-chain@file`를 사용해야 한다.
  - `gateway-standard-chain`은 `req-rate-limit`, `req-retry`, `req-circuit-breaker`를 포함해야 한다.
  - `req-rate-limit`은 기본값 `average=100`, `burst=50`을 유지한다.
  - `req-retry`는 `attempts=2`, `initialInterval=100ms`를 사용한다.
  - `req-circuit-breaker`는 `NetworkErrorRatio() > 0.30`을 사용한다.
  - Traefik 서비스는 readonly 템플릿(`template-infra-readonly-med`)을 사용한다.
  - Traefik process는 상태를 보유하지 않으며 설정은 Git에서 관리하고 읽기 전용으로 마운트한다.
  - `${DEFAULT_CERT_DIR}`의 private certificate material은 별도 private owner가
    백업·회전한다. 현재 구성에 없는 ACME state를 있다고 가정하지 않는다.
  - Docker socket은 read-only mount여도 host-control API다. 접근 주체와 노출
    경로를 제한하고 일반 애플리케이션에 전달하지 않는다.
- **허용**:
  - 신규 게이트웨이 소유 라우터에 동일 체인 적용
  - 운영 관측 결과 기반의 임계치 미세 조정(승인 후)
- **금지**:
  - 비게이트웨이 소유 라우터에 전역 강제 적용
  - BasicAuth 제거 또는 평문 인증정보 사용

### Known implementation nonconformance

현재 `gateway-standard-chain`은 retry와 circuit-breaker만 연결한다. limiter를
정의만 한 상태는 위의 필수 rate-limit 통제를 충족하지 않는다. @buenhyden이 별도
구현 변경과 route별 수용 검증을 소유한다. 문서·정적 검사 통과를 통제 복구로
기록하지 않으며, 기존 비상 예외도 사전 범위·위험·종료 조건 승인 없이 사용하지 않는다.

### Shared controls and accountability

운영 책임자는 @buenhyden이다. 변경·재시작·credential 작업의 대상과 영향, 승인,
종료 조건을 기록하며 예외는 위험·만료·원복 책임까지 명시한다. 공통 자원 상한과
mount 적용은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md), profile·
상호 배제는 [POL-0078](../01-common/0078-compose-profile-vocabulary.md), image 변경과 검토는
[POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다. OOM·반복 재시작·
인증 실패 증가 또는 이미지·노출·mount 변경 시 정기 주기를 기다리지 않고 검토한다.
보존할 상태와 private credential은 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의
접근·암호화·retention을 적용한다. 제거 전에 소비자와 복구 입력을 확인하고,
volume·인증서·secret 삭제는 서비스 중지와 분리된 승인 대상으로 한다.

## Exceptions

- 비상 복구 시 임시 체인 우회 가능. 단, 사후에 원복 커밋과 변경 기록을 남겨야 한다.

### SEC01 image acceptance — 2026-10-15

owner는 SEC01(SPEC-0204 TSK-0009 "Traefik and Prometheus upstream candidates")에서 Compose가 고정한 Traefik image
(index `575fa15b`)의 잔여 위험을 받아들였다. 적용 가능한 것은 서비스 거부뿐이다. Go HTTP/2 서버
결함 GO-2026-6612·6603·6611·6617은 LAN에서 인증 전에 닿고, GO-2026-6609는 인증 뒤에 닿는다.
GO-2026-6605·6610·6613은 UNPROVEN이다. 만료는 이 결함들을 고친 Go와 x/net으로 빌드된 upstream
릴리스가 나온 뒤 7일, 또는 2026-11-15 중 이른 날이며, 그날 자체 빌드 여부를 다시 결정한다. WAN
노출이나 공개 exploit이 생기면 수용을 앞당겨 철회한다. publisher 서명 확인은 아직 하지 않았으며
수용 범위가 아니라 열린 증거다. 다른 image로 고정을 바꾸면 이 수용은 이어지지 않는다.

### Recovery and Upgrade Controls

Config rollback과 certificate rollback을 구분한다. 이전 config와 certificate가
호환되는지 isolated route에서 확인한 후 80/443 traffic을 수용한다. Image upgrade는
official migration/release notes, config validation, dashboard authentication,
representative routes, metrics, and explicit prior-image rollback을 요구한다.

### Review Cadence

- 월 1회 정기 점검
- Traefik 버전 변경/라우터 추가 시 수시 점검

### Traceability

- Declared parent: [Gateway Tier Architecture Description](../../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Guide](../../guides/02-gateway-and-networking/0013-traefik.md) (`GDE-0013`), [Runbook](../../runbooks/02-gateway-and-networking/0013-traefik.md) (`RUN-0013`)

## Verification

- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `docker compose exec traefik traefik healthcheck --ping`과 같은 runtime health evidence는 승인된 root stack이 실행 중일 때만 유효하다.

## Related Documents

- [Official upstream operational documentation](https://doc.traefik.io/traefik/)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../../README.md)
- [Usage guide](../../guides/02-gateway-and-networking/0013-traefik.md)
- [Recovery runbook](../../runbooks/02-gateway-and-networking/0013-traefik.md)
