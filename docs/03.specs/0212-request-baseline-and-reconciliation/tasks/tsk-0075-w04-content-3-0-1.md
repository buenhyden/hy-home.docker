---
title: "W04 Content 3.0.1 Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-16"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0075"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-16"
---

# W04 Content 3.0.1 Task

## Scope

### Objective and Parent

Own W136 and criterion 131 under the [Spec](../spec.md) and [Plan](../plan.md).
Review the current Stage 01, 02, 05 and 90 corpus by claim and correct
demonstrated mismatches in the documents that own the meaning.

### Inputs and Authority

The direct 2026-11-16 W04-CONTENT request, revision 3.0.1, authorizes local
source and documentation reconciliation, records of findings, and isolated
synthetic checks. D15, D01 and D03 3.0.1 and the package's settled decisions
govern the comparison. S02–S07 and S27 inform role, source and verification
boundaries. Read-only preflight found a clean local `0013721db`, local and
remote main at `17bbde05a`, and only Renovate PRs 1047 and 1048 open.
[TSK-0068](tsk-0068-w01-contract-3-0-1.md) retains the accepted prerequisite.
[TSK-0074](tsk-0074-w04-lifecycle-3-0-1.md) supplies local draft-boundary evidence.

## Execution Log

### Work Performed

#### Design before implementation

Enumerate all tracked regular files under the four stages, including indexes
and agent guides. Record actual body read ranges and cross-checked claims.
Use parsed identities, links and command paths only as leads for unread bodies.
Keep a temporary per-file inventory and record durable decisions in this Task
and the affected owners. Retain historical observations with their date and
source, and qualify any current conclusion by the observed evidence.

Initial differences include blanket full-profile wording in an acceptance
requirement, an obsolete cancellation projection, and a daily backup
procedure that describes the intended capacity admission as current behavior.
Correct those exact statements using the canonical QA, lifecycle and
implementation contracts. Where implementation does not meet an existing
requirement, carry the obligation to its already named implementation owner.
Do not move it into a weaker requirement. Use existing focused tests for
selected commands and check the affected documents and their references.
Separate synthetic and structural results from host operations and acceptance.
Revert each bounded document correction to restore its former text.

#### Claim Review

The tracked inventory records the purpose, actual read ranges, selected
claims, checked sources, discovered readers and reason for any coverage
limit. It includes indexes and splits generated instructions from authored
prose. Parsed links and command paths identify candidate consumers. A
partial record covers only the claims and read ranges written in that row.

| Stage | Tracked | Partial | Reviewed for stated scope | Generated instructions |
| --- | --- | --- | --- | --- |
| 01 Requirements | 21 | 19 | 1 | 1 |
| 02 Architecture | 62 | 61 | 0 | 1 |
| 05 Operations | 288 | 286 | 1 | 1 |
| 90 References | 33 | 28 | 4 | 1 |
| Total | 404 | 394 | 6 | 4 |

- Stage 01 corrects the acceptance evidence bound for security, network
  segmentation and focused QA. Messaging and Open WebUI requirements now
  distinguish HOME and LAB. The retirement requirement names the typed
  cancellation record and preserves the disposition approval.
- Stage 02 reconciles Compose membership, the Open WebUI configuration
  boundary and the optional ComfyUI and Open Notebook profiles. It specifies
  Loki and Tempo snapshot exclusions from the tracked Restic exclusion list.
  The lifecycle, provider and development-host descriptions separate trusted
  authority, structural checks and any deployment evidence.
- Stage 05 aligns guide, policy, runbook and index routes with applicable
  membership and operator prerequisites. Its backup publications describe
  the export ledger, the two supported SQLite stores and the limits of the
  daily Restic path. The focused QA runbook distinguishes local execution
  from hosted work before either is started. All 116 Guide service
  declarations resolved to services in their tracked Compose files.
- Stage 90 keeps source revisions and historical observations in the
  existing reference owners. It corrects the LAB index path, retirement
  routing and any implication that recorded CI invocations describe present
  coverage.

Keep the accepted W01 contract, the W04 draft boundary and the approved
retirement authority. Keep ordinary recovery and the existing product
changelog parser. A retired document role confers no authority over the
product release process. No Stage 99 template or product source changed.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0075 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0075 | ready | in-progress | #design-before-implementation |

### Blockers and Decisions

Read-only review covers the selected local branch. Live service operation,
credential use, external writes and final transition work lack authorization
under this request. Unread meaning and unevidenced operations remain explicit.
The scheduled Restic jobs still lack shared-memory capacity admission. D-11
remains assigned to W08-MEMORY in the
[existing baseline Task](tsk-0067-w00-delta-gap-closure.md#new-items).
The independent R2 byte cap continues to apply. The procedure now directs
operators to the actual export evidence before describing memory as
recoverable.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Preflight | 131 | W136 | workspace-intake | Local 0013721db, package files, read-only GitHub query | PASS | Clean branch, present design inputs, no W04 PR | required | - |
| Inventory | 131 | W136 | claim and consumer inventory | 404 tracked files in the four stages at 0013721db with candidate overlays | PASS | Claim Review totals and session inventory CSV | required | - |
| Independent content review | 131 | W136 | source readback | Candidate security and network evidence method, messaging, AI membership, backup, lifecycle and reference claims | PASS | Claim Review observations, including applied evidence, membership and recovery corrections | required | - |
| Standalone Open WebUI | 131 | W136 | docker compose config | Synthetic env file, LAB manifest, lab-open-webui profile, Compose 5.6.1 | PASS | One service, one network, local bind, synthetic Ollama and local vector store, 0.561 s | required | - |
| Backup fixtures | 131 | W136 | unittest backup contract, offsite cap and restore classes | Existing synthetic unit inputs for memory export, byte cap and restore | PASS | Seven selected tests, 0.009 s | required | - |
| SQLite export | 131 | W136 | Restic export_sqlite.py | Temporary Grafana and Gatus SQLite WAL stores with committed test data | PASS | Marker and integrity verified, obsolete Open WebUI selector rejected, 0.035 s | required | - |
| Release parser | 131 | W136 | release.py validate --changelog CHANGELOG.md | Current product changelog | PASS | Main changelog format | optional | - |
| Corpus lifecycle | 131 | W136 | check-document-corpus-lifecycle.py --base-ref 0013721db | Candidate before this evidence update | PASS | Zero lifecycle and active occupancy findings | required | - |
| Document links | 131 | W136 | check-document-links.py alignment and language | Candidate before this evidence update, 877 documents and 8,577 links | PASS | Zero failures and warnings, 73.74 s and 22.51 s | required | - |
| Corpus command paths | 131 | W136 | check-document-links.py --mode commands | Candidate before this evidence update, 877 documents | PASS | Zero failures and warnings, 536.42 s, static command paths | required | - |
| Changed runbook command paths | 131 | W136 | document link check_commands | RUN-0004, RUN-0021 and RUN-0081 in the staged candidate | PASS | Zero command path or input findings, 2.50 s | required | - |
| Operations catalog | 131 | W136 | check-operations-catalog.py | Current catalog and affected routing changes | PASS | 26.47 s | required | - |
| Document metadata | 131 | W136 | check-document-metadata.py check-changed | First 36 changed files from 0013721db | PASS | Zero findings and zero overrides, 273.41 s | required | - |
| Focused metadata follow-up | 131 | W136 | check-document-metadata.py check-changed --changed-path | REQ-0003, REQ-0023 and TSK-0075 from 0013721db before recording results | PASS | Three files selected, zero findings and zero overrides, 250.87 s | required | - |
| Gate selection | 131 | W136 | run-ci-gate.py --profile changed --explain and --local-only --explain | Candidate scope and gate definitions | PASS | Selection observed. These invocations execute no gate leaves. | optional | - |

### Resolution Links

The baseline and candidate parsed the same 404 Markdown documents using
MarkdownIt, with file reads outside the timer and 35 candidate documents
changed. The three-run median was 3.302 seconds for each input. The timing
covers document parsing only.

The backup fixture command was
`.venv/bin/python -m unittest tests.validation.test_memory_backup_contract.BackupContractTests tests.validation.test_restic_offsite_cap.CapContractTests tests.validation.test_restic_offsite_artifact.RestoreContractTests`.
The Compose result used `docker compose --env-file` with a temporary file,
`-f labs/open-webui/docker-compose.yml --profile lab-open-webui config --format json`
and an otherwise empty environment except PATH. Only the rendered
configuration was read. The documented host backup and restore procedures
were not run.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 131 | pending | - | Owner decision after review and verification | @buenhyden |

### Remaining Conditions

Remaining prose in the partial records, actual hosted checks and any live
deployment, login, recovery, listener denial or latency claims require
separate evidence. Owner acceptance remains pending.

## Handoff

### Promotion Receipt

For W136 and criterion 131, the same logical change as this Task corrects
35 documents across the four stages listed in Claim Review. The
catalog, linked readers and affected runbook command paths were checked.
The criterion decision remains pending and the remaining obligations are
listed above.

### Next Owner

The implementer owns W136 follow-up on claims outside the recorded review
ranges. W08-MEMORY owns D-11. The owner decides criterion 131.
