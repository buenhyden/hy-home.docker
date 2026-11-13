---
title: "Hermes Provenance, Trust and Export Task"
version: "0.1.2"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0050"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-03"
---

# Hermes Provenance, Trust and Export Task

## Scope

### Objective and Parent

#### Objective

Implement the approved local P11 source and owned-isolation repair. New direct
reports require collector-issued source receipts; direct submission and Attester
replay preserve immutable bytes and fail closed on uncertain or corrupt state.
This Task documents the current Hermes trust boundaries without converting
synthetic checks or history into operational acceptance.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Historical Hermes Task](../../0204-service-integration-security-and-operations/tasks/tsk-0022-hermes-blog-ingestion.md)
- [n8n Runbook](../../../05.operations/runbooks/08-workflows-and-automation/0053-n8n.md)
- [Hermes workload README](../../../../infra/07-workflow/n8n/workloads/hermes-blog-ingestion/README.md)

### Inputs and Authority

The observed clean starting revision was
`e3a43821c6c1ba1a78aeee11f7070e57caa79aaf`. Local source, synthetic fixtures,
cached-image isolated tests and owned backup/restore targets are authorized.
Actual article collection, service restart, credential use, Windows B delivery,
external repositories and remote CI are not. The dependencies package was not
provided, so this Task does not claim a complete historical crosscheck.

SPEC-0204-TSK-0022 retains its historical detailed record. In particular, its
dated Gateway deployment, independent host Attester timer, two Export 1.0
Windows ACKs and bounded online-backup observations are reusable only at their
recorded actor, version and environment scope. Export 2.0 is the current
selected contract at Blog-data revision
`c05e5b88bae36ae8f5421fd27beada9b1d596a19` (schema 4); a new real Windows B
ACK, scheduled delivery and independent operational restore are not run here.

## Execution Log

### Work Performed

#### Single-writer leases

| Scope | Single writer | Independent review | Boundary |
| --- | --- | --- | --- |
| P11 source, direct outbox helper and Attester replay | P11 application writer | code and security reviewers | Hermes workload code and its tests only |
| QA, cache-only isolation and offline gate | P11 QA/CI writer | independent QA reviewer | owned fixtures, gate registration and test evidence |
| Current Task, SPEC/Plan, current SPEC-0204 wording, RUN-0053, workload README and DATA-0096 | P11 documentation writer | independent document reviewer | public documentation and ledger only |

The live Traefik dynamic route files are observation-only in this Task. Their
current consumer contract may be documented, but no watched route is modified.
The listed writer roles allocate a repository path; they do not grant operating
authority, credential access or Windows B authority.

`SPEC-0212-TSK-0050` is the P11 acceptance coordinator for this Task's local
source and isolated evidence only; the P11 documentation writer is only the
public-file integrator. The actual raw-source data owner, operational service
acceptor and Windows B receiver/ACK acceptor are **UNASSIGNED**. They
must be named by the service/data owners before activation; each must confirm
its own authorization, retention or delivery scope, and rollback/recovery
conditions. Until then, the documented source rollback procedure is only a
restart-preparation contract, no operational acceptance may be inferred, and
the relevant lanes remain `NOT_RUN`.

The current source interface is
`collect_research_source({item_id, source_url})` followed by
`submit_research_report({payload, source_receipts})`. The collector returns a
receipt identifier, final URL, fetch time, body digest, local call identifier
and normalized text only after persisting source bytes; `payload` currently has
schema version `1.0` and receipt IDs are 32 hex. An absent scheduler instant
rejects before network access. Exact source/QA tests, not this prose, own
validation of that wire contract.

The plugin rollback contract stops the service, preserves the current directory,
restores the exact source-only backup file set into an empty mode-0700 target
without an overlay, then runs `doctor`; restart remains separately approved.
It is a source contract only and was not exercised against an operating plugin.

#### Five independent trust boundaries

| Boundary | Current evidence | Decision and residual |
| --- | --- | --- |
| Direct Hermes to n8n webhook | Local receipt-bound request construction and isolated ingress checks | A collector receipt is audit/trace binding only: the Hermes tool and receipt use the same UID, so a compromised or non-cooperative tool can alter both bytes and digest. It is not producer authentication, independent Attestation, a real Cron submission or a durable Gateway receipt. |
| Publisher Ed25519 | Existing publisher key registry remains empty | BLOCKED for Publisher dispatch; no key registration or alternate signature path is created. |
| Independent Attester | Historical host timer/Attester observation is preserved; local replay code is separately tested | An Attester result does not authenticate a Publisher and local tests do not re-run its operation. |
| Gateway durable receipt | Exact response validation and immutable local request binding are tested locally | Gateway persistence is not final Windows delivery; server-side source binding remains Blog-data work. |
| Windows B Export/ACK | Two Export 1.0 ACKs are historical receipts; Export 2.0 is selected | A new Export 2.0 receive/ACK, scheduling and recovery acknowledgement are NOT_RUN. |

Collector-normalized text and source content remain untrusted data. They cannot
expand a tool's destination, file, credential or execution authority. Raw page
byte retention, data ownership and retention duration are operational inputs
for the data owner; this Task records only the source-level receipt contract.
The source limit is at most 2 MiB per item and 100 items per run, but that
bounded size is not a retention/activation decision and no public source was
collected in this Task.

The reused fetch path bounds socket read and redirect work but cannot promise a
stdlib `getaddrinfo` DNS lookup timeout. The Attester now counts terminal
reports separately so an active report after 100 terminal ones is exercised in
source regression; nevertheless it scans at most ten pages per run and stores
no server cursor checkpoint. More than ten pages of persistent local-terminal
records can still delay later reports until Gateway compaction or operator
action. Both concerns need an operational observation/cursor contract before
activation; neither is silently treated as a successful timeout or starvation
control.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Historical Export 1.0 ACK record | 100 | W105 | Scoped receipt readback | SPEC-0204-TSK-0022 dated records | PASS | Historical scope retained without re-running operation; it does not prove current Export 2.0 delivery. | required | - |
| Historical backup record | 101 | W106 | Scoped receipt readback | SPEC-0204-TSK-0022 dated records | PASS | The dated bounded online-backup observation is retained without re-running an operational restore. | required | - |
| Security-reviewed plugin source identity | 102 | W107 | Independent security re-review | Final `hermes-plugin/tools.py` candidate | PASS | Security reviewer recorded `tools.py` SHA-256 `b6161bcbe4240caa75248964bb234ce8723abff278b04db68472b94a2e4cad77`; no open Critical/Important finding. This identifies reviewed source only, not an installed release or operation. | required | - |
| Collector receipt and source-quality contract | 98 | W103 | Pre-freeze P11 workload suite | Owned synthetic source endpoint and local source | PASS | Initial direct-plugin RED reproduced five failures; before the final stale-clock repair, `python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` passed 395/395 in 22.598 s. Its then-pending source-frozen whole-suite/coverage rerun is historical context, resolved by the later final QA and coverage rows below. Actual collection, Hermes SDK Call-ID binding and raw-source lifecycle remain separate. | required | - |
| Direct receipt/outbox durability contract | 99 | W104 | Pre-freeze workload suite and concurrent-submit regression | Owned direct-record fixture and local source | PASS | The pre-freeze 395/395 suite covers direct receipt/outbox negative cases. The later stale-clock race fix was reproduced 100/100 under its concurrent-submit regression and independently security re-reviewed PASS; its then-pending source-frozen whole-suite/coverage rerun is historical context, resolved by later final QA and coverage rows. It does not prove Gateway-side source binding or durable live receipt. | required | - |
| Export 2.0 isolated contract | 100 | W105 | Cache-only upgrade/restore | Cached local images, `--network none --pull never`, owned volumes and synthetic receiver | PASS | E2E observed 11/11 checks: schema 3 backup → schema 4 separate-volume restore and ready Export. Held delivery, ACK, collector, Windows B and operational restore were not proved. A cache image ID is not OCI provenance or source binding. | required | - |
| Final cache-only isolated E2E | 100 | W105 | Synthetic collection through plugin/TLS adapter/n8n/Gateway/Attester/Export/ACK plus online snapshots and separate restore | Final app/QA frozen source, cached artifacts, owned isolated resources and synthetic receiver | PASS | P11 E2E agent, environment date 2026-11-03, session 22593: exit 0; 55 PASS/0 FAIL. It exercised synthetic collector → plugin → isolated n8n/Gateway → Attester → Export 2 → synthetic ACK, then separate source/outbox/Attester/Gateway online-backup restore with held/acknowledged state, duplicate prevention and interruption/restart. Tool chunks were collector `929e3b`, Attester `405216`, ACK/restore `76b33b`, Gateway restore `1ce23c`, result `a12522`, exit `ac62b2`; no UTC/KST execution time or separate retained raw-log file exists. Thirteen core source fingerprints plus seven workflow/fixture/Compose/route inputs matched before/after; each owned-resource label ended at 0. Windows B, operation, Queue, production TLS and artifact provenance remain NOT_RUN. | required | - |
| Isolated ingress first attempt | 99 | W104 | Cached n8n ingress E2E | Owned n8n fixture and external-rejection probe | ERROR | First attempt passed nine n8n checks, then hung because the external-rejection probe did not consume the Node response body. The owned n8n process was stopped (exit 137); a separate three-second probe observed 403. This pre-fix failure is retained; the later final cache-only E2E is recorded separately and does not turn this historical observation into a Windows or Queue acceptance. | required | - |
| Attester replay and owned SQLite restore | 101 | W106 | P11 workload suite and cache-only upgrade/restore | Owned temporary database, cached image and fixture records | PASS | QA workload suite passed 384/384; E2E supplied the schema 3→4 independent-volume receipt. Attester operational replay and production restore remain separate. | required | - |
| P11 gate registration and local plan | 102 | W107 | Offline gate, public validator and manifest contracts | Current P11 source and registered local/PR/push/workflow-dispatch contexts | PASS | CI writer reports 14/14 gate/P03-P11 contract tests, 61/61 workflow/GitHub tests, 68/68 plan/P03-P11 tests, workflow checker (5 workflows/7 jobs/9 actions), direct manifest PASS and 91% gate-line trace coverage. This registers a local gate; it is not remote CI. | required | - |
| Broad P11 gate baseline | 102 | W107 | Full offline suite | Current pre-freeze P11 source | ERROR | At that historical pre-fix point, the full gate reached 393 tests but had one `os.chown` supplementary gid 65534 `EINVAL` error and three loopback skips. An earlier 353-test run also had five pre-fix direct-delivery failures. Focused KeyCustody rerun passed 13/13. Its then-pending root-cause investigation and final rerun are resolved only by the separately recorded final host gate; focused PASS does not rewrite this result. | required | - |
| Independent security baseline | 102 | W107 | `python3 scripts/validation/check-p11-hermes.py` | Pre-freeze security-review source | ERROR | 389 tests: one concurrent direct-submit failure (focused rerun passed) plus a KeyCustody foreign-gid `chown` `EINVAL` error and three skips. This result is retained separately from later focused packets. | required | - |
| Pre-format host offline gate | 102 | W107 | `rtk python3 scripts/validation/check-p11-hermes.py` and cache-only contract | Post-review host namespace source | PASS | P11 CI writer, environment date 2026-11-03: before the later byte-only format repair, `rtk python3 scripts/validation/check-p11-hermes.py` exited 0 with 415 Python tests/0 skips; its associated cache-only contract was 1/1 PASS in 26.529 s, focused CI checks 81 PASS and gate coverage 100%. Exact wall-clock time, the cache-contract invocation detail and a retained raw stdout/stderr log are not available in this historical record. The restricted-sandbox gid constraint remains distinct; remote CI and operation are not run. | required | - |
| DATA-0096 receipt-preserving refresh | 102 | W107 | `workspace-inventory scan --connections` then `validate` | 98 retained public review records and all seven canonical curation sections from the prior public ledger | PASS | Earlier 42,102/42,102 and then 42,091/42,091 are separate observations. The current scan records files 42,094/42,094; whole review 6/2,337; partial 77/2,337; render 0/17; runtime/restore 0/112; validate reported metadata consistency only. The 42,102→42,091 difference was only `excluded.generated` (38,748 → 38,737). Comparing the 42,091 index observation with 42,094 finds no public file-list path addition/removal; excluded aggregates changed `generated` 38,737→38,741 and `private` 241→240, while binary/code/config/document stayed 35/132/482/120. Exact paths and either change cause remain unconfirmed. Compare invalidated 48 changed review inputs, including RUN-0053: its prior PARTIAL receipt is now `STALE`, explaining 6+78 → 6+77 without loss of the retained record. HEAD-to-current curation counts match 70 requirements, 8 reuse, 109 ownership, 70 research, 13 tiers, 8 learning domains and 65 handoffs. Generated `data.yaml` is excluded from its own recursive fingerprint. | required | - |
| Actual operation boundary | 102 | W107 | Authorized-operation boundary | Current Task authorization | NOT_RUN | Actual Hermes collection, service operation, credentials, Windows B ACK and remote CI are explicitly outside this Task; no local result substitutes for these lanes. | required | - |
| New Python execution coverage | 102 | W107 | `rtk python3 -m trace --count --missing --summary --coverdir /tmp/tmp.cEVsk5sn88 --module unittest` followed by `tests/test_source_collection.py`, `test_research_report_plugin.py`, `test_attester.py`, `test_source_fetch.py`, `test_plugin_bundle.py`, `test_outbox.py` under the Hermes workload test directory | Post-review source; source collection, research-report plugin, Attester, source fetch, plugin bundle and outbox tests | PASS | P11 QA writer, restricted local sandbox (uid/gid 1000/1000; groups 1000/65534; `/usr/bin/python3` 3.12.3), environment date 2026-11-03: exit 0; 156 tests in 10.265 s, `OK`. Changed/new execution-line readings: gateway receipt 97%, source collection 92%, Attester 92%, private records 92%, source fetch 93% and tools 87%; all exceed 80%. Result files were observed at `/tmp/tmp.cEVsk5sn88/*.cover`; their 2026-11-03 09:59:15 +0900 mtime is not an execution timestamp. No raw stdout/stderr log or exact start/end wall-clock time was retained. This is stdlib trace over named changed surfaces, not repository-wide coverage. | required | - |
| Final restricted QA | 102 | W107 | `python3 scripts/validation/check-p11-hermes.py`, Ruff and compile checks | Restricted environment with mapped supplemental gid | PASS | P11 QA writer, environment date 2026-11-03: exit 0; 400 tests ran: 396 passed and four skipped. The loopback-TLS `setUpClass` non-run cases remain separately counted. Same-key concurrency regression passed 100/100; malformed `'-' * 36` receipt IDs are rejected while real UUIDs succeed; `content_encoding` fetch failure is exercised; `ruff check`, `ruff format --check` and `compileall` passed. External-namespace final confirmation remains CI-owned. | required | - |
| Pre-hook document contract checks | 102 | W107 | Metadata, corpus lifecycle and links alignment | Changed P11 documentation before later hook, format and evidence additions | PASS | P11 coordinator, environment date 2026-11-03: `rtk python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e3a43821c6c1ba1a78aeee11f7070e57caa79aaf` exited 0 (selected 7, violations 0); `rtk python3 scripts/validation/check-document-corpus-lifecycle.py` exited 0 (violations 0, archive violations 0); `rtk python3 scripts/validation/check-document-links.py --mode alignment` exited 0 (failures 0, warning 1 for historical link 232). The corpus run preceded the final RUN-0053 link-only correction, which is lifecycle-neutral; links alignment ran after it. Exact wall-clock times and retained raw logs are unavailable. Independent code, security and document reviews were APPROVED. Later hook, format and Task-evidence additions mean a final current-Task-byte document check must be recorded separately. | required | - |
| Initial commit-hook formatting result | 102 | W107 | Commit hook formatting | Normal commit hook on final candidate | ERROR | The first normal commit-hook attempt found one `ruff format --check` failure: `gateway_receipt.py` would reformat. Shellcheck, YAML, Markdown and secret checks passed. This is retained as a formatting failure; it is not a functional, security or operational result. | required | - |
| Gateway receipt format correction | 102 | W107 | Commit hook formatting | `gateway_receipt.py` only | PASS | The application writer formatted only `gateway_receipt.py`. Byte SHA changed from `189b3612bf02c8476b1d899402bec3b9c86c48d7e3bfb05374ec7d2567fa61d8` to `65c71aa46b408eb13f33aba9e832e245e0a6e6767061a567c50b1da685bd3ba3`; before/after AST SHA remained `be00426a0b3b95ddb4bcbecfc357190a4457edc0cbb9fac214087d2bf0887db3`, and adapter tests passed 15/15. This resolves the initial hook-format observation only; it does not re-run the full P11 gate or retroactively bind pre-format E2E to the new bytes. | required | Initial commit-hook formatting result |
| Post-format P11 gate | 102 | W107 | Post-format P11 gate | Current formatted gateway-receipt bytes | NOT_RUN | The final cache-only E2E 55-PASS observation predates the byte-format correction. AST identity is recorded, but the required post-format full gate remains pending and must be recorded separately before local final acceptance; it does not affect operational or remote `NOT_RUN` lanes. | required | - |
| Post-format P11 gate result | 102 | W107 | Post-format P11 gate | Current formatted gateway-receipt bytes; host group namespace | PASS | P11 CI writer (`/root/p11_ci`), 2026-11-03T10:49:23+09:00 to 10:49:56+09:00, ran `rtk python3 scripts/validation/check-p11-hermes.py` in `/home/hyunyoun/data/hy-home.docker`; exit 0. It reported 415 Python tests in 24.009 s, `OK`, 0 skips, then ran its integrated `e2e-cache-contract.sh` step and reported cache-only E2E contract 1/1 PASS (tool wall time 24.515 s). Evidence is session execution output only; the UI output was truncated and no durable raw log/result path exists. This resolves the pending post-format local gate only, not actual Queue, operation, Windows ACK or remote CI. | required | Post-format P11 gate |
| Same-UID and recovery handoff | 102 | W107 | Residual handoff | Operator/data-owner/external receiver boundaries | NOT_RUN | File guards do not prove resistance to a compromised Hermes UID; raw-source ownership/retention, legacy/mixed Attester recovery and live route reload remain separate. Mixed or uncertain records must not auto-resend. Watched routes are read/fixture-only here. | required | - |
| DNS lookup deadline | 98 | W103 | Operational residual | Fetch/runtime operator | NOT_RUN | Socket/redirect deadline does not bound stdlib `getaddrinfo`; resume only with a separately accepted operational DNS-timeout observation. | required | - |
| Attester queue fairness | 101 | W106 | Operational residual | Attester operator and Blog-data provider | NOT_RUN | The terminal-count regression covers 100 terminal then one active report, but the fixed ten-pages/run reader has no Blog-data stable cursor, terminal ACK or compaction contract. Persistent local-terminal records beyond that window can indefinitely delay later reports. Resume only with a versioned provider cursor/terminal-ack/compaction contract and an observed over-window fairness test; do not claim this fixed. | required | - |

### Resolution Links

None: nothing was recorded here before this Task moved to the common form.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 98 | pending | Collector receipt and source-quality contract, DNS lookup deadline | Local workload proof passes; external Hermes SDK Call-ID linkage, actual collection and a bounded DNS lookup remain separate handoffs. | SPEC-0212 TSK-0050 |
| 99 | pending | Direct receipt/outbox durability contract, Isolated ingress first attempt | Local negative-path proof passes; Gateway-side binding and live durable receipt remain separate. The retained pre-fix ingress ERROR does not become Queue acceptance. | SPEC-0212 TSK-0050 |
| 100 | accepted | Historical Export 1.0 ACK record, Export 2.0 isolated contract, Final cache-only isolated E2E | Export 1.0 history is reused and cache-only Export 2.0 passes; new Export 2.0 Windows delivery remains unaccepted. Owner @buenhyden accepted on 2026-11-06. | SPEC-0212 TSK-0050 / Windows B owner |
| 101 | pending | Historical backup record, Attester replay and owned SQLite restore, Attester queue fairness | Local source and independent-volume proof pass; operational Attester replay/restore and fairness stay separate. | SPEC-0212 TSK-0050 |
| 102 | pending | Security-reviewed plugin source identity, P11 gate registration and local plan, Broad P11 gate baseline, Independent security baseline, Pre-format host offline gate, DATA-0096 receipt-preserving refresh, Actual operation boundary, New Python execution coverage, Final restricted QA, Pre-hook document contract checks, Initial commit-hook formatting result, Gateway receipt format correction, Post-format P11 gate, Post-format P11 gate result, Same-UID and recovery handoff | The post-format host gate and cache-only contract pass; the final cache-only E2E is recorded above. Restricted-sandbox gid mapping is environment-specific. Live route, actual Queue execution, external ownership and operations remain separate. | SPEC-0212 TSK-0050 |

### Remaining Conditions

After source freeze, run the registered P11 offline gate and the focused source,
security and document checks. Record coverage for new Python execution lines;
record a failed, cancelled or unavailable check with its actual Result rather
than upgrading it to PASS. Refresh DATA-0096 only through the receipt-preserving
inventory workflow after all P11 source and public documents freeze. Run
`graphify update .` only after all writers finish. Operational service changes,
route reload, credential changes, Windows B acceptance, independent production
restore, remote CI and final acceptance remain independent results.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

The Windows B owner consumes Export 2.0 through its external Node receiver
`scripts/ops/receive-hermes-exports.mjs`; that repository is not modified here.
Before a real acceptance it must record the Export schema/version, delivery ID,
ACK ID, scheduled execution, response-loss behavior, restart sequence, backup
and restore source, and the rule that held/uncertain reports are not silently
resent. The external Hermes SDK owner separately owns any platform Call-ID
binding: the local collector records only its own call identifier. The data
owner must separately accept raw-source retention, access and expiry; no model
or fetched source text can add an operational privilege.
