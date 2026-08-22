---
status: active
artifact_id: plan-0135
artifact_type: plan
parent_ids:
  - spec-0135
created: 2026-07-28
updated: 2026-08-11
---
# Target Surface Delta Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` for task-by-task implementation and
> independent review. Use `superpowers:executing-plans` for controller
> tracking. Every executable step uses checkbox (`- [ ]`) syntax.

**Goal:** Classify and converge the target-surface delta after Spec 133,
normalize confirmed document and version drift, harden the tracked GitHub
Actions/QA control plane, and reconcile canonical evidence without changing
live services or remote GitHub state.

**Architecture:** Spec 133 remains immutable predecessor evidence. A new
duplicate-safe delta manifest classifies every later target change and a
whole-surface validator checks the current repository independently of that
manifest. Native files keep native schemas; README and typed Markdown use
consumer-selected Stage 99 profiles. The local workflow contract becomes the
machine authority for exact triggers, jobs, permissions, direct Action
dependencies, typed CI gates, required-job roots, and local profile roots. A
dependency-free runner expands that declarative DAG and executes verified
first-party entry points without shell interpretation, while Stage 90 remains
observation/evidence rather than desired state.

**Tech Stack:** Python 3.12 standard-library JSON and subprocess APIs, PyYAML
for GitHub workflow documents, Bash, JSON-compatible YAML, Markdown/CommonMark,
GitHub Actions, actionlint, ShellCheck, markdownlint-cli2, pre-commit 4.6.1,
unittest, Git, and repository-owned generators.

**Revision R1 resume checkpoint:**
`a0f91bb50cbd589abdecd8cd217d1673ac0e76d9`

**Revision R2 status:** Revision R1 exhausted its two-attempt Plan review loop
with unresolved Important findings and returned to design/plan. The user
approved Revision R2 on 2026-07-29. Its first fresh review attempt returned
specification `C0/I5/M0` and quality/security `C0/I0/M0`; the bounded
correction then received final independent specification and quality/security
`C0/I0/M0` approvals over `e97b7966..8f82e88b`. Local Plan-bounded
T-TSDC-004R implementation reached the Task 4.4 review gate, but its two
implementation-remediation attempts exhausted with one remaining Important
option-bearing wrapper bypass. The user approved the bounded
T-TSDC-004R-4W design return on 2026-07-30. Its initial and sole corrected
Plans failed review, so 4W is retained only as non-executable design evidence.
The user approved T-TSDC-004R-4X on 2026-07-30 to correct GNU `env --`
assignment semantics and make every checkpoint proof session-local. Its
specification review passed, but its quality/security review found two
Important proof-oracle defects, so 4X is also non-executable history. The user
approved T-TSDC-004R-4Y on 2026-07-30 to make every authority block fail-fast
and bind Task 4.5 to the complete Plan-to-review lineage, exact scopes, and
file modes. Its quality/security review found one remaining substitution-status
masking defect, so 4Y is also non-executable history. The user approved
T-TSDC-004R-4Z on 2026-07-30 to require standalone capture of every fallible
command substitution before its value is tested. Its specification review
passed, but its quality/security review found an immediate-consumption
contract mismatch, so 4Z is also non-executable history. The user approved
T-TSDC-004R-4AA on 2026-07-30 to pair every non-RED capture with an immediately
following value test. Its Plan reviews passed, but its sole implementation
attempt failed fresh specification and quality/security review because
short/attached/clustered GNU `env -S` handling skipped the first inserted
token, unresolved dynamic command heads could fail open, and malformed signal
option near-prefixes could be accepted. The user approved
T-TSDC-004R-4AB on 2026-07-30 as a Plan-only bounded successor that makes
`dispatch`, `no-dispatch`, and `ambiguous` explicit, re-enters the same
budgeted `env` parser at the first split token, and recognizes only exact
signal option spellings. Its fresh Plan reviews each returned `C0/I2/M0`
because long split-string and no-relevant dynamic witnesses were missing,
ambiguous candidate collection could drop an embedded sibling, and unresolved
positional targets were excluded. The user approved T-TSDC-004R-4AC on
2026-07-30 as a bounded in-place successor that unions every exact and
embedded candidate, covers named and positional dynamic targets in both
positive and negative directions, and proves both long split-string forms.
Its specification Plan review returned `C0/I0/M0`, but quality/security
returned `C0/I1/M1`: terminal evidence sessions did not each rebind the full
reviewed predecessor chain, distances, exact scopes, and modes, so a
same-subject substituted lineage could receive evidence for a range the
reviewers did not inspect. The no-correction 4AC loop is exhausted without an
implementation attempt. The user approved T-TSDC-004R-4AD on 2026-07-30 as a
Plan-only bounded successor. Its Plan committed as `9de469a5`, and fresh
reviewers inspected exact range
`3510e9944655ee89077a295712e759d116e2e87f..9de469a52c4b05d2490d36d37b95b1277442f725`.
Specification returned `C0/I2/M1`; quality/security returned `C0/I0/M0`.
Rejected Task-only evidence committed as `5644c4a3`, so 4AD is
non-executable history. The user then approved T-TSDC-004R-4AE as a Plan-only
bounded repair. Its Plan checkpoint committed as `8abea15a`; its exact reviewed
range was `5644c4a301e38d3f0c32efe99e80f879df6e1ac8..8abea15a1ebafdf607be801789a409e6f312c099`.
Specification returned `C0/I0/M0`; quality/security returned `C0/I2/M0`, so
rejected Task-only evidence committed as `8cacc463`. The user then approved
T-TSDC-004R-4AF as a Plan-only repair. Its sole implementation attempt is now
historical and review-rejected because the frozen Step 4 evidence envelope
mistook valid silent success for failure. The user approved
T-TSDC-004R-4AG as the Plan-only successor: it supersedes only that delta
command capture/evidence envelope. Its Plan review exhausted at XP_AG. The
user subsequently approved T-TSDC-004R-4AH as the Plan-only successor from
clean D_AH `e9100b62f6ea18e2a003cfa805b14a7ad61a64ad`. Its Plan checkpoint committed
as `9ff217e63eaf452871cfc3ef47775e0fbd03e706`, but the fresh quality/security
review found that wrapper execution and the E_AH evidence commit were split
across sessions. Rejected Task-only XP_AH committed as
`88f55837be251318cd697bd8a1ab3a4f0ed1a824`, so 4AH is historical,
rejected/exhausted evidence. T-TSDC-004R-4AI was the Plan-only successor from
that clean XP_AH/D_AI checkpoint. It addressed the session-binding defect by
designing approval consumption, one byte-safe wrapper call, sanitized evidence
capture, E_AI commit, and postcommit proof as one self-contained transaction.
Its approval stopped after P_AI, two fresh independent Plan reviews over exact
`D_AI..P_AI`, and exactly one Task-only B_AI or XP_AI terminal. Those facts are
historical only and grant no current tests, validators, wrapper/proof,
revalidation, implementation, E_AI, R_AI, Wave C, runtime, remote, dependency,
secret, direct pre-commit, controlled-wrapper, or Graphify-update authority.

T-TSDC-004R-4AL was the approved executable Plan from D_AL
`2d2f49dfccb5fec282b2792fe0984d80327b4254` through exact S_AL
`eafdaf0433d9e600abbc9b8e2443bdd7b84a9868`. P_AL resolves only by exact unique
subject `docs(plan): define atomic reviewed-blob terminal proof`; its OID is
intentionally not self-asserted in its own tree. Four pairwise-distinct
candidate/formal reviewers and exactly one future Task-only B_AL or XP_AL are
the only authority P_AL originally granted. implementation, E_AL, R_AL, XE_AL,
Task 4.5, Wave C, Tasks 5–6, runtime, remote/external actions,
QA-wrapper/pre-commit execution, dependency changes, and Graphify update were
blocked/no authority under 4AL.

T-TSDC-004R-4AL later failed closed at terminal pre-publication proof. The
four immutable review reports selected XP_AL, but the frozen renderer omitted
two active asset-freeze projections and left current-transaction-not-run text
in its candidate Task. No publisher ran and no B_AL/XP_AL commit exists. On
2026-08-02 the user approved a new T-TSDC-004R-4AM correction design from exact
P_AL `fb05e296b6a791f850cf64d99c7dc17577bb7cfc`. Exact S_AM
`9eeb6365e4537de311f2bb46e80171c8719ef9c2` records the approved design; this
P_AM Plan may define the bounded planning-asset freeze and review sequence.
This approval does not authorize 4AL retry or
correction,
implementation, E_AL, R_AL, XE_AL, E_AM, R_AM, XE_AM, Task 4.5, Wave C,
Tasks 5–6, runtime, remote/external actions, QA-wrapper/pre-commit execution,
dependency changes, or Graphify update.

## Global Constraints

- Work only in
  `.worktrees/target-surface-delta-convergence` on
  `feat/135-target-surface-delta-convergence`; keep the root checkout on
  `main`.
- Preserve every Spec 133 path at its exact closure content. The immutable
  comparison commit is
  `63039b5b0b20c99a10aae7162627afefcd7a1d8b`.
- Use local implementation base
  `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`.
- The primary target roots are `.github`, `archive`, `examples`, `infra`,
  `projects`, `scripts`, `secrets`, and `tests`. Direct-impact edits outside
  them require a named TSDC requirement and a real target consumer.
- Native workflow, Compose, YAML, JSON, TOML, Python, shell, source, and test
  files must not receive Markdown frontmatter.
- README files remain profile-selected navigation and local-context surfaces.
  Shared governance belongs in Stage 00 or Stage 99, not copied README
  sections.
- Root `archive/**` uses the content-archive contract.
  `docs/98.archive/**` uses the SDLC-archive contract. Do not merge them.
- Secret work is limited to tracked names, paths, redacted inventory, and
  value-free validation. Do not read or persist payloads, credentials, tokens,
  auth files, shell history, or raw secret-bearing logs.
- Preserve historical or negative-fixture uses of `legacy` and `deprecated`.
  Remove only confirmed active obsolete paths with consumer, replacement,
  provenance, rollback, test, and two-review evidence.
- Do not start, stop, inspect, recreate, or mutate live Compose services.
  Static tracked version reconciliation is allowed; runtime change is not.
- Keep `.github/workflows/ci-quality.yml` as the sole required-quality
  workflow and preserve its 16 exact unique job IDs.
- Keep `.github/workflow-contract.yml` as the only CI registry. Schema version
  2 uses deterministic strict JSON syntax, which is also valid YAML, so the
  runner can bootstrap with the Python standard library before dependency
  installation. Do not create a generated or hard-coded parallel command
  registry.
- Required-quality executable steps may use only an immutable registered
  `uses:` action or the exact static
  `python3 scripts/validation/run-ci-gate.py --profile ci --gate <gate-id>`
  grammar. Non-gating automation retains its separate registered contract.
- Treat T-TSDC-001 through T-TSDC-003 and the original five T-TSDC-004
  remediation rounds as historical evidence. Do not rerun, rewrite, or
  reclassify them during the R1 recovery.
- Do not push, open or merge a pull request, dispatch a workflow, or mutate
  remote branch protection, rulesets, required checks, environments,
  variables, secrets, repository settings, or credentials.
- Dated remote observations may use sanitized metadata only. Local tests do
  not prove remote execution or enforcement.
- Use TDD for validators, workflow contracts, generators, scripts, and
  routing. Record the expected RED before the smallest GREEN change.
- Each logical task uses a fresh implementer, a distinct specification
  reviewer, and a distinct quality/security reviewer. Critical and Important
  findings must be remediated and re-reviewed.
- Each prospective R1 work unit ends in one independently revertible
  Conventional Commit. The six top-level Spec task identities remain stable;
  recovery commits do not rewrite historical commits. Generated-owner fallout
  belongs to the owning work unit.
- Use only the canonical `bounded-implementation-loop` and
  `independent-review-loop` from
  `docs/00.agent-governance/providers/registry.yaml`, each with
  `max_attempts: 2`. Exhaustion blocks the work unit and returns to
  design/plan; no prompt-local extra retry budget is created.
- Never run `pre-commit run --all-files` directly. A final Agent all-files run
  requires a new exact user approval and
  `scripts/validation/run-agent-precommit-all-files.sh` from a clean committed
  worktree.
- The CI-only pre-commit entry point created by Task 4 is not an Agent
  authorization route.
- Do not use `git reset --hard`, discard unrelated work, or overwrite another
  agent's edits.

## Overview

This Plan implements
[Spec 135](spec.md)
through six serial top-level tasks:

1. create the successor delta manifest, validator, and whole-surface contract;
2. normalize README, typed example, archive, project, and redacted secret
   documentation;
3. reconcile static version drift and verified active legacy/deprecated
   residue;
4. replace free-form CI semantic interpretation with a typed gate registry,
   dependency-free runner, and exact workflow/local projections;
5. refresh canonical audit, generated, and remote-observation evidence;
6. promote enforcement, run the final validation ladder, and close independent
   reviews.

The sibling
[Task ledger](task.md)
records actual commands, results, commits, deviations, deletion evidence, and
review verdicts. It does not duplicate planned implementation.

### Revision R1 Resume Boundary

- T-TSDC-001 through T-TSDC-003 remain completed.
- The original T-TSDC-004 implementation and five remediation rounds remain
  blocked historical evidence. No finding is waived and no old retry is
  reopened.
- Commit `a0f91bb5` contains the approved revised Spec and is the only R1
  planning base.
- T-TSDC-004R may start only after this revised Plan has explicit user
  approval and the complete corrected range receives independent
  specification and quality/security reviews with no Critical or Important
  finding.
- T-TSDC-005 and T-TSDC-006 remain serially blocked until T-TSDC-004R has
  completed specification and quality/security reviews.
- Plan text stays prospective. Existing commands, results, commits, and
  review verdicts remain in the Task ledger and are not normalized here.

## Context and Inputs

### Approved Inputs

- [Spec 135](spec.md)
- [Spec 133](../spec-0133-target-surface-contract-convergence/spec.md)
- [Spec 134](../spec-0134-agent-governance-canonical-convergence/spec.md)
- [Canonical implementation audit](../../90.references/audits/ref-0019-readme.md)
- [GitHub governance](../../00.agent-governance/policies/github-governance.md)
- [Approval boundaries](../../00.agent-governance/policies/approval-boundaries.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Existing target-surface manifest](../../90.references/data/governance/document-corpus-lifecycle/ref-0069-target-surface-convergence.yaml)
- [Existing target-surface checker](../../../scripts/validation/check-target-surface-contract.py)

### Verified Baseline

| Evidence | Fixed value |
| --- | --- |
| Feature base | `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74` |
| Spec 133 closure comparison | `63039b5b0b20c99a10aae7162627afefcd7a1d8b` |
| Current target inventory | 474 tracked paths |
| Target distribution | `.github` 16, `archive` 1, `examples` 9, `infra` 275, `projects` 52, `scripts` 53, `secrets` 19, `tests` 49 |
| Current document inventory | 82 Markdown/MDX files, including 75 READMEs |
| Post-closure target delta | 102 paths |
| Existing target tests | 40 passing tests at feature base |
| Canonical audit distribution | 77 Implemented, 60 Partial, 13 Missing, 2 N/A, 9 Needs Revalidation; total 161 |
| Local required-quality contract | 16 exact job IDs |
| Remote required contexts observed | 12 contexts; four locally desired contexts absent |
| Static tech-stack drift | Six registry values behind Compose declarations |
| R1 resume checkpoint | `a0f91bb50cbd589abdecd8cd217d1673ac0e76d9` |
| R1 current boundary | Tasks 1–3 complete; original Task 4 blocked after five rounds; Tasks 5–6 not started |

### External Sources

The implementation retains source URL and 2026-07-28 KST retrieval context
for the original facts and the 2026-07-29 KST CI design revalidation:

- GitHub workflow syntax:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub secure use:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- GitHub protected branches:
  <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches>
- GitHub reusable workflows:
  <https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows>
- GitHub Action metadata syntax:
  <https://docs.github.com/en/enterprise-cloud%40latest/actions/reference/workflows-and-actions/metadata-syntax>
- GitHub Actions Node 20 retirement:
  <https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/>
- GitHub self-hosted runner minimum-version enforcement:
  <https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/>
- pre-commit:
  <https://pre-commit.com/>
- GitHub YAML frontmatter:
  <https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter>
- CommonMark 0.31.2:
  <https://spec.commonmark.org/0.31.2/>
- GitHub Flavored Markdown:
  <https://github.github.com/gfm/>

The pinned official manifests for `actions/checkout`,
`actions/setup-python`, `actions/setup-node`, `actions/first-interaction`,
`actions/labeler`, `actions/stale`, `astral-sh/setup-uv`, and
`github/codeql-action/upload-sarif` declare Node 24 at their current tracked
SHAs. The pinned `pre-commit/action` manifest is composite and calls
`actions/cache@v4` by mutable tag, so Task 4 removes that path rather than
claiming its outer SHA makes the dependency graph immutable.

## Goals and Non-goals

### Goals

- Preserve Spec 133 while classifying the exact successor delta.
- Fail closed on omitted changed paths and whole-surface drift classes.
- Normalize target documentation without blanket metadata or template filler.
- Register the sample service as an explicit typed example fixture.
- Synchronize safe secret-path inventory without reading values.
- Reconcile six tracked static image-version drifts and their direct evidence.
- Preserve exact CI status identities while proving typed suite ownership and
  one-time DAG reachability.
- Use one schema version 2 registry with `gate_nodes`, `job_roots`, and
  `profile_roots`; remove free-form `owner_commands` and
  `expensive_commands`.
- Execute registered first-party entry points through a deterministic,
  non-shell runner with confined path, provenance, environment, and timeout
  controls.
- Enforce exact workflow triggers, permissions, timeouts, concurrency, and
  direct Action dependencies.
- Separate CI pre-commit execution from separately approved Agent execution.
- Record current remote state as dated observation, not local truth.
- Update only affected canonical audit rows and deterministic generated owners.
- Close every task through independent specification and quality/security
  review.

### Non-goals

- Live Compose, infrastructure, deployment, release, environment, or secret
  mutation.
- Remote GitHub mutation, push, pull request, workflow dispatch, or merge.
- Reading raw remote workflow logs or inferring an unverified failure cause.
- Rewriting the predecessor manifest, summary, Task evidence, or reviews.
- Applying one frontmatter schema to every Markdown document.
- Deleting historical evidence or negative fixtures because they contain
  lifecycle terminology.
- Creating a broad new `example` artifact type when the existing service
  template role can register the exact fixture path.
- Claiming self-hosted runner readiness without an authenticated runner
  inventory.

## Requirement Coverage

| Spec requirement | Owning task | Planned completion evidence |
| --- | --- | --- |
| TSDC-001, TSDC-002 | T-TSDC-001, T-TSDC-006 | predecessor hashes, exact delta coverage, blocking final contract |
| TSDC-003 | T-TSDC-001 through T-TSDC-004 | native parsers and no-frontmatter whole-surface checks |
| TSDC-004, TSDC-005 | T-TSDC-002 | exact README headings, typed fixture registration, metadata tests |
| TSDC-006, TSDC-007 | T-TSDC-002 | archive split and value-free secret inventory tests |
| TSDC-008, TSDC-009 | T-TSDC-002, T-TSDC-003 | owner routing and reviewed disposition ledger |
| TSDC-010 | T-TSDC-004R | exact workflow trigger and permission contract |
| TSDC-011 | T-TSDC-004R | unchanged 16-job identity across four owners |
| TSDC-012 | T-TSDC-004R | one schema v2 registry; unique leaf `suite_key`; one required-job root owner; at most one reachable workflow execution; ordered fake-executor proof |
| TSDC-013 | T-TSDC-004R | full-SHA Action registry and Node 20 rejection |
| TSDC-014 | T-TSDC-004R | separate CI and Agent pre-commit authority paths |
| TSDC-015 | T-TSDC-005 | dated local/remote observation with unverified boundaries |
| TSDC-016 | T-TSDC-005, T-TSDC-006 | affected audit rows and generated summaries fresh |
| TSDC-017 | all tasks, T-TSDC-004R, T-TSDC-006 | independently revertible logical units, task reviews, cutover review, and whole-branch reviews |

## Work Breakdown

### Task 1: T-TSDC-001 — Establish the Successor Delta Contract

**Files:**

- Create `scripts/validation/target_surface_delta_contract.py`.
- Create `scripts/validation/check-target-surface-delta-contract.py`.
- Create `tests/validation/test_target_surface_delta_contracts.py`.
- Create
  `docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml`.
- Create
  `docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md`.
- Modify `docs/90.references/data/governance/README.md`.
- Modify `docs/99.templates/support/document-metadata-profiles.yaml`.
- Modify `scripts/validation/check-repo-contracts.sh`.
- Modify `scripts/validation/run-local-qa-gates.sh`.
- Modify `scripts/README.md`.
- Modify `.pre-commit-config.yaml` only to route the new checker through the
  existing `check-repo-contracts` hook selector; do not create a second
  repository-contract hook.
- Modify the sibling Task ledger.

**Interfaces:**

```text
TARGET_ROOTS: Final[tuple[str, ...]]
DELTA_MANIFEST: Final[pathlib.PurePosixPath]
DELTA_SUMMARY: Final[pathlib.PurePosixPath]

@dataclass(frozen=True, order=True, slots=True)
class DeltaFinding:
    code: str
    path: str
    message: str

@dataclass(frozen=True, slots=True)
class DeltaManifestRow:
    path: str
    surface_class: str
    profile: str | None
    changed_since: str
    disposition: str
    canonical_owner: str
    direct_consumers: tuple[str, ...]
    finding: str
    replacement: str | None
    secret_safety: str
    validators: tuple[str, ...]
    tests: tuple[str, ...]
    provenance: tuple[str, ...]
    rollback: tuple[str, ...]
    spec_verdict: str
    quality_verdict: str

@dataclass(frozen=True, slots=True)
class DeltaManifestDocument:
    schema_version: int
    predecessor_closure: str
    implementation_base: str
    enforcement: str
    target_roots: tuple[str, ...]
    entries: tuple[DeltaManifestRow, ...]

@dataclass(frozen=True, slots=True)
class TargetInventory:
    paths: tuple[str, ...]
    counts_by_root: tuple[tuple[str, int], ...]
    markdown_count: int
    readme_count: int

def changed_target_paths(
    root: pathlib.Path,
    predecessor_commit: str,
    roots: tuple[str, ...] = TARGET_ROOTS,
) -> tuple[str, ...]

def load_delta_manifest(
    root: pathlib.Path,
    path: pathlib.PurePosixPath = DELTA_MANIFEST,
) -> DeltaManifestDocument

def validate_delta_manifest(
    root: pathlib.Path,
    document: DeltaManifestDocument,
) -> tuple[DeltaFinding, ...]

def current_target_inventory(root: pathlib.Path) -> TargetInventory

def render_delta_summary(
    document: DeltaManifestDocument,
    inventory: TargetInventory,
) -> str

def bootstrap_delta_manifest(
    root: pathlib.Path,
    output: pathlib.Path,
    predecessor_commit: str,
    implementation_base_commit: str,
) -> None

def main(argv: list[str] | None = None) -> int
```

The CLI defaults to check mode, accepts `--mode advisory|blocking`,
`--bootstrap`, `--write-summary`, `--predecessor-commit`, and
`--implementation-base-commit`, and emits sorted, value-free diagnostics.
Bootstrap is accepted only when the output does not already exist. Changed
path coverage is the union of the predecessor-to-`HEAD` Git delta and staged
or unstaged target paths, so implementation work cannot evade classification.

- [ ] Add RED tests for duplicate YAML keys, unknown fields, noncanonical
  paths, missing target roots, wrong baselines, invalid dispositions, unsafe
  secret fields, and unstable diagnostic ordering.
- [ ] Add RED
  `DeltaCoverageTests.test_every_changed_target_path_has_exactly_one_row` using
  a temporary Git repository with committed and uncommitted target changes.
- [ ] Add RED
  `PredecessorIntegrityTests.test_spec_133_artifacts_match_closure_commit` and
  assert byte equality against the closure commit without modifying
  predecessor files.
- [ ] Add RED
  `DestructiveDispositionTests.test_migrate_and_delete_require_complete_evidence`
  for consumers, replacement/withdrawal, provenance, rollback, tests, and two
  review verdicts.
- [ ] Add RED
  `WholeSurfaceTests.test_current_inventory_is_complete_and_native_safe` for
  tracked-path enumeration, symlink/non-regular rejection, README profile
  selection, native no-frontmatter, and value-free secret handling.
- [ ] Run the focused module and record the expected failures before adding
  the implementation.
- [ ] Implement duplicate-safe, size-bounded, no-follow readers and canonical
  relative path parsing. Never include raw file payloads in findings.
- [ ] Bootstrap the 102-row successor manifest from the two fixed commits,
  manually classify every row as `preserve`, `update`, `migrate`, or `delete`,
  and set initial `enforcement: advisory`.
- [ ] Register the summary as generated output with this checker as owner and
  write it deterministically.
- [ ] Integrate advisory delta validation into repository contracts and local
  QA listing/execution without adding a duplicate pre-commit hook.
- [ ] Run:

```bash
python3 -m unittest tests.validation.test_target_surface_delta_contracts -v
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
python3 scripts/validation/check-target-surface-delta-contract.py --write-summary
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
python3 scripts/validation/check-target-surface-contract.py
python3 scripts/validation/check-document-metadata.py --mode check-contracts
bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected GREEN: all focused tests pass; predecessor integrity passes; the
manifest covers every computed delta path exactly once; the generated summary
is fresh; existing target contracts remain green; advisory findings are
explicit and value-free.

- [ ] Update the Task ledger with RED/GREEN counts, changed paths, manifest
  counts, and implementation-agent handoff.
- [ ] Obtain independent specification and quality/security reviews.
- [ ] Commit as
  `feat(governance): establish target surface delta contract`.

### Task 2: T-TSDC-002 — Converge Documentation Surfaces

**Files:**

- Modify `infra/04-data/README.md`.
- Modify the 11 confirmed README heading-drift files:
  `infra/01-gateway/nginx/README.md`,
  `infra/01-gateway/traefik/README.md`,
  `infra/02-auth/keycloak/README.md`,
  `infra/04-data/analytics/README.md`,
  `infra/04-data/analytics/influxdb/README.md`,
  `infra/04-data/analytics/ksql/README.md`,
  `infra/04-data/analytics/opensearch/README.md`,
  `infra/04-data/analytics/warehouses/README.md`,
  `infra/05-messaging/rabbitmq/README.md`,
  `infra/07-workflow/n8n/README.md`, and
  `infra/09-tooling/README.md`.
- Modify the 26 confirmed shared-agent-policy README consumers:
  `infra/01-gateway/nginx/README.md`,
  `infra/01-gateway/traefik/README.md`,
  `infra/02-auth/README.md`,
  `infra/02-auth/keycloak/README.md`,
  `infra/02-auth/oauth2-proxy/README.md`,
  `infra/03-security/README.md`,
  `infra/03-security/vault/README.md`,
  `infra/04-data/analytics/README.md`,
  `infra/04-data/analytics/influxdb/README.md`,
  `infra/04-data/analytics/ksql/README.md`,
  `infra/04-data/analytics/opensearch/README.md`,
  `infra/04-data/analytics/warehouses/README.md`,
  `infra/05-messaging/README.md`,
  `infra/05-messaging/kafka/README.md`,
  `infra/06-observability/README.md`,
  `infra/06-observability/alertmanager/README.md`,
  `infra/06-observability/alloy/README.md`,
  `infra/06-observability/prometheus/README.md`,
  `infra/06-observability/pushgateway/README.md`,
  `infra/06-observability/pyroscope/README.md`,
  `infra/06-observability/tempo/README.md`,
  `infra/07-workflow/README.md`,
  `infra/07-workflow/airflow/README.md`,
  `infra/07-workflow/n8n/README.md`,
  `infra/08-ai/README.md`, and `infra/README.md`.
- Modify `examples/sample-web-service/service.md`.
- Modify `secrets/README.md`.
- Preserve `archive/Windows-Network-IP.md` unless a new failing contract proves
  a defect.
- Modify `docs/99.templates/support/document-metadata-profiles.yaml`.
- Modify `docs/99.templates/support/template-selection.md`.
- Modify `docs/99.templates/support/readme-profile-contract.md`.
- Modify `scripts/validation/check-document-metadata.py`.
- Modify `scripts/validation/target_surface_contract.py`.
- Modify `tests/validation/test_document_metadata.py`.
- Modify `tests/validation/test_target_surface_contracts.py`.
- Modify the Task 1 manifest/summary and sibling Task ledger.

**Interfaces and exact decisions:**

- Add `examples/sample-web-service/service.md` as an exact second
  `target_globs` entry on the existing `service` template role.
- Keep `artifact_type: spec`, set `status: draft`, use
  `artifact_id: spec:sample-web-service`, and set parents to
  `spec:126-security-supply-chain-remediation` and
  `spec:127-deployment-release-engineering-remediation`.
- Treat the file as an explicit consumer-backed example fixture, not as
  accepted current SDLC truth. Do not create an `example` artifact profile.
- Remove the old target checker assumption that current sample-service parents
  must equal the immutable predecessor manifest row; the successor manifest
  owns the current disposition.
- README heading IDs use exact profile names such as `## Overview`; Korean
  content remains beneath the heading.
- Shared Agent policy becomes one short link to Stage 00. Service-specific
  commands, constraints, validation, and troubleshooting stay in existing
  allowed local sections.
- `infra/04-data/README.md` becomes one folder index. Remove the obsolete
  prefixed operations guide and collapse the three identical Operations links
  to one.
- `secrets/README.md` adds only the tracked path identifier
  `secrets/db/surreal_db/`; no file payload is opened or echoed.

- [ ] Add RED metadata tests proving the exact sample fixture path selects the
  `service` role, `status: active` is rejected for that fixture, and its two
  domain parents are required.
- [ ] Add RED target-surface tests for all 11 exact `Overview` headings,
  absence of the duplicate data-guide preface/link triplet, and removal of the
  26 shared policy section headings.
- [ ] Add RED tests proving service-specific local constraints survive under
  allowed sections and that generic copied template sentences are absent.
- [ ] Add RED tests for the SurrealDB path-only inventory and a negative
  secret-value marker that must never appear in diagnostics.
- [ ] Add RED archive tests proving root content and Stage 98 SDLC profiles
  remain distinct and the existing Windows tombstone provenance remains valid.
- [ ] Record the expected focused failures before document edits.
- [ ] Normalize only confirmed headings and duplication; do not translate or
  rewrite unrelated topic content.
- [ ] Route shared policy to
  `docs/00.agent-governance/policies/agentic.md` and
  `docs/00.agent-governance/policies/documentation-protocol.md`.
- [ ] Register the typed sample fixture and update its current metadata and
  topic-specific sections.
- [ ] Update the manifest rows and regenerate the delta summary.
- [ ] Run:

```bash
python3 -m unittest \
  tests.validation.test_document_metadata \
  tests.validation.test_target_surface_contracts \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
python3 scripts/validation/check-target-surface-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/governance/validate-cross-links.sh
git diff --check
```

Expected GREEN: every affected README selects one profile and has exact
headings; no shared-policy duplicate remains; the sample fixture is typed but
not active; archive profiles remain distinct; secret checks expose names and
paths only; links and metadata pass.

- [ ] Record exact dispositions, preserve decisions, changed paths, and
  value-free evidence in the Task ledger.
- [ ] Obtain independent specification and quality/security reviews.
- [ ] Commit as
  `docs(governance): converge target documentation surfaces`.

### Task 3: T-TSDC-003 — Reconcile Static Version and Active Legacy Drift

**Files:**

- Modify generated-by-script `infra/tech-stack.versions.json`.
- Modify generated
  `docs/90.references/data/docker/ref-0061-tech-stack-version-provenance.md`.
- Modify `scripts/hardening/check-all-hardening.sh`.
- Create `tests/validation/test_tech_stack_version_contract.py`.
- Modify current target documentation containing the six stale values:
  `infra/01-gateway/README.md`,
  `infra/02-auth/keycloak/README.md`,
  `infra/06-observability/README.md`,
  `infra/06-observability/alloy/README.md`,
  `infra/06-observability/prometheus/README.md`,
  `infra/06-observability/pushgateway/README.md`,
  `infra/06-observability/pyroscope/README.md`,
  `infra/06-observability/tempo/README.md`, and
  `infra/08-ai/README.md`.
- Modify direct-impact operations documents:
  `docs/05.operations/catalog/06-observability/ops-0040-alloy/guide.md`,
  `docs/05.operations/catalog/06-observability/ops-0045-prometheus/guide.md`,
  `docs/05.operations/catalog/06-observability/ops-0040-alloy/policy.md`,
  `docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md`, and
  `docs/05.operations/catalog/06-observability/ops-0040-alloy/runbook.md`.
- Modify `scripts/validation/check-repo-contracts.sh` only where an exact stale
  version assertion exists; preserve historical prose and negative fixtures.
- Modify the Task 1 manifest/summary and sibling Task ledger.

**Version contract:**

| Component | Stale registry value | Compose-declared value |
| --- | --- | --- |
| Traefik | `v3.7.6` | `v3.7.8` |
| Keycloak | `26.6.4-1` | `26.7.0-0` |
| PostgreSQL | `17.6.1.143` | `17.6.1.150` |
| Prometheus | `v3.13.0` | `v3.13.1` |
| Alloy | `v1.17.1` | `v1.18.0` |
| Ollama | `0.31.1` | `0.32.1` |

`infra/tech-stack.versions.json` remains downstream of Compose declarations.
Use `sync-tech-stack-versions.sh` in write mode and the provenance generator;
do not hand-edit either generated output. Make the hardening assertion derive
the expected Keycloak image from the curated registry or a single checked
Compose source instead of adding another free-standing version owner.

- [ ] Add RED tests that load the curated registry, compare each entry with
  declared Compose images, and require direct-impact current docs to use the
  registry value.
- [ ] Add RED proving the hardening checker no longer embeds the stale
  Keycloak value as an independent constant.
- [ ] Add a classification test that preserves historical, incident,
  migration, archive, dashboard-label, and negative-fixture occurrences of
  `legacy`/`deprecated`, while failing only on a registered active obsolete
  implementation.
- [ ] Run the focused tests plus sync/hardening checks and record the expected
  six sync drifts and one Keycloak hardening failure.
- [ ] Run the canonical sync script in write mode; do not use a text-replace
  shortcut.
- [ ] Regenerate tech-stack provenance with its canonical generator.
- [ ] Update direct current documentation without changing Compose runtime
  declarations.
- [ ] Replace the duplicated hardening version literal with one canonical
  lookup and retain all security assertions.
- [ ] Classify every remaining target occurrence of `legacy` or `deprecated`;
  default to `preserve` unless all destructive gates are satisfied.
- [ ] Update manifest dispositions and regenerate the delta summary.
- [ ] Run:

```bash
python3 -m unittest tests.validation.test_tech_stack_version_contract -v
bash scripts/operations/sync-tech-stack-versions.sh --check
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
bash scripts/hardening/check-all-hardening.sh
python3 scripts/validation/check-supply-chain-policy.py --check
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

Expected GREEN: zero registry drift, fresh provenance, all 11 hardening tiers
pass, supply-chain fixtures remain 13 and green, direct current docs contain
only canonical values, no live service command ran, and no historical or
negative evidence was erased.

- [ ] Record generator commands, exact six replacements, preserve/delete
  classifications, secret boundary, and review results in the Task ledger.
- [ ] Obtain independent specification and quality/security reviews.
- [ ] Commit as
  `fix(infra): reconcile static version and lifecycle drift`.

### Task 4 Recovery: T-TSDC-004R — Cut Over to Typed CI Gates

The original Task 4 implementation remains blocked evidence. This recovery is
a new approved-design lineage under the same top-level Task ID, not a sixth
semantic-parser fix. It uses three implementation waves:

- **Wave A:** typed schema and dependency-free runner foundations;
- **Wave B:** atomic workflow and local-profile projection cutover;
- **Wave C:** old semantic interpreter removal after independent cutover
  approval.

#### Stable Public Interfaces

The following existing public names in
`scripts/validation/github_workflow_contract.py` remain import-compatible:

```text
WorkflowFinding
TriggerContract
ActionDependency
WorkflowDocument
WorkflowContractError
load_workflows(root: pathlib.Path) -> tuple[WorkflowDocument, ...]
load_workflow_contract(root: pathlib.Path) -> WorkflowContract
validate_workflows(root: pathlib.Path, contract: WorkflowContract) -> tuple[WorkflowFinding, ...]
main(argv: list[str] | None = None) -> int
```

The new `scripts/validation/ci_gate_contract.py` owns these exact typed
interfaces:

```python
class GateKind(enum.StrEnum):
    LEAF = "leaf"
    AGGREGATE = "aggregate"
    SETUP = "setup"


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class GateFinding:
    code: str
    path: str
    message: str


class GateContractError(ValueError):
    def __init__(self, code: str, path: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message


@dataclasses.dataclass(frozen=True, slots=True)
class GateNode:
    gate_id: str
    kind: GateKind
    suite_key: str | None
    entrypoint: pathlib.PurePosixPath | None
    argv: tuple[str, ...]
    cwd: pathlib.PurePosixPath | None
    allowed_env_keys: tuple[str, ...]
    timeout_minutes: int | None
    profiles: tuple[str, ...]
    opaque: bool
    children: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class JobRoot:
    workflow: str
    job_id: str
    root_gate_id: str
    classification: str


@dataclasses.dataclass(frozen=True, slots=True)
class ProfileRoot:
    profile: str
    root_gate_ids: tuple[str, ...]
    classification: str


@dataclasses.dataclass(frozen=True, slots=True)
class GateRegistry:
    nodes: tuple[GateNode, ...]
    job_roots: tuple[JobRoot, ...]
    profile_roots: tuple[ProfileRoot, ...]
```

The module exposes these exact functions:

```text
load_contract_document(root: pathlib.Path) -> dict[str, object]
parse_gate_registry(document: Mapping[str, object], path: str) -> GateRegistry
validate_gate_registry(root: pathlib.Path, registry: GateRegistry) -> tuple[GateFinding, ...]
expand_gate_ids(registry: GateRegistry, profile: str, gate_id: str | None, all_roots: bool) -> tuple[str, ...]
```

`load_contract_document` reads the one strict-JSON
`.github/workflow-contract.yml` through bounded descriptor-relative,
no-follow traversal and rejects duplicate JSON keys, non-UTF-8, oversized
input, noncanonical paths, and schema versions other than 2. JSON syntax is a
YAML 1.2 subset; no second registry file is created.

The new `scripts/validation/ci_gate_runner.py` owns:

```python
@dataclasses.dataclass(frozen=True, slots=True)
class GateInvocation:
    gate_id: str
    entrypoint: pathlib.PurePosixPath
    argv: tuple[str, ...]
    cwd: pathlib.PurePosixPath
    allowed_env_keys: tuple[str, ...]
    timeout_seconds: int


GateExecutor = collections.abc.Callable[[GateInvocation], int]
```

```text
build_execution_plan(registry: GateRegistry, profile: str, gate_id: str | None, all_roots: bool) -> tuple[GateInvocation, ...]
render_execution_plan(plan: tuple[GateInvocation, ...]) -> tuple[str, ...]
execute_execution_plan(root: pathlib.Path, plan: tuple[GateInvocation, ...], environ: Mapping[str, str], executor: GateExecutor | None = None) -> int
main(argv: list[str] | None = None) -> int
```

`scripts/validation/run-ci-gate.py` remains a thin executable wrapper around
`ci_gate_runner.main`. `scripts/validation/ci_gate_adapters.py` supplies only
the enumerated non-shell adapters needed to replace current inline workflow
logic:

```text
verify-metadata-base
publish-qa-recommendations
check-diff-hygiene
check-shell-syntax
install-python-requirements
run-unittest
run-agent-output-eval
run-npm
check-git-flow
prepare-compose-env
install-playwright
run-zizmor-sarif
```

The adapter does not accept an arbitrary command selector, shell source, or
gate ID. Every child process uses a literal argument vector with
`shell=False`. `run-zizmor-sarif` passes a no-follow output descriptor as
stdout instead of using shell redirection.

Adapter argument grammars are closed:

- `verify-metadata-base`, `publish-qa-recommendations`,
  `check-diff-hygiene`, `check-shell-syntax`, `run-agent-output-eval`,
  `check-git-flow`, `prepare-compose-env`, `install-playwright`, and
  `run-zizmor-sarif` accept no trailing arguments.
- `install-python-requirements` accepts exactly one repository-relative path:
  `scripts/requirements.txt` or
  `scripts/requirements-pre-commit.txt`.
- `run-unittest` accepts one or more module names matching
  `tests.validation.[A-Za-z0-9_.]+`, followed by the literal `-v`; options,
  paths, and module names outside that namespace are rejected.
- `run-npm` accepts exactly
  `audit --audit-level=high --prefix projects/storybook/nextjs`,
  `ci --prefix projects/storybook/nextjs`, or
  `run <script> --prefix projects/storybook/nextjs`, where `<script>` is one
  of `lint`, `typecheck`, `build`, `build-storybook`, or `coverage`.
- `install-playwright` owns the fixed child vector
  `npx --prefix projects/storybook/nextjs playwright install chromium
  --with-deps`.
- `run-zizmor-sarif` owns the fixed child vector
  `uvx --from zizmor==1.28.0 zizmor . --format sarif .` and the fixed
  repository-relative output `results.sarif`.
- `verify-metadata-base`, `publish-qa-recommendations`,
  `check-diff-hygiene`, `check-shell-syntax`, `run-agent-output-eval`,
  `check-git-flow`, and `prepare-compose-env` each replace one corresponding
  current workflow or local-runner body with a purpose-specific
  implementation. `check-shell-syntax` obtains only tracked
  `scripts/**/*.sh` and `.claude/hooks/*.sh` paths through NUL-delimited Git
  output before one literal `bash -n` call. None delegates to an arbitrary
  program.
- `prepare-compose-env` is CI-only. It copies the tracked regular
  `.env.example` to `.env` with descriptor-relative `O_NOFOLLOW | O_EXCL`
  creation and fails value-free when `.env` already exists; it never
  overwrites or reads an existing environment payload. No local profile
  reaches this setup node.

#### Canonical Root and Suite Mapping

The 16 required job IDs and their root IDs are exact:

| Required job ID | Root gate ID | Semantic suite keys |
| --- | --- | --- |
| `docs-traceability` | `ci.docs-traceability` | `docs-traceability` |
| `docs-implementation-alignment` | `ci.docs-implementation-alignment` | `docs-implementation-alignment`, `docs-qa-gate-recommendations` |
| `repo-contracts` | `ci.repo-contracts` | `repo-metadata-base`, `repo-document-metadata`, `ci-gate-contract-regressions`, `ci-gate-runner-regressions`, `ci-gate-adapter-regressions`, `workflow-contract-regressions`, `repo-contracts-control-plane-regressions`, `ci-precommit-regressions`, `workflow-contract`, `repo-contracts` |
| `agent-output-eval-fixture-gate` | `ci.agent-output-eval-fixture-gate` | `agent-output-eval-fixture-regressions`, `agent-output-eval-fixture-gate` |
| `supply-chain-fixture-policy` | `ci.supply-chain-fixture-policy` | `supply-chain-fixture-policy`, `supply-chain-deterministic-policy`, `supply-chain-summary-freshness` |
| `dependency-vulnerability-audit` | `ci.dependency-vulnerability-audit` | `dependency-vulnerability-audit` |
| `git-flow-contract` | `ci.git-flow-contract` | `git-flow-contract` |
| `compose-validation` | `ci.compose-validation` | `compose-validation` |
| `compose-all-profiles-validation` | `ci.compose-all-profiles-validation` | `compose-all-profiles-validation` |
| `infrastructure-hardening` | `ci.infrastructure-hardening` | `infrastructure-hardening` |
| `template-security-baseline` | `ci.template-security-baseline` | `template-security-baseline` |
| `quickwin-baseline` | `ci.quickwin-baseline` | `quickwin-baseline` |
| `pre-commit` | `ci.pre-commit` | `pre-commit` |
| `frontend-quality` | `ci.frontend-quality` | `frontend-lint`, `frontend-typecheck`, `frontend-build`, `frontend-quality` |
| `storybook-coverage` | `ci.storybook-coverage` | `storybook-coverage` |
| `zizmor` | `ci.zizmor` | `zizmor` |

Setup nodes have no `suite_key`. The exact setup IDs are
`setup.repo-python-dependencies`, `setup.precommit-python-dependencies`,
`setup.frontend-node-dependencies`, `setup.storybook-node-dependencies`,
`setup.storybook-playwright`, and `setup.compose-env`. Immutable
`actions/checkout`, `actions/setup-python`, `actions/setup-node`,
`astral-sh/setup-uv`, and `github/codeql-action/upload-sarif` steps remain
Action-registry consumers rather than gate nodes.

Every semantic leaf ID is exactly `leaf.<suite-key>`. The required roots have
these ordered children:

| Root gate ID | Ordered children |
| --- | --- |
| `ci.docs-traceability` | `leaf.docs-traceability` |
| `ci.docs-implementation-alignment` | `leaf.docs-implementation-alignment`, `leaf.docs-qa-gate-recommendations` |
| `ci.repo-contracts` | `leaf.repo-metadata-base`, `setup.repo-python-dependencies`, `leaf.repo-document-metadata`, `leaf.ci-gate-contract-regressions`, `leaf.ci-gate-runner-regressions`, `leaf.ci-gate-adapter-regressions`, `leaf.workflow-contract-regressions`, `leaf.repo-contracts-control-plane-regressions`, `leaf.ci-precommit-regressions`, `leaf.workflow-contract`, `leaf.repo-contracts` |
| `ci.agent-output-eval-fixture-gate` | `leaf.agent-output-eval-fixture-regressions`, `leaf.agent-output-eval-fixture-gate` |
| `ci.supply-chain-fixture-policy` | `leaf.supply-chain-fixture-policy`, `leaf.supply-chain-deterministic-policy`, `leaf.supply-chain-summary-freshness` |
| `ci.dependency-vulnerability-audit` | `leaf.dependency-vulnerability-audit` |
| `ci.git-flow-contract` | `leaf.git-flow-contract` |
| `ci.compose-validation` | `setup.compose-env`, `leaf.compose-validation` |
| `ci.compose-all-profiles-validation` | `setup.compose-env`, `leaf.compose-all-profiles-validation` |
| `ci.infrastructure-hardening` | `setup.compose-env`, `leaf.infrastructure-hardening` |
| `ci.template-security-baseline` | `setup.compose-env`, `leaf.template-security-baseline` |
| `ci.quickwin-baseline` | `setup.compose-env`, `leaf.quickwin-baseline` |
| `ci.pre-commit` | `setup.precommit-python-dependencies`, `leaf.pre-commit` |
| `ci.frontend-quality` | `setup.frontend-node-dependencies`, `leaf.frontend-lint`, `leaf.frontend-typecheck`, `leaf.frontend-build`, `leaf.frontend-quality` |
| `ci.storybook-coverage` | `setup.storybook-node-dependencies`, `setup.storybook-playwright`, `leaf.storybook-coverage` |
| `ci.zizmor` | `leaf.zizmor` |

The exact required-workflow runner targets are:

| Required job ID | Ordered static runner targets |
| --- | --- |
| `docs-traceability` | `ci.docs-traceability` |
| `docs-implementation-alignment` | `leaf.docs-implementation-alignment`, then the existing conditional `leaf.docs-qa-gate-recommendations` |
| `repo-contracts` | `ci.repo-contracts` |
| `agent-output-eval-fixture-gate` | `ci.agent-output-eval-fixture-gate` |
| `supply-chain-fixture-policy` | `ci.supply-chain-fixture-policy` |
| `dependency-vulnerability-audit` | `ci.dependency-vulnerability-audit` |
| `git-flow-contract` | `ci.git-flow-contract` |
| `compose-validation` | `ci.compose-validation` |
| `compose-all-profiles-validation` | `ci.compose-all-profiles-validation` |
| `infrastructure-hardening` | `ci.infrastructure-hardening` |
| `template-security-baseline` | `ci.template-security-baseline` |
| `quickwin-baseline` | `ci.quickwin-baseline` |
| `pre-commit` | `ci.pre-commit` |
| `frontend-quality` | `ci.frontend-quality` |
| `storybook-coverage` | `ci.storybook-coverage` |
| `zizmor` | `ci.zizmor` |

Every table cell denotes
`python3 scripts/validation/run-ci-gate.py --profile ci --gate <target>`.
The workflow validator expands the ordered target list and requires it to
equal the owning root expansion exactly once. The Storybook, frontend,
pre-commit, Compose, and repository setup chains therefore stay within one
runner lifetime rather than being flattened into separate processes.

Required leaf/setup execution fields are exact:

| Node ID | Entrypoint | Exact `argv` |
| --- | --- | --- |
| `leaf.docs-traceability` | `scripts/validation/check-doc-traceability.sh` | no arguments |
| `leaf.docs-implementation-alignment` | `scripts/validation/check-doc-implementation-alignment.sh` | no arguments |
| `leaf.docs-qa-gate-recommendations` | `scripts/validation/ci_gate_adapters.py` | `publish-qa-recommendations` |
| `leaf.repo-metadata-base` | `scripts/validation/ci_gate_adapters.py` | `verify-metadata-base` |
| `setup.repo-python-dependencies` | `scripts/validation/ci_gate_adapters.py` | `install-python-requirements`, `scripts/requirements.txt` |
| `leaf.repo-document-metadata` | `scripts/validation/check-document-metadata.py` | `--mode`, `check-changed` |
| `leaf.ci-gate-contract-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_ci_gate_contract`, `-v` |
| `leaf.ci-gate-runner-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_ci_gate_runner`, `-v` |
| `leaf.ci-gate-adapter-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_ci_gate_adapters`, `-v` |
| `leaf.workflow-contract-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_github_workflow_contract`, `-v` |
| `leaf.repo-contracts-control-plane-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_agent_governance_ci_routing`, `-v` |
| `leaf.ci-precommit-regressions` | `tests/validation/test_run_ci_precommit.sh` | no arguments |
| `leaf.workflow-contract` | `scripts/validation/check-github-workflow-contract.py` | no arguments |
| `leaf.repo-contracts` | `scripts/validation/check-repo-contracts.sh` | no arguments |
| `leaf.agent-output-eval-fixture-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_agent_output_eval_fixtures`, `-v` |
| `leaf.agent-output-eval-fixture-gate` | `scripts/validation/ci_gate_adapters.py` | `run-agent-output-eval` |
| `leaf.supply-chain-fixture-policy` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_compose_core_readiness`, `tests.validation.test_postgres_logical_upgrade_rehearsal`, `tests.validation.test_grype_db_seed`, `tests.validation.test_supply_chain_policy`, `tests.validation.test_sample_service_delivery_rehearsal`, `-v` |
| `leaf.supply-chain-deterministic-policy` | `scripts/validation/check-supply-chain-policy.py` | `--check` |
| `leaf.supply-chain-summary-freshness` | `scripts/security/generate-supply-chain-sample-service-summary.sh` | `--check` |
| `leaf.dependency-vulnerability-audit` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `audit`, `--audit-level=high`, `--prefix`, `projects/storybook/nextjs` |
| `leaf.git-flow-contract` | `scripts/validation/ci_gate_adapters.py` | `check-git-flow` |
| `setup.compose-env` | `scripts/validation/ci_gate_adapters.py` | `prepare-compose-env` |
| `leaf.compose-validation` | `scripts/validation/validate-docker-compose.sh` | no arguments |
| `leaf.compose-all-profiles-validation` | `scripts/validation/validate-docker-compose.sh` | no arguments |
| `leaf.infrastructure-hardening` | `scripts/hardening/check-all-hardening.sh` | no arguments |
| `leaf.template-security-baseline` | `scripts/validation/check-template-security-baseline.sh` | no arguments |
| `leaf.quickwin-baseline` | `scripts/validation/check-quickwin-baseline.sh` | no arguments |
| `setup.precommit-python-dependencies` | `scripts/validation/ci_gate_adapters.py` | `install-python-requirements`, `scripts/requirements-pre-commit.txt` |
| `leaf.pre-commit` | `scripts/validation/run-ci-precommit.sh` | no arguments |
| `setup.frontend-node-dependencies` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `ci`, `--prefix`, `projects/storybook/nextjs` |
| `leaf.frontend-lint` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `run`, `lint`, `--prefix`, `projects/storybook/nextjs` |
| `leaf.frontend-typecheck` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `run`, `typecheck`, `--prefix`, `projects/storybook/nextjs` |
| `leaf.frontend-build` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `run`, `build`, `--prefix`, `projects/storybook/nextjs` |
| `leaf.frontend-quality` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `run`, `build-storybook`, `--prefix`, `projects/storybook/nextjs` |
| `setup.storybook-node-dependencies` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `ci`, `--prefix`, `projects/storybook/nextjs` |
| `setup.storybook-playwright` | `scripts/validation/ci_gate_adapters.py` | `install-playwright` |
| `leaf.storybook-coverage` | `scripts/validation/ci_gate_adapters.py` | `run-npm`, `run`, `coverage`, `--prefix`, `projects/storybook/nextjs` |
| `leaf.zizmor` | `scripts/validation/ci_gate_adapters.py` | `run-zizmor-sarif` |

Every node above uses `cwd: "."`. Each required leaf/setup timeout equals its
owning job's preserved timeout: 5 minutes for documentation, agent-output,
git-flow, and supply-chain roots; 20 minutes for pre-commit, frontend, and
Storybook roots; and 10 minutes for all other required roots. Every semantic
leaf is `opaque: true`; every setup and aggregate is `opaque: false`. A shared
node's `profiles` field must equal its computed root reachability and cannot be
manually widened.

The local-only semantic leaves are exact:

| Gate ID | `suite_key` | Entrypoint | Exact `argv` |
| --- | --- | --- | --- |
| `leaf.local-diff-hygiene` | `local-diff-hygiene` | `scripts/validation/ci_gate_adapters.py` | `check-diff-hygiene` |
| `leaf.local-shell-syntax` | `local-shell-syntax` | `scripts/validation/ci_gate_adapters.py` | `check-shell-syntax` |
| `leaf.local-provider-surface-drift` | `local-provider-surface-drift` | `scripts/operations/sync-provider-surfaces.sh` | `--check` |
| `leaf.local-agent-governance-contract` | `local-agent-governance-contract` | `scripts/validation/check-agent-governance-contract.py` | `--mode`, `repository`, `--section`, `all` |
| `leaf.local-tech-stack-version-drift` | `local-tech-stack-version-drift` | `scripts/operations/sync-tech-stack-versions.sh` | `--check` |
| `leaf.local-document-corpus-lifecycle-tests` | `local-document-corpus-lifecycle-tests` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_document_corpus_lifecycle`, `-v` |
| `leaf.local-document-corpus-contract` | `local-document-corpus-contract` | `scripts/validation/check-document-corpus-lifecycle.py` | `--mode`, `check-contract` |
| `leaf.local-document-corpus-promoted` | `local-document-corpus-promoted` | `scripts/validation/check-document-corpus-lifecycle.py` | `--mode`, `check-promoted` |
| `leaf.local-target-surface-regressions` | `local-target-surface-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_target_surface_contracts`, `-v` |
| `leaf.local-target-surface-contract` | `local-target-surface-contract` | `scripts/validation/check-target-surface-contract.py` | no arguments |
| `leaf.local-target-delta-regressions` | `local-target-delta-regressions` | `scripts/validation/ci_gate_adapters.py` | `run-unittest`, `tests.validation.test_target_surface_delta_contracts`, `-v` |
| `leaf.local-target-delta-contract` | `local-target-delta-contract` | `scripts/validation/check-target-surface-delta-contract.py` | `--mode`, `advisory` |
| `leaf.local-security-readiness-freshness` | `local-security-readiness-freshness` | `scripts/validation/generate-security-automation-readiness.sh` | `--check` |
| `leaf.local-audit-matrix-freshness` | `local-audit-matrix-freshness` | `scripts/validation/generate-audit-implementation-matrix.sh` | `--check` |
| `leaf.local-llm-wiki-freshness` | `local-llm-wiki-freshness` | `scripts/knowledge/generate-llm-wiki.py` | `--check` |
| `leaf.local-script-manifest` | `local-script-manifest` | `scripts/validation/check-script-manifest.py` | none |

All local-only nodes use `cwd: "."`, `timeout_minutes: 10`, and
`opaque: true`. Their `profiles` fields must equal the exact profile-root
reachability below.

Local aggregate children are exact:

| Aggregate ID | Ordered children |
| --- | --- |
| `local.document-corpus-lifecycle` | `leaf.local-document-corpus-lifecycle-tests`, `leaf.local-document-corpus-contract`, `leaf.local-document-corpus-promoted` |
| `local.target-surface` | `leaf.local-target-surface-regressions`, `leaf.local-target-surface-contract`, `leaf.local-target-delta-regressions`, `leaf.local-target-delta-contract` |
| `local.workflow-harness` | `leaf.ci-gate-contract-regressions`, `leaf.ci-gate-runner-regressions`, `leaf.ci-gate-adapter-regressions`, `leaf.workflow-contract-regressions`, `leaf.repo-contracts-control-plane-regressions`, `leaf.ci-precommit-regressions`, `leaf.workflow-contract` |
| `local.supply-chain` | `leaf.supply-chain-deterministic-policy`, `leaf.supply-chain-summary-freshness` |
| `local.generated-freshness` | `leaf.local-security-readiness-freshness`, `leaf.local-audit-matrix-freshness`, `leaf.local-llm-wiki-index-freshness`, `leaf.local-llm-wiki-coverage-freshness` |
| `local.compose-validation` | `leaf.compose-validation` |
| `local.compose-all-profiles-validation` | `leaf.compose-all-profiles-validation` |
| `local.infrastructure-hardening` | `leaf.infrastructure-hardening` |
| `local.template-security-baseline` | `leaf.template-security-baseline` |
| `local.quickwin-baseline` | `leaf.quickwin-baseline` |

The `ci` profile derives from `job_roots`.
The exact `local-script-backed` root order is
`leaf.local-diff-hygiene`, `leaf.local-shell-syntax`,
`leaf.local-provider-surface-drift`,
`ci.agent-output-eval-fixture-gate`,
`leaf.local-agent-governance-contract`,
`leaf.local-tech-stack-version-drift`, `ci.docs-traceability`,
`leaf.docs-implementation-alignment`, `local.document-corpus-lifecycle`,
`local.target-surface`, `local.workflow-harness`, `local.supply-chain`,
`local.compose-validation`, `local.infrastructure-hardening`,
`local.template-security-baseline`, `local.quickwin-baseline`,
`local.generated-freshness`, and `leaf.repo-contracts`.

The exact `local-harness` root order is the same sequence without
`leaf.local-tech-stack-version-drift` and `local.quickwin-baseline`.
The exact `local-all-profiles` root order is the complete
`local-script-backed` sequence followed by
`local.compose-all-profiles-validation`. All three local profiles exclude real
pre-commit, dependency audit, frontend
dependency/build/coverage, Playwright installation, zizmor execution/upload,
and every CI-only or networked setup node. Contract and routing tests require
all three local profiles to exclude `setup.compose-env`, and an existing ignored
`.env` fixture must remain byte-identical after every local wrapper mode. The
existing `--all-profiles` local-runner mode remains a compatibility route: it
executes the registered `local-all-profiles` profile once. Normal and
all-profile Compose are distinct suite identities, so that profile
intentionally reaches each distinct leaf once without duplicate ownership.
The wrapper sets
`HYHOME_COMPOSE_PROFILES` to an already supplied nonempty value or to the exact
default `core data obs workflow ai tooling messaging security communication
service storage admin iac registry sast sync testing graph mng ksql nginx`; it
does not inherit `HYHOME_ALL_COMPOSE_PROFILES`.
`--script-backed`, `--harness`, and `--all-profiles` each select one registered
profile and contain no literal child-command list.

Gate-specific environment admission is exact:

| Gate purpose | Admitted keys |
| --- | --- |
| QA recommendation summary | `EVENT_NAME`, `PR_BASE_SHA`, `PUSH_BEFORE_SHA`, `GITHUB_STEP_SUMMARY` |
| Repository metadata base/check | `TEMPLATE_GATE_BASE` |
| Git-flow validation | `PR_TITLE`, `HEAD_REF` |
| All-profile Compose validation | `HYHOME_COMPOSE_PROFILES` |
| CI pre-commit leaf | `CI`, `GITHUB_ACTIONS`, `SKIP` |
| All other gates | no gate-specific inherited keys |

The runner constructs the child environment from an empty mapping. Its fixed
baseline is `PATH` copied from the controller environment,
`LANG=C.UTF-8`, `LC_ALL=C.UTF-8`, `HOME` set to a fresh
`/tmp/ci-gate-home-*` directory, `TMPDIR=/tmp`,
`PYTHONNOUSERSITE=1`, `PYTHONSAFEPATH=1`,
`PIP_DISABLE_PIP_VERSION_CHECK=1`, and a runner-created
`HYHOME_CI_GATE_ROOT` bound to the already verified repository-root
descriptor; a missing or empty controller `PATH` fails closed. For Python
entrypoints only, the runner constructs a fixed `PYTHONPATH` from that root
and `scripts/validation`; it never inherits a controller `PYTHONPATH`.
Before gate-specific admission it drops every ambient `GIT_*` key and never
inherits `NODE_OPTIONS`, `BASH_ENV`, `ENV`, `CDPATH`, `IFS`, `SHELLOPTS`, or
`GLOBIGNORE`. A
purpose-specific Git subprocess may construct
`GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` for that subprocess
only; those values are not inherited from the controller. Secret-, token-,
password-, credential-, and auth-shaped environment keys are rejected by the
registry validator. Values are never included in diagnostics.
The fresh HOME is removed in a `finally` path after the complete execution
plan, including timeout, child failure, and executor exception paths.

Entrypoints remain inode-bound: the runner opens the tracked regular
executable with descriptor-relative no-follow traversal, verifies its Git mode
and identity, and executes `/proc/self/fd/<fd>` with `pass_fds` and
`shell=False`. Because that kernel path intentionally changes
`BASH_SOURCE[0]`, Python `__file__`, and sibling-module discovery, Wave B must
migrate every affected registered entrypoint to consume the runner-created
`HYHOME_CI_GATE_ROOT` while preserving its existing direct-execution fallback.
The exact compatibility set is
`scripts/hardening/check-all-hardening.sh`,
`scripts/operations/sync-provider-surfaces.sh`,
`scripts/operations/sync-tech-stack-versions.sh`,
`scripts/validation/check-agent-governance-contract.py`,
`scripts/validation/check-document-corpus-lifecycle.py`,
`scripts/validation/check-document-metadata.py`, and
`scripts/validation/check-supply-chain-policy.py`. The focused workflow wrapper
also imports its sibling module through the fixed runner-created Python path.
Descriptor-mode smoke tests must prove repository-root and sibling-import
parity for this exact set before workflow cutover.

#### Task 4.0 / T-TSDC-004R-0: Revised Plan Approval Gate

**Files:**

- Modify this Plan in place.
- Append only the new Spec/Plan approval facts to the sibling Task ledger.

- [x] Record the first independent read-only Plan reviews of
  `a0f91bb5..1a86f929` as `C0/I4/M1` specification and `C1/I2/M1`
  quality/security; neither verdict authorizes implementation.
- [x] Record the second independent reviews of
  `a0f91bb5..e97b7966` as `C0/I3/M1` specification and `C0/I2/M1`
  quality/security. The two-attempt Plan review loop is exhausted and returns
  to design/plan.
- [x] Record the user's 2026-07-29 explicit approval of this exact Plan
  Revision R1.
- [x] Record that approval in the Task ledger without changing old work-log
  rows or treating it as controlled-wrapper, remote, runtime, or secret
  authority.
- [x] Record the user's 2026-07-29 explicit approval of this Revision R2.
- [x] After that approval, assign fresh independent specification and
  quality/security Plan reviewers to the complete R2 range.
- [x] Record the first R2 review attempt over
  `e97b7966..5b7388d0`: specification `C0/I5/M0`,
  `SPEC_COMPLIANCE NO`, `COMMIT_READY NO`; quality/security `C0/I0/M0`,
  `APPROVED`, `COMMIT_READY YES`. A separate specification corroboration
  returned `C0/I4/M0`; no verdict authorizes implementation.
- [x] Correct the union of the first-attempt findings without changing the
  approved external-authority boundary.
- [x] Assign one final fresh specification reviewer plus one different
  quality/security reviewer to the complete corrected R2 range.
- [x] Require both final R2 reviews to map TSDC-010 through TSDC-017, verify
  exact file ownership and commands, and return C0/I0 before implementation.

Expected gate: only after Revision R2 approval and both final corrected R2
reviews return C0/I0 does the Task ledger change from
`blocked pending corrected Revision R2 Plan reviews` to `active recovery`; no
production or test file changes before that transition.

Gate satisfied: the final specification and quality/security reviews of
`e97b7966..8f82e88b` each returned `C0/I0/M0` and `COMMIT_READY YES`.

#### Task 4.1 / Wave A / T-TSDC-004R-1: Typed Gate Contract

**Files:**

- Create `scripts/validation/ci_gate_contract.py`.
- Create `tests/validation/test_ci_gate_contract.py`.
- Modify
  `docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml`
  with exact new-path rows.
- Regenerate
  `docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md`.
- Modify `tests/validation/test_target_surface_delta_contracts.py` for exact
  path count, ownership, consumer, and pending-review assertions.
- Append actual RED/GREEN/review evidence to the Task ledger.

**Interfaces:**

- Consumes: the dataclasses and functions declared in Stable Public
  Interfaces.
- Produces: dependency-free schema parsing, kind validation, DAG expansion,
  suite ownership, job-root ownership, and local-profile projection for R2.
  Tasks 4.1 and 4.2 jointly form Spec Wave 1; Wave B cannot start until Task
  4.2 has converted and reviewed the canonical schema-v2 registry.

- [ ] **Step 1: Create an importable signature-only skeleton, then write
  schema-v2 RED tests.**

  Create only the declared dataclasses and function signatures, with every
  behavior raising `NotImplementedError`; the skeleton is not a usable
  validator. Add exact tests named:
  `test_schema_v2_contract_is_strict_json_and_duplicate_safe`,
  `test_gate_kind_fields_are_exact`,
  `test_gate_graph_rejects_cycles_missing_children_and_orphans`,
  `test_suite_keys_and_required_owners_are_unique`,
  `test_required_job_roots_are_the_exact_sixteen`,
  `test_profile_roots_are_ordered_and_cannot_override_nodes`, and
  `test_contract_reader_rejects_symlink_noncanonical_and_oversized_inputs`.

```python
def test_gate_graph_rejects_cycles_missing_children_and_orphans(self) -> None:
    for mutation, expected_code in (
        ("cycle", "ci-gate-cycle"),
        ("missing-child", "ci-gate-child-missing"),
        ("orphan", "ci-gate-orphan"),
    ):
        findings = self.validate_fixture(mutation)
        self.assertEqual({finding.code for finding in findings}, {expected_code})
```

- [ ] **Step 2: Run the RED suite.**

```bash
python3 -m unittest tests.validation.test_ci_gate_contract -v
```

Expected RED: the signature-only module imports, but each named contract test
fails on its own expected behavior or finding-code assertion. Missing-import
evidence alone is insufficient, and the behavior-specific failures are
recorded in the Task ledger.

- [ ] **Step 3: Implement the strict contract and graph validator.**

  Implement the declared dataclasses and functions. Aggregate nodes admit only
  ordered children. Leaf/setup nodes require tracked canonical first-party
  entrypoint fields, exact argv, cwd, timeout, profiles, and allowed
  environment keys. Each semantic `suite_key` belongs to one leaf; each
  required suite reaches one required root and at most one workflow path.
  Unknown fields fail rather than being ignored.

- [ ] **Step 4: Add exact manifest rows under a failing oracle and regenerate
  the summary through its canonical writer.**

  Edit the manifest only after the exact-row test fails; the manifest has no
  post-bootstrap row writer. The
  `scripts/validation/ci_gate_contract.py` row uses disposition `update`,
  canonical owner `scripts/validation/ci_gate_contract.py`, and direct consumer
  `tests/validation/test_ci_gate_contract.py`. The
  `tests/validation/test_ci_gate_contract.py` row uses disposition `update`,
  canonical owner `tests/validation/test_ci_gate_contract.py`, and no direct
  consumer in this unit. Both rows name the focused validator/test evidence and
  retain pending review verdicts. The exact oracle becomes 150 rows: 89
  `preserve`, 61 `update`, zero `migrate`, and zero `delete`. Regenerate only
  the derived summary with:

```bash
git add \
  scripts/validation/ci_gate_contract.py \
  tests/validation/test_ci_gate_contract.py
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory \
  --write-summary
```

  The scoped pre-validation staging makes the two new files visible to the
  tracked-path and canonical-owner checks; the commit step refreshes the same
  paths after all later edits.

- [ ] **Step 5: Run GREEN and static checks.**

```bash
python3 -m unittest tests.validation.test_ci_gate_contract -v
python3 -m unittest \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 -m ruff check \
  scripts/validation/ci_gate_contract.py \
  tests/validation/test_ci_gate_contract.py
python3 -m compileall -q \
  scripts/validation/ci_gate_contract.py \
  tests/validation/test_ci_gate_contract.py
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
git diff --check
```

Expected GREEN: every schema/DAG mutation has one value-free finding; the
canonical schema-v1 file remains the temporary current workflow authority
inside unfinished Spec Wave 1, and no workflow execution changes. Task 4.2
must convert the canonical registry to schema v2 before Wave B.

- [ ] **Step 6: Commit and review.**

```bash
git add \
  scripts/validation/ci_gate_contract.py \
  tests/validation/test_ci_gate_contract.py \
  tests/validation/test_target_surface_delta_contracts.py \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "feat(ci): add typed gate contract"
```

Assign fresh specification and quality/security reviewers. Use only the
canonical two-attempt implementation and review loops.

- [ ] **Step 7: Commit the independent review evidence before Task 4.2.**

  After both reviewers return C0/I0, append their exact range and verdicts to
  the Task ledger and commit the controller-owned evidence:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): record typed gate contract review"
```

  Task 4.2 starts only from this clean committed evidence boundary.

#### Task 4.2 / Wave A / T-TSDC-004R-2: Dependency-Free Runner and Adapters

**Files:**

- Create `scripts/validation/ci_gate_runner.py`.
- Create executable `scripts/validation/run-ci-gate.py`.
- Create executable `scripts/validation/ci_gate_adapters.py`.
- Create `tests/validation/test_ci_gate_runner.py`.
- Create `tests/validation/test_ci_gate_adapters.py`.
- Convert `.github/workflow-contract.yml` to deterministic strict-JSON schema
  version 2 after all registered new entrypoints exist.
- Modify `scripts/validation/github_workflow_contract.py` and
  `tests/validation/test_github_workflow_contract.py` for schema-v2 loading
  with a commit-bounded unchanged-current-workflow transition.
- Change only Git mode, from `100644` to `100755`, for these seven registered
  shebang entrypoints before schema-v2 conversion:
  `scripts/validation/check-agent-governance-contract.py`,
  `scripts/validation/check-doc-implementation-alignment.sh`,
  `scripts/validation/check-document-metadata.py`,
  `scripts/validation/check-document-corpus-lifecycle.py`,
  `scripts/validation/check-supply-chain-policy.py`,
  `scripts/security/generate-supply-chain-sample-service-summary.sh`, and
  `scripts/validation/check-target-surface-delta-contract.py`.
- Modify `scripts/README.md`.
- Modify the delta manifest, generated summary, exact manifest tests, and Task
  ledger for five new runner/test paths, the new
  `check-agent-governance-contract.py` row, and the six existing
  mode-normalized rows.
- Preserve `.pre-commit-config.yaml`; its existing repository-contract selector
  includes the exact `scripts/.*`, `tests/.*`, and `.github/.*` alternatives,
  so it already covers every new path.

**Interfaces:**

- Consumes: `GateRegistry`, `GateNode`, and `expand_gate_ids` from R1.
- Produces: the exact CLI and execution interfaces declared above for the
  atomic workflow cutover in R3 and completes Spec Wave 1 by introducing the
  one canonical schema-v2 registry while retaining current workflow execution.

- [ ] **Step 1: Create importable signature-only skeletons, then write runner
  and adapter RED tests.**

  Create only the declared symbols and closed subcommand names, with execution
  behavior raising `NotImplementedError`; do not add a working runner or
  adapter. Add exact runner tests for mutually exclusive `--gate`/`--all`, unknown
  profile/gate, deterministic `--list`, value-free `--dry-run`, ordered
  deduplication, timeout propagation, nonzero child propagation, minimal
  environment, all ambient `GIT_*` removal, one HOME shared by every node in
  one complete execution plan, cleanup after every exit path, and
  fake-executor one-time output.
  Add filesystem tests for symlink parent/leaf, untracked entrypoint, Git mode
  other than `100755`, unsupported shebang, non-regular file, cwd escape, and
  path replacement after descriptor open. Add descriptor-mode fixtures proving
  that `HYHOME_CI_GATE_ROOT` and the fixed Python import path preserve logical
  repository-root and sibling-module discovery without inherited
  `PYTHONPATH`.

```python
def test_fake_executor_receives_each_leaf_once_in_order(self) -> None:
    seen: list[str] = []
    result = execute_execution_plan(
        self.root,
        self.plan,
        environ={"PATH": "/usr/bin", "GIT_DIR": "/tmp/hostile"},
        executor=lambda invocation: seen.append(invocation.gate_id) or 0,
    )
    self.assertEqual(result, 0)
    self.assertEqual(seen, ["setup.repo-python-dependencies", "leaf.repo-contracts"])
```

  Add one adapter test per enumerated subcommand plus rejection tests for
  unknown subcommands, shell metacharacter command selectors, out-of-repository
  requirements paths, unapproved npm verbs, secret-shaped environment names,
  and SARIF symlink output. The `prepare-compose-env` tests must prove
  exclusive creation from a tracked regular `.env.example`, value-free failure
  when `.env` already exists, and byte-identical preservation of that existing
  file.

- [ ] **Step 2: Run RED.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  -v
```

Expected RED: after the signature-only skeletons import successfully, each
runner and adapter behavior group fails on its own expected result or
finding-code assertion. Missing-import evidence alone does not satisfy RED.

- [ ] **Step 3: Implement descriptor-bound execution.**

  Walk cwd and entrypoint components with `openat`-style
  `O_NOFOLLOW` descriptor traversal, require a tracked regular Git mode
  `100755` file and admitted Bash/Python shebang, and execute the verified file
  descriptor through `/proc/self/fd/<fd>` with `pass_fds`, `shell=False`, and
  the registered timeout. Use the verified directory descriptor for cwd.
  Fail closed when `/proc/self/fd` is unavailable.

- [ ] **Step 4: Implement deterministic CLI modes and adapters.**

  `--list` and `--dry-run` print gate IDs and repository-relative entrypoints
  only. They do not print environment values or execute child programs.
  Adapter subprocesses always use argument arrays and `shell=False`. Until
  Step 6 converts the canonical registry, CLI behavior tests use only bounded
  temporary strict-schema-v2 repositories; no live command targets the
  canonical schema-v1 file.

- [ ] **Step 5: Normalize every registered entrypoint mode, add exact manifest
  rows, and update the scripts index before schema conversion.**

```bash
chmod 0755 \
  scripts/validation/run-ci-gate.py \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/check-agent-governance-contract.py \
  scripts/validation/check-doc-implementation-alignment.sh \
  scripts/validation/check-document-metadata.py \
  scripts/validation/check-document-corpus-lifecycle.py \
  scripts/validation/check-supply-chain-policy.py \
  scripts/security/generate-supply-chain-sample-service-summary.sh \
  scripts/validation/check-target-surface-delta-contract.py
git add \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/run-ci-gate.py \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/check-agent-governance-contract.py \
  scripts/validation/check-doc-implementation-alignment.sh \
  scripts/validation/check-document-metadata.py \
  scripts/validation/check-document-corpus-lifecycle.py \
  scripts/validation/check-supply-chain-policy.py \
  scripts/security/generate-supply-chain-sample-service-summary.sh \
  scripts/validation/check-target-surface-delta-contract.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
git diff --cached --summary -- \
  scripts/validation/check-agent-governance-contract.py \
  scripts/validation/check-doc-implementation-alignment.sh \
  scripts/validation/check-document-metadata.py \
  scripts/validation/check-document-corpus-lifecycle.py \
  scripts/validation/check-supply-chain-policy.py \
  scripts/security/generate-supply-chain-sample-service-summary.sh \
  scripts/validation/check-target-surface-delta-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory \
  --write-summary
```

  The scoped summary must report exactly seven
  `mode change 100644 => 100755` entries and no content change for those
  paths. Edit manifest rows only after the exact-row test fails. Each new
  row's `canonical_owner` is its own path. Initial direct consumers are:
  `ci_gate_runner.py` by `run-ci-gate.py` and its focused test,
  `run-ci-gate.py` by its focused test, `ci_gate_adapters.py` by its focused
  test, and no direct consumers yet for either focused test file. Wave B
  updates those consumer edges only when the workflow and local profile
  projections become tracked consumers. Add
  `scripts/validation/check-agent-governance-contract.py` as an `update` row;
  change the four mode-normalized `preserve` rows to `update`; retain the two
  already-`update` rows. The exact oracle becomes 156 rows: 85 `preserve`, 71
  `update`, zero `migrate`, and zero `delete`.

- [ ] **Step 6: Complete Spec Wave 1 with the canonical schema-v2 registry.**

  After the runner and every registered new entrypoint are tracked and
  executable, serialize all seven workflow records, 23 job records, eight
  Action identities, 16 required IDs, `gate_nodes`, `job_roots`, and the three
  exact local `profile_roots` as deterministic strict JSON in the existing
  `.github/workflow-contract.yml`. Remove schema-v1 `owner_commands` and
  `expensive_commands`, and remove `ExpensiveCommandOwner` plus
  `_EXPENSIVE_COMMAND_BASELINE` in the same conversion.

  `github_workflow_contract.py` imports the typed parser and preserves its
  stable public interfaces. From this point the schema-v2 registry is the sole
  ownership authority: active validation no longer calls the old semantic
  ownership interpreter and no code-owned command table remains. The unused
  parser implementation may remain as dead cutover code only until Wave C.
  Task 4.2 must leave `.github/workflows/ci-quality.yml` byte-identical to the
  committed Task 4.1 review-evidence checkpoint and prove that boundary with
  an exact Git diff plus independent review; it makes no transitional semantic
  ownership claim for the unchanged free-form workflow. Add exact tests
  proving schema v1 now fails closed, the duplicate command authority is
  absent, and all registered entrypoints exist with required tracked modes.

  Update the existing `.github/workflow-contract.yml`,
  `scripts/validation/github_workflow_contract.py`, and
  `tests/validation/test_github_workflow_contract.py` manifest rows with
  factual schema-v2/transitional-consumer evidence while retaining their
  pending verdicts and dispositions.

- [ ] **Step 7: Run GREEN, live execution-free projections, and security
  regressions.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-harness --list
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness \
  --dry-run \
  --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles \
  --dry-run \
  --all
python3 -m ruff check \
  scripts/validation/ci_gate_contract.py \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/run-ci-gate.py \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/github_workflow_contract.py \
  tests/validation/test_ci_gate_contract.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_github_workflow_contract.py
python3 -m compileall -q \
  scripts/validation/ci_gate_contract.py \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/run-ci-gate.py \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/github_workflow_contract.py \
  scripts/validation/check-agent-governance-contract.py \
  scripts/validation/check-document-metadata.py \
  scripts/validation/check-document-corpus-lifecycle.py \
  scripts/validation/check-supply-chain-policy.py \
  scripts/validation/check-target-surface-delta-contract.py \
  tests/validation/test_github_workflow_contract.py
bash -n \
  scripts/validation/check-doc-implementation-alignment.sh \
  scripts/security/generate-supply-chain-sample-service-summary.sh
shellcheck --severity=warning \
  scripts/validation/check-doc-implementation-alignment.sh \
  scripts/security/generate-supply-chain-sample-service-summary.sh
TASK_4_1_REVIEW_COMMIT="$(
  git log -1 \
    --format=%H \
    --grep='^docs(task): record typed gate contract review$'
)"
test -n "$TASK_4_1_REVIEW_COMMIT"
git diff --exit-code "$TASK_4_1_REVIEW_COMMIT" -- \
  .github/workflows/ci-quality.yml
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
git diff --check
```

Expected GREEN: the fake executor observes one ordered execution per gate ID;
path, provenance, environment, timeout, and output tests fail closed without
running real CI suites or network operations; the canonical registry is strict
schema v2 and the current workflow remains byte-identical to the committed
Task 4.1 review boundary. No active semantic interpreter or parallel command
table remains.

- [ ] **Step 8: Commit and review.**

```bash
git add \
  .github/workflow-contract.yml \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/run-ci-gate.py \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/github_workflow_contract.py \
  scripts/validation/check-agent-governance-contract.py \
  scripts/validation/check-doc-implementation-alignment.sh \
  scripts/validation/check-document-metadata.py \
  scripts/validation/check-document-corpus-lifecycle.py \
  scripts/validation/check-supply-chain-policy.py \
  scripts/security/generate-supply-chain-sample-service-summary.sh \
  scripts/validation/check-target-surface-delta-contract.py \
  scripts/README.md \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_github_workflow_contract.py \
  tests/validation/test_target_surface_delta_contracts.py \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "feat(ci): add typed gate runner"
```

Assign fresh specification and quality/security reviewers before Wave B.

- [ ] **Step 9: Commit the independent review evidence before Wave B.**

  After both Task 4.2 reviewers return C0/I0, append the exact range and
  verdicts to the Task ledger and commit:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): record typed gate runner review"
```

  Wave B starts only from this clean committed evidence boundary.

##### Task 4.2S / Wave A design return: capability cleanup and pidfd identity finalization

**Status:** The sole redesigned lifecycle implementation at `8df1b9cd` was
reviewed over the exact range `e6fefb69..8df1b9cd`. The fresh specification
review returned `C0/I1/M0`, `SPEC_COMPLIANCE NO`, `COMMIT_READY NO`; the fresh
quality/security review returned `C0/I3/M0`, `CHANGES_REQUIRED`,
`COMMIT_READY NO`. These reviews supersede the prior “review pending” state.
They do not reopen schema-v2, workflow projection, or the historical
`17bb5cdd` remediation. Wave B remains blocked and all manifest verdicts
remain `pending`.

**Exact implementation allowlist:** after the uniquely named controller design
checkpoint is committed, the sole successor implementation paths are
`scripts/validation/ci_gate_runner.py`, `scripts/validation/ci_gate_adapters.py`,
`tests/validation/test_ci_gate_runner.py`,
`tests/validation/test_ci_gate_adapters.py`, and this Task ledger. Extend
existing test methods; do not add tests or alter contracts, manifests, summary,
workflow, profiles, or schema topology. `.github/workflow-contract.yml` and
`.github/workflows/ci-quality.yml` must be byte-identical to `17bb5cdd`; the
manifest and generated summary must remain unmodified. All other runtime,
Compose, remote, dependency, secret, wrapper, direct-`pre-commit`, and Wave
B/C work remains excluded.

- [ ] **Step S1: Write behavior-specific RED tests before implementation.**

  The test design must establish all of the following without running a real
  CI suite or network operation:

  1. Adapter ownership begins immediately after `_adopt_root` duplicates
     inherited capability `N` as owned CLOEXEC capability `M`, before it tries
     to close `N`. Every later operation, including `dict(environ)`, occurs
     inside one top-level cleanup controller governing `M`. If closing `N`
     fails, the controller still attempts to close `M`. For Compose, cleanup
     order is destination close, source close, conditional unlink of the
     created `.env`, then the top-level `M` close. For SARIF, cleanup order is
     output close, conditional unlink of the created `results.sarif`, then the
     top-level `M` close. A created artifact must be unlinked when the
     operation, either owned-descriptor close, or output close fails. Every
     applicable cleanup action is attempted independently even after an
     earlier action fails.

     The controller preserves the first typed product/operation error while
     cleanup proceeds. If every cleanup action succeeds, it returns that
     original error or product result. If any cleanup action fails, the first
     cleanup domain in the fixed order takes precedence because a safe state
     was not established; later cleanup failures are still attempted and
     collapse into that deterministic result. Root-capability, Compose, and
     SARIF cleanup failures use the fixed value-free codes
     `ci-gate-adapter-root-cleanup`,
     `ci-gate-adapter-compose-cleanup`, and
     `ci-gate-adapter-sarif-cleanup`, respectively. No `OSError` value, path,
     descriptor number, or environment value crosses the adapter boundary.
     Existing test methods add success, operation-error, simultaneous
     operation/close/unlink-error, and deterministic-priority witnesses
     without changing top-level test discovery.
  2. The runner opens a pidfd for the adapter leader immediately after
     `Popen`. It never calls `process.wait`, `poll`, `communicate`, or another
     reaping primitive before descendant cleanup. It waits for normal exit or
     timeout only by bounded pidfd `poll`/`select`, retaining an exited leader
     unreaped so its PID and PGID cannot be reused. It sends `TERM` to that
     still-reserved PGID, then—only after the leader pidfd is ready—uses a
     bounded `/proc` scan to enumerate same-PGID members excluding the pinned
     leader. If members remain, or the leader is not ready by grace expiry, it
     sends `KILL` to the PGID; it then requires leader readiness and zero
     remaining same-PGID members except the pinned leader before one and only
     one timeout-bounded `process.wait` reaps the leader and the pidfd closes.
     The wait is invoked only after pidfd readiness and can never be
     unbounded. Return a normal or nonzero product code, or timeout `124`, only
     after this cleanup succeeds. Any pidfd, proc-scan, non-`ESRCH` signal,
     readiness, reap-attempt timeout, reap, or close failure is typed and
     value-free. `TERM` or `KILL` returning `ESRCH` is the normal
     disappeared-target race between observation and signaling; it is not a
     cleanup failure and the runner must continue bounded leader-readiness and
     same-PGID-member validation.

     If initial `pidfd_open` fails, the still-unreaped leader reserves the
     identity while the runner records the fixed
     `ci-gate-runner-pidfd-acquisition` error, attempts group `KILL`, and then
     makes exactly one `process.wait(timeout=grace)` reap attempt even when
     `KILL` fails. `ESRCH` is safe in that recovery path. `TimeoutExpired`, a
     non-`ESRCH` signal failure, or a reap failure takes precedence as fixed
     value-free `ci-gate-runner-cleanup`; otherwise the recorded acquisition
     error is returned. This acquisition-failure path has no pidfd to close
     and never performs an unbounded wait.

     Any later scan or cleanup failure records its first typed error, then
     independently attempts group `KILL`, bounded leader readiness when the
     pidfd remains usable, a single bounded reap only if readiness was
     confirmed, and pidfd close. If readiness is unavailable or not reached,
     the runner records cleanup failure, skips `process.wait` rather than
     risking an unbounded wait, and still attempts pidfd close. If readiness
     was confirmed, `process.wait(timeout=grace)` is called exactly once; its
     timeout or failure does not prevent pidfd close. Every recovery action is
     attempted in that order, and any recovery-action failure collapses to
     `ci-gate-runner-cleanup` and takes precedence over the recorded scan,
     product, nonzero, or timeout result. The runner never observes or signals
     the numeric PGID after the sole successful reap or bounded reap attempt.
     Adapters create no session or process group.
  3. `/proc/<pid>/stat` scanning is strict, no-follow, disappearance-safe, and
     bounded to at most `65,536` strictly decimal PID entries and `4,096` bytes
     per `stat` file. Expected non-numeric procfs metadata entries are ignored;
     a transient vanished numeric process is absent. Permission, malformed
     numeric-entry content, numeric-entry symlink, entry-count overflow,
     byte overflow, read, or directory failure is fail-closed. Tests must not
     use a post-reap `killpg(..., 0)` absence probe as identity evidence.
     Instead, an ordered call trace proves that every numeric-PGID observation
     and signal precedes any bounded `process.wait` attempt; the harness is
     configured to fail if either is invoked after that attempt. Tests prove
     no wait/poll/communicate/reap before final signals and member-empty
     confirmation, safe normal and nonzero, timeout, output-overflow,
     read-error, child/grandchild cleanup, pidfd/reap/close failures, initial
     pidfd-acquisition plus non-`ESRCH` KILL failure with a bounded wait
     timeout, later readiness failure that skips wait but still closes pidfd,
     ready-then-wait-timeout that still closes pidfd, TERM and KILL `ESRCH`
     races, malformed/oversize/permission/disappearance numeric proc entries,
     expected non-numeric entry tolerance, and a simulated PGID-reuse target
     that cannot be observed or signaled after a reap attempt.
  4. Preserve exact HOME teardown behavior: at most three `rmtree` attempts,
     with exactly 50 ms sleeps after failures one and two. Preserve minimal
     environment, immutable-key denial, bounded two-stream output, SARIF
     cleanup/retry, Compose staged-blob identity, and registered product
     timeouts. No test performs a real CI, network, Compose, or external
     dependency action.

  RED command and accounting:

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_target_surface_delta_contracts \
  -v
```

  Expected RED: each new adopted-cleanup, pidfd-identity, bounded-proc, or
  output/source-cleanup witness fails on its named assertion, not by import
  failure.
  GREEN remains exactly `94` discovered tests: `83` pass and `11` documented
  Wave-C skips. No count change is authorized.

- [ ] **Step S2: Implement only the identity-safe cleanup boundaries.**

  Implement only the S1 ownership, deterministic cleanup-priority, pidfd,
  `ESRCH`, and bounded-proc design. Do not introduce nested sessions, broad
  descriptor inheritance, raw-PID liveness checks, pathname fallback, numeric
  group observation or signaling after reaping, or a second cleanup authority.
  Every applicable cleanup action runs even after a prior failure; cleanup
  failure takes precedence over product/operation outcome and is normalized to
  the fixed domain code defined in S1.

- [ ] **Step S3: Run GREEN and invariant gates.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-harness --list
python3 scripts/validation/run-ci-gate.py --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py --profile local-all-profiles --dry-run --all
python3 -m ruff check \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
python3 -m compileall -q \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
git diff --exit-code 17bb5cdd -- .github/workflow-contract.yml .github/workflows/ci-quality.yml
git diff --exit-code 17bb5cdd -- docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
TASK_4_2S_DESIGN_SUBJECT='docs(plan): record executable typed gate identity checkpoint'
TASK_4_2S_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2S_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2S_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2S_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
test "$(git show -s --format=%s "$TASK_4_2S_DESIGN_COMMIT")" = "$TASK_4_2S_DESIGN_SUBJECT"
TASK_4_2S_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2S_DESIGN_COMMIT" -- | sort)" = "$TASK_4_2S_EXPECTED_PATHS"
test -z "$(git ls-files --others --exclude-standard)"
git diff --check
```

  GREEN requires exact `94 = 83 pass + 11 skip`, workflow projection `7/23/8`,
  both execution-free projections, all four stated `17bb5cdd` byte freezes,
  unchanged manifest/summary, the exact checkpoint-to-working-tree path oracle,
  zero non-ignored untracked paths, and static/byte invariants. The pre-commit
  oracle deliberately compares the checkpoint directly to the working tree so
  staged and unstaged tracked changes are both visible. pidfd evidence must
  prove no child or grandchild survives every exercised exceptional path and
  safe normal completion, with identity-safe finalization ordering rather than
  an absence check after reaping.

- [ ] **Step S4: Commit, independent review, and gate.**

  Commit the bounded implementation as `fix(ci): finalize typed gate identity
  cleanup`. The implementation must begin after the unique controller commit
  whose exact subject is `docs(plan): record executable typed gate identity
  checkpoint`; that commit is the changed-path oracle baseline above. Assign
  new independent specification and quality/security reviewers to the exact
  checkpoint-through-implementation range. Immediately after the implementation
  commit and before review, re-resolve the unique subject, repeat the exact
  five-path comparison with `git diff --name-only "$TASK_4_2S_DESIGN_COMMIT"..HEAD`,
  reject any `git status --porcelain=v1 --untracked-files=all` output, and
  record those results in the Task ledger:

```bash
TASK_4_2S_DESIGN_SUBJECT='docs(plan): record executable typed gate identity checkpoint'
TASK_4_2S_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2S_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2S_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2S_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
TASK_4_2S_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2S_DESIGN_COMMIT"..HEAD | sort)" = "$TASK_4_2S_EXPECTED_PATHS"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Both reviewers must return `C0/I0`; otherwise return to design/plan without
  another implementation attempt. This subtask permits **one** implementation
  attempt and **one** independent review pair. Only a controller-owned
  review-evidence commit after that pair may unblock Wave B.

##### Task 4.2T / Wave A design return: typed interruption and evidence finalization

**Status:** The Task 4.2S implementation commit `17645f2a` was reviewed over
the exact range `86146050..17645f2a`. The fresh specification review returned
`C0/I3/M0`, `SPEC_COMPLIANCE NO`, `COMMIT_READY NO`; the fresh
quality/security review returned `C0/I1/M0`, `CHANGES_REQUIRED`,
`COMMIT_READY NO`. The 4.2S one-attempt allowance is exhausted, Wave B remains
blocked, and no manifest verdict is promoted. This subsection is the only
successor design authority for the next bounded implementation attempt. The
initial `4abc8009` design draft and `5d089dd4` checkpoint were committed by a
read-only analysis agent outside its assignment. They remain historical
evidence but grant no implementation authority and are superseded by the
corrected checkpoint defined below. The first corrected checkpoint `b73d2a99`
then received specification `C0/I0/M0` but quality/security `C0/I1/M0`
because it began interruption ownership after inherited-root adoption rather
than at the `N`-to-`M` transfer. It is also superseded and grants no
implementation authority.

**Exact implementation allowlist:** after the uniquely named controller design
checkpoint for this subsection is committed and independently approved, the
successor implementation paths remain exactly
`scripts/validation/ci_gate_runner.py`,
`scripts/validation/ci_gate_adapters.py`,
`tests/validation/test_ci_gate_runner.py`,
`tests/validation/test_ci_gate_adapters.py`, and this Task ledger. Do not alter
schema, workflow, manifest, generated summary, Stage 00 contract, runtime,
Compose, remote, secret, wrapper, direct-`pre-commit`, or Wave B/C files.

- [ ] **Step T0: Commit and independently approve the corrected design.**

  Commit the correction and then one Task-ledger-only checkpoint whose exact
  unique subject is
  `docs(plan): record adopted-root interruption checkpoint`. Fresh
  specification and quality/security reviewers inspect the exact
  `17645f2a`-through-checkpoint range. Both must return `C0/I0`,
  `IMPLEMENTATION_READY YES`; otherwise implementation remains blocked. The
  correction and checkpoint run only changed-document metadata, documentation
  traceability, and diff hygiene. They do not run production tests, child
  gates, runtime, Compose, network, wrapper, or direct pre-commit actions.

- [ ] **Step T1: Add behavior-specific RED witnesses inside existing tests.**

  Keep top-level discovery exactly `94` tests. Extend existing methods only.
  Required new or corrected witnesses:

  1. Adapter ownership transfers immediately when `F_DUPFD_CLOEXEC` returns
     owned capability `M`, before attempting to close inherited capability
     `N`. If closing `N` raises `OSError` or any control-flow
     `BaseException`, `_adopt_root` transfers `M` to the outer cleanup path.
     That path attempts to close `M` exactly once, does not retry or reuse
     `N`, and returns fixed value-free `ci-gate-adapter-root-cleanup`
     regardless of whether the `M` close succeeds, fails, or is interrupted.
     The original close value and interruption never cross the adapter
     boundary. Existing tests inject `KeyboardInterrupt`, `SystemExit`, and
     `GeneratorExit` at the `N` close, verify the exact `N`-then-`M` attempt
     order, verify exactly one `M` close attempt, and reject any raw payload.
  2. Adapter boundary taxonomy preserves an already typed `AdapterError`.
     Every other ordinary `Exception` raised while copying `dict(environ)` or
     dispatching a subcommand becomes the fixed value-free `AdapterError` code
     `ci-gate-adapter-operation` after the owned root capability `M` cleanup
     runs. `OSError` remains the same fixed operation error. A control-flow
     `BaseException` that is not an `Exception`, including `KeyboardInterrupt`,
     `SystemExit`, or `GeneratorExit`, still triggers `M` cleanup and is
     re-raised unchanged only when cleanup succeeds. The adapter never copies
     that interruption's value into an `AdapterError` or diagnostic. A root,
     Compose, or SARIF cleanup failure wins by the existing first-cleanup-domain
     order. Ordinary exception messages, environment values, paths, descriptor
     numbers, and raw payloads never cross the adapter's typed diagnostic
     boundary.
  3. Runner ownership begins when `Popen(start_new_session=True)` returns. If
     `pidfd_open` raises `OSError`, preserve the existing typed acquisition
     recovery. If it raises an ordinary unexpected `Exception`, perform the
     same no-pidfd recovery and return fixed value-free
     `ci-gate-runner-cleanup`. If it raises a control-flow `BaseException`,
     perform the same group `KILL` plus exactly one bounded wait attempt and
     re-raise the original interruption only when recovery succeeds. Any
     signal or wait failure takes precedence as `ci-gate-runner-cleanup`.
  4. After pidfd acquisition and before the sole bounded reap attempt, every
     `GateContractError`, unexpected ordinary `Exception`, or control-flow
     `BaseException` from pidfd readiness, process-group finalization, or proc
     scanning enters one later-failure cleanup controller. It independently
     attempts group `KILL`, bounded pidfd readiness, one bounded wait only when
     readiness is confirmed, and pidfd close. Cleanup success preserves an
     existing `GateContractError`, normalizes an unexpected ordinary
     `Exception` to fixed value-free `ci-gate-runner-cleanup`, and re-raises a
     control-flow interruption unchanged. Any recovery-action failure takes
     precedence as `ci-gate-runner-cleanup`.
  5. The runner tracks whether its single bounded wait/reap has begun. If the
     wait itself raises any exception or interruption, it never signals,
     observes, scans, or waits on the numeric PGID again; it still attempts
     pidfd close and returns fixed `ci-gate-runner-cleanup`. If pidfd close
     fails or is interrupted after a successful reap, it does not retry the
     close or touch the reaped identity and returns the same cleanup code.
     `/proc` directory, PID-directory, and stat descriptors use
     `BaseException`-safe `finally` cleanup, attempt all owned closes
     independently, and convert an incomplete close to the fixed runner
     cleanup domain without leaking the original value.
  6. Evidence wording: later runner recovery performs a single bounded
     `process.wait(timeout=grace)` only when readiness is confirmed; if
     readiness is unavailable or not reached, the runner skips wait, records
     cleanup failure, and still attempts pidfd close. Prohibit `process.poll`,
     `communicate`, and any reaping primitive before identity-safe finalization;
     do not state a broader "no poll" ban that could be confused with bounded
     pidfd polling.
  7. Post-implementation evidence: Task ledger evidence must explicitly record
     the changed-document metadata check result and documentation traceability
     result, or state `unverified` if a command was not run. Existing Ruff,
     compileall, advisory, diff, freeze, workflow, projection, and exact
     five-path evidence remains required.

  RED must fail only on the new adapter ordinary-exception/control-flow
  witnesses and runner acquisition/pre-reap/reap/close interruption witnesses,
  not on import or discovery. Mocks fail the test if any numeric-PGID action
  occurs after a bounded wait attempt. Existing real child/grandchild evidence
  for normal, nonzero, timeout, output-overflow, and read-error paths remains
  unchanged; no new live runtime, Compose, network, or external dependency
  action is authorized.

- [ ] **Step T2: Implement only the typed boundary corrections.**

  Preserve the accepted 4.2S descriptor ownership, Compose/SARIF cleanup order,
  pidfd identity, `/proc` bounds, `ESRCH`, HOME teardown, output bounds,
  minimal environment, and four `17bb5cdd` byte freezes. Do not introduce a
  second cleanup authority, raw PID liveness probe, post-reap PGID observation,
  pathname fallback, nested session, or added test method.

- [ ] **Step T3: Run GREEN and invariant gates.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-harness --list
python3 scripts/validation/run-ci-gate.py --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py --profile local-all-profiles --dry-run --all
python3 -m ruff check \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
python3 -m compileall -q \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
git diff --exit-code 17bb5cdd -- .github/workflow-contract.yml .github/workflows/ci-quality.yml
git diff --exit-code 17bb5cdd -- docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
TASK_4_2T_DESIGN_SUBJECT='docs(plan): record adopted-root interruption checkpoint'
TASK_4_2T_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2T_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2T_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2T_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
test "$(git show -s --format=%s "$TASK_4_2T_DESIGN_COMMIT")" = "$TASK_4_2T_DESIGN_SUBJECT"
TASK_4_2T_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2T_DESIGN_COMMIT" -- | sort)" = "$TASK_4_2T_EXPECTED_PATHS"
test -z "$(git ls-files --others --exclude-standard)"
git diff --check
```

  GREEN requires exact `94 = 83 pass + 11 skip`, workflow projection `7/23/8`,
  both execution-free projections, all four stated `17bb5cdd` byte freezes,
  unchanged manifest/summary, exact metadata and traceability evidence, the
  checkpoint-to-working-tree path oracle, zero non-ignored untracked paths, and
  static/byte invariants.

  After the successor implementation commit, repeat the same unique checkpoint
  resolution and compare `git diff --name-only "$TASK_4_2T_DESIGN_COMMIT"..HEAD`
  to the exact five paths above. Reject any
  `git status --porcelain=v1 --untracked-files=all` output before assigning
  reviewers.

- [ ] **Step T4: Commit, independent review, and gate.**

  This subsection permits one successor implementation attempt and one fresh
  independent review pair. Commit the bounded correction with the exact
  subject `fix(ci): close typed interruption boundary`, then run:

```bash
TASK_4_2T_DESIGN_SUBJECT='docs(plan): record adopted-root interruption checkpoint'
TASK_4_2T_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2T_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2T_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2T_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
test "$(git show -s --format=%s "$TASK_4_2T_DESIGN_COMMIT")" = "$TASK_4_2T_DESIGN_SUBJECT"
TASK_4_2T_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2T_DESIGN_COMMIT"..HEAD | sort)" = "$TASK_4_2T_EXPECTED_PATHS"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Assign fresh independent specification and quality/security reviewers to
  that exact checkpoint-through-implementation range. Both reviewers must
  return `C0/I0`. If either reports an Important or Critical finding, return
  to design/plan again without another implementation attempt. Only a
  controller-owned review-evidence commit after a passing pair may unblock
  Wave B.

##### Task 4.2U / Wave A design return: phase-owned runner lifecycle

**Status:** The sole Task 4.2T implementation `483d3a47` was reviewed over
`5cd98c7b..483d3a47`. Specification returned `C0/I0/M0`,
`SPEC_COMPLIANCE YES`, `COMMIT_READY YES`; quality/security returned
`C0/I1/M0`, `QUALITY_SECURITY CHANGES_REQUIRED`, `COMMIT_READY NO`. The
adapter changes and action-raised runner cleanup are accepted, but the runner
splits bound-process ownership across disjoint source-level `try` regions.
Interruptions in those closable transitions can escape cleanup. Task 4.2T is
exhausted, Wave B remains blocked, and no manifest verdict is promoted.

**Exact implementation allowlist:** after a new independently approved
checkpoint, the sole successor implementation paths are
`scripts/validation/ci_gate_runner.py`,
`tests/validation/test_ci_gate_runner.py`, and this Task ledger. Preserve
`scripts/validation/ci_gate_adapters.py` and
`tests/validation/test_ci_gate_adapters.py` byte-for-byte from `483d3a47`.
Preserve the four `17bb5cdd` contract/workflow/manifest/summary freezes.
Schema, workflow, profile, registry, runtime, Compose, remote, dependency,
secret, wrapper, direct-pre-commit, and Wave B/C changes remain excluded.

- [ ] **Step U0: Commit and independently approve the phase-owned design.**

  The first checkpoint `ce4111d8` is retained as superseded review history:
  its specification review returned `C0/I1` because the Task review matrix
  still named exhausted Task 4.2T as the Wave B prerequisite. Commit that
  controller-owned reconciliation with exact subject
  `docs(plan): reconcile phase-owned runner gate`, then create a new
  Task-ledger-only checkpoint with exact unique subject
  `docs(plan): record reconciled phase-owned runner checkpoint`. Fresh
  specification and quality/security reviewers inspect the exact
  `483d3a47`-through-checkpoint range. Both must return `C0/I0` and
  `IMPLEMENTATION_READY YES`. The design commits run only changed-document
  metadata, documentation traceability, and diff hygiene.

- [ ] **Step U1: Add transition-specific RED witnesses inside the existing
  runner test method.**

  Preserve exactly `94` top-level tests and the existing 11 Wave-C skips.
  The RED design proves:

  1. One outer lifecycle controller begins in the same `try` region that
     assigns a successfully returned `Popen` object and continues without a
     source-level gap through pidfd acquisition, finalization, the sole
     bounded reap, pidfd close, and return. A preinitialized process reference
     distinguishes a `Popen` failure from a bound child. This requirement does
     not claim control over the theoretical interval inside `Popen` before
     Python binds its result.
  2. The controller explicitly tracks `pidfd_acquired`, `reap_started`, and
     `pidfd_close_attempted`. Before reap starts, every `BaseException` after a
     bound process routes to no-pidfd acquisition recovery or pidfd-owned later
     recovery according to state. There is no unprotected transition after
     process binding, pidfd binding, or successful process-group finalization.
  3. `reap_started` is set immediately before the one
     `process.wait(timeout=grace)` call. After that state transition, an
     exception or interruption permits only one independent pidfd-close
     attempt. It never signals a PGID, observes readiness, scans `/proc`, or
     invokes a second wait. `pidfd_close_attempted` is set before the close so
     an interrupted or ambiguous close is never retried. Any incomplete
     reap/close state returns fixed value-free `ci-gate-runner-cleanup`.
  4. Proc-root descriptor cleanup is an actual `finally` region rather than a
     post-catch block. PID-directory and stat descriptors retain their
     independent `finally` closes. Cleanup failure takes fixed runner-cleanup
     precedence and no raw exception value crosses the typed boundary.
  5. Transition injections are behaviorally faithful: a private lifecycle
     state abstraction performs real production state changes, and test
     wrappers raise only after those changes. No no-op production test hook is
     added. Witnesses cover bound-process-before-pidfd, acquired-pidfd-before-
     readiness, finalized-group-before-reap, reap-started-before-wait, wait
     interruption, and close-started interruption. Ordered traces fail if any
     forbidden action follows the reap transition.

  Existing adapter interruption witnesses, live child/grandchild evidence,
  normal/nonzero/timeout/output/read paths, `ESRCH`, proc bounds, HOME
  teardown, and output bounds remain GREEN. RED must fail only in the existing
  runner top-level method on the new transition witnesses, never by import,
  discovery, network, Compose, runtime, or dependency failure.

- [ ] **Step U2: Implement only the single phase-owned runner controller.**

  Replace disjoint lifecycle `try` regions with the U1 controller and real
  state transitions. Do not add a second cleanup authority, unbounded wait,
  raw PID liveness probe, post-reap numeric-PGID action, nested session,
  pathname fallback, or test-only hook. Preserve every accepted Task 4.2T
  adapter and runner behavior outside the closable transition gaps.

- [ ] **Step U3: Run GREEN and exact invariants.**

  GREEN remains `94 = 83 pass + 11 skip`; workflow projection remains
  `7/23/8`; the frozen execution-free projections are `local-harness` list
  `32`, dry-run `32`, and `local-all-profiles` dry-run `35`. Run:

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-harness --list
python3 scripts/validation/run-ci-gate.py --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py --profile local-all-profiles --dry-run --all
python3 -m ruff check \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
python3 -m compileall -q \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
git diff --exit-code 483d3a47 -- \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_adapters.py
git diff --exit-code 17bb5cdd -- \
  .github/workflow-contract.yml \
  .github/workflows/ci-quality.yml \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md
TASK_4_2U_DESIGN_SUBJECT='docs(plan): record reconciled phase-owned runner checkpoint'
TASK_4_2U_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2U_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2U_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2U_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
test "$(git show -s --format=%s "$TASK_4_2U_DESIGN_COMMIT")" = "$TASK_4_2U_DESIGN_SUBJECT"
TASK_4_2U_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2U_DESIGN_COMMIT" -- | sort)" = "$TASK_4_2U_EXPECTED_PATHS"
test -z "$(git ls-files --others --exclude-standard)"
git diff --check
```

- [ ] **Step U4: Commit, independently review, and gate.**

  This subsection permits one implementation attempt and one fresh review
  pair. Commit with exact subject
  `fix(ci): close runner ownership transitions`. Before review, run:

```bash
TASK_4_2U_DESIGN_SUBJECT='docs(plan): record reconciled phase-owned runner checkpoint'
TASK_4_2U_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2U_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2U_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2U_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
test "$(git show -s --format=%s "$TASK_4_2U_DESIGN_COMMIT")" = "$TASK_4_2U_DESIGN_SUBJECT"
TASK_4_2U_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2U_DESIGN_COMMIT"..HEAD | sort)" = "$TASK_4_2U_EXPECTED_PATHS"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Both reviewers must return `C0/I0`; otherwise return to design without
  another implementation attempt. Only controller-owned passing review
  evidence may unblock Wave B.

##### Task 4.2V / Wave A design return: recovery-owned finalization

**Status:** The sole Task 4.2U implementation `ad2df527` was reviewed over
`5dc49631..ad2df527`. Specification returned `C0/I0/M0`,
`SPEC_COMPLIANCE YES`, `COMMIT_READY YES`; quality/security returned
`C0/I2/M0`, `QUALITY_SECURITY CHANGES_REQUIRED`, `COMMIT_READY NO`. The
primary lifecycle transitions, single wait/close sites, proc-root `finally`,
and local evidence are accepted, but cleanup still begins from an `except`
handler outside the primary `try`. Recovery has disjoint source-level gaps,
and unexpected ordinary `Popen` exceptions can expose private traceback
values. Task 4.2U is exhausted, Wave B remains blocked, and no manifest
verdict is promoted.

**Exact implementation allowlist:** after a new independently approved
checkpoint, the sole successor implementation paths remain
`scripts/validation/ci_gate_runner.py`,
`tests/validation/test_ci_gate_runner.py`, and this Task ledger. Preserve
`scripts/validation/ci_gate_adapters.py` and
`tests/validation/test_ci_gate_adapters.py` byte-for-byte from `483d3a47`.
Preserve the four `17bb5cdd` contract/workflow/manifest/summary freezes.
Schema, workflow, profile, registry, runtime, Compose, remote, dependency,
secret, wrapper, direct-pre-commit, and Wave B/C changes remain excluded.

- [ ] **Step V0: Commit and independently approve the recovery-owned
  design.**

  Commit the correction with exact subject
  `docs(plan): define recovery-owned runner finalization`, then create a
  Task-ledger-only checkpoint with exact unique subject
  `docs(plan): record recovery-owned runner checkpoint`. Fresh specification
  and quality/security reviewers inspect the exact
  `ad2df527`-through-checkpoint range. Both must return `C0/I0` and
  `IMPLEMENTATION_READY YES`. The design commits run only changed-document
  metadata, documentation traceability, and diff hygiene.

- [ ] **Step V1: Add recovery-transition and pre-bind RED witnesses inside
  the existing runner test method.**

  Preserve exactly `94` top-level tests and the existing 11 Wave-C skips.
  Extend the real lifecycle-wrapper pattern; do not add a no-op production
  hook. RED must prove:

  1. Process creation is owned by the lifecycle object itself. After a
     successful bind, every finalization and recovery action obtains the
     process from that one object; there is no independently authoritative
     local process reference. The only excluded interval is the theoretical
     interval inside `Popen` before Python binds its return.
  2. A pre-bind `Popen` `OSError` or other ordinary `Exception` becomes fixed
     value-free `ci-gate-child-exec`; `KeyboardInterrupt`, `SystemExit`, and
     `GeneratorExit` re-raise the original object when no child was bound.
     Private sentinels never appear in an ordinary-exception traceback or
     typed error.
  3. Normal completion and every bound-process failure converge on one actual
     `finally` owner. A product exception is recorded, not recovered from
     inside its `except` handler. The `finally` owner completes all still-safe
     cleanup stages before the product/error taxonomy is resolved.
  4. Recovery-transition wrappers raise only after real production actions
     and state mutations. Witnesses cover no-pidfd KILL completed before reap,
     pidfd-owned KILL completed before readiness, recovery readiness completed
     before reap, group-finalized entry to reap, reap started before wait,
     wait interruption, completed reap before close, and close started before
     `os.close`.
  5. Nested finalization guarantees that a `BaseException` at any closable
     recovery transition still reaches every later action permitted by state:
     no-pidfd recovery reaches its sole bounded reap; pidfd-owned recovery
     reaches readiness, readiness-confirmed recovery reaches its sole bounded
     reap, and every acquired-pidfd path reaches exactly one close attempt.
     Any residual cleanup interruption becomes fixed value-free
     `ci-gate-runner-cleanup`.
  6. Immediately after `reap_started`, only the current bounded wait and one
     independent pidfd-close attempt are permitted. After the wait starts,
     traces reject PGID signaling, readiness observation, `/proc` scanning,
     or a second wait. `pidfd_close_attempted` is set before `os.close`, so an
     interrupted or ambiguous close is never retried.

  Existing live child/grandchild, normal/nonzero/timeout/output/read, `ESRCH`,
  proc-bound, HOME teardown, adapter, and output-bound evidence remains
  GREEN. RED failures must be limited to the new witnesses in the existing
  runner top-level method, never import, discovery, network, Compose, runtime,
  or dependency failure.

- [ ] **Step V2: Implement one lifecycle-owned nested finalizer.**

  Replace the recovery call from the primary `except` with this structure:

  1. The lifecycle object performs and stores `Popen` binding and becomes the
     sole process identity. The primary body records any `BaseException` as
     the product error.
  2. One actual outer `finally` invokes a fail-closed lifecycle finalizer for
     both success and failure. The finalizer uses nested `try/finally`
     ownership, not sequential disjoint `try` regions:
     - without a pidfd, the KILL stage owns a `finally` that attempts the sole
       bounded reap;
     - with a pidfd before group finalization, KILL owns readiness
       observation, readiness owns the conditional sole bounded reap, and
       the reap stage owns the sole pidfd-close attempt;
     - after successful group finalization, the finalizer skips KILL and
       readiness and owns only the sole bounded reap followed by close;
     - after `reap_started`, no earlier stage can be re-entered and the
       deepest remaining action is the one close attempt.
  3. Each action catches and records `BaseException` without preventing its
     nested `finally`; any residual exception escaping a stage is caught only
     after the deepest permitted finalizer has run and is normalized to fixed
     runner cleanup. There is no second cleanup authority, retry loop,
     unbounded wait, raw PID liveness probe, post-reap numeric-PGID action,
     nested session, pathname fallback, or test-only hook.
  4. Cleanup failure takes precedence. With successful cleanup, preserve an
     existing `GateContractError`, normalize a pidfd-acquisition `OSError`,
     normalize other bound ordinary exceptions to fixed runner cleanup, and
     re-raise bound control-flow objects. With no bound child, normalize all
     ordinary `Popen` exceptions to fixed child-exec and re-raise only
     non-`Exception` control flow.
  5. Retain the actual proc-root `finally` and the independent PID-directory
     and stat-descriptor `finally` regions from Task 4.2U.

- [ ] **Step V3: Run GREEN and exact invariants.**

  GREEN remains `94 = 83 pass + 11 skip`; workflow projection remains
  `7/23/8`; execution-free projections remain `local-harness` list `32`,
  dry-run `32`, and `local-all-profiles` dry-run `35`. Run:

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-harness --list
python3 scripts/validation/run-ci-gate.py --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py --profile local-all-profiles --dry-run --all
python3 -m ruff check \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
python3 -m compileall -q \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
git diff --exit-code 483d3a47 -- \
  scripts/validation/ci_gate_adapters.py \
  tests/validation/test_ci_gate_adapters.py
git diff --exit-code 17bb5cdd -- \
  .github/workflow-contract.yml \
  .github/workflows/ci-quality.yml \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md
TASK_4_2V_DESIGN_SUBJECT='docs(plan): record recovery-owned runner checkpoint'
TASK_4_2V_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2V_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2V_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2V_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
test "$(git show -s --format=%s "$TASK_4_2V_DESIGN_COMMIT")" = "$TASK_4_2V_DESIGN_SUBJECT"
TASK_4_2V_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2V_DESIGN_COMMIT" -- | sort)" = "$TASK_4_2V_EXPECTED_PATHS"
test -z "$(git ls-files --others --exclude-standard)"
git diff --check
```

- [ ] **Step V4: Commit, independently review, and gate.**

  This subsection permits one implementation attempt and one fresh review
  pair. Commit with exact subject
  `fix(ci): close recovery ownership transitions`. Before review, run:

```bash
TASK_4_2V_DESIGN_SUBJECT='docs(plan): record recovery-owned runner checkpoint'
TASK_4_2V_DESIGN_COMMIT="$(git log --format=%H --grep="^${TASK_4_2V_DESIGN_SUBJECT}$")"
test -n "$TASK_4_2V_DESIGN_COMMIT"
test "$(printf '%s\n' "$TASK_4_2V_DESIGN_COMMIT" | wc -l | tr -d ' ')" = "1"
test "$(git show -s --format=%s "$TASK_4_2V_DESIGN_COMMIT")" = "$TASK_4_2V_DESIGN_SUBJECT"
TASK_4_2V_EXPECTED_PATHS="$(printf '%s\n' \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  scripts/validation/ci_gate_runner.py \
  tests/validation/test_ci_gate_runner.py | sort)"
test "$(git diff --name-only "$TASK_4_2V_DESIGN_COMMIT"..HEAD | sort)" = "$TASK_4_2V_EXPECTED_PATHS"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Both reviewers must return `C0/I0`; otherwise return to design without
  another implementation attempt. Only controller-owned passing review
  evidence may unblock Wave B.

#### Task 4.3 / Wave B / T-TSDC-004R-3: Atomic Workflow and Local Projection Cutover

**Files:**

- Preserve the reviewed strict-JSON schema-v2
  `.github/workflow-contract.yml` byte-for-byte.
- Modify `.github/workflows/ci-quality.yml`.
- Modify `scripts/validation/github_workflow_contract.py`.
- Preserve the stable thin
  `scripts/validation/check-github-workflow-contract.py` CLI.
- Modify `tests/validation/test_github_workflow_contract.py`.
- Modify `scripts/validation/check-repo-contracts.sh`.
- Modify `scripts/validation/run-local-qa-gates.sh`.
- Modify these descriptor-compatibility consumers without changing their
  direct-execution behavior:
  `scripts/hardening/check-all-hardening.sh`,
  `scripts/operations/sync-provider-surfaces.sh`,
  `scripts/operations/sync-tech-stack-versions.sh`,
  `scripts/validation/check-agent-governance-contract.py`,
  `scripts/validation/check-document-corpus-lifecycle.py`,
  `scripts/validation/check-document-metadata.py`, and
  `scripts/validation/check-supply-chain-policy.py`.
- Modify `tests/validation/test_agent_governance_ci_routing.py`.
- Modify `tests/validation/test_target_surface_delta_contracts.py`.
- Preserve `scripts/validation/run-ci-precommit.sh`,
  `tests/validation/test_run_ci_precommit.sh`, and
  `scripts/requirements-pre-commit.txt`; register the existing CI wrapper as a
  typed leaf without turning it into an Agent route.
- Modify `.github/INDEX.md` and `.github/rulesets/main-protection.md`.
- Modify `docs/00.agent-governance/policies/github-governance.md` and
  `docs/00.agent-governance/roles/qa.md`.
- Modify exact existing Task 4 manifest rows, regenerate the summary, and
  append Task evidence.
- Do not create `.github/README.md` or modify `.pre-commit-config.yaml`.

**Interfaces:**

- Consumes: reviewed R1 contract and R2 runner interfaces.
- Produces: exact required-workflow projection, shared local profiles, and an
  unused-but-still-present old semantic interpreter awaiting Wave C removal.

- [ ] **Step 1: Add workflow-projection RED tests.**

  Replace the old ownership assertions with exact tests named
  `test_required_jobs_project_their_registered_roots_once`,
  `test_required_run_steps_use_only_static_gate_invocations`,
  `test_workflow_projection_rejects_dynamic_ids_and_free_form_shell`,
  `test_workflow_and_registry_co_mutations_fail_closed`,
  `test_ci_and_local_profiles_share_node_definitions`, and
  `test_repository_umbrella_is_wiring_only`. Add exact regressions named
  `test_local_profiles_exclude_compose_env_setup`,
  `test_local_wrapper_preserves_existing_env_bytes`,
  `test_storybook_root_runs_setup_and_coverage_in_one_runner_lifetime`, and
  `test_descriptor_mode_root_and_import_compatibility_set_is_exact`.

```python
def test_required_run_steps_use_only_static_gate_invocations(self) -> None:
    programs = self.required_quality_run_programs()
    for program in programs:
        self.assertRegex(
            program,
            r"\Apython3 scripts/validation/run-ci-gate\.py "
            r"--profile ci --gate [a-z0-9.-]+\Z",
        )
```

  Preserve and rerun the current trigger, permission, concurrency, timeout,
  required-job, Action, YAML safety, bounded-reader, ambiguous-`on`, and CI
  pre-commit tests. Add mutations for multiline run bodies, workflow
  expressions, variables, heredocs, substitutions, `eval`, `source`, shell
  `-c`, direct scripts/tools, unregistered local Actions, duplicate
  `suite_key`, duplicate reachable leaf, and changed required root.

- [ ] **Step 2: Run RED against the reviewed schema-v2 registry and current
  workflows.**

```bash
python3 -m unittest \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
```

Expected RED: the schema-v2 registry and its graph remain valid, while current
required-quality workflow programs still contain direct and multiline
executable steps that fail the new exact projection tests.

- [ ] **Step 3: Freeze the reviewed canonical registry as the cutover input.**

  Read the Task 4.2 review-evidence commit from the Task ledger and require
  `.github/workflow-contract.yml` to be byte-unchanged from that checkpoint.
  It already contains all workflow, trigger, permission, job, Action, typed
  gate, job-root, and profile-root facts and contains no `owner_commands` or
  `expensive_commands`. Any needed registry change returns to Task 4.2 and
  consumes its bounded remediation loop rather than being folded into Wave B.

- [ ] **Step 4: Migrate the exact descriptor-compatibility set.**

  Each of the seven named consumers resolves its repository root from
  runner-created `HYHOME_CI_GATE_ROOT` when present and otherwise retains its
  current direct-execution `BASH_SOURCE[0]` or `__file__` fallback.
  `check-document-metadata.py` derives its sibling import directory from that
  selected root. No consumer reads a controller-supplied value because the
  runner builds the child environment from empty state. Run the descriptor
  compatibility test once per path and prove the focused workflow wrapper can
  import `github_workflow_contract` through the fixed runner-created Python
  path. Direct-execution regression tests must remain green.

- [ ] **Step 5: Convert every required-quality executable step.**

  Each `run:` scalar becomes one exact static `run-ci-gate.py` invocation.
  The ordered union of the invoked targets' expansions in each job must equal
  its root DAG expansion exactly once. A stateful setup chain is invoked as
  its complete root in one runner process: in particular
  `ci.storybook-coverage` performs node dependency installation, Playwright
  installation, and coverage under one fresh HOME that survives until the
  root finishes. Conditionally separated nodes such as the existing
  `always()` QA-summary leaf may remain separate exact static invocations, but
  their combined expansion must still cover the root once with no overlap.
  Preserve the metadata event condition, git-flow job condition, setup
  Actions, least-privilege permissions, timeouts, concurrency, and SARIF
  upload Action. Environment blocks may contain only keys admitted by the
  invoked node.

- [ ] **Step 6: Switch workflow validation to structural projection.**

  Replace the Task 4.2 unchanged-workflow transition boundary with active
  structural projection from the reviewed `gate_registry`.
  `validate_workflows` compares exact static gate invocations with root
  expansion and retains all existing workflow-shape, permission, trigger,
  Action, and remote-mutation checks. No semantic-owner compatibility
  projection or command table exists; the unused old parser functions remain
  dead code only until the independent cutover review.

- [ ] **Step 7: Switch local QA and the repository umbrella.**

  `run-local-qa-gates.sh` obtains `--list`, `--dry-run`, and execution order
  from the exact `profile_roots` above. `--script-backed` and `--harness`
  invoke their matching profile once. `--all-profiles` invokes the registered
  `local-all-profiles` profile once; it retains no child-command list or
  second direct `--gate` route.
  The local routes never reach `setup.compose-env`; their Compose validators
  retain the existing create-only-and-cleanup behavior and preserve any
  existing `.env` byte-for-byte. `check-repo-contracts.sh` no longer invokes
  the focused workflow checker because `leaf.workflow-contract` owns that
  suite explicitly in both the CI root and local workflow harness. The
  repository umbrella performs only unique wiring checks. Gate-specific tests
  prove it does not intentionally dispatch any sibling registered suite.

- [ ] **Step 8: Synchronize governance and desired-state documentation.**

  Replace semantic-parser claims with structural registry/DAG guarantees,
  preserve the 16 status IDs, keep non-gating automation separate, and state
  that remote enforcement remains unverified until a separately approved
  remote execution. Under the existing exact-row oracle, update the manifest
  consumer edges for `ci_gate_runner.py`, `run-ci-gate.py`,
  `ci_gate_adapters.py`, and their focused tests to the now-tracked workflow,
  local-profile, and validation consumers. Regenerate only the derived summary:

```bash
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory \
  --write-summary
```

  Task 4.2 already owns the new
  `scripts/validation/check-agent-governance-contract.py` row and all seven
  mode-provenance dispositions. Add only the two new `update` rows for
  `scripts/operations/sync-provider-surfaces.sh` and
  `scripts/operations/sync-tech-stack-versions.sh`, each with its own path as
  canonical owner and the typed local profile plus descriptor-compatibility
  test as direct consumers. Update the existing compatibility rows for
  hardening, agent governance, document corpus, metadata, and supply-chain
  policy with their new typed-runner consumers. The exact delta oracle becomes
  158 rows: 85 `preserve`, 73 `update`, zero `migrate`, and zero `delete`.

- [ ] **Step 9: Run cutover GREEN.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
bash tests/validation/test_run_ci_precommit.sh
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile ci --list
python3 scripts/validation/run-ci-gate.py \
  --profile ci \
  --dry-run \
  --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-script-backed \
  --dry-run \
  --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness \
  --dry-run \
  --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles \
  --dry-run \
  --all
bash scripts/validation/run-local-qa-gates.sh --list
bash -n \
  scripts/validation/check-repo-contracts.sh \
  scripts/validation/run-local-qa-gates.sh \
  scripts/hardening/check-all-hardening.sh \
  scripts/operations/sync-provider-surfaces.sh \
  scripts/operations/sync-tech-stack-versions.sh
shellcheck --severity=warning \
  scripts/validation/check-repo-contracts.sh \
  scripts/validation/run-local-qa-gates.sh \
  scripts/hardening/check-all-hardening.sh \
  scripts/operations/sync-provider-surfaces.sh \
  scripts/operations/sync-tech-stack-versions.sh
actionlint
python3 -m ruff check \
  scripts/validation/ci_gate_contract.py \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/github_workflow_contract.py \
  tests/validation/test_ci_gate_contract.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_github_workflow_contract.py
python3 -m compileall -q \
  scripts/validation/ci_gate_contract.py \
  scripts/validation/ci_gate_runner.py \
  scripts/validation/run-ci-gate.py \
  scripts/validation/ci_gate_adapters.py \
  scripts/validation/github_workflow_contract.py \
  tests/validation/test_ci_gate_contract.py \
  tests/validation/test_ci_gate_runner.py \
  tests/validation/test_ci_gate_adapters.py \
  tests/validation/test_github_workflow_contract.py \
  tests/validation/test_agent_governance_ci_routing.py
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
git diff --check
```

Expected GREEN: exact counts remain 7 workflows, 23 jobs, eight Actions, and
16 required IDs; the delta oracle is exactly 158 rows with 85 `preserve`, 73
`update`, and no destructive row; every required run step is a static
registered gate;
CI/local dry runs are deterministic and execute nothing; no direct
pre-commit, network, remote mutation, runtime, Compose service, dependency
installation, credential, or secret-payload action occurs.

- [ ] **Step 10: Commit the atomic cutover.**

```bash
git add \
  .github/workflows/ci-quality.yml \
  .github/INDEX.md \
  .github/rulesets/main-protection.md \
  docs/00.agent-governance/policies/github-governance.md \
  docs/00.agent-governance/roles/qa.md \
  scripts/validation/check-agent-governance-contract.py \
  scripts/validation/check-document-corpus-lifecycle.py \
  scripts/validation/check-document-metadata.py \
  scripts/validation/check-supply-chain-policy.py \
  scripts/hardening/check-all-hardening.sh \
  scripts/operations/sync-provider-surfaces.sh \
  scripts/operations/sync-tech-stack-versions.sh \
  scripts/validation/github_workflow_contract.py \
  scripts/validation/check-repo-contracts.sh \
  scripts/validation/run-local-qa-gates.sh \
  scripts/README.md \
  tests/validation/test_github_workflow_contract.py \
  tests/validation/test_agent_governance_ci_routing.py \
  tests/validation/test_target_surface_delta_contracts.py \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "ci(governance): cut over to typed gate projections"
```

#### Task 4.4 / T-TSDC-004R-4: Independent Cutover Review Gate

- [ ] Assign a fresh read-only specification reviewer to the exact R1-through-
  R3 range.
- [ ] Assign a different fresh read-only quality/security reviewer to that
  range.
- [ ] Require both reviews to verify the 16 IDs, root/suite uniqueness, fake
  executor order, CI/local profile parity, exact workflow grammar, trigger and
  permission retention, Action registry, pre-commit separation, descriptor
  identity and compatibility-root parity, `GIT_*` isolation, timeout,
  value-free diagnostics, local `.env` preservation, stateful Storybook
  setup-to-coverage continuity, and absence of hidden repository-umbrella
  sibling dispatch.
- [ ] Record C0/I0 verdicts in one evidence-only commit:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): record typed CI cutover review"
```

If either reviewer finds a design-contract defect, stop and return to
design/plan. For an implementation defect, use only the canonical
two-attempt loops; exhaustion blocks Task 4R.

#### Task 4.4W / T-TSDC-004R-4W: Option-Aware Wrapper-Proof Design Return

> **Superseded for execution by Task 4.4X.** Retain this section as failed
> design evidence only. Do not execute any 4W command block or create any 4W
> pending commit subject.

**Design-return prerequisite and authority boundary:**

- The exact unique `docs(task): record exhausted typed cutover review` commit
  must resolve to `1b054313` and be an ancestor of the implementation
  checkpoint.
- The Plan-only design commit may modify only this Plan and the sibling Task
  ledger. It grants no implementation authority until a fresh read-only
  specification reviewer and a different fresh read-only quality/security
  reviewer both return `C0/I0/M0`.
- The corrected Plan commit subject is exactly
  `docs(plan): correct option-aware cutover proof`. The final reviewers inspect
  the complete net design from `1b054313` through that unique correction.
  After both final reviews return `C0/I0/M0`, the controller records them in a
  Task-ledger-only commit whose exact unique subject is
  `docs(task): record option-aware proof plan reviews`. That commit must be
  `HEAD`, must descend from the unique corrected Plan commit, and becomes the
  immutable implementation base.
- Only after that executable checkpoint does one implementation agent receive
  exactly one attempt. That attempt may modify only:
  `tests/validation/test_agent_governance_ci_routing.py` and
  `docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md`.
- Freeze `.github/workflow-contract.yml`,
  `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, every typed gate runner and
  adapter, all target-delta artifacts, and every other tracked path. The
  missing proof is confined to the static test oracle; production behavior is
  already frozen.
- The implementation commit subject is exactly
  `fix(ci): close option-bearing wrapper proof`. A fresh specification
  reviewer and a different fresh quality/security reviewer inspect the exact
  checkpoint-to-implementation range. Any non-`C0/I0/M0` result ends this
  one-attempt successor without a retry, keeps Task 4R blocked, and requires a
  new user-approved design return.

**Required parser contract:**

- Replace only the narrow wrapper-prefix handling inside
  `_registered_sibling_dispatches` with a dependency-free, option-arity-aware
  recursive token parser. It must continue to preserve the existing literal
  Python/Bash, direct executable, quoted, variable-mediated,
  helper-indirection, Python heredoc `subprocess`, and `os.system` evidence
  families.
- Parse a wrapper chain until it reaches one real command sink. Initialize one
  work budget as `8 * (1 + original token count + total source-token character
  count)`. Charge every wrapper/option token and every
  split-string character against that budget; token expansion never adds
  credit. Budget exhaustion is ambiguous and fails closed. The parser must
  never invoke a shell, wrapper, sibling entrypoint, or repository gate.
- For the
  [Bash `command` builtin](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html),
  accept `-p`, `--`, and valid short-option clusters. `-p`
  continues to the wrapped command. Any `-v` or `-V` occurrence is a
  query-only form and therefore is not a dispatch. Unknown or malformed
  options are ambiguous and fail closed when a registered sibling path is
  present.
- For the
  [Bash `exec` builtin](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html),
  accept `-c`, `-l`, their valid short-option clusters, `-a NAME`
  (including an attached short argument when unambiguous), and `--`.
  Option operands are consumed before recursively parsing the wrapped
  command. Missing operands and unknown options are ambiguous and fail closed.
- For GNU `env`, follow the
  [Coreutils 9.11 `env` grammar](https://www.gnu.org/software/coreutils/manual/html_node/env-invocation.html).
  Accept flag-only `-`, `-i`/`--ignore-environment`, `-v`/`--debug`, and
  `--list-signal-handling`; accept the optional-equals signal forms
  `--block-signal[=SIG]`, `--default-signal[=SIG]`, and
  `--ignore-signal[=SIG]`; consume exactly one operand for
  `-u`/`--unset`, `-C`/`--chdir`, and `-a`/`--argv0`, including valid
  attached and long-equals forms; and treat `--help`/`--version` as
  query-only. `-0`/`--null` is no-dispatch: without a command it changes
  environment-list output, and with a command GNU `env` exits `125` rather
  than invoking it. Before `--`, every operand containing `=` is an environment
  assignment and the first operand without `=` is the command. After `--`,
  the immediately following token is the command even when it contains `=`.
- Do not substitute POSIX shell `shlex.split` for GNU
  `env -S`/`--split-string`. Use a small pure lexer for the documented static
  grammar: unquoted whitespace, single/double quotes, `\c`, `\f`, `\n`,
  `\r`, `\t`, `\v`, `\#`, `\$`, `\_`, `\"`, `\'`, `\\`, and a comment only
  when `#` begins an argument. Outside quotes `\_` is an argument separator;
  inside double quotes it is a space. `\c` outside quotes discards the
  remainder. Insert the resulting tokens at the `-S` position and resume the
  same bounded `env` parser. The parser must not read the ambient environment:
  `${VARNAME}`, unsupported/dangling escapes, malformed quotes, missing
  operands, and unknown options are ambiguous and fail closed
  deterministically by returning the complete registered sibling set. This is
  stricter than runtime expansion and keeps the proof environment-independent.
- Wrapper nesting is recursive, including combinations such as
  `env -u HOME command -p exec -a gate python3 <sibling>`. A registered
  sibling path consumed solely as the operand of a recognized option is not a
  dispatch. A sibling path in an unknown or malformed wrapper form is
  returned as a finding because execution position cannot be proved.
- The oracle returns only a deterministic set of registered sibling paths.
  It must not emit source statements, option values, environment values, raw
  command text, or exception payloads. Existing value-free assertion output
  remains unchanged.

- [ ] **Step 1: Prove the exact corrected Plan and Plan-review evidence
  checkpoints, then bind the clean implementation base.**

  Before this step, final read-only Plan reviewers inspect the complete
  `1b054313..$plan_checkpoint` net range. After both return `C0/I0/M0`, the
  controller changes only the Task ledger, records both reports and the exact
  range, and creates:

```bash
test -z "$(git ls-files --others --exclude-standard)"
test "$(git diff --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record option-aware proof plan reviews"
```

  The implementation agent then runs this executable prerequisite:

```bash
expected_predecessor="$(git rev-parse 1b054313)"
test "$(git log -1 --format=%H \
  --grep='^docs(task): record exhausted typed cutover review$')" = \
  "$expected_predecessor"
test "$(git log --format=%H \
  --grep='^docs(task): record exhausted typed cutover review$' | wc -l)" -eq 1
test "$(git log --format=%H \
  --grep='^docs(plan): correct option-aware cutover proof$' | wc -l)" -eq 1
plan_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(plan): correct option-aware cutover proof$')"
initial_plan="$(git rev-parse 98a3558d)"
git merge-base --is-ancestor "$initial_plan" "$plan_checkpoint"
test "$(git rev-list --count "$initial_plan..$plan_checkpoint")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$plan_checkpoint" | sort)" = "$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test "$(git log --format=%H \
  --grep='^docs(task): record option-aware proof plan reviews$' | wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record option-aware proof plan reviews$')"
test "$(git rev-parse HEAD)" = "$implementation_base"
git merge-base --is-ancestor "$expected_predecessor" "$plan_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
test "$(git rev-list --count "$plan_checkpoint..$implementation_base")" -eq 1
test "$(git diff --name-only \
  "$expected_predecessor..$implementation_base" | sort)" = "$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test "$(git diff-tree --no-commit-id --name-only -r \
  "$implementation_base" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

- [ ] **Step 2: Add the complete RED mutation matrix before changing the
  parser.**

  Put every new case in
  `test_repository_umbrella_is_wiring_only`; do not hide required cases in a
  sibling method that the named RED command does not execute. The exact
  minimum matrix is:

  - dispatch-positive `command -p`, `command -pp`, and `command --`;
  - query-only `command -v`, `command -V`, `command -pv`, `command -pV`, and
    `command -vp` negatives;
  - dispatch-positive `exec -a NAME`, `exec -aNAME`, `exec -c`, `exec -l`,
    `exec -cl`, `exec -claNAME`, and `exec --`;
  - dispatch-positive GNU `env -`, `-i`, `--ignore-environment`, `-v`,
    `--debug`, `--list-signal-handling`,
    `--block-signal`, `--block-signal=PIPE`, `--default-signal`,
    `--default-signal=PIPE`, `--ignore-signal`,
    `--ignore-signal=PIPE`, `-u NAME`, `-uNAME`, `--unset NAME`,
    `--unset=NAME`, `-C DIR`, `-CDIR`, `--chdir DIR`, `--chdir=DIR`,
    `-a ARG`, `-aARG`, `--argv0 ARG`, `--argv0=ARG`, short clusters
    `-iv`, `-vSSTRING`, ordinary `-S STRING`, `-SSTRING`,
    `--split-string STRING`, `--split-string=STRING`, pre-command
    assignments, and `--`;
  - non-dispatch `env -0`, `env --null`, `env --help`, and `env --version`
    negatives with the sibling positioned where a command would otherwise
    appear;
  - GNU split-string positives for ordinary whitespace, quoted whitespace,
    and `\_`; negatives proving `\c` and a comment discard a later sibling;
    an environment-expansion case that deterministically fails closed without
    reading ambient state; and invalid-escape plus malformed-quote cases that
    fail closed;
  - at least one `-S` expansion whose inserted tokens are another wrapper
    chain, plus one nested input that exhausts the fixed no-credit work budget
    and deterministically fails closed without unbounded recursion;
  - the nested dispatch
    `env -u HOME command -p exec -a gate python3 <sibling>`;
  - recognized option operands equal to a registered sibling path without an
    executable sibling sink for `env -u`, `env -C`, `env -a`, and `exec -a`,
    all of which must remain negative;
  - missing-operand, invalid split-string, and unknown-option forms for all
    three wrappers, which must fail closed when a sibling path remains in the
    ambiguous token stream; and
  - existing bare-wrapper and non-wrapper families, which must remain green.

  Run the focused test and record a behavior-specific RED in the Task ledger.
  Import or syntax errors, a missing test, or failure unrelated to the new
  option-bearing mutations do not count as RED:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
  -v
```

- [ ] **Step 3: Implement the bounded parser and run focused GREEN.**

  Use small pure helpers with explicit parse outcomes for executable,
  query-only, absent-command, and ambiguous forms. Consume option arity before
  evaluating a command position, preserve the existing path-resolution and
  heredoc evidence, and keep diagnostics value-free.

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 -m unittest \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
```

- [ ] **Step 4: Run the full frozen cutover regression and static evidence
  ladder.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
python3 scripts/validation/run-ci-gate.py --profile ci --list
python3 scripts/validation/run-ci-gate.py --profile ci --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-script-backed --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles --dry-run --all
python3 -m ruff check \
  tests/validation/test_agent_governance_ci_routing.py
python3 -m compileall -q \
  tests/validation/test_agent_governance_ci_routing.py
git diff --check
```

  Ruff absence is recorded as `unverified`; dependency installation is
  prohibited. The repository umbrella, registered typed child gates, direct
  pre-commit, controlled wrapper, Compose/runtime, network, secrets,
  credentials, remote state, and Graphify update remain prohibited. The
  named standalone static validators and execution-free `--list`/`--dry-run`
  projections above are the only authorized child-gate evidence; neither the
  repository umbrella nor a typed leaf executes. Bash and ShellCheck are not
  rerun because this successor freezes all shell files.

- [ ] **Step 5: Prove freezes, exact scope, modes, and commit the sole
  implementation attempt.**

```bash
test "$(git rev-parse HEAD)" = "$implementation_base"
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" --
    git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_paths"
git diff --exit-code "$implementation_base" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test "$(git ls-files -s \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test "$(git ls-files -s \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
git diff --check
git add \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = "$expected_paths"
git commit -m "fix(ci): close option-bearing wrapper proof"
implementation_commit="$(git rev-parse HEAD)"
test "$(git log --format=%H \
  --grep='^fix(ci): close option-bearing wrapper proof$' | wc -l)" -eq 1
test "$(git log -1 --format=%H \
  --grep='^fix(ci): close option-bearing wrapper proof$')" = \
  "$implementation_commit"
test "$(git rev-list --count \
  "$implementation_base..$implementation_commit")" -eq 1
test "$(git diff --name-only \
  "$implementation_base..$implementation_commit" | sort)" = \
  "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test "$(git ls-tree "$implementation_commit" \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$implementation_commit" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

- [ ] **Step 6: Require one fresh implementation review pair and record it
  separately.**

  The reviewers inspect the exact
  `$implementation_base..$implementation_commit` range. Both must verify every
  wrapper family, option arity, nested
  recursion, query-only negative, option-operand false-positive negative,
  malformed/unknown fail-closed case, deterministic bound, value-free output,
  frozen production paths, exact two-path scope, and all recorded validation
  evidence. On `C0/I0/M0`, record the exact range and verdicts in an
  evidence-only commit:

```bash
test -z "$(git status --porcelain=v1 --untracked-files=all)"
# After recording the two C0/I0 reports and exact range in the Task ledger:
test -z "$(git ls-files --others --exclude-standard)"
test "$(git diff --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record option-aware cutover review"
review_checkpoint="$(git rev-parse HEAD)"
test "$(git rev-list --count \
  "$implementation_commit..$review_checkpoint")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$review_checkpoint" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Only that accepted review checkpoint authorizes Task 4.5 Wave C. A failed
  review grants no retry and no downstream authority.

#### Task 4.4X / T-TSDC-004R-4X: Session-Local Option-Proof Design Return

> **Superseded for execution by Task 4.4Y.** Retain this section as failed
> design evidence only. Do not execute any 4X command block or create any 4X
> pending commit subject.

**Authority boundary and supersession:**

- The exact unique `docs(task): record exhausted option-aware plan review`
  commit must resolve to `7b792a37`, be `HEAD` when this design is authored,
  and remain an ancestor of every 4X checkpoint.
- This Plan-only successor may modify only this Plan and the sibling Task
  ledger. Its exact unique subject is
  `docs(plan): define session-local option proof`.
- Two fresh read-only reviewers inspect the complete
  `7b792a37..$plan_checkpoint` range: one specification reviewer and a
  different quality/security reviewer. Both must return `C0/I0/M0`. Any other
  result returns to design; there is no Plan correction inside 4X.
- After both approvals, the controller records the reports and exact range in
  a Task-ledger-only commit with the exact unique subject
  `docs(task): record session-local proof plan reviews`. That clean commit is
  the immutable implementation base.
- One implementation agent then receives exactly one attempt. It may modify
  only `tests/validation/test_agent_governance_ci_routing.py` and the sibling
  Task ledger. Its exact unique subject is
  `fix(ci): close session-local wrapper proof`.
- Freeze `.github/workflow-contract.yml`,
  `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, every typed gate runner and
  adapter, every target-delta artifact, and every other tracked path.
- A fresh read-only specification reviewer and a different fresh read-only
  quality/security reviewer inspect the exact implementation-base-to-commit
  range. Both must return `C0/I0/M0`. The controller then records the reports
  in a Task-ledger-only commit with the exact unique subject
  `docs(task): record session-local wrapper review`.
- Any non-`C0/I0/M0` implementation review exhausts 4X without a retry and
  keeps Task 4R, Wave C, Tasks 5–6, and final branch review blocked.
- 4X incorporates the complete 4W parser contract, RED matrix, focused GREEN,
  frozen regression ladder, value-free diagnostics rule, and prohibition
  boundaries except for the replacements stated below. If text conflicts,
  4X controls. All 4W command blocks and its three uncreated pending subjects
  are non-executable historical text.

**Correct GNU `env` command selection:**

- `--` ends GNU `env` option parsing only. It does not end the later
  environment-assignment scan.
- After recognized options are consumed, whether option parsing ended because
  of `--` or because the next token is an operand, consume every consecutive
  token containing `=` as an environment assignment. The first subsequent
  token without `=` is the command. If no such token exists, there is no
  dispatch.
- Therefore `env -- NAME=VALUE python3 <sibling>` and
  `env -- A=1 B=2 python3 <sibling>` dispatch the registered sibling, while
  `env -- NAME=<sibling>` alone does not. A registered sibling path embedded
  only in an assignment remains an assignment operand, not a command sink.
- Once option parsing has ended, a non-assignment token beginning with `-` is
  the command. The static parser does not resume option parsing after `--`.
  Tokens inserted by `-S` enter the same bounded parser and follow the same
  transition.
- The prior 4W sentence claiming that the token immediately after `--` is
  always the command is superseded. This replacement follows the GNU
  [Coreutils `env` invocation grammar](https://www.gnu.org/software/coreutils/manual/html_node/env-invocation.html):
  option parsing and assignment consumption are distinct phases.

**Session-local checkpoint rule:**

- Every fenced shell block is an independent agent/controller/reviewer
  session. A block must resolve every commit variable it reads inside that
  same block from an exact unique subject or an immutable literal.
- No later block may rely on `plan_checkpoint`, `implementation_base`,
  `implementation_commit`, `review_checkpoint`, `expected_paths`, or another
  variable assigned in an earlier block.
- Every subject lookup proves a count of exactly one before use. Every
  authority transition proves ancestry, direct commit count, exact
  `diff-tree`/range paths, required file modes, and a clean tracked and
  untracked state as applicable.

- [ ] **Step 1: Commit and independently review the 4X Plan.**

  Immediately after the Plan commit and before either review, the controller
  runs this self-contained checkpoint proof:

```bash
design_base="$(git rev-parse 7b792a37)"
test "$(git log --format=%H \
  --grep='^docs(task): record exhausted option-aware plan review$' |
  wc -l)" -eq 1
test "$(git log -1 --format=%H \
  --grep='^docs(task): record exhausted option-aware plan review$')" = \
  "$design_base"
test "$(git log --format=%H \
  --grep='^docs(plan): define session-local option proof$' |
  wc -l)" -eq 1
plan_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(plan): define session-local option proof$')"
test "$(git rev-parse HEAD)" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
test "$(git rev-list --count \
  "$design_base..$plan_checkpoint")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$plan_checkpoint" | sort)" = "$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test "$(git ls-tree "$plan_checkpoint" \
  docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$plan_checkpoint" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  After both Plan reviewers return `C0/I0/M0`, edit only the Task ledger. Run
  this separate self-contained proof and create the evidence checkpoint:

```bash
test "$(git log --format=%H \
  --grep='^docs(plan): define session-local option proof$' |
  wc -l)" -eq 1
plan_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(plan): define session-local option proof$')"
test "$(git rev-parse HEAD)" = "$plan_checkpoint"
actual_paths="$(
  {
    git diff --name-only
    git diff --cached --name-only
    git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record session-local proof plan reviews"
test "$(git log --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$')"
test "$(git rev-parse HEAD)" = "$implementation_base"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
test "$(git rev-list --count \
  "$plan_checkpoint..$implementation_base")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$implementation_base" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test "$(git ls-tree "$implementation_base" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

- [ ] **Step 2: Rebind the implementation session and capture the complete
  behavior-specific RED matrix.**

  The implementation agent begins with this self-contained prerequisite:

```bash
design_base="$(git rev-parse 7b792a37)"
test "$(git log --format=%H \
  --grep='^docs(plan): define session-local option proof$' |
  wc -l)" -eq 1
plan_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(plan): define session-local option proof$')"
test "$(git log --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$')"
test "$(git rev-parse HEAD)" = "$implementation_base"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
test "$(git rev-list --count \
  "$design_base..$plan_checkpoint")" -eq 1
test "$(git rev-list --count \
  "$plan_checkpoint..$implementation_base")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$implementation_base" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test "$(git ls-tree "$implementation_base" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$implementation_base" \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test "$(git diff --name-only \
  "$design_base..$implementation_base" | sort)" = "$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Add every 4W minimum matrix case to
  `test_repository_umbrella_is_wiring_only`, plus these named GNU `env`
  transitions:

- dispatch-positive `env -- NAME=VALUE python3 <sibling>`;
- dispatch-positive `env -- A=1 B=2 python3 <sibling>`;
- non-dispatch `env -- NAME=<sibling>` with no command;
- dispatch-positive `env -- NAME=<sibling> python3 <sibling>`, proving that
    assignment occurrence is ignored while the command sink is detected; and
- non-dispatch `env -- -command <sibling>` using a controlled static
    fixture, proving that `-command` is the command position rather than an
    unknown option and that its sibling argument is not itself dispatched.

  The first focused run must fail on at least one new behavior-specific
  assertion while importing and reaching the named test. Record the exact RED
  counts and representative corrected-semantics assertion in the Task ledger:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
  -v
```

- [ ] **Step 3: Implement the bounded pure parser and run focused GREEN.**

  Change only the narrow static oracle in the allowed test file. Preserve all
  incorporated 4W wrapper families, option arities, GNU split-string rules,
  deterministic no-credit work budget, fail-closed outcomes, and value-free
  diagnostics. Run:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 -m unittest \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
```

- [ ] **Step 4: Run the frozen regression and static evidence ladder.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
python3 scripts/validation/run-ci-gate.py --profile ci --list
python3 scripts/validation/run-ci-gate.py --profile ci --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-script-backed --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles --dry-run --all
python3 -m ruff check \
  tests/validation/test_agent_governance_ci_routing.py
python3 -m compileall -q \
  tests/validation/test_agent_governance_ci_routing.py
git diff --check
```

  Ruff absence remains `unverified`; do not install dependencies. The
  repository umbrella, registered typed child gates, direct pre-commit,
  controlled wrapper, Compose/runtime, network, secrets, credentials, remote
  state, and Graphify update remain prohibited. The listed standalone static
  validators and execution-free `--list`/`--dry-run` projections are the only
  authorized child-gate evidence.

- [ ] **Step 5: Re-resolve the implementation base, prove exact scope and
  freezes, then commit the sole attempt.**

```bash
test "$(git log --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$')"
test "$(git rev-parse HEAD)" = "$implementation_base"
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" --
    git diff --cached --name-only
    git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_paths"
git diff --exit-code "$implementation_base" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test "$(git ls-files -s \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test "$(git ls-files -s \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
git diff --check
git add \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = "$expected_paths"
git commit -m "fix(ci): close session-local wrapper proof"
test "$(git log --format=%H \
  --grep='^fix(ci): close session-local wrapper proof$' |
  wc -l)" -eq 1
implementation_commit="$(git log -1 --format=%H \
  --grep='^fix(ci): close session-local wrapper proof$')"
test "$(git rev-parse HEAD)" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
test "$(git rev-list --count \
  "$implementation_base..$implementation_commit")" -eq 1
test "$(git diff --name-only \
  "$implementation_base..$implementation_commit" | sort)" = \
  "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test "$(git ls-tree "$implementation_commit" \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$implementation_commit" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

- [ ] **Step 6: Re-resolve the exact review range in each review session and
  record the accepted pair separately.**

  Each reviewer independently runs this complete range proof before reading
  the implementation:

```bash
test "$(git log --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$')"
test "$(git log --format=%H \
  --grep='^fix(ci): close session-local wrapper proof$' |
  wc -l)" -eq 1
implementation_commit="$(git log -1 --format=%H \
  --grep='^fix(ci): close session-local wrapper proof$')"
test "$(git rev-parse HEAD)" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
test "$(git rev-list --count \
  "$implementation_base..$implementation_commit")" -eq 1
test "$(git diff --name-only \
  "$implementation_base..$implementation_commit" | sort)" = "$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test "$(git ls-tree "$implementation_commit" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$implementation_commit" \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  After both reviewers return `C0/I0/M0`, the controller edits only the Task
  ledger and runs this separate self-contained evidence proof:

```bash
test "$(git log --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record session-local proof plan reviews$')"
test "$(git log --format=%H \
  --grep='^fix(ci): close session-local wrapper proof$' |
  wc -l)" -eq 1
implementation_commit="$(git log -1 --format=%H \
  --grep='^fix(ci): close session-local wrapper proof$')"
test "$(git rev-parse HEAD)" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
test "$(git rev-list --count \
  "$implementation_base..$implementation_commit")" -eq 1
actual_paths="$(
  {
    git diff --name-only
    git diff --cached --name-only
    git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record session-local wrapper review"
test "$(git log --format=%H \
  --grep='^docs(task): record session-local wrapper review$' |
  wc -l)" -eq 1
review_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(task): record session-local wrapper review$')"
test "$(git rev-parse HEAD)" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
test "$(git rev-list --count \
  "$implementation_commit..$review_checkpoint")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$review_checkpoint" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test "$(git ls-tree "$review_checkpoint" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Only this accepted review checkpoint authorizes Task 4.5 Wave C.

#### Task 4.4Y / T-TSDC-004R-4Y: Fail-Fast Lineage-Proof Design Return

> **Superseded for execution by Task 4.4Z.** Retain this section as failed
> design evidence only. Do not execute any 4Y command block or create any 4Y
> pending commit subject.

**Authority boundary and supersession:**

- The exact unique `docs(task): record exhausted session-local plan review`
  commit must resolve to `481b1a8e`, be `HEAD` when this design is authored,
  and remain an ancestor of every 4Y checkpoint.
- This Plan-only successor may modify only this Plan and the sibling Task
  ledger. Its exact unique subject is
  `docs(plan): define fail-fast lineage proof`.
- Two fresh read-only reviewers inspect the complete
  `481b1a8e..$plan_checkpoint` range: one specification reviewer and a
  different quality/security reviewer. Both must return `C0/I0/M0`. Any other
  result returns to design; there is no Plan correction inside 4Y.
- After both approvals, the controller records the reports and exact range in
  a Task-ledger-only commit with the exact unique subject
  `docs(task): record fail-fast lineage plan reviews`. That clean commit is
  the immutable implementation base.
- One implementation agent then receives exactly one attempt. It may modify
  only `tests/validation/test_agent_governance_ci_routing.py` and the sibling
  Task ledger. Its exact unique subject is
  `fix(ci): close fail-fast wrapper proof`.
- Freeze `.github/workflow-contract.yml`,
  `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, every typed gate runner and
  adapter, every target-delta artifact, and every other tracked path.
- A fresh read-only specification reviewer and a different fresh read-only
  quality/security reviewer inspect the exact implementation-base-to-commit
  range. Both must return `C0/I0/M0`. The controller then records the reports
  in a Task-ledger-only commit with the exact unique subject
  `docs(task): record fail-fast wrapper review`.
- Any non-`C0/I0/M0` implementation review exhausts 4Y without a retry and
  keeps Task 4R, Wave C, Tasks 5–6, and final branch review blocked.
- 4Y incorporates the complete 4W parser grammar, RED matrix, deterministic
  no-credit work budget, focused GREEN, frozen regression ladder, value-free
  diagnostics, and prohibition boundaries. It also incorporates the corrected
  4X GNU `env --` assignment-selection contract and the requirement that every
  session resolve its own checkpoint variables. All 4W and 4X command blocks
  and uncreated pending subjects are non-executable historical text.

**Strict independent-session contract:**

- Every 4Y fenced Bash block is one independent invocation. It begins with
  `set -euo pipefail` and `shopt -s inherit_errexit`; an earlier failed test,
  Git command, pipeline element, or command substitution must terminate the
  block before any later stage or commit command.
- Expected RED is the sole nonzero exception. Its block temporarily disables
  `errexit` only around the named focused test, captures the exit status and
  output, immediately restores `errexit`, and requires both nonzero status and
  the fixed behavior-specific assertion marker
  `GNU env -- assignment scan must reach command`.
- Every compound command substitution joins fallible commands with `&&` and
  runs under `pipefail` plus inherited `errexit`. No proof depends on a final
  clean-state command to expose an earlier failure.
- Every block resolves every commit variable it reads inside that same block
  from an exact unique subject or the immutable `481b1a8e` literal. No block
  inherits shell state from another agent, controller, or reviewer.
- Every authority transition proves exact subject uniqueness, ancestry,
  direct commit count, exact commit/range paths, relevant `100644` modes, and
  tracked plus untracked cleanliness or the exact allowed dirty paths.
- Task 4.5 independently re-resolves and proves the complete
  design-base -> Plan -> Plan-review evidence -> implementation ->
  implementation-review chain. It rechecks the Plan two-path scope, both
  Task-only evidence scopes, the implementation two-path scope, all relevant
  modes, `HEAD`, and clean state before Wave C receives authority.

- [ ] **Step 1: Commit and independently review the 4Y Plan.**

  Immediately after the Plan commit and before either review, the controller
  runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 481b1a8e)"
test "$(git log --format=%H \
  --grep='^docs(task): record exhausted session-local plan review$' |
  wc -l)" -eq 1
test "$(git log -1 --format=%H \
  --grep='^docs(task): record exhausted session-local plan review$')" = \
  "$design_base"
test "$(git log --format=%H \
  --grep='^docs(plan): define fail-fast lineage proof$' |
  wc -l)" -eq 1
plan_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(plan): define fail-fast lineage proof$')"
test "$(git rev-parse HEAD)" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
test "$(git rev-list --count \
  "$design_base..$plan_checkpoint")" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test "$(git diff-tree --no-commit-id --name-only -r \
  "$plan_checkpoint" | sort)" = "$expected_plan_paths"
test "$(git ls-tree "$plan_checkpoint" \
  docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$plan_checkpoint" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  After both Plan reviewers return `C0/I0/M0`, edit only the Task ledger and
  run this separate strict session:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 481b1a8e)"
test "$(git log --format=%H \
  --grep='^docs(plan): define fail-fast lineage proof$' |
  wc -l)" -eq 1
plan_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(plan): define fail-fast lineage proof$')"
test "$(git rev-parse HEAD)" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
test "$(git rev-list --count \
  "$design_base..$plan_checkpoint")" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record fail-fast lineage plan reviews"
test "$(git log --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$')"
test "$(git rev-parse HEAD)" = "$implementation_base"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
test "$(git rev-list --count \
  "$plan_checkpoint..$implementation_base")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$implementation_base" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test "$(git ls-tree "$implementation_base" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

- [ ] **Step 2: Rebind the implementation session and capture the complete
  behavior-specific RED matrix.**

  The implementation agent begins with this strict prerequisite:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 481b1a8e)"
test "$(git log --format=%H \
  --grep='^docs(plan): define fail-fast lineage proof$' |
  wc -l)" -eq 1
plan_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(plan): define fail-fast lineage proof$')"
test "$(git log --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$')"
test "$(git rev-parse HEAD)" = "$implementation_base"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
test "$(git rev-list --count \
  "$design_base..$plan_checkpoint")" -eq 1
test "$(git rev-list --count \
  "$plan_checkpoint..$implementation_base")" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test "$(git diff-tree --no-commit-id --name-only -r \
  "$plan_checkpoint" | sort)" = "$expected_plan_paths"
test "$(git diff-tree --no-commit-id --name-only -r \
  "$implementation_base" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test "$(git ls-tree "$implementation_base" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$implementation_base" \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Add the complete 4W RED matrix and every 4X GNU `env --` transition to
  `test_repository_umbrella_is_wiring_only`. The
  `env -- NAME=VALUE python3 <sibling>` assertion must use the fixed message
  `GNU env -- assignment scan must reach command`. Use two distinct registered
  siblings in the assignment-plus-command case so its expected set proves
  that an assignment occurrence is ignored while the command occurrence is
  detected.

  Run the focused RED through this strict exception boundary:

```bash
set -euo pipefail
shopt -s inherit_errexit
set +e
red_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
    -v 2>&1
)"
red_status="$?"
set -e
printf '%s\n' "$red_output"
test "$red_status" -ne 0
case "$red_output" in
  *"GNU env -- assignment scan must reach command"*) ;;
  *) exit 1 ;;
esac
```

  Record the exact RED status, counts, and fixed assertion marker in the Task
  ledger. Import errors, missing tests, unrelated failures, or another marker
  do not count as RED.

- [ ] **Step 3: Implement the bounded pure parser and run focused GREEN.**

  Change only the narrow static oracle in the allowed test file. Preserve all
  incorporated wrapper families, option arities, GNU split-string rules,
  corrected post-`--` assignment phase, deterministic no-credit work budget,
  fail-closed outcomes, and value-free diagnostics.

```bash
set -euo pipefail
shopt -s inherit_errexit
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 -m unittest \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
```

- [ ] **Step 4: Run the frozen regression and static evidence ladder.**

```bash
set -euo pipefail
shopt -s inherit_errexit
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
python3 scripts/validation/run-ci-gate.py --profile ci --list
python3 scripts/validation/run-ci-gate.py --profile ci --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-script-backed --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles --dry-run --all
if python3 -c 'import ruff' >/dev/null 2>&1; then
  python3 -m ruff check \
    tests/validation/test_agent_governance_ci_routing.py
else
  printf '%s\n' 'UNVERIFIED: Ruff is unavailable; installation prohibited'
fi
python3 -m compileall -q \
  tests/validation/test_agent_governance_ci_routing.py
git diff --check
```

  The repository umbrella, registered typed child gates, direct pre-commit,
  controlled wrapper, Compose/runtime, network, secrets, credentials, remote
  state, and Graphify update remain prohibited. The listed standalone static
  validators and execution-free `--list`/`--dry-run` projections are the only
  authorized child-gate evidence.

- [ ] **Step 5: Re-resolve the implementation base, prove exact scope and
  freezes, then commit the sole attempt.**

```bash
set -euo pipefail
shopt -s inherit_errexit
test "$(git log --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$')"
test "$(git rev-parse HEAD)" = "$implementation_base"
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" -- &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_paths"
git diff --exit-code "$implementation_base" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test "$(git ls-files -s \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test "$(git ls-files -s \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
git diff --check
git add \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = "$expected_paths"
git commit -m "fix(ci): close fail-fast wrapper proof"
test "$(git log --format=%H \
  --grep='^fix(ci): close fail-fast wrapper proof$' |
  wc -l)" -eq 1
implementation_commit="$(git log -1 --format=%H \
  --grep='^fix(ci): close fail-fast wrapper proof$')"
test "$(git rev-parse HEAD)" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
test "$(git rev-list --count \
  "$implementation_base..$implementation_commit")" -eq 1
test "$(git diff --name-only \
  "$implementation_base..$implementation_commit" | sort)" = \
  "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test "$(git ls-tree "$implementation_commit" \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$implementation_commit" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

- [ ] **Step 6: Re-resolve the exact review range in each review session and
  record the accepted pair separately.**

  Each reviewer independently runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
test "$(git log --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$')"
test "$(git log --format=%H \
  --grep='^fix(ci): close fail-fast wrapper proof$' |
  wc -l)" -eq 1
implementation_commit="$(git log -1 --format=%H \
  --grep='^fix(ci): close fail-fast wrapper proof$')"
test "$(git rev-parse HEAD)" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
test "$(git rev-list --count \
  "$implementation_base..$implementation_commit")" -eq 1
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test "$(git diff --name-only \
  "$implementation_base..$implementation_commit" | sort)" = \
  "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test "$(git ls-tree "$implementation_commit" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test "$(git ls-tree "$implementation_commit" \
  tests/validation/test_agent_governance_ci_routing.py |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  After both reviewers return `C0/I0/M0`, the controller edits only the Task
  ledger and runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
test "$(git log --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$' |
  wc -l)" -eq 1
implementation_base="$(git log -1 --format=%H \
  --grep='^docs(task): record fail-fast lineage plan reviews$')"
test "$(git log --format=%H \
  --grep='^fix(ci): close fail-fast wrapper proof$' |
  wc -l)" -eq 1
implementation_commit="$(git log -1 --format=%H \
  --grep='^fix(ci): close fail-fast wrapper proof$')"
test "$(git rev-parse HEAD)" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
test "$(git rev-list --count \
  "$implementation_base..$implementation_commit")" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
test "$(git diff --cached --name-only | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record fail-fast wrapper review"
test "$(git log --format=%H \
  --grep='^docs(task): record fail-fast wrapper review$' |
  wc -l)" -eq 1
review_checkpoint="$(git log -1 --format=%H \
  --grep='^docs(task): record fail-fast wrapper review$')"
test "$(git rev-parse HEAD)" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
test "$(git rev-list --count \
  "$implementation_commit..$review_checkpoint")" -eq 1
test "$(git diff-tree --no-commit-id --name-only -r \
  "$review_checkpoint" | sort)" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
test "$(git ls-tree "$review_checkpoint" \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
  awk '{print $1}')" = "100644"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

  Only this accepted review checkpoint authorizes Task 4.5 Wave C.

#### Task 4.4Z / T-TSDC-004R-4Z: Status-Preserving Proof Design Return

> **Superseded for execution by Task 4.4AA.** Retain this section as failed
> design evidence only. Do not execute any 4Z command block or create any 4Z
> pending commit subject.

**Authority boundary and supersession:**

- The exact unique `docs(task): record exhausted fail-fast plan review` commit
  must resolve to `0177006c`, be `HEAD` when this design is authored, and
  remain an ancestor of every 4Z checkpoint.
- This Plan-only successor may modify only this Plan and the sibling Task
  ledger. Its exact unique subject is
  `docs(plan): define status-preserving proof`.
- Two fresh read-only reviewers inspect the complete
  `0177006c..$plan_checkpoint` range: one specification reviewer and a
  different quality/security reviewer. Both must return `C0/I0/M0`. Any other
  result returns to design; there is no Plan correction inside 4Z.
- After both approvals, the controller records the reports and exact range in
  a Task-ledger-only commit with the exact unique subject
  `docs(task): record status-preserving plan reviews`. That clean commit is
  the immutable implementation base.
- One implementation agent then receives exactly one attempt. It may modify
  only `tests/validation/test_agent_governance_ci_routing.py` and the sibling
  Task ledger. Its exact unique subject is
  `fix(ci): close status-preserving wrapper proof`.
- Freeze `.github/workflow-contract.yml`,
  `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, every typed gate runner and
  adapter, every target-delta artifact, and every other tracked path.
- A fresh read-only specification reviewer and a different fresh read-only
  quality/security reviewer inspect the exact implementation-base-to-commit
  range. Both must return `C0/I0/M0`. The controller then records the reports
  in a Task-ledger-only commit with the exact unique subject
  `docs(task): record status-preserving wrapper review`.
- Any non-`C0/I0/M0` implementation review exhausts 4Z without a retry and
  keeps Task 4R, Wave C, Tasks 5–6, and final branch review blocked.
- 4Z incorporates every accepted 4W parser/matrix/budget/evidence requirement,
  the corrected 4X GNU `env --` and session-local contract, and the 4Y strict
  session, bounded RED, full lineage/scope/mode proof, freezes, and
  prohibitions. All earlier command blocks and pending subjects are
  non-executable historical text.

**Status-preserving substitution contract:**

- Every 4Z fenced Bash block begins with `set -euo pipefail` and
  `shopt -s inherit_errexit`.
- Every fallible command substitution is the complete right-hand side of a
  standalone simple assignment. The next command tests the captured value.
  No `test`, `if`, `case`, comparison, function argument, or later compound
  command embeds `$()`.
- Because a standalone assignment returns the substitution status, a failed
  Git command or pipeline terminates the strict block before any value test or
  commit. `pipefail` preserves failure from non-final pipeline elements.
- The expected focused RED remains the sole exception: `errexit` is disabled
  only for its standalone output assignment, the status is captured
  immediately, and `errexit` is restored before output or assertions.
- A static extraction audit must prove that every `$()` opener in executable
  4Z and Task 4.5 Bash is on a line matching a simple assignment and that no
  direct `test "$(` or equivalent consumer exists. Bash syntax, strict first
  two lines, exact path scope, metadata, traceability, and diff hygiene remain
  mandatory before the Plan commit.

- [ ] **Step 1: Commit and independently review the 4Z Plan.**

  Immediately after the Plan commit and before either review, the controller
  runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 0177006c)"
failure_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted fail-fast plan review$' |
    wc -l
)"
test "$failure_subject_count" -eq 1
failure_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted fail-fast plan review$'
)"
test "$failure_checkpoint" = "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define status-preserving proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define status-preserving proof$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
task_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  After both Plan reviewers return `C0/I0/M0`, edit only the Task ledger and
  run this separate strict session:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 0177006c)"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define status-preserving proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define status-preserving proof$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record status-preserving plan reviews"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 2: Rebind the implementation session and capture the complete
  behavior-specific RED matrix.**

  The implementation agent begins with this strict prerequisite:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 0177006c)"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define status-preserving proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define status-preserving proof$'
)"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
base_test_mode="$(
  git ls-tree "$implementation_base" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$base_test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  Add the complete 4W RED matrix and every 4X GNU `env --` transition to
  `test_repository_umbrella_is_wiring_only`. The
  `env -- NAME=VALUE python3 <sibling>` assertion must use the fixed message
  `GNU env -- assignment scan must reach command`. Use two distinct registered
  siblings in the assignment-plus-command case so its expected set proves
  that an assignment occurrence is ignored while the command occurrence is
  detected.

```bash
set -euo pipefail
shopt -s inherit_errexit
set +e
red_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
    -v 2>&1
)"
red_status="$?"
set -e
printf '%s\n' "$red_output"
test "$red_status" -ne 0
case "$red_output" in
  *"GNU env -- assignment scan must reach command"*) ;;
  *) exit 1 ;;
esac
```

  Record the exact RED status, counts, and fixed assertion marker in the Task
  ledger. Import errors, missing tests, unrelated failures, or another marker
  do not count as RED.

- [ ] **Step 3: Implement the bounded pure parser and run focused GREEN.**

  Change only the narrow static oracle in the allowed test file. Preserve all
  incorporated wrapper families, option arities, GNU split-string rules,
  corrected post-`--` assignment phase, deterministic no-credit work budget,
  fail-closed outcomes, and value-free diagnostics.

```bash
set -euo pipefail
shopt -s inherit_errexit
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 -m unittest \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
```

- [ ] **Step 4: Run the frozen regression and static evidence ladder.**

```bash
set -euo pipefail
shopt -s inherit_errexit
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
python3 scripts/validation/run-ci-gate.py --profile ci --list
python3 scripts/validation/run-ci-gate.py --profile ci --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-script-backed --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles --dry-run --all
if python3 -c 'import ruff' >/dev/null 2>&1; then
  python3 -m ruff check \
    tests/validation/test_agent_governance_ci_routing.py
else
  printf '%s\n' 'UNVERIFIED: Ruff is unavailable; installation prohibited'
fi
python3 -m compileall -q \
  tests/validation/test_agent_governance_ci_routing.py
git diff --check
```

  The repository umbrella, registered typed child gates, direct pre-commit,
  controlled wrapper, Compose/runtime, network, secrets, credentials, remote
  state, and Graphify update remain prohibited. The listed standalone static
  validators and execution-free `--list`/`--dry-run` projections are the only
  authorized child-gate evidence.

- [ ] **Step 5: Re-resolve the implementation base, prove exact scope and
  freezes, then commit the sole attempt.**

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" -- &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_paths"
git diff --exit-code "$implementation_base" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_mode="$(
  git ls-files -s \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
task_mode="$(
  git ls-files -s \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
git diff --check
git add \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$expected_paths"
git commit -m "fix(ci): close status-preserving wrapper proof"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close status-preserving wrapper proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close status-preserving wrapper proof$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
committed_test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$committed_test_mode" = "100644"
committed_task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$committed_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 6: Re-resolve the exact review range in each review session and
  record the accepted pair separately.**

  Each reviewer independently runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$'
)"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close status-preserving wrapper proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close status-preserving wrapper proof$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  After both reviewers return `C0/I0/M0`, the controller edits only the Task
  ledger and runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record status-preserving plan reviews$'
)"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close status-preserving wrapper proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close status-preserving wrapper proof$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record status-preserving wrapper review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record status-preserving wrapper review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record status-preserving wrapper review$'
)"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$implementation_commit..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  Only this accepted review checkpoint authorizes Task 4.5 Wave C.

#### Task 4.4AA / T-TSDC-004R-4AA: Immediate-Consumption Proof Design Return

> **Superseded for execution by Task 4.4AB.** Retain this section and its
> rejected implementation as historical evidence only. Do not execute a 4AA
> command block or create its uncreated accepted-review subject.

**Authority boundary and supersession:**

- The exact unique
  `docs(task): record exhausted status-preserving plan review` commit must
  resolve to `355a1db5`, be `HEAD` when this design is authored, and remain an
  ancestor of every 4AA checkpoint.
- This Plan-only successor may modify only this Plan and the sibling Task
  ledger. Its exact unique subject is
  `docs(plan): define immediate-consumption proof`.
- Two fresh read-only reviewers inspect the complete
  `355a1db5..$plan_checkpoint` range: one specification reviewer and a
  different quality/security reviewer. Both must return `C0/I0/M0`. Any other
  result returns to design; there is no Plan correction inside 4AA.
- After both approvals, the controller records the reports and exact range in
  a Task-ledger-only commit with the exact unique subject
  `docs(task): record immediate-consumption plan reviews`. That clean commit
  is the immutable implementation base.
- One implementation agent then receives exactly one attempt. It may modify
  only `tests/validation/test_agent_governance_ci_routing.py` and the sibling
  Task ledger. Its exact unique subject is
  `fix(ci): close immediate-consumption wrapper proof`.
- Freeze `.github/workflow-contract.yml`,
  `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, every typed gate runner and
  adapter, every target-delta artifact, and every other tracked path.
- A fresh read-only specification reviewer and a different fresh read-only
  quality/security reviewer inspect the exact implementation-base-to-commit
  range. Both must return `C0/I0/M0`. The controller then records the reports
  in a Task-ledger-only commit with the exact unique subject
  `docs(task): record immediate-consumption wrapper review`.
- Any non-`C0/I0/M0` implementation review exhausts 4AA without a retry and
  keeps Task 4R, Wave C, Tasks 5–6, and final branch review blocked.
- 4AA incorporates every accepted 4W parser/matrix/budget/evidence
  requirement, the corrected 4X GNU `env --` and session-local contract, the
  4Y strict/full-lineage contract, and the 4Z standalone status-preserving
  capture, freezes, and prohibitions. All earlier command blocks and pending
  subjects are non-executable historical text.

**Immediate capture/test contract:**

- Every 4AA fenced Bash block begins with `set -euo pipefail` and
  `shopt -s inherit_errexit`.
- Every non-RED `$()` is the complete right-hand side of a standalone simple
  assignment. The immediately following command must be a `test` that names
  that exact captured variable.
- When a full semantic assertion is not yet available, the immediate test is
  `test -n "$variable"`. A later equality, scope, ancestry, or mode check may
  strengthen it but never replaces the adjacent consumption.
- Count, distance, scope, mode, and clean-state captures use their full
  semantic assertion as the immediate next command.
- The expected focused RED is the sole exception. Its `red_output` assignment
  is immediately followed by `red_status="$?"`, then `errexit` is restored
  before output and assertions.
- A static extraction audit must parse assignment boundaries and verify every
  non-RED capture is followed by a `test` containing the same variable. It
  must verify the sole `red_output -> red_status` exception, strict first two
  lines, Bash syntax, exact two-path scope, metadata, traceability, and diff
  hygiene before the Plan commit.

- [ ] **Step 1: Commit and independently review the 4AA Plan.**

  Immediately after the Plan commit and before either review, the controller
  runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 355a1db5)"
test -n "$design_base"
failure_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted status-preserving plan review$' |
    wc -l
)"
test "$failure_subject_count" -eq 1
failure_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted status-preserving plan review$'
)"
test "$failure_checkpoint" = "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define immediate-consumption proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define immediate-consumption proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
task_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  After both Plan reviewers return `C0/I0/M0`, edit only the Task ledger and
  run this separate strict session:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 355a1db5)"
test -n "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define immediate-consumption proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define immediate-consumption proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record immediate-consumption plan reviews"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 2: Rebind the implementation session and capture the complete
  behavior-specific RED matrix.**

  The implementation agent begins with this strict prerequisite:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 355a1db5)"
test -n "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define immediate-consumption proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define immediate-consumption proof$'
)"
test -n "$plan_checkpoint"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
base_test_mode="$(
  git ls-tree "$implementation_base" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$base_test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  Add the complete 4W RED matrix and every 4X GNU `env --` transition to
  `test_repository_umbrella_is_wiring_only`. The
  `env -- NAME=VALUE python3 <sibling>` assertion must use the fixed message
  `GNU env -- assignment scan must reach command`. Use two distinct registered
  siblings in the assignment-plus-command case so its expected set proves
  that an assignment occurrence is ignored while the command occurrence is
  detected.

```bash
set -euo pipefail
shopt -s inherit_errexit
set +e
red_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
    -v 2>&1
)"
red_status="$?"
set -e
printf '%s\n' "$red_output"
test "$red_status" -ne 0
case "$red_output" in
  *"GNU env -- assignment scan must reach command"*) ;;
  *) exit 1 ;;
esac
```

  Record the exact RED status, counts, and fixed assertion marker in the Task
  ledger. Import errors, missing tests, unrelated failures, or another marker
  do not count as RED.

- [ ] **Step 3: Implement the bounded pure parser and run focused GREEN.**

  Change only the narrow static oracle in the allowed test file. Preserve all
  incorporated wrapper families, option arities, GNU split-string rules,
  corrected post-`--` assignment phase, deterministic no-credit work budget,
  fail-closed outcomes, and value-free diagnostics.

```bash
set -euo pipefail
shopt -s inherit_errexit
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 -m unittest \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
```

- [ ] **Step 4: Run the frozen regression and static evidence ladder.**

```bash
set -euo pipefail
shopt -s inherit_errexit
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
python3 scripts/validation/run-ci-gate.py --profile ci --list
python3 scripts/validation/run-ci-gate.py --profile ci --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-script-backed --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles --dry-run --all
if python3 -c 'import ruff' >/dev/null 2>&1; then
  python3 -m ruff check \
    tests/validation/test_agent_governance_ci_routing.py
else
  printf '%s\n' 'UNVERIFIED: Ruff is unavailable; installation prohibited'
fi
python3 -m compileall -q \
  tests/validation/test_agent_governance_ci_routing.py
git diff --check
```

  The repository umbrella, registered typed child gates, direct pre-commit,
  controlled wrapper, Compose/runtime, network, secrets, credentials, remote
  state, and Graphify update remain prohibited. The listed standalone static
  validators and execution-free `--list`/`--dry-run` projections are the only
  authorized child-gate evidence.

- [ ] **Step 5: Re-resolve the implementation base, prove exact scope and
  freezes, then commit the sole attempt.**

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test -n "$expected_paths"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" -- &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_paths"
git diff --exit-code "$implementation_base" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_mode="$(
  git ls-files -s \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
task_mode="$(
  git ls-files -s \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
git diff --check
git add \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$expected_paths"
git commit -m "fix(ci): close immediate-consumption wrapper proof"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close immediate-consumption wrapper proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close immediate-consumption wrapper proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
committed_test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$committed_test_mode" = "100644"
committed_task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$committed_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 6: Re-resolve the exact review range in each review session and
  record the accepted pair separately.**

  Each reviewer independently runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$'
)"
test -n "$implementation_base"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close immediate-consumption wrapper proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close immediate-consumption wrapper proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test -n "$expected_paths"
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  After both reviewers return `C0/I0/M0`, the controller edits only the Task
  ledger and runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record immediate-consumption plan reviews$'
)"
test -n "$implementation_base"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close immediate-consumption wrapper proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close immediate-consumption wrapper proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record immediate-consumption wrapper review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record immediate-consumption wrapper review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record immediate-consumption wrapper review$'
)"
test -n "$review_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$implementation_commit..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  Only this accepted review checkpoint authorizes Task 4.5 Wave C.

#### Task 4.4AB / T-TSDC-004R-4AB: Explicit Parser-Outcome Proof Design Return

> **Superseded for execution by Task 4.4AC.** Retain this section as failed
> Plan-review evidence only. Do not execute a 4AB command block or create an
> uncreated 4AB implementation subject.

**Authority boundary and supersession:**

- The exact unique
  `docs(task): record exhausted immediate-consumption wrapper review` commit
  must resolve to
  `25524ce1af36ee8572b9e0c855700680db957921`, be `HEAD` when this
  design is authored, and remain an ancestor of every 4AB checkpoint.
- This Plan-only successor may modify only this Plan and the sibling Task
  ledger. Its exact unique subject is
  `docs(plan): define explicit parser outcome proof`.
- Two fresh read-only reviewers inspect the complete
  `25524ce1..$plan_checkpoint` range: one specification reviewer and a
  different quality/security reviewer. Both must return `C0/I0/M0`. Any other
  result is recorded in the exact Task-only
  `docs(task): record exhausted explicit parser outcome plan review`
  checkpoint and returns to design; there is no Plan correction inside 4AB.
- After both approvals, the controller records the reports and exact range in
  a Task-ledger-only commit with the exact unique subject
  `docs(task): record explicit parser outcome plan reviews`. That clean commit
  is the immutable implementation base.
- One fresh implementation agent then receives exactly one attempt. It may
  modify only
  `tests/validation/test_agent_governance_ci_routing.py` and the sibling Task
  ledger. Its exact unique subject is
  `fix(ci): close explicit parser outcome proof`.
- Freeze `.github/workflow-contract.yml`,
  `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, every typed gate contract,
  runner, adapter, and test outside the allowed routing test, every
  target-delta artifact, and every other tracked path.
- A fresh read-only specification reviewer and a different fresh read-only
  quality/security reviewer inspect the exact implementation-base-to-commit
  range. Both must return `C0/I0/M0`. The controller then records the accepted
  pair in a Task-ledger-only commit with the exact unique subject
  `docs(task): record explicit parser outcome review`.
- Any non-`C0/I0/M0` implementation review exhausts 4AB without retry. The
  controller records the rejected pair in a Task-ledger-only commit with the
  exact unique subject
  `docs(task): record exhausted explicit parser outcome review`; Task 4R,
  Wave C, Tasks 5–6, and final branch review remain blocked.
- 4AB supersedes 4AA for execution and incorporates every accepted 4W parser,
  matrix, budget, and evidence requirement; the corrected 4X GNU `env --` and
  session-local contract; the 4Y strict/full-lineage contract; the 4Z
  status-preserving contract; and the 4AA immediate capture/test contract.
  Every earlier command block and uncreated subject is historical and
  non-executable.

**Files and interfaces:**

- Modify
  `tests/validation/test_agent_governance_ci_routing.py` only inside
  `test_repository_umbrella_is_wiring_only` and its existing
  `_registered_sibling_dispatches` static oracle.
- Modify
  `docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md`
  only for bounded RED, GREEN, validation, commit, and review evidence.
- Do not create a parser module, helper script, workflow, contract field,
  generated artifact, dependency, or production runtime surface.
- Inside `command_sink`, the recursive parser consumes and produces one local
  `ParseResult = tuple[str, frozenset[str]]`. The tag is exactly one of
  `dispatch`, `no-dispatch`, or `ambiguous`. `dispatch` contains only
  statically proven registered sibling sinks; `no-dispatch` contains no paths;
  and `ambiguous` contains the exact relevant registered siblings when they
  are recoverable, otherwise the complete registered sibling set.
- Convert a `ParseResult` to the existing public `set[str]` only once at the
  outer `command_sink` boundary: materialize both `dispatch` and `ambiguous`
  paths as findings and materialize `no-dispatch` as the empty set. Existing
  callers, messages, and value-free diagnostics remain unchanged.

**Explicit outcome and parser contract:**

- `parse_chain`, `parse_command`, `parse_exec`, and `parse_env` return
  `ParseResult`; they never use an empty set to represent both a proved
  no-dispatch path and unresolved syntax.
- A literal registered command head is `dispatch`. A proved static
  non-sibling head is `no-dispatch`. An unresolved dynamic command head such
  as `$RUNNER` or `${RUNNER}` is `ambiguous` when any remaining token resolves
  to or contains a registered sibling. `command -v` and `command -V`, including
  valid clusters, are always `no-dispatch` before command-head evaluation.
- The original work budget remains exactly
  `8 * (1 + original token count + total source-token character count)`.
  Every wrapper/option token and every GNU split-string character charges that
  one closure-owned budget. Recursive parsing and inserted tokens never reset
  or add credit. Budget exhaustion is `ambiguous`.
- Follow the
  [Coreutils 9.11 `env` grammar](https://www.gnu.org/software/coreutils/manual/html_node/env-invocation.html)
  and keep the existing static lexer. For separated `-S STRING` and
  `--split-string STRING`, lex the operand and combine the resulting tokens
  with the untouched tail after the operand. For attached `-SSTRING`,
  `--split-string=STRING`, and clustered forms such as `-vSSTRING`, combine
  the split tokens with the untouched tail after the option token. Return
  immediately into the same `parse_env` function at the first combined token;
  do not perform the old unconditional index increment. An empty split result
  continues with the untouched tail. Malformed, unsupported, dynamic, or
  budget-exhausted split strings are `ambiguous`.
- Preserve the documented static `env -S` quotes, whitespace, comment,
  `\c`, `\f`, `\n`, `\r`, `\t`, `\v`, `\#`, `\$`, `\_`, `\"`, `\'`, and
  `\\` behavior. Do not read `os.environ`, invoke a shell, expand a variable,
  execute a wrapper, or execute any sibling entrypoint.
- Recognize signal options only when the token equals
  `--block-signal`, `--default-signal`, or `--ignore-signal`, or begins with
  that exact name followed immediately by `=`. A token that merely starts
  with one of those names, including `--block-signalX=...`,
  `--default-signalX=...`, or `--ignore-signalX=...`, is `ambiguous`.
  Preserve valid exact bare and exact-equals forms.
- Preserve the accepted Bash
  [`command`](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html)
  and
  [`exec`](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
  option arities, GNU `env --` assignment transition, option-operand
  no-dispatch behavior, nested wrapper recursion, deterministic value-free
  fallback, and all literal, quoted, variable-mediated, helper, Python
  heredoc `subprocess`, and `os.system` dispatch families.

**Strict proof contract:**

- Every 4AB fenced Bash block begins with `set -euo pipefail` and
  `shopt -s inherit_errexit`.
- Every non-RED `$()` is the complete right-hand side of a standalone simple
  assignment. The immediately following command is a `test` naming that exact
  variable. Count, distance, path, mode, and clean-state captures use their
  full semantic assertion as that immediate test.
- The focused RED is the sole exception: `red_output` is immediately followed
  by `red_status="$?"`; `errexit` is restored before output and assertions.
- Before committing this Plan, statically extract every 4AB and Task 4.5
  Step 0 Bash block; require strict first two lines, Bash syntax, adjacent
  capture consumption, the sole RED exception, exact two-path scope, exact
  `100644` modes, metadata, traceability, and diff hygiene.

- [ ] **Step 1: Commit and independently review the 4AB Plan.**

  Immediately after the Plan commit and before either review, the controller
  runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 25524ce1)"
test -n "$design_base"
failure_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted immediate-consumption wrapper review$' |
    wc -l
)"
test "$failure_subject_count" -eq 1
failure_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted immediate-consumption wrapper review$'
)"
test "$failure_checkpoint" = "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
task_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  If either Plan reviewer is not `C0/I0/M0`, edit only the Task ledger and
  terminate 4AB with this exact rejected-Plan checkpoint:

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record exhausted explicit parser outcome plan review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted explicit parser outcome plan review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted explicit parser outcome plan review$'
)"
test -n "$review_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$plan_checkpoint..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  This rejected-Plan checkpoint grants no correction, implementation, or
  downstream authority.

  After both Plan reviewers return `C0/I0/M0`, edit only the Task ledger and
  run this separate strict session:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 25524ce1)"
test -n "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record explicit parser outcome plan reviews"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 2: Rebind the implementation session and add
  fallback-resistant RED cases.**

  The implementation agent first proves the complete authority chain:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 25524ce1)"
test -n "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define explicit parser outcome proof$'
)"
test -n "$plan_checkpoint"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
base_test_mode="$(
  git ls-tree "$implementation_base" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$base_test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  Add these exact behavior families inside
  `test_repository_umbrella_is_wiring_only`. Exact singleton and empty-set
  assertions ensure that neither the all-registered fallback nor
  direct-head misclassification can satisfy RED accidentally:

```python
split_transition_dispatch = {
    "env-split-direct-separated": f"\nenv -S '{sibling}'\n",
    "env-split-direct-attached": f"\nenv -S'{sibling}'\n",
    "env-split-direct-clustered": f"\nenv -vS'{sibling}'\n",
    "env-split-nested-dispatch": (
        f"\nenv -S 'command -p exec -a gate python3 {sibling}'\n"
    ),
}
for family, mutation in split_transition_dispatch.items():
    with self.subTest(family=family):
        self.assertEqual(
            {sibling},
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "explicit parser outcome matrix must hold",
        )

split_transition_no_dispatch = {
    "env-split-query-separated": (
        f"\nenv -S 'command -v python3 {sibling}'\n"
    ),
    "env-split-query-attached": (
        f"\nenv -S'command -v python3 {sibling}'\n"
    ),
    "env-split-query-clustered": (
        f"\nenv -vS'command -v python3 {sibling}'\n"
    ),
}
for family, mutation in split_transition_no_dispatch.items():
    with self.subTest(family=family):
        self.assertEqual(
            set(),
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "explicit parser outcome matrix must hold",
        )

dynamic_head_mutations = {
    "command-dynamic-head": f'\ncommand "$RUNNER" {sibling}\n',
    "direct-dynamic-head": f'\n"$RUNNER" {sibling}\n',
    "python-dynamic-script": f'\npython3 "$SCRIPT" {sibling}\n',
}
for family, mutation in dynamic_head_mutations.items():
    with self.subTest(family=family):
        self.assertEqual(
            {sibling},
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "explicit parser outcome matrix must hold",
        )
self.assertEqual(
    set(),
    self._registered_sibling_dispatches(
        source + f'\ncommand -v "$RUNNER" {sibling}\n',
        sibling_entrypoints,
    ),
    "explicit parser outcome matrix must hold",
)

malformed_signal_options = {
    "env-block-signal-near-prefix": (
        f"\nenv --block-signalX={sibling} true\n"
    ),
    "env-default-signal-near-prefix": (
        f"\nenv --default-signalX={sibling} true\n"
    ),
    "env-ignore-signal-near-prefix": (
        f"\nenv --ignore-signalX={sibling} true\n"
    ),
}
for family, mutation in malformed_signal_options.items():
    with self.subTest(family=family):
        self.assertEqual(
            {sibling},
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "explicit parser outcome matrix must hold",
        )

valid_signal_operands = {
    "env-block-signal-exact-value": (
        f"\nenv --block-signal={sibling} true\n"
    ),
    "env-default-signal-exact-value": (
        f"\nenv --default-signal={sibling} true\n"
    ),
    "env-ignore-signal-exact-value": (
        f"\nenv --ignore-signal={sibling} true\n"
    ),
}
for family, mutation in valid_signal_operands.items():
    with self.subTest(family=family):
        self.assertEqual(
            set(),
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "explicit parser outcome matrix must hold",
        )
```

  Run the focused RED as the sole non-errexit exception:

```bash
set -euo pipefail
shopt -s inherit_errexit
set +e
red_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
    -v 2>&1
)"
red_status="$?"
set -e
printf '%s\n' "$red_output"
test "$red_status" -ne 0
case "$red_output" in
  *"explicit parser outcome matrix must hold"*) ;;
  *) exit 1 ;;
esac
```

  Valid RED imports and reaches exactly the named test, fails on one or more
  new behavior-specific assertions, and includes the fixed marker. Import
  errors, missing tests, unrelated failures, or another marker do not count.
  Record the exact status and subtest families in the Task ledger.

- [ ] **Step 3: Implement the three-outcome parser and run focused GREEN.**

  Within the existing local oracle, define the exact tagged return interface
  and convert it only at `command_sink` exit:

```python
ParseResult = tuple[str, frozenset[str]]

def dispatch(paths: set[str]) -> ParseResult:
    return ("dispatch", frozenset(paths))

def no_dispatch() -> ParseResult:
    return ("no-dispatch", frozenset())

def ambiguous(items: list[str]) -> ParseResult:
    return ("ambiguous", frozenset(fail_closed(items)))

def materialize(result: ParseResult) -> set[str]:
    kind, paths = result
    if kind == "no-dispatch":
        return set()
    if kind in {"dispatch", "ambiguous"}:
        return set(paths)
    raise AssertionError("invalid parser outcome")
```

  Change every recursive parser return to this interface. Use this exact
  transition shape for every split option; the nested call closes over the one
  original `budget` and therefore cannot mint new credit:

```python
def parse_env_split(
    split_value: str,
    tail: list[str],
) -> ParseResult:
    split_tokens = split_env_static(split_value)
    if split_tokens is None:
        return ambiguous([split_value, *tail])
    return parse_env([*split_tokens, *tail])

if token == "--split-string":
    if index + 1 >= len(items):
        return ambiguous(items[index:])
    return parse_env_split(items[index + 1], items[index + 2 :])
if token.startswith("--split-string="):
    return parse_env_split(token.split("=", 1)[1], items[index + 1 :])
```

  In the short-option loop, after consuming any preceding `i` or `v`, handle
  `S` as the terminal option in that token. For attached and clustered forms,
  pass the characters after `S` with `items[index + 1 :]`; for a separated
  operand, pass `items[index + 1]` with `items[index + 2 :]`. Return
  `parse_env_split(...)` immediately in both cases, with no index increment.

  Detect dynamic command-position tokens and exact signal names with these
  local predicates:

```python
signal_options = (
    "--block-signal",
    "--default-signal",
    "--ignore-signal",
)

def is_exact_signal_option(token: str) -> bool:
    return token in signal_options or any(
        token.startswith(option + "=")
        for option in signal_options
    )

def is_signal_near_prefix(token: str) -> bool:
    return any(token.startswith(option) for option in signal_options)

def is_unresolved_dynamic_head(token: str) -> bool:
    return (
        variable_re.fullmatch(token) is not None
        and resolved_path(token, positional) is None
    )

def has_relevant_sibling(items: list[str]) -> bool:
    return any(
        resolved_path(token, positional) is not None
        or any(path in token for path in sibling_entrypoints)
        for token in items
    )
```

  Evaluate the exact signal predicate before the near-prefix predicate. At a
  command position, return `ambiguous(items)` when
  `is_unresolved_dynamic_head(items[0])` and
  `has_relevant_sibling(items[1:])`; otherwise a proved static non-sibling
  head is `no_dispatch()`. Apply the same check to the script operand after a
  recognized `python3` or `bash` head. Query-only `command` forms return
  `no_dispatch()` before this head logic.

```bash
set -euo pipefail
shopt -s inherit_errexit
focused_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
    -v 2>&1
)"
test -n "$focused_output"
printf '%s\n' "$focused_output"
case "$focused_output" in
  *"Ran 1 test"*"OK"*) ;;
  *) exit 1 ;;
esac
routing_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing \
    -v 2>&1
)"
test -n "$routing_output"
printf '%s\n' "$routing_output"
case "$routing_output" in
  *"OK"*) ;;
  *) exit 1 ;;
esac
```

  GREEN must preserve the planned local `html5lib` skip exactly as a skip;
  it must not convert a failure into a skip or xfail.

- [ ] **Step 4: Run the frozen regression and static evidence ladder.**

```bash
set -euo pipefail
shopt -s inherit_errexit
regression_output="$(
  python3 -m unittest \
    tests.validation.test_ci_gate_contract \
    tests.validation.test_ci_gate_runner \
    tests.validation.test_ci_gate_adapters \
    tests.validation.test_github_workflow_contract \
    tests.validation.test_agent_governance_ci_routing \
    -v 2>&1
)"
test -n "$regression_output"
printf '%s\n' "$regression_output"
case "$regression_output" in
  *"OK"*) ;;
  *) exit 1 ;;
esac
workflow_output="$(
  python3 scripts/validation/check-github-workflow-contract.py 2>&1
)"
test -n "$workflow_output"
printf '%s\n' "$workflow_output"
delta_output="$(
  python3 scripts/validation/check-target-surface-delta-contract.py \
    --mode advisory 2>&1
)"
test -n "$delta_output"
printf '%s\n' "$delta_output"
metadata_output="$(
  python3 scripts/validation/check-document-metadata.py \
    --mode check-changed 2>&1
)"
test -n "$metadata_output"
printf '%s\n' "$metadata_output"
traceability_output="$(
  bash scripts/validation/check-doc-traceability.sh 2>&1
)"
test -n "$traceability_output"
printf '%s\n' "$traceability_output"
ci_list_output="$(
  python3 scripts/validation/run-ci-gate.py --profile ci --list 2>&1
)"
test -n "$ci_list_output"
printf '%s\n' "$ci_list_output"
ci_dry_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile ci --dry-run --all 2>&1
)"
test -n "$ci_dry_output"
printf '%s\n' "$ci_dry_output"
script_backed_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile local-script-backed --dry-run --all 2>&1
)"
test -n "$script_backed_output"
printf '%s\n' "$script_backed_output"
local_harness_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile local-harness --dry-run --all 2>&1
)"
test -n "$local_harness_output"
printf '%s\n' "$local_harness_output"
all_profiles_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile local-all-profiles --dry-run --all 2>&1
)"
test -n "$all_profiles_output"
printf '%s\n' "$all_profiles_output"
if python3 -c 'import ruff' >/dev/null 2>&1; then
  python3 -m ruff check \
    tests/validation/test_agent_governance_ci_routing.py
else
  printf '%s\n' 'UNVERIFIED: Ruff is unavailable; installation prohibited'
fi
python3 -m compileall -q \
  tests/validation/test_agent_governance_ci_routing.py
git diff --check
```

  The repository umbrella, registered typed child gates, direct pre-commit,
  controlled wrapper, Compose/runtime, network, secrets, credentials, remote
  state, and Graphify update remain prohibited. The listed standalone static
  validators and execution-free `--list`/`--dry-run` projections are the only
  authorized child-gate evidence.

- [ ] **Step 5: Re-resolve the implementation base, prove exact scope and
  freezes, then commit the sole attempt.**

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test -n "$expected_paths"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" -- &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_paths"
git diff --exit-code "$implementation_base" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_mode="$(
  git ls-files -s \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
task_mode="$(
  git ls-files -s \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
git diff --check
git add \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$expected_paths"
git commit -m "fix(ci): close explicit parser outcome proof"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
committed_test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$committed_test_mode" = "100644"
committed_task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$committed_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 6: Independently review the exact implementation range and
  record one terminal review checkpoint.**

  Each fresh reviewer independently runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record explicit parser outcome plan reviews$'
)"
test -n "$implementation_base"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test -n "$expected_paths"
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  If and only if both reports are `C0/I0/M0`, edit only the Task ledger and
  create the accepted checkpoint:

```bash
set -euo pipefail
shopt -s inherit_errexit
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record explicit parser outcome review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record explicit parser outcome review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record explicit parser outcome review$'
)"
test -n "$review_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$implementation_commit..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  If either report is not `C0/I0/M0`, edit only the Task ledger and run the
  mutually exclusive rejected-review checkpoint instead:

```bash
set -euo pipefail
shopt -s inherit_errexit
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close explicit parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record exhausted explicit parser outcome review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted explicit parser outcome review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted explicit parser outcome review$'
)"
test -n "$review_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$implementation_commit..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  The rejected checkpoint grants no implementation retry or downstream
  authority. The uncreated
  `docs(task): record explicit parser outcome review` checkpoint would have
  authorized Task 4.5 only under 4AB, but 4AC supersedes this section for
  execution and this historical block grants no current authority.

#### Task 4.4AC / T-TSDC-004R-4AC: Candidate-Closed Parser-Outcome Proof

**Authority boundary and supersession:**

- The exact unique
  `docs(task): record exhausted explicit parser outcome plan review` commit
  must resolve to
  `997719ff22cbaa9f4bc0c160f0e6c56fc76d54ba`, be `HEAD` when this
  design is authored, and remain an ancestor of every 4AC checkpoint.
- This Plan-only successor may modify only this Plan and the sibling Task
  ledger. Its exact unique subject is
  `docs(plan): define candidate-closed parser outcome proof`.
- Two fresh read-only reviewers inspect the complete
  `997719ff..$plan_checkpoint` range: one specification reviewer and a
  different quality/security reviewer. Both must return `C0/I0/M0`. Any other
  result is recorded in the exact Task-only
  `docs(task): record exhausted candidate-closed parser outcome plan review`
  checkpoint and returns to design; there is no Plan correction inside 4AC.
- After both approvals, the controller records the reports and exact range in
  a Task-ledger-only commit with the exact unique subject
  `docs(task): record candidate-closed parser outcome plan reviews`. That clean
  commit is the immutable implementation base.
- One fresh implementation agent then receives exactly one attempt. It may
  modify only
  `tests/validation/test_agent_governance_ci_routing.py` and the sibling Task
  ledger. Its exact unique subject is
  `fix(ci): close candidate-closed parser outcome proof`.
- Freeze `.github/workflow-contract.yml`,
  `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, every typed gate contract,
  runner, adapter, and test outside the allowed routing test, every
  target-delta artifact, and every other tracked path.
- A fresh read-only specification reviewer and a different fresh read-only
  quality/security reviewer inspect the exact implementation-base-to-commit
  range. Both must return `C0/I0/M0`. The controller then records the accepted
  pair in a Task-ledger-only commit with the exact unique subject
  `docs(task): record candidate-closed parser outcome review`.
- Any non-`C0/I0/M0` implementation review exhausts 4AC without retry. The
  controller records the rejected pair in a Task-ledger-only commit with the
  exact unique subject
  `docs(task): record exhausted candidate-closed parser outcome review`;
  Task 4R, Wave C, Tasks 5–6, and final branch review remain blocked.
- 4AC supersedes 4AB for execution and incorporates every accepted 4W parser,
  matrix, budget, and evidence requirement; the corrected 4X GNU `env --` and
  session-local contract; the 4Y strict/full-lineage contract; the 4Z
  status-preserving contract; the 4AA immediate capture/test contract; and
  the 4AB explicit three-outcome boundary. Every earlier command block and
  uncreated subject is historical and non-executable.

**Files and interfaces:**

- Modify
  `tests/validation/test_agent_governance_ci_routing.py` only inside
  `test_repository_umbrella_is_wiring_only` and its existing
  `_registered_sibling_dispatches` static oracle.
- Modify
  `docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md`
  only for bounded RED, GREEN, validation, commit, and review evidence.
- Do not create a parser module, helper script, workflow, contract field,
  generated artifact, dependency, or production runtime surface.
- Preserve the accepted static-oracle statement boundary. This successor does
  not add arbitrary shell interpretation for `&&`, `||`, pipelines, or
  `bash -c`; Spec 135 explicitly excludes inference of arbitrary shell
  semantics. A future expansion would require its own approved design and
  behavior-specific proof.
- Inside `command_sink`, the recursive parser consumes and produces one local
  `ParseResult = tuple[str, frozenset[str]]`. The tag is exactly one of
  `dispatch`, `no-dispatch`, or `ambiguous`. `dispatch` contains every
  statically proven registered sibling sink; `no-dispatch` contains no paths;
  and `ambiguous` contains the union of every exact and embedded recoverable
  registered sibling, falling back to the complete registered set only when
  syntax is ambiguous and no candidate is recoverable.
- Convert a `ParseResult` to the existing public `set[str]` only once at the
  outer `command_sink` boundary: materialize both `dispatch` and `ambiguous`
  paths as findings and materialize `no-dispatch` as the empty set. Existing
  callers, messages, and value-free diagnostics remain unchanged.

**Candidate-closed parser contract:**

- `candidate_paths(items)` scans every item before returning. For each token,
  union the path returned by `resolved_path(token, positional)`, when present,
  with every registered sibling whose literal path is embedded in that token.
  Never return early after finding an exact path.
- `ambiguous(items)` stores `candidate_paths(items)` when nonempty and stores
  the complete registered sibling set only when that union is empty.
  `has_relevant_sibling(items)` is true only when `candidate_paths(items)` is
  nonempty; it never uses the all-registered ambiguity fallback.
- A dynamic target is a named variable matched by `variable_re` or one of
  `$1` and `${1}` whose `resolved_path(token, positional)` is unresolved.
  A helper invocation that binds `positional` therefore resolves `$1` and
  `${1}` normally instead of marking them ambiguous.
- At a direct, `command`, `python3`, or `bash` command position, an unresolved
  dynamic target is `ambiguous` only when later tokens have a relevant
  sibling. The same unresolved target without a relevant later sibling is
  `no-dispatch`. `command -v` and `command -V`, including valid clusters,
  return `no-dispatch` before target evaluation.
- The original work budget remains exactly
  `8 * (1 + original token count + total source-token character count)`.
  Every wrapper/option token and every GNU split-string character charges that
  one closure-owned budget. Recursive parsing and inserted tokens never reset
  or add credit. Budget exhaustion is `ambiguous`.
- Follow the
  [Coreutils 9.11 `env` grammar](https://www.gnu.org/software/coreutils/manual/html_node/env-invocation.html)
  and keep the existing static lexer. Separated `-S STRING` and
  `--split-string STRING`, attached `-SSTRING` and
  `--split-string=STRING`, and clustered forms such as `-vSSTRING` all lex
  once, combine split tokens with only the untouched original tail, and
  immediately re-enter the same `parse_env` function at the first combined
  token. There is no post-insertion index increment.
- Preserve the documented static `env -S` quotes, whitespace, comment,
  `\c`, `\f`, `\n`, `\r`, `\t`, `\v`, `\#`, `\$`, `\_`, `\"`, `\'`, and
  `\\` behavior. Do not read `os.environ`, invoke a shell, expand a variable,
  execute a wrapper, or execute any sibling entrypoint.
- Recognize signal options only when the token equals
  `--block-signal`, `--default-signal`, or `--ignore-signal`, or begins with
  that exact name followed immediately by `=`. A token that merely starts
  with one of those names is `ambiguous`. A two-sibling regression must prove
  that ambiguity retains both an embedded option-value sibling and a different
  exact remaining sibling.
- Preserve the accepted Bash
  [`command`](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html)
  and
  [`exec`](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
  option arities, GNU `env --` assignment transition, option-operand
  no-dispatch behavior, nested wrapper recursion, deterministic value-free
  fallback, and all literal, quoted, variable-mediated, helper, Python
  heredoc `subprocess`, and `os.system` dispatch families.

**Strict proof contract:**

- Every 4AC fenced Bash block begins with `set -euo pipefail` and
  `shopt -s inherit_errexit`.
- Every non-RED `$()` is the complete right-hand side of a standalone simple
  assignment. The immediately following command is a `test` naming that exact
  variable. Count, distance, path, mode, and clean-state captures use their
  full semantic assertion as that immediate test.
- The focused RED is the sole exception: `red_output` is immediately followed
  by `red_status="$?"`; `errexit` is restored before output and assertions.
- Before committing this Plan, statically extract every 4AC and Task 4.5
  Step 0 Bash block; require strict first two lines, Bash syntax, adjacent
  capture consumption, the sole RED exception, exact two-path scope, exact
  `100644` modes, metadata, traceability, and diff hygiene.

- [ ] **Step 1: Commit and independently review the 4AC Plan.**

  Immediately after the Plan commit and before either review, the controller
  runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 997719ff)"
test -n "$design_base"
failure_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted explicit parser outcome plan review$' |
    wc -l
)"
test "$failure_subject_count" -eq 1
failure_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted explicit parser outcome plan review$'
)"
test "$failure_checkpoint" = "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
task_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  If either Plan reviewer is not `C0/I0/M0`, edit only the Task ledger and
  terminate 4AC with this exact rejected-Plan checkpoint:

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record exhausted candidate-closed parser outcome plan review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted candidate-closed parser outcome plan review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted candidate-closed parser outcome plan review$'
)"
test -n "$review_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$plan_checkpoint..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  This rejected-Plan checkpoint grants no correction, implementation, or
  downstream authority.

  After both Plan reviewers return `C0/I0/M0`, edit only the Task ledger and
  run this separate strict session:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 997719ff)"
test -n "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$'
)"
test -n "$plan_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$plan_checkpoint"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record candidate-closed parser outcome plan reviews"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 2: Rebind the implementation session and add the complete
  fallback-resistant RED matrix.**

  The implementation agent first proves the complete authority chain:

```bash
set -euo pipefail
shopt -s inherit_errexit
design_base="$(git rev-parse 997719ff)"
test -n "$design_base"
plan_subject_count="$(
  git log --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$' |
    wc -l
)"
test "$plan_subject_count" -eq 1
plan_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(plan): define candidate-closed parser outcome proof$'
)"
test -n "$plan_checkpoint"
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
git merge-base --is-ancestor "$design_base" "$plan_checkpoint"
git merge-base --is-ancestor "$plan_checkpoint" "$implementation_base"
plan_distance="$(
  git rev-list --count "$design_base..$plan_checkpoint"
)"
test "$plan_distance" -eq 1
base_distance="$(
  git rev-list --count "$plan_checkpoint..$implementation_base"
)"
test "$base_distance" -eq 1
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_task_mode="$(
  git ls-tree "$implementation_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_task_mode" = "100644"
base_test_mode="$(
  git ls-tree "$implementation_base" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$base_test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  Add these exact behavior families inside
  `test_repository_umbrella_is_wiring_only`. `assignment_sibling` is the
  existing second distinct registered path. Exact singleton, two-path, and
  empty-set assertions prevent all-registered fallback, direct-head
  misclassification, or early-return candidate loss from satisfying RED:

```python
split_transition_dispatch = {
    "env-split-direct-separated": f"\nenv -S '{sibling}'\n",
    "env-split-direct-attached": f"\nenv -S'{sibling}'\n",
    "env-split-direct-clustered": f"\nenv -vS'{sibling}'\n",
    "env-split-long-separated": (
        f"\nenv --split-string '{sibling}'\n"
    ),
    "env-split-long-equals": (
        f"\nenv --split-string='{sibling}'\n"
    ),
    "env-split-long-python-separated": (
        f"\nenv --split-string 'python3 {sibling}'\n"
    ),
    "env-split-long-python-equals": (
        f"\nenv --split-string='python3 {sibling}'\n"
    ),
    "env-split-nested-dispatch": (
        f"\nenv -S 'command -p exec -a gate python3 {sibling}'\n"
    ),
}
for family, mutation in split_transition_dispatch.items():
    with self.subTest(family=family):
        self.assertEqual(
            {sibling},
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )

split_transition_no_dispatch = {
    "env-split-query-separated": (
        f"\nenv -S 'command -v python3 {sibling}'\n"
    ),
    "env-split-query-attached": (
        f"\nenv -S'command -v python3 {sibling}'\n"
    ),
    "env-split-query-clustered": (
        f"\nenv -vS'command -v python3 {sibling}'\n"
    ),
    "env-split-query-long-separated": (
        f"\nenv --split-string 'command -v python3 {sibling}'\n"
    ),
    "env-split-query-long-equals": (
        f"\nenv --split-string='command -v python3 {sibling}'\n"
    ),
}
for family, mutation in split_transition_no_dispatch.items():
    with self.subTest(family=family):
        self.assertEqual(
            set(),
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )

dynamic_relevant_mutations = {
    "direct-named-dynamic-target": f'\n"$RUNNER" {sibling}\n',
    "direct-braced-named-dynamic-target": (
        f'\n"${{RUNNER}}" {sibling}\n'
    ),
    "command-named-dynamic-target": (
        f'\ncommand "$RUNNER" {sibling}\n'
    ),
    "command-braced-named-dynamic-target": (
        f'\ncommand "${{RUNNER}}" {sibling}\n'
    ),
    "python-named-dynamic-script": (
        f'\npython3 "$SCRIPT" {sibling}\n'
    ),
    "python-braced-named-dynamic-script": (
        f'\npython3 "${{SCRIPT}}" {sibling}\n'
    ),
    "bash-named-dynamic-script": f'\nbash "$SCRIPT" {sibling}\n',
    "bash-braced-named-dynamic-script": (
        f'\nbash "${{SCRIPT}}" {sibling}\n'
    ),
    "direct-positional-target": f'\n"$1" {sibling}\n',
    "direct-braced-positional-target": f'\n"${{1}}" {sibling}\n',
    "command-positional-target": f'\ncommand "$1" {sibling}\n',
    "command-braced-positional-target": (
        f'\ncommand "${{1}}" {sibling}\n'
    ),
    "python-positional-script": f'\npython3 "$1" {sibling}\n',
    "python-braced-positional-script": (
        f'\npython3 "${{1}}" {sibling}\n'
    ),
    "bash-positional-script": f'\nbash "$1" {sibling}\n',
    "bash-braced-positional-script": f'\nbash "${{1}}" {sibling}\n',
}
for family, mutation in dynamic_relevant_mutations.items():
    with self.subTest(family=family):
        self.assertEqual(
            {sibling},
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )

harmless = "not-a-registered-sibling"
dynamic_no_relevant_mutations = {
    "direct-named-no-relevant": f'\n"$RUNNER" {harmless}\n',
    "direct-braced-named-no-relevant": (
        f'\n"${{RUNNER}}" {harmless}\n'
    ),
    "command-named-no-relevant": (
        f'\ncommand "$RUNNER" {harmless}\n'
    ),
    "command-braced-named-no-relevant": (
        f'\ncommand "${{RUNNER}}" {harmless}\n'
    ),
    "python-named-no-relevant": f'\npython3 "$SCRIPT" {harmless}\n',
    "python-braced-named-no-relevant": (
        f'\npython3 "${{SCRIPT}}" {harmless}\n'
    ),
    "bash-named-no-relevant": f'\nbash "$SCRIPT" {harmless}\n',
    "bash-braced-named-no-relevant": (
        f'\nbash "${{SCRIPT}}" {harmless}\n'
    ),
    "direct-positional-no-relevant": f'\n"$1" {harmless}\n',
    "direct-braced-positional-no-relevant": (
        f'\n"${{1}}" {harmless}\n'
    ),
    "command-positional-no-relevant": f'\ncommand "$1" {harmless}\n',
    "command-braced-positional-no-relevant": (
        f'\ncommand "${{1}}" {harmless}\n'
    ),
    "python-positional-no-relevant": f'\npython3 "$1" {harmless}\n',
    "python-braced-positional-no-relevant": (
        f'\npython3 "${{1}}" {harmless}\n'
    ),
    "bash-positional-no-relevant": f'\nbash "$1" {harmless}\n',
    "bash-braced-positional-no-relevant": (
        f'\nbash "${{1}}" {harmless}\n'
    ),
}
for family, mutation in dynamic_no_relevant_mutations.items():
    with self.subTest(family=family):
        self.assertEqual(
            set(),
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )

dynamic_query_mutations = {
    "command-named-query-v": f'\ncommand -v "$RUNNER" {sibling}\n',
    "command-named-query-V": f'\ncommand -V "$RUNNER" {sibling}\n',
    "command-named-query-cluster": (
        f'\ncommand -pv "$RUNNER" {sibling}\n'
    ),
    "command-braced-named-query-cluster": (
        f'\ncommand -pV "${{RUNNER}}" {sibling}\n'
    ),
    "command-positional-query-v": f'\ncommand -v "$1" {sibling}\n',
    "command-positional-query-cluster": (
        f'\ncommand -pV "$1" {sibling}\n'
    ),
    "command-braced-positional-query-cluster": (
        f'\ncommand -vp "${{1}}" {sibling}\n'
    ),
}
for family, mutation in dynamic_query_mutations.items():
    with self.subTest(family=family):
        self.assertEqual(
            set(),
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )

candidate_union_mutations = {
    "env-block-signal-candidate-union": (
        f"\nenv --block-signalX={assignment_sibling} "
        f"python3 {sibling}\n"
    ),
    "env-default-signal-candidate-union": (
        f"\nenv --default-signalX={assignment_sibling} "
        f"python3 {sibling}\n"
    ),
    "env-ignore-signal-candidate-union": (
        f"\nenv --ignore-signalX={assignment_sibling} "
        f"python3 {sibling}\n"
    ),
}
for family, mutation in candidate_union_mutations.items():
    with self.subTest(family=family):
        self.assertEqual(
            {assignment_sibling, sibling},
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )

valid_signal_operands = {
    "env-block-signal-exact-value": (
        f"\nenv --block-signal={assignment_sibling} true\n"
    ),
    "env-default-signal-exact-value": (
        f"\nenv --default-signal={assignment_sibling} true\n"
    ),
    "env-ignore-signal-exact-value": (
        f"\nenv --ignore-signal={assignment_sibling} true\n"
    ),
}
for family, mutation in valid_signal_operands.items():
    with self.subTest(family=family):
        self.assertEqual(
            set(),
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )

valid_signal_commands = {
    "env-block-signal-exact-command": (
        f"\nenv --block-signal={assignment_sibling} "
        f"python3 {sibling}\n"
    ),
    "env-default-signal-exact-command": (
        f"\nenv --default-signal={assignment_sibling} "
        f"python3 {sibling}\n"
    ),
    "env-ignore-signal-exact-command": (
        f"\nenv --ignore-signal={assignment_sibling} "
        f"python3 {sibling}\n"
    ),
}
for family, mutation in valid_signal_commands.items():
    with self.subTest(family=family):
        self.assertEqual(
            {sibling},
            self._registered_sibling_dispatches(
                source + mutation,
                sibling_entrypoints,
            ),
            "candidate-closed parser outcome matrix must hold",
        )
```

  Run the focused RED as the sole non-errexit exception:

```bash
set -euo pipefail
shopt -s inherit_errexit
set +e
red_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
    -v 2>&1
)"
red_status="$?"
set -e
printf '%s\n' "$red_output"
test "$red_status" -ne 0
case "$red_output" in
  *"candidate-closed parser outcome matrix must hold"*) ;;
  *) exit 1 ;;
esac
```

  Valid RED imports and reaches exactly the named test, fails on one or more
  new behavior-specific assertions, and includes the fixed marker. Import
  errors, missing tests, unrelated failures, or another marker do not count.
  Record the exact status and subtest families in the Task ledger.

- [ ] **Step 3: Implement the candidate-closed three-outcome parser and run
  focused GREEN.**

  Within the existing local oracle, replace early-return candidate collection
  with this exact union and tagged return interface:

```python
ParseResult = tuple[str, frozenset[str]]

def candidate_paths(items: list[str]) -> set[str]:
    found: set[str] = set()
    for token in items:
        exact = resolved_path(token, positional)
        if exact is not None:
            found.add(exact)
        found.update(
            path
            for path in sibling_entrypoints
            if path in token
        )
    return found

def dispatch(paths: set[str]) -> ParseResult:
    return ("dispatch", frozenset(paths))

def no_dispatch() -> ParseResult:
    return ("no-dispatch", frozenset())

def ambiguous(items: list[str]) -> ParseResult:
    candidates = candidate_paths(items)
    if not candidates:
        candidates = set(sibling_entrypoints)
    return ("ambiguous", frozenset(candidates))

def materialize(result: ParseResult) -> set[str]:
    kind, paths = result
    if kind == "no-dispatch":
        return set()
    if kind in {"dispatch", "ambiguous"}:
        return set(paths)
    raise AssertionError("invalid parser outcome")
```

  Define the exact relevant-sibling and dynamic-target predicates. The
  positional binding check prevents helper-bound `$1` and `${1}` from being
  treated as unresolved:

```python
def has_relevant_sibling(items: list[str]) -> bool:
    return bool(candidate_paths(items))

def is_unresolved_dynamic_target(token: str) -> bool:
    is_supported_dynamic = (
        token in {"$1", "${1}"}
        or variable_re.fullmatch(token) is not None
    )
    return (
        is_supported_dynamic
        and resolved_path(token, positional) is None
    )
```

  Change `parse_chain`, `parse_command`, `parse_exec`, and `parse_env` to
  return `ParseResult`. After query-only handling, evaluate a direct or
  wrapper-selected dynamic target with this exact branch:

```python
if is_unresolved_dynamic_target(target):
    if has_relevant_sibling(remaining):
        return ambiguous([target, *remaining])
    return no_dispatch()
```

  A registered resolved target is `dispatch`; a proved static non-sibling
  target is `no_dispatch`. Apply the same branch to the script operand and
  remaining arguments after `python3` or `bash`.

  Use one same-parser transition for every split form:

```python
def parse_env_split(
    split_value: str,
    tail: list[str],
) -> ParseResult:
    split_tokens = split_env_static(split_value)
    if split_tokens is None:
        return ambiguous([split_value, *tail])
    return parse_env([*split_tokens, *tail])

if token == "--split-string":
    if index + 1 >= len(items):
        return ambiguous(items[index:])
    return parse_env_split(items[index + 1], items[index + 2 :])
if token.startswith("--split-string="):
    return parse_env_split(token.split("=", 1)[1], items[index + 1 :])
```

  In the short-option loop, after consuming preceding `i` or `v`, treat `S`
  as terminal in that token. Attached/clustered forms pass the characters
  after `S` with `items[index + 1 :]`; separated forms pass
  `items[index + 1]` with `items[index + 2 :]`. Return
  `parse_env_split(...)` immediately with no index increment.

  Evaluate exact signal names before near-prefix ambiguity:

```python
signal_options = (
    "--block-signal",
    "--default-signal",
    "--ignore-signal",
)

def is_exact_signal_option(token: str) -> bool:
    return token in signal_options or any(
        token.startswith(option + "=")
        for option in signal_options
    )

def is_signal_near_prefix(token: str) -> bool:
    return any(token.startswith(option) for option in signal_options)
```

```bash
set -euo pipefail
shopt -s inherit_errexit
focused_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_repository_umbrella_is_wiring_only \
    -v 2>&1
)"
test -n "$focused_output"
printf '%s\n' "$focused_output"
case "$focused_output" in
  *"Ran 1 test"*"OK"*) ;;
  *) exit 1 ;;
esac
routing_output="$(
  python3 -m unittest \
    tests.validation.test_agent_governance_ci_routing \
    -v 2>&1
)"
test -n "$routing_output"
printf '%s\n' "$routing_output"
case "$routing_output" in
  *"OK"*) ;;
  *) exit 1 ;;
esac
```

  GREEN must preserve the planned local `html5lib` skip exactly as a skip;
  it must not convert a failure into a skip or xfail.

- [ ] **Step 4: Run the frozen regression and static evidence ladder.**

```bash
set -euo pipefail
shopt -s inherit_errexit
regression_output="$(
  python3 -m unittest \
    tests.validation.test_ci_gate_contract \
    tests.validation.test_ci_gate_runner \
    tests.validation.test_ci_gate_adapters \
    tests.validation.test_github_workflow_contract \
    tests.validation.test_agent_governance_ci_routing \
    -v 2>&1
)"
test -n "$regression_output"
printf '%s\n' "$regression_output"
case "$regression_output" in
  *"OK"*) ;;
  *) exit 1 ;;
esac
workflow_output="$(
  python3 scripts/validation/check-github-workflow-contract.py 2>&1
)"
test -n "$workflow_output"
printf '%s\n' "$workflow_output"
delta_output="$(
  python3 scripts/validation/check-target-surface-delta-contract.py \
    --mode advisory 2>&1
)"
test -n "$delta_output"
printf '%s\n' "$delta_output"
metadata_output="$(
  python3 scripts/validation/check-document-metadata.py \
    --mode check-changed 2>&1
)"
test -n "$metadata_output"
printf '%s\n' "$metadata_output"
traceability_output="$(
  bash scripts/validation/check-doc-traceability.sh 2>&1
)"
test -n "$traceability_output"
printf '%s\n' "$traceability_output"
ci_list_output="$(
  python3 scripts/validation/run-ci-gate.py --profile ci --list 2>&1
)"
test -n "$ci_list_output"
printf '%s\n' "$ci_list_output"
ci_dry_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile ci --dry-run --all 2>&1
)"
test -n "$ci_dry_output"
printf '%s\n' "$ci_dry_output"
script_backed_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile local-script-backed --dry-run --all 2>&1
)"
test -n "$script_backed_output"
printf '%s\n' "$script_backed_output"
local_harness_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile local-harness --dry-run --all 2>&1
)"
test -n "$local_harness_output"
printf '%s\n' "$local_harness_output"
all_profiles_output="$(
  python3 scripts/validation/run-ci-gate.py \
    --profile local-all-profiles --dry-run --all 2>&1
)"
test -n "$all_profiles_output"
printf '%s\n' "$all_profiles_output"
if python3 -c 'import ruff' >/dev/null 2>&1; then
  python3 -m ruff check \
    tests/validation/test_agent_governance_ci_routing.py
else
  printf '%s\n' 'UNVERIFIED: Ruff is unavailable; installation prohibited'
fi
python3 -m compileall -q \
  tests/validation/test_agent_governance_ci_routing.py
git diff --check
```

  The repository umbrella, registered typed child gates, direct pre-commit,
  controlled wrapper, Compose/runtime, network, secrets, credentials, remote
  state, and Graphify update remain prohibited. The listed standalone static
  validators and execution-free `--list`/`--dry-run` projections are the only
  authorized child-gate evidence.

- [ ] **Step 5: Re-resolve the implementation base, prove exact scope and
  freezes, then commit the sole attempt.**

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$'
)"
test -n "$implementation_base"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_base"
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test -n "$expected_paths"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" -- &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_paths"
git diff --exit-code "$implementation_base" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_mode="$(
  git ls-files -s \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
task_mode="$(
  git ls-files -s \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
git diff --check
git add \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$expected_paths"
git commit -m "fix(ci): close candidate-closed parser outcome proof"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
committed_test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$committed_test_mode" = "100644"
committed_task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$committed_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

- [ ] **Step 6: Independently review the exact implementation range and
  record one terminal review checkpoint.**

  Each fresh reviewer independently runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
base_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$' |
    wc -l
)"
test "$base_subject_count" -eq 1
implementation_base="$(
  git log -1 --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome plan reviews$'
)"
test -n "$implementation_base"
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
git merge-base --is-ancestor "$implementation_base" "$implementation_commit"
implementation_distance="$(
  git rev-list --count "$implementation_base..$implementation_commit"
)"
test "$implementation_distance" -eq 1
expected_paths="$(
  printf '%s\n' \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
    tests/validation/test_agent_governance_ci_routing.py |
    sort
)"
test -n "$expected_paths"
implementation_paths="$(
  git diff --name-only \
    "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ':(exclude)tests/validation/test_agent_governance_ci_routing.py' \
  ':(exclude)docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
task_mode="$(
  git ls-tree "$implementation_commit" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
test_mode="$(
  git ls-tree "$implementation_commit" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  If and only if both reports are `C0/I0/M0`, edit only the Task ledger and
  create the accepted checkpoint:

```bash
set -euo pipefail
shopt -s inherit_errexit
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record candidate-closed parser outcome review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record candidate-closed parser outcome review$'
)"
test -n "$review_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$implementation_commit..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  If either report is not `C0/I0/M0`, edit only the Task ledger and create the
  mutually exclusive rejected-review checkpoint:

```bash
set -euo pipefail
shopt -s inherit_errexit
implementation_subject_count="$(
  git log --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$' |
    wc -l
)"
test "$implementation_subject_count" -eq 1
implementation_commit="$(
  git log -1 --format=%H \
    --grep='^fix(ci): close candidate-closed parser outcome proof$'
)"
test -n "$implementation_commit"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$implementation_commit"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git diff --check
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
git commit -m "docs(task): record exhausted candidate-closed parser outcome review"
review_subject_count="$(
  git log --format=%H \
    --grep='^docs(task): record exhausted candidate-closed parser outcome review$' |
    wc -l
)"
test "$review_subject_count" -eq 1
review_checkpoint="$(
  git log -1 --format=%H \
    --grep='^docs(task): record exhausted candidate-closed parser outcome review$'
)"
test -n "$review_checkpoint"
head_commit="$(git rev-parse HEAD)"
test "$head_commit" = "$review_checkpoint"
git merge-base --is-ancestor "$implementation_commit" "$review_checkpoint"
review_distance="$(
  git rev-list --count "$implementation_commit..$review_checkpoint"
)"
test "$review_distance" -eq 1
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
review_task_mode="$(
  git ls-tree "$review_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

  The rejected checkpoint grants no implementation retry or downstream
  authority. Only the accepted
  `docs(task): record candidate-closed parser outcome review` checkpoint
  authorizes Task 4.5 Wave C.

#### Task 4.4AF / T-TSDC-004R-4AF: Canonical-Row Authority Proof

**Design return:** The 4AE Plan preserved the accepted candidate-closed
parser, dynamic-target, GNU `env`, signal-option, RED/GREEN, scope, and
validation design, but its quality/security review found a duplicate
no-leading-pipe candidate-counting bypass and missing repeated fixed-line
authority-subject uniqueness. 4AF changes only those two approved deltas. It
inherits the immutable 4AC behavior and implementation requirements
from Plan commit `5bc5ab85e9d8841761ae00b7a169e899e3f8f515`: `Files and
interfaces`, `Candidate-closed parser contract`, the Step 2 content beginning
`Add these exact behavior families`, and all of Steps 3–4. Every earlier 4AC
or 4AD/4AE authority, commit, review, and Task 4.5 block remains historical and
non-executable.

**Authority boundary and review attestation:**

- Exact base
  `8cacc4634448416a7dbc8d3de69bf6011b62c6d5` is the sole 4AF design
  predecessor. It must have exact subject
  `docs(task): record exhausted exact-cell review-range plan review`,
  change only the Task ledger, retain mode `100644`, and be `HEAD` before 4AF
  drafting.
- This Plan-only checkpoint may change only this Plan and the sibling Task
  ledger. Its exact unique subject is
  `docs(plan): define canonical-row authority proof`.
- Each reviewer must report both reviewed endpoints as full 40-hex OIDs. The
  specification and quality/security reports must name the same endpoints.
  The controller copies that one full range into the canonical 4AF review
  matrix row in the Task ledger before any terminal evidence commit.
- A terminal session extracts the range from exactly one named Task matrix
  row. Missing, abbreviated, duplicated, malformed, or divergent review
  ranges fail closed. `git log --grep` is never an authority resolver.
- Every edge is a single-parent edge: the child has exactly one parent, that
  first parent equals the expected predecessor, ancestry holds, and the
  predecessor-to-child distance is exactly one.
- Two fresh read-only reviewers inspect exact
  `8cacc4634448416a7dbc8d3de69bf6011b62c6d5..$plan_checkpoint`. Both must
  return `C0/I0/M0`. Any other result
  is recorded in exact Task-only
  `docs(task): record exhausted canonical-row authority plan review`
  and exhausts 4AF without correction.
- Only exact Task-only
  `docs(task): record canonical-row authority plan reviews`
  authorizes one implementation attempt. The implementation may change only
  `tests/validation/test_agent_governance_ci_routing.py` and the Task ledger
  and uses exact subject
  `fix(ci): close canonical-row authority proof`.
- Fresh specification and quality/security reviewers inspect the exact
  accepted-Plan-evidence-to-implementation range and report identical full
  endpoints. Only exact Task-only
  `docs(task): record canonical-row authority review` authorizes
  Wave C. Exact Task-only
  `docs(task): record exhausted canonical-row authority review`
  exhausts the sole attempt.
- Freeze every path frozen by 4AC. Do not run the repository umbrella, direct
  pre-commit, controlled wrapper, Compose/runtime, network, secret, remote, or
  Graphify-update actions.

**Strict proof contract:**

- Every 4AF and rebound Task 4.5 Bash block begins with
  `set -euo pipefail` and `shopt -s inherit_errexit`.
- Every `$()` is the complete right-hand side of a standalone assignment and
  the immediately following command tests that exact variable. The inherited
  focused 4AC RED retains its one documented status-capture exception.
- Exact subject checks use `git show -s --format=%s` on an already bound full
  OID. Exact-subject uniqueness checks use `%s` output plus fixed whole-line
  comparison; commit-message-body matching is prohibited.
- Every applicable session proves the exact base path and mode, every
  predecessor edge, exact commit and range path sets, all applicable
  `100644` modes, and clean tracked, staged, and untracked state.
- The inline adversarial helper oracle requires: canonical-only pass;
  canonical-plus-canonical duplicate and canonical-plus-same-label
  no-leading/malformed no-leading candidates fail `review-range-row-count`;
  a sole no-leading candidate fails canonical shape; six/eight cells fail
  `review-range-cell-count`; later-cell, prefix, suffix, and case-variant
  labels are ignored; and the reviewed escape/extra-range failures remain.

- [ ] **Step 1: Commit and independently review the 4AF Plan checkpoint.**

  Immediately after the Plan commit, and independently inside each reviewer
  session, run:

```bash
set -euo pipefail
shopt -s inherit_errexit
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
design_base="$(
  git rev-parse --verify \
    '8cacc4634448416a7dbc8d3de69bf6011b62c6d5^{commit}'
)"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_mode="$(
  git ls-tree "$design_base" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$plan_checkpoint"
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$plan_checkpoint"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  Each reviewer returns the full
  `8cacc4634448416a7dbc8d3de69bf6011b62c6d5..$plan_checkpoint`
  range with its verdict. Before either terminal path, the controller records
  that identical full range in the
  `T-TSDC-004R-4AF canonical-row proof Plan` matrix row.

  If either reviewer is not `C0/I0/M0`, edit only the Task ledger and run this
  exact rejected terminal session:

```bash
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = \
  "docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$plan_checkpoint"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$task_file"
git commit -m \
  "docs(task): record exhausted canonical-row authority plan review"
review_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$review_checkpoint"
review_subject="$(
  git show -s --format=%s "$review_checkpoint"
)"
test "$review_subject" = \
  "docs(task): record exhausted canonical-row authority plan review"
review_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted canonical-row authority plan review'
)"
test "$review_subject_count" -eq 1
assert_edge "$plan_checkpoint" "$review_checkpoint"
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = "$task_file"
review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$review_checkpoint" |
    sort
)"
test "$review_range_paths" = "$task_file"
review_task_mode="$(
  git ls-tree "$review_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  This rejected checkpoint grants no correction, implementation, test, or
  downstream authority.

  If and only if both reviewers return `C0/I0/M0`, edit only the Task ledger
  and run this separate accepted terminal session:

```bash
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$plan_checkpoint"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$task_file"
git commit -m \
  "docs(task): record canonical-row authority plan reviews"
implementation_base="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$implementation_base"
base_review_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$base_review_subject" = \
  "docs(task): record canonical-row authority plan reviews"
base_review_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority plan reviews'
)"
test "$base_review_subject_count" -eq 1
assert_edge "$plan_checkpoint" "$implementation_base"
base_review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_review_paths" = "$task_file"
base_review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$implementation_base" |
    sort
)"
test "$base_review_range_paths" = "$task_file"
base_review_task_mode="$(
  git ls-tree "$implementation_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_review_task_mode" = "100644"
base_review_test_mode="$(
  git ls-tree "$implementation_base" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$base_review_test_mode" = "100644"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

- [ ] **Step 2: Rebind the accepted Plan chain and execute the inherited 4AC
  behavior proof.**

  The fresh implementation agent receives a brief composed from this 4AF
  section and, at immutable commit `5bc5ab85`, the 4AC Step 2 content beginning
  `Add these exact behavior families` plus all of Steps 3–4. It does not
  execute the earlier 4AC Step 2 authority block or any 4AC commit/review
  block. Before modifying files, run:

```bash
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
implementation_base="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$implementation_base"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
implementation_base_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$implementation_base_subject" = \
  "docs(task): record canonical-row authority plan reviews"
implementation_base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority plan reviews'
)"
test "$implementation_base_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$implementation_base"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
base_review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_review_paths" = "$task_file"
base_review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$implementation_base" |
    sort
)"
test "$base_review_range_paths" = "$task_file"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
base_review_task_mode="$(
  git ls-tree "$implementation_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_review_task_mode" = "100644"
base_review_test_mode="$(
  git ls-tree "$implementation_base" \
    tests/validation/test_agent_governance_ci_routing.py |
    awk '{print $1}'
)"
test "$base_review_test_mode" = "100644"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  Execute the inherited 4AC fallback-resistant RED, the candidate-closed
  parser implementation, focused GREEN, and bounded static validation exactly
  as specified in immutable 4AC Steps 2–4. Record actual RED, GREEN, skip,
  static-gate, scope, mode, freeze, and prohibition evidence in the Task
  ledger. Do not claim Ruff when unavailable and do not install it.

- [ ] **Step 3: Rebind the full accepted Plan chain, prove exact scope and
  freezes, then commit the sole implementation attempt.**

```bash
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
implementation_base="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$implementation_base"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
implementation_base_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$implementation_base_subject" = \
  "docs(task): record canonical-row authority plan reviews"
implementation_base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority plan reviews'
)"
test "$implementation_base_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$implementation_base"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
base_review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_review_paths" = "$task_file"
base_review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$implementation_base" |
    sort
)"
test "$base_review_range_paths" = "$task_file"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
base_review_task_mode="$(
  git ls-tree "$implementation_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_review_task_mode" = "100644"
base_review_test_mode="$(
  git ls-tree "$implementation_base" "$test_file" |
    awk '{print $1}'
)"
test "$base_review_test_mode" = "100644"
expected_implementation_paths="$(
  printf '%s\n' \
    "$task_file" \
    "$test_file" |
    sort
)"
test -n "$expected_implementation_paths"
actual_paths="$(
  {
    git diff --name-only "$implementation_base" -- &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$expected_implementation_paths"
git diff --exit-code "$implementation_base" -- . \
  ":(exclude)$task_file" \
  ":(exclude)$test_file"
task_mode="$(
  git ls-files -s "$task_file" |
    awk '{print $1}'
)"
test "$task_mode" = "100644"
test_mode="$(
  git ls-files -s "$test_file" |
    awk '{print $1}'
)"
test "$test_mode" = "100644"
git diff --check
git add "$task_file" "$test_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$expected_implementation_paths"
git commit -m \
  "fix(ci): close canonical-row authority proof"
implementation_commit="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$implementation_commit"
implementation_subject="$(
  git show -s --format=%s "$implementation_commit"
)"
test "$implementation_subject" = \
  "fix(ci): close canonical-row authority proof"
implementation_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'fix(ci): close canonical-row authority proof'
)"
test "$implementation_subject_count" -eq 1
assert_edge "$implementation_base" "$implementation_commit"
implementation_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_implementation_paths"
implementation_range_paths="$(
  git diff --name-only "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_range_paths" = "$expected_implementation_paths"
git diff --exit-code "$implementation_base..$implementation_commit" -- . \
  ":(exclude)$task_file" \
  ":(exclude)$test_file"
implementation_task_mode="$(
  git ls-tree "$implementation_commit" "$task_file" |
    awk '{print $1}'
)"
test "$implementation_task_mode" = "100644"
implementation_test_mode="$(
  git ls-tree "$implementation_commit" "$test_file" |
    awk '{print $1}'
)"
test "$implementation_test_mode" = "100644"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

- [ ] **Step 4: Independently review the exact implementation range and
  attest both full endpoints.**

  Each fresh reviewer independently runs:

```bash
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
implementation_commit="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$implementation_commit"
implementation_base="$(
  git rev-parse --verify "$implementation_commit^1"
)"
test -n "$implementation_base"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
implementation_base_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$implementation_base_subject" = \
  "docs(task): record canonical-row authority plan reviews"
implementation_base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority plan reviews'
)"
test "$implementation_base_subject_count" -eq 1
implementation_subject="$(
  git show -s --format=%s "$implementation_commit"
)"
test "$implementation_subject" = \
  "fix(ci): close canonical-row authority proof"
implementation_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'fix(ci): close canonical-row authority proof'
)"
test "$implementation_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$implementation_base"
assert_edge "$implementation_base" "$implementation_commit"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
base_review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_review_paths" = "$task_file"
base_review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$implementation_base" |
    sort
)"
test "$base_review_range_paths" = "$task_file"
expected_implementation_paths="$(
  printf '%s\n' \
    "$task_file" \
    "$test_file" |
    sort
)"
test -n "$expected_implementation_paths"
implementation_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_implementation_paths"
implementation_range_paths="$(
  git diff --name-only "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_range_paths" = "$expected_implementation_paths"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
base_review_task_mode="$(
  git ls-tree "$implementation_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_review_task_mode" = "100644"
base_review_test_mode="$(
  git ls-tree "$implementation_base" "$test_file" |
    awk '{print $1}'
)"
test "$base_review_test_mode" = "100644"
implementation_task_mode="$(
  git ls-tree "$implementation_commit" "$task_file" |
    awk '{print $1}'
)"
test "$implementation_task_mode" = "100644"
implementation_test_mode="$(
  git ls-tree "$implementation_commit" "$test_file" |
    awk '{print $1}'
)"
test "$implementation_test_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$implementation_commit"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  Each reviewer returns the full
  `$implementation_base..$implementation_commit` range with its verdict.
  Before either terminal path, the controller records the identical full range
  in the
  `T-TSDC-004R-4AF canonical-row implementation` matrix row.

- [ ] **Step 5: Record exactly one full-chain implementation-review
  checkpoint.**

  If and only if both implementation reviewers return `C0/I0/M0`, edit only
  the Task ledger and run:

```bash
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
implementation_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row implementation'
)"
test -n "$implementation_review_range"
implementation_base="${implementation_review_range%%..*}"
test -n "$implementation_base"
implementation_commit="${implementation_review_range##*..}"
test -n "$implementation_commit"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
verified_implementation_base="$(
  git rev-parse --verify "$implementation_base^{commit}"
)"
test "$verified_implementation_base" = "$implementation_base"
verified_implementation_commit="$(
  git rev-parse --verify "$implementation_commit^{commit}"
)"
test "$verified_implementation_commit" = "$implementation_commit"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
implementation_base_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$implementation_base_subject" = \
  "docs(task): record canonical-row authority plan reviews"
implementation_base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority plan reviews'
)"
test "$implementation_base_subject_count" -eq 1
implementation_subject="$(
  git show -s --format=%s "$implementation_commit"
)"
test "$implementation_subject" = \
  "fix(ci): close canonical-row authority proof"
implementation_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'fix(ci): close canonical-row authority proof'
)"
test "$implementation_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$implementation_base"
assert_edge "$implementation_base" "$implementation_commit"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
base_review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_review_paths" = "$task_file"
base_review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$implementation_base" |
    sort
)"
test "$base_review_range_paths" = "$task_file"
expected_implementation_paths="$(
  printf '%s\n' \
    "$task_file" \
    "$test_file" |
    sort
)"
test -n "$expected_implementation_paths"
implementation_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_implementation_paths"
implementation_range_paths="$(
  git diff --name-only "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_range_paths" = "$expected_implementation_paths"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
base_review_task_mode="$(
  git ls-tree "$implementation_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_review_task_mode" = "100644"
base_review_test_mode="$(
  git ls-tree "$implementation_base" "$test_file" |
    awk '{print $1}'
)"
test "$base_review_test_mode" = "100644"
implementation_task_mode="$(
  git ls-tree "$implementation_commit" "$task_file" |
    awk '{print $1}'
)"
test "$implementation_task_mode" = "100644"
implementation_test_mode="$(
  git ls-tree "$implementation_commit" "$test_file" |
    awk '{print $1}'
)"
test "$implementation_test_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$implementation_commit"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$task_file"
git commit -m \
  "docs(task): record canonical-row authority review"
review_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$review_checkpoint"
review_subject="$(
  git show -s --format=%s "$review_checkpoint"
)"
test "$review_subject" = \
  "docs(task): record canonical-row authority review"
review_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority review'
)"
test "$review_subject_count" -eq 1
assert_edge "$implementation_commit" "$review_checkpoint"
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = "$task_file"
review_range_paths="$(
  git diff --name-only "$implementation_commit..$review_checkpoint" |
    sort
)"
test "$review_range_paths" = "$task_file"
review_task_mode="$(
  git ls-tree "$review_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  Only this accepted checkpoint can authorize Task 4.5 after its independent
  Step 0 proof.

  If either reviewer is not `C0/I0/M0`, edit only the Task ledger and run the
  mutually exclusive rejected terminal session:

```bash
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
implementation_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row implementation'
)"
test -n "$implementation_review_range"
implementation_base="${implementation_review_range%%..*}"
test -n "$implementation_base"
implementation_commit="${implementation_review_range##*..}"
test -n "$implementation_commit"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
verified_implementation_base="$(
  git rev-parse --verify "$implementation_base^{commit}"
)"
test "$verified_implementation_base" = "$implementation_base"
verified_implementation_commit="$(
  git rev-parse --verify "$implementation_commit^{commit}"
)"
test "$verified_implementation_commit" = "$implementation_commit"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
implementation_base_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$implementation_base_subject" = \
  "docs(task): record canonical-row authority plan reviews"
implementation_base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority plan reviews'
)"
test "$implementation_base_subject_count" -eq 1
implementation_subject="$(
  git show -s --format=%s "$implementation_commit"
)"
test "$implementation_subject" = \
  "fix(ci): close canonical-row authority proof"
implementation_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'fix(ci): close canonical-row authority proof'
)"
test "$implementation_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$implementation_base"
assert_edge "$implementation_base" "$implementation_commit"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
base_review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_review_paths" = "$task_file"
base_review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$implementation_base" |
    sort
)"
test "$base_review_range_paths" = "$task_file"
expected_implementation_paths="$(
  printf '%s\n' \
    "$task_file" \
    "$test_file" |
    sort
)"
test -n "$expected_implementation_paths"
implementation_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_implementation_paths"
implementation_range_paths="$(
  git diff --name-only "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_range_paths" = "$expected_implementation_paths"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
base_review_task_mode="$(
  git ls-tree "$implementation_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_review_task_mode" = "100644"
base_review_test_mode="$(
  git ls-tree "$implementation_base" "$test_file" |
    awk '{print $1}'
)"
test "$base_review_test_mode" = "100644"
implementation_task_mode="$(
  git ls-tree "$implementation_commit" "$task_file" |
    awk '{print $1}'
)"
test "$implementation_task_mode" = "100644"
implementation_test_mode="$(
  git ls-tree "$implementation_commit" "$test_file" |
    awk '{print $1}'
)"
test "$implementation_test_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$implementation_commit"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$task_file"
git commit -m \
  "docs(task): record exhausted canonical-row authority review"
review_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$review_checkpoint"
review_subject="$(
  git show -s --format=%s "$review_checkpoint"
)"
test "$review_subject" = \
  "docs(task): record exhausted canonical-row authority review"
review_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted canonical-row authority review'
)"
test "$review_subject_count" -eq 1
assert_edge "$implementation_commit" "$review_checkpoint"
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = "$task_file"
review_range_paths="$(
  git diff --name-only "$implementation_commit..$review_checkpoint" |
    sort
)"
test "$review_range_paths" = "$task_file"
review_task_mode="$(
  git ls-tree "$review_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  The rejected checkpoint grants no retry or downstream authority.

#### T-TSDC-004R-4AG: Status-Based Silent-Success Proof (Plan-Only Successor)

**Historical non-executable provenance.** 4AG is rejected and exhausted at
its Task-only terminal. Its checklists and fenced proof text are retained only
to preserve the committed design record; they MUST NOT be run, resumed, or
used as authority. The sole executable future successor design is 4AH below.

- [ ] **Step 0: Bind the exhausted design boundary without reopening 4AF.**

  `D_AG` is exactly `737838fe80880b7eadbfb1c7e18d8dc251bcc8b9`, has sole
  subject `docs(task): record exhausted canonical-row authority review`, has
  parent `I` exactly `a7d05b0e5c0ffaeccde9e401450e696855cfb2b5`, changes this
  Task ledger only, and remains mode `100644`. Historical 4AF parser, test,
  command/argv/order, 61-family matrix, every Step 4 assertion other than the
  delta capture/evidence envelope, scopes, prohibitions, and files are frozen.
  No parser, product, workflow, validator, runtime, or test change is in this
  successor. TDD RED/GREEN is N/A: the framing oracle is negative/positive
  evidence, not a product change.

  Every 4AG proof block retains `set -euo pipefail` and
  `shopt -s inherit_errexit`. Each ordinary fallible command substitution is
  a standalone assignment whose immediately following command tests that same
  variable. The only framing exceptions are guarded production/oracle frame
  and oracle-result assignments. Their inner and outer branches each consume
  `$?` as their first command, and the next post-conditional command validates
  the frame sentinel or exact captured status before any bytes can be
  classified or discarded.

- [ ] **Step 1: Make P_AG and obtain its terminal Plan evidence.**

  Create `P_AG` as the single-parent successor of D_AG with exact subject
  `docs(plan): define status-based silent-success proof`, Plan plus Task paths
  only, and both modes `100644`. Two fresh independent Plan reviewers inspect
  exact `D_AG..P_AG`; both must return `C0/I0/M0`. If either does not, create
  Task-only `XP_AG` with exact subject
  `docs(task): record exhausted status-based silent-success plan review` and
  stop. If both do, create Task-only `B_AG` with exact subject
  `docs(task): record status-based silent-success plan reviews`. There is no
  correction inside 4AG. The present approval authorizes only Plan/Task
  drafting, P_AG, these fresh Plan reviews, and their accepted or rejected
  Task-only evidence; P_AG is not yet committed at this draft.

  Immediately after P_AG is committed, each fresh reviewer independently runs
  this immutable checkpoint proof and reports both printed full OIDs:

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
design_base="$(
  git rev-parse --verify \
    '737838fe80880b7eadbfb1c7e18d8dc251bcc8b9^{commit}'
)"
test "$design_base" = \
  "737838fe80880b7eadbfb1c7e18d8dc251bcc8b9"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted canonical-row authority review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted canonical-row authority review'
)"
test "$base_subject_count" -eq 1
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$plan_checkpoint"
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define status-based silent-success proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define status-based silent-success proof'
)"
test "$plan_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
expected_plan_paths="$(
  printf '%s\n' "$plan_file" "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" "$plan_file" |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$plan_checkpoint"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
printf 'REVIEWED_BASE=%s\nREVIEWED_HEAD=%s\n' \
  "$design_base" "$plan_checkpoint"
```

  The controller copies the identical full range and both completed verdicts
  into the single `T-TSDC-004R-4AG status-based silent-success Plan` row.
  The following one terminal session derives its branch from that row. The
  accepted cell values are exactly
  `C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES` and
  `C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES`; any other two
  completed C/I/M verdicts select XP_AG. Pending, malformed, duplicated, or
  divergent evidence fails before a commit:

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_attestation="$(
  python3 - "$task_file" <<'PY'
import pathlib
import re
import sys

label = "T-TSDC-004R-4AG status-based silent-success Plan"
try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("plan-review-read")
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("plan-review-row-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("plan-review-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("plan-review-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("plan-review-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("plan-review-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("plan-review-extra-range")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("plan-review-range")
complete = re.compile(r"^C[0-9]+/I[0-9]+/M[0-9]+; .+", re.ASCII)
if complete.fullmatch(cells[2]) is None or complete.fullmatch(cells[3]) is None:
    raise SystemExit("plan-review-incomplete")
accepted = (
    cells[2]
    == "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES"
    and cells[3]
    == "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES"
)
outcome = "accepted" if accepted else "rejected"
print(f"{match.group(1)}..{match.group(2)}\t{outcome}")
PY
)"
test -n "$plan_attestation"
plan_review_range="${plan_attestation%%$'\t'*}"
test -n "$plan_review_range"
review_outcome="${plan_attestation##*$'\t'}"
test "$review_outcome" = accepted || test "$review_outcome" = rejected
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "737838fe80880b7eadbfb1c7e18d8dc251bcc8b9"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted canonical-row authority review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted canonical-row authority review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define status-based silent-success proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define status-based silent-success proof'
)"
test "$plan_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
expected_plan_paths="$(
  printf '%s\n' "$plan_file" "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
plan_mode="$(
  git ls-tree "$plan_checkpoint" "$plan_file" |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$plan_checkpoint"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$task_file"
if [ "$review_outcome" = accepted ]; then
  terminal_subject='docs(task): record status-based silent-success plan reviews'
else
  terminal_subject='docs(task): record exhausted status-based silent-success plan review'
fi
git commit -m "$terminal_subject"
terminal_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$terminal_checkpoint"
recorded_subject="$(
  git show -s --format=%s "$terminal_checkpoint"
)"
test "$recorded_subject" = "$terminal_subject"
subject_count="$(
  git log --all --format='%s' |
    grep -Fxc "$terminal_subject"
)"
test "$subject_count" -eq 1
assert_edge "$plan_checkpoint" "$terminal_checkpoint"
terminal_paths="$(
  git diff-tree --no-commit-id --name-only -r "$terminal_checkpoint" |
    sort
)"
test "$terminal_paths" = "$task_file"
terminal_range_paths="$(
  git diff --name-only "$plan_checkpoint..$terminal_checkpoint" |
    sort
)"
test "$terminal_range_paths" = "$task_file"
terminal_task_mode="$(
  git ls-tree "$terminal_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$terminal_task_mode" = "100644"
terminal_head="$(
  git rev-parse HEAD
)"
test "$terminal_head" = "$terminal_checkpoint"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

- [ ] **Step 2: Use the strict status-based Step 4 delta envelope after a
  separate future approval.**

  Only after B_AG exists and the user separately approves one evidence-only
  revalidation attempt, run the frozen delta command exactly once without code
  edits. Retain `set -euo pipefail` and `shopt -s inherit_errexit`; admit only
  this exact external simple command in conditional context:

```bash
set -euo pipefail
shopt -s inherit_errexit
delta_sentinel=$'\x1e'
if delta_frame="$(
  if python3 \
      scripts/validation/check-target-surface-delta-contract.py \
      --mode advisory 2>&1; then
    delta_inner_status=$?
  else
    delta_inner_status=$?
  fi
  printf '%s' "$delta_sentinel"
  exit "$delta_inner_status"
)"; then
  delta_status=$?
else
  delta_status=$?
fi
case "$delta_frame" in
  *"$delta_sentinel") ;;
  *)
    unset delta_frame
    if [ "$delta_status" -eq 0 ]; then
      exit 125
    fi
    exit "$delta_status"
    ;;
esac
delta_body="${delta_frame%"$delta_sentinel"}"
unset delta_frame
if [[ -n "$delta_body" ]]; then
  delta_output_class=nonempty
else
  delta_output_class=empty
fi
unset delta_body
printf 'result status=%d output=%s\n' \
  "$delta_status" "$delta_output_class"
if [ "$delta_status" -ne 0 ]; then
  exit "$delta_status"
fi
```

  The sentinel is inside the guarded assignment, so trailing-newline-only
  output remains nonempty. Capture inner and outer status immediately through
  `if`/`else`; classify only `status=<n>` and `output=empty|nonempty`; unset
  the body promptly; never print or persist its raw body. Do not use `set +e`,
  `!`, `|| true`, `eval`, pipelines, temporary/raw-log files, or a second
  execution. Bash variables cannot represent NUL, so this is bounded to the
  existing bounded value-free text validator.

  Future adversarial proof uses local shell functions, never `bash -c`:
  success with zero bytes must classify `0/empty`; success with newline-only
  output must classify `0/nonempty`; stderr-only output containing a fixed raw
  marker must classify `0/nonempty` without emitting that marker; a deliberately
  corrupted success frame must exit reserved status `125`; and status `23`
  with empty and nonempty combined output must produce only its value-free
  class, exit exactly `23`, emit no successor marker, and invoke the function
  once. The oracle must separately assert that no raw stdout or stderr marker
  appears in persisted or displayed evidence.

  The future revalidation runs this local-function oracle before the exact
  external validator command. It is self-contained, uses no file or second
  execution, and proves that nonzero and corrupt frames never reach the
  successor marker:

```bash
set -euo pipefail
shopt -s inherit_errexit
produce_empty() {
  probe_count=$((probe_count + 1))
  return 0
}
produce_newline() {
  probe_count=$((probe_count + 1))
  printf '\n'
}
produce_stderr_marker() {
  probe_count=$((probe_count + 1))
  printf '%s' 'RAW-STDERR-MARKER' >&2
}
produce_23_empty() {
  probe_count=$((probe_count + 1))
  return 23
}
produce_23_nonempty() {
  probe_count=$((probe_count + 1))
  printf '%s' 'RAW-NONZERO-MARKER'
  return 23
}
run_probe() {
  local producer="$1"
  local frame_mode="$2"
  local probe_sentinel=$'\x1e'
  local probe_frame
  local probe_inner_status
  local probe_status
  local probe_body
  local probe_output_class
  probe_count=0
  if probe_frame="$(
    if "$producer" 2>&1; then
      probe_inner_status=$?
    else
      probe_inner_status=$?
    fi
    if [ "$probe_count" -ne 1 ]; then
      exit 126
    fi
    if [ "$frame_mode" = intact ]; then
      printf '%s' "$probe_sentinel"
    fi
    exit "$probe_inner_status"
  )"; then
    probe_status=$?
  else
    probe_status=$?
  fi
  case "$probe_frame" in
    *"$probe_sentinel") ;;
    *)
      unset probe_frame
      if [ "$probe_status" -eq 0 ]; then
        exit 125
      fi
      exit "$probe_status"
      ;;
  esac
  probe_body="${probe_frame%"$probe_sentinel"}"
  unset probe_frame
  if [[ -n "$probe_body" ]]; then
    probe_output_class=nonempty
  else
    probe_output_class=empty
  fi
  unset probe_body
  printf 'result status=%d output=%s\n' \
    "$probe_status" "$probe_output_class"
  if [ "$probe_status" -ne 0 ]; then
    exit "$probe_status"
  fi
  printf '%s\n' 'successor-marker'
}
if probe_output="$(run_probe produce_empty intact)"; then
  probe_status=$?
else
  probe_status=$?
fi
test "$probe_status" -eq 0
test "$probe_output" = $'result status=0 output=empty\nsuccessor-marker'
if probe_output="$(run_probe produce_newline intact)"; then
  probe_status=$?
else
  probe_status=$?
fi
test "$probe_status" -eq 0
test "$probe_output" = \
  $'result status=0 output=nonempty\nsuccessor-marker'
if probe_output="$(run_probe produce_stderr_marker intact)"; then
  probe_status=$?
else
  probe_status=$?
fi
test "$probe_status" -eq 0
test "$probe_output" = \
  $'result status=0 output=nonempty\nsuccessor-marker'
case "$probe_output" in
  *RAW-STDERR-MARKER*) exit 1 ;;
  *) ;;
esac
if probe_output="$(run_probe produce_23_empty intact)"; then
  probe_status=$?
else
  probe_status=$?
fi
test "$probe_status" -eq 23
test "$probe_output" = 'result status=23 output=empty'
case "$probe_output" in
  *successor-marker*) exit 1 ;;
  *) ;;
esac
if probe_output="$(run_probe produce_23_nonempty intact)"; then
  probe_status=$?
else
  probe_status=$?
fi
test "$probe_status" -eq 23
test "$probe_output" = 'result status=23 output=nonempty'
case "$probe_output" in
  *RAW-NONZERO-MARKER*|*successor-marker*) exit 1 ;;
  *) ;;
esac
if probe_output="$(run_probe produce_empty corrupt)"; then
  probe_status=$?
else
  probe_status=$?
fi
test "$probe_status" -eq 125
test -z "$probe_output"
```

- [ ] **Step 3: Rebind immutable history and record E_AG only after that
  approved revalidation.**

  The historical code range is exactly
  `7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5`.
  Prove the test-file blob at B_AG equals I, every commit after I through B_AG
  changes only allowed Plan/Task evidence, and test mode remains `100644`.
  Do not cherry-pick, amend, revert, reapply, or create empty commits. Create
  Task-only logical evidence `E_AG` after the one revalidation with exact
  subject `docs(task): record status-based silent-success revalidation`.
  Fresh specification and quality/security reviewers inspect both the immutable
  historical implementation range and exact B_AG..E_AG evidence range, attest
  all four full OIDs, and prove `B_4AF -> I -> D_AG -> P_AG -> B_AG -> E_AG`.
  The accepted terminal is Task-only `R_AG`, exact subject
  `docs(task): record status-based silent-success review`; rejection is
  Task-only `XE_AG`, exact subject
  `docs(task): record exhausted status-based silent-success review`. Only
  accepted R_AG unlocks Task 4.5.

  After the separately approved status-based ladder passes, edit only the Task
  ledger and run this E_AG commit proof. It derives P_AG from the accepted Plan
  row, binds B_AG from clean `HEAD`, proves the immutable test blob, and
  records no raw command output:

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  python3 - "$task_file" <<'PY'
import pathlib
import re
import sys

label = "T-TSDC-004R-4AG status-based silent-success Plan"
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("plan-review-row-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("plan-review-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("plan-review-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("plan-review-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("plan-review-label")
if cells[2] != "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES":
    raise SystemExit("plan-review-spec")
if cells[3] != "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES":
    raise SystemExit("plan-review-quality")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("plan-review-extra-range")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("plan-review-range")
print(f"{match.group(1)}..{match.group(2)}")
PY
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "737838fe80880b7eadbfb1c7e18d8dc251bcc8b9"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
implementation_base="$(
  git rev-parse --verify \
    '7e32c37cafde08b108ee33e3439cda3aea336961^{commit}'
)"
test "$implementation_base" = \
  "7e32c37cafde08b108ee33e3439cda3aea336961"
implementation_commit="$(
  git rev-parse --verify \
    'a7d05b0e5c0ffaeccde9e401450e696855cfb2b5^{commit}'
)"
test "$implementation_commit" = \
  "a7d05b0e5c0ffaeccde9e401450e696855cfb2b5"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
evidence_base="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$evidence_base"
implementation_base_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$implementation_base_subject" = \
  "docs(task): record canonical-row authority plan reviews"
implementation_subject="$(
  git show -s --format=%s "$implementation_commit"
)"
test "$implementation_subject" = \
  "fix(ci): close canonical-row authority proof"
design_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$design_subject" = \
  "docs(task): record exhausted canonical-row authority review"
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define status-based silent-success proof"
evidence_base_subject="$(
  git show -s --format=%s "$evidence_base"
)"
test "$evidence_base_subject" = \
  "docs(task): record status-based silent-success plan reviews"
for expected_subject in \
  'docs(task): record canonical-row authority plan reviews' \
  'fix(ci): close canonical-row authority proof' \
  'docs(task): record exhausted canonical-row authority review' \
  'docs(plan): define status-based silent-success proof' \
  'docs(task): record status-based silent-success plan reviews'
do
  subject_count="$(
    git log --all --format='%s' |
      grep -Fxc "$expected_subject"
  )"
  test "$subject_count" -eq 1
done
assert_edge "$implementation_base" "$implementation_commit"
assert_edge "$implementation_commit" "$design_base"
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$evidence_base"
expected_plan_paths="$(
  printf '%s\n' "$plan_file" "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
expected_implementation_paths="$(
  printf '%s\n' "$task_file" "$test_file" |
    sort
)"
test -n "$expected_implementation_paths"
implementation_base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$implementation_base_paths" = "$task_file"
implementation_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_implementation_paths"
design_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$design_paths" = "$task_file"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
evidence_base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$evidence_base" |
    sort
)"
test "$evidence_base_paths" = "$task_file"
evidence_base_range_paths="$(
  git diff --name-only "$plan_checkpoint..$evidence_base" |
    sort
)"
test "$evidence_base_range_paths" = "$task_file"
post_implementation_paths="$(
  git diff --name-only "$implementation_commit..$evidence_base" |
    sort
)"
test "$post_implementation_paths" = "$expected_plan_paths"
for commit_path in \
  "$implementation_base:$task_file" \
  "$implementation_commit:$task_file" \
  "$implementation_commit:$test_file" \
  "$design_base:$task_file" \
  "$plan_checkpoint:$plan_file" \
  "$plan_checkpoint:$task_file" \
  "$evidence_base:$task_file" \
  "$evidence_base:$test_file"
do
  tree_mode="$(
    git ls-tree "${commit_path%%:*}" "${commit_path#*:}" |
      awk '{print $1}'
  )"
  test "$tree_mode" = "100644"
done
implementation_blob="$(
  git rev-parse "$implementation_commit:$test_file"
)"
test -n "$implementation_blob"
evidence_base_blob="$(
  git rev-parse "$evidence_base:$test_file"
)"
test "$evidence_base_blob" = "$implementation_blob"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$task_file"
git commit -m \
  "docs(task): record status-based silent-success revalidation"
evidence_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$evidence_checkpoint"
evidence_subject="$(
  git show -s --format=%s "$evidence_checkpoint"
)"
test "$evidence_subject" = \
  "docs(task): record status-based silent-success revalidation"
evidence_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record status-based silent-success revalidation'
)"
test "$evidence_subject_count" -eq 1
assert_edge "$evidence_base" "$evidence_checkpoint"
evidence_paths="$(
  git diff-tree --no-commit-id --name-only -r "$evidence_checkpoint" |
    sort
)"
test "$evidence_paths" = "$task_file"
evidence_range_paths="$(
  git diff --name-only "$evidence_base..$evidence_checkpoint" |
    sort
)"
test "$evidence_range_paths" = "$task_file"
evidence_mode="$(
  git ls-tree "$evidence_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$evidence_mode" = "100644"
evidence_blob="$(
  git rev-parse "$evidence_checkpoint:$test_file"
)"
test "$evidence_blob" = "$implementation_blob"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$evidence_checkpoint"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  Both composite reviewers then report the same two exact ranges: historical
  `B_4AF..I` and new `B_AG..E_AG`. The controller copies their completed
  verdicts into both canonical implementation/revalidation rows and edits only
  the Task ledger. This terminal session requires the two rows to carry
  identical verdicts. It selects R_AG only when both are the exact accepted
  C0/I0/M0 forms; any other two completed verdicts select XE_AG:

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
review_attestation="$(
  python3 - "$task_file" <<'PY'
import pathlib
import re
import sys

labels = (
    "T-TSDC-004R-4AG status-based silent-success Plan",
    "T-TSDC-004R-4AG frozen canonical-row implementation",
    "T-TSDC-004R-4AG status-based revalidation",
)
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
found = {label: [] for label in labels}
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell in found:
        found[first_cell].append(line)
if any(len(found[label]) != 1 for label in labels):
    raise SystemExit("review-row-count")
rows = []
for label in labels:
    row = found[label][0]
    if not row.startswith("|") or not row.endswith("|"):
        raise SystemExit("review-cell-count")
    if "\\|" in row or "\\`" in row:
        raise SystemExit("review-escape")
    parts = row.split("|")
    if len(parts) != 9 or parts[0] or parts[-1]:
        raise SystemExit("review-cell-count")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if len(cells) != 7 or cells[0] != label:
        raise SystemExit("review-label")
    rows.append(cells)
ranges = []
for cells in rows:
    for index, cell in enumerate(cells):
        if index != 4 and ("`" in cell or ".." in cell):
            raise SystemExit("review-extra-range")
    match = re.fullmatch(
        r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
        cells[4],
        flags=re.ASCII,
    )
    if match is None:
        raise SystemExit("review-range")
    ranges.append(f"{match.group(1)}..{match.group(2)}")
accepted_spec = "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES"
accepted_quality = "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES"
if rows[0][2] != "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES":
    raise SystemExit("plan-review-spec")
if rows[0][3] != "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES":
    raise SystemExit("plan-review-quality")
complete = re.compile(r"^C[0-9]+/I[0-9]+/M[0-9]+; .+", re.ASCII)
for cells in rows[1:]:
    if complete.fullmatch(cells[2]) is None:
        raise SystemExit("composite-spec-incomplete")
    if complete.fullmatch(cells[3]) is None:
        raise SystemExit("composite-quality-incomplete")
if rows[1][2:4] != rows[2][2:4]:
    raise SystemExit("composite-verdict-divergence")
accepted = (
    rows[1][2] == accepted_spec
    and rows[1][3] == accepted_quality
)
outcome = "accepted" if accepted else "rejected"
print("\t".join((*ranges, outcome)))
PY
)"
test -n "$review_attestation"
plan_review_range="${review_attestation%%$'\t'*}"
test -n "$plan_review_range"
attestation_tail="${review_attestation#*$'\t'}"
test -n "$attestation_tail"
implementation_review_range="${attestation_tail%%$'\t'*}"
test -n "$implementation_review_range"
attestation_tail="${attestation_tail#*$'\t'}"
test -n "$attestation_tail"
revalidation_review_range="${attestation_tail%%$'\t'*}"
test -n "$revalidation_review_range"
review_outcome="${attestation_tail##*$'\t'}"
test "$review_outcome" = accepted || test "$review_outcome" = rejected
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "737838fe80880b7eadbfb1c7e18d8dc251bcc8b9"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
implementation_base="${implementation_review_range%%..*}"
test "$implementation_base" = \
  "7e32c37cafde08b108ee33e3439cda3aea336961"
implementation_commit="${implementation_review_range##*..}"
test "$implementation_commit" = \
  "a7d05b0e5c0ffaeccde9e401450e696855cfb2b5"
evidence_base="${revalidation_review_range%%..*}"
test -n "$evidence_base"
evidence_checkpoint="${revalidation_review_range##*..}"
test -n "$evidence_checkpoint"
for bound_commit in \
  "$implementation_base" "$implementation_commit" "$design_base" \
  "$plan_checkpoint" "$evidence_base" "$evidence_checkpoint"
do
  verified_commit="$(
    git rev-parse --verify "$bound_commit^{commit}"
  )"
  test "$verified_commit" = "$bound_commit"
done
expected_subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record status-based silent-success plan reviews'
  'docs(task): record status-based silent-success revalidation'
)
bound_commits=(
  "$implementation_base" "$implementation_commit" "$design_base"
  "$plan_checkpoint" "$evidence_base" "$evidence_checkpoint"
)
for index in "${!bound_commits[@]}"; do
  bound_subject="$(
    git show -s --format=%s "${bound_commits[$index]}"
  )"
  test "$bound_subject" = "${expected_subjects[$index]}"
  subject_count="$(
    git log --all --format='%s' |
      grep -Fxc "${expected_subjects[$index]}"
  )"
  test "$subject_count" -eq 1
done
assert_edge "$implementation_base" "$implementation_commit"
assert_edge "$implementation_commit" "$design_base"
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$evidence_base"
assert_edge "$evidence_base" "$evidence_checkpoint"
expected_plan_paths="$(
  printf '%s\n' "$plan_file" "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
expected_implementation_paths="$(
  printf '%s\n' "$task_file" "$test_file" |
    sort
)"
test -n "$expected_implementation_paths"
expected_paths=(
  "$task_file"
  "$expected_implementation_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$task_file"
)
for index in "${!bound_commits[@]}"; do
  commit_paths="$(
    git diff-tree --no-commit-id --name-only -r \
      "${bound_commits[$index]}" |
      sort
  )"
  test "$commit_paths" = "${expected_paths[$index]}"
done
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
implementation_range_paths="$(
  git diff --name-only "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_range_paths" = "$expected_implementation_paths"
base_range_paths="$(
  git diff --name-only "$plan_checkpoint..$evidence_base" |
    sort
)"
test "$base_range_paths" = "$task_file"
evidence_range_paths="$(
  git diff --name-only "$evidence_base..$evidence_checkpoint" |
    sort
)"
test "$evidence_range_paths" = "$task_file"
for commit_path in \
  "$implementation_base:$task_file" \
  "$implementation_commit:$task_file" \
  "$implementation_commit:$test_file" \
  "$design_base:$task_file" \
  "$plan_checkpoint:$plan_file" \
  "$plan_checkpoint:$task_file" \
  "$evidence_base:$task_file" \
  "$evidence_base:$test_file" \
  "$evidence_checkpoint:$task_file" \
  "$evidence_checkpoint:$test_file"
do
  tree_mode="$(
    git ls-tree "${commit_path%%:*}" "${commit_path#*:}" |
      awk '{print $1}'
  )"
  test "$tree_mode" = "100644"
done
implementation_blob="$(
  git rev-parse "$implementation_commit:$test_file"
)"
test -n "$implementation_blob"
evidence_base_blob="$(
  git rev-parse "$evidence_base:$test_file"
)"
test "$evidence_base_blob" = "$implementation_blob"
evidence_blob="$(
  git rev-parse "$evidence_checkpoint:$test_file"
)"
test "$evidence_blob" = "$implementation_blob"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$evidence_checkpoint"
actual_paths="$(
  {
    git diff --name-only &&
      git diff --cached --name-only &&
      git ls-files --others --exclude-standard
  } | sort -u
)"
test "$actual_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(
  git diff --cached --name-only |
    sort
)"
test "$cached_paths" = "$task_file"
if [ "$review_outcome" = accepted ]; then
  terminal_subject='docs(task): record status-based silent-success review'
else
  terminal_subject='docs(task): record exhausted status-based silent-success review'
fi
git commit -m "$terminal_subject"
terminal_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$terminal_checkpoint"
terminal_subject_actual="$(
  git show -s --format=%s "$terminal_checkpoint"
)"
test "$terminal_subject_actual" = "$terminal_subject"
terminal_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc "$terminal_subject"
)"
test "$terminal_subject_count" -eq 1
assert_edge "$evidence_checkpoint" "$terminal_checkpoint"
terminal_paths="$(
  git diff-tree --no-commit-id --name-only -r "$terminal_checkpoint" |
    sort
)"
test "$terminal_paths" = "$task_file"
terminal_range_paths="$(
  git diff --name-only "$evidence_checkpoint..$terminal_checkpoint" |
    sort
)"
test "$terminal_range_paths" = "$task_file"
terminal_mode="$(
  git ls-tree "$terminal_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$terminal_mode" = "100644"
terminal_blob="$(
  git rev-parse "$terminal_checkpoint:$test_file"
)"
test "$terminal_blob" = "$implementation_blob"
terminal_head="$(
  git rev-parse HEAD
)"
test "$terminal_head" = "$terminal_checkpoint"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  R_AG authorizes Task 4.5 only when `review_outcome=accepted`; XE_AG is
  terminal and grants no correction, retry, Wave C, or downstream authority.

#### T-TSDC-004R-4AH: Collision-Safe Disposition Proof (Historical Rejected Successor)

4AH is rejected/exhausted at XP_AH
`88f55837be251318cd697bd8a1ab3a4f0ed1a824`. Committed 4AG and 4AH evidence is
historical, non-executable provenance only. The quality/security Plan review
rejected the split AH-3/AH-4 session boundary; B_AH, E_AH, R_AH, and XE_AH were
not created. Every block below is preserved as historical design evidence and
grants no execution or downstream authority.

- [ ] **Step AH-1: Commit and prove P_AH.**

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_subject='docs(plan): define collision-safe disposition proof'
head_before="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_before" = "$d_ah"
d_subject="$(git show -s --format=%s "$d_ah")"
test "$d_subject" = 'docs(task): record exhausted status-based silent-success plan review'
dirty_paths="$({ git diff --name-only; git diff --cached --name-only; git ls-files --others --exclude-standard; } | sort -u)"
expected_paths="$(printf '%s\n' "$plan_file" "$task_file" | sort)"
test "$dirty_paths" = "$expected_paths"
git diff --check
git add "$plan_file" "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$expected_paths"
git commit -m "$p_subject"
p_ah="$(git rev-parse --verify 'HEAD^{commit}')"
test -n "$p_ah"
p_actual_subject="$(git show -s --format=%s "$p_ah")"
test "$p_actual_subject" = "$p_subject"
p_subject_count="$(git log --all --format='%s' | grep -Fxc "$p_subject")"
test "$p_subject_count" -eq 1
p_parent_count="$(git rev-list --parents -n 1 "$p_ah" | awk '{print NF - 1}')"
test "$p_parent_count" -eq 1
p_parent="$(git rev-parse "$p_ah^1")"
test "$p_parent" = "$d_ah"
p_distance="$(git rev-list --count "$d_ah..$p_ah")"
test "$p_distance" -eq 1
p_paths="$(git diff-tree --no-commit-id --name-only -r "$p_ah" | sort)"
test "$p_paths" = "$expected_paths"
p_range_paths="$(git diff --name-only "$d_ah..$p_ah" | sort)"
test "$p_range_paths" = "$expected_paths"
for path in "$plan_file" "$task_file"; do
  mode="$(git ls-tree "$p_ah" "$path" | awk '{print $1}')"
  test "$mode" = 100644
done
python3 - "$task_file" <<'PY'
import pathlib
import sys


def section(text, start_heading, end_heading):
    start_marker = f"{start_heading}\n"
    end_marker = f"{end_heading}\n"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise SystemExit("p-ah-section-count")
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    return text[start:end]


def exact_row(body, label, expected):
    candidates = []
    for source_line in body.splitlines():
        line = source_line.strip(" \t")
        view = line[1:] if line.startswith("|") else line
        separator = view.find("|")
        if separator >= 0 and view[:separator].strip(" \t") == label:
            candidates.append(line)
    if len(candidates) != 1:
        raise SystemExit(f"p-ah-row-count:{label}")
    row = candidates[0]
    if not row.startswith("|") or not row.endswith("|") or "\\|" in row:
        raise SystemExit(f"p-ah-row-shape:{label}")
    parts = row.split("|")
    if len(parts) != len(expected) + 2 or parts[0] or parts[-1]:
        raise SystemExit(f"p-ah-row-cells:{label}")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if cells != expected:
        raise SystemExit(f"p-ah-row-values:{label}")


text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
work = section(text, "## Work Breakdown", "## Work Log")
validation = section(text, "### Task execution evidence", "### T-TSDC-001 bounded implementation evidence")
reviews = section(text, "## Review Evidence", "## Commit Ledger")
ledger = section(text, "## Commit Ledger", "## Deferred and Blocked Items")
deferred = section(text, "## Deferred and Blocked Items", "## Related Documents")

exact_row(work, "T-TSDC-004R-4AH", [
    "T-TSDC-004R-4AH",
    "Define collision-safe byte classification and truthful disposition proof without changing frozen implementation",
    "Plan/evidence",
    "TSDC-010–014",
    "fresh Plan reviews pending",
    "controller and fresh independent reviewers",
    "active Plan-only checkpoint; P_AH committed and resolved by its exact unique subject; fresh Plan reviews pending; no downstream authority",
])
exact_row(validation, "T-TSDC-004", [
    "T-TSDC-004",
    "Historical 4AF RED evidence is preserved; 4AG is rejected history and 4AH adds no product RED because parser/test content is frozen.",
    "Historical GREEN evidence is preserved; 4AH executes no tests, validators, wrapper, or revalidation.",
    "P_AH committed and resolved by its exact unique subject; fresh Plan reviews are pending; no downstream authority exists.",
    "active Plan-only; P_AH committed and resolved by its exact unique subject; fresh Plan reviews pending; no downstream authority",
])
exact_row(reviews, "T-TSDC-004R-4AH collision-safe disposition Plan", [
    "T-TSDC-004R-4AH collision-safe disposition Plan",
    "Controller",
    "pending fresh independent review",
    "pending fresh independent review",
    "awaiting exact reviewed range",
    "checkpoint committed; fresh Plan reviews pending; no downstream authority",
    "P_AH committed and resolved by its exact unique subject; no future OID is claimed in its own tree",
])
exact_row(ledger, "T-TSDC-004R-4AH Plan checkpoint P_AH", [
    "T-TSDC-004R-4AH Plan checkpoint P_AH",
    "Define collision-safe disposition proof",
    "`docs(plan): define collision-safe disposition proof`",
    "resolved by this exact unique subject",
    "P_AH committed; resolved by its exact unique subject; fresh Plan reviews pending; no downstream authority. Plan + Task only from D_AH; both modes `100644`; no future OID is claimed in its own tree.",
])
exact_row(deferred, "T-TSDC-004R-3 atomic projection cutover", [
    "T-TSDC-004R-3 atomic projection cutover",
    "blocked; 4AH Plan reviews pending",
    "Historical 4AF and rejected 4AG evidence remain frozen. P_AH committed and resolved by its exact unique subject; fresh Plan reviews pending; no downstream authority.",
    "await fresh 4AH Plan reviews and exactly one B_AH or XP_AH terminal; no correction, tests, revalidation, Wave C, downstream work, runtime, or remote action",
])
handoff = "Current 4AH final handoff: P_AH committed; resolved by its exact unique subject; fresh Plan reviews pending; no downstream authority."
if deferred.count(handoff) != 1:
    raise SystemExit("p-ah-final-handoff")
PY
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

At the P_AH tree the canonical row is exactly:

| Review unit | Owner | Specification | Quality/security | Reviewed range | Disposition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-004R-4AH collision-safe disposition Plan | Controller | pending fresh independent review | pending fresh independent review | awaiting exact reviewed range | checkpoint committed; fresh Plan reviews pending; no downstream authority | P_AH committed and resolved by its exact unique subject; no future OID is claimed in its own tree |

- [ ] **Step AH-2: Parse completed Plan reviews and commit one terminal.**

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
b_4af=7e32c37cafde08b108ee33e3439cda3aea336961
i=a7d05b0e5c0ffaeccde9e401450e696855cfb2b5
d_ag=737838fe80880b7eadbfb1c7e18d8dc251bcc8b9
p_ag=f2a4b5041222c48f392bc251eae014655cee7b7c
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_subject='docs(plan): define collision-safe disposition proof'
subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record exhausted status-based silent-success plan review'
  "$p_subject"
)
commits=("$b_4af" "$i" "$d_ag" "$p_ag" "$d_ah")
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(git rev-list --count "$parent..$child")"
  test "$distance" -eq 1
  parent_count="$(git rev-list --parents -n 1 "$child" | awk '{print NF - 1}')"
  test "$parent_count" -eq 1
  first_parent="$(git rev-parse "$child^1")"
  test "$first_parent" = "$parent"
}
assert_commit_paths() {
  local commit="$1"
  shift
  local actual
  local expected
  actual="$(git diff-tree --no-commit-id --name-only -r "$commit" | sort)"
  expected="$(printf '%s\n' "$@" | sort)"
  test "$actual" = "$expected"
}
assert_range_paths() {
  local range="$1"
  shift
  local actual
  local expected
  actual="$(git diff --name-only "$range" | sort)"
  expected="$(printf '%s\n' "$@" | sort)"
  test "$actual" = "$expected"
}
assert_modes() {
  local commit="$1"
  shift
  local mode
  local path
  for path in "$@"; do
    mode="$(git ls-tree "$commit" "$path" | awk '{print $1}')"
    test "$mode" = 100644
  done
}
p_subject_count="$(git log --all --format='%s' | grep -Fxc "$p_subject")"
test "$p_subject_count" -eq 1
p_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$p_subject" '$2 == s {print $1}')"
test -n "$p_ah"
commits+=("$p_ah")
for index in "${!commits[@]}"; do
  actual_subject="$(git show -s --format=%s "${commits[$index]}")"
  test "$actual_subject" = "${subjects[$index]}"
  subject_count="$(git log --all --format='%s' | grep -Fxc "${subjects[$index]}")"
  test "$subject_count" -eq 1
done
assert_edge "$b_4af" "$i"
assert_edge "$i" "$d_ag"
assert_edge "$d_ag" "$p_ag"
assert_edge "$p_ag" "$d_ah"
assert_edge "$d_ah" "$p_ah"
head_commit="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_commit" = "$p_ah"
assert_commit_paths "$b_4af" "$task_file"
assert_commit_paths "$i" "$task_file" "$test_file"
assert_commit_paths "$d_ag" "$task_file"
assert_commit_paths "$p_ag" "$plan_file" "$task_file"
assert_commit_paths "$d_ah" "$task_file"
assert_commit_paths "$p_ah" "$plan_file" "$task_file"
assert_range_paths "$b_4af..$i" "$task_file" "$test_file"
assert_range_paths "$d_ah..$p_ah" "$plan_file" "$task_file"
for commit in "${commits[@]}"; do
  assert_modes "$commit" "$plan_file" "$task_file" "$test_file"
done
implementation_blob="$(git rev-parse "$i:$test_file")"
p_ah_blob="$(git rev-parse "$p_ah:$test_file")"
test "$p_ah_blob" = "$implementation_blob"
dirty_paths="$({ git diff --name-only; git diff --cached --name-only; git ls-files --others --exclude-standard; } | sort -u)"
test "$dirty_paths" = "$task_file"
selection="$({ python3 - "$task_file" "$d_ah" "$p_ah" <<'PY'
import pathlib
import re
import sys

label = "T-TSDC-004R-4AH collision-safe disposition Plan"
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator >= 0 and candidate_view[:separator].strip(" \t") == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("plan-candidate-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("plan-shape")
if "\\|" in row or "\\`" in row:
    raise SystemExit("plan-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("plan-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("plan-label")
if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
    raise SystemExit("plan-extra-range-token")
if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
    raise SystemExit("plan-range-shape")
if cells[4] != f"`{sys.argv[2]}..{sys.argv[3]}`":
    raise SystemExit("plan-range")
spec_re = r"C\d+/I\d+/M\d+; SPEC_COMPLIANCE (YES|NO); IMPLEMENTATION_READY (YES|NO)"
quality_re = r"C\d+/I\d+/M\d+; QUALITY_SECURITY (PASS|FAIL); IMPLEMENTATION_READY (YES|NO)"
if re.fullmatch(spec_re, cells[2], flags=re.ASCII) is None:
    raise SystemExit("plan-spec-verdict")
if re.fullmatch(quality_re, cells[3], flags=re.ASCII) is None:
    raise SystemExit("plan-quality-verdict")
accepted = (
    cells[2] == "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES"
    and cells[3] == "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES"
)
expected = (
    (
        "accepted; B_AH resolved by its exact unique subject",
        "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
    )
    if accepted
    else (
        "rejected/exhausted; XP_AH resolved by its exact unique subject",
        "One or both fresh Plan reviews rejected; no correction, revalidation, or Wave C authority",
    )
)
if tuple(cells[5:7]) != expected:
    raise SystemExit("plan-outcome-pair")
print("B_AH" if accepted else "XP_AH")
PY
})"
test "$selection" = B_AH || test "$selection" = XP_AH
case "$selection" in
  B_AH)
    terminal_subject='docs(task): record collision-safe disposition plan reviews'
    ;;
  XP_AH)
    terminal_subject='docs(task): record exhausted collision-safe disposition plan review'
    ;;
esac
git diff --check
git add "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$task_file"
git commit -m "$terminal_subject"
terminal="$(git rev-parse --verify 'HEAD^{commit}')"
test -n "$terminal"
actual_subject="$(git show -s --format=%s "$terminal")"
test "$actual_subject" = "$terminal_subject"
subject_count="$(git log --all --format='%s' | grep -Fxc "$terminal_subject")"
test "$subject_count" -eq 1
parent_count="$(git rev-list --parents -n 1 "$terminal" | awk '{print NF - 1}')"
test "$parent_count" -eq 1
parent="$(git rev-parse "$terminal^1")"
test "$parent" = "$p_ah"
distance="$(git rev-list --count "$p_ah..$terminal")"
test "$distance" -eq 1
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$terminal" | sort)"
test "$commit_paths" = "$task_file"
range_paths="$(git diff --name-only "$p_ah..$terminal" | sort)"
test "$range_paths" = "$task_file"
mode="$(git ls-tree "$terminal" "$task_file" | awk '{print $1}')"
test "$mode" = 100644
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

XP_AH is terminal. Accepted B_AH still grants no revalidation or Wave C
authority. A separate user approval must name the resolved full B_AH OID
before any remaining 4AH block may execute.

- [ ] **Step AH-3: Run the one approved byte-safe advisory revalidation.**

  This is one self-contained Bash block. The inline Python oracle covers every
  byte/status case before one counted real validator call. It preserves the
  caller's cwd, environment, and stdin, emits no raw child bytes, and creates
  no temporary or persistent raw-output artifact.

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
b_4af=7e32c37cafde08b108ee33e3439cda3aea336961
i=a7d05b0e5c0ffaeccde9e401450e696855cfb2b5
d_ag=737838fe80880b7eadbfb1c7e18d8dc251bcc8b9
p_ag=f2a4b5041222c48f392bc251eae014655cee7b7c
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_subject='docs(plan): define collision-safe disposition proof'
b_subject='docs(task): record collision-safe disposition plan reviews'
approved_b_ah_oid="${APPROVED_B_AH_OID:?explicit approved B_AH OID required}"
[[ "$approved_b_ah_oid" =~ ^[0-9a-f]{40}$ ]]
subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record exhausted status-based silent-success plan review'
  "$p_subject"
  "$b_subject"
)
commits=("$b_4af" "$i" "$d_ag" "$p_ag" "$d_ah")
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(git rev-list --count "$parent..$child")"
  test "$distance" -eq 1
  parent_count="$(git rev-list --parents -n 1 "$child" | awk '{print NF - 1}')"
  test "$parent_count" -eq 1
  first_parent="$(git rev-parse "$child^1")"
  test "$first_parent" = "$parent"
}
assert_commit_paths() {
  local commit="$1"
  shift
  local actual
  local expected
  actual="$(git diff-tree --no-commit-id --name-only -r "$commit" | sort)"
  expected="$(printf '%s\n' "$@" | sort)"
  test "$actual" = "$expected"
}
assert_range_paths() {
  local range="$1"
  shift
  local actual
  local expected
  actual="$(git diff --name-only "$range" | sort)"
  expected="$(printf '%s\n' "$@" | sort)"
  test "$actual" = "$expected"
}
assert_modes() {
  local commit="$1"
  shift
  local mode
  local path
  for path in "$@"; do
    mode="$(git ls-tree "$commit" "$path" | awk '{print $1}')"
    test "$mode" = 100644
  done
}
p_count="$(git log --all --format='%s' | grep -Fxc "$p_subject")"
test "$p_count" -eq 1
p_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$p_subject" '$2 == s {print $1}')"
test -n "$p_ah"
b_count="$(git log --all --format='%s' | grep -Fxc "$b_subject")"
test "$b_count" -eq 1
b_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$b_subject" '$2 == s {print $1}')"
test -n "$b_ah"
test "$b_ah" = "$approved_b_ah_oid"
commits+=("$p_ah" "$b_ah")
for index in "${!commits[@]}"; do
  actual_subject="$(git show -s --format=%s "${commits[$index]}")"
  test "$actual_subject" = "${subjects[$index]}"
  subject_count="$(git log --all --format='%s' | grep -Fxc "${subjects[$index]}")"
  test "$subject_count" -eq 1
done
assert_edge "$b_4af" "$i"
assert_edge "$i" "$d_ag"
assert_edge "$d_ag" "$p_ag"
assert_edge "$p_ag" "$d_ah"
assert_edge "$d_ah" "$p_ah"
assert_edge "$p_ah" "$b_ah"
head_commit="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_commit" = "$b_ah"
assert_commit_paths "$b_4af" "$task_file"
assert_commit_paths "$i" "$task_file" "$test_file"
assert_commit_paths "$d_ag" "$task_file"
assert_commit_paths "$p_ag" "$plan_file" "$task_file"
assert_commit_paths "$d_ah" "$task_file"
assert_commit_paths "$p_ah" "$plan_file" "$task_file"
assert_commit_paths "$b_ah" "$task_file"
assert_range_paths "$b_4af..$i" "$task_file" "$test_file"
assert_range_paths "$d_ah..$p_ah" "$plan_file" "$task_file"
assert_range_paths "$p_ah..$b_ah" "$task_file"
for commit in "${commits[@]}"; do
  assert_modes "$commit" "$plan_file" "$task_file" "$test_file"
done
implementation_blob="$(git rev-parse "$i:$test_file")"
b_ah_blob="$(git rev-parse "$b_ah:$test_file")"
test "$b_ah_blob" = "$implementation_blob"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
python3 - "$task_file" "$d_ah" "$p_ah" <<'PY'
import pathlib
import re
import sys

label = "T-TSDC-004R-4AH collision-safe disposition Plan"
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0 and view[:separator].strip(" \t") == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("accepted-plan-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|") or "\\|" in row or "\\`" in row:
    raise SystemExit("accepted-plan-shape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("accepted-plan-cells")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("accepted-plan-label")
if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
    raise SystemExit("accepted-plan-extra-range")
if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
    raise SystemExit("accepted-plan-range-shape")
expected = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    f"`{sys.argv[2]}..{sys.argv[3]}`",
    "accepted; B_AH resolved by its exact unique subject",
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
]
if cells[2:7] != expected:
    raise SystemExit("accepted-plan-values")
PY
wrapper_status=0
wrapper_output="$({
  python3 - \
    python3 scripts/validation/check-target-surface-delta-contract.py \
    --mode advisory <<'PY'
import os
import subprocess
import sys

RESERVED = 125


def run_once(argv, runner=subprocess.run):
    try:
        if not argv:
            raise ValueError("missing argv")
        completed = runner(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            shell=False,
        )
        rc = completed.returncode
        payload = completed.stdout
        if (
            isinstance(rc, bool)
            or not isinstance(rc, int)
            or rc < 0
            or rc > 255
            or not isinstance(payload, (bytes, bytearray))
        ):
            return RESERVED, "internal"
        return rc, "nonempty" if payload else "empty"
    except Exception:
        return RESERVED, "internal"


def render(rc, output_class):
    return f"result status={rc} output={output_class}\n".encode("ascii")


class Completed:
    def __init__(self, returncode, stdout):
        self.returncode = returncode
        self.stdout = stdout


def require_canonical(result, expected, markers):
    if result != expected:
        raise RuntimeError("oracle-result")
    rendered = render(*result)
    expected_line = f"result status={expected[0]} output={expected[1]}\n".encode("ascii")
    if rendered != expected_line:
        raise RuntimeError("oracle-canonical")
    if any(marker in rendered for marker in markers):
        raise RuntimeError("oracle-raw-leak")


def oracle():
    markers = (b"stderr-merged-raw-marker", b"successor-marker")
    cases = (
        (0, b"", (0, "empty")),
        (0, b"\n", (0, "nonempty")),
        (0, b"stderr-merged-raw-marker", (0, "nonempty")),
        (0, b"\x1e", (0, "nonempty")),
        (0, b"\x00", (0, "nonempty")),
        (23, b"", (23, "empty")),
        (23, b"successor-marker", (23, "nonempty")),
        (125, b"", (125, "empty")),
        (125, b"stderr-merged-raw-marker", (125, "nonempty")),
        (-9, b"", (125, "internal")),
        (256, b"", (125, "internal")),
        (0, "invalid-stdout", (125, "internal")),
    )
    expected_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "check": False,
        "shell": False,
    }
    for returncode, stdout, expected in cases:
        calls = []

        def fake(argv, **kwargs):
            calls.append((argv, kwargs))
            return Completed(returncode, stdout)

        result = run_once(["fake-validator"], fake)
        if calls != [(["fake-validator"], expected_kwargs)]:
            raise RuntimeError("oracle-call-count-or-shape")
        require_canonical(result, expected, markers)

    exception_calls = []

    def raising_runner(argv, **kwargs):
        exception_calls.append((argv, kwargs))
        raise RuntimeError("runner failure")

    exception_result = run_once(["fake-validator"], raising_runner)
    if exception_calls != [(["fake-validator"], expected_kwargs)]:
        raise RuntimeError("oracle-exception-call-count")
    require_canonical(exception_result, (125, "internal"), markers)

    missing_calls = []

    def forbidden_runner(argv, **kwargs):
        missing_calls.append((argv, kwargs))
        return Completed(0, b"")

    missing_result = run_once([], forbidden_runner)
    if missing_calls:
        raise RuntimeError("oracle-missing-call-count")
    require_canonical(missing_result, (125, "internal"), markers)


def main():
    oracle()
    expected_argv = [
        "python3",
        "scripts/validation/check-target-surface-delta-contract.py",
        "--mode",
        "advisory",
    ]
    if sys.argv[1:] != expected_argv:
        raise RuntimeError("real-argv")
    real_calls = []

    def counted_runner(argv, **kwargs):
        real_calls.append((argv, kwargs))
        return subprocess.run(argv, **kwargs)

    rc, output_class = run_once(sys.argv[1:], counted_runner)
    expected_real_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "check": False,
        "shell": False,
    }
    if real_calls != [(expected_argv, expected_real_kwargs)]:
        raise RuntimeError("real-call-count-or-shape")
    canonical = render(rc, output_class)
    written = os.write(1, canonical)
    if written != len(canonical):
        raise RuntimeError("canonical-short-write")
    return rc


try:
    rc = main()
except Exception:
    rc = RESERVED
    try:
        internal = render(RESERVED, "internal")
        written = os.write(1, internal)
        if written != len(internal):
            raise RuntimeError("internal-short-write")
    except Exception:
        pass
raise SystemExit(rc)
PY
})" || wrapper_status=$?
case "$wrapper_output" in
  'result status=125 output=internal')
    exit 125
    ;;
  "result status=$wrapper_status output=empty" | \
  "result status=$wrapper_status output=nonempty")
    ;;
  *)
    exit 125
    ;;
esac
if [ "$wrapper_status" -ne 0 ]; then
  exit "$wrapper_status"
fi
case "$wrapper_output" in
  'result status=0 output=empty' | 'result status=0 output=nonempty')
    ;;
  *)
    exit 125
    ;;
esac
```

- [ ] **Step AH-4: Prove accepted B_AH, record E_AH, and prove the commit.**

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
b_4af=7e32c37cafde08b108ee33e3439cda3aea336961
i=a7d05b0e5c0ffaeccde9e401450e696855cfb2b5
d_ag=737838fe80880b7eadbfb1c7e18d8dc251bcc8b9
p_ag=f2a4b5041222c48f392bc251eae014655cee7b7c
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_subject='docs(plan): define collision-safe disposition proof'
b_subject='docs(task): record collision-safe disposition plan reviews'
e_subject='docs(task): record collision-safe disposition revalidation'
edge() {
  local parent="$1"
  local child="$2"
  local count
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  count="$(git rev-list --count "$parent..$child")"
  test "$count" -eq 1
  parent_count="$(git rev-list --parents -n 1 "$child" | awk '{print NF - 1}')"
  test "$parent_count" -eq 1
  first_parent="$(git rev-parse "$child^1")"
  test "$first_parent" = "$parent"
}
p_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$p_subject" '$2 == s {print $1}')"
test -n "$p_ah"
p_count="$(git log --all --format='%s' | grep -Fxc "$p_subject")"
test "$p_count" -eq 1
b_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$b_subject" '$2 == s {print $1}')"
test -n "$b_ah"
b_count="$(git log --all --format='%s' | grep -Fxc "$b_subject")"
test "$b_count" -eq 1
head_commit="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_commit" = "$b_ah"
subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record exhausted status-based silent-success plan review'
  "$p_subject"
  "$b_subject"
)
commits=("$b_4af" "$i" "$d_ag" "$p_ag" "$d_ah" "$p_ah" "$b_ah")
for index in "${!commits[@]}"; do
  actual="$(git show -s --format=%s "${commits[$index]}")"
  test "$actual" = "${subjects[$index]}"
  count="$(git log --all --format='%s' | grep -Fxc "${subjects[$index]}")"
  test "$count" -eq 1
done
edge "$b_4af" "$i"
edge "$i" "$d_ag"
edge "$d_ag" "$p_ag"
edge "$p_ag" "$d_ah"
edge "$d_ah" "$p_ah"
edge "$p_ah" "$b_ah"
python3 - "$task_file" "$d_ah" "$p_ah" <<'PY'
import pathlib
import re
import sys

label = "T-TSDC-004R-4AH collision-safe disposition Plan"
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0 and view[:separator].strip(" \t") == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("accepted-plan-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|") or "\\|" in row or "\\`" in row:
    raise SystemExit("accepted-plan-shape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("accepted-plan-cells")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("accepted-plan-label")
if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
    raise SystemExit("accepted-plan-extra-range")
if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
    raise SystemExit("accepted-plan-range-shape")
expected = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    f"`{sys.argv[2]}..{sys.argv[3]}`",
    "accepted; B_AH resolved by its exact unique subject",
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
]
if cells[2:7] != expected:
    raise SystemExit("accepted-plan-values")
PY
python3 - "$task_file" <<'PY'
import pathlib
import sys

label = "T-TSDC-004R-4AH collision-safe disposition revalidation"
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0 and view[:separator].strip(" \t") == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("evidence-row-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("evidence-row-shape")
if "\\|" in row or "\\`" in row:
    raise SystemExit("evidence-row-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("evidence-row-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("evidence-row-label")
if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
    raise SystemExit("evidence-row-extra-range")
expected = [
    "pending fresh independent review",
    "pending fresh independent review",
    "awaiting exact reviewed range",
    "E_AH committed; fresh composite reviews pending; no downstream authority",
    "E_AH resolved by its exact unique subject; revalidation approval consumed; R_AH and XE_AH are not created",
]
if cells[2:7] != expected:
    raise SystemExit("evidence-row-values")
PY
expected_plan_paths="$(printf '%s\n' "$plan_file" "$task_file" | sort)"
test -n "$expected_plan_paths"
expected_test_paths="$(printf '%s\n' "$task_file" "$test_file" | sort)"
test -n "$expected_test_paths"
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$b_4af" | sort)"
test "$commit_paths" = "$task_file"
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$i" | sort)"
test "$commit_paths" = "$expected_test_paths"
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$d_ag" | sort)"
test "$commit_paths" = "$task_file"
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$p_ag" | sort)"
test "$commit_paths" = "$expected_plan_paths"
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$d_ah" | sort)"
test "$commit_paths" = "$task_file"
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$p_ah" | sort)"
test "$commit_paths" = "$expected_plan_paths"
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$b_ah" | sort)"
test "$commit_paths" = "$task_file"
historical_range_paths="$(git diff --name-only "$b_4af..$i" | sort)"
test "$historical_range_paths" = "$expected_test_paths"
plan_range_paths="$(git diff --name-only "$d_ah..$p_ah" | sort)"
test "$plan_range_paths" = "$expected_plan_paths"
historical_blob="$(git rev-parse "$i:$test_file")"
test -n "$historical_blob"
b_blob="$(git rev-parse "$b_ah:$test_file")"
test "$b_blob" = "$historical_blob"
for commit_path in \
  "$b_4af:$task_file" \
  "$i:$task_file" "$i:$test_file" \
  "$d_ag:$task_file" \
  "$p_ag:$plan_file" "$p_ag:$task_file" \
  "$d_ah:$task_file" \
  "$p_ah:$plan_file" "$p_ah:$task_file" \
  "$b_ah:$task_file"
do
  mode="$(git ls-tree "${commit_path%%:*}" "${commit_path#*:}" | awk '{print $1}')"
  test "$mode" = 100644
done
dirty_paths="$({ git diff --name-only; git diff --cached --name-only; git ls-files --others --exclude-standard; } | sort -u)"
test "$dirty_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$task_file"
git commit -m "$e_subject"
e_ah="$(git rev-parse --verify 'HEAD^{commit}')"
test -n "$e_ah"
e_actual_subject="$(git show -s --format=%s "$e_ah")"
test "$e_actual_subject" = "$e_subject"
e_count="$(git log --all --format='%s' | grep -Fxc "$e_subject")"
test "$e_count" -eq 1
edge "$b_ah" "$e_ah"
e_paths="$(git diff-tree --no-commit-id --name-only -r "$e_ah" | sort)"
test "$e_paths" = "$task_file"
e_range_paths="$(git diff --name-only "$b_ah..$e_ah" | sort)"
test "$e_range_paths" = "$task_file"
e_mode="$(git ls-tree "$e_ah" "$task_file" | awk '{print $1}')"
test "$e_mode" = 100644
e_blob="$(git rev-parse "$e_ah:$test_file")"
test "$e_blob" = "$historical_blob"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

Before composite review, the revalidation row is exactly:

| Review unit | Owner | Specification | Quality/security | Reviewed range | Disposition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-004R-4AH collision-safe disposition revalidation | Controller | pending fresh independent review | pending fresh independent review | awaiting exact reviewed range | E_AH committed; fresh composite reviews pending; no downstream authority | E_AH resolved by its exact unique subject; revalidation approval consumed; R_AH and XE_AH are not created |

- [ ] **Step AH-5: Parse composite rows and commit R_AH or XE_AH.**

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
b_4af=7e32c37cafde08b108ee33e3439cda3aea336961
i=a7d05b0e5c0ffaeccde9e401450e696855cfb2b5
d_ag=737838fe80880b7eadbfb1c7e18d8dc251bcc8b9
p_ag=f2a4b5041222c48f392bc251eae014655cee7b7c
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_subject='docs(plan): define collision-safe disposition proof'
b_subject='docs(task): record collision-safe disposition plan reviews'
e_subject='docs(task): record collision-safe disposition revalidation'
p_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$p_subject" '$2 == s {print $1}')"
test -n "$p_ah"
p_count="$(git log --all --format='%s' | grep -Fxc "$p_subject")"
test "$p_count" -eq 1
b_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$b_subject" '$2 == s {print $1}')"
test -n "$b_ah"
b_count="$(git log --all --format='%s' | grep -Fxc "$b_subject")"
test "$b_count" -eq 1
e_ah="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$e_subject" '$2 == s {print $1}')"
test -n "$e_ah"
e_count="$(git log --all --format='%s' | grep -Fxc "$e_subject")"
test "$e_count" -eq 1
head_commit="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_commit" = "$e_ah"
selection="$({ python3 - "$task_file" "$d_ah" "$p_ah" "$b_4af" "$i" "$b_ah" "$e_ah" <<'PY'
import pathlib
import re
import sys

labels = (
    "T-TSDC-004R-4AH collision-safe disposition Plan",
    "T-TSDC-004R-4AH frozen canonical-row implementation",
    "T-TSDC-004R-4AH collision-safe disposition revalidation",
)
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
found = {label: [] for label in labels}
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0:
        first_cell = view[:separator].strip(" \t")
        if first_cell in found:
            found[first_cell].append(line)
if any(len(found[label]) != 1 for label in labels):
    raise SystemExit("composite-candidate-count")
rows = []
for label in labels:
    row = found[label][0]
    if not row.startswith("|") or not row.endswith("|"):
        raise SystemExit("composite-shape")
    if "\\|" in row or "\\`" in row:
        raise SystemExit("composite-escape")
    parts = row.split("|")
    if len(parts) != 9 or parts[0] or parts[-1]:
        raise SystemExit("composite-cell-count")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if len(cells) != 7 or cells[0] != label:
        raise SystemExit("composite-label")
    if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
        raise SystemExit("composite-extra-range")
    if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
        raise SystemExit("composite-range-shape")
    rows.append(cells)
plan, implementation, revalidation = rows
expected_plan = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    f"`{sys.argv[2]}..{sys.argv[3]}`",
    "accepted; B_AH resolved by its exact unique subject",
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
]
if plan[2:7] != expected_plan:
    raise SystemExit("composite-plan")
if implementation[4] != f"`{sys.argv[4]}..{sys.argv[5]}`":
    raise SystemExit("composite-implementation-range")
if revalidation[4] != f"`{sys.argv[6]}..{sys.argv[7]}`":
    raise SystemExit("composite-revalidation-range")
spec_re = r"C\d+/I\d+/M\d+; SPEC_COMPLIANCE (YES|NO); COMMIT_READY (YES|NO)"
quality_re = r"C\d+/I\d+/M\d+; QUALITY_SECURITY (PASS|FAIL); COMMIT_READY (YES|NO)"
for cells in (implementation, revalidation):
    if re.fullmatch(spec_re, cells[2], flags=re.ASCII) is None:
        raise SystemExit("composite-spec-verdict")
    if re.fullmatch(quality_re, cells[3], flags=re.ASCII) is None:
        raise SystemExit("composite-quality-verdict")
if implementation[2:4] != revalidation[2:4]:
    raise SystemExit("composite-divergent-verdicts")
accepted_reviews = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES",
]
accepted = implementation[2:4] == accepted_reviews
if accepted:
    expected_implementation = [
        "accepted; frozen implementation approved in 4AH composite review",
        "Composite reviewers accepted the exact historical implementation and revalidation ranges; frozen test blob preserved",
    ]
    expected_revalidation = [
        "accepted; R_AH resolved by its exact unique subject",
        "Separately approved revalidation and both fresh composite reviews accepted; Task 4.5 authority granted",
    ]
else:
    expected_implementation = [
        "rejected/exhausted; frozen implementation not approved in 4AH composite review",
        "One or both fresh composite reviews rejected; frozen history grants no downstream authority",
    ]
    expected_revalidation = [
        "rejected/exhausted; XE_AH resolved by its exact unique subject",
        "One or both fresh composite reviews rejected; no correction, retry, or Wave C authority",
    ]
if implementation[5:7] != expected_implementation:
    raise SystemExit("composite-implementation-outcome")
if revalidation[5:7] != expected_revalidation:
    raise SystemExit("composite-revalidation-outcome")
print("R_AH" if accepted else "XE_AH")
PY
})"
test "$selection" = R_AH || test "$selection" = XE_AH
case "$selection" in
  R_AH)
    terminal_subject='docs(task): record collision-safe disposition review'
    ;;
  XE_AH)
    terminal_subject='docs(task): record exhausted collision-safe disposition review'
    ;;
esac
dirty_paths="$({ git diff --name-only; git diff --cached --name-only; git ls-files --others --exclude-standard; } | sort -u)"
test "$dirty_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$task_file"
git commit -m "$terminal_subject"
terminal="$(git rev-parse --verify 'HEAD^{commit}')"
test -n "$terminal"
actual_subject="$(git show -s --format=%s "$terminal")"
test "$actual_subject" = "$terminal_subject"
subject_count="$(git log --all --format='%s' | grep -Fxc "$terminal_subject")"
test "$subject_count" -eq 1
edge() {
  local parent="$1"
  local child="$2"
  local count
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  count="$(git rev-list --count "$parent..$child")"
  test "$count" -eq 1
  parent_count="$(git rev-list --parents -n 1 "$child" | awk '{print NF - 1}')"
  test "$parent_count" -eq 1
  first_parent="$(git rev-parse "$child^1")"
  test "$first_parent" = "$parent"
}
edge "$b_4af" "$i"
edge "$i" "$d_ag"
edge "$d_ag" "$p_ag"
edge "$p_ag" "$d_ah"
edge "$d_ah" "$p_ah"
edge "$p_ah" "$b_ah"
edge "$b_ah" "$e_ah"
edge "$e_ah" "$terminal"
subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record exhausted status-based silent-success plan review'
  "$p_subject"
  "$b_subject"
  "$e_subject"
  "$terminal_subject"
)
commits=("$b_4af" "$i" "$d_ag" "$p_ag" "$d_ah" "$p_ah" "$b_ah" "$e_ah" "$terminal")
for index in "${!commits[@]}"; do
  verified="$(git rev-parse --verify "${commits[$index]}^{commit}")"
  test "$verified" = "${commits[$index]}"
  commit_subject="$(git show -s --format=%s "${commits[$index]}")"
  test "$commit_subject" = "${subjects[$index]}"
  commit_subject_count="$(git log --all --format='%s' | grep -Fxc "${subjects[$index]}")"
  test "$commit_subject_count" -eq 1
done
expected_plan_paths="$(printf '%s\n' "$plan_file" "$task_file" | sort)"
expected_test_paths="$(printf '%s\n' "$task_file" "$test_file" | sort)"
expected_paths=(
  "$task_file"
  "$expected_test_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$task_file"
  "$task_file"
)
for index in "${!commits[@]}"; do
  commit_paths="$(git diff-tree --no-commit-id --name-only -r "${commits[$index]}" | sort)"
  test "$commit_paths" = "${expected_paths[$index]}"
done
terminal_range_paths="$(git diff --name-only "$e_ah..$terminal" | sort)"
test "$terminal_range_paths" = "$task_file"
plan_range_paths="$(git diff --name-only "$d_ah..$p_ah" | sort)"
test "$plan_range_paths" = "$expected_plan_paths"
historical_range_paths="$(git diff --name-only "$b_4af..$i" | sort)"
test "$historical_range_paths" = "$expected_test_paths"
evidence_range_paths="$(git diff --name-only "$b_ah..$e_ah" | sort)"
test "$evidence_range_paths" = "$task_file"
for commit_path in \
  "$b_4af:$task_file" \
  "$i:$task_file" "$i:$test_file" \
  "$d_ag:$task_file" \
  "$p_ag:$plan_file" "$p_ag:$task_file" \
  "$d_ah:$task_file" \
  "$p_ah:$plan_file" "$p_ah:$task_file" \
  "$b_ah:$task_file" "$e_ah:$task_file" "$terminal:$task_file"
do
  mode="$(git ls-tree "${commit_path%%:*}" "${commit_path#*:}" | awk '{print $1}')"
  test "$mode" = 100644
done
historical_blob="$(git rev-parse "$i:$test_file")"
test -n "$historical_blob"
terminal_blob="$(git rev-parse "$terminal:$test_file")"
test "$terminal_blob" = "$historical_blob"
head_after="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_after" = "$terminal"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

XE_AH is terminal. Only the exact accepted R_AH chain authorizes Task 4.5.

#### Historical T-TSDC-004R-4AI: Session-Bound Collision-Safe Proof

At the time of its approval, 4AI was the Plan-only successor from clean
D_AI/XP_AH `88f55837be251318cd697bd8a1ab3a4f0ed1a824`. It preserves every 4AH
block as historical, non-executable evidence and changed only the rejected
split-session boundary. Its separately approved revalidation, one byte-safe
wrapper call, sanitized result, Task-only E_AI commit, and postcommit proof
were designed as one fail-fast transaction. That historical approval stopped
after P_AI, two fresh independent Plan reviews over exact `D_AI..P_AI`, and
exactly one Task-only B_AI or XP_AI terminal. AI-3, AI-4, Task 4.5, tests,
validators, wrapper/proof execution, revalidation, runtime, remote, direct
pre-commit, and Graphify remained blocked pending later gates.

The exact subjects are:

- P_AI: `docs(plan): define session-bound collision-safe proof`
- B_AI: `docs(task): record session-bound collision-safe plan reviews`
- XP_AI: `docs(task): record exhausted session-bound collision-safe plan review`
- E_AI: `docs(task): record session-bound collision-safe revalidation`
- R_AI: `docs(task): record session-bound collision-safe review`
- XE_AI: `docs(task): record exhausted session-bound collision-safe review`

- [ ] **Step AI-1: Commit and prove P_AI.**

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
d_ai=88f55837be251318cd697bd8a1ab3a4f0ed1a824
p_subject='docs(plan): define session-bound collision-safe proof'
head_before="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_before" = "$d_ai"
d_subject="$(git show -s --format=%s "$d_ai")"
test "$d_subject" = 'docs(task): record exhausted collision-safe disposition plan review'
p_pre_count="$(git log --all --format='%s' | awk -v subject="$p_subject" '$0 == subject {count++} END {print count + 0}')"
test "$p_pre_count" -eq 0
unstaged_paths="$(git diff --name-only)"
test "$?" -eq 0
staged_paths="$(git diff --cached --name-only)"
test "$?" -eq 0
untracked_paths="$(git ls-files --others --exclude-standard)"
test "$?" -eq 0
dirty_paths="$(printf '%s\n' "$unstaged_paths" "$staged_paths" "$untracked_paths" | sed '/^$/d' | sort -u)"
expected_paths="$(printf '%s\n' "$plan_file" "$task_file" | sort)"
test "$dirty_paths" = "$expected_paths"
git diff --check
git add "$plan_file" "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$expected_paths"
git commit -m "$p_subject"
p_ai="$(git rev-parse --verify 'HEAD^{commit}')"
test -n "$p_ai"
actual_subject="$(git show -s --format=%s "$p_ai")"
test "$actual_subject" = "$p_subject"
subject_count="$(git log --all --format='%s' | grep -Fxc "$p_subject")"
test "$subject_count" -eq 1
parent_count="$(git rev-list --parents -n 1 "$p_ai" | awk '{print NF - 1}')"
test "$parent_count" -eq 1
parent="$(git rev-parse "$p_ai^1")"
test "$parent" = "$d_ai"
distance="$(git rev-list --count "$d_ai..$p_ai")"
test "$distance" -eq 1
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$p_ai" | sort)"
test "$commit_paths" = "$expected_paths"
range_paths="$(git diff --name-only "$d_ai..$p_ai" | sort)"
test "$range_paths" = "$expected_paths"
for file_path in "$plan_file" "$task_file"; do
  mode="$(git ls-tree "$p_ai" "$file_path" | awk '{print $1}')"
  test "$mode" = 100644
done
python3 - "$task_file" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")


def exact_line(expected):
    if text.splitlines().count(expected) != 1:
        raise SystemExit(f"p-ai-line-count:{expected}")


label = "T-TSDC-004R-4AI session-bound collision-safe Plan"
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0 and view[:separator].strip(" \t") == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("p-ai-row-count")
expected = (
    "| T-TSDC-004R-4AI session-bound collision-safe Plan | Controller | "
    "pending fresh independent review | pending fresh independent review | "
    "awaiting exact reviewed range | checkpoint committed; fresh Plan reviews "
    "pending; no downstream authority | P_AI committed and resolved by its "
    "exact unique subject; no future OID is claimed in its own tree |"
)
if candidates[0] != expected:
    raise SystemExit("p-ai-row-values")
exact_line("- 4AI transaction state: not-run; separate approval required.")
exact_line("- 4AI sanitized result: not-run.")
exact_line(
    "| T-TSDC-004R-4AI Plan checkpoint P_AI | Define session-bound collision-safe proof | "
    "`docs(plan): define session-bound collision-safe proof` | resolved by this exact unique subject | "
    "P_AI committed; resolved by its exact unique subject; fresh Plan reviews pending; no downstream authority. |"
)
exact_line(
    "Current 4AI final handoff: P_AI committed; resolved by its exact unique subject; "
    "fresh Plan reviews pending; no downstream authority."
)
exact_line(
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
    "blocked; Plan reviews pending | blocked; Plan reviews pending | "
    "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "blocked; B_AI is not created | Frozen implementation remains historical; "
    "no composite-review authority |"
)
exact_line(
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
    "blocked; Plan reviews pending | blocked; Plan reviews pending | awaiting exact reviewed range | "
    "blocked; B_AI is not created | B_AI is not created; approval not consumed; "
    "E_AI, R_AI, and XE_AI are not created |"
)
PY
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

At the P_AI tree the canonical row is exactly:

| Review unit | Owner | Specification | Quality/security | Reviewed range | Disposition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-004R-4AI session-bound collision-safe Plan | Controller | pending fresh independent review | pending fresh independent review | awaiting exact reviewed range | checkpoint committed; fresh Plan reviews pending; no downstream authority | P_AI committed and resolved by its exact unique subject; no future OID is claimed in its own tree |

- [ ] **Step AI-2: Parse completed Plan reviews first and commit one terminal.**

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
d_ai=88f55837be251318cd697bd8a1ab3a4f0ed1a824
p_subject='docs(plan): define session-bound collision-safe proof'
p_ai="$(git rev-parse --verify 'HEAD^{commit}')"
selection="$({ python3 - "$task_file" "$d_ai" "$p_ai" <<'PY'
import pathlib
import re
import sys

label = "T-TSDC-004R-4AI session-bound collision-safe Plan"
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0 and view[:separator].strip(" \t") == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("plan-candidate-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("plan-shape")
if "\\|" in row or "\\`" in row:
    raise SystemExit("plan-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("plan-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("plan-label")
if cells[1] != "Controller":
    raise SystemExit("plan-owner")
if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
    raise SystemExit("plan-extra-range-token")
if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
    raise SystemExit("plan-range-shape")
if cells[4] != f"`{sys.argv[2]}..{sys.argv[3]}`":
    raise SystemExit("plan-range")
spec_re = r"C\d+/I\d+/M\d+; SPEC_COMPLIANCE (YES|NO); IMPLEMENTATION_READY (YES|NO)"
quality_re = r"C\d+/I\d+/M\d+; QUALITY_SECURITY (PASS|FAIL); IMPLEMENTATION_READY (YES|NO)"
if re.fullmatch(spec_re, cells[2], flags=re.ASCII) is None:
    raise SystemExit("plan-spec-verdict")
if re.fullmatch(quality_re, cells[3], flags=re.ASCII) is None:
    raise SystemExit("plan-quality-verdict")
accepted = (
    cells[2] == "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES"
    and cells[3] == "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES"
)
expected = (
    (
        "accepted; B_AI resolved by its exact unique subject",
        "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
    )
    if accepted
    else (
        "rejected/exhausted; XP_AI resolved by its exact unique subject",
        "One or both fresh Plan reviews rejected; no correction, revalidation, or Wave C authority",
    )
)
if tuple(cells[5:7]) != expected:
    raise SystemExit("plan-outcome-pair")
print("B_AI" if accepted else "XP_AI")
PY
})"
test "$selection" = B_AI || test "$selection" = XP_AI
head_subject="$(git show -s --format=%s "$p_ai")"
test "$head_subject" = "$p_subject"
p_count="$(git log --all --format='%s' | grep -Fxc "$p_subject")"
test "$p_count" -eq 1
parent_count="$(git rev-list --parents -n 1 "$p_ai" | awk '{print NF - 1}')"
test "$parent_count" -eq 1
parent="$(git rev-parse "$p_ai^1")"
test "$parent" = "$d_ai"
distance="$(git rev-list --count "$d_ai..$p_ai")"
test "$distance" -eq 1
expected_plan_paths="$(printf '%s\n' "$plan_file" "$task_file" | sort)"
p_paths="$(git diff-tree --no-commit-id --name-only -r "$p_ai" | sort)"
test "$p_paths" = "$expected_plan_paths"
p_range_paths="$(git diff --name-only "$d_ai..$p_ai" | sort)"
test "$p_range_paths" = "$expected_plan_paths"
implementation_blob="$(git rev-parse "a7d05b0e5c0ffaeccde9e401450e696855cfb2b5:$test_file")"
test -n "$implementation_blob"
p_blob="$(git rev-parse "$p_ai:$test_file")"
test "$p_blob" = "$implementation_blob"
unstaged_paths="$(git diff --name-only)"
test "$?" -eq 0
staged_paths="$(git diff --cached --name-only)"
test "$?" -eq 0
untracked_paths="$(git ls-files --others --exclude-standard)"
test "$?" -eq 0
dirty_paths="$(printf '%s\n' "$unstaged_paths" "$staged_paths" "$untracked_paths" | sed '/^$/d' | sort -u)"
test "$dirty_paths" = "$task_file"
b_subject='docs(task): record session-bound collision-safe plan reviews'
xp_subject='docs(task): record exhausted session-bound collision-safe plan review'
case "$selection" in
  B_AI)
    terminal_subject="$b_subject"
    opposite_subject="$xp_subject"
    ;;
  XP_AI)
    terminal_subject="$xp_subject"
    opposite_subject="$b_subject"
    ;;
esac
selected_pre_count="$(git log --all --format='%s' | awk -v subject="$terminal_subject" '$0 == subject {count++} END {print count + 0}')"
test "$selected_pre_count" -eq 0
opposite_pre_count="$(git log --all --format='%s' | awk -v subject="$opposite_subject" '$0 == subject {count++} END {print count + 0}')"
test "$opposite_pre_count" -eq 0
python3 - "$task_file" "$selection" "$d_ai" "$p_ai" <<'PY'
import os
import pathlib
import re
import stat
import sys
import tempfile

path = pathlib.Path(sys.argv[1])
selection = sys.argv[2]
text = path.read_text(encoding="utf-8")
label = "T-TSDC-004R-4AI session-bound collision-safe Plan"
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0 and view[:separator].strip(" \t") == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("terminal-plan-candidate-count")
row = candidates[0]
if not row.startswith("|") or not row.endswith("|") or "\\|" in row or "\\`" in row:
    raise SystemExit("terminal-plan-shape")
parts = row.split("|")
if len(parts) != 9 or parts[0] or parts[-1]:
    raise SystemExit("terminal-plan-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label or cells[1] != "Controller":
    raise SystemExit("terminal-plan-identity")
if cells[4] != f"`{sys.argv[3]}..{sys.argv[4]}`":
    raise SystemExit("terminal-plan-range")
spec_re = r"C\d+/I\d+/M\d+; SPEC_COMPLIANCE (YES|NO); IMPLEMENTATION_READY (YES|NO)"
quality_re = r"C\d+/I\d+/M\d+; QUALITY_SECURITY (PASS|FAIL); IMPLEMENTATION_READY (YES|NO)"
if re.fullmatch(spec_re, cells[2], flags=re.ASCII) is None:
    raise SystemExit("terminal-plan-spec")
if re.fullmatch(quality_re, cells[3], flags=re.ASCII) is None:
    raise SystemExit("terminal-plan-quality")
accepted = cells[2:4] == [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
]
expected_selection = "B_AI" if accepted else "XP_AI"
if selection != expected_selection:
    raise SystemExit("terminal-selection-drift")
expected_outcome = (
    [
        "accepted; B_AI resolved by its exact unique subject",
        "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
    ]
    if accepted
    else [
        "rejected/exhausted; XP_AI resolved by its exact unique subject",
        "One or both fresh Plan reviews rejected; no correction, revalidation, or Wave C authority",
    ]
)
if cells[5:7] != expected_outcome:
    raise SystemExit("terminal-plan-outcome")
old_frozen = (
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
    "blocked; Plan reviews pending | blocked; Plan reviews pending | "
    "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "blocked; B_AI is not created | Frozen implementation remains historical; "
    "no composite-review authority |"
)
old_revalidation = (
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
    "blocked; Plan reviews pending | blocked; Plan reviews pending | awaiting exact reviewed range | "
    "blocked; B_AI is not created | B_AI is not created; approval not consumed; "
    "E_AI, R_AI, and XE_AI are not created |"
)
old_approval_owner = "- 4AI revalidation approval owner/source: not approved; no source recorded."
old_approved_oid = "- 4AI `APPROVED_B_AI_OID`: not recorded; B_AI is not created."
old_parent_work_breakdown = (
    "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
    "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
    "agent; original agents remain historical | active; P_AI committed; resolved by its exact unique subject; "
    "fresh Plan reviews pending; no downstream authority |"
)
old_work_breakdown = (
    "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit "
    "in one fail-fast session without changing frozen implementation | Plan/evidence | TSDC-010–014 | "
    "two future fresh independent reviews over exact `D_AI..P_AI` | controller and future fresh "
    "independent reviewers | P_AI committed; resolved by its exact unique subject; fresh Plan reviews "
    "pending; no downstream authority |"
)
old_work_log = (
    "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | "
    "Not run; B_AI is not created; approval not consumed; E_AI is not created. |"
)
old_verification = (
    "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, "
    "one wrapper call, sanitized result, and Task-only E_AI in one session | "
    "Not run; B_AI is not created and no approval is consumed |"
)
old_b_ledger = (
    "| T-TSDC-004R-4AI accepted Plan evidence B_AI | Record accepted session-bound collision-safe Plan "
    "reviews | `docs(task): record session-bound collision-safe plan reviews` | future; not created | "
    "May be the sole future Task-only Plan terminal only if both fresh `D_AI..P_AI` reviews are "
    "C0/I0/M0; it does not authorize revalidation without separate approval. |"
)
old_xp_ledger = (
    "| T-TSDC-004R-4AI rejected Plan evidence XP_AI | Record exhausted session-bound collision-safe Plan "
    "review | `docs(task): record exhausted session-bound collision-safe plan review` | future; not created | "
    "Must be the sole future Task-only Plan terminal if either fresh Plan review is not accepted; "
    "terminal and no downstream authority. |"
)
old_e_ledger = (
    "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
    "`docs(task): record session-bound collision-safe revalidation` | future; not created | "
    "Blocked pending accepted B_AI and separate one-attempt approval naming its resolved full OID; "
    "evidence and commit must share one fail-fast session. |"
)
old_deferred = (
    "| T-TSDC-004R-3 atomic projection cutover | blocked; 4AI Plan reviews pending | Historical 4AF and "
    "rejected/exhausted 4AG/4AH evidence remain frozen. P_AI is resolved by its exact unique subject; "
    "B_AI/XP_AI/E_AI/R_AI/XE_AI are not created; no downstream authority. | complete two fresh "
    "`D_AI..P_AI` Plan reviews and exactly one future Task-only B_AI/XP_AI terminal; any revalidation "
    "still requires separate approval, and only accepted R_AI may unlock Wave C |"
)
old_handoff = (
    "Current 4AI final handoff: P_AI committed; resolved by its exact unique subject; fresh Plan reviews "
    "pending; no downstream authority."
)
old_current_boundary = (
    "- The active 4AI checkpoint is Plan-only. Pending reviews and future/uncreated\n"
    "  B_AI, XP_AI, E_AI, R_AI, and XE_AI do not establish revalidation, Task 4.5,\n"
    "  Wave C, downstream, runtime, or remote authority."
)
old_no_run = (
    "- No 4AI validator, test, wrapper, proof, revalidation, composite review,\n"
    "  implementation, runtime, remote, Graphify, Task 4.5, or Wave C action has\n"
    "  run. Fresh independent Plan reviews are pending and no downstream authority\n"
    "  exists."
)
old_final_block = (
    "T-TSDC-004R-4AI is the current Plan-only successor from clean XP_AH/D_AI\n"
    "`88f55837be251318cd697bd8a1ab3a4f0ed1a824`. P_AI committed; resolved by its\n"
    "exact unique subject; fresh Plan reviews pending; no downstream authority.\n"
    "B_AI, XP_AI, E_AI, R_AI, and XE_AI are future and not created. The current\n"
    "approval ends after two fresh exact-range Plan reviews and exactly one\n"
    "Task-only B_AI/XP_AI terminal. No validator, test, wrapper, proof,\n"
    "revalidation, implementation, runtime, remote, Graphify, Task 4.5, Wave C,\n"
    "Tasks 5–6, or whole-branch review authority exists. Only a future accepted\n"
    "R_AI, produced after a separately approved single-session E_AI revalidation\n"
    "and accepted fresh composite reviews, may unlock Task 4.5/Wave C."
)
if selection == "B_AI":
    replacements = {
        old_frozen: (
            "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
            "blocked; revalidation not run | blocked; revalidation not run | "
            "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
            "blocked; separately approved revalidation not run | Frozen implementation "
            "remains historical; no composite-review authority |"
        ),
        old_revalidation: (
            "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
            "blocked; revalidation not run | blocked; revalidation not run | awaiting exact reviewed range | "
            "blocked; separately approved revalidation not run | B_AI accepted; approval not yet "
            "consumed; E_AI, R_AI, and XE_AI are not created |"
        ),
        old_approval_owner: (
            "- 4AI revalidation approval owner/source: separate future User / Controller approval "
            "required; not consumed."
        ),
        old_approved_oid: (
            "- 4AI `APPROVED_B_AI_OID`: awaiting a separate approval naming the resolved full B_AI OID."
        ),
        old_parent_work_breakdown: (
            "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
            "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
            "agent; original agents remain historical | active; B_AI accepted and resolved by its exact unique "
            "subject; separate revalidation approval required; no downstream authority |"
        ),
        old_work_breakdown: (
            "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit "
            "in one fail-fast session without changing frozen implementation | Plan/evidence | TSDC-010–014 | "
            "accepted fresh Plan reviews over exact `D_AI..P_AI`; separate revalidation approval required | "
            "controller and future fresh independent reviewers | B_AI accepted and resolved by its exact "
            "unique subject; separate one-attempt approval required; no downstream authority |"
        ),
        old_work_log: (
            "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | Not run; B_AI "
            "accepted by both fresh Plan reviews; separate one-attempt approval not granted or consumed; "
            "E_AI is not created. |"
        ),
        old_verification: (
            "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, "
            "one wrapper call, sanitized result, and Task-only E_AI in one session | Not run; B_AI accepted; "
            "separate one-attempt approval not granted or consumed |"
        ),
        old_b_ledger: (
            "| T-TSDC-004R-4AI accepted Plan evidence B_AI | Record accepted session-bound collision-safe "
            "Plan reviews | `docs(task): record session-bound collision-safe plan reviews` | resolved by this "
            "exact unique subject | Sole Task-only accepted Plan terminal; separate approval naming the "
            "resolved full B_AI OID remains required before AI-3. |"
        ),
        old_xp_ledger: (
            "| T-TSDC-004R-4AI rejected Plan evidence XP_AI | Record exhausted session-bound collision-safe "
            "Plan review | `docs(task): record exhausted session-bound collision-safe plan review` | not "
            "created | Mutually excluded by the accepted B_AI terminal. |"
        ),
        old_e_ledger: (
            "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
            "`docs(task): record session-bound collision-safe revalidation` | not created | Blocked pending "
            "separate one-attempt approval naming the resolved full B_AI OID. |"
        ),
        old_deferred: (
            "| T-TSDC-004R-3 atomic projection cutover | blocked; accepted B_AI but revalidation not approved | "
            "Historical 4AF and rejected/exhausted 4AG/4AH evidence remain frozen. B_AI is the sole accepted "
            "Plan terminal; XP_AI/E_AI/R_AI/XE_AI are not created; no downstream authority. | obtain separate "
            "one-attempt approval naming the resolved full B_AI OID; only later accepted R_AI may unlock Wave C |"
        ),
        old_handoff: (
            "Current 4AI final handoff: B_AI accepted and resolved by its exact unique subject; separate "
            "one-attempt revalidation approval required; E_AI/R_AI/XE_AI not created; no downstream authority."
        ),
        old_current_boundary: (
            "- The active 4AI checkpoint has accepted B_AI, but revalidation is not approved. XP_AI, E_AI,\n"
            "  R_AI, and XE_AI are uncreated and do not establish Task 4.5, Wave C, downstream, runtime,\n"
            "  or remote authority."
        ),
        old_no_run: (
            "- No 4AI validator, test, wrapper, proof, revalidation, composite review, implementation, runtime,\n"
            "  remote, Graphify, Task 4.5, or Wave C action has run. Both fresh Plan reviews accepted B_AI,\n"
            "  but separate one-attempt revalidation approval is absent and no downstream authority exists."
        ),
        old_final_block: (
            "T-TSDC-004R-4AI is the current accepted-Plan successor from clean XP_AH/D_AI\n"
            "`88f55837be251318cd697bd8a1ab3a4f0ed1a824`. B_AI is accepted and resolved by its\n"
            "exact unique subject; XP_AI is not created. Separate one-attempt revalidation approval naming\n"
            "the resolved full B_AI OID is absent; E_AI, R_AI, and XE_AI are not created. No validator,\n"
            "test, wrapper, proof, revalidation, implementation, runtime, remote, Graphify, Task 4.5,\n"
            "Wave C, Tasks 5–6, or whole-branch review authority exists."
        ),
    }
elif selection == "XP_AI":
    replacements = {
        old_frozen: (
            "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
            "blocked; Plan rejected | blocked; Plan rejected | "
            "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
            "rejected/exhausted; XP_AI terminal | Frozen implementation remains historical; "
            "no composite-review authority |"
        ),
        old_revalidation: (
            "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
            "blocked; Plan rejected | blocked; Plan rejected | not applicable; Plan rejected | "
            "rejected/exhausted; XP_AI terminal | XP_AI resolved by its exact unique subject; "
            "no revalidation, retry, or Wave C authority |"
        ),
        "- 4AI transaction state: not-run; separate approval required.":
            "- 4AI transaction state: not-run; Plan rejected and XP_AI terminal.",
        "- 4AI sanitized result: not-run.":
            "- 4AI sanitized result: not-run; no revalidation authority.",
        old_approval_owner: (
            "- 4AI revalidation approval owner/source: not applicable; Plan rejected and XP_AI terminal."
        ),
        old_approved_oid: (
            "- 4AI `APPROVED_B_AI_OID`: not applicable; B_AI is not created."
        ),
        old_parent_work_breakdown: (
            "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
            "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
            "agent; original agents remain historical | rejected/exhausted at 4AI Plan review; XP_AI resolved "
            "by its exact unique subject; no downstream authority |"
        ),
        old_work_breakdown: (
            "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit "
            "in one fail-fast session without changing frozen implementation | Plan/evidence | TSDC-010–014 | "
            "completed rejected Plan reviews only; no downstream validation | controller and fresh independent "
            "reviewers | rejected/exhausted; XP_AI resolved by its exact unique subject; no downstream authority |"
        ),
        old_work_log: (
            "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | Not run; Plan rejected "
            "and XP_AI terminal; approval not consumed; B_AI/E_AI/R_AI/XE_AI are not created. |"
        ),
        old_verification: (
            "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, "
            "one wrapper call, sanitized result, and Task-only E_AI in one session | Not run; Plan rejected "
            "and XP_AI terminal; no revalidation authority |"
        ),
        old_b_ledger: (
            "| T-TSDC-004R-4AI accepted Plan evidence B_AI | Record accepted session-bound collision-safe "
            "Plan reviews | `docs(task): record session-bound collision-safe plan reviews` | not created | "
            "Mutually excluded by the rejected XP_AI terminal. |"
        ),
        old_xp_ledger: (
            "| T-TSDC-004R-4AI rejected Plan evidence XP_AI | Record exhausted session-bound collision-safe "
            "Plan review | `docs(task): record exhausted session-bound collision-safe plan review` | resolved "
            "by this exact unique subject | Sole Task-only rejected Plan terminal; no correction, revalidation, "
            "retry, or Wave C authority. |"
        ),
        old_e_ledger: (
            "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
            "`docs(task): record session-bound collision-safe revalidation` | not created | Not created; "
            "Plan-review exhaustion blocks revalidation. |"
        ),
        old_deferred: (
            "| T-TSDC-004R-3 atomic projection cutover | rejected/exhausted at 4AI Plan review | Historical "
            "4AF and rejected/exhausted 4AG/4AH evidence remain frozen. XP_AI is the sole rejected Plan "
            "terminal; B_AI/E_AI/R_AI/XE_AI are not created; no downstream authority. | return to a newly "
            "approved design; 4AI grants no correction, retry, or Wave C authority |"
        ),
        old_handoff: (
            "Current 4AI final handoff: rejected/exhausted; XP_AI resolved by its exact unique subject; "
            "B_AI/E_AI/R_AI/XE_AI not created; no downstream authority."
        ),
        old_current_boundary: (
            "- The active 4AI Plan is rejected/exhausted at XP_AI. B_AI, E_AI, R_AI, and XE_AI are uncreated;\n"
            "  no revalidation, Task 4.5, Wave C, downstream, runtime, or remote authority exists."
        ),
        old_no_run: (
            "- No 4AI validator, test, wrapper, proof, revalidation, composite review, implementation, runtime,\n"
            "  remote, Graphify, Task 4.5, or Wave C action has run. XP_AI is terminal and no downstream\n"
            "  authority exists."
        ),
        old_final_block: (
            "T-TSDC-004R-4AI is rejected/exhausted at the Task-only XP_AI terminal from clean XP_AH/D_AI\n"
            "`88f55837be251318cd697bd8a1ab3a4f0ed1a824`. XP_AI is resolved by its exact unique subject;\n"
            "B_AI, E_AI, R_AI, and XE_AI are not created. No validator, test, wrapper, proof, revalidation,\n"
            "implementation, runtime, remote, Graphify, Task 4.5, Wave C, Tasks 5–6, or whole-branch review\n"
            "authority exists."
        ),
    }
else:
    raise SystemExit("terminal-selection")
residue = tuple(path.parent.glob(f".{path.name}.*"))
if residue:
    raise SystemExit("terminal-temp-residue")
for old, new in replacements.items():
    if text.count(old) != 1 or old == new or new in text:
        raise SystemExit("terminal-replacement-shape")
for old, new in replacements.items():
    text = text.replace(old, new, 1)
source_mode = stat.S_IMODE(path.stat().st_mode)
temporary = None
try:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = pathlib.Path(stream.name)
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, source_mode)
    os.replace(temporary, path)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_fd = os.open(path.parent, directory_flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    temporary = None
finally:
    # Preserve any crash residue as a fail-closed rerun blocker.
    pass
PY
validated_task_blob="$(git hash-object "$task_file")"
[[ "$validated_task_blob" =~ ^[0-9a-f]{40}$ ]]
git diff --check
git add "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$task_file"
staged_task_blob="$(git rev-parse ":$task_file")"
test "$staged_task_blob" = "$validated_task_blob"
git commit -m "$terminal_subject"
terminal="$(git rev-parse --verify 'HEAD^{commit}')"
actual_subject="$(git show -s --format=%s "$terminal")"
test "$actual_subject" = "$terminal_subject"
subject_count="$(git log --all --format='%s' | grep -Fxc "$terminal_subject")"
test "$subject_count" -eq 1
opposite_count="$(git log --all --format='%s' | awk -v subject="$opposite_subject" '$0 == subject {count++} END {print count + 0}')"
test "$opposite_count" -eq 0
terminal_task_blob="$(git rev-parse "$terminal:$task_file")"
test "$terminal_task_blob" = "$validated_task_blob"
parent_count="$(git rev-list --parents -n 1 "$terminal" | awk '{print NF - 1}')"
test "$parent_count" -eq 1
parent="$(git rev-parse "$terminal^1")"
test "$parent" = "$p_ai"
distance="$(git rev-list --count "$p_ai..$terminal")"
test "$distance" -eq 1
commit_paths="$(git diff-tree --no-commit-id --name-only -r "$terminal" | sort)"
test "$commit_paths" = "$task_file"
range_paths="$(git diff --name-only "$p_ai..$terminal" | sort)"
test "$range_paths" = "$task_file"
mode="$(git ls-tree "$terminal" "$task_file" | awk '{print $1}')"
test "$mode" = 100644
terminal_blob="$(git rev-parse "$terminal:$test_file")"
test "$terminal_blob" = "$implementation_blob"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

XP_AI is terminal. Accepted B_AI still grants no AI-3, revalidation, or Wave C
authority. A separate approval must name the resolved full B_AI OID and the
one-attempt AI-3 transaction before it may execute.

- [ ] **Step AI-3: In one session consume approval, run once, record E_AI, and prove it.**

  This future step is one indivisible fail-fast Bash transaction. All lineage,
  subject, path, mode, frozen-blob, accepted-row, and clean-B preflight checks
  finish before an atomic Task-only in-progress guard is written. The very
  next command is the one existing byte-safe wrapper call. The same session
  converts the guard and current Task evidence to only the sanitized canonical
  result, commits Task-only E_AI, and proves the commit. Canonical nonzero and
  internal results are committed truthfully and can only lead to XE_AI. Any
  failure after the guard is written consumes the approval and prohibits
  cleanup or retry without a separately approved recovery design.

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
b_4af=7e32c37cafde08b108ee33e3439cda3aea336961
i=a7d05b0e5c0ffaeccde9e401450e696855cfb2b5
d_ag=737838fe80880b7eadbfb1c7e18d8dc251bcc8b9
p_ag=f2a4b5041222c48f392bc251eae014655cee7b7c
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_ah=9ff217e63eaf452871cfc3ef47775e0fbd03e706
d_ai=88f55837be251318cd697bd8a1ab3a4f0ed1a824
p_subject='docs(plan): define session-bound collision-safe proof'
b_subject='docs(task): record session-bound collision-safe plan reviews'
xp_subject='docs(task): record exhausted session-bound collision-safe plan review'
e_subject='docs(task): record session-bound collision-safe revalidation'
r_subject='docs(task): record session-bound collision-safe review'
xe_subject='docs(task): record exhausted session-bound collision-safe review'
approved_b_ai_oid="${APPROVED_B_AI_OID:?explicit approved B_AI OID required}"
[[ "$approved_b_ai_oid" =~ ^[0-9a-f]{40}$ ]]
resolve_unique_subject() {
  local subject="$1"
  local count
  local oid
  count="$(git log --all --format='%s' | grep -Fxc "$subject")"
  test "$count" -eq 1
  oid="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$subject" '$2 == s {print $1}')"
  test -n "$oid"
  printf '%s\n' "$oid"
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(git rev-list --count "$parent..$child")"
  test "$distance" -eq 1
  parent_count="$(git rev-list --parents -n 1 "$child" | awk '{print NF - 1}')"
  test "$parent_count" -eq 1
  first_parent="$(git rev-parse "$child^1")"
  test "$first_parent" = "$parent"
}
assert_paths() {
  local commit="$1"
  shift
  local actual
  local expected
  actual="$(git diff-tree --no-commit-id --name-only -r "$commit" | sort)"
  expected="$(printf '%s\n' "$@" | sort)"
  test "$actual" = "$expected"
}
assert_range_paths() {
  local range="$1"
  shift
  local actual
  local expected
  actual="$(git diff --name-only "$range" | sort)"
  expected="$(printf '%s\n' "$@" | sort)"
  test "$actual" = "$expected"
}
assert_mode() {
  local commit="$1"
  local file_path="$2"
  local mode
  mode="$(git ls-tree "$commit" "$file_path" | awk '{print $1}')"
  test "$mode" = 100644
}
p_ai="$(resolve_unique_subject "$p_subject")"
b_ai="$(resolve_unique_subject "$b_subject")"
test "$b_ai" = "$approved_b_ai_oid"
xp_count="$(git log --all --format='%s' | awk -v subject="$xp_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xp_count" -eq 0
head_commit="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_commit" = "$b_ai"
subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record exhausted status-based silent-success plan review'
  'docs(plan): define collision-safe disposition proof'
  'docs(task): record exhausted collision-safe disposition plan review'
  "$p_subject"
  "$b_subject"
)
commits=("$b_4af" "$i" "$d_ag" "$p_ag" "$d_ah" "$p_ah" "$d_ai" "$p_ai" "$b_ai")
for index in "${!commits[@]}"; do
  verified="$(git rev-parse --verify "${commits[$index]}^{commit}")"
  test "$verified" = "${commits[$index]}"
  actual_subject="$(git show -s --format=%s "${commits[$index]}")"
  test "$actual_subject" = "${subjects[$index]}"
  subject_count="$(git log --all --format='%s' | grep -Fxc "${subjects[$index]}")"
  test "$subject_count" -eq 1
done
assert_edge "$b_4af" "$i"
assert_edge "$i" "$d_ag"
assert_edge "$d_ag" "$p_ag"
assert_edge "$p_ag" "$d_ah"
assert_edge "$d_ah" "$p_ah"
assert_edge "$p_ah" "$d_ai"
assert_edge "$d_ai" "$p_ai"
assert_edge "$p_ai" "$b_ai"
assert_paths "$b_4af" "$task_file"
assert_paths "$i" "$task_file" "$test_file"
assert_paths "$d_ag" "$task_file"
assert_paths "$p_ag" "$plan_file" "$task_file"
assert_paths "$d_ah" "$task_file"
assert_paths "$p_ah" "$plan_file" "$task_file"
assert_paths "$d_ai" "$task_file"
assert_paths "$p_ai" "$plan_file" "$task_file"
assert_paths "$b_ai" "$task_file"
assert_range_paths "$b_4af..$i" "$task_file" "$test_file"
assert_range_paths "$d_ah..$p_ah" "$plan_file" "$task_file"
assert_range_paths "$d_ai..$p_ai" "$plan_file" "$task_file"
assert_range_paths "$p_ai..$b_ai" "$task_file"
for commit_path in \
  "$b_4af:$task_file" \
  "$i:$task_file" "$i:$test_file" \
  "$d_ag:$task_file" \
  "$p_ag:$plan_file" "$p_ag:$task_file" \
  "$d_ah:$task_file" \
  "$p_ah:$plan_file" "$p_ah:$task_file" \
  "$d_ai:$task_file" \
  "$p_ai:$plan_file" "$p_ai:$task_file" \
  "$b_ai:$task_file"
do
  assert_mode "${commit_path%%:*}" "${commit_path#*:}"
done
implementation_blob="$(git rev-parse "$i:$test_file")"
test -n "$implementation_blob"
b_ai_blob="$(git rev-parse "$b_ai:$test_file")"
test "$b_ai_blob" = "$implementation_blob"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
python3 - "$task_file" "$d_ai" "$p_ai" <<'PY'
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
lines = text.splitlines()


def exact_line(expected):
    if lines.count(expected) != 1:
        raise SystemExit(f"preflight-line-count:{expected}")


def exact_row(label):
    candidates = []
    for source_line in lines:
        line = source_line.strip(" \t")
        view = line[1:] if line.startswith("|") else line
        separator = view.find("|")
        if separator >= 0 and view[:separator].strip(" \t") == label:
            candidates.append(line)
    if len(candidates) != 1:
        raise SystemExit(f"preflight-row-count:{label}")
    row = candidates[0]
    if not row.startswith("|") or not row.endswith("|") or "\\|" in row or "\\`" in row:
        raise SystemExit(f"preflight-row-shape:{label}")
    parts = row.split("|")
    if len(parts) != 9 or parts[0] or parts[-1]:
        raise SystemExit(f"preflight-row-cells:{label}")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if len(cells) != 7 or cells[0] != label:
        raise SystemExit(f"preflight-row-label:{label}")
    if cells[1] != "Controller":
        raise SystemExit(f"preflight-row-owner:{label}")
    return cells


plan = exact_row("T-TSDC-004R-4AI session-bound collision-safe Plan")
expected_plan = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    f"`{sys.argv[2]}..{sys.argv[3]}`",
    "accepted; B_AI resolved by its exact unique subject",
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
]
if plan[2:7] != expected_plan:
    raise SystemExit("preflight-plan")
frozen = exact_row("T-TSDC-004R-4AI frozen canonical-row implementation")
expected_frozen = [
    "blocked; revalidation not run",
    "blocked; revalidation not run",
    "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5`",
    "blocked; separately approved revalidation not run",
    "Frozen implementation remains historical; no composite-review authority",
]
if frozen[2:7] != expected_frozen:
    raise SystemExit("preflight-frozen")
revalidation = exact_row("T-TSDC-004R-4AI session-bound collision-safe revalidation")
expected_revalidation = [
    "blocked; revalidation not run",
    "blocked; revalidation not run",
    "awaiting exact reviewed range",
    "blocked; separately approved revalidation not run",
    "B_AI accepted; approval not yet consumed; E_AI, R_AI, and XE_AI are not created",
]
if revalidation[2:7] != expected_revalidation:
    raise SystemExit("preflight-revalidation")
exact_line("- 4AI transaction state: not-run; separate approval required.")
exact_line("- 4AI sanitized result: not-run.")
exact_line(
    "- 4AI revalidation approval owner/source: separate future User / Controller approval "
    "required; not consumed."
)
exact_line(
    "- 4AI `APPROVED_B_AI_OID`: awaiting a separate approval naming the resolved full B_AI OID."
)
exact_line(
    "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit "
    "in one fail-fast session without changing frozen implementation | Plan/evidence | TSDC-010–014 | "
    "accepted fresh Plan reviews over exact `D_AI..P_AI`; separate revalidation approval required | "
    "controller and future fresh independent reviewers | B_AI accepted and resolved by its exact unique "
    "subject; separate one-attempt approval required; no downstream authority |"
)
exact_line(
    "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | Not run; B_AI accepted "
    "by both fresh Plan reviews; separate one-attempt approval not granted or consumed; E_AI is not created. |"
)
exact_line(
    "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, one wrapper "
    "call, sanitized result, and Task-only E_AI in one session | Not run; B_AI accepted; separate one-attempt "
    "approval not granted or consumed |"
)
exact_line(
    "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
    "`docs(task): record session-bound collision-safe revalidation` | not created | Blocked pending separate "
    "one-attempt approval naming the resolved full B_AI OID. |"
)
exact_line(
    "Current 4AI final handoff: B_AI accepted and resolved by its exact unique subject; separate one-attempt "
    "revalidation approval required; E_AI/R_AI/XE_AI not created; no downstream authority."
)
if re.search(r"result status=\d+ output=(?:empty|nonempty|internal)", text, flags=re.ASCII):
    raise SystemExit("preflight-premature-result")
PY
wrapper_status=0
e_pre_count="$(git log --all --format='%s' | awk -v subject="$e_subject" '$0 == subject {count++} END {print count + 0}')"
test "$e_pre_count" -eq 0
r_pre_count="$(git log --all --format='%s' | awk -v subject="$r_subject" '$0 == subject {count++} END {print count + 0}')"
test "$r_pre_count" -eq 0
xe_pre_count="$(git log --all --format='%s' | awk -v subject="$xe_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xe_pre_count" -eq 0
python3 - "$task_file" "$approved_b_ai_oid" <<'PY'
import os
import pathlib
import stat
import sys
import tempfile

path = pathlib.Path(sys.argv[1])
approved_b_ai_oid = sys.argv[2]
if len(approved_b_ai_oid) != 40 or any(character not in "0123456789abcdef" for character in approved_b_ai_oid):
    raise SystemExit("guard-approved-oid")
text = path.read_text(encoding="utf-8")
replacements = {
    "- 4AI transaction state: not-run; separate approval required.":
        "- 4AI transaction state: in-progress; approval consumed; retry and cleanup require recovery approval.",
    "- 4AI sanitized result: not-run.":
        "- 4AI sanitized result: pending.",
    "- 4AI revalidation approval owner/source: separate future User / Controller approval required; not consumed.":
        "- 4AI revalidation approval owner/source: User / Controller; exact one-attempt AI-3 approval consumed by in-progress guard.",
    "- 4AI `APPROVED_B_AI_OID`: awaiting a separate approval naming the resolved full B_AI OID.":
        f"- 4AI `APPROVED_B_AI_OID`: `{approved_b_ai_oid}`; validated against the unique accepted B_AI subject.",
    (
        "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | Not run; B_AI accepted "
        "by both fresh Plan reviews; separate one-attempt approval not granted or consumed; E_AI is not created. |"
    ): (
        "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | In progress; User / "
        f"Controller approval naming B_AI `{approved_b_ai_oid}` consumed by the guard; wrapper call is the "
        "immediate next command; E_AI is not created. |"
    ),
    (
        "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, one wrapper "
        "call, sanitized result, and Task-only E_AI in one session | Not run; B_AI accepted; separate one-attempt "
        "approval not granted or consumed |"
    ): (
        "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, one wrapper "
        "call, sanitized result, and Task-only E_AI in one session | In progress; approval consumed by the guard; "
        "wrapper is the immediate next command |"
    ),
    (
        "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
        "`docs(task): record session-bound collision-safe revalidation` | not created | Blocked pending separate "
        "one-attempt approval naming the resolved full B_AI OID. |"
    ): (
        "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
        "`docs(task): record session-bound collision-safe revalidation` | in-progress; not committed | Approval "
        f"naming B_AI `{approved_b_ai_oid}` consumed; retry and cleanup require recovery approval. |"
    ),
}
residue = tuple(path.parent.glob(f".{path.name}.*"))
if residue:
    raise SystemExit("guard-temp-residue")
for old, new in replacements.items():
    if text.count(old) != 1 or old == new or new in text:
        raise SystemExit("guard-replacement-shape")
for old, new in replacements.items():
    text = text.replace(old, new, 1)
source_mode = stat.S_IMODE(path.stat().st_mode)
temporary = None
try:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = pathlib.Path(stream.name)
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, source_mode)
    os.replace(temporary, path)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_fd = os.open(path.parent, directory_flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    temporary = None
finally:
    # Preserve any crash residue as a fail-closed rerun blocker.
    pass
PY
wrapper_output="$({
  python3 - \
    python3 scripts/validation/check-target-surface-delta-contract.py \
    --mode advisory <<'PY'
import os
import subprocess
import sys

RESERVED = 125


def run_once(argv, runner=subprocess.run):
    try:
        if not argv:
            raise ValueError("missing argv")
        completed = runner(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            shell=False,
        )
        rc = completed.returncode
        payload = completed.stdout
        if (
            isinstance(rc, bool)
            or not isinstance(rc, int)
            or rc < 0
            or rc > 255
            or not isinstance(payload, (bytes, bytearray))
        ):
            return RESERVED, "internal"
        return rc, "nonempty" if payload else "empty"
    except Exception:
        return RESERVED, "internal"


def render(rc, output_class):
    return f"result status={rc} output={output_class}\n".encode("ascii")


class Completed:
    def __init__(self, returncode, stdout):
        self.returncode = returncode
        self.stdout = stdout


def require_canonical(result, expected, markers):
    if result != expected:
        raise RuntimeError("oracle-result")
    rendered = render(*result)
    expected_line = f"result status={expected[0]} output={expected[1]}\n".encode("ascii")
    if rendered != expected_line:
        raise RuntimeError("oracle-canonical")
    if any(marker in rendered for marker in markers):
        raise RuntimeError("oracle-raw-leak")


def oracle():
    markers = (b"stderr-merged-raw-marker", b"successor-marker")
    cases = (
        (0, b"", (0, "empty")),
        (0, b"\n", (0, "nonempty")),
        (0, b"stderr-merged-raw-marker", (0, "nonempty")),
        (0, b"\x1e", (0, "nonempty")),
        (0, b"\x00", (0, "nonempty")),
        (23, b"", (23, "empty")),
        (23, b"successor-marker", (23, "nonempty")),
        (125, b"", (125, "empty")),
        (125, b"stderr-merged-raw-marker", (125, "nonempty")),
        (-9, b"", (125, "internal")),
        (256, b"", (125, "internal")),
        (0, "invalid-stdout", (125, "internal")),
    )
    expected_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "check": False,
        "shell": False,
    }
    for returncode, stdout, expected in cases:
        calls = []

        def fake(argv, **kwargs):
            calls.append((argv, kwargs))
            return Completed(returncode, stdout)

        result = run_once(["fake-validator"], fake)
        if calls != [(["fake-validator"], expected_kwargs)]:
            raise RuntimeError("oracle-call-count-or-shape")
        require_canonical(result, expected, markers)
    exception_calls = []

    def raising_runner(argv, **kwargs):
        exception_calls.append((argv, kwargs))
        raise RuntimeError("runner failure")

    exception_result = run_once(["fake-validator"], raising_runner)
    if exception_calls != [(["fake-validator"], expected_kwargs)]:
        raise RuntimeError("oracle-exception-call-count")
    require_canonical(exception_result, (125, "internal"), markers)
    missing_calls = []

    def forbidden_runner(argv, **kwargs):
        missing_calls.append((argv, kwargs))
        return Completed(0, b"")

    missing_result = run_once([], forbidden_runner)
    if missing_calls:
        raise RuntimeError("oracle-missing-call-count")
    require_canonical(missing_result, (125, "internal"), markers)


def main():
    oracle()
    expected_argv = [
        "python3",
        "scripts/validation/check-target-surface-delta-contract.py",
        "--mode",
        "advisory",
    ]
    if sys.argv[1:] != expected_argv:
        raise RuntimeError("real-argv")
    real_calls = []

    def counted_runner(argv, **kwargs):
        real_calls.append((argv, kwargs))
        return subprocess.run(argv, **kwargs)

    rc, output_class = run_once(sys.argv[1:], counted_runner)
    expected_real_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "check": False,
        "shell": False,
    }
    if real_calls != [(expected_argv, expected_real_kwargs)]:
        raise RuntimeError("real-call-count-or-shape")
    canonical = render(rc, output_class)
    written = os.write(1, canonical)
    if written != len(canonical):
        raise RuntimeError("canonical-short-write")
    return rc


try:
    rc = main()
except Exception:
    rc = RESERVED
    try:
        internal = render(RESERVED, "internal")
        written = os.write(1, internal)
        if written != len(internal):
            raise RuntimeError("internal-short-write")
    except Exception:
        pass
raise SystemExit(rc)
PY
})" || wrapper_status=$?
case "$wrapper_output" in
  "result status=$wrapper_status output=empty")
    output_class=empty
    ;;
  "result status=$wrapper_status output=nonempty")
    output_class=nonempty
    ;;
  'result status=125 output=internal')
    test "$wrapper_status" -eq 125
    output_class=internal
    ;;
  *)
    exit 125
    ;;
esac
writer_e_task_blob="$({ python3 - \
  "$task_file" "$wrapper_status" "$output_class" "$approved_b_ai_oid" <<'PY'
import hashlib
import os
import pathlib
import stat
import sys
import tempfile

path = pathlib.Path(sys.argv[1])
try:
    status = int(sys.argv[2], 10)
except ValueError:
    raise SystemExit("outcome-status")
output_class = sys.argv[3]
approved_b_ai_oid = sys.argv[4]
if status < 0 or status > 255:
    raise SystemExit("outcome-status-range")
if output_class not in {"empty", "nonempty", "internal"}:
    raise SystemExit("outcome-class")
if output_class == "internal" and status != 125:
    raise SystemExit("outcome-internal-status")
if len(approved_b_ai_oid) != 40 or any(character not in "0123456789abcdef" for character in approved_b_ai_oid):
    raise SystemExit("outcome-approved-oid")
text = path.read_text(encoding="utf-8")
old_frozen = (
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
    "blocked; revalidation not run | blocked; revalidation not run | "
    "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "blocked; separately approved revalidation not run | Frozen implementation "
    "remains historical; no composite-review authority |"
)
new_frozen = (
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
    "pending fresh independent review | pending fresh independent review | "
    "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "E_AI committed; fresh composite reviews pending; no downstream authority | "
    "Frozen historical implementation and test blob await exact composite review |"
)
old_revalidation = (
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
    "blocked; revalidation not run | blocked; revalidation not run | awaiting exact reviewed range | "
    "blocked; separately approved revalidation not run | B_AI accepted; approval not yet "
    "consumed; E_AI, R_AI, and XE_AI are not created |"
)
new_revalidation = (
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
    "pending fresh independent review | pending fresh independent review | awaiting exact reviewed range | "
    "E_AI committed; fresh composite reviews pending; no downstream authority | Revalidation "
    f"approval consumed; result status={status} output={output_class}; E_AI resolved by its exact "
    "unique subject; no future OID is claimed in its own tree |"
)
replacements = {
    "- 4AI transaction state: in-progress; approval consumed; retry and cleanup require recovery approval.":
        "- 4AI transaction state: completed; approval consumed; no retry authority.",
    "- 4AI sanitized result: pending.":
        f"- 4AI sanitized result: result status={status} output={output_class}.",
    "- 4AI revalidation approval owner/source: User / Controller; exact one-attempt AI-3 approval consumed by in-progress guard.":
        "- 4AI revalidation approval owner/source: User / Controller; exact one-attempt AI-3 approval consumed.",
    (
        "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
        "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
        "agent; original agents remain historical | active; B_AI accepted and resolved by its exact unique "
        "subject; separate revalidation approval required; no downstream authority |"
    ): (
        "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
        "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
        "agent; original agents remain historical | active; E_AI committed and resolved by its exact unique "
        "subject; fresh composite reviews pending; no downstream authority |"
    ),
    (
        "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit in one "
        "fail-fast session without changing frozen implementation | Plan/evidence | TSDC-010–014 | accepted "
        "fresh Plan reviews over exact `D_AI..P_AI`; separate revalidation approval required | controller and "
        "future fresh independent reviewers | B_AI accepted and resolved by its exact unique subject; separate "
        "one-attempt approval required; no downstream authority |"
    ): (
        "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit in one "
        "fail-fast session without changing frozen implementation | Plan/evidence | TSDC-010–014 | immutable "
        "E_AI evidence plus two future fresh composite reviews | controller and future fresh independent "
        "reviewers | E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; "
        "no downstream authority |"
    ),
    (
        "| T-TSDC-006 | Promote blocking enforcement and close reviews | closure/QA | TSDC-001–017 | "
        "final ladder and whole-branch reviews | fresh closure implementer after Tasks 1–5 | blocked; Task 5 "
        "and Wave C authority are absent while 4AI Plan reviews are pending |"
    ): (
        "| T-TSDC-006 | Promote blocking enforcement and close reviews | closure/QA | TSDC-001–017 | "
        "final ladder and whole-branch reviews | fresh closure implementer after Tasks 1–5 | blocked; E_AI "
        "is committed but accepted R_AI, Wave C, and Task 5 completion are absent |"
    ),
    (
        "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | In progress; User / "
        f"Controller approval naming B_AI `{approved_b_ai_oid}` consumed by the guard; wrapper call is the "
        "immediate next command; E_AI is not created. |"
    ): (
        "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | Completed in one "
        f"fail-fast session; approval naming B_AI `{approved_b_ai_oid}` consumed; result status={status} "
        f"output={output_class}; E_AI resolved by its exact unique subject; fresh composite reviews pending. |"
    ),
    (
        "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Not run; E_AI, R_AI, and XE_AI "
        "are not created. |"
    ): (
        "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Pending two fresh independent "
        "reviews over immutable E_AI evidence; R_AI and XE_AI are not created. |"
    ),
    (
        "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, one wrapper "
        "call, sanitized result, and Task-only E_AI in one session | In progress; approval consumed by the guard; "
        "wrapper is the immediate next command |"
    ): (
        "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, one wrapper "
        f"call, sanitized result, and Task-only E_AI in one session | Completed; B_AI `{approved_b_ai_oid}`; "
        f"result status={status} output={output_class}; E_AI resolved by its exact unique subject |"
    ),
    (
        "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly "
        "one R_AI/XE_AI terminal | Not run; E_AI, R_AI, and XE_AI are not created |"
    ): (
        "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly "
        "one R_AI/XE_AI terminal | Pending; E_AI committed; fresh composite reviews not yet recorded |"
    ),
    (
        "| T-TSDC-004 | Historical 4AF RED evidence and rejected 4AG/4AH Plan history are preserved; 4AI "
        "changes only Plan/Task evidence design and adds no product RED. | Historical GREEN evidence is "
        "preserved; 4AI ran no tests, validators, wrapper, proof, or revalidation. | P_AI committed; resolved "
        "by its exact unique subject; fresh Plan reviews pending; no downstream authority. | active Task 4; "
        "4AI Plan review pending; no Wave C authority |"
    ): (
        "| T-TSDC-004 | Historical 4AF RED evidence and rejected 4AG/4AH Plan history are preserved; 4AI "
        "changes only Plan/Task evidence design and adds no product RED. | Frozen product GREEN evidence "
        f"remains unchanged; the separately approved evidence-only wrapper returned status={status} "
        f"output={output_class}. | E_AI committed and resolved by its exact unique subject; fresh composite "
        "reviews pending; no downstream authority. | active Task 4; 4AI composite review pending; no Wave C authority |"
    ),
    (
        "| T-TSDC-005 | Not run — no accepted R_AI or Wave C authority exists | Not run — no accepted R_AI "
        "or Wave C authority exists | Not run — 4AI Plan reviews are pending | blocked |"
    ): (
        "| T-TSDC-005 | Not run — no accepted R_AI or Wave C authority exists | Not run — no accepted R_AI "
        "or Wave C authority exists | E_AI committed; fresh composite reviews and accepted R_AI are pending | blocked |"
    ),
    (
        "| T-TSDC-006 | Not run — Wave C and Task 5 blocked | Not run — Wave C and Task 5 blocked | "
        "Not run — 4AI has no downstream authority | blocked |"
    ): (
        "| T-TSDC-006 | Not run — accepted R_AI, Wave C, and Task 5 are absent | Not run — accepted R_AI, "
        "Wave C, and Task 5 are absent | E_AI committed; composite terminal not created | blocked |"
    ),
    (
        "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
        "`docs(task): record session-bound collision-safe revalidation` | in-progress; not committed | Approval "
        f"naming B_AI `{approved_b_ai_oid}` consumed; retry and cleanup require recovery approval. |"
    ): (
        "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
        "`docs(task): record session-bound collision-safe revalidation` | resolved by this exact unique subject | "
        f"Approval naming B_AI `{approved_b_ai_oid}` consumed; result status={status} output={output_class}; "
        "Task-only E_AI committed in the same fail-fast session. |"
    ),
    (
        "| T-TSDC-004R-4AI accepted review R_AI | Record accepted session-bound collision-safe review | "
        "`docs(task): record session-bound collision-safe review` | future; not created | Blocked pending E_AI "
        "plus two accepted fresh composite reviews; only this accepted terminal may authorize Task 4.5/Wave C. |"
    ): (
        "| T-TSDC-004R-4AI accepted review R_AI | Record accepted session-bound collision-safe review | "
        "`docs(task): record session-bound collision-safe review` | not created | Pending two accepted fresh "
        "composite reviews and accepting immutable E_AI result; mutually exclusive with XE_AI. |"
    ),
    (
        "| T-TSDC-004R-4AI rejected review XE_AI | Record exhausted session-bound collision-safe review | "
        "`docs(task): record exhausted session-bound collision-safe review` | future; not created | Blocked "
        "pending E_AI; required terminal for any nonzero/internal E evidence or non-accepted composite review "
        "and grants no downstream authority. |"
    ): (
        "| T-TSDC-004R-4AI rejected review XE_AI | Record exhausted session-bound collision-safe review | "
        "`docs(task): record exhausted session-bound collision-safe review` | not created | Pending composite "
        "disposition; mandatory for nonzero/internal E_AI evidence or either non-accepted fresh review; mutually "
        "exclusive with R_AI. |"
    ),
    (
        "| T-TSDC-006 | pending | pending | pending | not available | blocked | Wave C and Task 5 remain "
        "blocked while 4AI Plan reviews are pending. |"
    ): (
        "| T-TSDC-006 | pending | pending | pending | not available | blocked | E_AI is committed; accepted "
        "R_AI, Wave C, and Task 5 completion remain absent. |"
    ),
    (
        "| Whole branch | not applicable | pending final fresh reviewer after accepted R_AI, Wave C, and Tasks "
        "5–6 | pending different final fresh reviewer after accepted R_AI, Wave C, and Tasks 5–6 | not available | "
        "blocked | P_AI has no downstream authority; historical 4AF/4AG/4AH evidence cannot authorize Wave C, "
        "Tasks 5–6, or final branch review. |"
    ): (
        "| Whole branch | not applicable | pending final fresh reviewer after accepted R_AI, Wave C, and Tasks "
        "5–6 | pending different final fresh reviewer after accepted R_AI, Wave C, and Tasks 5–6 | not available | "
        "blocked | E_AI and pending composite reviews grant no Wave C, Tasks 5–6, or final branch-review authority. |"
    ),
    (
        "| T-TSDC-004R-3 atomic projection cutover | blocked; accepted B_AI but revalidation not approved | "
        "Historical 4AF and rejected/exhausted 4AG/4AH evidence remain frozen. B_AI is the sole accepted Plan "
        "terminal; XP_AI/E_AI/R_AI/XE_AI are not created; no downstream authority. | obtain separate one-attempt "
        "approval naming the resolved full B_AI OID; only later accepted R_AI may unlock Wave C |"
    ): (
        "| T-TSDC-004R-3 atomic projection cutover | blocked; E_AI committed and composite reviews pending | "
        f"B_AI `{approved_b_ai_oid}` is accepted, XP_AI is not created, and E_AI records result status={status} "
        f"output={output_class}; R_AI/XE_AI are not created and no downstream authority exists. | complete two "
        "fresh composite reviews over immutable E_AI evidence and exactly one R_AI/XE_AI terminal; only accepted "
        "R_AI may unlock Wave C |"
    ),
    (
        "Current 4AI final handoff: B_AI accepted and resolved by its exact unique subject; separate one-attempt "
        "revalidation approval required; E_AI/R_AI/XE_AI not created; no downstream authority."
    ): (
        f"Current 4AI final handoff: E_AI committed in the approval-consuming session with result status={status} "
        f"output={output_class}; B_AI `{approved_b_ai_oid}` approved and XP_AI absent; fresh composite reviews "
        "pending; R_AI/XE_AI not created; no downstream authority."
    ),
    (
        "- The active 4AI checkpoint has accepted B_AI, but revalidation is not approved. XP_AI, E_AI,\n"
        "  R_AI, and XE_AI are uncreated and do not establish Task 4.5, Wave C, downstream, runtime,\n"
        "  or remote authority."
    ): (
        "- The active 4AI checkpoint has immutable E_AI evidence and pending fresh composite reviews. XP_AI,\n"
        "  R_AI, and XE_AI are uncreated; E_AI alone does not establish Task 4.5, Wave C, downstream, runtime,\n"
        "  or remote authority."
    ),
    (
        "- D_AI is the clean Task-only XP_AH terminal\n"
        "  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`. Historical 4AG and 4AH rows,\n"
        "  OIDs, ranges, and verdicts remain immutable evidence. P_AI is the current\n"
        "  Plan-and-Task-only checkpoint with exact subject\n"
        "  `docs(plan): define session-bound collision-safe proof`; this tree states\n"
        "  exactly: “P_AI committed; resolved by its exact unique subject; fresh Plan\n"
        "  reviews pending; no downstream authority”."
    ): (
        "- D_AI remains the clean Task-only XP_AH terminal\n"
        "  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`; P_AI and accepted B_AI are immutable lineage\n"
        f"  evidence. The current checkpoint is Task-only E_AI with approved B_AI `{approved_b_ai_oid}`,\n"
        f"  canonical result status={status} output={output_class}, and pending fresh composite reviews."
    ),
    (
        "- The prospective accepted lineage is `B_4AF -> I -> D_AG -> P_AG -> D_AH ->\n"
        "  P_AH -> XP_AH/D_AI -> P_AI -> B_AI -> E_AI -> R_AI`. The exact Plan-review\n"
        "  range is future `D_AI..P_AI`. Exactly one Task-only B_AI or XP_AI may record\n"
        "  those two fresh reviews. B_AI alone grants no wrapper, revalidation,\n"
        "  composite-review, implementation, Task 4.5, or Wave C authority."
    ): (
        "- The realized evidence lineage is `B_4AF -> I -> D_AG -> P_AG -> D_AH -> P_AH ->\n"
        "  XP_AH/D_AI -> P_AI -> B_AI -> E_AI`; XP_AI is absent. E_AI alone grants no implementation,\n"
        "  Task 4.5, or Wave C authority; exactly one future R_AI/XE_AI composite terminal remains required."
    ),
    (
        "- No 4AI validator, test, wrapper, proof, revalidation, composite review, implementation, runtime,\n"
        "  remote, Graphify, Task 4.5, or Wave C action has run. Both fresh Plan reviews accepted B_AI,\n"
        "  but separate one-attempt revalidation approval is absent and no downstream authority exists."
    ): (
        f"- The separately approved 4AI revalidation transaction ran once and committed only sanitized result "
        f"status={status} output={output_class} as E_AI. Fresh composite reviews, R_AI/XE_AI, Task 4.5, Wave C,\n"
        "  runtime, remote, Graphify, Tasks 5–6, and whole-branch review remain unexecuted and unauthorized."
    ),
    (
        "T-TSDC-004R-4AI is the current accepted-Plan successor from clean XP_AH/D_AI\n"
        "`88f55837be251318cd697bd8a1ab3a4f0ed1a824`. B_AI is accepted and resolved by its\n"
        "exact unique subject; XP_AI is not created. Separate one-attempt revalidation approval naming\n"
        "the resolved full B_AI OID is absent; E_AI, R_AI, and XE_AI are not created. No validator,\n"
        "test, wrapper, proof, revalidation, implementation, runtime, remote, Graphify, Task 4.5,\n"
        "Wave C, Tasks 5–6, or whole-branch review authority exists."
    ): (
        "T-TSDC-004R-4AI now has immutable Task-only E_AI evidence from one approval-consuming session.\n"
        f"B_AI `{approved_b_ai_oid}` is accepted and XP_AI is absent; the canonical sanitized result is\n"
        f"status={status} output={output_class}. Fresh composite reviews remain pending, so R_AI and XE_AI are\n"
        "not created and no Task 4.5, Wave C, Tasks 5–6, runtime, remote, Graphify, or whole-branch review\n"
        "authority exists."
    ),
    old_frozen: new_frozen,
    old_revalidation: new_revalidation,
}
approved_oid_line = (
    f"- 4AI `APPROVED_B_AI_OID`: `{approved_b_ai_oid}`; validated against the unique accepted B_AI subject."
)
if text.count(approved_oid_line) != 1:
    raise SystemExit("outcome-approved-oid-evidence")
residue = tuple(path.parent.glob(f".{path.name}.*"))
if residue:
    raise SystemExit("outcome-temp-residue")
for old, new in replacements.items():
    if text.count(old) != 1 or old == new or new in text:
        raise SystemExit("outcome-replacement-shape")
for old, new in replacements.items():
    text = text.replace(old, new, 1)
payload = text.encode("utf-8")
git_blob_object = b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload
writer_blob_oid = hashlib.sha1(git_blob_object, usedforsecurity=False).hexdigest()
source_mode = stat.S_IMODE(path.stat().st_mode)
temporary = None
try:
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = pathlib.Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, source_mode)
    os.replace(temporary, path)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_fd = os.open(path.parent, directory_flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    temporary = None
    oid_record = f"{writer_blob_oid}\n".encode("ascii")
    if os.write(1, oid_record) != len(oid_record):
        raise RuntimeError("outcome-blob-oid-short-write")
finally:
    # Preserve any crash residue as a fail-closed rerun blocker.
    pass
PY
})"
[[ "$writer_e_task_blob" =~ ^[0-9a-f]{40}$ ]]
unstaged_paths="$(git diff --name-only)"
test "$?" -eq 0
staged_paths="$(git diff --cached --name-only)"
test "$?" -eq 0
untracked_paths="$(git ls-files --others --exclude-standard)"
test "$?" -eq 0
dirty_paths="$(printf '%s\n' "$unstaged_paths" "$staged_paths" "$untracked_paths" | sed '/^$/d' | sort -u)"
test "$dirty_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$task_file"
staged_e_task_blob="$(git rev-parse ":$task_file")"
test "$staged_e_task_blob" = "$writer_e_task_blob"
git commit -m "$e_subject"
e_ai="$(git rev-parse --verify 'HEAD^{commit}')"
committed_e_task_blob="$(git rev-parse "$e_ai:$task_file")"
test "$committed_e_task_blob" = "$writer_e_task_blob"
actual_subject="$(git show -s --format=%s "$e_ai")"
test "$actual_subject" = "$e_subject"
subject_count="$(git log --all --format='%s' | grep -Fxc "$e_subject")"
test "$subject_count" -eq 1
xp_count="$(git log --all --format='%s' | awk -v subject="$xp_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xp_count" -eq 0
r_count="$(git log --all --format='%s' | awk -v subject="$r_subject" '$0 == subject {count++} END {print count + 0}')"
test "$r_count" -eq 0
xe_count="$(git log --all --format='%s' | awk -v subject="$xe_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xe_count" -eq 0
assert_edge "$b_ai" "$e_ai"
assert_paths "$e_ai" "$task_file"
assert_range_paths "$b_ai..$e_ai" "$task_file"
assert_mode "$e_ai" "$task_file"
e_blob="$(git rev-parse "$e_ai:$test_file")"
test "$e_blob" = "$implementation_blob"
python3 - "$task_file" "$wrapper_status" "$output_class" <<'PY'
import pathlib
import sys

text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
status = sys.argv[2]
output_class = sys.argv[3]
expected = (
    "- 4AI transaction state: completed; approval consumed; no retry authority.",
    f"- 4AI sanitized result: result status={status} output={output_class}.",
    (
        "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
        "pending fresh independent review | pending fresh independent review | "
        "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
        "E_AI committed; fresh composite reviews pending; no downstream authority | "
        "Frozen historical implementation and test blob await exact composite review |"
    ),
    (
        "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
        "pending fresh independent review | pending fresh independent review | awaiting exact reviewed range | "
        "E_AI committed; fresh composite reviews pending; no downstream authority | Revalidation "
        f"approval consumed; result status={status} output={output_class}; E_AI resolved by its exact "
        "unique subject; no future OID is claimed in its own tree |"
    ),
)
for item in expected:
    if text.count(item) != 1:
        raise SystemExit("e-ai-evidence-count")
PY
head_after="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_after" = "$e_ai"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

Before composite review, the two review rows are exactly the pending rows
written by the E_AI transaction, and the only outcome is the exact unique
`4AI sanitized result` marker. A status other than zero or `output=internal`
is valid failure evidence, never acceptance evidence.

- [ ] **Step AI-4: Parse exact composite evidence and commit R_AI or XE_AI.**

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
b_4af=7e32c37cafde08b108ee33e3439cda3aea336961
i=a7d05b0e5c0ffaeccde9e401450e696855cfb2b5
d_ag=737838fe80880b7eadbfb1c7e18d8dc251bcc8b9
p_ag=f2a4b5041222c48f392bc251eae014655cee7b7c
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_ah=9ff217e63eaf452871cfc3ef47775e0fbd03e706
d_ai=88f55837be251318cd697bd8a1ab3a4f0ed1a824
p_subject='docs(plan): define session-bound collision-safe proof'
b_subject='docs(task): record session-bound collision-safe plan reviews'
xp_subject='docs(task): record exhausted session-bound collision-safe plan review'
e_subject='docs(task): record session-bound collision-safe revalidation'
r_subject='docs(task): record session-bound collision-safe review'
xe_subject='docs(task): record exhausted session-bound collision-safe review'
resolve_unique_subject() {
  local subject="$1"
  local count
  local oid
  count="$(git log --all --format='%s' | grep -Fxc "$subject")"
  test "$count" -eq 1
  oid="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$subject" '$2 == s {print $1}')"
  test -n "$oid"
  printf '%s\n' "$oid"
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(git rev-list --count "$parent..$child")"
  test "$distance" -eq 1
  parent_count="$(git rev-list --parents -n 1 "$child" | awk '{print NF - 1}')"
  test "$parent_count" -eq 1
  first_parent="$(git rev-parse "$child^1")"
  test "$first_parent" = "$parent"
}
p_ai="$(resolve_unique_subject "$p_subject")"
b_ai="$(resolve_unique_subject "$b_subject")"
e_ai="$(resolve_unique_subject "$e_subject")"
xp_count="$(git log --all --format='%s' | awk -v subject="$xp_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xp_count" -eq 0
r_pre_count="$(git log --all --format='%s' | awk -v subject="$r_subject" '$0 == subject {count++} END {print count + 0}')"
test "$r_pre_count" -eq 0
xe_pre_count="$(git log --all --format='%s' | awk -v subject="$xe_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xe_pre_count" -eq 0
head_commit="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_commit" = "$e_ai"
e_task_status=0
e_task_text="$(git show "$e_ai:$task_file")" || e_task_status=$?
test "$e_task_status" -eq 0
test -n "$e_task_text"
selection="$({ python3 - \
  "$task_file" "$d_ai" "$p_ai" "$b_4af" "$i" "$b_ai" "$e_ai" \
  3<<<"$e_task_text" <<'PY'
import os
import pathlib
import re
import sys

labels = (
    "T-TSDC-004R-4AI session-bound collision-safe Plan",
    "T-TSDC-004R-4AI frozen canonical-row implementation",
    "T-TSDC-004R-4AI session-bound collision-safe revalidation",
)
e_text = os.fdopen(3, encoding="utf-8").read()
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
lines = text.splitlines()
e_lines = e_text.splitlines()
e_state = "- 4AI transaction state: completed; approval consumed; no retry authority."
if e_lines.count(e_state) != 1 or lines.count(e_state) != 1:
    raise SystemExit("composite-e-state")
e_results = [line for line in e_lines if line.startswith("- 4AI sanitized result: ")]
if len(e_results) != 1:
    raise SystemExit("composite-e-result-count")
match = re.fullmatch(
    r"- 4AI sanitized result: result status=(\d{1,3}) output=(empty|nonempty|internal)\.",
    e_results[0],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("composite-e-result-shape")
status = int(match.group(1), 10)
output_class = match.group(2)
if status > 255 or (output_class == "internal" and status != 125):
    raise SystemExit("composite-e-result-value")
if lines.count(e_results[0]) != 1:
    raise SystemExit("composite-current-result-drift")
immutable_e_lines = (
    "- 4AI revalidation approval owner/source: User / Controller; exact one-attempt AI-3 approval consumed.",
    f"- 4AI `APPROVED_B_AI_OID`: `{sys.argv[6]}`; validated against the unique accepted B_AI subject.",
    (
        "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
        "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
        "agent; original agents remain historical | active; E_AI committed and resolved by its exact unique "
        "subject; fresh composite reviews pending; no downstream authority |"
    ),
    (
        "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit in one "
        "fail-fast session without changing frozen implementation | Plan/evidence | TSDC-010–014 | immutable "
        "E_AI evidence plus two future fresh composite reviews | controller and future fresh independent "
        "reviewers | E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; "
        "no downstream authority |"
    ),
    (
        "| 2026-08-01 | T-TSDC-004R-4AI revalidation transaction | Controller | Completed in one fail-fast "
        f"session; approval naming B_AI `{sys.argv[6]}` consumed; result status={status} output={output_class}; "
        "E_AI resolved by its exact unique subject; fresh composite reviews pending. |"
    ),
    (
        "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Pending two fresh independent "
        "reviews over immutable E_AI evidence; R_AI and XE_AI are not created. |"
    ),
    (
        "| 4AI session-bound revalidation | Exact approved B_AI OID, one approval-consuming guard, one wrapper "
        f"call, sanitized result, and Task-only E_AI in one session | Completed; B_AI `{sys.argv[6]}`; result "
        f"status={status} output={output_class}; E_AI resolved by its exact unique subject |"
    ),
    (
        "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly "
        "one R_AI/XE_AI terminal | Pending; E_AI committed; fresh composite reviews not yet recorded |"
    ),
    (
        "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
        "`docs(task): record session-bound collision-safe revalidation` | resolved by this exact unique subject | "
        f"Approval naming B_AI `{sys.argv[6]}` consumed; result status={status} output={output_class}; "
        "Task-only E_AI committed in the same fail-fast session. |"
    ),
    (
        "| T-TSDC-004R-3 atomic projection cutover | blocked; E_AI committed and composite reviews pending | "
        f"B_AI `{sys.argv[6]}` is accepted, XP_AI is not created, and E_AI records result status={status} "
        f"output={output_class}; R_AI/XE_AI are not created and no downstream authority exists. | complete two "
        "fresh composite reviews over immutable E_AI evidence and exactly one R_AI/XE_AI terminal; only accepted "
        "R_AI may unlock Wave C |"
    ),
    (
        f"Current 4AI final handoff: E_AI committed in the approval-consuming session with result status={status} "
        f"output={output_class}; B_AI `{sys.argv[6]}` approved and XP_AI absent; fresh composite reviews pending; "
        "R_AI/XE_AI not created; no downstream authority."
    ),
)
for immutable_line in immutable_e_lines:
    if e_lines.count(immutable_line) != 1 or lines.count(immutable_line) != 1:
        raise SystemExit("composite-e-immutable-surface")
e_plan_row = (
    "| T-TSDC-004R-4AI session-bound collision-safe Plan | Controller | "
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | "
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES | "
    f"`{sys.argv[2]}..{sys.argv[3]}` | accepted; B_AI resolved by its exact unique subject | "
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority |"
)
e_frozen_row = (
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | pending fresh independent review | "
    "pending fresh independent review | `7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "E_AI committed; fresh composite reviews pending; no downstream authority | Frozen historical "
    "implementation and test blob await exact composite review |"
)
e_revalidation_row = (
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | pending fresh independent "
    "review | pending fresh independent review | awaiting exact reviewed range | E_AI committed; fresh "
    "composite reviews pending; no downstream authority | Revalidation approval consumed; "
    f"result status={status} output={output_class}; E_AI resolved by its exact unique subject; no future OID "
    "is claimed in its own tree |"
)
for pending_row in (e_plan_row, e_frozen_row, e_revalidation_row):
    if e_lines.count(pending_row) != 1:
        raise SystemExit("composite-e-pending-row")
if lines.count(e_plan_row) != 1:
    raise SystemExit("composite-current-plan-row")
found = {label: [] for label in labels}
for source_line in lines:
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0:
        first_cell = view[:separator].strip(" \t")
        if first_cell in found:
            found[first_cell].append(line)
if any(len(found[label]) != 1 for label in labels):
    raise SystemExit("composite-candidate-count")
rows = []
for label in labels:
    row = found[label][0]
    if not row.startswith("|") or not row.endswith("|"):
        raise SystemExit("composite-shape")
    if "\\|" in row or "\\`" in row:
        raise SystemExit("composite-escape")
    parts = row.split("|")
    if len(parts) != 9 or parts[0] or parts[-1]:
        raise SystemExit("composite-cell-count")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if len(cells) != 7 or cells[0] != label:
        raise SystemExit("composite-label")
    if cells[1] != "Controller":
        raise SystemExit("composite-owner")
    if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
        raise SystemExit("composite-extra-range")
    if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
        raise SystemExit("composite-range-shape")
    rows.append(cells)
plan, frozen, revalidation = rows
expected_plan = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    f"`{sys.argv[2]}..{sys.argv[3]}`",
    "accepted; B_AI resolved by its exact unique subject",
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
]
if plan[2:7] != expected_plan:
    raise SystemExit("composite-plan")
if frozen[4] != f"`{sys.argv[4]}..{sys.argv[5]}`":
    raise SystemExit("composite-frozen-range")
if revalidation[4] != f"`{sys.argv[6]}..{sys.argv[7]}`":
    raise SystemExit("composite-revalidation-range")
spec_re = r"C\d+/I\d+/M\d+; SPEC_COMPLIANCE (YES|NO); COMMIT_READY (YES|NO)"
quality_re = r"C\d+/I\d+/M\d+; QUALITY_SECURITY (PASS|FAIL); COMMIT_READY (YES|NO)"
for cells in (frozen, revalidation):
    if re.fullmatch(spec_re, cells[2], flags=re.ASCII) is None:
        raise SystemExit("composite-spec-verdict")
    if re.fullmatch(quality_re, cells[3], flags=re.ASCII) is None:
        raise SystemExit("composite-quality-verdict")
if frozen[2:4] != revalidation[2:4]:
    raise SystemExit("composite-divergent-verdicts")
state = "- 4AI transaction state: completed; approval consumed; no retry authority."
if lines.count(state) != 1:
    raise SystemExit("composite-state-count")
result_candidates = [
    line
    for line in lines
    if line.startswith("- 4AI sanitized result: ")
]
if len(result_candidates) != 1:
    raise SystemExit("composite-result-count")
match = re.fullmatch(
    r"- 4AI sanitized result: result status=(\d{1,3}) output=(empty|nonempty|internal)\.",
    result_candidates[0],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("composite-result-shape")
status = int(match.group(1), 10)
output_class = match.group(2)
if status > 255 or (output_class == "internal" and status != 125):
    raise SystemExit("composite-result-value")
accepted_verdicts = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES",
]
reviews_accepted = frozen[2:4] == accepted_verdicts
outcome_accepted = status == 0 and output_class in {"empty", "nonempty"}
accepted = reviews_accepted and outcome_accepted
if accepted:
    expected_frozen = [
        "accepted; frozen implementation approved in 4AI composite review",
        "Composite reviewers accepted exact frozen implementation and session-bound revalidation ranges; frozen test blob preserved",
    ]
    expected_revalidation = [
        "accepted; R_AI resolved by its exact unique subject",
        f"Revalidation result status={status} output={output_class} and both fresh composite reviews accepted; Task 4.5 authority granted",
    ]
else:
    expected_frozen = [
        "rejected/exhausted; frozen implementation not approved in 4AI composite review",
        "One or both fresh composite reviews rejected or sanitized revalidation outcome was non-accepting; frozen history grants no downstream authority",
    ]
    expected_revalidation = [
        "rejected/exhausted; XE_AI resolved by its exact unique subject",
        f"Revalidation result status={status} output={output_class} was non-accepting or one or both fresh composite reviews rejected; no correction, retry, or Wave C authority",
    ]
if frozen[5:7] != expected_frozen:
    raise SystemExit("composite-frozen-outcome")
if revalidation[5:7] != expected_revalidation:
    raise SystemExit("composite-revalidation-outcome")
normalized = text
for e_row, current_row in (
    (e_frozen_row, found[labels[1]][0]),
    (e_revalidation_row, found[labels[2]][0]),
):
    if normalized.count(current_row) != 1 or current_row == e_row:
        raise SystemExit("composite-normalization-shape")
    normalized = normalized.replace(current_row, e_row, 1)
if normalized != e_text:
    raise SystemExit("composite-e-terminal-diff-scope")
print("R_AI" if accepted else "XE_AI")
PY
})"
test "$selection" = R_AI || test "$selection" = XE_AI
case "$selection" in
  R_AI)
    terminal_subject="$r_subject"
    opposite_subject="$xe_subject"
    ;;
  XE_AI)
    terminal_subject="$xe_subject"
    opposite_subject="$r_subject"
    ;;
esac
selected_pre_count="$(git log --all --format='%s' | awk -v subject="$terminal_subject" '$0 == subject {count++} END {print count + 0}')"
test "$selected_pre_count" -eq 0
opposite_pre_count="$(git log --all --format='%s' | awk -v subject="$opposite_subject" '$0 == subject {count++} END {print count + 0}')"
test "$opposite_pre_count" -eq 0
python3 - \
  "$task_file" "$selection" "$d_ai" "$p_ai" "$b_4af" "$i" "$b_ai" "$e_ai" \
  3<<<"$e_task_text" <<'PY'
import os
import pathlib
import re
import stat
import sys
import tempfile

path = pathlib.Path(sys.argv[1])
selection = sys.argv[2]
e_text = os.fdopen(3, encoding="utf-8").read()
current_text = path.read_text(encoding="utf-8")
result_candidates = [line for line in e_text.splitlines() if line.startswith("- 4AI sanitized result: ")]
if len(result_candidates) != 1:
    raise SystemExit("terminal-e-result-count")
match = re.fullmatch(
    r"- 4AI sanitized result: result status=(\d{1,3}) output=(empty|nonempty|internal)\.",
    result_candidates[0],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("terminal-e-result-shape")
status = int(match.group(1), 10)
output_class = match.group(2)
if status > 255 or (output_class == "internal" and status != 125):
    raise SystemExit("terminal-e-result-value")
accepted = selection == "R_AI"
if selection not in {"R_AI", "XE_AI"}:
    raise SystemExit("terminal-selection")
e_frozen = (
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | pending fresh independent review | "
    "pending fresh independent review | `7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "E_AI committed; fresh composite reviews pending; no downstream authority | Frozen historical "
    "implementation and test blob await exact composite review |"
)
e_revalidation = (
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | pending fresh independent "
    "review | pending fresh independent review | awaiting exact reviewed range | E_AI committed; fresh "
    "composite reviews pending; no downstream authority | Revalidation approval consumed; "
    f"result status={status} output={output_class}; E_AI resolved by its exact unique subject; no future OID "
    "is claimed in its own tree |"
)
lines = current_text.splitlines()
e_lines = e_text.splitlines()
state = "- 4AI transaction state: completed; approval consumed; no retry authority."
if e_lines.count(state) != 1 or lines.count(state) != 1:
    raise SystemExit("terminal-state-count")
current_results = [line for line in lines if line.startswith("- 4AI sanitized result: ")]
if len(current_results) != 1 or current_results[0] != result_candidates[0]:
    raise SystemExit("terminal-current-result-drift")

labels = (
    "T-TSDC-004R-4AI session-bound collision-safe Plan",
    "T-TSDC-004R-4AI frozen canonical-row implementation",
    "T-TSDC-004R-4AI session-bound collision-safe revalidation",
)
found = {label: [] for label in labels}
for source_line in lines:
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0:
        first_cell = view[:separator].strip(" \t")
        if first_cell in found:
            found[first_cell].append(line)
if any(len(found[label]) != 1 for label in labels):
    raise SystemExit("terminal-candidate-count")
rows = []
for label in labels:
    row = found[label][0]
    if not row.startswith("|") or not row.endswith("|"):
        raise SystemExit("terminal-row-shape")
    if "\\|" in row or "\\`" in row:
        raise SystemExit("terminal-row-escape")
    parts = row.split("|")
    if len(parts) != 9 or parts[0] or parts[-1]:
        raise SystemExit("terminal-row-cell-count")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if len(cells) != 7 or cells[0] != label:
        raise SystemExit("terminal-row-label")
    if cells[1] != "Controller":
        raise SystemExit("terminal-row-owner")
    if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
        raise SystemExit("terminal-row-extra-range")
    if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
        raise SystemExit("terminal-row-range-shape")
    rows.append(cells)
plan, frozen, revalidation = rows
expected_plan = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    f"`{sys.argv[3]}..{sys.argv[4]}`",
    "accepted; B_AI resolved by its exact unique subject",
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
]
if plan[2:7] != expected_plan:
    raise SystemExit("terminal-plan-row")
if frozen[4] != f"`{sys.argv[5]}..{sys.argv[6]}`":
    raise SystemExit("terminal-frozen-range")
if revalidation[4] != f"`{sys.argv[7]}..{sys.argv[8]}`":
    raise SystemExit("terminal-revalidation-range")
spec_re = r"C\d+/I\d+/M\d+; SPEC_COMPLIANCE (YES|NO); COMMIT_READY (YES|NO)"
quality_re = r"C\d+/I\d+/M\d+; QUALITY_SECURITY (PASS|FAIL); COMMIT_READY (YES|NO)"
for cells in (frozen, revalidation):
    if re.fullmatch(spec_re, cells[2], flags=re.ASCII) is None:
        raise SystemExit("terminal-spec-verdict")
    if re.fullmatch(quality_re, cells[3], flags=re.ASCII) is None:
        raise SystemExit("terminal-quality-verdict")
if frozen[2:4] != revalidation[2:4]:
    raise SystemExit("terminal-divergent-verdicts")
accepted_verdicts = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES",
]
reviews_accepted = frozen[2:4] == accepted_verdicts
outcome_accepted = status == 0 and output_class in {"empty", "nonempty"}
writer_selection = "R_AI" if reviews_accepted and outcome_accepted else "XE_AI"
if selection != writer_selection:
    raise SystemExit("terminal-selection-drift")
accepted = writer_selection == "R_AI"
if accepted:
    expected_frozen = [
        "accepted; frozen implementation approved in 4AI composite review",
        "Composite reviewers accepted exact frozen implementation and session-bound revalidation ranges; frozen test blob preserved",
    ]
    expected_revalidation = [
        "accepted; R_AI resolved by its exact unique subject",
        f"Revalidation result status={status} output={output_class} and both fresh composite reviews accepted; Task 4.5 authority granted",
    ]
else:
    expected_frozen = [
        "rejected/exhausted; frozen implementation not approved in 4AI composite review",
        "One or both fresh composite reviews rejected or sanitized revalidation outcome was non-accepting; frozen history grants no downstream authority",
    ]
    expected_revalidation = [
        "rejected/exhausted; XE_AI resolved by its exact unique subject",
        f"Revalidation result status={status} output={output_class} was non-accepting or one or both fresh composite reviews rejected; no correction, retry, or Wave C authority",
    ]
if frozen[5:7] != expected_frozen:
    raise SystemExit("terminal-frozen-outcome")
if revalidation[5:7] != expected_revalidation:
    raise SystemExit("terminal-revalidation-outcome")
terminal_frozen = found[labels[1]][0]
terminal_revalidation = found[labels[2]][0]

review_transitions = {
    e_frozen: terminal_frozen,
    e_revalidation: terminal_revalidation,
}
review_candidate = e_text
for old, new in review_transitions.items():
    if review_candidate.count(old) != 1 or old == new or new in review_candidate:
        raise SystemExit("terminal-review-transition-shape")
    review_candidate = review_candidate.replace(old, new, 1)
if current_text != review_candidate:
    raise SystemExit("terminal-prewrite-diff-scope")

e_parent_work_breakdown = (
    "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
    "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
    "agent; original agents remain historical | active; E_AI committed and resolved by its exact unique subject; "
    "fresh composite reviews pending; no downstream authority |"
)
e_work_breakdown = (
    "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit in one fail-fast "
    "session without changing frozen implementation | Plan/evidence | TSDC-010–014 | immutable E_AI evidence "
    "plus two future fresh composite reviews | controller and future fresh independent reviewers | E_AI committed "
    "and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority |"
)
e_task5_work_breakdown = (
    "| T-TSDC-005 | Reconcile canonical audit and remote observation evidence | evidence/docs | TSDC-015–016 | "
    "audit semantic, generators, links | fresh implementer after a separately approved future successor and "
    "Wave C completion | blocked; no accepted R_AI or Wave C authority exists |"
)
e_task6_work_breakdown = (
    "| T-TSDC-006 | Promote blocking enforcement and close reviews | closure/QA | TSDC-001–017 | "
    "final ladder and whole-branch reviews | fresh closure implementer after Tasks 1–5 | blocked; E_AI "
    "is committed but accepted R_AI, Wave C, and Task 5 completion are absent |"
)
e_work_log = (
    "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Pending two fresh independent reviews "
    "over immutable E_AI evidence; R_AI and XE_AI are not created. |"
)
e_verification = (
    "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly one "
    "R_AI/XE_AI terminal | Pending; E_AI committed; fresh composite reviews not yet recorded |"
)
e_task4_execution = (
    "| T-TSDC-004 | Historical 4AF RED evidence and rejected 4AG/4AH Plan history are preserved; 4AI "
    "changes only Plan/Task evidence design and adds no product RED. | Frozen product GREEN evidence "
    f"remains unchanged; the separately approved evidence-only wrapper returned status={status} "
    f"output={output_class}. | E_AI committed and resolved by its exact unique subject; fresh composite "
    "reviews pending; no downstream authority. | active Task 4; 4AI composite review pending; no Wave C authority |"
)
e_task5_execution = (
    "| T-TSDC-005 | Not run — no accepted R_AI or Wave C authority exists | Not run — no accepted R_AI "
    "or Wave C authority exists | E_AI committed; fresh composite reviews and accepted R_AI are pending | blocked |"
)
e_task6_execution = (
    "| T-TSDC-006 | Not run — accepted R_AI, Wave C, and Task 5 are absent | Not run — accepted R_AI, "
    "Wave C, and Task 5 are absent | E_AI committed; composite terminal not created | blocked |"
)
e_r_ledger = (
    "| T-TSDC-004R-4AI accepted review R_AI | Record accepted session-bound collision-safe review | "
    "`docs(task): record session-bound collision-safe review` | not created | Pending two accepted fresh composite "
    "reviews and accepting immutable E_AI result; mutually exclusive with XE_AI. |"
)
e_xe_ledger = (
    "| T-TSDC-004R-4AI rejected review XE_AI | Record exhausted session-bound collision-safe review | "
    "`docs(task): record exhausted session-bound collision-safe review` | not created | Pending composite "
    "disposition; mandatory for nonzero/internal E_AI evidence or either non-accepted fresh review; mutually "
    "exclusive with R_AI. |"
)
e_task6_review = (
    "| T-TSDC-006 | pending | pending | pending | not available | blocked | E_AI is committed; accepted "
    "R_AI, Wave C, and Task 5 completion remain absent. |"
)
e_whole_review = (
    "| Whole branch | not applicable | pending final fresh reviewer after accepted R_AI, Wave C, and Tasks "
    "5–6 | pending different final fresh reviewer after accepted R_AI, Wave C, and Tasks 5–6 | not available | "
    "blocked | E_AI and pending composite reviews grant no Wave C, Tasks 5–6, or final branch-review authority. |"
)
e_deferred = (
    "| T-TSDC-004R-3 atomic projection cutover | blocked; E_AI committed and composite reviews pending | "
    f"B_AI `{sys.argv[7]}` is accepted, XP_AI is not created, and E_AI records result status={status} "
    f"output={output_class}; R_AI/XE_AI are not created and no downstream authority exists. | complete two "
    "fresh composite reviews over immutable E_AI evidence and exactly one R_AI/XE_AI terminal; only accepted "
    "R_AI may unlock Wave C |"
)
e_handoff = (
    f"Current 4AI final handoff: E_AI committed in the approval-consuming session with result status={status} "
    f"output={output_class}; B_AI `{sys.argv[7]}` approved and XP_AI absent; fresh composite reviews pending; "
    "R_AI/XE_AI not created; no downstream authority."
)
e_boundary = (
    "- The active 4AI checkpoint has immutable E_AI evidence and pending fresh composite reviews. XP_AI,\n"
    "  R_AI, and XE_AI are uncreated; E_AI alone does not establish Task 4.5, Wave C, downstream, runtime,\n"
    "  or remote authority."
)
e_checkpoint = (
    "- D_AI remains the clean Task-only XP_AH terminal\n"
    "  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`; P_AI and accepted B_AI are immutable lineage\n"
    f"  evidence. The current checkpoint is Task-only E_AI with approved B_AI `{sys.argv[7]}`,\n"
    f"  canonical result status={status} output={output_class}, and pending fresh composite reviews."
)
e_lineage = (
    "- The realized evidence lineage is `B_4AF -> I -> D_AG -> P_AG -> D_AH -> P_AH ->\n"
    "  XP_AH/D_AI -> P_AI -> B_AI -> E_AI`; XP_AI is absent. E_AI alone grants no implementation,\n"
    "  Task 4.5, or Wave C authority; exactly one future R_AI/XE_AI composite terminal remains required."
)
e_execution_state = (
    "- The separately approved 4AI revalidation transaction ran once and committed only sanitized result "
    f"status={status} output={output_class} as E_AI. Fresh composite reviews, R_AI/XE_AI, Task 4.5, Wave C,\n"
    "  runtime, remote, Graphify, Tasks 5–6, and whole-branch review remain unexecuted and unauthorized."
)
e_final_block = (
    "T-TSDC-004R-4AI now has immutable Task-only E_AI evidence from one approval-consuming session.\n"
    f"B_AI `{sys.argv[7]}` is accepted and XP_AI is absent; the canonical sanitized result is\n"
    f"status={status} output={output_class}. Fresh composite reviews remain pending, so R_AI and XE_AI are\n"
    "not created and no Task 4.5, Wave C, Tasks 5–6, runtime, remote, Graphify, or whole-branch review\n"
    "authority exists."
)
if accepted:
    terminal_values = {
        e_parent_work_breakdown: e_parent_work_breakdown.replace(
            "E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority",
            "R_AI accepted and resolved by its exact unique subject; Task 4.5 authorized; Wave C not run",
        ),
        e_work_breakdown: e_work_breakdown.replace(
            "E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority",
            "R_AI accepted and resolved by its exact unique subject; Task 4.5 authorized; Wave C not run",
        ),
        e_task5_work_breakdown: e_task5_work_breakdown.replace(
            "blocked; no accepted R_AI or Wave C authority exists",
            "blocked; accepted R_AI authorizes Task 4.5 only; Task 4.5 and Wave C not run",
        ),
        e_task6_work_breakdown: e_task6_work_breakdown.replace(
            "blocked; E_AI is committed but accepted R_AI, Wave C, and Task 5 completion are absent",
            "blocked; accepted R_AI exists but Task 4.5, Wave C, and Task 5 completion are absent",
        ),
        e_work_log: (
            "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Completed; immutable "
            f"result status={status} output={output_class} and both fresh composite reviews accepted; R_AI "
            "resolved by its exact unique subject; Task 4.5 authorized and Wave C not run. |"
        ),
        e_verification: (
            "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly "
            "one R_AI/XE_AI terminal | Accepted; R_AI resolved by its exact unique subject; Task 4.5 authorized |"
        ),
        e_task4_execution: (
            "| T-TSDC-004 | Historical 4AF RED evidence and rejected 4AG/4AH Plan history are preserved; 4AI "
            "changes only Plan/Task evidence design and adds no product RED. | Frozen product GREEN evidence "
            f"remains unchanged; the separately approved evidence-only wrapper returned status={status} "
            f"output={output_class}. | R_AI accepted and resolved by its exact unique subject; Task 4.5 "
            "authorized; Wave C not run. | active Task 4; Task 4.5 authorized; Wave C not run |"
        ),
        e_task5_execution: (
            "| T-TSDC-005 | Not run — Task 4.5 and Wave C not run | Not run — Task 4.5 and Wave C not run | "
            "Accepted R_AI authorizes Task 4.5 only; Wave C not run | blocked |"
        ),
        e_task6_execution: (
            "| T-TSDC-006 | Not run — Task 4.5, Wave C, and Task 5 not run | Not run — Task 4.5, Wave C, "
            "and Task 5 not run | Accepted R_AI authorizes Task 4.5 only; no Task 5/6 authority | blocked |"
        ),
        e_r_ledger: (
            "| T-TSDC-004R-4AI accepted review R_AI | Record accepted session-bound collision-safe review | "
            "`docs(task): record session-bound collision-safe review` | resolved by this exact unique subject | "
            "Both fresh composite reviews accepted immutable accepting E_AI evidence; Task 4.5 authorized. |"
        ),
        e_xe_ledger: (
            "| T-TSDC-004R-4AI rejected review XE_AI | Record exhausted session-bound collision-safe review | "
            "`docs(task): record exhausted session-bound collision-safe review` | not created | Mutually excluded "
            "by accepted R_AI. |"
        ),
        e_task6_review: (
            "| T-TSDC-006 | pending | pending | pending | not available | blocked | Accepted R_AI authorizes "
            "Task 4.5 only; Wave C and Task 5 completion remain absent. |"
        ),
        e_whole_review: (
            "| Whole branch | not applicable | pending final fresh reviewer after accepted R_AI, Wave C, and "
            "Tasks 5–6 | pending different final fresh reviewer after accepted R_AI, Wave C, and Tasks 5–6 | "
            "not available | blocked | Accepted R_AI authorizes Task 4.5 only; Wave C, Tasks 5–6, and final "
            "branch review remain unexecuted and unauthorized. |"
        ),
        e_deferred: (
            "| T-TSDC-004R-3 atomic projection cutover | authorized for Task 4.5; Wave C not run | Immutable "
            f"E_AI result status={status} output={output_class} and both fresh composite reviews accepted; R_AI "
            "is the sole terminal and XE_AI is absent. | execute Task 4.5 only from this exact accepted R_AI "
            "chain; Wave C remains unexecuted |"
        ),
        e_handoff: (
            f"Current 4AI final handoff: accepted R_AI resolved by its exact unique subject; immutable E_AI "
            f"result status={status} output={output_class}; XP_AI/XE_AI absent; Task 4.5 authorized; Wave C not run."
        ),
        e_boundary: (
            "- Accepted R_AI is the sole 4AI terminal. It authorizes Task 4.5 only; Wave C, Tasks 5–6, runtime,\n"
            "  remote, Graphify, and whole-branch review remain unexecuted and separately governed."
        ),
        e_checkpoint: (
            "- D_AI remains the clean Task-only XP_AH terminal\n"
            "  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`; P_AI, B_AI, and E_AI are immutable lineage\n"
            f"  evidence. Accepted Task-only R_AI is the current checkpoint with canonical result status={status}\n"
            f"  output={output_class}; it authorizes Task 4.5 only, which has not run."
        ),
        e_lineage: (
            "- The realized accepted lineage is `B_4AF -> I -> D_AG -> P_AG -> D_AH -> P_AH ->\n"
            "  XP_AH/D_AI -> P_AI -> B_AI -> E_AI -> R_AI`; XP_AI and XE_AI are absent. R_AI authorizes\n"
            "  Task 4.5 only; Wave C and all later work remain unexecuted and separately governed."
        ),
        e_execution_state: (
            "- The separately approved 4AI revalidation transaction ran once and committed only sanitized result "
            f"status={status} output={output_class} as E_AI. Both fresh composite reviews then accepted that\n"
            "  immutable evidence and R_AI became the sole terminal. Task 4.5 is authorized but unexecuted; Wave C,\n"
            "  runtime, remote, Graphify, Tasks 5–6, and whole-branch review remain unexecuted and unauthorized."
        ),
        e_final_block: (
            "T-TSDC-004R-4AI completed at accepted Task-only R_AI. Immutable E_AI records\n"
            f"status={status} output={output_class}; B_AI and R_AI are the sole accepted terminals while XP_AI\n"
            "and XE_AI are absent. Task 4.5 is authorized, but Wave C, Tasks 5–6, runtime, remote, Graphify,\n"
            "and whole-branch review have not run."
        ),
    }
else:
    terminal_values = {
        e_parent_work_breakdown: e_parent_work_breakdown.replace(
            "active; E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority",
            "rejected/exhausted at XE_AI; no correction, Task 4.5, or Wave C authority",
        ),
        e_work_breakdown: e_work_breakdown.replace(
            "E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority",
            "rejected/exhausted; XE_AI resolved by its exact unique subject; no downstream authority",
        ),
        e_task5_work_breakdown: e_task5_work_breakdown.replace(
            "blocked; no accepted R_AI or Wave C authority exists",
            "blocked; rejected XE_AI grants no Task 4.5 or Wave C authority",
        ),
        e_task6_work_breakdown: e_task6_work_breakdown.replace(
            "blocked; E_AI is committed but accepted R_AI, Wave C, and Task 5 completion are absent",
            "blocked; rejected XE_AI is terminal and grants no Task 4.5, Wave C, or Task 5 authority",
        ),
        e_work_log: (
            "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Completed; immutable "
            f"result status={status} output={output_class} or one or both fresh reviews were non-accepting; "
            "XE_AI resolved by its exact unique subject; no correction, retry, Task 4.5, or Wave C authority. |"
        ),
        e_verification: (
            "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly "
            "one R_AI/XE_AI terminal | Rejected/exhausted; XE_AI resolved by its exact unique subject; no "
            "downstream authority |"
        ),
        e_task4_execution: (
            "| T-TSDC-004 | Historical 4AF RED evidence and rejected 4AG/4AH Plan history are preserved; 4AI "
            "changes only Plan/Task evidence design and adds no product RED. | Frozen product GREEN evidence "
            f"remains unchanged; the separately approved evidence-only wrapper returned status={status} "
            f"output={output_class}. | XE_AI rejected/exhausted and resolved by its exact unique subject; no "
            "downstream authority. | blocked Task 4; no correction, Task 4.5, or Wave C authority |"
        ),
        e_task5_execution: (
            "| T-TSDC-005 | Not run — rejected XE_AI grants no authority | Not run — rejected XE_AI grants no "
            "authority | XE_AI is terminal; Task 4.5 and Wave C are unauthorized | blocked |"
        ),
        e_task6_execution: (
            "| T-TSDC-006 | Not run — rejected XE_AI grants no authority | Not run — rejected XE_AI grants no "
            "authority | XE_AI is terminal; Tasks 5–6 and closure are unauthorized | blocked |"
        ),
        e_r_ledger: (
            "| T-TSDC-004R-4AI accepted review R_AI | Record accepted session-bound collision-safe review | "
            "`docs(task): record session-bound collision-safe review` | not created | Mutually excluded by "
            "rejected XE_AI. |"
        ),
        e_xe_ledger: (
            "| T-TSDC-004R-4AI rejected review XE_AI | Record exhausted session-bound collision-safe review | "
            "`docs(task): record exhausted session-bound collision-safe review` | resolved by this exact unique "
            "subject | Non-accepting immutable E_AI outcome or fresh composite review; terminal with no "
            "correction, retry, Task 4.5, or Wave C authority. |"
        ),
        e_task6_review: (
            "| T-TSDC-006 | pending | pending | pending | not available | blocked | Rejected XE_AI is terminal; "
            "Task 4.5, Wave C, and Task 5 remain unauthorized. |"
        ),
        e_whole_review: (
            "| Whole branch | not applicable | pending final fresh reviewer after accepted R_AI, Wave C, and "
            "Tasks 5–6 | pending different final fresh reviewer after accepted R_AI, Wave C, and Tasks 5–6 | "
            "not available | blocked | Rejected XE_AI grants no Task 4.5, Wave C, Tasks 5–6, or final "
            "branch-review authority. |"
        ),
        e_deferred: (
            "| T-TSDC-004R-3 atomic projection cutover | rejected/exhausted at XE_AI | Immutable E_AI result "
            f"status={status} output={output_class} or a fresh composite review was non-accepting; XE_AI is the "
            "sole terminal and R_AI is absent. | return to a newly approved design; no correction, retry, Task "
            "4.5, or Wave C authority |"
        ),
        e_handoff: (
            f"Current 4AI final handoff: rejected/exhausted at XE_AI resolved by its exact unique subject; "
            f"immutable E_AI result status={status} output={output_class}; XP_AI/R_AI absent; no downstream authority."
        ),
        e_boundary: (
            "- Rejected XE_AI is the sole 4AI composite terminal. R_AI is absent and no correction, retry,\n"
            "  Task 4.5, Wave C, downstream, runtime, remote, Graphify, or whole-branch authority exists."
        ),
        e_checkpoint: (
            "- D_AI remains the clean Task-only XP_AH terminal\n"
            "  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`; P_AI, B_AI, and E_AI are immutable lineage\n"
            f"  evidence. Rejected Task-only XE_AI is the current checkpoint with immutable result status={status}\n"
            f"  output={output_class}; it grants no correction or downstream authority."
        ),
        e_lineage: (
            "- The realized rejected lineage is `B_4AF -> I -> D_AG -> P_AG -> D_AH -> P_AH ->\n"
            "  XP_AH/D_AI -> P_AI -> B_AI -> E_AI -> XE_AI`; XP_AI and R_AI are absent. XE_AI is terminal\n"
            "  and grants no correction, Task 4.5, Wave C, or later-work authority."
        ),
        e_execution_state: (
            "- The separately approved 4AI revalidation transaction ran once and committed only sanitized result "
            f"status={status} output={output_class} as E_AI. The immutable result or a fresh composite review was\n"
            "  non-accepting, so XE_AI became the sole terminal. Task 4.5, Wave C, runtime, remote, Graphify,\n"
            "  Tasks 5–6, and whole-branch review remain unexecuted and unauthorized."
        ),
        e_final_block: (
            "T-TSDC-004R-4AI is rejected/exhausted at Task-only XE_AI. Immutable E_AI records\n"
            f"status={status} output={output_class}; B_AI and XE_AI exist while XP_AI and R_AI are absent. No\n"
            "correction, retry, Task 4.5, Wave C, Tasks 5–6, runtime, remote, Graphify, or whole-branch review\n"
            "authority exists."
        ),
    }

transitions = dict(review_transitions)
transitions.update(terminal_values)
candidate = e_text
for old, new in transitions.items():
    if candidate.count(old) != 1 or old == new or new in candidate:
        raise SystemExit("terminal-transition-shape")
for old, new in transitions.items():
    candidate = candidate.replace(old, new, 1)
normalized = candidate
for old, new in reversed(tuple(transitions.items())):
    if normalized.count(new) != 1:
        raise SystemExit("terminal-reverse-count")
    normalized = normalized.replace(new, old, 1)
if normalized != e_text:
    raise SystemExit("terminal-reverse-equality")
residue = tuple(path.parent.glob(f".{path.name}.*"))
if residue:
    raise SystemExit("terminal-temp-residue")
source_mode = stat.S_IMODE(path.stat().st_mode)
temporary = None
try:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = pathlib.Path(stream.name)
        stream.write(candidate)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, source_mode)
    os.replace(temporary, path)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_fd = os.open(path.parent, directory_flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    temporary = None
finally:
    # Preserve any crash residue as a fail-closed rerun blocker.
    pass
PY
validated_terminal_blob="$(git hash-object "$task_file")"
[[ "$validated_terminal_blob" =~ ^[0-9a-f]{40}$ ]]
subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record exhausted status-based silent-success plan review'
  'docs(plan): define collision-safe disposition proof'
  'docs(task): record exhausted collision-safe disposition plan review'
  "$p_subject"
  "$b_subject"
  "$e_subject"
)
commits=("$b_4af" "$i" "$d_ag" "$p_ag" "$d_ah" "$p_ah" "$d_ai" "$p_ai" "$b_ai" "$e_ai")
for index in "${!commits[@]}"; do
  verified="$(git rev-parse --verify "${commits[$index]}^{commit}")"
  test "$verified" = "${commits[$index]}"
  actual_subject="$(git show -s --format=%s "${commits[$index]}")"
  test "$actual_subject" = "${subjects[$index]}"
  subject_count="$(git log --all --format='%s' | grep -Fxc "${subjects[$index]}")"
  test "$subject_count" -eq 1
done
assert_edge "$b_4af" "$i"
assert_edge "$i" "$d_ag"
assert_edge "$d_ag" "$p_ag"
assert_edge "$p_ag" "$d_ah"
assert_edge "$d_ah" "$p_ah"
assert_edge "$p_ah" "$d_ai"
assert_edge "$d_ai" "$p_ai"
assert_edge "$p_ai" "$b_ai"
assert_edge "$b_ai" "$e_ai"
unstaged_paths="$(git diff --name-only)"
test "$?" -eq 0
staged_paths="$(git diff --cached --name-only)"
test "$?" -eq 0
untracked_paths="$(git ls-files --others --exclude-standard)"
test "$?" -eq 0
dirty_paths="$(printf '%s\n' "$unstaged_paths" "$staged_paths" "$untracked_paths" | sed '/^$/d' | sort -u)"
test "$dirty_paths" = "$task_file"
git diff --check
git add "$task_file"
cached_paths="$(git diff --cached --name-only | sort)"
test "$cached_paths" = "$task_file"
staged_terminal_blob="$(git rev-parse ":$task_file")"
test "$staged_terminal_blob" = "$validated_terminal_blob"
git commit -m "$terminal_subject"
terminal="$(git rev-parse --verify 'HEAD^{commit}')"
actual_subject="$(git show -s --format=%s "$terminal")"
test "$actual_subject" = "$terminal_subject"
subject_count="$(git log --all --format='%s' | grep -Fxc "$terminal_subject")"
test "$subject_count" -eq 1
opposite_count="$(git log --all --format='%s' | awk -v subject="$opposite_subject" '$0 == subject {count++} END {print count + 0}')"
test "$opposite_count" -eq 0
committed_terminal_blob="$(git rev-parse "$terminal:$task_file")"
test "$committed_terminal_blob" = "$validated_terminal_blob"
assert_edge "$e_ai" "$terminal"
expected_plan_paths="$(printf '%s\n' "$plan_file" "$task_file" | sort)"
expected_test_paths="$(printf '%s\n' "$task_file" "$test_file" | sort)"
expected_paths=(
  "$task_file"
  "$expected_test_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$task_file"
  "$task_file"
)
commits+=("$terminal")
for index in "${!commits[@]}"; do
  commit_paths="$(git diff-tree --no-commit-id --name-only -r "${commits[$index]}" | sort)"
  test "$commit_paths" = "${expected_paths[$index]}"
done
plan_range_paths="$(git diff --name-only "$d_ai..$p_ai" | sort)"
test "$plan_range_paths" = "$expected_plan_paths"
frozen_range_paths="$(git diff --name-only "$b_4af..$i" | sort)"
test "$frozen_range_paths" = "$expected_test_paths"
evidence_range_paths="$(git diff --name-only "$b_ai..$e_ai" | sort)"
test "$evidence_range_paths" = "$task_file"
terminal_range_paths="$(git diff --name-only "$e_ai..$terminal" | sort)"
test "$terminal_range_paths" = "$task_file"
for commit_path in \
  "$b_4af:$task_file" \
  "$i:$task_file" "$i:$test_file" \
  "$d_ag:$task_file" \
  "$p_ag:$plan_file" "$p_ag:$task_file" \
  "$d_ah:$task_file" \
  "$p_ah:$plan_file" "$p_ah:$task_file" \
  "$d_ai:$task_file" \
  "$p_ai:$plan_file" "$p_ai:$task_file" \
  "$b_ai:$task_file" "$e_ai:$task_file" "$terminal:$task_file"
do
  mode="$(git ls-tree "${commit_path%%:*}" "${commit_path#*:}" | awk '{print $1}')"
  test "$mode" = 100644
done
implementation_blob="$(git rev-parse "$i:$test_file")"
test -n "$implementation_blob"
terminal_blob="$(git rev-parse "$terminal:$test_file")"
test "$terminal_blob" = "$implementation_blob"
head_after="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_after" = "$terminal"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

Historical non-executable evidence only: XE_AI is terminal; R_AI was never
created and grants no current Task 4.5 or Wave C authority.

#### Historical non-executable Task 4.5 / Wave C / T-TSDC-004R-5 procedure: Remove the Old Semantic Interpreter

- [ ] **Step 0: Prove the complete accepted 4AI chain.**

  Before any Wave C change, this prerequisite requires the exact accepted
  review, range, disposition, sanitized result, and evidence values on all
  three 4AI rows. It also requires unique R_AI at clean HEAD, every
  sole-parent distance-one edge from the frozen historical lineage, exact
  commit and range paths, mode `100644`, and the frozen test blob.

```bash
set -euo pipefail
shopt -s inherit_errexit
plan_file='docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md'
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
b_4af=7e32c37cafde08b108ee33e3439cda3aea336961
i=a7d05b0e5c0ffaeccde9e401450e696855cfb2b5
d_ag=737838fe80880b7eadbfb1c7e18d8dc251bcc8b9
p_ag=f2a4b5041222c48f392bc251eae014655cee7b7c
d_ah=e9100b62f6ea18e2a003cfa805b14a7ad61a64ad
p_ah=9ff217e63eaf452871cfc3ef47775e0fbd03e706
d_ai=88f55837be251318cd697bd8a1ab3a4f0ed1a824
p_subject='docs(plan): define session-bound collision-safe proof'
b_subject='docs(task): record session-bound collision-safe plan reviews'
xp_subject='docs(task): record exhausted session-bound collision-safe plan review'
e_subject='docs(task): record session-bound collision-safe revalidation'
r_subject='docs(task): record session-bound collision-safe review'
xe_subject='docs(task): record exhausted session-bound collision-safe review'
resolve_unique_subject() {
  local subject="$1"
  local count
  local oid
  count="$(git log --all --format='%s' | grep -Fxc "$subject")"
  test "$count" -eq 1
  oid="$(git log --all --format='%H%x09%s' | awk -F '\t' -v s="$subject" '$2 == s {print $1}')"
  test -n "$oid"
  printf '%s\n' "$oid"
}
edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(git rev-list --count "$parent..$child")"
  test "$distance" -eq 1
  parent_count="$(git rev-list --parents -n 1 "$child" | awk '{print NF - 1}')"
  test "$parent_count" -eq 1
  first_parent="$(git rev-parse "$child^1")"
  test "$first_parent" = "$parent"
}
p_ai="$(resolve_unique_subject "$p_subject")"
b_ai="$(resolve_unique_subject "$b_subject")"
e_ai="$(resolve_unique_subject "$e_subject")"
r_ai="$(resolve_unique_subject "$r_subject")"
xp_count="$(git log --all --format='%s' | awk -v subject="$xp_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xp_count" -eq 0
xe_count="$(git log --all --format='%s' | awk -v subject="$xe_subject" '$0 == subject {count++} END {print count + 0}')"
test "$xe_count" -eq 0
head_commit="$(git rev-parse --verify 'HEAD^{commit}')"
test "$head_commit" = "$r_ai"
e_task_status=0
e_task_text="$(git show "$e_ai:$task_file")" || e_task_status=$?
test "$e_task_status" -eq 0
test -n "$e_task_text"
unstaged_paths="$(git diff --name-only)"
test "$?" -eq 0
test -z "$unstaged_paths"
staged_paths="$(git diff --cached --name-only)"
test "$?" -eq 0
test -z "$staged_paths"
untracked_paths="$(git ls-files --others --exclude-standard)"
test "$?" -eq 0
test -z "$untracked_paths"
python3 - \
  "$task_file" "$d_ai" "$p_ai" "$b_4af" "$i" "$b_ai" "$e_ai" \
  3<<<"$e_task_text" <<'PY'
import os
import pathlib
import re
import sys

labels = (
    "T-TSDC-004R-4AI session-bound collision-safe Plan",
    "T-TSDC-004R-4AI frozen canonical-row implementation",
    "T-TSDC-004R-4AI session-bound collision-safe revalidation",
)
e_text = os.fdopen(3, encoding="utf-8").read()
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
e_lines = e_text.splitlines()
lines = text.splitlines()
state = "- 4AI transaction state: completed; approval consumed; no retry authority."
if e_lines.count(state) != 1 or lines.count(state) != 1:
    raise SystemExit("authority-e-state")
e_results = [line for line in e_lines if line.startswith("- 4AI sanitized result: ")]
if len(e_results) != 1 or lines.count(e_results[0]) != 1:
    raise SystemExit("authority-e-result-count")
e_match = re.fullmatch(
    r"- 4AI sanitized result: result status=0 output=(empty|nonempty)\.",
    e_results[0],
    flags=re.ASCII,
)
if e_match is None:
    raise SystemExit("authority-e-result")
e_output_class = e_match.group(1)
approval_lines = (
    "- 4AI revalidation approval owner/source: User / Controller; exact one-attempt AI-3 approval consumed.",
    f"- 4AI `APPROVED_B_AI_OID`: `{sys.argv[6]}`; validated against the unique accepted B_AI subject.",
    (
        "| T-TSDC-004R-4AI revalidation E_AI | Record session-bound collision-safe revalidation | "
        "`docs(task): record session-bound collision-safe revalidation` | resolved by this exact unique subject | "
        f"Approval naming B_AI `{sys.argv[6]}` consumed; result status=0 output={e_output_class}; "
        "Task-only E_AI committed in the same fail-fast session. |"
    ),
)
for approval_line in approval_lines:
    if e_lines.count(approval_line) != 1 or lines.count(approval_line) != 1:
        raise SystemExit("authority-e-approval")
found = {label: [] for label in labels}
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    view = line[1:] if line.startswith("|") else line
    separator = view.find("|")
    if separator >= 0:
        first_cell = view[:separator].strip(" \t")
        if first_cell in found:
            found[first_cell].append(line)
if any(len(found[label]) != 1 for label in labels):
    raise SystemExit("authority-candidate-count")
rows = []
for label in labels:
    row = found[label][0]
    if not row.startswith("|") or not row.endswith("|"):
        raise SystemExit("authority-shape")
    if "\\|" in row or "\\`" in row:
        raise SystemExit("authority-escape")
    parts = row.split("|")
    if len(parts) != 9 or parts[0] or parts[-1]:
        raise SystemExit("authority-cell-count")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if len(cells) != 7 or cells[0] != label:
        raise SystemExit("authority-label")
    if cells[1] != "Controller":
        raise SystemExit("authority-owner")
    if any(("`" in cell or ".." in cell) for index, cell in enumerate(cells) if index != 4):
        raise SystemExit("authority-extra-range")
    if re.fullmatch(r"`[0-9a-f]{40}\.\.[0-9a-f]{40}`", cells[4], flags=re.ASCII) is None:
        raise SystemExit("authority-range-shape")
    rows.append(cells)
plan, frozen, revalidation = rows
expected_plan = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    f"`{sys.argv[2]}..{sys.argv[3]}`",
    "accepted; B_AI resolved by its exact unique subject",
    "Both fresh Plan reviews accepted; separate revalidation approval still required; no Wave C authority",
]
expected_frozen = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES",
    f"`{sys.argv[4]}..{sys.argv[5]}`",
    "accepted; frozen implementation approved in 4AI composite review",
    "Composite reviewers accepted exact frozen implementation and session-bound revalidation ranges; frozen test blob preserved",
]
output_class = e_output_class
expected_revalidation = [
    "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES",
    "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES",
    f"`{sys.argv[6]}..{sys.argv[7]}`",
    "accepted; R_AI resolved by its exact unique subject",
    f"Revalidation result status=0 output={output_class} and both fresh composite reviews accepted; Task 4.5 authority granted",
]
if plan[2:7] != expected_plan:
    raise SystemExit("authority-plan")
if frozen[2:7] != expected_frozen:
    raise SystemExit("authority-frozen")
if revalidation[2:7] != expected_revalidation:
    raise SystemExit("authority-revalidation")

status = 0
e_frozen = (
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | pending fresh independent review | "
    "pending fresh independent review | `7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "E_AI committed; fresh composite reviews pending; no downstream authority | Frozen historical "
    "implementation and test blob await exact composite review |"
)
r_frozen = (
    "| T-TSDC-004R-4AI frozen canonical-row implementation | Controller | "
    "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | "
    "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES | "
    "`7e32c37cafde08b108ee33e3439cda3aea336961..a7d05b0e5c0ffaeccde9e401450e696855cfb2b5` | "
    "accepted; frozen implementation approved in 4AI composite review | Composite reviewers accepted exact "
    "frozen implementation and session-bound revalidation ranges; frozen test blob preserved |"
)
e_revalidation = (
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | pending fresh independent "
    "review | pending fresh independent review | awaiting exact reviewed range | E_AI committed; fresh "
    "composite reviews pending; no downstream authority | Revalidation approval consumed; "
    f"result status={status} output={output_class}; E_AI resolved by its exact unique subject; no future OID "
    "is claimed in its own tree |"
)
r_revalidation = (
    "| T-TSDC-004R-4AI session-bound collision-safe revalidation | Controller | "
    "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | "
    "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES | "
    f"`{sys.argv[6]}..{sys.argv[7]}` | accepted; R_AI resolved by its exact unique subject | "
    f"Revalidation result status={status} output={output_class} and both fresh composite reviews accepted; "
    "Task 4.5 authority granted |"
)
e_parent_work_breakdown = (
    "| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | "
    "gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation "
    "agent; original agents remain historical | active; E_AI committed and resolved by its exact unique subject; "
    "fresh composite reviews pending; no downstream authority |"
)
e_work_breakdown = (
    "| T-TSDC-004R-4AI | Bind wrapper execution, sanitized evidence mutation, and E_AI commit in one fail-fast "
    "session without changing frozen implementation | Plan/evidence | TSDC-010–014 | immutable E_AI evidence "
    "plus two future fresh composite reviews | controller and future fresh independent reviewers | E_AI committed "
    "and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority |"
)
e_task5_work_breakdown = (
    "| T-TSDC-005 | Reconcile canonical audit and remote observation evidence | evidence/docs | TSDC-015–016 | "
    "audit semantic, generators, links | fresh implementer after a separately approved future successor and "
    "Wave C completion | blocked; no accepted R_AI or Wave C authority exists |"
)
e_task6_work_breakdown = (
    "| T-TSDC-006 | Promote blocking enforcement and close reviews | closure/QA | TSDC-001–017 | "
    "final ladder and whole-branch reviews | fresh closure implementer after Tasks 1–5 | blocked; E_AI "
    "is committed but accepted R_AI, Wave C, and Task 5 completion are absent |"
)
e_work_log = (
    "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Pending two fresh independent reviews "
    "over immutable E_AI evidence; R_AI and XE_AI are not created. |"
)
e_verification = (
    "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly one "
    "R_AI/XE_AI terminal | Pending; E_AI committed; fresh composite reviews not yet recorded |"
)
e_task4_execution = (
    "| T-TSDC-004 | Historical 4AF RED evidence and rejected 4AG/4AH Plan history are preserved; 4AI "
    "changes only Plan/Task evidence design and adds no product RED. | Frozen product GREEN evidence "
    f"remains unchanged; the separately approved evidence-only wrapper returned status={status} "
    f"output={output_class}. | E_AI committed and resolved by its exact unique subject; fresh composite "
    "reviews pending; no downstream authority. | active Task 4; 4AI composite review pending; no Wave C authority |"
)
e_task5_execution = (
    "| T-TSDC-005 | Not run — no accepted R_AI or Wave C authority exists | Not run — no accepted R_AI "
    "or Wave C authority exists | E_AI committed; fresh composite reviews and accepted R_AI are pending | blocked |"
)
e_task6_execution = (
    "| T-TSDC-006 | Not run — accepted R_AI, Wave C, and Task 5 are absent | Not run — accepted R_AI, "
    "Wave C, and Task 5 are absent | E_AI committed; composite terminal not created | blocked |"
)
e_r_ledger = (
    "| T-TSDC-004R-4AI accepted review R_AI | Record accepted session-bound collision-safe review | "
    "`docs(task): record session-bound collision-safe review` | not created | Pending two accepted fresh composite "
    "reviews and accepting immutable E_AI result; mutually exclusive with XE_AI. |"
)
e_xe_ledger = (
    "| T-TSDC-004R-4AI rejected review XE_AI | Record exhausted session-bound collision-safe review | "
    "`docs(task): record exhausted session-bound collision-safe review` | not created | Pending composite "
    "disposition; mandatory for nonzero/internal E_AI evidence or either non-accepted fresh review; mutually "
    "exclusive with R_AI. |"
)
e_task6_review = (
    "| T-TSDC-006 | pending | pending | pending | not available | blocked | E_AI is committed; accepted "
    "R_AI, Wave C, and Task 5 completion remain absent. |"
)
e_whole_review = (
    "| Whole branch | not applicable | pending final fresh reviewer after accepted R_AI, Wave C, and Tasks "
    "5–6 | pending different final fresh reviewer after accepted R_AI, Wave C, and Tasks 5–6 | not available | "
    "blocked | E_AI and pending composite reviews grant no Wave C, Tasks 5–6, or final branch-review authority. |"
)
e_deferred = (
    "| T-TSDC-004R-3 atomic projection cutover | blocked; E_AI committed and composite reviews pending | "
    f"B_AI `{sys.argv[6]}` is accepted, XP_AI is not created, and E_AI records result status={status} "
    f"output={output_class}; R_AI/XE_AI are not created and no downstream authority exists. | complete two "
    "fresh composite reviews over immutable E_AI evidence and exactly one R_AI/XE_AI terminal; only accepted "
    "R_AI may unlock Wave C |"
)
e_handoff = (
    f"Current 4AI final handoff: E_AI committed in the approval-consuming session with result status={status} "
    f"output={output_class}; B_AI `{sys.argv[6]}` approved and XP_AI absent; fresh composite reviews pending; "
    "R_AI/XE_AI not created; no downstream authority."
)
e_boundary = (
    "- The active 4AI checkpoint has immutable E_AI evidence and pending fresh composite reviews. XP_AI,\n"
    "  R_AI, and XE_AI are uncreated; E_AI alone does not establish Task 4.5, Wave C, downstream, runtime,\n"
    "  or remote authority."
)
e_checkpoint = (
    "- D_AI remains the clean Task-only XP_AH terminal\n"
    "  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`; P_AI and accepted B_AI are immutable lineage\n"
    f"  evidence. The current checkpoint is Task-only E_AI with approved B_AI `{sys.argv[6]}`,\n"
    f"  canonical result status={status} output={output_class}, and pending fresh composite reviews."
)
e_lineage = (
    "- The realized evidence lineage is `B_4AF -> I -> D_AG -> P_AG -> D_AH -> P_AH ->\n"
    "  XP_AH/D_AI -> P_AI -> B_AI -> E_AI`; XP_AI is absent. E_AI alone grants no implementation,\n"
    "  Task 4.5, or Wave C authority; exactly one future R_AI/XE_AI composite terminal remains required."
)
e_execution_state = (
    "- The separately approved 4AI revalidation transaction ran once and committed only sanitized result "
    f"status={status} output={output_class} as E_AI. Fresh composite reviews, R_AI/XE_AI, Task 4.5, Wave C,\n"
    "  runtime, remote, Graphify, Tasks 5–6, and whole-branch review remain unexecuted and unauthorized."
)
e_final_block = (
    "T-TSDC-004R-4AI now has immutable Task-only E_AI evidence from one approval-consuming session.\n"
    f"B_AI `{sys.argv[6]}` is accepted and XP_AI is absent; the canonical sanitized result is\n"
    f"status={status} output={output_class}. Fresh composite reviews remain pending, so R_AI and XE_AI are\n"
    "not created and no Task 4.5, Wave C, Tasks 5–6, runtime, remote, Graphify, or whole-branch review\n"
    "authority exists."
)
accepted_to_e = {
    r_frozen: e_frozen,
    r_revalidation: e_revalidation,
    e_parent_work_breakdown.replace(
        "E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority",
        "R_AI accepted and resolved by its exact unique subject; Task 4.5 authorized; Wave C not run",
    ): e_parent_work_breakdown,
    e_work_breakdown.replace(
        "E_AI committed and resolved by its exact unique subject; fresh composite reviews pending; no downstream authority",
        "R_AI accepted and resolved by its exact unique subject; Task 4.5 authorized; Wave C not run",
    ): e_work_breakdown,
    e_task5_work_breakdown.replace(
        "blocked; no accepted R_AI or Wave C authority exists",
        "blocked; accepted R_AI authorizes Task 4.5 only; Task 4.5 and Wave C not run",
    ): e_task5_work_breakdown,
    e_task6_work_breakdown.replace(
        "blocked; E_AI is committed but accepted R_AI, Wave C, and Task 5 completion are absent",
        "blocked; accepted R_AI exists but Task 4.5, Wave C, and Task 5 completion are absent",
    ): e_task6_work_breakdown,
    (
        "| 2026-08-01 | T-TSDC-004R-4AI composite terminal | Controller | Completed; immutable "
        f"result status={status} output={output_class} and both fresh composite reviews accepted; R_AI "
        "resolved by its exact unique subject; Task 4.5 authorized and Wave C not run. |"
    ): e_work_log,
    (
        "| 4AI composite terminal | Immutable E_AI evidence plus two fresh composite reviews select exactly "
        "one R_AI/XE_AI terminal | Accepted; R_AI resolved by its exact unique subject; Task 4.5 authorized |"
    ): e_verification,
    (
        "| T-TSDC-004 | Historical 4AF RED evidence and rejected 4AG/4AH Plan history are preserved; 4AI "
        "changes only Plan/Task evidence design and adds no product RED. | Frozen product GREEN evidence "
        f"remains unchanged; the separately approved evidence-only wrapper returned status={status} "
        f"output={output_class}. | R_AI accepted and resolved by its exact unique subject; Task 4.5 "
        "authorized; Wave C not run. | active Task 4; Task 4.5 authorized; Wave C not run |"
    ): e_task4_execution,
    (
        "| T-TSDC-005 | Not run — Task 4.5 and Wave C not run | Not run — Task 4.5 and Wave C not run | "
        "Accepted R_AI authorizes Task 4.5 only; Wave C not run | blocked |"
    ): e_task5_execution,
    (
        "| T-TSDC-006 | Not run — Task 4.5, Wave C, and Task 5 not run | Not run — Task 4.5, Wave C, "
        "and Task 5 not run | Accepted R_AI authorizes Task 4.5 only; no Task 5/6 authority | blocked |"
    ): e_task6_execution,
    (
        "| T-TSDC-004R-4AI accepted review R_AI | Record accepted session-bound collision-safe review | "
        "`docs(task): record session-bound collision-safe review` | resolved by this exact unique subject | "
        "Both fresh composite reviews accepted immutable accepting E_AI evidence; Task 4.5 authorized. |"
    ): e_r_ledger,
    (
        "| T-TSDC-004R-4AI rejected review XE_AI | Record exhausted session-bound collision-safe review | "
        "`docs(task): record exhausted session-bound collision-safe review` | not created | Mutually excluded "
        "by accepted R_AI. |"
    ): e_xe_ledger,
    (
        "| T-TSDC-006 | pending | pending | pending | not available | blocked | Accepted R_AI authorizes "
        "Task 4.5 only; Wave C and Task 5 completion remain absent. |"
    ): e_task6_review,
    (
        "| Whole branch | not applicable | pending final fresh reviewer after accepted R_AI, Wave C, and "
        "Tasks 5–6 | pending different final fresh reviewer after accepted R_AI, Wave C, and Tasks 5–6 | "
        "not available | blocked | Accepted R_AI authorizes Task 4.5 only; Wave C, Tasks 5–6, and final "
        "branch review remain unexecuted and unauthorized. |"
    ): e_whole_review,
    (
        "| T-TSDC-004R-3 atomic projection cutover | authorized for Task 4.5; Wave C not run | Immutable "
        f"E_AI result status={status} output={output_class} and both fresh composite reviews accepted; R_AI "
        "is the sole terminal and XE_AI is absent. | execute Task 4.5 only from this exact accepted R_AI "
        "chain; Wave C remains unexecuted |"
    ): e_deferred,
    (
        f"Current 4AI final handoff: accepted R_AI resolved by its exact unique subject; immutable E_AI "
        f"result status={status} output={output_class}; XP_AI/XE_AI absent; Task 4.5 authorized; Wave C not run."
    ): e_handoff,
    (
        "- Accepted R_AI is the sole 4AI terminal. It authorizes Task 4.5 only; Wave C, Tasks 5–6, runtime,\n"
        "  remote, Graphify, and whole-branch review remain unexecuted and separately governed."
    ): e_boundary,
    (
        "- D_AI remains the clean Task-only XP_AH terminal\n"
        "  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`; P_AI, B_AI, and E_AI are immutable lineage\n"
        f"  evidence. Accepted Task-only R_AI is the current checkpoint with canonical result status={status}\n"
        f"  output={output_class}; it authorizes Task 4.5 only, which has not run."
    ): e_checkpoint,
    (
        "- The realized accepted lineage is `B_4AF -> I -> D_AG -> P_AG -> D_AH -> P_AH ->\n"
        "  XP_AH/D_AI -> P_AI -> B_AI -> E_AI -> R_AI`; XP_AI and XE_AI are absent. R_AI authorizes\n"
        "  Task 4.5 only; Wave C and all later work remain unexecuted and separately governed."
    ): e_lineage,
    (
        "- The separately approved 4AI revalidation transaction ran once and committed only sanitized result "
        f"status={status} output={output_class} as E_AI. Both fresh composite reviews then accepted that\n"
        "  immutable evidence and R_AI became the sole terminal. Task 4.5 is authorized but unexecuted; Wave C,\n"
        "  runtime, remote, Graphify, Tasks 5–6, and whole-branch review remain unexecuted and unauthorized."
    ): e_execution_state,
    (
        "T-TSDC-004R-4AI completed at accepted Task-only R_AI. Immutable E_AI records\n"
        f"status={status} output={output_class}; B_AI and R_AI are the sole accepted terminals while XP_AI\n"
        "and XE_AI are absent. Task 4.5 is authorized, but Wave C, Tasks 5–6, runtime, remote, Graphify,\n"
        "and whole-branch review have not run."
    ): e_final_block,
}
if len(accepted_to_e) != 22:
    raise SystemExit("authority-allowlist-size")
normalized = text
for accepted_value, e_value in accepted_to_e.items():
    if accepted_value == e_value or normalized.count(accepted_value) != 1:
        raise SystemExit("authority-allowlist-shape")
    normalized = normalized.replace(accepted_value, e_value, 1)
if normalized != e_text:
    raise SystemExit("authority-full-e-normalization")
PY
subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record exhausted status-based silent-success plan review'
  'docs(plan): define collision-safe disposition proof'
  'docs(task): record exhausted collision-safe disposition plan review'
  "$p_subject"
  "$b_subject"
  "$e_subject"
  "$r_subject"
)
commits=("$b_4af" "$i" "$d_ag" "$p_ag" "$d_ah" "$p_ah" "$d_ai" "$p_ai" "$b_ai" "$e_ai" "$r_ai")
for index in "${!commits[@]}"; do
  verified="$(git rev-parse --verify "${commits[$index]}^{commit}")"
  test "$verified" = "${commits[$index]}"
  actual="$(git show -s --format=%s "${commits[$index]}")"
  test "$actual" = "${subjects[$index]}"
  count="$(git log --all --format='%s' | grep -Fxc "${subjects[$index]}")"
  test "$count" -eq 1
done
edge "$b_4af" "$i"
edge "$i" "$d_ag"
edge "$d_ag" "$p_ag"
edge "$p_ag" "$d_ah"
edge "$d_ah" "$p_ah"
edge "$p_ah" "$d_ai"
edge "$d_ai" "$p_ai"
edge "$p_ai" "$b_ai"
edge "$b_ai" "$e_ai"
edge "$e_ai" "$r_ai"
expected_plan_paths="$(printf '%s\n' "$plan_file" "$task_file" | sort)"
expected_test_paths="$(printf '%s\n' "$task_file" "$test_file" | sort)"
expected_paths=(
  "$task_file"
  "$expected_test_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$expected_plan_paths"
  "$task_file"
  "$task_file"
  "$task_file"
)
for index in "${!commits[@]}"; do
  paths="$(git diff-tree --no-commit-id --name-only -r "${commits[$index]}" | sort)"
  test "$paths" = "${expected_paths[$index]}"
done
historical_range_paths="$(git diff --name-only "$b_4af..$i" | sort)"
test "$historical_range_paths" = "$expected_test_paths"
plan_range_paths="$(git diff --name-only "$d_ai..$p_ai" | sort)"
test "$plan_range_paths" = "$expected_plan_paths"
evidence_range_paths="$(git diff --name-only "$b_ai..$e_ai" | sort)"
test "$evidence_range_paths" = "$task_file"
terminal_range_paths="$(git diff --name-only "$e_ai..$r_ai" | sort)"
test "$terminal_range_paths" = "$task_file"
for commit_path in \
  "$b_4af:$task_file" \
  "$i:$task_file" "$i:$test_file" \
  "$d_ag:$task_file" \
  "$p_ag:$plan_file" "$p_ag:$task_file" \
  "$d_ah:$task_file" \
  "$p_ah:$plan_file" "$p_ah:$task_file" \
  "$d_ai:$task_file" \
  "$p_ai:$plan_file" "$p_ai:$task_file" \
  "$b_ai:$task_file" "$e_ai:$task_file" "$r_ai:$task_file"
do
  mode="$(git ls-tree "${commit_path%%:*}" "${commit_path#*:}" | awk '{print $1}')"
  test "$mode" = 100644
done
historical_blob="$(git rev-parse "$i:$test_file")"
test -n "$historical_blob"
r_blob="$(git rev-parse "$r_ai:$test_file")"
test "$r_blob" = "$historical_blob"
clean_state="$(git status --porcelain=v1 --untracked-files=all)"
test -z "$clean_state"
```

The accepted R_AI is the only Wave C authority. The 4AF block below remains a
non-executable historical illustration and cannot authorize work.

**Historical non-executable 4AF authority illustration:**

```text
set -euo pipefail
shopt -s inherit_errexit
task_file='docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
test_file='tests/validation/test_agent_governance_ci_routing.py'
extract_range() {
  python3 - "$task_file" "$1" <<'PY'
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("review-range-read")

label = sys.argv[2]
candidates = []
for source_line in text.splitlines():
    line = source_line.strip(" \t")
    candidate_view = line[1:] if line.startswith("|") else line
    separator = candidate_view.find("|")
    if separator < 0:
        continue
    first_cell = candidate_view[:separator].strip(" \t")
    if first_cell == label:
        candidates.append(line)
if len(candidates) != 1:
    raise SystemExit("review-range-row-count")

row = candidates[0]
if not row.startswith("|") or not row.endswith("|"):
    raise SystemExit("review-range-cell-count")
if "\\|" in row or "\\`" in row:
    raise SystemExit("review-range-escape")
parts = row.split("|")
if len(parts) != 9 or parts[0] != "" or parts[-1] != "":
    raise SystemExit("review-range-cell-count")
cells = [part.strip(" \t") for part in parts[1:-1]]
if len(cells) != 7 or cells[0] != label:
    raise SystemExit("review-range-label")
for index, cell in enumerate(cells):
    if index != 4 and ("`" in cell or ".." in cell):
        raise SystemExit("review-range-extra-token")
match = re.fullmatch(
    r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
    cells[4],
    flags=re.ASCII,
)
if match is None:
    raise SystemExit("review-range-value")
print(f"{match.group(1)}..{match.group(2)}")
PY
}
assert_edge() {
  local parent="$1"
  local child="$2"
  local distance
  local parent_count
  local first_parent
  git merge-base --is-ancestor "$parent" "$child"
  distance="$(
    git rev-list --count "$parent..$child"
  )"
  test "$distance" -eq 1
  parent_count="$(
    git rev-list --parents -n 1 "$child" |
      awk '{print NF - 1}'
  )"
  test "$parent_count" -eq 1
  first_parent="$(
    git rev-parse "$child^1"
  )"
  test "$first_parent" = "$parent"
}
plan_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row proof Plan'
)"
test -n "$plan_review_range"
design_base="${plan_review_range%%..*}"
test "$design_base" = \
  "8cacc4634448416a7dbc8d3de69bf6011b62c6d5"
plan_checkpoint="${plan_review_range##*..}"
test -n "$plan_checkpoint"
implementation_review_range="$(
  extract_range \
    'T-TSDC-004R-4AF canonical-row implementation'
)"
test -n "$implementation_review_range"
implementation_base="${implementation_review_range%%..*}"
test -n "$implementation_base"
implementation_commit="${implementation_review_range##*..}"
test -n "$implementation_commit"
review_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$review_checkpoint"
verified_design_base="$(
  git rev-parse --verify "$design_base^{commit}"
)"
test "$verified_design_base" = "$design_base"
verified_plan_checkpoint="$(
  git rev-parse --verify "$plan_checkpoint^{commit}"
)"
test "$verified_plan_checkpoint" = "$plan_checkpoint"
verified_implementation_base="$(
  git rev-parse --verify "$implementation_base^{commit}"
)"
test "$verified_implementation_base" = "$implementation_base"
verified_implementation_commit="$(
  git rev-parse --verify "$implementation_commit^{commit}"
)"
test "$verified_implementation_commit" = "$implementation_commit"
base_subject="$(
  git show -s --format=%s "$design_base"
)"
test "$base_subject" = \
  "docs(task): record exhausted exact-cell review-range plan review"
base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record exhausted exact-cell review-range plan review'
)"
test "$base_subject_count" -eq 1
plan_subject="$(
  git show -s --format=%s "$plan_checkpoint"
)"
test "$plan_subject" = \
  "docs(plan): define canonical-row authority proof"
plan_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(plan): define canonical-row authority proof'
)"
test "$plan_subject_count" -eq 1
implementation_base_subject="$(
  git show -s --format=%s "$implementation_base"
)"
test "$implementation_base_subject" = \
  "docs(task): record canonical-row authority plan reviews"
implementation_base_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority plan reviews'
)"
test "$implementation_base_subject_count" -eq 1
implementation_subject="$(
  git show -s --format=%s "$implementation_commit"
)"
test "$implementation_subject" = \
  "fix(ci): close canonical-row authority proof"
implementation_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'fix(ci): close canonical-row authority proof'
)"
test "$implementation_subject_count" -eq 1
review_subject="$(
  git show -s --format=%s "$review_checkpoint"
)"
test "$review_subject" = \
  "docs(task): record canonical-row authority review"
review_subject_count="$(
  git log --all --format='%s' |
    grep -Fxc \
      'docs(task): record canonical-row authority review'
)"
test "$review_subject_count" -eq 1
assert_edge "$design_base" "$plan_checkpoint"
assert_edge "$plan_checkpoint" "$implementation_base"
assert_edge "$implementation_base" "$implementation_commit"
assert_edge "$implementation_commit" "$review_checkpoint"
base_paths="$(
  git diff-tree --no-commit-id --name-only -r "$design_base" |
    sort
)"
test "$base_paths" = "$task_file"
expected_plan_paths="$(
  printf '%s\n' \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
    "$task_file" |
    sort
)"
test -n "$expected_plan_paths"
expected_implementation_paths="$(
  printf '%s\n' \
    "$task_file" \
    "$test_file" |
    sort
)"
test -n "$expected_implementation_paths"
plan_paths="$(
  git diff-tree --no-commit-id --name-only -r "$plan_checkpoint" |
    sort
)"
test "$plan_paths" = "$expected_plan_paths"
plan_range_paths="$(
  git diff --name-only "$design_base..$plan_checkpoint" |
    sort
)"
test "$plan_range_paths" = "$expected_plan_paths"
base_review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_base" |
    sort
)"
test "$base_review_paths" = "$task_file"
base_review_range_paths="$(
  git diff --name-only "$plan_checkpoint..$implementation_base" |
    sort
)"
test "$base_review_range_paths" = "$task_file"
implementation_paths="$(
  git diff-tree --no-commit-id --name-only -r "$implementation_commit" |
    sort
)"
test "$implementation_paths" = "$expected_implementation_paths"
implementation_range_paths="$(
  git diff --name-only "$implementation_base..$implementation_commit" |
    sort
)"
test "$implementation_range_paths" = "$expected_implementation_paths"
git diff --exit-code \
  "$implementation_base..$implementation_commit" -- . \
  ":(exclude)$test_file" \
  ":(exclude)$task_file"
review_paths="$(
  git diff-tree --no-commit-id --name-only -r "$review_checkpoint" |
    sort
)"
test "$review_paths" = "$task_file"
review_range_paths="$(
  git diff --name-only "$implementation_commit..$review_checkpoint" |
    sort
)"
test "$review_range_paths" = "$task_file"
base_mode="$(
  git ls-tree "$design_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_mode" = "100644"
plan_mode="$(
  git ls-tree "$plan_checkpoint" \
    docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md |
    awk '{print $1}'
)"
test "$plan_mode" = "100644"
plan_task_mode="$(
  git ls-tree "$plan_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$plan_task_mode" = "100644"
base_review_task_mode="$(
  git ls-tree "$implementation_base" "$task_file" |
    awk '{print $1}'
)"
test "$base_review_task_mode" = "100644"
base_review_test_mode="$(
  git ls-tree "$implementation_base" "$test_file" |
    awk '{print $1}'
)"
test "$base_review_test_mode" = "100644"
implementation_test_mode="$(
  git ls-tree "$implementation_commit" "$test_file" |
    awk '{print $1}'
)"
test "$implementation_test_mode" = "100644"
implementation_task_mode="$(
  git ls-tree "$implementation_commit" "$task_file" |
    awk '{print $1}'
)"
test "$implementation_task_mode" = "100644"
review_task_mode="$(
  git ls-tree "$review_checkpoint" "$task_file" |
    awk '{print $1}'
)"
test "$review_task_mode" = "100644"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$review_checkpoint"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

**Files:**

- Modify `scripts/validation/github_workflow_contract.py`.
- Modify `tests/validation/test_github_workflow_contract.py`.
- Modify the Task ledger.

- [ ] **Step 1: Add a RED absence test for the obsolete authority.**

  First assert that Wave A already removed `ExpensiveCommandOwner` and
  `_EXPENSIVE_COMMAND_BASELINE`. Require removal of the remaining dead
  `_ShellSubstitution`, `_PreparedShellProgram`, `_ScriptInvocation`,
  `_ShellAnalysis`, `_VariableBinding`, `_SemanticResolution`,
  `_TraversalBudget`, `_analyze_shell_program`, `_analyze_python_helper`,
  `_resolve_job_semantics`, `_semantic_command_marker`, and
  `_semantic_command_signatures`.

- [ ] **Step 2: Run RED.**

```bash
python3 -m unittest \
  tests.validation.test_github_workflow_contract \
  -v
```

Expected RED: the independently approved but obsolete interpreter symbols
still exist.

- [ ] **Step 3: Delete the dead interpreter and only its obsolete grammar
  tests.**

  Preserve every schema-v2, exact projection, trigger, permission,
  concurrency, timeout, job identity, Action, YAML safety, bounded-reader,
  remote-mutation, and CI-precommit regression. Remove unused imports and
  constants only after static analysis proves no consumer.

- [ ] **Step 4: Run behavior-preserving GREEN.**

```bash
python3 -m unittest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
python3 scripts/validation/check-github-workflow-contract.py
actionlint
python3 -m ruff check \
  scripts/validation/github_workflow_contract.py \
  tests/validation/test_github_workflow_contract.py
python3 -m compileall -q \
  scripts/validation/github_workflow_contract.py \
  tests/validation/test_github_workflow_contract.py
git diff --check
```

Expected GREEN: typed behavior is byte-for-byte equivalent at the CLI
boundary, old semantic symbols are absent, and no shell/Python source
interpreter remains.

- [ ] **Step 5: Commit and review.**

```bash
git add \
  scripts/validation/github_workflow_contract.py \
  tests/validation/test_github_workflow_contract.py \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "refactor(ci): remove semantic command interpreter"
```

Assign fresh specification and quality/security reviewers. Both must return
C0/I0 before Task 4R evidence promotion.

- [ ] **Step 6: Commit the removal-review evidence.**

  After both reviewers return C0/I0, append their exact range and verdicts and
  commit:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): record semantic interpreter removal review"
```

#### Task 4.6 / T-TSDC-004R-6: Task 4 Recovery Evidence

- [ ] Run the full Task 4R focused ladder from a clean committed checkpoint.
- [ ] Record exact commands, results, skipped CI-only gates, rollback commits,
  and review ranges in the Task ledger.
- [ ] Keep every manifest review verdict `pending`; Task 6 owns one unified,
  review-bound promotion after Tasks 1–5 all have committed C0/I0 evidence.
- [ ] Regenerate the delta summary through its canonical writer.

```bash
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory \
  --write-summary
```

- [ ] Commit the evidence candidate:

```bash
git add \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): close typed CI gate recovery"
```

- [ ] Assign fresh final Task 4R specification and quality/security reviewers
  to the whole recovery range.
- [ ] If both remain C0/I0, append a value-free final review record and mark
  T-TSDC-004 completed.
- [ ] Commit that terminal Task 4R review evidence before T-TSDC-005:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): record final typed CI recovery review"
```

  Only this clean committed boundary may start T-TSDC-005.

Expected completion evidence:

- exact 7/23/8/16 workflow invariants;
- one strict schema-v2 registry with no `owner_commands`,
  `expensive_commands`, or semantic interpreter;
- one required root owner and at most one workflow reachability for every
  required `suite_key`;
- deterministic fake executor, `--list`, and dry-run output;
- CI/local profile parity;
- separate CI and Agent pre-commit authority;
- local tracked implementation only, with remote execution and enforcement
  still unverified.

### Task 5: T-TSDC-005 — Reconcile Audit and Remote Observation Evidence

**Files:**

- Modify
  `docs/90.references/data/governance/ref-0071-github-actions-control-plane-observation.yaml`.
- Modify
  `docs/90.references/audits/ref-0019-readme.md`.
- Modify affected rows only in:
  `implementation-overview.md`,
  `automation-candidates.md`,
  `frontmatter-template-readme-implementation.md`,
  `sdlc-quality-formatting-implementation.md`, and
  `security-framework-maturity.md`.
- Modify
  `docs/90.references/data/governance/ref-0065-audit-implementation-matrix.md`
  only through
  `scripts/validation/generate-audit-implementation-matrix.sh`.
- Modify
  `docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md`
  only through the metadata checker report mode.
- Modify `scripts/validation/check-repo-contracts.sh` and
  `tests/validation/test_agent_governance_ci_routing.py` only for the updated
  remote observation schema/facts.
- Modify the Task 1 manifest/summary and sibling Task ledger.

**Observation facts:**

- repository: `buenhyden/hy-home.docker`;
- observed local base:
  `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`;
- remote default commit:
  `bffc5aedb7c2bd7da1da0db34d58e56bf144412e`, behind local;
- recent main CI run: `30325161033`, conclusion `failure`;
- recent PR run: `30325219960`, conclusion `failure`;
- remote required contexts: 12;
- locally desired but not remotely required:
  `docs-implementation-alignment`,
  `agent-output-eval-fixture-gate`,
  `supply-chain-fixture-policy`, and
  `dependency-vulnerability-audit`;
- strict checks, one approval, CODEOWNERS review, conversation resolution,
  force-push/deletion disabled;
- `enforce_admins=false`, `required_linear_history=false`,
  `dismiss_stale_reviews=false`, `require_last_push_approval=false`, required
  signatures disabled, rulesets response empty;
- root causes and raw logs remain `unverified`/unread.

- [ ] Add exact RED tests
  `test_remote_observation_separates_desired_observed_unverified_and_proposed`,
  `test_remote_required_context_drift_is_exact_set_difference`, and
  `test_canonical_audit_records_typed_gate_control_plane` to
  `AgentGovernanceRoutingTests`. They distinguish tracked desired state,
  observed remote state, unverified cause, proposed future synchronization,
  and the four-context set difference without claiming that remote checks
  failed to run. The audit assertion covers the delta checker, README
  convergence, version synchronization, schema-v2 typed gate registry,
  structural CI ownership boundary, CI pre-commit route, and remaining
  remote/CD/runtime gaps.
- [ ] Run and record the behavior-specific RED before any observation, audit,
  generator, or manifest edit:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_remote_observation_separates_desired_observed_unverified_and_proposed \
  tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_remote_required_context_drift_is_exact_set_difference \
  tests.validation.test_agent_governance_ci_routing.AgentGovernanceRoutingTests.test_canonical_audit_records_typed_gate_control_plane \
  -v
```

  Expected RED: all three named tests import and fail on stale tracked facts;
  a missing test or import failure is not accepted as RED evidence.

- [ ] Update the observation using only sanitized metadata already obtained;
  do not perform another remote call or read raw logs.
- [ ] Reconcile only audit rows whose implementation truth changed. Keep CD,
  live deployment, broad vulnerability scanning, self-hosted runner inventory,
  and remote enforcement as Partial, Missing, or Needs Revalidation according
  to evidence.
- [ ] Preserve the 2026-07-07 pack as superseded mapping-only evidence; do not
  revive or duplicate it.
- [ ] Regenerate the audit matrix and metadata inventory through these exact
  write commands, then prove byte-for-byte freshness with their `--check`
  forms:

```bash
bash scripts/validation/generate-audit-implementation-matrix.sh
python3 scripts/validation/check-document-metadata.py \
  --mode report \
  --output docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md
```

- [ ] Update only the applicable delta-manifest review/evidence rows and
  regenerate only its derived summary through:

```bash
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory \
  --write-summary
```

- [ ] Run:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_ci_routing \
  tests.validation.test_target_surface_delta_contracts \
  -v
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
bash scripts/validation/generate-audit-implementation-matrix.sh --check
python3 scripts/validation/check-document-metadata.py \
  --mode report \
  --output docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md \
  --check
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

Expected GREEN: canonical audit total remains 161 with recalculated affected
statuses; generated matrix and inventory are fresh; the observation contains
the dated 12-vs-16 comparison and no root-cause inference; audit claims describe
typed structural ownership without claiming arbitrary leaf semantics or remote
enforcement; all cross-links resolve.

- [ ] Record affected audit row IDs, before/after totals, generator commands,
  and the observation boundary in the Task ledger, then commit the
  implementation candidate:

```bash
git add \
  docs/90.references/data/governance/ref-0071-github-actions-control-plane-observation.yaml \
  docs/90.references/audits/ref-0019-readme.md \
  docs/90.references/audits/ref-0026-implementation-overview.md \
  docs/90.references/audits/ref-0021-automation-candidates.md \
  docs/90.references/audits/ref-0024-frontmatter-template-readme-implementation.md \
  docs/90.references/audits/ref-0030-sdlc-quality-formatting-implementation.md \
  docs/90.references/audits/ref-0031-security-framework-maturity.md \
  docs/90.references/data/governance/ref-0065-audit-implementation-matrix.md \
  docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md \
  scripts/validation/check-repo-contracts.sh \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(audit): reconcile target surface evidence"
```

- [ ] Obtain independent specification and quality/security reviews of that
  committed candidate.
- [ ] After both return C0/I0, append their exact ranges and verdicts and
  commit the evidence before Task 6:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): record audit reconciliation review"
```

### Task 6: T-TSDC-006 — Promote Enforcement and Close the Branch

**Files:**

- Modify
  `docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml`
  to set `enforcement: blocking` only after Tasks 1–5 have pass/pass reviews.
- Regenerate
  `docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md`.
- Inspect `scripts/validation/check-repo-contracts.sh` and
  `scripts/validation/run-local-qa-gates.sh` with the exact
  `check-target-surface-delta-contract.py --mode advisory` search. Replace each
  matching active invocation with `--mode blocking`; when neither file
  contains that exact active invocation, leave both byte-unchanged and record
  the no-op in the Task ledger.
- Modify this Plan status to `completed`.
- Modify the sibling Task ledger status to `completed` only after all closure
  evidence exists.
- Modify `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md` for the bounded handoff.
- Modify generated owners only through their registered generators.

**Closure interface:**

The manifest can move from `advisory` to `blocking` only when all 158 rows have
a valid disposition and both review verdicts equal `pass`, Tasks 1–5 and every
Task 4R review boundary are committed and independently approved, generated
outputs are fresh, and the Spec 133 integrity test is green. A finding after
promotion is a product failure and blocks closure.

- [ ] Confirm the worktree is clean at the Task 5 reviewed commit before final
  verification.
- [ ] From that clean checkpoint, compute the exact Git-visible branch-delta
  path set for the optional controlled Agent wrapper. For every changed path,
  use the full file path as an `--allow-prefix` unless a proposed directory
  prefix contains no other tracked or untracked Git-visible path. Append the
  literal path-by-path command and reviewed path set to the Task ledger without
  running it. No command substitution, generated shell fragment, wildcard,
  root-level target prefix, or direct `pre-commit run` is admitted.
- [ ] Commit that command-evidence boundary before requesting approval:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): stage controlled all-files qa request"
```

- [ ] Confirm the worktree is clean at that new command-evidence commit, then
  request a separate user approval for the exact recorded one-attempt command.
  Approval for any earlier command, prefix set, or checkpoint does not carry
  forward.
- [ ] If separately approved, run that exact literal wrapper command once. If
  approval is absent or the user directs a skip, do not run it and record
  `NOT AUTHORIZED / NOT RUN`. In either case append only value-free
  disposition, exit/snapshot facts when available, and exact Git-visible path
  sets to the Task ledger.
- [ ] Before any manifest, routing, enforcement, Plan-status, or handoff edit,
  commit the wrapper disposition. If the one approved attempt produced
  allowlisted hook mutations, inspect and validate them, include them in this
  independently reviewed logical unit, and do not run a second attempt:

```bash
git add docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "docs(task): record controlled all-files qa disposition"
```

  Add any actual allowlisted hook-mutated paths explicitly to that `git add`
  command; never stage by directory or wildcard. A failed or skipped attempt
  remains honest evidence and is not converted to pass. Any necessary manual
  remediation is a new focused implementation/review unit, not a second
  wrapper attempt.

- [ ] Recompute predecessor-to-`HEAD` target changes and confirm every path has
  exactly one current manifest row.
- [ ] Confirm Spec 133 tracked artifact hashes match the closure commit.
- [ ] Build a `Manifest Review Promotion Crosswalk` in the Task ledger before
  changing any verdict. It must list each of the 158 row paths exactly once,
  assign the latest logical unit that created or modified that row, and cite
  that unit's committed implementation range plus independent specification
  and quality/security C0/I0 review ranges. Use the Task 5 reviewed commit as
  the fixed checkpoint and `git blame --line-porcelain` on the complete row
  blocks to detect later uncited row changes. Duplicate, missing, uncommitted,
  non-C0/I0, or out-of-range evidence blocks promotion.
- [ ] Record the pre-promotion oracle:

```bash
rg -c '^  spec_verdict: pending$' \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml
rg -c '^  quality_verdict: pending$' \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml
```

  Both counts must equal 158; any existing `pass` or `fail` before this unified
  step is a contract error, proven by:

```bash
if rg -n '^  (spec_verdict|quality_verdict): (pass|fail)$' \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml; then
  exit 1
fi
```

- [ ] Use `apply_patch` to change exactly the 158 crosswalk-approved
  `spec_verdict: pending` and 158 `quality_verdict: pending` values to `pass`.
  Change no row identity, finding, provenance, rollback, owner, consumer,
  validator, or test field in that patch.
- [ ] Prove the post-promotion oracle before changing enforcement:

```bash
rg -c '^  spec_verdict: pass$' \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml
rg -c '^  quality_verdict: pass$' \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml
```

  Both counts must equal 158, and exact searches for pending or failed review
  verdicts must return no row:

```bash
if rg -n '^  (spec_verdict|quality_verdict): (pending|fail)$' \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml; then
  exit 1
fi
```

- [ ] Set enforcement to `blocking`, regenerate the summary through its
  canonical writer, and run the focused delta tests/checker.

```bash
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode blocking \
  --write-summary
```

- [ ] Run the final local validation ladder:

```bash
python3 -m unittest \
  tests.validation.test_target_surface_contracts \
  tests.validation.test_target_surface_delta_contracts \
  tests.validation.test_document_metadata \
  tests.validation.test_tech_stack_version_contract \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
bash tests/validation/test_run_ci_precommit.sh
python3 scripts/validation/check-target-surface-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py --mode blocking
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile ci --list
python3 scripts/validation/run-ci-gate.py --profile ci --dry-run --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-script-backed \
  --dry-run \
  --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-harness \
  --dry-run \
  --all
python3 scripts/validation/run-ci-gate.py \
  --profile local-all-profiles \
  --dry-run \
  --all
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/operations/sync-tech-stack-versions.sh --check
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
bash scripts/hardening/check-all-hardening.sh
python3 scripts/validation/check-supply-chain-policy.py --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/check-repo-contracts.sh
actionlint
git diff --check
```

Expected GREEN: all focused and aggregate checks pass; delta enforcement is
blocking with zero findings; generated owners are fresh; version, hardening,
metadata, links, typed gate registry, deterministic dry-run, workflow, audit,
and repository contracts are green.

- [ ] If any command is unavailable, record the exact environment limitation
  and leave the corresponding result `unverified`; never convert it to pass.
- [ ] Do not run direct all-files pre-commit.

- [ ] Commit the blocking-enforcement candidate before whole-branch review:

```bash
git add \
  docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md \
  scripts/validation/check-repo-contracts.sh \
  scripts/validation/run-local-qa-gates.sh \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git commit -m "feat(governance): promote target delta enforcement"
```

- [ ] Assign a fresh whole-branch correctness/specification reviewer to that
  committed candidate.
- [ ] Assign a different fresh whole-branch security/quality reviewer.
- [ ] Remediate every Critical and Important finding with a new focused test
  and re-review.
- [ ] Record final commits, review ranges, deletion ledger, local/remote/
  skipped/unverified distinctions, and terminal evidence.
- [ ] Advance `current.md` to the next bounded handoff without rewriting
  historical `progress.md`.
- [ ] Only after both whole-branch reviewers return C0/I0, set this Plan and
  the Task ledger to `completed`, update `current.md`, and commit the terminal
  evidence:

```bash
git add \
  docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
  docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
  docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md
git commit -m "docs(task): close target surface delta convergence"
```

### T-TSDC-004R-4AL — Atomic reviewed-blob terminal proof

This section is preserved as the historical 4AL design and P_AL review package
contract for the bounded documentation-only lineage
`D_AL -> S_AL -> P_AL -> B_AL|XP_AL`. D_AL is
`2d2f49dfccb5fec282b2792fe0984d80327b4254`. S_AL is
`eafdaf0433d9e600abbc9b8e2443bdd7b84a9868`, has the exact unique subject
`docs(design): define atomic reviewed-blob successor`, and is the sole parent
of P_AL. P_AL has the exact subject
`docs(plan): define atomic reviewed-blob terminal proof`; its own OID could not
be self-asserted in its tree and had to be resolved after publication by exact
subject, parent, distance, tree, paths, modes, and blob proof. The current
correction authority is the 4AM section below; AL steps are no longer executable
current instructions.

The two mutually exclusive terminal subjects are
`docs(task): record atomic reviewed-blob terminal plan reviews` for B_AL and
`docs(task): record exhausted atomic reviewed-blob terminal plan review` for
XP_AL. P_AL contains no B_AL or XP_AL Commit Ledger row. The terminal builder
adds exactly one selected row and must prove that the other subject and row are
absent. B_AL records a fully accepted Plan review set. XP_AL records a
complete, parseable review set that is non-accepted or has a proved reviewer
identity collision. Missing, truncated, hash-invalid, or schema-malformed
evidence stops without a terminal. Neither terminal grants implementation
authority by itself.

At the time P_AL was current, the Task ledger owner was `TSDC-AL-STATE`. Its
state block, Approval Evidence, Work Breakdown, Work Log, Planning Verification,
Task Execution Evidence, atomic reviewed-blob Plan boundary, Review Evidence,
Commit Ledger, Deferred and Blocked Items, and final handoff were intended as
the exact eleven projections of one tuple. 4AL failed because that inventory was
not complete enough for terminal publication; 4AM replaces it with a
full-document discovery and bijective inventory requirement.

#### Authority and exact file map

- P_AL may modify only
  `docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md` and
  `docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md`,
  both as mode `100644`.
- B_AL or XP_AL may modify only the Task path above as mode `100644`; the Plan
  blob must equal P_AL exactly.
- Titles, frontmatter, artifact status, and folder-level summaries remain
  unchanged, so no parent README update is required.
- 4AI and rejected 4AK remain immutable historical evidence. Rejected 4AK is
  bound to frozen draft SHA256
  `b746147f3f40039c801d5e97f1448575e096012f158f7dc313b4b54733f4bf47`,
  formal `C0/I5/M0; SPEC_COMPLIANCE NO; DRAFT_READY NO`, quality/security
  `C0/I6/M0; QUALITY_SECURITY FAIL; DRAFT_READY NO`, no P_AK/B_AK/XP_AK, and
  an exact reversal to clean D_AL.
- implementation, E_AL, R_AL, XE_AL, Task 4.5, Wave C, Tasks 5–6, runtime, remote/external actions, QA-wrapper/pre-commit execution, dependency changes, and Graphify update are blocked/no authority. This exact tuple must
  remain verbatim in every current Task projection through P_AL and either
  terminal.

#### Immutable review and identity contract

The review package is an LF-delimited, final-newline envelope with this exact
field order:

```text
BEGIN TSDC-4AL-PACKAGE
schema: tsdc-4al-plan-review/v2
d_al: 2d2f49dfccb5fec282b2792fe0984d80327b4254
s_al: eafdaf0433d9e600abbc9b8e2443bdd7b84a9868
p_al: 40-lowercase-hex P_AL OID
s_subject: docs(design): define atomic reviewed-blob successor
p_subject: docs(plan): define atomic reviewed-blob terminal proof
review_distance: 1
plan_path: docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md
task_path: docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
plan_mode: 100644
task_mode: 100644
plan_blob: 40-or-64-lowercase-hex object OID
task_blob: 40-or-64-lowercase-hex object OID
p_commit_sha256: 64-lowercase-hex digest of raw commit bytes
p_commit_bytes: positive decimal integer
p_diff_sha256: 64-lowercase-hex digest of binary S_AL..P_AL diff bytes
p_diff_bytes: positive decimal integer
pal_transaction_blob: 40-or-64-lowercase-hex object OID
pal_transaction_sha256: 64-lowercase-hex digest
pal_transaction_bytes: positive decimal integer
terminal_renderer_blob: 40-or-64-lowercase-hex object OID
terminal_renderer_sha256: 64-lowercase-hex digest
terminal_renderer_bytes: positive decimal integer
terminal_publisher_blob: 40-or-64-lowercase-hex object OID
terminal_publisher_sha256: 64-lowercase-hex digest
terminal_publisher_bytes: positive decimal integer
b_al_subject: docs(task): record atomic reviewed-blob terminal plan reviews
xp_al_subject: docs(task): record exhausted atomic reviewed-blob terminal plan review
projection_anchors_sha256: 64-lowercase-hex digest of the ordered anchor list
prohibited_authority: implementation, E_AL, R_AL, XE_AL, Task 4.5, Wave C, Tasks 5–6, runtime, remote/external actions, QA-wrapper/pre-commit execution, dependency changes, and Graphify update are blocked/no authority.
END TSDC-4AL-PACKAGE
```

The package blob is `git hash-object -w --stdin` over those exact bytes. Its
SHA256 and byte count are computed before materialization and rebound by every
assignment and report.

The projection-anchor input is not an informal list. It is one immutable,
LF-delimited, final-newline file with these exact bytes and order:

```text
BEGIN TSDC-4AL-PROJECTION-ANCHORS
schema: tsdc-4al-projection-anchors/v1
task_path: docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
owner: TSDC-AL-STATE
anchor: state
anchor: approval_evidence
anchor: work_breakdown
anchor: work_log
anchor: planning_verification
anchor: task_execution_evidence
anchor: boundary_section
anchor: review_evidence
anchor: commit_ledger
anchor: deferred_blocked
anchor: final_handoff
END TSDC-4AL-PROJECTION-ANCHORS
```

The package stores only this file's SHA256; the controller separately freezes
and materializes the anchor file itself as a reviewed Git blob so a reviewer can
recompute the digest. P_AL cannot self-assert its own commit OID or the final
`S_AL..P_AL` diff digest in the two tracked files without recursion. The
controller therefore freezes the final tracked bytes first, resolves the two
document blob OIDs and binary diff outside the tree, launches the reviewed P_AL
transaction with those exact externally bound values, and only then resolves
P_AL by parent, subject, distance, raw commit, tree, path, mode, and blob. AL-3
binds those resolved values into the immutable package; no placeholder in the
P_AL tree is treated as evidence.

Exactly four read-only review slots inspect the same immutable P_AL lineage:

1. `C_AL_SPEC`: candidate specification review;
2. `C_AL_QS`: candidate quality/security review;
3. `F_AL_SPEC`: formal specification review, including the candidate artifacts;
4. `F_AL_QS`: formal quality/security review, including the candidate artifacts.

The orchestrator assigns all four slots directly. Their canonical agent
identities must be pairwise distinct and may not be inferred from self-declared
labels. The controller takes the canonical task path returned by the
orchestrator assignment call, creates one immutable assignment envelope, and
sends only its blob OID plus the package blob OID to that reviewer. Assignment
bytes use this closed order:

```text
BEGIN TSDC-4AL-ASSIGNMENT
schema: tsdc-4al-assignment/v1
slot: C_AL_SPEC|C_AL_QS|F_AL_SPEC|F_AL_QS
canonical_identity: canonical task path returned by the orchestrator
assignment_source: /root
package_blob: 40-or-64-lowercase-hex package object OID
package_sha256: 64-lowercase-hex package digest
package_bytes: positive decimal package byte count
candidate_spec_review_blob: NONE|40-or-64-lowercase-hex object OID
candidate_qs_review_blob: NONE|40-or-64-lowercase-hex object OID
END TSDC-4AL-ASSIGNMENT
```

Candidate assignments require both candidate-review fields `NONE`; formal
assignments require both exact candidate report OIDs. The terminal renderer
trusts identity and assignment source only from these controller-created
assignment blobs and requires each reviewer envelope to match its assignment.
Each record also binds S_AL and P_AL OIDs, exact `S_AL..P_AL` distance, Plan and
Task blob OIDs, review package identity, verdict, and readiness field. A
reviewer must not edit the worktree or create a commit.

Every reviewer output is captured once, materialized once with
`git hash-object -w --stdin`, and then consumed only by its blob OID through
`git cat-file blob`. Multiline output uses an exact `BEGIN ...` and `END ...`
envelope, LF line endings, final newline, byte count, and SHA256. Candidate
review blobs become inputs to both formal reviewers. The terminal Task embeds
all four exact envelopes plus their blob OIDs, byte counts, and hashes; mutable
pathname rereads are prohibited.

The envelope grammar is closed and line ordered:

```text
BEGIN TSDC-4AL-REVIEW
slot: C_AL_SPEC|C_AL_QS|F_AL_SPEC|F_AL_QS
canonical_identity: orchestrator-assigned canonical task path
assignment_source: /root
assignment_blob: 40-or-64-lowercase-hex assignment object OID
review_base: 40-lowercase-hex S_AL OID
review_head: 40-lowercase-hex P_AL OID
review_distance: 1
plan_blob: 40-or-64-lowercase-hex object OID
task_blob: 40-or-64-lowercase-hex object OID
package_blob: 40-or-64-lowercase-hex package object OID
package_sha256: 64-lowercase-hex digest
package_bytes: positive decimal integer
candidate_spec_review_blob: NONE|40-or-64-lowercase-hex object OID
candidate_qs_review_blob: NONE|40-or-64-lowercase-hex object OID
critical: nonnegative decimal integer
important: nonnegative decimal integer
minor: nonnegative decimal integer
spec_compliance: YES|NO|NA
quality_security: PASS|FAIL|NA
plan_terminal_ready: YES|NO
findings: value-free single-line disposition
END TSDC-4AL-REVIEW
```

Specification slots must use `quality_security: NA`; quality/security slots
must use `spec_compliance: NA`. Candidate slots must use `NONE` for both
candidate-review blob fields. Formal slots must name both exact candidate
report blob OIDs. All other enum or field combinations are malformed and
cannot select B_AL. Envelope hash and byte-count metadata are kept outside the
envelope to avoid self-reference.

B_AL is selected only when all four reports are structurally valid, identity
distinctness is proved, each reports `C0/I0/M0`, both specification slots state
`SPEC_COMPLIANCE YES`, both quality/security slots state
`QUALITY_SECURITY PASS`, and all four state `PLAN_TERMINAL_READY YES`. Every
other completed disposition selects XP_AL. Missing or malformed evidence stops
before terminal construction; it is not silently converted into acceptance.

#### Frozen reviewed assets and closed launchers

These out-of-tree assets are immutable Plan evidence. Their Git blob OIDs are
the content-addressed results for the exact bytes shown; the controller must
materialize those same bytes before any authorized downstream use.

| Asset | SHA256 | Bytes | Lines | Git blob OID |
| --- | --- | ---: | ---: | --- |
| P_AL transaction `/tmp/tsdc-4al-create-pal.sh` | `752293831b3b3117476092c0526ea1ac728051fdfb1a3103473c353cb749ac0f` | 75,145 | 1,013 | `e26e6f02be09bf67c56cc16840b03f289ea553aa` |
| Package builder `/tmp/tsdc-4al-build-review-package.py` | `3aac58ddeae93f06d39bd28351d1e63a6134ab30967b8b9ab82325cf69a78f8a` | 34,348 | 932 | `6da62868ec3f630a3e77dfdb286641c49d9bc37c` |
| Terminal renderer `/tmp/tsdc-4al-render-terminal.py` | `df6a57db6814b34f3969774331522eeeca544d8f75581fd1a362d47fe6ee4598` | 69,917 | 1,862 | `0666e96ab43d66e9d075892d591ca790f8280661` |
| Terminal publisher `/tmp/tsdc-4al-publish-terminal.py` | `e6841b0d7627bbd97b0e2b9b9ca7b486cd4964f1467dcf68ea9531d473559b83` | 208,072 | 5,552 | `755ffde61559cb259021d6a7b2752f99afb67959` |
| Projection anchors `/tmp/tsdc-4al-projection-anchors.txt` | `4dbee6d432d9f3a2cc704881867d7db7b42595846c96f3a413f392475fde114b` | 468 | 16 | `bd036ba49089cc1f27d91bdaa1f2478fcb1ef1f9` |

The P_AL transaction has independent final specification and security verdicts
`C0/I0/M0`, `PASS`, and `EXECUTION_READY YES`. The package builder has an
independent `C0/I0/M0` contract verdict. The renderer and final publisher each
have independent specification and security verdicts `C0/I0/M0`, `PASS`, and
`EXECUTION_READY YES`; rejected intermediate publisher identities are not
execution authority.

One earlier reviewed P_AL transaction identity,
`5c0c0a1bf9e84e2879638777c15365ac4160c8fe5e952aeaf6db37a2f50e9be5`/
`fcf15cf2839f72242db9933c4ff72a7cae8f0f77`, was launched once and failed
closed at `configuration contract` before object creation,
transaction-directory creation, ref/index/worktree mutation, or success
output. Git accepts unsupported `core.fsync*` values with exit zero while
emitting C-locale warnings, so the superseded probe's nonzero-exit assumption
was rejected. The current transaction instead requires empty stderr for the
valid probe and exact C-locale warnings for both invalid probes. The prior
identity is historical failure evidence only. A retry may use only the current
identity after the Plan, Task, diff package, launcher, and transaction are all
rebound to their exact final bytes and independently re-reviewed.

The P_AL transaction is launched only from an unlinked memfd sealed with
`F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE`. Its exact command is
`/usr/bin/bash /proc/<launcher-pid>/fd/<sealed-fd>` with inherited cwd `/` and a
closed environment containing only `PATH=/usr/bin:/bin`, `LC_ALL=C`,
`TZ=Asia/Seoul`, Bash-normalized `PWD=/`, `SHLVL=1`, `_`,
`TSDC_PACKAGE_PATH=/tmp/review-4al-plan.diff`, the externally resolved package
SHA256 and byte count, and
`TSDC_REVIEWED_SCRIPT_SHA256=752293831b3b3117476092c0526ea1ac728051fdfb1a3103473c353cb749ac0f`.
Classifier mode replaces the package path with exact recovery mode/directory
fields while retaining the package identity and reviewed-script identity.

The package builder accepts exactly these six option/value pairs in order:

```text
--p-al <resolved-P_AL>
--pal-transaction-blob e26e6f02be09bf67c56cc16840b03f289ea553aa
--terminal-renderer-blob 0666e96ab43d66e9d075892d591ca790f8280661
--terminal-publisher-blob 755ffde61559cb259021d6a7b2752f99afb67959
--anchors-file /tmp/tsdc-4al-projection-anchors.txt
--output /tmp/tsdc-4al-review-package.txt
```

The renderer is launched from its own sealed descriptor as
`/usr/bin/python3 -I -B /proc/self/fd/<sealed-fd>`, cwd `/`, with exactly
`PATH`, `HOME`, `XDG_CONFIG_HOME`, `LC_ALL`, `LANG`, `TZ`, `TERM`, and two
pairwise-distinct inherited output-FD variables. The fixed values are
`PATH=/usr/bin:/bin`, `HOME=/nonexistent`,
`XDG_CONFIG_HOME=/nonexistent`, `LC_ALL=C`, `LANG=C`, `TZ=UTC`, and
`TERM=dumb`. Its exact ordered options are `--p-al`, `--manifest-blob`,
`--candidate-spec-blob`, `--candidate-qs-blob`, `--formal-spec-blob`,
`--formal-qs-blob`, `--output /tmp/tsdc-4al-terminal-task.md`, and
`--publication-output /tmp/tsdc-4al-terminal-publication.txt`.

The terminal publisher is launched from its own sealed descriptor with no
arguments as `/usr/bin/python3 -I -S -B /proc/self/fd/<sealed-fd>`, cwd `/`.
Its baseline environment is exactly `PATH=/usr/bin:/bin`, `HOME=/nonexistent`,
`XDG_CONFIG_HOME=/nonexistent`, `LC_ALL=C`, `LANG=C`, and `TZ=UTC`. Publish mode
adds only `TSDC_PUBLICATION_MANIFEST_BLOB`,
`TSDC_CANDIDATE_PATH=/tmp/tsdc-4al-terminal-task.md`,
`TSDC_CANDIDATE_SHA256`, `TSDC_CANDIDATE_BYTES`, and
`TSDC_REVIEWED_SCRIPT_SHA256`. `classify-terminal` mode instead adds only the
mode, exact recovery directory, and reviewed-script identity;
`resolve-terminal` mode adds only the mode, immutable publication-manifest blob,
and reviewed-script identity.

#### Construction and concurrency contract

P_AL publication and terminal publication share reviewed Git-object, raw-commit,
ref-CAS, index-lock, durability, and fail-closed primitives, but they use two
different state machines. P_AL publication consumes the already-edited Plan and
Task worktree bytes and never writes either worktree file. Terminal publication
must install the renderer's exact Task bytes and therefore uses the distinct
`tsdc-4al-terminal-publication/v2` state machine defined below; treating both as
one no-worktree-write transaction is prohibited. Both assets run hook-free and
configuration-bounded with system/global configuration disabled;
repository/local influences rejected or explicitly overridden; no ambient
`GIT_*`; explicit UTF-8, author/committer identity, timestamps, timezone
offsets, and exact message bytes; disabled signing; no replacement objects,
grafts, alternates, lazy fetch, filters, fsmonitor, attributes, text conversion,
external diff, pager, or hooks. Ordinary `git commit` is prohibited.

The builder copies the exact parent index to an owned temporary index, installs
only the reviewed blob OIDs with `git update-index --cacheinfo`, refreshes the
candidate index, proves both `git ls-files -v` and `git ls-files -f` have only
ordinary non-masking entries, writes the tree, and creates a single-parent
commit with `git commit-tree`. Before ref mutation it byte-compares the raw
commit object to an allowlist containing only the exact tree, sole parent,
author, committer, dates and offsets, blank line, subject plus final newline,
and no extra header such as `encoding`, `gpgsig`, or `mergetag`.

Before construction, capture the primary index byte hash/stat identity and the
complete tracked binary diff plus untracked-path state. Prebuild the candidate
index from the exact parent tree. Acquire the canonical `index.lock` with a
dedicated owned guard inode before the final pre-CAS recheck and hold that same
guard continuously across ref CAS and index reconciliation. The candidate
index is exposed through a distinct owned same-directory install inode and is
atomically moved to the primary index without ever vacating `index.lock`.
Publication uses `git update-ref --stdin` expected-old semantics with hooks
disabled. A CAS conflict or pre-CAS drift before ref advancement stops without
retry and removes owned state only after proving the branch, primary index,
complete binary diff, and untracked-path set remain exactly unchanged.

The P_AL builder never overwrites working-tree files. After CAS it rechecks the
complete tracked diff, untracked state, Plan/Task blobs, package, configuration,
and guard before atomically installing the prebuilt candidate index. If
reconciliation or a post-CAS check fails, it preserves user work, the original
index, the pre-proved commit, journal, and validated guard and reports
`index-reconciliation-required` with the recovery directory. Normal success
installs the candidate index, proves the committed state while guarded, releases
the index guard and ref-verification transaction, proves the same state with no
locks, removes only exact owned recovery residue, reproves the residue-free
state, and only then emits the P_AL result. External writes that bypass Git lock
discipline are outside the guarantee and make the final proof fail when
observed.

Before ref prepare, the P_AL transaction writes and durably persists an owned
`journal` inside its canonical Git-dir transaction directory. It uses a
same-filesystem temporary file, file `fsync`, atomic rename, and directory
`fsync` for every phase transition. The journal is exactly 19 LF-terminated
`key=value` lines with a final newline and no envelope:

```text
schema_version=1
branch_ref=refs/heads/feat/135-target-surface-delta-convergence
parent=40-lowercase-hex expected-old S_AL OID
new_commit=40-lowercase-hex pre-proved P_AL OID
original_index=canonical owned original-index path
original_sha256=64-lowercase-hex original-index digest
candidate_index=canonical owned candidate-index path
candidate_sha256=64-lowercase-hex candidate-index digest
index_lock=canonical linked-worktree index.lock path
lock_identity=decimal-device:decimal-inode of the dedicated guard
plan_blob=40-lowercase-hex Plan blob OID
task_blob=40-lowercase-hex Task blob OID
tree=40-lowercase-hex tree OID
package_sha256=64-lowercase-hex frozen diff digest
package_bytes=positive decimal frozen diff byte count
script_sha256=64-lowercase-hex reviewed transaction digest
author_epoch=positive decimal Unix epoch
raw_commit_sha256=64-lowercase-hex raw commit digest
phase=PREPARED|REF_ADVANCED|INDEX_INSTALLED
```

`PREPARED` is durable before `update-ref` prepare, `REF_ADVANCED` immediately
after the expected-old CAS, and `INDEX_INSTALLED` immediately after candidate
index installation. Recovery never trusts phase alone: a crash between CAS and
the phase rename is inferred from the journal's pre-proved `new_commit`, current
ref, original/candidate index hashes, dedicated guard inode, full retained diff,
untracked-path state, and exact Plan/Task worktree blobs. The current repository
uses SHA-1 object IDs, so this transaction requires 40-lowercase-hex Git OIDs;
the generic review-package envelope remains format-capable for 40- or 64-hex
object stores. Startup refuses a new transaction when any matching residue or
branch-ref lock exists and reports `recovery-required`.

The same frozen P_AL transaction asset exposes a read-only classifier mode. It
accepts exactly one canonical owned transaction directory, validates the closed
journal, paths, ownership, no-symlink boundary, hashes, inode relation, ref,
index, full retained binary diff, untracked-path set, branch-ref-lock absence,
and worktree identity, and prints exactly one value-free state:
`branch-unchanged`, `index-reconciliation-required`,
`complete-removal-safe`, or `foreign-drift`. Classification never mutates.
Cleanup may remove the directory only after normal complete proof or a proved
branch-unchanged/original-index state. Any other recovery action requires
explicit approval.

#### Distinct terminal publication contract

The terminal renderer writes exactly two private outputs: the selected Task
candidate at `/tmp/tsdc-4al-terminal-task.md` and a publication manifest at
`/tmp/tsdc-4al-terminal-publication.txt`. It materializes each once as a Git
blob and returns their OID, SHA256, and byte count. The publisher pins the Task
candidate with one no-follow file descriptor, verifies those exact bytes
against the immutable manifest, and never rereads the mutable pathname. The
publication manifest is LF-delimited, final-newline text with this exact field
order:

```text
BEGIN TSDC-4AL-TERMINAL-PUBLICATION
schema: tsdc-4al-terminal-publication/v2
branch_ref: refs/heads/feat/135-target-surface-delta-convergence
p_al: 40-lowercase-hex P_AL OID
plan_path: docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md
task_path: docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
plan_blob: 40-lowercase-hex P_AL Plan blob OID
expected_task_blob: 40-lowercase-hex P_AL Task blob OID
selected_terminal: B_AL|XP_AL
terminal_subject: exact selected terminal subject
new_task_blob: 40-lowercase-hex selected Task blob OID
new_task_sha256: 64-lowercase-hex selected Task digest
new_task_bytes: positive decimal selected Task byte count
package_blob: 40-lowercase-hex package blob OID
candidate_spec_assignment_blob: 40-lowercase-hex assignment blob OID
candidate_qs_assignment_blob: 40-lowercase-hex assignment blob OID
formal_spec_assignment_blob: 40-lowercase-hex assignment blob OID
formal_qs_assignment_blob: 40-lowercase-hex assignment blob OID
candidate_spec_review_blob: 40-lowercase-hex review blob OID
candidate_qs_review_blob: 40-lowercase-hex review blob OID
formal_spec_review_blob: 40-lowercase-hex review blob OID
formal_qs_review_blob: 40-lowercase-hex review blob OID
terminal_renderer_blob: 40-lowercase-hex renderer blob OID
terminal_publisher_blob: 40-lowercase-hex publisher blob OID
author_name: AI Agent
author_email: agent@example.com
author_epoch: positive decimal Unix epoch
author_offset: +0900
committer_name: AI Agent
committer_email: agent@example.com
committer_epoch: same exact author_epoch
committer_offset: +0900
END TSDC-4AL-TERMINAL-PUBLICATION
```

The publisher validates the manifest, v2 package, four assignment blobs, four
review blobs, renderer and publisher identities, P_AL topology, repository and
configuration, and the pinned candidate before mutation. The initial renderer
captures `time.time_ns() // 1_000_000_000` exactly once, validates it as a
positive decimal epoch, and embeds that same value in both manifest epoch
fields. It is not a caller-provided environment or CLI input. The publisher
parses that immutable manifest value, then its isolated bootstrap overrides
`time.time_ns()` to return exactly `author_epoch * 1_000_000_000` before
executing the package-bound renderer from a sealed immutable descriptor. The
replay uses two distinct inherited empty output descriptors, the exact
nine-key renderer environment, and the closed ordered renderer arguments. The
replayed Task bytes, publication bytes, Git object IDs, SHA256 values, byte
counts, and seven-line renderer stdout must exactly equal the supplied
candidate and manifest. This deterministic replay is an authenticity boundary,
not a later diagnostic. The publisher creates a private
transaction directory in the linked-worktree Git directory, proves that it and
the Task parent are on one filesystem, copies the current primary index, and
prebuilds a candidate index/tree/raw commit that changes only the mode-`100644`
Task entry while preserving the exact P_AL Plan blob. It refreshes the
candidate index, proves the candidate and live primary index have ordinary
non-masking flags, acquires one dedicated continuous `index.lock` guard, and
uses a separate same-directory install inode for the candidate index.

After acquiring the canonical primary-index lock, the publisher durably records
`PREPARED`, prepares expected-old `update-ref` without committing it, persists
`REF_PREPARED`, and reproves P_AL ref/index/Plan/Task/candidate identities. It
then performs the
only permitted worktree mutation with Linux `renameat2(..., RENAME_NOREPLACE)`:
move the exact P_AL Task to owned `task.old`, fsync both parent directories and
persist `TASK_DETACHED`; prove the displaced inode and bytes; move owned
`task.new` to the Task path, fsync both directories, and persist
`TASK_INSTALLED`. It never truncates a tracked file, never writes the Plan, and
never overwrites an occupied or divergent Task pathname.

Only after re-proving Task candidate, backup, Plan, candidate index, and current
P_AL ref may it commit the expected-old ref transaction, persist
`REF_ADVANCED`, install the candidate index, persist `INDEX_INSTALLED`, prove
the exact Task-only terminal and clean status under ref/index guards, persist
`COMPLETE`, and advance the exact journal to `OUTPUT_PENDING`. The publisher
first establishes a collision-safe external completion receipt in the
linked-worktree Git directory while the internal journal remains durable,
file-fsyncs the receipt, and fsyncs the Git directory. Only then may it remove
and fsync the internal journal, remove the empty transaction directory, and
retain the external receipt as the durable cleanup witness. The exact duplicate
journal-plus-receipt intermediate is valid only when both copies are
byte-identical and rebind every immutable input, renderer replay result,
selected terminal, raw commit/tree, installed index and flags, configuration,
and live Plan/Task identity. The receipt bytes are the same closed journal with
`phase: OUTPUT_PENDING`; it is removed only after a receipt-bound stateless
terminal proof. A second strict zero-residue stateless proof follows receipt
removal. A crash is
classified from the observed ref/index/path/inode/hash tuple rather than the
recorded phase alone. The read-only terminal classifier returns exactly one of
`branch-unchanged`, `task-detached`, `task-installed-ref-pending`,
`index-reconciliation-required`, `complete-removal-safe`, `ref-conflict`, or
`foreign-drift`. It never restores, resumes, removes, or overwrites anything;
every non-complete recovery mutation requires separate explicit approval.

The terminal journal is an LF-delimited, final-newline envelope with
`BEGIN TSDC-4AL-TERMINAL-TRANSACTION`, schema
`tsdc-4al-terminal-transaction/v2`, these exact ordered keys, and
`END TSDC-4AL-TERMINAL-TRANSACTION`:

```text
schema
branch_ref
p_al
new_commit
tree
selected_terminal
terminal_subject
plan_path
task_path
plan_blob
expected_task_blob
new_task_blob
new_task_sha256
new_task_bytes
manifest_blob
manifest_sha256
manifest_bytes
package_blob
candidate_spec_assignment_blob
candidate_qs_assignment_blob
formal_spec_assignment_blob
formal_qs_assignment_blob
candidate_spec_review_blob
candidate_qs_review_blob
formal_spec_review_blob
formal_qs_review_blob
terminal_renderer_blob
terminal_renderer_sha256
terminal_renderer_bytes
terminal_publisher_blob
renderer_replay_status
renderer_task_blob
renderer_task_sha256
renderer_task_bytes
renderer_publication_blob
renderer_publication_sha256
renderer_publication_bytes
renderer_stdout_sha256
renderer_stdout_bytes
transaction_dir
transaction_identity
original_index_path
original_index_sha256
original_index_bytes
original_index_identity
primary_index_original_identity
candidate_index_path
candidate_index_sha256
candidate_index_bytes
candidate_index_identity
install_index_path
install_index_sha256
install_index_bytes
install_index_identity
index_lock_path
index_lock_identity
index_flags_v_sha256
index_flags_v_bytes
index_flags_f_sha256
index_flags_f_bytes
branch_ref_lock_path
branch_ref_lock_sha256
branch_ref_lock_bytes
branch_ref_lock_identity
task_parent_path
task_parent_identity
plan_identity
original_task_identity
original_task_sha256
original_task_bytes
task_old_path
task_new_path
task_new_identity
config_identity
config_sha256
config_bytes
script_sha256
author_epoch
raw_commit_sha256
raw_commit_bytes
phase
```

`phase` is exactly one of `PREPARED`, `REF_PREPARED`, `TASK_DETACHED`,
`TASK_INSTALLED`, `REF_ADVANCED`, `INDEX_INSTALLED`, `COMPLETE`, or
`OUTPUT_PENDING`. The classifier accepts a `journal.next`, prepared branch-ref
lock, or external completion receipt only through its own closed identity and
phase-specific grammar. Missing or malformed terminal stdout is never authority
to retry: the controller invokes the sealed publisher in `resolve-terminal`
mode with the immutable publication-manifest blob. That stateless resolver
returns exactly `B_AL`, `XP_AL`, `branch-unchanged`, or `foreign-drift`. The Git
branch and proved zero-residue state are the durable receipt; stdout is only a
notification.

The following AL-1 through AL-7 steps are preserved as immutable historical
4AL execution design. They no longer grant current execution authority after
the P_AL review set selected XP_AL and terminal pre-publication proof failed
closed. Any remaining `P_AL current`, `reviews not started`, or `terminal none`
phrases in AL-1 through AL-7 describe the old P_AL pre-review state only; 4AM
must not treat them as current authority.

#### AL-1 — Freeze and prove the P_AL candidate

**Files:** modify only the Plan and Task paths named above. No test, validator,
controlled wrapper, pre-commit, runtime, remote, dependency, or Graphify command
is authorized.

- [ ] Start from clean S_AL and prove the exact branch, parent, subject
  cardinalities, modes, and empty lock/residue state:

```bash
test "$(git rev-parse HEAD)" = eafdaf0433d9e600abbc9b8e2443bdd7b84a9868
test "$(git rev-parse HEAD^)" = 2d2f49dfccb5fec282b2792fe0984d80327b4254
test "$(git rev-list --count 2d2f49dfccb5fec282b2792fe0984d80327b4254..HEAD)" = 1
test "$(git symbolic-ref -q HEAD)" = refs/heads/feat/135-target-surface-delta-convergence
test -z "$(git status --porcelain=v1 --untracked-files=all)"
subjects="$(git log --all --format=%s)"
test "$(awk '$0 == "docs(design): define atomic reviewed-blob successor" {n++} END {print n+0}' <<<"$subjects")" = 1
test "$(awk '$0 == "docs(plan): define atomic reviewed-blob terminal proof" {n++} END {print n+0}' <<<"$subjects")" = 0
test ! -e "$(git rev-parse --git-path index).lock"
```

- [ ] Update every `TSDC-AL-STATE` projection to P_AL current state: exact
  D_AL/S_AL, P_AL subject-resolvable with self OID unasserted, all four reviews
  not started, terminal none, and the exact prohibited-authority tuple.
- [ ] Confirm the only changed paths and modes, then capture the candidate once:

```bash
test "$(git diff --name-only)" = $'docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md\ndocs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md'
git diff --check
test "$(git ls-files -s -- docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md | cut -d' ' -f1)" = 100644
test "$(git ls-files -s -- docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md | cut -d' ' -f1)" = 100644
```

- [ ] Freeze the exact binary diff, Plan blob, Task blob, SHA256, byte counts,
  and transaction script identity. Any subsequent byte change invalidates the
  package and requires a new freeze from clean S_AL.

#### AL-2 — Publish P_AL with reviewed-blob plumbing

- [ ] Run static Bash syntax and ShellCheck only on the out-of-tree transaction
  asset. These checks validate the transaction asset; they are not repository
  validators, tests, or the QA wrapper.
- [ ] Launch the exact reviewed transaction bytes from a sealed immutable file
  descriptor. The transaction must implement the construction and concurrency
  contract above and use the exact subject
  `docs(plan): define atomic reviewed-blob terminal proof`.
- [ ] Before CAS, prove the candidate tree differs from S_AL at exactly the two
  allowed paths and that both entries equal the frozen reviewed blobs at mode
  `100644`.
- [ ] After CAS and index reconciliation, prove P_AL has sole parent S_AL,
  distance one, exact raw commit bytes, exact tree/path/mode/blob set, clean
  status, no index lock or transaction residue, one S_AL subject, one P_AL
  subject, and zero B_AL/XP_AL subjects.
- [ ] Keep P_AL's own Task evidence prospective and self-reference-free. The
  controller handoff reports the resolved P_AL OID and transaction output
  externally; the later selected terminal records those already-resolved facts.

#### AL-3 — Build the immutable P_AL review package

- [ ] Resolve P_AL by exact unique subject, then rebind its OID using exact
  parent S_AL, distance one, raw object, tree, paths, modes, and blobs.
- [ ] Create the exact deterministic LF-delimited v2 package shown above. It
  contains D_AL, S_AL, P_AL, both checkpoint subjects, Plan/Task modes and blob
  OIDs, raw commit and binary diff SHA256/bytes, all three reviewed runtime
  asset identities, both terminal subjects, the ordered projection-anchor
  digest, and the prohibited-authority tuple. The Plan/Task blobs bind the
  historical freezes; the package does not duplicate a projection list or
  historical-freeze fields.
- [ ] Hash and materialize the manifest once as a Git blob. Every reviewer must
  receive that manifest blob OID and retrieve its bytes through Git object
  access.

#### AL-4 — Run the candidate review pair

- [ ] Assign `C_AL_SPEC` and `C_AL_QS` directly to two distinct new read-only
  agents. Record their canonical identities and assignment source.
- [ ] Require both to inspect the immutable manifest, P_AL objects, both
  reviewed document blobs, every `TSDC-AL-STATE` projection, terminal selection
  rules, failure/recovery states, and the closed-world prohibition.
- [ ] Capture each exact report once with its required envelope and materialize
  it as a Git blob. Do not remediate P_AL in place; any Critical, Important, or
  Minor finding is an input to XP_AL.

#### AL-5 — Run the formal review pair

- [ ] Assign `F_AL_SPEC` and `F_AL_QS` directly to two new read-only agents whose
  canonical identities differ from one another and both candidate reviewers.
- [ ] Give both formal reviewers the immutable P_AL manifest and both candidate
  report blob OIDs. Require independent verification rather than acceptance of
  candidate conclusions by reference.
- [ ] Capture and materialize each exact formal report once. Prove the four
  identity records are pairwise distinct and every report rebinds the same
  P_AL package before selecting a terminal.

#### AL-6 — Produce exactly one terminal Task blob

- [ ] Select B_AL only under the complete acceptance predicate above. Select
  XP_AL only for a complete, hash-valid, parseable set that fails acceptance or
  proves an identity collision. Missing or malformed evidence stops without a
  terminal. Do not create a correction commit in the 4AL lineage.
- [ ] Starting from the immutable P_AL Task blob, update the state block, Work
  Breakdown, Planning Verification, Task Execution Evidence, Review Evidence,
  Commit Ledger, Deferred/Blocked, Approval Evidence, Work Log, atomic
  reviewed-blob Plan boundary, and final handoff in one candidate Task blob.
- [ ] Embed all four immutable review envelopes and their OID/hash/byte metadata.
  Add exactly one terminal Commit Ledger row and prove the alternative row is
  absent. Keep the exact prohibited-authority tuple in every current projection.
- [ ] Prove the terminal candidate differs from P_AL only at the Task path,
  whose mode remains `100644`; prove the Plan blob is byte-identical to P_AL.
- [ ] Write the exact Task candidate and
  `tsdc-4al-terminal-publication/v2` manifest to their fixed private paths,
  materialize each exactly once as a Git blob, and capture only this exact
  seven-line stdout envelope:

```text
TSDC_4AL_TERMINAL=B_AL|XP_AL
TSDC_4AL_TASK_SHA256=64-lowercase-hex digest
TSDC_4AL_TASK_BYTES=positive decimal byte count
TSDC_4AL_TASK_BLOB=40-lowercase-hex object OID
TSDC_4AL_PUBLICATION_SHA256=64-lowercase-hex digest
TSDC_4AL_PUBLICATION_BYTES=positive decimal byte count
TSDC_4AL_PUBLICATION_BLOB=40-lowercase-hex object OID
```

The terminal updater uses this projection matrix as a closed allowlist:

| Projection | P_AL value | B_AL value | XP_AL value |
| --- | --- | --- | --- |
| `TSDC-AL-STATE` | four reviews not started; terminal none | four accepted reports; B_AL selected; XP_AL absent | completed review set non-accepted; XP_AL selected; B_AL absent |
| Work Breakdown | Plan current; reviews not started | accepted Plan terminal; implementation still blocked | exhausted Plan terminal; no correction |
| Planning Verification | P_AL subject-resolvable; terminal absent | exact P_AL OID/package and B selection proof | exact P_AL OID/package and XP selection proof |
| Task Execution Evidence | no repository test/validator/wrapper action | same; review evidence only | same; review evidence only |
| Atomic reviewed-blob Plan boundary | P_AL current; reviews not started; terminal none | exact accepted review set and B_AL publication boundary | exact non-accepted review set and XP_AL exhaustion boundary |
| Review Evidence | four named slots not started | four immutable accepted envelopes | four immutable envelopes and non-acceptance cause |
| Commit Ledger | S_AL row plus P_AL row only | add exactly one B_AL row | add exactly one XP_AL row |
| Deferred/Blocked | four reviews then one terminal | separate user decision required; closed-world tuple remains | exhausted; closed-world tuple remains |
| Approval Evidence | 2026-08-02 P_AL/review/terminal-only approval | approval consumed only for B_AL evidence transaction | approval consumed only for XP_AL evidence transaction |
| Work Log | P_AL Plan-writing entry | append B_AL review/transaction entry | append XP_AL review/transaction entry |
| Final handoff | P_AL current; reviews not started | B_AL current; no implementation authority | XP_AL terminal; no correction/downstream authority |

No other active Task row, paragraph, or status phrase may retain a prior P_AL
state after the terminal transition.

#### AL-7 — Publish and prove B_AL or XP_AL atomically

- [ ] Launch the distinct reviewed terminal publisher from sealed immutable
  bytes with the immutable publication-manifest blob and one pinned no-follow
  candidate Task descriptor. Rebind the publisher/renderer/package/assignment/
  review OIDs before any mutation.
- [ ] Use P_AL as expected old ref and sole parent, preserve the immutable P_AL
  Plan blob, and apply the exact Task-path no-replace CAS, extended journal,
  primary-index/ref guards, raw-commit allowlist, and observed-state recovery
  classifier defined above.
- [ ] Prove exact topology `D_AL -> S_AL -> P_AL -> B_AL` or
  `D_AL -> S_AL -> P_AL -> XP_AL`, exactly one terminal subject and row, the
  other absent, Task-only diff, mode `100644`, clean status, and no residue.
- [ ] Treat the four-line publisher stdout as notification only. If it is
  missing, truncated, or not exact, run the same sealed publisher in
  `resolve-terminal` mode and accept only its closed stateless result; never
  retry publication from process status or output loss.

```text
TSDC_4AL_PUBLISHED=B_AL|XP_AL
TSDC_4AL_COMMIT=40-lowercase-hex selected terminal OID
TSDC_4AL_RECOVERY=none
TSDC_4AL_RESOLVER=resolve-terminal
```

- [ ] Stop at the terminal handoff. B_AL still requires a separate explicit user
  decision before any implementation successor; XP_AL is exhausted and grants
  no correction or downstream authority.

#### Failure and recovery matrix

| Failure point | Required state | Retry rule |
| --- | --- | --- |
| Candidate freeze or static transaction review fails | ref/index unchanged; discard only owned temporary artifacts | no automatic retry; repair and refreeze under the same user-approved Plan-writing scope |
| Pre-CAS identity, config, scope, raw-object, lock, or worktree proof fails before any Task-path mutation | ref/index/Task unchanged; user work preserved; exact owned P_AL state may be removed only after full unchanged-state proof | no automatic retry |
| P_AL ref CAS conflicts before advancement | competing ref retained; proved-owned P_AL state removed only after unchanged-state proof | no automatic retry; new approval/rebase analysis required |
| CAS succeeds but index reconciliation fails | new pre-proved commit retained; original index/user work preserved; `index-reconciliation-required` | explicit recovery approval required |
| P_AL process or power loss from durable PREPARED through INDEX_INSTALLED and lock/residue cleanup | startup refuses a new transaction; the four-state P_AL classifier reports one observed state | no automatic mutation; explicit recovery approval required unless state is proved `complete-removal-safe` |
| Terminal process or power loss from durable PREPARED through REF_PREPARED, TASK_DETACHED, TASK_INSTALLED, REF_ADVANCED, INDEX_INSTALLED, COMPLETE, OUTPUT_PENDING, destination-first receipt durability, duplicate journal/receipt, and stateless cleanup | journal/external-receipt classifier applies while durable residue exists; otherwise the exact canonical terminal branch is the durable receipt and the stateless resolver proves the terminal or returns `foreign-drift` | no retry from missing stdout or process status; explicit recovery approval unless exact zero-residue terminal state is proved |
| Review evidence missing, malformed, or mutable | no terminal commit | correct evidence collection only; never infer acceptance |
| Complete, hash-valid, parseable evidence proves a reviewer identity collision | XP_AL is the sole eligible terminal | no correction in 4AL; never infer acceptance |
| Any complete review is non-accepted | XP_AL is the sole eligible terminal | no correction in 4AL |
| Terminal pre-publication proof fails | P_AL ref/index/Task remain current | no automatic retry |
| Terminal Task detached before ref CAS | P_AL ref/index retained; exact old/new Task artifacts retained; classifier returns `task-detached` | explicit no-replace resume or rollback approval required |
| Terminal Task installed before ref CAS | P_AL ref/index retained; new Task and exact old backup retained; classifier returns `task-installed-ref-pending` | explicit resume or uncontested no-replace rollback approval required |
| Terminal ref advances before index install | selected terminal ref and Task retained; old index plus owned candidate lock retained; classifier returns `index-reconciliation-required` | explicit roll-forward index approval required |
| Terminal prepared ref conflicts or live ref differs from P_AL and the pre-proved terminal | unlike pre-advance P_AL CAS cleanup, all terminal Task/index/journal/ref-lock artifacts are retained; classifier returns `ref-conflict` | no mutation; new analysis and approval required |
| Terminal path, inode, hash, Plan, index, lock, or manifest differs | all artifacts retained; classifier returns `foreign-drift` | no mutation; new analysis and approval required |

#### P_AL completed and exhausted boundary

P_AL is exact commit `fb05e296b6a791f850cf64d99c7dc17577bb7cfc` and remains
the immutable D_AM predecessor. Its four completed reviews selected XP_AL, but
terminal pre-publication proof rejected the only rendered candidate before the
publisher ran. No B_AL/XP_AL commit exists, and 4AL has no retry or correction
authority. The new 4AM lineage must use fresh subjects, assets, review evidence,
and terminal identities.

### T-TSDC-004R-4AM — Projection-complete terminal correction design

> Historical non-executable boundary after S_AN: this section records the
> design that produced exact P_AM. The AM-2 asset pair was later rejected by
> quality/security at `C0/I3/M0`; AM-3 through AM-8 and B_AM/XP_AM are not
> authorized. Current authority is defined only by the 4AN section below.

4AM is the approved correction successor for the failed 4AL terminal
pre-publication proof. It starts from exact D_AM/P_AL
`fb05e296b6a791f850cf64d99c7dc17577bb7cfc` and must not retry, mutate, or
reinterpret the 4AL lineage. 4AL remains historical evidence: its package and
four reports selected XP_AL, but the single frozen renderer attempt retained
prior P_AL phrases in active Task projections, so no B_AL or XP_AL commit was
published.

The 4AM lineage is `D_AM -> S_AM -> P_AM -> B_AM|XP_AM`. S_AM is this
design-only correction checkpoint with exact subject
`docs(design): define projection-complete terminal successor`. P_AM is this
Plan+Task checkpoint with exact subject
`docs(plan): define projection-complete terminal correction proof`; its OID is
intentionally not self-asserted in its own tree. B_AM and
XP_AM are future mutually exclusive Task-only terminals. B_AM is selected only
when the new 4AM package, projection inventory, asset reviews, and four
P_AM-object reviews are all accepted. XP_AM is selected for a complete
non-accepted review set. Missing, malformed, mutable, or incomplete evidence
stops before terminal construction.

#### AM authority and non-reuse boundary

- S_AM may modify only this Plan and its paired Task, both mode `100644`.
- P_AM may modify only this Plan and its paired Task, both mode `100644`, and
  may freeze out-of-tree 4AM assets as reviewed evidence.
- B_AM or XP_AM may modify only the Task path as mode `100644`; the Plan blob
  must equal P_AM exactly.
- The old 4AL publisher, renderer, package builder, transaction, and anchor
  assets are not reusable execution authority. A 4AM asset may copy reviewed
  primitives only by creating a new byte identity, rebinding it into the P_AM
  package, and receiving fresh 4AM-specific specification and quality/security
  reviews.
- The 4AM terminal publisher must be newly rebound. The 4AL publisher was
  reviewed against 4AL manifest fields, fixed paths, renderer output, and
  projection assumptions; using it for 4AM would bypass the correction that
  makes projection completeness an explicit input.
- implementation, E_AL, R_AL, XE_AL, E_AM, R_AM, XE_AM, Task 4.5, Wave C,
  Tasks 5–6, runtime, remote/external actions, QA-wrapper/pre-commit execution,
  dependency changes, 4AL retry/correction, and Graphify update are blocked/no
  authority.

#### Closed-world projection inventory

P_AM must introduce a reviewed `TSDC-4AM-PROJECTION-INVENTORY` blob. The
inventory is a deterministic LF-delimited file, materialized as a Git blob and
bound by SHA256, byte count, and blob OID in the P_AM review package. It is not
an informal checklist. It must enumerate every active Task projection row,
paragraph, and status phrase that can mention the current checkpoint,
transaction state, review state, asset state, terminal selection, or prohibited
authority tuple.

Each inventory row must include:

- stable projection key;
- exact Markdown anchor or table name;
- exact selector for the source row or paragraph;
- expected D_AM/S_AM/P_AM value;
- expected B_AM value;
- expected XP_AM value;
- historical exception policy, limited to named 4AI/4AK/4AL history rows;
- stale-phrase denylist for that projection.

The inventory count is derived from the exact P_AM Task blob; it is never a
hand-maintained constant. At minimum, discovery must consider the approval
evidence, current-state marker, Work Breakdown, Work Log, Planning
Verification, Task Execution Evidence, 4AL and 4AM boundary sections, review
artifact insertion point, Review Evidence, whole-branch row, Commit Ledger,
Deferred/Blocked row, and final handoff. The builder must scan the entire Task
for 4AM namespace and current-state tokens, then prove a bijection: every
discovered active occurrence belongs to exactly one inventory row and every
inventory row matches exactly one active fragment. Uncovered, multiply covered,
or orphaned entries fail before a package or terminal manifest is emitted.

The projection denylist must include at least the phrases that caused 4AL to
fail: `current transaction execution remains not-run` and
`current transaction not run`. P_AM must also deny prior-current statements such
as `four P_AL reviews are not started`, `terminal none`, and `B_AL/XP_AL absent`
outside rows explicitly classified as historical 4AL evidence. A terminal
candidate is invalid if any inventory selector is missing, duplicated,
ambiguous, or leaves an undeclared prior-state phrase in an active projection.

The renderer must consume the inventory blob and build the terminal candidate
from the immutable P_AM Task blob. It may not rely on ad hoc string replacement,
a fixed row count, or a section-heading checklist alone. Rendering fails closed
unless every
inventory row is matched exactly once, every expected transition is applied,
the historical-exception rows remain intentionally historical, and a final
full-document stale-phrase scan proves no undeclared P_AM-prior state remains.
The renderer must emit preimage and candidate projection reports, each
materialized as a Git blob, with input and output line numbers, selector
SHA256, output SHA256, and stale-phrase counts for every AM-Pxx row. The
publisher must rebind those report blobs before any mutation.

#### 4AM package and review contract

The 4AM immutable package must bind:

- exact D_AM/P_AL and S_AM/P_AM subjects;
- P_AM OID resolved externally after publication by parent, subject, distance,
  raw commit, tree, path, mode, and blob proof;
- Plan and Task blob OIDs at mode `100644`;
- raw commit SHA256/bytes and binary `S_AM..P_AM` diff SHA256/bytes;
- fresh 4AM package-builder, renderer, terminal-publisher, and projection
  inventory identities;
- a separate terminal publication manifest schema version;
- the prohibited-authority tuple above.

The P_AM transaction must close the 4AL fsmonitor finding by proving both
`git ls-files -v` and `git ls-files -f` ordinary-entry views over the candidate
index and primary index. The proof must fail if fsmonitor-valid entries,
skip-worktree, assume-unchanged, intent-to-add, unmerged, sparse, or other
non-ordinary flags can make the candidate appear clean without being ordinary.

Exactly four fresh read-only 4AM review slots inspect the same immutable P_AM
package: `C_AM_SPEC`, `C_AM_QS`, `F_AM_SPEC`, and `F_AM_QS`. Their canonical
orchestrator-assigned identities must be pairwise distinct and must also differ
from the completed 4AL reviewer identities. Candidate reviews consume only the
P_AM package. Formal reviews consume the P_AM package plus both candidate
review blobs. Any reviewer-created edit or commit invalidates that review as
independence evidence.

#### 4AM terminal gates and recovery

Before terminal publication, the controller must prove the rendered candidate:

1. differs from P_AM only at the Task path;
2. preserves the P_AM Plan blob byte-for-byte;
3. updates every projection inventory row exactly once;
4. embeds all four immutable 4AM review envelopes and blob/hash/byte metadata;
5. contains exactly one B_AM or XP_AM Commit Ledger row and excludes the
   alternative subject and row;
6. has no undeclared stale P_AM, P_AL, B_AL, XP_AL, or 4AL-current phrases in
   active state surfaces;
7. keeps historical 4AI/4AK/4AL evidence as history rather than current
   authority.

The terminal publisher must use a fresh 4AM publication-manifest blob and a
pinned no-follow descriptor for the rendered Task candidate. It must perform a
Task-path no-replace CAS before the ref update, preserve the displaced exact
P_AM Task bytes, hold the primary index guard through Task install, ref CAS,
and index installation, and classify recovery from observed ref/index/path/
inode/hash tuples. The allowed classifier results are
`branch-unchanged`, `task-detached`, `task-installed-ref-pending`,
`index-reconciliation-required`, `complete-removal-safe`, `ref-conflict`, and
`foreign-drift`. Missing stdout, malformed stdout, power loss, or process loss
never authorizes a retry by itself; only a stateless resolver over the durable
Git state and receipt artifacts may prove the terminal.

#### AM design acceptance boundary

S_AM is exact commit `9eeb6365e4537de311f2bb46e80171c8719ef9c2`.
It authorizes this P_AM Plan/Task drafting checkpoint, but it does not authorize
running future assets, assigning the four terminal reviewers, creating
B_AM/XP_AM, running validators/tests/wrappers/pre-commit, updating Graphify, or
performing runtime/remote actions. P_AM must be published and its exact objects
must be rebound before the asset-freeze steps below begin.

### T-TSDC-004R-4AM — Executable projection-complete correction Plan

> Historical rejected checklist after S_AN: AM-1 completed at exact P_AM
> `143b5efe9b68d8688770b10c82fc3e4a9616bc66`; AM-2 completed with a
> non-accepted asset-review pair; AM-3 through AM-8 did not run. These
> checkboxes grant no current execution or retry authority.

P_AM is the Plan+Task checkpoint with exact subject
`docs(plan): define projection-complete terminal correction proof`. Its parent
must be exact S_AM `9eeb6365e4537de311f2bb46e80171c8719ef9c2`; its own OID is
resolved only after publication and is intentionally not self-asserted in its
tree. P_AM changes only this Plan and the paired Task, both mode `100644`.

P_AM authorizes only the planning-asset freeze, immutable review, terminal
construction, and Task-only publication sequence below.
implementation, E_AL, R_AL, XE_AL, E_AM, R_AM, XE_AM, Task 4.5, Wave C, Tasks 5–6, runtime, remote/external actions, QA-wrapper/pre-commit execution, dependency changes, 4AL retry/correction, and Graphify update are blocked/no authority.

#### AM-1 — Publish and rebind P_AM

**Files:**

- Modify:
  `docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md`
- Modify:
  `docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md`

- [ ] Prove HEAD is exact S_AM, both paths are the only changed tracked paths,
  both base and candidate modes are `100644`, and both `git ls-files -v` and
  `git ls-files -f` report ordinary entries for the two paths.
- [ ] Publish P_AM without invoking repository hooks. The raw single-parent
  commit must use the exact subject above, and expected-old ref CAS must name
  exact S_AM.
- [ ] Re-resolve P_AM by full parent, distance-one, exact unique subject, raw
  commit, tree, path, mode, and blob proof. Require a clean branch/index/
  worktree and repeat both `-v` and `-f` ordinary-entry proofs.
- [ ] Record the exact P_AM OID and Plan/Task blob OIDs outside P_AM's own tree
  before any planning asset is authored.

#### AM-2 — Build the closed-world projection inventory

**Planning assets:**

- Create: `/tmp/tsdc-4am-build-inventory.py`
- Generate: `/tmp/tsdc-4am-projection-inventory.jsonl`
- Generate: `/tmp/tsdc-4am-projection-preimage.txt`

- [ ] Assign one fresh implementation agent ownership of only the inventory
  builder and its generated outputs. The agent must not edit repository files
  and must not reuse a completed 4AL reviewer identity.
- [ ] Make the builder dependency-free and deterministic under absolute Python
  with `-I -S`, UTF-8, LF endings, final newlines, a closed environment, and an
  exact immutable P_AM Task input blob. Obtain repository input only from an
  exact Git blob object or from one single-open, no-follow, regular-file,
  bounded descriptor whose device, inode, byte count, SHA256, and Git blob OID
  are pinned before parsing; never hash and then reopen a mutable pathname.
- [ ] Emit one JSON object per projection with at least `schema`, `id`,
  `section`, `selector_kind`, `selector`, `class`, `source_sha256`,
  `expected_p_am`, `expected_b_am`, `expected_xp_am`,
  `historical_exception`, and `stale_denylist`.
- [ ] Scan the complete Task for current-state and 4AM namespace tokens. Every
  discovered occurrence must be covered by exactly one inventory object, and
  every inventory object must match exactly one source fragment. The derived
  count is output evidence, never a hard-coded acceptance constant.
- [ ] Cover at minimum approval evidence, `TSDC-AM-STATE`, Work Breakdown,
  Work Log, Planning Verification, Task Execution Evidence, 4AL and 4AM
  boundaries, the 4AM review-artifact insertion marker, Review Evidence,
  whole-branch status, Commit Ledger, Deferred/Blocked status, and final
  handoff. Treat both previously omitted asset-freeze rows as mandatory
  witnesses.
- [ ] Classify every covered occurrence as either terminal-transition or
  hash-preserved historical/static evidence. An exception must name its exact
  section and fragment hash; broad section, substring, or line-number-only
  exceptions are forbidden.
- [ ] Reject missing, duplicate, overlapping, uncovered, multiply-covered, or
  orphaned entries before writing a success report.
- [ ] Freeze builder, inventory, and preimage identities by SHA256, byte count,
  and Git blob OID. Reviewers must consume those exact Git objects or the same
  single-open pinned descriptors, not mutable `/tmp` pathnames. A distinct
  read-only specification reviewer and a distinct read-only quality/security
  reviewer must return `C0/I0/M0` before AM-3.

#### AM-3 — Build and review the projection-complete renderer source

**Planning assets:**

- Create: `/tmp/tsdc-4am-render-terminal.py`

- [ ] Assign a fresh implementation agent ownership of only the renderer
  source. The 4AL renderer may be read as historical evidence, but its byte
  identity, fixed row count, replacements, and authority must not be reused.
- [ ] Define a source-only renderer interface that will later accept only the
  exact P_AM Task blob, projection inventory, final package, and four immutable
  review-report blobs. Each input must arrive as an exact Git object or one
  single-open, no-follow, regular-file, bounded descriptor whose identity is
  pinned before parsing; mutable pathname reopen is forbidden.
- [ ] Validate all four review envelopes and pairwise-distinct canonical
  identities. Select B_AM only for four accepted `C0/I0/M0` verdicts with the
  required specification and quality/security flags; every complete
  non-accepted set selects XP_AM. Missing or malformed evidence stops without
  a candidate.
- [ ] Replay the inventory preimage proof against exact P_AM Task bytes, apply
  each terminal-transition entry exactly once, preserve every historical/
  static fragment hash, and insert all four immutable review envelopes only
  between the exact `TSDC-4AM-REVIEW-ARTIFACTS` markers.
- [ ] After rendering, rescan the full candidate. Require the same
  discovery-to-inventory bijection, the selected terminal state for every
  transition entry, zero undeclared prior-state phrases, and zero alternative
  terminal subject or ledger rows.
- [ ] Emit candidate and publication reports containing the derived inventory
  count, every input/output fragment hash, per-entry stale counts, Task blob/
  SHA256/bytes, selected subject, Plan blob equality, and exact prohibited
  authority tuple.
- [ ] Do not execute the renderer or generate a candidate, projection report,
  terminal Task, or publication manifest in this step. Freeze only the renderer
  source identity by SHA256, byte count, and Git blob OID. Distinct read-only
  specification and quality/security reviewers must consume that exact source
  object and return `C0/I0/M0` before AM-4.

#### AM-4 — Build and review the fresh terminal publisher, resolver, and launcher

**Planning assets:**

- Create: `/tmp/tsdc-4am-publish-terminal.py`
- Create: `/tmp/tsdc-4am-resolve-terminal.py`
- Create: `/tmp/tsdc-4am-sealed-launcher.py`

- [ ] Assign a fresh implementation agent ownership of these three assets.
  The 4AL publisher may contribute reviewed algorithmic primitives only through
  new bytes, complete 4AM rebinding, and fresh review.
- [ ] The launcher must verify its own and target asset identities, copy exact
  verified bytes to sealed descriptors, use a closed environment, and never
  hash then reopen a mutable pathname.
- [ ] The publisher must consume a pinned no-follow descriptor for the rendered
  Task and a fresh `tsdc-4am-terminal-publication/v1` manifest. The manifest
  distinguishes `expected_task_blob` from `new_task_blob` and binds every
  package, review, inventory, renderer, publisher, subject, author/committer,
  epoch, offset, path, mode, and object identity.
- [ ] Before any mutation, prove exact P_AM topology, Plan/Task bytes, primary
  index, clean tracked state, candidate bytes, same-filesystem transaction
  directory, and ordinary index state through both `git ls-files -v` and
  `git ls-files -f`. Reject skip-worktree, assume-unchanged, fsmonitor-valid,
  intent-to-add, unmerged, sparse, or any other non-ordinary state.
- [ ] Build the exact Task-only tree and raw single-parent commit, prove the
  Plan blob equals P_AM, and acquire the primary index guard plus expected-old
  ref lock before Task-path publication.
- [ ] Use no-replace Task detach/install CAS, preserve the displaced exact
  P_AM Task bytes, fsync both parent directories, update the ref only from exact
  P_AM, install the candidate index atomically, and prove clean final state.
- [ ] Persist journal states `PREPARED`, `REF_PREPARED`, `TASK_DETACHED`,
  `TASK_INSTALLED`, `REF_ADVANCED`, `INDEX_INSTALLED`, `COMPLETE`, and
  `OUTPUT_PENDING`. Resolver classification derives from observed ref/index/
  path/inode/hash state and returns only `branch-unchanged`, `task-detached`,
  `task-installed-ref-pending`, `index-reconciliation-required`,
  `complete-removal-safe`, `ref-conflict`, or `foreign-drift`.
- [ ] Missing stdout, malformed stdout, process loss, and power loss never
  authorize retry. Every non-complete recovery mutation requires a new explicit
  approval; only exact complete-removal-safe residue may be removed after proof.
- [ ] Freeze all three source identities by SHA256, byte count, and Git blob
  OID. Separate read-only specification and quality/security reviewers must
  consume the exact frozen source objects and return `C0/I0/M0` before AM-5.

#### AM-5 — Build and freeze the final immutable review package exactly once

**Planning assets:**

- Create: `/tmp/tsdc-4am-build-review-package.py`
- Generate once: `/tmp/tsdc-4am-review-package.txt`

- [ ] Assign a fresh implementation agent ownership of only the package-builder
  source. Do not reuse the 4AL package builder as executable authority.
- [ ] Make the builder accept only exact Git blob objects or single-open,
  no-follow, regular-file, bounded descriptors with pinned device, inode, byte
  count, SHA256, and Git blob OID. It must never treat a mutable pathname,
  hash-then-reopen result, or reviewer transcript as evidence.
- [ ] Bind exact D_AM/P_AL, S_AM, P_AM, branch ref, Plan/Task modes and blobs,
  raw P_AM commit SHA256/bytes, binary `S_AM..P_AM` diff SHA256/bytes, final
  reviewed inventory-builder/inventory/preimage identities, final reviewed
  renderer identity, all three final reviewed publisher/resolver/launcher
  identities, the final reviewed package-builder identity, manifest schema
  version, four review slots, and the exact prohibited-authority tuple.
- [ ] Use a closed LF-delimited grammar with unique keys, no duplicate fields,
  no mutable paths as evidence, and no self-asserted P_AM OID from P_AM's tree.
- [ ] Freeze and review the package-builder source before executing it. One
  read-only specification reviewer and one read-only quality/security reviewer,
  distinct from asset implementers and future `C_AM_*`/`F_AM_*` reviewers,
  must consume its exact Git blob and return `C0/I0/M0`.
- [ ] Execute the reviewed builder exactly once from the final reviewed asset
  identities, then freeze the resulting package by SHA256, byte count, and Git
  blob OID. Do not rebuild, patch, or replace this package downstream.

#### AM-6 — Run four immutable P_AM reviews over the one final package

- [ ] Resolve the AM-5 package by its exact Git blob OID, SHA256, and byte count.
  Reviewers must consume that Git object or the same single-open pinned
  descriptor; mutable-path-only evidence is invalid. Never rebuild the package.
- [ ] Assign four fresh, pairwise-distinct, read-only canonical identities:
  `C_AM_SPEC`, `C_AM_QS`, `F_AM_SPEC`, and `F_AM_QS`. They must differ from all
  completed 4AL identities and all 4AM asset implementers/reviewers.
- [ ] Candidate reviewers consume only the immutable P_AM package. Formal
  reviewers consume the same package plus both candidate report blobs. Every
  report binds assignment source, canonical identity, exact package identity,
  P_AM topology and document blobs, verdict, readiness, and findings.
- [ ] Materialize each exact LF-delimited report as a Git blob. A reviewer edit,
  commit, mutable-path-only report, identity collision, malformed envelope, or
  incomplete set stops before terminal construction.

#### AM-7 — Render and prove exactly one terminal candidate

- [ ] Invoke the sealed renderer exactly once only after all four immutable
  reports exist. Feed it only the exact pinned P_AM Task, inventory, AM-5
  package, and four report objects. Capture its selected terminal, candidate
  identity, projection/preimage reports, terminal Task, and publication
  manifest without executing the publisher.
- [ ] Independently prove the candidate is Task-only, preserves the P_AM Plan
  blob, contains all four exact review envelopes, satisfies the full-document
  discovery-to-inventory bijection, changes every transition entry exactly
  once, preserves every historical/static entry, contains the exact blocked
  tuple, and excludes the alternative terminal subject and ledger row.
- [ ] Any pre-publication failure leaves P_AM current and exhausts this 4AM
  attempt. Do not patch the candidate, rerun the renderer, infer acceptance, or
  invoke the publisher.

#### AM-8 — Publish B_AM or XP_AM once, or stop

- [ ] B_AM is eligible only when the four reports are complete, structurally
  valid, pairwise distinct, and fully accepted. Every complete non-accepted set
  makes XP_AM the sole eligible terminal.
- [ ] Invoke the sealed publisher exactly once only after AM-7 passes. Require
  expected-old P_AM ref CAS, Task-only tree diff, exact Plan equality, ordinary
  `-v` and `-f` index proofs, durable Task/index/ref convergence, clean status,
  and zero foreign residue before accepting success output.
- [ ] If stdout is missing or ambiguous, run only the read-only stateless
  resolver. Never retry from process status or stdout loss.
- [ ] Stop at B_AM or XP_AM. B_AM still needs a separate user decision before
  any implementation successor; XP_AM is exhausted and grants no correction or
  downstream authority.

#### 4AM failure matrix

| Failure point | Durable result | Next authority |
| --- | --- | --- |
| P_AM publication proof or expected-old CAS fails | S_AM remains current or observed foreign state is preserved | new analysis and approval; no automatic retry |
| Inventory discovery/bijection or either asset review fails | P_AM remains current; frozen rejected bytes remain evidence only | stop and return to design |
| Package or four-review evidence is missing, malformed, mutable, or identity-colliding | no terminal candidate | evidence correction only when it does not change frozen inputs; otherwise new design approval |
| Any complete review is non-accepted | XP_AM is sole eligible terminal | render XP_AM once only after the complete set is frozen |
| Terminal pre-publication proof fails | P_AM remains current; publisher not run | 4AM exhausted; no patch or rerender |
| Publisher stops before Task detach | P_AM ref/index/Task preserved | explicit recovery analysis; no automatic retry |
| Task detached or installed before ref CAS | exact old/new Task artifacts and P_AM ref/index preserved | explicit no-replace resume or rollback approval |
| Ref advances before index installation | selected terminal ref/Task plus old index and owned lock preserved | explicit roll-forward approval only |
| Ref conflict, foreign lock, path/inode/hash drift, or unclassified tuple | all evidence retained without mutation | new analysis and approval |
| Exact terminal is complete but stdout is lost | Git state and durable receipt are authoritative | read-only resolver only; never retry |

### T-TSDC-004R-4AN — Secure occurrence-bound inventory successor design

The 4AM AM-2 attempt is rejected at its asset-review gate. Its exact
specification review returned `C0/I0/M0`, but its independent quality/security
review returned `C0/I3/M0`, `QUALITY_SECURITY FAIL`, `AM2_COMPLETE NO`, and
`AM3_READY NO`. Under the 4AM failure matrix, exact P_AM
`143b5efe9b68d8688770b10c82fc3e4a9616bc66` remains the last executable Plan
checkpoint, AM-3 was not authorized, and the frozen rejected bytes are
historical evidence only:

- builder blob `b10244352953cff18cf2765e60ee29347efd9da1`, SHA256
  `a70978b3918b6cfd932271802d2ff7c3f79092e49ce4c2c220a6c10510b46401`,
  `38522` bytes;
- inventory blob `40b8cd68ce484a0b407ff11dad8096ec64b378b2`, SHA256
  `44c175f13e241d8b2a031bf977591a39cc227f2ed26360b48919763f6c881ae2`,
  `239305` bytes;
- preimage blob `548e8773e63e26f6c0fc230d49db105326563470`, SHA256
  `ce6f9abc8490a0e1870711e81e7caf9670002645246407747407a3f8402b10d0`,
  `24987` bytes.

The user approved this return-to-design successor on 2026-08-02. The new
planning-and-evidence lineage is
`D_AN/P_AM -> S_AN -> P_AN -> E_AN -> R_AN|XE_AN`. S_AN is the design-only
Plan-and-Task checkpoint with exact subject
`docs(design): define secure occurrence-bound inventory successor`. P_AN is a
future Plan-and-Task checkpoint with exact subject
`docs(plan): define secure occurrence-bound inventory proof`; its OID must not
be self-asserted in its own tree. E_AN is a required Task-only execution-gate
checkpoint with exact subject
`docs(task): record secure inventory Plan approval`; it alone may record the
resolved P_AN OID, the two accepted P_AN review identities and verdicts,
publication/rebinding proof, and the user's later AN-2 execution approval.
R_AN and XE_AN are mutually exclusive Task-only AN-2 evidence terminals with
exact subjects `docs(task): record accepted secure inventory evidence` and
`docs(task): record exhausted secure inventory evidence`. A future AN-3 design
must define any B_AN/XP_AN renderer terminals separately; P_AN does not create
or authorize them. No 4AN asset, review package, candidate, publisher, or
terminal exists in S_AN.

The first frozen P_AN candidate was reviewed but rejected before publication:
Plan SHA256/blob/bytes
`45f451a032905dab1da6f1db0ac760163e3ab4c4fa40264bc9d9233c63358d5f`/
`629926f1d0621ac9549c8262f17a95dc3c90e3bb`/`794477`, Task
`91ed61f6185938df9286fa6574bb531158c14f3faefd3628dcb54add60906450`/
`9da539cfae55be22ec5fad951db8d89e84e4b6a2`/`376297`, and binary diff
SHA256/bytes
`fd44e33ecedfefec00c5cbe8a039335d784ab1b1fef4b1d818cab3c37c378647`/
`94255`. Reviewer `/root/task4an_pan_plan_spec_r2_review` returned `C0/I5/M0`,
`SPEC_COMPLIANCE NO`, `PLAN_COMMIT_READY NO`; its fresh quality/security
reviewer `/root/task4an_pan_plan_security_r2_review` returned `C0/I4/M0`,
`QUALITY_SECURITY FAIL`, `PLAN_COMMIT_READY NO`.
Those reports are correction inputs only and can never approve a corrected
byte identity. The corrected candidate must be frozen and reviewed by a wholly
fresh pair before publication.

The rejected `/tmp/tsdc-4am-*` paths and their Git blobs must never be patched,
overwritten, reclassified as accepted, or executed again. New bytes use the
`tsdc-4an-*` namespace, new Git blob identities, a fresh implementer, and fresh
reviewers. implementation, E_AL, R_AL, XE_AL, E_AM, R_AM, XE_AM, Task 4.5,
Wave C, Tasks 5–6, runtime, remote/external actions,
QA-wrapper/pre-commit execution, dependency changes, 4AL/4AM retry or
correction, and Graphify update remain blocked/no authority. E_AN is
conditional on accepted corrected-P_AN reviews, exact publication/rebinding,
and a new explicit user execution approval. R_AN or XE_AN is conditional on
one authorized AN-2 attempt reaching a classified accepted or exhausted
outcome; neither exists or has current authority in this tree.

#### Private atomic output publication

The 4AN inventory builder must not publish to predictable shared `/tmp`
pathnames. P_AN binds the exact temporary parent path and its acceptance
contract. The reviewed 4AN controller opens that parent once with
`O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC`, proves its pinned device/inode, trusted
owner, directory type, and sticky-write policy, and creates one unpredictable
128-bit-name transaction directory relative to that descriptor. Creation uses
no-follow, create-only semantics and mode `0700`; the controller proves the new
directory is owned by the current effective UID, has initial link count two,
and is not group- or world-accessible before any child file is created.

Inventory, preimage, and receipt files are created relative to the transaction
directory descriptor with `O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC`, mode `0600`,
and no truncation path. Every opened descriptor is checked with `fstat` for
regular-file type, effective-UID ownership, link count one, expected device and
inode, and mode; `fchmod(0600)` is applied before writing. The builder writes,
rewinds, rereads, hashes, and length-checks through the same descriptor, then
fsyncs the file. It never hashes and reopens a pathname.

After both payloads are independently proved, the controller materializes
their exact bytes as Git blobs from pinned descriptors under the closed Git
environment below. A deterministic pair receipt binds schema, exact P_AN Task
blob, inventory and preimage SHA256/blob/byte identities, builder identity, and
completion state; the unpredictable directory name is never receipt content.
The receipt is written and fsynced last, materialized as an exact Git blob from
the same pinned descriptor, and followed by a transaction-directory fsync.
Only a complete receipt Git object whose two payload identities revalidate is
review authority. A crash,
partial pair, missing fsync, pre-existing path, hardlink, symlink, ownership
mismatch, permission mismatch, or receipt mismatch is non-accepting. Cleanup
may remove only a proved-owned unchanged transaction directory after an
explicit disposition; it may never follow links or touch the rejected 4AM
paths.

The build/source transaction and the production-output transaction are
different children of the same pinned parent. The bounded governance
orchestrator creates only the build/source child before the reviewed controller
exists; the reviewed controller later creates only the production-output child
after `HARNESS_ACCEPTED`. Each actor performs its own separate complete
16-byte `getrandom(2)` read; interruption, short read, all-zero policy failure,
encoding failure, or `EEXIST` is terminal and is never retried with a second
name. The build/source basename is exactly
`tsdc-4an-` plus 32 lowercase hexadecimal characters. The production-output
basename is exactly `tsdc-4an-out-` plus a different 32 lowercase hexadecimal
string. Each is created relative to `PARENT_FD` with `mkdirat(..., 0700)`,
captured with `fstatat(..., AT_SYMLINK_NOFOLLOW)`, then opened exactly once
with `openat2(PARENT_FD, name,
{O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC,
RESOLVE_BENEATH|RESOLVE_NO_SYMLINKS|RESOLVE_NO_MAGICLINKS|RESOLVE_NO_XDEV})`.
The opened descriptor identity must equal the captured identity.
`TX_FD` and `OUT_FD` must have the pinned parent's device, distinct new inodes,
effective-UID/effective-GID ownership, exact mode `0700`, link count two before
their first child, and zero group/world permission bits. Neither basename nor
pathname crosses an executable interface or enters a receipt. The orchestrator
passes the already-open `PARENT_FD` and `TX_FD` as bootstrap capabilities, and
the controller independently reproves both before accepting any input. The
controller creates and owns `OUT_FD`; the builder receives only the already-open directory
identity indirectly. The controller creates the two payload files itself and
passes only their already-open regular FDs in the builder's fixed output slots;
the builder never receives `PARENT_FD`, `TX_FD`, or `OUT_FD` and cannot open,
rename, remove, or rediscover the parent or either child pathname.

#### Closed and bounded Git-object reader

Every production Git subprocess is created only by the reviewed controller;
the isolated harness creates only the reviewed fake-Git server. Each child has an
absolute executable, a fixed repository, a closed environment, C locale, UTC,
and fixed timeout. The environment sets
`GIT_NO_REPLACE_OBJECTS=1`,
`GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0`, and
`GIT_CONFIG_NOSYSTEM=1`; `GIT_CONFIG_COUNT=0`, system/global configuration,
HOME/XDG, TMPDIR, and `PATH=/nonexistent` are fixed by the private view below.
Commands also use `--no-replace-objects`.
Every ambient `GIT_*` variable not explicitly admitted below is absent. The
reader requires both repository `objects/info/alternates` and
`objects/info/http-alternates` to be absent, not merely empty, before reading.
No credential, proxy, replace-ref, hook, fsmonitor, pager, editor, or prompt
input is inherited.

Production repository local/worktree configuration is never a Git input. The
controller gives each Git child a private bare control directory under
`TX_FD` whose exact `config` bytes are
`[core]\n\trepositoryformatversion = 0\n\tbare = true\n`. It is a
controller-created mode-`0600` regular file opened once, byte-reproved, and
watched together with its parent for every write/attribute/create/move/delete
event. The control directory also has exact mode-`0600` `HEAD` bytes
`ref: refs/heads/tsdc-4an-void\n`, an empty mode-`0700` `refs/heads`
directory, no `config.worktree`, no `commondir`, and no object or alternate
path. `GIT_DIR` is exactly `/proc/self/fd/<CONTROL_GIT_FD>` for the once-opened
control-directory descriptor, `GIT_CONFIG_SYSTEM=/dev/null`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and
`GIT_OBJECT_DIRECTORY` is exactly
`/proc/self/fd/<OBJECTS_FD>`, where `OBJECTS_FD` is the inherited read-only
once-opened production object-directory descriptor. The exact descriptor
number is fixed by the runtime manifest and is non-CLOEXEC only for that Git
child; all other descriptors are closed before exec. `GIT_COMMON_DIR`,
production local/worktree config paths, `include` sources, remote/promisor
configuration, and filters are therefore unreachable.
`GIT_ALTERNATE_OBJECT_DIRECTORIES` is absent. Because the private config has no
partial-clone/promisor declaration, a missing object is a local failure and no
Git version-specific lazy-fetch switch is relied upon.

When `info` exists, both alternate files must be absent under the pinned
`INFO_FD`, and the controller watches that descriptor plus `OBJECTS_FD`; if it is
absent, it watches `OBJECTS_FD` and rejects any creation or replacement of
`info`. The controller keeps the private `CONTROL_GIT_FD`, `CONFIG_FD`,
`OBJECTS_FD`, and any `INFO_FD` open, installs nonblocking inotify watches
before the first object read for write, attrib, create, delete, move,
self-delete, self-move, ignored, and queue-overflow events, and records the
private control/config identities/SHA256 plus both absence witnesses. Any
control-parent/config event, any `INFO_FD` event, any `OBJECTS_FD` event whose
name is exact `info`, watch failure/invalidation/overflow,
pathname/descriptor divergence, or pre/post identity/hash/absence difference
rejects the attempt even if bytes are later restored. Direct object-fanout
events are not alternate evidence: during materialization they must match the
controller's separately expected object-write ledger, and at all other phases
they are recorded but acceptance still depends on exact requested-object
reproof. The controller drains
and rechecks the watches and all identities after every Git child and
immediately before accepting each payload or receipt object. The case set
contains explicit private-control/config mutation and either-alternate
create/replace races;
a single precheck is never sufficient.

Before reading content, the reader performs a bounded exact-object metadata
probe and requires the requested full OID, object type `blob`, and the frozen
byte count. Content is then streamed once from `git cat-file blob <full-oid>`
through nonblocking pipes. The reader stores at most `expected_bytes + 1` of
stdout and a fixed bounded stderr diagnostic, enforces a monotonic deadline,
kills and reaps on overflow or timeout, rejects short and extra content, and
computes SHA256 plus Git blob OID while streaming. A missing local object,
replacement attempt, lazy-fetch request, prompt, config expansion, stderr
overflow, timeout, signal, nonzero exit, or identity mismatch fails before any
output publication or object-store write.

Production Git-object publication is implemented by the reviewed controller's
descriptor-fed loose-object materializer, not by a pathname-fed shell or an
unbounded `git hash-object` call. Its input is one already-rewound regular
payload FD plus the pinned `OBJECTS_FD`; it computes canonical
`blob <decimal-byte-count>\0<payload>` bytes, SHA-1 OID, SHA256, and zlib stream
under the fixed caps while rereading only that FD. Compression uses exact
`deflateInit2(Z_DEFAULT_COMPRESSION, Z_DEFLATED, MAX_WBITS, 8,
Z_DEFAULT_STRATEGY)` and the pinned `libz.a` identity. It opens or creates the
two-hex fanout directory relative to `OBJECTS_FD` with no-follow checks and
requires a same-device directory owned by the effective UID with no
group/world write bit. For a new object it performs one complete independent
16-byte `getrandom` read and creates exactly one same-directory basename
`.tsdc-4an-object-` plus 32 lowercase hex with
`O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC`, mode `0444`; short read, all-zero
policy failure, encoding failure, or collision is terminal with no second
name. It writes the complete compressed stream, rereads and validates it,
fsyncs it, and publishes with
`renameat2(..., RENAME_NOREPLACE)`. It then fsyncs the final object descriptor,
fanout directory, and `OBJECTS_FD` in that order. An `EEXIST` final object is
accepted only after the once-opened existing regular descriptor is boundedly
inflated and proves exact type, length, SHA-1, SHA256, owner, link count, and
non-writable mode; it is never replaced or truncated. Any temporary residue is
preserved on an ambiguous failure and no Git object is deleted. After an
`EEXIST` final object is fully accepted, the controller may unlink only the
still-open random temporary file after re-proving its exact name/device/inode/
owner/link-count tuple, then fsync the fanout directory again. An unlink or
fsync ambiguity is non-accepting and preserves the observed residue; it never
authorizes a second materialization attempt.

Inventory and preimage objects are materialized and durably reproved first.
The controller then drains the config/alternates watches, revalidates both
payload object descriptors and fanout-directory fsync receipts, constructs the
pair receipt from those exact identities, and only then creates, fsyncs,
publishes, and reproves the receipt object through the retained published FD or
the one pinned existing-object FD by the same algorithm. The receipt
cannot reach `completion=COMPLETE` unless both payload objects are already
durable. Object receipt records separate logical prestate (`absent` or
`present`) and loose publication state (`created-new-loose` or
`verified-existing-loose`) for each payload OID plus final
object/fanout/object-directory descriptor identities and fsync success. A
logically present packed object with no loose file is `present` plus
`created-new-loose`, never falsely new at the logical layer. The later
production-run evidence records the pair-receipt
object by the same fields. Stdout text or a returned OID alone is never
durability evidence.

#### Occurrence- and subspan-bound inventory schema

P_AN must define `tsdc-4an-projection-inventory/v2`. Each JSONL projection
object binds one exact source fragment by section, selector kind, selector,
fragment SHA256, and byte length, then partitions the complete fragment into
ordered, contiguous, non-overlapping byte subspans. There are no gaps, overlaps,
negative offsets, out-of-range offsets, or line-number-only selectors.

Every subspan has a stable ID, byte start/end, class
`terminal-transition`, `historical`, or `static`, source SHA256, occurrence
IDs, typed P_AN/B_AN/XP_AN expectations, exact historical exception when
applicable, and its own stale denylist. Every discovered namespace or
current-state occurrence is wholly contained by exactly one subspan and repeats
that subspan's class. Every occurrence belongs to exactly one fragment, every
fragment belongs to exactly one projection object, and every byte of every
selected fragment belongs to exactly one subspan.

Historical and static subspans are hash-preserved into both terminal
alternatives. Only terminal-transition subspans may change, and each must
produce exactly its selected typed value once. A mixed fragment must be split;
in particular, the rejected inventory's `AM-P043` source block must preserve
its immutable 4AL P_AL/package/candidate/no-terminal history as exact hashed
subspans while changing only its active 4AN/current-authority subspans. A
renderer that changes, drops, merges, or reclassifies a preserved subspan must
fail even when its fragment-level selector still matches.

Full-document discovery remains count-derived from the exact P_AN Task blob.
The builder rejects missing, duplicate, overlapping, uncovered,
multiply-covered, orphaned, ambiguously classified, or mixed-without-split
occurrences. It emits a deterministic preimage containing the fragment,
subspan, and occurrence bijection plus aggregate counts; none of those counts
is a hand-maintained acceptance constant.

Discovery is not implementer-selected. The policy manifest contains one
canonical `tsdc-4an-discovery-rules/v1` section, and the inventory core contains
the byte-identical compiled table; the builder request carries
`discovery_rules_sha256`, and the core serializes its table and rejects a hash
mismatch before scanning. The first whole-Task pass scans raw bytes, including
tables, fences, comments, and historical sections, for exact identifier-bound
tokens `D_AN`, `S_AN`, `P_AN`, `E_AN`, `R_AN`, `XE_AN`, `B_AN`, `XP_AN`,
`AN-1`, `AN-1E`, `AN-2`, `AN-2A` through `AN-2G`, and `AN-3`, plus the exact
four 4AN commit subjects defined by this Plan. Identifier tokens are bounded
on both sides by start/end or a byte outside ASCII `[A-Za-z0-9_]`, so `P_AN`
inside `XP_AN` or `P_AN_SELF_OID` is not a second seed.

The deterministic Markdown byte parser maps every seed to exactly one smallest
complete owning table row, list item, fenced block, marker block, or heading
range under the fixed precedence encoded in the same rules. A second pass over
that selected-fragment union records every exact state token, commit subject,
full 40-hex OID, and identifier-bounded authority/status token from the closed
rules table. No line-number, renderer output, source-code self-discovery, or
manual include/exclude list can add or suppress an occurrence. An unmapped
seed, structurally ambiguous owner, overlapping owner without the deterministic
merge rule, or policy/core serialization difference is fatal.

The v2 machine grammar is closed. Each inventory line is UTF-8 JSON followed
by one LF, has no BOM or insignificant whitespace, and uses shortest canonical
decimal integers with no sign or leading zero except `0`. Object keys appear
in the exact order below; arrays retain semantic order. Strings use valid
shortest UTF-8 and JSON escapes only for quotation mark, reverse solidus, and
U+0000 through U+001F; solidus and non-ASCII code points are never escaped.
Duplicate/unknown/missing keys, floats, exponent notation, invalid UTF-8,
noncanonical escape spellings, CR, or a missing/final extra LF reject the
inventory.

The Task and every semantic identifier input must contain no NUL. Every field
rendered as one token in the ASCII preimage must also contain no ASCII control
or whitespace byte outside the literal delimiters admitted below. All offsets,
byte counts, and derived
counts are checked unsigned 64-bit values, and every addition/subtraction/
multiplication is overflow-checked before use. Task/fixture input is capped at
`2097152` bytes, one inventory JSON line at `1048576` bytes, each complete
inventory and preimage at `16777216` bytes, and each projection/subspan/
occurrence count at `1000000`; hitting an overflow sentinel or exceeding a cap
fails before receipt creation.

Each top-level object has exact ordered keys `schema`, `projection_id`,
`task_blob`, `section`, `selector_kind`, `selector`, `fragment_start`,
`fragment_end`, `fragment_sha256`, `fragment_bytes`, and `subspans`.
`schema` is literal `tsdc-4an-projection-inventory/v2`; `task_blob` is the
exact 40-lowercase-hex P_AN Task blob. `selector_kind` is one of
`html-marker-range`, `heading-range`, `table-row`, or `literal-range` and its
selector is a unique byte-exact UTF-8 selector, never a line number.
`fragment_start` and `fragment_end` are zero-based half-open absolute byte
offsets in the Task blob and `fragment_bytes=end-start`.

Each `subspans` member has exact ordered keys `subspan_id`, `start`, `end`,
`class`, `sha256`, `occurrences`, `pan`, `ban`, `xpan`,
`historical_exception`, and `stale_denylist`. Its offsets are also absolute
half-open Task-blob byte offsets. Each `occurrences` member has exact ordered
keys `occurrence_id`, `kind`, `start`, `end`, and `sha256`; occurrence offsets
are absolute and wholly contained by the owning subspan. `kind` is one of
`namespace`, `current-state`, `authority`, `asset`, `review`, or `terminal`.
Every `pan`/`ban`/`xpan` expectation has exact ordered keys `kind`,
`value_utf8`, `value_sha256`, and `value_bytes`. `kind` is `exact`, `absent`,
or `preserve`; `absent` uses the empty value, zero bytes, and the SHA256 of
empty bytes, while `preserve` uses an empty `value_utf8` plus the exact source
subspan SHA256/length. `historical_exception` has exact ordered keys `kind`
and `evidence`; `kind=none` requires empty evidence and `kind=exact` requires
one nonempty stable evidence ID. Each stale-denylist member has ordered keys
`value_utf8`, `sha256`, and `bytes`, and members are sorted by raw UTF-8 bytes.

Stable IDs are full lowercase SHA256, never truncated. `projection_id` is
`anp-` plus SHA256 of the NUL-delimited bytes
`projection`, task blob, selector kind, selector, canonical decimal
fragment-start, and fragment-end. `subspan_id` is `ans-` plus SHA256 of
`subspan`, projection ID, canonical decimal start/end, class, and subspan
SHA256. `occurrence_id` is `ano-` plus SHA256 of `occurrence`, subspan ID,
kind, canonical decimal start/end, and occurrence SHA256. Each literal token
above is UTF-8, every field is followed by one NUL including the last, and any
ID collision or recomputation mismatch is fatal. Projection lines are sorted
by `(fragment_start, fragment_end, projection_id)`; subspans and occurrences
are sorted analogously by `(start, end, id)`.

The preimage grammar is ASCII LF text with schema
`tsdc-4an-projection-preimage/v2`. It begins with unique ordered header fields
`schema`, `pan_task_blob`, `task_sha256`, `task_bytes`, `inventory_blob`,
`inventory_sha256`, and `inventory_bytes`, each encoded as
`<key> <value>\n`. The three record productions are exactly:

```text
P <projection_id> <start> <end> <fragment_sha256> <subspan_count> <occurrence_count>\n
S <projection_id> <subspan_id> <start> <end> <class> <sha256> <occurrence_count>\n
O <projection_id> <subspan_id> <occurrence_id> <kind> <start> <end> <sha256>\n
```

The angle-bracket tokens are replaced by one token each; every rendered record
contains no line break until its shown final `\n`. Record order exactly matches
inventory order. It ends with unique
ordered derived fields `projection_count`, `fragment_bytes_total`,
`subspan_count`, `occurrence_count`, `terminal_transition_count`,
`historical_count`, `static_count`, and `completion COMPLETE`. Tokens are
single-space separated; IDs/hashes are lowercase hex and numbers use the same
canonical decimal grammar. Counts and totals are recomputed from records and
the exact Task bytes, never trusted from the inventory.

#### OS-enforced fake-only harness containment

P_AN must bind a new exact controller source, containment-launcher source,
reproducible build provenance, static executables, and policy alongside the
builder and adversarial harness. Source-only authority is forbidden. Every
executable must be one
self-contained static ELF for the P_AN-bound architecture: no shebang,
`PT_INTERP`, external `DT_NEEDED`, `RPATH`/`RUNPATH`, environment-selected
loader, writable-executable segment, or executable stack. Its entry point,
program headers, machine/type, build receipt, source-to-binary correspondence,
Git blob, SHA256, byte length, and mode are exact review inputs.

Every reference below to “the controller” means only the reviewed
`tsdc-4an-controller` static PIE whose source, binary, build identity, fixed
interfaces, and source-to-binary correspondence are in the same source package
and both source reviews. It owns the parent/TX/OUT descriptors, immutable
input opening, launcher sealed-memfd construction, bounded child capture,
preflight-plus-case aggregation, production gate, exactly-once builder
invocation, config/alternates watches, descriptor-fed object materialization,
receipt-last durability, and terminal classification. No shell, agent prose,
Python interpreter, mutable helper pathname, or unspecified “already-running
controller” may perform one of those duties. The governance process may only
start that exact controller once by its pinned reviewed ELF descriptor with
the P_AN-bound argv/env/FD map; a different starter or controller identity is
non-accepting.

The separate term “governance orchestrator” means only the root Subagent-Driven
session that bootstraps reviewable out-of-tree inputs before that executable
exists. Its write authority is confined to one proved-owned `TX_FD` beneath
the ignored repo-support parent. It may author candidate sources/manifests, run
the exact reproducible build commands, freeze isolated review objects, copy
the exact returned reviewer bytes into sealed transfer memfds, construct the
non-authoritative controller request, and start the reviewed controller once.
It may perform only the bounded read-only topology/object rebind needed to
freeze exact P_AN/E_AN planning inputs; it may not write the production Git
object store, expose a production descriptor or pathname to a candidate asset,
create `OUT_FD`, execute a candidate asset before its required review, modify a
tracked repository file, or decide acceptance from its own assertions. Every
orchestrator-produced byte and descriptor is independently rebound by source
review and then by the static controller; a mismatch stops before harness or
production access. This explicit bootstrap boundary prevents the impossible
claim that the controller binary creates or reviews its own source and build.

The reviewed controller pins and hash-reproves the exact launcher ELF
through one no-follow descriptor, copies the same bytes into a memfd sealed
against write, grow, shrink, and further seal changes, rereads and rehashes the
sealed bytes, then invokes it directly with `execveat(..., AT_EMPTY_PATH)`.
The kernel therefore runs no interpreter, dynamic loader, shared library,
startup file, or mutable host pathname before the containment launcher. The
controller supplies the P_AN-bound bootstrap argv and a newly constructed
empty or exact-minimal bootstrap environment; it never forwards its own argv,
environment, cwd, descriptor, signal, or startup state. Any ELF-policy,
provenance, seal, identity, or direct-exec mismatch stops before launcher
execution.

The reviewed static launcher is the only component that may prepare the
harness process. Before any untrusted harness instruction runs, it creates a
private mode-`0700` sandbox transaction and enters dedicated user, mount, PID,
IPC, UTS, and network namespaces. It makes mount propagation private,
constructs a new tmpfs-backed root, and copies through pinned no-follow
descriptors only the exact reviewed fake-Git executable and path-free
case/policy/environment payloads listed by the P_AN-bound runtime manifest.
The bootstrap runtime manifest itself is consumed and closed, never copied
into the new root. It constructs every fake fixture from that manifest's
complete canonical fixture-byte map and the reviewed linked fixture generator;
no separate fixture pathname or undeclared input exists. The harness is already linked into the
launcher image and is not copied or executed as a separate file. Every runtime file is
individually pinned and hash/size/mode-proved through one descriptor, copied
from that descriptor into the tmpfs root, reread and hash-reproved there, then
placed on a read-only runtime subtree. Host-file and directory-wide runtime
binds are forbidden. Fixture inputs are regular manifest/blob descriptors;
the launcher constructs every required symlink, hardlink, collision, and mode
witness anew inside the tmpfs fake-work tree and never imports or follows a
host link. A separate fake-work subtree is the only writable
filesystem surface. The launcher then `pivot_root`s into the new root, changes
directory to `/`, detaches the old root, and proves no cwd, root, mount, or
descriptor reference retains it. The production worktree, canonical
Task, common Git directory and object store, user home, host temporary
directory, credentials, and host `/proc`, `/sys`, and device tree are not
mounted into the sandbox.

The launcher closes and unshares the inherited descriptor table before the
harness activation. Let `G` be the count of case-manifest rows whose domain is
exact `git-reader`; the frozen P_AN manifest derives `G=13`. Only read-only
null stdin `0`, ledger stdout `1`, bounded diagnostic stderr `2`, the read-only
sealed AN-C015 proof `3`, and the following manifest-derived table may remain.
For zero-based git-reader case ordinal `j`, worker role `r` is ordered
negative-metadata, negative-content, positive-metadata, positive-content and
has base FD `b=4+16j+4r`; harness-side request-write/stdout-read/stderr-read/
pidfd are `b/b+1/b+2/b+3`. Every pipe comes from
`pipe2(O_CLOEXEC|O_NONBLOCK)` and every
worker from `clone3(CLONE_PIDFD)` before the final filter. Each entry is mapped
once after direction/type/inode and pidfd/PID reproof. No pipe or pidfd resolves
to a production path or object store, and FD `3` contains no production
pathname.
After root construction and irreversible privilege drop but before worker
creation, it installs `no_new_privs` and a Landlock allowlist confined to the
sandbox root. After every worker readiness proof and all five sacrificial
denials, it installs the fixed default-deny seccomp allowlist containing only
the P_AN-bound same-image harness syscalls.
Landlock grants read/execute only to the proved runtime subtree and grants
write/create/remove only inside the fake-work subtree. The bounded ledger,
worker pipes, and pidfds are pre-opened protocol descriptors, not filesystem
authority.
The seccomp policy
therefore denies socket creation, mount or namespace manipulation, `setns`,
`chroot`/`pivot_root`, handle-based filesystem access, ptrace and cross-process
memory access, kernel keyring/BPF/performance interfaces, `io_uring`, and every
unlisted escape primitive. The sandbox contains the reviewed fake Git only;
the production Git executable and repository configuration are unreachable.
If any namespace, mount, Landlock, seccomp, descriptor-closing, or privilege
primitive is unavailable, the launcher fails before harness activation. There is no
weaker fallback.

The parent writes `deny` to `/proc/<child>/setgroups` before the one-line maps
`65532 <outer-euid> 1` and `65532 <outer-egid> 1`. Because that denial makes a
later `setgroups` permanently invalid, the child never claims to clear its
inherited supplementary list. Instead it proves every inherited group is
either the mapped primary GID `65532` or the namespace overflow GID `65534`,
that no second outside GID is mapped, and that no retained old-root/host FD or
mount can turn an overflow group into authority. Any other mapped
supplementary group fails before mount construction.

After UID/GID maps and all mount/root construction are complete but before any
harness activation, the launcher performs one exact irreversible privilege
sequence while it still has the namespace capabilities needed for the drop.
It first clears the ambient set and locks exact securebits
`SECBIT_NOROOT|SECBIT_NOROOT_LOCKED|SECBIT_NO_SETUID_FIXUP|
SECBIT_NO_SETUID_FIXUP_LOCKED|SECBIT_KEEP_CAPS_LOCKED|
SECBIT_NO_CAP_AMBIENT_RAISE|SECBIT_NO_CAP_AMBIENT_RAISE_LOCKED`. It then drops
every capability from zero through the pinned pre-pivot `cap_last_cap` value
from the bounding set, fixes real/effective/saved GID and UID in that order to
mapped namespace ID `65532`, and sets all effective/permitted/inheritable
capability words to zero. Finally it sets `PR_SET_DUMPABLE=0` and
`PR_SET_NO_NEW_PRIVS=1`. The launcher proves with
`getresuid`, `getresgid`, `getgroups`, `capget`, `PR_CAPBSET_READ`,
`PR_CAP_AMBIENT_IS_SET`, `PR_GET_SECUREBITS`, `PR_GET_DUMPABLE`, and
`PR_GET_NO_NEW_PRIVS` that all values exactly match policy. Any unknown kernel
capability above the compiled maximum, unsupported securebit/ambient primitive,
supplementary group outside the exact mapped-primary/overflow rule, unlocked
bit, nonzero capability/dumpability, or mismatch is a hard pre-activation
failure. The launcher does not `execve` a second harness image: after all
restrictions pass it calls the reviewed harness translation unit in the same
static process, so the kernel cannot reset dumpability between the proof and
harness code. The harness entry rechecks dumpability and the complete
privilege tuple before reading FD `3` or any other external input.

Before lowering process/file limits or exposing any external input, the
launcher derives `G` from the sealed case manifest, requires `G=13`, requires
the inherited hard limits to admit the exact `4G+6` peak processes and
`16G+16` descriptors,
and predeclares exactly four fake-Git workers for each git-reader case plus one
sacrificial child for each of `AN-C017`, `AN-C018`, `AN-C019`, `AN-C020`, and
`AN-C037`. It records every PID/pidfd and creates no other
sandbox child. Negative-metadata, negative-content, positive-metadata, and
positive-content workers are distinct so an overflow, timeout, or kill/reap
oracle cannot destroy a later witness. Before creating the pool, the launcher
opens the copied-and-reproved read-only `/runtime` fake-Git ELF once with
`O_PATH|O_NOFOLLOW|O_CLOEXEC`, binds its identity to the runtime manifest, and
retains that descriptor only through worker creation. Each worker maps its
exact request pipe to stdin `0`, response pipe
to stdout `1`, diagnostic pipe to stderr `2`, retains the sealed executable
only as CLOEXEC FD `3`, closes everything else, and calls
`execveat(3, "", ..., AT_EMPTY_PATH)` with one-entry argv and zero-entry envp.
Fake-Git entry therefore sees only FDs `0` through `2`; the launcher closes its
last executable-descriptor reference before same-image harness activation. Its
first-entry path proves case/phase
identity and privilege state, resets and proves dumpability zero after the
exec transition, lowers its own soft/hard derived rlimits, proves the inherited
Landlock boundary with the fixed negative/positive probes, installs a
no-clone/no-exec final filter, and only then reads the first bounded
request from stdin. The request grammar is checked after those controls.
The two `negative-*` roles jointly implement one declared negative phase; when
the fault belongs to only metadata or content, the other role emits the exact
valid counterpart. The two `positive-*` roles jointly implement the corrected
phase. Thus four workers do not invent undeclared extra negative controls.
The same `tsdc-4an-inventory-core.o` is linked into both the production builder
and launcher, so harness builder cases call the production parser/renderer core
without spawning an unreviewed process. Only the thin production builder entry
point remains exclusive to the builder ELF.

Before any case request is written, each worker emits exactly one bounded
readiness line `WORKER_READY <case_id> <role> <evidence_sha256>\n` on stdout;
`role` is one of the four manifest tokens in the fixed order. The digest binds
the worker PID/pidfd, its three pipe identities, post-exec credential/
capability/dumpability tuple, exact derived rlimits, Landlock policy identity,
and installed final-filter identity. The launcher polls and consumes exactly
one readiness line from all `4G` workers within one `10`-second monotonic pool
deadline, requires every stderr pipe still empty, and folds the ordered results
into `worker_table_sha256`. Missing, duplicate, malformed, oversized, extra,
or mismatched readiness is fatal before same-image harness activation; no case
request is used as a readiness substitute.

Each sacrificial child installs the exact final filter, attempts only its one
assigned forbidden syscall (`setns`, `mount`, `open_by_handle_at`, `socket`, or
fork-like `clone3` respectively), and must be killed by seccomp with the exact
SIGSYS/pidfd/reap evidence. The launcher reaps all five before harness
activation; offline policy fixtures additionally prove that every syscall in
each forbidden family, including both `clone` and `clone3` and both handle
syscalls, is absent from the compiled filter.
The final seccomp policy admits neither `clone` nor `clone3`, so the initial
accepted live topology inside the sandbox is exactly namespace-init
launcher/harness plus `4G` one-case fake-Git workers; the bounded outer
launcher supervisor is recorded separately. Each fake-Git worker has already
lowered its own limits at first entry. Immediately after the exact worker and
sacrificial reaping set, the surviving launcher lowers its soft and hard
`RLIMIT_NPROC` to `4G+4` and `RLIMIT_NOFILE` to `16G+16` before same-image
harness activation. No role ever raises either value or creates another child
after its final filter. This ordering
keeps host real-UID population from making trusted predeclaration structurally
impossible while retaining both limits as defense-in-depth after all
capability bypasses are absent.

Neither launcher nor harness inherits an ambient environment. P_AN defines two
closed, ordered key/value manifests: the static-launcher bootstrap environment
and the post-pivot harness environment. The controller and launcher construct
their respective `envp` arrays from scratch, reject duplicate keys, embedded
NULs, unknown keys, values outside the sandbox, credentials, proxy/startup
controls, and every unlisted `LD_*`, `PYTHON*`, `GIT_*`, shell-init, locale, or
tool configuration variable. Any admitted locale, timezone, `PATH`, `HOME`, or
`TMPDIR` value is literal, points only inside the proved sandbox where
applicable, and is hash-bound by P_AN. Before harness activation, the launcher proves
byte-for-byte key order, key count, values, and serialized environment digest
against that manifest. It also fixes argv, cwd `/`, umask, signal dispositions
and mask, resource limits, and process personality. No inherited value can
reach the permitted protocol descriptors.

While still trusted and before harness activation, the launcher emits one bounded
containment preflight receipt. It proves namespace identities differ from the
parent, the old root is detached, the mount set equals the closed allowlist,
the descriptor set equals the protocol allowlist, the environment equals the
complete P_AN manifest with no inherited or extra key/value, no network route
or production process is reachable, UID/GID/groups equal the fixed tuple,
effective/permitted/inheritable/bounding/ambient capability sets are empty,
securebits are exactly locked, dumpability is zero, `no_new_privs` is one, and
open/stat attempts for the canonical
production worktree, Task, common Git directory, and object store fail with
the P_AN-bound denial.
Those production-path probe strings exist only in the trusted launcher phase
and are read from the runtime manifest into fixed mutable buffers, never
compiled as launcher literals or memory-mapped. After the four probes, the
launcher closes the manifest FD, applies `explicit_bzero` to every primary and
derived buffer, proves through volatile byte reads that each is zero, and
source/binary review confirms that none of the exact path byte strings occurs
in the launcher ELF or retained runtime files. Only then may same-image harness
activation occur. A missing,
duplicate, malformed, oversized, or non-pass preflight
field, unexpected descriptor or mount, successful negative-reachability probe,
or inability to prove the final restricted state stops before the harness. A
post-run comparison is defense-in-depth only and never substitutes for this
pre-execution OS boundary.

#### Data flow, adversarial verification, and review gates

The only permitted progression after a user-reviewed S_AN is:

1. publish and exactly rebind P_AN as a Plan-and-Task-only successor;
2. after fresh accepted P_AN reviews and explicit user execution approval,
   publish and exactly rebind the Task-only E_AN execution gate while
   preserving the P_AN Plan blob;
3. from exact E_AN, freeze a new controller source, builder source,
   containment-launcher/linked-harness sources, fake-Git source, and exact
   static ELF closure
   plus reproducible source-to-binary receipt, bootstrap/harness environment
   manifests, and isolated adversarial test-harness source;
4. obtain fresh independent specification and quality/security reviews of
   those exact source, executable, receipt, and policy blobs;
5. execute the reviewed containment launcher, require its exact preflight
   receipt, and permit it to activate the linked reviewed harness only after every
   namespace, mount, descriptor, environment, syscall-policy, and negative
   reachability proof passes;
6. inside that OS-enforced sandbox, execute the reviewed adversarial harness
   against isolated fake directories and fake bounded Git subprocesses without
   the production Task or object store; require exit zero, no signal or
   timeout, empty bounded stderr, and a deterministic case ledger containing
   exactly one `PASS` for every P_AN-bound case ID with no missing, duplicate,
   unknown, or non-pass result;
7. only after steps 5 and 6 pass completely and the controller re-proves that
   the harness had no production Task, Git object-store, path, descriptor, or
   network reachability, execute exactly one production builder invocation in
   the private transaction; that invocation must exit zero without signal or
   timeout and materialize a complete inventory, preimage, and pair receipt as
   exact Git blobs, or fail
   closed under the matrix below;
8. independently reprove the receipt, full-document/subspan bijection, and all
   frozen identities;
9. obtain fresh independent specification and quality/security reviews of the
   complete builder/inventory/preimage/receipt asset set; and
10. publish exactly one Task-only R_AN accepted-evidence checkpoint when both
    final asset reviews return `C0/I0/M0`, or, only after an explicit safe
    disposition, one mutually exclusive Task-only XE_AN exhausted-evidence
    checkpoint for a classified non-security failure; and
11. proceed to a separately defined AN-3 renderer step only from exact R_AN
    and only after a new user decision.

The adversarial asset must cover a pre-existing symlink, a same-UID hardlink,
an existing output name, a crash between payloads, a missing or mismatched
receipt, oversized and short Git stdout, oversized stderr, a stalled Git
process, a replacement object, a missing promisor object with lazy fetch
disabled, and a mixed historical/transition fragment whose preserved subspan
is altered. Containment witnesses also attempt production absolute paths,
inherited-descriptor access, namespace or mount re-entry, handle-based path
access, and network escape and require the exact P_AN-bound denial. These are
out-of-tree planning-asset tests only; they do not run
repository validators, repository tests, QA wrapper, or pre-commit.

The manifest additionally binds privilege-state proof, process-creation
enforcement, repository-config/include mutation, and alternates replacement as
closed cases. The launcher owns the evidence oracles for `AN-C017` through
`AN-C020`, `AN-C036`, and `AN-C037` and seals their fixed evidence into the
preflight after
zero-capability, exact-worker-pool, no-clone-filter, and defense-in-depth
rlimit checks. `AN-C015` is jointly evidenced by the launcher and harness. To
preserve one globally ordered ledger, the linked harness verifies those three
classes of sealed launcher evidence and emits their sole case lines at the normal
manifest ordinals; the launcher emits no `PASS <case_id>` line. All other case
evidence is harness-owned. The controller derives the expected set and order
from every manifest line, cross-checks launcher-owned digests against their
seven harness case lines, and rejects any missing/duplicate/unknown/out-of-order
ID.

The P_AN-bound case manifest is closed and independent of the harness source:
P_AN enumerates every mandatory case ID and expected failure domain, source
reviewers prove a one-to-one implementation for those IDs, and the controller
derives the expected ledger set from the exact P_AN Task rather than from
self-reported harness discovery. The controller requires the ledger bijection
before reading a success exit as acceptance and treats any harness nonzero
exit, signal, timeout, malformed or oversized output, stderr byte, missing
case, duplicate case, unknown case, or non-pass result as failure. Such a
failure revokes the production invocation for that attempt. A later command,
partial ledger, or manual inspection cannot cure it.

The implementer, source reviewers, and final asset reviewers must be fresh and
pairwise distinct from the rejected 4AM implementer and reviewers. Reviewers
consume exact Git objects or the same pinned descriptors, never mutable
pathnames. Any reviewer edit, object write, asset execution, or repository
mutation invalidates that review. P_AN may authorize only these bounded
planning assets until the final two reviews pass.

#### 4AN failure matrix

| Failure point | Durable result | Next authority |
| --- | --- | --- |
| S_AN publication or written-design review fails | P_AM remains the last executable Plan; rejected 4AM evidence is unchanged | stop and revise design only after user direction |
| P_AN review/publication/rebinding, user execution approval, or E_AN publication/rebinding fails | S_AN or P_AN remains current, or foreign state is preserved | new analysis and approval; no AN-2 asset and no automatic retry |
| Static-launcher ELF/provenance/seal/direct-exec proof, containment primitive, construction, environment equality, preflight receipt, or negative-reachability proof fails | E_AN remains current; no untrusted harness activation, production invocation, production transaction, accepted asset, or production object-store write exists; exact launcher/policy identities and bounded failure evidence may be retained | stop before untrusted harness activation with no fallback; XE_AN only after explicit safe disposition; no automatic cleanup, reconstruction, rerun, or retry |
| Adversarial harness does not prove every bound case or emits a non-accepting result while its fake-only boundary remains proved | E_AN remains current; frozen source/harness identities and bounded failure evidence may be retained, but no production invocation, production transaction, accepted receipt/assets, or production object-store write exists | stop before production; XE_AN only after explicit safe disposition; no automatic cleanup, rerun, or retry |
| Harness fake-only isolation cannot be proved or any production-path/object access is observed | no absence-of-mutation claim is made; preserve exact observed P_AN topology, repository/object-store state, isolated evidence, and bounded diagnostics without further access | stop as a security incident; no cleanup, production invocation, rerun, or retry; require explicit incident disposition and user authority |
| Production builder exits nonzero, is signaled or timed out, emits malformed/oversized diagnostics, or fails for an otherwise unclassified reason | no complete receipt or asset set is accepted; preserve exact observed topology, the incomplete private transaction, any already-materialized unreachable blobs or foreign drift, and bounded diagnostics without claiming P_AN is unchanged until read-only reproved | stop; no automatic cleanup, rebuild, rerun, or retry; require explicit security/evidence disposition and a user-approved return to design |
| Private directory, descriptor, ownership, mode, hardlink, fsync, or pair-receipt proof fails | no complete receipt or asset set is accepted and no absence-of-object-write claim is made; preserve the exact observed topology, proved-owned incomplete transaction, attempted payload/receipt OIDs, any already-materialized unreachable Git blobs or foreign drift, and bounded diagnostics until read-only object-store and P_AN topology reproving completes | stop; no automatic cleanup, object deletion, rebuild, rerun, or retry; require explicit security/evidence disposition and user authority |
| Git object is missing, replaced, fetched, oversized, short, timed out, prompted, or otherwise unclosed | no accepted output pair or review authority | read-only reproof; XE_AN only after explicit safe disposition |
| Fragment/subspan/occurrence partition or bijection fails | frozen bytes remain rejected evidence only | XE_AN only after explicit safe disposition |
| Either source or final asset review is not `C0/I0/M0` | E_AN remains current; AN-3 is not authorized | XE_AN only after explicit safe disposition |
| All final asset gates pass | exact receipt-bound assets become immutable P_AN-bound evidence | publish/rebind R_AN, then stop for a separate AN-3 drafting decision |

#### 4AN design acceptance boundary

S_AN is exact commit `bac234abf9e1e320d2311b8a8f448afe0a6cbac1`, a
single-parent successor of exact P_AM. Its final written-design specification
review and final quality/security review both returned `C0/I0/M0`, affirmative
compliance/readiness, and no finding. The user reviewed and approved S_AN, so
it authorizes drafting and reviewing the P_AN executable Plan below. It does
not itself authorize creation or execution of a 4AN asset, Git-object write,
repository validator/test, QA wrapper, pre-commit, Graphify update, runtime or
remote action, AN-3 renderer work, terminal construction, or publication.

### T-TSDC-004R-4AN — Executable secure occurrence-bound inventory Plan

> Current planning checkpoint: this checklist is executable only after P_AN is
> committed, exactly rebound, independently reviewed, and explicitly approved
> by the user. Until that approval, every AN-2 step is not started.

P_AN is the Plan-and-Task-only successor with exact subject
`docs(plan): define secure occurrence-bound inventory proof`. Its parent must
be exact S_AN `bac234abf9e1e320d2311b8a8f448afe0a6cbac1`; its own OID is
resolved only after publication and is intentionally not self-asserted in its
tree. P_AN changes only this Plan and its paired Task, both mode `100644`.

P_AN authorizes only AN-1. After fresh accepted P_AN reviews, exact
publication/rebinding, and explicit user execution approval, it authorizes
only AN-1E's Task-only E_AN checkpoint. Exact E_AN in turn authorizes the
bounded AN-2A through AN-2G evidence sequence. AN-3 is reserved for a separate
renderer Plan that does not yet exist. No AN-2 success authorizes
implementation, E_AL, R_AL, XE_AL, E_AM, R_AM, XE_AM, Task 4.5, Wave C,
Tasks 5–6, runtime, remote/external action,
QA-wrapper/pre-commit execution, dependency change, 4AL/4AM retry or
correction, Graphify update, terminal construction, or publication.

#### P_AN file map and immutable interfaces

AN-2 uses exact parent
`/home/hy/projects/hy-home.docker/.worktrees/target-surface-delta-convergence/_workspace/repo-support`,
opened once by the governance orchestrator as `PARENT_FD` with
`O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC`. The orchestrator records and proves
the opened directory's device, inode, owner, group, mode, link count,
filesystem type, and sticky-write policy before use. It accepts only the
effective-UID/effective-GID owner policy, exact mode `0755`, zero group/world
write bits, and zero sticky bit; a shared-writable or ownership mismatch stops
without creating a child. This is the governance-approved ignored repo-support
staging surface, not a diagnostics, log, credential, or durable-evidence store.
The orchestrator obtains 128 random bits with a complete `getrandom` read,
encodes them as 32 lowercase hexadecimal characters, and creates exactly one
build/source child at this stage whose basename is the literal prefix
`tsdc-4an-` followed by those 32
hexadecimal characters, relative to `PARENT_FD`, with create-only mode `0700`.
The orchestrator captures it with `fstatat(..., AT_SYMLINK_NOFOLLOW)` and opens
that child exactly once as `TX_FD` with the exact `openat2` flags and resolve
policy defined above. The opened/captured identities must match and have the same
device as `PARENT_FD`, a new inode, effective-UID/effective-GID ownership,
mode `0700`, link count two before subdirectory creation, and no group/world
access. The runtime-selected suffix is evidence but never an input to a hash,
receipt, or acceptance decision.

The following source/build/evidence names are exact relative to `TX_FD`; no
rejected `tsdc-4am-*` pathname is opened, patched, removed, or executed:

- `src/tsdc-4an-support.h` and `src/tsdc-4an-support.c`: bounded I/O, SHA256,
  Git-blob hashing, exact grammar, descriptor, deadline, and subprocess
  primitives shared by all binaries;
- `src/tsdc-4an-object-store.h` and `src/tsdc-4an-object-store.c`: bounded
  canonical loose-blob encoding/inflation, SHA-1/SHA256, create-no-replace,
  descriptor reproof, and file/fanout/object-directory durability primitives;
- `src/tsdc-4an-controller.c`: the sole host-side acceptance state machine,
  fixed controller request/FD interface, launcher and builder child ownership,
  bounded capture, config/alternates watches, production gate, object
  materialization, receipt-last decision, and no-retry classification;
- `src/tsdc-4an-inventory-core.h` and
  `src/tsdc-4an-inventory-core.c`: the sole deterministic inventory parser,
  partition verifier, and renderer core linked byte-identically into builder
  and launcher;
- `src/tsdc-4an-inventory-builder.c`: the thin production/fake request and FD
  entry point over that core; it writes only through two pre-opened payload FDs
  and owns neither Git nor publication;
- `src/tsdc-4an-containment-launcher.c`: the only namespace/root constructor;
  it owns ELF verification, namespace construction, root pivot, descriptor
  closure, Landlock, seccomp, preflight, and same-image harness activation;
- `src/tsdc-4an-adversarial-harness.c`: the closed case-manifest executor and
  one-PASS-per-case ledger producer, linked into the containment launcher and
  never emitted or executed as a separate ELF;
- `src/tsdc-4an-fake-git.c`: the only Git executable present in the sandbox;
- `manifests/tsdc-4an-cases.jsonl`: exact bytes copied from the paired Task's
  `TSDC-4AN-CASE-MANIFEST` block after a byte-for-byte extraction proof. The
  asset is the ordered concatenation of only the JSON object lines between the
  markers, each including one LF; comments and code fences are excluded;
- `manifests/tsdc-4an-policy.txt`: exact architecture, Landlock rights,
  seccomp allowlist, namespace, mount, descriptor, signal, rlimit, personality,
  argv, and timeout policy;
- `manifests/tsdc-4an-bootstrap.env`: the empty bootstrap environment, zero
  bytes, SHA256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `manifests/tsdc-4an-harness.env`: NUL-delimited ordered bytes
  `HOME=/nonexistent`, `LANG=C`, `LC_ALL=C`, `TMPDIR=/work/tmp`, `TZ=UTC`,
  each followed by NUL, total `58` bytes, SHA256
  `cb082fead837d5d1c9fcfefd74c100c743853d91711202b9df5117d1b749204c`;
- `manifests/tsdc-4an-runtime.txt`: exact runtime destination, blob/SHA256,
  byte count, mode, and source descriptor slot for the linked harness/inventory-core
  translation-unit identities, fake-Git ELF, case/environment/policy manifests,
  the four launcher-only production-denial probe strings, plus the complete
  canonical fixture-byte/link/mode construction map. The bootstrap manifest is
  consumed and zeroized rather than copied into `/runtime`; no
  separate fixture input, harness ELF, or sandbox builder ELF exists;
- `manifests/tsdc-4an-git-view.txt`: exact private control-directory tree,
  descriptor slots, Git argv/envp, configuration/alternate watches, bounded
  reader commands, object-format requirement, materializer policy, and the
  exact canonical production worktree, historical P_AN Task, common Git,
  object-directory, and `/usr/bin/git` open/probe strings. The controller may
  use those host strings only after `HARNESS_ACCEPTED`; the launcher may use
  the four denial-probe strings only before zeroizing them and activating the
  same-image harness;
- `evidence/tsdc-4an-controller-request.txt`: one create-only dynamic entry
  envelope rendered only after both source reports return. It uses the exact
  controller-request grammar and names all P_AN/E_AN/Task/package/build/
  manifest/binary/source-review identities admitted at the execution gate.
  It is excluded from the source package and both source-review inputs, is
  treated as untrusted by the controller, and becomes evidence only after the
  controller rederives every field from its pinned descriptors;
- `build-a/` and `build-b/`: independent reproducible-build destinations;
- `evidence/tsdc-4an-build-receipt.txt`: toolchain closure, two-build
  correspondence, ELF policy, and source-to-binary proof;
- `evidence/tsdc-4an-source-package.txt`: immutable isolated-object identities
  supplied to both source reviewers;
- `evidence/tsdc-4an-asset-review-package.txt`: immutable receipt-bound input
  set supplied identically to both final asset reviewers;
- `evidence/tsdc-4an-production-run.txt`: the non-self-referential final
  controller receipt for Git-view identity, invocation counts, payload and
  pair-receipt object state/durability, config/alternates watch state, and
  `completion=COMPLETE`;
- `tsdc-4an-projection-inventory.jsonl`,
  `tsdc-4an-projection-preimage.txt`, and
  `tsdc-4an-pair-receipt.txt`: exact names relative only to a separate
  unpredictable mode-`0700` `OUT_FD` created beneath `PARENT_FD` for the one
  production attempt. These three names are not relative to `TX_FD` and never
  exist directly beneath shared `/tmp`.

The four binaries are self-contained static PIE ELF objects for exact
`x86_64-linux-gnu`: `tsdc-4an-controller`, `tsdc-4an-inventory-builder`,
`tsdc-4an-containment-launcher`, and `tsdc-4an-fake-git`. The launcher binary
contains the separately named harness translation unit. The source package
also binds absolute `/usr/bin/cc`, the
actual linker and startup/static archive closure reported by that compiler,
absolute `/usr/bin/git`, and every build input by descriptor identity,
SHA256, byte count, mode, and computed Git blob OID. Tool lookup through
`PATH`, package installation, network fetch, and build fallback are forbidden.

The controller's start contract is exact: argv is the one-entry vector
`tsdc-4an-controller`, envp has zero entries, cwd is `/`, umask is `0077`, the
signal mask is empty, and all catchable dispositions are default. After an
outer descriptor-bound sealed-memfd direct exec, its inherited FD map is: `0`
read-only null, `1` bounded canonical result, `2` bounded diagnostic, `3`
controller request, `4` exact P_AN Task blob, `5` source package, `6` build
receipt, `7` case manifest, `8` policy, `9` runtime, `10` bootstrap env, `11`
harness env, `12` controller ELF self descriptor, `13` launcher ELF, `14`
builder ELF, `15` fake-Git ELF, `16` source specification report, `17` source
quality/security report, `18` PARENT_FD, `19` TX_FD, `20` exact E_AN Task
blob, `21` Git-view manifest, and `22` one controller-side
`SOCK_SEQPACKET|SOCK_CLOEXEC` final-review transfer endpoint whose peer remains
with the governance orchestrator. FD `23` and above are closed/unshared before
controller code proceeds. Before child creation the orchestrator copies each
data input in FDs `3` through `11`, `16`, `17`, `20`, and `21` into its own
`MFD_ALLOW_SEALING|MFD_CLOEXEC|MFD_NOEXEC_SEAL` memfd, applies and verifies
write/grow/shrink/seal plus execute-denial seals, and maps only the read-only
copies. It copies each executable in FDs `12` through `15` into a distinct
`MFD_ALLOW_SEALING|MFD_CLOEXEC|MFD_EXEC` memfd with the four
write/grow/shrink/seal seals and no execute-denial seal. The controller rereads
and rehashes every sealed FD before use; `PARENT_FD`, `TX_FD`, and FD `22` are
the only non-memfd inputs. Missing kernel seal support is a hard pre-start
failure with no regular-file fallback. The
controller-request schema `tsdc-4an-controller-request/v1` has unique ordered
LF fields `schema`, `pan_commit`, `pan_task_blob`, `ean_commit`,
`ean_task_blob`, `source_package_blob`,
`build_receipt_blob`, the four binary blob/SHA256/byte tuples, six input-manifest
blob/SHA256/byte tuples, two source-review blob/assignment/verdict tuples,
`completion=REQUEST`, and final `request_sha256`. Unknown, missing, duplicate,
out-of-order, mutable, or mismatched input fails before any child or production
descriptor is opened. The request is never a source-package child and never
vouches for itself: the controller recomputes every tuple from FDs `4` through
`21`, exact branch topology, and the two canonical source reports before using
it as an execution gate.

Controller input caps are exact and checked before allocation: request
`65536` bytes; each P_AN/E_AN Task `2097152`; source package, build receipt,
and runtime manifest `16777216` each; case, policy, and Git-view manifests
`1048576` each; bootstrap environment zero; harness environment exactly `58`;
each executable `33554432`; and each source report `262144`. Every streamed
count uses checked unsigned 64-bit arithmetic. Exceeding a cap, arithmetic
overflow, short/extra byte, or trailing data stops before child or production
access.

The controller state machine is exactly `INIT -> INPUTS_BOUND ->
HARNESS_STARTED -> HARNESS_REAP_STARTED -> HARNESS_REAPED -> HARNESS_ACCEPTED
-> PRODUCTION_INPUTS_BOUND -> OUT_CREATED -> BUILDER_STARTED ->
BUILDER_REAP_STARTED -> BUILDER_REAPED -> PAIR_ACCEPTED ->
REVIEW_PACKAGE_FROZEN -> ASSET_REVIEWS_PENDING -> ASSET_REPORTS_BOUND ->
COMPLETE` on the accepted path.
`*_STARTED` is recorded before the child-creation syscall and
`*_REAP_STARTED` before the sole bounded wait. Ambiguous return, lost child,
or lost output never retries. Before `HARNESS_ACCEPTED`, the controller may not
open the production common Git directory, object directory, Git executable,
configuration, alternates surface, or `OUT_FD`.

After `REVIEW_PACKAGE_FROZEN`, the controller makes no further change to any
review input and emits one canonical `ASSET_REVIEW_READY` identity envelope.
It remains alive while the two final reviewers consume that exact object set.
Only in `ASSET_REVIEWS_PENDING` may FD `22` receive exactly two ordered
messages, asset specification then asset quality/security. Each message has
zero inline payload and exactly one `SCM_RIGHTS` descriptor for a read-only
memfd sealed with `F_SEAL_WRITE|F_SEAL_GROW|F_SEAL_SHRINK|F_SEAL_SEAL`; the
orchestrator copies exactly the returned canonical reviewer bytes into that
memfd and cannot submit a pathname. The controller caps each report at
`262144` bytes, rereads it once, verifies seals, canonical schema, reserved and
pairwise-distinct assignment, complete reviewed identities, verdict, findings,
and digest, then materializes those exact bytes once in the isolated object
store. Before the first message it also requires FD-`22` `SO_PEERCRED` to equal
the exact orchestrator PID/effective-UID/effective-GID tuple captured at
controller creation; peer or credential drift is fatal. Missing, duplicate,
reordered, extra-descriptor, malformed, unsealed,
oversized, identity-mismatched, non-`C0/I0/M0`, or non-affirmative reports, or
failure to receive both within the fixed `1800`-second monotonic review window,
is a classified non-accepting terminal with no resubmission or controller
restart. FD `22` is never inherited by launcher, builder, or Git children and
is closed immediately after the second accepted report.

Controller stdout is a two-frame canonical protocol capped at `16384` bytes;
accepted execution emits exactly
`ASSET_REVIEW_READY <review_package_blob> <review_package_sha256>\n`, then
`CONTROLLER_STATUS PASS <run_sha256> <asset_spec_blob> <asset_qs_blob>\n` only
after both reports are accepted. A pre-ready or post-ready failure emits no
PASS frame and at most one bounded
`CONTROLLER_STATUS FAIL <fixed_code> <evidence_sha256>\n`; the orchestrator
still reaps the same controller and never restarts it. Controller stderr is
capped at `4096` bytes and acceptance requires zero bytes. Unknown, duplicate,
out-of-order, trailing, oversized, or post-PASS output is non-accepting.

The builder's exact argv is the one-entry vector
`tsdc-4an-inventory-builder`; envp has zero entries. Its inherited map is `0`
bounded request input, `1` canonical result output, `2` bounded diagnostic,
`3` sealed exact Task-or-fixture input, `4` pre-created inventory output, and
`5` pre-created preimage output; FD `6` and above are closed. The unique-key LF
request grammar `tsdc-4an-builder-request/v1` contains ordered fields `schema`,
`mode` (`FAKE` or `PRODUCTION`), `case_id`, `input_oid`, `input_type=blob`,
`input_sha256`, `input_bytes`, `object_format=sha1`,
`discovery_rules_sha256`, `completion=REQUEST`, and `request_sha256`;
`completion=REQUEST` is penultimate, and the request is capped at
`4096` bytes. This request is the only mode
selector. The builder never invokes Git and never receives a repository,
worktree, parent, transaction, or output-directory pathname/FD. The controller
owns production Git reads and object publication; the harness exercises the
same bounded-reader primitives against the reviewed fake Git. No interface
accepts a mutable Task pathname.

For the sole production invocation, the controller copies and reproves the
reviewed builder ELF into a fully sealed executable memfd, records
`BUILDER_STARTED` before exactly one
`clone3(flags=CLONE_PIDFD, exit_signal=SIGCHLD)` with all other fields zero,
and lets only that child map FDs `0` through `5`, close the rest, and
`execveat(..., AT_EMPTY_PATH)`. The controller retains the pidfd and output
FDs, records `BUILDER_REAP_STARTED` before its only bounded wait, and never
substitutes an in-process or pathname execution.

The production pair receipt schema is exactly
`tsdc-4an-pair-receipt/v1`. Unique ordered fields are `schema`,
`pan_task_blob`, `execution_gate_commit`, `execution_gate_task_blob`,
`controller_blob`, `controller_sha256`, `controller_bytes`,
`builder_blob`, `builder_sha256`, `builder_bytes`,
`inventory_blob`, `inventory_sha256`, `inventory_bytes`, `preimage_blob`,
`preimage_sha256`, `preimage_bytes`, `case_manifest_blob`,
`source_package_blob`, `git_view_manifest_blob`,
`git_view_manifest_sha256`, `payload_durability_sha256`,
`harness_ledger_sha256`, `completion`, and
`receipt_sha256`; `completion=COMPLETE` is the penultimate field and the final
field hashes the canonical preceding bytes. No pathname, transaction suffix,
timestamp, process ID, locale-dependent value, or self-referential receipt Git
OID occurs in the receipt.

`payload_durability_sha256` binds only the inventory and preimage object-state
and durability records, never the pair receipt's own future object state. After
the receipt object is durably reproved, the controller writes the separate
`tsdc-4an-production-run/v1` evidence with ordered identities for exact E_AN,
controller, the rederived controller request, both accepted source reports,
Git view, watches, one harness activation, complete two-level
supervisor/namespace-init reap, one builder invocation, both
payloads, the pair receipt, all three object states/durability tiers, and
`completion=COMPLETE`; its final `run_sha256` hashes preceding bytes. That run
receipt is stored only in the isolated review object store and is not a field
of the pair receipt, avoiding either self-reference.

Before entering `REVIEW_PACKAGE_FROZEN`, the controller performs the final
config/alternates drain and object/durability reproof, copies only canonical
identity evidence into the isolated review store, and closes every production
Git executable, control/config, Task, object-directory, watch, payload,
receipt, and `OUT_FD` capability. It then reproves that none remains. During
the final-review wait it retains only its sealed self/input identities, the
isolated `TX_FD` evidence capability, bounded result/diagnostic channels, the
controller pid state, and FD `22`; a production capability surviving the
transition is non-accepting.

The frozen final-review package schema is
`tsdc-4an-asset-review-package/v1`. Its unique ordered LF fields bind exact
P_AN/E_AN topology, controller request, source package/build receipt, six input
manifests, four binaries, two source reports, containment preflight and worker
table, complete harness ledger, production-run receipt, inventory, preimage,
pair receipt, loose-object/durability states, review-role constraints,
`completion=REVIEW_READY`, and final `package_sha256`. It contains neither its
own future Git OID nor either final report. The controller materializes this
package once, reopens it by exact object identity, and only then emits the
ready frame; both final reviewers bind the ready-frame blob and SHA256.

The isolated source-package schema is exactly
`tsdc-4an-source-package/v1`. Its canonical unique-key LF grammar binds exact
P_AN commit/Task blob and E_AN commit/Task blob OIDs resolved after their
respective publications, object format,
branch, every source, the exact six immutable input manifests, and every
four-binary blob-SHA256-byte-mode tuple, compiler, linker,
startup/static-archive closure, build receipt, case manifest,
bootstrap/harness environments, runtime/policy manifests, fixed bounds, four
source/final-asset review-role names, the already accepted `AN_GATE_VERIFY`
identity, the reserved `AN_TERMINAL_VERIFY` role name, the implementation
assignment, the exact forbidden-identity sets and pairwise-distinctness rules,
and the complete
prohibited-authority tuple. It
contains no mutable pathname or self-asserted P_AN value from the P_AN tree.
The dynamic controller request and all source/final review reports are
deliberately excluded: reports bind this already-frozen package, while the
later untrusted request binds the returned source reports. This directed
dependency order forbids a package/request/report hash cycle.
Actual source-review assignments are bound later by their reports and the
dynamic request; actual final-review and terminal-verifier assignments are
bound by their own later evidence. Each is checked against the frozen role and
forbidden-identity rules before it can grant authority.

The containment launcher receives exactly these inherited descriptors after
the reviewed controller maps them with `dup3`: stdin `0` as read-only null,
stdout `1` as the bounded ledger pipe, stderr `2` as the bounded diagnostic
pipe, runtime manifest `3`, fake-Git ELF `4`, case manifest `5`, policy
manifest `6`, harness environment manifest `7`, and one controller-created
`SOCK_SEQPACKET|SOCK_CLOEXEC` supervisor-control endpoint `8`.
No other descriptor is admitted. Bootstrap argv contains exactly one entry,
`tsdc-4an-containment-launcher`, and bootstrap envp contains zero entries.
Before harness activation the launcher has copied and reproved every runtime input,
then writes the accepted production-denial witness into one non-executable
memfd capped at `4096` bytes, verifies the exact grammar and digest, and seals
it with `F_SEAL_WRITE|F_SEAL_GROW|F_SEAL_SHRINK|F_SEAL_SEAL`. It maps that
read-only sealed proof to harness FD `3`, maps the already-proved worker
pipe/pidfd table contiguously at FDs `4` through `16G+3`, then
closes/unshares every higher descriptor. The linked harness entry receives the logical
one-entry argv `tsdc-4an-adversarial-harness` and the exact 58-byte environment
manifest through explicit arguments; it never consults inherited `environ`.
The harness validates FD `3` identity, size, seals, grammar, P_AN Task
binding, and digest, caches only its exact AN-C015 proof hash, ordered
AN-C017–AN-C020 sacrificial-denial digest, AN-C036 evidence seed, and AN-C037
evidence hash, and closes it before emitting any case line.
It also verifies every four-FD worker tuple against the exact case ordinal,
request/response/diagnostic pipe direction and inode, pidfd/PID, and preflight
identity set. Each git-reader case consumes its four one-shot workers in exact
negative-metadata, negative-content, positive-metadata, positive-content order,
enforces the declared timeout/overflow/kill/reap behavior, validates the typed
byte-stream and diagnostic transcript, closes all twelve harness-side pipe
descriptors, and reaps all four pidfds before advancing. After the last case no
worker pipe, pidfd, or fake worker remains open/live.

The sealed proof schema is `tsdc-4an-preflight-proof/v1` with unique ordered LF
fields `schema`, `pan_task_blob`, `execution_gate_commit`,
`execution_gate_task_blob`, `case_id=AN-C015`, `probe_count=4`, four
ordered role-specific denial-code/errno fields for worktree, Task, common Git,
and object store, `containment_case_count=4`,
`containment_denials_sha256`, `privilege_case_id=AN-C036`,
`privilege_case_seed_sha256`,
`process_case_id=AN-C037`, `process_case_sha256`, `policy_sha256`,
`production_path_denials_sha256`,
`status=PASS`, and final `proof_sha256`. It contains no production pathname
bytes. `AN-C015` emits its one ledger PASS only after observing this sealed
proof, rejecting a generic fake-root negative witness without the boundary,
and accepting the `/work` positive witness. Its evidence digest is SHA256 of
the NUL-delimited tuple `AN-C015`, preflight-proof SHA256, negative-witness
SHA256, and positive-witness SHA256, including a final NUL. The controller
cross-checks that proof digest against the launcher's stdout preflight receipt
and the harness ledger; either channel alone is non-accepting.

For each of `AN-C017` through `AN-C020`, the harness derives the sole case
evidence digest from the NUL-delimited case ID, assigned syscall/family,
compiled-policy SHA256, sacrificial PID/pidfd identity, exact SIGSYS status,
sole-reap proof, and ordered `containment_denials_sha256`, including a final
NUL. It never performs the killing syscall in the long-lived harness process.

Before reading FD `3` or any case/runtime manifest, the harness entry reproves
UID/GID/supplementary mapping, all capability sets and
bounding/ambient bits, locked securebits, dumpability zero, no-new-privs one,
and every rlimit. It emits exactly one bounded line
`POSTDROP_PRIVILEGE PASS <evidence_sha256>` before the case ledger; its digest
binds the sealed preflight privilege fields and the same-image post-drop
observations.
This line and the corresponding `AN-C036` case are both required, but the
controller still permits only one `PASS AN-C036 ...` case line. That case
digest is SHA256 of the NUL-delimited AN-C036 seed and POSTDROP digest, with a
final NUL. Missing,
late, duplicate, or mismatched post-drop privilege evidence stops the harness
before any fake Git or filesystem case.

#### P_AN closed policy and acceptance outputs

The policy manifest requires Landlock ABI at least 3 and handles exactly
`EXECUTE`, `READ_FILE`, `READ_DIR`, `WRITE_FILE`, `REMOVE_DIR`, `REMOVE_FILE`,
`MAKE_CHAR`, `MAKE_DIR`, `MAKE_REG`, `MAKE_SOCK`, `MAKE_FIFO`, `MAKE_BLOCK`,
`MAKE_SYM`, `REFER`, and `TRUNCATE`. Rules grant `EXECUTE`, `READ_FILE`, and
`READ_DIR` only under `/runtime`. Rules for `/work` grant `READ_FILE`,
`READ_DIR`, `WRITE_FILE`, `REMOVE_DIR`, `REMOVE_FILE`, `MAKE_DIR`, `MAKE_REG`,
`REFER`, and `TRUNCATE`; they do not grant device, FIFO, socket, symlink, host,
network, or old-root creation/access. Absence of the requested ABI or right is
a hard failure, not a best-effort downgrade.

The same policy fixes monotonic bounds rather than implementation defaults:
each Git metadata stdout is at most `256` bytes, each Git content stdout is
exactly the frozen object length with an `expected+1` overflow sentinel, every
Git stderr is capped at `4096` bytes, and every Git child deadline is `10`
seconds. Launcher/harness stdout is capped at `131072` bytes, each ledger line
at `256` bytes, launcher/harness stderr at `4096` bytes but acceptance requires
zero bytes, and the whole harness deadline is `60` seconds. Production-builder
stdout is capped at `16384` bytes, stderr at `4096` bytes but acceptance
requires zero bytes, and its deadline is `60` seconds. Compiler stdout/stderr
are each capped at `4096` bytes, acceptance requires both empty, and each build
deadline is `60` seconds. All overflow/timeout paths kill and reap the exact
child and never continue from partial output.

Post-pivot state fixes cwd `/`, umask `0077`, an empty signal mask, default
disposition for every catchable signal, personality `PER_LINUX` with
`READ_IMPLIES_EXEC` and `ADDR_NO_RANDOMIZE` absent, and exact rlimits:
`RLIMIT_CORE=0`, `RLIMIT_CPU=30`, `RLIMIT_FSIZE=16777216`,
`RLIMIT_NOFILE=16G+16` (exact `224` for `G=13`),
`RLIMIT_NPROC=4G+4` (exact `56`), `RLIMIT_STACK=8388608`, and
`RLIMIT_AS=268435456`, each with equal soft and hard values. The closed mount
set is the tmpfs `/` plus a
bind-remounted read-only `/runtime`; `/work` is the only writable directory in
the tmpfs root. No `/proc`, `/sys`, `/dev`, host bind, or additional mount is
present and the new network namespace has no route or enabled interface.

The seccomp filter first rejects a non-`AUDIT_ARCH_X86_64` architecture and
then defaults to process-killing denial. Its only admitted syscall names are:
`read`, `write`, `readv`, `writev`, `close`, `lseek`, `pread64`, `pwrite64`,
`fstat`, `newfstatat`, `statx`, `fcntl`, `openat`, `openat2`,
`mkdirat`, `unlinkat`, `renameat2`, `fchmod`, `fchmodat2`, `fsync`,
`fdatasync`, `getdents64`, `inotify_init1`, `inotify_add_watch`,
`inotify_rm_watch`, `wait4`, `waitid`,
`pidfd_send_signal`, `poll`, `ppoll`, `clock_gettime`, `nanosleep`, `mmap`,
`mprotect`, `munmap`, `mremap`, `brk`, `madvise`, `futex`, `set_tid_address`,
`set_robust_list`, `rseq`, `arch_prctl`, `prlimit64`, `getrandom`, `getpid`,
`getppid`, `gettid`, `getuid`, `geteuid`, `getgid`, `getegid`, `getresuid`,
`getresgid`, `getgroups`, `capget`, `prctl`,
`rt_sigaction`, `rt_sigprocmask`, `rt_sigreturn`, `sigaltstack`, `exit`,
`exit_group`, and `uname`. Neither `clone` nor `clone3` is admitted after the
predeclared fake-Git and sacrificial children are created; each of the five
sacrificial children must therefore die on its one role-bound post-filter
attempt.
`mmap` and `mprotect`
reject every request containing `PROT_EXEC`. `prctl` is argument-filtered to
`PR_SET_DUMPABLE` with value zero and read-only `PR_GET_DUMPABLE`,
`PR_GET_NO_NEW_PRIVS`, `PR_GET_SECUREBITS`, `PR_CAPBSET_READ`, and
`PR_CAP_AMBIENT_IS_SET`; every other option or nonzero unused argument is
killed. `fcntl` is argument-filtered to `F_GET_SEALS` on sealed proof FD `3`
and `F_GETFD`/`F_GETFL` on the manifest-bound descriptor range; duplication,
flag mutation, ownership, lease, notification, and every other command is
killed. `pidfd_send_signal` admits only `SIGTERM` or `SIGKILL`, a null siginfo,
zero flags, and a pidfd in the manifest-bound worker table. `prlimit64` is
admitted only for `pid=0`, one of the exact policy
resources, `new_limit=NULL`, and a non-null old-limit output; it cannot modify
any limit. `inotify_init1` admits only `IN_NONBLOCK|IN_CLOEXEC`; source and
runtime checks constrain add/remove operations to the exact fake `/work` watch
set and closed event mask. Source review must remove any
syscall not reached by the frozen binaries; adding an unlisted syscall after
source review changes the policy identity and invalidates both reviews.
Sockets, mounts, namespace
changes, `setns`, `chroot`, `pivot_root`, file handles, ptrace,
process-memory access, keyrings, BPF, performance events, `io_uring`, and every
other unlisted syscall remain denied after containment.

Before installing the final seccomp filter, the launcher uses `clone3` with
`flags=CLONE_NEWUSER|CLONE_NEWNS|CLONE_NEWPID|CLONE_NEWIPC|CLONE_NEWUTS|
CLONE_NEWNET|CLONE_PIDFD` and `exit_signal=SIGCHLD`; all other `clone_args`
fields are zero. The returned pidfd and PID identify the same child. The
parent opens and rechecks one `/proc/<pid>` directory identity, writes exact
`deny` to `setgroups`, then the one-line GID map, then the one-line UID map,
and the child does not continue until those writes, read-backs, and descriptor
identities pass. It converts
mount propagation to `MS_REC|MS_PRIVATE`, mounts the new `nodev,nosuid` tmpfs
root, installs individually pinned runtime files, remounts `/runtime`
read-only, keeps `/work` as the sole writable subtree, performs `pivot_root`,
changes to `/`, detaches and removes the old root, fixes umask `0077`, resets
all signal dispositions and mask, fixes reviewed rlimits and personality,
consumes and closes the runtime inputs, maps only the sealed proof and exact
worker pipe/pidfd table to FDs `3` through `16G+3`, and uses the
overflow-checked equivalent of
`close_range(16G+4, UINT_MAX, CLOSE_RANGE_UNSHARE)`. It then reproves exactly
FDs `0` through `16G+3` against the manifest-derived table. `ENOSYS`, `EINVAL`,
or any partial primitive
is failure;
there is no `/proc/self/fd` or weaker fallback. It then sets
`PR_SET_NO_NEW_PRIVS`, installs Landlock, installs seccomp, and directly calls
the linked static harness entry without an intervening exec or loader.

The pre-namespace launcher branch is a bounded trusted supervisor, not a
harness process. Immediately after successful namespace `clone3`, it sends the
returned inner-PID-namespace-init pidfd and exact outer PID once to the
controller over FD `8` with `SCM_RIGHTS`; the controller verifies the pidfd/PID
pair before allowing the child barrier to open. The supervisor then closes all
runtime and ledger descriptors, retains only its inner pidfd and control
endpoint, writes/maps the child's IDs through the pinned `/proc/<pid>`
descriptor, and performs one bounded wait. The sandbox child closes FD `8`
before root construction. On timeout, signal, supervisor loss, or controller
cancellation, the controller signals the inner PID-namespace init directly by
pidfd, then the supervisor, and reaps both; killing namespace PID 1 terminates
all remaining sandbox descendants. A missing/duplicate pidfd transfer,
credential mismatch, pidfd/PID mismatch, lost supervisor, or incomplete
two-level reap is non-accepting and never leaves a fake worker running.

The trusted controller copies the exact reviewed static containment ELF into
an executable memfd created with
`MFD_ALLOW_SEALING|MFD_CLOEXEC|MFD_EXEC`. It never sets
`MFD_NOEXEC_SEAL` or `F_SEAL_EXEC` on that executable object. After a complete
write it adds and verifies `F_SEAL_WRITE|F_SEAL_GROW|F_SEAL_SHRINK|
F_SEAL_SEAL`, rereads and rehashes the bytes, and creates exactly one launcher
child with `clone3(flags=CLONE_PIDFD, exit_signal=SIGCHLD)` and all other
fields zero. `HARNESS_STARTED` is durable before that syscall. The child maps
only launcher FDs `0` through `8`, closes everything else, and invokes only
`execveat(memfd, "", argv, envp, AT_EMPTY_PATH)`; the controller retains the
returned pidfd, drains bounded pipes, and remains the sole acceptance owner.
A shebang, `PT_INTERP`,
external `DT_NEEDED`, `RPATH`/`RUNPATH`, wrong class/data/machine/type, malformed
or out-of-range program header, W+X `PT_LOAD`, or executable `PT_GNU_STACK`
is rejected by a bounded parser before the memfd is executed. `ldd` is never
used as authority.

The launcher emits one canonical LF-delimited preflight receipt to stdout
before same-image harness activation. Required unique fields are `schema`,
`pan_task_blob`, `execution_gate_commit`, `execution_gate_task_blob`,
`launcher_blob`, `policy_blob`, `runtime_manifest_blob`, `bootstrap_env_sha256`,
`harness_env_sha256`, `namespace_proof`, `old_root_detached`, `mount_set`,
`fd_set`, `uid_map_sha256`, `gid_map_sha256`, `setgroups_state`,
`credential_state`, `supplementary_group_state`, `capability_sets`,
`bounding_set`, `ambient_set`, `securebits`, `dumpable`, `rlimit_state`,
`worker_pool_state`, `worker_table_sha256`, `sacrificial_count=5`,
`sacrificial_denials_sha256`, `process_creation_proof`,
`pid_namespace_pid`, `trace_guard_state`, `landlock_abi`,
`seccomp_arch`, `no_new_privs`, `network_state`, `supervisor_state`,
`inner_pidfd_state`, `process_state`,
`production_path_denials_sha256`, `sealed_proof_sha256`, `status`, and
`preflight_sha256`. `status=PASS` is penultimate and `preflight_sha256` is the
SHA256 of every preceding canonical byte, including the status LF. The
controller rejects unknown, missing, duplicate, oversized, or
out-of-order fields. Harness ledger lines then use exactly
`PASS <case_id> <evidence_sha256>` in ascending case-manifest order. One final
`HARNESS_STATUS PASS` is accepted only after the exact case-set bijection;
process exit alone never grants production authority.

#### AN-1 — Publish and rebind P_AN

**Files:**

- Modify:
  `docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md`
- Modify:
  `docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md`

- [ ] Prove HEAD is exact S_AN, the two canonical paths are the only changed
  tracked paths, base and candidate modes are `100644`, and `git ls-files -v`
  plus `git ls-files -f` both report ordinary entries.
- [ ] Freeze candidate Plan/Task SHA256, byte counts, Git blob OIDs, and binary
  `S_AN..P_AN` diff SHA256/bytes. Obtain fresh read-only specification and
  quality/security Plan reviews over those exact bytes; both must return
  `C0/I0/M0`, affirmative compliance/security, and `PLAN_COMMIT_READY YES`.
- [ ] Publish exactly one raw single-parent P_AN commit without repository
  hooks. Expected-old ref CAS names exact S_AN and the subject is exact.
- [ ] Re-resolve P_AN by full parent, distance one, exact unique subject, raw
  commit, tree, both path modes/blobs, and clean branch/index/worktree proof.
  Record the exact P_AN OID outside its own tree. Stop for explicit user review;
  AN-2A has no authority before that approval and the E_AN checkpoint below.

**Planning-only verification commands:**

```text
git diff --check
git diff --name-only bac234abf9e1e320d2311b8a8f448afe0a6cbac1 --
git ls-files -s -- docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
git log --format=%H%x00%P%x00%s --all --fixed-strings --grep='docs(plan): define secure occurrence-bound inventory proof'
```

Expected before publication: `git diff --check` is silent; the changed-path
command prints exactly the Plan then Task paths; both index modes are `100644`;
the exact P_AN subject count is zero. Expected after publication: the subject
count is one, its sole parent is exact S_AN, and the worktree is clean.

#### AN-1E — Publish the Task-only execution gate E_AN

- [ ] The P_AN tree intentionally asserts neither its own post-publication OID,
  corrected Plan-review outcome, user execution decision, nor any AN-2
  start/result. Those facts are external and non-authoritative until E_AN.
- [ ] After the user explicitly approves AN-2 execution, render one Task-only
  successor whose parent is exact P_AN, whose Plan blob/mode equals P_AN, and
  whose exact subject is
  `docs(task): record secure inventory Plan approval`. It records exact P_AN
  OID/Plan/Task/diff identities, the two fresh corrected-P_AN reviewer
  identities and `C0/I0/M0` verdicts, publication/rebinding proof, the user
  decision, Subagent-Driven mode, and every asset/review as not started.
- [ ] Assign fresh read-only `AN_GATE_VERIFY`, distinct from both corrected
  P_AN reviewers and every reserved implementation/source/asset/terminal role.
  It independently proves the E_AN candidate changes only the Task as mode
  `100644`, contains no self OID, has exact parent P_AN and unique subject, and
  preserves the Plan blob byte-for-byte. Publish/rebind it by expected-old CAS.
  AN-2A begins only from exact E_AN. A missing/rejected approval, failed render,
  review defect, CAS conflict, or rebind defect leaves AN-2 unauthorized.

E_AN is an evidence gate, not implementation or asset evidence. It changes the
current Task bytes, so every AN-2 inventory remains explicitly bound to the
historical exact P_AN Task blob. Any future AN-3 design must rediscover and
rebind the then-current R_AN Task rather than treating the P_AN inventory as a
current-Task inventory.

#### AN-2A — Author the closed cases before implementation

- [ ] Assign one fresh implementation agent ownership of only the exact
  transaction-relative source/manifests/build/evidence/output file map above.
  The agent is distinct from the rejected 4AM implementer and every 4AM/4AN
  reviewer and must not edit repository files.
- [ ] Copy the exact paired-Task case block into
  `manifests/tsdc-4an-cases.jsonl` and first implement the fake Git, fixtures,
  negative controls, and harness oracles. Each case has one deliberate bad
  witness that the oracle must reject and one corrected witness that must pass;
  a case emits its single PASS only after both results are observed.
- [ ] Negative controls never weaken the live containment. Filesystem, Git,
  and partition controls use vulnerable fake implementations inside the fake
  root. Containment controls use offline policy fixtures plus sacrificial
  post-seccomp children whose forbidden syscall must be killed or denied; no
  child receives a host namespace, mount, network, production-path, or extra-FD
  capability. Canonical production path strings remain launcher-only and are
  not copied into the runtime or case manifest; `AN-C015` binds the launcher's
  sealed FD-`3` proof, controller cross-check, and generic fake-root path
  witness. Privilege/process cases bind the launcher's zero-capability,
  exact-worker-pool, no-clone, and derived-limit evidence. Positive controls
  operate only on `/runtime` and
  `/work`.
- [ ] Author the two exact environment manifests, the policy/runtime manifests,
  the controller-request encoder/parser and hostile grammar fixtures, the
  controller, launcher, object-store/support libraries, and
  an intentionally non-accepting builder stub before filling the production
  builder behavior. Do not render the dynamic controller request before the
  two source reports exist. Static source inspection
  must show the fixed evidence-owner rule is total and disjoint: `AN-C015` is
  joint; `AN-C017` through `AN-C020`, `AN-C036`, and `AN-C037` are
  launcher-evidenced; and every other case is harness-evidenced. The harness
  alone emits all ordered case lines after
  verifying sealed launcher evidence. Every `domain=git-reader` row additionally
  owns exactly its four predeclared negative-metadata, negative-content,
  positive-metadata, and positive-content worker tuples, but its sole ledger PASS is
  still emitted by the harness. Every harness-evidenced case is referenced once
  by its implementation, launcher-evidenced cases are referenced once by the
  preflight state machine and once by the verifier/emitter, and neither side
  uses source-code self-discovery as its acceptance list.
- [ ] Complete the smallest builder implementation that makes all manifest
  cases pass without changing the case manifest or harness oracle. The builder
  implements `tsdc-4an-projection-inventory/v2`, exact fragment partitioning,
  occurrence/subspan bijection, AM-P043 historical preservation, and the exact
  inventory/preimage grammar while reading and writing only its fixed FDs. The
  controller and shared support code separately implement closed Git reads,
  create-only output setup, object durability, and receipt-last publication.
- [ ] Freeze the complete source/manifests in an isolated bare review object
  store located inside the private transaction. That object store has no
  alternates and is not the production common Git object store. Every source
  object is addressed by full OID and its receipt also binds SHA256/bytes/mode.

Expected RED evidence is structural and isolated: every deliberate bad witness
maps to its declared reject domain, while the builder stub cannot produce
`HARNESS_STATUS PASS`. No unreviewed harness process runs in AN-2A.

#### AN-2B — Reproducibly build and freeze the static executable closure

- [ ] Map `TX_FD` to descriptor 10 only for the build subprocess. Run absolute
  `/usr/bin/cc` twice under `env -i`, `LC_ALL=C`, `LANG=C`, `TZ=UTC`, and the
  same frozen sources with `-std=c17 -D_GNU_SOURCE -O2 -static-pie
  -fstack-protector-strong -D_FORTIFY_SOURCE=3 -fno-strict-overflow
  -fno-record-gcc-switches -Wdate-time -Werror=date-time
  -ffile-prefix-map=/proc/self/fd/10=. -fmacro-prefix-map=/proc/self/fd/10=.
  -Wl,--build-id=none,-z,noexecstack,-z,relro,-z,now`. Every compilation uses
  exactly one translation-unit-specific argument:
  `-frandom-seed=tsdc-4an-support`,
  `-frandom-seed=tsdc-4an-object-store`,
  `-frandom-seed=tsdc-4an-controller`,
  `-frandom-seed=tsdc-4an-inventory-core`,
  `-frandom-seed=tsdc-4an-inventory-builder`,
  `-frandom-seed=tsdc-4an-containment-launcher`,
  `-frandom-seed=tsdc-4an-adversarial-harness`, and
  `-frandom-seed=tsdc-4an-fake-git`. The harness object links only into the
  launcher. Within each build slot, the exact ordered final link inputs are:
  controller = `controller.o support.o object-store.o -lz`; builder =
  `inventory-builder.o inventory-core.o support.o -lz`; launcher =
  `containment-launcher.o adversarial-harness.o inventory-core.o support.o
  object-store.o -lz`;
  and fake Git = `fake-git.o support.o -lz`. No object from build A may enter
  build B or vice versa. The eight A/B objects and four A/B final binaries are
  written independently to `build-a` and `build-b`. Each corresponding A/B argv differs
  only in its build-slot output token, and both use exact
  `SOURCE_DATE_EPOCH=0` in the otherwise closed environment. No shell lookup or
  network/dependency command runs.
- [ ] Before either build, run a separate bounded read-only toolchain discovery
  phase under the same closed environment. Exact `/usr/bin/cc -dumpmachine`,
  `-dumpfullversion -dumpversion`, and `-dumpspecs` calls have stdout caps
  `256`, `256`, and `1048576` bytes and empty stderr; exact
  `-print-prog-name=ld` plus `-print-file-name=` queries for `Scrt1.o`,
  `crti.o`, `crtbeginS.o`, `crtendS.o`, `crtn.o`, `libgcc.a`, `libc.a`, and
  `libz.a` each return one absolute LF-terminated path within `4096` bytes and
  empty stderr. Separate `/usr/bin/cc -###` invocations cover all eight compile
  argvs and four final link argvs, execute no compiler phase, require empty
  stdout, cap stderr at `262144` bytes, and are parsed by the exact C-locale
  quoted-token grammar recorded in the policy manifest. The lexer rejects a
  response file, relative stage executable, `-specs`, `-B`, wrapper, plugin,
  unknown stage, control byte, shell operator, substitution, or input/output
  outside the frozen source/build slots. Expanded argvs may resolve only to
  already queried compiler/assembler/linker/startup/archive descriptors.
  Discovery output is evidence, never mixed with the actual-build empty-output
  contract.
- [ ] Open `/usr/bin/cc`, its resolved compiler executable, specs source when
  present, linker, every startup object, and every static archive once with
  no-follow regular-file checks. Record device/inode/owner/mode/SHA256/bytes
  before discovery, after discovery, after build A, and after build B; any
  change or path/descriptor divergence fails. The build receipt stores both
  complete ordered sets of eight compile argvs and four link argvs plus their
  env vectors, all eight explicit random seeds,
  bounded discovery digests, and the exact descriptor closure.
- [ ] Require exit zero, empty bounded stdout/stderr, and byte-identical A/B
  corresponding objects and final binaries. Hash and Git-blob-ID every
  toolchain/source/input/output descriptor;
  record the exact compiler-expanded link argv and the startup/static archive
  closure in the build receipt.
- [ ] Parse each ELF with the launcher's bounded parser and require the exact
  policy above. Corroborate with `/usr/bin/readelf -h -l -d -W` and
  `/usr/bin/objdump -p`, but never execute `ldd`; advisory tool output cannot
  override the bounded parser.
- [ ] Add negative ELF fixtures for a shebang, `PT_INTERP`, dynamic dependency,
  wrong architecture/class, truncated or overflowed program headers, W+X load
  segment, and executable stack. The parser must reject every fixture before
  any exec attempt.
- [ ] Freeze binaries, build receipt, manifests, and source objects into the
  isolated review object store. Any A/B mismatch, build diagnostic, ELF-policy
  defect, toolchain drift, or receipt ambiguity stops without harness or
  production execution.

Expected GREEN build evidence is one deterministic receipt binding two equal
builds of each binary and zero accepted negative ELF fixtures. It is not
production-builder evidence.

#### AN-2C — Obtain two fresh immutable source/executable/policy reviews

- [ ] Assign fresh pairwise-distinct read-only identities `AN_SOURCE_SPEC` and
  `AN_SOURCE_QS`; neither may equal the implementer, a rejected 4AM identity,
  a S_AN design reviewer, or either future final-asset reviewer.
- [ ] Both reviewers consume the same isolated source-package Git object and
  its full-OID children, not mutable pathnames. They verify source/binary
  correspondence for all eight translation units and four executables, exact
  controller/launcher/builder
  interfaces and state machine, exact cases, output/object-durability state
  machine, bounded Git reader plus config/alternates race closure, exact v2 and
  preimage grammar, partition proof, reproducible toolchain discovery and
  seeds, ELF/memfd policy, namespace ordering, UID/GID maps, zero
  capabilities/groups, locked securebits, dumpability/process limit,
  exact `G=13` derivation, 52 four-role one-shot workers, five role-bound
  sacrificial denials, peak `4G+6`, final `4G+4`/`16G+16` limits,
  mount/pivot/old-root detachment, FD closure, exact environments, Landlock,
  seccomp architecture/default denial, and no fallback.
- [ ] Each report is canonical LF-delimited evidence stored in the isolated
  review object store by the governance orchestrator with create-only semantics
  only after the read-only reviewer returns it. It binds reviewer assignment,
  source package OID, every reviewed child identity, verdict, readiness, and
  findings. The orchestrator then renders the one dynamic controller request;
  neither reports nor request are inserted into the source package. At
  controller start, FDs `16` and `17` and the request are independently
  rehashed, reparsed, and cross-bound before the controller stores its own
  accepted report copies. Any reviewer file/object write, report mutation,
  missing field, identity collision, request/package/report dependency cycle,
  or verdict other than `C0/I0/M0` stops before launcher execution.

#### AN-2D — Run the fake-only adversarial harness exactly once

- [ ] The governance process opens the exact reviewed controller ELF once,
  proves its source-package identity and bounded static-ELF policy, copies only
  those bytes into `MFD_ALLOW_SEALING|MFD_CLOEXEC|MFD_EXEC`, applies and
  verifies all four write/grow/shrink/seal seals, rereads/reproves the memfd,
  precreates bounded stdout/stderr and the FD-`22` final-review socketpair, and
  creates exactly one controller child with
  `clone3(flags=CLONE_PIDFD, exit_signal=SIGCHLD)` and all other fields zero.
  Only that child installs the exact controller FD map and performs one
  `execveat(..., AT_EMPTY_PATH)` with one-entry argv and zero-entry envp. The
  governance orchestrator retains the controller pidfd, capture endpoints, and
  FD-`22` peer so it can coordinate the later final reviews without a second
  controller start. The
  controller rehashes its inherited sealed self FD before entering
  `INPUTS_BOUND`; a pathname execution, external interpreter, mutable helper,
  missing seal, or second controller start is non-accepting.
- [ ] The controller rebinds exact current E_AN, its sole-parent P_AN, both
  exact Task blobs, the source package, both accepted reports,
  runtime file identities, exact case set from the P_AN Task blob, and the
  empty/58-byte environments before execution. It opens every input once with
  no-follow bounded descriptor checks and maps only FDs `0` through `8` as
  specified above.
- [ ] Copy and seal the exact launcher ELF in an executable memfd, require all
  four seals, create the sole pidfd-bound launcher child as specified above,
  and let only that child call `execveat(..., AT_EMPTY_PATH)` with the one-entry
  argv and zero-entry envp. The controller remains alive to reap it. The
  launcher must emit the complete PASS preflight before
  any harness instruction and must have no weaker path if a primitive fails.
- [ ] Execute the reviewed harness once in the dedicated namespaces and
  pivoted fake-only root. Require exit zero, no signal/timeout, empty bounded
  stderr, the exact preflight field set, exactly one ordered PASS line per
  paired-Task case ID, no missing/duplicate/unknown/non-pass case, and final
  `HARNESS_STATUS PASS`.
- [ ] Reprove from the controller that the sandbox never held a production
  Task/common-Git/object-store descriptor or mount and had no network route.
  The canonical production path strings used for the trusted negative probes
  are absent from the runtime/case manifests and disappear with the launcher
  at harness activation.
  Preserve the exact preflight/ledger bytes as isolated evidence. Do not rerun
  to cure a failed case or lost output.

Expected success output is the exact preflight receipt, same-image post-drop
privilege receipt, exact case-set ledger, and `HARNESS_STATUS PASS` in that
order; stderr
is zero bytes. A nonzero exit,
signal, timeout, extra byte, or set mismatch is failure even if other lines say
PASS.

#### AN-2E — Execute exactly one production builder invocation

- [ ] Only after AN-2D accepts, reprove exact current E_AN topology, its
  sole-parent P_AN/unchanged Plan relation, and open the production common Git
  directory, exact historical P_AN Task blob, absolute Git
  executable, and the exact repo-support parent once. Host directory/file
  opens use one post-harness root descriptor plus the manifest's exact relative
  components under
  `RESOLVE_BENEATH|RESOLVE_NO_SYMLINKS|RESOLVE_NO_MAGICLINKS|RESOLVE_NO_XDEV`,
  and every captured/opened device/inode/type/owner/mode identity must match;
  no `.git` indirection or mutable path rediscovery is accepted. Reject a nonempty
  `objects/info/alternates` before starting. Record the object-store baseline
  without claiming that later failure leaves it unchanged.
- [ ] The controller constructs Git subprocess envp from scratch with exactly
  `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_CONFIG_GLOBAL=/dev/null`,
  `GIT_CONFIG_NOSYSTEM=1`, `GIT_NO_REPLACE_OBJECTS=1`,
  `GIT_OPTIONAL_LOCKS=0`,
  `GIT_TERMINAL_PROMPT=0`, `HOME` and `XDG_CONFIG_HOME` pointing to proved
  empty private directories, `TMPDIR` pointing to a proved private directory,
  `PATH=/nonexistent`, `GIT_CONFIG_COUNT=0`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`, the exact private
  `GIT_DIR`, and descriptor-backed `GIT_OBJECT_DIRECTORY` defined above. It
  uses the absolute Git executable with supported global options
  `--no-replace-objects --no-optional-locks`; the private Git control directory
  and descriptor-backed object view replace any version-specific lazy-fetch
  option.
- [ ] Metadata is one bounded `cat-file --batch-check` request requiring the
  full requested OID, type `blob`, and exact byte count. Content is one
  nonblocking `cat-file blob <full-oid>` stream with stdout cap
  `expected_bytes+1`, bounded stderr, monotonic deadline, kill/reap on failure,
  and simultaneous SHA256/Git-blob recomputation into one sealed Task memfd.
  The controller drains all configuration/alternates watches after metadata
  and content children and before accepting the memfd. No prompt, replacement,
  alternate, lazy fetch, short/extra content, config/watch event, or unbounded
  buffer is accepted.
- [ ] After the Task memfd is accepted, the controller creates exact `OUT_FD`
  by the independent 128-bit/open-once contract. Relative to that FD it creates
  only `tsdc-4an-projection-inventory.jsonl` and
  `tsdc-4an-projection-preimage.txt` with
  `O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC`, mode `0600`. Every child is a new
  same-device regular inode owned by the effective UID/GID, link count one,
  with no group/world bits; `fchmod(0600)` and same-FD reproof precede use.
  The reviewed builder is then invoked exactly once with the fixed request,
  sealed Task FD, and these two output FDs. It cannot see the directory FD or
  any production pathname.
- [ ] Require builder exit zero, no signal/timeout, empty bounded diagnostic,
  and exact canonical result. Rewind, reread, hash, length-check, and fsync both
  payloads through the same FDs. Materialize and durably reprove their loose
  Git objects with the controller algorithm. Only after both durable proofs and
  a fresh config/alternates watch drain may the controller create the exact
  receipt file under `OUT_FD`, write/fsync/reprove it, materialize its object
  last, require exactly three regular output entries and no extras, and fsync
  `OUT_FD`. No truncation, pathname reopen, cleanup, rebuild, or retry is
  allowed.
- [ ] Require process exit zero, no signal/timeout, empty bounded stderr, one
  canonical completion receipt, and exact inventory/preimage/receipt
  SHA256/blob/byte identities. Failure preserves the private transaction,
  attempted OIDs, possible unreachable production blobs, observed topology,
  and bounded diagnostics for explicit disposition.

No raw stdout/stderr, credentials, environment dump, shell history, or secret
value is written under `_workspace`. Failure preservation records only the
canonical non-secret failure code, bounded byte counts, hashes, attempted OIDs,
and proved topology fields; raw diagnostic bytes remain memory-only and are
discarded after their bounded digest is recorded.

#### AN-2F — Reprove the complete pair and obtain final asset reviews

- [ ] Independently stream exact P_AN Task, inventory, preimage, and receipt
  objects through the bounded reader. Recompute the full-document discovery,
  fragment/subspan byte partition, occurrence bijection, typed P_AN/B_AN/XP_AN
  expectations, stale denylist, aggregate derived counts, and exact AM-P043
  historical hashes. Require the receipt to bind exact P_AN Task and accepted
  builder/source-package identities.
- [ ] Assign fresh pairwise-distinct read-only identities `AN_ASSET_SPEC` and
  `AN_ASSET_QS`, distinct from every implementer/source/design/4AM reviewer.
  After the still-running controller emits `ASSET_REVIEW_READY`, both consume
  the same frozen receipt-bound exact objects while the controller makes no
  change to that input set. Their reports bind all identities, the harness
  receipt/ledger, verdict, readiness, and findings. The governance orchestrator
  copies each exact returned byte string into its own sealed memfd and submits
  the two descriptors once over the FD-`22` protocol; only the controller may
  materialize returned final-report bytes in the isolated object store. A
  reviewer write, report resubmission, or review-input mutation invalidates
  that review.
- [ ] Accept AN-2 only when both reports are complete `C0/I0/M0` with
  affirmative asset readiness, the controller reaches `COMPLETE`, and the
  governance orchestrator reaps that sole controller child exactly once with
  empty bounded stderr and the canonical completion envelope. Freeze all
  evidence and continue only to the
  bounded R_AN evidence checkpoint in AN-2G. This success does not authorize
  renderer source, terminal reviews, B_AN/XP_AN, publisher execution,
  repository tests/validators, or any downstream work.

#### AN-2G — Publish exactly one Task-only AN-2 evidence terminal

- [ ] For accepted AN-2 evidence, render R_AN from exact E_AN with exact
  subject `docs(task): record accepted secure inventory evidence`. It changes
  only the Task as mode `100644`, preserves the P_AN Plan blob/mode exactly,
  has E_AN as its sole parent, and records the exact E_AN and P_AN identities,
  accepted P_AN review pair, source package and build closure, four executable
  identities, six input manifests, the dynamic controller-request identity,
  source-review pair, one controller activation, one harness activation,
  preflight/privilege/ledger hashes, complete case bijection, one production
  builder invocation, inventory/preimage/pair-receipt/production-run identities
  and durability states, final asset-review pair, `completion=ACCEPTED`, and
  the authority boundary below.
- [ ] For a classified non-security failure, create XE_AN only after the user
  explicitly approves the exact safe disposition. Its exact subject is
  `docs(task): record exhausted secure inventory evidence`; it has the same
  Task-only/mode/Plan-preservation/single-parent rules and records the first
  canonical failure code, last completed state, retained non-secret identity
  hashes, skipped steps/reviews, no-rerun fact, disposition identity, and
  `completion=EXHAUSTED`. It never claims absence of mutation unless the
  bounded read-only reproof established it. A security incident, raw-secret
  exposure, foreign drift, ambiguous object-store result, or unclassified
  topology creates no automatic XE_AN commit.
- [ ] Assign one fresh read-only terminal-evidence verifier, distinct from the
  implementer and all Plan/source/asset reviewers. Freeze the candidate Task
  SHA256/bytes/blob and `E_AN..terminal` binary diff; require exact evidence
  correspondence, `C0/I0/M0`, and affirmative terminal readiness. Prove exact
  unique subject, sole parent E_AN, unchanged Plan blob, Task-only path set,
  ordinary mode `100644`, no self OID, and current branch/index/worktree
  cleanliness before and after expected-old ref publication. R_AN and XE_AN
  are mutually exclusive and neither may be reconstructed or retried after an
  ambiguous publication result without read-only resolution and new approval.

R_AN authorizes only a new user decision on drafting an AN-3 renderer Plan.
XE_AN authorizes only the recorded disposition or a separately approved
return-to-design successor. Because either terminal changes the Task bytes,
AN-3 must rediscover and review the exact R_AN Task; the historical P_AN-bound
inventory is evidence for AN-2 and is not a current-Task renderer inventory.

#### P_AN execution failure matrix

| Failure point | Durable result | Next authority |
| --- | --- | --- |
| P_AN review/publication/exact-object rebind, user execution approval, or E_AN render/review/publication/rebind fails | S_AN/P_AN remains current or the exact observed foreign state is preserved | stop; no AN-2 asset may be created |
| Private parent/transaction, source freeze, reproducible build, ELF policy, or source-package proof fails | no harness or production invocation; proved-owned isolated evidence may remain | preserve; after explicit safe disposition, XE_AN may record exhaustion; no cleanup/rebuild/retry without separate approval |
| Either source/executable/policy review is not complete `C0/I0/M0` | frozen isolated assets remain non-accepted; no launcher or production invocation | after explicit safe disposition, XE_AN may record exhaustion; otherwise stop |
| Seal/direct exec, namespace, ID map, mount/root, FD, environment, Landlock, seccomp, preflight, or negative-reachability proof fails | no untrusted harness or production invocation; exact isolated evidence retained | fail before harness with no fallback; after explicit safe disposition, XE_AN may record exhaustion |
| Harness case/ledger/process contract fails while fake-only isolation is proved | no production invocation or production object-store write | preserve isolated evidence; after explicit safe disposition, XE_AN may record exhaustion; no cleanup/rerun/retry |
| Fake-only isolation is unproved or a production path/object/descriptor/network access is observed | no absence-of-mutation claim; exact repository/object-store/topology and diagnostics preserved | stop as a security incident; no further access, cleanup, production invocation, or retry |
| Git reader, production builder, private file, fsync, object write, or receipt proof fails | no accepted pair; preserve incomplete private transaction, attempted OIDs, possible unreachable blobs, foreign drift, and bounded diagnostics | read-only reproof first; XE_AN only after an explicit disposition proves the state safe to summarize; never delete/cleanup/rebuild/rerun automatically |
| Fragment/subspan/occurrence partition or independent reproof fails | receipt-bound bytes remain rejected evidence only | after explicit safe disposition, XE_AN may record exhaustion; otherwise stop |
| Either final asset review is not complete `C0/I0/M0` | E_AN remains current and AN-3 is unauthorized | after explicit safe disposition, XE_AN may record exhaustion; otherwise stop |
| Both final asset reviews pass | exact source/package/harness/receipt/assets become immutable P_AN-bound evidence | render, independently verify, publish, and rebind R_AN; then stop for a separate AN-3 drafting decision |
| R_AN/XE_AN render, verification, publication, or rebind fails | exact E_AN or observed foreign state and all frozen evidence are preserved | stop; no terminal retry without read-only resolution and new approval |

#### P_AN approval and execution boundary

This P_AN tree is planning evidence only until its exact candidate receives two
fresh independent `C0/I0/M0` Plan reviews, is published from exact S_AN, is
rebound by its full OID and exact two blobs, and the user explicitly selects
execution. That approval is first recorded and independently verified in
Task-only E_AN; AN-2A has no authority from P_AN alone. The selected execution
mode is Subagent-Driven: AN-2A uses one fresh implementation agent, every
review uses a fresh read-only identity, and the controller stops at each
review/failure boundary. No P_AN drafting or
approval implicitly runs an asset, repository validator/test, wrapper,
pre-commit, Graphify, runtime, remote action, or dependency command.

The planning commit for this unit is P_AN. After the user's execution
approval, E_AN is the one Task-only execution-gate commit. AN-2A through AN-2G
are one bounded out-of-tree evidence transaction and create no tracked source
or Plan change. AN-2G publishes exactly one Task-only evidence terminal:
R_AN for accepted evidence, or XE_AN after an explicitly approved safe
failure disposition. A security incident or unclassified/ambiguous state
creates neither terminal automatically. No AN-3 work starts in this Plan.

## Verification Plan

### Per-task Gate

Every task must provide:

1. a clean starting commit and scoped ownership;
2. the named RED tests and expected failure;
3. the smallest GREEN implementation;
4. native syntax and focused contract checks;
5. value-free evidence in the Task ledger;
6. one independently revertible commit per logical implementation unit;
7. independent specification review;
8. independent quality/security review;
9. remediation and re-review for all Critical and Important findings.

### Cross-task Invariants

- Spec 133 evidence remains byte-identical.
- The successor manifest covers the complete current delta.
- Native formats remain free of Markdown metadata.
- README and typed documents have one exact consumer.
- Root content archive and Stage 98 SDLC archive remain distinct.
- Secret values never enter commands, output, tests, or evidence.
- The six version changes are static tracked synchronization only.
- The 16 required job IDs never change.
- `.github/workflow-contract.yml` is the one schema-v2 CI registry; no
  generated or code-owned duplicate command table exists.
- Every required semantic `suite_key` belongs to one leaf, one required root,
  and at most one workflow execution path.
- Required-quality `run` steps are exact static gate-runner invocations.
- CI and local profiles share node definitions and differ only in registered
  roots.
- CI-only Compose setup is unreachable from local profiles, and local
  execution preserves an existing ignored `.env` byte-for-byte.
- Stateful setup/leaf chains such as Storybook coverage execute under one
  complete runner lifetime and one fresh HOME.
- The runner uses `shell=False`, descriptor-bound repository paths, tracked
  executable provenance, bounded timeouts, minimal environment, and no ambient
  `GIT_*`.
- CI pre-commit and Agent pre-commit remain separate authority paths.
- Remote GitHub state remains observed, not mutated.
- Canonical audit claims remain bounded by actual evidence.

## Risks and Rollback

| Risk | Guardrail | Rollback |
| --- | --- | --- |
| Predecessor evidence rewritten | closure-commit hash tests | revert the offending task; never regenerate Spec 133 |
| Changed target omitted | Git delta plus worktree union | add the missing reviewed row before promotion |
| README policy duplication | exact heading/owner tests | revert the affected README task |
| Topic content lost | service-specific preservation tests and review | restore exact file from task parent, then reapply scoped normalization |
| Secret exposure | path-only readers, bounded diagnostics, no raw logs | stop, remove exposed evidence, rotate externally only under separate authority |
| Version owner duplication | Compose → curated registry → generated provenance chain | revert Task 3; do not change Compose runtime |
| CI status name drift | four-way exact ID contract | revert Task 4 before remote use |
| Workflow privilege widening | typed permission/trigger validator | revert Task 4 and keep remote unchanged |
| Action dependency drift | full-SHA registry and runtime check | revert Action consumer and registry together |
| Registry bootstrap depends on an uninstalled YAML package | strict JSON serialization in the one `.yml` registry and standard-library reader | revert the R2 schema conversion; keep current workflow active |
| Wave A runner is exercised before schema-v2 cutover | temporary strict-JSON fixtures only during early R2; first canonical runner command occurs after R2 completes the schema-v2 conversion | revert R2 if fixture-bound CLI tests are not isolated |
| Gate graph duplicates or omits a suite | unique `suite_key`, root reachability, cycle/orphan checks, and fake executor | revert the owning R1/R3 unit |
| Workflow bypasses typed execution | exact single-line projection and Action registry | revert R3 before remote use |
| Entrypoint or cwd is redirected | descriptor-relative no-follow traversal, tracked mode, verified identity, and fail-closed `/proc/self/fd` requirement | revert R2 and block cutover |
| Descriptor execution changes script-relative root or imports | fixed runner-created root/Python path plus exact compatibility migrations and descriptor smoke tests | revert the compatibility edits and block R3 |
| Local Compose setup overwrites ignored `.env` | local-only aggregates exclude CI setup; byte-preservation regression | stop local cutover and restore prior local routing |
| Stateful setup data disappears between workflow steps | one root invocation and one HOME for each stateful plan | revert the affected job projection |
| Ambient Git or secret-shaped environment changes execution | construct minimal environment, clear ambient `GIT_*`, reject secret-shaped keys | stop execution and correct the node contract |
| Dead semantic interpreter is reactivated or retained | Wave A removes its authority/table, R3 uses only structural projection, and R4 approval precedes the R5 symbol-removal gate | leave Task 4R blocked; do not start Task 5 |
| Audit overclaim | local/remote/unverified schema | correct the affected audit row and regenerate owners |
| Reviewer mutation | explicit read-only review role | discard no work; inspect and separately authorize any reviewer-created commit |

Rollback uses task-level `git revert` after reviewing the exact range. No
rollback command may discard unrelated user work. Remote or runtime rollback
is not applicable because neither surface is mutated.

## Approval Gates

- Original Spec 135, the 2026-07-28 Plan, and Tasks 1–3 are approved historical
  execution.
- The typed CI design at Spec commit `a0f91bb5` is approved.
- The 2026-07-28 Plan approval does not authorize T-TSDC-004R after the
  exhausted five-round breaker.
- The user approved Revision R1 on 2026-07-29. Its two-attempt Plan review
  loop remained blocked and returned to design/plan.
- Revision R2 and successors through 4AF are historical. 4AF's sole
  implementation is frozen evidence and its rejected quality/security review
  grants no Wave C or downstream authority.
- 4AG is rejected/exhausted at XP_AG and is preserved only as historical
  evidence. Its rejected terminal grants no correction or downstream authority.
- 4AH is rejected/exhausted at XP_AH
  `88f55837be251318cd697bd8a1ab3a4f0ed1a824`. Its split-session design and all
  4AH blocks are historical, non-executable evidence; B_AH, E_AH, R_AH, and
  XE_AH were not created.
- 4AI is rejected/exhausted historical evidence only; it grants no current
  authority. The rejected 4AK draft is historical only and was reversed to
  clean D_AL. 4AL reached exact P_AL
  `fb05e296b6a791f850cf64d99c7dc17577bb7cfc`, then failed closed at terminal
  pre-publication proof after its immutable review set selected XP_AL. No 4AL
  publisher ran and no B_AL/XP_AL commit exists.
- The 4AM topology stopped at exact P_AM
  `143b5efe9b68d8688770b10c82fc3e4a9616bc66`. Its AM-2 specification review
  passed C0/I0/M0, but quality/security failed C0/I3/M0, so AM-3, B_AM, and
  XP_AM are unauthorized/uncreated and the rejected blobs remain historical
  evidence only.
- The current planning topology is
  `D_AN/P_AM -> S_AN -> P_AN -> E_AN -> R_AN|XE_AN`. S_AN is exact
  `bac234abf9e1e320d2311b8a8f448afe0a6cbac1`; its final written-design reviews
  are C0/I0/M0 and the user approved P_AN drafting. The P_AN tree intentionally
  asserts neither its own post-publication OID/currentness, corrected Plan
  review outcome, publication/rebinding result, user execution decision, nor
  any AN-2 start/result. Those facts become authoritative only in exact E_AN.
  E_AN may be created only after they exist. Every 4AN asset,
  source/final asset review, R_AN/XE_AN evidence terminal, AN-3 renderer,
  immutable renderer-terminal review, publisher, B_AN, and XP_AN is not
  started/not created. implementation,
  E_AL, R_AL, XE_AL, E_AM, R_AM,
  XE_AM, AN-3, Task 4.5, Wave C, Tasks 5–6, runtime,
  remote/external actions, QA-wrapper/pre-commit execution, dependency changes,
  4AL/4AM retry or correction, and Graphify update are blocked/no authority.
- Remote mutation, live runtime work, push, pull request, merge, workflow
  dispatch, credential change, and raw-log access remain separately gated.
- A controlled final Agent all-files wrapper attempt requires a new exact
  approval after a clean committed checkpoint. No prior approval carries
  forward.

## Completion Criteria

- TSDC-001 through TSDC-017 have named passing evidence.
- Every completed top-level task and R1 recovery unit has independently
  revertible logical commits; historical remediation commits remain preserved.
- Every task has independent specification and quality/security approval.
- The delta manifest is blocking, complete, duplicate-safe, and green.
- Spec 133 artifacts are unchanged from their closure commit.
- README, typed fixture, archive, secret inventory, and version contracts pass.
- Workflow triggers, permissions, jobs, Action dependencies, typed gate
  registry/DAG, runner security, CI/local projections, and CI QA pass.
- The 16 required job IDs are unchanged.
- `owner_commands`, `expensive_commands`, and the shell/Python semantic
  interpreter are absent after the reviewed cutover.
- Canonical audit/generated evidence is fresh and does not overclaim remote or
  runtime state.
- A fresh whole-branch correctness review and a different security review have
  no unresolved Critical or Important findings.
- Plan and Task are terminal only after the evidence is committed.
- The branch remains local unless the user separately authorizes integration.

## Related Documents

- [Spec 135](spec.md)
- [Task ledger](task.md)
- [Spec 133](../spec-0133-target-surface-contract-convergence/spec.md)
- [Spec 134](../spec-0134-agent-governance-canonical-convergence/spec.md)
- [Canonical audit](../../90.references/audits/ref-0019-readme.md)
- [GitHub governance](../../00.agent-governance/policies/github-governance.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Workflow contract](../../../.github/workflow-contract.yml)
- [Repository contract checker](../../../scripts/validation/check-repo-contracts.sh)
- [Controlled Agent pre-commit wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
