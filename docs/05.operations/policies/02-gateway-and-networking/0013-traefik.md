---
title: "01-Gateway Traefik Operations Policy"
version: "1.5.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0013"
parent_ids:
- "AD-0001"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# 01-Gateway Traefik Operations Policy

## Purpose and Scope

### Objective

이 문서는 `01-gateway`의 Traefik 운영 정책을 정의한다. 런타임 모델은 `Traefik Primary`이며, 표준 하드닝 강도는 `Balanced`다.

#### Authority

- Declared parent: [Gateway Tier Architecture Description](../../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)

### Applies To

- `infra/01-gateway/traefik/docker-compose.yml`
- `infra/01-gateway/traefik/dynamic/middleware.yml`
- Gateway 소유 라우터(`dashboard` 등) 라벨 정책과 root `core` profile 검증 경계

- **Systems**: Traefik v3 (gateway tier)
- **Environments**: Local, Dev, Stage, Production-like

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0013-R1 | 항상 | 필수: `check-all-hardening.sh 01-gateway` 실패 0건을 유지한다 | `bash scripts/hardening/check-all-hardening.sh 01-gateway` | none |
| POL-0013-R2 | 인증 루프/대량 429/dashboard 접근 장애 발생 시 | 필수: 즉시 런북 절차를 수행한다 | none | none |
| POL-0013-R3 | Dashboard 라우터 | 필수: `dashboard-auth@file,gateway-standard-chain@file`를 사용한다 | none | none |
| POL-0013-R4 | `gateway-standard-chain` | 필수: `req-rate-limit`/`req-retry`/`req-circuit-breaker`를 이 순서로 포함한다 | none | none |
| POL-0013-R5 | `req-rate-limit` | 필수: `average=100`/`period=1s`/`burst=200`을 사용한다 | none | none |
| POL-0013-R6 | `req-rate-limit` | 필수: 출발지를 TCP peer(`ipStrategy.depth=0`)로 구분한다 | none | none |
| POL-0013-R7 | `req-rate-limit` | 금지: 클라이언트가 보낸 헤더를 출발지로 쓴다 | none | none |
| POL-0013-R8 | middlewares가 있는 모든 라우터 | 필수: `gateway-standard-chain@file`(또는 이를 포함한 `sso-protected-chain@file`)을 거친다 | none | none |
| POL-0013-R9 | `req-retry` | 필수: `attempts=2`/`initialInterval=100ms`를 사용한다 | none | none |
| POL-0013-R10 | `req-circuit-breaker` | 필수: `NetworkErrorRatio() > 0.30`을 사용한다 | none | none |
| POL-0013-R11 | Traefik 서비스 | 필수: readonly 템플릿(`template-infra-readonly-med`)을 사용한다 | none | none |
| POL-0013-R12 | Traefik process | 필수: 상태를 보유하지 않는다 | none | none |
| POL-0013-R13 | Traefik 설정 | 필수: Git에서 관리하고 읽기 전용으로 마운트한다 | none | none |
| POL-0013-R14 | `${DEFAULT_CERT_DIR}`의 private certificate material | 필수: 별도 private owner가 백업/회전한다 | none | none |
| POL-0013-R15 | ACME state | 금지: 현재 구성에 없는 ACME state를 있다고 가정한다 | none | none |
| POL-0013-R16 | Docker socket(read-only mount 포함) | 필수: 접근 주체와 노출 경로를 제한한다 | none | none |
| POL-0013-R17 | Docker socket | 금지: 일반 애플리케이션에 전달한다 | none | none |
| POL-0013-R18 | 신규 게이트웨이 소유 라우터 | 허용: 동일 체인을 적용한다 | none | none |
| POL-0013-R19 | 운영 관측 결과 기반 임계치 미세 조정 | 허용: 승인 후 조정한다 | 수동 | none |
| POL-0013-R20 | 비게이트웨이 소유 라우터 | 금지: 전역 강제 적용한다 | none | none |
| POL-0013-R21 | 인증 설정 | 금지: BasicAuth를 제거한다 | none | none |
| POL-0013-R22 | 인증 설정 | 금지: 평문 인증정보를 사용한다 | none | none |
| POL-0013-R23 | rate-limit 사용 | 금지: 속도 제한을 인증·인가 대용으로 사용한다 | none | none |
| POL-0013-R24 | HOME 통제 적용 기록 | 금지: 문서/정적 검사 통과만으로 HOME 통제 적용을 기록한다 | none | HOME 적용 뒤 라우터별 수용 증거는 SPEC-0204 TSK-0011이 소유한다 |
| POL-0013-R25 | 공통 자원 상한과 mount 적용 | 필수: [POL-0006](../01-common/0006-infrastructure-optimization-governance.md)을 적용한다 | none | none |
| POL-0013-R26 | profile/상호 배제 | 필수: [POL-0078](../01-common/0078-compose-profile-vocabulary.md)을 적용한다 | none | none |
| POL-0013-R27 | image 변경과 검토 | 필수: [POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다 | none | none |
| POL-0013-R28 | 보존할 상태와 private credential | 필수: [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 접근/암호화/retention을 적용한다 | none | none |
| POL-0013-R29 | 제거 전 | 필수: 소비자와 복구 입력을 확인한다 | none | none |
| POL-0013-R30 | volume/인증서/secret 삭제 | 필수: 서비스 중지와 분리된 승인 대상으로 한다 | 수동 | none |
| POL-0013-R31 | rollback | 필수: config rollback과 certificate rollback을 구분한다 | none | none |
| POL-0013-R32 | 80/443 트래픽 수용 전 | 필수: 이전 config와 certificate의 호환을 격리 route에서 확인한다 | none | none |
| POL-0013-R33 | Image upgrade | 필수: 공식 migration/release note 검토/config 검증/dashboard 인증/대표 route/metrics/명시적 이전 image rollback을 요구한다 | none | none |

- **필수**:
  - `check-all-hardening.sh 01-gateway` 실패 0건을 유지해야 한다.
  - 인증 루프, 대량 429, dashboard 접근 장애 발생 시 즉시 런북 절차를 수행해야 한다.
  - Dashboard 라우터는 `dashboard-auth@file,gateway-standard-chain@file`를 사용해야 한다.
  - `gateway-standard-chain`은 `req-rate-limit`, `req-retry`, `req-circuit-breaker`를 이 순서로 포함해야 한다.
  - `req-rate-limit`은 `average=100`, `period=1s`, `burst=200`을 사용하고 출발지를
    TCP peer(`ipStrategy.depth=0`)로 구분한다. 클라이언트가 보낸 헤더를 출발지로 쓰지 않는다.
  - middlewares가 있는 모든 라우터는 `gateway-standard-chain@file`(또는 이를 포함한
    `sso-protected-chain@file`)을 거쳐야 한다.
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

#### Rate-limit basis

2026-10-20 @buenhyden이 burst를 50에서 200으로 올리는 조정을 승인했다. 24시간 access log의
최대치는 한 출발지·라우터 기준 open-webui 123 req/s, prometheus-api 33 req/s였다.
당시 Traefik은 average 100에서 최대 지연이 5ms라 bucket을 넘는 요청에 바로 429를 준다.
bucket은 라우터·출발지별이다. host와 k3d 요청은 docker-proxy를 지나 `edge_net`
게이트웨이 주소로 들어오므로 라우터마다 한 bucket을 함께 쓴다. 속도 제한은 인증·인가를
대신하지 않는다. HOME 적용 뒤의 라우터별 수용 증거는 SPEC-0204 TSK-0011이 소유하며,
문서·정적 검사 통과만으로 HOME 통제 적용을 기록하지 않는다.

#### Shared controls and accountability

공통 자원 상한과
mount 적용은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md), profile·
상호 배제는 [POL-0078](../01-common/0078-compose-profile-vocabulary.md), image 변경과 검토는
[POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다. 보존할 상태와 private credential은 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의
접근·암호화·retention을 적용한다. 제거 전에 소비자와 복구 입력을 확인하고,
volume·인증서·secret 삭제는 서비스 중지와 분리된 승인 대상으로 한다.

#### Recovery and Upgrade Controls

Config rollback과 certificate rollback을 구분한다. 이전 config와 certificate가
호환되는지 격리 route에서 확인한 후 80/443 트래픽을 수용한다. Image upgrade는
공식 migration/release note 검토, config 검증, dashboard 인증, 대표 route, metrics와
명시적인 이전 image rollback을 요구한다.

### Exceptions

#### Exception Conditions

- 비상 복구 시 임시 체인 우회 가능. 단, 사후에 원복 커밋과 변경 기록을 남겨야 한다.

#### SEC01 image acceptance — 2026-10-15

owner는 SEC01(SPEC-0204 TSK-0009 "Traefik and Prometheus upstream candidates")에서 Compose가 고정한 Traefik image
(index `575fa15b`)의 잔여 위험을 받아들였다. 적용 가능한 것은 서비스 거부뿐이다. Go HTTP/2 서버
결함 GO-2026-6612·6603·6611·6617은 LAN에서 인증 전에 닿고, GO-2026-6609는 인증 뒤에 닿는다.
GO-2026-6605·6610·6613은 UNPROVEN이다. 만료는 이 결함들을 고친 Go와 x/net으로 빌드된 upstream
릴리스가 나온 뒤 7일, 또는 2026-11-15 중 이른 날이며, 그날 자체 빌드 여부를 다시 결정한다. WAN
노출이나 공개 exploit이 생기면 수용을 앞당겨 철회한다. publisher 서명 확인은 아직 하지 않았으며
수용 범위가 아니라 열린 증거다. 다른 image로 고정을 바꾸면 이 수용은 이어지지 않는다.

**Superseded — 2026-10-30.** 위 수용은 고친 upstream 릴리스가 나온 뒤 7일이 지난
2026-10-22에 만료되었다. owner는 2026-10-30에 Compose 고정을 고친 Go와 x/net으로 빌드된
upstream 릴리스(index `1336e85a`)로 바꾸기로 결정했으므로 이 수용은 채택한 고정 image로
대체된다. 정확한 tag와 빌드 정보는 SPEC-0204-TSK-0021과 Compose 고정이 소유한다. 위 기록은 이력으로 보존하며 새 image에는 이어지지 않는다. 새 image의 pull,
offline scan, 독립 applicability 검토, config 부팅, HOME 재생성과 rollback은 아직 `NOT_RUN`이고
SPEC-0204-TSK-0021이 owner 단계로 기록한다.

#### Approval and Review

- 월 1회 정기 점검
- Traefik 버전 변경/라우터 추가 시 수시 점검

- OOM·반복 재시작·인증 실패 증가 또는 이미지·노출·mount 변경 시 정기 주기를 기다리지 않고 검토한다.

## Enforcement

### Mechanisms

- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `docker compose exec traefik traefik healthcheck --ping`과 같은 runtime health evidence는 승인된 root stack이 실행 중일 때만 유효하다.

### Limits

이 정책은 아래 규칙에 대해 명명된 자동 검사를 연결하지 않거나 수동 검토에 맡긴다.

- hardening/대응: 명명된 검사 없음 R2 (`POL-0013-` 접두)
- 라우터 체인: 명명된 검사 없음 R3~R10 (`POL-0013-` 접두)
- 서비스 구성: 명명된 검사 없음 R11~R17 (`POL-0013-` 접두)
- 허용/금지: 명명된 검사 없음 R18, R20~R22; 수동 검토 R19 (`POL-0013-` 접두)
- Rate-limit 근거: 명명된 검사 없음 R23, R24 (`POL-0013-` 접두)
- 공통 통제: 명명된 검사 없음 R25~R29; 수동 검토 R30 (`POL-0013-` 접두)
- 복구/업그레이드: 명명된 검사 없음 R31~R33 (`POL-0013-` 접두)
- 명명된 검사는 hardening 점검과 core profile 정적 렌더링뿐이며 `docker compose exec traefik traefik healthcheck --ping` 같은 runtime health evidence는 승인된 root stack이 실행 중일 때만 유효하다(150, 154행).
- 현재 고정 image의 pull, offline scan, 독립 applicability 검토, config 부팅, HOME 재생성과 rollback은 `NOT_RUN`이며 publisher 서명 확인은 하지 않았다(134~135, 127~128행).

## Ownership

### Owner

운영 책임자는 @buenhyden이다. 변경·재시작·credential 작업의 대상과 영향, 승인,
종료 조건을 기록하며 예외는 위험·만료·원복 책임까지 명시한다.

### Review Triggers

- Subject peers: [Guide](../../guides/02-gateway-and-networking/0013-traefik.md) (`GDE-0013`), [Runbook](../../runbooks/02-gateway-and-networking/0013-traefik.md) (`RUN-0013`)

- [Official upstream operational documentation](https://doc.traefik.io/traefik/)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../../README.md)
