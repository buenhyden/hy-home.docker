---
title: "P06 OpenBao Consumer Migration Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0014"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P06 OpenBao Consumer Migration Task

## Objective

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git baseline | 1, 20 | W46 | status/worktrees/ls-remote/open PR and main CI | Localf754 / remote4e26 | PASS | Read-only baseline; no remote write | pending |
| Reference audit | 20 | W46 | Eleven files and synthetic pytest | Prompt0d11d0fd04ba; inputf754 | PASS | 10 PASS,0.24s, exit0; command below | pending |
| Selection schemas | 20 | W47 | RED/GREEN public closed-input cases | c940c2ac plus frozen seven-file hashes above | PASS | 17 synthetic tests; dedicated coverage98percent | pending |
| Shared proposals | 20 | W47 | Manifest/workflow/links and independent delta review | c940c2ac plus patch44bae1ef | PASS | Isolated fixture only; W55 sole-integrator application pending | pending |
| Independent source review | 20 | W47 | Code and security review | Frozen seven source hashes plus final proposal | PASS | No findings; operational scope unassessed | pending |
| Copy executor | 20 | W48 | Synthetic CAS/TLS/response/file/privacy failures | P02 binding pending | NOT_RUN | No real copy or client implementation yet | pending |
| Renderer delivery | 20 | W49 | Version/inode/identity/reload/LKG failure proof | P01/P03 facts pending | NOT_RUN | Reuse their sole-owned contracts | pending |
| Real pilot | 20 | W50 | Actual DEV ingest/S3 canary | P01/SEC/P02/P03/P04 gates pending | NOT_RUN | No resource, token or value action | pending |
| Authority and recovery | 20 | W51 | Rollback/snapshot/empty restore/reauth | No reviewed exact target | NOT_RUN | No authority transition | pending |
| Higher waves | 20 | W52 | Sequential actual consumption/recovery | Pilot acceptance pending | NOT_RUN | No bulk import | pending |
| Old-copy removal | 12, 20 | W53 | Five-axis evidence and owning executor | No eligible exact target | NOT_RUN | No private unlink or metadata change | pending |
| Rotation | 20 | W54 | Actual server/native-copy change and denial | No selected exact server | NOT_RUN | Same-value copy is not rotation | pending |
| Delivery | 8, 20 | W55 | Registered QA/review/latest-head PR/merge | No P06 PR | NOT_RUN | Dedicated source checkpoint; combined registration/CI pending | pending |

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
