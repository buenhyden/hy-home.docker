---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md -->

# Reference: Automation, Pipeline, and Workflow Loops

## Overview

This reference maps tracked local scripts, hooks, generated-reference checks,
GitHub workflows, and agent orchestration to their triggers, authorities,
evidence, retry behavior, and external-action boundaries. The inventory is from
tracked source at `cf8790ca98ad395bb58c127ea41b1d0d02455f0e`, not from the
older advisory Graphify report.

## Purpose

Make automation loops inspectable without confusing capability with authority,
or local/CI evidence with current remote enforcement.

## Repository Role

This Stage 90 reference explains current automation. It does not create or
change scripts, hooks, workflows, provider settings, task policy, protected
GitHub settings, or external resources.

## Scope

### In Scope

- Actual workflow/job inventory from all tracked workflow YAML
- Local validation, recommendation, hook, synchronization, and generation loops
- CI quality, changelog, version-drift, contributor, labeling, and stale loops
- Task/subagent orchestration and explicit remote approval boundaries

### Out of Scope

- Workflow, script, provider, runtime, credential, or remote-state mutation
- Claims that workflow YAML proves branch protection or required-check settings
- Adoption of DORA, continuous-delivery, or vendor guidance as policy

## Definitions / Facts

- **Automation** repeats a bounded action; its authority comes from the tracked
  owner and user approval boundary, not from its ability to execute.
- **Pipeline** means an ordered or parallel set of checks/actions. In the
  tracked quality workflow no job declares `needs:`, so the YAML does not define
  an inter-job dependency chain.
- **Evidence** is a named exit result, generated freshness result, task record,
  workflow status, or remote observation. A generated artifact must be refreshed
  by its canonical generator, never hand-edited.
- **External boundary** distinguishes local repository state, GitHub-hosted CI,
  and actions that change remote resources or require explicit approval.

## Tracked Workflow and Job Inventory

The following count is derived from job mappings under `jobs:` in each tracked
YAML file, not from workflow filenames or Graphify.

| Workflow | Trigger | Tracked job IDs | Count | Class / caveat |
| --- | --- | --- | --- | --- |
| [`ci-quality.yml`](../../../../.github/workflows/ci-quality.yml) | push/PR to `main`; manual dispatch | `docs-traceability`, `docs-implementation-alignment`, `repo-contracts`, `agent-output-eval-fixture-gate`, `dependency-vulnerability-audit`, `git-flow-contract`, `compose-validation`, `compose-all-profiles-validation`, `infrastructure-hardening`, `template-security-baseline`, `quickwin-baseline`, `pre-commit`, `frontend-quality`, `storybook-coverage`, `zizmor` | 15 | CI jobs; tracked presence does not prove remote required-check enforcement. |
| [`generate-changelog.yml`](../../../../.github/workflows/generate-changelog.yml) | pushed `v*.*.*` tag | `changelog` | 1 | Remote verifier; checks tag coverage in `CHANGELOG.md` and does not generate it. |
| [`greetings.yml`](../../../../.github/workflows/greetings.yml) | newly opened issue/PR | `issue-greeting`, `pull-request-greeting` | 2 | Remote write automation with scoped token permissions. |
| [`pr-labeler.yml`](../../../../.github/workflows/pr-labeler.yml) | opened/synchronized/reopened PR to `main` | `triage` | 1 | Remote PR-label mutation. |
| [`stale.yml`](../../../../.github/workflows/stale.yml) | daily schedule | `stale` | 1 | Remote issue/PR label/close mutation. |
| [`tech-stack-version-sync.yml`](../../../../.github/workflows/tech-stack-version-sync.yml) | PR paths affecting Compose/version registry | `drift-gate` | 1 | Read-only CI drift gate; does not auto-commit. |

Total: **6 workflows, 21 job IDs**. The 15-job local CI contract is distinct
from the historical 12 required remote contexts recorded on 2026-07-04 in
[`main-protection.md`](../../../../.github/rulesets/main-protection.md). This
task did not reverify remote settings, so current enforcement is remote-only and
unknown.

## Automation Loop Matrix

| Automation | Trigger | Authority | Inputs | Actions | Evidence | Failure / retry | Rollback / escalation | External boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Local QA gate runner | Manual invocation: default, `--script-backed`, `--all-profiles`, `--harness`, or `--list` | [`run-local-qa-gates.sh`](../../../../scripts/validation/run-local-qa-gates.sh) | Worktree plus tracked scripts/config | Default, `--script-backed`, and `--all-profiles` execute 12 script-backed gates; `--harness` executes 8; `--list` executes none and only lists responsibilities, including 1 advisory non-executed recommender | Named gate exits for executing modes; list-only stdout for `--list` is not gate evidence | Fix the failing owner, then rerun the named gate or executing mode; correct list ownership separately | Revert authored change; escalate CI/remote-only gaps rather than simulating them | Local only; no SARIF upload, dependency install, branch query, or merge authority |
| QA gate recommender | Working/staged/base diff or explicit paths; CI summary step | [`recommend-qa-gates.sh`](../../../../scripts/validation/recommend-qa-gates.sh) | Changed path list | Prints deduplicated recommendations and remote/manual notes; executes no gate | Advisory stdout or `GITHUB_STEP_SUMMARY` | Correct path selection and rerun; recommendation failure is not gate evidence | Escalate unsupported mappings to the QA owner | Local/CI advisory; no repository, runtime, remote, or secret mutation |
| Post-tool validation | Provider file-edit hook payload | [`post-tool-validate.sh`](../../../../scripts/hooks/post-tool-validate.sh) | JSON payload and changed paths | Normalizes basic whitespace/newlines unless check-only; conditionally runs shfmt, ShellCheck, yamllint, diff, JSON, Compose, repo-contract, and traceability checks | Hook exit and named validator output | Fix changed-path failure and replay payload or run validator directly | `--check` disables writes; revert hook formatting if inappropriate | Local hook; it does not run Prettier or prove CI/remote state |
| Provider-neutral event dispatcher | Session/tool/stop event from a provider adapter | [`agent-event-hook.sh`](../../../../scripts/hooks/agent-event-hook.sh) | Event name, JSON payload, tracked governance and paths | Produces context, warnings, or validation dispatch based on event/path | Hook JSON/output and exit | Correct adapter/event/payload; rerun without inventing unsupported event parity | Escalate provider incompatibility to Stage 00 provider owner | Local adapter; provider behavior is not policy authority |
| Provider-surface sync | Manual default verify or approved `--write` | [`sync-provider-surfaces.sh`](../../../../scripts/operations/sync-provider-surfaces.sh) | Canonical agent catalog, Claude skills, model policy | Compares or generates Codex TOMLs and Gemini pointers | `no drift`, drift list, or write summary | Resolve canonical-source mismatch; verify again | Revert generated projection; policy/model changes need approved Stage 00/04 evidence | Verify is local/read-only; write changes tracked provider adapters, never external accounts |
| Tech-stack version sync script | Manual default write, `--check`, or `--dry-run` | [`sync-tech-stack-versions.sh`](../../../../scripts/operations/sync-tech-stack-versions.sh) | Compose image declarations and curated registry | Detects or updates registry tag drift | `changes=N`, check exit, or written file | Resolve missing/ambiguous image mapping; rerun check | Revert generated registry; runtime changes require separate approval | Local tracked file only; no registry query or deployment |
| LLM Wiki index freshness | Docs path change or explicit generator/check | [`generate-llm-wiki-index.sh`](../../../../scripts/knowledge/generate-llm-wiki-index.sh) | Indexed tracked paths | Generates or verifies Wiki path index | Fresh/stale result; `repo-contracts` coverage | Run generator, inspect generated diff, rerun check | Revert generated output and fix source/index rules | Local generated reference; never hand-edit |
| LLM Wiki coverage freshness | Stage/category coverage change or explicit generator/check | [`generate-llm-wiki-coverage.sh`](../../../../scripts/knowledge/generate-llm-wiki-coverage.sh) | Tracked stage paths and Wiki data | Generates or verifies coverage snapshot | Fresh/stale result | Run canonical generator and rerun check | Revert generated output and escalate schema drift | Local generated reference; never hand-edit |
| Other generated evidence checks | Repo-contract execution or explicit generator `--check` | Canonical scripts listed in [`scripts/README.md`](../../../../scripts/README.md) | Audit pack, security/workflow surfaces, Compose and version registry | Generate/check audit matrix, security readiness, profile coverage, and version provenance | Generator check output and `repo-contracts` | Use only the owning generator; inspect source drift | Report stale generated data before any scope expansion | Local reference generation; does not run scanners, sign artifacts, query registries, or query GitHub |
| CI quality workflow | push/PR to `main` or manual dispatch | [`ci-quality.yml`](../../../../.github/workflows/ci-quality.yml) | Checked-out commit, pinned actions, GitHub runner context | Runs 15 independent job definitions, including docs, contracts, Compose, frontend, coverage, dependency, and `zizmor` evidence | GitHub job/check status and SARIF for `zizmor` | Fix job-specific failure and rerun through GitHub controls | Revert offending commit; permissions/workflow changes require review | Remote GitHub CI; YAML presence does not prove required-check enforcement |
| Tech-stack drift workflow | Relevant PR path filter | [`tech-stack-version-sync.yml`](../../../../.github/workflows/tech-stack-version-sync.yml) | PR Compose/version-registry diff | Runs sync script in read-only `--check` mode | `drift-gate` status | Author updates the registry locally and pushes through approved workflow | Revert mismatched registry/Compose edit; no auto-commit | Remote CI read-only content permission |
| Changelog tag-coverage verification | Push of a semantic-looking `v*.*.*` tag | [`generate-changelog.yml`](../../../../.github/workflows/generate-changelog.yml) | Tag name and tracked `CHANGELOG.md` | Verifies that the pushed release tag already appears in the changelog | `changelog` job status and error naming absent tag | Update changelog through a release-branch PR before repushing tag | Delete/correct an erroneous tag only with explicit remote approval | Remote verifier; despite filename, it does not generate or commit a changelog |
| PR labeler | PR opened, synchronized, or reopened | [`pr-labeler.yml`](../../../../.github/workflows/pr-labeler.yml) | PR file paths and labeler config | Applies path-based labels | `triage` job and resulting labels | Correct config/permissions and rerun via GitHub event/action controls | Remove incorrect labels with approved remote mutation | Remote PR mutation; no local equivalent |
| Stale issue/PR automation | Daily scheduled event | [`stale.yml`](../../../../.github/workflows/stale.yml) | Issue/PR activity age and configured labels/messages | Marks stale, waits seven days, then closes inactive threads | `stale` job plus issue/PR state | Correct workflow/config and rerun on schedule/manual GitHub control if authorized | Reopen/remove label with approved remote mutation; escalate false positives | Remote issue/PR mutation |
| First-interaction greetings | Newly opened issue or PR | [`greetings.yml`](../../../../.github/workflows/greetings.yml) | Event actor/thread and messages | Posts first-interaction message | Two conditional job statuses and comment | Correct permission/message and retrigger only through valid GitHub event | Remove erroneous comment with approved remote mutation | Remote issue/PR write |
| Task and subagent orchestration | Approved Stage 04 task and explicit delegation | [`subagent-protocol.md`](../../../00.agent-governance/subagent-protocol.md) | Spec/plan/task, [`workflows.md`](../../../00.agent-governance/rules/workflows.md), role catalog, handoff/evidence boundary | Routes bounded work, handoff, review, and task evidence | Stage 04 record, implementer report, commit, reviewer verdict | Return to earliest failed owner; do not self-record an independent verdict | Stop/escalate on ambiguity, protected surfaces, or incompatible adapter | Local/repository orchestration; dispatching remote agents or paid jobs requires explicit approval |
| Remote approval and merge boundary | Explicit user authorization plus named remote target | [`approval-boundaries.md`](../../../00.agent-governance/rules/approval-boundaries.md) | Approval source, repository/surface, [GitHub governance](../../../00.agent-governance/rules/github-governance.md), before evidence, rollback path | Permits only the specifically approved read/write action | Before/after remote evidence and task record | Stop when approval or current remote evidence is absent | Roll back through approved GitHub mechanism; never bypass checks/review | Remote-only; current branch protection remains unknown in this task |

## Workspace Comparison and Ownership

| Category | Current state | Primary comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Local automation | Purpose-folder scripts and hook dispatchers expose bounded validate/recommend/sync/generate loops. | pre-commit shows configurable local/CI hooks; EditorConfig/Prettier show tool-specific style automation. | Implemented | Consumers can be mistaken for owners, and advisory output for a gate. | Cite the purpose-folder script and state whether it checks, writes, or only recommends. | `scripts/README.md` | Matrix above and tracked scripts | High |
| GitHub workflows | Six YAML workflows define 21 job IDs and scoped permissions. | GitHub syntax defines triggers/jobs/steps; secure-use guidance frames permissions and action pinning. | Partially Implemented | Current remote required checks and branch protection were not verified on 2026-07-11. | Keep tracked implementation and remote enforcement as separate evidence classes. | `docs/00.agent-governance/rules/github-governance.md` | `.github/workflows/*.yml`, historical local proposal | High |
| Changelog authority | `generate-changelog.yml` only verifies that a pushed tag already appears in `CHANGELOG.md`, while active Stage 00 governance labels it “generate release changelog.” | GitHub syntax distinguishes the tracked steps actually executed from a workflow filename or governance summary. | Partially Implemented | The active governance claim contradicts the tracked workflow and can reintroduce the stale generation claim. | Correct `docs/00.agent-governance/rules/github-governance.md` in separately approved Stage 00 work; do not change policy or workflow in this Stage 90 task. | `docs/00.agent-governance/rules/github-governance.md` | `.github/workflows/generate-changelog.yml:15-42`; `docs/00.agent-governance/rules/github-governance.md:147-155` | High |
| CI feedback | Quality, drift, release-tag, and contributor loops produce inspectable repository-event feedback; the 15 quality jobs have no `needs:` dependency chain. | GitHub Actions defines event-triggered jobs and optional job dependencies. | Implemented | Job definitions and local checks do not prove remote success or required-check enforcement. | Report exact job/run evidence and keep remote enforcement separately verified. | `docs/00.agent-governance/rules/github-governance.md` | Workflow inventory | High |
| CD / deployment promotion | No workflow job uses a GitHub environment or deploys an application/infrastructure target. | GitHub environments gate jobs with reviewers, branch restrictions, protection rules, delayed secret access, and deployment history. | Missing | CI, build, and tag verification are not deployment promotion. | Author a later Stage 03/04 delivery contract before adding environment/promotion automation. | `docs/03.specs/README.md` | Workflow scan; release runbook | High |
| Release records | `CHANGELOG.md`, the manual release-management runbook, and pushed-tag coverage validation exist; no workflow creates a GitHub Release or attaches artifacts. | GitHub Releases associate a tag with release notes and optional downloadable assets. | Partially Implemented | Current evidence lacks an automated release record, artifact identity/integrity, and release-to-deployment linkage. | Keep tag coverage accurately named and define release artifact/record ownership with delivery work. | `docs/05.operations/runbooks/00-workspace/release-management.md` | Changelog workflow and runbook | High |
| Deployment approval | Repository governance requires explicit approval for remote/runtime changes, but no tracked deployment environment implements that approval. | GitHub deployment protection rules can require reviewers/custom checks and prevent secret access until approval. | Partially Implemented | Policy intent is not an executable deployment gate. | Preserve the manual hard stop and implement environment controls only after a concrete target and rollback contract are approved. | `docs/00.agent-governance/rules/approval-boundaries.md` | Stage 00 policy; workflow absence | High |
| Deployment rollback | Stage 05 release readiness requires affected recovery links and backup/N/A evidence; no generic automated rollback is tracked. | OWASP SAMM Secure Deployment expects repeatable deployment, security milestones, deployment records, and stop/reverse behavior for unacceptable defects. | Partially Implemented | Documentation coverage does not prove tested application/data rollback. | Route service-specific rollback, migration compatibility, and recovery verification to the later runtime/delivery specifications. | `docs/05.operations/runbooks/00-workspace/release-management.md` | Release runbook and service runbooks | Medium |

## Analysis

The repository has multiple loops rather than one pipeline. Local validators
fail fast; recommenders only advise; hooks react to provider events; generators
own derived data; CI supplies remote runner evidence; issue/PR workflows mutate
GitHub state. The explicit boundary prevents a green local run from being
presented as SARIF upload, required-check satisfaction, merge readiness, or
continuous-delivery performance.

## Application Notes for This Workspace

- Name the trigger, canonical authority, mutation behavior, and evidence for
  every automation claim.
- Treat the local runner as a subset, not a full CI replica.
- Treat `generate-changelog.yml` as pushed-tag coverage verification.
- Keep the contradictory Stage 00 “generate release changelog” label visible as
  an unresolved governance gap until separately approved policy work corrects
  `docs/00.agent-governance/rules/github-governance.md`.
- Treat current branch protection/required checks as unknown until a direct
  read-only remote check is recorded.
- Never repair stale generated data by hand; run the canonical generator or
  report the scope expansion needed.

## Potential Follow-up / Gap

- Reverify remote branch protection and required contexts in a separately
  authorized GitHub audit.
- Keep the tracked 15-job CI contract and any remote required-check list coupled
  only through approved governance/workflow work.
- In separately approved Stage 00 work, correct the non-gating automation table
  in `docs/00.agent-governance/rules/github-governance.md` so it describes
  pushed-tag coverage verification; the workflow itself needs no behavior
  change for this documentation drift.
- Define delivery metrics only when an application/service deployment and
  incident data source exists.

## Source Rules

- Fixed external sources were retrieved on **2026-07-11**; the Task 4 source
  ledger records supported claim, local/CI/remote class, and caveat.
- GitHub and tool pages are mutable retrieval-time guidance.
- Repo-local facts come from tracked workflow/job/script/config definitions;
  Graphify is advisory and was not used for counts.
- No source listed here is adopted policy.

## Sources

- [Task 4 source ledger](../../../04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md) - fixed-source retrieval and caveats
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - triggers, permissions, jobs, and steps
- [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) - least privilege, untrusted input, secrets, and action pinning
- [GitHub deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) - environment approvals, restrictions, secrets, and protection rules
- [GitHub deployment history](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history) - commits, environments, workflow logs, URLs, and deployment status history
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) - tagged release records, release notes, and assets
- [OWASP SAMM Secure Deployment](https://owaspsamm.org/model/implementation/secure-deployment/) - documented/automated deployment, security milestones, separation of duties, and secret handling
- [pre-commit](https://pre-commit.com/) - local/CI hook orchestration and skip behavior
- [EditorConfig](https://editorconfig.org/) and [specification](https://spec.editorconfig.org/) - editor-level style automation and precedence
- [Prettier overview](https://prettier.io/docs) and [CLI](https://prettier.io/docs/cli) - formatter and check-mode behavior
- [DORA metrics](https://dora.dev/guides/dora-metrics/) - five service-level delivery metrics and context caveat
- [Martin Fowler: Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html) - releasability and automated pipeline feedback
- [Scripts README](../../../../scripts/README.md) - canonical script inventory and lifecycle
- [Tracked workflows](../../../../.github/workflows/ci-quality.yml) - workflow/job implementation entry point

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when workflows, scripts, hooks, generated references, remote evidence, or primary guidance changes
- **Update Trigger**: Re-enumerate every `jobs:` mapping and every local runner step from tracked source

## Related Documents

- [research pack index](./README.md)
- [quality, CI, CD, QA, and formatting](./quality-ci-formatting.md)
- [loop engineering](./loop-engineering.md)
- [workspace baseline](./workspace-baseline.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)
