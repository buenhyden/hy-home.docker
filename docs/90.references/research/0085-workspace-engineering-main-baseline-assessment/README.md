---
title: "Workspace Engineering Main Baseline Assessment"
version: "0.3.0"
type: "reference/research-pack"
status: "review"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
artifact_id: "RES-0085"
parent_ids: []
created: "2026-09-04"
observed_at: "2026-09-05"
---

# Workspace Engineering Main Baseline Assessment

## Question

What binding scope, evidence boundary, and identity-recovery provenance must be
preserved from the assessment of
`main@4c6d211129615eab372d720ebd209b6c27618c86` after current workspace-baseline
ownership is consolidated into RES-0002-m0020?

This package no longer owns mutable current-state conclusions. It preserves the
dated assessment envelope and the recovered request identity while the
publication lifecycle proceeds through review.

## Scope

- Dated repository baseline: `buenhyden/hy-home.docker`
  `main@4c6d211129615eab372d720ebd209b6c27618c86`.
- Repository observation date: 2026-09-05; external-source confirmation date:
  2026-09-05.
- Included: the original binding request, exact baseline identity, evidence
  class definitions, the SPEC-0172 recovery tuple, and the dated observations
  needed to interpret the assessment.
- Excluded: secret or credential values, user-global Claude/Codex settings,
  shell history, raw logs, new provider calls, new runtime mutation, live
  deployment, tag, and release.
- Current baseline interpretation and topical research belong to
  [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)
  and its sibling members. GitHub Actions mechanics remain in
  [RES-0084](../0084-github-actions-platform/README.md).

## Method

1. Preserve the exact baseline SHA, observation date, source request, recovered
   artifact identity, and reciprocal Task decision.
2. Compare the package question with RES-0002-m0020 using question, evidence
   model, lifecycle, and decision-route criteria.
3. Move mutable current-baseline ownership to RES-0002-m0020 without moving or
   re-identifying the recovery carrier.
4. Retain only dated evidence here and route topical or current claims to their
   canonical members.
5. Validate the forward `draft` to `review` transition, identity recovery,
   inbound links, protected RES-0002 set, and generated-index freshness.

## Findings

| Evidence retained here | Dated result | Evidence depth | Current owner / disposition |
| --- | --- | --- | --- |
| Assessment target | `main@4c6d211129615eab372d720ebd209b6c27618c86`, observed 2026-09-05 | Defined, Local-executed | Historical assessment boundary; current baseline moves to RES-0002-m0020 |
| Request identity | `RES-0085-SCOPE` recovered as `RES-0085-m0001` in the same package | Repository-enforced | Preserve the exact carrier and reciprocal SPEC-0172 Task tuple |
| Evidence classes | Repository, Hosted, provider, runtime, and remote observations remain non-substitutable | Defined | RES-0002-m0020 applies these classes to current conclusions |
| Hosted and remote observations | SPEC-0172 records exact Hosted runs and the 2026-09-05 protection read-back | Hosted-executed, Remote-verified at cutoff | Task and main-protection record remain execution owners |
| Deployment and release | No exact target or version was supplied | Unverified / not adopted | No acceptance claim; separate SDLC work required |
| Consolidation lifecycle | Package and member advance from `draft` to `review` | Repository-enforced | Publication and later supersession require subsequent forward transitions |

Detailed current findings are not repeated here. They are consolidated in
[RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md).

## Sources

- Repository baseline: Git commit
  `4c6d211129615eab372d720ebd209b6c27618c86`.
- [Stage 00 governance](../../../00.agent-governance/README.md) and
  [provider registry](../../../00.agent-governance/providers/registry.yaml).
- [Stage 99 Registry](../../../99.templates/registry.json),
  [research-pack template](../../../99.templates/templates/references/research-pack.template.md),
  and [research-member template](../../../99.templates/templates/references/research.template.md).
- [SPEC-0172](../../../03.specs/0172-document-contract-convergence/spec.md) and
  its [execution evidence](../../../03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md).
- [CI workflow](../../../../.github/workflows/ci-quality.yml),
  [workflow contract](../../../../.github/workflow-contract.yml), and
  [main protection record](../../../../.github/rulesets/main-protection.md).
- [GitHub ruleset status-check rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
  [Docker Compose specification](https://docs.docker.com/compose/compose-file/),
  [Claude Code feature model](https://code.claude.com/docs/en/features-overview),
  and [Codex sandbox and approval controls](https://openai.com/index/running-codex-safely/),
  re-opened 2026-09-05.
- Detailed topical and current-baseline sources remain with the corresponding
  RES-0002 member and RES-0084; this dated evidence package does not duplicate
  their source inventories.

## Implications

- Use RES-0002-m0020 for current workspace-baseline conclusions and future
  baseline re-observation.
- Keep this package intact until its forward publication lifecycle permits a
  later `superseded` transition; do not replace it with a redirect.
- Preserve the exact identity-recovery tuple and Task decision throughout that
  lifecycle.
- Route any actionable current gap through the canonical RES-0002 member and
  the normal Requirement-to-Task chain.

## Traceability

- Current baseline, topical members, and preservation declaration:
  [RES-0002](../0002-agentic-engineering-research-pack/README.md) and
  [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md).
- GitHub Actions mechanics: [RES-0084](../0084-github-actions-platform/README.md).
- Binding scope: [RES-0085-m0001](m0001-request-scope.md).
- Governance authority: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [AD-0027](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md), and
  [ADR-0029](../../../02.architecture/decisions/0029-workspace-governance-authority.md).
- Lifecycle authority: [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md),
  [AD-0030](../../../02.architecture/descriptions/0030-document-lifecycle-governance.md), and
  [ADR-0031](../../../02.architecture/decisions/0031-preserved-archive-record.md).
- Current work/evidence owner: [SPEC-0172 Task](../../../03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md).
- Operations authority: [Stage 05](../../../05.operations/README.md).
- Audit/data evidence: [implementation overview](../../audits/0026-implementation-overview/README.md),
  [Compose defects](../../audits/0097-compose-domain-defect-register/README.md),
  [LLM Wiki index](../../data/0082-llm-wiki-index/README.md), and
  [repository map](../../data/0083-repository-map/README.md).
- Package registry: [Research index](../README.md) and
  [Stage 99 Registry](../../../99.templates/registry.json).

## Limitations

- No secret, credential value, private key, environment value, raw log, shell
  history, or user-global provider setting was inspected.
- This pass made no provider call, Compose service start, deployment, restart,
  rollout, recovery, tag, or release mutation.
- The 2026-09-04 provider/runtime and 2026-09-05 GitHub control-plane evidence
  are point-in-time records from SPEC-0172, not perpetual guarantees.
- `review` is not a terminal disposition. This package remains present until
  the publication lifecycle advances through a later approved change.
- Static Compose rendering does not settle the four AUD-0097 domain defects or
  prove service health, durability, recovery, performance, or production fit.
- Mutable external sources may change after 2026-09-05; paid ISO text was not
  accessed and public catalog/definition material is used only within its
  visible boundary.
