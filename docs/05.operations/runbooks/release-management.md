---
status: active
---
<!-- Target: docs/05.operations/runbooks/release-management.md -->

# Release Management Runbook

## Overview (KR)

이 런북은 `hy-home.docker`의 수동 release/tag readiness, evidence capture, rollback evidence 확인 절차를 정의한다. 이 문서는 배포 자동화, GitHub branch protection, required check, Docker runtime, secret, `.env`, port, permission 동작을 변경하지 않는다.

## Release Management Runbook Procedure

> Scope: Release Management Runbook operational execution

### Purpose

- Release Management Runbook 작업을 반복 가능하고 검증 가능한 절차로 수행한다.
- 실행 전후 evidence, rollback 또는 escalation 기준을 명확히 남긴다.

### Canonical References

- [Operations index](../README.md)
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

## Rollback or Recovery

- Use only rollback or recovery steps that are already documented for the affected service, workflow, or deployment surface.
- N/A for a generic release rollback command: this runbook does not validate a universal rollback procedure for every Compose service.
- If a release/tag decision is blocked or rollback evidence is incomplete, stop the release decision and escalate with the evidence listed above.

## Escalation

- Escalate to the repository owner or responsible operator before creating tags, pushing release branches, changing branch protection, changing required checks, deploying, or mutating runtime state.
- Escalate immediately if validation output suggests secret exposure, `.env` drift requiring value-bearing changes, or rollback evidence that cannot be corroborated from tracked docs.

## Related Documents

- [Operations index](../README.md)
- [Runbooks index](./README.md)
- [LLM Wiki maintenance runbook](./llm-wiki-maintenance.md)
- [Execution plans](../../04.execution/plans/README.md)
- [Execution tasks](../../04.execution/tasks/README.md)
