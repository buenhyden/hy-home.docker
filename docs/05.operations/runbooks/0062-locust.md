---
title: "Locust Recovery Runbook"
version: "1.3.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0062"
parent_ids:
- "GDE-0062"
created: "2026-05-17"
---

# Locust Recovery Runbook

## Overview

Locust LAB 실행 중 target 상태가 나빠지거나 worker 연결이 끊길 때 부하를 멈추고 진단하는 절차다.
시나리오 파일 복구와 승인된 upgrade canary도 다룬다.

## Trigger and Preconditions

test 중 target health가 저하되거나, worker 연결이 끊기거나, master UI가 실패하거나,
scenario file이 손상되거나, Locust image/dependency upgrade에 승인된 canary가 필요할 때
사용한다. 모든 command는 저장소 루트에서 독립 LAB Compose file을 지정한다.
아래 공개 명령은 `labs/.env.example`와 명시한 합성 경로만 사용한다. 실제 승인된
실행 값은 승인된 실행 도구가 주입하며 문서에 비공개 env 파일 경로를 적지 않는다.

## Procedure

1. target, users, spawn rate, duration, worker count, scenario digest, 그리고 처음
   실패한 target SLI를 기록한다. cookie, token, response body는 수집하지 않는다.
2. 진단 전에 load를 중지한다. `lab.py run`으로 시작한 실행이면 그 제어기에 SIGTERM
   (`Ctrl-C`)을 보낸다. 제어기가 master를 grace 기간 동안 멈추고 project를 내린다.
   제어기가 이미 죽었으면 `python3 scripts/operations/lab.py down locust`를 쓴다. 아래
   Compose 명령은 제어기 없이 시작한 경우에만 쓴다.

   ```bash
   LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result \
   docker compose -f labs/locust.yml --env-file labs/.env.example --profile lab-locust stop lab-locust-worker lab-locust-master
   ```

3. bounded status와 로그를 캡처한다.

   ```bash
   LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result \
   docker compose -f labs/locust.yml --env-file labs/.env.example --profile lab-locust ps lab-locust-master lab-locust-worker
   LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result \
   docker compose -f labs/locust.yml --env-file labs/.env.example --profile lab-locust logs --tail=200 lab-locust-master lab-locust-worker
   ```

4. `docker compose -f labs/locust.yml --env-file labs/.env.example config --quiet`로 확인한다. worker를 재생성하기
   전에 master health failure를 점검한다. target SLI가 회복되지 않았으면 Locust를
   중지 상태로 두고 target owner에게 escalation한다.
5. master가 healthy이고 재시작이 승인되면 master를 먼저 시작하고 worker를 시작한다.

   ```bash
   LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result \
   docker compose -f labs/locust.yml --env-file labs/.env.example --profile lab-locust up -d lab-locust-master
   LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result \
   docker compose -f labs/locust.yml --env-file labs/.env.example --profile lab-locust up -d lab-locust-worker
   ```

6. scenario 복구 시에는 두 service를 모두 중지한 상태로 두고, 현재 bind-backed scenario
   디렉터리를 protected quarantine path로 복사하고, 검토된 파일을 별도 디렉터리로
   복원하고, hash를 비교한 뒤에만 active file을 교체한다. 캡처된 credential이나 raw
   personal data는 절대 복원하지 않는다.
7. upgrade 시에는 검토된 Dockerfile에서 rebuild하고, master 하나와 worker 하나를
   시작하여 별도로 승인된 소규모 canary를 실행한다. worker 등록에 실패하거나 통계가
   벌어지면 image/build 변경을 롤백한다. 시도 사이에는 Locust master와 worker를 중지 상태로 유지한다. 대상 애플리케이션을
   임의로 중지하지 않는다.

### 실패 유형별 판단

- `deadline_exceeded`(124)·`cancelled`(130): CSV는 멈춘 시점까지의 집계다. 목표 시간을
  채운 결과로 보고하지 않는다.
- master 비정상 종료(137 등): CSV는 마지막 주기 저장본이다. worker가 남아 있을 수 있으니
  project가 내려갔는지 확인한다.
- worker 탈락: master 종료 코드는 0일 수 있다. 실행 전후 worker 수를 비교한다.
- worker 부족: `LAB_LOCUST_EXPECT_WORKERS_MAX_WAIT` 안에 다 붙지 않으면 master가 부하 없이
  non-zero로 끝난다.

격리 재현은 다음 harness가 맡는다.

```bash
python3 examples/operations/locust-telemetry/lifecycle.py \
  --locust-image '<approved-locust@sha256:digest>' \
  --mock-image '<approved-wiremock@sha256:digest>'
```

### 시나리오 보존과 업그레이드

Locust에는 application database가 없다. Bind-backed scenario/result directory가
유일한 local persistent scope다. Test가 쓰고 있지 않을 때만 ordinary file로
backup한다. 시나리오가 Git에 추적되는지 확인하고, 추적되지 않으면 검토본·해시·복구본의 소유자를
별도로 기록한다. 호스트 bind를 사용한다는 사실만으로 Git 추적을 보장하지 않는다. Locust 또는
dependency upgrade 전에 isolated run에서 scenario syntax를 validate하고, 작은
승인된 canary를 실행한 뒤 worker registration과 aggregate metrics를 비교한다.
이 documentation task에서는 backup, restore, load execution을 수행하지 않았다.

## Verification

명령 종료·시각·설정 커밋·시나리오 digest·worker 수·정제된 집계·대상 SLI와 최종
중지/실행 상태를 기록한다.

### 확인 항목

- Master UI health가 성공하고 예상 worker count가 등록된다.
- 별도로 승인된 canary가 지정된 target SLI 범위 내에 머문다.
- 최종 full run은 명시적으로 승인되었거나 Locust가 중지 상태로 남아 있다.
- scenario/result restore와 upgrade rehearsal은 Task가 protected path, command,
  관찰된 결과를 기록할 때까지 **미실행** 상태로 남는다.

## Rollback and Escalation

### Rollback or Recovery

Locust를 중지하고, 이전에 검토된 scenario/build를 격리된 상태로 복원한 뒤, static
validation과 소규모 승인된 canary를 반복한다. 이 런북의 어떤 조치도 target service를
롤백하거나 target data를 복구하지 않는다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

load 중지 후에도 target health가 회복되지 않거나, worker가 healthy master에 등록되지
않거나, scenario provenance를 알 수 없거나, log/result에 secret이나 personal data가
나타날 때 escalation한다.

## Related Documents

### Traceability

- [Guide](../guides/0062-locust.md) (`GDE-0062`)
- [Policy](../policies/0062-locust.md) (`POL-0062`)
- [Locust LAB Compose](../../../labs/locust.yml)

- [Locust LAB Compose source](../../../labs/locust.yml)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Locust distributed mode](https://docs.locust.io/en/stable/running-distributed.html)
- [Operations index](../README.md)
