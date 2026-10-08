---
title: "Locust Usage Guide"
version: "1.3.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "operations"
artifact_id: "GDE-0062"
parent_ids:
- "POL-0062"
created: "2026-05-10"
---

# Locust Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Purpose and classification

Locust는 DEV 전용 distributed load generator LAB다. Coordinating master와 하나 이상의
worker가 필요한 Python-based scenario 실습을 위해 유지된다. 정상 root Compose와
`testing` profile에는 포함되지 않으며, 독립 `labs/locust.yml` entrypoint만 사용한다. Test run은 지정된 target에 external effect를 주므로
target-owner 승인, limit, stop condition이 필요하다.

### Implementation and data flow

- Source: [Locust LAB Compose](../../../labs/locust.yml)와
  [실행 이미지](../../../infra/11-quality/locust/Dockerfile). Dockerfile/build 선언이
  image source를 소유하며, LAB Compose가 master/worker closure를 소유한다.
- LAB selection: repository root에서 `docker compose -f labs/locust.yml --env-file labs/.env ...`.
  root HOME project, network, volume, secret을 공유하지 않는다.
- 접속 흐름: master와 worker는 `lab_locust_net`에서 통신한다. 기본 host UI port는
  게시하지 않고 headless 결과를 `LAB_LOCUST_RESULT_DIR`에 쓴다.
- Dependency: worker는 LAB master의 process healthcheck를 기다린다. Target service는
  Compose dependency에서 빠져 있으며 이미 승인되고 도달 가능해야 한다.
- Health: master와 worker process 확인은 target이 안전하다거나 test result가
  유효하다는 것을 증명하지 않는다.
- Resources: LAB는 `template-job-med`를 상속한다. worker replica 수와 master가 기다리는
  worker 수는 `LAB_LOCUST_EXPECT_WORKERS` 하나에서 정해지며 기본값은 2다. worker가
  `LAB_LOCUST_EXPECT_WORKERS_MAX_WAIT` 안에 다 붙지 않으면 master는 부하 없이 non-zero로 끝난다.

Scenario directory와 result directory에는 target URL, credential, payload, test result가 들어 있을 수
있다. Credential은 승인된 secret channel에 보관하고, scenario file과 evidence에서
제외하며, retention 전에 request/response data를 sanitize한다.

### Normal use

1. 대상·테스트 소유자·최대 사용자 수·생성 속도·지속 시간·중단 SLI·worker 수를
   기록한다.
2. `LAB_LOCUST_SCENARIO_DIR`와 fresh `LAB_LOCUST_RESULT_DIR`을 준비하고 `docker compose -f labs/locust.yml --env-file labs/.env config --quiet`를
   실행한다.
3. scenario directory에 있는 `locustfile.py`와 fixture를 검토한다. 정확히 그 effect를
   승인받지 않았다면 production data를 수정할 수 없는지 확인한다.
4. Runtime 승인을 받은 뒤 `python3 scripts/operations/lab.py run locust --purpose "<목적>"
   --lease <기간> --deadline <상한>`으로 실행한다. 제어기는 master가 끝나기를 기다리고,
   상한에 닿거나 SIGTERM을 받으면 master를 grace 기간(기본 30초) 동안 SIGTERM으로 멈춘 뒤
   project를 내린다. Target abort SLI를 넘으면 제어기에 SIGTERM을 보내 즉시 멈춘다.
5. 설정 커밋·시나리오 digest·정제된 집계 결과·최종 중지 상태를 보존한다. Raw request body, cookie, token, personal data는
   evidence가 아니다.

### 종료 결과 해석

`lab.py run`은 결과를 ledger의 `outcome`과 자신의 종료 코드로 남긴다. 아래는 SPEC-0214
TSK-0002의 격리 실행에서 관찰한 동작이다.

| outcome | 제어기 코드 | master 종료 코드 | CSV |
| --- | --- | --- | --- |
| `completed` | 0 | 0 | 최종 집계 |
| `failed` | master 코드(예: `--exit-code-on-error` 1) | 같은 값 | 최종 집계 |
| `deadline_exceeded` | 124 | SIGTERM 뒤 0 | 멈춘 시점까지의 집계 |
| `cancelled` | 130 | SIGTERM 뒤 0 | 멈춘 시점까지의 집계 |
| `failed`(master 비정상 종료) | 137 등 | 같은 값 | 마지막 주기 저장본이며 최종 집계가 아님 |

- SIGTERM을 받은 master는 CSV를 쓰고 0으로 끝난다. 상한이나 취소로 멈춘 run은 master
  종료 코드가 아니라 제어기 코드와 `outcome`으로만 구분된다.
- 실행 중 worker 하나가 죽어도 master 종료 코드는 0이다. worker 탈락은 종료 코드로
  드러나지 않으므로 worker 수를 따로 기록한다.
- master가 비정상 종료하면 worker는 project를 내릴 때까지 남는다. 제어기는 결과와 무관하게
  project를 내린다.

Locust 결과는 LAB result directory의 CSV로 남는다. 현재 장기 비교를 소비할 named
consumer가 없어 `perf_db`로 가져오는 adapter는 만들지 않았다. 고정 이미지에 OpenTelemetry
SDK가 없으므로 `--otel`과 OTLP 전달은 지원하지 않는다.

### Persistence, backup, and upgrade

실행 순서와 실패·복구 판단은 [런북](../runbooks/0062-locust.md)의 `시나리오 보존과 업그레이드` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result docker compose -f labs/locust.yml --env-file labs/.env.example --profile lab-locust config --quiet`
- `LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result docker compose -f labs/locust.yml --env-file labs/.env.example --profile lab-locust config --services`
- `bash scripts/hardening/check-all-hardening.sh 11-quality`

### Runbook Handoff

Load 중지, worker loss 진단, scenario file 복구, 승인된 upgrade canary 수행에는
[runbook](../runbooks/0062-locust.md)을 사용한다.

### 재시작과 보존 한계

LAB 서비스는 job template을 사용하며 정상 root 재시작 정책을 상속하지 않는다. 테스트 종료 때 master와 worker를 명시적으로
중지하고 결과 디렉터리와 worker 종료 상태를 확인해야 한다. 자체 데이터베이스·TLS 인증서 복구는 없고, 호스트의
시나리오·결과와 대상 시스템의 상태는 서로 다른 소유자가 복구한다.

### Traceability

- [Policy](../policies/0062-locust.md) (`POL-0062`)
- [Runbook](../runbooks/0062-locust.md) (`RUN-0062`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)

## Related Documents

- [Locust distributed load generation](https://docs.locust.io/en/stable/running-distributed.html)
- [Locust running without the web UI](https://docs.locust.io/en/stable/running-without-web-ui.html)
- [Locust LAB Compose](../../../labs/locust.yml)
- [Operations index](../README.md)
