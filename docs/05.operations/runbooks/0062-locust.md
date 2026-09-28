---
title: "Locust Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0062"
parent_ids:
- "GDE-0062"
created: "2026-05-17"
---

# Locust Recovery Runbook

## When to Use

test 중 target health가 저하되거나, worker가 연결이 끊기거나, master UI가 실패하거나,
scenario file이 손상되거나, Locust image/dependency upgrade에 승인된 canary가 필요할 때
사용한다. 모든 command는 저장소 루트에서 실행한다.

## Procedure

1. target, users, spawn rate, duration, worker count, scenario digest, 그리고 처음
   실패한 target SLI를 기록한다. cookie, token, response body는 수집하지 않는다.
2. 진단 전에 load를 중지한다.

   ```bash
   docker compose --profile testing stop locust-worker locust-master
   ```

3. bounded status와 로그를 캡처한다.

   ```bash
   docker compose --profile testing ps locust-master locust-worker
   docker compose --profile testing logs --tail=200 locust-master locust-worker
   ```

4. `docker compose --profile testing config --quiet`로 확인한다. worker를 재생성하기
   전에 master health failure를 점검한다. target SLI가 회복되지 않았으면 Locust를
   중지 상태로 두고 target owner에게 escalation한다.
5. master가 healthy이고 재시작이 승인되면 master를 먼저 시작하고 worker를 시작한다.

   ```bash
   docker compose --profile testing up -d locust-master
   docker compose --profile testing up -d locust-worker
   ```

6. scenario 복구 시에는 두 service를 모두 중지한 상태로 두고, 현재 bind-backed scenario
   디렉터리를 protected quarantine path로 복사하고, 검토된 파일을 별도 디렉터리로
   복원하고, hash를 비교한 뒤에만 active file을 교체한다. 캡처된 credential이나 raw
   personal data는 절대 복원하지 않는다.
7. upgrade 시에는 검토된 Dockerfile에서 rebuild하고, master 하나와 worker 하나를
   시작하여 별도로 승인된 소규모 canary를 실행한다. worker 등록에 실패하거나 통계가
   벌어지면 image/build 변경을 롤백한다. 시도 사이에는 target을 중지 상태로 유지한다.

### Verification Steps

- Master UI health가 성공하고 예상 worker count가 등록된다.
- 별도로 승인된 canary가 지정된 target SLI 범위 내에 머문다.
- 최종 full run은 명시적으로 승인되었거나 Locust가 중지 상태로 남아 있다.
- scenario/result restore와 upgrade rehearsal은 Task가 protected path, command,
  관찰된 결과를 기록할 때까지 **미실행** 상태로 남는다.

## Evidence

command exit, timestamp, configuration commit, scenario digest, worker count,
sanitized aggregate, target SLI, 최종 stopped/running 상태를 기록한다.

## Rollback or Recovery

Locust를 중지하고, 이전에 검토된 scenario/build를 격리된 상태로 복원한 뒤, static
validation과 소규모 승인된 canary를 반복한다. 이 런북의 어떤 조치도 target service를
롤백하거나 target data를 복구하지 않는다.

## Escalation

load 중지 후에도 target health가 회복되지 않거나, worker가 healthy master에 등록되지
않거나, scenario provenance를 알 수 없거나, log/result에 secret이나 personal data가
나타날 때 escalation한다.

## Traceability

- [Guide](../guides/0062-locust.md) (`GDE-0062`)
- [Policy](../policies/0062-locust.md) (`POL-0062`)
- [Locust Compose](../../../infra/09-tooling/locust/docker-compose.yml)

## Related Documents

- [Locust Compose source](../../../infra/09-tooling/locust/docker-compose.yml)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Locust distributed mode](https://docs.locust.io/en/stable/running-distributed.html)
- [Operations index](../README.md)
