---
title: "09-Tooling Optimization Hardening Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "operations"
artifact_id: "RUN-0063"
parent_ids:
- "GDE-0063"
created: "2026-05-17"
---
<!-- Target: docs/05.operations/catalog/09-tooling/0063-optimization-hardening/runbook.md -->

# 09-Tooling Optimization Hardening Runbook

## Overview

> Scope: restore the documented hardening baseline for optional `09-tooling` compose leaves.

이 런북은 `09-tooling` 하드닝 회귀가 의심될 때 사용한다. 공개 경계 SSO 체인, `infra_net` external 경계, Locust worker healthcheck, k6 wrapper volume 계약, 문서/검증 링크를 current-truth 기준으로 복구한다.

### Purpose

service-local compose 단독 검증과 root optional context를 혼동하지 않고, 현재 구현에 맞는 하드닝 기준선을 재확인한다.

## When to Use

- `infrastructure-hardening` CI or local hardening check fails for `09-tooling`.
- SonarQube/Terrakube/Syncthing middleware chain drifts.
- Locust worker healthcheck or command contract drifts.
- k6 wrapper volume or service-name documentation drifts.
- Active docs reintroduce service-local standalone config claims for optional tooling leaves.

## Procedure

### Checklist

- [ ] Failure category를 middleware, network, healthcheck, volume, docs, script 중 하나로 분류한다.
- [ ] 최근 변경 커밋과 affected files를 확인한다.
- [ ] root `docker-compose.yml`의 09-tooling includes가 optional/commented 상태인지 확인한다.

### Steps

1. 하드닝 기준선을 실행한다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 09-tooling
   ```

2. 문서 계약과 stale literal guard를 실행한다.

   ```bash
   python3 scripts/validation/run-ci-gate.py --profile changed
   python3 scripts/validation/check-document-links.py --mode alignment
   ```

3. 증상별로 복구한다.
   - Middleware drift: SonarQube/Terrakube/Syncthing 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 복원한다.
   - Network drift: tooling compose의 `infra_net` external 선언을 복원한다.
   - Locust drift: `locust-worker` command와 worker process healthcheck를 복원한다.
   - k6 drift: `k6-master` service name과 `k6-data:/mnt/locust:rw` volume 계약을 복원한다.
   - Documentation drift: active docs에서 없는 worker/route/version/service-local standalone claims를 제거한다.

4. 재검증한다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 09-tooling
   bash scripts/validation/check-template-security-baseline.sh
   python3 scripts/validation/check-document-links.py --mode traceability
   python3 scripts/validation/run-ci-gate.py --profile changed
   ```

### Verification Steps

- tooling hardening script 실패 0건.
- repo contracts 실패 0건.
- optimization-hardening guide/policy/runbook links가 guide, policy, runbook 각각의 목적 bucket을 가리킨다.
- optional tooling leaf runtime 검증은 root network/secret/dependency context 필요성이 문서화되어 있다.

### Observability and Evidence Sources

- **Logs**: CI `infrastructure-hardening`, local validation output, related service logs when runtime was approved.
- **Metrics**: N/A for docs-only hardening; runtime rehearsal metrics are separate evidence.
- **Evidence to Capture**: failed check, changed files, before/after hardening result, doc link scan result.

### Safe Rollback or Recovery Procedure

1. 문서-only 회귀는 직전 diff 단위로 되돌리거나 current-truth 문서로 정정한다.
2. compose/script 회귀는 affected file만 최소 복구하고 hardening check를 재실행한다.
3. runtime 재시작은 이 런북 범위를 벗어나며 대상 service runbook과 사용자 승인을 따른다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: tooling 자동 변경 파이프라인 일시 중지에는 승인 필요.
- **Eval Re-run**: `check-all-hardening.sh 09-tooling`, `run-ci-gate.py`, `check-document-links.py --mode alignment`

## Evidence

- Capture command output, timestamps, failed check names, file diffs, and final pass state.
- Record root optional include context when compose rendering is part of the evidence.

## Rollback or Recovery

Use only the focused restore steps above. If service runtime, data mutation, or credential changes are required, stop and escalate under `## Escalation`.

## Escalation

Escalate to the tooling owner when hardening remains failed after focused restore, secret exposure risk appears, optional root context cannot be reconstructed, or runtime service changes are required.

## Traceability

- Declared parent: [09-Tooling Optimization Hardening Usage Guide](guide.md) (`GDE-0063`)
- Governing authority: [Tooling Tier Architecture Description](../../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- Subject peers: [Guide](guide.md) (`GDE-0063`), [Policy](policy.md) (`POL-0063`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
