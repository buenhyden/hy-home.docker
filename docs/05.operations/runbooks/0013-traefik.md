---
title: "01-Gateway Traefik Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0013"
parent_ids:
- "GDE-0013"
created: "2026-05-17"
---

# 01-Gateway Traefik Runbook

## Overview

이 런북은 Traefik 미들웨어 회귀, dashboard 접근 장애, 라우팅 이상 상황에서 복구 절차를 정의한다.

> Scope: Traefik Primary Gateway Recovery

### Purpose

- `gateway-standard-chain` 회귀 시 신속 복구
- Dashboard 인증/접근 장애 진단
- Traefik 서비스 정상성 복원

## When to Use

- dashboard 접근 실패(401 loop, 429 burst, 5xx)
- 미들웨어 체인 누락/오타/잘못된 순서
- Traefik healthcheck 실패

## Procedure

### Target and prerequisites

저장소 루트, 승인된 Docker context의 `traefik`만 대상으로 한다. `core`/`dev`/
`local` 중 기존 선택과 Nginx 비활성, host bind/80·443, root network, 인증서와
BasicAuth Secret 참조를 확인한다. Docker socket은 host 제어 접근이므로 전체 API
응답이나 secret mount 내용을 증거로 출력하지 않는다. config/image 변경·restart는
서비스 영향과 이전 config/certificate/image identity가 확인된 별도 승인이 필요하다.

### Static checks and diagnosis

```bash
HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 01-gateway
```

exit 0이더라도 `gateway-standard-chain`의 실제 멤버십을 따로 확인한다.
현재 `req-rate-limit`은 정의되어 있으나 chain에는 retry/circuit-breaker만 있다.
이는 [POL-0013](../policies/0013-traefik.md)의 구현 미준수다. 문자열 블록 존재 검사로
고쳐졌다고 보고하지 않는다. 별도 구현 변경과 수용 검증 전에는 rate limit이
보장되는 절차로 완료 처리하지 않는다.

| 증상 | 읽기 전용 확인·판단 |
| --- | --- |
| Dashboard401 | 라우터의 `dashboard-auth@file,gateway-standard-chain@file` 순서와 private usersFile 참조를 확인한다. 인증 제거로 복구하지 않는다. |
| SSO redirect/403 | `sso-errors`는401만302로 바꾸고403은 유지한다. Proxy 그룹 거부와 issuer/callback 문제를 [RUN-0015](0015-oauth2-proxy.md)로 분리한다. |
| 429 또는5xx | 실제 적용 middleware와 대상 backend를 확인한다. limiter 선언만으로429 원인을 단정하지 않는다. retry 횟수와 circuit-breaker 조건은 Policy에 대조한다. |
| Route/인증서 실패 | `edge_net`, provider enable label, domain, certificate/CA·file path와 middleware 이름을 확인한다. |
| Health 실패 | 내부 metrics entrypoint의 ping과 실제 사용자 요청을 구분하고, OOM/restart 상태와 정제된 오류 유형을 확인한다. |

실행 중인 승인 대상에서만 다음을 수행한다.

```bash
docker compose ps traefik
docker compose exec -T traefik traefik healthcheck --ping
```

### Startup, shutdown and apply

기존 로컬 image와 network·secret·cert 입력이 준비됐고 runtime 변경이 승인된
경우에만 아래를 실행한다. start는80/443을 점유하며 stop은 모든 해당 route를 중단한다.

```bash
docker compose --profile core up -d --no-deps --no-build --pull never traefik
# 승인된 중지에만 실행한다.
docker compose stop traefik
```

`/dynamic` directory의 file watch 변경은 실행 중 즉시 반영될 수 있다. 실제
mount source를 확인하지 않고 Git merge 자체를 배포로 단정하지 않는다. 정적
단일 파일 변경은 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)에
따라 대상 `up -d --no-deps --no-build --pull never --force-recreate traefik`와
post-apply hash 검사를 수행한다. healthy, dashboard BasicAuth 성공·거부,
대표 ForwardAuth와 native OIDC route, 내부 metrics 수집을 별개로 확인한다.
실패하면 새 설정 적용을 중단하고 아래 rollback으로 전달한다.

## Evidence

시각·revision·승인 대상, 명령 exit, chain 멤버십, 정제된 health/route/metrics
결과만 Task/Incident에 남긴다. secret 값, Authorization/Cookie, 원문 access/error
로그는 첨부하지 않는다. 증거별 static/runtime/NOT_RUN을 구분한다.

## Rollback or Recovery

1. Git의 검토된 static/dynamic 설정과 private owner의 일치하는 인증서 세트를
   준비한다. key를 repository/evidence에 복사하지 않는다.
2. static 검증, 승인된 대상 apply/hash 검사, health와 대표 route별 정상·거부
   검증을 반복한다. canary/격리 route가 준비되지 않았으면 만들어졌다고 가정하지
   말고 적용을 중단한다. limiter 미준수는 config rollback만으로 해소되지 않는다.
3. [RUN-0086](0086-dependency-version-management.md)의 migration/release 검토 후
   image 변경을 수행하고, 실패하면 이전 image identity와 호환 config를 함께
   복구한다. certificate rollback은 별도 private custody 범위다.
4. ACME storage 선언이 없으므로 존재하지 않는 ACME state 복원은 하지 않는다.
   서비스 중지는 인증서/secret 삭제가 아니며 제거는 Policy의 소비자·보존 심사를 따른다.

기존 2026-09-20 복구 계획과 이번 감사는 runtime 복구를 실행하지 않았다.
전체 호스트 cold-start는 [RUN-0098](0098-cold-start-and-reboot.md)이 소유한다.

## Escalation

limiter 미준수, 인증 우회·credential 노출 징후, persistent health/route 오류,
잘못된 bind/network, 또는 canary·rollback 입력 부재는 @buenhyden에게 전달한다.
영향 route, 정제된 관찰과 필요한 별도 구현/운영 승인을 기록한다. 여러 티어
장애는 [RUN-0099](0099-system-operations.md)로 연결한다.

## Traceability

- Declared parent: [01-Gateway Traefik Usage Guide](../guides/0013-traefik.md) (`GDE-0013`)
- Governing authority: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Guide](../guides/0013-traefik.md) (`GDE-0013`), [Policy](../policies/0013-traefik.md) (`POL-0013`)

## Related Documents

- [Official upstream operational documentation](https://doc.traefik.io/traefik/)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0013-traefik.md)
- [Operations policy](../policies/0013-traefik.md)
