---
title: "Locust Usage Guide"
version: "1.1.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0062"
parent_ids:
- "POL-0062"
implementation_services:
  infra/11-quality/locust/docker-compose.yml:
  - locust-master
  - locust-worker
created: "2026-05-10"
---

# Locust Usage Guide

## Usage

### Purpose and classification

Locust는 DEV 전용 distributed load generator다. Coordinating web UI와 하나 이상의
worker가 필요한 Python-based scenario를 위해 유지된다. `locust-master`와
`locust-worker` 모두 `testing` profile에만 속하며, 넓은 `tooling` selection으로는
둘 다 시작되지 않는다. Test run은 지정된 target에 external effect를 주므로
target-owner 승인, limit, stop condition이 필요하다.

### Implementation and data flow

- Source: [Locust Compose](../../../infra/11-quality/locust/docker-compose.yml)와
  그 sibling Dockerfile. Dockerfile/build 선언이 runtime source를 소유하며, derived
  image projection은 navigation일 뿐 build authority가 아니다.
- Root selection: repository root에서 `docker compose --profile testing ...`.
  Root project가 project default network를 제공하므로, leaf를 standalone project로
  사용하지 않는다.
- 접속 흐름: 운영자/브라우저 -> 호스트 포트 `127.0.0.1:${LOCUST_HOST_PORT:-18089}` -> master UI;
  worker -> project default network를 통해 `locust-master`; master와 worker는
  `/mnt/locust`에서 공유 `locust-data` bind-backed volume을 읽는다.
- Dependency: worker는 master의 HTTP healthcheck를 기다린다. Target service는
  의도적으로 Compose dependency에서 뺐으며 이미 승인되고 도달 가능해야 한다.
- Health: master는 자신의 UI를 probe하고, worker는 자신의 process를 확인한다.
  Health는 target이 안전하다거나 test result가 유효하다는 것을 증명하지 않는다.
- Resources: 두 service 모두 `template-infra-med`를 상속한다. Compose는
  `locust-worker` replica 2개를 선언한다. 승인된 test는 두 Locust service를 모두
  지정하고 `--scale locust-worker=N`으로 이 default를 override할 수 있다.

Scenario directory에는 target URL, credential, payload, test result가 들어 있을 수
있다. Credential은 승인된 secret channel에 보관하고, scenario file과 evidence에서
제외하며, retention 전에 request/response data를 sanitize한다.

### Normal use

1. 대상·테스트 소유자·최대 사용자 수·생성 속도·지속 시간·중단 SLI·worker 수를
   기록한다.
2. Repository root에서 `docker compose --profile testing config --quiet`를
   실행하고 `docker compose --profile testing config --services`로 선택된
   service를 확인한다.
3. `locust-data` 뒤의 host directory에 있는 scenario를 검토한다. 정확히 그 effect를
   승인받지 않았다면 production data를 수정할 수 없는지 확인한다.
4. Runtime 승인을 받은 뒤 `locust-master`와 `locust-worker`만 시작하고 host-bound UI를
   사용한다. Target abort SLI를 넘으면 즉시 run을 중지한다.
5. 설정 커밋·시나리오 digest·정제된 집계 결과·최종 중지 상태를 보존한다. Raw request body, cookie, token, personal data는
   evidence가 아니다.

### Persistence, backup, and upgrade

실행 순서와 실패·복구 판단은 [런북](../runbooks/0062-locust.md)의 `시나리오 보존과 업그레이드` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

## Common Checks

- `docker compose --profile testing config --quiet`
- `docker compose --profile testing config --services`
- `bash scripts/hardening/check-all-hardening.sh 11-quality`

## Runbook Handoff

Load 중지, worker loss 진단, scenario file 복구, 승인된 upgrade canary 수행에는
[runbook](../runbooks/0062-locust.md)을 사용한다.

### 재시작과 보존 한계

두 서비스는 공통 템플릿의 `restart: unless-stopped`를 상속한다. 부하 시작 방식과
별개로 컨테이너가 다시 기동될 수 있으므로 테스트 종료 때 master와 worker를 명시적으로
중지하고 확인해야 한다. 작업 재생 금지 정책을 충족했다고 단정하지 않으며 재시작 계약
변경은 별도 구현 검토 대상이다. 자체 데이터베이스·TLS 인증서 복구는 없고, 호스트의
시나리오·결과와 대상 시스템의 상태는 서로 다른 소유자가 복구한다.

## Traceability

- [Policy](../policies/0062-locust.md) (`POL-0062`)
- [Runbook](../runbooks/0062-locust.md) (`RUN-0062`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)

## Related Documents

- [Locust distributed load generation](https://docs.locust.io/en/stable/running-distributed.html)
- [Locust running without the web UI](https://docs.locust.io/en/stable/running-without-web-ui.html)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Operations index](../README.md)
