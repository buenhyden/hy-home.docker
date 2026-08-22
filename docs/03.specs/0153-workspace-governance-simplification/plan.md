---
profile_id: plan
status: active
artifact_id: plan-0153
artifact_type: plan
parent_ids:
  - SPEC-0153
created: 2026-08-20
updated: 2026-08-21
---

# Workspace Governance and SDLC Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Converge documentation, AI-agent governance, templates, validation,
fixtures, provenance, and lifecycle evidence onto the approved two-provider,
authority-first taxonomy without restoring or retaining legacy surfaces.

**Architecture:** Stage 99 becomes the document-contract authority before any
corpus move. Stage 00 then becomes the provider-neutral human and agent
governance authority, and each document stage migrates through a typed Migration
ledger. Six public gate suites compose focused validators; no aggregate owns
validation logic.

**Tech Stack:** Python 3.12+, Bash, JSON Schema Draft 2020-12, PyYAML, Git,
unittest, GitHub Actions, Markdown, JSON, YAML, GraphQL, OpenAPI, and Proto.

**Spec:** `docs/03.specs/0153-workspace-governance-simplification/spec.md`

## Global Constraints

- Stage 99 `registry.json` and its two schemas are the sole machine authority
  for document paths, profiles, identity spaces, sections, lifecycle, templates,
  traceability, and exceptions.
- Stage 00 owns policies, roles, provider differences, reusable skills, and the
  SDLC flow; generated provider surfaces never own policy.
- The supported providers are Claude and Codex only. Gemini and Antigravity are
  removed completely, including models, adapters, projections, tests, and shims.
- `.agents/skills/` is a generated compatibility projection of canonical Stage
  00 skills, not a source authority.
- Stage 01 uses Requirement Packages with `REQ-####`,
  `REQ-####-FR-####`, `REQ-####-NFR-####`, and `REQ-####-IF-####`.
- Stage 02 paths omit `ad-` and `adr-`; stable IDs are `AD-####` and
  `ADR-####`; superseded ADRs remain in the decision log.
- Stage 03 paths omit `spec-`; `design.md` and `tests.md` are not document
  roles; executable interface contracts are optional files under `contracts/`.
- Stage 03 Plan and Task evidence is transient. A completed living Spec retains
  current behavior; completed one-time migration packages are removed after
  durable migration evidence and Git recovery proof exist.
- Stage 05 retains `catalog/<domain>/<subject>/` ownership, removes the `ops-`
  path prefix, preserves registered role IDs, and removes Releases completely.
- Incident year containment under `incidents/<year>/inc-####-<slug>/` is the
  only date/path identity exception.
- Stage 90 contains only `research/`, `audits/`, and `data/` packages with
  numeric prefixless paths and stable frontmatter IDs.
- Stage 98 contains only README, minimal Migrations, and minimal Tombstones;
  Git history is the default full-content archive.
- Issued identity spaces advance monotonically. Deletion never lowers a
  high-water mark and no issued ID is reused.
- Runtime and product roots such as `infra/`, `examples/`, `projects/`,
  `secrets/`, and `.github/` remain intact unless a task names an exact consumer
  edit.
- Root `DESIGN.md` remains the UI/design-system authority and is not repurposed.
- All moves of tracked paths use `git mv`; compatibility copies, redirects, and
  duplicate active authorities are forbidden.
- One-time migration utilities remain under `/tmp` and are deleted before the
  task commit.
- Every generator defaults to check mode; repository mutation requires an
  explicit `--write` invocation.
- Before every commit, compare `git status --short` with that Task's **Files**
  list and its frozen Migration consumer rows. Invoke `git add --` or
  `git add -A --` separately on each literal Task-owned path; globs, broad stage
  roots, command substitutions, and unrelated hunks are forbidden. Verify the
  result with `git diff --cached --name-only` before `git commit`.
- Runtime-changing scripts, remote actions, secret changes, pushes, and merges
  are outside this plan unless the user grants separate explicit approval.
- Each Task uses RED, minimal GREEN, focused verification, self-review,
  independent specification review, independent quality review, and a logical
  Conventional Commit.
- Never stage unrelated worktree changes. Stop if a selected path is concurrently
  owned or if the migration ledger and tracked inventory disagree.

---

## Objective

This plan implements the approved Spec 0153 in one dependency-ordered program.
The current package remains at its legacy-compatible path until Task 2 installs
the Stage 99 authority that can validate the prefixless target. Task 3 then moves
the package natively and creates transient task evidence. Subsequent tasks migrate
one authority domain at a time and keep all unrelated runtime surfaces unchanged.

The final Task closes generated outputs and links, verifies all six public gate
suites, records recovery evidence, and removes the completed one-time Spec, Plan,
and Task package according to the approved lifecycle.

## Dependencies

### Verified starting state

- The isolated worktree branch is `codex/workspace-governance-simplification`.
- Spec 0153 is approved and independently reviewed at `C0/I0/M0` for both
  architecture/specification and quality.
- Graphify predates the branch and is advisory. Every plan decision was
  corroborated against tracked Stage 00, Stage 99, stage documents, scripts,
  tests, and workflow contracts.
- `check-document-metadata.py --mode check-changed` passes for the approved Spec.
- `check-document-links.py --mode alignment` currently reports 233 repository
  baseline findings and no Spec 0153 finding.
- `check-repo-contracts.sh` currently exits 1 with `failures=10`; the known
  owners include legacy Stage 04/archive links, Stage 00 memory, stale script
  references, and deleted `docs/05.operations/guides/...` expectations.
- `check-operations-catalog.py --mode complete` currently reports two index-route
  findings.
- `tests.validation.test_script_manifest` currently has 19 failures; Task 11
  owns this baseline and may not hide it with exceptions.
- Stage 01 contains 25 PRD files. Stage 02 contains 25 Architecture Descriptions
  and 25 ADRs. Stage 03 contains 34 Spec packages. Stage 04 contains 7 files.
- Stage 05 contains 75 subjects, 66 Guides, 64 Policies, and 62 Runbooks.
- Stage 90 contains five current category roots. Stage 98 contains 146 change
  packets, 38 Tombstones, and 2 Migrations.

Every Task re-measures its selected inventory before editing. A count mismatch is
a blocking concurrent-change signal, not permission to update expected counts.

### File responsibility map

| Responsibility | Canonical implementation files |
| :--- | :--- |
| Approved behavior | `docs/03.specs/0153-workspace-governance-simplification/spec.md` |
| Program sequence | `docs/03.specs/0153-workspace-governance-simplification/plan.md` |
| Cross-stage decision | `docs/02.architecture/decisions/0029-workspace-governance-authority.md`, later prefixless |
| Migration ledger | `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`, later prefixless |
| Document registry | `docs/99.templates/registry.json` |
| Registry schemas | `docs/99.templates/contracts/frontmatter.schema.json`, `document-profile.schema.json` |
| Registry loader | `scripts/lib/document_governance/registry.py` |
| Metadata and identity | `metadata_validator.py`, `metadata_contract.py`, `taxonomy.py` |
| Lifecycle and provenance | `git_provenance.py`, `check-document-corpus-lifecycle.py` |
| Document graph | `links.py`, `check-document-links.py` |
| Operations topology | `operations_catalog.py`, `check-operations-catalog.py` |
| Agent governance | `agent_governance_contract.py`, `check-agent-governance-contract.py`, `provider_surface_renderer.py` |
| Script ownership | `scripts/manifest.yaml`, `check-script-manifest.py` |
| Gate graph | `.github/workflow-contract.yml`, `ci_gate_contract.py`, `ci_gate_runner.py`, `ci_gate_adapters.py` |
| Public entrypoint | `scripts/validation/run-ci-gate.py` |
| CI and local routing | `.github/workflows/ci-quality.yml`, `.pre-commit-config.yaml`, `run-local-qa-gates.sh` |

### Spec coverage map

| Acceptance contract | Implementing Tasks |
| :--- | :--- |
| Approved documentation and provider control-plane roots | 2-13 |
| Sole Stage 99 registry/schema/template authority | 2, 13 |
| Simplified Stage 00 and no project memory | 4 |
| Complete Gemini and Antigravity removal | 4, 12 |
| Unified Requirement Packages and full IDs | 5 |
| Prefixless AD/ADR and linked supersession | 1, 6 |
| Prefixless Specs, interface contracts, no Stage 04/design/tests | 3, 7 |
| Prefixless Operations subjects and no duplicate roles/Releases | 8 |
| Exact Incident packet topology | 8 |
| Stage 90 Research/Audit/Data only | 9 |
| Minimal Stage 98 | 10 |
| Mirrored script/test ownership and no one-time tools | 11, 12 |
| Six public suites over focused validators | 11, 12 |
| Registry-driven bounded fixtures and simplified provenance | 2, 10, 11 |
| No stale current link and exact ID allocation/membership | 2-13 |
| Full-profile GREEN and independent final review | 13 |

## Goals and Non-goals

### Goals

- Install explicit, testable authority before moving its corpus.
- Preserve stable semantic and numeric identities while removing path prefixes.
- Make every deletion recoverable from Git plus a minimal Migration or Tombstone.
- Reduce public validation to six comprehensible suites without combining focused
  validators or fixtures into a new monolith.
- End with no compatibility document, transition script, stale provider, Release
  surface, project memory, or duplicated Stage 99 support rule.

### Non-goals

- Changing Docker Compose topology or service runtime state.
- Rewriting product requirements, architecture decisions, or operational
  procedures beyond the approved role consolidation and path migration.
- Rewriting Git history or preserving full retired document copies in Stage 98.
- Adding provider capabilities for unsupported AI runtimes.
- Converting root `DESIGN.md` into an SDLC artifact.

## Execution Sequence

### Task 1: Register the Cross-Stage Decision and Migration Ledger

**Files:**

- Create: `docs/02.architecture/decisions/0029-workspace-governance-authority.md`
- Create: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/task.md`
- Create: `tests/validation/test_workspace_governance_migration.py`
- Modify: `docs/03.specs/0153-workspace-governance-simplification/spec.md`
- Modify: `docs/03.specs/0153-workspace-governance-simplification/plan.md`

**Interfaces:**

- Consumes: approved Spec 0153, tracked inventory, Git object identity.
- Produces: `ADR-0029`, Migration `mig-0003`, typed `planned_creations`, and
  immutable transition rows. Each creation has `path`, `artifact_id`, and
  `owner_task`. Each transition has `row_id`, `source_path`, `target_path`,
  `artifact_id`, `action`, `owner_task`, `source_kind`, `source_owner_task`,
  `active_consumers`, `recovery_commit`, and `status`.

- [x] **Step 1: Write the missing-control-plane RED test**

```python
from pathlib import Path
import unittest

ADR = Path("docs/02.architecture/decisions/0029-workspace-governance-authority.md")
MIGRATION = Path("docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md")

class WorkspaceGovernanceMigrationTests(unittest.TestCase):
    def test_governance_migration_control_plane_exists(self) -> None:
        self.assertTrue(ADR.is_file())
        self.assertTrue(MIGRATION.is_file())
```

- [x] **Step 2: Run RED and record the exact absence**

Run:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Expected: FAIL because both approved control-plane files are absent.

- [x] **Step 3: Create ADR-0029 from the current ADR template**

Record context, authority alternatives, the chosen Stage 00/99 split, generated
provider projections, six public suites, consequences, and confirmation tests.
Use `artifact_id: ADR-0029`, `status: draft`, and link Spec 0153. Do not move or
uppercase it until Task 6 installs the Stage 02 target profile.

- [x] **Step 4: Create Migration mig-0003 from the current archive template**

Add a machine-readable fenced YAML block with this exact row contract:

```yaml
schema_version: 2
migration_id: mig-0003
baseline_commit: 889d3868ecd0913cddac79a718584a54a8453525
approval:
  status: pending
  approved_by: null
  approved_at: null
consumer_policy:
  version: 1
  literal_references: exact-repository-relative-path
  markdown_links: shared-local-relative-parser
  delete_consumers: inactive-when-delete-owner-task-lte-source-owner-task
  excluded_noncurrent: []
  derived_edges_sha256: <64-lowercase-hex>
final_compaction:
  owner_task: 13
  schema_version: 3
  top_level_keys: [schema_version, migration_id, rows]
  row_keys: [source_path, target_path, artifact_id, action, recovery_commit]
planned_creations:
  - path: docs/02.architecture/decisions/0029-workspace-governance-authority.md
    artifact_id: ADR-0029
    owner_task: 1
rows:
  - row_id: mig-0003-r0001
    source_path: docs/03.specs/spec-0153-workspace-governance-simplification/spec.md
    target_path: docs/03.specs/0153-workspace-governance-simplification/spec.md
    artifact_id: SPEC-0153
    action: rename
    owner_task: 3
    source_kind: tracked
    source_owner_task: null
    active_consumers: []
    recovery_commit: null
    status: planned
```

Populate one structural row for every Stage 00/01/02/03/04/05/90/98/99,
provider, script, and mirrored-test source selected by this plan. Ordinary
in-place semantic edits are not Migration rows. `planned_creations` registers a
new path only when a later transition consumes it. `action` is `rename`,
`merge`, or `delete`; create is never a transition action. `null` recovery is
allowed only while a row remains planned; Task 13 rejects it for
completed/deleted rows.

- [x] **Step 5: Expand the test to validate every ledger row**

Require exactly one YAML fence and a strict loader that rejects duplicate keys,
aliases, anchors, and explicit tags. Assert unique row and source-transition
identities, canonical POSIX paths, allowed actions, exact required keys, and no
normalized collision across baseline, planned creation, and target namespaces
except explicit merge or ordered transition lineage. Freeze the exact base
commit and prove every `tracked` source through `git ls-tree -rz --full-tree` as
mode `100644` or `100755` and type `blob`. A
`planned-output` source must match either a `planned_creations` path/artifact
whose `source_owner_task` is earlier than its transition owner or the exact
target/artifact of an earlier transition row. Require every current tracked
source to carry its exact owner-ordered active-consumer list. Resolve local
Markdown relative links with the shared safe parser and retain literal scanning
for code/config/plain references. A delete-disposition consumer is inactive only
when its delete owner Task is no later than the source transition owner. Exclude
Stage 98 recovery, Graphify collateral, and immutable or generated Stage 90
evidence. Bind the baseline commit, consumer policy, derived-edge digest,
final-compaction contract, creations, and rows into the selection digest. Reject
Release, Gemini, or Antigravity targets and create actions inside transitions.

- [x] **Step 6: Run focused GREEN checks**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
git diff --check
```

Expected: migration tests and changed metadata pass; no corpus path has moved.

Actual Task 1 evidence after final re-review: the initial one-test RED failed on the
absent ADR. The quality-remediation RED then ran `8` tests with `7` failures;
after correction, `11/11` focused tests pass. The frozen packet contains `17`
planned creations, `903` transitions, and `3,571` derived consumer edges with
edge SHA-256 `2f1840983d98ed93ffdc183305c49b389b17e5c8362538e5df97d451be2b9139` and
selection SHA-256
`9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1`.
Changed metadata reports `selected=5 violations=0 legacy_exceptions=0
transition_overrides=0`; `git diff --check` exits zero. Exact output is recorded
in `task.md`. Final independent specification and quality re-reviews each report
`C0/I0/M0`; the earlier quality `I5` and lifecycle `I1` are addressed. The user
approved the exact selection digest as `user` on `2026-08-20`; no corpus
transition has executed.

- [ ] **Step 7: Review and commit the control plane**

Status: independent reviews, exact user row-set approval, and the approved-state
`11/11` focused suite are complete. Only the controller-owned logical commit and
its identity remain.

Require independent specification and quality approval of the complete selected
row set, then obtain the user's explicit approval of that exact row set. Record
the verdicts, approval identity/date, and Task 1 RED/GREEN evidence in `task.md`,
change `approval.status` from `pending` to `approved`, and run the same lifecycle
suite before staging. `pending` requires null approval identity/date; `approved`
requires a nonempty identity and a real canonical `YYYY-MM-DD` date. Both states
retain the same selected rows and digest.

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Only after that command passes may the control plane be staged:

```bash
git add docs/02.architecture/decisions/0029-workspace-governance-authority.md \
  docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md \
  docs/03.specs/0153-workspace-governance-simplification \
  tests/validation/test_workspace_governance_migration.py
git commit -m "docs: register workspace governance migration"
```

### Task 2: Establish Stage 99 Registry, Schema, and Template Authority

**Files:**

- Create: `docs/99.templates/registry.json`
- Create: `docs/99.templates/contracts/frontmatter.schema.json`
- Create: `docs/99.templates/contracts/document-profile.schema.json`
- Create: `scripts/lib/document_governance/registry.py`
- Create: `scripts/lib/document_governance/identity_history.py`
- Create: `tests/validation/test_document_registry.py`
- Create: `tests/validation/test_identity_history.py`
- Create: `docs/99.templates/templates/requirements/requirement-package.template.md`
- Create: `docs/99.templates/templates/architecture/architecture-description.template.md`
- Create: `docs/99.templates/templates/architecture/adr.template.md`
- Create: `docs/99.templates/templates/specs/spec.template.md`
- Create: `docs/99.templates/templates/specs/plan.template.md`
- Create: `docs/99.templates/templates/specs/task.template.md`
- Create: `docs/99.templates/templates/specs/openapi.template.yaml`
- Create: `docs/99.templates/templates/specs/schema.template.graphql`
- Create: `docs/99.templates/templates/specs/service.template.proto`
- Create: `docs/99.templates/templates/references/research.template.md`
- Create: `docs/99.templates/templates/references/audit.template.md`
- Create: `docs/99.templates/templates/references/data.template.md`
- Create: `docs/99.templates/templates/archive/migration.template.md`
- Create: `docs/99.templates/templates/archive/tombstone.template.md`
- Modify: `docs/99.templates/README.md`
- Modify: `docs/99.templates/templates/README.md`
- Modify: `docs/99.templates/templates/operations/guide.template.md`
- Modify: `docs/99.templates/templates/operations/policy.template.md`
- Modify: `docs/99.templates/templates/operations/runbook.template.md`
- Modify: `docs/99.templates/templates/operations/incident.template.md`
- Modify: `docs/99.templates/templates/operations/postmortem.template.md`
- Modify: `scripts/requirements.txt`
- Modify: `scripts/lib/document_governance/metadata_validator.py`
- Modify: `scripts/lib/document_governance/metadata_contract.py`
- Modify: `scripts/lib/document_governance/taxonomy.py`
- Modify: `scripts/validation/check-document-metadata.py`
- Modify: `scripts/validation/check-document-corpus-lifecycle.py`
- Modify: `scripts/manifest.yaml`
- Modify: `tests/validation/test_document_metadata.py`
- Modify: `tests/validation/test_four_digit_document_identity.py`
- Modify: `tests/validation/test_document_corpus_lifecycle.py`
- Modify: `docs/03.specs/0153-workspace-governance-simplification/task.md`

**Interfaces:**

- Consumes: current support YAML only as a one-time translation input and
  Migration `mig-0003` as transition evidence.
- Produces:
  `load_registry(path: pathlib.Path = DEFAULT_REGISTRY) -> DocumentRegistry`,
  `validate_registry(raw: Mapping[str, object]) -> tuple[RegistryFinding, ...]`,
  and immutable `DocumentRegistry.profiles`, `.template_roles`, `.lifecycles`,
  `.identity_spaces`, `.transitions`.

- [ ] **Step 1: Write registry RED tests**

```python
import unittest

class DocumentRegistryTests(unittest.TestCase):
    def test_default_authority_is_registry_json(self) -> None:
        registry = load_registry()
        self.assertEqual(
            registry.source.as_posix(), "docs/99.templates/registry.json"
        )
        self.assertNotIn("release", registry.profiles)
        self.assertGreater(registry.identity_spaces["requirement"].next_number, 0)

    def test_prefixless_spec_and_full_requirement_ids(self) -> None:
        self.assertEqual(
            classify_path("docs/03.specs/0153-example/spec.md"), "spec"
        )
        self.assertTrue(is_valid_internal_requirement_id("REQ-0001-NFR-0001"))
        self.assertFalse(is_valid_internal_requirement_id("PRD-001-R001"))
```

Add negative tests for malformed JSON, schema recursion/depth, duplicate profile
IDs, `next_number <= high_water`, an unregistered lifecycle transition, a
Release profile, and a target template that embeds a concrete target path.

Add a temporary-Git-repository fixture containing a deleted lowercase package
ID and deleted FR/NFR/IF child IDs. The fixture must prove that history-derived
high-water marks reserve those numbers even when the files are absent at HEAD.

- [ ] **Step 2: Run the focused RED set**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_document_registry \
  tests.validation.test_identity_history \
  tests.validation.test_four_digit_document_identity -v
```

Expected: FAIL because the registry, schemas, loader, and new identity patterns
do not exist.

- [ ] **Step 3: Add the JSON Schema dependency and immutable registry model**

Add `jsonschema>=4.23,<5.0` to `scripts/requirements.txt`. Implement frozen
records in `registry.py`:

```python
@dataclasses.dataclass(frozen=True)
class IdentitySpace:
    prefix: str
    width: int
    high_water: int
    next_number: int
    child_spaces: Mapping[str, "IdentitySpace"]

@dataclasses.dataclass(frozen=True)
class DocumentRegistry:
    source: pathlib.PurePosixPath
    profiles: Mapping[str, Mapping[str, object]]
    template_roles: Mapping[str, Mapping[str, object]]
    lifecycles: Mapping[str, tuple[str, ...]]
    identity_spaces: Mapping[str, IdentitySpace]
    transitions: Mapping[str, object]
```

Use `jsonschema.Draft202012Validator`, reject symlinks/non-regular files,
enforce a byte/depth bound, and deep-freeze all returned mappings and sequences.
Implement
`collect_issued_identities(repo: Path, refs: tuple[str, ...] = ("--all",))`
using bounded `git log --no-ext-diff -U0 -G` output with a module-owned constant
covering canonical and known legacy ID families, plus the tracked current
corpus. Normalize lowercase historical aliases, union the
observed package and child spaces, and compare their maxima with registry
high-water values. The full history scan runs only in the full document-contract
profile; changed mode validates against the persisted allocation state.

- [ ] **Step 4: Build registry.json and both schemas**

Translate every still-current profile from
`support/document-metadata-profiles.yaml`, then replace the target shapes with
the approved profiles. Add exact lifecycle transitions, uppercase standalone
package IDs, Operations subject-member identity, Incident exception, and
monotonic identity spaces. Transition sources exist only as rows in Migration
`mig-0003`; they are not second active profiles.

- [ ] **Step 5: Create and register the simplified templates**

Merge PRD/SRS/Interface into Requirement Package; move AD/ADR and Spec roles;
register optional OpenAPI/GraphQL/Proto payloads; retain Operations roles except
Release; split Research/Audit/Data and Migration/Tombstone. Every Markdown
template frontmatter contains a `profile_id` token and no concrete target path.

- [ ] **Step 6: Switch metadata and lifecycle consumers to registry.py**

Keep `load_profiles()` as a temporary API adapter returning
`load_registry().profiles`, but change its default source to `registry.json`.
Replace hard-coded PRD/SRS/IFR/Release path inference and internal IDs. Update
`metadata_contract.py` exports and CLI `--registry` arguments. Do not delete
`support/` in this Task.

- [ ] **Step 7: Run focused GREEN and mutation checks**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_document_registry \
  tests.validation.test_identity_history \
  tests.validation.test_document_metadata \
  tests.validation.test_four_digit_document_identity \
  tests.validation.test_document_corpus_lifecycle -v
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-script-manifest.py
git diff --check
```

Expected: new registry tests pass; any remaining repository findings are listed
as migration-source rows, not configuration errors or hidden exceptions.

- [ ] **Step 8: Review and commit the authority unit**

Require independent specification and Python quality approval, append the actual
Task 2 RED/GREEN/review evidence to the bootstrap `task.md`, then:

```bash
git add docs/99.templates scripts/requirements.txt \
  scripts/lib/document_governance scripts/validation/check-document-metadata.py \
  scripts/validation/check-document-corpus-lifecycle.py scripts/manifest.yaml \
  tests/validation/test_document_registry.py \
  tests/validation/test_identity_history.py \
  tests/validation/test_document_metadata.py \
  tests/validation/test_four_digit_document_identity.py \
  tests/validation/test_document_corpus_lifecycle.py
git add docs/03.specs/0153-workspace-governance-simplification/task.md
git commit -m "refactor(docs): establish stage 99 registry authority"
```

### Task 3: Bootstrap the Canonical Spec 0153 Execution Package

**Files:**

- Move: the approved legacy package path in Migration rows `mig-0003-r0001`
  and `mig-0003-r0002` -> `docs/03.specs/0153-workspace-governance-simplification/`
- Create: `docs/03.specs/0153-workspace-governance-simplification/README.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0001-control-plane.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0002-stage99.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0003-bootstrap.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0005-requirements.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0006-architecture.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0007-spec-lifecycle.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0008-operations.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0009-references.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0010-archive.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0011-script-tests.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0012-gates.md`
- Create: `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0013-closure.md`
- Modify: moved `spec.md` and `plan.md`
- Delete after evidence migration: moved legacy `task.md`
- Modify: `docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md`
- Modify: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`
- Modify: all active consumers returned by `rg -l 'SPEC-0153-workspace-governance-simplification|SPEC-0153|plan-0153' docs scripts tests .github .agents .claude .codex AGENTS.md CLAUDE.md`
- Test: `tests/validation/test_document_registry.py`
- Test: `tests/validation/test_document_metadata.py`
- Test: `tests/validation/test_workspace_governance_migration.py`

**Interfaces:**

- Consumes: Task 2 prefixless Spec profile and identity allocation state.
- Produces: canonical `SPEC-0153`, transient `plan-0153`, and task identities
  `task-0153-0001` through `task-0153-0013` at registered paths.

- [ ] **Step 1: Write the canonical-package RED**

```python
import unittest

from scripts.lib.document_governance.frontmatter import read_frontmatter_values

class WorkspaceGovernancePackageTests(unittest.TestCase):
    def test_spec_0153_uses_canonical_package(self) -> None:
        package = Path("docs/03.specs/0153-workspace-governance-simplification")
        self.assertTrue(package.joinpath("README.md").is_file())
        self.assertTrue(package.joinpath("spec.md").is_file())
        self.assertTrue(package.joinpath("plan.md").is_file())
        self.assertEqual(len(tuple(package.joinpath("tasks").glob("tsk-*.md"))), 13)

    def test_spec_0153_supersedes_spec_0136_reciprocally(self) -> None:
        package = Path("docs/03.specs/0153-workspace-governance-simplification")
        current = read_frontmatter_values(package.joinpath("spec.md"))
        predecessor = read_frontmatter_values(
            Path("docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md")
        )
        self.assertIn("SPEC-0136", current["supersedes"])
        self.assertEqual(predecessor["superseded_by"], "SPEC-0153")
```

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Expected: FAIL because the package remains at its bootstrap path.

- [ ] **Step 3: Move the package natively and normalize identity**

Move the two sources selected by Migration rows `mig-0003-r0001` and
`mig-0003-r0002` to their registered canonical package path with native
`git mv` operations.

Set `spec.md` to `artifact_id: SPEC-0153`; keep Plan/Task identity formats exactly
as registered in Task 2. Set `SPEC-0153 supersedes SPEC-0136` and update the
predecessor's `superseded_by` in the same unit. Rewrite all selected inbound
references atomically.

- [ ] **Step 4: Create the package README and thirteen Task records**

Use the registered README and Task templates. Each Task links `SPEC-0153` and
`plan-0153` and owns only its numbered boundary. Migrate the already-recorded
Task 1 and Task 2 evidence from bootstrap `task.md` into `tsk-0001` and
`tsk-0002`, verify byte/field completeness, then delete bootstrap `task.md`.
Tasks 3-13 start `draft` with empty evidence tables instead of prospective PASS
claims.

- [ ] **Step 5: Validate paths, identity, links, and migration row**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
python3 scripts/validation/check-document-links.py --mode traceability
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_document_registry \
  tests.validation.test_document_metadata \
  tests.validation.test_workspace_governance_migration -v
git diff --check
```

Expected: no finding owned by the moved package; unrelated baseline link findings
remain explicitly attributed and are not called PASS.

- [ ] **Step 6: Review and commit the bootstrap move**

Require independent specification and quality approval, then stage only the
native move, new package records, exact inbound consumers, and migration row:

```bash
git commit -m "docs(spec): activate canonical governance package"
```

### Task 4: Converge Stage 00 and Provider Surfaces on Claude and Codex

**Files:**

- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Delete: `GEMINI.md`
- Delete: every tracked path under `.gemini/`
- Modify: `docs/00.agent-governance/README.md`
- Create: `docs/00.agent-governance/sdlc.md`
- Move: registered normative sources under `docs/00.agent-governance/rules/`
  to their Migration `owner_task: 4` targets under
  `docs/00.agent-governance/policies/`
- Move: registered ownership/scope sources under
  `docs/00.agent-governance/scopes/` to their Migration `owner_task: 4` targets
  under `docs/00.agent-governance/roles/`
- Move: `docs/00.agent-governance/agents/agents/` to
  `docs/00.agent-governance/roles/`
- Move: `docs/00.agent-governance/agents/functions/` to
  `docs/00.agent-governance/skills/`
- Delete: `docs/00.agent-governance/agents/README.md`
- Delete: every tracked path under `docs/00.agent-governance/memory/`
- Create: `docs/00.agent-governance/providers/README.md`
- Create: `docs/00.agent-governance/providers/registry.yaml`
- Delete: `docs/00.agent-governance/providers/gemini.md`
- Delete after integrating bootstrap/provider-neutral content into root shims,
  `providers/README.md`, and `providers/registry.yaml`:
  `docs/00.agent-governance/providers/agents-md.md`
- Modify: `docs/00.agent-governance/providers/claude.md`
- Modify: `docs/00.agent-governance/providers/codex.md`
- Delete after moving machine facts to Stage 99 and provider facts to
  `providers/registry.yaml`: every tracked file under
  `docs/00.agent-governance/contracts/`
- Delete after content disposition: `docs/00.agent-governance/harness-implementation-map.md`
- Delete after content disposition: `docs/00.agent-governance/subagent-protocol.md`
- Delete in place instead of moving:
  `docs/00.agent-governance/agents/functions/project-memory-stewardship.md`
- Delete: `docs/99.templates/templates/governance/memory.template.md`
- Delete: `docs/99.templates/templates/governance/progress.template.md`
- Modify: `docs/99.templates/templates/governance/README.md`
- Modify: `docs/99.templates/registry.json`
- Modify: `scripts/validation/agent_governance_contract.py`
- Modify: `scripts/validation/check-agent-governance-contract.py`
- Modify: `scripts/validation/agent_output_eval.py`
- Modify: `scripts/operations/provider_surface_renderer.py`
- Modify: `scripts/operations/sync-provider-surfaces.sh`
- Modify: `tests/validation/test_agent_governance_contract.py`
- Modify: `tests/validation/test_provider_native_surfaces.py`
- Modify: `tests/validation/test_provider_surface_renderer.py`
- Modify: `tests/validation/test_agent_governance_ci_routing.py`
- Modify: `.github/CODEOWNERS`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `.github/labeler.yml`
- Modify: `scripts/README.md`
- Modify: every additional active Gemini/Antigravity consumer returned by the
  Task 4 exact scan and registered in Migration `mig-0003`
- Modify: generated projections under `.agents/`, `.claude/`, and `.codex/`
- Modify: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`

The Migration rows are the exact move/delete selection. No recursive source
root is acted on until its tracked members equal the registered row set.

**Interfaces:**

- Consumes: Stage 99 profiles for governance policy, role, provider adapter,
  and skill; current agent catalog and provider-model contracts.
- Produces: canonical Stage 00 source plus deterministic Claude and Codex
  projections. `render_all(source_root, providers=("claude", "codex"))`
  returns immutable output records and has no Gemini branch.

- [ ] **Step 1: Write the two-provider and no-memory RED**

```python
import unittest

class AgentGovernanceConvergenceTests(unittest.TestCase):
    def test_supported_providers_and_governance_roots_are_exact(self) -> None:
        state = load_agent_governance(ROOT)
        self.assertEqual(state.providers, ("claude", "codex"))
        self.assertEqual(
            state.root_entries,
            ("README.md", "policies", "providers", "roles", "sdlc.md", "skills"),
        )
        self.assertEqual(
            state.provider_entries,
            ("README.md", "claude.md", "codex.md", "registry.yaml"),
        )
        self.assertFalse(Path("docs/00.agent-governance/memory").exists())
        self.assertFalse(Path(".gemini").exists())
        self.assertFalse(Path("GEMINI.md").exists())
```

Add mutation cases for an Antigravity token, a generated file that owns policy,
a `.agents/skills` file without a canonical Stage 00 source, and bootstrap files
that still load `memory/current.md`.

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_agent_governance_contract \
  tests.validation.test_provider_native_surfaces \
  tests.validation.test_provider_surface_renderer -v
```

Expected: FAIL on the third provider, project memory, old source roots, and
generated-authority assumptions.

- [ ] **Step 3: Move canonical roles, skills, and policies natively**

For each Migration row, use one `git mv source_path target_path`. Merge `rules/`
only where normative purpose is identical. Integrate `scopes/` into role
responsibilities, not Policies. Integrate the human content from
`harness-implementation-map.md` and `subagent-protocol.md` into the owning
policy, role, provider registry, or skill before deleting them. Exclude
`project-memory-stewardship.md` from the functions move and delete it in place.
`sdlc.md` owns Requirements -> Architecture -> Spec -> Implementation ->
Operations and links Stage 99 for shapes and `scripts/` for execution.

- [ ] **Step 4: Remove memory, Gemini, and Antigravity atomically**

Remove bootstrap references before deleting memory. Remove provider contracts,
renderer branches, projection files, `.gemini/`, `GEMINI.md`, and every active
Gemini/Antigravity consumer in the same commit. Historical Migration recovery
fields may name deleted paths; active authority may not.

- [ ] **Step 5: Regenerate compatibility surfaces**

```bash
bash scripts/operations/sync-provider-surfaces.sh --write
bash scripts/operations/sync-provider-surfaces.sh --check
```

The writer may create only registered `.agents`, `.claude`, and `.codex`
outputs. It must prove byte-for-byte parity and absence of unsupported outputs.

- [ ] **Step 6: Run focused GREEN and stale-token checks**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_agent_governance_contract \
  tests.validation.test_provider_native_surfaces \
  tests.validation.test_provider_surface_renderer \
  tests.validation.test_agent_governance_ci_routing -v
python3 scripts/validation/check-agent-governance-contract.py
rg -n -i 'gemini|antigravity|project.memory|memory/current' \
  AGENTS.md CLAUDE.md docs/00.agent-governance scripts .agents .claude .codex
git diff --check
```

Expected: tests and contract pass; `rg` returns no active-governance match.
Approved Migration recovery evidence is reviewed separately and is not rewritten.

- [ ] **Step 7: Review and commit Stage 00**

Require independent governance and quality approval, then commit only the
registered sources, consumers, projections, tests, and Migration rows:

```bash
git commit -m "refactor(governance): converge claude and codex authority"
```

### Task 5: Consolidate Stage 01 into Requirement Packages

**Files:**

- Modify: `docs/01.requirements/README.md`
- Move: the 25 tracked `docs/01.requirements/prd-####-<slug>.md` files to the
  exact `docs/01.requirements/####-<slug>.md` targets in Migration `mig-0003`
- Create: `scripts/lib/document_governance/requirements.py`
- Create: `tests/validation/test_requirement_packages.py`
- Modify: `scripts/lib/document_governance/metadata_validator.py`
- Modify: `scripts/lib/document_governance/taxonomy.py`
- Modify: `tests/validation/test_document_metadata.py`
- Modify: `tests/validation/test_four_digit_document_identity.py`
- Modify: every Migration-declared active consumer of the 25 source paths and
  their PRD/SRS/IFR/internal IDs
- Modify: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`

**Interfaces:**

- Consumes: `requirement-package` registry profile and its identity space.
- Produces: `parse_requirement_package(path) -> RequirementPackage` with stable
  package ID `REQ-####` and child IDs `REQ-####-FR-####`,
  `REQ-####-NFR-####`, or `REQ-####-IF-####`.

- [ ] **Step 1: Freeze inventory and write Requirement RED tests**

```python
import unittest

class RequirementPackageTests(unittest.TestCase):
    def test_requirement_package_identity_is_owned_by_path(self) -> None:
        package = parse_requirement_package(
            Path("docs/01.requirements/0001-workspace-platform.md")
        )
        self.assertEqual(package.artifact_id, "REQ-0001")
        self.assertTrue(
            all(item.identity.startswith("REQ-0001-") for item in package.items)
        )
        self.assertLessEqual({item.kind for item in package.items}, {"FR", "NFR", "IF"})
```

Add failures for `PRD-`, `SRS-`, `IFR-`, bare `FR-0001`, duplicate child IDs,
path/package-number mismatch, issued-ID reuse, and executable OpenAPI/GraphQL/
Proto payloads under Stage 01.

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_requirement_packages \
  tests.validation.test_four_digit_document_identity -v
```

- [ ] **Step 3: Generate a deterministic one-time conversion preview**

Use a temporary script under `/tmp` to classify existing requirement statements
by their source sections. The preview maps every old package and internal ID to
exact new IDs and stops on ambiguity. Review the 25 package rows and delete the
temporary script before staging.

- [ ] **Step 4: Move and rewrite the 25 packages atomically**

Use `git mv` for every registered path. Preserve problem, goals, stakeholders,
constraints, acceptance meaning, and trace links. Consolidate functional,
non-functional, and solution-independent interface requirements in the same
file. Rewrite all cross-document references to full child IDs.

- [ ] **Step 5: Implement package and allocation validation**

`requirements.py` parses bounded UTF-8 regular files, returns frozen records,
and rejects malformed or ambiguous declaration lines. Update registry high-water
state without lowering or reusing any issued number.

- [ ] **Step 6: Run focused GREEN, link, and metadata gates**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_requirement_packages \
  tests.validation.test_document_metadata \
  tests.validation.test_four_digit_document_identity -v
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
python3 scripts/validation/check-document-links.py --mode traceability
git diff --check
```

Expected: all 25 current packages pass; no active legacy requirement identity or
path remains; unrelated baseline link findings remain attributed.

- [ ] **Step 7: Review and commit Requirement Packages**

Stage each literal Task 5 File-list and reviewed consumer path, verify the
cached-name list, then:

```bash
git commit -m "refactor(requirements): unify requirement packages"
```

### Task 6: Move Stage 02 to Prefixless Descriptions and Decisions

**Files:**

- Modify: `docs/02.architecture/README.md`
- Move: the 25 tracked description files in Migration 0003 Task 6 rows to exact
  `docs/02.architecture/descriptions/####-<slug>.md` targets
- Move: the 26 tracked decision files in Migration 0003 Task 6 rows after Task 1,
  including ADR-0029, to exact
  `docs/02.architecture/decisions/####-<slug>.md` targets
- Create: `scripts/lib/document_governance/architecture.py`
- Create: `tests/validation/test_architecture_documents.py`
- Modify: `scripts/lib/document_governance/metadata_validator.py`
- Modify: `scripts/lib/document_governance/taxonomy.py`
- Modify: all Migration-declared active AD/ADR path and ID consumers
- Modify: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`

**Interfaces:**

- Consumes: Stage 99 architecture-description and ADR profiles.
- Produces: prefixless paths with `AD-####` and `ADR-####` frontmatter and a
  directed supersession graph whose nodes remain in Stage 02.

- [ ] **Step 1: Write path, identity, and supersession RED tests**

```python
import unittest

class ArchitectureDocumentTests(unittest.TestCase):
    def test_architecture_paths_and_ids_are_consistent(self) -> None:
        corpus = load_architecture_documents(Path("docs/02.architecture"))
        self.assertTrue(
            all(not item.path.name.startswith(("ad-", "adr-")) for item in corpus)
        )
        self.assertTrue(
            all(item.artifact_id.startswith(("AD-", "ADR-")) for item in corpus)
        )
        self.assertEqual(validate_supersession_graph(corpus), ())
```

Mutation cases cover lowercase stable IDs, number mismatch, cycles, dangling
`supersedes`/`superseded_by`, archived superseded ADRs, and a restored forbidden
Stage 02 requirements subdirectory.

- [ ] **Step 2: Run RED, then move files natively**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_architecture_documents -v
```

Use one `git mv` per exact Migration row. Uppercase stable IDs, preserve content,
and add reciprocal supersession links without relocating superseded ADRs.

- [ ] **Step 3: Implement immutable graph validation and rewrite consumers**

Load only registered regular files, deep-freeze graph nodes, verify exact path/ID
number ownership, and reject symlink or duplicate identities. Rewrite current
consumers; preserve old path only in Migration recovery fields.

- [ ] **Step 4: Run focused GREEN and graph gates**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_architecture_documents \
  tests.validation.test_document_metadata -v
python3 scripts/validation/check-document-links.py --mode traceability
python3 scripts/validation/check-document-links.py --mode alignment
git diff --check
```

- [ ] **Step 5: Review and commit Stage 02**

Stage each literal Task 6 File-list and reviewed consumer path, verify the
cached-name list, then:

```bash
git commit -m "refactor(architecture): use prefixless document paths"
```

### Task 7: Simplify Stage 03 and Retire Stage 04

**Files:**

- Modify: `docs/03.specs/README.md`
- Move: the 33 remaining tracked `docs/03.specs/spec-####-<slug>/` packages to
  the exact prefixless targets registered in Migration `mig-0003`; Spec 0153 is
  already prefixless from Task 3, so the resulting total remains 34
- Move or integrate: the seven tracked Stage 04 files:
  `docs/04.execution/README.md`,
  `docs/04.execution/plans/README.md`,
  `docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md`,
  `docs/04.execution/tasks/README.md`,
  `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`,
  `docs/04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md`,
  and `docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md`
- Delete: `docs/04.execution/` after all seven rows are executed
- Create: `scripts/lib/document_governance/spec_packages.py`
- Create: `tests/validation/test_spec_packages.py`
- Modify: `scripts/lib/document_governance/metadata_validator.py`
- Modify: `scripts/validation/check-document-corpus-lifecycle.py`
- Modify: `tests/validation/test_document_corpus_lifecycle.py`
- Modify: every Migration-declared active Stage 03/04 consumer
- Modify: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`

**Interfaces:**

- Consumes: Stage 99 Spec, Plan, Task, and optional contract profiles.
- Produces: `README.md`, `spec.md`, optional `contracts/`, transient `plan.md`,
  and `tasks/tsk-####-<slug>.md`; no `design.md`, `tests.md`, or Stage 04.

- [ ] **Step 1: Enforce the concurrent-work precondition**

Before selecting any package, require the Spec 0137 work to be committed and the
isolated branch to have no unrelated changes. Recount 34 total packages, exactly
33 still carrying `spec-`, and seven Stage 04 files. Stop on mismatch.

- [ ] **Step 2: Write package/lifecycle RED tests**

```python
import unittest

class SpecPackageTests(unittest.TestCase):
    def test_spec_package_roles_and_execution_stage_are_exact(self) -> None:
        packages = load_spec_packages(Path("docs/03.specs"))
        self.assertTrue(
            all(not package.path.name.startswith("spec-") for package in packages)
        )
        self.assertTrue(
            all(not package.path.joinpath("design.md").exists() for package in packages)
        )
        self.assertTrue(
            all(not package.path.joinpath("tests.md").exists() for package in packages)
        )
        self.assertFalse(Path("docs/04.execution").exists())
```

Add lifecycle cases proving living completed Specs retain `spec.md`, completed
Plans/Tasks are removed after evidence, and one-time migration packages require a
recovery commit before deletion.

- [ ] **Step 3: Run RED and create an exact content-disposition report**

Classify every `design.md` paragraph as Spec Technical Approach/Acceptance
Contract, Plan risk/sequence/rollback, or cross-change ADR. Classify every
`tests.md` statement as an executable acceptance assertion or obsolete duplicate.
The report is a reviewed Migration block, not a permanent extra document.

- [ ] **Step 4: Move packages and integrate Stage 04 content**

Use native moves. Integrate the agentic research Plan/Task evidence into its
owning Stage 03 package, remove date-bearing execution filenames, and delete the
empty Stage 04 root. Move executable OpenAPI/GraphQL/Proto only into the owning
Spec `contracts/` directory.

- [ ] **Step 5: Run focused GREEN and lifecycle checks**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_spec_packages \
  tests.validation.test_document_corpus_lifecycle \
  tests.validation.test_document_metadata -v
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-document-links.py --mode traceability
git diff --check
```

- [ ] **Step 6: Review and commit Stage 03/04**

Stage each literal Task 7 File-list and reviewed consumer path, verify the
cached-name list, then:

```bash
git commit -m "refactor(specs): unify specification execution lifecycle"
```

### Task 8: Normalize the Operations Catalog and Remove Releases

**Files:**

- Modify: `docs/05.operations/README.md`
- Modify: all 13 tracked `docs/05.operations/catalog/<domain>/README.md` files
- Move: all 75 tracked `docs/05.operations/catalog/<domain>/ops-####-<slug>/`
  subjects to their exact `docs/05.operations/catalog/<domain>/####-<slug>/`
  Migration targets
- Modify: the 66 registered `guide.md`, 64 registered `policy.md`, and 62
  registered `runbook.md` role members only where the Migration marks a path,
  duplicate-role merge, or approved stale-reference rewrite
- Delete: `docs/05.operations/releases/README.md`
- Delete: every remaining tracked path under `docs/05.operations/releases/`
- Modify: `docs/99.templates/registry.json`
- Delete: `docs/99.templates/templates/operations/release.template.md`
- Modify: `docs/05.operations/incidents/README.md`
- Modify: `scripts/lib/document_governance/operations_catalog.py`
- Modify: `scripts/validation/check-operations-catalog.py`
- Modify: `tests/validation/test_operations_catalog.py`
- Modify: `tests/validation/test_operations_taxonomy.py`
- Modify: every Migration-declared active Operations path consumer
- Modify: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`

**Interfaces:**

- Consumes: approved Operations catalog manifest and Stage 99 Operations and
  Incident profiles.
- Produces: retained domain/subject topology, prefixless subject paths, stable
  registered member IDs, exact Incident packets, and no Release document role.

- [ ] **Step 1: Write topology and no-Release RED tests**

```python
import unittest

class OperationsTopologyTests(unittest.TestCase):
    def test_operations_topology_is_prefixless_and_release_free(self) -> None:
        catalog = load_operations_catalog(ROOT)
        self.assertEqual(len(catalog.domains), 13)
        self.assertEqual(len(catalog.subjects), 75)
        self.assertTrue(
            all(not subject.path.name.startswith("ops-") for subject in catalog.subjects)
        )
        self.assertFalse(ROOT.joinpath("docs/05.operations/releases").exists())
```

Add cases for duplicate role purpose, role-member ID change, an Incident outside
`incidents/<year>/inc-####-<slug>/`, a Release profile, and the deleted parallel
`docs/05.operations/guides/` topology reported by the old monolith.

- [ ] **Step 2: Run RED and freeze role-body witnesses**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_operations_catalog \
  tests.validation.test_operations_taxonomy -v
```

Generate source-derived semantic witnesses for every approved role rewrite and
duplicate merge. A witness must come from body text, not frontmatter, a heading,
or a stale path.

- [ ] **Step 3: Move subjects and rewrite exact active consumers**

Use `git mv` for every subject. Keep domain/subject ownership and role filenames.
Rewrite only consumers selected by Migration and typed consumer discovery;
immutable Stage 98 recovery fields are not active consumers.

- [ ] **Step 4: Remove Releases and repair operational ownership**

Delete Release profiles, templates, navigation, validators, fixtures, and
tracked Release documents. Deployment planning stays in a Spec Plan; release
execution/rollback remains in the registered workspace delivery Runbook;
`CHANGELOG.md` and Git tags remain repository release history.

- [ ] **Step 5: Run complete semantic and topology GREEN**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_operations_catalog \
  tests.validation.test_operations_taxonomy -v
python3 scripts/validation/check-operations-catalog.py --mode complete
python3 scripts/validation/check-document-links.py --mode alignment
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
git diff --check
```

Expected: 13 domains, 75 semantic subjects, no `ops-` target, exact role
membership and Incident topology, no Releases, and no restored guide root.

- [ ] **Step 6: Review and commit Operations**

Stage each literal Task 8 File-list and reviewed consumer path, verify the
cached-name list, then:

```bash
git commit -m "refactor(operations): normalize catalog subjects"
```

### Task 9: Reduce Stage 90 to Research, Audit, and Data Packages

**Files:**

- Modify: `docs/90.references/README.md`
- Move: every registered current package under `docs/90.references/research/`
  to its exact `docs/90.references/research/####-<slug>/` Migration target
- Move: every registered current package under `docs/90.references/audits/`
  to its exact `docs/90.references/audits/####-<slug>/` Migration target
- Move: every registered current structured inventory to its exact
  `docs/90.references/data/####-<slug>/` Migration target
- Move: each tracked `docs/90.references/learning/` document to either its
  approved Stage 05 Guide owner or Stage 90 Research target
- Move: generated `docs/90.references/llm-wiki/` outputs to the approved Data
  package and preserve generator ownership
- Delete: empty `docs/90.references/learning/` and
  `docs/90.references/llm-wiki/` roots
- Delete: every registered deprecated redirect document
- Create: `scripts/lib/document_governance/references.py`
- Create: `tests/validation/test_reference_packages.py`
- Modify: `scripts/knowledge/generate-llm-wiki.py`
- Modify: `scripts/knowledge/generate-llm-wiki-index.sh`
- Modify: `scripts/knowledge/generate-llm-wiki-coverage.sh`
- Modify: `tests/validation/test_generate_llm_wiki.py`
- Modify: `tests/validation/test_llm_wiki_retiring_pack_exclusion.py`
- Modify: `scripts/lib/document_governance/metadata_validator.py`
- Modify: every Migration-declared active Stage 90 consumer
- Modify: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`

**Interfaces:**

- Consumes: Stage 99 Research, Audit, and Data profiles plus Migration content
  dispositions.
- Produces: package IDs `RES-####`, `AUD-####`, or `DATA-####`; prefixless,
  date-free package paths; and generated Data outputs with canonical provenance.

- [ ] **Step 1: Write category, path, and authority RED tests**

```python
import unittest

class ReferencePackageTests(unittest.TestCase):
    def test_reference_roots_and_package_paths_are_exact(self) -> None:
        corpus = load_reference_packages(Path("docs/90.references"))
        self.assertEqual(corpus.category_names, ("audits", "data", "research"))
        self.assertTrue(
            all(PACKAGE_PATH.fullmatch(item.relative_package) for item in corpus)
        )
        self.assertFalse(any(item.overrides_normative_stage for item in corpus))
```

Mutation cases cover dated names, `res-`/`aud-` path prefixes, redirect-only
documents, current clickable links to retired paths, and a Stage 90 assertion
that overrides Stage 00/01/02/03/05 authority.

- [ ] **Step 2: Run RED and classify every source row**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_reference_packages \
  tests.validation.test_generate_llm_wiki \
  tests.validation.test_llm_wiki_retiring_pack_exclusion -v
```

Record `research`, `audit`, `data`, `guide`, or `delete-redirect` on every source
in Migration `mig-0003`. Stop on any unclassified file.

- [ ] **Step 3: Move packages and update generators**

Use native moves for tracked packages. Preserve external citations and audit
scope while removing normative wording. Update the LLM Wiki generator's exact
registered destinations, then run it once with `--write` and once in check mode.

- [ ] **Step 4: Rewrite current links and convert historical links**

Current consumers link new packages. An obsolete-path citation becomes an
approved Git commit or Migration reference; it does not remain a clickable
current link. Stage 98 recovery text is immutable evidence and is not rewritten
as a current consumer.

- [ ] **Step 5: Run focused GREEN and freshness gates**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_reference_packages \
  tests.validation.test_generate_llm_wiki \
  tests.validation.test_llm_wiki_retiring_pack_exclusion -v
python3 scripts/knowledge/generate-llm-wiki.py --check
python3 scripts/validation/check-document-links.py --mode alignment
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
git diff --check
```

- [ ] **Step 6: Review and commit Stage 90**

Stage each literal Task 9 File-list and reviewed consumer path, verify the
cached-name list, then:

```bash
git commit -m "refactor(references): simplify evidence packages"
```

### Task 10: Minimize Stage 98 and Centralize Recovery Provenance

**Files:**

- Modify: `docs/98.archive/README.md`
- Move: `docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md` to
  `docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md`
- Move: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
  to `docs/98.archive/migrations/0002-operations-catalog-convergence.md`
- Move: `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`
  to `docs/98.archive/migrations/0003-workspace-governance-simplification.md`
- Replace: the 146 tracked `docs/98.archive/changes/` packets with exact minimal
  Migration or Tombstone rows selected by the preservation audit
- Replace: the 38 tracked Tombstones with minimal
  `docs/98.archive/tombstones/<original-stage>/####-<slug>.md` records only when
  the stable deleted path still needs direct recovery lookup
- Delete: empty `docs/98.archive/changes/` and obsolete snapshot roots
- Create: `scripts/lib/document_governance/archive.py`
- Create: `scripts/lib/document_governance/provenance_policy.py`
- Create: `tests/validation/test_archive_minimization.py`
- Create: `tests/validation/test_provenance_policy.py`
- Modify: `scripts/lib/document_governance/git_provenance.py`
- Modify: `scripts/validation/check-document-corpus-lifecycle.py`
- Modify: `tests/validation/test_document_corpus_lifecycle.py`
- Modify: every active Archive index or Migration consumer

**Interfaces:**

- Consumes: source Git object identities and approved disposition rows.
- Produces: `RecoveryReference(commit, original_path)` and minimal Migration or
  Tombstone documents. Recovery uses one commit-level identity, never line SHA,
  branch snapshot, or whole-archive count.
- Migration 0003 may retain its approved execution fields through Task 10 because
  they are required to execute and review later transitions. Task 13 compacts
  the durable completed Migration to mapping and recovery fields only.

- [ ] **Step 1: Write minimal-archive RED tests**

```python
import unittest

class ArchiveMinimizationTests(unittest.TestCase):
    def test_archive_has_only_minimal_registered_roots(self) -> None:
        archive = load_archive(Path("docs/98.archive"))
        self.assertEqual(
            archive.root_entries, ("README.md", "migrations", "tombstones")
        )
        self.assertFalse(Path("docs/98.archive/changes").exists())
        self.assertTrue(all(item.is_minimal for item in archive.tombstones))
```

Add recovery negatives for nonexistent commit objects, missing original blobs,
symlink/tree sources, null recovery on completed deletion, line-number SHAs,
snapshot counts, active direct Tombstone links, and archived superseded ADRs.
Add repository-policy mutations for Markdown branch snapshots, line-number SHAs,
duplicated digest fields, and fixed-HEAD fixtures. Positive fixtures retain only
external security pins, Migration/Tombstone recovery, canonical generated-output
provenance, and runtime CI base/head selection.

- [ ] **Step 2: Run RED and generate the preservation decision table**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_archive_minimization \
  tests.validation.test_provenance_policy -v
```

Expected: FAIL on the current Change packets, non-minimal Tombstones, duplicated
provenance, and fixed-HEAD fixtures.

For all 184 existing Change/Tombstone files, select exactly one disposition:
`migration-row`, `minimal-tombstone`, or `git-only`. Record stable path,
replacement, reason, and recovery commit. Require a reviewer decision for every
non-`git-only` row before deletion.

- [ ] **Step 3: Verify recovery before reducing content**

Implement `validate_recovery_rows(rows, repo) -> tuple[Finding, ...]` with
argument-vector Git calls (`git cat-file -e commit:path` and `git cat-file -t
commit:path`) for each parsed Migration value. Expose the bounded mode and run:

```bash
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-recovery
```

The validator requires the existence check to succeed and type to equal `blob`
for every deleted document body. It rejects NUL/control characters, leading
hyphens, invalid object IDs, symlinks, trees, and unregistered row fields before
constructing the argument vector.

- [ ] **Step 4: Move Migrations, write minimal Tombstones, delete snapshots**

Use native moves for the three Migrations. Tombstones contain only old path,
replacement or `none`, reason, status, and recovery commit. Do not copy retired
Spec/Plan/Task bodies. Preserve Migration 0003's reviewed execution ledger without
expanding it; its per-mapping flow rows remain temporary execution evidence.

- [ ] **Step 5: Run focused GREEN and provenance mutation tests**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_archive_minimization \
  tests.validation.test_provenance_policy \
  tests.validation.test_document_corpus_lifecycle -v
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-document-links.py --mode traceability
git diff --check
```

- [ ] **Step 6: Review and commit Stage 98**

Stage each literal Task 10 File-list and reviewed consumer path, verify the
cached-name list, then:

```bash
git commit -m "refactor(archive): retain minimal recovery records"
```

### Task 11: Mirror Script/Test Ownership and Create Six Public Suites

**Files:**

- Modify: `scripts/README.md`
- Modify: `scripts/manifest.yaml`
- Create: `scripts/lib/document_governance/suite_registry.py`
- Create: `tests/lib/document_governance/test_suite_registry.py`
- Move: document-governance library unit tests currently under
  `tests/validation/` to exact mirrored targets under
  `tests/lib/document_governance/` as registered in `scripts/manifest.yaml`
- Keep: CLI/aggregate contract tests under `tests/validation/`
- Create: `tests/docs/README.md`
- Create: `tests/setup/README.md`
- Create: `tests/qa/README.md`
- Create: `tests/lib/README.md`
- Create: `tests/validation/README.md`
- Modify: `scripts/validation/check-script-manifest.py`
- Modify: `tests/validation/test_script_manifest.py`
- Modify: `scripts/validation/ci_gate_contract.py`
- Modify: `tests/validation/test_ci_gate_contract.py`
- Modify: `scripts/validation/ci_gate_runner.py`
- Modify: `tests/validation/test_ci_gate_runner.py`

**Interfaces:**

- Consumes: atomic validator rows from `scripts/manifest.yaml`.
- Produces: exact public suite names `document-contract`, `document-graph`,
  `document-lifecycle`, `operations`, `agent-governance`, and
  `repository-integrity`. `suite_registry.load()` returns immutable suites and
  rejects a validator mapped to zero or multiple suites.

- [ ] **Step 1: Write suite ownership and mirrored-test RED tests**

```python
import unittest

class SuiteRegistryTests(unittest.TestCase):
    def test_public_suites_and_atomic_ownership_are_exact(self) -> None:
        registry = load_suite_registry(Path("scripts/manifest.yaml"))
        self.assertEqual(
            registry.public_names,
            (
                "agent-governance", "document-contract", "document-graph",
                "document-lifecycle", "operations", "repository-integrity",
            ),
        )
        self.assertTrue(
            all(len(item.public_suites) == 1 for item in registry.validators)
        )
        self.assertTrue(
            all(item.has_mirrored_test for item in registry.production_modules)
        )
```

Add mutation cases for duplicate behavioral consumers, a suite containing logic,
missing mirrored tests, stale successor edges, write-capable scripts declared
`mutation: none`, cycles, and untracked/non-executable CLI entrypoints.

- [ ] **Step 2: Run RED against the known 19-failure baseline**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_script_manifest \
  tests.validation.test_ci_gate_contract \
  tests.lib.document_governance.test_suite_registry -v
```

Record each failure owner; do not weaken assertions or add transition exceptions.

- [ ] **Step 3: Split responsibility without changing behavior**

Move side-effect-free logic to focused library modules and leave CLIs as argument
and rendering adapters. Move their unit tests to mirrored paths. Do not combine
focused implementations or fixtures inside public suite modules.

- [ ] **Step 4: Replace repository-sized fixtures with registry builders**

Each validator gets one smallest valid fixture from Stage 99 plus boundary
mutations for symlink, containment, traversal, invalid UTF-8, and unsafe writes
where applicable. Long repository integration remains `profile: full` only.

- [ ] **Step 5: Run focused GREEN and manifest validation**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_script_manifest \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.lib.document_governance.test_suite_registry -v
python3 scripts/validation/check-script-manifest.py
git diff --check
```

Expected: the 19-failure baseline is zero without allowlisting retired files.

- [ ] **Step 6: Review and commit test/script ownership**

Stage each literal Task 11 File-list and reviewed manifest path, verify the
cached-name list, then:

```bash
git commit -m "refactor(validation): mirror ownership and register suites"
```

### Task 12: Route Every Gate Through the Six Suites and Delete Legacy Validators

**Files:**

- Modify: `scripts/validation/run-ci-gate.py`
- Modify: `scripts/validation/ci_gate_adapters.py`
- Modify: `scripts/validation/ci_gate_contract.py`
- Modify: `scripts/validation/ci_gate_runner.py`
- Modify: `.github/workflow-contract.yml`
- Modify: `.github/workflows/ci-quality.yml`
- Modify: `.pre-commit-config.yaml`
- Modify: `scripts/validation/run-local-qa-gates.sh`
- Modify: `scripts/hooks/agent-event-hook.sh`
- Modify: `scripts/hooks/post-tool-validate.sh`
- Modify: `.claude/settings.json`
- Modify: `.github/INDEX.md`
- Modify: `scripts/validation/target_surface_delta_contract.py`
- Modify: `scripts/validation/github_workflow_contract.py`
- Modify: `scripts/validation/generate-security-automation-readiness.sh`
- Delete after successor coverage: `scripts/validation/recommend-qa-gates.sh`
- Modify: `docs/00.agent-governance/providers/claude.md`
- Modify: `docs/00.agent-governance/providers/codex.md`
- Assert absent from Task 4:
  `docs/00.agent-governance/providers/agents-md.md`
- Assert absent from Task 4:
  `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml`
- Modify: `tests/validation/test_ci_gate_adapters.py`
- Modify: `tests/validation/test_ci_gate_contract.py`
- Modify: `tests/validation/test_ci_gate_runner.py`
- Modify: `tests/validation/test_github_workflow_contract.py`
- Modify: `tests/validation/test_target_surface_delta_contracts.py`
- Modify: `tests/validation/test_security_automation_readiness.py`
- Delete: `scripts/validation/check-repo-contracts.sh`
- Delete: every script whose `scripts/manifest.yaml` lifecycle is `transition`
  or `merge` after its successor has exact consumer and test coverage
- Modify: `scripts/manifest.yaml`

**Interfaces:**

- Consumes: Task 11 immutable suite registry and atomic validator adapters.
- Produces: `run-ci-gate.py --profile changed|full [--explain]`. Explain mode
  renders selected suite -> validator mappings without executing validators.

- [ ] **Step 1: Write routing parity and legacy-absence RED tests**

```python
import unittest

class GateRoutingTests(unittest.TestCase):
    def test_all_entrypoints_select_only_public_suites(self) -> None:
        contract = load_ci_gate_contract()
        self.assertEqual(contract.pre_commit, contract.local_changed)
        self.assertEqual(contract.pull_request, contract.ci_changed)
        self.assertEqual(contract.push, contract.ci_full)
        self.assertFalse(Path("scripts/validation/check-repo-contracts.sh").exists())
```

Add cases proving `--explain` covers every atomic validator exactly once,
unknown suites fail closed, changed-path selection cannot skip impacted suites,
and workflows/hooks contain no copied validator command.

- [ ] **Step 2: Run RED and capture all current consumers**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_github_workflow_contract -v
```

Before deleting a legacy entrypoint, require `rg -l` and manifest semantic
consumer discovery to agree on zero current consumers after rewrites.

Run the exact active-surface scan:

```bash
rg -n 'check-repo-contracts' .codex .claude scripts/hooks \
  docs/00.agent-governance .github .pre-commit-config.yaml scripts/validation
```

Before deletion this scan must name only files in the Task 12 file list. After
rewrites and deletion it may name only non-clickable Migration recovery evidence;
current hooks, generated settings, docs, workflows, contracts, and scripts must
have zero match.

- [ ] **Step 3: Route local, pre-commit, PR, and push profiles**

Make every surface call `run-ci-gate.py` with a profile. Keep suite composition
in the manifest/contract; workflows and hooks contain no policy logic.

- [ ] **Step 4: Delete the monolith and completed transition scripts**

Delete only scripts whose successor, tests, consumers, mutation mode, and
executable permissions pass the manifest contract. Never replace the old
monolith with another cross-responsibility implementation.

- [ ] **Step 5: Run suite/routing GREEN**

```bash
python3 scripts/validation/run-ci-gate.py --profile changed --explain
python3 scripts/validation/run-ci-gate.py --profile full --explain
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_ci_gate_adapters \
  tests.validation.test_ci_gate_contract \
  tests.validation.test_ci_gate_runner \
  tests.validation.test_github_workflow_contract \
  tests.validation.test_target_surface_delta_contracts \
  tests.validation.test_security_automation_readiness \
  tests.validation.test_script_manifest -v
python3 scripts/validation/check-script-manifest.py
git diff --check
```

- [ ] **Step 6: Review and commit gate routing**

Stage each literal Task 12 File-list and exact zero-consumer rewrite, verify the
cached-name list, then:

```bash
git commit -m "refactor(ci): route validation through public suites"
```

### Task 13: Close the Migration and Retire the One-Time Spec Package

**Files:**

- Modify: `docs/99.templates/README.md`
- Modify: `docs/99.templates/templates/README.md`
- Modify: `docs/99.templates/templates/common/README.md`
- Delete: every tracked path under `docs/99.templates/support/`
- Delete: retired templates under `docs/99.templates/templates/changes/`
- Delete: the registry-replaced tracked files under
  `docs/99.templates/templates/sdlc/` and
  `docs/99.templates/templates/spec-contracts/`
- Delete: the registry-replaced
  `docs/99.templates/templates/common/archive.template.md`,
  `docs/99.templates/templates/common/audit.template.md`, and
  `docs/99.templates/templates/common/reference.template.md`
- Delete: retired `design.template.md`, `tests.template.md`, and separate
  PRD/SRS/Interface Requirement templates
- Modify: all registered generated provider and Stage 90 Data outputs
- Modify: `docs/98.archive/migrations/0003-workspace-governance-simplification.md`
- Modify: `docs/98.archive/README.md`
- Modify: `tests/validation/test_workspace_governance_migration.py`
- Delete in the retirement commit:
  `docs/03.specs/0153-workspace-governance-simplification/README.md`,
  `spec.md`, `plan.md`, and all thirteen `tasks/tsk-####-<slug>.md` files
- Modify: every active link to Spec 0153 so it resolves through ADR-0029,
  Migration 0003, Stage 00, or Stage 99 according to purpose

**Interfaces:**

- Consumes: completed Migration rows, six public suites, canonical generators,
  and the closure commit object.
- Produces: a clean final tree, completed Migration 0003 with non-null recovery
  commit/path pairs, and no one-time Spec 0153 package.

- [ ] **Step 1: Prove legacy Stage 99 consumers are zero**

```bash
rg -n 'docs/99\.templates/support|templates/changes|design\.template|tests\.template|prd\.template|srs\.template|interface.*template' \
  docs scripts tests .github .agents .claude .codex AGENTS.md CLAUDE.md
```

Expected: no active consumer. Migration recovery text is inspected separately
and is not rewritten into an active link.

- [ ] **Step 2: Delete retired Stage 99 surfaces and regenerate outputs**

Delete only registry-replaced support/templates. Run each registered generator
once with `--write`, then all in check mode. Generated output diffs must equal
their manifest-declared destinations.

- [ ] **Step 3: Run all six public suites and document gates**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-document-links.py --mode traceability
python3 scripts/validation/check-document-links.py --mode alignment
python3 scripts/validation/check-operations-catalog.py --mode complete
python3 scripts/validation/check-agent-governance-contract.py
python3 scripts/validation/check-script-manifest.py
git diff --check
```

Expected: every command exits zero. Record counts and durations only after the
run; never write prospective PASS evidence.

- [ ] **Step 4: Obtain independent final reviews**

Require one specification/architecture review and one implementation/security
quality review over the complete branch diff. Resolve all Critical and Important
findings, rerun affected focused gates, then rerun the full profile once.

- [ ] **Step 5: Complete Migration evidence and create the closure commit**

First add or update the focused final-state fixture and mutations. The fixture
uses schema version `3` and only `schema_version`, `migration_id`, and `rows` at
the top level. Each row has exactly `source_path`, `target_path`, `artifact_id`,
`action`, and `recovery_commit`. Add mutations for schema version `2`, null
recovery, and every execution-only top-level or row field.

Run RED before changing the durable Migration:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Expected RED: the completed fixture or at least one mutation proves the pending
execution schema cannot serve as the final compacted schema. Implement the
minimal schema-version-3 mapping and rerun the same command. Expected GREEN:
both pending/approved execution fixtures and final compacted fixtures pass their
state-specific contracts, while all cross-state mutations fail closed.

Set every executed row to `completed`; bind deleted/moved source recovery to an
existing regular blob commit; update allocation high-water values; record exact
suite evidence and review verdicts. Commit the still-present Spec package with
the completed evidence. Stage each literal Task 13 closure path and verify the
cached-name list, then:

```bash
git commit -m "docs: complete workspace governance convergence"
```

Resolve that commit with `git rev-parse HEAD` and write it as the recovery commit
for the one-time Spec 0153 package rows. This avoids a self-referential commit.

Then compact the durable Stage 98 Migration to schema version `3`. Its top level
contains only `schema_version`, `migration_id`, and `rows`; every row contains exactly
`source_path`, `target_path`, `artifact_id`, `action`, and `recovery_commit`.
Drop pending-only approval, owner, status, source-kind, source-owner, planned
creation, consumer-policy, derived-consumer, and row-identity fields. A focused
minimality assertion must reject any extra field or null recovery for an
executed mapping before retirement proceeds.

- [ ] **Step 6: Retire Spec 0153 and its transient execution evidence**

Verify the closure commit contains each package file with `git cat-file -e`,
remove the package files listed above, and update current links. Keep only ADR
0029 and Migration 0003 as durable decision/recovery evidence. Stage only the
literal retirement/dependent-link paths and verify the cached-name list. Confirm
that every pending planned creation is represented by an executed mapping before
the temporary creation registry is dropped during compaction.

- [ ] **Step 7: Run retirement-focused and full final verification**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration \
  tests.validation.test_document_corpus_lifecycle -v
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/check-document-links.py --mode traceability
git diff --check
```

- [ ] **Step 8: Commit the retirement unit and finish the branch**

```bash
git commit -m "docs(spec): retire completed governance migration"
```

Use `superpowers:finishing-a-development-branch` to present the verified merge,
push/PR, keep, or discard options. Do not push, merge, or delete the branch
without the user's separate explicit choice.

## Verification

### Task-level verification

Every Task follows the same evidence order:

1. Freeze the selected Migration/manifest/registry inventory and compare it to
   tracked regular files.
2. Add a focused RED that fails for the exact missing behavior.
3. Implement only the selected logical unit.
4. Run the focused GREEN tests plus their mutation cases.
5. Run changed metadata, relevant document graph mode, and `git diff --check`.
6. Obtain independent specification and quality review.
7. Stage only Task-owned files and create one Conventional Commit.

### Stage exit verification

| Stage boundary | Required evidence |
| :--- | :--- |
| Stage 99 | Registry/schema/template tests; metadata and lifecycle consumers read registry; no Release/Gemini profile |
| Stage 00 | Two-provider governance contract; generated projection parity; no memory/Gemini/Antigravity current token |
| Stage 01 | 25 Requirement Packages; full package-owned IDs; no legacy PRD/SRS/IFR identity |
| Stage 02 | 25 descriptions and 26 decisions after ADR-0029; prefixless paths; reciprocal acyclic supersession |
| Stage 03/04 | 34 migrated packages before lifecycle retirement; no design/tests roles; no Stage 04 |
| Stage 05 | 13 domains, 75 prefixless subjects, registered role membership, exact Incidents, no Releases |
| Stage 90 | only Research/Audit/Data roots; generator freshness; no redirect authority |
| Stage 98 | only README/Migrations/Tombstones; every deletion recoverable; no snapshot bodies |
| Scripts/tests | mirrored responsibility; manifest clean; six exact suites |
| Final | six full suites, metadata/lifecycle/links/Operations/agent/manifest, independent `C0/I0` reviews |

### Baseline handling

The existing 233 alignment findings, ten monolith contract failures, two
Operations index findings, and nineteen script-manifest failures are explicit
migration inputs. A Task may close only its owned subset; it may not rename a
baseline failure to a warning, skip it, or claim a repository-wide PASS before
Task 13. Task 13 requires zero findings.

## Risk and Rollback

| Risk | Prevention | Rollback |
| :--- | :--- | :--- |
| Registry/corpus deadlock | Install registry and transition rows before first move | Revert the Task 2 commit; no corpus path has moved |
| Bulk rewrite changes history or runtime files | Select exact typed consumers and exclude recovery evidence | Revert the single stage commit; recover source blobs from its parent |
| ID collision or reuse | Enforce registry high-water and path/ID ownership before moves | Stop before commit; restore the Task worktree from the prior logical commit |
| Semantic loss during consolidation | Freeze source-derived body witnesses and require reviewed disposition rows | Recover exact blob from Migration recovery commit/path |
| Generated surface becomes authority | Compare outputs to Stage 00/90 sources and manifest destinations | Revert generated outputs and renderer in the same logical commit |
| Gate reduction hides validation | Map every atomic validator to exactly one suite and mutation-test routing | Revert Task 12 while keeping focused validators from Task 11 |
| Concurrent Spec 0137 overlap | Require committed clean precondition before Task 7 | Stop; do not stage or overwrite the overlapping path |
| Archive reduction loses recovery | Verify commit:path regular blob before deletion | Restore from the verified Git object and repair the ledger |
| One-time Spec deletion loses execution evidence | Create closure commit first, then record it in Migration 0003 | Restore package files from the closure commit |

No rollback uses `git reset --hard`, unbounded deletion, copy-based rename, or
history rewrite. Reverts are logical-commit scoped or exact Git-object restores.

## Approval Gates

- The approved Spec 0153 design is the authority for execution depth and folder
  ownership; no further structural choice is inferred during implementation.
- Task 1 requires review of the complete Migration selection before any corpus
  move.
- Task 4 requires confirmation that all supported provider behavior is present
  in Claude/Codex before Gemini/Antigravity deletion.
- Tasks 5-10 require disposition review for every merge, content integration,
  or deletion; path-only native renames need inventory proof but no new design.
- Task 10 requires explicit preservation decisions for all 184 existing Archive
  records.
- Task 12 requires exact consumer-zero proof before any legacy script deletion.
- Task 13 requires user approval before any push, merge, or branch deletion.

## Completion Criteria

- The final tracked roots and ownership boundaries match Spec 0153 exactly.
- Stage 99 is the only machine document authority and contains no duplicate
  support rules or retired template profile.
- Stage 00 contains no project memory and supports only Claude and Codex.
- Stage 01/02/03/05/90/98 paths, IDs, lifecycles, links, and templates satisfy
  their registered profiles with no compatibility copy or redirect body.
- `docs/04.execution/`, `docs/05.operations/releases/`, `.gemini/`,
  `GEMINI.md`, Gemini/Antigravity governance, and the completed one-time Spec
  0153 package are absent.
- All moved/deleted stable paths have non-reused IDs and exact Git recovery.
- Scripts and tests mirror responsibility; no duplicate/transition script or
  repository-sized fixture remains.
- The six public suites cover every atomic validator exactly once and all final
  required commands exit zero.
- Independent final specification and quality reviews report no Critical or
  Important findings.
- Every logical unit is committed with a Conventional Commit and the worktree
  contains no Task-owned uncommitted change.

## Related Documents

- `docs/03.specs/0153-workspace-governance-simplification/spec.md`
- `docs/02.architecture/decisions/0029-workspace-governance-authority.md`
- `docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/99.templates/README.md`
- `scripts/manifest.yaml`
- `.github/workflow-contract.yml`
