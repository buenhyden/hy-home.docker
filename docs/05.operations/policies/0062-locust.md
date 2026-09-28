---
title: "Locust Operations Policy"
version: "1.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0062"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Locust Operations Policy

## Overview

Locust는 명시적인 `testing` capability다. HOME이나 broad tooling
startup에는 절대 포함되지 않는다. 이 정책은 test target을 보호하고 검토되지
않은 load, credential capture, 오해를 부르는 performance evidence를
막는다.

## Policy Scope

`locust-master`와 `locust-worker` service, bind-backed scenario
디렉터리, target authorization, result handling, scaling, image upgrade.

## Controls

- **Activation:** `testing` profile만 선택하고 Locust service를
  명시한다. 모든 run은 target owner, duration, user/spawn limit, worker
  count, abort SLI, stop owner를 기록한다. repository에 정의된 generic
  RPS threshold나 maintenance window는 없다.
- **Authorization:** target credential은 승인된 secret channel을
  사용하며 `locustfile.py`, Compose, log, 보관된 raw result에 내장할 수
  없다.
- **Data:** scenario와 result는 `locust-data` host path에 남는다.
  sanitized된 집계는 소유 Task/incident 아래에 보관한다; 명시적인
  evidence 필요가 없으면 payload나 identifier를 보관하지 않는다.
- **Resources:** worker scaling은 명시적이며 승인된 test로 제한된다.
  run 후 worker와 master를 중지한다; host 재시작 후 load를 재생하는
  restart 동작을 절대 추가하지 않는다.
- **Backup:** test가 중지된 동안에만 scenario/result 디렉터리를 복사한다.
  Repository-tracked scenario는 Git에서 복원한다; untracked result
  recovery는 overwrite 전에 별도 디렉터리에서 rehearse해야 한다.
- **Upgrade:** Locust/Python dependency의 release note를 검토하고,
  tracked Dockerfile에서 rebuild하며, 정상 test envelope을 복원하기 전에
  작은 승인된 canary를 실행한다.
- **Removal:** scenario ownership, 보관된 evidence, 모든 consumer가
  해결된 후에만 service를 제거한다. host 디렉터리 삭제는 별도의
  destructive action이다.

## Exceptions

모든 편차는 target, blast radius, expiry, stop condition, recovery
owner를 명시해야 한다. exception은 target authorization이나 secret
handling을 면제할 수 없다.

## Verification

Static Compose와 hardening check는 configuration만 증명한다. Runtime
evidence는 worker registration, target SLI, sanitized result, 최종
stopped state를 포함해야 한다.

## Review Cadence

profile, Dockerfile dependency, scenario storage, target network, scaling
동작이 변경될 때 검토한다.

## Traceability

- [Guide](../guides/0062-locust.md) (`GDE-0062`)
- [Runbook](../runbooks/0062-locust.md) (`RUN-0062`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)

## Related Documents

- [Locust Compose source](../../../infra/09-tooling/locust/docker-compose.yml)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Locust documentation](https://docs.locust.io/en/stable/)
- [Operations index](../README.md)
