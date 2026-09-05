---
title: "Reference: GitHub Actions Platform Mechanics"
version: "2.0.0"
type: "reference/research-pack"
status: "published"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
artifact_id: "RES-0084"
parent_ids: []
created: "2026-07-05"
observed_at: "2026-09-05"
---

# Reference: GitHub Actions Platform Mechanics

## Question

Which GitHub Actions security, execution, permission, identity, supply-chain,
runner, and remote-enforcement mechanics matter to this repository, and which
of them are actually configured, executed, or remotely verified?

Detailed platform analysis belongs to
[RES-0084-m0001](m0001-platform-mechanics.md). This README owns the package
question, evidence boundary, result summary, and navigation only.

## Scope

- Repository baseline: `buenhyden/hy-home.docker`
  `main@4c6d211129615eab372d720ebd209b6c27618c86`.
- Repository and external observation date: 2026-09-05.
- Included: workflow permissions, token/OIDC model, triggers, untrusted input,
  action pinning, concurrency, runners, aggregate gates, rulesets, required
  checks, Hosted evidence, and rollback.
- Excluded: secret values, organization policy not present in approved
  read-back, environment/deployment mutation, artifact publication, new
  workflow dispatch, tag, and release.
- Stage 90 records evidence and implications. Workflow/configuration authority
  remains in `.github/`, execution evidence in the owning Task, and remote
  truth in dated authenticated read-back.

## Method

1. Preserve the existing platform analysis as a member instead of leaving a
   600-line package README or creating a competing research package.
2. Compare the current workflow YAML and typed workflow contract with official
   GitHub documentation re-opened on 2026-09-05.
3. Use SPEC-0172's exact Hosted run and remote protection evidence without
   treating tracked configuration as remote proof.
4. Classify claims as Configured, Repository-enforced, Hosted-executed,
   Remote-verified, or Unverified.
5. Validate member identity, links, generated index freshness, and the public
   repository gates after the split.

## Findings

| Category | Member | Repository state | Evidence depth | Priority |
| --- | --- | --- | --- | --- |
| Permissions, OIDC, reusable actions/workflows, untrusted input, supply chain, execution, rulesets, runners, and static analysis | [Platform mechanics](m0001-platform-mechanics.md) | Six workflows; two CI aggregate jobs; full-SHA action pins; least-privilege permissions | Configured, Repository-enforced, Hosted-executed | High |
| Required status checks | [Platform mechanics](m0001-platform-mechanics.md) | `strict=true`; `validation-changed` and `validation-full` bound to app ID 15368 | Remote-verified on 2026-09-05 | High |
| CD, OIDC, environment, deployment, release | [Platform mechanics](m0001-platform-mechanics.md) | No exact live target or current publication route | Unverified / not adopted | High when target exists |

The major change from the previous package revision is structural: detailed
analysis moved to a member. The major evidence change is that Hosted aggregate
jobs and remote required-check replacement are now observed, while deployment
and release remain outside the evidence boundary.

## Sources

- [GitHub ruleset status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).
- [GitHub Actions script injection](https://docs.github.com/en/actions/concepts/security/script-injections).
- [GitHub Actions OIDC](https://docs.github.com/en/actions/reference/security/oidc).
- [Workflow contract](../../../../.github/workflow-contract.yml) and
  [CI Quality Gates](../../../../.github/workflows/ci-quality.yml).
- [Main protection record](../../../../.github/rulesets/main-protection.md).
- [Completed SPEC-0172 outcome](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md).

The member owns the detailed source inventory and claim-by-claim analysis.

## Implications

- Keep both aggregate CI jobs as workflow identities and as strict required
  checks while authenticated read-back matches.
- Use the recorded 12-check before-state for rollback on mismatch; do not infer
  a replacement from job display names.
- Continue using explicit least-privilege permissions and immutable action
  SHAs.
- Introduce OIDC, environments, promotion, or deployment only after a named
  target, trust boundary, approval, acceptance, and rollback contract exists.
- Route any implementation through Requirement → Architecture/ADR → Spec →
  Plan → Task → Verification → Independent Review.

## Traceability

- Member: [RES-0084-m0001](m0001-platform-mechanics.md).
- Research index: [Research Packages](../README.md).
- Related topical research: [automation](../0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md),
  [quality](../0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md),
  [security](../0002-agentic-engineering-research-pack/m0017-security-governance.md), and
  [verification](../0002-agentic-engineering-research-pack/m0019-verification-validation.md).
- Current baseline: [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md).
- Dated baseline/recovery evidence:
  [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md).
- Governance: [Stage 00](../../../00.agent-governance/README.md).
- Requirement/Architecture: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [AD-0027](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md), and
  [ADR-0029](../../../02.architecture/decisions/0029-workspace-governance-authority.md).
- Implementation/evidence: [completed SPEC-0172 outcome](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md)
  and [current lifecycle reconciliation](../../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md).
- Templates and Registry: [research-pack template](../../../99.templates/templates/references/research-pack.template.md),
  [research-member template](../../../99.templates/templates/references/research.template.md), and
  [Registry](../../../99.templates/registry.json).

## Limitations

- Remote protection is verified only at the 2026-09-05 read-back; later state
  may differ.
- No secret, environment value, artifact, raw log, or organization-level
  Actions policy was inspected in this renewal.
- No new workflow was dispatched and no deployment, release, tag, or provider
  mutation occurred.
- Hosted CI success proves the named revision and run, not future runner or
  external-service availability.
- GitHub platform documentation is mutable after 2026-09-05.
