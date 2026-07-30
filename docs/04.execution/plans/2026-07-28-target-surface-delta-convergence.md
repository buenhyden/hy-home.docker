---
status: active
artifact_id: plan:2026-07-28-target-surface-delta-convergence
artifact_type: plan
parent_ids:
  - spec:135-target-surface-delta-convergence
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
command capture/evidence envelope. Tests, revalidation, E_AG, R_AG, and Wave C
remain blocked until accepted B_AG exists and the user separately approves one
evidence-only revalidation attempt. Remote, runtime, dependency, secret,
direct pre-commit, controlled-wrapper, and Graphify-update authority remain
unchanged.

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
  `docs/00.agent-governance/contracts/provider-models.yaml`, each with
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
[Spec 135](../../03.specs/135-target-surface-delta-convergence/spec.md)
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
[Task ledger](../tasks/2026-07-28-target-surface-delta-convergence.md)
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

- [Spec 135](../../03.specs/135-target-surface-delta-convergence/spec.md)
- [Spec 133](../../03.specs/133-target-surface-contract-convergence/spec.md)
- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- [Approval boundaries](../../00.agent-governance/rules/approval-boundaries.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Existing target-surface manifest](../../90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml)
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
  `docs/90.references/data/governance/target-surface-delta-manifest.yaml`.
- Create
  `docs/90.references/data/governance/target-surface-delta-summary.md`.
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
  `docs/00.agent-governance/rules/agentic.md` and
  `docs/00.agent-governance/rules/documentation-protocol.md`.
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
  `docs/90.references/data/docker/tech-stack-version-provenance.md`.
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
  `docs/05.operations/guides/06-observability/alloy.md`,
  `docs/05.operations/guides/06-observability/prometheus.md`,
  `docs/05.operations/policies/06-observability/alloy.md`,
  `docs/05.operations/policies/06-observability/prometheus.md`, and
  `docs/05.operations/runbooks/06-observability/alloy.md`.
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
| `leaf.local-llm-wiki-index-freshness` | `local-llm-wiki-index-freshness` | `scripts/knowledge/generate-llm-wiki-index.sh` | `--check` |
| `leaf.local-llm-wiki-coverage-freshness` | `local-llm-wiki-coverage-freshness` | `scripts/knowledge/generate-llm-wiki-coverage.sh` | `--check` |

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
  `docs/90.references/data/governance/target-surface-delta-manifest.yaml`
  with exact new-path rows.
- Regenerate
  `docs/90.references/data/governance/target-surface-delta-summary.md`.
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md \
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md \
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
git diff --exit-code 17bb5cdd -- docs/90.references/data/governance/target-surface-delta-manifest.yaml docs/90.references/data/governance/target-surface-delta-summary.md
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
git diff --exit-code 17bb5cdd -- docs/90.references/data/governance/target-surface-delta-manifest.yaml docs/90.references/data/governance/target-surface-delta-summary.md
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md
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
- Modify `docs/00.agent-governance/rules/github-governance.md` and
  `docs/00.agent-governance/scopes/qa.md`.
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
  docs/00.agent-governance/rules/github-governance.md \
  docs/00.agent-governance/scopes/qa.md \
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md \
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

#### Task 4.5 / Wave C / T-TSDC-004R-5: Remove the Old Semantic Interpreter

- [ ] **Step 0: Re-extract the three canonical rows and prove the complete
  accepted 4AG chain.**

  Before any Wave C change, run this active prerequisite. It extracts exactly
  the three 4AG canonical rows, accepts only completed C0/I0/M0 evidence,
  proves `B_4AF -> I -> D_AG -> P_AG -> B_AG -> E_AG -> R_AG`, and binds the
  current test blob to historical I:

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
authority_ranges="$(
  python3 - "$task_file" <<'PY'
import pathlib
import re
import sys

labels = (
    "T-TSDC-004R-4AG status-based silent-success Plan",
    "T-TSDC-004R-4AG frozen canonical-row implementation",
    "T-TSDC-004R-4AG status-based revalidation",
)
try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit("authority-read")
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
    raise SystemExit("authority-row-count")
rows = []
for label in labels:
    row = found[label][0]
    if not row.startswith("|") or not row.endswith("|"):
        raise SystemExit("authority-cell-count")
    if "\\|" in row or "\\`" in row:
        raise SystemExit("authority-escape")
    parts = row.split("|")
    if len(parts) != 9 or parts[0] or parts[-1]:
        raise SystemExit("authority-cell-count")
    cells = [part.strip(" \t") for part in parts[1:-1]]
    if len(cells) != 7 or cells[0] != label:
        raise SystemExit("authority-label")
    rows.append(cells)
expected_reviews = (
    (
        "C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES",
        "C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES",
    ),
    (
        "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES",
        "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES",
    ),
    (
        "C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES",
        "C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES",
    ),
)
ranges = []
for cells, expected in zip(rows, expected_reviews, strict=True):
    if tuple(cells[2:4]) != expected:
        raise SystemExit("authority-review")
    for index, cell in enumerate(cells):
        if index != 4 and ("`" in cell or ".." in cell):
            raise SystemExit("authority-extra-range")
    match = re.fullmatch(
        r"`([0-9a-f]{40})\.\.([0-9a-f]{40})`",
        cells[4],
        flags=re.ASCII,
    )
    if match is None:
        raise SystemExit("authority-range")
    ranges.append(f"{match.group(1)}..{match.group(2)}")
print("\t".join(ranges))
PY
)"
test -n "$authority_ranges"
plan_review_range="${authority_ranges%%$'\t'*}"
test -n "$plan_review_range"
authority_tail="${authority_ranges#*$'\t'}"
test -n "$authority_tail"
implementation_review_range="${authority_tail%%$'\t'*}"
test -n "$implementation_review_range"
revalidation_review_range="${authority_tail##*$'\t'}"
test -n "$revalidation_review_range"
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
review_checkpoint="$(
  git rev-parse --verify 'HEAD^{commit}'
)"
test -n "$review_checkpoint"
bound_commits=(
  "$implementation_base" "$implementation_commit" "$design_base"
  "$plan_checkpoint" "$evidence_base" "$evidence_checkpoint"
  "$review_checkpoint"
)
expected_subjects=(
  'docs(task): record canonical-row authority plan reviews'
  'fix(ci): close canonical-row authority proof'
  'docs(task): record exhausted canonical-row authority review'
  'docs(plan): define status-based silent-success proof'
  'docs(task): record status-based silent-success plan reviews'
  'docs(task): record status-based silent-success revalidation'
  'docs(task): record status-based silent-success review'
)
for index in "${!bound_commits[@]}"; do
  verified_commit="$(
    git rev-parse --verify "${bound_commits[$index]}^{commit}"
  )"
  test "$verified_commit" = "${bound_commits[$index]}"
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
assert_edge "$evidence_checkpoint" "$review_checkpoint"
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
review_range_paths="$(
  git diff --name-only "$evidence_checkpoint..$review_checkpoint" |
    sort
)"
test "$review_range_paths" = "$task_file"
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
  "$evidence_checkpoint:$test_file" \
  "$review_checkpoint:$task_file" \
  "$review_checkpoint:$test_file"
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
review_blob="$(
  git rev-parse "$review_checkpoint:$test_file"
)"
test "$review_blob" = "$implementation_blob"
head_commit="$(
  git rev-parse HEAD
)"
test "$head_commit" = "$review_checkpoint"
clean_state="$(
  git status --porcelain=v1 --untracked-files=all
)"
test -z "$clean_state"
```

  The accepted R_AG is the only Wave C authority. The former 4AF-only block
  below is retained as non-executable provenance and cannot authorize work.

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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md \
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
  `docs/90.references/data/governance/github-actions-control-plane-observation.yaml`.
- Modify
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md`.
- Modify affected rows only in:
  `implementation-overview.md`,
  `automation-candidates.md`,
  `frontmatter-template-readme-implementation.md`,
  `sdlc-quality-formatting-implementation.md`, and
  `security-framework-maturity.md`.
- Modify
  `docs/90.references/data/governance/audit-implementation-matrix.md`
  only through
  `scripts/validation/generate-audit-implementation-matrix.sh`.
- Modify
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`
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
  --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
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
  --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md \
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
  docs/90.references/data/governance/github-actions-control-plane-observation.yaml \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md \
  docs/90.references/data/governance/audit-implementation-matrix.md \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md \
  scripts/validation/check-repo-contracts.sh \
  tests/validation/test_agent_governance_ci_routing.py \
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md \
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
  `docs/90.references/data/governance/target-surface-delta-manifest.yaml`
  to set `enforcement: blocking` only after Tasks 1–5 have pass/pass reviews.
- Regenerate
  `docs/90.references/data/governance/target-surface-delta-summary.md`.
- Inspect `scripts/validation/check-repo-contracts.sh` and
  `scripts/validation/run-local-qa-gates.sh` with the exact
  `check-target-surface-delta-contract.py --mode advisory` search. Replace each
  matching active invocation with `--mode blocking`; when neither file
  contains that exact active invocation, leave both byte-unchanged and record
  the no-op in the Task ledger.
- Modify this Plan status to `completed`.
- Modify the sibling Task ledger status to `completed` only after all closure
  evidence exists.
- Modify `docs/00.agent-governance/memory/current.md` for the bounded handoff.
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml
rg -c '^  quality_verdict: pending$' \
  docs/90.references/data/governance/target-surface-delta-manifest.yaml
```

  Both counts must equal 158; any existing `pass` or `fail` before this unified
  step is a contract error, proven by:

```bash
if rg -n '^  (spec_verdict|quality_verdict): (pass|fail)$' \
  docs/90.references/data/governance/target-surface-delta-manifest.yaml; then
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml
rg -c '^  quality_verdict: pass$' \
  docs/90.references/data/governance/target-surface-delta-manifest.yaml
```

  Both counts must equal 158, and exact searches for pending or failed review
  verdicts must return no row:

```bash
if rg -n '^  (spec_verdict|quality_verdict): (pending|fail)$' \
  docs/90.references/data/governance/target-surface-delta-manifest.yaml; then
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
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md \
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
  docs/00.agent-governance/memory/current.md
git commit -m "docs(task): close target surface delta convergence"
```

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
- The user's current approval authorizes only the 4AG Plan/Task checkpoint
  P_AG, two fresh independent Plan reviews over exact `D_AG..P_AG`, and one
  accepted B_AG or rejected XP_AG Task-only terminal. It authorizes no test,
  validator, product, workflow, runtime, or remote execution.
- A future status-based evidence-only revalidation requires accepted B_AG plus
  a separate explicit one-attempt approval. That approval may create Task-only
  E_AG and obtain fresh composite reviews; only accepted Task-only R_AG
  authorizes Task 4.5 Wave C. Rejected XP_AG or XE_AG is terminal.
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

- [Spec 135](../../03.specs/135-target-surface-delta-convergence/spec.md)
- [Task ledger](../tasks/2026-07-28-target-surface-delta-convergence.md)
- [Spec 133](../../03.specs/133-target-surface-contract-convergence/spec.md)
- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Canonical audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Workflow contract](../../../.github/workflow-contract.yml)
- [Repository contract checker](../../../scripts/validation/check-repo-contracts.sh)
- [Controlled Agent pre-commit wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
