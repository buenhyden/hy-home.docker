---
title: "Agent Quality and Security Standards"
version: "1.7.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
---

# Agent Quality and Security Standards

## Overview

Universal quality gate for agent-driven changes in this repository.

## Scope

Change-specific verification, security, reliability, generated freshness, and local or hosted quality routing.

## Rules

### 1. Documentation Quality Rubric

| Grade | Description | Requirements                                                           |
| :---- | :---------- | :--------------------------------------------------------------------- |
| A     | Elite       | Accurate routing, valid commands, no policy conflicts, SSoT alignment  |
| B     | Strong      | Mostly aligned with minor omissions                                    |
| C     | Functional  | Works but has clarity or coverage gaps                                 |
| D     | Weak        | Multiple stale references or ambiguous guidance                        |
| F     | Failing     | Hardcoded secrets, broken governance links, contradictory instructions |

Quality dimensions:

- Actionability: instructions are concrete and testable.
- Conciseness: avoid generic filler.
- Accuracy: references match current repository structure.

### 2. Security Baseline

- Never commit plaintext credentials.
- Prefer secret managers or mounted secret files.
- Keep inter-service networking restricted by intended network boundaries.
- Use least-privilege runtime defaults when modifying infrastructure.
- Identity and access: centralized authentication via Keycloak (OIDC/SAML), and
  least-privilege RBAC/ABAC at API and data layers.
- Secrets management: plaintext credentials in source-controlled configs are
  prohibited; Docker secrets and/or an OpenBao-backed secret flow are mandatory.
- Container hardening, mandatory where compatible: non-root runtime,
  `no-new-privileges`, minimal capabilities, read-only mounts for static
  config, and secret injection by file rather than image layer or plaintext
  environment value. These are manual review expectations unless an existing
  validator or hook enforces the specific field.
- Network hardening: isolate traffic on intended networks and enforce TLS at
  ingress boundaries.

#### Bounded npm risk acceptance

No npm risk acceptance is active. The single bounded acceptance for
GHSA-vfj7-8cjw-p6xm was retired after GitHub withdrew the advisory on
2026-10-23; `leaf.dependency-vulnerability-audit` is again the strict
`npm audit --audit-level=high` run, and the CI contract rejects an
`npm_audit_acceptance` record. A new acceptance needs a reviewed policy
amendment that names the advisory, locked chain, owner approval and an expiry
no more than 30 days after approval, with negative fixtures. An acceptance is
never a vulnerability fix or a branch protection bypass. Never use a skipped
audit, lower threshold, continue-on-error, blanket package exception or
omitted development audit.

Remote PR candidate validation and independent review own candidate acceptance, while
main-push security remains a post-merge observation.

### 3. Reliability Baseline

- Recurring QA covers current document forms, templates, frontmatter, identity,
  relationships, links, lifecycle and preservation, plus this workspace's
  Docker/Compose services, configuration and operations contracts.
- A supporting parser, selector, style controller or release regression must
  prove one of those current contracts. An agent answer score, a past migration
  census or a completed Task's fixed hash is not a recurring quality contract.
- Remove event-specific expectations for a completed document's current
  status, wording or inventory, and contract assertions coupled only to a
  retired file, helper or symbol. Current Registry validators and meaningful
  boundary regressions own continuing guarantees; do not replace obsolete
  expectations with another permanent forbidden-name list. Generic preserved
  byte, recovery and compatibility proofs remain current contracts.
- Explicit Skill evaluation may retain paired task/output/scoring/aggregate
  evidence outside recurring repository QA. The evaluation README routes that
  evidence; agentic policy owns authority and stop conditions. A representative
  score is not whole-Skill coverage, runtime activation or Task acceptance.
- Behavior changes require focused failure reproduction and regression evidence.
  Wording-only changes require applicable content and style validation, not new
  implementation tests or a universal coverage percentage.
- Runtime health, live smoke, operator acceptance, backup and restore evidence
  belong to their approved service Task. Compose render or static hardening does
  not prove any of them. A SEV1/SEV2 incident uses its incident postmortem.
- Retire one-time QA in this order: transfer a continuing guarantee to its
  current owner; remove callers and registration; remove exclusive helpers,
  fixtures and tests; preserve useful actual results in existing Task/history.
  Do not delete generic archive integrity or proof readers needed for preserved
  bytes merely because their inputs are historical. Hold/recovery conditions
  remain owned by the retention contract.
- Shared implementation libraries under `scripts/lib/` and executable QA
  owners retain meaningful test evidence. A nonmutating companion library
  outside that shared surface may be retained through a proven current
  consumer without creating a dedicated purpose-excluded QA suite. Mutation,
  missing consumers, unsafe paths and invalid import claims remain rejected
  by the manifest contract; this grants no runtime acceptance.
- A library's behavioral evidence is judged by its tracked, admitted test owner
  and actual API/fixture use. Directory mirroring is the default organization,
  not a second mandatory evidence source. A registered cross-module or
  entrypoint test may own that behavior without a duplicate library smoke.
  Source-token bans, test-of-test census scans and retired filename assertions
  do not substitute for current mutation, preservation or parser behavior.
- Age, filenames, test counts and failing results alone are not deletion
  criteria. A removed check must have a disposition and any continuing owner.
  Failed required checks remain failures until repaired or deliberately retired
  under the approved contract.

### 4. Execution Boundary

- **Authoring**: explicit formatting may write eligible authored files. Focused
  RED/GREEN and selected read-only lint help diagnose a change. Observe actual
  installed Git hooks separately; tracked configuration does not change a
  user-global hook. Never use SKIP, fake CI variables or `--no-verify`.
- **Local implementation verification**: the workflow contract's typed
  `public_gate.local_only_gate_ids` owns document-library, hook, mocked native
  and other isolated implementation regressions plus local links. The closed
  hosted-unit set is the exception: CI gate-contract, Compose-baseline and
  repository-integrity regressions run in both selected local verification and
  hosted candidate validation. Use
  `scripts/validation/run-ci-gate.py --profile changed --local-only --explain`
  to inspect the complementary local-only plan. Use
  `scripts/validation/run-ci-gate.py --profile changed --explain` and then the
  same command without `--explain` once on the final implementation input when
  a changed owner selects a promoted regression. The shared runner
  and registered path owners remain the execution route; no parallel wrapper
  or command inventory is created. Result-only Task additions receive minimum
  document checks. Do not repeat the local full profile after commit or push.
- **Candidate acceptance**: the public repository uses remote PR QA through
  `scripts/validation/run-ci-gate.py --profile changed`. Inspect the selected
  plan and prerequisites before execution. Every hosted context excludes the
  typed local-only leaves; only the PR context admits the closed hosted-unit
  set above. Push, initial-push and manual-dispatch contexts exclude it so
  merged-input security observation does not repeat candidate QA.
  Before installing PR-controlled dependencies, the candidate captures the
  immutable GitHub event and merge SHA, the raw two-parent merge topology and
  the absolute system Git executable and the configured Python interpreter;
  the capture step uses the fixed system Bash path. Both prerequisite selection
  and gate execution must match that captured identity, ignore replacement refs and
  reject mutable event, SHA or PATH disagreements before contract loading or
  changed-path selection. This binding prevents later PATH redirection; it does
  not make candidate source, installed dependencies or interpreter files
  immutable, so review and the actual hosted result remain acceptance inputs.
  Changes to the workflow contract, Compose baselines, Airflow SQL, n8n
  workflows and their registered repository owners select the applicable
  hosted regression leaf; a nonzero leaf result fails the candidate. Remote QA retains actual document content and
  catalog, diff/style/commit, machine contracts, selected Docker/security,
  frontend build/HTTP/browser integration and actual release configuration checks.
  Mocked release/service/supply-chain negative cases stay intact and selected
  locally; hosted PRs do not execute those unit behaviors. Optional native
  Compose cases remain explicit skips or separately authorized observations;
  the hosted Compose-baseline unit leaf does not start HOME resources or turn a
  skipped native case into a pass. Production guards
  and independent exact-source review still apply. Mixed unit/corpus commands
  must have distinct registered gate IDs and closed modes; invocation identity
  includes argv, and actual corpus checks cannot be discarded with a unit leaf.
  Local implementation PASS is separate evidence and does not satisfy or bypass the remote candidate.
- **Document links**: `check-document-links.py --mode all` owns local-only
  read-only link validation on the final source input before result-only Task
  evidence recording. Record the bound source/base/history and result before
  submission; remote PR and hosted plans exclude this leaf. Result-only Task
  additions use minimum document checks and scoped validation of any new or
  changed link destinations, without repeating the whole link corpus.
  Local focused feedback does not become hosted evidence or trigger another
  candidate aggregate.
- **Before local commit**: after the reviewed change is staged, the
  read-only pre-commit and commit-msg hooks observed on a normal `git commit`
  check the final index, configuration, and message. Do not run the same
  hooks by hand first once their installation and execution are confirmed.
  When delivery of the installed checks is unconfirmed, or a separate
  diagnosis is needed, `scripts/validation/run-ci-precommit.sh --mode
  local-staged` checks an isolated copy of the same registered pins and
  index. A change to that copy, or source or index drift, is also a failure
  and never a reason to bypass the normal hooks. On failure, fix explicitly,
  review the diff, restage, and commit normally again. When the index changes,
  an earlier result is not reused. Keep the effective secret guard and the
  user-global hooks.
- **Server final defense**: the PR candidate runs the same controller with
  `--mode pr-merge` on its authenticated merge input before accepting selected
  builds. As in local mode, every hook runs on an isolated copy and a fixer
  without a check mode may change only that copy, which fails the run. Local
  staged PASS cannot replace that server result. Build steps in
  the same candidate consume its result rather than calling style twice.
  A future deployment must require successful server lint/format evidence for
  its exact promoted revision and configuration before deployment; changed
  inputs require a new server check. The repository currently has no deployment
  workflow, so this rule supplies no deployment execution or acceptance.
- **Validation**: both style-controller modes use a hook's check mode where it
  has one, run every hook on an isolated copy, and preserve source bytes.
  Formatting and validation have separate purposes.
  Direct Agent `pre-commit run` is prohibited; the controlled all-files wrapper
  is an explicitly approved authoring/maintenance lane, never routine PR QA.
- **Execution identity**: deduplicate an identical leaf within one run using
  input/index/base/history, configuration, toolchain, mode and trust. Different
  staged, PR merge and main/security inputs are not interchangeable. Parsed
  immutable Git input may be shared within one invocation; working-tree bytes
  and acceptance are not cached across changed inputs or runs.
- **Prerequisites and budget**: Task planning records selected tools, available
  execution permissions, numeric budget or UNKNOWN, timeout and failure owner
  before required execution. Missing prerequisites block that lane; unrelated
  tools must not block a small document-only plan. Preserve bounded process,
  pipe and descendant cleanup; do not hide environment failures by skipping it.

#### Canonical delivery phase matrix

| Boundary | Automatic owner | Distinct evidence |
| --- | --- | --- |
| Commit | Observed read-only installed pre-commit and commit-msg; the local-staged controller for unconfirmed delivery or diagnosis | Exact index/config and message; effective secret guard |
| Feature push | No repeated public QA | New commits become PR candidate input |
| Agent Stop | Diagnostics only | Working tree; no second aggregate run |
| Before submission | Selected local-only implementation and link leaves once | Final source/index, base/history, tools and actual local result |
| PR to main | One candidate job including pr-merge lint/format before selected builds; excludes local-only leaves | Authenticated base/head/merge, pins, prerequisites and hosted result |
| Main push | Separate security/SARIF observation | Merged SHA and hosted security trust; no candidate suite repeat |
| Release preparation PR | Same candidate owner selects changelog/release checks | Main-targeted CHANGELOG and reviewed source |
| Approved release dispatch | Sole main-only SemVer producer | Exact commit, create-only tag, complete draft assets, publication receipt |
| Future deployment | Server lint/format evidence for exact promoted inputs, then deployment-specific checks | Distinct deployment authority/result; no deployment workflow currently |

The machine workflow contract owns exact job identities, DAG and path-to-root
selection. Ordinary documents retain profile, parent and lifecycle/content
checks remotely, plus operating catalog checks for operations documents. Link
validation belongs only to the local lane. Wording changes do not select Compose,
service, hook, tool or implementation regression suites; these follow their
actual changed owners. Frontend checks follow the frontend project, not every script or workflow
edit. Unknown paths fail closed, including rename/delete evidence. `--explain`
inspects selection without executing a leaf. No wrapper creates a second
orchestration inventory.

Keep the PR workflow present without path/commit skips; a missing required check
can remain pending. Title edits do not cancel revision validation. See
[GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
CodeQL and external security integrations are distinct remote observations;
source edits do not prove that their server-side settings changed. Actual
protection settings require approved mutation and authenticated read-back.

### 8. Workflow and Language Routing

- Follow the sole load order in `.agents/governance/bootstrap.md#canonical-load-order`.
- Follow repeatable orchestration in `.agents/governance/workflows.md`.
- Apply the document language priority in
  `.agents/governance/documentation-protocol.md#document-language` and the
  README navigation rule in
  `.agents/governance/documentation-protocol.md#readme-navigation`.
- Resolve write permission through `.agents/governance/approval-boundaries.md`.

### 9. Completion Routing

Use only `.agents/governance/task-checklists.md#before-completion`. Its conditional
harness, evidence, documentation, and controlled-gate clauses determine which
quality checks apply. PR-specific completion remains owned by the Completion
Gate in `.agents/governance/github-governance.md`.

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Verification

### 5. Change-Type Verification Matrix

Use the smallest meaningful selected checks. This is the sole matrix for all
providers; Task evidence names each input, result, acceptance and unexecuted lane.

| Change | Focused authoring feedback | Remote candidate or distinct observation |
| --- | --- | --- |
| Ordinary documents/templates | Local-only registered links; scoped metadata and read-only style feedback | Profile, relationships and lifecycle; operations catalog when applicable; no link or implementation regression rerun |
| Validator/parser/Registry implementation | RED/GREEN, relevant style and selected local-only implementation regressions | Actual content checks; no local implementation suite repeat |
| Gate/workflow/style controller | Selected local-only selection, trust, failure and cleanup regressions | Actual workflow/contract validators; exact hosted job/event evidence |
| Docker/Compose/service configuration | Relevant syntax/render/hardening feedback | Selected configuration checks; live HOME/smoke/restore only for a named exact target |
| Commit/changelog/release implementation | Commitizen and SemVer/changelog/draft-asset regression | PR candidate checks; release publication only for its approved exact version |
| Historical QA retirement | Caller/registration closure and continuing-owner proof | Applicable current document/archive/runner checks; frozen bytes preserved |
| Remote setting or high-risk runtime | Concrete approved target, before-state and recovery | Actual read-back or runtime receipt; source-only evidence is insufficient |

A PASS check is not criterion acceptance, authorization, integration or runtime
activation. ACCEPTED_RISK remains a typed security exception with its original
expiry, not a vulnerability fix or live service success. No synthetic fixture
proves arbitrary agent prose or provider performance. Missing required evidence
remains FAIL, BLOCKED, NOT_RUN or unverified as applicable. Independent review
reads the exact diff, contract and actual results; the current Task owns it.

### 6. Generated-Artifact Freshness

Some artifacts are generated from repository content and must be regenerated as
part of QA before completion. Treat regeneration as a verification step, not an
optional cleanup.

- **Generated path indexes**: none exist. The repo-local LLM Wiki and its two
  tracked outputs were retired on 2026-09-10 with their generator, so adding,
  removing, or renaming a document no longer carries a regeneration step.
- **Knowledge graph**: `graphify-out/` is local generated intelligence and is
  not tracked. `.gitignore` governs the whole directory, so a rebuild produces
  no diff, needs no commit, and cannot conflict with the `pre-commit`
  intermediate stash. Refresh it with one-shot `graphify update .` when the CLI
  is available, which costs no API tokens, and report when it is skipped. Do not
  re-track it: a rebuild replaced a 148 MiB blob on every graph-touching commit,
  and a clone can regenerate it. The `pre-commit` file hooks still carry
  `exclude: '^graphify-out/'` so a formatter never reaches the working copy.
- **General rule**: never hand-edit a generated artifact to pass a check. Re-run
  its generator and commit the generated result as a separate logical unit.

### 7. Local QA/CI Orchestration

Use `python3 scripts/validation/run-ci-gate.py --profile changed --explain` to render the
selected public suite-to-validator mapping without execution. The public runner
exposes `--profile changed`, `--profile full`, and `--explain` routes and contains
no duplicated child-command inventory. These routes do not
upload SARIF, verify remote branch protection, install CI-only dependencies, or
declare protected-branch readiness. The `repo-contracts` gate also blocks
unjustified runtime-pin duplication in current operational, architecture and
infrastructure README bodies. Compose and Dockerfile declarations own exact
runtime pins; `infra/tech-stack.versions.json` is a curated machine-readable projection,
not a second authored authority. Narrative documents link the relevant sources.
Necessary compatibility, advisory, workaround, migration or historical literals
must state their concrete reason through the Stage 99 exception contract. Current
implementation claims remain subject to drift checks; historical and migration
boundaries are not rewritten to match a newer pin. Document frontmatter versions
are independent. The registered metadata validator owns executable enforcement.

Remote PR QA uses the same public entrypoint and suite manifest; execution
context determines leaf eligibility. A local focused or `full` result is never
proof of a hosted result. Do not fake GitHub environment variables to
invoke CI-only wrappers locally. Record missing tools and unexecuted checks
explicitly; neither absence nor a skipped check is a PASS.

A local run records a result only on the same toolchain as the hosted
controller. Before a LOCAL run, the runner checks that the interpreter
version equals the `python-version` pin in `.github/workflows/ci-quality.yml`
and that the active packages in `scripts/requirements-controller.lock` are
installed at the same versions; otherwise it fails with
`ci-gate-local-toolchain` without running. The build that matches hosted is
the Ubuntu release from `actions/python-versions`, and a build without the
memfd seal constants, such as a uv standalone build, is refused. `--explain`
is not a run, so it skips this check.

The local runner validates `.github/workflow-contract.yml` and the registered
workflow definitions through
`scripts/validation/check-github-workflow-contract.py`. The required
`leaf.local-tech-stack-version-drift` owns version drift detection in every
public context. The public runner admits only the authenticated `--mode pr-merge` invocation.
The explicit `--mode local-staged` route is separate from aggregate QA and runs
real staged checks immediately before commit. Isolated wrapper regressions do
not substitute for an observed local or hosted execution.

#### Explicit Full Audit

`full` is an explicitly scoped comprehensive audit, not a commit, feature-push,
PR, main or release completion ritual. Record its selected context, tools,
budget or UNKNOWN and approval before executing it. LOCAL full includes the
registered local units and content checks; hosted contexts exclude local-only
units and links. A modeled full plan does not prove a workflow executes it.
Unknown changed inputs still expand fail-closed within their actual context.
Do not follow successful selected verification with an unconditional full run.

Final review and evidence-update reuse follow
[Workflows](workflows.md#review-scope-and-evidence-updates), including affected
slice revalidation and mandatory protected-surface expertise. An evidence-only
Task update does not create another independent source-review gate.

#### Gate and Fixture Ownership

A gate owns one current invariant, not a historical document count, a copied
command list, or a Task's observed commit. The workflow manifest owns composition;
agent governance owns approval and completion policy; Stage 99 owns document structure.
A provider adapter and a PR template refer to these owners rather than adding
another unconditional full run or independent checklist.

Both public profiles use one Compose leaf. With no inherited profile override,
it validates every declared selection independently, including port-collision
checks. An explicit operator-selected combination belongs to the standalone
Compose validator, not a second required leaf with the same command.

Focused fixtures are appropriate when a current lifecycle, parser or gate
contract changes. Reuse focused valid/invalid cases for the changed invariant; do not
require model execution or a second all-files sweep for wording-only edits.
Retain negative cases for authorization, ownership, symlinks, and fail-closed
execution. A smaller suite must not mean missing behavioral coverage.

### 10. Formatting and Linting Ownership

At commit time, end-of-file and trailing whitespace are checked by
read-only checkers, mixed-line-ending runs with `--fix=no`, Ruff format with
`--check`, and markdownlint with `fix: false`. When a fix is needed, run the
existing `end-of-file-fixer` and `trailing-whitespace` manual hooks,
`ruff format`, or `markdownlint-cli2 --fix` separately on named files.
Review the fix diff, restage only the needed files or hunks, and commit
normally. A checker must never add unstaged content to the index on its own,
and no separate formatting tool is added.

- `.pre-commit-config.yaml` owns shared formatter and linter invocations;
  registered project-local package scripts own their actual package scope.
  A config file alone does not establish an executing owner. Formatting rewrites
  bytes; linting reports defects, and a syntax/security check is not a formatter.
  Keep one formatting owner per file scope; a scope can have no formatter.
- Check commands must preserve authored source. Use supported check options;
  Agent-invoked all-files pre-commit runs use the controlled isolated final-QA
  boundary and report any resulting diff. Normal automatic Git commit hooks
  retain their existing authorization and must not be bypassed. Explicit
  fixes are reviewed separately and a second formatting pass must be unchanged.
  Ruff format is the Python formatter and `ruff check` is the Python linter.
  Both are registered hooks and both are pinned in `ruff.toml`, which owns the
  format settings and the selected lint rules with the measurement behind each
  selection and each exception.
- Formatting settings are pinned in the repository, not left to a tool default
  or to whichever version a machine has. `ruff.toml` pins Python.
- A repository-registered agent editor hook reports formatting defects and
  does not rewrite files.
  An explicit fix command may format a file only in agreement with the
  registered owner. Where a hook lives outside the repository and cannot be registered,
  the repository states its own boundary in the tool's ignore file;
  `.prettierignore` does this for Prettier.
- Do not add a second tool over a file type that already has an owner. Two
  formatters on one file type is a conflict, not redundancy.
- A registered formatter or linter carries a `files` selector that names the
  scope it owns. A tool that reads more file types than its owner declares is
  the same defect as a second owner: `ruff format` also reformats Python
  fenced inside Markdown, and invoked without that selector it rewrote a
  frozen archive body. The selector, not the invoker's memory, is the boundary.
- A validator must not depend on where a line breaks. A check that a formatter
  can break was satisfied by typography rather than by content, and the
  exemption belongs on the line as a stated marker.
- Adopting or changing a formatter reformats the corpus once, in its own
  commit, after every check that the reformatting would break is fixed.

## Related Documents

- `.agents/governance/github-governance.md`
- `.agents/governance/git-workflow.md`
- `.agents/governance/agentic.md`
