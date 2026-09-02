---
title: Workspace Governance Simplification Migration
type: archive/migration
layer: archive
status: completed
owner: "@buenhyden"
artifact_id: MIG-0003
parent_ids: [ADR-0029]
created: 2026-08-20
updated: 2026-08-28
---

# Workspace Governance Simplification Migration

## Purpose

Record the executed path and authority changes. Git history owns the complete
previous bodies; this document is a lookup record, not current SDLC policy.

## Authority Change

Stage 00 owns shared policy and supported provider adapters. Stage 99 owns
document profiles, identities, lifecycle and templates. Registered scripts own
executable validation. Stages 01, 02, 03 and 05 own their current requirements,
architecture, behavior and operations; Stage 90 remains reference evidence.

## Path Mapping

The ordered mapping projects the historical approved selection onto actual
execution. Three unexecuted plans (r0842, r0848, r0852) are omitted: the metadata
CLI test, runtime rehearsal and unique hook-parity report remain current.
Task 11 commit `f042bc1e26cfb9169c94baa0ff4ac2269a0a6953` records the actual
identity-test move; Task 12 commit `1c620dd079c1c28f5bea434f00093463e7764e1a`
records retained script ownership. Five Task targets use their canonical
`tasks/` paths. Terminal mappings record two helper and three session deletions.

```yaml
schema_version: 3
migration_id: mig-0003
rows:
- source_path: docs/03.specs/spec-0153-workspace-governance-simplification/spec.md
  target_path: docs/03.specs/0153-workspace-governance-simplification/spec.md
  artifact_id: SPEC-0153
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0153-workspace-governance-simplification/plan.md
  target_path: docs/03.specs/0153-workspace-governance-simplification/plan.md
  artifact_id: plan-0153
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0153-workspace-governance-simplification/task.md
  target_path: null
  artifact_id: task-0153-01
  action: delete
  recovery_commit: 71f89ba1430245c89d10c36a084fc2fae9cfe98b
- source_path: docs/00.agent-governance/rules/agentic.md
  target_path: docs/00.agent-governance/policies/agentic.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/approval-boundaries.md
  target_path: docs/00.agent-governance/policies/approval-boundaries.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/bootstrap.md
  target_path: docs/00.agent-governance/policies/bootstrap.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/documentation-protocol.md
  target_path: docs/00.agent-governance/policies/documentation-protocol.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/environment-constraints.md
  target_path: docs/00.agent-governance/policies/environment-constraints.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/git-workflow.md
  target_path: docs/00.agent-governance/policies/git-workflow.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/github-governance.md
  target_path: docs/00.agent-governance/policies/github-governance.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.block-absolute-file-link.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.block-absolute-file-link.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.block-direct-main-push.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.block-direct-main-push.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.block-gha-secrets-in-run.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.block-gha-secrets-in-run.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.block-git-no-verify.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.block-git-no-verify.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.block-plaintext-secret-compose.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.block-plaintext-secret-compose.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.block-unpinned-gha-action.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.block-unpinned-gha-action.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.enforce-docs-templates.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.enforce-docs-templates.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.require-logical-commits-before-stop.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.require-logical-commits-before-stop.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-branch-naming.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-branch-naming.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-conventional-commit.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-conventional-commit.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-docker-infra-stop.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-docker-infra-stop.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-force-push.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-force-push.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-governance-memory-edit.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-governance-memory-edit.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-hook-parity-edit.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-hook-parity-edit.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-korean-in-governance.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-korean-in-governance.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-parallel-doc-file.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-parallel-doc-file.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-post-edit-style-automation.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-post-edit-style-automation.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-pre-commit-manual.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-pre-commit-manual.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/hooks/hookify.warn-stage-doc-edit.md
  target_path: docs/00.agent-governance/policies/hooks/hookify.warn-stage-doc-edit.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/jit-markers.md
  target_path: docs/00.agent-governance/policies/jit-markers.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/output-style.md
  target_path: docs/00.agent-governance/policies/output-style.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/persona.md
  target_path: docs/00.agent-governance/policies/persona.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/postflight-checklist.md
  target_path: docs/00.agent-governance/policies/postflight-checklist.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/provider-capability-matrix.md
  target_path: docs/00.agent-governance/policies/provider-capability-matrix.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/quality-standards.md
  target_path: docs/00.agent-governance/policies/quality-standards.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/stage-authoring-matrix.md
  target_path: docs/00.agent-governance/policies/stage-authoring-matrix.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/standards.md
  target_path: docs/00.agent-governance/policies/standards.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/task-checklists.md
  target_path: docs/00.agent-governance/policies/task-checklists.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/rules/workflows.md
  target_path: docs/00.agent-governance/policies/workflows.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/agentic.md
  target_path: docs/00.agent-governance/roles/agentic.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/architecture.md
  target_path: docs/00.agent-governance/roles/architecture.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/common.md
  target_path: docs/00.agent-governance/roles/common.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/docs.md
  target_path: docs/00.agent-governance/roles/docs.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/infra.md
  target_path: docs/00.agent-governance/roles/infra.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/ops.md
  target_path: docs/00.agent-governance/roles/ops.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/qa.md
  target_path: docs/00.agent-governance/roles/qa.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/scopes/security.md
  target_path: docs/00.agent-governance/roles/security.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/ci-cd-engineer.md
  target_path: docs/00.agent-governance/roles/ci-cd-engineer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/code-reviewer.md
  target_path: docs/00.agent-governance/roles/code-reviewer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/doc-writer.md
  target_path: docs/00.agent-governance/roles/doc-writer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/drift-detector.md
  target_path: docs/00.agent-governance/roles/drift-detector.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/eval-engineer.md
  target_path: docs/00.agent-governance/roles/eval-engineer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/hook-developer.md
  target_path: docs/00.agent-governance/roles/hook-developer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/iac-reviewer.md
  target_path: docs/00.agent-governance/roles/iac-reviewer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/incident-responder.md
  target_path: docs/00.agent-governance/roles/incident-responder.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/infra-implementer.md
  target_path: docs/00.agent-governance/roles/infra-implementer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/qa-engineer.md
  target_path: docs/00.agent-governance/roles/qa-engineer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/rules-engineer.md
  target_path: docs/00.agent-governance/roles/rules-engineer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/security-auditor.md
  target_path: docs/00.agent-governance/roles/security-auditor.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/skill-creator.md
  target_path: docs/00.agent-governance/roles/skill-creator.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/agents/workflow-supervisor.md
  target_path: docs/00.agent-governance/roles/workflow-supervisor.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/adr-writing.md
  target_path: docs/00.agent-governance/skills/adr-writing.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/ci-cd-patterns.md
  target_path: docs/00.agent-governance/skills/ci-cd-patterns.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/code-review-dimensions.md
  target_path: docs/00.agent-governance/skills/code-review-dimensions.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/code-reviewer.md
  target_path: docs/00.agent-governance/skills/code-reviewer.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/compose-stack-agent.md
  target_path: docs/00.agent-governance/skills/compose-stack-agent.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/container-threat-modeling.md
  target_path: docs/00.agent-governance/skills/container-threat-modeling.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/deployment-pipeline-design.md
  target_path: docs/00.agent-governance/skills/deployment-pipeline-design.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/docker-compose-patterns.md
  target_path: docs/00.agent-governance/skills/docker-compose-patterns.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/e2e-testing.md
  target_path: docs/00.agent-governance/skills/e2e-testing.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/execution-plan-agent.md
  target_path: docs/00.agent-governance/skills/execution-plan-agent.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/incident-response.md
  target_path: docs/00.agent-governance/skills/incident-response.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/infra-cross-validate.md
  target_path: docs/00.agent-governance/skills/infra-cross-validate.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/infra-validate.md
  target_path: docs/00.agent-governance/skills/infra-validate.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/knowledge-map-agent.md
  target_path: docs/00.agent-governance/skills/knowledge-map-agent.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/ops-runbook-agent.md
  target_path: docs/00.agent-governance/skills/ops-runbook-agent.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/policy-gate-agent.md
  target_path: docs/00.agent-governance/skills/policy-gate-agent.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/project-memory-stewardship.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/provider-model-evaluation.md
  target_path: docs/00.agent-governance/skills/provider-model-evaluation.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/requirements-to-design-agent.md
  target_path: docs/00.agent-governance/skills/requirements-to-design-agent.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/security-audit.md
  target_path: docs/00.agent-governance/skills/security-audit.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/style-validation.md
  target_path: docs/00.agent-governance/skills/style-validation.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/task-breakdown-agent.md
  target_path: docs/00.agent-governance/skills/task-breakdown-agent.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/test-automator.md
  target_path: docs/00.agent-governance/skills/test-automator.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/functions/workspace-audit-revalidation.md
  target_path: docs/00.agent-governance/skills/workspace-audit-revalidation.md
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/ci-cd-engineer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/code-reviewer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/doc-writer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/drift-detector.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/eval-engineer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/hook-developer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/iac-reviewer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/incident-responder.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/infra-implementer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/qa-engineer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/rules-engineer.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/security-auditor.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/skill-creator.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/agents/workflow-supervisor.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/hooks/agent-event-hook.sh
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: .gemini/settings.json
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: GEMINI.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/agents/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/contracts/agent-catalog.yaml
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/contracts/agent-governance-artifacts.yaml
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/contracts/deferred-paths.yaml
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/contracts/provider-models.yaml
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/harness-implementation-map.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/agentic-harness-contract-hardening.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/current.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/direct-deletion-branch-unadopted-design.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/docker-doc-contract-backlog.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/execution-stage-legacy-debt.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/governance-memory-usage-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/harness-agent-first-gap-audit.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/ignored-sdd-scratch-deletion.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/operations-target-marker-contract-tension.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/progress.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/reviewer-checkout-destroyed-dirty-state.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/spec-136-migration-branch-preservation.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/stage-docs-lifecycle-audit.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/stop-gate-ignores-task-ownership.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/memory/worktree-consolidation-2026-08-18.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/providers/agents-md.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/providers/gemini.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/00.agent-governance/subagent-protocol.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/governance/memory.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/governance/progress.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0001-gateway.md
  target_path: docs/01.requirements/0001-gateway.md
  artifact_id: REQ-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0002-auth.md
  target_path: docs/01.requirements/0002-auth.md
  artifact_id: REQ-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0003-security.md
  target_path: docs/01.requirements/0003-security.md
  artifact_id: REQ-0003
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0004-data.md
  target_path: docs/01.requirements/0004-data.md
  artifact_id: REQ-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0005-data-analytics.md
  target_path: docs/01.requirements/0005-data-analytics.md
  artifact_id: REQ-0005
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0006-messaging.md
  target_path: docs/01.requirements/0006-messaging.md
  artifact_id: REQ-0006
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0007-observability.md
  target_path: docs/01.requirements/0007-observability.md
  artifact_id: REQ-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0008-workflow.md
  target_path: docs/01.requirements/0008-workflow.md
  artifact_id: REQ-0008
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0009-ai.md
  target_path: docs/01.requirements/0009-ai.md
  artifact_id: REQ-0009
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0010-tooling.md
  target_path: docs/01.requirements/0010-tooling.md
  artifact_id: REQ-0010
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0011-communication.md
  target_path: docs/01.requirements/0011-communication.md
  artifact_id: REQ-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0012-laboratory.md
  target_path: docs/01.requirements/0012-laboratory.md
  artifact_id: REQ-0012
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0013-ai-open-webui.md
  target_path: docs/01.requirements/0013-ai-open-webui.md
  artifact_id: REQ-0013
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0014-auth-optimization-hardening.md
  target_path: docs/01.requirements/0014-auth-optimization-hardening.md
  artifact_id: REQ-0014
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0015-security-optimization-hardening.md
  target_path: docs/01.requirements/0015-security-optimization-hardening.md
  artifact_id: REQ-0015
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0016-data-optimization-hardening.md
  target_path: docs/01.requirements/0016-data-optimization-hardening.md
  artifact_id: REQ-0016
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0017-messaging-optimization-hardening.md
  target_path: docs/01.requirements/0017-messaging-optimization-hardening.md
  artifact_id: REQ-0017
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0018-observability-optimization-hardening.md
  target_path: docs/01.requirements/0018-observability-optimization-hardening.md
  artifact_id: REQ-0018
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0019-workflow-optimization-hardening.md
  target_path: docs/01.requirements/0019-workflow-optimization-hardening.md
  artifact_id: REQ-0019
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0020-ai-optimization-hardening.md
  target_path: docs/01.requirements/0020-ai-optimization-hardening.md
  artifact_id: REQ-0020
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0021-tooling-optimization-hardening.md
  target_path: docs/01.requirements/0021-tooling-optimization-hardening.md
  artifact_id: REQ-0021
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0022-laboratory-optimization-hardening.md
  target_path: docs/01.requirements/0022-laboratory-optimization-hardening.md
  artifact_id: REQ-0022
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0023-standardize-infra-net.md
  target_path: docs/01.requirements/0023-standardize-infra-net.md
  artifact_id: REQ-0023
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0024-agent-governance-standardization.md
  target_path: docs/01.requirements/0024-agent-governance-standardization.md
  artifact_id: REQ-0024
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/01.requirements/prd-0025-operational-readiness-closure.md
  target_path: docs/01.requirements/0025-operational-readiness-closure.md
  artifact_id: REQ-0025
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0001-gateway-architecture.md
  target_path: docs/02.architecture/descriptions/0001-gateway-architecture.md
  artifact_id: AD-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0002-auth-architecture.md
  target_path: docs/02.architecture/descriptions/0002-auth-architecture.md
  artifact_id: AD-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0003-security-architecture.md
  target_path: docs/02.architecture/descriptions/0003-security-architecture.md
  artifact_id: AD-0003
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0004-data-architecture.md
  target_path: docs/02.architecture/descriptions/0004-data-architecture.md
  artifact_id: AD-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0005-messaging-architecture.md
  target_path: docs/02.architecture/descriptions/0005-messaging-architecture.md
  artifact_id: AD-0005
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0006-observability-architecture.md
  target_path: docs/02.architecture/descriptions/0006-observability-architecture.md
  artifact_id: AD-0006
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0007-workflow-architecture.md
  target_path: docs/02.architecture/descriptions/0007-workflow-architecture.md
  artifact_id: AD-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0008-ai-architecture.md
  target_path: docs/02.architecture/descriptions/0008-ai-architecture.md
  artifact_id: AD-0008
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0009-tooling-architecture.md
  target_path: docs/02.architecture/descriptions/0009-tooling-architecture.md
  artifact_id: AD-0009
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0010-communication-architecture.md
  target_path: docs/02.architecture/descriptions/0010-communication-architecture.md
  artifact_id: AD-0010
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0011-laboratory-architecture.md
  target_path: docs/02.architecture/descriptions/0011-laboratory-architecture.md
  artifact_id: AD-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0012-data-analytics-architecture.md
  target_path: docs/02.architecture/descriptions/0012-data-analytics-architecture.md
  artifact_id: AD-0012
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0013-open-webui-architecture.md
  target_path: docs/02.architecture/descriptions/0013-open-webui-architecture.md
  artifact_id: AD-0013
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0014-auth-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0014-auth-optimization-hardening-architecture.md
  artifact_id: AD-0014
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0018-security-optimization-hardening-architecture.md
  artifact_id: AD-0018
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0019-data-optimization-hardening-architecture.md
  artifact_id: AD-0019
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0020-messaging-optimization-hardening-architecture.md
  artifact_id: AD-0020
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0021-observability-optimization-hardening-architecture.md
  artifact_id: AD-0021
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0022-workflow-optimization-hardening-architecture.md
  artifact_id: AD-0022
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md
  artifact_id: AD-0023
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md
  artifact_id: AD-0024
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  target_path: docs/02.architecture/descriptions/0025-laboratory-optimization-hardening-architecture.md
  artifact_id: AD-0025
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0026-standardize-infra-net.md
  target_path: docs/02.architecture/descriptions/0026-standardize-infra-net.md
  artifact_id: AD-0026
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0027-agent-governance-canonical-adapter.md
  target_path: docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md
  artifact_id: AD-0027
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/descriptions/ad-0028-operational-readiness-closure.md
  target_path: docs/02.architecture/descriptions/0028-operational-readiness-closure.md
  artifact_id: AD-0028
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0001-traefik-nginx-hybrid.md
  target_path: docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md
  artifact_id: ADR-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0002-keycloak-oauth2-proxy-choice.md
  target_path: docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md
  artifact_id: ADR-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0003-vault-as-secrets-manager.md
  target_path: docs/02.architecture/decisions/0003-vault-as-secrets-manager.md
  artifact_id: ADR-0003
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0004-postgresql-ha-patroni.md
  target_path: docs/02.architecture/decisions/0004-postgresql-ha-patroni.md
  artifact_id: ADR-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0005-kafka-vs-rabbitmq-selection.md
  target_path: docs/02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md
  artifact_id: ADR-0005
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0006-lgtm-stack-selection.md
  target_path: docs/02.architecture/decisions/0006-lgtm-stack-selection.md
  artifact_id: ADR-0006
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0007-airflow-n8n-hybrid-workflow.md
  target_path: docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md
  artifact_id: ADR-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0008-ollama-openwebui-local-ai.md
  target_path: docs/02.architecture/decisions/0008-ollama-openwebui-local-ai.md
  artifact_id: ADR-0008
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0009-tooling-services.md
  target_path: docs/02.architecture/decisions/0009-tooling-services.md
  artifact_id: ADR-0009
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0010-communication-services.md
  target_path: docs/02.architecture/decisions/0010-communication-services.md
  artifact_id: ADR-0010
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0011-laboratory-services.md
  target_path: docs/02.architecture/decisions/0011-laboratory-services.md
  artifact_id: ADR-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0015-analytics-engine-selection.md
  target_path: docs/02.architecture/decisions/0015-analytics-engine-selection.md
  artifact_id: ADR-0015
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0016-open-webui-implementation.md
  target_path: docs/02.architecture/decisions/0016-open-webui-implementation.md
  artifact_id: ADR-0016
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0017-auth-hardening-runtime-and-fail-closed.md
  target_path: docs/02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md
  artifact_id: ADR-0017
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0018-vault-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0018
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0019-04-data-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0019
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0020-messaging-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0020
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0021-observability-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0021
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0022-workflow-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0022
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0023-ai-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0023
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0024-tooling-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0024
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0025-laboratory-hardening-and-ha-expansion-strategy.md
  target_path: docs/02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md
  artifact_id: ADR-0025
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0026-standardize-infra-net.md
  target_path: docs/02.architecture/decisions/0026-standardize-infra-net.md
  artifact_id: ADR-0026
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0027-stage-00-canonical-adapter-model.md
  target_path: docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md
  artifact_id: ADR-0027
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md
  target_path: docs/02.architecture/decisions/0028-local-isolated-readiness-evidence.md
  artifact_id: ADR-0028
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/02.architecture/decisions/adr-0029-workspace-governance-authority.md
  target_path: docs/02.architecture/decisions/0029-workspace-governance-authority.md
  artifact_id: adr-0029
  action: rename
  recovery_commit: 71f89ba1430245c89d10c36a084fc2fae9cfe98b
- source_path: docs/03.specs/spec-0001-gateway/spec.md
  target_path: docs/03.specs/0001-gateway/spec.md
  artifact_id: SPEC-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0002-auth/spec.md
  target_path: docs/03.specs/0002-auth/spec.md
  artifact_id: SPEC-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0003-security/spec.md
  target_path: docs/03.specs/0003-security/spec.md
  artifact_id: SPEC-0003
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0004-data/spec.md
  target_path: docs/03.specs/0004-data/spec.md
  artifact_id: SPEC-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0005-data-analytics/spec.md
  target_path: docs/03.specs/0005-data-analytics/spec.md
  artifact_id: SPEC-0005
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0006-messaging/spec.md
  target_path: docs/03.specs/0006-messaging/spec.md
  artifact_id: SPEC-0006
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0007-observability/spec.md
  target_path: docs/03.specs/0007-observability/spec.md
  artifact_id: SPEC-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0008-workflow/spec.md
  target_path: docs/03.specs/0008-workflow/spec.md
  artifact_id: SPEC-0008
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0009-ai/spec.md
  target_path: docs/03.specs/0009-ai/spec.md
  artifact_id: SPEC-0009
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0010-tooling/spec.md
  target_path: docs/03.specs/0010-tooling/spec.md
  artifact_id: SPEC-0010
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0011-communication/spec.md
  target_path: docs/03.specs/0011-communication/spec.md
  artifact_id: SPEC-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0012-laboratory/spec.md
  target_path: docs/03.specs/0012-laboratory/spec.md
  artifact_id: SPEC-0012
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md
  target_path: docs/03.specs/0090-workspace-audit-2026-05/spec.md
  artifact_id: SPEC-0090
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0091-workspace-doc-consistency-2026-05/spec.md
  target_path: docs/03.specs/0091-workspace-doc-consistency-2026-05/spec.md
  artifact_id: SPEC-0091
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0092-workspace-consistency-2026-05b/spec.md
  target_path: docs/03.specs/0092-workspace-consistency-2026-05b/spec.md
  artifact_id: SPEC-0092
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md
  target_path: docs/03.specs/0093-docs-taxonomy-agent-first-migration/spec.md
  artifact_id: SPEC-0093
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  target_path: docs/03.specs/0094-harness-agent-first-engineering/spec.md
  artifact_id: SPEC-0094
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0095-infra-secrets-docs-refresh/spec.md
  target_path: docs/03.specs/0095-infra-secrets-docs-refresh/spec.md
  artifact_id: SPEC-0095
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md
  target_path: docs/03.specs/0096-llm-wiki-agent-first-completion/spec.md
  artifact_id: SPEC-0096
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md
  target_path: docs/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md
  artifact_id: SPEC-0097
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0098-standardize-infra-net/spec.md
  target_path: docs/03.specs/0098-standardize-infra-net/spec.md
  artifact_id: SPEC-0098
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0102-workspace-document-contract-audit-pack/spec.md
  target_path: docs/03.specs/0102-workspace-document-contract-audit-pack/spec.md
  artifact_id: SPEC-0102
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0103-document-restructure-audit-contract-archive/spec.md
  target_path: docs/03.specs/0103-document-restructure-audit-contract-archive/spec.md
  artifact_id: SPEC-0103
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0105-agentic-engineering-implementation-audit-pack/spec.md
  target_path: docs/03.specs/0105-agentic-engineering-implementation-audit-pack/spec.md
  artifact_id: SPEC-0105
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0123-agentic-engineering-audit-remediation/spec.md
  target_path: docs/03.specs/0123-agentic-engineering-audit-remediation/spec.md
  artifact_id: SPEC-0123
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0123-agentic-engineering-audit-remediation/task.md
  target_path: docs/03.specs/0123-agentic-engineering-audit-remediation/tasks/tsk-0001-research-pack-extension.md
  artifact_id: TASK-0123-01
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0131-document-corpus-lifecycle-migration-foundation/spec.md
  target_path: docs/03.specs/0131-document-corpus-lifecycle-migration-foundation/spec.md
  artifact_id: SPEC-0131
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0132-agent-governance-harness-convergence/spec.md
  target_path: docs/03.specs/0132-agent-governance-harness-convergence/spec.md
  artifact_id: SPEC-0132
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0133-target-surface-contract-convergence/spec.md
  target_path: docs/03.specs/0133-target-surface-contract-convergence/spec.md
  artifact_id: SPEC-0133
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0134-agent-governance-canonical-convergence/plan.md
  target_path: docs/03.specs/0134-agent-governance-canonical-convergence/plan.md
  artifact_id: PLAN-0134
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0134-agent-governance-canonical-convergence/spec.md
  target_path: docs/03.specs/0134-agent-governance-canonical-convergence/spec.md
  artifact_id: SPEC-0134
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0134-agent-governance-canonical-convergence/task.md
  target_path: docs/03.specs/0134-agent-governance-canonical-convergence/tasks/tsk-0001-canonical-convergence.md
  artifact_id: TASK-0134-01
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  target_path: docs/03.specs/0135-target-surface-delta-convergence/plan.md
  artifact_id: PLAN-0135
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0135-target-surface-delta-convergence/spec.md
  target_path: docs/03.specs/0135-target-surface-delta-convergence/spec.md
  artifact_id: SPEC-0135
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0135-target-surface-delta-convergence/task.md
  target_path: docs/03.specs/0135-target-surface-delta-convergence/tasks/tsk-0001-delta-convergence.md
  artifact_id: TASK-0135-01
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md
  target_path: docs/03.specs/0136-sdlc-taxonomy-convergence/plan.md
  artifact_id: PLAN-0136
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md
  target_path: docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md
  artifact_id: SPEC-0136
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md
  target_path: docs/03.specs/0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md
  artifact_id: TASK-0136-01
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0152-deleted-reference-leaf-disposition/plan.md
  target_path: docs/03.specs/0152-deleted-reference-leaf-disposition/plan.md
  artifact_id: PLAN-0152
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0152-deleted-reference-leaf-disposition/spec.md
  target_path: docs/03.specs/0152-deleted-reference-leaf-disposition/spec.md
  artifact_id: SPEC-0152
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/spec-0152-deleted-reference-leaf-disposition/task.md
  target_path: docs/03.specs/0152-deleted-reference-leaf-disposition/tasks/tsk-0001-reference-disposition.md
  artifact_id: TASK-0152-01
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/137-agentic-research-pack-rebuild/spec.md
  target_path: docs/03.specs/0137-agentic-research-pack-rebuild/spec.md
  artifact_id: SPEC:137-AGENTIC-RESEARCH-PACK-REBUILD
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/04.execution/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/04.execution/plans/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md
  target_path: docs/03.specs/0137-agentic-research-pack-rebuild/plan.md
  artifact_id: plan:2026-08-08-agentic-research-pack-rebuild
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/04.execution/tasks/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
  target_path: docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md
  artifact_id: task:2026-08-08-agentic-research-pack-rebuild
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md
  target_path: docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0002-source-refresh.md
  artifact_id: task:2026-08-11-agentic-research-pack-source-refresh
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md
  target_path: docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0003-deepening.md
  artifact_id: task:2026-08-14-agentic-research-pack-deepening
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md
  target_path: docs/05.operations/catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md
  artifact_id: policy-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0002-developer-environment/guide.md
  target_path: docs/05.operations/catalog/00-workspace/0002-developer-environment/guide.md
  artifact_id: guide-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison/guide.md
  target_path: docs/05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md
  artifact_id: guide-0003
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  target_path: docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md
  artifact_id: guide-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  target_path: docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/policy.md
  artifact_id: policy-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/runbook.md
  target_path: docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/runbook.md
  artifact_id: runbook-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  target_path: docs/05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md
  artifact_id: policy-0006
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  target_path: docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md
  artifact_id: guide-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  target_path: docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/policy.md
  artifact_id: policy-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  target_path: docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/runbook.md
  artifact_id: runbook-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding/guide.md
  target_path: docs/05.operations/catalog/00-workspace/0008-new-service-onboarding/guide.md
  artifact_id: guide-0008
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0009-release-management/runbook.md
  target_path: docs/05.operations/catalog/00-workspace/0009-release-management/runbook.md
  artifact_id: runbook-0009
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  target_path: docs/05.operations/catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md
  artifact_id: guide-0010
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/guide.md
  target_path: docs/05.operations/catalog/01-gateway/0011-nginx/guide.md
  artifact_id: guide-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/policy.md
  target_path: docs/05.operations/catalog/01-gateway/0011-nginx/policy.md
  artifact_id: policy-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/runbook.md
  target_path: docs/05.operations/catalog/01-gateway/0011-nginx/runbook.md
  artifact_id: runbook-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack/guide.md
  target_path: docs/05.operations/catalog/01-gateway/0012-edge-routing-stack/guide.md
  artifact_id: guide-0012
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/guide.md
  target_path: docs/05.operations/catalog/01-gateway/0013-traefik/guide.md
  artifact_id: guide-0013
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/policy.md
  target_path: docs/05.operations/catalog/01-gateway/0013-traefik/policy.md
  artifact_id: policy-0013
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/runbook.md
  target_path: docs/05.operations/catalog/01-gateway/0013-traefik/runbook.md
  artifact_id: runbook-0013
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/guide.md
  target_path: docs/05.operations/catalog/02-auth/0014-keycloak/guide.md
  artifact_id: guide-0014
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/policy.md
  target_path: docs/05.operations/catalog/02-auth/0014-keycloak/policy.md
  artifact_id: policy-0014
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/runbook.md
  target_path: docs/05.operations/catalog/02-auth/0014-keycloak/runbook.md
  artifact_id: runbook-0014
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/guide.md
  target_path: docs/05.operations/catalog/02-auth/0015-oauth2-proxy/guide.md
  artifact_id: guide-0015
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/policy.md
  target_path: docs/05.operations/catalog/02-auth/0015-oauth2-proxy/policy.md
  artifact_id: policy-0015
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/runbook.md
  target_path: docs/05.operations/catalog/02-auth/0015-oauth2-proxy/runbook.md
  artifact_id: runbook-0015
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/03-security/ops-0016-vault/guide.md
  target_path: docs/05.operations/catalog/03-security/0016-vault/guide.md
  artifact_id: guide-0016
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/03-security/ops-0016-vault/policy.md
  target_path: docs/05.operations/catalog/03-security/0016-vault/policy.md
  artifact_id: policy-0016
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/03-security/ops-0016-vault/runbook.md
  target_path: docs/05.operations/catalog/03-security/0016-vault/runbook.md
  artifact_id: runbook-0016
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0017-influxdb/guide.md
  target_path: docs/05.operations/catalog/04-data/0017-influxdb/guide.md
  artifact_id: guide-0017
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0017-influxdb/policy.md
  target_path: docs/05.operations/catalog/04-data/0017-influxdb/policy.md
  artifact_id: policy-0017
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0017-influxdb/runbook.md
  target_path: docs/05.operations/catalog/04-data/0017-influxdb/runbook.md
  artifact_id: runbook-0017
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0018-ksqldb/guide.md
  target_path: docs/05.operations/catalog/04-data/0018-ksqldb/guide.md
  artifact_id: guide-0018
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0018-ksqldb/policy.md
  target_path: docs/05.operations/catalog/04-data/0018-ksqldb/policy.md
  artifact_id: policy-0018
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0018-ksqldb/runbook.md
  target_path: docs/05.operations/catalog/04-data/0018-ksqldb/runbook.md
  artifact_id: runbook-0018
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0019-opensearch/guide.md
  target_path: docs/05.operations/catalog/04-data/0019-opensearch/guide.md
  artifact_id: guide-0019
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0019-opensearch/policy.md
  target_path: docs/05.operations/catalog/04-data/0019-opensearch/policy.md
  artifact_id: policy-0019
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0019-opensearch/runbook.md
  target_path: docs/05.operations/catalog/04-data/0019-opensearch/runbook.md
  artifact_id: runbook-0019
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0020-starrocks/guide.md
  target_path: docs/05.operations/catalog/04-data/0020-starrocks/guide.md
  artifact_id: guide-0020
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0020-starrocks/policy.md
  target_path: docs/05.operations/catalog/04-data/0020-starrocks/policy.md
  artifact_id: policy-0020
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0020-starrocks/runbook.md
  target_path: docs/05.operations/catalog/04-data/0020-starrocks/runbook.md
  artifact_id: runbook-0020
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0021-backup-and-restore/policy.md
  target_path: docs/05.operations/catalog/04-data/0021-backup-and-restore/policy.md
  artifact_id: policy-0021
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/guide.md
  target_path: docs/05.operations/catalog/04-data/0022-valkey-cluster/guide.md
  artifact_id: guide-0022
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/policy.md
  target_path: docs/05.operations/catalog/04-data/0022-valkey-cluster/policy.md
  artifact_id: policy-0022
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/runbook.md
  target_path: docs/05.operations/catalog/04-data/0022-valkey-cluster/runbook.md
  artifact_id: runbook-0022
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0023-minio/guide.md
  target_path: docs/05.operations/catalog/04-data/0023-minio/guide.md
  artifact_id: guide-0023
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0023-minio/policy.md
  target_path: docs/05.operations/catalog/04-data/0023-minio/policy.md
  artifact_id: policy-0023
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0023-minio/runbook.md
  target_path: docs/05.operations/catalog/04-data/0023-minio/runbook.md
  artifact_id: runbook-0023
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/guide.md
  target_path: docs/05.operations/catalog/04-data/0024-seaweedfs/guide.md
  artifact_id: guide-0024
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/policy.md
  target_path: docs/05.operations/catalog/04-data/0024-seaweedfs/policy.md
  artifact_id: policy-0024
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/runbook.md
  target_path: docs/05.operations/catalog/04-data/0024-seaweedfs/runbook.md
  artifact_id: runbook-0024
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0025-cassandra/guide.md
  target_path: docs/05.operations/catalog/04-data/0025-cassandra/guide.md
  artifact_id: guide-0025
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0025-cassandra/policy.md
  target_path: docs/05.operations/catalog/04-data/0025-cassandra/policy.md
  artifact_id: policy-0025
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0025-cassandra/runbook.md
  target_path: docs/05.operations/catalog/04-data/0025-cassandra/runbook.md
  artifact_id: runbook-0025
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0026-couchdb/guide.md
  target_path: docs/05.operations/catalog/04-data/0026-couchdb/guide.md
  artifact_id: guide-0026
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0026-couchdb/policy.md
  target_path: docs/05.operations/catalog/04-data/0026-couchdb/policy.md
  artifact_id: policy-0026
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0026-couchdb/runbook.md
  target_path: docs/05.operations/catalog/04-data/0026-couchdb/runbook.md
  artifact_id: runbook-0026
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0027-mongodb/guide.md
  target_path: docs/05.operations/catalog/04-data/0027-mongodb/guide.md
  artifact_id: guide-0027
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0027-mongodb/policy.md
  target_path: docs/05.operations/catalog/04-data/0027-mongodb/policy.md
  artifact_id: policy-0027
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0027-mongodb/runbook.md
  target_path: docs/05.operations/catalog/04-data/0027-mongodb/runbook.md
  artifact_id: runbook-0027
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0028-management-database/guide.md
  target_path: docs/05.operations/catalog/04-data/0028-management-database/guide.md
  artifact_id: guide-0028
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0028-management-database/policy.md
  target_path: docs/05.operations/catalog/04-data/0028-management-database/policy.md
  artifact_id: policy-0028
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0028-management-database/runbook.md
  target_path: docs/05.operations/catalog/04-data/0028-management-database/runbook.md
  artifact_id: runbook-0028
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0029-supabase/guide.md
  target_path: docs/05.operations/catalog/04-data/0029-supabase/guide.md
  artifact_id: guide-0029
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0029-supabase/policy.md
  target_path: docs/05.operations/catalog/04-data/0029-supabase/policy.md
  artifact_id: policy-0029
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0029-supabase/runbook.md
  target_path: docs/05.operations/catalog/04-data/0029-supabase/runbook.md
  artifact_id: runbook-0029
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/guide.md
  target_path: docs/05.operations/catalog/04-data/0030-optimization-hardening/guide.md
  artifact_id: guide-0030
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/policy.md
  target_path: docs/05.operations/catalog/04-data/0030-optimization-hardening/policy.md
  artifact_id: policy-0030
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/runbook.md
  target_path: docs/05.operations/catalog/04-data/0030-optimization-hardening/runbook.md
  artifact_id: runbook-0030
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/guide.md
  target_path: docs/05.operations/catalog/04-data/0031-postgresql-cluster/guide.md
  artifact_id: guide-0031
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/policy.md
  target_path: docs/05.operations/catalog/04-data/0031-postgresql-cluster/policy.md
  artifact_id: policy-0031
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/runbook.md
  target_path: docs/05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md
  artifact_id: runbook-0031
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  target_path: docs/05.operations/catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  artifact_id: runbook-0032
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0033-neo4j/guide.md
  target_path: docs/05.operations/catalog/04-data/0033-neo4j/guide.md
  artifact_id: guide-0033
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0033-neo4j/policy.md
  target_path: docs/05.operations/catalog/04-data/0033-neo4j/policy.md
  artifact_id: policy-0033
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0033-neo4j/runbook.md
  target_path: docs/05.operations/catalog/04-data/0033-neo4j/runbook.md
  artifact_id: runbook-0033
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0034-qdrant/guide.md
  target_path: docs/05.operations/catalog/04-data/0034-qdrant/guide.md
  artifact_id: guide-0034
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0034-qdrant/policy.md
  target_path: docs/05.operations/catalog/04-data/0034-qdrant/policy.md
  artifact_id: policy-0034
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0034-qdrant/runbook.md
  target_path: docs/05.operations/catalog/04-data/0034-qdrant/runbook.md
  artifact_id: runbook-0034
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/04-data/ops-0035-storage-exhaustion/runbook.md
  target_path: docs/05.operations/catalog/04-data/0035-storage-exhaustion/runbook.md
  artifact_id: runbook-0035
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/guide.md
  target_path: docs/05.operations/catalog/05-messaging/0036-kafka/guide.md
  artifact_id: guide-0036
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/policy.md
  target_path: docs/05.operations/catalog/05-messaging/0036-kafka/policy.md
  artifact_id: policy-0036
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/runbook.md
  target_path: docs/05.operations/catalog/05-messaging/0036-kafka/runbook.md
  artifact_id: runbook-0036
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/guide.md
  target_path: docs/05.operations/catalog/05-messaging/0037-optimization-hardening/guide.md
  artifact_id: guide-0037
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/policy.md
  target_path: docs/05.operations/catalog/05-messaging/0037-optimization-hardening/policy.md
  artifact_id: policy-0037
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/runbook.md
  target_path: docs/05.operations/catalog/05-messaging/0037-optimization-hardening/runbook.md
  artifact_id: runbook-0037
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/guide.md
  target_path: docs/05.operations/catalog/05-messaging/0038-rabbitmq/guide.md
  artifact_id: guide-0038
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/policy.md
  target_path: docs/05.operations/catalog/05-messaging/0038-rabbitmq/policy.md
  artifact_id: policy-0038
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/runbook.md
  target_path: docs/05.operations/catalog/05-messaging/0038-rabbitmq/runbook.md
  artifact_id: runbook-0038
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/guide.md
  target_path: docs/05.operations/catalog/06-observability/0039-alertmanager/guide.md
  artifact_id: guide-0039
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/policy.md
  target_path: docs/05.operations/catalog/06-observability/0039-alertmanager/policy.md
  artifact_id: policy-0039
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0039-alertmanager/runbook.md
  artifact_id: runbook-0039
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/guide.md
  target_path: docs/05.operations/catalog/06-observability/0040-alloy/guide.md
  artifact_id: guide-0040
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/policy.md
  target_path: docs/05.operations/catalog/06-observability/0040-alloy/policy.md
  artifact_id: policy-0040
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0040-alloy/runbook.md
  artifact_id: runbook-0040
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/guide.md
  target_path: docs/05.operations/catalog/06-observability/0041-grafana/guide.md
  artifact_id: guide-0041
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/policy.md
  target_path: docs/05.operations/catalog/06-observability/0041-grafana/policy.md
  artifact_id: policy-0041
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0041-grafana/runbook.md
  artifact_id: runbook-0041
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  target_path: docs/05.operations/catalog/06-observability/0042-lgtm-stack/guide.md
  artifact_id: guide-0042
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0043-loki/guide.md
  target_path: docs/05.operations/catalog/06-observability/0043-loki/guide.md
  artifact_id: guide-0043
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0043-loki/policy.md
  target_path: docs/05.operations/catalog/06-observability/0043-loki/policy.md
  artifact_id: policy-0043
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0043-loki/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0043-loki/runbook.md
  artifact_id: runbook-0043
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/guide.md
  target_path: docs/05.operations/catalog/06-observability/0044-optimization-hardening/guide.md
  artifact_id: guide-0044
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/policy.md
  target_path: docs/05.operations/catalog/06-observability/0044-optimization-hardening/policy.md
  artifact_id: policy-0044
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0044-optimization-hardening/runbook.md
  artifact_id: runbook-0044
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/guide.md
  target_path: docs/05.operations/catalog/06-observability/0045-prometheus/guide.md
  artifact_id: guide-0045
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md
  target_path: docs/05.operations/catalog/06-observability/0045-prometheus/policy.md
  artifact_id: policy-0045
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0045-prometheus/runbook.md
  artifact_id: runbook-0045
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/guide.md
  target_path: docs/05.operations/catalog/06-observability/0046-pushgateway/guide.md
  artifact_id: guide-0046
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/policy.md
  target_path: docs/05.operations/catalog/06-observability/0046-pushgateway/policy.md
  artifact_id: policy-0046
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0046-pushgateway/runbook.md
  artifact_id: runbook-0046
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  target_path: docs/05.operations/catalog/06-observability/0047-pyroscope/guide.md
  artifact_id: guide-0047
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/policy.md
  target_path: docs/05.operations/catalog/06-observability/0047-pyroscope/policy.md
  artifact_id: policy-0047
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0047-pyroscope/runbook.md
  artifact_id: runbook-0047
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  target_path: docs/05.operations/catalog/06-observability/0048-telemetry-retention/policy.md
  artifact_id: policy-0048
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  target_path: docs/05.operations/catalog/06-observability/0049-tempo/guide.md
  artifact_id: guide-0049
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/policy.md
  target_path: docs/05.operations/catalog/06-observability/0049-tempo/policy.md
  artifact_id: policy-0049
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/runbook.md
  target_path: docs/05.operations/catalog/06-observability/0049-tempo/runbook.md
  artifact_id: runbook-0049
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/guide.md
  target_path: docs/05.operations/catalog/07-workflow/0050-airflow/guide.md
  artifact_id: guide-0050
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/policy.md
  target_path: docs/05.operations/catalog/07-workflow/0050-airflow/policy.md
  artifact_id: policy-0050
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/runbook.md
  target_path: docs/05.operations/catalog/07-workflow/0050-airflow/runbook.md
  artifact_id: runbook-0050
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/guide.md
  target_path: docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/guide.md
  artifact_id: guide-0051
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/policy.md
  target_path: docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md
  artifact_id: policy-0052
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/guide.md
  target_path: docs/05.operations/catalog/07-workflow/0053-n8n/guide.md
  artifact_id: guide-0053
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/policy.md
  target_path: docs/05.operations/catalog/07-workflow/0053-n8n/policy.md
  artifact_id: policy-0053
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/runbook.md
  target_path: docs/05.operations/catalog/07-workflow/0053-n8n/runbook.md
  artifact_id: runbook-0053
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/guide.md
  target_path: docs/05.operations/catalog/07-workflow/0054-optimization-hardening/guide.md
  artifact_id: guide-0054
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/policy.md
  target_path: docs/05.operations/catalog/07-workflow/0054-optimization-hardening/policy.md
  artifact_id: policy-0054
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/runbook.md
  target_path: docs/05.operations/catalog/07-workflow/0054-optimization-hardening/runbook.md
  artifact_id: runbook-0054
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery/runbook.md
  target_path: docs/05.operations/catalog/08-ai/0055-gpu-recovery/runbook.md
  artifact_id: runbook-0055
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/guide.md
  target_path: docs/05.operations/catalog/08-ai/0056-ollama/guide.md
  artifact_id: guide-0056
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/policy.md
  target_path: docs/05.operations/catalog/08-ai/0056-ollama/policy.md
  artifact_id: policy-0056
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/runbook.md
  target_path: docs/05.operations/catalog/08-ai/0056-ollama/runbook.md
  artifact_id: runbook-0056
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/guide.md
  target_path: docs/05.operations/catalog/08-ai/0057-open-webui/guide.md
  artifact_id: guide-0057
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/policy.md
  target_path: docs/05.operations/catalog/08-ai/0057-open-webui/policy.md
  artifact_id: policy-0057
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/runbook.md
  target_path: docs/05.operations/catalog/08-ai/0057-open-webui/runbook.md
  artifact_id: runbook-0057
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/guide.md
  target_path: docs/05.operations/catalog/08-ai/0058-optimization-hardening/guide.md
  artifact_id: guide-0058
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md
  target_path: docs/05.operations/catalog/08-ai/0058-optimization-hardening/policy.md
  artifact_id: policy-0058
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/runbook.md
  target_path: docs/05.operations/catalog/08-ai/0058-optimization-hardening/runbook.md
  artifact_id: runbook-0058
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/08-ai/ops-0059-rag-workflow/guide.md
  target_path: docs/05.operations/catalog/08-ai/0059-rag-workflow/guide.md
  artifact_id: guide-0059
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0060-iac-deployment/policy.md
  artifact_id: policy-0060
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0061-k6/guide.md
  artifact_id: guide-0061
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0061-k6/policy.md
  artifact_id: policy-0061
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0061-k6/runbook.md
  artifact_id: runbook-0061
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0062-locust/guide.md
  artifact_id: guide-0062
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0062-locust/policy.md
  artifact_id: policy-0062
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0062-locust/runbook.md
  artifact_id: runbook-0062
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0063-optimization-hardening/guide.md
  artifact_id: guide-0063
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0063-optimization-hardening/policy.md
  artifact_id: policy-0063
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0063-optimization-hardening/runbook.md
  artifact_id: runbook-0063
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0064-performance-testing/guide.md
  artifact_id: guide-0064
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0064-performance-testing/policy.md
  artifact_id: policy-0064
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0064-performance-testing/runbook.md
  artifact_id: runbook-0064
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0065-registry/guide.md
  artifact_id: guide-0065
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0065-registry/policy.md
  artifact_id: policy-0065
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0065-registry/runbook.md
  artifact_id: runbook-0065
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0066-sonarqube/guide.md
  artifact_id: guide-0066
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0066-sonarqube/policy.md
  artifact_id: policy-0066
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0066-sonarqube/runbook.md
  artifact_id: runbook-0066
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0067-syncthing/guide.md
  artifact_id: guide-0067
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0067-syncthing/policy.md
  artifact_id: policy-0067
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0067-syncthing/runbook.md
  artifact_id: runbook-0067
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0068-terraform/guide.md
  artifact_id: guide-0068
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0068-terraform/policy.md
  artifact_id: policy-0068
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0068-terraform/runbook.md
  artifact_id: runbook-0068
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/guide.md
  target_path: docs/05.operations/catalog/09-tooling/0069-terrakube/guide.md
  artifact_id: guide-0069
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/policy.md
  target_path: docs/05.operations/catalog/09-tooling/0069-terrakube/policy.md
  artifact_id: policy-0069
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/runbook.md
  target_path: docs/05.operations/catalog/09-tooling/0069-terrakube/runbook.md
  artifact_id: runbook-0069
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/10-communication/ops-0070-mail/guide.md
  target_path: docs/05.operations/catalog/10-communication/0070-mail/guide.md
  artifact_id: guide-0070
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/10-communication/ops-0070-mail/policy.md
  target_path: docs/05.operations/catalog/10-communication/0070-mail/policy.md
  artifact_id: policy-0070
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/10-communication/ops-0070-mail/runbook.md
  target_path: docs/05.operations/catalog/10-communication/0070-mail/runbook.md
  artifact_id: runbook-0070
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/guide.md
  target_path: docs/05.operations/catalog/11-laboratory/0071-homer-dashboard/guide.md
  artifact_id: guide-0071
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/policy.md
  target_path: docs/05.operations/catalog/11-laboratory/0071-homer-dashboard/policy.md
  artifact_id: policy-0071
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/runbook.md
  target_path: docs/05.operations/catalog/11-laboratory/0071-homer-dashboard/runbook.md
  artifact_id: runbook-0071
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  target_path: docs/05.operations/catalog/11-laboratory/0072-dozzle/guide.md
  artifact_id: guide-0072
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/policy.md
  target_path: docs/05.operations/catalog/11-laboratory/0072-dozzle/policy.md
  artifact_id: policy-0072
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/runbook.md
  target_path: docs/05.operations/catalog/11-laboratory/0072-dozzle/runbook.md
  artifact_id: runbook-0072
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/guide.md
  target_path: docs/05.operations/catalog/11-laboratory/0073-open-notebook/guide.md
  artifact_id: guide-0073
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/policy.md
  target_path: docs/05.operations/catalog/11-laboratory/0073-open-notebook/policy.md
  artifact_id: policy-0073
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/runbook.md
  target_path: docs/05.operations/catalog/11-laboratory/0073-open-notebook/runbook.md
  artifact_id: runbook-0073
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md
  target_path: docs/05.operations/catalog/11-laboratory/0074-optimization-hardening/guide.md
  artifact_id: guide-0074
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md
  target_path: docs/05.operations/catalog/11-laboratory/0074-optimization-hardening/policy.md
  artifact_id: policy-0074
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md
  target_path: docs/05.operations/catalog/11-laboratory/0074-optimization-hardening/runbook.md
  artifact_id: runbook-0074
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/guide.md
  target_path: docs/05.operations/catalog/11-laboratory/0075-portainer/guide.md
  artifact_id: guide-0075
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/policy.md
  target_path: docs/05.operations/catalog/11-laboratory/0075-portainer/policy.md
  artifact_id: policy-0075
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/runbook.md
  target_path: docs/05.operations/catalog/11-laboratory/0075-portainer/runbook.md
  artifact_id: runbook-0075
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/guide.md
  target_path: docs/05.operations/catalog/11-laboratory/0076-redisinsight/guide.md
  artifact_id: guide-0076
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/policy.md
  target_path: docs/05.operations/catalog/11-laboratory/0076-redisinsight/policy.md
  artifact_id: policy-0076
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/runbook.md
  target_path: docs/05.operations/catalog/11-laboratory/0076-redisinsight/runbook.md
  artifact_id: runbook-0076
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/guide.md
  target_path: docs/05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md
  artifact_id: guide-0077
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/policy.md
  target_path: docs/05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md
  artifact_id: policy-0077
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/runbook.md
  target_path: docs/05.operations/catalog/12-infra-net/0077-ip-address-management/runbook.md
  artifact_id: runbook-0077
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/05.operations/releases/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0001-readme.md
  target_path: docs/90.references/audits/0001-readme/README.md
  artifact_id: AUD-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0002-automation-coverage-map.md
  target_path: docs/90.references/audits/0002-automation-coverage-map/README.md
  artifact_id: AUD-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0003-ci-qa-parser-graphify-decision.md
  target_path: docs/90.references/audits/0003-ci-qa-parser-graphify-decision/README.md
  artifact_id: AUD-0003
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0004-contract-governance-map.md
  target_path: docs/90.references/audits/0004-contract-governance-map/README.md
  artifact_id: AUD-0004
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0005-frontmatter-inventory.md
  target_path: docs/90.references/audits/0005-frontmatter-inventory/README.md
  artifact_id: AUD-0005
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0006-frontmatter-routing-profile.md
  target_path: docs/90.references/audits/0006-frontmatter-routing-profile/README.md
  artifact_id: AUD-0006
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0007-gap-register.md
  target_path: docs/90.references/audits/0007-gap-register/README.md
  artifact_id: AUD-0007
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0008-historical-evidence-preservation.md
  target_path: docs/90.references/audits/0008-historical-evidence-preservation/README.md
  artifact_id: AUD-0008
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0009-readme-profile-inventory.md
  target_path: docs/90.references/audits/0009-readme-profile-inventory/README.md
  artifact_id: AUD-0009
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0010-section-profile-inventory.md
  target_path: docs/90.references/audits/0010-section-profile-inventory/README.md
  artifact_id: AUD-0010
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0011-template-application-gaps.md
  target_path: docs/90.references/audits/0011-template-application-gaps/README.md
  artifact_id: AUD-0011
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0012-readme.md
  target_path: docs/90.references/audits/0012-readme/README.md
  artifact_id: AUD-0012
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0013-ci-qa-formatting-contract.md
  target_path: docs/90.references/audits/0013-ci-qa-formatting-contract/README.md
  artifact_id: AUD-0013
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0014-frontmatter-profile-inventory.md
  target_path: docs/90.references/audits/0014-frontmatter-profile-inventory/README.md
  artifact_id: AUD-0014
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0015-operations-bucket-restructure.md
  target_path: docs/90.references/audits/0015-operations-bucket-restructure/README.md
  artifact_id: AUD-0015
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0016-restructure-gap-register.md
  target_path: docs/90.references/audits/0016-restructure-gap-register/README.md
  artifact_id: AUD-0016
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0017-sdlc-spec-archive-candidates.md
  target_path: docs/90.references/audits/0017-sdlc-spec-archive-candidates/README.md
  artifact_id: AUD-0017
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0018-template-contract-drift.md
  target_path: docs/90.references/audits/0018-template-contract-drift/README.md
  artifact_id: AUD-0018
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0019-readme.md
  target_path: docs/90.references/audits/0019-readme/README.md
  artifact_id: AUD-0019
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0020-agent-instructions-catalog-vibe-models.md
  target_path: docs/90.references/audits/0020-agent-instructions-catalog-vibe-models/README.md
  artifact_id: AUD-0020
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0021-automation-candidates.md
  target_path: docs/90.references/audits/0021-automation-candidates/README.md
  artifact_id: AUD-0021
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0022-compose-infrastructure-operations-readiness.md
  target_path: docs/90.references/audits/0022-compose-infrastructure-operations-readiness/README.md
  artifact_id: AUD-0022
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md
  target_path: docs/90.references/audits/0023-frontmatter-semantic-inventory/README.md
  artifact_id: AUD-0023
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0024-frontmatter-template-readme-implementation.md
  target_path: docs/90.references/audits/0024-frontmatter-template-readme-implementation/README.md
  artifact_id: AUD-0024
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0025-harness-engineering-implementation.md
  target_path: docs/90.references/audits/0025-harness-engineering-implementation/README.md
  artifact_id: AUD-0025
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0026-implementation-overview.md
  target_path: docs/90.references/audits/0026-implementation-overview/README.md
  artifact_id: AUD-0026
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0027-loop-engineering-implementation.md
  target_path: docs/90.references/audits/0027-loop-engineering-implementation/README.md
  artifact_id: AUD-0027
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0028-provider-harness-loop-implementation.md
  target_path: docs/90.references/audits/0028-provider-harness-loop-implementation/README.md
  artifact_id: AUD-0028
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0029-sdlc-document-contracts-implementation.md
  target_path: docs/90.references/audits/0029-sdlc-document-contracts-implementation/README.md
  artifact_id: AUD-0029
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0030-sdlc-quality-formatting-implementation.md
  target_path: docs/90.references/audits/0030-sdlc-quality-formatting-implementation/README.md
  artifact_id: AUD-0030
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0031-security-framework-maturity.md
  target_path: docs/90.references/audits/0031-security-framework-maturity/README.md
  artifact_id: AUD-0031
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0032-workspace-rules-environment-implementation.md
  target_path: docs/90.references/audits/0032-workspace-rules-environment-implementation/README.md
  artifact_id: AUD-0032
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0033-readme.md
  target_path: docs/90.references/audits/0033-readme/README.md
  artifact_id: AUD-0033
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0034-agent-catalog-audit.md
  target_path: docs/90.references/audits/0034-agent-catalog-audit/README.md
  artifact_id: AUD-0034
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0035-automation-candidates.md
  target_path: docs/90.references/audits/0035-automation-candidates/README.md
  artifact_id: AUD-0035
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0036-harness-loop-audit.md
  target_path: docs/90.references/audits/0036-harness-loop-audit/README.md
  artifact_id: AUD-0036
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0037-implementation-overview.md
  target_path: docs/90.references/audits/0037-implementation-overview/README.md
  artifact_id: AUD-0037
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/audits/ref-0038-sdlc-qa-security-audit.md
  target_path: docs/90.references/audits/0038-sdlc-qa-security-audit/README.md
  artifact_id: AUD-0038
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/README.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/agent-instructions-vibe-coding.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/agent-model-selection.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/ai-agent-catalogs.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/automation-pipeline-workflow.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/docker-compose-infrastructure.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/document-metadata-lifecycle.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/documentation-architecture.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/documentation-architecture.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/harness-engineering.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/llm-wiki-system.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/llm-wiki-system.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/loop-engineering.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/memory-hierarchy.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/memory-hierarchy.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/provider-implementation-comparison.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/provider-model-landscape.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/quality-ci-formatting.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/scope-application-matrix.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/scope-application-matrix.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/sdlc-document-roles.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/security-governance.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/spec-driven-sdlc.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md
  target_path: docs/90.references/research/0001-agentic-research-pack-refresh/workspace-baseline.md
  artifact_id: RES-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/README.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/README.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/agent-instructions-vibe-coding.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/agent-instructions-vibe-coding.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/agent-model-selection.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/agent-model-selection.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/ai-agent-catalogs.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/ai-agent-catalogs.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/automation-pipeline-workflow.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/automation-pipeline-workflow.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/docker-compose-infrastructure.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/docker-compose-infrastructure.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/document-metadata-lifecycle.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/document-metadata-lifecycle.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/documentation-architecture.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/documentation-architecture.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/harness-engineering.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/harness-engineering.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/llm-wiki-system.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/llm-wiki-system.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/loop-engineering.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/loop-engineering.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/memory-hierarchy.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/memory-hierarchy.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/provider-implementation-comparison.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/provider-implementation-comparison.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/provider-model-landscape.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/provider-model-landscape.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/quality-ci-formatting.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/quality-ci-formatting.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/scope-application-matrix.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/scope-application-matrix.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/sdlc-document-roles.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/sdlc-document-roles.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/security-governance.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/security-governance.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/spec-driven-sdlc.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/spec-driven-sdlc.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/verification-validation.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/verification-validation.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/2026-08-08-agentic-engineering-research-pack/workspace-baseline.md
  target_path: docs/90.references/research/0002-agentic-engineering-research-pack/workspace-baseline.md
  artifact_id: RES-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/research/ref-0084-github-actions-platform.md
  target_path: docs/90.references/research/0084-github-actions-platform/README.md
  artifact_id: RES-0084
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/learning/ref-0080-roadmap-v1.md
  target_path: docs/90.references/research/0080-roadmap-v1/README.md
  artifact_id: RES-0080
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/learning/ref-0081-roadmap.md
  target_path: docs/90.references/research/0081-roadmap/README.md
  artifact_id: RES-0081
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/docker/ref-0059-compose-profile-service-coverage.md
  target_path: docs/90.references/data/0059-compose-profile-service-coverage/README.md
  artifact_id: DATA-0059
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/docker/ref-0060-image-version-interpretation.md
  target_path: docs/90.references/data/0060-image-version-interpretation/README.md
  artifact_id: DATA-0060
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/docker/ref-0061-tech-stack-version-provenance.md
  target_path: docs/90.references/data/0061-tech-stack-version-provenance/README.md
  artifact_id: DATA-0061
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/glossary/ref-0062-stable-reference-terms.md
  target_path: docs/90.references/data/0062-stable-reference-terms/README.md
  artifact_id: DATA-0062
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0066-foundation-summary.md
  target_path: docs/90.references/data/0066-foundation-summary/README.md
  artifact_id: DATA-0066
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0067-foundation.yaml
  target_path: docs/90.references/data/0067-foundation/data.yaml
  artifact_id: DATA-0067
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0068-target-surface-convergence-summary.md
  target_path: docs/90.references/data/0068-target-surface-convergence-summary/README.md
  artifact_id: DATA-0068
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0069-target-surface-convergence.yaml
  target_path: docs/90.references/data/0069-target-surface-convergence/data.yaml
  artifact_id: DATA-0069
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0063-agent-governance-retirement-ledger.yaml
  target_path: docs/90.references/data/0063-agent-governance-retirement-ledger/data.yaml
  artifact_id: DATA-0063
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0064-agent-output-eval-fixtures.md
  target_path: docs/90.references/data/0064-agent-output-eval-fixtures/README.md
  artifact_id: DATA-0064
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0065-audit-implementation-matrix.md
  target_path: docs/90.references/data/0065-audit-implementation-matrix/README.md
  artifact_id: DATA-0065
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0070-gap-to-stage-routing.md
  target_path: docs/90.references/data/0070-gap-to-stage-routing/README.md
  artifact_id: DATA-0070
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0071-github-actions-control-plane-observation.yaml
  target_path: docs/90.references/data/0071-github-actions-control-plane-observation/data.yaml
  artifact_id: DATA-0071
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0072-provider-hook-parity-matrix.md
  target_path: docs/90.references/data/0072-provider-hook-parity-matrix/README.md
  artifact_id: DATA-0072
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml
  target_path: docs/90.references/data/0073-target-surface-delta-manifest/data.yaml
  artifact_id: DATA-0073
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md
  target_path: docs/90.references/data/0074-target-surface-delta-summary/README.md
  artifact_id: DATA-0074
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/hads/ref-0075-profile.md
  target_path: docs/90.references/data/0075-profile/README.md
  artifact_id: DATA-0075
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  target_path: docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md
  artifact_id: DATA-0076
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/kubernetes/ref-0077-docker-compose-to-k3s-migration.md
  target_path: docs/90.references/data/0077-docker-compose-to-k3s-migration/README.md
  artifact_id: DATA-0077
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/security/ref-0078-security-automation-readiness.md
  target_path: docs/90.references/data/0078-security-automation-readiness/README.md
  artifact_id: DATA-0078
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/security/ref-0079-supply-chain-sample-service.md
  target_path: docs/90.references/data/0079-supply-chain-sample-service/README.md
  artifact_id: DATA-0079
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  target_path: docs/90.references/data/0082-llm-wiki-index/README.md
  artifact_id: DATA-0082
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/llm-wiki/ref-0083-repository-map.md
  target_path: docs/90.references/data/0083-repository-map/README.md
  artifact_id: DATA-0083
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/learning/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/llm-wiki/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/llm-wiki/llm-wiki-index.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/docker/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/glossary/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/governance/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/hads/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/knowledge/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/kubernetes/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/90.references/data/security/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md
  target_path: docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md
  artifact_id: mig-0001
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md
  target_path: docs/98.archive/migrations/0002-operations-catalog-convergence.md
  artifact_id: mig-0002
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md
  target_path: docs/98.archive/migrations/0003-workspace-governance-simplification.md
  artifact_id: mig-0003
  action: rename
  recovery_commit: 71f89ba1430245c89d10c36a084fc2fae9cfe98b
- source_path: docs/98.archive/changes/chg-0002-01-gateway-standardization/plan.md
  target_path: null
  artifact_id: plan-0002
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0003-02-auth-standardization/plan.md
  target_path: null
  artifact_id: plan-0003
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0004-03-security-standardization/plan.md
  target_path: null
  artifact_id: plan-0004
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0005-04-data-standardization/plan.md
  target_path: null
  artifact_id: plan-0005
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0006-05-messaging-standardization/plan.md
  target_path: null
  artifact_id: plan-0006
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0007-06-observability-standardization/plan.md
  target_path: null
  artifact_id: plan-0007
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0008-07-workflow-standardization/plan.md
  target_path: null
  artifact_id: plan-0008
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0009-08-ai-standardization/plan.md
  target_path: null
  artifact_id: plan-0009
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0010-09-tooling-standardization/plan.md
  target_path: null
  artifact_id: plan-0010
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0011-10-communication-standardization/plan.md
  target_path: null
  artifact_id: plan-0011
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0012-11-laboratory-standardization/plan.md
  target_path: null
  artifact_id: plan-0012
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0013-08-ai-open-webui/plan.md
  target_path: null
  artifact_id: plan-0013
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0013-08-ai-open-webui/task.md
  target_path: null
  artifact_id: task-0013-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0015
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0015-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0016
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0016-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0017-03-security-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0017
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0017-03-security-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0017-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0018-04-data-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0018
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0018-04-data-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0018-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0019
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0019-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0020
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0020-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0021
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0021-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0022
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0022-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0023
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0023-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/plan.md
  target_path: null
  artifact_id: plan-0024
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/task.md
  target_path: null
  artifact_id: task-0024-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0025-standardize-infra-net/plan.md
  target_path: null
  artifact_id: plan-0025
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0025-standardize-infra-net/task.md
  target_path: null
  artifact_id: task-0025-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/plan.md
  target_path: null
  artifact_id: plan-0026
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/task.md
  target_path: null
  artifact_id: task-0026-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0027-harness-agent-first-engineering/plan.md
  target_path: null
  artifact_id: plan-0027
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0027-harness-agent-first-engineering/task.md
  target_path: null
  artifact_id: task-0027-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/plan.md
  target_path: null
  artifact_id: plan-0028
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/task.md
  target_path: null
  artifact_id: task-0028-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/plan.md
  target_path: null
  artifact_id: plan-0029
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/task.md
  target_path: null
  artifact_id: task-0029-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/plan.md
  target_path: null
  artifact_id: plan-0030
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/task.md
  target_path: null
  artifact_id: task-0030-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/plan.md
  target_path: null
  artifact_id: plan-0031
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/task.md
  target_path: null
  artifact_id: task-0031-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0032-requirements-standardization/plan.md
  target_path: null
  artifact_id: plan-0032
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0032-requirements-standardization/task.md
  target_path: null
  artifact_id: task-0032-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/plan.md
  target_path: null
  artifact_id: plan-0033
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/task.md
  target_path: null
  artifact_id: task-0033-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/plan.md
  target_path: null
  artifact_id: plan-0034
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/task.md
  target_path: null
  artifact_id: task-0034-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/plan.md
  target_path: null
  artifact_id: plan-0035
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/task.md
  target_path: null
  artifact_id: task-0035-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0036-execution-stage-remediation/plan.md
  target_path: null
  artifact_id: plan-0036
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0036-execution-stage-remediation/task.md
  target_path: null
  artifact_id: task-0036-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/plan.md
  target_path: null
  artifact_id: plan-0037
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/task.md
  target_path: null
  artifact_id: task-0037-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/plan.md
  target_path: null
  artifact_id: plan-0038
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/task.md
  target_path: null
  artifact_id: task-0038-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/plan.md
  target_path: null
  artifact_id: plan-0039
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/task.md
  target_path: null
  artifact_id: task-0039-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/plan.md
  target_path: null
  artifact_id: plan-0040
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/task.md
  target_path: null
  artifact_id: task-0040-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/plan.md
  target_path: null
  artifact_id: plan-0041
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/task.md
  target_path: null
  artifact_id: task-0041-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/plan.md
  target_path: null
  artifact_id: plan-0042
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/task.md
  target_path: null
  artifact_id: task-0042-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/plan.md
  target_path: null
  artifact_id: plan-0043
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/task.md
  target_path: null
  artifact_id: task-0043-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0044-workspace-audit-grill-review/plan.md
  target_path: null
  artifact_id: plan-0044
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0044-workspace-audit-grill-review/task.md
  target_path: null
  artifact_id: task-0044-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0045-workspace-audit-improvement/plan.md
  target_path: null
  artifact_id: plan-0045
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0045-workspace-audit-improvement/task.md
  target_path: null
  artifact_id: task-0045-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/plan.md
  target_path: null
  artifact_id: plan-0046
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/task.md
  target_path: null
  artifact_id: task-0046-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/plan.md
  target_path: null
  artifact_id: plan-0047
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/task.md
  target_path: null
  artifact_id: task-0047-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/plan.md
  target_path: null
  artifact_id: plan-0048
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/task.md
  target_path: null
  artifact_id: task-0048-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/plan.md
  target_path: null
  artifact_id: plan-0049
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/task.md
  target_path: null
  artifact_id: task-0049-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/plan.md
  target_path: null
  artifact_id: plan-0050
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/task.md
  target_path: null
  artifact_id: task-0050-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0051-workspace-audit/plan.md
  target_path: null
  artifact_id: plan-0051
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0051-workspace-audit/task.md
  target_path: null
  artifact_id: task-0051-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0052-workspace-doc-consistency/plan.md
  target_path: null
  artifact_id: plan-0052
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0052-workspace-doc-consistency/task.md
  target_path: null
  artifact_id: task-0052-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/plan.md
  target_path: null
  artifact_id: plan-0053
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/task.md
  target_path: null
  artifact_id: task-0053-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0054-claude-harness-governance-verification/plan.md
  target_path: null
  artifact_id: plan-0054
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0054-claude-harness-governance-verification/task.md
  target_path: null
  artifact_id: task-0054-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0055-agent-governance-decision-items/plan.md
  target_path: null
  artifact_id: plan-0055
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/plan.md
  target_path: null
  artifact_id: plan-0056
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/task.md
  target_path: null
  artifact_id: task-0056-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/plan.md
  target_path: null
  artifact_id: plan-0057
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/task.md
  target_path: null
  artifact_id: task-0057-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/plan.md
  target_path: null
  artifact_id: plan-0058
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/task.md
  target_path: null
  artifact_id: task-0058-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/plan.md
  target_path: null
  artifact_id: plan-0059
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/task.md
  target_path: null
  artifact_id: task-0059-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/plan.md
  target_path: null
  artifact_id: plan-0060
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/task.md
  target_path: null
  artifact_id: task-0060-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0061-governance-optimization/plan.md
  target_path: null
  artifact_id: plan-0061
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0061-governance-optimization/task.md
  target_path: null
  artifact_id: task-0061-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0062-governance-surgical-reverification/plan.md
  target_path: null
  artifact_id: plan-0062
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0062-governance-surgical-reverification/task.md
  target_path: null
  artifact_id: task-0062-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0063-template-system-reorganization/plan.md
  target_path: null
  artifact_id: plan-0063
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0063-template-system-reorganization/task.md
  target_path: null
  artifact_id: task-0063-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0064-document-contract-remediation-batches/plan.md
  target_path: null
  artifact_id: plan-0064
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0064-document-contract-remediation-batches/task.md
  target_path: null
  artifact_id: task-0064-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0065-template-system-contract-standardization/plan.md
  target_path: null
  artifact_id: plan-0065
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0065-template-system-contract-standardization/task.md
  target_path: null
  artifact_id: task-0065-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/plan.md
  target_path: null
  artifact_id: plan-0066
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/task.md
  target_path: null
  artifact_id: task-0066-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/plan.md
  target_path: null
  artifact_id: plan-0067
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/task.md
  target_path: null
  artifact_id: task-0067-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/plan.md
  target_path: null
  artifact_id: plan-0068
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/task.md
  target_path: null
  artifact_id: task-0068-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/plan.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/task.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/plan.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/task.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0071-audit-pack-coverage-report/plan.md
  target_path: null
  artifact_id: plan-0071
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0071-audit-pack-coverage-report/task.md
  target_path: null
  artifact_id: task-0071-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/plan.md
  target_path: null
  artifact_id: plan-0072
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/task.md
  target_path: null
  artifact_id: task-0072-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0073-gap-routing-recommendation/plan.md
  target_path: null
  artifact_id: plan-0073
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0073-gap-routing-recommendation/task.md
  target_path: null
  artifact_id: task-0073-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/plan.md
  target_path: null
  artifact_id: plan-0074
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/task.md
  target_path: null
  artifact_id: task-0074-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/plan.md
  target_path: null
  artifact_id: plan-0075
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/task.md
  target_path: null
  artifact_id: task-0075-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/plan.md
  target_path: null
  artifact_id: plan-0076
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/task.md
  target_path: null
  artifact_id: task-0076-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/plan.md
  target_path: null
  artifact_id: plan-0077
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/task.md
  target_path: null
  artifact_id: task-0077-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0078-workspace-support-surface-contract/plan.md
  target_path: null
  artifact_id: plan-0078
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0078-workspace-support-surface-contract/task.md
  target_path: null
  artifact_id: task-0078-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/plan.md
  target_path: null
  artifact_id: plan-0079
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/task.md
  target_path: null
  artifact_id: task-0079-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0080-agent-output-eval-runner/plan.md
  target_path: null
  artifact_id: plan-0080
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0080-agent-output-eval-runner/task.md
  target_path: null
  artifact_id: task-0080-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/plan.md
  target_path: null
  artifact_id: plan-0081
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/task.md
  target_path: null
  artifact_id: task-0081-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/plan.md
  target_path: null
  artifact_id: plan-0082
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/task.md
  target_path: null
  artifact_id: task-0082-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/plan.md
  target_path: null
  artifact_id: plan-0083
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/task.md
  target_path: null
  artifact_id: task-0083-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/plan.md
  target_path: null
  artifact_id: plan-0084
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/task.md
  target_path: null
  artifact_id: task-0084-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/plan.md
  target_path: null
  artifact_id: plan-0085
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/task.md
  target_path: null
  artifact_id: task-0085-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/plan.md
  target_path: null
  artifact_id: plan-0086
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/task.md
  target_path: null
  artifact_id: task-0086-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0087-tech-stack-version-provenance/plan.md
  target_path: null
  artifact_id: plan-0087
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0087-tech-stack-version-provenance/task.md
  target_path: null
  artifact_id: task-0087-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/plan.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/task.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/plan.md
  target_path: null
  artifact_id: plan:2026-07-11-agentic-engineering-audit-remediation
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/task.md
  target_path: null
  artifact_id: task:2026-07-11-agentic-engineering-audit-remediation
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/plan.md
  target_path: null
  artifact_id: plan-0090
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/task.md
  target_path: null
  artifact_id: task-0090-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/plan.md
  target_path: null
  artifact_id: plan-0091
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md
  target_path: null
  artifact_id: task-0091-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/plan.md
  target_path: null
  artifact_id: plan-0092
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/task.md
  target_path: null
  artifact_id: task-0092-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0093-security-supply-chain-remediation/plan.md
  target_path: null
  artifact_id: plan-0093
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0093-security-supply-chain-remediation/task.md
  target_path: null
  artifact_id: task-0093-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/plan.md
  target_path: null
  artifact_id: plan-0094
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/task.md
  target_path: null
  artifact_id: task-0094-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0095-document-contract-canonicalization/plan.md
  target_path: null
  artifact_id: plan:2026-07-13-document-contract-canonicalization
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0095-document-contract-canonicalization/task.md
  target_path: null
  artifact_id: task:2026-07-13-document-contract-canonicalization
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/plan.md
  target_path: null
  artifact_id: plan-0096
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/task.md
  target_path: null
  artifact_id: task-0096-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/plan.md
  target_path: null
  artifact_id: plan-0097
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/task.md
  target_path: null
  artifact_id: task-0097-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/plan.md
  target_path: null
  artifact_id: plan:2026-07-15-agent-governance-harness-convergence
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/task.md
  target_path: null
  artifact_id: task:2026-07-15-agent-governance-harness-convergence
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0099-target-surface-contract-convergence/plan.md
  target_path: null
  artifact_id: plan:2026-07-18-target-surface-contract-convergence
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0099-target-surface-contract-convergence/task.md
  target_path: null
  artifact_id: task:2026-07-18-target-surface-contract-convergence
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0100-operational-readiness-closure-program/plan.md
  target_path: null
  artifact_id: plan-0100
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0100-operational-readiness-closure-program/task.md
  target_path: null
  artifact_id: task-0100-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0104-01-gateway/task.md
  target_path: null
  artifact_id: task-0104-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0105-02-auth/task.md
  target_path: null
  artifact_id: task-0105-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0106-03-security/task.md
  target_path: null
  artifact_id: task-0106-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0107-04-data/task.md
  target_path: null
  artifact_id: task-0107-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0108-05-messaging/task.md
  target_path: null
  artifact_id: task-0108-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0109-06-observability/task.md
  target_path: null
  artifact_id: task-0109-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0110-07-workflow/task.md
  target_path: null
  artifact_id: task-0110-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0111-08-ai/task.md
  target_path: null
  artifact_id: task-0111-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0112-09-tooling/task.md
  target_path: null
  artifact_id: task-0112-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0113-10-communication/task.md
  target_path: null
  artifact_id: task-0113-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0114-11-laboratory/task.md
  target_path: null
  artifact_id: task-0114-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0115-agent-governance-missing-items-implementation/task.md
  target_path: null
  artifact_id: task-0115-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0116-docs-implementation-audit/task.md
  target_path: null
  artifact_id: task-0116-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0117-harness-engineering/task.md
  target_path: null
  artifact_id: task-0117-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0118-language-policy-boundary-audit/task.md
  target_path: null
  artifact_id: task-0118-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0119-language-policy-hard-enforcement/task.md
  target_path: null
  artifact_id: task-0119-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0120-language-policy-normalization-batch-1/task.md
  target_path: null
  artifact_id: task-0120-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0121-language-policy-normalization-batch-2/task.md
  target_path: null
  artifact_id: task-0121-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0122-language-policy-normalization-batch-3/task.md
  target_path: null
  artifact_id: task-0122-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0123-language-policy-plan-normalization-batch-1/task.md
  target_path: null
  artifact_id: task-0123-02
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0124-language-policy-plan-normalization-batch-2/task.md
  target_path: null
  artifact_id: task-0124-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0125-language-policy-plan-normalization-batch-3/task.md
  target_path: null
  artifact_id: task-0125-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0126-language-policy-plan-normalization-batch-4/task.md
  target_path: null
  artifact_id: task-0126-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0127-language-policy-plan-normalization-batch-5/task.md
  target_path: null
  artifact_id: task-0127-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0128-language-policy-plan-normalization-batch-6/task.md
  target_path: null
  artifact_id: task-0128-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0129-language-policy-plan-normalization-batch-7/task.md
  target_path: null
  artifact_id: task-0129-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0130-language-policy-plan-normalization-batch-8/task.md
  target_path: null
  artifact_id: task-0130-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0131-language-policy-reference-normalization/task.md
  target_path: null
  artifact_id: task-0131-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0132-language-policy-task-normalization-batch-1/task.md
  target_path: null
  artifact_id: task-0132-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0133-language-policy-task-normalization-batch-2/task.md
  target_path: null
  artifact_id: task-0133-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0134-language-policy-task-normalization-batch-3/task.md
  target_path: null
  artifact_id: task-0134-02
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0135-language-policy-task-normalization-batch-4/task.md
  target_path: null
  artifact_id: task-0135-02
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0136-language-policy-task-normalization-batch-5/task.md
  target_path: null
  artifact_id: task-0136-02
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0137-language-policy-task-normalization-batch-6/task.md
  target_path: null
  artifact_id: task-0137-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0138-language-policy-task-normalization-batch-7/task.md
  target_path: null
  artifact_id: task-0138-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0139-examples-scaffold-contract-remediation/task.md
  target_path: null
  artifact_id: task-0139-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0140-frontmatter-routing-evidence-refresh/task.md
  target_path: null
  artifact_id: task-0140-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0141-github-branch-protection-reverification/task.md
  target_path: null
  artifact_id: task-0141-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0142-infra-tech-stack-version-refresh/task.md
  target_path: null
  artifact_id: task-0142-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0143-ai-governance-reorg/plan.md
  target_path: null
  artifact_id: plan-0143
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0144-standardizing-agent-governance/plan.md
  target_path: null
  artifact_id: plan-0144
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0144-standardizing-agent-governance/task.md
  target_path: null
  artifact_id: task-0144-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/plan.md
  target_path: null
  artifact_id: plan-0145
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/task.md
  target_path: null
  artifact_id: task-0145-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0146-agent-governance-phase2-alignment/plan.md
  target_path: null
  artifact_id: plan-0146
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0147-agent-governance-phase3-implementation/task.md
  target_path: null
  artifact_id: task-0147-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0148-agent-governance-phase3-stage01-02-continuation/task.md
  target_path: null
  artifact_id: task-0148-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0149-agent-governance-phase3-strategy-integration/task.md
  target_path: null
  artifact_id: task-0149-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0150-agent-governance-phase4-closure/task.md
  target_path: null
  artifact_id: task-0150-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/changes/chg-0151-agent-governance-stage01-02-alignment/task.md
  target_path: null
  artifact_id: task-0151-01
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0099-template-system-numbered-sdlc-paths.md
  target_path: docs/98.archive/tombstones/03.specs/0099-template-system-numbered-sdlc-paths.md
  artifact_id: spec-0099
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0100-template-system-contract-standardization.md
  target_path: docs/98.archive/tombstones/03.specs/0100-template-system-contract-standardization.md
  artifact_id: spec-0100
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0101-template-system-reorganization.md
  target_path: docs/98.archive/tombstones/03.specs/0101-template-system-reorganization.md
  artifact_id: spec-0101
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0104-agentic-research-pack-refresh.md
  target_path: docs/98.archive/tombstones/03.specs/0104-agentic-research-pack-refresh.md
  artifact_id: spec-0104
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0106-workspace-support-surface-contract.md
  target_path: docs/98.archive/tombstones/03.specs/0106-workspace-support-surface-contract.md
  artifact_id: spec-0106
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0107-provider-semantic-parity-validator.md
  target_path: docs/98.archive/tombstones/03.specs/0107-provider-semantic-parity-validator.md
  artifact_id: spec-0107
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0108-compose-profile-service-coverage-snapshot.md
  target_path: docs/98.archive/tombstones/03.specs/0108-compose-profile-service-coverage-snapshot.md
  artifact_id: spec-0108
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0109-gap-routing-recommendation.md
  target_path: docs/98.archive/tombstones/03.specs/0109-gap-routing-recommendation.md
  artifact_id: spec-0109
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0110-agent-output-eval-fixtures.md
  target_path: docs/98.archive/tombstones/03.specs/0110-agent-output-eval-fixtures.md
  artifact_id: spec-0110
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0111-qa-gate-recommendation-ci-summary.md
  target_path: docs/98.archive/tombstones/03.specs/0111-qa-gate-recommendation-ci-summary.md
  artifact_id: spec-0111
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0112-audit-pack-coverage-report.md
  target_path: docs/98.archive/tombstones/03.specs/0112-audit-pack-coverage-report.md
  artifact_id: spec-0112
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0113-llm-wiki-stage-category-coverage.md
  target_path: docs/98.archive/tombstones/03.specs/0113-llm-wiki-stage-category-coverage.md
  artifact_id: spec-0113
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0114-tech-stack-version-provenance.md
  target_path: docs/98.archive/tombstones/03.specs/0114-tech-stack-version-provenance.md
  artifact_id: spec-0114
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0115-provider-hook-parity-matrix.md
  target_path: docs/98.archive/tombstones/03.specs/0115-provider-hook-parity-matrix.md
  artifact_id: spec-0115
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0116-agent-output-eval-runner.md
  target_path: docs/98.archive/tombstones/03.specs/0116-agent-output-eval-runner.md
  artifact_id: spec-0116
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0117-security-automation-readiness-snapshot.md
  target_path: docs/98.archive/tombstones/03.specs/0117-security-automation-readiness-snapshot.md
  artifact_id: spec-0117
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0118-audit-implementation-matrix-snapshot.md
  target_path: docs/98.archive/tombstones/03.specs/0118-audit-implementation-matrix-snapshot.md
  artifact_id: spec-0118
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0119-sdlc-document-contract-corpus-normalization.md
  target_path: docs/98.archive/tombstones/03.specs/0119-sdlc-document-contract-corpus-normalization.md
  artifact_id: spec-0119
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0120-agent-output-eval-ci-gate.md
  target_path: docs/98.archive/tombstones/03.specs/0120-agent-output-eval-ci-gate.md
  artifact_id: spec-0120
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0121-dependency-vulnerability-audit-gate.md
  target_path: docs/98.archive/tombstones/03.specs/0121-dependency-vulnerability-audit-gate.md
  artifact_id: spec-0121
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0122-agentic-research-pack-consolidation.md
  target_path: docs/98.archive/tombstones/03.specs/0122-agentic-research-pack-consolidation.md
  artifact_id: spec-0122
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md
  target_path: docs/98.archive/tombstones/03.specs/0124-compose-runtime-readiness-remediation.md
  artifact_id: spec-0124
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md
  target_path: docs/98.archive/tombstones/03.specs/0125-infrastructure-operations-readiness-remediation.md
  artifact_id: spec-0125
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md
  target_path: docs/98.archive/tombstones/03.specs/0126-security-supply-chain-remediation.md
  artifact_id: spec-0126
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0127-deployment-release-engineering-remediation.md
  target_path: docs/98.archive/tombstones/03.specs/0127-deployment-release-engineering-remediation.md
  artifact_id: spec-0127
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0128-agentic-audit-harness-consolidation.md
  target_path: docs/98.archive/tombstones/03.specs/0128-agentic-audit-harness-consolidation.md
  artifact_id: spec-0128
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0129-document-contract-canonicalization.md
  target_path: docs/98.archive/tombstones/03.specs/0129-document-contract-canonicalization.md
  artifact_id: spec-0129
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/03.specs/spec-0130-template-contract-system-canonicalization.md
  target_path: docs/98.archive/tombstones/03.specs/0130-template-contract-system-canonicalization.md
  artifact_id: spec-0130
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0086-01-setup.md
  target_path: docs/98.archive/tombstones/05.operations/0086-01-setup.md
  artifact_id: ref-0086
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0087-ksql-streaming.md
  target_path: docs/98.archive/tombstones/05.operations/0087-ksql-streaming.md
  artifact_id: ref-0087
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0088-01-airflow-dag-dev.md
  target_path: docs/98.archive/tombstones/05.operations/0088-01-airflow-dag-dev.md
  artifact_id: ref-0088
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0089-airbyte.md
  target_path: docs/98.archive/tombstones/05.operations/0089-airbyte.md
  artifact_id: ref-0089
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0090-01-llm-inference.md
  target_path: docs/98.archive/tombstones/05.operations/0090-01-llm-inference.md
  artifact_id: ref-0090
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0091-local-llm-setup.md
  target_path: docs/98.archive/tombstones/05.operations/0091-local-llm-setup.md
  artifact_id: ref-0091
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0092-01-iac-automation.md
  target_path: docs/98.archive/tombstones/05.operations/0092-01-iac-automation.md
  artifact_id: ref-0092
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0093-airbyte.md
  target_path: docs/98.archive/tombstones/05.operations/0093-airbyte.md
  artifact_id: ref-0093
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0094-airbyte.md
  target_path: docs/98.archive/tombstones/05.operations/0094-airbyte.md
  artifact_id: ref-0094
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/98.archive/tombstones/05.operations/ref-0095-windows-network-ip.md
  target_path: docs/98.archive/tombstones/05.operations/0095-windows-network-ip.md
  artifact_id: ref-0095
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: tests/validation/test_document_links.py
  target_path: tests/lib/document_governance/test_links.py
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: tests/validation/test_document_taxonomy.py
  target_path: tests/lib/document_governance/test_taxonomy.py
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: tests/validation/test_operations_catalog.py
  target_path: tests/lib/document_governance/test_operations_catalog.py
  artifact_id: null
  action: rename
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: scripts/hooks/patch-graphify-post-commit.sh
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: scripts/knowledge/generate-llm-wiki-coverage.sh
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: scripts/knowledge/generate-llm-wiki-index.sh
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: scripts/validation/check-repo-contracts.sh
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: scripts/validation/recommend-gap-routing.sh
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: scripts/validation/recommend-qa-gates.sh
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/archive-retention-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/common-document-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/corpus-migration-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/document-corpus-migration-contract.yaml
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/document-metadata-profiles.yaml
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/external-source-rationale.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/frontmatter-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/lifecycle-status.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/readme-profile-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/sdlc-document-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/template-contract.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/template-governance.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/support/template-selection.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/common/archive.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/common/audit.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/common/reference.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/adr.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/architecture-description.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/interface-requirement.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/plan.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/prd.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/spec.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/srs.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/sdlc/task.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/agent-design.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/api-spec.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/data-model.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/openapi.template.yaml
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/schema.template.graphql
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/service.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/service.template.proto
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/99.templates/templates/spec-contracts/tests.template.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525
- source_path: docs/03.specs/0153-workspace-governance-simplification/spec.md
  target_path: null
  artifact_id: SPEC-0153
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/plan.md
  target_path: null
  artifact_id: plan-0153
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/README.md
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0001-control-plane.md
  target_path: null
  artifact_id: task-0153-0001
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0002-stage99.md
  target_path: null
  artifact_id: task-0153-0002
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0003-bootstrap.md
  target_path: null
  artifact_id: task-0153-0003
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md
  target_path: null
  artifact_id: task-0153-0004
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0005-requirements.md
  target_path: null
  artifact_id: task-0153-0005
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0006-architecture.md
  target_path: null
  artifact_id: task-0153-0006
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0007-spec-lifecycle.md
  target_path: null
  artifact_id: task-0153-0007
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0008-operations.md
  target_path: null
  artifact_id: task-0153-0008
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0009-references.md
  target_path: null
  artifact_id: task-0153-0009
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0010-archive.md
  target_path: null
  artifact_id: task-0153-0010
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0011-script-tests.md
  target_path: null
  artifact_id: task-0153-0011
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0012-gates.md
  target_path: null
  artifact_id: task-0153-0012
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0013-closure.md
  target_path: null
  artifact_id: task-0153-0013
  action: delete
  recovery_commit: 5bab8b360b1e56de0c6b5f5d6f984a421ed81c44
- source_path: scripts/validation/check-task4-migration.py
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 494065806794980080b081439298d7b534d10803
- source_path: tests/validation/test_task4_migration_verifier.py
  target_path: null
  artifact_id: null
  action: delete
  recovery_commit: 494065806794980080b081439298d7b534d10803
- source_path: docs/03.specs/0090-workspace-audit-2026-05/spec.md
  target_path: null
  artifact_id: SPEC-0090
  action: delete
  recovery_commit: 494065806794980080b081439298d7b534d10803
- source_path: docs/03.specs/0091-workspace-doc-consistency-2026-05/spec.md
  target_path: null
  artifact_id: SPEC-0091
  action: delete
  recovery_commit: 494065806794980080b081439298d7b534d10803
- source_path: docs/03.specs/0092-workspace-consistency-2026-05b/spec.md
  target_path: null
  artifact_id: SPEC-0092
  action: delete
  recovery_commit: 494065806794980080b081439298d7b534d10803
```

## Recovery

Each row binds its original path to a verified regular Git blob at the stated
commit. The one-time execution package is recoverable from closure commit
`5bab8b360b1e56de0c6b5f5d6f984a421ed81c44`. Preserve recovery-bearing commit identities
through history-preserving integration; a squash or rebase is not equivalent.
The original approval selection remains in Git, not a duplicate current ledger.

## Approval

The user approved the authority-first structure, supported-provider removal,
Operations domain/subject preservation, release removal and minimal Archive.
The closure code/readiness reviews reported C0/I0/M0 for specification and
implementation/security. Actual physical-retirement verification is recorded
in the subsequent retirement commit; it is not inferred from those reviews.

## Traceability

- [Authority decision](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Shared governance](../../00.agent-governance/README.md)
- [Document authority](../../99.templates/README.md)
- [Archive lookup](../README.md)

## Execution Evidence

Closure commit `5bab8b360b1e56de0c6b5f5d6f984a421ed81c44` preserves the execution
Tasks, actual full-profile exit 0, recovery checks and independent review
dispositions. It records 884 prior executed transitions separately from the
then-pending package deletions and three unexecuted superseded plans.
This compact record replaces execution-only fields and full-body copies.
