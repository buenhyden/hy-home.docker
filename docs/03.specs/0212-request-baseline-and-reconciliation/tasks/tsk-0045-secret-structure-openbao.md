---
title: "Secret Structure and OpenBao Contract Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0045"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-02"
---

# Secret Structure and OpenBao Contract Task

## Overview

### Objective

Implement the approved local P06 secret-structure, SMTP reader and OpenBao
contract reconciliation. Preserve historical acceptance and separate current
source, isolated validation and any authorized private read from actual HOME
operation, rotation, independent restoration and final operator acceptance.

## Inputs and Authorization

The direct P06 plan authorizes local source, tests, documentation, CI selection,
independent review, and a normal local logical commit. The actual `.env`, private
registry and fixed SMTP paths may be compared read-only only after synthetic
value-leak tests and independent security review. Values, value hashes, lengths
and source lines are excluded from receipts. Private changes, secret issuance,
rotation, deletion, operating service/host changes, external mail and remote
integration are excluded. Missing dependency-package documents do not establish
complete historical crosscheck.

Initial workspace HEAD was clean at
`0a2f7aad418029f0b49645b16ec5a90c86a83a12`. Existing metadata-only observation
found `.env` and the local registry regular and mode 0600; canonical SMTP file
present and old candidate absent. These observations are dated facts, not a
new deletion, equality or current functional-consumer result.

Governing inputs are REQ-0027, AD-0031, SPEC-0212 and its Plan, the P05
TSK-0044 native credential handoff, SPEC-0204 Task P01/P02/P06, and existing
catalog, SMTP and consumer-migration sources. Source proof is not a new HOME
acceptance. Historical Task bodies and issued secret identities stay intact.

## Work Log

### Single-writer leases

Each writer records exact existing-path public fingerprints and ABSENT new
paths before editing; changed shared input pauses the affected slice only.
Acceptance owner, file writer, reviewer, data owner and operational accepter
are separate. Agent labels confer no human identity or operating authority.

| Scope | Single writer | Independent review | Boundary |
| --- | --- | --- | --- |
| Read-only structure CLI, library and directly corresponding tests | `/root/p06_structure` | independent code/security reviewer | New structure command, library and owned tests; no existing secret writer or private mutation |
| SMTP public/private readers and focused tests | `/root/p06_smtp` | independent code/security reviewer | `smtp_public_source.py`, `smtp_contract.py` and directly corresponding tests only |
| Public catalog comparison test helpers and synthetic duplicate tests | `/root/p06_qa` | independent QA reviewer | `test_secret_metadata_sync.py` helper/test slice; no catalog authority change |
| SPEC-0212, this Task, DATA-0096 and P06 living docs | `/root/p06_documents` | independent document reviewer | Current Task and author-owned documentation only; preserve completed Task bodies |
| Script manifest and CI selector integration | `/root/p06_ci` | independent CI reviewer | Exact manifest/CI registration slices and `tests/validation/test_smtp_ci_routing.py`; no unrelated gate or skip change |

The documentation baseline is public Spec SHA
`73a8028ece505acaf85261c0e84985792bc18d85da5a7b45560b360d09b53487`, Plan SHA
`70233035e0222b77907bc3c7f6a332074b5de1be014256571797e675859feec1`, DATA README
`f26bbfa388598cb48efbc7bbcc6630a1486f06d9160760cdec87faa4851ffc71`, and DATA
payload `0e23c6b85c436e6dbceed4108f65bcf8e179e82a0b0299874cdd112a7dccc215`.
This Task was absent. Exact source/test packet fingerprints are recorded by
their single writers before edits. Data owner and operational accepter remain
UNASSIGNED pending actual owner nomination.

SMTP writer's pre-edit public packet: `smtp_public_source.py` SHA
`e84c37702fff817e20356bf38a6df1eacba3ab19509992fa0e08353ce49b79f0`,
`smtp_contract.py` SHA
`a0f5ef2df330d4b92d1279512c3af8a62c4388f991ef376bfaa5912451cbb002`,
`test_smtp_public_source.py` SHA
`e7334d2c2c897a38fec03fde9bfc17afc9613d9a26cac9a5046e7c1809459229`, and
`test_smtp_contract.py` SHA
`9d7c47c0edbc2443f77e25356d1f8206db148226b50a6b58bc3437896d99a2a7`.

Living-document baseline: OpenBao consumer README SHA
`c5b232d6791a600f38720e47af095b4b52b9cc515b3b149a2f716cc1aa1a4b99`, RUN-0106
`8788554b76834e5a10bf3edb59b9371f88ba0ed1f27fa3b45bcc2d619d2101f5`,
GDE-0010 `112e22b9e8013606fecd6a0583521ad46c897d7a41c4ce77ebed25cdc57dab38`,
and GDE-0003 `f295888e8a1165d3106ba5f22272c5ee40b2dba3c1f4f3ccd78ef831f58277db`.
QA helper baseline `tests/validation/test_secret_metadata_sync.py` is
`44c8193ca6d21aa7d835d523275dce79dca0fcc53023c05d2c1b78e521a82e2c`.
CI baseline: workflow contract
`95deb0da017de31f2c07998358c38d31d483ba245e939a2bc3b26f12a828f997`,
script manifest `8d703b7601af47d1955154dc7f8e478c2f12023f7c44a4088d17056a5c855ece`,
and CI routing test
`e236dfb0704e9468d234c3844c11ec0bc11f28bac9566cc103b5e0c5493fe353`.
The new structural CLI, library and test did not exist at the baseline.

### Current dispositions

| Item | Criterion | Work Unit | Initial disposition | Current boundary |
| --- | --- | --- | --- | --- |
| P06.01 | 76 | W81 | SOURCE_READY | Reuse catalog/schema/view and distinguish metadata from image support validation |
| P06.02 | 77 | W82 | IMPLEMENT_GAP | Key-only environment comparison does not establish complete structure parity |
| P06.03 | 78 | W83 | REUSE_ACCEPTED | Preserve dated trust/custody/restore receipts at their actor/version scope |
| P06.04 | 79 | W84 | TEST_RESIDUAL | Retain completed consumers; producer adapter, held consumers and n8n remain separate |
| P06.05 | 80 | W85 | IMPLEMENT_GAP | Bound SMTP reader races and report observed old-copy absence without equality |
| P06.06 | 81 | W86 | BLOCKED | Preserve recovery copies; no newly authorized retirement target or consumer-zero proof |

### Safety and evidence boundaries

The comparison must reject symlink, hardlink, nonregular, permission, growth,
rebind, duplicate and ambiguous inputs without writing private files. Values
may enter process memory only during the explicitly authorized read-only
comparison; no payload, hash, length, raw configuration, private filename or
credential is recorded. The user selected existing consumer contracts; n8n
OpenBao production delivery and refresh is an explicit handoff, not a new wave.
Catalog `DEPLOYED` remains distinct from `APPROVED` copy authority. IAM-004/013
held consumers do not start, and PG-020/recovery material is not removed.

Source, static, synthetic/isolated tests, historical operator acceptance,
this execution's direct operation, credential rotation, independent restore,
remote CI and final acceptance are independent axes. Actual HOME changes,
real rotation/restore, remote integration and P12 final acceptance are NOT_RUN.

### Existing acceptance and applicability

SPEC-0204 TSK-0014 records the 2026-10-27 Grafana admin and Keycloak admin
cutover, rollback and re-cutover, and the Grafana OIDC client's selected
source comparison and cutover. Interactive browser SSO was not run as part of
that OIDC receipt. The owner-reported 2026-10-28 OIDC batch cut over six named
services; OpenSearch Dashboards and Superset remained held. The same Task
records ten deployed Agent output plans, with separate `UNKNOWN` consumption
for IAM-004 and IAM-013 where held consumers remain. These are dated operator
records, not direct observations in this execution. Rendering, consumption,
rotation and recovery remain independent evidence.

SPEC-0204 TSK-0006 records 2026-10-14 owner-attested custody, subsequent
protected snapshot/R2 agreement and HOME 2.7.1 transition, and separately
selected 2026-10-27 isolated restore probes. Custody remains an owner statement,
not an independently inspected secret or location. The 2026-10-30 correction
records the five window residuals' 2026-12-15 review date; no automatic
extension or current operational pass is inferred here.

The current public catalog check at the observed baseline passed in the
existing dependency-equipped QA Python with 149 entries and one alias. The
system Python check returned `P02_METADATA_BLOCKED` because its `referencing`
dependency was absent; an unrelated package environment also lacked
`markdown_it`. These observations are environment-specific, not runtime
credentials or support-matrix validation. The baseline SMTP public-source
module independently passed 17 tests; prior 68-test SMTP receipt was reported
by its assigned writer. Private metadata and credentials were not read.

The 2026-11-02 official-source check read the OpenBao Agent template 2.7.x
page, the Airflow Celery provider configuration, Valkey ACL, restic restore,
and RFC 5321. The OpenBao page documents file rendering, missing-key behavior,
permissions and one previous-render backup; template output does not prove
consumer reauthentication. Airflow's currently published provider page is
3.26.0, so its public `_CMD` reference is not by itself evidence of the
installed provider version. Valkey named ACL commands/keys, restic restore
target behavior, and SMTP server acceptance each retain their own scope.
The P06 implementation does not alter any installed image or version.

The tracked OpenBao Agent HCL does not explicitly set `error_on_missing_key`
or per-template `backup`; it sets `exit_on_retry_failure=false`, and template
files use 0640 or 0600 according to the declared output. Its health script
separately checks every declared template's actual KV field against the
rendered file and rejects unexpected group-readable output. The official 2.7.x
page documents a false missing-key default and one prior-file backup by default.
The observed source/default difference is an IMPROVEMENT_CANDIDATE, not proof
of current leakage or functioning rotation: reproduce the exact installed
image behavior and consumer/backup implications in an owned fixture before a
separately reviewed source change or any operator-authorized rollout.

Official URLs and 2026-11-02T12:32:50Z research observation:

- <https://openbao.org/docs/agent-and-proxy/agent/template/>
- <https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/configurations-ref.html>
- <https://valkey.io/topics/acl/>
- <https://restic.readthedocs.io/en/stable/050_restore.html>
- <https://www.rfc-editor.org/rfc/rfc5321.html#section-6.1>

The Open WebUI current environment reference was also consulted at
2026-11-02T12:37:50Z: <https://docs.openwebui.com/reference/env-configuration/>.
It documents stored configuration precedence for marked settings. This is a
current-page reference, not proof that a particular installed version or
stored provider credential has the same state; no WebUI configuration was read
or changed.

The selected P05 synthetic Mailpit native credential update proves the next
owned Worker execution consumed changed material under the same credential ID.
It does not prove OpenBao rendered or updated that native credential, real
Stalwart delivery, actual issuer rotation or refresh of an in-flight execution.
P06 retains the exact producer/issuer, operator, native UI/API and recovery
handoff as missing inputs; no synthetic P05 identity is issued as a production
catalog identity.

### Public catalog duplicate regression

The QA writer changed only `tests/validation/test_secret_metadata_sync.py`
from baseline SHA `44c8193ca6d21aa7d835d523275dce79dca0fcc53023c05d2c1b78e521a82e2c`
to `f1062ae419a62d8f4fa78d0847bfeb5f770c2d14fba8aa52f1d2f8a8d742c02f`.
Synthetic duplicate environment-key and registry-ID tests first demonstrated
four failing subcases, then seven focused tests and all 21 public schema tests
passed. The latter took 57.623 seconds. Ruff check/format and diff check passed.
The writer used public source and synthetic inputs only. A follow-up corrected
the empty public registry fixture to use production parsing; its newer SHA is
`76fca98d9a85549cbb371c79249e2fe0d8916176ecbf2759a2bb6245f167e800`.
At that observation seven focused tests and Ruff passed. The writer reran the
full public schema class against the newer SHA: 21 tests passed in 59.655
seconds. Independent security reviewer `/root/p06_security_review` approved
that newer source and reran three synthetic tests successfully. Neither source
epoch establishes current private structure or image support.

### SMTP reader correction and local regression

The SMTP writer reproduced seven synthetic RED cases for FIFO replacement,
growth and name/parent rebinding. The current source packet is public reader
SHA `92b73ca8f39a80e923184075194d5fc0ee19df32b87f674526605783c5732656`,
private reader `edafb4f49b6fef68aaddf2f8bd00c4a89d73ad6cb002343f0fdc10127c6d5c15`,
public test `f42fcd23fe7130f1829ee55eded05740543c8aa719c3d0a1b34b01773ef9f72b`
and private test `9ee20c5ba82749c77493f2fa4203c14f5b27675f3310fa0ec6cdb316d0267af5`.
The writer reports 91 synthetic source/contract/proof tests passed in 2.064
seconds and Ruff check/format passed. Conservative changed executable-line
traces covered 28/33 public and 53/63 private reader lines, excluding module
load. Independent QA code review approved the frozen packet and reran all 91
tests successfully. Public source is capped at 256 KiB; protected private
snapshots use a 2 MiB bound and verify leaf and parent rebinding. Real SMTP and
private equality are not inferred from synthetic results.

Follow-up security review found a read-only return boundary that needed another
parent/held/old-absence recheck. The SMTP writer corrected it and the independent
security reviewer approved the current public reader
`92b73ca8f39a80e923184075194d5fc0ee19df32b87f674526605783c5732656`, contract
`3dccd7a476a0c6798557876c97a52c4330be9958cdef30e896ee0336ec0bde54`, public test
`f42fcd23fe7130f1829ee55eded05740543c8aa719c3d0a1b34b01773ef9f72b` and private
test `1811aea7d36530c36edfe4a32fdf3f33bd98bda65cec104de75892069ee24ad8` packet.
The reviewer reran 93 synthetic tests successfully. This supersedes the earlier
contract/test source epoch only; no real SMTP or private consumer was tested.

### CI registration and known residual

The CI writer registered the new synthetic-only structure test and paths in
the existing selector and manifest. Frozen workflow SHA
`d9041760171b958aafa6dd9e8d32baec80354a327db8ae05a3986db364146ac7`,
manifest `cb87cd932ec667f82ae5cf1d1fb4a49312897af4ed2444f7c78a097c61860159`
and routing test `55632ed20566e4d3d9855c8365d1f7da137976c284ad06bfc4906c85cc114fc3`
were independently reviewed by the QA writer. Registered synthetic structure
and routing tests passed 22/22; the routing subset passed 4/4 and the workflow
contract checker passed for five workflows, seven jobs and nine actions.
The changed-profile explain remains exit 1 on the existing `leaf.p03-hermes`
admission parity, not a P06 or remote-CI pass. The actual manifest checker
initially exited 1 with five untracked-path/consumer/test failures for the new
CLI, library and test. Staging and a successful rerun are required before
claiming a manifest pass; no path or admission rule is bypassed.

The first changed-document metadata check failed with 146 reported issues,
beginning with the Plan dependency grammar. P06 W81–W85 cells used prose where
the registered parser requires `None` or Work Unit references. The baseline
Plan also had prose in P05 W77 and W78 dependencies: a separate `git show HEAD`
readback and parser call reproduced both as invalid. The documentation writer
normalized these cells to `None` or their existing Work Unit reference while
preserving their source-input and no-hidden-prerequisite meaning in the Plan
prose; W83–W85 is an accepted range. Completed Task bodies were not changed.
The second changed-document check also failed with 146 diagnostics, starting
with an out-of-domain `BLOCKED` Evidence Result. The SMTP comparison was not
performed, so its registered result was corrected to `NOT_RUN` while its
`OLD_ABSENT`, exit 2 and blocked reason were retained. An independent full
active Spec loader then passed all 40 packages. The third changed-document
check passed with eight selected, zero violations, zero legacy exceptions and
zero transition overrides; its same-scope result establishes that the 145
archive/type diagnostics were downstream of the failed Spec load. The first
two failed runs remain evidence, not retroactive passes.

The CI writer then ran the remaining documentation gates serially. Link
alignment passed for 1,184 documents and 9,646 links with zero failures; one
existing historical warning remains for 232 legacy archive links lacking a
capture source. Operations catalog passed, Registry contracts reported zero
violations, and corpus lifecycle passed with zero violations (five migrations,
140 tombstones, 116 preserved, 286 decisions and 374 recovery rows). These
are local source/document checks, not remote CI or runtime acceptance.

The diff has no Node or Python dependency manifest/lock change. A scoped
`npm audit --offline --package-lock-only --ignore-scripts --json` on the
existing OpsflowSmtp lock returned exit 0, zero vulnerabilities in 155
dependencies using cached advisory data only; it proves neither current
advisory completeness nor image, SBOM or provenance acceptance. `pip-audit`
was absent from PATH, so Python dependency audit is NOT_RUN and no global
installation was attempted. The manifest checker and normal staged wrapper
remain pending until the newly added paths are staged.

### Authorized private read-only observation

After the synthetic leak tests and independent security approval on the then
current source/test packet, the coordinator ran the explicit P06 read-only
checks against the workspace on 2026-11-02. The structure check returned exit 1
with `env=DRIFT`, `registry=DRIFT`; the SMTP check returned exit 2 with
`OLD_ABSENT`, `comparison_performed=false`. No value, value hash, length or
raw line was printed or retained, and no private file was modified. Absence is
not equality or a new retirement. The actual SMTP observation used prior
approved library `7ce7d084752bc17d6c6fdb2a8454c4346ec306be5487800aece0a0bac5485a18`,
CLI `848862f54e5a2dc7b955197d415fcea56ba30f1994ab45caadab1802aa492967`,
and tests `5eceff4a3c12db3417087cb935903dcde3eae73af2c317e63cf3cabefca59386`.
The later diagnostic library did not re-execute the actual SMTP check. After a separately security-reviewed
diagnostic improvement, a read-only repeat returned `DRIFT`: the first
public-reference positions were env line 52 `PUBLIC_ASSIGNMENT` and registry
line 18 `PUBLIC_TEXT`. These are public-reference coordinates, not private
line positions or proven causes. No value, hash, length, raw line or private
identifier appeared. Private correction is outside this user's selected scope;
no unsupported partial match is inferred.

The observed workspace root has mode 0775. Descriptor, identity and pre/post
checks narrow races but do not establish immunity to every uncooperative actor
with same-group write access between checks. Quiescence and a trusted writer
remain operational prerequisites; this is not a guarantee of atomic private
snapshot acquisition or authority to change private files.

The final structural tool source packet is library
`0f2cf8e46be62f482f92778a88b3f4f71b4f0702e5a20a8cafaa131507b68f88`, CLI
`848862f54e5a2dc7b955197d415fcea56ba30f1994ab45caadab1802aa492967`, and
synthetic tests `5fdc64ae786d89a3b14babe6619716bce0205ed182c9553dd5205add988a1d70`.
Independent security review approved this packet after the initial untrusted
argument reflection and diagnostic findings were corrected. The reviewer ran
22 synthetic tests successfully. The writer reports full executable Python
line coverage 303/320 (94.69%) and Ruff/format pass. Tests cover the closed
output and failure paths, not HOME consumer or credential acceptance.

### Current workspace inventory

After the source writers reported frozen public inputs, DATA-0096 was refreshed
with the existing scanner's connection extraction and explicit public paths for
the four new files. The scanner reported PASS without private metadata output:
41,898/41,898 accessible file entries, six complete and 84 partial reviews of
2,308 reviewable text files, zero of 17 planned renders, and zero of 112
declared services directly operated or independently restored in this scan.
These are different denominators; file discovery and synthetic test results do
not imply full body review, HOME operation or restore.

The dated comparison with the previous published DATA observation returned four
public additions, 16 changed public paths, and no changed connections. Its
earlier snapshot was collected before the P05 commit at `e14ebe0...`, whereas
this Task began at clean `0a2f7aa...`; the result includes that observation
boundary and must not be treated as a pure P06 commit diff. New paths were
explicitly included before staging. The data package's own current hash is
excluded from its fingerprint to avoid a circular digest. Curated P05 records
and prior leases are preserved; P06 owns six new requirement rows and the
current lease for each changed public path. This inventory records public
source and aggregate exclusions only; no private file body or metadata output
was retained by this scan.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline and writer leases | 76 | W81 | Git status and public fingerprint readback | Clean 0a2f7aa and public source | PASS | Inputs and Authorization; Single-writer leases | required | - |
| Protected structure tests | 77 | W82 | Synthetic normal, rejection, interruption and disclosure tests | Frozen structural tool packet; synthetic inputs | PASS | Structural tool packet: 22 tests and independent security review; 303/320 Python lines | required | - |
| Private structure observation | 77 | W82 | Authorized read-only full structure comparison | Actual protected paths; fixed outputs only | FAIL | env and registry DRIFT; public-reference first positions only, no values | required | - |
| Historical acceptance reconciliation | 78 | W83 | Source and scoped prior Task readback | Prior operator records and current versions | PASS | Existing acceptance and applicability; no current HOME result | required | - |
| Consumer and n8n handoff | 79 | W84 | Producer and native credential boundary readback | Current catalog and P05 Task | PASS | Existing acceptance and applicability; RUN-0106 handoff | required | - |
| SMTP source safety and alias | 80 | W85 | Bounded read, race and alias regression | Frozen SMTP source and synthetic inputs | PASS | SMTP reader correction; independent QA/security and 93 synthetic tests | required | - |
| SMTP private equality | 80 | W85 | Authorized read-only comparison | Fixed canonical/historical paths | NOT_RUN | OLD_ABSENT, comparison_performed=false; exit 2, comparison blocked | required | - |
| Retirement and recovery assessment | 81 | W86 | Reader, custody, backup and ownership review | Public source and prior receipts | PASS | Existing acceptance and applicability; no new deletion target | required | - |
| Workspace public inventory | 76 | W81 | Scan, compare and metadata validation | Frozen public paths, current curation and explicit new paths | PASS | Current workspace inventory; no private output or runtime/render execution | required | - |
| Changed document and lifecycle gates | 76 | W81 | Metadata, links, operations catalog, Registry and corpus lifecycle | Exact P06 document set after schema corrections | PASS | CI registration and known residual; two earlier metadata FAILs retained, one historical link warning remains | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 76 | pending | Baseline and writer leases | SOURCE_READY pending scoped catalog checks. | SPEC-0212 TSK-0045 |
| 77 | pending | Protected structure tests, Private structure observation | TEST_RESIDUAL: synthetic and security checks passed; real env and registry DRIFT, private correction outside scope. | SPEC-0212 TSK-0045 |
| 78 | accepted | Historical acceptance reconciliation | REUSE_ACCEPTED only within historical evidence scope; current equivalence is separate. Owner @buenhyden accepted on 2026-11-06. | SPEC-0212 TSK-0045 |
| 79 | pending | Consumer and n8n handoff | TEST_RESIDUAL: handoff recorded; actual producer/consumer authorization and rotation remain separate. | SPEC-0212 TSK-0045 |
| 80 | pending | SMTP source safety and alias, SMTP private equality | SOURCE_READY: bounded reader and synthetic review pass; old-copy absence prevents equality comparison. | SPEC-0212 TSK-0045 |
| 81 | pending | Retirement and recovery assessment | BLOCKED for actual retirement without exact target, authorization and recovery evidence. | SPEC-0212 TSK-0045 |

## Review and Completion

Current implementation, independent review and local checks are pending.
No prospective test or historical acceptance is promoted to current operation.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace inventory](../../../90.references/data/0096-workspace-inventory/README.md)
- [Opsflow notifier recovery Task](tsk-0044-opsflow-notifier-recovery.md)
- [Historical OpenBao consumer migration Task](../../0204-service-integration-security-and-operations/tasks/tsk-0014-p06-openbao-consumer-migration.md)
