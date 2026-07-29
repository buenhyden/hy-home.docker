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
specification `C0/I5/M0` and quality/security `C0/I0/M0`; implementation
remains blocked while this bounded correction receives the final second
independent specification and quality/security `C0/I0` review pair.

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
- [ ] Require both final R2 reviews to map TSDC-010 through TSDC-017, verify
  exact file ownership and commands, and return C0/I0 before implementation.

Expected gate: only after Revision R2 approval and both final corrected R2
reviews return C0/I0 does the Task ledger change from
`blocked pending corrected Revision R2 Plan reviews` to `active recovery`; no
production or test file changes before that transition.

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

#### Task 4.5 / Wave C / T-TSDC-004R-5: Remove the Old Semantic Interpreter

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
- Revision R2 requires a new explicit user approval, then fresh independent
  specification and quality/security C0/I0 reviews before any R1 production
  or test file is created or modified.
- After Revision R2 approval and both fresh reviews, protected local workflow,
  contract, governance, and test changes listed under T-TSDC-004R are within
  the Plan-bounded class.
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
