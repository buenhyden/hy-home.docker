---
status: active
artifact_id: runbook-0009
artifact_type: runbook
parent_ids: []
created: 2026-06-04
updated: 2026-08-11
---
<!-- Target: docs/05.operations/00-workspace/ops-0009-release-management/runbook.md -->

# Release Management Runbook

## Overview

이 런북은 `hy-home.docker`의 수동 release/tag readiness, evidence capture, rollback evidence 확인 절차를 정의한다. 이 문서는 배포 자동화, GitHub branch protection, required check, Docker runtime, secret, `.env`, port, permission 동작을 변경하지 않는다.

## Release Management Runbook Procedure

> Scope: Release Management Runbook operational execution

### Purpose

- Release Management Runbook 작업을 반복 가능하고 검증 가능한 절차로 수행한다.
- 실행 전후 evidence, rollback 또는 escalation 기준을 명확히 남긴다.

### Canonical References

- [Operations index](../../README.md)
- **Policy**: N/A — no upstream source
- **Guide**: N/A — no upstream source

## When to Use

- Release 또는 tag 생성 전에 local documentation, validation, changelog readiness를 확인해야 할 때.
- PR 또는 local branch가 release candidate로 승격되기 전에 어떤 evidence를 남겨야 하는지 확인할 때.
- Rollback 가능성을 주장하기 전에 실제로 남겨야 할 local evidence를 확인해야 할 때.

## Procedure

### Checklist

- [ ] 관련 policy, guide, runbook handoff를 확인한다.
- [ ] 현재 상태와 변경 범위를 기록한다.

1. Confirm the release candidate branch and intended base branch.

   ```bash
   git status --short --branch
   git branch --show-current
   ```

2. Review the scoped branch diff before release/tag decisions.

   ```bash
   git diff --stat
   git diff --check
   ```

3. Confirm local repository documentation and validation gates relevant to the release candidate.

   ```bash
   bash scripts/validation/check-repo-contracts.sh
   bash scripts/validation/check-doc-traceability.sh
   bash scripts/knowledge/generate-llm-wiki-index.sh --check
   ```

4. Confirm Compose readiness without starting or stopping runtime services.

   ```bash
   bash scripts/validation/validate-docker-compose.sh --preflight
   bash scripts/validation/validate-docker-compose.sh
   ```

5. Confirm changelog and tag readiness from tracked release surfaces.

   ```bash
   git log --oneline --decorate -n 20
   git tag --list
   ```

   Before pushing a `v*.*.*` tag, confirm `CHANGELOG.md` already contains the
   exact release tag string. The repository tag workflow fails when the pushed
   tag is missing from `CHANGELOG.md`.

   ```bash
   rg -n "vX.Y.Z" CHANGELOG.md
   ```

6. Confirm release-readiness checklist items before any release or deploy claim.

   - Backup evidence or an explicit N/A rationale for every affected stateful surface.
   - Affected rollback or recovery runbook link for every changed service, workflow, or deployment surface.
   - Incident record path or escalation channel for blocked, failed, or rolled-back release decisions.
   - Remote gate verification evidence before claiming branch protection, required checks, or release workflow enforcement is current.

7. Capture release readiness evidence in the relevant execution task or PR description. Do not paste secret values, `.env` values, raw logs containing credentials, shell history, or deployment tokens.

8. `sample-web-service`의 local promotion/rollback 계약을 확인할 때는 먼저
   Docker를 시작하지 않는 fixture-only preflight를 실행한다.

   ```bash
   bash scripts/operations/rehearse-sample-service-delivery.sh preflight --task-id 2026-07-19-dre --baseline-verdict tests/fixtures/sample-service-delivery/spec126-verdict.baseline.accepted.json --candidate-verdict tests/fixtures/sample-service-delivery/spec126-verdict.candidate.accepted.json
   ```

   `evidence=fixture-contract-only`, `readiness=passed`,
   `recovery_boundary=passed`, `compose=passed`, `ports=18080,18081`이 모두
   있어야 한다. Fixture verdict는 실제 실행 승인이 아니다.

9. 실제 local rehearsal은 다음 canonical Spec 126 파일 세 개가 모두 존재하고,
   verdict schema v2와 pair schema/generation v3 계약을 통과할 때만 실행한다.

   ```text
   _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json
   _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json
   _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.pair.json
   ```

   Verdict v2는 OCI manifest/config/archive, deterministic Docker-load archive,
   deterministic local image reference, runtime image ID/kind의 전체 tuple을
   포함한다. Pair v3 (`hyhome-verification-verdict-pair-v3`)는 두 verdict의
   exact byte hash와 role별 전체 tuple을 고정한다. 하나라도 없거나 legacy,
   stale, mixed, substituted이면 class `10`에서 중단하며 Docker/Compose 호출,
   project, record를 만들지 않는다. 현재 Spec 126 accepted pair는 존재하며,
   승인된 Task 5 positive promotion 및 injected rollback 순서는 완료되었다.
   현재 실행 상태와 정확한 project, timestamp, record hash/inode, cleanup
   증거는
   Deployment/release Task가
   소유한다. 과거 14-Critical 결과와 missing-seed 결과는 superseded
   history이며 현재 blocker가 아니다.

10. 승인된 Task 5 runtime은 positive `rehearse` 후 injected-rollback
    `rehearse` 순서로 정확히 한 번씩 완료되었다. Baseline/canary는
    `hyhome-dre-20260719-<decimal-pid>-baseline|canary`, loopback
    `18080`/`18081`, exact ownership labels로 제한된다. Canary 실패 시 previous
    runtime image ID와 baseline health를 확인한 뒤 in-process cleanup한다.
    시작 전 deterministic local ref의 `.Id`와 role label을 verdict의 값과
    비교하고, 시작 후 container `.Image`를 같은 runtime ID와 비교한다. Merged
    topology에는 build path가 없고 `pull_policy: never`, `--pull never`,
    `--no-build`가 필수다. 각 run은 cleanup 후 schema-v4 record를 publish한다.
    Canonical record가 하나이므로 positive record hash/요약 필드를 먼저 Task에
    기록한 다음 negative run이 이를 교체했다. Standalone `cleanup --task-id`는
    interrupted/partial exact owned pair를 위한 rescue-only 명령이며 성공 run
    후에는 실행하지 않는다. 이미 cleanup된 상태에서는 의도대로 class `60`을
    반환한다. Stateful impact는 즉시 Spec 125로 handoff한다. 이 런북은 완료된
    sequence의 재실행을 승인하지 않는다. 재실행이 필요하면 새 Stage 04 승인과
    실행 evidence 계약을 먼저 작성한다.

### Steps

1. 이 runbook의 trigger와 checklist를 확인한다.
2. 기존 절차가 문서에 포함되어 있으면 그 순서대로 수행한다.
3. 실행 중 생성된 명령 출력과 판단 근거를 evidence로 남긴다.
4. 검증 실패, secret exposure 위험, 파괴적 변경 필요 시 즉시 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- [ ] 관련 validation script 또는 수동 확인을 실행한다.
- [ ] 변경 결과가 policy, guide, runbook handoff와 충돌하지 않는지 확인한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 runbook 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Current branch and clean/expected working-tree state.
- Diff summary and `git diff --check` result.
- Repo contract, doc traceability, LLM Wiki freshness, and Compose validation results.
- Changelog tag-string evidence and commit-range evidence used for the release/tag decision.
- Backup or N/A rationale, affected rollback/recovery links, incident path, and remote gate verification evidence when a release/deploy claim depends on those controls.
- Explicit statement that no runtime deployment, secret value mutation, `.env` sync, port, permission, or remote branch-protection change was performed unless separately approved.
- Local delivery evidence에는 revision, digest/verdict reference, project,
  full portable identity tuple의 concise fields, marker presence, decision,
  `data_impact=none`, cleanup, schema-v4 record hash만 기록한다. HTTP body,
  runtime log, secret, credential, token은 기록하지 않는다.
- 현재 canonical local-delivery record는 injected-negative 결과이며, positive
  record의 교체 전 hash/inode와 negative record의 교체 후 hash/inode는
  Deployment/release Task에서
  확인한다. 이 상태 확인은 rehearsal 재실행 지시가 아니다.

## Rollback or Recovery

- Use only rollback or recovery steps that are already documented for the affected service, workflow, or deployment surface.
- N/A for a generic release rollback command: this runbook does not validate a universal rollback procedure for every Compose service.
- If a release/tag decision is blocked or rollback evidence is incomplete, stop the release decision and escalate with the evidence listed above.
- Local delivery cleanup의 project/resource ownership query가 누락되거나
  ambiguous하면 broad cleanup을 시도하지 말고 class `60`으로 중단한다.
- In-process cleanup은 exact all-versus-owned container/network ID, 단일
  cardinality, zero volume을 확인한 뒤 그 ID만 직접 제거한다. Standalone
  cleanup은 pair가 absent/incomplete/additional/nonmatching이면 destructive
  call 없이 class `60`으로 중단한다.

## Escalation

- Escalate to the repository owner or responsible operator before creating tags, pushing release branches, changing branch protection, changing required checks, deploying, or mutating runtime state.
- Escalate immediately if validation output suggests secret exposure, `.env` drift requiring value-bearing changes, or rollback evidence that cannot be corroborated from tracked docs.

## Related Documents

- [Operations index](../../README.md)
- [Runbooks index](../../README.md)
- [LLM Wiki maintenance runbook](../ops-0007-llm-wiki-maintenance/runbook.md)
- [Execution plans](../../../03.specs/README.md)
- [Execution tasks](../../../03.specs/README.md)
- Deployment/release Task
- Spec 127
