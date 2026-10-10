---
title: "OpenBao Trust Bootstrap and Recovery Task"
version: "0.1.0"
type: "sdlc/task"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0006"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-10"
---

# OpenBao Trust Bootstrap and Recovery Task

## Objective

Implement P01 before P06: native verified TLS, fresh AppRole authentication,
functional renderer readiness, HMAC audit and recoverable restricted snapshots.
Keep source, synthetic tests, real consumption and external custody separate.

## Inputs and Authorization

The current 2026-10-10 P01 user request authorizes the named OpenBao source,
clients, bootstrap/audit/recovery contracts, regressions, logical commits and
branch/PR/merge after checks and independent review. The subsequent `ok`
accepts an isolated exact 2.6.2 environment first. It names no HOME host/CA
path or verified external custody; no such state or permission is invented.
Only fresh synthetic data/credentials generated inside the invocation-owned
fixture are processed without output or secret-bearing argv/log/snapshots.
Real HOME credential reads/issuance, restarts, cold boot and restore await the
concrete host, impact and recovery facts. Existing bootstrap and snapshot
source is reused; old source-only/prompt/draft labels do not stop independent
work. LAB and all learning-app planning/implementation are excluded.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0006 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0006 | ready | in-progress | #w19-baseline-and-boundaries |
| SPEC-0204-TSK-0006 | in-progress | blocked | #w23-home-boundary-and-p06-hold |

### W19 Baseline and Boundaries

Clean main, HEAD and fetched origin/main equal
`1ee5d6707e3b75b61222baad0c51050c64e1b10d`. Baseline d19fbfde6-to-main has
only eight P00 document changes; relevant executable OpenBao source unchanged.
The cached exact image reports 2.6.2 commit dd9c19c37a878cf4a81b18efb8d6f0599c7da923,
image ID sha256:11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641,
linux/amd64. Docker server 29.8.2. Image has sh/bao/timeout/cmp, no jq/curl.
No HOME containers, auth files, private env, raw logs or secret values were read.

NO_CHANGE: image pin, Shamir method (ADR-0042), existing renderer data paths and metrics/snapshot
least-privilege policy paths, existing backup renewal/save code and snapshot
issuer procedure. TSK-0005 W13 and SPEC-0229 record historical source/isolated
success and pending owner token run, not current HOME recovery. The existing
POL-0085 single-file custody exception is not independent custody proof.

Confirmed gaps: HTTP internal listener/clients, HCL hardcoded port, sink-only
health, no wrapped reissue path, no tracked audit devices/capacity/failure proof.
The Plan exact writer map applies. No new Spec ID is allocated.

The root writer also owns `scripts/hardening/check-all-hardening.sh` (retire
its internal-HTTP requirement), `infra/06-observability/gatus` endpoint/CA
entrypoint changes, the existing backup missing-token failure branch,
`tests/validation/test_service_runtime_compatibility.py`, affected Gatus unit
fixtures, `infra/03-security/openbao/scripts/start-server.sh`, renderer role
metadata/version templates and issuer policy. These are the same atomic TLS/
bootstrap change, not extra engines or downstream consumer migration.

### W20 TLS and Fresh Renderer Authentication

Fresh root regression RED: four selected tests on the original OpenBao source
failed (TLS and missing-token failure assertions; absent audit/HTTPS scrape
fields). The same tests pass after the coherent source patch. Source material
paths remain a provisioning contract, not invented existing certificates.

Agent worker regression RED/GREEN was refreshed after independent review.
Exact-byte RED: 16 cases, three failures, test SHA
`493662b62c0e8730672209a5215e8bc9dc7646ee667ebdee9a2c260b6000de72`.
Exact-byte GREEN: all 16 cases PASS, test SHA
`2173b33c649e407702c102c3fabaf308cbd84424f912a62d142fb37450529560`.
Exact cached CLI help corrected the unsupported kv-metadata `-field` assumption;
health uses `bao read -field=current_version` on only two exact metadata paths.
Final permission RED: 21 cases, three failures, test SHA
`4fdca8299014c3b09d5b3d7ceef1fd2e5576be3596aab18e79314a614a79f33d`;
GREEN: all 21 cases PASS, final test SHA
`728bd3971614c9e1e58ba3009f9a0c89fc4cd7b2440a455e214a27011a29d28e`.
The cached native stat -c %a contract was verified before requiring 0600 on
all five token/value/version files. Eight calls each have a three-second bound;
Compose health timeout is 30 seconds.
Successful fetch, streaming byte equality and version equality are distinct
from application consumption. No plaintext scratch or Agent Docker socket.
Stopped-Agent mount inspection and both immutable image identities precede credential reading and four-argument wrapped issuance.

Independent reviews found and corrected private-key exposure through the
shared certificate root and helper-only wrapping enforcement. TLS material is
now outside DEFAULT_CERT_DIR, in DEFAULT_SECURITY_DIR/openbao/tls; only the
public CA is mounted into clients. Issuer policy requires 30–60-second response
wrapping server-side, while the helper requests 60 seconds. New guards first
failed, then passed. Read-only check-tls-material.sh validates explicit SAN,
chain, expiry, key match and native UID readability without emitting material.
The helper requires only exact readonly material files and no network/pull.

### W21 Audit and Snapshot Recovery

Independent IaC design verdict before mutation:
READY_FOR_SOURCE_AND_ISOLATED_IMPLEMENTATION. HOME recovery readiness remains
blocked: actual artifact/capacity/custody/host/roles absent. Current audited
system health is not functional readiness. Exact v2.6.2 tagged upstream sources
confirm native TLS, VAULT_ADDR override, wrapped SecretID creation-path check,
declarative audit and SIGHUP file reopen; no 2.7-only tls_auto_reload option
is used. One file backend is one failure domain, not redundant custody.

Fresh initial exact-image native engine/Agent/audit/recovery trial PASS in
108.137 seconds. This is superseded for final changed input by the expanded
client/preflight test below; it is not copied into a new input result.
Native observed audit metric TYPE is counter despite names lacking _total.
The new alert evaluates increase over five minutes; a public promtool fixture
proves no alert at 2m, firing at 4m and recovery at 10m. Initial promtool launch
failed because readonly /tmp blocked test storage; adding ephemeral /tmp tmpfs
allowed the same fixture to PASS. A full audit backend can block metrics too,
so scrape-down remains a separate cause-unknown signal; HOME notification
and rotation/capacity ownership are unverified.

Exact tagged docs' nested JSON audit example was rejected by the actual image.
Tagged command/server/config.go parseAuditDevices uses type/path/options; that
shape was applied and accepted by the engine. Neither HTTP nor audit bypass
was used to make the trial pass.

[Official release notes](https://openbao.org/community/release-notes/2-6-0/#v264)
identify GHSA-7m59-mp95-w6ph: expired unused SecretIDs can authenticate before
tidy on the selected image. A native short-TTL case reproduced acceptance;
explicit accessor destruction subsequently denied authentication. One-use
and wrapping reduce exposure but do not fix expiry. Later patches also fix
malformed audit-input plaintext and legacy unauthenticated root/rekey response
behavior on audit failure. Steady-state listener explicitly disables both
legacy endpoint families; normal string HMAC results do not prove every input.
No silent runtime upgrade or full lifetime/HMAC safety acceptance is claimed.
The owning runtime-update residual remains W23 in this package, not a duplicate
new Spec. HOME deployment and P06 are held until fixed-version verification.

Failed wrapped delivery's underlying SecretID accessor cleanup is unresolved;
the limited issuer is not silently broadened. Separate restricted cleanup
identity/receipt proof is required before HOME acceptance. Real offsite key/
unseal custody remains unverified; no external material is manufactured.

### W22 Verification and Delivery

Fresh affected unit run: 38 tests PASS (runtime compatibility, 12 Agent stub
contract cases and Gatus CA/identity entrypoint). First integration unit run
failed three affected cases for the new required Gatus CA trust input; fixtures
were updated and the public CA variable uses `_PATH`, not secret `_FILE` semantics.
The requirement's functional guard was retained. No historical run is reused.
The new tests are selected by the existing compose-baseline regression gate;
the native rehearsal is explicitly opt-in/optional in CI, never an implied
hosted runtime PASS. Infra scripts are outside the script manifest's admitted
roots; no spurious manifest owner is added. Existing hardening remains under
its registered owner. Independent security fresh final production run PASS: 54 tests in 12.169
seconds. Root registered-package focused run PASS: 55 cases in 11.996 seconds,
one explicit native opt-in skip; not a hosted native execution.
Changed YAML lint PASS and changed shell warning-level lint PASS.
Changed document metadata PASS: 9 selected, zero violations/overrides; the
new Task is blocked and Plan/Spec remain correctly blocked. Initial
full-skill fixture checks failed unsupported-input-graph and default lint diagnostics; those failures are preserved, not reclassified.
A second tracked-input skill fixture still reports unsupported-input-graph:
its generic graph adapter does not admit this repository's extends/top-level
networks/volumes. This is NOT a Compose PASS and the helper is not weakened.
A separate owned public-only projection of the five selected P01 services,
unchanged common-v2 inheritance, root network declarations and external secret-
name stubs renders with Docker Compose config JSON, all selected profiles:
PASS. No env_file inputs or private values are loaded/output. Direct standalone
leaf rendering failed on missing root secret/network declarations; an initial
core/local-only projection omitted selected profiles and failed the explicit
set assertion; neither is recast as success. Final projection activates all
selected profiles and validates TLS/health/memory scratch/nonprivileged state.
This is STATIC selected-source projection, not HOME activation/root census.
The first stable-input registered aggregate failed because this new Evidence
table used explanatory text outside its registered result/acceptance domains.
Those cells are corrected to canonical PASS/pending; scope stays in prose.
The propagated archive diagnostics do not authorize archive changes. The
aggregate is freshly rerun on the corrected receipt before delivery. Graphify refresh
NOT_RUN: report and CLI unavailable. No alternate undocumented graph authority was introduced.
Independent final code review caught the package invocation import failure
after the native fixture was split for the 800-line limit. The registered
module invocation failed before optional skip; its RED result is retained.
Explicit relative package imports and direct-discovery fallback corrected it;
the exact registered default invocation now passes with one opt-in skip. No historical or direct-
discovery skip is substituted for the registered package check.
Final code review also caught two delivery-boundary defects. A wrong server
container could receive issuer credentials before failing; immutable cached
image IDs are now checked on both containers before reading stdin. Its RED
18-test input SHA was 408da6da79979c14205df0e8877441ebb49416c9d83bd6e3990e912fc57248b2,
then GREEN 18 cases passed. A stale encrypted snapshot from a killed backup
could reach the next Restic/offsite run when the current token was absent;
the exact staging file is now removed before all OpenBao branch checks. The
seeded-stale regression failed first, then passed. Existing snapshot renewal
and save code remain reused.

Only the existing root OpenBao secrets-group exception row is amended: it now
names the exact TLS key bind, new audit write path, restricted custody and
unverified HOME permissions, preserving the historical 2026-10-09 observation.
No common-v2 implementation or LAB exception is changed. It is the same P01
source contract, not a duplicate P07 ownership claim. Permission readiness
checks are finalized with independent review before the final native input.
Superseded registered native input
`2622b6e5560c3d15387798a61b12a33eef29bee402ab6394c2ee0fa471fa6853`
passed in 188.827 seconds before the cleanup failure-path correction.
Final registered native input
`e4bde131a34928e19266ddc6dbe86ecc78ccc4ef895d44f39666f60e2e2a9fee`
PASS: two tests, exit 0, 189.952 seconds. The unchanged-byte guard passed
and every owned container, volume, network and temporary directory was cleaned.
It exercises all six native client trust cases, both SANs/expiry/preflight,
server-enforced wrapping/immutable-image target binding, fresh Agent restart,
byte/version/0600 readiness, limited snapshot renew/save/empty restore/original
shares/foreign-share denial/restored-root revocation, HMAC normal-string data,
full audit filesystem request 500 versus health 200 and anonymous legacy POST
denials. The known expired-SecretID bad behavior is recorded separately.

The 181.776-second preceding trial failed because the fixture omitted the
leader-ready barrier after final unseal; it was repaired and freshly rerun.
Earlier capacity trial failed while allocated audit-file page space remained;
bounded fault-injection reads establish actual denial instead of assuming it.
No failure is copied as a PASS. The final reviewer then found an exception path
that could stop cleanup before remaining owned removals. Five failure-path
regressions first failed, then passed after cleanup accumulated errors while
attempting every owned removal. The final exact registered native run above
includes that correction; the default registered invocation exits 0 with
two discovered tests: one cleanup PASS and one native opt-in SKIP.

Final independent code, security and IaC reviews assess the frozen public
source, not historical drafts. Code, security and IaC accept SOURCE/STATIC/ISOLATED
with the W23 runtime hold; no remaining source-blocking finding is reported.
The public changed-input manifest contains 41 paths (excluding this receipt
Task to avoid self-reference), base 1ee5d6707e3b75b61222baad0c51050c64e1b10d,
SHA256 12d63451be3e30e3d50110c1a591b46dbffd92be17f9653f519a14d068a0b0cc.
No private input is part of either digest. A subsequent documentation-only
formatting correction removes two extra Plan blank lines and clarifies the
hidden-input prompt; the refreshed
manifest supersedes its Plan bytes without changing native inputs:
SHA256 de0335192b5779177758ff14a04643eeefd42cdac90467d07d5e56742c4aa6b0.

Fresh commands and environments:

| Command | Environment | Result |
| --- | --- | --- |
| `python3 -m unittest tests.validation.test_openbao_agent_contract tests.validation.test_service_runtime_compatibility tests.validation.test_gatus_oidc -v` | Local static/stub; independent reviewers | PASS 54; no native claim |
| `python3 -m unittest tests.validation.test_openbao_rehearsal -v` | Local registered default | Exit 0; 2 discovered, 1 PASS, 1 native opt-in SKIP |
| `HYHOME_OPENBAO_REHEARSAL=1 python3 -m unittest tests.validation.test_openbao_rehearsal -v` | Invocation-owned Docker 29.8.2, exact cached OpenBao 2.6.2, synthetic material | PASS 2 in 189.952s; byte guard and cleanup PASS |
| `python3 scripts/validation/run-ci-gate.py --profile changed --local-only` | Registered local selected leaves | Prior receipt-domain FAIL; full metadata contracts now PASS, aggregate fresh rerun pending |
| `bash scripts/validation/run-ci-precommit.sh --mode local-staged` | Isolated index snapshot; readonly style controller | Source and corrected documentation units PASS, including gitleaks; first docs formatting rejection retained |

Effective authority exercised is public repository source and synthetic
isolated Docker resources. Branch/PR delivery is authorized but not yet exercised. No HOME service, LAB,
private auth/configuration, credential migration or third-party notification
is used. Source delivery is distinct from runtime acceptance.

| State | Disposition |
| --- | --- |
| SOURCE | Implemented, independently reviewed; source commit 0853904c06830fb26e44a1ccb21ce8f377c184f5 |
| UNIT | PASS, including negative credentials/modes and cleanup failures |
| STATIC | Selected-source Compose projection, metadata/links/lint PASS; generic graph helper limitation retained |
| ISOLATED | PASS at final native SHA above, including synthetic restore/unseal |
| HOME | NOT_RUN; target/material/custody and runtime residuals unresolved |
| MIGRATION | NOT_RUN; P06 held, no real secret or consumer cutover |
| RECOVERY | ISOLATED synthetic proof PASS; actual HOME/offsite recovery NOT_RUN |
| DELIVERY | Local candidate prepared; actual remote checks and merge pending |

The logical source unit owns executable/client/policy/test/gate changes and the
existing root exception row; the documentation unit owns Spec/Plan/this Task,
OpenBao README and the five affected operating documents. Their paths are the
frozen public manifest, not LAB or unrelated surfaces. Each uses the W23
rollback boundary. Source commit: 0853904c06830fb26e44a1ccb21ce8f377c184f5
(33 executable/config/test/gate paths), input manifest 12d63451...a0b0cc,
UNIT/ISOLATED and read-only staged controller PASS. Native input is unchanged.
Documentation staged lint/format/secret checks PASS on its isolated index
snapshot; full document contracts PASS with zero violations. The initial
readonly controller detected formatting changes in its disposable checkout
and rejected them; after owned formatting fixes the fresh controller passes
without mutation. The ordinary native commit hook rejected the hidden-input prompt's token/colon
text as a generic credential assignment; no secret value existed. The prompt
is clarified to Enter limited issuer credential, with stdin/unset semantics
unchanged. No hook bypass or private configuration edit is used. Actual remote
receipts follow after candidate checks.

### W23 HOME Boundary and P06 Hold

HOME target/connection, CA/server material location and separate unseal/offsite
custody were requested without asking for values. User answered `ok` only.
HOME deployment, cold boot, real token issuance/use, actual encrypted snapshot
restore and custody verification remain NOT_RUN. P06 expansion and HOME deployment are held for both these missing facts and the known runtime residual.
Isolation is a synthetic recovery test, never a HOME or physical-host reboot.
SOURCE/UNIT/STATIC/ISOLATED/HOME/MIGRATION/RECOVERY/DELIVERY remain separate.
Before HOME activation, source rollback is a reviewed revert. After activation,
rollback must retain native TLS, audit declaration/log custody and verified
client trust through a reviewed override or fix-forward; never revert to HTTP
or remove audit to restore requests. Fixture cleanup removes only owned
names/paths and leaves HOME, LAB and user work untouched.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline | 1, 11 | W19 | status, refs, fetch, scoped baseline diff | 1ee5d6707e3b75b61222baad0c51050c64e1b10d | PASS | W19 Baseline and Boundaries | accepted |
| Renderer trust | 11 | W20 | Negative token/CA/modes, native clients and Agent restart | e4bde131a34928e19266ddc6dbe86ecc78ccc4ef895d44f39666f60e2e2a9fee | PASS | W20 and W22 | pending |
| Audit and recovery | 11 | W21 | Native audit-full denial, snapshot save/empty restore/unseal | e4bde131a34928e19266ddc6dbe86ecc78ccc4ef895d44f39666f60e2e2a9fee | PASS | W21 and W22 | pending |
| Public source review | 11 | W22 | Independent security and IaC; code review delta | de0335192b5779177758ff14a04643eeefd42cdac90467d07d5e56742c4aa6b0 | PASS | W22 | pending |
| HOME preconditions | 11 | W23 | Named host, CA and independent custody | User P01 and `ok` | NOT_RUN | W23 HOME Boundary and P06 Hold | pending |

## Review and Completion

Blocked on the named W23 target/custody and runtime residuals. Source and isolated proof do not complete HOME custody/boot/recovery
acceptance or authorize P06. No secret migration or consumer switch is claimed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [P00 Task](../../0212-request-baseline-and-reconciliation/tasks/tsk-0003-active-contract-and-exclusions.md)
- [OpenBao Runbook](../../../05.operations/runbooks/0085-openbao.md)
- [Backup Runbook](../../../05.operations/runbooks/0021-backup-and-restore.md)
