---
status: draft
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
machine authority for exact triggers, jobs, permissions, and direct Action
dependencies, while Stage 90 remains observation/evidence rather than desired
state.

**Tech Stack:** Python 3.12, PyYAML, Bash, JSON, YAML, Markdown/CommonMark,
GitHub Actions, actionlint, ShellCheck, markdownlint-cli2, pre-commit 4.6.1,
unittest, Git, and repository-owned generators.

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
- Each task ends in one independently revertible Conventional Commit.
  Generated-owner fallout belongs to the owning task.
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
through six serial logical tasks:

1. create the successor delta manifest, validator, and whole-surface contract;
2. normalize README, typed example, archive, project, and redacted secret
   documentation;
3. reconcile static version drift and verified active legacy/deprecated
   residue;
4. type and harden local GitHub Actions and QA ownership;
5. refresh canonical audit, generated, and remote-observation evidence;
6. promote enforcement, run the final validation ladder, and close independent
   reviews.

The sibling
[Task ledger](../tasks/2026-07-28-target-surface-delta-convergence.md)
records actual commands, results, commits, deviations, deletion evidence, and
review verdicts. It does not duplicate planned implementation.

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

### External Sources

The implementation retains source URL and 2026-07-28 KST retrieval context
for fast-moving facts:

- GitHub workflow syntax:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub secure use:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- GitHub protected branches:
  <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches>
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
- Preserve exact CI status identities while removing redundant execution.
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
| TSDC-010 | T-TSDC-004 | exact workflow trigger and permission contract |
| TSDC-011 | T-TSDC-004 | unchanged 16-job identity across four owners |
| TSDC-012 | T-TSDC-004 | one CI owner for every expensive semantic gate |
| TSDC-013 | T-TSDC-004 | full-SHA Action registry and Node 20 rejection |
| TSDC-014 | T-TSDC-004 | separate CI and Agent pre-commit authority paths |
| TSDC-015 | T-TSDC-005 | dated local/remote observation with unverified boundaries |
| TSDC-016 | T-TSDC-005, T-TSDC-006 | affected audit rows and generated summaries fresh |
| TSDC-017 | all tasks, T-TSDC-006 | six logical commits, task reviews, whole-branch reviews |

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

```python
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
) -> tuple[str, ...]: ...

def load_delta_manifest(
    root: pathlib.Path,
    path: pathlib.PurePosixPath = DELTA_MANIFEST,
) -> DeltaManifestDocument: ...

def validate_delta_manifest(
    root: pathlib.Path,
    document: DeltaManifestDocument,
) -> tuple[DeltaFinding, ...]: ...

def current_target_inventory(root: pathlib.Path) -> TargetInventory: ...

def render_delta_summary(
    document: DeltaManifestDocument,
    inventory: TargetInventory,
) -> str: ...

def bootstrap_delta_manifest(
    root: pathlib.Path,
    output: pathlib.Path,
    predecessor_commit: str,
    implementation_base_commit: str,
) -> None: ...

def main(argv: list[str] | None = None) -> int: ...
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

### Task 4: T-TSDC-004 — Converge GitHub Actions and QA Control Plane

**Files:**

- Create `.github/workflow-contract.yml`.
- Create `scripts/validation/github_workflow_contract.py`.
- Create `scripts/validation/check-github-workflow-contract.py`.
- Create `tests/validation/test_github_workflow_contract.py`.
- Create `scripts/validation/run-ci-precommit.sh`.
- Create `tests/validation/test_run_ci_precommit.sh`.
- Create `scripts/requirements-pre-commit.txt` with exact
  `pre-commit==4.6.1`.
- Modify `.github/workflows/ci-quality.yml`.
- Modify `.github/rulesets/main-protection.md`.
- Modify `.github/INDEX.md`.
- Modify `docs/00.agent-governance/rules/github-governance.md`.
- Modify `docs/00.agent-governance/scopes/qa.md`.
- Modify `scripts/validation/check-repo-contracts.sh`.
- Modify `scripts/validation/run-local-qa-gates.sh`.
- Modify `scripts/README.md`.
- Modify `tests/validation/test_agent_governance_ci_routing.py`.
- Modify `.pre-commit-config.yaml` routing only if the new checker paths are
  not already selected by the existing repository-contract hook.
- Modify the Task 1 manifest/summary and sibling Task ledger.

**Interfaces:**

```python
@dataclass(frozen=True, order=True, slots=True)
class WorkflowFinding:
    code: str
    path: str
    message: str

@dataclass(frozen=True, slots=True)
class TriggerContract:
    events: tuple[str, ...]
    branches: tuple[str, ...]
    paths: tuple[str, ...]
    schedules: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ActionDependency:
    action: str
    sha: str
    runtime: str
    manifest_url: str
    retrieved_at: str
    consumers: tuple[str, ...]
    security_disposition: str

def load_workflow_contract(root: pathlib.Path) -> WorkflowContract: ...
def load_workflows(root: pathlib.Path) -> tuple[WorkflowDocument, ...]: ...
def validate_workflows(
    root: pathlib.Path,
    contract: WorkflowContract,
) -> tuple[WorkflowFinding, ...]: ...
def main(argv: list[str] | None = None) -> int: ...
```

The contract registers exact event/branch/path/schedule combinations,
permissions, concurrency, timeouts, job IDs, semantic job owner commands, and
direct Action dependencies. It rejects `pull_request_target`, unapproved
`workflow_run`/`workflow_call`, event widening, write-all, permission widening,
mutable Action refs, Node 20, duplicate job identities, missing timeouts, and
unsafe interpolation.

The 16 required IDs remain:

`docs-traceability`, `docs-implementation-alignment`, `repo-contracts`,
`agent-output-eval-fixture-gate`, `supply-chain-fixture-policy`,
`dependency-vulnerability-audit`, `git-flow-contract`,
`compose-validation`, `compose-all-profiles-validation`,
`infrastructure-hardening`, `template-security-baseline`,
`quickwin-baseline`, `pre-commit`, `frontend-quality`,
`storybook-coverage`, and `zizmor`.

`scripts/validation/run-ci-precommit.sh`:

- requires both `GITHUB_ACTIONS=true` and `CI=true`;
- rejects positional arguments and Agent-wrapper variables;
- executes exactly
  `pre-commit run --all-files --show-diff-on-failure`;
- preserves `SKIP=eslint-nextjs`;
- propagates the child exit code;
- does not snapshot or authorize Agent changes.

- [ ] Add RED workflow tests for every tracked workflow's exact trigger,
  permission, timeout, concurrency, and job contract.
- [ ] Add mutation RED cases for `pull_request_target`, event/branch/path
  widening, unapproved `workflow_call`/`workflow_run`, write permissions,
  missing timeout, duplicate job ID, mutable Action tag, unregistered Action,
  and Node 20.
- [ ] Add RED asserting `ci-quality.yml` retains exactly the 16 required IDs
  and each expensive semantic command has one CI job owner.
- [ ] Add shell RED tests for CI environment requirements, exact command,
  `SKIP` preservation, argument rejection, fake pre-commit exit propagation,
  and no Agent-wrapper acceptance.
- [ ] Record expected RED failures before production edits.
- [ ] Write the workflow contract and full-SHA Action registry from the
  verified official manifests.
- [ ] Replace `pre-commit/action` with setup-python, installation from
  `scripts/requirements-pre-commit.txt`, and the CI-only script.
- [ ] Remove overlapping inline workflow parsing from
  `check-repo-contracts.sh`; invoke the focused checker once and retain
  separate Stage 00 routing assertions.
- [ ] Register `tech-stack-version-sync.yml` in the non-gating taxonomy and
  local-runner remote-automation inventory.
- [ ] Synchronize `.github/INDEX.md`, desired protection, Stage 00 GitHub/QA
  governance, and tests without creating `.github/README.md`.
- [ ] Update manifest dispositions and regenerate the delta summary.
- [ ] Run:

```bash
python3 -m unittest tests.validation.test_github_workflow_contract -v
bash tests/validation/test_run_ci_precommit.sh
python3 -m unittest tests.validation.test_agent_governance_ci_routing -v
python3 scripts/validation/check-github-workflow-contract.py
bash scripts/validation/check-repo-contracts.sh
actionlint
shellcheck scripts/validation/run-ci-precommit.sh tests/validation/test_run_ci_precommit.sh
bash -n scripts/validation/run-ci-precommit.sh
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory
git diff --check
```

Expected GREEN: exact triggers and job identities match the machine contract;
all direct Actions are registered full SHAs with Node 24/composite evidence;
the mutable transitive pre-commit Action path is absent; CI and Agent
pre-commit routes remain distinct; repository contracts invoke one focused
workflow checker.

- [ ] Record exact workflow/job/action counts, removed duplicate execution,
  CI-script evidence, and no-remote-mutation statement in the Task ledger.
- [ ] Obtain independent specification and quality/security reviews.
- [ ] Commit as
  `ci(governance): type workflow and qa ownership`.

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
- remote default commit: `bffc5aed...`, behind local;
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

- [ ] Add RED schema tests that distinguish tracked desired state, observed
  remote state, unverified cause, and proposed future synchronization.
- [ ] Add RED proving the four-context drift list is the set difference, not a
  claim that remote checks failed to run.
- [ ] Add RED audit semantic assertions for the new delta checker, README
  convergence, version synchronization, workflow contract, CI pre-commit
  route, and remaining remote/CD/runtime gaps.
- [ ] Record expected failures before evidence edits.
- [ ] Update the observation using only sanitized metadata already obtained;
  do not perform another remote call or read raw logs.
- [ ] Reconcile only audit rows whose implementation truth changed. Keep CD,
  live deployment, broad vulnerability scanning, self-hosted runner inventory,
  and remote enforcement as Partial, Missing, or Needs Revalidation according
  to evidence.
- [ ] Preserve the 2026-07-07 pack as superseded mapping-only evidence; do not
  revive or duplicate it.
- [ ] Regenerate the audit matrix and metadata inventory with canonical
  owners.
- [ ] Update delta manifest review/evidence rows and regenerate its summary.
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
bash scripts/governance/validate-cross-links.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

Expected GREEN: canonical audit total remains 161 with recalculated affected
statuses; generated matrix and inventory are fresh; the observation contains
the dated 12-vs-16 comparison and no root-cause inference; all cross-links
resolve.

- [ ] Record affected audit row IDs, before/after totals, generator commands,
  observation boundary, and reviewers in the Task ledger.
- [ ] Obtain independent specification and quality/security reviews.
- [ ] Commit as
  `docs(audit): reconcile target surface evidence`.

### Task 6: T-TSDC-006 — Promote Enforcement and Close the Branch

**Files:**

- Modify
  `docs/90.references/data/governance/target-surface-delta-manifest.yaml`
  to set `enforcement: blocking` only after Tasks 1–5 have pass/pass reviews.
- Regenerate
  `docs/90.references/data/governance/target-surface-delta-summary.md`.
- Modify `scripts/validation/check-repo-contracts.sh` and
  `scripts/validation/run-local-qa-gates.sh` only if advisory invocation still
  needs promotion to blocking.
- Modify this Plan status to `completed`.
- Modify the sibling Task ledger status to `completed` only after all closure
  evidence exists.
- Modify `docs/00.agent-governance/memory/current.md` for the bounded handoff.
- Modify generated owners only through their registered generators.

**Closure interface:**

The manifest can move from `advisory` to `blocking` only when all rows have a
valid disposition, every destructive row has both review verdicts, Tasks 1–5
are committed and independently approved, generated outputs are fresh, and
the Spec 133 integrity test is green. A finding after promotion is a product
failure and blocks closure.

- [ ] Confirm the worktree is clean at the Task 5 reviewed commit before final
  verification.
- [ ] Recompute predecessor-to-`HEAD` target changes and confirm every path has
  exactly one current manifest row.
- [ ] Confirm Spec 133 tracked artifact hashes match the closure commit.
- [ ] Set enforcement to `blocking`, regenerate the summary, and run the
  focused delta tests/checker.
- [ ] Run the final local validation ladder:

```bash
python3 -m unittest \
  tests.validation.test_target_surface_contracts \
  tests.validation.test_target_surface_delta_contracts \
  tests.validation.test_document_metadata \
  tests.validation.test_tech_stack_version_contract \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_agent_governance_ci_routing \
  -v
bash tests/validation/test_run_ci_precommit.sh
python3 scripts/validation/check-target-surface-contract.py
python3 scripts/validation/check-target-surface-delta-contract.py --mode blocking
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/operations/sync-tech-stack-versions.sh --check
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
bash scripts/hardening/check-all-hardening.sh
python3 scripts/validation/check-supply-chain-policy.py --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/governance/validate-cross-links.sh
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/check-repo-contracts.sh
actionlint
git diff --check
```

Expected GREEN: all focused and aggregate checks pass; delta enforcement is
blocking with zero findings; generated owners are fresh; version, hardening,
metadata, links, workflow, audit, and repository contracts are green.

- [ ] If any command is unavailable, record the exact environment limitation
  and leave the corresponding result `unverified`; never convert it to pass.
- [ ] Do not run direct all-files pre-commit.
- [ ] If the user separately approves one exact final wrapper attempt, run
  only:

```bash
bash scripts/validation/run-agent-precommit-all-files.sh \
  --allow-prefix .github \
  --allow-prefix archive \
  --allow-prefix examples \
  --allow-prefix infra \
  --allow-prefix projects \
  --allow-prefix scripts \
  --allow-prefix secrets \
  --allow-prefix tests \
  --allow-prefix docs/00.agent-governance \
  --allow-prefix docs/03.specs/135-target-surface-delta-convergence \
  --allow-prefix docs/04.execution \
  --allow-prefix docs/05.operations \
  --allow-prefix docs/90.references \
  --allow-prefix docs/99.templates
```

Expected controlled result, if separately authorized: the wrapper records a
value-free pass/fail, exit status, snapshot result, and exact Git-visible path
sets. One approval authorizes one attempt only.

- [ ] Assign a fresh whole-branch correctness/specification reviewer.
- [ ] Assign a different fresh whole-branch security/quality reviewer.
- [ ] Remediate every Critical and Important finding with a new focused test
  and re-review.
- [ ] Record final commits, review ranges, deletion ledger, local/remote/
  skipped/unverified distinctions, and terminal evidence.
- [ ] Advance `current.md` to the next bounded handoff without rewriting
  historical `progress.md`.
- [ ] Commit as
  `docs(task): close target surface delta convergence`.

## Verification Plan

### Per-task Gate

Every task must provide:

1. a clean starting commit and scoped ownership;
2. the named RED tests and expected failure;
3. the smallest GREEN implementation;
4. native syntax and focused contract checks;
5. value-free evidence in the Task ledger;
6. one logical commit;
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
| Audit overclaim | local/remote/unverified schema | correct the affected audit row and regenerate owners |
| Reviewer mutation | explicit read-only review role | discard no work; inspect and separately authorize any reviewer-created commit |

Rollback uses task-level `git revert` after reviewing the exact range. No
rollback command may discard unrelated user work. Remote or runtime rollback
is not applicable because neither surface is mutated.

## Approval Gates

- Spec 135 and this design are approved.
- This Plan and Task ledger require explicit user approval before Task 1
  implementation begins.
- Protected local workflow, contract, governance, and template changes are
  within the Plan-bounded approved class after that approval.
- Remote mutation, live runtime work, push, pull request, merge, workflow
  dispatch, credential change, and raw-log access remain separately gated.
- A controlled final Agent all-files wrapper attempt requires a new exact
  approval after a clean committed checkpoint. No prior approval carries
  forward.

## Completion Criteria

- TSDC-001 through TSDC-017 have named passing evidence.
- Six logical task commits exist and are independently revertible.
- Every task has independent specification and quality/security approval.
- The delta manifest is blocking, complete, duplicate-safe, and green.
- Spec 133 artifacts are unchanged from their closure commit.
- README, typed fixture, archive, secret inventory, and version contracts pass.
- Workflow triggers, permissions, jobs, Action dependencies, and CI QA pass.
- The 16 required job IDs are unchanged.
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
- [Repository contract checker](../../../scripts/validation/check-repo-contracts.sh)
- [Controlled Agent pre-commit wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
