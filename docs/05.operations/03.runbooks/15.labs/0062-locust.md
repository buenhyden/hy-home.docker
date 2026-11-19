---
title: "Locust Recovery Runbook"
version: "1.4.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0062"
parent_ids:
- "GDE-0062"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Locust Recovery Runbook

## Trigger and Scope

### Trigger

Locust LAB 실행 중 target 상태가 나빠지거나 worker 연결이 끊길 때 부하를 멈추고 진단하는 절차다.
시나리오 파일 복구와 승인된 upgrade canary도 다룬다.

test 중 target health가 저하되거나, worker 연결이 끊기거나, headless master가 실패하거나,
scenario file이 손상되거나, Locust image/dependency upgrade에 승인된 canary가 필요할 때
사용한다.

### Targets

- [Guide](../../01.guides/15.labs/0062-locust.md) (`GDE-0062`)
- [Policy](../../02.policies/15.labs/0062-locust.md) (`POL-0062`)
- [Locust LAB Compose](../../../../labs/locust/docker-compose.yml)

- [Locust LAB Compose source](../../../../labs/locust/docker-compose.yml)
- [Derived Compose image projection](../../../../infra/tech-stack.versions.json)
- [Locust distributed mode](https://docs.locust.io/en/stable/running-distributed.html)
- [Operations index](../../README.md)

## Preflight

### Authority

저장소 루트에서 실행한다. 정적 render는 `labs/.env.example`와 합성 경로만 사용한다.
실제 진단·정지는 승인된 Docker context, `hy-home-lab-locust` project와 실행 당시
입력을 확인한 뒤에만 한다. `LAB_ENV_FILE`은 그 실행에 사용한 LAB 환경 파일 경로다.
필요한 환경 입력과 경로는 승인된 실행 도구가 주입하며 값은 증거에 남기지 않는다.

### Environment

읽기 전용 사전 점검은 Steps의 1단계(target·users·scenario digest 기록), 3단계(bounded status와 로그), 4단계(`config --quiet`와 master health failure 점검)이다. 시나리오 backup과 upgrade 전 점검은 다음과 같다.

#### 시나리오 보존과 업그레이드

Locust에는 application database가 없다. Bind-backed scenario/result directory가
유일한 local persistent scope다. Test가 쓰고 있지 않을 때만 ordinary file로
backup한다. 시나리오가 Git에 추적되는지 확인하고, 추적되지 않으면 검토본·해시·복구본의 소유자를
별도로 기록한다. 호스트 bind를 사용한다는 사실만으로 Git 추적을 보장하지 않는다. Locust 또는
dependency upgrade 전에 isolated run에서 scenario syntax를 validate하고, 작은
승인된 canary를 실행한 뒤 worker registration과 aggregate metrics를 비교한다.
이 documentation task에서는 backup, restore, load execution을 수행하지 않았다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | target, users, spawn rate, duration, worker count, scenario digest, 처음 실패한 target SLI 기록 | 문서에 기록 없음 | cookie/token/response body는 수집하지 않으며 예상 밖이면 중단 |
| 2 | 진단 전 load 중지 (`lab.py run` 제어기에 종료 신호, 종료됐다면 `lab.py down locust`) | 제어기가 master를 grace 기간 동안 멈추고 project를 내림 | 대상 service와 project identity를 확인한 경우에만 Compose `stop` 사용 |
| 3 | 실제 project의 bounded status와 남은 컨테이너 로그 확인 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 target owner에게 escalation |
| 4 | 합성 입력으로 현재 source를 렌더링하고 master/worker 실패 원인 점검 | `config --quiet`가 성공 | target SLI가 회복되지 않았으면 Locust를 중지한 채 target owner에게 보고 |
| 5 | 승인된 canary를 별도 `LAB_CANARY_ENV_FILE`로 render 후 새 제어기 실행 시작 | render 성공, 대상과 한도가 승인값과 일치 | 일치하지 않으면 실행하지 않으며 중지 상태 유지 후 target owner에게 escalation |
| 6 | scenario 복구: 두 service 중지 상태에서 scenario 디렉터리를 quarantine path로 복사, 검토된 파일 복원, hash 비교 후 교체 | hash 비교 일치 | credential이나 raw personal data는 복원하지 않으며 불일치 시 교체하지 않음 |
| 7 | upgrade: 검토된 Dockerfile에서 rebuild 후 5단계의 소규모 canary 실행 | 문서에 기록 없음 | worker 등록 실패 또는 통계가 벌어지면 image/build 변경을 롤백하고 Locust를 중지 상태로 유지 |

1. target, users, spawn rate, duration, worker count, scenario digest, 그리고 처음
   실패한 target SLI를 기록한다. cookie, token, response body는 수집하지 않는다.
2. 진단 전에 load를 중지한다. `lab.py run`으로 시작한 실행이면 제어기에 종료 신호
   (대화형 터미널에서는 `Ctrl-C`)를 보낸다. 제어기가 master를 grace 기간 동안 멈추고 project를 내린다.
   제어기가 이미 종료됐다면 `python3 scripts/operations/lab.py --env-file "$LAB_ENV_FILE" down locust`를 쓴다.
   아래 Compose 명령은 제어기 없이 시작했고 대상 service와 project identity를 확인한 경우에만 쓴다.

   ```bash
   docker compose --project-name hy-home-lab-locust --env-file "$LAB_ENV_FILE" -f labs/locust/docker-compose.yml --profile lab-locust stop lab-locust-master lab-locust-worker
   ```

3. 실제 project의 bounded status와 남아 있는 컨테이너의 로그를 확인한다.

   ```bash
   docker compose --project-name hy-home-lab-locust --env-file "$LAB_ENV_FILE" -f labs/locust/docker-compose.yml --profile lab-locust ps -a lab-locust-master lab-locust-worker
   docker compose --project-name hy-home-lab-locust --env-file "$LAB_ENV_FILE" -f labs/locust/docker-compose.yml --profile lab-locust logs --tail=200 lab-locust-master lab-locust-worker
   ```

4. 합성 입력으로 현재 source를 렌더링한다. master와 worker의 실패 원인을 실제 기록에서
   점검한다. target SLI가 회복되지 않았으면 Locust를 중지한 채 target owner에게 보고한다.

   ```bash
   LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result \
   docker compose --env-file labs/.env.example -f labs/locust/docker-compose.yml --profile lab-locust config --quiet
   ```

5. 대상과 새 canary가 승인되면 기존 실행과 다른 `LAB_CANARY_ENV_FILE`을 사용한다.
   이 파일에는 검토된 scenario, 비어 있는 새 result directory, 승인된 최소 users·spawn rate·run time·
   worker 수를 설정한다. 실행 환경에서 해당 설정을 덮어쓰는 상속 변수를 제거한다.
   같은 canary 입력으로 render가 성공하고 대상과 한도가 승인값과 일치할 때만 새 제어기 실행을 시작한다.
   목적·lease·deadline은 각 승인값이다.

   ```bash
   docker compose --project-name hy-home-lab-locust --env-file "$LAB_CANARY_ENV_FILE" -f labs/locust/docker-compose.yml --profile lab-locust config --quiet &&
     python3 scripts/operations/lab.py --env-file "$LAB_CANARY_ENV_FILE" run locust --purpose "$LAB_PURPOSE" --lease "$LAB_LEASE" --deadline "$LAB_DEADLINE"
   ```

6. scenario 복구 시에는 두 service를 모두 중지한 상태로 두고, 현재 bind-backed scenario
   디렉터리를 protected quarantine path로 복사하고, 검토된 파일을 별도 디렉터리로
   복원하고, hash를 비교한 뒤에만 active file을 교체한다. 캡처된 credential이나 raw
   personal data는 절대 복원하지 않는다.
7. upgrade 시에는 검토된 Dockerfile에서 rebuild하고, 승인된 worker 수로 5단계의
   소규모 canary를 실행한다. worker 등록에 실패하거나 통계가
   벌어지면 image/build 변경을 롤백한다. 시도 사이에는 Locust master와 worker를 중지 상태로 유지한다. 대상 애플리케이션을
   임의로 중지하지 않는다.

#### 실패 유형별 판단

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

### Stop Conditions

target SLI가 회복되지 않았으면 Locust를 중지 상태로 두고 target owner에게 escalation한다. worker 등록에 실패하거나 통계가 벌어지면 image/build 변경을 롤백하고, 시도 사이에는 Locust master와 worker를 중지 상태로 유지한다.

## Verification

### Expected Results

#### Service Checks

- Headless master의 TCP healthcheck가 성공하고 예상 worker count가 등록된다.
- 별도로 승인된 canary가 지정된 target SLI 범위 내에 머문다.
- 최종 full run은 명시적으로 승인되었거나 Locust가 중지 상태로 남아 있다.
- scenario/result restore와 upgrade rehearsal은 Task가 protected path, command,
  관찰된 결과를 기록할 때까지 **미실행** 상태로 남는다.

#### Evidence

명령 종료·시각·설정 커밋·시나리오 digest·worker 수·정제된 집계·대상 SLI와 최종
중지/실행 상태를 기록한다.

### Unverified Conditions

이 runbook이 아직 관찰하지 못한 항목은 다음과 같다. 문서는 일부 항목을 Task가 기록할 때까지 미실행 상태로 둔다고 적고 있다.

- scenario/result restore와 upgrade rehearsal: 문서는 이 둘을 Task가 protected path, command, 관찰된 결과를 기록할 때까지 미실행 상태로 둔다고 적고 있다. 해당 기록이 관찰되면 검증된다.
- 승인된 canary 실행: 새 제어기 실행은 대상과 canary 승인이 필요하며 이 문서에는 실행 결과가 기록되어 있지 않다. canary가 target SLI 범위 안에 머무는 것이 관찰되면 검증된다.
- 최종 full run: 명시적 승인이 필요하며 그렇지 않으면 Locust가 중지 상태로 남아야 한다. 승인 기록 또는 중지 상태가 관찰되면 검증된다.
- headless master TCP healthcheck와 예상 worker count 등록: 이 문서에는 실행 결과가 기록되어 있지 않다.
- 격리 재현 harness(`lifecycle.py`): 실행 결과가 기록되어 있지 않다.

## Escalation

### Next Owner

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

load 중지 후에도 target health가 회복되지 않거나, worker가 healthy master에 등록되지
않거나, scenario provenance를 알 수 없거나, log/result에 secret이나 personal data가
나타날 때 escalation한다.

### Recovery or Forward Repair

Locust를 중지하고, 이전에 검토된 scenario/build를 격리된 상태로 복원한 뒤, static
validation과 소규모 승인된 canary를 반복한다. 이 런북의 어떤 조치도 target service를
롤백하거나 target data를 복구하지 않는다.
