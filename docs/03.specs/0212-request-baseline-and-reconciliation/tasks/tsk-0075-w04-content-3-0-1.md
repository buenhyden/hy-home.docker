---
title: "W04 Content 3.0.1 Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-18"
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
The direct continuation request retains W136 and criterion 131, using
the clean local `ddf416bdf` on `codex/w04-content`. Read-only remote
inspection again found main at `17bbde05a` and open PRs 1047 and 1048.

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
| SPEC-0212-TSK-0075 | in-progress | completed | #criterion-decisions |

#### Continuation design

D15, D01 and D03 at 3.0.1 still govern this slice. The prior change retained
the accepted contract and passed local document and catalog checks, but
route and dependency descriptions that consume the moved services can
still report the former topology. Verify the unchanged baseline again with
the catalog and commit diff, then independently compare remaining prose
against tracked configuration and approved direction by document family.
Correct corroborated discrepancies in the description or operating
procedure that owns each claim. Preserve historical decision text and
keep each implementation gap visible with its actual owner. Replace
individual claims in place to keep identifiers, links and reader contracts
stable. Revert each bounded change to recover its previous wording.
Use focused metadata, command-path, synthetic configuration and link
checks on the affected surfaces. Leave claims that require external or
live observations explicitly open.

#### Continuation findings

- Stage 01 reviewed the verification methods of 18 Requirement packages
  against current Spec citations and selected acceptance authorities.
  REQ-0004, REQ-0011, REQ-0012, REQ-0024 and REQ-0027 now distinguish the
  required observations from source review, migration or candidate evidence,
  with the existing requirement and acceptance roles preserved.
- Stage 02 compared 17 bounded scopes and corrected eight Descriptions.
  Kafka, Open WebUI and other optional services now distinguish the current
  topology, route controls, state ownership and approved later changes.
  The descriptions point to the current ADR-0062 decisions. Keep ADR-0059
  as the accepted historical decision text under the Stage 02 authoring
  rules and use ADR-0062 for the later affected deployment choices.
- Stage 05 reviewed 13 selected Guide and Policy scopes and recorded
  68 review entries across 57 Runbook, index and incident paths. A source
  scan over 98 runbook and incident documents resolved 176 literal
  standalone Compose selectors in the 52 documents with comparable input.
  This slice corrected 18 Stage 05 paths, including three navigation indexes.
  Candidate promotion manifests for Kafka and OpenSearch carry no approval
  to replace a HOME service. LAB commands name the complete Compose target
  and use the environment file for that operation. Open WebUI HOME
  retirement identifies the old container by project and service before a
  write. Locust diagnosis identifies the original lease while its new canary
  requires separately reviewed inputs, a fresh result path and a deadline.
  The storage runbooks distinguish excluded Loki and Tempo object history
  from recovery with a separately acquired, consistent state copy.
- Stage 90 compared bounded prose in 28 files and corrected two members.
  Product release evidence routes through existing owners. The GitHub
  Actions account retains the dated historical cadence and names current
  staged, PR candidate and main-push routes separately.

The continuation inventory keeps the 404 tracked paths, prior coverage and
new scoped records together. It records 390 partial authored paths, 10
reviewed for their stated scopes, and four generated instruction files.
Source, shell and synthetic configuration checks leave actual service
operation and user acceptance open. The accepted W01 contract, product
publishing path and W08-MEMORY handoff are retained.

#### Merged baseline reference follow-up

D15 and D01 3.0.1 govern the two selected current reference sections.
The RES-0002 role index lists publication as a peer of the five current
Operations roles. The RES-0084 timing table delays its historical date
until after entries that read as current. Keep the historical source
values in place and align the index and labels with the current owner.
Use the local link and metadata checks and report the selected scope.
Revert the two in-place reference corrections to undo this unit.

Listed all 54 Stage 01 and Stage 90 tracked paths. Read the QA and
authority clauses of REQ-0010, REQ-0024, REQ-0025 and REQ-0026 and the
Stage 01 index lifecycle guidance. Compared the active coverage table
in RES-0002 with its role and workflow members, and the RES-0084
dated findings with the tracked actions workflow. Other parts of the
404-path corpus retain their earlier partial or generated classification.

#### W04-CONTENT 4.2.0 recheck

The 2026-11-18 W04-CONTENT request read D15, D01, D03 and D25 of the 4.2.0
package against `7a165d018`. D15 adds that completed document currency work
is not rerun: only a confirmed requirement change or consumer mismatch
reopens a sentence or its reference closure, and a full meaning audit belongs
to a baseline or an important contract change. D25 requires each finding to
name its read scope and evidence kind. No attachment disposition targets
W04-CONTENT. No external source was rechecked; the package states the carried
status of S02 to S07, S14, S20, S22 and S27.

Since the reported completion at `ffc3247ce`, the four stages keep the same
404 tracked paths. All 23 commits that touch them are T99 moves to the role
design core and their review fixes, recorded in
[TSK-0081](tsk-0081-t99-role-design-adoption.md). Outside the documents, only
the document governance readers, the provider surface renderer, their tests and
README files changed; no Compose, lab, workflow or operations script that a
Stage 01, 02, 05 or 90 claim describes changed. That form change is the
important contract change, so its consumer closure was checked:

| Closure | Read scope | Finding | Disposition |
| --- | --- | --- | --- |
| Prose naming a section, table or column absent from every current heading or table header | All 404 paths, fenced blocks excluded | Eight names in RES-0002 members m0009, m0012, m0013, m0015 and m0020, each unchanged since `ffc3247ce` and part of a dated observation of a retired or external source | KEEP |
| Prose naming one of the 50 template headings that T99 removed | All 404 paths | None | KEEP |
| Lifecycle generation, Registry and criterion table claims | REQ-0026, AD-0030, ADR-0048 and every Registry mention in the four stages | REQ-0026 and AD-0030 match the current readers, the lineage section target and the Criterion Acceptance name that `sdlc.md` keeps; ADR-0048 is accepted decision text for generations 5 and 6 | KEEP |
| History recovery, release document reintroduction and always-full checks | Every line added in the four stages since `ffc3247ce` | Only the product changelog step kept above, upstream release notes and dated Stage 90 observations | KEEP |
| Links, anchors and fenced command paths | 887 documents and 8,938 links | No failure or warning | KEEP |

AD-0030 does not describe lifecycle generation 8 or the role design core.
That omission contradicts no claim; governance and Stage 99 own both, and D15
adds no new Description for it. No Stage 01, 02, 05 or 90 document changes.

Every current document keeps one classification. Ten authored paths are
reviewed for their stated scopes. The 390 other authored paths are partial:
outside their recorded ranges they are unreviewed because D15 limits the
meaning audit to a baseline or an important contract change, and the only
such change since then, the T99 form move, passed the closure above. The four
generated instruction files carry no authored claim. A later change to a
claim or its consumer reopens only that closure.

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
| Resume baseline | 131 | W136 | check-operations-catalog.py and git diff HEAD^ HEAD --check | Clean ddf416bdf, local and read-only GitHub state observed | PASS | Catalog exit 0 in 21.55 s, unchanged commit and base | required | - |
| Resume requirement readback | 131 | W136 | compare typed frontmatter, child requirements and traceability | Five changed requirements against ddf416bdf | PASS | Status, identity, substantive Requirements and downstream links preserved, 0.10 s | required | - |
| Resume Kafka LAB | 131 | W136 | docker compose config | Kafka LAB, lab-kafka profile, Compose 5.6.1, synthetic data root and cluster ID plus missing-ID input | PASS | Seven services, internal network, no published ports, missing ID rejected, render 0.51 s | required | - |
| Resume OpenSearch LAB | 131 | W136 | docker compose config --services | Standalone OpenSearch LAB, Compose 5.6.1, synthetic LAB inputs | PASS | Four services; no startup | required | - |
| Resume Locust LAB | 131 | W136 | docker compose config | Locust LAB, lab-locust profile, synthetic scenario and result roots plus missing-path input | PASS | Headless master, terminal job label, no published ports, absent path rejected, render 0.13 s | required | - |
| Resume corpus lifecycle | 131 | W136 | check-document-corpus-lifecycle.py --base-ref ddf416bdf | Continuation candidate, no lifecycle transition | PASS | Zero lifecycle and active occupancy findings, 159.52 s | required | - |
| Resume corpus alignment | 131 | W136 | check-document-links.py --mode alignment | Continuation candidate before late prose and evidence rows | PASS | 877 documents, 8,593 links, zero failures or warnings, 82.71 s | required | - |
| Resume operations catalog | 131 | W136 | check-operations-catalog.py | Continuation catalog and routing changes | PASS | Exit 0, 28.17 s | required | - |
| Resume runbook paths | 131 | W136 | check_commands and bash -n on changed fences | Nine changed runbook and index paths before Locust was added | PASS | Zero path findings, six changed Bash blocks, 7.93 s | required | - |
| Resume metadata | 131 | W136 | check-document-metadata.py --mode check-changed --base-ref ddf416bdf | 33 changed paths before the Locust runbook was added | PASS | Zero violations and overrides, 260.13 s | required | - |
| Resume late documents | 131 | W136 | registered frontmatter, body, language and link checks | AD-0002, AD-0020, RES-0084-m0001 and initial RUN-0062 continuation text | PASS | Four contracts, 38 links and zero findings, 2.54 s | required | - |
| Resume Locust canary input | 131 | W136 | scoped body, command and synthetic Compose checks | Final RUN-0062 with separate original and canary inputs | PASS | Five Bash blocks, six links, no path findings; synthetic rendered bounds and fresh result bind in 0.123 s | required | - |
| Resume inventory | 131 | W136 | tracked inventory and per-file scopes | 404 tracked and 33 changed corpus paths against ddf416bdf | PASS | Exact path sets and 116 declared Guide services verified | required | - |
| Resume independent review | 131 | W136 | requirements and high-impact diff readback | 34-path continuation from ddf416bdf, selected route, procedure, authority and source changes | PASS | CI cadence, LAB OIDC diagram and separate Locust canary input corrected and re-reviewed | required | - |
| 4.2.0 claim closure | 131 | W136 | source readback | Section, heading, Registry, generation and conflicting phrase scans over the 404 paths at `7a165d018` against `ffc3247ce` | PASS | W04-CONTENT 4.2.0 recheck table, no stage change needed | required | - |
| 4.2.0 links and commands | 131 | W136 | check-document-links.py alignment and commands | `7a165d018`, 887 documents and 8,938 links | PASS | Zero failures and warnings, exit 0, 29.49 s and 16.12 s | required | - |
| 4.2.0 operations catalog | 131 | W136 | check-operations-catalog.py | `7a165d018` | PASS | Exit 0, 21.02 s | required | - |

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

On continuation, the MarkdownIt comparison used the same 404 tracked paths
at `ddf416bdf` and the 33-document corpus update, alternating three timed
parses per input with file reads excluded. The medians were 3.158 seconds
and 3.271 seconds. This records local measurement variation and tree parsing
cost only.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 131 | accepted | Resume inventory, Resume metadata, Resume independent review | Owner @buenhyden accepted on 2026-11-16 in this chat; the unread prose review stays a W04-CONTENT condition | @buenhyden |

### Remaining Conditions

None for W136. The owner accepted criterion 131 on 2026-11-16 and every
required row passed. Prose outside the recorded ranges stays classified as
unreviewed with the reason above. Hosted checks and any live deployment,
login, recovery, listener denial or latency claims need their own evidence
and were not run.

## Handoff

### Promotion Receipt

For W136 and criterion 131, the same logical change as this Task corrects
35 documents across the four stages listed in Claim Review. The
catalog, linked readers and affected runbook command paths were checked.
The continuation from `ddf416bdf` corrects 33 corpus documents and records
the added checks above. Each affected stage retains authority for its own
claims.
The 4.2.0 recheck changed no corpus document. The owner accepted criterion 131.

### Next Owner

None for W136. A later claim or consumer change reopens only its closure.
W08-MEMORY owns D-11.
