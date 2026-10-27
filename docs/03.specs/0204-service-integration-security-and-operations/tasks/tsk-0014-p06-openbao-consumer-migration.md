---
title: "P06 OpenBao Consumer Migration Task"
version: "0.1.10"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0014"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P06 OpenBao Consumer Migration Task

## Overview

### Objective

Own criterion20/W46-W55: one existing consumer pilot, sequential catalog-bound
same-byte OpenBao copy, verified rendering/consumption and recovery, followed
by precisely owned obsolete-copy removal and separately targeted rotation.
Issuance provides an executable ownership and admission contract. It reads
no actual secret, creates no KV/AppRole/DB/object, and changes no runtime.

## Inputs and Authorization

The user's full P06 prompt and coordination request authorize assessment,
formal Task issuance and independent worker instructions. Prompt SHA256 is
`0d11d0fd04ba1fd7c2eefddc7414476d3783c795d86e7719f75c95c9e87037ad`;
its historical baseline is `860ac1c3633eac9ad416fb1abd8a61a6e617ebd8`.
Actual clean coordinator/local main is
`f7543e0697e2473cbbbeb254792e7a1d5b4b8423`. Fresh ls-remote confirms remote
main `4e26a5a8022a7307c7461af60337442912955df1`; open PR list is empty.
Remote CI Quality Gates38105014827 and Push on main38105014631 succeeded
at4e26. Those are remote baseline receipts, not P06 CI or native acceptance.
SMTP PR413 is MERGED at `34c7d4644fee6541d0d969390abf1bb54c16fd27`;
source canonicalization does not close operational retirement/recovery.

Read bootstrap/provider, SPEC-0204/0212 and the current P01/P02/P03/P04
Tasks, catalog and selected consumer. Preserve completed P00, Influx retirement,
DEV/MNG, RedisInsight/exporter, k6/OTLP, common controls and Stage05 source.
Preserve OpenBao PR409/410 TLS, wrapped reauthentication, readiness, audit and
snapshot implementation. Reuse existing issuer/renderer and registered
operations/retirement helpers; no duplicate Spec, catalog or workflow authority.
Preserve issued IDs, created dates, prior receipts and completed historical Tasks.

The latest full P06 prompt selects logical commits and an owning-Spec PR after
implementation, required CI and independent review at the latest head. Earlier
SEC01/SMTP01/CLN01 retain their local-main/no-PR delivery instruction. Dev is
unused. Reconcile unpublished main and dependency delivery before a P06-only
PR; this assessment neither pushes main nor creates a PR or worker chat.
Do not repeat source/commit/review permission questions. Investigate operational
facts read-only where authorized; before private actions record exact target,
consumer, effects, validation, backup, recovery and executor here. Missing
facts block only their dependent action and cannot become invented PASS.

### Worker and Exact Ownership

One P06 writer uses `codex/p06-openbao-consumer-migration` in
`/home/hyunyoun/data/hy-home.docker/.worktrees/p06-openbao-consumer-migration`
from the reviewed issuance commit integrated into local main. Record actual
branch/HEAD, base, clean status and source hashes first. Other writers remain
active: never reset, stash, clean, stage or force-push their changes.

After confirming these paths are still absent, own only:

- This Task, its lifecycle, implementation evidence and logical commit ledger.
- `infra/03-security/openbao/consumer-migration/README.md`,
  `wave.schema.json` and `receipt.schema.json` in that directory.
- `scripts/lib/ops/openbao_consumer_migration.py` and the narrow CLI
  `scripts/operations/openbao-consumer-migration.py`.
- `tests/lib/ops/test_openbao_consumer_migration.py` and
  `tests/validation/test_openbao_consumer_migration_contract.py`.
- Synthetic fixtures generated in those tests. If stored fixtures are needed,
  only `tests/fixtures/openbao-consumer-migration/README.md`, `valid-wave.json`
  and `invalid-wave.json`; confirm the existing family README first.

New folder README bodies are Korean and follow Registry profiles. Existing
family/service README edits are proposals to their sole writer. No production
reference/ copy or new top-level authority. Split private I/O internally only
after an exact added-file lease; the above names define the initial write set.

P02 exclusively owns catalog/schema, issued-ID classification, parser, views
and `secret_catalog` API. Reuse its public validation/load interfaces after
the reviewed source commit is integrated; record that dependency SHA. P02
adds any genuinely existing opsflow identities and approved destinations using
its issued-ID contract. P06 cannot invent IDs, fill null destinations, approve
its own catalog classification, or copy `catalog_views.py`. Until P02 source
is an ancestor, public schemas and explicitly provisional injected-interface
tests may proceed; final production binding and copy execution wait.

P01 exclusively owns existing OpenBao scripts/config, issuer/journal/renderer
engine and subject0085/OpenBao service README. Submit per-consumer renderer,
policy or wrapped-issuer requirements for that owner; do not install the
sample `agent-opsflow.hcl` as a second Agent implementation. P03 owns endpoint/
delivery contracts. P04 owns actual opsflow resources, role/schema/migrations,
adapters/DAGs and PG/S3 canaries. P05 owns notifier/native credential refresh.
Do not copy `workflow_lib/*`, provision a database/role, or expand n8n access.

SEC01 owns selected images/digests/trust/security. SMTP01 is the sole
COMM-003 retirement executor; CLN01 owns generic deletion eligibility.
Root/leaf Compose, environment, gateway, Alloy, backup, generator integration,
shared helpers/tests, catalog support, Registry, indexes, Script Manifest,
workflow registration and Spec/Plan remain read-only without an exact exclusive
lease. Submit base blob IDs, exact hunks, consumer/test/rollback map and hashes
as ignored proposals. The coordinator/named owner integrates once, preserving
both sides of conflicts; latest submission never overwrites prior work.

### Current Prerequisites and Parallel Boundary

W46/W47 can start now: public contract/reuse audit, closed value-free wave/
receipt schemas, RED/GREEN synthetic selection/privacy tests and proposals.
W48 production integration consumes the P02 API after its source delivery;
pure transport/synthetic tests may use an explicit injected interface meanwhile.
Mocks are neither an approved real catalog nor native TLS/KV acceptance.

Latest local P01 HEAD is
`5fa707d842098e9acef0c3f9176afaa3c48421a0`: journal-identity source correction
and bounded server-diagnostic tests are committed; four subject0085/service
documents remain dirty. Its Task is blocked. Latest selected-version native,
HOME, snapshot-only token, independent custody and empty restore/consumer
reauthentication acceptance remain pending. A diagnostic is not full P01.

Latest observed P02 HEAD is
`b06b513c93194cffbd2d6ab4f65fb259a9804c57`, atop its four source commits
rebased onf754. A staged Task follow-up reports a new ignored lock-inheritance
proposal: parent-death RED, eight lock,13 generator and147 regression PASS,
plus independent review. This is worker-reported proposal evidence, not a
coordinator-applied combined-head result. Final shared generator/registration
integration still waits. Catalog has145 entries, COMM-003 aliasing COMM-002,
but no opsflow entry and no approved KV destination. PG-020 remains retained
for initialization/rollback; a known nlink2 is not an eligible deletion.

P03 HEAD `93ad5da2538f99cc978745a458587e2fde71550c` contains source contracts;
two documentation clarifications are staged. P04 HEAD4e26 and P05 HEADf754
have uncommitted owned workload/test drafts. No frozen P04 native consumer or
P05 credential receipt is handed off. SEC latest/security and HOME remain
unclosed; SMTP actual cutover/retirement and CLN actual apply/recovery remain
unaccepted. These local facts are not remote GitHub changes. Never stage
their files to satisfy this session's Stop hook.

W50 first actual pilot waits for all relevant facts:

1. SEC01 supplies accepted exact OpenBao server/Agent/CLI digest, architecture,
   version and trust/security receipt. Source selects2.7.1; prior HOME2.6.2
   observations are historical, not a current deployment verdict. Unrelated
   image acceptance is not a global P06 gate.
2. P01 supplies accepted selected-version TLS/SAN/CA, wrapped fresh issuer,
   cleanup/version/readiness contract and W23 actual authentication, restricted
   snapshot, independent custody and empty-restore/reauthentication evidence.
3. P02 supplies exact existing static IDs, source binding, consumer and server
   owner, mount/data path/field, classification/action, ACL and delivery; no
   null/BLOCKED destination or alias is eligible. The sample PG-006 path is
   not an authoritative opsflow identity.
4. P03 supplies exact endpoint/TLS, host/process identity, actual UID/GID/mode,
   mount/reopen/recreate behavior, LKG/TTL/failure policy and denied peers.
5. P04 W38 supplies an existing `opsflow_dev` ingest/S3 consumer, reviewed role,
   restricted object identity, actual canary and backup/restore target. P04
   may prove its bounded DEV batch with restricted file delivery before P06;
   do not create a circular dependency or Wiki resources to manufacture a pilot.

Pilot is one existing opsflow consumer, not all services or all secrets; P05
is not a first-pilot prerequisite unless a notifier native credential joins
the selected wave. P06 does not create that consumer. W51 authority changes
and W53 removal additionally require coherent integrated P02 generator guards,
the corrected SMTP lock inheritance, actual native copy/consumer recovery and
fresh writer-stop/zero-consumer proof. A cooperative SMTP lock does not stop
CLN's separate lock or nonparticipating writers. Subsequent consumers have
their own exact gates; never promote a synthetic or source-only result.

### Required Copy and Delivery Contract

Use P02's closed versioned catalog. Wave/receipt schemas are selection and
evidence contracts, not another catalog: no secret bytes, tokens, raw paths to
unapproved resources, value hashes, environment dumps or arbitrary fields.
Validate the entire selected plan before private/network I/O. Reject unknown
IDs, duplicate destinations, aliases, out-of-scope/lab/unused rows, unresolved
consumers or paths, traversal, wildcard/admin authority and unsupported fields.
Keep bootstrap_external and stable_crypto outside generic copy/rotation;
remove confirmed unused material via its owner rather than importing it.

First copy preserves exact existing bytes. Source, token and CA/trust-bundle
reads use bounded descriptors from every-component no-follow directory opens.
Require regular single-link leaves, exact approved UID/GID/mode/size, stable
root and before/after dev/ino/size/mtime/ctime identity. Bind CA bytes/provenance
to P01's accepted public trust artifact hash/receipt, never a private-key hash.
Prefer loading held verified CA bytes into the TLS context; a path-only TLS
library needs the verified immutable P01-owned mount and identity rechecks
through the handshake. RED cases cover parent/leaf symlinks, hardlinks,
wrong owner/mode, FIFO/devices, empty/oversize input and rebind/mutation for
source/token/CA, plus secret-redaction markers. Do not resolve arbitrary
private paths during the public plan. Reuse project-aware guards where suitable.
Private dotenv conversion uses the current Compose parser and approved ID map,
never shell source. Private tokens use protected input files/descriptors, not
argv, Git, receipts or raw logs; no token-producing operation is inferred.

Use exact approved HTTPS origin/mount, TLS CA/SAN verification, no redirects
and no ambient proxy interception. Bound response/body/depth, connect/read and
whole-operation budgets, retries and server errors. Reject duplicate JSON keys,
nonfinite values and malformed/version-missing responses. Normalize failures
to fixed diagnostics without URL credentials, response bodies or tracebacks.
An undetermined shared overall budget remains explicitly unknown.

KV-v2 uses CAS=0 only for a genuinely absent key; equal existing bytes are a
no-op, different bytes a conflict. Soft-deleted/destroyed versions, missing
mount, authorization failure and HTTP404 are not automatically safe absence.
Lost responses or CAS races require bounded readback/metadata reconciliation:
exactly equal accepted bytes/version may resolve success; different data stops;
unknown/deleted/unverifiable state stays unresolved. Do not retry an ambiguous
write as an unconditional overwrite or delete metadata to make CAS=0 succeed.
Compare values only in memory. Receipts record public IDs, states/version and
input source/schema hashes, never secret-derived hashes or values.

The copy token has only create/read on the exact approved pilot data paths,
short nonrenewable TTL and verified identity/policy; deny update/patch/delete/
list, sibling/project/mount access and unnecessary metadata. P01 supplies
any required exact reconciliation-read interface without widening this token.
An earlier successful item followed by failure is PARTIAL; preserve its
version and old source, never auto-delete or overwrite it on retry.

Per-consumer least-privilege renderer grants only required exact data paths
and necessary version metadata; no list/write/admin/other-project access.
KV-v2 path policy does not provide field-level isolation: never mix privileged
and consumer values in one readable connection object. Reuse P01 wrapped
SecretID delivery, fresh metadata/readiness and version checks. The sample
direct SecretID/uid50000 contract is provisional and cannot override P01.
Current P01 issuance is bound to its existing role/paths. P01 must provide a
dedicated opsflow role/policy/template and issuer target, or reviewed typed
parameterization; adding pilot paths to the shared global role is not isolation.

Directory mounts and reopen behavior must handle atomic replacement/inodes;
otherwise target only the selected consumer for recreation. Verify host file
UID/GID/mode, not Compose mode declaration alone. Refuse empty/missing/stale/
auth-failed delivery and prove LKG/TTL failure policy. Agent has no Docker
socket, restart privilege or server-password rotation authority. Prove native
PG/API/S3/mail consumption only for the selected wave's genuine consumer.
n8n's encrypted native execution copy requires P05's explicit supported
refresh/rotation owner; it is not an automatically refreshed file mount.

### Authority, Recovery, Removal and Rotation

States are inventoried, classified, copied, rendered, consumed, authoritative,
recoverable and local-plaintext-removed, with versioned transitions and public
evidence. Rotation is separate. Pilot actual rollback and restored-key consumer
reconciliation gate authoritative status; deletion additionally requires the
recoverable state, elapsed reviewed rollback window and zero current consumers.
If any wave fails, stop expansion and restore only its last accepted boundary.

Record exact Docker context/project, host checkout, consumer/image/role/object,
operator, private inputs, effects, deadline, budget, backup snapshot identity,
independently held unseal/key/CA references, owned empty restore path, canary,
cleanup and rollback before actions. Establish facts by authorized read-only
investigation, not by asking for secret values. No in-place downgrade, shared
volume initialization, broad chown, full up/down, prune or destructive HOME
failure injection. Owned isolated synthetic environments precede real targets.

Recovery must restore the accepted snapshot/key version in an isolated empty
target with schedules/egress controlled, reauthenticate fresh bootstrap and
prove the consumer against reconciled management/server/native-copy state.
Retain independently recoverable historical encrypted backups/keys; a source
revert, file copy or two-file SMTP restore is not OpenBao/consumer recovery.
Do not destroy KV metadata/versions or rotate stable encryption keys to simplify
the ledger. Old server credentials in historical snapshots need explicit
post-restore reconciliation, not assumed equivalence with current credentials.

Old active plaintext, private Markdown value cells, temporary export/render
backups and obsolete paths are removed only after fresh source/runtime/job/
backup-restore/external zero-consumer evidence, backup/reissue and exact owner
execution. Canonical COMM-002 stays protected; COMM-003 remains SMTP01-only,
generic material CLN01-owned, PG-020 retained. Source absence alone is not an
import or deletion receipt. Private material must never be staged for Git.
Update P02 metadata/generator through its sole writer; generator cannot
reissue or overwrite authoritative/retired IDs. Prove identity-bound locking
and nonparticipating-writer quiescence before private mutation.

W54 separately targets genuine provider/server rotation after same-value
consumption and recovery proof. Change the selected actual server credential,
reconcile new KV version, render/native copies, old sessions/pools, restart
and old-credential denial; restore the exact accepted rollback boundary on
failure. `_FILE` initialization does not rotate an existing PG role. No broad
credential rotation or encryption/session/bootstrap-key replacement. Missing
selected server target keeps ROTATION NOT_RUN without blocking public source.

## Work Log

### W48 Synthetic Decision Preparation — 2026-10-11

Input `4c83f14b11a77e13e582eb85d0bf256685472a95`; clean69be0b5e fast-forwarded,
exit0. Root owns only existing library/unit-test/dedicated README/Task; common
files are NO_CHANGE. Independent planning approved a pure, frozen, value-free
decision model for criterion20/W48; the dedicated README defines the cases.
Focused unittest SyntheticKvDecisionTests.test_prewrite_not_found_needs_never_created_metadata
witnessed RED (missing SyntheticKvObservation, exit1); SyntheticKvDecisionTests
then passed9 tests in0.053s, exit0. No selection, byte comparison or I/O is added.
Production approval/copier, native reconciliation and W49-W54 remain NOT_RUN;
P02 BLOCKED_P01, existing receipt restrictions and criterion20 stay unchanged.
Final focused suite:32 tests in17.526s, exit0; branch/subprocess coverage98%.
Ruff and QA-environment pip-audit exit0; independent code/security review PASS.
Registered local aggregate exit1: baseline P04 compose.workflow.override.yml
has `${OPSFLOW_AIRFLOW_IMAGE:?}` rejected by tech-stack, outside the P06 lease;
P04 owns source repair; the coordinator owns integration/revalidation.
Canonical remaining five leaves exit0: supply263, compose596 (71 optional skips),
repository439. Links1205/11658: failures0, warning1;2870 legacy captures unverified.
Only the QA copy normalized two unchanged entrypoints to0755; live modes retained.
Frozen input/plan/result receipts: `.agent-work/p06-w48-{review-hashes,local-selection,validation}.json`.
Suffix PASS does not resolve aggregate FAIL or supply hosted/native acceptance.

### Coordinator Source Integration — 2026-10-11

The combined input is local main `0207808560214c7ab88c582cfb4a3d76a70551eb`
with worker `69be0b5e4f816449c19d22e2e03d71c4226c281a`. Seven worker
source/schema/test files are byte-preserved. The stale registration patch failed
apply-check; current common files were reconciled without overwriting P01–P04.
Workflow SHA256 is `f47782da98092e996744419f9083318c4b56d504919525dfb07dba6aee4f734c`;
manifest SHA256 is `6429c6849d7aa9a6a5d96939a3e7b21edb1d611816a04f62cbad14326fae7273`.
Both routing maps include the canonical folder. Direct manifest edges follow
unit-to-library and contract-to-CLI-to-library; unproven transitive edges were
removed after the initial manifest failure. Source and corrected common review
are separately approved. Six affected registered leaves passed with default
executor/environment/timeouts; the full aggregate was not run. Dedicated
synthetic tests passed23; combined repository regression passed430 in96.501s.
Coverage98percent remains worker evidence, not a fresh coordinator measurement.
Earlier combined metadata selected3 documents with0 violations; links checked
1205 documents/11658 links with0 failures and1 existing archive warning.
Lifecycle violations were0. The first final Task metadata check failed147
findings after an invalid Evidence Acceptance value prevented package lifecycle
loading; the value was corrected to pending without changing archive or validator
contracts. Final Task metadata and staged checks are mandatory
before the integration commit, whose Git parents preserve both input histories.
Receipts are `p06-combined-acceptance.json` in the coordinator scratch directory.
Local source delivery does not accept criterion20: HOME, native pilot, migration,
rotation, actual deletion and snapshot/empty recovery remain NOT_RUN.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0014 | draft | ready | #public-work-admission |
| SPEC-0204-TSK-0014 | ready | in-progress | #public-contract-implementation |

### Public Work Admission

The current user directs work from the issued Task, beginning with W46/W47,
while actual pilot, deletion and rotation wait for unmet prerequisites. On
2026-10-11 the exclusive P06 worktree and index were clean at issuance commit
`6f230c56eb97c3cd587d636ba6492b24de13e53d`, which also resolves local main.
Fresh `rtk git ls-remote origin refs/heads/main` returned
`4e26a5a8022a7307c7461af60337442912955df1`, exit0. No fetch, push or remote
mutation was performed. The original checkout and other workers are preserved.
All seven owned source/test/schema paths were absent from that commit.

The root records Task evidence under the doc-writer responsibility; one
delegated qa-engineer owns all dedicated W47 source and tests. Neither writes
shared catalog, generator, manifest, workflow, parent README, Spec or Plan.
Required shared changes remain exact base-blob/patch proposals for their sole
integrator. Request/token/time/price ceilings and provider hard enforcement are
UNKNOWN; native team concurrency is at most7, with one implementation writer.
No private input, credential issue, native resource or billed job is admitted.

Observed dependency worktree HEADs are P01 `9130b6989`, P02 `d32ef6354`, P03
`c1bc25f1a`, P04 `b2a46bc88` and P05 `f7543e069`. These update the issuance
observations without rewriting their historical receipts. P02's validator
currently rejects approved delivery bindings and retains BLOCKED_P01 fields;
it is not an ancestor of P06. W47 therefore uses an explicitly provisional,
injected selection interface in synthetic tests. It creates no production
catalog reader or private copy command. P04 source progress does not establish
its native W38 consumer acceptance. W48 production binding and W49-W54 remain
dependent on their named owners' integrated contracts and actual receipts.

### Public Contract Implementation

Admission was independently reviewed PASS and committed as
`c940c2acb73d844f6af13c99c772f6a998c38ae0`. Its readiness input was issuance
`6f230c56eb97c3cd587d636ba6492b24de13e53d`. Registered Task metadata returned
selected1/violations0, exit0; document links returned failures0 and one
pre-existing historical capture warning, exit0. The first staged style
environment had pre-commit4.6.1 and failed the required4.6.2 pin, exit2.
Reusing `/tmp/hy-home-p09-qa/bin` resolved that environment mismatch without
changing tools or the registered pin: the same Task index passed the staged
controller and hardcoded-secret check, exit0. Exact Python Commitizen4.15.1
validated the message, exit0; the unrelated PATH Node `cz` was not accepted
as message-verification evidence. Sandbox initialization failed before several
commands; their separately approved read-only/scoped retries supplied the
actual results. One narrower review/writer retry resolved stalled tool delivery;
the writer reported that no source edit had occurred before resumption.

Admission commands (repository root, public source input6f230c56e; all final
checks exit0 unless the failed tool pin is stated above):

```sh
rtk python3 scripts/validation/check-document-metadata.py \
  --mode check-changed \
  --changed-path docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0014-p06-openbao-consumer-migration.md \
  --base-ref HEAD
rtk python3 scripts/validation/check-document-links.py --mode all
rtk /tmp/hy-home-staged-style-tools/bin/cz check --message-length-limit 75 \
  --commit-msg-file .agent-work/p06-ready-commit.txt
rtk env PATH=/tmp/hy-home-p09-qa/bin:/home/hyunyoun/.local/bin:/home/hyunyoun/.nvm/versions/node/v26.10.0/bin:/usr/local/bin:/usr/bin:/bin \
  bash scripts/validation/run-ci-precommit.sh --mode local-staged
rtk git commit -F .agent-work/p06-ready-commit.txt
```

Actual public P02 observation on `d32ef6354`: catalog1.0.0 has145 entries,
zero opsflow matches and145 BLOCKED_P01 destination statuses. Draft nonnull
paths are not approvals. PG-020 remains RETAINED_FOR_RECOVERY and COMM-003 is
an alias. Its `load_catalog(root)` returns the validated public catalog;
there is no selection API or approved delivery binding yet. Public Git blobs:
catalog `efa0be3d052a5cd2d5336f333c01352447d2490a`, catalog schema
`433f872bec88ac88ba87de8a69cf1fb9dbad3749`, API
`84c2763614da61dadd10fd1c8d3d89e537c6d3d9`, I/O helper
`2ebe6852ef9d756968870c1b8f15941fd527fede`. These are source objects, not
secret-derived hashes or integration receipts.

The delegated writer's scoped tool delivery remained stalled and it confirmed
no edits. Root interrupted that writer, explicitly revoked its source lease,
and took the sole qa-engineer implementation responsibility. Independent
reviewers retain read-only responsibility; other workers' files are preserved.
Root implemented W47 schemas, public validation CLI and explicitly provisional
injected-interface tests. Candidate bindings cannot select their own authority.
No production catalog import, network transport, private read or copy command
is admitted by this unit.

W47 input is readiness commit `c940c2acb73d844f6af13c99c772f6a998c38ae0` plus
the seven dedicated source files. First unit RED failed with missing library,
exit1; CLI RED failed with missing executable, exit1. Additional scope/admin
mount regressions produced four failures in two methods, exit1. Correcting
`scope=root` and rejecting reserved `sys`/`auth`/`identity` mounts resolved
those failures without changing P02. Final focused unit and CLI subprocess
checks passed17 tests, exit0. Branch-enabled coverage including subprocesses
measured library99percent, CLI93percent, combined98percent (184 statements,
58 branches;5 missing statements and1 partial branch), exit0. This is dedicated
synthetic coverage, not repository-wide or native-consumer coverage. Scoped
Ruff format/check passed all four Python files. Initial Ruff failures for loop
binding, unnecessary suppression and implicit subprocess check were corrected.

Both schemas are closed1.0.0 contracts. Receipt evidence is synthetic and
permits only inventoried/classified with null KV version; native or copied/
rendered/consumed/authoritative/recoverable/deleted claims are rejected.
CLI accepts only bounded stdin shape validation, never private paths or token
arguments. Unit tests bind authority independently of candidate input, enforce
immutable selection, reject duplicate destinations and unsafe paths, and
exercise fixed redacted errors. Subsequent copy/receipt behavior needs a
reviewed extension with meaningful RED cases; it is not implemented here.

Frozen seven-file source SHA256 values reviewed independently:

| Source | SHA256 |
| --- | --- |
| consumer-migration/README.md | `6484d86fc8049c9aac21a3f6353d4c1c8145ec0f9a44d09ea9032000c5e409b3` |
| consumer-migration/wave.schema.json | `2c3156b8f06ce2f1ac8dc37e579d2d9105032fab1636a08a71253e4df2975755` |
| consumer-migration/receipt.schema.json | `563f9ae4e36ba80cdbb86cdd1adc8ee4e28547e67fdcc2fb0b7ca5cba108a37f` |
| scripts/lib/ops/openbao_consumer_migration.py | `84a3bacde569248173e8664a059ddb31d5e4e9069c0da449df0f3892af914bca` |
| scripts/operations/openbao-consumer-migration.py | `280c2a1cd5312f2c3ab3b39c1182b0b40f71a67705b19c9f12857b73ca48f268` |
| tests/lib/ops/test_openbao_consumer_migration.py | `97c16b58494ba5366ce0f3529c171e3e2389afd2c7f826cb591019281359afe9` |
| tests/validation/test_openbao_consumer_migration_contract.py | `97f7e7dae607081719aa4f5c21c21668e3eed056252380accd417c9c563e9294` |

The first three paths are relative to `infra/03-security/openbao/`.
Independent code review passed the frozen source and the proposal correction.
Independent security review passed the same seven source hashes and the final
proposal with no findings. Its trust/input/privilege/dependency verdict covers
only synthetic public preparation; W48-W54 remain unassessed and NOT_RUN.
Proposal ledger SHA256 is
`93ba0e325bd0cbc9e0ae5a1b923084a234feece3b94fdb814d72a2955294af32`.
Independent review also passed the result-only Task delta, including lifecycle,
lease reassignment, coverage limits and all remaining NOT_RUN lanes. Changed
file classification selected exactly8 files:2 Markdown,4 Python and2 JSON.
Commitizen4.15.1 message validation and the registered pre-commit4.6.2 staged
controller passed, exit0, including hardcoded-secret detection. Staged
`git diff --check` passed, exit0. The controller is rerun after this evidence
update on the exact commit index; any new failure blocks that commit.

Shared registration and navigation remain ignored proposals under
`.agent-work/p06-shared-proposals/registration.patch` and `base-blobs.json`.
Final patch SHA256 is
`44bae1efa9a35d31c805a55e98e85728ac80bf19de5f155bf66df83961829992`,
bound to readiness commitc940c2ac. Exact unchanged base blobs are workflow
contract `7dc037023853a003ef38a53d21e2c8d1ac0dd3b4`, Script Manifest
`a4ebf87ef288e9b5c4830eac22b4e2dba800b44f`, OpenBao README
`9e060dfeb3402c28fd2efd2ac5e807c11ae6a55d`, ops README
`6f4fb0694eec94c1861e20ce7ab3dae55c345b2c`. The manifest maps the library
to its unit importer and CLI to subprocess contract tests; workflow proposes
both modules on repository-integrity regressions. Their consumer is the
dedicated CLI/README; rollback removes only these four proposed hunks.

An owned isolated fixture at `.agent-work/p06-registration-qa` applied these
proposals without modifying P06's shared files. Initial manifest checks failed
paths-unsorted, then tests-unproven; correcting alphabetical insertion and
mapping only the direct library test produced manifest PASS, exit0. Workflow
contract passed5 workflows/7 jobs/8 actions, exit0. All-document links on the
tracked fixture, including new README, passed1196 documents/failures0 with
one pre-existing historical capture warning, exit0. Changed metadata selected
Task and README with violations0, exit0. The registered changed-profile
`--explain` returned the local plan, exit0; no aggregate gate execution or
hosted CI is claimed. The proposals require sole-integrator combined-head
validation and are not installed registration on this branch.

Focused verification commands at the P06 root (final results exit0):

```sh
rtk env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python \
  -m coverage run --rcfile=.agent-work/p06-coverage.rc -m unittest \
  tests.lib.ops.test_openbao_consumer_migration \
  tests.validation.test_openbao_consumer_migration_contract -v
rtk /tmp/hy-home-p09-qa/bin/python -m coverage combine \
  --rcfile=.agent-work/p06-coverage.rc
rtk /tmp/hy-home-p09-qa/bin/python -m coverage report \
  --rcfile=.agent-work/p06-coverage.rc
rtk ruff check scripts/lib/ops/openbao_consumer_migration.py \
  scripts/operations/openbao-consumer-migration.py \
  tests/lib/ops/test_openbao_consumer_migration.py \
  tests/validation/test_openbao_consumer_migration_contract.py
rtk /tmp/hy-home-staged-style-tools/bin/cz check --message-length-limit 75 \
  --commit-msg-file .agent-work/p06-source-commit.txt
rtk env PATH=/tmp/hy-home-p09-qa/bin:/home/hyunyoun/.local/bin:/home/hyunyoun/.nvm/versions/node/v26.10.0/bin:/usr/local/bin:/usr/bin:/bin \
  bash scripts/validation/run-ci-precommit.sh --mode local-staged
```

Ignored coverage configuration uses branch=True and patch=subprocess with
only the library and CLI in its measurement scope. Shared checks were run
from the isolated fixture using `check-script-manifest.py`,
`check-github-workflow-contract.py`, and `check-document-links.py --mode all`;
only the selection preview used `run-ci-gate.py --profile changed --explain`.
No runtime, private copy, deletion, rotation, resource or remote action ran.

Two later metadata runs failed, exit1, each with146 diagnostics: the newly
added shared-proposal Evidence row first used a composite Work Unit, then
paired criterion8 with W47. Each invalid Spec Package also exposed145 archive
type diagnostics. The corrected row now binds only criterion20/W47; W55 and
criterion8 remain in the pending Delivery row. No archive was changed. Final
metadata revalidation must pass before the logical source commit.

### P02 Integrated Public API Binding

The user's next handoff delivers P02 functional source
`962e11be50260a3dce2e2700b22951fce1b3f4f7`, synthesis
`ab346b2c9a329731af3fff74be651531d87067cc` and clean local main
`08b009a9ce0f288926f2edc4eebcbc5fb475d1e5`, preserving P01 main
`6d1d6960e59c316fad2c6d168d853989da565faa`. P06's clean two-commit series
was rebased onto08b009a9 with no conflicts, exit0. Historical readinessc940
and sourceeb0e8ad are preserved in Git and prior evidence; their replayed
commits are `d134c5dd0634593e1e296968acb70dea8482edde` and
`42a82e19161368ee9d997c0f4b299da68f373ae1`. Both962e11be and6d1d6960 are
ancestors of the P06 candidate, confirmed by `git merge-base --is-ancestor`,
exit0. Original checkout's24 unrelated worker paths remain untouched.

This is a W47 compatibility continuation under the existing exclusive lease.
Root alone writes the dedicated library, existing unit test, dedicated README
and this Task. P02 API/schema/catalog, shared files and P01 tracked documents
remain read-only. Read-only planning independently approved test-only API
binding; no production loader/factory or approval interface is introduced.
Nullable source/mount/path/field annotations now match P02's public schema.

The existing test owner calls P02 `load_catalog(ROOT)` and preserves issued
IDs, tuple consumers, nullable destinations, classifications and dispositions
in frozen test-only rows. It does not parse a second catalog or resolve aliases.
Six new cases prove current rows are not copy-approved, IMPLEMENT does not
approve a destination, COMM-003 cannot select COMM-002, PG-020 retains its
recovery hold, candidate hash/revision drift stops before lookup, and P02
rejects a fabricated approval in an isolated in-memory negative fixture.
No fixture is written to the authoritative catalog or assigned an opsflow ID.
The existing guards already enforce these refusals; no production behavior
was added and no new RED failure is claimed. Prior W47 RED/GREEN stays above.

Observed API result on candidate42a82e19: schema1.0.0,145 issued entries,
one COMM-003-to-COMM-002 alias, all destination statuses BLOCKED_P01,
PG-020 RETAINED_FOR_RECOVERY, and COMM-002/003 generation_allowed false.
The recurring tests compare issued IDs dynamically, not against a fixed census.
First focused run passed22 tests, exit0; after the final IMPLEMENT boundary
case, subprocess-instrumented verification passed23 in19.176s, exit0.
Dedicated branch coverage remains98percent (library99/CLI93), exit0.
Scoped Ruff passed the two changed Python files, exit0. A public observation
using system Python failed before validation because referencing was absent;
the existing `/tmp/hy-home-p09-qa/bin/python` environment rerun passed, exit0.
No dependency or validation contract was changed to mask that environment gap.

Public raw input SHA256 fingerprints are catalog
`a069d84360fdad0da16bd415c80019aa78859a137cdb1ba1fe50aa2882f7e141`,
schema `c044474d26a7f6f16f41d32fe07ca2dd34c08c0a3a3513f890717a7cf510582d`,
API `89602c6da2c48b341d913c7582780c29ca9bcd3b44f5d8946105551c62eeb52d`.
These are compatibility fingerprints, not W48 authentication. P02 loading also
depends on its public metadata/support files and internal I/O/helper contracts.
An accepted revision/digest-bound selection/approval interface, exact approved
IDs, KV destination, ACL and delivery are still missing. W48 executor and all
actual pilot/authority/recovery/deletion/rotation lanes remain NOT_RUN.

Shared proposals were regenerated under
`.agent-work/p06-p02-binding-proposals/` against08b009a9, leaving the old
`.agent-work/p06-shared-proposals/` history unchanged. New registration.patch
Final SHA256 is `4b5031a10d490d6300dc9a27ed9e9369ca2f77c2390b54f55ff3b367e3118ad7`;
base-blobs.json SHA256 is
`351b4a698c10c6f14cf629eb302135984f32096af310791576b857e7d5a79eb6`.
Base blobs: workflow `2c97d82fa7dfd73b56ec247dc72d5ef2625968e4`, manifest
`ff28ade87857c092768b8a5765f4aa3b4bee0aa9`, OpenBao README
`312cd463ba9f2c8160e71b753133fa4645da872c`, ops README
`9d0e057de8728c586849e4b310c03dd38c6958d8`. P02 and prior regression
registration remain present. The coordinator owns final shared integration;
P01 owns adjustment of its current documents against historical P02 proposal
71907ca6, which is not applied to current main. CLI RUN-0085 remains authority;
its proven consumer stays the actual subprocess test until P01 adds a runbook
invocation and the coordinator validates that manifest delta.

Final public-source verification used detached candidate42a82e19 under
`.agent-work/p06-p02-binding-qa`, with only the four owned deltas and shared
proposal staged there. Manifest validation passed, exit0. The final workflow
contract passed, exit0 (5 workflows/7 jobs/8 actions). The live shared files,
P02 source/catalog/generator and P01 tracked documents remain unchanged.

The registered command `run-ci-gate.py --profile changed --local-only --explain`
selected17 leaves, exit0. The same command without --explain ran once and
returned exit1: compose-baseline's544 tests had two permission failures.
Both fixture entrypoints (OpenWebUI/Gatus) had checkout mode0775, unchanged
HEAD content and tracked100755. Only their disposable fixture modes were
corrected to0755; live checkout modes/content and both indexes were preserved.
The original aggregate FAIL remains in p06-p02-binding-local-gate.log.

The unchanged canonical loader/validator/planner and execute_execution_plan
then ran the selected suffix from leaf.compose-baseline-regressions, with no
alternate executor or environment skip. Compose544 passed in127.173s,
skipped71; contract27 passed. Runner60 then failed two own-leaf routing
subtests: the proposal lacked changed_root_rules for the two P06 test paths.
This recovery returned exit1, preserved in
p06-p02-binding-local-gate-recovery.log. The initial proposal b2c6571f and
ledger3703a73e remain as registration.initial.patch/base-blobs.initial.json.

The final proposal adds the same four exact P06 prefixes to changed_root_rules
for the existing repository-integrity leaf, preserving prior registrations.
After workflow validation, the canonical selected suffix from the affected
leaf.ci-gate-contract-regressions ran all eight remaining nodes, exit0:
contract27, runner60, adapter42, workflow38, control-plane59, staged-controller
regressions, release18 and repository-integrity388 (96.313s) all passed.
Its receipt is p06-p02-binding-local-gate-routing-recovery.log. Earlier
unchanged leaves retain PASS: hook15, candidate preflight, links, lifecycle15,
metadata142, governance655, supply-chain263 and conftest18. Thus all17 selected
leaves have successful local evidence; no full aggregate exit0 is claimed.
Opt-in skips are not native acceptance. Links inspected1196 documents/11614
links: failures0, one pre-existing historical capture warning, exit0.

Worker reviews approved the four owned source deltas. Coordinator re-review
of69be0b5e accepted the implementation but found P2 omissions in the final
common proposal: the canonical schema-folder route and complete library
consumers/tests were missing. The finding-free common-review claim is
superseded. Fresh common integration and affected-gate acceptance are pending. The historical W47 input69be0b5e owned SHA256s
remain helper `4c61cf97cb6ba8bf91a4fcdb52d4009d03558c15ad262d8faac4fcfd61322464`,
test `66c9f68be5a134e10d9ae98a427865082b024df5253a27cf5a9142ee0332c3f2`,
README `695be452cfdc0c1f08cdf77b71cb4f0dbe71007c2fa9e93f54c585376d0dcb70`.
Dependency audit of scripts/requirements.txt first failed because the system
Python lacked ensurepip, exit1. An isolated-cache pip-audit of the actual
/tmp/hy-home-p09-qa/lib/python3.12/site-packages passed, exit0, with no known
vulnerabilities. No advisory was ignored or dependency/global tool changed.
This QA-environment audit does not assert production dependency acceptance.

A fresh read-only git ls-remote origin refs/heads/main observed
`08b009a9ce0f288926f2edc4eebcbc5fb475d1e5`, exit0, newer than the supplied
6d1d6960 remote snapshot. This observation is not hosted CI evidence.
These final result-only Task additions receive minimum metadata/diff checks;
no link destination changes or implementation rerun are required. The reviewed
final index still requires run-ci-precommit.sh --mode local-staged immediately
before the ordinary commit, with its observed receipt retained under ignored
.agent-work. Commitizen4.15.1 accepted the prepared message, exit0.

No P06 main integration, push, PR, hosted CI, deployment or operational action
is claimed by this continuation. SMTP01 remains COMM-003's sole executor;
cooperative inherited locks do not quiesce CLN or nonparticipating writers.

### Assessment and Next Work Units

All eleven supplied reference files were read and extracted only under ignored
`.agent-work/p06-reference-audit/reference/`. Ten reference tests passed using
fake Bao and synthetic temporary files; they contain no native HTTP/TLS/CAS
server, actual Agent, database, S3 or recovery proof. Do not copy the reference
classifier/catalog/schema, P04 workflow library or P01 Agent. Its schema_version1
and eight-column parser conflict with P02's closed1.0.0/current parser; its
copy client lacks ambiguous-write reconciliation. These gaps are RED cases
for the dedicated implementation, not reasons to weaken existing contracts.

1. W46: freeze baseline, parent interfaces, exact proposed pilot and owners;
   inspect changes without touching other sessions; meaningful RED cases first.
2. W47: closed public wave/receipt schemas and injected synthetic selection;
   then bind integrated P02 API and exact schema/source hash, preserving IDs.
3. W48: bounded CLI/copy implementation with CAS/readback, whole deadline,
   TLS/proxy/response/file/identity/privacy failures; no secret hash receipt.
4. W49: P01/P03-approved per-consumer renderer/delivery proposals, version and
   negative readiness; native evidence waits for exact selected contracts.
5. W50: one real P04 existing DEV/S3 pilot after all admission conditions.
6. W51: scoped rollback, independent empty restore, fresh reauthentication and
   integrated regeneration guards, then management authority acceptance.
7. W52: only approved additional consumers sequentially, with separate receipts.
8. W53: fresh five-axis proof and named SMTP/CLN/service removal after recovery.
9. W54: one independently identified server rotation unit and denial/rollback.
10. W55: shared registration/docs, current-head QA/review/PR and downstream SHA.

### Segmented Local Source Validation — 2026-10-11

Frozen source input is `5b1a92db48fd508feff4cee0753b3b4468dd41dc`, following
common/worker integration `c7d56a383ad8b77dd615327d11605b3e15d2146e`.
The registered local execution plan has33 nodes; public explain exposes10.
The front-door run exited124 after nodes0–9 passed. First canonical continuation
exited1 at node18; nodes10–17 passed. Permission-corrected continuation exited1
at node26; nodes18–25 passed. Final continuation26–32 exited0 with ordinary
Python, debug true/optimization0 and clean unchanged post-input. Thus all33
nodes have segmented successful receipts; the original124 and both suffix1
failures remain failures. No fresh aggregate exit0 or hosted PASS is claimed.

Only two coordinator-checkout entrypoint modes changed775 to755, matching their
tracked100755 modes: Open WebUI and Gatus. File content hashes and index were
unchanged, with Git clean and no HOME/runtime effect. The only source delta
from c7d56a383 is the synthetic workflow fixture's canonical working directory,
seven changed lines in the existing test. RED: one test/four subcase failures,
exit1,1.769s; GREEN:39 tests,exit0,7.492s; Ruff/staged checks exit0 and independent
review ACCEPT. The registered workflow contract SHA256 remains
`bdb1941e522865a9a381b0913f4a8e266dfb613cbb832ca35889ff26ac3ecfc5`.

Receipts are `.agent-work/p04-p07-registered-suffix-final-fixture-result.json`,
`.agent-work/p04-p07-checkout-permissions-repair.json` and
`.agent-work/p05-fixture-cwd-receipt.json`; final output is
`.agent-work/p04-p07-registered-suffix-final-fixture.log`. Earlier aggregate and
suffix logs remain preserved. These SOURCE/UNIT/STATIC checks do not complete
operational criteria. Local-main source integration awaits final documentation
checks and review; its delivery SHA is not yet known. Current direct-user
local-main delivery uses no dev, remote push, PR or hosted execution.

Worker source `8a9f6bf12e04599b7861a04372274cbc9676a758` contains current W48
synthetic preparation. Its SHA256s are helper
`a40eb677172847a817e4b607d3abc6a10696665c8204fca366ac61ac38d6e831`, unit test
`854013518aab1d437d62e80e5bfc18f90a8cfebde7ac3b476f6778bd6ab71594` and README
`11afbb5a1fb15886b2296e624616487dd25504c530149ca4823a7bc4081373f0`.
The earlier4c61/66c9/695b full hashes remain historical W47 input69be0b5e;
they are not current W48 bytes. Coordinator preservation checks confirmed both
input histories without replacing the historical record.

Fresh coordinator P06/P07 four-module checks passed62 in16.592s, exit0;
196 P04/P05 tests are separate workload-source evidence. The earlier98percent
coverage remains worker evidence, not a fresh coordinator measurement. All
criterion20 real-copy/renderer/pilot/authority/deletion/rotation and recovery
lanes remain pending/NOT_RUN. SMTP retains COMM-003's sole retirement executor.
The final repository leaf passed494 tests/127.874s, exit0; neither it nor local
source integration authenticates production selection or supplies a real copy.

### W48 Runtime Primitive Preparation — 2026-10-14

The direct user request now authorizes concrete deployment, issuance,
migration, retirement, recovery and related development cleanup; the latest
steering prioritizes P01. Exact operational targets and physical inputs still
must exist. The user reports independent custody or holders need preparation
and asks for investigated target choices. No provisional catalog path is
promoted to an approved destination, no real pilot is selected or copied.

Base main/origin were `1e7e2ba841c4e428a06762a61a570011711bc1ef`.
The six-file frozen source packet is manifest
`5539f188775cc9d9f9d262564fc4fe4b33b940c53d0a82c7467a6d7caac9f24e`:
lexically sorted repository-relative `path SHA256` rows with final LF. It
contains migration API, two private I/O/transport modules, unit/runtime tests
and the direct consumer-migration README. The coordinator integrates manifest
runtime classifications, both existing CI selection maps and existing family
README navigation; validation CLI behavior remains unchanged.

The primitive consumes separately bound source, copy-token, metadata-token
and CA files. It rejects lexical role aliases before private reads and held
inode aliases before HTTP, requires distinct token bytes, immutable verified
CA, strict DNS origin plus separate numeric connection IP, no proxy/redirect
or ambient auth, bounded HTTP/JSON and total request budget. Copy preserves
UTF8 bytes including whitespace; non-UTF8 inputs fail closed. Genuine absent
KV-v2 data and metadata are checked before CAS0; equal existing is NOOP,
conflict/history is blocked. Each POST is single-attempt; bounded readback
separates `write_attempted`, acknowledged `accepted_version` and observed
`kv_version`. Post-write uncertainty remains PARTIAL, including cleanup errors;
pre-write cleanup failure remains BLOCKED with observed NOOP evidence retained.

Initial missing-executor RED failed. The original 54-test packet passed93%
coverage but independent review failed role alias, write-provenance and DNS
origin validation. Narrow correction RED recorded five cases/14 assertion
failures, plus one unexpected POST exception failure. A full corrected60-test
run initially had one old version assertion failure; the corrected freeze
passed60, but review found a separate ExitStack-close defect that discarded
completed write evidence. Its focused RED had2 failures; final fixed source
passed62. These failures remain historical, with final exact-input review
resolving the identified source findings only.

Independent QA command:

```sh
rtk /tmp/hyhome-p04-qa-tools/bin/python -m unittest tests.lib.ops.test_openbao_copy_runtime tests.lib.ops.test_openbao_consumer_migration tests.validation.test_openbao_consumer_migration_contract -v
```

Exit0,62/62 PASS,skip0,38.680s. Worker final branch coverage93% (I/O90%,
transport95%,migration94%); scoped five-Python Ruff/format and diff passed.
Direct README metadata selected1/violations0. Independent code/security
review approved the final six-file input, including close-failure provenance
and fixed diagnostics. System Python attempts missing `referencing` remain
recorded environment failures, not source PASS; the configured QA environment
supplies the actual full receipt.

The first coordinator runtime-registration proposal failed independent review:
retained runtime rows pointed to a README instead of the required Operations
Runbook authority, and one consumer list was unsorted. The narrowed correction
uses RUN-0085 for runtime rows and lexically sorts the internal I/O consumers.
Final manifest and combined gates/review remain required; this source-only
registration defect changes no runtime or credential.

The r2 combined QA then found that RUN-0085 was still draft and did not
directly name the two runtime modules. P01/TSK-0006 owns the minimal authorized
Runbook activation after independent rules review: a current reusable
procedure is not evidence that deployment occurred. RUN-0085 now directly
governs the runtime API and private HTTPS transport, while preserving the
validate-only public CLI and missing production adapter/controller factory.
The exact activation/link delta and affected registered gates remain under
review. This is an authority binding only; every private/native copy,
renderer, pilot, authority transition, recovery, removal and rotation remains
NOT_RUN. It does not complete criterion20 or admit direct library invocation.

This is partial W48 source/API implementation: public CLI stays validate-only,
production P02 selection/adapter and P01 limited token/ACL/TTL/custody binding,
controller authorization, renderer delivery, native pilot, authority change,
rotation and recovery remain NOT_RUN. Callback input is not a JSON approval.
Criterion20 remains pending; code or unit approval is not HOME acceptance.

### W49 First-consumer plan and verifier — 2026-10-27

The owner chose "Plan + first consumer": inventory the Agent-rendered
consumers, write a value-free cutover/rollback plan and a consumption verifier
for one of them, and stop before any HOME cutover.

The Agent renders only the Keycloak and Grafana admin passwords. Both services
still read the repository-local `./secrets/` files through Compose file
secrets; nothing consumes the Agent output yet, and both values only seed the
first boot. Grafana is the pilot: OIDC with the login form disabled leaves the
admin password as a break-glass path, while Keycloak serves sign-in for every
other service. Metadata-only reads found the blocker: the Agent (UID 100)
renders `0600` files, which Grafana (UID 472, group 1000) cannot read, and
`health-agent.sh` requires `600`. Cutover therefore waits for a P01 change to
`0640` for the Grafana template and its health check, with an Agent recreate.

`consumer-migration/verify-grafana-consumption.sh` prints only check names,
PASS/FAIL, the rendered KV version and the login HTTP status. Bytes compare
inside two pipes; the login probe quotes the value inside Grafana and feeds
curl from stdin. The plan, rollback and the single-file bind-mount caveat are in
the consumer-migration README. The first synthetic run caught a real gap: a
mounted file holding only a newline passed `test -s`. An independent security
review then found no Critical/High issues and one Medium: an unvalidated
`GRAFANA_PORT` such as `3000@host` would send the password to another host. The
fixes validate the port and container names, compare after removing trailing
newlines only (as Grafana's `__FILE` read does, so CR counts), require a
non-empty rendered value, escape the user name, and scope the README's `0640`
step to the Grafana `.txt` file with a healthy Agent first. Final run: 9 tests
OK and shellcheck clean. An agent-side comparison of the live files was denied by the
session's permission classifier, so the pre-cutover run is the owner's:
`bash infra/03-security/openbao/consumer-migration/verify-grafana-consumption.sh`.
The Evidence table below is a frozen pre-generation-7 table that admits no new
rows, so this section is the W49 record: synthetic verifier PASS; the HOME
pre-cutover run, the P01 `0640` change, cutover and rollback remain NOT_RUN.

Owner pre-cutover run, 2026-10-27, on HOME with Grafana still reading the
`./secrets/` file: `rendered_version version=1`, `mounted_equals_rendered` and
`admin_login http=200`, all PASS, exit 0. The current file value therefore
equals the Agent-rendered KV value and is Grafana's effective admin password,
so the cutover changes the file's source, not the value. The P01 `0640`
change, cutover, post-cutover run and rollback remain NOT_RUN.

### W49 Grafana delivery source — 2026-10-27

Review before cutover found that the README plan's step 3 conflicted with
existing contracts. It said to repoint the root Compose `grafana_admin_password`
file at the Agent output. But `test_secret_metadata_sync` rejects `${…}` and
absolute secret paths, and `gen-secrets.sh` rejects symlinked or escaping
ones, so every Compose secret stays a real file under `./secrets/`. The owner
chose a directory mount instead. Grafana gets a read-only bind of
`${DEFAULT_SECURITY_DIR}/openbao/out/observability` at
`/run/openbao/observability`, and `GF_SECURITY_ADMIN_PASSWORD__FILE` becomes
`${GRAFANA_ADMIN_PASSWORD_FILE:-/run/secrets/grafana_admin_password}`. That
leaves today's behaviour unchanged when the variable is empty. Being a
directory bind, it also follows Agent re-renders, which removes the
stale-inode caveat. The Agent renders only the Grafana `.txt` at `0640`, and
`health-agent.sh` requires `640` for that file and `600` for the Keycloak file
and both `.version` files.

The verifier now reads Grafana's `GF_SECURITY_ADMIN_PASSWORD__FILE`, accepts
only those two paths, and prints it as `consumed_file`. Checks:

- consumer-migration and Agent contract suites, 37 OK, including new exact-mode
  and template-perms cases;
- update-gates and workflow bundle OK after the observability Compose
  `include_inputs` rehash, with 13 row source hashes updated;
- secret metadata, service wiring, Compose baseline and SEC01 version suites
  all pass;
- hardening for `03-security` and `06-observability` PASS; shellcheck clean.

The Agent and Grafana recreates on HOME, the cutover run, and the rollback run
follow after merge.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git baseline | 1, 20 | W46 | status/worktrees/ls-remote/open PR and main CI | Localf754 / remote4e26 | PASS | Read-only baseline; no remote write | - |
| Reference audit | 20 | W46 | Eleven files and synthetic pytest | Prompt0d11d0fd04ba; inputf754 | PASS | 10 PASS,0.24s, exit0; command below | - |
| Selection schemas | 20 | W47 | RED/GREEN public closed-input cases | c940c2ac plus frozen seven-file hashes above | PASS | 17 synthetic tests; dedicated coverage98percent | - |
| Shared proposals | 20 | W47 | Historical worker manifest/workflow/links fixture | c940c2ac plus patch44bae1ef | PASS | Historical isolated fixture; current P2 review supersedes delivery acceptance | - |
| Current common proposal review | 20 | W47 | Canonical folder route and manifest relations | 69be0b5e plus patch4b5031a1 | FAIL | Coordinator independent findings; corrected common integration pending | - |
| Corrected coordinator common integration | 20 | W47 | Both routing maps, direct graph and registered gates | local02078085 plus worker69be0b5e; common hashes in Work Log | PASS | Source-only: six affected leaves exit0; repository430; full aggregate NOT_RUN | Current common proposal review |
| Independent source review | 20 | W47 | Code and security review | Frozen seven source hashes only | PASS | No source findings; common proposal reviewed separately; operational scope unassessed | - |
| P02 API compatibility | 20 | W47 | Actual public API load and synthetic binding refusals | P02 source962e11be integrated in08b009a9; candidate42a82e19 | PASS | 23 tests; production selection/approval interface pending | - |
| Synthetic KV decisions | 20 | W48 | Pure hypothetical state/phase/version guards | combined4c83f14b plus owned unit delta | PASS | 32 unit/CLI tests;98% coverage; no copier, approval or operational receipt | - |
| Production copy binding | 20 | W48 | Operational P02 selection, P01 credential/custody and controller authorization | Native authorization/catalog prerequisites pending | NOT_RUN | Reviewed bounded primitive exists; production adapter and actual copy remain absent | - |
| Renderer delivery | 20 | W49 | Version/inode/identity/reload/LKG failure proof | P01/P03 facts pending | NOT_RUN | Reuse their sole-owned contracts | - |
| Real pilot | 20 | W50 | Actual DEV ingest/S3 canary | P01/SEC/P02/P03/P04 gates pending | NOT_RUN | No resource, token or value action | - |
| Authority and recovery | 20 | W51 | Rollback/snapshot/empty restore/reauth | No reviewed exact target | NOT_RUN | No authority transition | - |
| Higher waves | 20 | W52 | Sequential actual consumption/recovery | Pilot acceptance pending | NOT_RUN | No bulk import | - |
| Old-copy removal | 12, 20 | W53 | Five-axis evidence and owning executor | No eligible exact target | NOT_RUN | No private unlink or metadata change | - |
| Rotation | 20 | W54 | Actual server/native-copy change and denial | No selected exact server | NOT_RUN | Same-value copy is not rotation | - |
| Delivery | 8, 20 | W55 | Registered QA/review/latest-head PR/merge | No P06 PR | NOT_RUN | Dedicated source checkpoint; combined registration/CI pending | - |
| Segmented source checks | 8 | W55 | Registered local nodes0–32 across preserved runs; final continuation26–32 exit0 | c7d56a383 then5b1a92db; unchanged registered contract | PASS | Segmented Local Source Validation; original aggregate124 and suffix1/1 preserved; final docs/delivery pending | - |
| Initial runtime primitive review | 20 | W48 | Independent role-alias, write-provenance and DNS findings despite54 unit PASS | manifestd9174e21 | FAIL | W48 Runtime Primitive Preparation — 2026-10-14 | - |
| Intermediate runtime close review | 20 | W48 | FD cleanup discarded completed write facts despite60 unit PASS | manifest412e62c9 | FAIL | W48 Runtime Primitive Preparation — 2026-10-14 | - |
| Corrected runtime primitive review and QA | 20 | W48 | Independent code/security approval;62 unique tests/0skip;93% branch coverage;Ruff/format/diff/README metadata | manifest5539f188 | PASS | W48 Runtime Primitive Preparation — 2026-10-14 | Initial runtime primitive review, Intermediate runtime close review |
| Runtime registration review | 20 | W48 | Independent runtime-authority-invalid and unsorted consumer list findings | manifestb44de862 proposal | FAIL | W48 Runtime Primitive Preparation — 2026-10-14 | - |
| Runtime authority activation binding | 20 | W48 | P01-owned RUN-0085 activation and direct runtime links; rules lifecycle/authorization assessment only, final delta/gates pending | Current direct user authorization; common r2 findings | NOT_RUN | W48 Runtime Primitive Preparation — 2026-10-14 | - |
| Actual runtime copy admission | 20 | W50 | No approved operational P02 destination/P01 token/custody/native canary | User requests investigated choices; P01 physical inputs pending | NOT_RUN | W48 Runtime Primitive Preparation — 2026-10-14 | - |

Actual reference command on clean inputf754, exit0:

```sh
PYTHONPATH="$PWD/.agent-work/p06-reference-audit/reference" \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 \
  /tmp/hy-home-p04-reference-qa.970sdfx3/bin/python -m pytest \
  .agent-work/p06-reference-audit/reference/tests -q
```

The existing isolated QA environment was reused, not globally changed.
Ten fake/file tests passed in0.24s; wrapper elapsed0.527s. At issuance no new
implementation RED/GREEN had run; W47's later synthetic results are above.
Real HTTPS/CAS/Agent, HOME, migration, deletion, rotation and recovery remain
NOT_RUN. SOURCE / UNIT / STATIC / ISOLATED / HOME / MIGRATION / ROTATION / RECOVERY /
DELIVERY must remain separate, with input SHA, exact command, exit, failure/
correction and receipt. Worker modules above plus affected P02/P01/SMTP/CLN
contracts select focused tests and meaningful80percent coverage; source unit
results never substitute for actual private consumption or deployment.

Before final source delivery, coordinator integrates existing manifest/workflow
registration and README proposals, then selects the registered changed profile
through `scripts/validation/run-ci-gate.py --profile changed`,
scoped Ruff/syntax and document metadata/links, git diff --check and the
registered run-ci-precommit.sh --mode local-staged on the reviewed index.
Native commands are selected only after the implementation CLI/test route and
exact target/input are frozen; this issuance does not invent an executable
production migration command. For a blocked lane, record the next exact
command and missing input once the owner has supplied its real interface.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 20 | pending | - | - |

## Review and Completion

Public work is in-progress through the observed lifecycle events above.
Source-only
delivery may proceed with operational lanes marked
NOT_RUN; it does not complete criterion20 or P06. Full completion requires the
selected actual pilot and accepted sequential waves, authority/recovery,
eligible-copy removal and separate selected rotation evidence. Unused, unknown
and retained-bootstrap/crypto material keep explicit dispositions.

Keep logical commits for schemas/selection, bounded copy executor/tests,
renderer binding, actual pilot/rollback/recovery receipts, targeted removals,
separate server rotation and docs. First integrate reviewed P02 source API;
its shared lock/generator repair is mandatory before cutover/removal. Rebase
the clean P06 branch onto the delivered issuance/main/dependency SHA while
preserving owned work. Integrate P01/P03/P04 facts and shared proposals through
their single writers; revalidate the combined head rather than sequentially
applying colliding manifest/workflow patches.

After current-head registered checks and independent code/security/IaC/docs
review, form one SPEC-0204 P06 PR without unrelated unpublished dependencies.
Required hosted CI and review must match the latest head; changed inputs rerun
affected checks/review. No admin bypass or fake PASS. Record commit/PR/head/
merge SHA and actual operational state separately. Remove only delivered,
clean branches/worktrees after evidence preservation; dirty/undelivered ones
are never deleted to satisfy Stop. Coordinator issuance does not merge any
other worker's implementation or close its Task.

Hand P01 exact renderer/version/auth/restore findings; P02 final issued ID,
destination/ACL/delivery/state and regeneration proof; P03 actual identity/
mount/reload/endpoint and denial facts; P04 native PG/S3 and recovery receipt;
P05 native credential-copy refresh/rotation rules before its wave; SEC exact
artifact/version/security receipt; SMTP/CLN five-axis eligibility and sole
executor receipt; P07 measured render/resource behavior; P08 final subject0085/
README paths; P10 fresh end-to-end/cold-boot/restore acceptance fixtures.
Each handoff names final main/consumer/helper/schema SHA and separates actual
results from remaining NOT_RUN commands/inputs. P09 may consume value-free
readiness facts only. No Wiki implementation/resource/schedule, learning-app
planning, LAB runtime, external workspace or blog-data write is permitted.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Request reconciliation](../../0212-request-baseline-and-reconciliation/spec.md)
- [P01 authentication and recovery owner](tsk-0006-openbao-trust-bootstrap-and-recovery.md)
- [P02 catalog](tsk-0010-p02-secret-catalog-and-views.md)
- [P03 delivery and endpoint contracts](tsk-0011-p03-service-integration-contracts.md)
- [P04 actual opsflow consumer](tsk-0012-p04-airflow-manifest-pipeline.md)
- [P05 native execution copies](tsk-0013-p05-n8n-outbox-notifier.md)
- [SEC01 image/security](tsk-0009-sec01-stable-security-integration.md)
- [SMTP01 sole retirement executor](tsk-0005-cross-tier-contracts-second-round.md)
- [CLN01 eligibility](tsk-0007-cln01-material-retirement.md)
- [OpenBao source](../../../../infra/03-security/openbao/README.md)
- [Official KV-v2 CAS and metadata semantics](https://openbao.org/docs/secrets/kv/kv-v2/)
- [Official AppRole Agent wrapping](https://openbao.org/docs/agent-and-proxy/autoauth/methods/approle/)
- [Official path-based policies](https://openbao.org/docs/concepts/policies/)
