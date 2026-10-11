---
title: "P06 OpenBao Consumer Migration Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
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
| Selection schemas | 20 | W47 | RED/GREEN public closed-input cases | Issuance source pending | NOT_RUN | Independent worker owns implementation | pending |
| Copy executor | 20 | W48 | Synthetic CAS/TLS/response/file/privacy failures | P02 binding pending | NOT_RUN | No real copy or client implementation yet | pending |
| Renderer delivery | 20 | W49 | Version/inode/identity/reload/LKG failure proof | P01/P03 facts pending | NOT_RUN | Reuse their sole-owned contracts | pending |
| Real pilot | 20 | W50 | Actual DEV ingest/S3 canary | P01/SEC/P02/P03/P04 gates pending | NOT_RUN | No resource, token or value action | pending |
| Authority and recovery | 20 | W51 | Rollback/snapshot/empty restore/reauth | No reviewed exact target | NOT_RUN | No authority transition | pending |
| Higher waves | 20 | W52 | Sequential actual consumption/recovery | Pilot acceptance pending | NOT_RUN | No bulk import | pending |
| Old-copy removal | 12, 20 | W53 | Five-axis evidence and owning executor | No eligible exact target | NOT_RUN | No private unlink or metadata change | pending |
| Rotation | 20 | W54 | Actual server/native-copy change and denial | No selected exact server | NOT_RUN | Same-value copy is not rotation | pending |
| Delivery | 8, 20 | W55 | Registered QA/review/latest-head PR/merge | No P06 PR | NOT_RUN | Task issuance only | pending |

Actual reference command on clean inputf754, exit0:

```sh
PYTHONPATH="$PWD/.agent-work/p06-reference-audit/reference" \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 \
  /tmp/hy-home-p04-reference-qa.970sdfx3/bin/python -m pytest \
  .agent-work/p06-reference-audit/reference/tests -q
```

The existing isolated QA environment was reused, not globally changed.
Ten fake/file tests passed in0.24s; wrapper elapsed0.527s. No new implementation
RED/GREEN, real HTTPS/CAS/Agent, HOME, migration, deletion, rotation or recovery
ran. SOURCE / UNIT / STATIC / ISOLATED / HOME / MIGRATION / ROTATION / RECOVERY /
DELIVERY must remain separate, with input SHA, exact command, exit, failure/
correction and receipt. Worker modules above plus affected P02/P01/SMTP/CLN
contracts select focused tests and meaningful80percent coverage; source unit
results never substitute for actual private consumption or deployment.

Before final source delivery, coordinator integrates existing manifest/workflow
registration and README proposals, then runs affected scripts/qa.py changed,
scoped Ruff/syntax and document metadata/links, git diff --check and the
registered run-ci-precommit.sh --mode local-staged on the reviewed index.
Native commands are selected only after the implementation CLI/test route and
exact target/input are frozen; this issuance does not invent an executable
production migration command. For a blocked lane, record the next exact
command and missing input once the owner has supplied its real interface.

## Review and Completion

Issuance remains draft; use the existing lifecycle event contract when the
worker starts. Source-only delivery may proceed with operational lanes marked
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
