---
status: active
---
<!-- Target: docs/05.operations/runbooks/release-management.md -->

# Release Management Runbook

## Overview (KR)

이 런북은 `hy-home.docker`의 수동 release/tag readiness, evidence capture, rollback evidence 확인 절차를 정의한다. 이 문서는 배포 자동화, GitHub branch protection, required check, Docker runtime, secret, `.env`, port, permission 동작을 변경하지 않는다.

## When to Use

- Release 또는 tag 생성 전에 local documentation, validation, changelog readiness를 확인해야 할 때.
- PR 또는 local branch가 release candidate로 승격되기 전에 어떤 evidence를 남겨야 하는지 확인할 때.
- Rollback 가능성을 주장하기 전에 실제로 남겨야 할 local evidence를 확인해야 할 때.

## Procedure

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

6. Capture release readiness evidence in the relevant execution task or PR description. Do not paste secret values, `.env` values, raw logs containing credentials, shell history, or deployment tokens.

## Evidence

- Current branch and clean/expected working-tree state.
- Diff summary and `git diff --check` result.
- Repo contract, doc traceability, LLM Wiki freshness, and Compose validation results.
- Changelog or commit-range evidence used for the release/tag decision.
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
- [Operations template](../../99.templates/operation.template.md)
