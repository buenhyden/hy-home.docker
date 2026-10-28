---
title: "Archive Disposition Dry-Run Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0011"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Archive Disposition Dry-Run Task

## Overview

### Objective

Execute W27: record, per Stage 98 retention unit, whether a Git-history-only
disposition could be approved now and, if not, what blocks it. This Task owns
criterion 22 only. It removes no file, adds no Retention Catalog row or
`archive_authorizations` entry, and does not reopen TSK-0007 criterion 14 or
TSK-0010 criterion 21.

## Inputs and Authorization

The direct user request on 2026-10-29 selected a dry-run before any archive
removal and authorized recording it as a SPEC-0212 Task. The input is published
main `2059b0d572db75f5d6ce907b27a77f813cbdbb68`, equal to the remote ref at the
start of the work, with a clean working tree. The authorization covers this
documentation change, its branch, pull request, and merge through the protected
path. It does not authorize an archived-body edit, a catalog row, a checker
change, or any removal.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0011 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0011 | ready | in-progress | #method |
| SPEC-0212-TSK-0011 | in-progress | completed | #disposition-summary |

### Method

A read-only scratch script grouped every tracked file under
`docs/98.archive/{completed,superseded,retired}/` with the checker's own
`retention_unit()`. It found current Markdown consumers with
`build_document_graph()` over every tracked Markdown file outside those three
classes. Links from `docs/98.archive/README.md` and `retention-catalog.md` are
index entries and were not counted. Machine consumers are tracked non-Markdown
files outside `docs/98.archive/` and `graphify-out/` that name the unit path.
Capture state and holds come from `assessment_lookup()`. A unit is a candidate
only with no current Markdown consumer, no machine consumer, and no hold.
Route records (`tombstones/`, `migrations/`) hold no body and are out of scope.

### Disposition summary

237 units hold 356 files. The corpus checker's `preserved=354` counts
Markdown records only; the two-file difference is non-Markdown payload such as
`retired/90.references/data/0067-foundation/data.yaml`.

| Class | Disposition | Units | Files |
| --- | --- | --- | --- |
| completed | blocked | 22 | 77 |
| completed | captured candidate | 15 | 46 |
| completed | uncaptured candidate | 18 | 22 |
| retired | blocked | 1 | 1 |
| retired | captured candidate | 7 | 9 |
| retired | uncaptured candidate | 141 | 141 |
| superseded | blocked | 1 | 3 |
| superseded | captured candidate | 24 | 47 |
| superseded | uncaptured candidate | 8 | 10 |

### Capture-row gap

`scripts/lib/document_governance/archive_assessments.py` rejects a Current
Assessments row whose unit has no Retention Catalog capture row. The catalog
states that pre-catalog units are not loaded retroactively, and TSK-0010
recorded that adding such rows contradicts that contract. The 167 uncaptured
candidates therefore have no valid Git-history-only route under the current
contract. Opening one is a contract change for the Stage 98 policy owner, not
a step this Task may take.

### Captured candidates

These 46 units (102 files) are the only units a unit-scoped approval could
cover today. An isolated restore with `git archive HEAD` reproduced all 102
files byte for byte, and each unit's catalog `Source` commit and path object
exists.

| Unit | Class | Files |
| --- | --- | --- |
| `completed/03.specs/0184-readme-navigation-and-language-contract/` | completed | 3 |
| `completed/03.specs/0186-document-governance-dead-code-removal/` | completed | 3 |
| `completed/03.specs/0187-document-language-migration/` | completed | 3 |
| `completed/03.specs/0188-compose-host-port-exposure/` | completed | 3 |
| `completed/03.specs/0189-home-classification-and-valkey-key/` | completed | 3 |
| `completed/03.specs/0190-home-classification-remaining/` | completed | 3 |
| `completed/03.specs/0191-backup-valkey-export-timeout/` | completed | 3 |
| `completed/03.specs/0192-backup-and-host-alerting/` | completed | 3 |
| `completed/03.specs/0193-observability-dashboards-signals-and-alerting/` | completed | 3 |
| `completed/03.specs/0194-agent-contract-integration/` | completed | 3 |
| `completed/03.specs/0196-ollama-0-35-decision-model/` | completed | 3 |
| `completed/03.specs/0199-ci-delivery-gate-optimization/` | completed | 3 |
| `completed/03.specs/0200-path-aware-pr-regressions/` | completed | 3 |
| `completed/03.specs/0205-storybook-dependency-refresh/` | completed | 3 |
| `completed/03.specs/0206-shared-storybook-and-docs-mcp/` | completed | 4 |
| `retired/03.specs/0195-agent-native-observations/` | retired | 3 |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/guide.md` | retired | 1 |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/policy.md` | retired | 1 |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/runbook.md` | retired | 1 |
| `retired/05.operations/guides/0017-influxdb.md` | retired | 1 |
| `retired/05.operations/policies/0017-influxdb.md` | retired | 1 |
| `retired/05.operations/runbooks/0017-influxdb.md` | retired | 1 |
| `superseded/02.architecture/decisions/0015-analytics-engine-selection.md` | superseded | 1 |
| `superseded/02.architecture/decisions/0019-data-hardening-and-ha-expansion-strategy.md` | superseded | 1 |
| `superseded/02.architecture/decisions/0033-full-spec-package-preservation.md` | superseded | 1 |
| `superseded/02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md` | superseded | 1 |
| `superseded/02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md` | superseded | 1 |
| `superseded/03.specs/0190-agent-contract-hardening/` | superseded | 12 |
| `superseded/03.specs/0201-home-infrastructure-diagnosis-and-work-design/` | superseded | 4 |
| `superseded/03.specs/0202-development-data-and-lab-isolation/` | superseded | 4 |
| `superseded/03.specs/0203-quality-results-and-isolated-load-testing/` | superseded | 3 |
| `superseded/03.specs/0205-storybook-dependency-refresh/` | superseded | 3 |
| `superseded/03.specs/0240-unseal-backup-exclusion/` | superseded | 3 |
| `superseded/05.operations/catalog/03-security/0016-vault/guide.md` | superseded | 1 |
| `superseded/05.operations/catalog/03-security/0016-vault/policy.md` | superseded | 1 |
| `superseded/05.operations/catalog/03-security/0016-vault/runbook.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0018-ksqldb/guide.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0018-ksqldb/policy.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0018-ksqldb/runbook.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0020-starrocks/guide.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0020-starrocks/policy.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0020-starrocks/runbook.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0023-minio/guide.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0023-minio/policy.md` | superseded | 1 |
| `superseded/05.operations/catalog/04-data/0023-minio/runbook.md` | superseded | 1 |
| `superseded/90.references/research/0081-roadmap/README.md` | superseded | 1 |

### Blocked units

These 24 units stay `retained`. A unit with current links can move only after
its consumers cite a current owner. A machine reference needs its code or test
owner to change first.

| Unit | Files | Current Markdown consumers | Machine consumers | Blocker |
| --- | --- | --- | --- | --- |
| `completed/03.specs/0094-harness-agent-first-engineering/` | 1 | 3 | - | current links |
| `completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/` | 1 | 2 | - | current links |
| `completed/03.specs/0098-standardize-infra-net/` | 1 | 3 | - | current links |
| `completed/03.specs/0156-compose-enablement-model-convergence/` | 3 | 1 | - | current links |
| `completed/03.specs/0158-document-governance-lifecycle-convergence/` | 1 | 10 | - | current links |
| `completed/03.specs/0169-document-lifecycle-convergence/` | 3 | 21 | - | current links |
| `completed/03.specs/0171-compose-sibling-pair-resolution/` | 3 | 1 | - | current links |
| `completed/03.specs/0172-document-contract-convergence/` | 1 | 5 | - | current links |
| `completed/03.specs/0173-governance-qa-surface-convergence/` | 8 | 6 | - | current links |
| `completed/03.specs/0175-governance-knowledge-and-prompt-surface/` | 3 | 1 | - | current links |
| `completed/03.specs/0177-archive-disposition-enforcement/` | 3 | 1 | - | current links |
| `completed/03.specs/0178-archive-occupancy-citation-and-frozen-identity/` | 3 | 1 | - | current links |
| `completed/03.specs/0179-package-disposition-wait-and-task-cancellation/` | 3 | 1 | - | current links |
| `completed/03.specs/0180-home-dev-convergence/` | 10 | 17 | `scripts/lib/document_governance/requirement_recovery.py` | current links; machine reference |
| `completed/03.specs/0181-home-residual-operations/` | 3 | 1 | - | current links |
| `completed/03.specs/0183-operations-role-layout/` | 3 | 1 | - | current links |
| `completed/03.specs/0185-agentic-research-refresh/` | 3 | 4 | - | current links |
| `completed/03.specs/0197-infra-tier-layout/` | 4 | 4 | - | current links |
| `completed/03.specs/0198-operations-documentation-system/` | 9 | 16 | - | current links |
| `completed/03.specs/0201-home-infrastructure-diagnosis-and-work-design/` | 4 | 1 | - | current links |
| `completed/03.specs/0202-development-data-and-lab-isolation/` | 4 | 1 | - | current links |
| `completed/03.specs/0203-quality-results-and-isolated-load-testing/` | 3 | 2 | - | current links |
| `retired/90.references/data/0067-foundation/data.yaml` | 1 | 0 | `scripts/lib/document_governance/archive.py` | machine reference |
| `superseded/03.specs/0172-document-contract-convergence/` | 3 | 0 | `tests/lib/document_governance/test_registry.py` | machine reference |

### Removal prerequisites

A later removal Task must carry, per unit, an `archive_authorizations` entry
with `unit`, `action`, `approved_by`, `approved_at`, `evidence`, and `status`.
The evidence heading must contain the line
`> <owner> approved <action> for <unit> on <date>.`, and the Current Assessments
row must use the same date. No such approval exists for any unit.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unit grouping | 22 | W27 | `retention_unit()` over `git ls-files` payload paths | Main `2059b0d572db75f5d6ce907b27a77f813cbdbb68` | PASS | 237 units, 356 files | required | - |
| Consumer trace | 22 | W27 | `build_document_graph()` plus non-Markdown path search | Same main; Python 3.12.3 | PASS | 24 units blocked by consumers; 0 holds | required | - |
| Capture-row rule | 22 | W27 | Source read of `archive_assessments.py` `_snapshot()` | Same main | PASS | Uncaptured units cannot take an assessment row | required | - |
| Isolated restore | 22 | W27 | `git archive HEAD` into scratch, SHA-256 compare; `git cat-file -e` on each `Source` | Same main; Git 2.43.0 | PASS | 102 of 102 files identical; 46 of 46 sources present | required | - |
| Archive integrity | 22 | W27 | `check-document-corpus-lifecycle.py` | Same main | PASS | 0 violations | required | - |
| Current link regression | 22 | W27 | `check-document-links.py --mode alignment` | Same main | PASS | 0 failures; 1 warning (`historical-links-unrecorded`, 2,870) | required | - |
| Changed document metadata | 22 | W27 | `check-document-metadata.py --mode check-changed --base-ref origin/main` | This branch | PASS | See Review and Completion | required | - |

The script ran from an ignored session scratch directory and is not a durable
artifact; the method above and the Git objects at the named commit reproduce
every count.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 22 | accepted | Unit grouping, Consumer trace, Capture-row rule, Isolated restore, Archive integrity, Current link regression, Changed document metadata | The dry-run names 46 approvable candidates, 167 candidates without a valid route, and 24 blocked units; nothing is removed or authorized. | SPEC-0212 TSK-0011 |

## Review and Completion

This Task completes on the source evidence above. It makes no removal, hosted,
merge, or runtime claim; those are observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Historical link classification Task](tsk-0010-historical-link-classification.md)
