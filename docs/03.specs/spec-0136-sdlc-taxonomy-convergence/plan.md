---
status: active
artifact_id: plan-0136
artifact_type: plan
parent_ids:
  - spec-0136
created: 2026-08-07
updated: 2026-08-11
---
# SDLC Taxonomy and Agent Governance Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

## Overview

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

### Global Constraints

- Operations remains docs/05.operations; it is never renumbered.
- docs/02.architecture/requirements is replaced by descriptions and
  Architecture Description.
- docs/04.execution is removed after Plan and Task migration.
- Every documentation identity uses a stable type ID and slug; no date prefix
  or year partition remains.
- Dates live in typed frontmatter. Event timelines may retain timestamps in
  body content.
- docs/98.archive is the only documentation archive.
- Active documents never link directly to Stage 98.
- No redirect, legacy, deprecated, dormant, or compatibility file remains at
  completion.
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
| Operations grouped by domain and subject | Tasks 6A through 6D |
| No date or year path identity | Tasks 4 through 7 and Task 14 |
| Typed frontmatter dates | Tasks 2, 4 through 7 |
| Stage 98 is the sole archive | Task 7 |
| No active-to-archive links | Tasks 5, 7, 10, and 13 |
| Stage 99 matches the taxonomy | Task 2 |
| Stage 00 has one authority model | Tasks 2 and 8 |
| Every script has owner, consumer, mutation, and test | Tasks 3 and 9 |
| Duplicate and one-time scripts are absent | Tasks 9 and 11 |
| Validator ownership and local/CI parity | Tasks 10 through 12 |
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

- Modify: docs/00.agent-governance/contracts/agent-governance-artifacts.yaml
- Modify: docs/00.agent-governance/rules/documentation-protocol.md
- Modify: docs/00.agent-governance/rules/stage-authoring-matrix.md
- Modify: docs/00.agent-governance/scopes/docs.md
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

- Modify: docs/00.agent-governance/rules/bootstrap.md
- Modify: documentation-protocol.md, output-style.md, standards.md,
  agentic.md, workflows.md, task-checklists.md, postflight-checklist.md,
  persona.md, and stage-authoring-matrix.md
- Modify or delete: docs/00.agent-governance/scopes/backend.md, entry.md,
  frontend.md, meta.md, mobile.md, and product.md
- Modify: docs/00.agent-governance/providers/agents-md.md
- Modify: docs/00.agent-governance/providers/claude.md
- Modify: docs/00.agent-governance/providers/codex.md
- Modify: docs/00.agent-governance/providers/gemini.md
- Modify: docs/00.agent-governance/contracts/provider-models.yaml
- Modify: docs/00.agent-governance/memory/current.md
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

- [ ] **Step 1: Write equivalence and failure tests**

Fixtures cover anchors, fenced examples, relative links, current-to-archive
links, parent_ids, missing replacements, and immutable created dates.

- [ ] **Step 2: Verify tests fail before extraction**

~~~bash
PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py
PYTHONPATH=. .venv/bin/python tests/validation/test_document_links.py
~~~

Expected: FAIL because shared modules and new CLI do not exist.

- [ ] **Step 3: Extract libraries and replace Shell validators**

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
archive, links, traceability, templates, governance, provider freshness,
generated freshness, and script manifest. Pull Request uses base SHA; push
uses before SHA. Scheduled reporting reuses the same leaves.

- [ ] **Step 4: Verify typed execution**

~~~bash
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-script-backed --list
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_contract.py
PYTHONPATH=. .venv/bin/python tests/validation/test_ci_gate_runner.py
PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_ci_routing.py
PYTHONPATH=. .venv/bin/python tests/validation/test_github_workflow_contract.py
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
- Modify: docs/00.agent-governance/memory/current.md
- Modify: active Markdown links reported by check-document-links.py
- Modify: scripts/README.md
- Modify: .github/INDEX.md and CODEOWNERS when paths changed
- Regenerate: every output registered in scripts/manifest.yaml
- Modify: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md
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
- Modify: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md
- Modify: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md
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

- [ ] **Step 3: Run the full required validation set**

~~~bash
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py --mode check-active
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-archive
python3 scripts/validation/check-document-links.py --mode traceability
python3 scripts/validation/check-document-links.py --mode alignment
python3 scripts/validation/check-script-manifest.py
bash scripts/operations/sync-provider-surfaces.sh --check
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile local-script-backed
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/validation -p 'test_*.py'
git diff --check
git status --short
~~~

Expected: every validator and test PASS. git status shows only the intended
Task 14 evidence changes before commit.

- [ ] **Step 4: Write back and archive execution evidence**

Update spec.md to current implemented behavior. Complete task.md with command
outputs and Commit IDs. Move plan.md and task.md together to
docs/98.archive/changes/chg-0001-sdlc-taxonomy-convergence/. No active document
links directly to the archived packet.

- [ ] **Step 5: Commit**

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
test ! -e archive
~~~

All six commands must return zero.

The final path scan must return no tracked documentation identity containing a
YYYY-MM-DD prefix or a four-digit year directory. The final script manifest
must exactly equal git ls-files scripts. Graphify regeneration is last and is
advisory when its health report identifies ignored-volume or unrelated-root
contamination.

## Risks and Rollback

| Risk | Guardrail | Recovery |
| :-- | :-- | :-- |
| Link explosion from bulk moves | Commit mapping first; move one bounded unit; run link gate | Correct links or revert the logical commit |
| Target profiles hide old paths | Explicit bounded migration manifest and final no-transition test | Restore prior profile commit |
| Full Specs remain in tombstone role | Per-Spec mig-0001 disposition and active-consumer check | Restore current Spec before re-running archive task |
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
- [Stage 00 bootstrap](../../00.agent-governance/rules/bootstrap.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Workflow contract](../../../.github/workflow-contract.yml)
