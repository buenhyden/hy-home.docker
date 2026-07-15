---
status: completed
artifact_id: plan:2026-07-14-document-corpus-lifecycle-migration-foundation
artifact_type: plan
parent_ids:
  - spec:131-document-corpus-lifecycle-migration-foundation
---

# Document Corpus Lifecycle Migration Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (- [ ]) syntax for tracking.

**Goal:** Build the tested, source-backed control plane that later document
corpus migration waves must pass before they may normalize, move, merge,
archive, regenerate, or delete tracked documentation.

**Architecture:** Keep document-type and frontmatter semantics in the existing
Stage 99 metadata registry and its current checker. Add one separate Stage 99
migration-policy registry and one focused Python lifecycle companion for
manifest coverage, archive Git provenance, duplicate candidates, retention
signals, directory budgets, and deterministic ledgers. Route both through the
existing repository-contract job for pull requests and pushes, while a separate
read-only scheduled/manual workflow reports full-corpus debt without promoting
that debt to blocking before Wave E.

**Tech Stack:** YAML 1.2-compatible metadata, Python 3.12, PyYAML, unittest,
Git object plumbing, SHA-256, Bash, Markdown/CommonMark with GitHub Flavored
Markdown conventions, GitHub Actions, pre-commit, repository generators, and
Git.

## Global Constraints

- Spec 131 owns the Foundation only. Do not migrate the active SDLC corpus,
  operations corpus, completed evidence, existing Stage 98 tombstones, Stage 90
  corpus, README corpus, or Stage 04 year partitions in this plan.
- The later migration sequence remains Spec 132 Wave A, Spec 133 Wave B, Spec
  134 Wave C, Spec 135 Wave D, and Spec 136 Wave E. Do not create or implement
  those specifications here.
- docs/99.templates/support/document-metadata-profiles.yaml remains the sole
  machine-readable owner of document-type, frontmatter, relation, heading, and
  template-profile semantics.
- Add exactly one separate machine-readable lifecycle owner for migration
  dispositions, manifest shape, archive preservation, review signals,
  directory budgets, and wave enforcement. It must not redefine document
  profile semantics.
- The metadata checker owns static changed/new archive frontmatter validation.
  A single focused lifecycle companion owns Git-object checks, manifest
  coverage, duplicate candidates, retention signals, directory budgets, and
  deterministic migration/archive ledgers.
- Keep all existing metadata command interfaces compatible. Full-corpus
  findings remain advisory until Wave E; contract corruption, unsafe paths,
  malformed manifests, and promoted Foundation-scope failures remain
  fail-closed.
- An exact content hash, matching title, shared topic, or type match creates
  only an advisory duplicate candidate. No tool may automatically choose
  merge, archive, or delete.
- Destructive manifest dispositions require canonical ownership, enumerated
  active consumers, replacement semantics where applicable, preservation and
  rollback evidence, and independent specification and quality verdicts.
- Default archive preservation is a provenance tombstone tied to immutable Git
  commit and blob objects. Full snapshots are allowed only for approved audit,
  legal, or evidence-preserve cases and must be content-addressed and scanned
  for prohibited material.
- Never read, copy, hash into a report, or print secret values, credentials,
  tokens, private keys, auth files, shell history, raw logs, or diagnostic
  payloads. Diagnostics contain bounded paths, stable finding codes, safe
  metadata, and counts only.
- Directory review signals are 100 immediate Markdown leaves for warning and
  150 for blocking a newly added leaf without an approved partition plan.
  Review-age signals are draft 30 days, active 90 days, and completed execution
  180 days. None may mutate lifecycle status.
- _workspace remains exactly two tracked contract README files plus ignored
  non-secret repo-support scratch. Dry-run output may be staged only under
  _workspace/repo-support and is never treated as canonical evidence.
- Do not create docs/03.specs/requirements or docs/03.specs/decisions.
  Requirements remain in Stage 01 and architecture decisions remain in Stage
  02.
- Preserve historical commands, results, dates, decisions, counts, verdicts,
  approvals, and hashes. Foundation contract edits may clarify current rules
  but must not rewrite historical evidence to resemble current policy.
- No Docker Compose, infrastructure runtime, deployment runtime, secrets,
  credentials, provider-global configuration, model policy, remote GitHub
  setting, ruleset, environment, release, or branch-protection mutation is
  authorized.
- README edits are limited to existing routing, structure, or related-document
  areas. Do not add policy sections to README files.
- Use TDD for every parser, validator, generator, and repository-gate behavior.
  Use apply_patch for authored changes and canonical owner scripts for generated
  outputs.
- Execute tasks serially. Assign every task to a fresh implementation agent,
  then a separate specification reviewer, then a separate quality reviewer.
  A task closes only after all Critical and Important findings are resolved and
  both reviewers re-approve.
- Use at least one logical Conventional Commit per task. Review fixes remain
  separate logical commits when they materially change behavior.
- Never run pre-commit run --all-files directly. The final all-files gate uses
  scripts/validation/run-agent-precommit-all-files.sh from this clean linked
  worktree with the tracked Task evidence file and explicit allowed prefixes.
- After Python, shell, workflow, or validation code changes, run graphify update
  . when available. Graphify remains advisory; corroborate a stale or noisy
  report against tracked source, Stage 00 governance, and stage contracts.

## Overview

This plan implements Spec 131 as six dependency-ordered units. Task 1 defines
the exact machine contracts and static archive metadata semantics. Task 2 adds
the focused lifecycle validator and deterministic data interfaces. Task 3
aligns the human contracts, archive template, Stage 98 route, and Stage 00
authoring duties. Task 4 wires local and tracked CI/QA enforcement without
changing the required-job taxonomy. Task 5 publishes the approved Foundation
manifest and generated Stage 90 evidence. Task 6 runs the controlled all-files
gate, independent branch review, evidence closure, and final status
transitions.

Foundation bootstraps the migration gate that later waves consume. Therefore,
its baseline selection and intended file responsibility are recorded in the
Task before Task 1, then retrospectively validated by the new manifest checker
before Foundation can close. No later wave may use this bootstrap exception.

## Context and Inputs

At baseline e00e1483, the advisory inventory reports 901 typed records and
2,025 findings. Stage 04 has 95 Plans and 117 Tasks in flat directories, and
Stage 98 has 20 tombstones, including five whose provenance exists only in body
tables. Existing changed/new validation is fail-closed, while full-corpus debt
is intentionally advisory.

The current repository already has a strong metadata checker, repository
contract gate, local QA selector, controlled all-files wrapper, 23 pre-commit
hooks, and a 15-job quality-only GitHub Actions workflow. This plan extends
those owners rather than adding a second document schema, a second repository
gate, or a required-job taxonomy.

The Graphify report was built from f8a72211 and is stale relative to this
branch. It is navigation evidence only. Tracked Stage 00, Stage 03, Stage 98,
Stage 99, validation code, tests, and Git history remain authoritative.

Canonical inputs:

- docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md
- docs/03.specs/130-template-contract-system-canonicalization/spec.md
- docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md
- docs/99.templates/support/document-metadata-profiles.yaml
- docs/99.templates/support/frontmatter-contract.md
- docs/99.templates/support/lifecycle-status.md
- docs/99.templates/support/template-governance.md
- docs/98.archive/README.md
- docs/00.agent-governance/rules/documentation-protocol.md
- docs/00.agent-governance/rules/stage-authoring-matrix.md
- docs/00.agent-governance/rules/github-governance.md
- scripts/validation/check-document-metadata.py
- scripts/validation/check-repo-contracts.sh
- scripts/validation/run-agent-precommit-all-files.sh
- .pre-commit-config.yaml
- .github/workflows/ci-quality.yml
- _workspace/README.md

External source decisions already approved in Spec 131:

- YAML 1.2.2 for typed, duplicate-key-safe metadata parsing.
- GitHub Docs frontmatter for consumer-specific profiles.
- CommonMark and GFM for body structure independent of YAML.
- Diataxis for distinct Guide, Policy, Runbook, Reference, and Audit roles.
- ISO/IEC/IEEE 29148 and 42010 plus NASA SWE-052 for identity and
  bidirectional traceability.
- MADR and GitHub Spec Kit for decision and SDLC-stage separation.
- Google SRE incident and postmortem guidance for event-role separation.
- W3C PROV-O for original/derived entity provenance.
- Git object documentation for immutable commit/blob identity.
- GitHub Actions workflow syntax for read-only scheduled/manual checks.
- pre-commit documentation for controlled all-files execution.

## Goals and Non-goals

### Goals

- Define exact machine-readable migration and archive contracts with no
  duplicated document-profile ownership.
- Make new/changed archive tombstones conform to typed, ordered, conditional
  frontmatter.
- Validate complete wave classification, safe disposition semantics, Git
  provenance, snapshot integrity, retention signals, and directory budgets.
- Produce deterministic, reviewable Foundation manifests, archive-ledger
  previews, duplicate candidates, and safe summary evidence.
- Add pull-request/push routing through the existing repo-contracts job and a
  separate read-only scheduled/manual full-corpus workflow.
- Align human Stage 99 contracts, the archive template, Stage 98 routing, and
  Stage 00 agent duties with the executable machine contracts.
- Close with logical commits, fresh implementer/reviewer evidence, generated
  freshness, controlled wrapper evidence, and a clean worktree.

### Non-goals

- Broad frontmatter or body normalization.
- Existing tombstone conversion or immutable snapshot creation.
- Stage 04 year moves.
- Duplicate merge, archive, or deletion actions.
- Full-corpus blocking in pull requests or pushes.
- Runtime Compose, infrastructure, deployment, security-resource, or provider
  configuration changes.
- Remote GitHub mutation or claims about remote workflow execution.

## Acceptance Map

| ID | Foundation acceptance |
| --- | --- |
| VAL-131-001 | One metadata registry owns document profiles and one migration registry owns lifecycle migration policy without overlapping keys. |
| VAL-131-002 | New/changed archive metadata enforces typed identity, conditional replacement, Git provenance shape, and preservation-class conditions. |
| VAL-131-003 | A deterministic manifest covers each selected baseline path exactly once and rejects unsafe or insufficiently evidenced destructive rows. |
| VAL-131-004 | Archive validation proves commit type, blob type, commit:path equality, and snapshot path/SHA-256 equality without leaking payloads. |
| VAL-131-005 | Duplicate reporting is advisory only; directory budgets enforce the 99/100 and 149/150 boundaries; review-age signals never mutate status. |
| VAL-131-006 | Human contracts, templates, Stage 98, and Stage 00 route to the same executable semantics without copied policy in README or templates. |
| VAL-131-007 | Pull-request/push contracts remain in the existing repo-contracts path; scheduled/manual full-corpus reporting is read-only and advisory. |
| VAL-131-008 | Foundation data, generated indexes, audit inventory, Task evidence, reviews, wrapper evidence, and Git commits are deterministic and current. |

## File Responsibility Map

| Surface | Responsibility in this plan |
| --- | --- |
| docs/99.templates/support/document-metadata-profiles.yaml | Sole typed document/profile and static archive frontmatter owner. |
| docs/99.templates/support/document-corpus-migration-contract.yaml | Sole machine owner for migration manifests, dispositions, archive provenance rules, review signals, budgets, and wave enforcement. |
| scripts/validation/check-document-metadata.py | Existing changed/new typed metadata and static archive-condition validator. |
| scripts/validation/check-document-corpus-lifecycle.py | Focused manifest, Git provenance, snapshot, duplicate, retention, budget, and ledger CLI. |
| tests/validation/test_document_metadata.py | Registry v2 and static archive RED/GREEN tests. |
| tests/validation/test_document_corpus_lifecycle.py | Lifecycle companion unit, Git fixture, deterministic output, redaction, and CLI tests. |
| docs/99.templates/support/*.md | Human migration, archive, retention, frontmatter, lifecycle, template, and source-rationale contracts. |
| docs/99.templates/templates/common/archive.template.md | Copyable archive tombstone form only; no migration algorithm. |
| docs/00.agent-governance/rules/*.md | Agent authorization, protected boundaries, authoring, QA, and workflow duties only. |
| docs/98.archive/README.md | Stage 98 routing and transitional ledger status; no duplicated policy. |
| docs/90.references/data/governance/document-corpus-lifecycle/ | Approved Foundation manifest plus deterministic safe summaries. |
| .github/workflows/document-corpus-lifecycle.yml | Read-only scheduled/manual advisory full-corpus reporting and blocking Foundation-contract check. |
| scripts/validation/check-repo-contracts.sh | Existing integrated fail-closed local/CI contract owner. |
| scripts/validation/recommend-qa-gates.sh | Changed-surface routing recommendation. |
| scripts/validation/run-local-qa-gates.sh | Local deterministic gate routing. |
| .pre-commit-config.yaml | Existing changed/new metadata and repo-contract hook routing; no duplicate schema. |
| docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md | Approvals, baseline, task results, reviews, deviations, commits, wrapper path sets, and closure evidence. |

## Work Breakdown

| Task | Description | Acceptance | Primary validation |
| --- | --- | --- | --- |
| T-DCLM-001 | Define migration policy and archive metadata machine contracts. | VAL-131-001/002 | Registry/schema and static archive tests. |
| T-DCLM-002 | Implement the lifecycle companion and safe deterministic interfaces. | VAL-131-003/004/005 | Focused lifecycle unit/CLI/Git tests. |
| T-DCLM-003 | Align human contracts, archive template, Stage 98, and Stage 00 routes. | VAL-131-002/006 | Template/contract/repository checks. |
| T-DCLM-004 | Route Foundation checks through local QA and tracked CI. | VAL-131-007 | Workflow, pre-commit, script-inventory, and repo-contract tests. |
| T-DCLM-005 | Publish the approved Foundation manifest and generated evidence. | VAL-131-003/008 | Manifest and generator write/check equality. |
| T-DCLM-006 | Run full QA, wrapper, whole-branch review, and close evidence. | VAL-131-001 through 008 | Full validation, wrapper, reviews, clean Git state. |

### Planning Prerequisite Completed Before Task 1

The approved execution ledger already exists at
docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md.
It was instantiated from the canonical Task template with not-run result fields
and routed from the Spec and Stage 04 indexes in the same planning commit as
this Plan. The approved Spec transitions from draft to active in that planning
commit. Task 1 therefore updates a tracked artifact; it does not depend on a
future or untracked file.

### Subagent-Driven Commit and Review Protocol

For each Task 1 through 5, the fresh implementer runs RED/GREEN, performs
self-review, records evidence, and creates the initial logical commit. The
controller then supplies that task's exact BASE..HEAD range to a fresh
specification reviewer and, only after specification PASS, to a separate
quality reviewer. Fixes are separate commits, affected checks are rerun, and
both reviewers re-review the new HEAD. The controller never asks reviewers to
approve an uncommitted working tree.

Before any task commit that adds or removes a tracked path, stage only the new
or removed path so Git-backed generators can see the intended index, run the
applicable canonical generators in this order, inspect their exact diffs, and
include the owned fallout in the same task or an immediately following
generated commit:

~~~bash
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
python3 scripts/validation/check-document-metadata.py \
  --mode report \
  --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
~~~

Security readiness is required when scripts or workflows change; the audit
matrix follows it. LLM index/coverage are required for path changes. The
metadata inventory is last when tracked typed documents change. Run each owner
again in check mode before asking for review.

The per-task generated follow-up commands are fixed:

Task 1:

~~~bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
git add docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
git commit -m "docs(generated): index lifecycle machine contract"
~~~

Task 2:

~~~bash
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
git add docs/90.references/data/security/security-automation-readiness.md docs/90.references/data/governance/audit-implementation-matrix.md docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
git commit -m "docs(generated): index lifecycle validator"
~~~

Task 3:

~~~bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
python3 scripts/validation/check-document-metadata.py \
  --mode report \
  --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
git add docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
git commit -m "docs(generated): index lifecycle human contracts"
~~~

Task 4:

~~~bash
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
git add docs/90.references/data/security/security-automation-readiness.md docs/90.references/data/governance/audit-implementation-matrix.md docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
git commit -m "docs(generated): index lifecycle workflow"
~~~

If a listed owner produces no diff, record that check-mode result in the Task
and omit only that empty generated commit. Each task review range includes its
implementation commit and its generated follow-up commit when created.

## Task 1: Machine Contracts and Static Archive Metadata

**Files:**

- Add docs/99.templates/support/document-corpus-migration-contract.yaml.
- Modify docs/99.templates/support/document-metadata-profiles.yaml.
- Modify scripts/validation/check-document-metadata.py.
- Modify tests/validation/test_document_metadata.py.
- Update the Task evidence file.

**Interfaces:** Preserve report, check-changed, check-active, and
check-contracts behavior. The existing checker reads metadata registry schema
version 2 and validates only static archive frontmatter conditions; it does not
run Git-object or snapshot-byte checks.

- [ ] **Step 1: Add RED schema and archive-condition tests**

Add focused tests with these responsibilities:

~~~text
ProfileSchemaTests.test_archive_profile_has_canonical_v2_order
ProfileSchemaTests.test_archive_profile_rejects_unknown_condition_fields
ProfileSchemaTests.test_migration_contract_has_exact_nonoverlapping_ownership
MetadataValidationTests.test_archive_replacement_is_conditional
MetadataValidationTests.test_git_history_forbids_snapshot_fields
MetadataValidationTests.test_immutable_snapshot_requires_all_snapshot_fields
MetadataValidationTests.test_archive_rejects_sentinel_paths_hashes_and_object_ids
MetadataValidationTests.test_existing_tombstones_remain_wave_d_advisory_debt
~~~

Temporary fixtures must cover duplicate YAML keys, unknown enums, absolute and
traversal paths, empty values, N/A sentinels, uppercase/truncated object IDs,
and partial snapshot triples.

Use the existing MetadataValidationTests.record()/codes() fixture pattern. A
complete representative RED test is:

~~~python
def test_git_history_forbids_snapshot_fields(self) -> None:
    record = self.record(
        "docs/98.archive/04.execution/example.md",
        {
            "status": "archived",
            "artifact_id": "archive:04-execution-example",
            "artifact_type": "archive",
            "parent_ids": [],
            "archived_from": "docs/04.execution/example.md",
            "archived_on": "2026-07-14",
            "archive_reason": "Superseded by the canonical execution record.",
            "archive_disposition": "superseded",
            "archived_commit": "a" * 40,
            "archived_blob": "b" * 40,
            "preservation_class": "git-history",
            "current_replacement": "docs/04.execution/canonical.md",
            "snapshot_path": (
                "docs/98.archive/evidence/" + ("c" * 64) + ".md.snapshot"
            ),
            "content_sha256": "c" * 64,
            "snapshot_reason": "Audit evidence.",
        },
        "archive",
    )
    codes = self.codes(record)
    self.assertIn("archive-snapshot-forbidden", codes)
~~~

Use this exact remaining case table in a parameterized test; each row constructs
the same complete archive record, applies overrides, and asserts the listed
stable finding code:

| Case overrides | Expected code |
| --- | --- |
| immutable-snapshot without snapshot_path | archive-snapshot-path-required |
| immutable-snapshot without content_sha256 | archive-content-sha256-required |
| immutable-snapshot without snapshot_reason | archive-snapshot-reason-required |
| withdrawn with current_replacement | archive-replacement-forbidden |
| superseded without current_replacement | archive-replacement-required |
| archived_commit equal to N/A | invalid-archived-commit |
| archived_blob equal to 39 lowercase hex characters | invalid-archived-blob |
| content_sha256 equal to uppercase 64 hex characters | invalid-content-sha256 |
| snapshot_path containing parent traversal | invalid-snapshot-path |

- [ ] **Step 2: Run RED**

~~~bash
python3 -m unittest \
  tests.validation.test_document_metadata.ProfileSchemaTests \
  tests.validation.test_document_metadata.MetadataValidationTests \
  -v
~~~

Expected: new tests fail because schema version 2, the migration contract, and
conditional archive fields are not implemented.

- [ ] **Step 3: Add the exact machine contract**

The migration contract uses exact, fail-closed mappings:

~~~yaml
schema_version: 1
manifest:
  dispositions:
    - migrate
    - preserve
    - move
    - merge
    - archive
    - delete
    - regenerate
    - exempt
archive:
  dispositions:
    - superseded
    - duplicate
    - conflict
    - withdrawn
    - evidence-preserve
  preservation_classes:
    - git-history
    - immutable-snapshot
directory_budgets:
  warning_at: 100
  block_new_leaf_at: 150
review_signals:
  draft_days: 30
  active_days: 90
  completed_execution_days: 180
~~~

Declare the exact manifest shape in the same contract:

~~~yaml
manifest_schema:
  top_level_fields:
    - schema_version
    - wave
    - baseline_commit
    - generated_by
    - enforcement
    - entries
  entry_fields:
    - source_path
    - target_path
    - artifact_id
    - artifact_type
    - status_before
    - status_after
    - parent_ids
    - disposition
    - canonical_replacement
    - active_consumers
    - partition_plan
    - preservation_class
    - evidence
    - review_verdict
  evidence_fields:
    - commands
    - sources
    - repository_paths
    - consumer_scan
    - rollback
  review_verdict_fields:
    - specification
    - quality
  review_verdict_values:
    - pending
    - pass
    - changes-required
~~~

Types and nullability are exact:

- schema_version is integer 1; wave and generated_by are non-empty strings;
  baseline_commit is a verified lowercase full commit object ID; enforcement is
  advisory or blocking; entries is a list.
- source_path is a safe baseline-tracked path. target_path is a safe path or
  null. artifact_id is a valid stable ID or null only for a declared profile
  exception. artifact_type is a registered type.
- status_before and status_after are registry statuses or null only for a
  declared exception. parent_ids, active_consumers, and all five evidence
  members are deterministically ordered string lists. partition_plan is a safe
  approved Plan path or null.
- canonical_replacement and preservation_class are strings or null.
  preservation_class, when present, is git-history or immutable-snapshot.
- review_verdict is exactly a specification/quality mapping.
- delete requires null target_path. move, merge, and archive require a distinct
  non-null target. migrate, preserve, regenerate, and exempt require
  target_path equal to source_path.
- merge, archive, and delete require an explicit active_consumers list, a
  non-empty consumer_scan evidence list proving that enumeration, non-empty
  commands/sources/repository_paths/rollback lists, a preservation class,
  required replacement semantics, and pass/pass reviews. An honestly verified
  orphan may have an empty active_consumers list; the validator must never
  fabricate a consumer. No pending or changes-required destructive row is
  executable.

Define a separate bounded exception input for the future check-full interface:

~~~yaml
exception_schema:
  top_level_fields:
    - schema_version
    - exceptions
  entry_fields:
    - finding_code
    - scope_paths
    - owner
    - reason
    - approved_at
    - expires_on
    - exit_condition
    - evidence
~~~

Every exception must be finding-code-specific, path-bounded, owned, reasoned,
approved, unexpired, and have a non-empty exit condition and safe evidence
paths. Wildcard/global, ownerless, permanent, expired, or unknown-code
exceptions fail closed. Foundation tests this contract but does not add an
exception file.

Also declare disposition conditions, replacement requirements, snapshot
admission conditions and safe diagnostics. The Foundation source selection is
the following exact baseline-tracked document list:

~~~yaml
waves:
  foundation:
    enforcement: advisory
    manifest_path: null
    scope_state: approved
    source_paths:
      - docs/00.agent-governance/memory/progress.md
      - docs/00.agent-governance/rules/documentation-protocol.md
      - docs/00.agent-governance/rules/github-governance.md
      - docs/00.agent-governance/rules/stage-authoring-matrix.md
      - docs/00.agent-governance/rules/task-checklists.md
      - docs/03.specs/README.md
      - docs/04.execution/README.md
      - docs/04.execution/plans/README.md
      - docs/04.execution/tasks/README.md
      - docs/90.references/README.md
      - docs/90.references/data/README.md
      - docs/90.references/data/governance/README.md
      - docs/98.archive/README.md
      - docs/99.templates/support/README.md
      - docs/99.templates/support/common-document-contract.md
      - docs/99.templates/support/external-source-rationale.md
      - docs/99.templates/support/frontmatter-contract.md
      - docs/99.templates/support/lifecycle-status.md
      - docs/99.templates/support/sdlc-document-contract.md
      - docs/99.templates/support/template-contract.md
      - docs/99.templates/support/template-governance.md
      - docs/99.templates/support/template-selection.md
      - docs/99.templates/templates/common/README.md
      - docs/99.templates/templates/common/archive.template.md
    declared_outputs:
      - .github/workflows/document-corpus-lifecycle.yml
      - docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md
      - docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md
      - docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md
      - docs/90.references/data/governance/document-corpus-lifecycle/README.md
      - docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md
      - docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
      - docs/99.templates/support/archive-retention-contract.md
      - docs/99.templates/support/corpus-migration-contract.md
      - docs/99.templates/support/document-corpus-migration-contract.yaml
      - scripts/validation/check-document-corpus-lifecycle.py
      - tests/validation/test_document_corpus_lifecycle.py
  wave-a-active-sdlc:
    enforcement: advisory
    manifest_path: null
    scope_state: unapproved
    source_paths: []
    declared_outputs: []
  wave-b-operations:
    enforcement: advisory
    manifest_path: null
    scope_state: unapproved
    source_paths: []
    declared_outputs: []
  wave-c-historical-evidence:
    enforcement: advisory
    manifest_path: null
    scope_state: unapproved
    source_paths: []
    declared_outputs: []
  wave-d-archive-provenance:
    enforcement: advisory
    manifest_path: null
    scope_state: unapproved
    source_paths: []
    declared_outputs: []
  wave-e-references-final-gates:
    enforcement: advisory
    manifest_path: null
    scope_state: unapproved
    source_paths: []
    declared_outputs: []
planned_partitions:
  docs/04.execution/plans: docs/04.execution/plans/YYYY
  docs/04.execution/tasks: docs/04.execution/tasks/YYYY
~~~

Declared outputs are validated safe paths but are not represented as
fictional baseline source rows. Declare later-wave enforcement as advisory.
Reject
unknown keys, non-positive thresholds, warning values not below blocking
values, overlapping ownership with the metadata registry, or a later wave
marked blocking.

- [ ] **Step 4: Extend archive metadata profile version 2**

Use this canonical presentation order after archive_reason:

~~~text
archive_disposition
archived_commit
archived_blob
preservation_class
current_replacement
snapshot_path
content_sha256
snapshot_reason
~~~

New archive targets require status, artifact_id, artifact_type, parent_ids,
archived_from, archived_on, archive_reason, archive_disposition,
archived_commit, archived_blob, and preservation_class. Supersedes and
current_replacement remain conditional. The snapshot triple is conditional.

Static conditions:

- current_replacement is required for superseded, duplicate, and conflict;
  forbidden for withdrawn; optional for evidence-preserve.
- git-history forbids all snapshot fields.
- immutable-snapshot requires snapshot_path, content_sha256, and
  snapshot_reason.
- object IDs are lowercase full 40- or 64-hex strings.
- content_sha256 is lowercase 64-hex.
- repository paths are relative, normalized, and traversal-free.

- [ ] **Step 5: Implement fail-closed static validation**

Extend load_profiles() and validate_record() without embedding Git access.
Keep existing tombstones outside Foundation changed/new blocking unless they
are edited; Wave D owns their migration. Emit stable finding codes and never
include frontmatter payload values in diagnostics when a key can contain
sensitive text.

- [ ] Parse and exact-key-check migration contract schema version 1.
- [ ] Parse registry schema version 2 and reject unknown archive conditions.
- [ ] Add archive enum and conditional-required/forbidden helpers.
- [ ] Add lowercase full object-ID and SHA-256 shape helpers.
- [ ] Add safe relative archive/snapshot path checks.
- [ ] Wire helpers into validate_record() for new/changed archive records.
- [ ] Preserve existing CLI mode selection and advisory legacy behavior.

- [ ] **Step 6: Run GREEN and compatibility checks**

~~~bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e00e1483
python3 scripts/validation/check-document-metadata.py --mode check-active
git diff --check
~~~

Expected: all metadata tests pass; changed mode has zero blocking findings;
active mode retains its advisory baseline rather than becoming a migration
gate.

- [ ] **Step 7: Commit, then review**

Run graphify update . because Python changed. Record implementer self-review
and commit the GREEN implementation:

~~~bash
git add docs/99.templates/support/document-corpus-migration-contract.yaml docs/99.templates/support/document-metadata-profiles.yaml scripts/validation/check-document-metadata.py tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md
git commit -m "feat(docs): define corpus lifecycle machine contracts"
~~~

Provide that commit range to the fresh specification reviewer and then the
fresh quality reviewer. Resolve findings in separate fix commits and obtain
re-review before starting Task 2.

## Task 2: Lifecycle Validator, Git Provenance, and Deterministic Data

**Files:**

- Add scripts/validation/check-document-corpus-lifecycle.py.
- Add tests/validation/test_document_corpus_lifecycle.py.
- Update the Task evidence file.

**Interfaces:** The companion imports shared metadata parsing as a module
without renaming or repurposing the current artifact-ID Manifest type. It
defaults to the canonical metadata and migration registries and supports
explicit root paths for isolated tests.

Required modes:

~~~text
check-contract
generate-manifest
check-manifest
check-promoted
generate-summary
check-summary
check-impacted
report-duplicates
report-full
check-full
check-archive
check-directory-budget
generate-archive-ledger
check-archive-ledger
generate-snapshot-manifest
check-snapshot-manifest
~~~

Write-capable modes require an explicit output path. generate-manifest creates
only a pending skeleton; check-manifest validates a reviewed manifest and its
canonical serialization without replacing human dispositions. generate-summary
derives the safe summary from that reviewed manifest, and check-summary compares
the generated bytes without mutation. Other check modes never mutate.
report-full exits zero for bounded corpus debt but nonzero for parser, contract,
Git safety, path safety, or internal failures. check-full blocks all findings
and is implemented now but is not promoted to CI until Wave E.

The CLI arguments and exit contract are exact:

~~~text
--root PATH
--profiles PATH
--contract PATH
--mode MODE
--wave WAVE
--base-ref GIT_REF
--manifest PATH
--exceptions PATH
--output PATH
~~~

- root defaults to the repository root; profiles and contract default to the
  two canonical Stage 99 registries.
- wave is required for explicit manifest generation/validation. check-promoted
  forbids wave and manifest because it reads every declared wave from the
  registry. base-ref is required for skeleton generation and check-impacted.
- manifest is required for explicit manifest and summary modes.
  exceptions is optional only for check-full and must pass the exact exception
  schema when supplied.
- output is required only for generate-manifest, generate-summary,
  report-duplicates, generate-archive-ledger, and
  generate-snapshot-manifest. Their paired check modes require the same output
  path and never write.
- exit 0 means the selected contract passes or an advisory report completed
  safely; exit 1 means blocking findings; exit 2 means CLI misuse; exit 3 means
  contract/parser/Git/path/redaction safety failure.

check-promoted is the exception to the explicit wave and manifest arguments:
it rejects either argument and reads every wave entry from the migration
contract in stable order. An advisory wave may have manifest_path null. A
blocking wave must have a safe existing manifest_path, and check-promoted
applies check-manifest to it. The manifest enforcement value must equal the
registry wave enforcement value. This lets Task 4 install CI before Task 5
promotes Foundation without tolerating a missing or mismatched blocking
manifest.

Implement the parser from one fixed mode tuple so tests and help output cannot
drift:

~~~python
MODES = (
    "check-contract",
    "generate-manifest",
    "check-manifest",
    "check-promoted",
    "generate-summary",
    "check-summary",
    "check-impacted",
    "report-duplicates",
    "report-full",
    "check-full",
    "check-archive",
    "check-directory-budget",
    "generate-archive-ledger",
    "check-archive-ledger",
    "generate-snapshot-manifest",
    "check-snapshot-manifest",
)

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=pathlib.Path, default=ROOT)
parser.add_argument("--profiles", type=pathlib.Path, default=DEFAULT_PROFILES)
parser.add_argument("--contract", type=pathlib.Path, default=DEFAULT_CONTRACT)
parser.add_argument("--mode", required=True, choices=MODES)
parser.add_argument("--wave")
parser.add_argument("--base-ref")
parser.add_argument("--manifest", type=pathlib.Path)
parser.add_argument("--exceptions", type=pathlib.Path)
parser.add_argument("--output", type=pathlib.Path)
args = parser.parse_args()
~~~

Immediately validate mode-specific required/forbidden argument combinations
and return exit 2 before opening a repository file when the CLI shape is
invalid.

Use these exact public data contracts and signatures:

~~~python
@dataclasses.dataclass(frozen=True)
class ReviewVerdict:
    specification: str
    quality: str


@dataclasses.dataclass(frozen=True)
class ManifestEvidence:
    commands: tuple[str, ...]
    sources: tuple[str, ...]
    repository_paths: tuple[pathlib.PurePosixPath, ...]
    consumer_scan: tuple[str, ...]
    rollback: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class MigrationManifestRow:
    source_path: pathlib.PurePosixPath
    target_path: pathlib.PurePosixPath | None
    artifact_id: str | None
    artifact_type: str
    status_before: str | None
    status_after: str | None
    parent_ids: tuple[str, ...]
    disposition: str
    canonical_replacement: str | None
    active_consumers: tuple[pathlib.PurePosixPath, ...]
    partition_plan: pathlib.PurePosixPath | None
    preservation_class: str | None
    evidence: ManifestEvidence
    review_verdict: ReviewVerdict


@dataclasses.dataclass(frozen=True)
class MigrationManifestDocument:
    schema_version: int
    wave: str
    baseline_commit: str
    generated_by: str
    enforcement: str
    entries: tuple[MigrationManifestRow, ...]


@dataclasses.dataclass(frozen=True, order=True)
class DuplicateCandidate:
    left_path: pathlib.PurePosixPath
    right_path: pathlib.PurePosixPath
    artifact_type: str
    signals: tuple[str, ...]
~~~

The exact public signatures are:

~~~text
load_migration_contract(path: pathlib.Path) -> dict[str, object]
load_migration_manifest(path: pathlib.Path) -> MigrationManifestDocument
render_migration_manifest(document: MigrationManifestDocument) -> str
generate_manifest_skeleton(
    root: pathlib.Path,
    contract: dict[str, object],
    *,
    wave: str,
    baseline_ref: str,
) -> MigrationManifestDocument
validate_migration_manifest(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    document: MigrationManifestDocument,
) -> list[Finding]
collect_impacted_records(
    root: pathlib.Path,
    records: collections.abc.Sequence[Record],
    profiles: dict[str, object],
    contract: dict[str, object],
    documents: collections.abc.Sequence[MigrationManifestDocument],
    *,
    base_ref: str,
) -> tuple[Record, ...]
validate_archive_provenance(
    root: pathlib.Path,
    record: Record,
) -> list[Finding]
validate_directory_budgets(
    records: collections.abc.Sequence[Record],
    *,
    added_paths: frozenset[pathlib.PurePosixPath],
    warning_at: int,
    block_new_leaf_at: int,
    enforce_all: bool,
) -> list[Finding]
find_duplicate_candidates(
    root: pathlib.Path,
    records: collections.abc.Sequence[Record],
) -> tuple[DuplicateCandidate, ...]
render_archive_ledger(records: collections.abc.Sequence[Record]) -> str
render_snapshot_manifest(records: collections.abc.Sequence[Record]) -> str
validate_exceptions(
    path: pathlib.Path,
    *,
    known_codes: frozenset[str],
    today: datetime.date,
) -> list[Finding]
~~~

The names, parameters, return types, nullability, and ownership are fixed by
this Plan. Implementations must return immutable, deterministically ordered
values and stable Finding records rather than printing from library functions.

- [ ] **Step 1: Add RED manifest and contract tests**

Cover exact top-level/entry keys, deterministic serialization, one row per
selected baseline path, duplicate and omitted rows, unsafe paths, wrong types,
unknown dispositions, baseline commit verification, disposition/target
conditions, and pending/pass/changes-required reviewer objects. Also prove
check-promoted skips an advisory null manifest_path, rejects a blocking null or
missing manifest_path, rejects registry/manifest enforcement mismatch, and
validates a blocking existing manifest.

A generated skeleton must use review verdict pending and must not invent
parent IDs, replacements, consumers, evidence, preservation choices, or
approval. Blocking validation intentionally rejects destructive pending rows.

Add a complete representative fixture using the same helper pattern for every
condition:

~~~python
def test_destructive_pending_row_is_rejected(self) -> None:
    row = self.valid_row(
        disposition="delete",
        target_path=None,
        preservation_class="git-history",
        active_consumers=("docs/consumer.md",),
        evidence={
            "commands": ["git show BASE:docs/source.md"],
            "sources": ["docs/source.md"],
            "repository_paths": ["docs/source.md"],
            "consumer_scan": ["rg --fixed-strings docs/source.md"],
            "rollback": ["revert logical task commit"],
        },
        review_verdict={
            "specification": "pending",
            "quality": "pending",
        },
    )
    findings = self.validate(entries=[row])
    self.assertIn(
        "manifest-destructive-review-required",
        {finding.code for finding in findings},
    )
~~~

Use one parameterized manifest test with the exact additional rows:

| Mutation | Expected code |
| --- | --- |
| remove one selected source row | manifest-source-missing |
| duplicate one source row | manifest-source-duplicate |
| set delete target_path to source_path | manifest-delete-target-invalid |
| set move target_path to null | manifest-move-target-required |
| set preserve target_path to a different path | manifest-preserve-target-invalid |
| set source_path to an absolute path | manifest-source-path-invalid |
| use an unknown artifact_type | manifest-artifact-type-invalid |
| use an expired bounded exception | exception-expired |
| use wildcard exception scope | exception-scope-invalid |
| omit exception owner | exception-owner-required |

- [ ] **Step 2: Add RED archive-provenance tests**

Use temporary Git repositories to verify:

- archived_commit exists and resolves as a commit;
- archived_blob exists and resolves as a blob;
- archived_commit:archived_from resolves to exactly archived_blob;
- snapshot_path equals
  docs/98.archive/evidence/<content_sha256>.md.snapshot;
- snapshot bytes and archived blob bytes both hash to content_sha256;
- git-history forbids snapshot bytes;
- secret-, credential-, token-, key-, shell-history-, and raw-log-like snapshot
  fixtures are rejected without printing their contents.

The same fixtures must prove generate-archive-ledger/check-archive-ledger and
generate-snapshot-manifest/check-snapshot-manifest byte equality in temporary
output paths. They do not publish repository outputs in Foundation.

- [ ] **Step 3: Add RED duplicate, review, and budget tests**

Cover same-type exact-content and normalized-title candidate signals,
cross-type exclusion, deterministic ordering, no automatic disposition,
review-age-unavailable when no real review evidence exists, no status mutation,
immediate-leaf counting exclusions, and the 99/100 and 149/150 boundaries.
Adding a new leaf at 150 must fail unless the manifest carries an approved
partition-plan reference; editing an existing leaf must not be treated as an
addition.

check-impacted must select changed/new typed records plus direct parent,
supersession, manifest consumer, replacement, and Markdown-link dependents. A
RED fixture changes one source and proves its declared consumer is selected;
another title-similar but unlinked document must not be selected.

check-impacted loads every non-null wave manifest_path declared by the
migration contract in wave order, validates each manifest before use, and
passes that immutable sequence into collect_impacted_records(). Before Task 5
the sequence is empty and metadata/link dependents still work; after promotion
the Foundation consumer/replacement rows participate automatically.

Add bounded exception fixtures for unknown finding codes, wildcard paths,
missing owner/reason/exit condition, expired dates, and a valid unexpired
path-specific exception. check-full is the only mode that consumes this input;
report-full never suppresses findings.

- [ ] **Step 4: Run RED**

~~~bash
python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v
~~~

Expected: failure because the lifecycle companion does not exist.

- [ ] **Step 5: Implement the focused companion**

Use immutable dataclasses for MigrationManifestRow,
MigrationManifestDocument, and DuplicateCandidate. Reuse the existing
metadata parser, Record, Finding, safe-path checks, and artifact-ID index;
never repurpose its Manifest class.

Git probes use argument arrays and verify object type before comparison.
Diagnostics expose finding code, bounded path, and safe reason only. All
renderers sort paths and keys deterministically, use LF line endings, and
support write/check equality. The archive ledger is derived from validated
tombstone metadata; it never becomes an editable source of truth.

- [ ] Add immutable data classes and exact YAML loaders/renderers.
- [ ] Add mode-specific CLI argument validation and stable exit codes.
- [ ] Add baseline commit and exact source-coverage validation.
- [ ] Add disposition, reviewer, preservation, and exception validation.
- [ ] Add impacted-parent/supersession/consumer/replacement/link selection.
- [ ] Add Git commit/blob/path equality and snapshot-byte SHA-256 validation.
- [ ] Add redacted confidentiality-pattern rejection.
- [ ] Add immediate-leaf budgets and non-mutating review-age signals.
- [ ] Add deterministic duplicate candidates, summary, archive ledger, and
  snapshot manifest render/check modes.
- [ ] Add report-full advisory aggregation and check-full blocking aggregation.

- [ ] **Step 6: Run GREEN and compatibility checks**

~~~bash
python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v
python3 -m unittest tests.validation.test_document_metadata -v
python3 -m py_compile scripts/validation/check-document-corpus-lifecycle.py scripts/validation/check-document-metadata.py
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
git diff --check
~~~

Expected: all focused and metadata tests pass; compile and contract checks
return zero; no corpus file or archive payload is modified.

- [ ] **Step 7: Commit, then review**

Run graphify update ., record implementer self-review, and commit:

~~~bash
git add scripts/validation/check-document-corpus-lifecycle.py tests/validation/test_document_corpus_lifecycle.py docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md
git commit -m "feat(validation): add document corpus lifecycle checks"
~~~

Review the committed range with fresh specification and quality reviewers.
Commit fixes separately and obtain both re-reviews before Task 3.

## Task 3: Human Contracts, Archive Template, and Governance Routing

**Files:**

- Add docs/99.templates/support/corpus-migration-contract.md.
- Add docs/99.templates/support/archive-retention-contract.md.
- Modify docs/99.templates/support/frontmatter-contract.md.
- Modify docs/99.templates/support/lifecycle-status.md.
- Modify docs/99.templates/support/common-document-contract.md.
- Modify docs/99.templates/support/sdlc-document-contract.md.
- Modify docs/99.templates/support/template-contract.md.
- Modify docs/99.templates/support/template-governance.md.
- Modify docs/99.templates/support/template-selection.md.
- Modify docs/99.templates/support/external-source-rationale.md.
- Modify docs/99.templates/support/README.md.
- Modify docs/99.templates/templates/common/archive.template.md.
- Modify docs/99.templates/templates/common/README.md.
- Modify docs/98.archive/README.md.
- Modify docs/00.agent-governance/rules/documentation-protocol.md.
- Modify docs/00.agent-governance/rules/stage-authoring-matrix.md.
- Modify docs/00.agent-governance/rules/task-checklists.md.
- Modify tests/validation/test_document_metadata.py.
- Modify tests/validation/test_document_corpus_lifecycle.py.
- Update the Task evidence file.

- [ ] **Step 1: Add RED human-contract and template tests**

Extend focused validation to assert:

- one human owner for migration and one human owner for archive/retention;
- every human enum, threshold, field, and condition matches the machine
  contract;
- template governance contains approval boundaries but not copied archive or
  migration algorithms;
- archive.template.md uses the exact archive profile and canonical key order;
- Overview, Archive Metadata, Archive Ledger, and Related Documents are
  required;
- Current Replacement and Preserved Evidence are conditional sections;
- no N/A placeholder instructs users to fabricate a replacement;
- Stage 98 declares its hand-maintained ledger transitional until Wave D;
- Stage 00 routes agent duties to Stage 99 instead of redefining them.

- [ ] **Step 2: Run RED**

~~~bash
python3 -m unittest \
  tests.validation.test_document_metadata.ProfileSchemaTests \
  tests.validation.test_document_metadata.MetadataValidationTests \
  -v
python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v
~~~

Expected: failures identify missing human owners, template drift, and missing
Stage 00/98 routing.

- [ ] **Step 3: Write the canonical human contracts**

corpus-migration-contract.md owns manifest scope, dispositions, consumer and
replacement evidence, review verdicts, duplicate proof, wave promotion,
rollback, and dry-run/promotion boundaries.

archive-retention-contract.md owns tombstone provenance, Git object identity,
snapshot admission and confidentiality, review signals, directory budgets,
Stage 04 future partition shape, archive-ledger derivation, and evidence
preservation.

Link shared metadata semantics rather than copying them. Move any archive or
retention algorithm currently embedded in template-governance.md into the new
owner; leave only governance/approval boundaries in template governance.

- [ ] Write corpus-migration-contract.md from the machine manifest contract.
- [ ] Write archive-retention-contract.md from the machine archive contract.
- [ ] Route frontmatter-contract.md to conditional archive metadata.
- [ ] Route lifecycle-status.md to review signals without automatic mutation.
- [ ] Route common/sdlc contracts to their lifecycle responsibilities.
- [ ] Remove copied algorithms from template-governance.md.
- [ ] Align template-contract.md, template-selection.md, and support README.
- [ ] Add only source-to-local-consequence analysis to
  external-source-rationale.md.

- [ ] **Step 4: Align template and direct consumers**

Update the archive template with required typed metadata and conditional
sections. Do not copy rules or sample evidence into the template. Update Stage
98 routing and label its current manual ledger transitional; do not claim it
is generated and do not edit the 20 existing tombstones.

Update Stage 00 authoring and checklist duties to require manifest-first
classification, safe provenance checks, independent review, canonical
generator use, and wrapper evidence. Stage 00 remains the authority owner and
routes exact document semantics to Stage 99.

- [ ] Update archive.template.md keys and required/conditional headings.
- [ ] Update the common template catalog route.
- [ ] Update Stage 98 README routing and transitional-ledger wording.
- [ ] Update documentation-protocol.md authoring sequence.
- [ ] Update stage-authoring-matrix.md archive/migration routes.
- [ ] Update task-checklists.md evidence and wrapper duties.

- [ ] **Step 5: Verify primary-source attribution**

Ensure external-source-rationale.md records the approved consequences from
YAML, GitHub frontmatter, CommonMark/GFM, Diataxis, traceability sources,
MADR/Spec Kit, Google SRE, W3C PROV-O, Git, GitHub Actions, and pre-commit.
Repository-local values and approval rules must be clearly identified as local
decisions, not claims made by external sources.

- [ ] **Step 6: Run GREEN**

~~~bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e00e1483
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
~~~

Expected: all focused tests and documentation contracts pass; zero broken
routes; existing tombstones remain unchanged.

- [ ] **Step 7: Commit, then review**

Record implementer self-review and commit the exact human-contract surfaces:

~~~bash
git add docs/00.agent-governance/rules docs/98.archive/README.md docs/99.templates/support docs/99.templates/templates/common/archive.template.md docs/99.templates/templates/common/README.md tests/validation/test_document_metadata.py tests/validation/test_document_corpus_lifecycle.py docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md
git commit -m "docs(governance): align corpus migration and archive rules"
~~~

Review the committed range with fresh specification and quality reviewers.
Commit fixes separately and obtain both re-reviews before Task 4.

## Task 4: Repository Contracts, QA Routing, and Tracked Workflow

**Files:**

- Add .github/workflows/document-corpus-lifecycle.yml.
- Modify scripts/validation/check-repo-contracts.sh.
- Modify scripts/validation/recommend-qa-gates.sh.
- Modify scripts/validation/run-local-qa-gates.sh.
- Modify scripts/README.md.
- Modify .pre-commit-config.yaml only to extend the existing repo-contracts
  changed-file routing.
- Modify docs/00.agent-governance/rules/github-governance.md.
- Update the Task evidence file.

**Interfaces:** Keep all ci-quality.yml job IDs and local ruleset required
status checks unchanged. Do not add a second schema hook. The existing
repo-contracts gate invokes lifecycle contract and current Foundation checks.

- [ ] **Step 1: Add RED repository and workflow contract assertions**

Add exact assertions for:

- the lifecycle script and test are inventoried;
- the migration registry exists and passes check-contract;
- repo-contracts runs check-contract and check-promoted without path-filter
  dependence;
- the pre-commit repo-contracts file selector includes the new registry,
  lifecycle script/test, .github/workflows, and .pre-commit-config.yaml;
- the scheduled workflow has only schedule and workflow_dispatch triggers;
- top-level and job permissions are contents: read;
- checkout and setup-python are immutable SHA-pinned;
- checkout uses fetch-depth: 0 for Git-object provenance;
- dependencies come from scripts/requirements.txt;
- no write permission, secret interpolation, pull_request_target,
  continue-on-error, deployment, release, environment, or remote mutation
  command exists;
- the workflow blocks contract/promoted-wave errors and runs full-corpus debt
  in advisory report mode.

- [ ] **Step 2: Run RED**

~~~bash
bash -n scripts/validation/check-repo-contracts.sh scripts/validation/recommend-qa-gates.sh scripts/validation/run-local-qa-gates.sh
bash scripts/validation/check-repo-contracts.sh
~~~

Expected: the new exact assertions fail because workflow and routing do not
exist.

- [ ] **Step 3: Add the read-only workflow**

Create document-corpus-lifecycle.yml with schedule and workflow_dispatch,
concurrency cancellation, least privilege, pinned actions, full Git history,
Python dependency setup, contract check, promoted-wave check, advisory
report-full, and advisory duplicate report to the job log. Outputs remain safe
counts and paths only. Do not upload
raw corpus or snapshot payload artifacts.

Use the exact schedule 17 17 * * 1 (Monday 17:17 UTC, Tuesday 02:17 KST), job
ID document-corpus-lifecycle, ubuntu-latest, timeout-minutes 15,
actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 with
persist-credentials false and fetch-depth 0, and
actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 with Python
3.12. The workflow runs check-contract, check-promoted, check-impacted against
HEAD~1 when present, report-full, and report-duplicates to a temporary runner
path. report-full is the only repository-wide archive/snapshot operation in
Foundation: it exits zero for bounded legacy debt and nonzero for
contract/parser/Git/path/redaction safety failure. The workflow does not run
repository check-archive, archive-ledger, or snapshot-manifest blocking before
Wave D.

- [ ] **Step 4: Integrate existing local/CI owners**

Update check-repo-contracts.sh to invoke the companion and validate the exact
workflow/pre-commit contracts. Update QA recommendation and local gates for
lifecycle contract, manifest, archive, workflow, and generated-data changes.
Register the new script in scripts/README.md.

The repository-contract path always runs check-contract and check-promoted.
When TEMPLATE_GATE_BASE resolves to a commit, it
also runs check-impacted with that exact ref; local execution without the
environment uses HEAD~1 when it resolves and otherwise reports that no
comparison base exists without inventing one.

- [ ] Add script/test/workflow inventory assertions to repo contracts.
- [ ] Add exact trigger, permission, action-SHA, fetch-depth, and command
  assertions for document-corpus-lifecycle.yml.
- [ ] Invoke check-contract and check-promoted unconditionally.
- [ ] Invoke check-impacted only with a verified explicit or HEAD~1 base.
- [ ] Extend the existing pre-commit repo-contract files selector.
- [ ] Route lifecycle surfaces in recommend-qa-gates.sh.
- [ ] Route lifecycle checks in run-local-qa-gates.sh.
- [ ] Register the companion in scripts/README.md.
- [ ] Route tracked-definition and remote-state boundaries in
  github-governance.md.

Do not add a required CI job, modify ci-quality.yml job IDs, or change local
ruleset status checks. The existing repo-contracts job is the pull-request and
push consumer.

- [ ] **Step 5: Run GREEN**

~~~bash
bash -n scripts/validation/check-repo-contracts.sh scripts/validation/recommend-qa-gates.sh scripts/validation/run-local-qa-gates.sh
python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v
python3 -m unittest tests.validation.test_document_metadata -v
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-impacted --base-ref e00e1483
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/recommend-qa-gates.sh
git diff --check
~~~

Expected: syntax and tests pass; repo contracts report failures=0; recommended
gates include lifecycle validation for each owned changed surface.

- [ ] **Step 6: Commit, then review**

Run graphify update ., record implementer self-review, and commit:

~~~bash
git add .github/workflows/document-corpus-lifecycle.yml .pre-commit-config.yaml scripts/README.md scripts/validation/check-repo-contracts.sh scripts/validation/recommend-qa-gates.sh scripts/validation/run-local-qa-gates.sh docs/00.agent-governance/rules/github-governance.md docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md
git commit -m "ci(docs): route corpus lifecycle governance checks"
~~~

Review the committed range with fresh specification and quality reviewers.
Commit fixes separately and obtain both re-reviews before Task 5.

## Task 5: Foundation Manifest and Generated Evidence

**Files:**

- Add docs/90.references/data/governance/document-corpus-lifecycle/README.md.
- Add docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml.
- Add docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md.
- Modify docs/99.templates/support/document-corpus-migration-contract.yaml.
- Modify docs/90.references/data/governance/README.md.
- Modify docs/90.references/data/README.md.
- Modify docs/90.references/README.md.
- Modify docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md.
- Modify docs/90.references/data/security/security-automation-readiness.md.
- Modify docs/90.references/data/governance/audit-implementation-matrix.md.
- Modify docs/90.references/llm-wiki/llm-wiki-index.md.
- Modify docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md.
- Modify docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md.
- Modify docs/00.agent-governance/memory/progress.md.

Foundation does not publish an archive ledger or snapshot manifest. Task 2
proves both deterministic write/check interfaces in temporary fixtures; Wave D
publishes their first canonical Stage 98 outputs after remediating existing
tombstones. The current hand-maintained Stage 98 ledger remains transitional.

- [ ] **Step 1: Generate the Foundation skeleton from the immutable baseline**

~~~bash
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode generate-manifest \
  --wave foundation \
  --base-ref e00e1483 \
  --output _workspace/repo-support/document-corpus-lifecycle/foundation.yaml
~~~

Expected: every Foundation-selected baseline path appears exactly once in
stable order, new implementation outputs are listed as declared outputs rather
than fictional baseline sources, and every review verdict is pending.

- [ ] **Step 2: Classify without inventing evidence**

Review each row against the actual diff and Git history. Use migrate or
preserve for Foundation-owned existing documents; no merge, archive, or delete
is expected in Foundation. Record exact active consumers, source paths,
commands, preservation decision, and rollback commit range. Keep YAML null for
inapplicable values; never use N/A.

Promote the reviewed manifest and generator-owned summary into the Stage 90
governance namespace. README files add routing only.

- [ ] **Step 3: Prove deterministic generation and validation**

~~~bash
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-manifest \
  --wave foundation \
  --manifest docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode generate-summary \
  --manifest docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml \
  --output docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-summary \
  --manifest docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml \
  --output docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md
~~~

Expected: schema, coverage, conditions, and write/check equality pass. Review
verdicts remain pending until independent reviews complete, so enforcement is
advisory at this step.

- [ ] **Step 4: Stage authored Foundation namespace paths**

Stage the authored namespace README and reviewed manifest, but not the
generated summary:

~~~bash
git add docs/90.references/data/governance/document-corpus-lifecycle/README.md docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
~~~

The summary remains untracked until after the authored baseline commit, so it
cannot leak into that logical unit.

- [ ] **Step 5: Commit advisory evidence, review, and promote**

Commit authored routing and the advisory manifest with exact paths:

~~~bash
git add docs/90.references/README.md docs/90.references/data/README.md docs/90.references/data/governance/README.md docs/90.references/data/governance/document-corpus-lifecycle/README.md docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(data): publish corpus lifecycle foundation baseline"
~~~

Stage the generated summary so Git-backed index generators see it, then
regenerate downstream owners in order. The metadata inventory is last because
the new tracked evidence changes its counts:

~~~bash
git add docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
python3 scripts/validation/check-document-metadata.py \
  --mode report \
  --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
~~~

Run every owner in check mode, then commit generated fallout separately:

~~~bash
git add docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md docs/90.references/data/security/security-automation-readiness.md docs/90.references/data/governance/audit-implementation-matrix.md docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
git commit -m "docs(generated): refresh corpus lifecycle evidence"
~~~

Obtain independent Task 5 specification and quality reviews of both commits.
After PASS/APPROVED, update the manifest review objects to pass, set the
manifest enforcement field to blocking, set Foundation manifest_path to
docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml,
set Foundation enforcement to blocking in the migration registry, record the review messages
in the Task, regenerate the summary, and create the promotion commit:

~~~bash
git add docs/99.templates/support/document-corpus-migration-contract.yaml docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md
git commit -m "docs(governance): promote corpus lifecycle foundation gate"
~~~

Supply the final manifest hash and promotion commit to both reviewers and
require explicit re-approval before Task 6. Later waves remain advisory.

- [ ] **Step 6: Run GREEN**

~~~bash
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-manifest --wave foundation --manifest docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e00e1483
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
git diff --check
~~~

Expected: all checks pass, Foundation is blocking, future waves are advisory,
and no existing tombstone or broad corpus leaf changed.

## Task 6: Full QA, Controlled Wrapper, and Foundation Closure

**Files:**

- Modify docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md.
- Modify docs/03.specs/README.md.
- Modify docs/04.execution/README.md.
- Modify docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md.
- Modify docs/04.execution/plans/README.md.
- Modify docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md.
- Modify docs/04.execution/tasks/README.md.
- Modify docs/00.agent-governance/memory/progress.md.
- Modify docs/90.references/llm-wiki/llm-wiki-index.md.
- Modify docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md.
- Modify docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md.

- [ ] **Step 1: Run the complete focused and repository suite**

~~~bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v
bash tests/validation/test_run_agent_precommit_all_files.sh
python3 -m py_compile scripts/validation/check-document-metadata.py scripts/validation/check-document-corpus-lifecycle.py
bash -n scripts/validation/check-repo-contracts.sh scripts/validation/recommend-qa-gates.sh scripts/validation/run-local-qa-gates.sh
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e00e1483
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-manifest --wave foundation --manifest docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-impacted --base-ref e00e1483
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
git diff --check
~~~

Expected: all commands exit zero. Full-corpus report may list advisory legacy
debt, but Foundation, parser, contract, path, provenance-safety, and generated
freshness failures are zero.

- [ ] **Step 2: Refresh and corroborate Graphify**

~~~bash
graphify update .
bash scripts/knowledge/report-graphify-health.sh
~~~

Expected: graph refresh completes when available. Advisory health, inferred
cross-root edges, ignored/generated volumes, or unrelated collateral are
recorded and corroborated against tracked source. Do not include unrelated
Graphify collateral in Foundation commits. If unavailable, record the exact
skip in the Task.

- [ ] **Step 3: Obtain whole-branch reviews**

Assign a fresh whole-branch specification reviewer to compare e00e1483..HEAD
against every Spec 131 contract and VAL-131-001 through VAL-131-008. Then assign
a separate whole-branch quality reviewer for correctness, determinism,
maintainability, security/redaction, preservation, workflow least privilege,
rollback, and test quality.

Resolve every Critical and Important finding in separate logical fix commits,
rerun affected tests, and obtain explicit re-review. Record Medium/Minor
findings only when they are genuinely deferred to a named later-wave Spec.

- [ ] **Step 4: Run and record the pre-closure controlled all-files gate**

Commit all reviewed implementation and generated changes, confirm the linked
worktree is clean, then run the exact bounded wrapper:

~~~bash
scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md \
  --allow-prefix .github/workflows/document-corpus-lifecycle.yml \
  --allow-prefix .pre-commit-config.yaml \
  --allow-prefix docs/00.agent-governance/rules \
  --allow-prefix docs/00.agent-governance/memory/progress.md \
  --allow-prefix docs/03.specs/131-document-corpus-lifecycle-migration-foundation \
  --allow-prefix docs/03.specs/README.md \
  --allow-prefix docs/04.execution \
  --allow-prefix docs/90.references/data/governance/document-corpus-lifecycle \
  --allow-prefix docs/90.references/data/governance/audit-implementation-matrix.md \
  --allow-prefix docs/90.references/data/security/security-automation-readiness.md \
  --allow-prefix docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md \
  --allow-prefix docs/90.references/llm-wiki/llm-wiki-index.md \
  --allow-prefix docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md \
  --allow-prefix docs/98.archive/README.md \
  --allow-prefix docs/99.templates/support \
  --allow-prefix docs/99.templates/templates/common \
  --allow-prefix scripts/README.md \
  --allow-prefix scripts/validation/check-document-corpus-lifecycle.py \
  --allow-prefix scripts/validation/check-document-metadata.py \
  --allow-prefix scripts/validation/check-repo-contracts.sh \
  --allow-prefix scripts/validation/recommend-qa-gates.sh \
  --allow-prefix scripts/validation/run-local-qa-gates.sh \
  --allow-prefix tests/validation/test_document_metadata.py \
  --allow-prefix tests/validation/test_document_corpus_lifecycle.py
~~~

Record its exact command, exit status, before path set, after path set,
hook-managed path set, unexpected path set, and disposition in the Task. If
hooks modify an expected path, review and commit that change, rerun affected
checks, and repeat this step from clean. Any unexpected path stops closure.

- [ ] **Step 5: Close statuses, regenerate, and commit closure**

Set Spec 131, this Plan, and the Task to completed only after all checks,
task reviews, whole-branch reviews, and the pre-closure wrapper pass. Record
exact commit hashes and wrapper evidence, update existing Stage 03/04 routing
text and progress memory, regenerate LLM Wiki outputs and the metadata
inventory, and rerun all generator check modes.

Commit only the exact closure paths:

~~~bash
git add docs/00.agent-governance/memory/progress.md docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md docs/03.specs/README.md docs/04.execution/README.md docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md docs/04.execution/tasks/README.md docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
git commit -m "docs(execution): close corpus lifecycle foundation"
~~~

- [ ] **Step 6: Re-run the controlled wrapper on the closure commit**

With the closure commit at HEAD and an empty git status, repeat the exact
Step 4 wrapper command byte-for-byte. This second invocation is the final
all-files gate over the delivered tree. It must exit zero with empty before,
after, changed, and unexpected path sets. Its non-mutating result is included
in the final handoff together with the Task's recorded pre-closure evidence.

- [ ] **Step 7: Final clean verification**

~~~bash
git status --short
git log --oneline --decorate e00e1483..HEAD
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-manifest --wave foundation --manifest docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
git diff --check
~~~

Expected: empty status, logical commit ledger matches Git, final wrapper passed
the closure commit, Foundation manifest is blocking and valid, all
repository/document/generator checks pass, and no later-wave mutation appears
in the diff.

## Verification Plan

### Focused TDD

~~~bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v
bash tests/validation/test_run_agent_precommit_all_files.sh
~~~

### Static and Contract Checks

~~~bash
python3 -m py_compile scripts/validation/check-document-metadata.py scripts/validation/check-document-corpus-lifecycle.py
bash -n scripts/validation/check-repo-contracts.sh scripts/validation/recommend-qa-gates.sh scripts/validation/run-local-qa-gates.sh
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e00e1483
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-manifest --wave foundation --manifest docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-impacted --base-ref e00e1483
bash scripts/validation/check-repo-contracts.sh
~~~

### Documentation and Generated Freshness

~~~bash
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
git diff --check
~~~

### Final Controlled All-Files Gate

Use only scripts/validation/run-agent-precommit-all-files.sh with the exact
tracked Task and allowed prefixes in Task 6. Direct pre-commit all-files
execution is prohibited.

## Risks and Rollback

| Risk | Mitigation | Rollback |
| --- | --- | --- |
| Parallel document schemas drift | Keep type/profile semantics in the existing registry and lifecycle-only semantics in one separate registry; test ownership overlap. | Revert Task 1 contract commit and restore schema version 1. |
| Existing tombstone debt blocks Foundation | Apply v2 changed/new enforcement only to edited/new targets; keep Wave D conversion explicit. | Revert archive profile/checker changes without touching tombstones. |
| Manifest generator invents semantic decisions | Skeletons emit pending/null values and blocking checks require reviewed evidence. | Delete unpromoted repo-support output and revert the affected manifest commit. |
| Git provenance leaks payloads | Use object type/identity/hash probes with redacted diagnostics; never print blob or snapshot bytes. | Revert companion/workflow commit and preserve only safe Task findings. |
| Similarity triggers destructive action | Candidate report has no disposition mutation and destructive rows require two reviews. | Revert the manifest row; no corpus mutation occurs in Foundation. |
| Scheduled workflow blocks on legacy debt | report-full remains advisory; only contract and promoted Foundation scope are blocking. | Revert the workflow commit; local validation remains available. |
| Directory budget blocks current flat Stage 04 | Block only a newly added leaf at the threshold; planned year moves remain Wave C. | Revert budget routing while retaining the tested machine contract. |
| Generator changes unrelated evidence | Run owners in dependency order, inspect path sets, and stage exact paths. | Revert only the generated commit and rerun canonical owners. |
| Wrapper modifies unexpected files | Wrapper fails and records paths before cleanup; no direct all-files command is used. | Inspect, revert only task-owned hook output with approval, then rerun clean. |
| Graphify emits unrelated collateral | Treat it as advisory and corroborate tracked source; stage no unrelated graph files. | Leave graph collateral unstaged or revert only task-generated graph output. |

Every task rollback is its logical commit range in reverse order. Never use git
reset --hard, history rewriting, or --no-verify. A failed later task does not
authorize reverting earlier approved work.

## Approval Gates

- User approval of Spec 131 and this staged Foundation scope is already
  recorded in the conversation and must be copied to the Task evidence.
- The tracked Task evidence shell must exist before Task 1 implementation
  evidence is recorded.
- Each Task 1 through 5 requires fresh implementer self-review, independent
  specification PASS, independent quality APPROVED, remediation, and re-review
  before its logical commit is considered closed.
- Foundation manifest enforcement may change from advisory to blocking only
  after its independent reviews pass.
- Task 6 requires fresh whole-branch specification and quality reviews.
- Existing tombstone migration, snapshot payload creation, broad corpus
  migration, Stage 04 year moves, runtime changes, and remote GitHub mutations
  require their later approved Specs or separate user approval.
- Local merge to main is not part of this Plan. It occurs only after branch
  finishing and explicit user authorization.

## Completion Criteria

- Metadata registry v2 and migration registry contracts are exact,
  non-overlapping, and validated.
- New/changed archive metadata enforces all conditional fields and safe shapes.
- Lifecycle companion tests prove manifest, provenance, snapshot, duplicate,
  retention, budget, deterministic write/check, and safe-diagnostic behavior.
- Human contracts, archive template, Stage 98, and Stage 00 match machine
  semantics without copied policy.
- Existing repo-contracts CI routing remains mandatory; scheduled/manual
  lifecycle workflow is read-only and advisory for legacy debt.
- Foundation manifest covers its baseline selection exactly once, has two
  independent passing verdicts, and is promoted to blocking.
- No broad corpus leaf, existing tombstone, Stage 04 partition, runtime,
  secret, provider-global, or remote setting changed.
- All focused tests, repository contracts, traceability, implementation
  alignment, generators, controlled wrapper, Graphify handling, and final
  clean checks pass.
- Spec, Plan, Task, indexes, progress, manifest, summary, generated outputs,
  review evidence, and logical commit ledger agree.
- Worktree is clean and ready for the finishing-a-development-branch workflow.

## Related Documents

- [Spec 131](../../03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Spec 130](../../03.specs/130-template-contract-system-canonicalization/spec.md)
- [Stage 04 Task evidence](../tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md)
- [Metadata registry](../../99.templates/support/document-metadata-profiles.yaml)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [Lifecycle contract](../../99.templates/support/lifecycle-status.md)
- [Template governance](../../99.templates/support/template-governance.md)
- [Archive stage](../../98.archive/README.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
