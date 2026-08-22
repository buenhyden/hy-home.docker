---
status: active
artifact_id: plan-0136
artifact_type: plan
parent_ids:
  - spec-0136
created: 2026-08-07
updated: 2026-08-13
---
# SDLC Taxonomy and Agent Governance Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Converge the documentation, agent-governance, archive, template,
validator, CI, and script corpus onto the approved stable-ID SDLC taxonomy
without leaving legacy, deprecated, dated-path, duplicate, or compatibility
surfaces.

**Architecture:** Typed Stage 00 and Stage 99 contracts define authority and
document shape; a focused document-governance library enforces those contracts;
a migration ledger accounts for every path change; and the typed workflow graph
runs identical leaf gates locally and in CI. Corpus movement follows contract
installation, and transition allowances are removed in the final task.

**Tech Stack:** Python 3.12+, Bash, PyYAML, html5lib, Git, unittest,
GitHub Actions, Markdown, and repository-local typed YAML contracts.

## Global Constraints

- Operations remains docs/05.operations; it is never renumbered.
- Current Operations domains exist only under
  `docs/05.operations/catalog/<domain>/`; `incidents/` and `releases/` are
  siblings of `catalog/`, not domains.
- Operations subjects use `ops-####-<managed-object-or-operational-capability>`.
  Retain Guide, Policy, and Runbook only when each owns distinct role semantics;
  similarity alone never authorizes a merge or deletion.
- docs/02.architecture/requirements is replaced by descriptions and
  Architecture Description.
- docs/04.execution is removed after Plan and Task migration.
- Every documentation identity uses a stable type ID with exactly four digits
  and a slug; no date prefix or identity-bearing year partition remains. The
  sole year containment exception is
  `docs/05.operations/incidents/<year>/inc-####-<slug>/`.
- Internal requirement and acceptance identifiers use four digits, including
  `PRD-0001-R0001`, `PRD-0001-AC0001`, `SRS-0001-R0001`, and
  `IFR-0001-R0001`.
- Dates live in typed frontmatter. Event timelines may retain timestamps in
  body content.
- docs/98.archive is the only documentation archive.
- Active documents never link directly to Stage 98.
- No redirect, legacy, deprecated, dormant, or compatibility file remains at
  completion.
- When an earlier rule, term, template, validator, script, or provider
  projection conflicts with the approved typed owner, preserve any unique
  valid semantics in the owner, migrate consumers, and delete the predecessor.
- Each AI agent has one typed canonical function/role contract; provider-local
  surfaces are generated projections and do not copy independent policy.
- Agent and function counts are review outcomes rather than fixed targets;
  duplicate or consumerless roles are consolidated or deleted after their
  valid behavior moves.
- Review every SDLC term and template for a necessary, non-duplicated role
  before corpus-wide enforcement.
- One-time migration utilities remain under /tmp and are never committed.
- Every generator defaults to check mode; repository mutation requires
  explicit --write.
- Runtime-changing scripts require an Operations Runbook and are never executed
  as part of document migration.
- Use git mv for tracked path moves.
- Preserve unrelated user changes and do not rewrite Git history.
- Commit each Task as its own logical unit after its scoped verification passes.
- Do not push, merge, modify remote resources, change secrets, or change
  Compose runtime topology.

---

## Context and Inputs

The approved specification is
docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md. The starting commit for the
implementation plan is e3e7615d.

The revised design checkpoint is `a626ae79`. Tasks 1 through 9 are complete.
Task 10 validator extraction and Task 10A four-digit identity work were already
in progress when the revised Operations catalog design was approved. Preserve
those worktree changes, complete and commit Task 10 before Task 10A, then
execute the new Operations tasks below. Do not reset, re-create, or fold the
two in-progress units together.

Measured starting debt:

| Surface | Starting condition |
| :-- | :-- |
| Stage 01 | 25 legacy-numbered PRDs |
| Stage 02 | 25 ARDs and 25 ADRs |
| Stage 03 | 27 active Spec directories and 22 child READMEs |
| Stage 04 | 102 dated Plans and 130 dated Tasks |
| Stage 05 | 66 Guides, 64 Policies, 62 Runbooks, and 71 READMEs |
| Stage 90 | 92 Markdown files plus 5 other artifacts, including dated paths |
| Stage 98 | 52 tombstones; 32 contain full Spec bodies |
| Metadata | 1,276 active findings across 303 documents |
| Alignment | 184 findings, including 182 active-to-archive links |
| Lifecycle | 25 promoted findings and 20 provenance-incomplete tombstones |
| Scripts | 63 tracked files, 59 executable Python or Shell files |

Pre-flight baseline on the isolated worktree:

- tests/validation/test_document_metadata.py runs 225 unittest cases.
- 209 pass and 16 fail on the starting tree.
- The 16 failures are existing Template, Registry, README-count, and
  repository-contract delegation drift covered by Tasks 2, 6D, and 11.
- No Task may increase the 16-failure baseline. Task 2 must either resolve a
  failure or leave it explicitly attributable to Task 6D or Task 11; Task 11
  must reduce the focused suite to zero failures.

The existing Graphify report was built from f8a72211 and is advisory. Tracked
source, typed contracts, stage documents, and validators are authoritative.

### File Responsibility Map

| Unit | Files and responsibility |
| :-- | :-- |
| Authority | docs/00.agent-governance/contracts/*.yaml and rules/*.md |
| Document profiles | docs/99.templates/support/document-metadata-profiles.yaml |
| Lifecycle and archive | lifecycle-status.md, archive-retention-contract.md, corpus migration contracts |
| Templates | docs/99.templates/templates/sdlc and templates/operations |
| Path engine | scripts/lib/document_governance/ |
| Metadata CLI | scripts/validation/check-document-metadata.py |
| Lifecycle CLI | scripts/validation/check-document-corpus-lifecycle.py |
| Link CLI | scripts/validation/check-document-links.py |
| Operations catalog authority | docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md |
| Operations catalog CLI | scripts/validation/check-operations-catalog.py |
| Operations catalog tests | tests/validation/test_operations_catalog.py |
| Script inventory | scripts/manifest.yaml |
| Gate graph | .github/workflow-contract.yml |
| CI entrypoint | scripts/validation/run-ci-gate.py |
| Human history | docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md |

### Script Disposition Baseline

Task 3 records every tracked script file individually. These decisions are
mandatory unless Task 3 proves an active consumer or test that changes the
decision and records the evidence:

| Paths | Initial disposition |
| :-- | :-- |
| scripts/hooks/patch-graphify-post-commit.sh | merge into canonical hook generation, then delete |
| scripts/hooks/post-tool-validate.sh | rewrite as non-mutating typed dispatcher |
| scripts/knowledge/generate-llm-wiki-index.sh and generate-llm-wiki-coverage.sh | merge, then delete both old files |
| scripts/validation/check-doc-traceability.sh and check-doc-implementation-alignment.sh | merge into check-document-links.py, then delete |
| scripts/validation/check-repo-contracts.sh | decompose, replace residual invariants, then delete |
| scripts/validation/recommend-qa-gates.sh | merge into run-ci-gate.py --recommend, then delete |
| scripts/validation/report-provider-hook-parity.sh | merge into provider_surface_renderer.py, then delete |
| scripts/validation/recommend-gap-routing.sh | move routing to typed governance and delete |
| metadata and lifecycle CLIs | retain thin CLIs, extract shared library |
| CI gate runner, contract, adapters, and public runner | retain |
| provider renderer and sync wrapper | retain |
| target-surface CLI/core pairs | retain while Spec 135 and tests consume them |
| recurring PostgreSQL and sample-delivery rehearsals | retain only with current Runbook links and tests; replace dated Task paths |
| security, Compose, hardening, and secret operations | retain when current Runbooks and tests consume them |
| consumerless report, recommendation, fixture, or rehearsal | merge evidence into its owner and delete |

## Goals and Non-goals

### Goals

- Make the target taxonomy executable through typed contracts and tests.
- Preserve complete Git provenance for every move and deletion.
- Keep each migration Task independently reviewable.
- End with zero legacy transition allowances.
- End with one validator implementation for each policy topic.
- End with every tracked script justified by an owner, consumer, mutation
  profile, and test.

### Non-goals

- Deploying or restarting services.
- Regenerating external credentials.
- Running destructive incident or recovery commands.
- Rewriting archived Git history.
- Creating empty SRS, Interface Requirement, Incident, Postmortem, or Release
  instances merely to exercise a template.

### Spec Coverage Map

| Spec acceptance criterion | Implementing Task |
| :-- | :-- |
| Target top-level taxonomy and Stage 04 absence | Task 5 |
| Architecture Description replaces ARD | Tasks 2 and 4 |
| Spec, Plan, and Task co-location | Task 5 |
| No parallel Operations role roots | Tasks 6A through 6D |
| Operations domains moved under catalog | Tasks 10B and 10C |
| Operations subject naming and role-purpose consolidation | Tasks 10B and 10D through 10H |
| Incidents and releases remain outside catalog | Tasks 10B, 10C, and 10H |
| No date or year path identity, except Incident containment | Tasks 4 through 7, Task 10A, and Task 14 |
| Four-digit document IDs and year-partitioned Incident packets | Task 10A |
| Four-digit internal requirement and acceptance IDs | Task 10A |
| Typed frontmatter dates | Tasks 2, 4 through 7 |
| Stage 98 is the sole archive | Task 7 |
| No active-to-archive links | Tasks 5, 7, 10, and 13 |
| Stage 99 matches the taxonomy | Tasks 2, 10A, 10B, and 10H |
| Stage 00 has one authority model and reviewed per-agent contracts | Tasks 2, 8, 10A, and 14 |
| Every script has owner, consumer, mutation, and test | Tasks 3 and 9 |
| Duplicate and one-time scripts are absent | Tasks 9 and 11 |
| Validator ownership and local/CI parity | Tasks 10, 10B, 11, and 12 |
| Complete migration ledger | Tasks 3 through 14 |
| All final gates pass without grandfathered debt | Task 14 |

## Work Breakdown

### Task 1: Add the Stable Document Taxonomy Engine

**Files:**

- Create: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md
- Create: scripts/lib/document_governance/__init__.py
- Create: scripts/lib/document_governance/taxonomy.py
- Create: tests/validation/test_document_taxonomy.py
- Modify: scripts/requirements.txt

**Interfaces:**

- Consumes: a profile mapping loaded by the caller.
- Produces: classify_path(path, profiles), validate_stable_identity(path,
  metadata, profiles), and find_dated_identity_parts(path).

- [ ] **Step 1: Create the stable execution Task evidence**

Create task.md from the Task template with artifact_id task-0136-01, parent
spec:136-sdlc-taxonomy-convergence, every Task heading in this Plan as its work
breakdown, and empty evidence tables rather than invented results. It moves
with the Spec directory in Task 5 and receives actual command and Commit
evidence after each Task.

- [ ] **Step 2: Write failing taxonomy tests**

~~~python
import unittest
from pathlib import PurePosixPath
from scripts.lib.document_governance.taxonomy import (
    find_dated_identity_parts,
    validate_stable_identity,
)

class StableDocumentTaxonomyTests(unittest.TestCase):
    def test_rejects_date_prefix_and_year_partition(self):
        self.assertEqual(
            ("2026", "2026-08-09-audit.md"),
            find_dated_identity_parts(PurePosixPath(
                "docs/90.references/research/2026/2026-08-09-audit.md"
            )),
        )

    def test_accepts_architecture_description_identity(self):
        findings = validate_stable_identity(
            PurePosixPath(
                "docs/02.architecture/descriptions/ad-0001-gateway.md"
            ),
            {
                "artifact_id": "ad-0001",
                "artifact_type": "architecture-description",
            },
            {
                "architecture-description": {
                    "id_pattern": r"ad-[0-9]{4}",
                }
            },
        )
        self.assertEqual([], findings)
~~~

- [ ] **Step 3: Run the focused tests and verify failure**

Run:

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py
~~~

Expected: collection fails because scripts.lib.document_governance does not
exist.

- [ ] **Step 4: Implement the dependency-free taxonomy functions**

taxonomy.py must use PurePosixPath and compiled regular expressions, return
stable finding objects, and perform no file writes. It must not hardcode the
complete repository profile table.

~~~python
@dataclass(frozen=True)
class TaxonomyFinding:
    code: str
    path: str
    message: str

def find_dated_identity_parts(path: PurePosixPath) -> tuple[str, ...]:
    return tuple(
        part for part in path.parts
        if re.fullmatch(r"[0-9]{4}", part)
        or re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-", part)
    )

def validate_stable_identity(
    path: PurePosixPath,
    metadata: Mapping[str, object],
    profiles: Mapping[str, Mapping[str, object]],
) -> list[TaxonomyFinding]:
    findings: list[TaxonomyFinding] = []
    artifact_type = str(metadata.get("artifact_type", ""))
    artifact_id = str(metadata.get("artifact_id", ""))
    profile = profiles.get(artifact_type)
    if profile is None:
        return [TaxonomyFinding("profile-missing", str(path), artifact_type)]
    id_pattern = str(profile["id_pattern"])
    if re.fullmatch(id_pattern, artifact_id) is None:
        findings.append(TaxonomyFinding(
            "artifact-id-invalid", str(path), artifact_id
        ))
    if not any(
        part == artifact_id or part.startswith(artifact_id + "-")
        for part in path.parts
    ):
        findings.append(TaxonomyFinding(
            "path-id-mismatch", str(path), artifact_id
        ))
    for part in find_dated_identity_parts(path):
        findings.append(TaxonomyFinding(
            "dated-path-identity", str(path), part
        ))
    return findings
~~~

- [ ] **Step 5: Run focused and existing metadata tests**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py
~~~

Expected: PASS.

- [ ] **Step 6: Commit**

~~~bash
git add docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md scripts/lib/document_governance scripts/requirements.txt tests/validation/test_document_taxonomy.py
git commit -m "feat(validation): add stable document taxonomy engine"
~~~

### Task 2: Establish Canonical Stage 00 and Stage 99 Contracts

**Files:**

- Modify: docs/99.templates/registry.json
- Modify: docs/00.agent-governance/policies/documentation-protocol.md
- Modify: docs/00.agent-governance/policies/stage-authoring-matrix.md
- Modify: docs/00.agent-governance/roles/docs.md
- Modify: docs/99.templates/support/document-metadata-profiles.yaml
- Modify: docs/99.templates/support/frontmatter-contract.md
- Modify: docs/99.templates/support/lifecycle-status.md
- Modify: docs/99.templates/support/sdlc-document-contract.md
- Modify: docs/99.templates/support/template-selection.md
- Modify: docs/99.templates/support/archive-retention-contract.md
- Modify: docs/99.templates/support/document-corpus-migration-contract.yaml
- Rename: docs/99.templates/templates/sdlc/ard.template.md to
  docs/99.templates/templates/sdlc/architecture-description.template.md
- Create: docs/99.templates/templates/sdlc/srs.template.md
- Create: docs/99.templates/templates/sdlc/interface-requirement.template.md
- Modify: docs/99.templates/templates/sdlc/prd.template.md
- Modify: docs/99.templates/templates/sdlc/adr.template.md
- Modify: docs/99.templates/templates/sdlc/spec.template.md
- Modify: docs/99.templates/templates/sdlc/plan.template.md
- Modify: docs/99.templates/templates/sdlc/task.template.md
- Modify: docs/99.templates/templates/operations/guide.template.md
- Modify: docs/99.templates/templates/operations/policy.template.md
- Modify: docs/99.templates/templates/operations/runbook.template.md
- Modify: docs/99.templates/templates/operations/incident.template.md
- Modify: docs/99.templates/templates/operations/postmortem.template.md
- Modify: docs/99.templates/templates/operations/release.template.md
- Modify: tests/validation/test_document_metadata.py
- Modify: tests/validation/test_agent_governance_contract.py

**Interfaces:**

- Consumes: taxonomy functions from Task 1.
- Produces: target profiles for PRD, SRS, Interface Requirement, Architecture
  Description, ADR, Spec, Plan, Task, Operations roles, Archive roles, and a
  bounded migration phase named sdlc-taxonomy-convergence.

- [ ] **Step 1: Add failing contract fixtures**

Add fixtures that accept ad-0001-*.md and reject ARD, accept stable operation
subjects, reject date prefixes, require created and updated after promotion,
and identify Rules Engineer as the Stage 00 policy owner.

- [ ] **Step 2: Run the focused contract tests**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_contract.py
~~~

Expected: FAIL on missing profiles and old authority.

- [ ] **Step 3: Apply template and contract changes**

Use git mv for the Architecture Description template. The migration contract
must enumerate the old source roots as bounded inputs and must not define a
permanent legacy profile. Operations conditional sections are represented as
conditional_headings, not required boilerplate.

- [ ] **Step 4: Check contract validity**

~~~bash
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-agent-governance-contract.py --mode contract
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_contract.py
~~~

Expected: all commands PASS. Corpus-wide promotion is not expected yet.

- [ ] **Step 5: Commit**

~~~bash
git add docs/00.agent-governance docs/99.templates tests/validation
git commit -m "governance: establish canonical SDLC document contracts"
~~~

### Task 3: Freeze the Migration Ledger and Script Manifest

**Files:**

- Create: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md
- Create: scripts/manifest.yaml
- Modify: scripts/README.md
- Create: tests/validation/test_script_manifest.py

**Interfaces:**

- Consumes: the target identities from Task 2 and git ls-files.
- Produces: an exhaustive old-to-new document path ledger and a 63-file script
  disposition inventory used by every later Task.

- [ ] **Step 1: Write a failing manifest completeness test**

~~~python
import subprocess
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

class ScriptManifestTests(unittest.TestCase):
    def test_every_tracked_script_has_one_manifest_record(self):
        tracked = set(subprocess.run(
            ["git", "ls-files", "scripts"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout.splitlines())
        manifest = yaml.safe_load(
            (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        declared = [row["path"] for row in manifest["files"]]
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(tracked, set(declared))
~~~

- [ ] **Step 2: Generate read-only inventories under /tmp**

~~~bash
git ls-files docs scripts > /tmp/sdlc-taxonomy-tracked-paths.txt
rg -n --glob '*.md' '\]\([^)]*docs/(01|02|03|04|05|90|98)\.' . > /tmp/sdlc-taxonomy-inbound-links.txt
git ls-files scripts | sort > /tmp/sdlc-taxonomy-script-paths.txt
~~~

Expected: 63 tracked script paths and a complete inbound-link evidence file.

- [ ] **Step 3: Author the exhaustive ledgers**

Every document row records legacy_path, stable_path, artifact_id, action,
replacement, source_commit, and reason. Every script row records path, kind,
authority, lifecycle, mutation, consumers, disposition, successor, and tests.
Use the mandatory dispositions in Context and Inputs. No row may use unknown,
later, undecided, legacy, deprecated, or dormant.

- [ ] **Step 4: Run completeness tests**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_script_manifest.py
python3 - <<'PY'
from pathlib import Path
text = Path("docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md").read_text()
for key in ("legacy_path", "stable_path", "artifact_id", "action",
            "replacement", "source_commit", "reason"):
    assert key in text, key
PY
~~~

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add docs/98.archive/migrations scripts/manifest.yaml scripts/README.md tests/validation/test_script_manifest.py
git commit -m "docs: freeze SDLC and script migration dispositions"
~~~

### Task 4: Migrate Requirements and Architecture

**Files:**

- Rename: docs/01.requirements/[0-9][0-9][0-9]-*.md to
  docs/01.requirements/prd-[0-9][0-9][0-9]-*.md
- Rename: the legacy Architecture Requirements rows recorded in `mig-0001` to
  docs/02.architecture/descriptions/ad-*.md
- Rename: docs/02.architecture/decisions/*.md to
  docs/02.architecture/decisions/adr-*.md
- Modify: all inbound paths enumerated for these rows in mig-0001
- Modify: docs/01.requirements/README.md
- Modify: docs/02.architecture/README.md
- Modify: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md

**Interfaces:**

- Consumes: exact path rows from Task 3.
- Produces: stable PRD, Architecture Description, and ADR paths and IDs.

- [ ] **Step 1: Add failing migration assertions**

Add tests to test_document_taxonomy.py that assert no tracked Stage 01 document
matches three-digits-without-prd and no Stage 02 requirements path exists.

- [ ] **Step 2: Verify the assertions fail**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py
~~~

Expected: FAIL against current paths.

- [ ] **Step 3: Apply exact git mv rows and frontmatter updates**

Use only mappings already committed in mig-0001. Change parent_ids and links in
the same edit. Architecture content is normalized to stakeholders, boundaries,
views, flows, quality scenarios, requirement disposition, and related ADRs
without inventing unimplemented architecture.

- [ ] **Step 4: Verify Stage 01 and 02**

~~~bash
test ! -d docs/02.architecture/requirements
test -d docs/02.architecture/descriptions
PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
bash scripts/validation/check-doc-implementation-alignment.sh
~~~

Expected: tests PASS and alignment findings do not increase.

- [ ] **Step 5: Commit**

~~~bash
git add docs/01.requirements docs/02.architecture docs/98.archive/migrations tests/validation
git commit -m "docs: migrate requirements and architecture identities"
~~~

### Task 5: Co-locate Spec, Plan, and Task and Remove Stage 04

**Files:**

- Rename: docs/03.specs/[0-9][0-9][0-9]-*/ to
  docs/03.specs/spec-0[0-9][0-9][0-9]-*/
- Rename: docs/04.execution/plans/2026-08-07-sdlc-taxonomy-convergence.md
  to docs/03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md
- Reclassify: docs/98.archive/03.specs/* according to mig-0001
- Rename active execution documents to owning Stage 03 plan.md and task.md
- Move completed execution pairs to docs/98.archive/changes/chg-*/
- Delete: capability child README.md files
- Delete after empty: docs/04.execution/
- Modify: docs/03.specs/README.md
- Modify: docs/98.archive/README.md
- Modify: all inbound links and mig-0001 rows
- Modify: tests/validation/test_document_corpus_lifecycle.py

**Interfaces:**

- Consumes: Requirement and Architecture IDs from Task 4 and the disposition
  rows from Task 3.
- Produces: one active capability directory per current Spec and complete
  change packets for completed Plan and Task evidence.

- [ ] **Step 1: Add failing co-location tests**

~~~python
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class CoLocatedExecutionTests(unittest.TestCase):
    def test_active_capability_has_no_child_readme(self):
        readmes = list((ROOT / "docs/03.specs").glob("spec-*/README.md"))
        self.assertEqual([], readmes)

    def test_stage_04_is_absent(self):
        self.assertFalse((ROOT / "docs/04.execution").exists())

    def test_active_change_is_at_most_one_pair(self):
        for capability in (ROOT / "docs/03.specs").glob("spec-*"):
            self.assertLessEqual(len(list(capability.glob("plan.md"))), 1)
            self.assertLessEqual(len(list(capability.glob("task.md"))), 1)
~~~

- [ ] **Step 2: Run lifecycle tests and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py
~~~

Expected: FAIL on Stage 04 and current directory shapes.

- [ ] **Step 3: Restore or tombstone the 32 archived Specs**

For each mig-0001 row, restore a current capability to Stage 03 or replace a
retired capability body with a concise provenance tombstone. Rewrite active
consumers to current Specs before touching the archive copy.

- [ ] **Step 4: Move execution evidence**

Active Plan and Task move to plan.md and task.md under their owning capability.
Completed pairs move together to one chg-ID directory. Orphans receive the
explicit owner or retirement disposition already recorded in mig-0001.

- [ ] **Step 5: Verify co-location and archive safety**

~~~bash
test ! -e docs/04.execution
PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted
bash scripts/validation/check-doc-implementation-alignment.sh
~~~

Expected: no Stage 04, no active-to-archive link, and all commands PASS for
promoted paths.

- [ ] **Step 6: Commit**

~~~bash
git add -A docs/03.specs docs/04.execution docs/98.archive tests/validation
git commit -m "docs: co-locate specifications and execution evidence"
~~~

### Task 6A: Reorganize Operations Domains 00 through 03

**Files:**

- Rename subjects from guides, policies, and runbooks under 00-workspace,
  01-gateway, 02-auth, and 03-security to their exact ops-ID paths in mig-0001
- Move the four domain README files to docs/05.operations/<domain>/README.md
- Create: tests/validation/test_operations_taxonomy.py
- Modify: all inbound links and mig-0001 rows for these four domains

**Interfaces:**

- Consumes: subject-to-ops-ID mappings from Task 3.
- Produces: domain-first subjects for domains 00 through 03.

- [ ] **Step 1: Write the failing bounded-domain test**

~~~python
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATED_DOMAINS = (
    "00-workspace", "01-gateway", "02-auth", "03-security",
)

class OperationsTaxonomyTests(unittest.TestCase):
    def test_migrated_domains_leave_no_role_root_copy(self):
        for role in ("guides", "policies", "runbooks"):
            for domain in MIGRATED_DOMAINS:
                self.assertFalse(
                    (ROOT / "docs/05.operations" / role / domain).exists()
                )
~~~

- [ ] **Step 2: Run the test and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
~~~

Expected: FAIL on 00-workspace under the parallel roots.

- [ ] **Step 3: Move each mapped subject as one role set**

For each mig-0001 subject, move all existing roles, normalize role artifact IDs
to the shared numeric ops ID, update inbound links, and then start the next
subject. Do not create a missing role.

- [ ] **Step 4: Verify migrated domains**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
~~~

Expected: PASS for migrated domains.

- [ ] **Step 5: Commit**

~~~bash
git add docs/05.operations docs/98.archive/migrations tests/validation
git commit -m "docs: migrate operations domains 00 through 03"
~~~

### Task 6B: Reorganize Operations Domains 04 through 06

**Files:**

- Rename subjects under 04-data, 05-messaging, and 06-observability to exact
  ops-ID paths in mig-0001
- Move the three domain README files
- Modify: tests/validation/test_operations_taxonomy.py
- Modify: all inbound links and mig-0001 rows for these domains

**Interfaces:**

- Consumes: Task 6A Operations catalog.
- Produces: domain-first subjects for domains 04 through 06.

- [ ] **Step 1: Expand the bounded-domain test**

~~~python
MIGRATED_DOMAINS = (
    "00-workspace", "01-gateway", "02-auth", "03-security",
    "04-data", "05-messaging", "06-observability",
)
~~~

- [ ] **Step 2: Run and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
~~~

Expected: FAIL on 04-data, 05-messaging, or 06-observability source paths.

- [ ] **Step 3: Move mapped role sets and verify**

For each 04 through 06 subject row, move every existing role to the declared
ops-ID directory, update role frontmatter and inbound links, and mark the
ledger row complete before verification.

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
~~~

Expected: PASS for migrated domains.

- [ ] **Step 4: Commit**

~~~bash
git add docs/05.operations docs/98.archive/migrations tests/validation
git commit -m "docs: migrate operations domains 04 through 06"
~~~

### Task 6C: Reorganize Operations Domains 07 through 09

**Files:**

- Rename subjects under 07-workflow, 08-ai, and 09-tooling to exact ops-ID
  paths in mig-0001
- Move the three domain README files
- Modify: tests/validation/test_operations_taxonomy.py
- Modify: all inbound links and mig-0001 rows for these domains

**Interfaces:**

- Consumes: Task 6B Operations catalog.
- Produces: domain-first subjects for domains 07 through 09.

- [ ] **Step 1: Expand the bounded-domain test**

~~~python
MIGRATED_DOMAINS = (
    "00-workspace", "01-gateway", "02-auth", "03-security",
    "04-data", "05-messaging", "06-observability",
    "07-workflow", "08-ai", "09-tooling",
)
~~~

- [ ] **Step 2: Run and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
~~~

Expected: FAIL on at least one 07 through 09 source path.

- [ ] **Step 3: Move mapped role sets and verify**

For each 07 through 09 subject row, move every existing role to the declared
ops-ID directory, update role frontmatter and inbound links, and mark the
ledger row complete before verification.

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
~~~

Expected: PASS for migrated domains.

- [ ] **Step 4: Commit**

~~~bash
git add docs/05.operations docs/98.archive/migrations tests/validation
git commit -m "docs: migrate operations domains 07 through 09"
~~~

### Task 6D: Complete Operations Domains 10 through 12

**Files:**

- Rename subjects under 10-communication, 11-laboratory, and 12-infra-net to
  exact ops-ID paths in mig-0001
- Move the three domain README files
- Delete after empty: docs/05.operations/guides
- Delete after empty: docs/05.operations/policies
- Delete after empty: docs/05.operations/runbooks
- Modify: docs/05.operations/README.md
- Modify: Operations templates and metadata fixtures
- Modify: tests/validation/test_operations_taxonomy.py
- Modify: all inbound links and mig-0001 rows for these domains

**Interfaces:**

- Consumes: Task 6C Operations catalog.
- Produces: the complete single domain-first Operations root.

- [ ] **Step 1: Add the final root and role-boundary tests**

~~~python
class FinalOperationsTaxonomyTests(unittest.TestCase):
    def test_operations_has_no_parallel_role_roots(self):
        for name in ("guides", "policies", "runbooks"):
            self.assertFalse((ROOT / "docs/05.operations" / name).exists())

    def test_prometheus_roles_share_one_subject(self):
        matches = list(
            (ROOT / "docs/05.operations/06-observability").glob(
                "ops-*-prometheus"
            )
        )
        self.assertEqual(1, len(matches))
        roles = {path.stem for path in matches[0].glob("*.md")}
        self.assertEqual({"guide", "policy", "runbook"}, roles)
~~~

- [ ] **Step 2: Run and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
~~~

Expected: FAIL while the remaining source domains and role roots exist.

- [ ] **Step 3: Move final role sets and remove empty roots**

Normalize Guide, Policy, and Runbook content to their sole responsibilities.
Guide Runbook Handoff and Runbook Automation Handoff remain conditional.

- [ ] **Step 4: Verify the complete Operations corpus**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
~~~

Expected: PASS with no parallel role root and no required missing role.

- [ ] **Step 5: Commit**

~~~bash
git add -A docs/05.operations docs/99.templates docs/98.archive/migrations tests/validation
git commit -m "docs: complete domain-first operations taxonomy"
~~~

### Task 7: Consolidate References and Archive on Stable IDs

**Files:**

- Rename: dated docs/90.references paths to ref-<id>-<slug>
- Rename: dated or mirrored docs/98.archive paths to chg-, mig-, or tombstone
  stable paths
- Move: root archive/Windows-Network-IP.md to its mig-0001 disposition
- Delete after empty: root archive/
- Modify: docs/90.references/README.md
- Modify: docs/98.archive/README.md
- Modify: docs/99.templates/support/archive-retention-contract.md
- Modify: all inbound links and mig-0001
- Modify: tests/validation/test_document_corpus_lifecycle.py

**Interfaces:**

- Consumes: stable IDs and archive roles from Tasks 2 and 3.
- Produces: the sole Stage 98 archive and a date-free Stage 90 and Stage 98.

- [ ] **Step 1: Add failing corpus-wide date-path and archive-root tests**

The test scans git ls-files docs and rejects a path component matching four
digits or a basename starting YYYY-MM-DD. README.md and role filenames inherit
their parent identity and remain valid.

- [ ] **Step 2: Run and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py
~~~

Expected: FAIL on current Stage 90, Stage 98, and root archive paths.

- [ ] **Step 3: Apply ledger moves and typed dates**

Move path dates into created, updated, observed_at, completed_at, released_at,
occurred_at, or archived_at according to artifact type. Preserve body timeline
timestamps. Complete archived_commit and archived_blob for every tombstone.

- [ ] **Step 4: Verify archive and dates**

~~~bash
test ! -e archive
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-archive
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted
PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py
~~~

Expected: PASS and no dated documentation identity.

- [ ] **Step 5: Commit**

~~~bash
git add -A docs/90.references docs/98.archive docs/99.templates archive tests/validation
git commit -m "docs: consolidate references and archive identities"
~~~

### Task 8: Reconcile Stage 00 Rules and Provider Projections

**Files:**

- Modify: docs/00.agent-governance/policies/bootstrap.md
- Modify: documentation-protocol.md, output-style.md, standards.md,
  agentic.md, workflows.md, task-checklists.md, postflight-checklist.md,
  persona.md, and stage-authoring-matrix.md
- Modify or delete: docs/00.agent-governance/scopes/backend.md, entry.md,
  frontend.md, meta.md, mobile.md, and product.md
- Modify: docs/00.agent-governance/providers/README.md
- Modify: docs/00.agent-governance/providers/claude.md
- Modify: docs/00.agent-governance/providers/codex.md
- Modify: docs/00.agent-governance/providers/README.md
- Modify: docs/00.agent-governance/providers/registry.yaml
- Modify: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md
- Modify generated provider surfaces owned by provider_surface_renderer.py
- Modify: tests/validation/test_agent_governance_contract.py
- Modify: tests/validation/test_provider_surface_renderer.py
- Modify: tests/validation/test_provider_native_surfaces.py

**Interfaces:**

- Consumes: final taxonomy and typed authority.
- Produces: one provider-neutral SDLC and generated provider adapters.

- [ ] **Step 1: Add failing ownership, language, scope, and provider tests**

Tests assert Rules Engineer policy ownership, role-specific language routing,
24 generated functions, no copied provider model version prose, and no
unconditional mobile or frontend workspace mandate.

- [ ] **Step 2: Run focused tests and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_contract.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_surface_renderer.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_native_surfaces.py
~~~

Expected: FAIL on current conflicts.

- [ ] **Step 3: Consolidate canonical rules and regenerate adapters**

Keep one load order in bootstrap, one workflow in workflows.md, one completion
contract in task-checklists.md, and pointers elsewhere. Generate provider
surfaces from typed contracts; do not hand-copy model versions.

- [ ] **Step 4: Verify governance**

~~~bash
python3 scripts/validation/check-agent-governance-contract.py --mode contract
bash scripts/operations/sync-provider-surfaces.sh --check
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_contract.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_surface_renderer.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_native_surfaces.py
~~~

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add docs/00.agent-governance .claude .codex .gemini tests/validation
git commit -m "governance: reconcile SDLC authority and provider projections"
~~~

### Task 9: Enforce the Script Manifest and Consolidate Generators

**Files:**

- Create: scripts/validation/check-script-manifest.py
- Create: scripts/knowledge/generate-llm-wiki.py
- Delete: scripts/knowledge/generate-llm-wiki-index.sh
- Delete: scripts/knowledge/generate-llm-wiki-coverage.sh
- Modify: scripts/manifest.yaml
- Modify: scripts/README.md
- Modify: .github/workflow-contract.yml
- Modify: tests/validation/test_script_manifest.py
- Create: tests/validation/test_generate_llm_wiki.py

**Interfaces:**

- Consumes: manifest records from Task 3.
- Produces: validate_manifest_document(document, tracked_paths),
  check_manifest(repo_root, manifest_path), check_generated(repo_root,
  manifest_path), the CLI mode --check-generated, and one LLM Wiki generator
  with --check and --write modes.

- [ ] **Step 1: Add failing consumer and mutation tests**

~~~python
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class LlmWikiGeneratorTests(unittest.TestCase):
    def test_generator_defaults_to_check(self):
        before = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout
        result = subprocess.run(
            ["python3", "scripts/knowledge/generate-llm-wiki.py"],
            cwd=ROOT,
            text=True,
            check=False,
            capture_output=True,
        )
        after = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, after)

class ScriptManifestValidationTests(unittest.TestCase):
    def test_manifest_rejects_unreferenced_executable(self):
        findings = validate_manifest_document({
            "files": [{
                "path": "scripts/example.sh",
                "kind": "validator",
                "authority": "script-manifest",
                "lifecycle": "maintained",
                "mutation": "none",
                "consumers": [],
                "disposition": "retain",
                "successor": None,
                "tests": [],
            }]
        }, {"scripts/example.sh"})
        self.assertIn("consumer-missing", {row.code for row in findings})
~~~

- [ ] **Step 2: Run focused tests and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_script_manifest.py
PYTHONPATH=. .venv/bin/python tests/validation/test_generate_llm_wiki.py
~~~

Expected: FAIL on missing CLIs.

- [ ] **Step 3: Implement the manifest gate and merged generator**

The merged generator owns both existing outputs and shares one tracked-file
selection and classification pass. The manifest CLI --check-generated invokes
each maintained generator's registered check command without writing. No
compatibility wrappers remain after all workflow and documentation consumers
move.

~~~python
def build_outputs(repo_root: Path) -> dict[Path, str]:
    candidates = collect_candidates(repo_root)
    return {
        INDEX_OUTPUT: render_index(candidates),
        COVERAGE_OUTPUT: render_coverage(candidates),
    }

def apply_mode(outputs: Mapping[Path, str], mode: str) -> int:
    if mode == "check":
        return check_outputs(outputs)
    if mode == "write":
        write_outputs(outputs)
        return 0
    raise ValueError(mode)
~~~

- [ ] **Step 4: Verify manifest and freshness**

~~~bash
python3 scripts/validation/check-script-manifest.py
python3 scripts/knowledge/generate-llm-wiki.py --check
PYTHONPATH=. .venv/bin/python tests/validation/test_script_manifest.py
PYTHONPATH=. .venv/bin/python tests/validation/test_generate_llm_wiki.py
~~~

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add scripts .github/workflow-contract.yml tests/validation
git commit -m "scripts: enforce manifest and unify LLM Wiki generation"
~~~

### Task 10: Consolidate Document Validators

**Files:**

- Create: scripts/lib/document_governance/frontmatter.py
- Create: scripts/lib/document_governance/git_provenance.py
- Create: scripts/lib/document_governance/links.py
- Create: scripts/validation/check-document-links.py
- Modify: scripts/validation/check-document-metadata.py
- Modify: scripts/validation/check-document-corpus-lifecycle.py
- Delete: scripts/validation/check-doc-traceability.sh
- Delete: scripts/validation/check-doc-implementation-alignment.sh
- Modify: scripts/manifest.yaml
- Modify: .github/workflow-contract.yml
- Modify: .pre-commit-config.yaml
- Modify: tests/validation/test_document_metadata.py
- Modify: tests/validation/test_document_corpus_lifecycle.py
- Create: tests/validation/test_document_links.py

**Interfaces:**

- Consumes: taxonomy engine and Stage 99 profiles.
- Produces: read_frontmatter(path), resolve_git_provenance(path, commit),
  build_document_graph(paths), and the CLI modes traceability and alignment.

**Resume checkpoint:** The shared modules, link CLI, and link tests already
exist in the worktree; both old Shell validators are deleted; focused link
tests and both modes passed before the design pause. Preserve that work. The
remaining known blockers are the manifest behavioral-evidence fixture for a
YAML `entry:` consumer and Ruff findings caused by the metadata import alias.

- [ ] **Step 1: Reconcile the existing Task 10 diff and rerun its focused RED/GREEN evidence**

Confirm that the existing fixtures cover anchors, fenced examples, relative
links, current-to-archive links, parent_ids, missing replacements, and
immutable created dates. Do not recreate the files or overwrite the existing
working implementation.

- [ ] **Step 2: Verify tests fail before extraction**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_links.py
~~~

Expected: FAIL because shared modules and new CLI do not exist.

- [ ] **Step 3: Finish the library extraction and manifest registration**

CLI behavior remains deterministic and non-mutating. Separate gate IDs call
the same CLI with explicit modes. Lifecycle must import the shared module, not
dynamically import the metadata CLI file.

~~~python
MODE_HANDLERS = {
    "traceability": check_traceability,
    "alignment": check_alignment,
}

def run_mode(mode: str, paths: Iterable[Path]) -> list[LinkFinding]:
    graph = build_document_graph(paths)
    try:
        handler = MODE_HANDLERS[mode]
    except KeyError as error:
        raise ValueError(f"unsupported link-check mode: {mode}") from error
    return handler(graph)
~~~

FrontmatterRecord, Provenance, DocumentGraph, and LinkFinding are frozen
dataclasses defined in their owning modules and compared directly in the
fixtures from Step 1.

Remove the unused `UniqueKeyLoader` import and expose
`read_frontmatter_values` under one canonical name rather than an unused import
alias. Extend the script-manifest semantic-evidence test so a registered YAML
`entry:` that names the exact CLI is accepted, while a prose/comment-only
basename remains rejected.

- [ ] **Step 4: Verify all document gates**

~~~bash
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-links.py --mode traceability
python3 scripts/validation/check-document-links.py --mode alignment
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_links.py
~~~

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add scripts .github/workflow-contract.yml .pre-commit-config.yaml tests/validation
git commit -m "scripts: consolidate document governance validators"
~~~

### Task 10A: Normalize Four-Digit IDs and Incident Year Routing

**Files:**

- Move: every `docs/01.requirements/prd-###-<slug>.md` to
  `docs/01.requirements/prd-####-<slug>.md`
- Modify: `docs/99.templates/support/document-metadata-profiles.yaml`
- Modify: `docs/99.templates/support/template-selection.md`
- Modify: Stage 00 authoring/function contracts and `docs/05.operations/incidents/README.md`
- Modify: affected current frontmatter IDs, internal requirement and acceptance
  IDs, parent/supersedes relations, links, `mig-0001`, and generated provider
  projections
- Test: `tests/validation/test_four_digit_document_identity.py`
- Modify: metadata, taxonomy, Operations, and repository-contract tests that
  enforce identity and Incident routing

**Interfaces:**

- Consumes: Task 10 shared parsing/path libraries and current Stage 99 profiles.
- Produces: one four-digit numeric identity width for document artifacts and
  internal requirement/acceptance identities.
- Produces Incident packet paths only as
  `docs/05.operations/incidents/<year>/inc-####-<slug>/` with fixed role files
  `incident.md` and `postmortem.md`.

- [ ] **Step 1: Repair the profile parser blocker with a focused RED fixture**

Add a test that loads `document-metadata-profiles.yaml` with `yaml.safe_load`
and asserts the exact Incident selector. Quote regex-like scalars inside YAML
flow lists so `[0-9]` is data rather than YAML syntax.

~~~python
def test_profiles_parse_and_publish_exact_incident_selector(self):
    document = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))
    selector = document["template_roles"]["incident"]["path_patterns"]
    self.assertIn(
        "docs/05.operations/incidents/[0-9][0-9][0-9][0-9]/"
        "inc-[0-9][0-9][0-9][0-9]-*/incident.md",
        selector,
    )
~~~

Run:

~~~bash
PYTHONPATH=. .venv/bin/python -m unittest \
  tests.validation.test_four_digit_document_identity.FourDigitDocumentIdentityTests.test_profiles_parse_and_publish_exact_incident_selector -v
~~~

Expected: FAIL before the quoting repair and PASS afterward.

- [ ] **Step 2: Add failing width, relation, and Incident-route tests**

Tests reject every tracked docs path with a three-digit typed ID, reject an
Incident packet without a four-digit year directory, accept the exact
year/`inc-####` form, reject `PRD-001-R001`, and accept
`PRD-0001-R0001`/`PRD-0001-AC0001`.

~~~python
def test_internal_requirement_ids_are_four_digits(self):
    self.assertFalse(is_valid_requirement_id("PRD-001-R001"))
    self.assertTrue(is_valid_requirement_id("PRD-0001-R0001"))
    self.assertTrue(is_valid_requirement_id("PRD-0001-AC0001"))

def test_incident_route_requires_year_and_four_digit_id(self):
    self.assertTrue(is_valid_incident_path(
        PurePosixPath(
            "docs/05.operations/incidents/2026/"
            "inc-0001-control-plane-outage/incident.md"
        )
    ))
    self.assertFalse(is_valid_incident_path(
        PurePosixPath(
            "docs/05.operations/incidents/inc-001-control-plane-outage/"
            "incident.md"
        )
    ))
~~~

- [ ] **Step 3: Finish native PRD moves and atomic identity migration**

Reconcile the already-started Git index before issuing any new move. Move all
25 current PRDs with Git exactly once, change artifact IDs to `prd-0001`
through `prd-0025`, normalize internal requirement/acceptance IDs, and update
every current identity relation and link in the same change. Immutable evidence
retains its recorded legacy source values; the migration ledger records the
corrected stable destinations.

- [ ] **Step 4: Converge Incident contracts**

Update the Stage 00 function owners, documentation protocol, Stage 05 Incident
index, Stage 99 profiles and selection contract, repository validator, and
generated provider projections. Uppercase `INC-###` and yearless `inc-*`
routes are rejected as active publication shapes.

- [ ] **Step 5: Verify metadata, taxonomy, links, providers, and diff hygiene**

~~~bash
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-contracts
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
PYTHONPATH=. .venv/bin/python tests/validation/test_four_digit_document_identity.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py
bash scripts/operations/sync-provider-surfaces.sh --check
git diff --check
~~~

- [ ] **Step 6: Commit**

~~~bash
git add docs scripts tests .agents .claude .gemini
git commit -m "docs: normalize four-digit identities and incident routing"
~~~

### Task 10B: Freeze the Operations Catalog Manifest and Validator

**Files:**

- Create: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
- Create: `scripts/lib/document_governance/operations_catalog.py`
- Create: `scripts/validation/check-operations-catalog.py`
- Create: `tests/validation/test_operations_catalog.py`
- Modify: `docs/99.templates/support/document-metadata-profiles.yaml`
- Modify: `docs/99.templates/support/template-selection.md`
- Modify: `docs/99.templates/support/corpus-migration-contract.md`
- Modify: `docs/00.agent-governance/policies/stage-authoring-matrix.md`
- Modify: `scripts/manifest.yaml`
- Modify: `.github/workflow-contract.yml`
- Modify: `.pre-commit-config.yaml`

**Interfaces:**

- Consumes: Task 10 shared frontmatter/Git/path helpers and the 77 current
  subject directories containing 66 Guides, 64 Policies, and 62 Runbooks.
- Produces: frozen `OperationSubjectRecord` and `OperationFileRecord`
  dataclasses, `load_operations_catalog_manifest(path)`,
  `validate_operations_catalog_manifest(root, manifest)`, and
  `find_operations_merge_candidates(subjects)`.
- Produces CLI modes `manifest`, `structure`, `executed`, and `complete`;
  `executed` accepts an explicit comma-separated `--domains` slice and every
  other mode rejects `--domains`.
- Produces: a user-approved manifest with separate structural and semantic
  dispositions. Later Tasks may execute only its exact records.

- [ ] **Step 1: Write failing manifest topology and fail-closed tests**

~~~python
class OperationsCatalogManifestTests(unittest.TestCase):
    def test_manifest_covers_exact_current_inventory(self):
        manifest = load_operations_catalog_manifest(MANIFEST)
        self.assertEqual(77, len(manifest.subjects))
        self.assertEqual(
            {"guide": 66, "policy": 64, "runbook": 62,
             "domain-readme": 13},
            Counter(row.role for row in manifest.files),
        )

    def test_similarity_cannot_authorize_merge(self):
        row = valid_subject_record(
            semantic_action="merge", merge_into="ops-0050"
        )
        row = replace(row, owner_match=False)
        findings = validate_subject_disposition(row)
        self.assertIn("merge-owner-boundary-unproven", finding_codes(findings))
~~~

Run:

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py -v
~~~

Expected: FAIL because the manifest, library, and CLI do not exist.

- [ ] **Step 2: Implement the typed manifest model and parser**

~~~python
@dataclass(frozen=True)
class OperationSubjectRecord:
    legacy_subject_path: PurePosixPath
    source_commit: str
    source_tree: str
    current_ops_id: str
    catalog_domain: str
    catalog_path: PurePosixPath
    canonical_ops_id: str
    canonical_slug: str
    final_path: PurePosixPath
    semantic_action: Literal["retain", "rename", "merge", "delete"]
    merge_into: str | None
    owner_match: bool
    control_boundary_match: bool
    trigger_and_recovery_match: bool
    independent_evidence_boundary: bool
    reason: str

@dataclass(frozen=True)
class OperationFileRecord:
    legacy_path: PurePosixPath
    source_commit: str
    source_blob: str
    role: Literal["guide", "policy", "runbook", "domain-readme"]
    catalog_path: PurePosixPath
    final_path: PurePosixPath | None
    semantic_action: Literal["retain", "rewrite", "merge", "delete"]
    canonical_role_owner: PurePosixPath | None
    preserved_semantics: tuple[str, ...]
    removed_semantics: tuple[str, ...]
    active_consumers: tuple[PurePosixPath, ...]
~~~

Reject unknown keys, unsafe paths, missing Git objects, non-blob sources,
duplicate source/target/ID ownership, self-merges, merge cycles, and merge rows
that do not prove all four Spec criteria.

- [ ] **Step 3: Audit all subjects and write the frozen manifest**

For each of the 77 subjects, read every current role body, frontmatter,
incoming link, script/automation consumer, review date, trigger, validation,
recovery, and owner. Record exact source commit/tree and per-file blob IDs.
Name the final subject by managed object or independent operational capability;
reject role words, dates, versions, states, repeated tokens, redundant domain
names, and unsupported `basics`/`setup` suffixes.

Build the machine block from the verified repository state; do not hand-enter
or abbreviate the baseline commit:

~~~python
baseline_commit = subprocess.run(
    ["git", "rev-parse", "HEAD"],
    cwd=root,
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
document = {
    "schema_version": 1,
    "migration_id": "mig-0002",
    "baseline_commit": baseline_commit,
    "subjects": subject_rows,
    "files": file_rows,
    "approval": {
        "status": "pending",
        "approved_at": None,
        "approved_by": None,
    },
}
~~~

The parser requires all displayed keys. `pending` is a typed lifecycle state
with defined transition semantics; no later Task may execute while it remains
pending.

- [ ] **Step 4: Obtain user approval for the exact subject map**

Present a table containing each current `ops-####`, proposed domain/path,
semantic action, canonical owner, roles retained/deleted, and reason. After
explicit approval, set `approval.status: approved`, record the approval date
and `user`, and rerun the manifest validator. Do not move or delete a corpus
file in this Task.

- [ ] **Step 5: Register and verify the focused validator**

~~~bash
.venv/bin/python scripts/validation/check-operations-catalog.py --mode manifest
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
.venv/bin/python scripts/validation/check-script-manifest.py
.venv/bin/python scripts/validation/check-github-workflow-contract.py
git diff --check
~~~

Expected: PASS with 77 subjects, 205 current files, no unproved merge, and an
approved manifest.

- [ ] **Step 6: Independent review and commit**

~~~bash
git add docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md \
  docs/99.templates/support docs/00.agent-governance/policies/stage-authoring-matrix.md \
  scripts/lib/document_governance/operations_catalog.py \
  scripts/validation/check-operations-catalog.py scripts/manifest.yaml \
  .github/workflow-contract.yml .pre-commit-config.yaml \
  tests/validation/test_operations_catalog.py
git commit -m "docs: register operations catalog migration"
~~~

### Task 10C: Move Operations Domains Under Catalog

**Files:**

- Create: `docs/05.operations/catalog/README.md`
- Move: `docs/05.operations/00-workspace/` through
  `docs/05.operations/12-infra-net/` under `docs/05.operations/catalog/`
- Modify: `docs/05.operations/README.md`
- Modify: every active path consumer and generator owner selected by the
  approved `mig-0002` structural map
- Modify: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
- Modify: `tests/validation/test_operations_catalog.py`
- Modify: path-aware tests that consume current Operations paths

**Interfaces:**

- Consumes: approved Task 10B `catalog_path` values.
- Produces: all 13 domain roots and the same 77 subject names under `catalog/`;
  subject bodies and semantic dispositions remain unchanged.

- [ ] **Step 1: Add the structural RED tests**

~~~python
def test_all_domains_are_under_catalog(self):
    self.assertEqual(
        EXPECTED_DOMAINS,
        {path.name for path in (ROOT / "docs/05.operations/catalog").iterdir()
         if path.is_dir()},
    )
    for domain in EXPECTED_DOMAINS:
        self.assertFalse((ROOT / "docs/05.operations" / domain).exists())

def test_event_roots_are_not_catalog_domains(self):
    self.assertFalse((ROOT / "docs/05.operations/catalog/incidents").exists())
    self.assertFalse((ROOT / "docs/05.operations/catalog/releases").exists())
~~~

Run the two tests and verify they fail because `catalog/` is absent.

- [ ] **Step 2: Execute only the approved structural Git moves**

Create `docs/05.operations/catalog/`, then run native `git mv` once for each
exact domain root in numeric order. Do not rename a subject, move role content,
or remove a role file in this Task.

~~~bash
mkdir -p docs/05.operations/catalog
git mv -- docs/05.operations/00-workspace docs/05.operations/catalog/00-workspace
git mv -- docs/05.operations/01-gateway docs/05.operations/catalog/01-gateway
git mv -- docs/05.operations/02-auth docs/05.operations/catalog/02-auth
git mv -- docs/05.operations/03-security docs/05.operations/catalog/03-security
git mv -- docs/05.operations/04-data docs/05.operations/catalog/04-data
git mv -- docs/05.operations/05-messaging docs/05.operations/catalog/05-messaging
git mv -- docs/05.operations/06-observability docs/05.operations/catalog/06-observability
git mv -- docs/05.operations/07-workflow docs/05.operations/catalog/07-workflow
git mv -- docs/05.operations/08-ai docs/05.operations/catalog/08-ai
git mv -- docs/05.operations/09-tooling docs/05.operations/catalog/09-tooling
git mv -- docs/05.operations/10-communication docs/05.operations/catalog/10-communication
git mv -- docs/05.operations/11-laboratory docs/05.operations/catalog/11-laboratory
git mv -- docs/05.operations/12-infra-net docs/05.operations/catalog/12-infra-net
~~~

- [ ] **Step 3: Migrate current consumers and indexes atomically**

Update active Markdown destinations, typed selectors, script/test constants,
CODEOWNERS/workflow path selectors, and generated-source owners from each exact
legacy domain prefix to its catalog prefix. Do not rewrite immutable
`archived_from`, source paths, commit-pinned manifests, or historical ledger
values. Create the catalog README as a domain navigation index and reduce the
root README to catalog/incidents/releases routing.

- [ ] **Step 4: Verify structural equivalence**

~~~bash
.venv/bin/python scripts/validation/check-operations-catalog.py --mode structure
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
git diff --check
~~~

Expected: 13 catalog domains, 77 unchanged subject IDs/names, 192 unchanged
role files, zero current old-prefix consumers, and zero link failures.

- [ ] **Step 5: Independent review and commit**

~~~bash
git add -A docs/05.operations docs/98.archive/migrations \
  docs/00.agent-governance docs/99.templates scripts tests .github
git commit -m "docs: move operations domains under catalog"
~~~

### Task 10D: Converge Operations Subjects in Domains 00 Through 03

**Files:**

- Modify/move/delete only approved records below
  `docs/05.operations/catalog/{00-workspace,01-gateway,02-auth,03-security}/`
- Modify: active consumers named by those manifest records
- Modify: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
- Modify: `tests/validation/test_operations_catalog.py`

**Interfaces:**

- Consumes: approved Task 10B semantic rows for domains 00–03.
- Produces: canonical subject names and role files for those four domains with
  every predecessor absent and every unique valid semantic preserved.

- [ ] **Step 1: Add an execution RED test for the exact domain slice**

~~~python
def test_domains_00_03_match_approved_semantic_targets(self):
    records = manifest.subjects_for_domains(
        {"00-workspace", "01-gateway", "02-auth", "03-security"}
    )
    findings = validate_executed_subject_records(ROOT, records)
    self.assertEqual([], findings)
~~~

Run this method and verify it fails on every approved rename/merge/delete that
has not executed.

- [ ] **Step 2: Execute approved subject renames and mergers**

Use native `git mv` for each `rename`. For a `merge`, first move each
`preserved_semantics` item into its declared canonical Guide/Policy/Runbook,
update active consumers, and run the per-row preservation assertion. Use
`git rm` only for the exact predecessor role files after that assertion passes.
Do not create missing Guide, Policy, or Runbook roles unless the approved row
identifies unique source semantics for that role.

- [ ] **Step 3: Normalize role bodies and domain indexes**

Keep Guide limited to concepts/normal use/non-destructive checks, Policy to
controls/exceptions/review, and Runbook to executable trigger-through-recovery
steps. Remove duplicate headings and template residue listed in the manifest.
Update the four domain READMEs to list only final canonical subjects.

- [ ] **Step 4: Verify, review, and commit the slice**

~~~bash
.venv/bin/python scripts/validation/check-operations-catalog.py --mode executed --domains 00-workspace,01-gateway,02-auth,03-security
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
git diff --check
git add -A docs/05.operations/catalog/00-workspace \
  docs/05.operations/catalog/01-gateway docs/05.operations/catalog/02-auth \
  docs/05.operations/catalog/03-security docs/98.archive/migrations \
  scripts tests
git commit -m "docs: converge operations catalog domains 00 through 03"
~~~

### Task 10E: Converge Operations Subjects in Domains 04 Through 06

**Files:**

- Modify/move/delete only approved records below
  `docs/05.operations/catalog/{04-data,05-messaging,06-observability}/`
- Modify: active consumers named by those manifest records
- Modify: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
- Modify: `tests/validation/test_operations_catalog.py`

**Interfaces:**

- Consumes: approved Task 10B semantic rows for domains 04–06.
- Produces: canonical data, messaging, and observability subjects without
  repeated category tokens or role words and with role semantics preserved.

- [ ] **Step 1: Add and run the domain-slice RED test**

~~~python
def test_domains_04_06_match_approved_semantic_targets(self):
    records = manifest.subjects_for_domains(
        {"04-data", "05-messaging", "06-observability"}
    )
    self.assertEqual([], validate_executed_subject_records(ROOT, records))
~~~

Expected: FAIL on every unexecuted approved row, including any reviewed
replacement for repeated tokens such as `backup-backup` or
`optimization-optimization`.

- [ ] **Step 2: Execute only approved renames and mergers**

Use native `git mv` for each approved rename. For a merge, copy no complete
body: move only manifest-listed unique paragraphs or steps into their declared
role owner, update current consumers, prove the canonical target contains each
preservation token, then use `git rm` on the exact predecessor. Preserve Git
source commit/blob values in `mig-0002`.

- [ ] **Step 3: Enforce role boundaries and domain ownership**

Keep service-specific operations with their managed service. Keep an
independent backup, retention, logical-upgrade, or storage-exhaustion subject
only when the approved row proves a separate trigger, control owner,
verification/recovery boundary, or review cadence. Update all three domain
READMEs to final subjects only.

- [ ] **Step 4: Run scoped and shared gates**

~~~bash
.venv/bin/python scripts/validation/check-operations-catalog.py --mode executed --domains 04-data,05-messaging,06-observability
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
git diff --check
~~~

- [ ] **Step 5: Independent review and commit**

~~~bash
git add -A docs/05.operations/catalog/04-data \
  docs/05.operations/catalog/05-messaging \
  docs/05.operations/catalog/06-observability \
  docs/98.archive/migrations scripts tests
git commit -m "docs: converge operations catalog domains 04 through 06"
~~~

### Task 10F: Converge Operations Subjects in Domains 07 Through 09

**Files:**

- Modify/move/delete only approved records below
  `docs/05.operations/catalog/{07-workflow,08-ai,09-tooling}/`
- Modify: active consumers named by those manifest records
- Modify: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
- Modify: `tests/validation/test_operations_catalog.py`

**Interfaces:**

- Consumes: approved Task 10B semantic rows for domains 07–09.
- Produces: canonical workflow, AI, and tooling subjects with service and
  independent-capability boundaries proven by the manifest.

- [ ] **Step 1: Add and run the domain-slice RED test**

~~~python
def test_domains_07_09_match_approved_semantic_targets(self):
    records = manifest.subjects_for_domains(
        {"07-workflow", "08-ai", "09-tooling"}
    )
    self.assertEqual([], validate_executed_subject_records(ROOT, records))
~~~

Expected: FAIL on every unexecuted row. The test must report Airflow/DAG,
optimization, and IaC naming decisions by exact `ops-####`, not by fuzzy name.

- [ ] **Step 2: Execute approved subject dispositions**

Use native `git mv` for renames. Merge `airflow-dag-basics` or
`dag-deployment` into Airflow only if their approved rows prove no independent
owner, trigger, evidence, or cadence. Keep GPU recovery, performance testing,
Terraform, or Terrakube separate only when their manifest rows prove an
independent operational boundary. Move unique semantics to their declared role
owners before exact `git rm`.

- [ ] **Step 3: Repair current automation and script consumers**

Update Runbook consumers, script manifest authorities, generator inputs,
workflow selectors, infrastructure navigation, and current docs to final
paths. Preserve immutable Stage 90/98 path evidence. Update the three domain
READMEs to final subjects only.

- [ ] **Step 4: Run scoped and shared gates**

~~~bash
.venv/bin/python scripts/validation/check-operations-catalog.py --mode executed --domains 07-workflow,08-ai,09-tooling
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
.venv/bin/python scripts/validation/check-script-manifest.py
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
git diff --check
~~~

- [ ] **Step 5: Independent review and commit**

~~~bash
git add -A docs/05.operations/catalog/07-workflow \
  docs/05.operations/catalog/08-ai docs/05.operations/catalog/09-tooling \
  docs/98.archive/migrations scripts tests infra .github
git commit -m "docs: converge operations catalog domains 07 through 09"
~~~

### Task 10G: Converge Operations Subjects in Domains 10 Through 12

**Files:**

- Modify/move/delete only approved records below
  `docs/05.operations/catalog/{10-communication,11-laboratory,12-infra-net}/`
- Modify: active consumers named by those manifest records
- Modify: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
- Modify: `tests/validation/test_operations_catalog.py`

**Interfaces:**

- Consumes: approved Task 10B semantic rows for domains 10–12.
- Produces: canonical communication, laboratory, and infrastructure-network
  subjects with no generic optimization bucket lacking an independent owner.

- [ ] **Step 1: Add and run the domain-slice RED test**

~~~python
def test_domains_10_12_match_approved_semantic_targets(self):
    records = manifest.subjects_for_domains(
        {"10-communication", "11-laboratory", "12-infra-net"}
    )
    self.assertEqual([], validate_executed_subject_records(ROOT, records))
~~~

Expected: FAIL for every approved rename, merge, or role deletion that has not
executed.

- [ ] **Step 2: Execute approved subject and role dispositions**

Use native `git mv` for exact renames. Keep each laboratory service subject
only when it owns distinct controls or procedures. Merge a generic hardening
subject into service Policies/Runbooks only when the manifest identifies every
target role and preservation token. Keep `standardize-infra-net` only if the
approved name remains a managed operational capability; otherwise execute its
approved canonical rename.

- [ ] **Step 3: Repair consumers and domain indexes**

Update infrastructure READMEs, script/Runbook authorities, current links, and
the three domain indexes. No current path may point to a predecessor; immutable
provenance retains its source path and blob.

- [ ] **Step 4: Run scoped and shared gates**

~~~bash
.venv/bin/python scripts/validation/check-operations-catalog.py --mode executed --domains 10-communication,11-laboratory,12-infra-net
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
git diff --check
~~~

- [ ] **Step 5: Independent review and commit**

~~~bash
git add -A docs/05.operations/catalog/10-communication \
  docs/05.operations/catalog/11-laboratory \
  docs/05.operations/catalog/12-infra-net \
  docs/98.archive/migrations scripts tests infra
git commit -m "docs: converge operations catalog domains 10 through 12"
~~~

### Task 10H: Align Operations Indexes, Incidents, Releases, and Templates

**Files:**

- Modify: `docs/05.operations/README.md`
- Modify: `docs/05.operations/catalog/README.md`
- Modify: every `docs/05.operations/catalog/<domain>/README.md`
- Modify: `docs/05.operations/incidents/README.md`
- Modify: `docs/05.operations/releases/README.md`
- Modify: `docs/99.templates/templates/operations/incident.template.md`
- Modify: `docs/99.templates/templates/operations/postmortem.template.md`
- Modify: `docs/99.templates/templates/operations/release.template.md`
- Modify: `docs/99.templates/support/document-metadata-profiles.yaml`
- Modify: `docs/99.templates/support/template-selection.md`
- Modify: Stage 00 Operations function and authoring contracts
- Modify: `docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md`
- Modify: `tests/validation/test_operations_catalog.py`
- Modify: `tests/validation/test_document_metadata.py`

**Interfaces:**

- Consumes: final catalog paths and roles from Tasks 10C–10G.
- Produces: the sole permitted Operations indexes, exact Incident/Release
  routes, conditional sibling sections, and completed `mig-0002` evidence.

- [ ] **Step 1: Add final topology and template RED tests**

~~~python
def test_operations_root_has_only_catalog_and_event_roots(self):
    directories = {
        path.name for path in (ROOT / "docs/05.operations").iterdir()
        if path.is_dir()
    }
    self.assertEqual({"catalog", "incidents", "releases"}, directories)

def test_incident_template_uses_typed_catalog_relations(self):
    body = INCIDENT_TEMPLATE.read_text(encoding="utf-8")
    self.assertIn("affected_ops_ids", body)
    self.assertNotIn("docs/05.operations/<domain>", body)
~~~

Also assert that only the Stage 05, catalog, domain, incidents, and releases
READMEs exist; no subject README is permitted.

- [ ] **Step 2: Rewrite indexes from final current inventory**

Generate no invented subjects. The root README routes to catalog, incidents,
and releases; the catalog README routes to 13 domains; each domain README lists
only its current `ops-####` subjects and retained roles. Remove predecessor
labels and links while preserving immutable migration provenance.

- [ ] **Step 3: Align Incident, Postmortem, and Release contracts**

Require `docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md`, an
optional sibling `postmortem.md`, and
`docs/05.operations/releases/rel-####-<slug>/release.md`. Incident templates
carry typed `affected_ops_ids`; Postmortem remains a strict Incident child;
Release remains executed-event evidence. Conditional Runbook/Postmortem/
automation handoffs render only when their real target exists.

- [ ] **Step 4: Complete Operations verification**

~~~bash
.venv/bin/python scripts/validation/check-operations-catalog.py --mode complete
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-contracts
.venv/bin/python scripts/validation/check-document-links.py --mode traceability
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_taxonomy.py
git diff --check
~~~

Expected: 13 domains under catalog, no other domain root, no subject README,
no unexecuted `mig-0002` row, zero stale consumers, and zero link failures.

- [ ] **Step 5: Independent review and commit**

~~~bash
git add docs/05.operations docs/00.agent-governance docs/99.templates \
  docs/98.archive/migrations scripts tests
git commit -m "docs: align operations events indexes and templates"
~~~

### Task 11: Decompose the Repository Policy Monolith and Remove One-Time Tools

**Files:**

- Create: scripts/validation/check-repository-invariants.py
- Modify: scripts/validation/ci_gate_adapters.py
- Modify: scripts/validation/run-ci-gate.py
- Modify: scripts/operations/provider_surface_renderer.py
- Modify: canonical Graphify hook generation owner identified in manifest
- Delete: scripts/validation/check-repo-contracts.sh
- Delete: scripts/validation/recommend-qa-gates.sh
- Delete: scripts/validation/recommend-gap-routing.sh
- Delete: scripts/validation/report-provider-hook-parity.sh
- Delete: scripts/hooks/patch-graphify-post-commit.sh
- Rewrite: scripts/hooks/post-tool-validate.sh
- Modify or delete: every other merge/delete row in scripts/manifest.yaml
- Modify: scripts/manifest.yaml, scripts/README.md, .pre-commit-config.yaml,
  .github/workflow-contract.yml, and active documentation consumers
- Create: tests/validation/test_repository_invariants.py
- Modify: tests/validation/test_ci_gate_adapters.py
- Modify: tests/validation/test_provider_surface_renderer.py

**Interfaces:**

- Consumes: specialized validators and exact dispositions in scripts/manifest.
- Produces: a residual invariant CLI with --mode repository and
  --mode stale-paths, run-ci-gate.py --recommend, provider parity report mode,
  and canonical Graphify hook generation.

- [ ] **Step 1: Add tests for every successor behavior**

Tests prove typed template and metadata rules are absent from the residual CLI,
recommendation uses workflow-contract gate IDs, provider parity uses typed
provider contracts, and post-tool validation cannot write.

- [ ] **Step 2: Run tests and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_repository_invariants.py
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_adapters.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_surface_renderer.py
~~~

Expected: FAIL on missing successor functions.

- [ ] **Step 3: Move residual behavior and delete predecessors**

For each manifest merge/delete row, first migrate code, tests, workflow nodes,
hooks, Runbooks, and documentation consumers. Then delete the old file and
remove its live manifest record. Record the deletion in mig-0001.

~~~python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("repository", "stale-paths"),
        default="repository",
    )
    return parser

def recommend(paths: Sequence[str], contract: GateContract) -> list[str]:
    return sorted(contract.required_gates_for_paths(paths))
~~~

- [ ] **Step 4: Prove no active reference remains**

~~~bash
python3 scripts/validation/check-script-manifest.py
rg -n 'check-repo-contracts|recommend-qa-gates|recommend-gap-routing|report-provider-hook-parity|patch-graphify-post-commit' .github .pre-commit-config.yaml scripts docs/00.agent-governance docs/05.operations
~~~

Expected: rg returns no active reference; migration history references under
Stage 98 are excluded.

- [ ] **Step 5: Run focused tests and commit**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_repository_invariants.py
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_adapters.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_surface_renderer.py
git add scripts .github .pre-commit-config.yaml docs tests/validation
git commit -m "scripts: remove duplicate and one-time policy tooling"
~~~

### Task 12: Align CI, Local, and Hook Gates

**Files:**

- Modify: .github/workflow-contract.yml
- Modify: .github/workflows/ci-quality.yml
- Delete or reduce to schedule-only reporting:
  .github/workflows/document-corpus-lifecycle.yml
- Modify: scripts/validation/ci_gate_contract.py
- Modify: scripts/validation/ci_gate_runner.py
- Modify: scripts/validation/ci_gate_adapters.py
- Modify: scripts/validation/run-local-qa-gates.sh
- Modify: scripts/validation/run-ci-precommit.sh
- Modify: .pre-commit-config.yaml
- Modify: tests/validation/test_ci_gate_contract.py
- Modify: tests/validation/test_ci_gate_runner.py
- Modify: tests/validation/test_agent_governance_ci_routing.py
- Modify: tests/validation/test_github_workflow_contract.py
- Modify: tests/validation/test_operations_catalog.py

**Interfaces:**

- Consumes: all canonical leaf validators.
- Produces: ci.document-governance and local.document-governance aggregates
  with identical leaves and explicit base SHA inputs.

- [ ] **Step 1: Add failing gate parity and base-range tests**

~~~python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class DocumentGovernanceGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text()
        )
        cls.nodes = {
            row["gate_id"]: row for row in document["gate_nodes"]
        }

    def test_local_and_ci_document_governance_share_leaves(self):
        self.assertEqual(
            self.nodes["ci.document-governance"]["children"],
            self.nodes["local.document-governance"]["children"],
        )

    def test_impacted_gate_requires_explicit_base(self):
        gate = self.nodes["leaf.document-lifecycle-impacted"]
        command = " ".join([gate["entrypoint"], *gate["argv"]])
        self.assertIn("--base-ref", command)
        self.assertNotIn("HEAD~1", command)
~~~

- [ ] **Step 2: Run gate contract tests and verify failure**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_contract.py
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_runner.py
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_ci_routing.py
PYTHONPATH=. .venv/bin/python tests/validation/test_github_workflow_contract.py
~~~

Expected: FAIL on current parity and lifecycle workflow routing.

- [ ] **Step 3: Register required aggregates**

The PR aggregate includes document contract, metadata, stable paths, lifecycle,
archive, links, traceability, Operations catalog integrity, templates,
governance, provider freshness, generated freshness, and script manifest. Pull
Request uses base SHA; push uses before SHA. Scheduled reporting reuses the
same leaves.

- [ ] **Step 4: Verify typed execution**

~~~bash
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-script-backed --list
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_contract.py
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_runner.py
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_ci_routing.py
PYTHONPATH=. .venv/bin/python tests/validation/test_github_workflow_contract.py
PYTHONPATH=. .venv/bin/python tests/validation/test_operations_catalog.py
~~~

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add .github .pre-commit-config.yaml scripts/validation tests/validation
git commit -m "ci: align local and remote document governance gates"
~~~

### Task 13: Repair Cross-Links, Indexes, Memory, and Generated Evidence

**Files:**

- Modify: docs/README.md and stage README files
- Modify: docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md
- Modify: active Markdown links reported by check-document-links.py
- Modify: scripts/README.md
- Modify: .github/INDEX.md and CODEOWNERS when paths changed
- Regenerate: every output registered in scripts/manifest.yaml
- Modify: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md
- Modify: docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md
- Modify: tests that assert old canonical paths

**Interfaces:**

- Consumes: final path graph and generator ownership.
- Produces: complete navigation, current memory, generated evidence, and no
  stale canonical reference.

- [ ] **Step 1: Capture failing link and freshness output**

~~~bash
python3 scripts/validation/check-document-links.py --mode alignment
python3 scripts/validation/check-script-manifest.py --check-generated
~~~

Expected: any remaining stale link or output is listed by exact owner.

- [ ] **Step 2: Repair only reported owners**

Update canonical links and indexes. Run registered generators with explicit
--write once, then immediately rerun --check. Do not hand-edit generated files.

- [ ] **Step 3: Prove old path literals are gone**

~~~bash
python3 scripts/validation/check-repository-invariants.py --mode stale-paths
~~~

Expected: no active canonical use. Historical prose is allowed only in
mig-0001 and tombstone provenance.

- [ ] **Step 4: Verify links and freshness**

~~~bash
python3 scripts/validation/check-document-links.py --mode traceability
python3 scripts/validation/check-document-links.py --mode alignment
python3 scripts/validation/check-script-manifest.py --check-generated
git diff --check
~~~

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add docs scripts .github tests
git commit -m "docs: repair navigation memory and generated evidence"
~~~

### Task 14: Remove Transition Contracts and Complete Regression Verification

**Files:**

- Modify: docs/99.templates/support/document-corpus-migration-contract.yaml
- Modify: docs/99.templates/support/corpus-migration-contract.md
- Modify: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md
- Modify: docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md
- Modify: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md
- Modify: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md
- Modify: docs/00.agent-governance/providers/registry.yaml only if the
  final typed audit finds a duplicate or consumerless active role
- Modify: tests/validation/test_agent_governance_contract.py
- Modify: scripts/manifest.yaml
- Modify: tests/validation affected by transition removal

**Interfaces:**

- Consumes: completed corpus and all required gates.
- Produces: zero transition allowances, completed migration evidence, and a
  durable Spec with Plan and Task archived as chg-0001.

- [ ] **Step 1: Add a failing no-transition assertion**

~~~python
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

class CompletedMigrationContractTests(unittest.TestCase):
    def test_taxonomy_migration_has_no_live_transition(self):
        contract = yaml.safe_load(
            (ROOT / "docs/99.templates/support/"
             "document-corpus-migration-contract.yaml").read_text()
        )
        names = {
            row["migration_id"]
            for row in contract.get("live_transitions", [])
        }
        self.assertNotIn("sdlc-taxonomy-convergence", names)
~~~

- [ ] **Step 2: Remove bounded migration allowances**

Mark every mig-0001 row complete, remove old-root allowances, and make the
target profiles the only accepted paths. Do not remove the historical ledger.

- [ ] **Step 3: Revalidate the per-agent governance outcome**

Load every active `agent-catalog.yaml` agent and function and prove stable
identity, one primary responsibility, bounded scope, typed inputs/process/
outputs, gates, mutation authority, escalation, consumer, and provider
projection. Assert that every function has exactly one owner and every active
agent has at least one current consumer/projection. The current reviewed
outcome is 14 agents and 24 functions; those counts are evidence, not a target.
If a negative mutation proves a duplicate or consumerless role, move its unique
behavior to the canonical owner, regenerate projections, and delete the
redundant typed and generated entries in the same change.

- [ ] **Step 4: Run the full required validation set**

~~~bash
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-contracts
.venv/bin/python scripts/validation/check-document-metadata.py --mode check-active
.venv/bin/python scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
.venv/bin/python scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted
.venv/bin/python scripts/validation/check-document-corpus-lifecycle.py --mode check-archive
.venv/bin/python scripts/validation/check-document-links.py --mode traceability
.venv/bin/python scripts/validation/check-document-links.py --mode alignment
.venv/bin/python scripts/validation/check-operations-catalog.py --mode complete
.venv/bin/python scripts/validation/check-script-manifest.py
.venv/bin/python scripts/validation/check-agent-governance-contract.py --mode contract
.venv/bin/python scripts/validation/check-agent-governance-contract.py --mode repository --section all
bash scripts/operations/sync-provider-surfaces.sh --check
.venv/bin/python scripts/validation/check-github-workflow-contract.py
.venv/bin/python scripts/validation/run-ci-gate.py --profile local-script-backed
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_contract.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_surface_renderer.py
PYTHONPATH=. .venv/bin/python tests/validation/test_provider_native_surfaces.py
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/validation -p 'test_*.py'
git diff --check
git status --short
~~~

Expected: every validator and test PASS. git status shows only the intended
Task 14 evidence changes before commit.

- [ ] **Step 5: Write back and archive execution evidence**

Update spec.md to current implemented behavior. Complete task.md with command
outputs and Commit IDs. Move plan.md and task.md together to
docs/98.archive/changes/chg-0001-sdlc-taxonomy-convergence/. No active document
links directly to the archived packet.

- [ ] **Step 6: Commit**

~~~bash
git add docs scripts tests
git commit -m "test: complete SDLC governance convergence"
~~~

## Verification Plan

Each Task runs its focused tests before commit. The final required sequence is
the Task 14 Step 3 command block.

Expected final structural assertions:

~~~bash
test ! -e docs/04.execution
test ! -e docs/02.architecture/requirements
test ! -e docs/05.operations/guides
test ! -e docs/05.operations/policies
test ! -e docs/05.operations/runbooks
test -d docs/05.operations/catalog
test ! -e docs/05.operations/00-workspace
test ! -e docs/05.operations/12-infra-net
test -d docs/05.operations/incidents
test -d docs/05.operations/releases
test ! -e archive
~~~

All commands must return zero.

The final path scan must return no tracked documentation identity containing a
YYYY-MM-DD prefix or a four-digit year directory except the exact
`docs/05.operations/incidents/<year>/inc-####-<slug>/` containment route. The
final script manifest must exactly equal `git ls-files scripts`. Graphify
regeneration is last and is advisory when its health report identifies
ignored-volume or unrelated-root contamination.

## Risks and Rollback

| Risk | Guardrail | Recovery |
| :-- | :-- | :-- |
| Link explosion from bulk moves | Commit mapping first; move one bounded unit; run link gate | Correct links or revert the logical commit |
| Target profiles hide old paths | Explicit bounded migration manifest and final no-transition test | Restore prior profile commit |
| Full Specs remain in tombstone role | Per-Spec mig-0001 disposition and active-consumer check | Restore current Spec before re-running archive task |
| Similar Operations names are incorrectly merged | Require all four typed merge criteria, per-file preservation tokens, user approval, and a negative similarity-only mutation | Revert the bounded domain commit and correct the approved mig-0002 rows |
| Structure and content changes become unreviewable | Commit the catalog move before any semantic subject change; use four bounded domain-group commits | Revert only the affected logical commit |
| Operations roles lose unique content | Move roles before deduplication; diff each subject | Restore content from previous commit |
| Script deletion breaks a hidden consumer | Manifest consumers, rg scan, tests, and gate graph | Restore file and consumer record in corrective commit |
| Generator changes working tree in check mode | Mutation test around every generator | Revert generator commit |
| CI differs from local | Exact leaf-set parity test | Revert workflow routing commit |
| Runtime-changing rehearsal executes accidentally | Plan invokes only tests and check modes | Stop; do not retry Runtime command without separate approval |

No recovery step uses git reset --hard, checkout discard, force push, or
history rewriting.

## Approval Gates

- The user approved the four-section design and the written Spec.
- Protected Stage 00 and Stage 99 edits require their typed owners and
  mandatory reviewers during subagent-driven implementation.
- Runtime, remote, credential, and deployment actions remain outside approval.
- Any proposed change to the target taxonomy returns to the user before
  implementation continues.

## Completion Criteria

- All 16 acceptance criteria in Spec 136 are satisfied.
- Every Task has an independently reviewable logical Commit.
- Stage 04, Architecture requirements, parallel Operations role roots, root
  archive, and dated documentation identities are absent.
- The live script manifest contains only maintained files.
- The migration ledger accounts for every move, merge, replacement, and
  deletion.
- Local and CI document-governance aggregates contain identical leaves.
- Required metadata, lifecycle, archive, link, traceability, template,
  governance, provider, generated-output, script, workflow, and test gates pass.
- Spec current truth is written back before Plan and Task evidence is archived.

## Related Documents

- [Approved specification](spec.md)
- [Stage 00 bootstrap](../../00.agent-governance/policies/bootstrap.md)
- [Stage authoring matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Workflow contract](../../../.github/workflow-contract.yml)
