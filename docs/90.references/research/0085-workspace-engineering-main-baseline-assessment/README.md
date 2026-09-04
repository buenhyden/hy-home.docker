---
title: "Workspace Engineering Main Baseline Assessment"
version: "0.2.0"
type: "reference/research-pack"
status: "draft"
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

What does `buenhyden/hy-home.docker` actually provide on `main` for workspace
engineering, agent governance, spec-driven delivery, infrastructure, CI/CD,
quality, security, documentation, provider integration, context handling, and
runtime operation, and which claims still require direct external evidence?

The package also asks whether the 2026-09-04 pre-integration gaps remain true
after SPEC-0172 reached `main`, and whether repository configuration, local
execution, hosted execution, provider acceptance, runtime acceptance, and
remote enforcement are being kept as distinct evidence classes.

## Scope

- Repository baseline: `buenhyden/hy-home.docker`
  `main@4c6d211129615eab372d720ebd209b6c27618c86`.
- Repository observation date: 2026-09-05; external-source confirmation date:
  2026-09-05.
- Included: tracked policies, provider adapters, Registry and templates,
  Requirement/Architecture/Spec/Operations owners, workflows, validators,
  generated navigation, Compose declarations, prior hosted results, and the
  approved remote protection read-back recorded by SPEC-0172.
- Excluded: secret or credential values, user-global Claude/Codex settings,
  shell history, raw logs, new provider calls, new runtime mutation, live
  deployment, tag, and release.
- RES-0085 owns only this repository-local baseline. Topic research remains in
  [RES-0002](../0002-agentic-engineering-research-pack/README.md), with GitHub
  Actions mechanics in [RES-0084](../0084-github-actions-platform/README.md).

## Method

1. Inventory existing research by path, identity, parent relation, headings,
   incoming links, preservation boundary, and observation date before editing.
2. Read current Stage 00, Stage 99, Requirement, Architecture, Spec,
   Operations, workflow, validator, audit, data, infrastructure, and test
   owners at the exact baseline commit.
3. Re-open official provider, GitHub, Docker, documentation-architecture,
   spec-driven development, verification, and security sources on 2026-09-05.
4. Classify each claim as Defined, Configured, Local-executed,
   Repository-enforced, Runtime-verified, Remote-verified, or Unverified; never
   promote evidence by implication.
5. Run the canonical full gate on the clean baseline and record the exact exit
   result separately from hosted, runtime, and remote observations.

## Findings

| Area | Current `main` evidence | Evidence depth | Disposition |
| --- | --- | --- | --- |
| Research ownership | RES-0002 has 20 protected topical members; RES-0084 owns platform mechanics; RES-0085 owns this baseline | Repository-enforced | Reuse existing packages; no RES-0096 allocation |
| Agent governance | 14 canonical roles and 23 canonical skills project through Claude/Codex adapters | Defined, Configured, Repository-enforced | Shared authority is implemented; native behavior remains provider-specific |
| Provider runtime | Registry keeps both providers `adopted` with `runtime_acceptance: needs_revalidation`; SPEC-0172 records bounded Codex and Claude entitlement observations | Configured, Runtime-verified at 2026-09-04 only | No future entitlement, model quality, latency, or cost claim |
| Loop, context, and handoff | Stage 00 owns bounded retry, stop, context loading, compaction, and Task evidence; native hook sets differ | Defined, Configured, Repository-enforced | Structural parity exists; outcome parity is unverified |
| Document contract | Common-six metadata, profile-specific lifecycle graphs, current-corpus migration, and RES-0085 identity recovery are on `main` | Repository-enforced | The former missing-README blocker is closed |
| SDLC | Requirement → Architecture/ADR → Spec/Plan/Task → Verification → review is registered and validated | Defined, Repository-enforced | Research remains advisory; intended-use acceptance stays owner-bound |
| Operations roles | Guide, Policy, Runbook, Incident, and Postmortem are registered; release evidence is composed from Task, changelog/tag, CI, and runbook evidence | Defined, Repository-enforced | Do not create an independent Release profile without a consumer contract |
| CI quality plane | Six workflows are tracked; `validation-changed` and `validation-full` project the registered CI gate graph | Configured, Repository-enforced, Hosted-executed in SPEC-0172 | CI is implemented; CD and production promotion are not implied |
| Main protection | 2026-09-05 approved read-back kept `strict=true` and replaced 12 leaf contexts with two app-bound aggregate checks | Remote-verified at 2026-09-05 | Exact 12-check rollback is retained; later state needs a new read-back |
| Compose | 40 included Compose files plus one explicitly excluded YAML variant expose 28 declared profile selections; the clean baseline statically rendered all selections | Configured, Local-executed, Repository-enforced | Static validity is not service health or deployment acceptance |
| Compose defects | AUD-0097 retains four owner-routed defects not caught by static rendering | Defined, Local-executed historical evidence | Fixes require domain decisions and separate SDLC work |
| Security | Least-privilege workflow permissions, SHA-pinned actions, supply-chain fixtures, document safety, Compose baselines, and static gates are tracked | Configured, Repository-enforced | Live production controls, secrets, and deployment posture remain unverified |
| Documentation architecture | Stage/category/package/subject indexes and generated LLM Wiki outputs route readers to canonical owners | Configured, Repository-enforced | Diátaxis/C4/arc42 are selectively composed, not parallel taxonomies |
| Local quality baseline | Clean `main` full profile completed with exit 0 on 2026-09-05 | Local-executed | Point-in-time local verification only |
| Editor integration | No repository-wide `.vscode`, `.idea`, or `.devcontainer` authority is tracked | Unverified / gap | Add only through a permission- and command-bounded owner contract |

Changed conclusions since the 2026-09-04 observation are: RES-0085 now has a
canonical package envelope; the document-contract migration is merged; hosted
changed/full acceptance exists for the merged candidate; and remote `main`
protection now requires the two aggregate checks. Live deployment and release
remain unverified because no exact target/version was supplied.

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
- Detailed topical sources remain with the corresponding RES-0002 member and
  RES-0084; this baseline does not duplicate their source inventories.

## Implications

- Preserve the Stage 00 → provider adapter projection and Stage 99 → validator
  contract split; it gives policy and enforcement distinct owners.
- Route actionable gaps as Research → Requirement → Architecture/ADR → Spec →
  Plan → Task → Verification → Independent Review. This research package does
  not authorize their implementation.
- Keep the two aggregate required checks and `strict=true` while they match
  authenticated read-back. On mismatch, use the recorded 12-check rollback
  rather than inventing a replacement.
- Treat live deployment, release, provider quality/cost, persistent memory, and
  editor automation as separate acceptance problems, not as consequences of a
  green documentation or CI gate.

## Traceability

- Topical members and preservation declaration:
  [RES-0002](../0002-agentic-engineering-research-pack/README.md).
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
- Static Compose rendering does not settle the four AUD-0097 domain defects or
  prove service health, durability, recovery, performance, or production fit.
- Mutable external sources may change after 2026-09-05; paid ISO text was not
  accessed and public catalog/definition material is used only within its
  visible boundary.
