---
title: "OpenBao Trust Bootstrap and Recovery Task"
version: "0.2.11"
type: "sdlc/task"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-13"
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
| `python3 scripts/validation/run-ci-gate.py --profile changed --local-only` | Registered local selected leaves | Prior failures preserved; final 11-leaf local candidate PASS at f6903c14f; actual final-head delivery receipt linked from PR #411 |
| `python3 scripts/validation/check-operations-catalog.py` | Local public source and current inventory | Initial hosted drift FAIL; nine-cell correction fresh PASS |
| `bash scripts/validation/run-ci-precommit.sh --mode local-staged` | Isolated index snapshot; readonly style controller | Source and corrected documentation units PASS, including gitleaks; first docs formatting rejection retained |

Effective authority exercised is public repository source and synthetic
isolated Docker resources. The two reviewed commits were pushed and PR #409 was created under the
authorized branch/PR delivery scope; actual checks remain separately recorded. No HOME service, LAB,
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
| DELIVERY | PRs #409 and #410 externally merged with their actual results preserved; final source delivery checks/merge owned by PR #411; HOME delivery NOT_RUN |

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

Source unit commit: 0853904c06830fb26e44a1ccb21ce8f377c184f5.
Documentation unit commit: 1510c3a6ab01dcb12b2c81dc5d1df4cacceda5de.
[Delivery PR #409](https://github.com/buenhyden/hy-home.docker/pull/409),
first candidate head 1510c3a6ab01dcb12b2c81dc5d1df4cacceda5de, hosted
run 38036201251: candidate-quality FAIL on nine stale current-inventory
Persistence/Env cells for the five changed services. Seven other hosted
checks PASS; issue-greeting/main-security SKIP. No failed result is called
success. The serial root writer updates those nine current-source cells only;
service membership/classification, historical table and LAB rows are unchanged.
The same operations-catalog validator now freshly reports PASS. The Plan
writer map owns this required source-accounting delta in W22. No executable
or native input changes. The corrected delivery manifest has 42 public paths
(excluding this Task), SHA256
0ad4409e92671a8a0e5c346cdb3488c3c7e702c4c4ded233b25069494f7d0ac5.
The prior 41-path digest is retained as pre-inventory evidence. This documentation
unit uses the same pre-HOME reviewed-revert rollback boundary. Before the correction push, PR #409 was externally merged by buenhyden at
2026-10-10T08:00:35Z, merge e31ba58c5849f7d2d39558ca074d40834f4b7f21,
head 1510c3a6ab01dcb12b2c81dc5d1df4cacceda5de. Its failed quality result
is preserved and not described as a checked merge. Fetch confirmed current
origin/main equals that merge. The correction commit bb63f27ed62ccf860aa8af2b8e5603dce481b12e
was retained on the original branch and cherry-picked into the clean new
codex/p01-inventory-receipt branch from actual origin/main as 633d285eb.
No reset/stash/clean or user work rewrite was used. A same-package follow-up
PR owns the nine-cell correction and delivery receipt; its fresh actual checks
must pass before the agent merges it. No second acceptance owner is created.

[Correction and final delivery PR #410](https://github.com/buenhyden/hy-home.docker/pull/410)
is based on actual merge e31ba58c5849f7d2d39558ca074d40834f4b7f21.
Its initial candidate c7217539175bcb107747ada367e88d8e1b33823d is published;
quality run 38036906048 was initially in progress, seven other checks PASS and
two explicitly SKIP. The same initial head subsequently completed: actual
candidate-quality PASS in 3m15s, eight hosted checks PASS and two SKIP.
This is evidence for c721 only; the following receipt head requires its own
hosted checks before agent merge.
The PR's final validation receipt and hosted checks/merge timeline are the
actual delivery evidence for the subsequent result-only head; no unobserved
future success is copied here. Independent delta review accepts all nine
inventory cells, preserves history/LAB and confirms native input unchanged.
The corrected three-file staged controller and operations-catalog are PASS.
The long registered local run additionally freshly passes 142 metadata tests
in 388.481s; remaining selected leaves are not predeclared PASS. Final results
are recorded on the linked delivery PR before agent merge. W23 and full P01
acceptance stay blocked regardless of source delivery.

### W22 Regression Contract Follow-up

PR #410 final head 14368bbee8885fe7dbaeceb7ed17db91414117a9 freshly
completed hosted checks: seven PASS, main-security SKIP; candidate-quality
run 38037242917 PASS in 3m7s. It was externally merged by buenhyden at
2026-10-10T08:28:06Z, merge 860ac1c3633eac9ad416fb1abd8a61a6e617ebd8.
The final test/receipt branch codex/p01-regression-receipt starts from that
actual origin/main. No reset/stash/clean or existing work removal was used.

The earlier 17-leaf local aggregate exited 1: its Compose leaf ran 421 tests
in 120.248s with one failure, two errors and 59 explicit optional skips.
Old assertions expected an Agent command, only short-form mounts and the
previous Prometheus generated-file list. An ordinary workflow contract run
also failed its old exact module roster. These failures remain evidence.
Direct adapter calls outside their registered runner were denied by their
environment contract (exit 2); they are not gate successes or bypassed.

The root writer owns exactly three existing regression files: Compose
baseline, DEV data boundary and GitHub workflow contract. The correction
asserts the wrapper entrypoint and absence of a Compose command override,
validates actual read-only wrapper/config mounts in both mount forms and
retains exact persistent destination bounds. DEV fixtures require the new
OpenBao discovery target while retaining DEV-state rejection checks. The
workflow roster includes both OpenBao modules; Agent and cleanup tests remain
mandatory, and only the native rehearsal class is optional. Production,
workflow configuration, native fixtures, LAB and consumer code are unchanged.
Independent delta code review reports PASS with no findings.

RED test SHA256 values (Compose / DEV / workflow):
32269bd0d3fbbf62f6c43b7eb18c396475ad104b84a7f869dc4bdd3924a934a7 /
84739c327fd415cfda2445f3ea5fb5b0f919dea361a5d2c714ed3942c01505fb /
7de06c661804f8b2c5e8eb75884a5d51144499eb095cb54851ec62f6e72b5ed2.
Final reviewed SHA256 values in the same order:
362acdc1791a79dfd68428d1903d86d3a8b3e058172800e807a9dfe65e56a3a7 /
1176c5e1a0a8042c54491508c366eef9d536a7b6f1c0768615c40e064a7fb69c /
5595fc193c4932b02b12b3f5fcbabf24f92253625cf156c9f0c75f22e3360a81.
The current public manifest has 45 paths excluding this self-referential
Task; SHA256 ef22f5f377a13185fb396e3b65e33debedf67108257dd3098a579c0292b1c35a,
base 1ee5d6707e3b75b61222baad0c51050c64e1b10d. The native input remains
unchanged at e4bde131a34928e19266ddc6dbe86ecc78ccc4ef895d44f39666f60e2e2a9fee.

Fresh corrected five-leaf registered local aggregate exited 0: preflight,
links, supply fixture (239 tests), conftest (18) and Compose baseline (421 in
119.188s, 59 optional skips). This selection preceded the workflow-test delta;
it is not represented as the earlier 17-leaf aggregate passing. Ordinary
module checks additionally passed CI contract 27, runner 60, adapter 42,
workflow 36, release checks and repository integrity 164 tests in 52.765s.
Independent focused delta verification passed eight tests; full workflow
verification passed all 36. Ruff formatting/checks passed all three files.
The frozen final branch receives a fresh registered changed-profile aggregate
and draft follow-up PR; their final head/results/merge receipt are recorded
on that actual PR before delivery. No future result is declared here.

This logical unit uses the same reviewed pre-HOME revert boundary. Remaining
HOME target/custody, native-version security and restricted failed-delivery
cleanup residuals stay in W23. No new acceptance owner or runtime success is
created by correcting regression expectations.

### W22 Final Registered Candidate Receipt

Regression unit commit f6903c14f64f71ae51356215e6b4322706a4954e changes
the three tests and this Task. Registered staged controller PASS, including
formatting/lint and secret checks, followed by ordinary native commit hooks.
Independent final receipt review PASS: exact four-file boundary, actual prior
merge, all RED/final test hashes and every public input digest independently
reproduced; no finding. The manifest digest is SHA256 of UTF-8 compact JSON
of the relative-path-to-file-SHA256 map, with sorted keys and separators
(',', ':'); it excludes this Task and contains no private inputs.

Fresh `python3 scripts/validation/run-ci-gate.py --profile changed --local-only`
on f6903c14f, base 860ac1c3633eac9ad416fb1abd8a61a6e617ebd8, exited 0.
All 11 registered selected leaves passed: local candidate preflight, document
links, supply-chain fixtures, conftest policy, Compose baseline, CI contract,
runner, adapter, workflow contract, repository-control-plane and precommit
contract. Compose: 421 tests in 119.025s, 59 explicit optional skips; supply:
239 in 81.894s; conftest: 18; CI contract: 27, runner: 60, adapter: 42,
workflow: 36. Expected negative-fixture error messages did not fail the runner.
Document links retain one existing historical-resolution warning with zero
failures. No earlier failed aggregate is reclassified by this fresh result.

[Final regression and delivery PR #411](https://github.com/buenhyden/hy-home.docker/pull/411)
was created as draft from the actual main merge. Its first reviewed head is
f6903c14f64f71ae51356215e6b4322706a4954e. This final receipt-only commit
adds the actual local results and PR link without changing any of the 45
reviewed public inputs or native input. The PR's final head check records,
validation description and merge timeline own the actual hosted/delivery
receipt before the agent makes it ready and merges it. Pending checks are
never copied as PASS; W23/full P01 acceptance remain blocked.

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

### Current P01 Continuation — 2026-10-11

This is the existing blocked P01 Task, not a new issuance or implementation
restart. Its artifact ID, created date, historical failures/receipts and W23
hold remain. The current user supplies a full P01 execution prompt and requests
prerequisite assessment, an independent worker branch, ownership and delivery
instructions. The assessment itself executes no real credential, backup,
restore or HOME action. Later matching operational authorization is reused
only after the concrete admission contract and independent review exist.

**Verified baseline.** Clean local main is
`728ec6379f193256cee342550e38479cf3ebfc56`; a fresh remote query confirms
`2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`, with no open PRs observed.
Local main has two coordinator documentation commits not yet on remote.
Root is detached at `a03c8930a` with 24 foreign entries; SEC/SMTP/P09 foreign
worktrees and their source changes are preserved. Do not stage, reset, stash,
clean or force-push them. The legacy `codex/p01-openbao-trust` at `bb63f27ed`
is retained; its inventory correction was already cherry-picked as `633d285eb`
and delivered via PR410. Do not reapply those patches or resume that stale
branch as the current source baseline.

The official stable release query reports v2.7.1, draft=false,
prerelease=false, published 2026-10-01T14:03:19Z; see
[the official release](https://github.com/openbao/openbao/releases/tag/v2.7.1).
Both declared server and Agent use
`openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf`.
The separately selected linux/amd64 fixture input is
`sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`;
never confuse that platform/admission input with the multi-platform digest.
SEC01 owns final image trust and CVE decisions; no newer-version result
waives security or HOME verification. Fresh value-free runtime metadata at
2026-10-11T01:17:52Z observes both HOME containers running/healthy on the
2.6.2 image identity. Healthy is not candidate deployment or recovery.

**Reuse and residuals.** NO_CHANGE applies to implemented native TLS/CA binds,
wrapped reissue, immutable target/source receipt checks, limited issuer and
separate cleanup policy, durable nonce journal, functional byte/version/0600
readiness, audit/HMAC declaration, snapshot and empty synthetic restore.
SEC01's submitted 2.7.1 isolated result (two tests, 177.078 seconds) remains
attributed to its submitted input; do not copy it into a current-head PASS.
Historical 2.6.2 proof and known bad expiry behavior remain preserved.

The current helper is `scripts/renderer-issuance.py` under the OpenBao family,
using `sec01_nonce`, `sec01_role`, `sec01_issued_at`, exact-role lookup/destroy
and a creation window. The prompt requests `issuance_id`; this naming/receipt
contract is a bounded IMPLEMENT residual, not a reason to replace cleanup.
Use a tested versioned compatibility change that preserves existing active
journals and receipts, rejects contradictory or duplicate metadata, and never
falls back to broad tidy/list deletion, wrap-revoke assumptions or admin rights.
Verify response loss/interruption/accessor destruction in the exact candidate
before HOME admission; stub policy matching is not native authorization proof.
Malformed JSON nonexposure is a specific case, not every malformed-audit advisory.

**Worker branch.** Prepare `codex/p01-openbao-recovery` at
`/home/hyunyoun/data/hy-home.docker/.worktrees/p01-openbao-recovery` from the
coordinator handoff commit after local-main delivery. Record its full SHA,
HEAD and clean state. Exactly one separately assigned P01 worker owns source
continuation; assessment reviewers are not additional implementers.

**Exclusive file ownership.** P01 owns OpenBao `scripts/` and `config/`, this
Task, `infra/03-security/openbao/README.md`, existing subject-0085 Guide/Policy/
Runbook, and these existing tests:

- `tests/validation/test_openbao_agent_contract.py`;
- `tests/lib/ops/test_openbao_issuance.py` and `test_openbao_issuance_trust.py`;
- `tests/validation/test_openbao_candidate.py`, `test_openbao_rehearsal.py`,
  `_openbao_rehearsal_fixture.py`, `_openbao_rehearsal_clients.py` and
  `tests/validation/fixtures/openbao-audit-alerts.test.yml`.

P02 exclusively owns catalog/schema and its dedicated tools/tests; it submits
0085/README catalog paragraphs to P01 instead of editing the same files.
SEC01 stops simultaneous edits of P01 helpers/tests and owns stable selection,
image trust/SBOM/CVE triage, ledger and generated version projection. SMTP01
owns COMM-002/COMM-003 conversion/retirement; CLN01 owns general deletion
eligibility. Both positive initialization/rollback consumers stay retained.
The coordinator is the sole final writer of OpenBao Compose, root Compose,
environment, gateway, Prometheus/Gatus/Alloy, backup/RUN-0021/RUN-0098,
shared validators/manifest/workflow, inventory/Registry and Spec/Plan.
P01 places exact-base proposals in ignored
`.agent-work/integration-proposal/README.md`; no last-writer replacement.

**Parallel now.** Public source/role/template review, versioned journal
compatibility, synthetic regression fixes, exact isolated-contract review,
HOME operator/receipt preparation and bounded 0085 documentation may proceed.
Native isolation uses only invocation-generated credentials and owned empty
volumes, internal network, exact cached candidate and existing cleanup; it
requires available host capacity, reviewed daemon/input identities and a
single native-job lease. Reuse unchanged-input receipts; rerun only when changed
source/admission inputs or missing coverage require it. Do not run concurrent
SEC scans, SMTP recovery or another P01 native fixture on the same capacity.
Independent IaC/security review precedes changed fixture execution.

**Wait before HOME.** SEC01 must accept this exact OpenBao artifact's
signature/SBOM/CVE applicability. Bind the existing host
`/home/hyunyoun/data/hy-home.docker`, exact server/Agent IDs and source images,
TLS/snapshot-token paths and journal mounts in a fresh sanitized operator
contract. Obtain a restricted snapshot-only credential, prove ordinary-secret
read denial and renewal/save, and identify a fresh authenticated pre-upgrade
Raft snapshot. The observed missing
`secrets/backup/openbao/snapshot_token.txt` is a blocker, not a successful skip.
Prove independent/off-host unseal and CA/server-key custody, actual successful
backup/catalog scope, and exact empty restore/unseal/canary/renderer reauth.
Old `2b9f5ec8` HOME readiness receipts and the bounded SMTP two-file restore
cannot satisfy this current OpenBao/full HOME gate. Never place bootstrap or
recovery material only inside the OpenBao it must recover.

Review a mode-specific stateful recovery contract with the actual trusted user
instruction, implementer, independent reviewer, exact source artifact and empty
target, limits, prior attempt/result retention and rollback before execution.
First-isolated evidence generation may use its existing bounded review mode;
production readiness cannot inherit that waiver. Do not invent admin input,
independent key custody or a ready verdict. Keep unavailable operations BLOCKED
with the exact missing input; continue unaffected source work.

After admission, stage selected services sequentially: authenticated snapshot
and verified recovery boundary, server upgrade, manual unseal/native readiness,
then Agent upgrade/fresh wrapped reauthentication and current-consumer proof.
No in-place Raft downgrade, HTTP/audit bypass, HOME fault injection, whole-host
reboot, global stack restart, prune, broad chown, credential rotation, P06
migration, LAB runtime, learning-app planning or actual Wiki implementation.
A cold-start simulation and a real reboot are distinct evidence lanes.

**Actual checks in this assessment.** On input `728ec6379`, the focused command
below passed 64 tests in 14.866 seconds, exit 0, without native opt-ins:

```bash
python3 -m unittest tests.validation.test_openbao_agent_contract tests.lib.ops.test_openbao_issuance tests.lib.ops.test_openbao_issuance_trust tests.validation.test_openbao_candidate.ExpiryRegression tests.validation.test_sec01_version_contract -v
```

The registered native commands remain NOT_RUN in this assessment:

```bash
HYHOME_OPENBAO_CANDIDATE=1 python3 -m unittest tests.validation.test_openbao_candidate.CandidateNative -v
HYHOME_OPENBAO_REHEARSAL=1 python3 -m unittest tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests -v
```

A real unit change requires meaningful RED/GREEN, focused coverage, Ruff/
shell checks, affected metadata/links/catalog/version drift and registered
changed/staged gates. Native opt-in skips are not native PASS. Preserve small
logical commits for proven source residuals, fixture/isolated evidence, shared
integration and operational documents. The coordinator integrates common
patches once and reruns affected gates. Before a SPEC-0204 P01 PR, align the
local-only coordinator prefix with fresh remote main so the functional PR
contains only P01 changes. Require actual latest-head CI and independent
code/security/IaC/recovery review; no admin bypass or future PASS. No PR/push
occurs during this assessment. Only merged clean worker resources may later
be removed after evidence preservation; the old foreign worktrees stay intact.

Deliver P02/P03/P06/P08/P10 the final main/input SHA, server/Agent/snapshot CLI
index/platform identities, role/ACL/template/cold-boot graph, journal schema
and issuance_id compatibility, snapshot/offsite/restore/custody references,
measured audit/alert/recovery results and each BLOCKED/NOT_RUN lane. Keep
SOURCE/UNIT/STATIC/ISOLATED/HOME/MIGRATION/ROTATION/RECOVERY/DELIVERY separate.
W23 and this Task stay blocked until their actual conditions pass; catalogue
preparation and source delivery do not release P06.

### W20/W22 Versioned Issuance Continuation — 2026-10-11

The current user authorizes source compatibility on this existing Task, branch
`codex/p01-openbao-recovery`, and worktree
`/home/hyunyoun/data/hy-home.docker/.worktrees/p01-openbao-recovery`.
Root is the sole helper implementer; the assigned QA writer owns only
`tests/lib/ops/test_openbao_issuance_trust.py`. Independent reviewers are read-only.
The four held files are OpenBao README and subject-0085 Guide, Policy and Runbook:
P02 must preserve and hand off its changes before author transfer. Common
Compose/env, CI/manifest, Registry, Spec/Plan and other Tasks remain coordinator-owned.

This continuation preserves TLS, wrapped delivery, token roles/policies, source
receipts, audit, readiness and backup behavior. Legacy unversioned v1 journal,
anchor and metadata remain supported and are reconciled before another issuance.
New v2 issuance binds `schema_version: 2` in journal and anchor to equal `nonce`
and `issuance_id` aliases; metadata binds string `issuance_schema: "2"` to equal
`sec01_nonce` and `issuance_id`. One internal identity derives both aliases.
Exact shapes, explicit version types, duplicate-key rejection and the existing
role/time window are required. Same-identity cross-version metadata is blocked
in either direction; it cannot attest an accessor issued by that journal.
Conflicts preserve uncertainty and never authorize broad cleanup.

Execution order is witnessed RED, minimal helper correction, GREEN and coverage,
registered source/style gates, independent code/security review, logical commit
and the owning-Spec PR. Native admission remains separate: synthetic results
do not establish 2.7.1 authentication, actual recovery or HOME readiness.
W23, HOME and P06 hold remain unchanged. Rollback is a source-commit revert;
it does not downgrade HOME state or discard an active v2 journal.

Current baseline commands, all in the designated worktree:

- `rtk git status --short`: exit 0, empty; this continuation began clean.
- `rtk git rev-parse HEAD main origin/main`: exit 0; all three were
  `6da5e3bf380d5002e0e28181136fde8c016e49ce`.
- `rtk git ls-remote origin refs/heads/main`: initial sandbox attempt exit 1
  (`bwrap` loopback error); permitted retry exit 0, actual remote main
  `6da5e3bf380d5002e0e28181136fde8c016e49ce`. This supersedes the earlier
  remote observation `2b9f5ec82`, and requires no baseline rebase now.
- Bootstrap/provider, owning Spec/Plan/Task, REQ-0027, AD-0031, ADR-0046,
  implementation/QA roles and test/review/handoff/commit procedures: read-only
  commands exit 0. Discovery of nonexistent `scripts/renderer-issuance.py`
  and `scripts/script-manifest.json` failed; resolved paths are the OpenBao
  script family and `scripts/manifest.yaml`. No file was created at either
  guessed location. A discovery command including absent `.agent-work` exited 2.
- QA uses the existing isolated `/tmp/hy-home-p09-qa` tool installation,
  without changing its dependencies. `rtk proxy /tmp/hy-home-p09-qa/bin/python
  -m pip show coverage ruff pre-commit commitizen PyYAML jsonschema`: exit 1
  (pip absent). Read-only `importlib.metadata` query: exit 0; Python 3.12.3,
  coverage 7.16.2, Ruff 0.15.12, pre-commit 4.6.2, Commitizen 4.15.1,
  PyYAML 6.0.3 and jsonschema 4.26.0. Coverage output will use `/tmp`.

The witnessed RED command was `rtk python3 -m unittest
tests.lib.ops.test_openbao_issuance.IssuanceRecoveryTests.test_new_issuance_binds_versioned_id_to_legacy_metadata_alias
-v`: exit 1, one collected assertion FAIL, expected the versioned identity but
received `None`. The helper was unchanged at RED. After minimal implementation,
`rtk python3 -m unittest tests.lib.ops.test_openbao_issuance -v`: exit 0,
34 PASS. QA authored compatibility regressions in the existing trust suite.
The first coverage command incorrectly passed the Python filename as `--source`:
37 tests passed, exit 0, but coverage emitted `module-not-imported` and
`no-data-collected`; this is not coverage evidence. Corrected directory-source
measurement used:

```bash
rtk proxy /tmp/hy-home-p09-qa/bin/python -m coverage run --branch --data-file=/tmp/p01-issuance-compat-v2.coverage --source=infra/03-security/openbao/scripts -m unittest tests.lib.ops.test_openbao_issuance tests.lib.ops.test_openbao_issuance_trust -v
rtk proxy /tmp/hy-home-p09-qa/bin/python -m coverage report --data-file=/tmp/p01-issuance-compat-v2.coverage --show-missing --fail-under=80
```

Both exited 0: 45 tests PASS; helper 90-percent combined statement/branch
coverage (435 statements, 35 missing, 160 branches, 21 partial). Subsequent
test improvements will be remeasured before commit. The security reviewer
identified missing exact legacy keys and a stringified numeric anchor; both
were corrected. Parsing moved to `Record.from_document` to keep the modified
load function small. Source receipts and effective runtime image binding remain
unchanged. Ruff check and format, and `rtk git diff --check`, exited 0.
One patch failed to match Ruff-formatted context and made no change; the next
patch used the actual context. The QA patch tool stalled and was interrupted;
no second writer took over its file.

`rtk proxy /tmp/hy-home-p09-qa/bin/python
scripts/validation/run-ci-gate.py --profile changed --local-only --explain`
exited 0. The registered local selection is candidate preflight, full links,
supply-chain fixture policy, Conftest policy tests, Compose regressions and
repository-integrity regressions. The same command without `--explain` exited 1:
preflight metadata selected 1 / violations 0, image projection synchronized,
links 1,191 documents / 11,562 links / failures 0 / historical warning 1,
supply-chain fixture suite 263 PASS, and Conftest 18 PASS. Compose regression
ran 527 tests with 70 declared opt-in skips and two failures: existing Open WebUI
and Gatus entrypoint permissions. Repository-integrity was not reached.
`check-script-manifest.py` independently exited 0.

Read-only exact-path `stat` showed both original entrypoints at mode 0775;
the current Git declaration is executable mode 100755. No public source bytes
or permissions were changed to hide this baseline failure. A new invocation-owned
QA worktree was created by `rtk bash -c 'umask 022; exec git worktree add
--detach /tmp/hy-home-p01-compat-qa
6da5e3bf380d5002e0e28181136fde8c016e49ce'`: exit 0. Both fresh entrypoints
are mode 0755. The exact two permission tests on that unchanged baseline exited
0, 2 PASS. The final candidate will be copied into this Git checkout using only
the five P01-owned paths; its hashes and effective source checks must be recorded
separately from the original checkout failure. Original common files remain
read-only. A guessed Open WebUI path in an initial `stat` failed and was corrected
to `infra/08-ai/open-webui/docker-entrypoint.sh`.

The user explicitly assigned P01 the single native execution slot. Preflight
commands `rtk docker version --format '{{.Server.Version}}'`, exact image
`inspect`, `rtk free -h` and `rtk df -hT /tmp` all exited 0: daemon 29.8.2,
platform image `sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`
on linux/amd64, 9.3 GiB available RAM and 27 GiB disk; swap is full.
Independent IaC review admits only the new
`OpenBaoRehearsalTests.test_native_versioned_issuance_reconciliation` after source
commit and fresh input digest. Peak running fixture is one server capped at
384 MiB / 1 CPU / 128 PIDs on an internal network, plus stopped setup/Agent
containers. Owner is printed before creation; owned cleanup runs in `finally`.
Native and HOME are still NOT_RUN at this source-preparation record.

The existing delivery helper lacks owner name/label and resource caps. The new
test returns before that path and Agent start; it instead verifies actual v1/v2
lookup, persisted journal, installed helper process, exact destruction, empty
LIST and cleanup ACL denials. Direct v2 wrapped API authentication uses the
limited issuer, and login/replay explicitly omit any root token. This does not
claim current Agent delivery or recovery readiness. Cleanup attempts all owned
resources; it does not promise to retain failed resources.

Final QA froze the trust test at SHA-256
`be0847f0a564153160ff5a70b60077f26fcc637e8ff7871e92da83c024df259e`.
It adds hand-written legacy journal input, preserved legacy delivered-generation
updates, v1/v2 completion witnesses, 32-digit numeric anchor rejection, malformed
versions/shapes, duplicate keys/accessors and version/alias collision refusals.
Focused trust tests are 13 PASS; combined unit tests are 47 PASS, exit 0.
Final coverage commands, each exit 0:

```bash
rtk proxy /tmp/hy-home-p09-qa/bin/python -m coverage run --branch --data-file=/tmp/p01-issuance-compat-final.coverage --source=infra/03-security/openbao/scripts -m unittest tests.lib.ops.test_openbao_issuance tests.lib.ops.test_openbao_issuance_trust
rtk proxy /tmp/hy-home-p09-qa/bin/python -m coverage report --data-file=/tmp/p01-issuance-compat-final.coverage --include=infra/03-security/openbao/scripts/renderer-issuance.py
```

Final helper coverage is 90 percent with the same 435 / 35 / 160 / 21 counts.
The original `nonce=1` numeric-anchor test did not reproduce the old conversion
gap; QA corrected it to a 32-digit integer and added the recovery boundaries.
The QA additions are post-GREEN regressions, not a separately witnessed RED.
Helper SHA-256 is
`be2343a0eb2c5c19a7e7ea4e10c042d1f62d0597faa784d41d060641486b365e`.

Graph refresh is NOT_RUN: `rtk which graphify` exited 1; the generated graph
report and ECC navigation guide are absent (read command exit 1). Existing
canonical source/governance entries supplied navigation. The general QA-tools
discovery exited 1 because pnpm, shfmt, hadolint and check-jsonschema were absent
from that shell; only tools required by the selected actual checks are evidence.

Handoff remains P02 resource/ACL and versioned journal identity, P03 issuer/login
contract, P06 unresolved custody/backup/migration prerequisites, P08 the four
held document paths and author transfer, and P10 source/native acceptance limits.
The image/CLI declaration is unchanged; SEC01 owns artifact security acceptance.
HOME authentication, real snapshot, independent custody, operational rotation,
migration and recovery remain BLOCKED/NOT_RUN. No message was sent to another
chat. Common CI/manifest registration already maps the existing suites; any
documentation or delivery-container admission repair is a coordinator proposal.

The renewed P01 prompt was read from the user attachment on 2026-10-11.
SPEC-0212 Spec/Plan at `6da5e3bf380d5002e0e28181136fde8c016e49ce` confirms
current request precedence, one writer per shared surface and separate runtime
acceptance. Subject-0085 remains owned by P01; the user answered author transfer
with `confirmed`, but supplied no preserved P02 commit/patch. Preserve the four
files until that input can be integrated. The user explicitly answered actual
HOME host, credential reference, independent custody, empty restore target and
rollback inputs as `undetermined`. Those dependent actions remain NOT_RUN;
source delivery and the already admitted isolated method may continue.

`rtk bash .agents/skills/infra-validate/scripts/static-checks.sh` on the exact
candidate in `/tmp/hy-home-p01-compat-qa` exited 2: 11 checks PASS, 4 BLOCKED,
0 FAIL. The input graph refuses `external-absolute-path`; Compose plugin/render/
structure are blocked by that prerequisite. Public source includes Docker socket
and host bind paths; this wrapper permits only its copied fixture graph. No
private path was opened, no bind was weakened and no HOME readiness is claimed.
The registered changed gate remains the authoritative source regression route.
The optional `ops-runbook-agent` procedure was read, not invoked: actual HOME
behavior and recovery inputs are not yet verified, so no executable HOME runbook
is published from assumptions.

Independent security review approved helper `be2343a0...`, final trust test
`be0847f0...`, base unit `6d96abc0...` and native test `ca585511...`, with no
remaining finding. Its final independent compatibility rerun passed 10 tests,
exit 0. This is source review, not artifact-security, HOME or recovery acceptance.

Delivery recheck: `rtk git ls-remote origin refs/heads/main`, exit 0, returned
`4e26a5a8022a7307c7461af60337442912955df1`. `rtk git fetch origin main`, exit 0,
and scoped diff/log inspection found only P03/P04 Spec/Plan and issued Task
documents. `rtk git merge --ff-only 4e26a5a8022a7307c7461af60337442912955df1`
exited 0 in both P01 and the isolated QA worktree, preserving all five owned
changes. No other worktree was reset, stashed, cleaned or staged.

The first final candidate changed gate exited 1: supply-chain 263 PASS,
Conftest 18 PASS and Compose 537 tests PASS with 70 opt-in skips; repository
integrity ran 284 tests with two import errors for the existing Wiki suites.
Although the controller used the QA Python, its `python3` leaves used the system
PATH and lacked `referencing`. The fix is an explicit QA-venv-first PATH for the
registered controller and all leaves, not a source or test contract change.
The new base/document input and corrected tool routing require a fresh gate.
Main protection readback (`rtk proxy gh api` branches/main/protection and
rulesets, both exit 0) has strict status checking but zero named required
contexts, zero required approving reviews and no repository rulesets. Actual
latest-head hosted CI and independent review are still required by this request.
`rtk proxy /tmp/hy-home-p09-qa/bin/cz check -l 75 -m
'fix(openbao): Preserve versioned issuance journal identity'` exited 0.

### W22 Source Commit and Isolated Attempt — 2026-10-11

The aligned registered gate command was:

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; rtk proxy python3 scripts/validation/run-ci-gate.py --profile changed --local-only > /tmp/p01-compat-aligned-gate.log 2>&1'
```

It exited 0 on base `4e26a5a8022a7307c7461af60337442912955df1` with unchanged
four frozen source/test hashes and Task hash
`835303a53b861b6c4f82196439b8857990f98636e50a503b99b6dfcabbac99c7`.
Metadata selected 1 document, 0 violations; links checked 1193 documents / 11582
links, 0 failures and 1 preserved historical warning. Supply-chain ran 263 PASS,
Conftest 18 PASS, Compose 537 tests PASS with 70 opt-in skips, and repository
integrity 317 PASS. The explicit QA PATH resolved the prior two import errors.
The diagnostic `FIXTURE_FAILURE` lines belong to passing negative regressions;
they are not a native service receipt.

Only the helper, base unit, trust unit, rehearsal test and this Task were staged.
Index tree was `baa39c5392a3da09fdbd760ee4b695c9d751e754`.
Immediately after that final index mutation, the following exited 0:

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; export PRE_COMMIT_HOME=/tmp/hy-home-p09-qa/precommit-cache; rtk bash scripts/validation/run-ci-precommit.sh --mode local-staged > /tmp/p01-compat-staged.log 2>&1'
```

Markdown, Ruff format/check and hardcoded-secret checks passed. Independent code
review returned Spec PASS / Quality APPROVED, zero Critical/Important/Minor
findings on the four frozen hashes; its own earlier run passed 45 tests. Final
QA passed 47 tests and security independently passed 10 compatibility tests.
Its own Ruff rerun hit sandbox failure and an aborted escalation wait; final QA
and the staged controller supply the actual Ruff PASS. Native/HOME were excluded
from that source approval. `rtk git commit -m 'fix(openbao): Preserve versioned
issuance journal identity'` exited 0, creating
`9f36cbfa47c0759b4500169dbdac291eab2a79d6`.

Current vendor release readback (`rtk proxy gh api
repos/openbao/openbao/releases/latest --jq '{tag_name,published_at,prerelease,draft,html_url}'`)
exited 0: v2.7.1, published 2026-10-01T14:03:19Z, neither draft nor prerelease.
Candidate image inspect and Docker version each exited 0: cached multi-platform
identity `sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf`,
cached linux/amd64 fixture identity
`sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`,
daemon 29.8.2. Provenance/signature/SBOM/CVE applicability remain UNKNOWN and
pending SEC01. Independent IaC clarification retained admission for only the
one synthetic method, without promoting artifact or HOME acceptance.

After source commit, fresh input digest was
`dd8db4addb4edbacb690a4d3c816b75b2a48349cf4683024146f4ba7ddf5314d`.
Exactly one admitted attempt ran:

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; export HYHOME_OPENBAO_REHEARSAL=1; rtk proxy python3 -m unittest tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests.test_native_versioned_issuance_reconciliation -v > /tmp/p01-versioned-native.log 2>&1'
```

Exit 1, one ERROR after 15.453 seconds, owner
`p01-d330e6b50ad941fcbb4d197b6c7a158c`: existing fixture `server()` failed its
initial `docker exec <owned-server> bao version` command before initialization,
configuration, SecretID issuance or metadata reconciliation. Captured command
output remained withheld. No metadata/native authentication PASS is claimed.
`finally` cleanup ran; owner-filtered container/network/volume listings exited 0
with no retained resources. Owner/name-filtered Docker event queries exited 0
with no retained rows, so the startup failure category remains undetermined.
No automatic retry, broader class, Agent delivery or HOME action ran. Independent
IaC review is requested for a bounded diagnostic/recovery boundary.

The P02 worktree at `ea927d004` has no dirty or committed delta against current
main on the four subject-0085/README paths. Its preserved public proposal is
`.agent-work/integration-proposal/p02-openbao-docs.patch`, SHA-256
`a8af84ec3bf2db57a41e321688c9b6b48cb5160fcccbd81483cef052699a2459`.
Its source catalog/CLI is not yet integrated; those paragraphs/commands remain
a proposal. The user confirmed author transfer, so P01 now owns a narrow Korean
compatibility explanation in the four existing documents, preserving their
operational bodies and IDs. The earlier missing-patch hold is superseded by this
actual preservation receipt. No new HOME command is invented.

### W22 Sanitized Server Diagnostic Preparation — 2026-10-11

The user's exclusive P01 native assignment and dedicated-test ownership remain
valid; no new permission is inferred from elapsed time. Independent IaC review
clarified that only the first metadata method's reviewed one-attempt budget was
consumed. This new diagnostic is a separately reviewed unit and does not retry
metadata, initialize OpenBao or enter HOME. P01 owns the two existing dedicated
test files, including `_openbao_rehearsal_fixture.py`; no concurrent writer was
assigned to them.

First diagnostic RED (exit 1, one collected assertion failure):

```bash
rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest tests.validation.test_openbao_rehearsal.OpenBaoCleanupTests.test_version_probe_failure_reports_sanitized_owned_state -v
```

Expected `OOM_KILLED` did not match the original generic version-probe failure.
After the bounded projection implementation, five related unit tests passed.
Independent security found an IMPORTANT substring-version check and MINOR
inherited expired-certificate wording; IaC also requested refusal of
contradictory running/OOM/exit state. The existing substring check preceded this
unit, but an exact diagnostic claim requires correction.

The additional boundary RED command exited 1 (two collected tests, five failing
subtest assertions), before those corrections:

```bash
rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest tests.validation.test_openbao_rehearsal.OpenBaoCleanupTests.test_version_probe_rejects_similar_and_prefixed_version_tokens tests.validation.test_openbao_rehearsal.OpenBaoCleanupTests.test_failed_version_probe_categories_never_echo_output -v
```

Version first-two-token equality now refuses 2.7.10, suffix and prefixed output;
failed exec output remains withheld. Only an invocation-owned container is
inspected, with exact `Running`, `OOMKilled`, `ExitCode` projection and strict
keys/bool/int/range/consistency validation. No `State.Error`, logs, environment,
mount, configuration or payload is read. Failure results are fixed sanitized
categories; address/TCP failure has its own diagnostic enum.

Final GREEN (`rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest
tests.validation.test_openbao_rehearsal.OpenBaoCleanupTests -v`) exited 0 with six
tests. Ruff format/check and diff-check exited 0. Fixture hash is
`8bda42ab74a8444fbc956f614446d60143452f6cee2bc30f9726b10909dc04aa`;
rehearsal hash is
`69d349a982cfd35dcfcec41da28795c7b50ff57f3750731fb8c902da9ab3e7b8`.
The helper remains `be2343a0...` with its prior 47-unit/90-percent coverage receipt.
Independent final security review passed five focused tests, exit 0, and approved
the exact hashes with no remaining finding. Changed material is re-reviewed.

Proposed exact selector is
`OpenBaoRehearsalTests.test_native_server_start_diagnostic`: one fresh owner,
one internal-network/no-port server with existing 384 MiB / 1 CPU / 128 PID caps,
exact cached linux/amd64/daemon checks, version probe then raw TCP only, and owned
cleanup in `finally`. It creates no Agent, role, SecretID, snapshot or operational
resource. Execution remains NOT_RUN until source commit, fresh digest and
independent readiness; no broader class or unchanged-input automatic retry.

The four documentation hashes are README `7ec2c828...`, Guide `f887ebc8...`,
Policy `cd88641f...`, Runbook `250487ed...`. Independent contract/security review
approved them with no remaining finding. Doc-writer metadata and all-link checks
each exited 0; an earlier unsupported link `--mode changed` exited 2 and was
replaced with `--mode all`. The valid checks emitted no count receipt, so they
are not assigned invented counts. Later Task changes need their own final
metadata check. The preserved P02 proposal remains unapplied.

Final independent code re-review on `8bda42ab...` / `69d349a9...` returned Spec
PASS, Quality APPROVED and zero findings; independent diff-check exited 0.
IaC returned READY_FOR_ONE_BOUNDED_SERVER_START_DIAGNOSTIC_ATTEMPT after the
exact-token and consistency corrections. Its conditions are logical source
commit, fresh digest, unchanged cached image/amd64/tag and daemon, capacity and
the persisting exclusive assignment. Diagnostic is NOT_RUN at this checkpoint.

`rtk git worktree add --detach /tmp/hy-home-p01-diagnostic-qa
9f36cbfa47c0759b4500169dbdac291eab2a79d6` under umask 022 exited 0 after absence
check. An exact seven-owned-path patch applied there with exit 0. Changed gate
`--explain` exited 0 and selects the registered full fallback (17 local leaves)
for the additional existing fixture path. No ad-hoc skip or common mapping edit
was made. The actual changed controller is running with QA-venv-first PATH at
`/tmp/p01-diagnostic-gate.log`; its result is pending, not PASS at this checkpoint.

### W22 Server Diagnostic Receipt and Owned Config Mode — 2026-10-11

The diagnostic preparation index was
`a9b51b30e4096de23070efdfc0b63ba86b012a74`. Its final-index staged controller
exited 0 (`/tmp/p01-diagnostic-staged.log`). Only the two dedicated test files
and this Task were committed, command `rtk git commit -m 'test(openbao): Classify
bounded server diagnostic failures'`, exit 0, commit
`5fa707d842098e9acef0c3f9176afaa3c48421a0`. Sandbox wrapper failures before Git
execution exited 1; scoped escalated retries succeeded without changing scope.

Fresh image/version/capacity commands exited 0: exact cached linux/amd64 image
`sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`,
public label v2.7.1, daemon 29.8.2, memory available 7.5 GiB and /tmp free 25 GiB.
Remote main readback remained `4e26a5a8022a7307c7461af60337442912955df1`, exit 0.
The existing exclusive native assignment persists; the registered offline gate
has no opt-in native flag. Fresh source digest command (`rtk proxy
/tmp/hy-home-p09-qa/bin/python -c 'from tests.validation.test_openbao_rehearsal
import OpenBaoRehearsalTests; print(OpenBaoRehearsalTests().input_digest())'`)
exited 0 with
`7b7247baf9538f61bab2703f83983758a4362be5c25607f23e82ce92f962737e`.

Exactly one independently admitted server-only diagnostic ran:

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; export HYHOME_OPENBAO_REHEARSAL=1; rtk proxy python3 -m unittest tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests.test_native_server_start_diagnostic -v > /tmp/p01-server-diagnostic.log 2>&1'
```

Exit 1, one ERROR / 26.181 seconds, owner
`p01-f1951054e1fd4b708697f191a6baeec8`, sanitized category `EXITED_1` at the
version probe. No init, API configuration, metadata, SecretID, Agent or HOME
ran. `finally` cleanup ran; exact owner-filtered container/network/volume checks
and exact owner-prefix /tmp directory count each exited 0 with no resources.
Sandbox launch failed before execution; its escalated launch was the sole
actual attempt. Failed command output and authentication logs stayed withheld.

Public source investigation, not a captured runtime error, found a concrete
fixture defect: `mkdir(mode=0770)` under approved umask 022 leaves 0750. The
caller is UID/GID 1000; server UID/GID is 100:1000. The official v2.7.1 image
[launcher](https://github.com/openbao/openbao/blob/v2.7.1/.release/docker/docker-entrypoint.sh)
writes `/openbao/config/local.json` before `SKIP_CHOWN`. The fresh config bind
therefore lacks required group write. This is a source-supported cause candidate;
the sanitized exit category alone does not prove it was the only runtime cause.

Meaningful RED before correction, one collected assertion failure (exit 1):

```bash
rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest tests.validation.test_openbao_rehearsal.OpenBaoCleanupTests.test_server_config_bind_preserves_group_write_under_safe_umask -v
```

Expected mode 0770 differed from actual 0750. The correction explicitly chmods
only the newly created invocation-owned config directory to 0770; it changes no
common file, HOME path or permission policy. The mocked creation-boundary test
restores umask and removes its own temporary directory. Final seven cleanup
tests, Ruff check and Ruff format-check exited 0. Independent code review returned
Spec PASS / Quality APPROVED, zero findings. Further native execution requires a
new source commit, fresh digest and independent changed-input readiness; neither
failed native receipt is promoted to PASS. A guessed explain-log read exited 2
(file absent); no receipt was inferred from that failed read.

The corrected fixture SHA-256 is
`945de3cb929ac82a917139d550d4d3ee1a164790cac3f3da0bc4b8e606ee06ef`; rehearsal
SHA-256 is `31554becdbe64915d412dec3df0628cf1367a3f56457055de509354353eb6179`.
Independent security re-review approved these exact hashes, zero findings, and
independently passed seven cleanup tests / diff-check, exit 0. Independent IaC
returned READY_FOR_ONE_NEW_BOUNDED_SERVER_START_DIAGNOSTIC_ATTEMPT for this
changed input after commit, fresh digest and preflight. No metadata retry or HOME
is included. The running aggregate gate retains the earlier frozen QA input;
the corrected fixture/test must receive focused revalidation before final delivery.

### W22 Changed-Input Server Diagnostic — 2026-10-11

The config-mode correction index was
`8367b28a257c1d948c635ce70c30ce740108057f`. The immediately following staged
controller (`/tmp/p01-config-mode-staged.log`) exited 0; Markdown, Ruff format/check
and hardcoded-secret checks passed. Commit message validation exited 0.
`rtk git commit -m 'test(openbao): Preserve owned config group write under umask'`
exited 0, commit `9130b69894bb8ac3673ac969a72111d855299f98`, changing only the
fixture, rehearsal test and execution Task.

Fresh preflight commands all exited 0: exact tag's linux/amd64 cached image ID
`sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`,
public label v2.7.1, daemon 29.8.2, available memory 7.7 GiB, /tmp free 25 GiB.
Fresh input digest was
`868e44af22ecf1f5be5c1e6d3b38a292f37a7838141c15bdf00ee07ad490ca0b`.

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; export HYHOME_OPENBAO_REHEARSAL=1; rtk proxy python3 -m unittest tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests.test_native_server_start_diagnostic -v > /tmp/p01-server-diagnostic-mode-fixed.log 2>&1'
```

Exit 0, one test / 16.504 seconds, owner
`p01-0783b9e193874c51beffc218eea5dc15`, result
`SERVER_START_VERSION_TCP_DIAGNOSTIC: PASS`. This is version/raw TCP evidence
only. No init/API/metadata/Agent/snapshot/HOME ran. Owner-filtered
container/network/volume listings and owner-prefix temporary directory count
all exited 0 and were empty. Earlier failed attempts remain separate receipts.

Independent IaC then admitted exactly one changed-input
`test_native_versioned_issuance_reconciliation` attempt, conditional on the
empty cleanup above. The exact helper/test input remained unchanged; recomputed
digest matched `868e44af...`, exit 0. Fresh image/tag/amd64, daemon, memory and
/tmp checks all exited 0 (6.7 GiB available, /tmp 25 GiB free). The existing
exclusive native assignment persists. This is reviewed regression execution
after a concrete fixture fix, not an unchanged-input automatic retry. It excludes
the broader class, `DockerAPI.deliver`, Agent start, HOME, snapshot and recovery.

### W22 Changed-Input Native Metadata Receipt — 2026-10-11

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; export HYHOME_OPENBAO_REHEARSAL=1; rtk proxy python3 -m unittest tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests.test_native_versioned_issuance_reconciliation -v > /tmp/p01-versioned-native-mode-fixed.log 2>&1'
```

Exit 0, one test / 55.098 seconds, source commit
`9130b69894bb8ac3673ac969a72111d855299f98`, input digest
`868e44af22ecf1f5be5c1e6d3b38a292f37a7838141c15bdf00ee07ad490ca0b`, owner
`p01-1b8caa953f69402aaad68d48ed22c3e7`. Recorded native v1 exact reconciliation,
v2 exact reconciliation, and v2 wrapped API login / single-use replay denial:
PASS. The installed helper reconciled the corresponding version-specific actual
accessor metadata with bounded cleanup identity. No secret output was disclosed.
Owner-filtered container/network/volume listings and exact owner-prefix temporary
directory count exited 0 and were empty. No Agent start/delivery, HOME, snapshot,
migration, rotation or real recovery ran. Historical native proofs and the first
failed metadata/diagnostic receipts are retained with their distinct inputs.

Current acceptance lanes: SOURCE implemented / independently approved; UNIT 47
issuance tests and seven fixture tests PASS, helper coverage 90%; STATIC final
registered fallback timed out; ISOLATED changed v1/v2/API contract PASS within the
method above; HOME / MIGRATION / ROTATION / RECOVERY NOT_RUN, inputs undetermined;
DELIVERY commits present, owning-Spec PR/head CI/merge pending. Actual HOME and
other operational resources changed: 0. W23 and P06 holds remain in effect.

### W22 Registered Diagnostic Candidate Timeout — 2026-10-11

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; rtk proxy python3 scripts/validation/run-ci-gate.py --profile changed --local-only > /tmp/p01-diagnostic-gate.log 2>&1'
```

The 17-leaf full fallback exited 124. Its input was detached
`9f36cbfa47c0759b4500169dbdac291eab2a79d6` plus the then-frozen seven-owned-path
patch: fixture `8bda42ab...`, rehearsal `69d349a9...`, four final doc blobs and
the Task checkpoint. The fallback selected by the existing fixture path was not
bypassed. Metadata selected five documents with zero violations; all links
checked 1193 documents / 11582 links with zero failures and one historical
warning. The 15 lifecycle regressions passed in 138.017 seconds, after which the
local metadata regression leaf reached its registered 10-minute timeout. The
known child was runnable; at 9:54 wall time it had 1:41 CPU time. No assertion
failure receipt was emitted for that leaf, and no aggregate PASS is claimed.
Common timeout/mapping remained unchanged. Later leaves not reached by this
candidate are NOT_RUN for that invocation; the earlier aligned candidate PASS
is a distinct input receipt. Current exact fixture tests and independent reviews
passed after the config-mode correction; latest-head hosted QA remains required.

Read-only discovery attempts for absent QA `.agent-work` and the wrong
`scripts/lib/gate/ci_gate_runner.py` path exited 2; `rg --files scripts` located
the actual `scripts/validation/ci_gate_runner.py`. No report was invented from
missing paths. The coordinator proposal names the exact existing fixture path
for possible future changed/root mapping, with no common source mutation here.

Final Task metadata initially exited 1, selected five documents / 146 violations:
the new Evidence row used unknown combined Work Unit `W20/W22`; its two new
Acceptance cells also used noncanonical scope prose. Independent review identified
the exact contracts, and the rows now use assigned `W22` and canonical `pending`.
Source/isolated scope remains in the narratives. The metadata reference loader
computes legacy archive aliases only after successful Spec Package validation;
that package failure also produced 145 unchanged-archive type findings. Those
files were not edited. A corrected metadata check remains required; no reduction
of the Acceptance domain or archive validation was made.

Remote mutation authority is the user's P01 attachment, permitting this existing
Task's logical commits / owning-Spec PR / independent review / merge. Target is
`buenhyden/hy-home.docker`, feature branch `codex/p01-openbao-recovery`, base `main`.
Before-state queries each exited 0: no remote feature branch, no open PR for this
head; current remote main `4e26a5a8022a7307c7461af60337442912955df1`. Protection
readback has strict status checks but empty contexts/checks, zero required reviews
and no enforced owner review. CODEOWNERS routes all changed paths to @buenhyden.
The user still requires actual latest-head CI and independent review. No main push,
protection mutation, self-approval or bypass is authorized or performed. Git source
commits preserve recovery; operational rollback is NOT_RUN because HOME is untouched.

After both Evidence corrections, the following exited 0 on the five final
documents: zero metadata violations, zero legacy exceptions and zero transition
overrides; the unchanged archive cascade disappeared.

```bash
rtk bash -c 'export PATH=/tmp/hy-home-p09-qa/bin:$PATH; rtk proxy python3 scripts/validation/check-document-metadata.py --mode check-changed > /tmp/p01-corrected-evidence-metadata.log 2>&1'
```

The intermediate rerun (`/tmp/p01-final-metadata.log`) had still captured the
uncorrected Acceptance cells and exited 1 / 146 findings. Its failure is retained,
not treated as the final result. The earlier document-only staged controller
exited 0, but subsequent index corrections require a new final-index controller.
This result-only paragraph adds no link or metadata identity. Final source/docs
delivery remains an owning-Spec PR candidate; latest-head hosted CI is pending.

### W22 Source PR and Final Staged Receipt — 2026-10-11

The corrected five-document final index was
`dbe123017afc334ea4dab403144624ddd2f5ed89`. Immediately after its final mutation,
the registered controller exited 0; Markdown and hardcoded-secret checks passed,
with unrelated language checks correctly skipped:

```bash
rtk bash -c 'umask 022; export PATH=/tmp/hy-home-p09-qa/bin:$PATH; export PRE_COMMIT_HOME=/tmp/hy-home-p09-qa/precommit-cache; rtk bash scripts/validation/run-ci-precommit.sh --mode local-staged > /tmp/p01-final-docs-staged.log 2>&1'
rtk proxy /tmp/hy-home-p09-qa/bin/cz check -l 75 -m 'docs(openbao): Record versioned recovery evidence and HOME holds'
rtk git commit -m 'docs(openbao): Record versioned recovery evidence and HOME holds'
rtk git push -u origin codex/p01-openbao-recovery
rtk proxy gh pr create --repo buenhyden/hy-home.docker --base main --head codex/p01-openbao-recovery --draft --title 'fix(openbao): Preserve versioned issuance journal identity' --body-file .agent-work/p01-pr-body.md
```

All commands exited 0. Document commit was
`1c2c3c0908151f3f3adac77959cb5baa344f8c98`, tree equal to the final index; the
worktree was clean. The installed ECC pre-push hook reported no supported checks
and skipped; no automatic lint/QA enforcement is inferred from that hook.
Source PR is `https://github.com/buenhyden/hy-home.docker/pull/421`, created draft
and attached to this task's desktop artifact. Authenticated readback returned
head `1c2c3c0908151f3f3adac77959cb5baa344f8c98`, base
`4e26a5a8022a7307c7461af60337442912955df1`, mergeable true and draft true.

`gh pr view --json baseRefOid` exited 1 because this installed CLI does not
support that field; supported `headRefOid`/check fields and `gh api .../pulls/421`
readback each exited 0. Candidate-quality run `38108083728` was IN_PROGRESS on
the document commit; no hosted PASS or merge was claimed at this checkpoint.
CodeQL was also running; GitGuardian readback was SUCCESS. The source branch
push does not trigger aggregate candidate QA; the PR workflow owns it.

Independent exact-head code/contract and security reviews approved document
head `1c2c3c09...`, zero findings, with all ten P01 paths and frozen code/test/doc
hashes unchanged. This result-only Task follow-up records the later staged/PR
receipts and preserves canonical Evidence assignments. Its prospective latest
head must receive hosted QA and exact-head rebind before source merge. W23,
HOME/recovery/P06 remain blocked; no operational resource was changed.

### W22 Accepted Source Delivery — 2026-10-11

Result-only receipt commit was `d3ae5587d7e3376bed22bbef82badf3875d8fb95`, tree
`d0c4d82b7cb078251e8cd6ccb320300f0f0bb24b`. Its final-index staged controller
and Conventional Commit validation exited 0; commit and feature push exited 0.
Independent exact-head code/contract/security review approved that head, zero
findings; only Task receipt bytes differed from the previously approved source.

The actual latest-head candidate-quality run `38108268245` completed SUCCESS at
2026-10-11T03:32:34Z, job `114378325906`, 7m55s, head
`d3ae5587d7e3376bed22bbef82badf3875d8fb95`, base
`4e26a5a8022a7307c7461af60337442912955df1`. Readback / watch exited 0. All
CodeQL and GitGuardian checks were SUCCESS on that head; PR `main-security`
was intentionally SKIPPED and is not a security PASS. The local full fallback
exit 124 remains a separate preserved receipt. Hosted QA is not HOME evidence.
Run URL is `https://github.com/buenhyden/hy-home.docker/actions/runs/38108268245`.

The old installed `gh pr edit` exited 1 on deprecated Projects-classic GraphQL.
The same prepared body was then updated with the official REST API, exit 0:

```bash
rtk proxy gh api --method PATCH repos/buenhyden/hy-home.docker/pulls/421 -F body=@.agent-work/p01-pr-body.md --jq '{number,html_url,draft}'
rtk proxy gh pr ready 421 --repo buenhyden/hy-home.docker
rtk proxy gh pr checks 421 --repo buenhyden/hy-home.docker
rtk proxy gh pr merge 421 --repo buenhyden/hy-home.docker --merge --match-head-commit d3ae5587d7e3376bed22bbef82badf3875d8fb95 --subject 'fix(openbao): Preserve versioned issuance journal identity'
rtk proxy gh pr view 421 --repo buenhyden/hy-home.docker --json state,mergedAt,mergeCommit,url,headRefOid,isDraft
rtk git fetch origin main
rtk git merge --ff-only origin/main
```

All commands above exited 0. Before merge, ready/non-draft PR had CLEAN /
MERGEABLE state, the verified head/base above, no pending or failed check and
independent approval. Source PR `https://github.com/buenhyden/hy-home.docker/pull/421`
was MERGED at 2026-10-11T03:34:44Z with normal merge commit
`da2c84ce5b92a2a594002050c9b3e70fa795451e`. No admin bypass, squash, rebase,
main push, branch deletion or protection mutation occurred. Named source recovery
commits remain reachable. Only the clean P01 feature worktree was fast-forwarded;
other worktrees and coordinator-owned local main were left untouched.

This paragraph records the accepted source delivery without changing any
implementation, Evidence assignment or runtime acceptance. SOURCE / UNIT /
bounded ISOLATED are accepted at their stated scope; latest-head hosted STATIC
and source DELIVERY passed. HOME / MIGRATION / ROTATION / real RECOVERY remain
NOT_RUN. Full native rehearsal, latest-image expiry/advisory/snapshot reacceptance
and Agent delivery are not proved by the narrow metadata method. W23/P06 retain
their named-target, custody, snapshot/empty-restore and rollback prerequisites.
Actual HOME / other operational resource changes: 0.

### W22 P02 Catalog Documentation Reconciliation — 2026-10-11

The user handed over P02's reviewed public catalog proposal to this P01 sole
writer. Source commit is `962e11be50260a3dce2e2700b22951fce1b3f4f7`, synthetic
integration commit is `ab346b2c9a329731af3fff74be651531d87067cc`, and assessed
integrated main is `08b009a9ce0f288926f2edc4eebcbc5fb475d1e5`. The handoff said
remote delivery was pending, but the fresh actual `rtk git ls-remote origin
refs/heads/main` returned 08b009a9, exit 0. This observed result supersedes only
that historical remote-state statement, not P02's unexecuted operational lanes.

Root checkout HEAD remains a03c8930 with foreign SMTP/CLN/coordinator changes.
The existing P01 worktree started clean at 6d1d6960; `rtk git fetch origin main`
and `rtk git merge --ff-only origin/main` both exited 0. The nineteen integrated
P02 paths were inspected; none changes the four P01 documents. No foreign file,
coordinator main, common manifest/workflow, Spec/Plan or Task0010 was authored.

The frozen historical proposal is
`.agent-work/p02-frozen-handoff/p02-openbao-docs.patch` in the P02 integration
worktree. Its SHA-256 is
`71907ca6135cee7ad60df3868b92214967ef19822cf17b715810b3bb7419b7f4`.
Its older patch bases differ from current input blobs below. It was read for
comparison and was not applied, overwritten or deleted.

| Owned document | Current input blob at 08b009a9 |
| --- | --- |
| GDE-0085 | f1a16868ddaa29fef1722d566cc4c0affe70b534 |
| POL-0085 | 0ff09df88e82fd44beebf9462287afbf1acfdbf9 |
| RUN-0085 | 15d8c4ef57e2233d527b15e1cc87dde0c88939b9 |
| OpenBao README | 312cd463ba9f2c8160e71b753133fa4645da872c |

Four in-place Korean document additions explain the single public catalog,
classification/lifecycle versus actual acceptance, cooperative lock boundary,
source-retired alias versus physical deletion, and exact public-only CLI calls.
IDs, created dates, existing v1/v2 issuance, TLS/wrapping/readiness/audit/snapshot
and recovery sources are preserved. Actual destinations/ACL/delivery/reload and
RPO/RTO remain unaccepted. No opsflow ID, credential or operational target is
invented. Schema is 1.0.0; fresh CLI finds 145 entries and one alias. COMM-002
and COMM-003 regeneration is rejected; SMTP01 alone owns actual COMM-003
retirement. PG-020 retention and HOME/P06 holds remain.

The four immutable public CLI input SHA-256 values are:

- catalog: `a069d84360fdad0da16bd415c80019aa78859a137cdb1ba1fe50aa2882f7e141`;
- schema: `c044474d26a7f6f16f41d32fe07ca2dd34c08c0a3a3513f890717a7cf510582d`;
- public example: `c9b644730f5b963bc1a6b5af4d42de0eef858ed815857aa185f4a2cab1f756ca`;
- support matrix: `0eab707f24b88d891618441b8b768accfb370c7b29950deefb0d68cb2ab47654`.

CLI verification used existing `/tmp/hy-home-p09-qa`: Python3.12.3,
jsonschema4.26.0, referencing0.37.0, pre-commit4.6.2, Commitizen4.15.1.
The fixed public CLI and existing behavioral tests are unchanged. No new RED
or coverage run applies to this document-only change; earlier helper coverage
is not relabeled as a new measurement.

| Exact command or input-bound invocation | Exit | Observed result |
| --- | --- | --- |
| `rtk proxy /tmp/hy-home-p09-qa/bin/python scripts/operations/secret-catalog.py --root /home/hyunyoun/data/hy-home.docker/.worktrees/p01-openbao-recovery check` | 0 | P02_METADATA_VALID, 145 entries, 1 alias |
| `rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest tests.lib.ops.test_secret_catalog.SyntheticRepositoryTests.test_cli_check_render_guard_and_drift -v` | 0 | One existing actual-subprocess synthetic regression PASS |
| `rtk bash -c 'umask 022; rtk git worktree add --detach /tmp/hy-home-p01-catalog-doc-qa 08b009a9ce0f288926f2edc4eebcbc5fb475d1e5'` | 0 | New absent-before-create isolated public QA checkout |
| `rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check` | 0 | P02_METADATA_VALID, 145 entries, 1 alias |
| `rtk python3 scripts/operations/secret-catalog.py --root "$PWD" render` | 0 | STAGING_RENDERED, exactly four public staging files |
| `rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-views` | 0 | P02_VIEWS_MATCH |
| `rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-002` | 2 | Expected P02_GENERATION_BLOCKED refusal |
| `rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-003` | 2 | Expected P02_GENERATION_BLOCKED refusal |
| `rtk python3 scripts/validation/check-document-metadata.py --mode check-changed` | 0 | Selected 9, violations 0, legacy exceptions 0, transition overrides 0; source=local upstream, merge-base 26e37a22 |
| `rtk python3 scripts/validation/check-document-links.py --mode all` | 0 | 1195 documents, 11611 links, failures 0, one existing historical warning |
| `rtk python3 scripts/validation/check-script-manifest.py` | 0 | Existing catalog authority/behavioral consumer registration valid |
| `rtk python3 scripts/validation/run-ci-gate.py --profile changed --local-only --explain` | 0 | Selected registered local preflight, links, supply-chain, Conftest, Compose and repository-integrity leaves; explain only |
| `rtk git diff --check` | 0 | No whitespace errors |

The five direct public staging calls ran sequentially in the new QA checkout,
with PATH `/tmp/hy-home-p09-qa/bin` first. Its new owner-owned `.agent-work`
and regular single-link README were created exclusively, exit 0. Outputs are
`SENSITIVE_ENV_VARS.md.example`, `secret-catalog-summary.json`, `README.md` and
`SENSITIVE_ENV_VARS.md` only inside ignored `.agent-work/p02-views`; the last
name is a value-free public projection, not the private metadata source.
Source public input bytes remain unchanged. Rendering is per-file replacement,
not an atomic four-file transaction. The QA artifact is preserved for review.

Several initial tool-wrapper attempts exited 1 with the sandbox's bwrap
loopback error before the requested Git/Python check executed. Authorized
escalated retries completed as recorded above; these are not test failures or
RED. An initial `apply_patch` to the dedicated /tmp QA README was rejected by
the project-root hook. The explicit scoped exclusive file creation was then
approved and succeeded; no hook or global setting was changed. The earlier
local full gate exit124 is still historical failure evidence; no aggregate
rerun was substituted for this document change. Remote candidate QA owns the
new PR's aggregate result.

Independent four-document security review approved the frozen hashes with no
findings. Exact contract/documentation review and final staged controller are
recorded in the ensuing delivery receipt. Implementation and common files
remain unchanged. The coordinator receives a narrow proposal to add RUN-0085
to the CLI's proven consumers after these actual calls are accepted, while
keeping `tests/lib/ops/test_secret_catalog.py`, RUN authority and P02 regression
registration. This P01 author does not change the common manifest.

SOURCE is reconciled documentation; UNIT is one reused synthetic CLI regression;
STATIC is the observed document/manifest evidence above; public staging QA is
not OpenBao native ISOLATED or application E2E. HOME, MIGRATION, ROTATION and
real RECOVERY are NOT_RUN. Actual operational changes are zero; missing actual
HOME/snapshot/custody/empty restore/rollback inputs keep this Task blocked.

The first Task-only metadata invocation exited 1: the new receipt was placed
under Evidence, interrupting its registered contiguous table. Moving this
receipt into Work Log preserves the unchanged Evidence rows. The 145 archive
profile findings were a package-validation cascade, not archive changes; no
archive or validator was edited. The affected metadata and staged checks are
re-run on the corrected input before committing.

### W22 P02 Documentation Submission Receipt — 2026-10-11

The corrected Task-only check completed exit 0:
`rtk python3 scripts/validation/check-document-metadata.py --mode check-changed
--base-ref HEAD --changed-path
docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0006-openbao-trust-bootstrap-and-recovery.md`.
It selected one Task with zero violations, legacy exceptions and transition
overrides. Bound HEAD is 08b009a9; QA PATH is the same environment recorded
above. The first exit1 and its correction remain recorded separately.

After restaging only the corrected Task, the final
`rtk bash scripts/validation/run-ci-precommit.sh --mode local-staged` exited 0
with PATH `/tmp/hy-home-p09-qa/bin` first, PRE_COMMIT_HOME
`/tmp/hy-home-p09-qa/precommit-cache`, umask022. Markdown, whitespace and secret
checks PASS; unrelated language checks SKIPPED. Exact final source index tree
was `a45f37a3da7f3e811dab914c065e2305ee9a1c8d`; `rtk git diff --cached --check`
exited 0. Commitizen title check exited 0. Source commit is
`47c263c1da9b47dd21a8bb4522b49feda9bf1210`,
`docs(openbao): Reconcile public catalog guidance`, parent08b009a9. Its five
owned paths have 238 insertions and five deletions. Ordinary commit and
`rtk git push -u origin codex/p01-openbao-recovery` both exited 0.

Independent security review approved the four document SHA-256 values:

- README: `af33a0ff4bcb813f7d348e17b70cab5a6a6d31bad6bb31d1745218b9c6ba6908`;
- GDE-0085: `1c1980e7cf49c93db6a7acc8675a2f41d36ada29366c2c35781aebbf4790bccf`;
- POL-0085: `f5a9f8a2ec205271eeaf2ffc030289e61df37d61f03555e8c18ee5fdf60c1650`;
- RUN-0085: `be098691343d20dcf3cdea56381e2318a0af1dfaca8d2915bcc4026d16501bad`.

It also approved the corrected Task hash
`226950fef6ae76c7466124bbf94c8286149cb0dde91cac9001cf88fa78144d24`, with no
findings. Contract/documentation review is pending at this receipt timestamp;
approval must be observed before ready/merge. No operational acceptance changes.

`rtk proxy gh pr create --repo buenhyden/hy-home.docker --base main --head
codex/p01-openbao-recovery --draft --title
'docs(openbao): Reconcile public catalog guidance' --body-file
.agent-work/p01-catalog-pr-body.md` exited 0 and created
`https://github.com/buenhyden/hy-home.docker/pull/423`; it was attached to the
task. API readback exited 0: actual head47c263c, base08b009a9, five changed
files, draft, mergeable. Candidate run38113294386 was IN_PROGRESS on that head
when queried, not passing acceptance. The result-only submission receipt
requires its own final index check and latest-head CI; no old head's result is
substituted for them. Final hosted check/review/merge receipt remains the remote
PR's observed delivery boundary.

Coordinator-only consumer proposal
`.agent-work/integration-proposal/p02-catalog-consumer.patch` preserves the
existing subprocess test and RUN-0085 authority while adding RUN-0085 as a
proven CLI consumer. `rtk git apply --check` exited 0; the patch was not applied.
It and the public QA staging artifacts are preserved until accepted. No
common file, P02 Task or another worker's branch/worktree was modified.

### W22 P02 Documentation Delivery Receipt — 2026-10-11

The document source commit47c263c and result-only submission commit
`8cd71a252237f0cd96154bc2ab7982ba24c0d1ad` were delivered together in PR423.
Final reviewed head is 8cd71a2, tree
`ee38ab9b5163ff76a2b13f5bbec79caab36b705b`, actual base
`08b009a9ce0f288926f2edc4eebcbc5fb475d1e5`. Its result-only receipt staged
controller exited 0, with Markdown, whitespace and secret checks PASS;
unrelated language checks SKIPPED. The four document hashes are unchanged
from the preceding receipt. Final Task hash at that head is
`41b5f8efabc8dee0d43232001ca59d7b7e942285099d08f2cbd5d4fce9ef2b42`.

`rtk proxy gh run view 38113523746 --repo buenhyden/hy-home.docker --json
status,conclusion,headSha,jobs,url` exited 0 and confirmed the latest-head
candidate SUCCESS. Job114393813965 ran from 2026-10-11T05:03:12Z to
2026-10-11T05:07:59Z (4m47s). Registered changed validation and its selected
prerequisites passed. `rtk proxy gh pr checks 423 --repo
buenhyden/hy-home.docker` exited 0: candidate-quality, CodeQL analyses and
aggregate, GitGuardian and triage PASS. main-security was workflow-skipped;
it supplies no execution evidence. Earlier run38113294386 on head47c263c
was CANCELLED after the ordinary receipt push, not substituted as passing
evidence. The local aggregate timeout and corrected Task metadata failure
remain recorded above rather than overwritten by hosted results.

Independent contract/code review of 08b009a9..8cd71a2 returned specification
PASS and quality PASS, with no Critical/Important/Minor findings. Independent
security review approved exact head8cd71a2/treeee38ab9b and all five hashes;
no findings remained. Coordinator-only consumer registration remains a
scoped follow-up, not an authored common-file change.

PR body update, `rtk proxy gh pr ready 423 --repo buenhyden/hy-home.docker`
and API head/base/mergeability readback all exited 0. Readback showed non-draft,
head8cd71a2/base08b009a9, mergeable and clean. `rtk proxy gh pr merge 423
--repo buenhyden/hy-home.docker --merge --match-head-commit
8cd71a252237f0cd96154bc2ab7982ba24c0d1ad --subject
'docs(openbao): Reconcile public catalog guidance'` exited 0. API readback
confirmed merged at 2026-10-11T05:12:52Z, ordinary merge commit
`3da11e6b75182b07c96a3f32ed29210a3e246c74`. `rtk git fetch origin main`
and `rtk git merge --ff-only origin/main` exited 0 in the clean P01 worktree.
No coordinator checkout or other worker branch was moved.

SOURCE is the accepted four-document catalog reconciliation; UNIT is the
existing subprocess regression PASS; STATIC is the recorded metadata, links,
staged and latest-head hosted checks. ISOLATED here is public staging only,
not new OpenBao native or app E2E proof. HOME/MIGRATION/ROTATION/real RECOVERY
remain NOT_RUN; DELIVERY is the observed PR423 merge. Operational resource
changes remain zero. Task status remains blocked, W23/P06 holds remain, and
the manifest-consumer proposal and public QA artifacts are preserved for
the coordinator. No new Task or source implementation is introduced by
this result-only delivery receipt.

### W23 Current Acceptance Assessment — 2026-10-13

Superseded in part: the TLS-files-absent finding below is superseded by W23
Current TLS and Snapshot Retry Receipt (TLS_PREPARED / NOT_DEPLOYED), and the
DELIVERY lane by W23 Merged-Source Readiness Checkpoint (PR #431 merged as
`7620f2d22`). The tables are kept as observed at the time.

This assessment is bound to `origin/main` and the isolated worktree HEAD
`62556dc63b66c828c27e9c33017d26cdf70b8542`; the supplied baseline is
`23e37362b72e98028a4675f282819c0346ae59dc`. The fresh fetch, ref, status,
worktree and pull-request observations are recorded by the coordinator: fetched
`origin/main` equals this HEAD, no open PR was observed, and the ten existing
foreign worktrees were clean. This writer used only
`codex/p01-current-acceptance` and did not alter main or another worktree.

| Classification | Current result | Boundary |
| --- | --- | --- |
| SOURCE_APPLIED | Client-mount correction, fixture/rehearsal regressions, two stale Korean volume tables and this value-free W23 receipt | Nine owned paths; no image, secret, data or runtime change |
| NO_CHANGE | OpenBao server/Agent 2.7.1 pin `6d2b9385...`; source and the five named modules were unchanged at the starting SHA | The current fixture helper and rehearsal module are the separate SOURCE_APPLIED correction; SEC01 owns any image/security disposition |
| CONFIRMED_GAP | Initial default-context observation found the initialized Raft server sealed with failing streak 1799; the later operator unseal resolved that state and the latest value-free status is sealed=false. Server and Agent remain 2.6.2 rather than declared 2.7.1; expected source TLS files are absent, Traefik's whole-directory client mount includes the private CA-key path, and Agent stale/auth notification has no Prometheus/Gatus producer/consumer | This is neither cold-boot nor recovery acceptance. Agent failing streak is 0. Values, raw logs, secrets and private files were not read; existing generic snapshot-stale status is not a missing-gap finding |
| CONSUMER_DEPENDENT | Keycloak/Grafana and the later P06 pilot require a named consumer, its least-privilege ACL and an approved runtime boundary | No consumer file/content or KV value was read; P06 migration remains held |
| RUNTIME_UNVERIFIED | Agent has exit code 0 and failing streak 0 but exposes only `agent.hcl`, templates and agent/output volumes; no public CA or script bind was observed | A health state does not prove rendered freshness, current-version authentication or consumer read |
| SECURITY_WARNING_CONFIRMED | Whole-directory client mount including a private CA-key path violates the source trust-scope contract; actual byte access or disclosure is NOT_RUN and unconfirmed. No current 2.7.1 image warning is confirmed | Cached index digest `6d2b9385...` resolves to linux/amd64 platform image `a36ea8c2...`; SEC01 ledger applicability is UNKNOWN and signature/SBOM checks are NOT_RUN. The eight source-code paths are independently approved; this Task receipt remains pending review |
| OUT_OF_SCOPE | Runtime/service/data/secret/image changes, rotation, migration, deletion, LAB and learning-app work | No change beyond this Task receipt |

The historical starting-SHA run discovered 80 cases: 76 PASS and four explicit
native opt-in skips in 17.919s (exit 0). After the fixture correction, the
current command is:

`python3 -m unittest tests.validation.test_openbao_rehearsal
tests.validation.test_openbao_agent_contract tests.validation.test_openbao_candidate
tests.lib.ops.test_openbao_issuance tests.lib.ops.test_openbao_issuance_trust`
discovered 81 cases: 77 PASS and four explicit native opt-in skips in 19.802s
(exit 0). This is a fresh source/synthetic result only. It does not establish a
current 2.7.1 image, HOME Agent render, functional consumer authentication,
or any recovery result.

Eight OpenBao-only runtime-compatibility static tests also passed in 0.336s
(exit 0).
The public five-service Compose projection first refused missing public
Gatus variables and duplicate group `1000/1000`; after its owner supplied
public defaults from the existing `.env.example`, the projection passed (exit
0) without reading a private env. `.env.example` was not edited here.

The separate reviewed linux/amd64 candidate native check on `a36ea8c2...`
completed 1 test PASS in 116.362s (exit 0). It exercised wrong-CA,
expired-SecretID, short-role, audit-full and snapshot-to-empty-target cases
with synthetic data only.
The full-class rehearsal on original reviewed input
`ac34e89d1f0d177933dbd96d24044e18b287e3e366a30be3d749bcfe4db3fe2e`
timed out at its 240-second outer limit (exit 124) while restoration was
running. Its preceding observed checks are retained as partial evidence only;
they do not make the full isolated lane PASS. Existing labelled/path-bound
cleanup then passed for exact owner `70c1...`: 16 containers, four volumes,
one network and the invocation temporary directory were removed through the
existing helper, with no HOME mutation.

On fixed input
`95dc53a900fe7d22ea49e830adc0ff5f69b7a82ab9b4daedd66f33edf5b512ff`, the
narrow v1/v2 receipt is `HYHOME_OPENBAO_REHEARSAL=1 timeout 240 python3 -m
unittest tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests.test_native_versioned_issuance_reconciliation
-v`: 1 PASS in 89.661s (exit 0). The full-trust receipt is
`HYHOME_OPENBAO_REHEARSAL=1 timeout 480 python3 -m unittest
tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests.test_native_trust_auth_audit_and_recovery
-v`: 1 PASS in 247.084s (exit 0). It observed Agent render mode 0600,
start/restart/cold boot, current version 1, snapshot renewal/save,
malformed-audit nonexposure, empty-Raft restore with foreign-share
denial/original unseal, audit-full HTTP 500 with health 200, and sealed-readiness
denial. The `finally` cleanup passed. `scripts/validation/check-script-manifest.py`
and `git diff --check` also passed (exit 0). All of these use synthetic material.

The audit case covers malformed-JSON request nonexposure, ordinary HMAC-SHA256
output and raw-marker absence. Tampered/invalid-HMAC verification is NOT_RUN:
there is no audit-hash producer in this contract. This is a coverage limit, not
an audit-integrity PASS.

The registered broad local selector
`python3 scripts/validation/run-ci-gate.py --profile changed --local-only` is
NOT_RUN. Its `--explain` selection includes LAB credential, isolation,
controller and Supabase SMTP rehearsal leaves through
`.github/workflow-contract.yml` lines 678–741, which this request excludes.
The selector and its workflow contract were not changed. The scoped five-module
command above is not a substitute for that aggregate gate; required hosted CI
remains pending for any later draft PR.

| Lane | Synthetic / isolated target | HOME / operational target | Boundary |
| --- | --- | --- | --- |
| ISOLATED | PASS (synthetic only): candidate, fixed v1/v2 and fixed full-trust rehearsals passed | NOT_RUN | Fixture results do not establish HOME, a physical cold boot or application consumption |
| HOME_COLD_BOOT | NOT_APPLICABLE | NOT_RUN | Host and replacement intent are selected and authorized; actual TLS and restricted snapshot-credential/artifact preconditions remain missing |
| INDEPENDENT_CUSTODY | NOT_APPLICABLE | NOT_RUN | Synthetic unseal shares do not establish independently held actual unseal/snapshot-key custody; the later readiness declaration is not verification |
| WRAPPED_REISSUE | PASS: fixed v1/v2 fixture | NOT_RUN | No selected runtime issuer, role or cleanup target |
| CURRENT_VERSION_AUTH | PASS: candidate and full synthetic authentication | NOT_RUN | HOME target is selected but has no 2.7 current-version or consumer authentication result |
| SELECTED_EMPTY_RESTORE | PASS: candidate synthetic empty-target case | NOT_RUN | Exact empty-Raft target is selected but not created/exercised; actual snapshot credential/artifact, capacity/RPO/RTO and custody checks remain |
| CONSUMER_READ | NOT_RUN | NOT_RUN | Agent render-file validation is not a Keycloak/Grafana application read; no named consumer/ACL/runtime target and no values were read |
| DELIVERY | NOT_APPLICABLE | DRAFT_ONLY / BLOCKED | This receipt is uncommitted; the broad local gate is excluded by its LAB leaves, and no PR, exact-head CI, independent review or merge exists |

The observed runtime is not an upgrade instruction. The verified rollback for
this receipt is a Git revert of the nine-path logical commit to source baseline
`62556dc63b66c828c27e9c33017d26cdf70b8542`. A future runtime rollback requires
the exact verified image, CA/role/journal, compatible storage snapshot and
independently held unseal material; it must not restore the old no-TLS endpoint.

The later operator declaration supersedes the earlier statement that HOME
recovery/custody preparation was unready: the intended operation is replacement
of the named running OpenBao 2.6.2 server and Agent with declared 2.7.1.
It is a readiness declaration, not verified custody or runtime acceptance.
HOME remains NOT_RUN until dedicated TLS execution/verification, a restricted
snapshot credential and created integrity-bound artifact, independent custody,
empty-restore and consumer checks complete. The host, paths, window and
unseal/decrypt owner are selected. No runtime cutover has begun. The first KV
migration remains P06-owned; P01 does not copy or rotate values.

The value-free actual inventory identifies `hy-home-server` through the default
Docker context. Docker is 29.8.2, and the actual 2.6.2 server image is known:
`sha256:11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641`
on linux/amd64. The current server data and Agent/output volumes resolve to
`/home/hyunyoun/storage/volumes/security/openbao/{data,agent,out}`. The supplied
certificate leaf chain and expiry checks pass, but its SAN lacks `openbao`
(while `127.0.0.1` is present). The source-required public TLS paths
`storage/volumes/security/openbao/tls/{ca.pem,server.pem,server-key.pem}` are
absent. Current Traefik mounts the repository's `secrets/certs` directory at
`/certs:ro`; its private `rootCA-key.pem` is mode 0400 but lies inside that
client-visible mount. The mount scope violates the intended contract, but byte
access/disclosure is not confirmed: Traefik has default root user, `cap_drop:
ALL`, `no-new-privileges`, and a read-only root filesystem, while the key is
owned by UID 1000/GID 1001 at mode 0400. The metadata-only unseal file (0600)
and token file (0640) exist but are not independent-custody proof. Public
certificate metadata was parsed; private-key, authentication-secret, KV-value
and raw-log contents were not read. This is an upgrade preparation mapping
only; execution waits for TLS-key isolation, a dedicated `openbao` SAN
certificate, restricted snapshot credential/artifact preparation and actual
custody/restore checks. The backup, empty-restore and downtime selections are
already recorded above.

Value-free `bao status -format=json` on the actual server exited 2 and reports
initialized=true, sealed=true, storage_type=raft, version=2.6.2,
ha_enabled=true and migration=false. This identifies sealing as the current
unhealthy cause; it neither unseals the server nor proves recovery. The public
source path `secrets/backup/openbao/snapshot_token.txt` is absent. A guessed
host backup path is not evidence that no actual backup exists, because the
rendered staging path depends on a private environment input that was not read.
The actual Raft storage means the 2.7.1 file-backend removal does not require a
storage-backend migration, but the 2.6.2-to-2.7.1 private backup/restore test is
NOT_RUN.

The operator subsequently completed the source unseal. A fresh value-free root
status exited 0 and reports initialized=true, sealed=false, storage_type=raft,
version=2.6.2, ha_enabled=true and migration=false. It accepts the initial
source status only; it is neither cold-boot, restore nor 2.7.1 acceptance.

Value-free `stat`/`findmnt` inspection confirms the selected, but not created,
`/home/hyunyoun/backups/p01-openbao-20261013/raft-pre-2.7.1.snap` for a fresh
authenticated 2.6.2 snapshot after `buenhyden` unseals and writes are quiesced.
`/home/hyunyoun/backups` is an existing non-symlink ext4 path with about 51.2
GiB free; it is a different device from live Raft data, whose filesystem has
about 2.49 TiB free. It is not offsite or independent-custody proof, and
automatic Restic inclusion is unknown. The existing staging candidate
`/home/hyunyoun/backups/staging/openbao-raft.snap` is absent; no Restic
repository was inspected, so this does not prove no backup exists. The live
snapshot size is UNKNOWN because no actual snapshot exists. The host disk-usage
check was denied and its error is withheld, while a bounded read-only container
check reports current allocated Raft data of 39,728 KiB (about 38.8 MiB).

The proposed fresh empty restore target is
`/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013`,
with internal no-egress container name `p01-home-restore-20261013`. Both
candidate paths were confirmed absent and were not created. Before execution,
preflight must set/verify a private 0700 directory and 0600 snapshot file
owned by UID/GID 1000, confirm the exact restore size/capacity and never reuse
the live volume. `/home/hyunyoun/storage/backups` shares the live-data device
and is therefore not an independent-disk backup candidate. Plan a 30-minute
service cutover plus a 60-minute maintenance window and a fresh-snapshot,
quiesced-write RPO objective as planning estimates, not observed RTO/RPO.
Reserve a 1 GiB restore work budget for startup and growth; it is a
recommendation, not a measured snapshot-capacity maximum.

The named operator (`buenhyden`) must unseal/decrypt and confirm independent
custody. Upstream's [upgrade guide](https://openbao.org/docs/guides/upgrade/)
requires a backup before upgrade and does not promise backward data
compatibility; rollback requires compatible storage and image, so replacing the
image alone is unsafe. The operator selected the proposed snapshot path
`/home/hyunyoun/backups/p01-openbao-20261013/raft-pre-2.7.1.snap`, empty restore
path `/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013`
and container `p01-home-restore-20261013`, with the 1 GiB work budget, a
60-minute maintenance window and a 30-minute cutover goal. `buenhyden` owns
unseal/decrypt. Replacement intent is already authorized; no cutover action has
begun because TLS material and snapshot credential/artifact facts remain missing.

The operator explicitly authorizes Codex to sign only the existing
`rootCA-key.pem`, without output, to provision the source TLS-path files for
DNS `openbao` and loopback. That TLS operation has not executed and will be
delegated to the actual credential-preparation owner. The restricted snapshot
identity/token is still missing and remains an operator-preparation prerequisite.

Independent IaC review found the nine-path source correction ready with no
source finding, but production readiness is BLOCKED on dedicated TLS execution/
verification, restricted snapshot credential plus created integrity-bound
artifact, independent custody, and unexecuted empty-restore/consumer checks.
The target and maintenance window are selected but RTO remains unmeasured. The
existing replacement request supplies intent, so no second permission is
needed once those checks are available. A first actual isolated restoration may
later create its own restoreability receipt through the registered
`first_isolated_restoreability` mode; synthetic evidence supplies no actual
artifact proof.

### W23 Client-Mount Correction Admission — 2026-10-13

Independent security review closes the mount-scope finding as HIGH for source
correction. The user's private-key separation request authorizes the minimal
source repair: four client certificate binds across the Traefik, Nginx and
OpenSearch (including Dashboard) Compose documents, with the existing runtime
compatibility regression. The assigned infra implementer is the exclusive
writer for those three YAML files and its test. This logical commit owns nine
paths: those four source/test paths, two fixture tests, these two stale Korean
volume tables and this Task. The receipt will record its RED/GREEN, YAML render,
nine client static tests and independent source review once complete. No runtime
action, image pin/scanner change or secret-value read is authorized by that repair.

The frozen four-file source repair has exact diff hash
`f42ea58a66214b32bb1c8d7be589b3ba838d59abbe7610e5e1515008670b4f8e`.
Its focused RED was one expected failure (exit 1); the corrected focused case
passed in 0.066s (exit 0), and the selected OpenBao suite passed 9 cases in
0.399s (exit 0). Public-only core, Nginx and OpenSearch Compose projections
using `.env.example` plus public Gatus UID/GID overrides each rendered (exit
0). The registered `.yamllint` passed (exit 0); the initial guessed
`.yamllint.yml` invocation failed (exit 1) because that file is absent and is
preserved as discovery evidence. The repair requires `DEFAULT_CERT_DIR` and
uses twelve exact read-only leaf binds with host-path creation disabled.
Independent exact-diff IaC and security review both PASS with no findings.
No ROOT image, scanner, version or runtime change occurred.

The source rollback is a nine-path Git revert. That revert would restore the
confirmed private-CA parent mount, so a future HOME rollback must use its
reviewed TLS/recovery contract and must not blindly revert this source repair.

The fixed native input `95dc53a...` remains valid Agent-fixture evidence: the
Traefik Compose file is outside its input digest, and the physical fixture uses
the independently corrected CA-only mount with unchanged images/dynamic
configuration. A full native rerun is therefore not required solely for the
client-bind YAML repair. Related Korean README bind descriptions may be changed
only if their inspected volume-contract tables are stale. The inspected Traefik
and Nginx README tables are stale and now enumerate the same three explicit
read-only certificate paths as the reviewed bind contract. OpenSearch's general
certificate-directory statement makes no whole-mount claim and is NO_CHANGE.
The operator selected the recommended backup artifact, empty target and
downtime choice above. This earlier receipt predates the current TLS and
artifact-preparation results below; P01 remains blocked on custody and restore
execution checks.

### W23 Current TLS and Snapshot Retry Receipt — 2026-10-13

Implementation commit is `b8d3ea818c91b6e3f3da078906e70c361842c5d5`
(parent `a4d8c9cf4`, tree `cb08b7c65da984d8915a14a6216836b0cb2ae294`);
current checkout/PR #431 head is `69f9b06162c99f555b4589d276fbbf476f2c6da1`.
The first candidate run on `b8d3ea8` failed at the catalog receipt. Candidate run
38285415072 failed at the catalog receipt, before operations or any LAB module;
the local-only aggregate remains NOT_RUN. The catalog correction is separate.

At 2026-10-12T18:26:42Z, user `buenhyden` marked PR #431 READY_FOR_REVIEW
(`isDraft=false`). The latest-head candidate-quality run 38289397982 passed in
7m49s; CodeQL, triage and GitGuardian passed, while main-security was skipped.
PR #431 is open, mergeable and clean, with no formal review and no merge. The
failed `b8d3ea8` run remains historical. DELIVERY is not PASS until independent
review and merge occur.

TLS_PREPARED / NOT_DEPLOYED: authorized preparation completed without emitting private material: three
regular TLS files exist at the source path with the recorded directory/file
ownership and modes; public certificate checks pass. The CA private key was
not copied or mounted, and no server restart or image change occurred.

OIDC preflight corrected the configured container user to UID/GID 1000 and
the loopback health interpretation to `standby=false`; neither correction made
an API call. The protected operator file was mode 0664 and was changed to 0600
before read. Its bounded capabilities permit snapshot read/sudo but deny generic
or role token creation; permanent backup identity issuance remains BLOCKED.
The ephemeral packet validator first failed (RED), then passed all nine cases
after three minimal fixes; its public code hash is
`16a4d06ce4b97ca910b31dec0bb13cbaca73e808e38f322d7abd02bfea4280d3`.
Independent security review passed. No token, accessor, secret, private-key or
raw-log value is recorded.

The designated retry is BLOCKED: fresh OIDC authorization TTL is below 600
seconds. No renewal or snapshot API call was made. The selected restore target
remains absent, temporary staging is empty, and host-stage cleanup passed. The
earlier save result is retained as historical but cannot establish a valid
artifact because native inspect is unsupported; it is not relabeled corrupt or
successful recovery. The first restore ledger remains unused/prospective:
`p01-home-empty-restore-20261013-01`, selected 2026-10-12T17:47:08Z, human
`buenhyden`, implementer `p01_home_tls`, independent reviewer
`home_readiness`; no restore executed. Task status remains blocked.

### W23 Snapshot Salvage Receipt — 2026-10-13

The refreshed-OIDC attempt made exactly one native save successfully, then
remained PARTIAL because BusyBox `find -printf` is unsupported in the guard and
cleanup counter. Its owned temporary artifact was preserved; this is neither a
corrupt-snapshot finding nor a recovery PASS. Approved no-token/no-API salvage
then completed in 2.134s: pre/post structural integrity and private hash match,
atomic directory publish, and cleanup all passed.

The final value-free artifact is
`/home/hyunyoun/backups/p01-openbao-20261013/raft-pre-2.7.1.snap` (58,396
bytes). Its directory is device 64512, inode 5382803, UID/GID 1000, mode 0700;
the snapshot is inode 5382808, mode 0600, nlink 1. The private-hash sidecar is
inode 5382809, mode 0600, nlink 1; its value is not disclosed. Runtime remains
the unsealed active 2.6.2 image `11fd...`. Available backup capacity is
55,284,146,176 bytes, above the 1,073,741,824-byte work budget. Filesystem
total is 266,918,543,360 bytes and is not a requirement. Salvage started at
2026-10-13T03:16:15+09:00 and took 2.134s. Snapshot mtime is
2026-10-12T18:10:33Z; it is the
native saved-file timestamp, not a precise Raft atomic-capture instant or a
verification time.

Independent `p01_snapshot_drift` verification passed all guard, structural,
private-hash and path-stability checks in 10.937ms without private output.
Its `observed_at` is NOT_CAPTURED; activation/completion is bounded after
2026-10-12T18:16:15Z and before 18:18:34Z by the root clock. Native save is
bounded by root-clock times [18:06:27Z, 18:14:39Z], not an exact capture time.
NATIVE_INSPECT, SEALED_AUTHENTICITY and SEMANTIC_RESTOREABILITY are NOT_RUN.
This is prepared artifact evidence only, not HOME recovery, cold boot,
current-2.7 consumer authentication or independent-custody acceptance.
The first restore remains contract planning only: target absent, no restore
execution, permanent backup issuer denied and its file absent. Task status
remains blocked.

### W23 Pre-Execution FILE_USABILITY Checkpoint — 2026-10-13

At receipt head `08891676e031d8900efe6250c1cc53260855e608`, candidate-quality
failed with exit 2 in `leaf.local-diff-hygiene`: the pull-request-range adapter
used event base `6de86f9dc36b087cb3a56f0ac7b346c56b58b291` while the checkout
merge parent was `0a00d34bc0c8df30120100be181fee0f4ca49ceb`. This is a CI
base-race receipt, not a source or runtime failure; earlier public leaves,
CodeQL and GitGuardian passed. The fetch/main and root-HEAD observation window
was 2026-10-12T19:03:53Z–2026-10-12T19:06:29Z; an exact wall-clock capture is
NOT_CAPTURED. The freshly fetched main was the same
`0a00d34bc0c8df30120100be181fee0f4ca49ceb`; its 11 foreign P03 paths have no
P01-owned ten-path overlap, and the catalog renderer is unchanged.

Before any target write, the full-App first plan was BLOCKED because fresh OIDC
TTL was 1,166 seconds, below its 1,500-second requirement. After that block, no
renewal, target credential mount/use, snapshot save or restore retry occurred.
The canonical
`first_isolated_restoreability_evidence_generation` FILE_USABILITY form keeps
the same first attempt `p01-home-empty-restore-20261013-01`, selected path,
container and snapshot as UNUSED and excludes OIDC use; it records neither a
target write nor custody proof. CURRENT_VERSION_AUTH and CONSUMER_READ remain
NOT_RUN; HOME_COLD_BOOT, INDEPENDENT_CUSTODY, SELECTED_EMPTY_RESTORE and
RECOVERY are also NOT_RUN. QA file layout proof and final independent readiness
review are pending, and Task status remains blocked.

### W23 Merged-Source Readiness Checkpoint — 2026-10-13

SOURCE_DELIVERY is PASS: the reviewed ten-path P01 diff is in integration
commit `14ae4282948ef7a43ad54c16f5628bc6b15a8520`, merged as
`7620f2d22d6331566b7d14df7ccd536d011235cb`, with shared tree
`282180b7ae188444670d0b847f5574004cdf646f`. Required head-14 CI passed.
Post-main Quality Gates 38299450330 and CodeQL 38299449909 succeeded;
main-security passed and candidate-quality was intentionally skipped. GitHub
formal reviews are none and required reviews are zero; separate IaC and security
agents approved the final operations packet. This source delivery does not
complete any HOME lane.

The published 58,396-byte snapshot remains integrity evidence only. Isolated
FILE_USABILITY QA passed in 71.4s and the probe passed in 61s; neither is a
HOME restore. The final operations packet is READY with public input hashes:
source/main `89d9fb4be12d0551e6f06d68e4a3f55368660d8bf8864712ecb60df4537fb01a`,
monitor `76336a1d6b08e3b40073b1054f8674c7b0501816665b7a48a2abc99e3f437c2c`,
tests `a5f66b2b7dcf9808005e085969d6f1bdeced32cdd8bfe3073d18ba869e05d3c2` and
launcher `d08a585559c213649f2a1ef7036ba15b8e815599ab58a7c54bd4da5dc8ff7878`.

The same UNUSED first FILE_USABILITY attempt retains its selected empty target
`/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013`,
container `p01-home-restore-20261013`, snapshot and guarded coordinator
receipt `/home/hyunyoun/backups/p01-openbao-20261013/p01-home-empty-restore-20261013-01`.
Read-only absence checks passed and the four operation names remain absent;
mandatory execution preflight and source-hash checks are NOT_RUN_BY_DESIGN while
awaiting an ACTIVE operator availability reply. No operation write has occurred.
A normal coordinator has a 900-second limit including handled SIGINT/TERM/HUP
and its 180-second reserve; the monitor's 1 GiB/64 postcondition is not a quota.
SIGKILL,
host-loss and CID-window residuals require manual stop-and-preserve by exact
name/ID, with no automatic retry.

CURRENT_VERSION_AUTH, CONSUMER_READ, HOME_COLD_BOOT, INDEPENDENT_CUSTODY,
SELECTED_EMPTY_RESTORE, SEALED_AUTHENTICITY, cutover and RECOVERY remain
NOT_RUN. An earlier PR-description patch was rejected; the merged-state draft
at `/tmp/p01-pr-body-merged.md` is prepared locally and awaits explicit
approval. Task status remains blocked awaiting human input.

Checkpoint validation passed: Task metadata selected 1 document with 0
violations, and `check-script-manifest` and `git diff --check` each exited 0.
These are SOURCE/DOC checks, not runtime acceptance. The OpenBao 2.7.1
pin/scanner and unrelated service configuration are NO_CHANGE; the only
recorded P01 source exceptions are the client certificate bindings in three
Compose files and their fixture, test and documentation receipts.

### W23 Actual Pre-Restore Outcomes 01/02 — 2026-10-13

Actual attempt 01 was ABORTED_PREFLIGHT, consumed=false, exit 2 in about
0.25 seconds. Its helper mode was 0775 where 0755 is required. The mode-only
FD correction completed from 22:23:57.790134Z to 22:23:57.803510Z with bytes
and inode unchanged: device 64512, inode 2372835, UID/GID 1000, nlink 1,
size 1,859,732 and post-mode 0755. All four reserved names were absent; no
new restore artifact, target, receipt or container was created. The abort wall
clock is NOT_CAPTURED; contemporaneous root clock was 2026-10-12T22:21:33Z,
before the repair upper bound.

Attempt 02 followed reviewed READY evidence but is
BLOCKED_PRE_RESTORE_PARTIAL, not FAILED_RESTORE or FILE_USABILITY failure:
exit 2 after 0.959 seconds, consumed=true, preserved=true and
cleanup_failed=false. Pre-start capability comparison blocked on expected
`CHOWN` versus Docker `CAP_CHOWN`. Coordinator T0 is NOT_CAPTURED. The
root-observed operation window is
2026-10-12T22:30:03Z–2026-10-12T22:30:59Z; the blocked receipt file mtime
2026-10-12T22:30:35.136449541Z is metadata rather than exact durable
completion, and recorded monotonic blocked elapsed is 0.959 seconds. The CHOWN helper
`p01-home-restore-20261013-chown`
(`326a586711e9a1f31d4c9688c718ca64314e582a7253052d241c80e4dafaec3f`) remains
Created and never started. The target is device 2064, inode 115610180,
UID/GID 1000, mode 0750, with exactly empty `audit` (inode 115628621, 0700)
and `raft` (inode 115624583, 0700) directories. This is exclusive target
creation/consumption evidence only. FILE_USABILITY, restore API, CHOWN and
chmod helper execution, watcher, server/bootstrap and original-unseal checks
are NOT_RUN. `cleanup_failed=false` means only that its cleanup call did not
error; it does not claim residual removal. All 02 objects are preserved and
must not be reused; live 2.6 remains running, unsealed, Raft active, restart 0.
Independent drift preservation verification passed with the target IDs/modes,
the two named empty children, the same Created helper, DropAll/no network/
read-only-root/no-new-privileges, the other three reserved names absent and
the live server/Agent state. Its correction observation clock is NOT_CAPTURED.
The operational receipt is
`/home/hyunyoun/backups/p01-openbao-20261013/p01-home-empty-restore-20261013-02`;
it has regular non-symlink `attempt.json` (0400), `chown.cid` (0600) and
`receipt.jsonl` (0600). No receipt content was read.

The canonical lanes HOME_COLD_BOOT, INDEPENDENT_CUSTODY,
SELECTED_EMPTY_RESTORE, CURRENT_VERSION_AUTH, CONSUMER_READ,
SEALED_AUTHENTICITY and RECOVERY remain NOT_RUN. At the 01/02 checkpoint,
attempt 03 had not executed. A
minimal local CAP_CHOWN source-fix preparation is authorized, but a new target,
container and receipt require fresh independent review and user approval.

The approved PR #431 description update is present remotely at
`1088f196bd9aa72ae42c2d8f22c7214e9e700aaf7d84cb0d43c3e0419c0c91fc`
(6,339 bytes), superseding the earlier pending-approval statement. SOURCE_DELIVERY
for PR #431 is PASS; operational delivery remains blocked on this failure and
future execution review/approval.

### W23 Actual Pre-Restore Outcome 03 — 2026-10-13

Attempt `p01-home-empty-restore-20261013-03` is
BLOCKED_PRE_RESTORE_PARTIAL: consumed=true, preserved=true and
cleanup_failed=false. Its SERVER_ENTRYPOINT_LOCAL_CONFIG_READONLY cause is
that the image entrypoint attempted to materialize `BAO_LOCAL_CONFIG` at
`/openbao/config/local.json` while the root filesystem was read-only. The
server exited 1 before Bao server/bootstrap/restore; raw logs are suppressed.
The preserved server
`857395112de2734454864711a15498d435315779af6f911a32a67e8f40997666` has
OOM=false and empty State.Error. Container start passed, but Bao/native
application start was blocked.

ATTEMPT_CONSUMED monotonic time is 0.012 seconds and FILE_USABILITY_BLOCKED is
18.506 seconds at `operation-blocked`; neither is a wall-clock elapsed time.
T0 is NOT_CAPTURED. Durable metadata bounds are attempt.json mtime
2026-10-12T22:42:02.410478Z, target-root mtime 22:42:02.440478Z, server
StartedAt 22:42:19.832086160Z, FinishedAt 22:42:20.311839536Z and final receipt
mtime 22:42:20.945514Z. The root-observed operation window is
2026-10-12T22:41:13Z–2026-10-12T22:43:23Z; file mtimes are metadata only, not
a durability clock.

The preserved target
`/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013-03`
is device 2064, inode 115626592, UID/GID 1000, mode 0700, nlink 4. Its receipt
directory is device 64512, inode 5383336, UID/GID 1000, mode 0700, with regular
non-symlink `attempt.json` (0400), `chown.cid`, `chmod.cid`, `watcher.cid` and
`server.cid` (0600), and `receipt.jsonl` (0600); `bootstrap.json` is absent.
CHOWN, chmod and watcher helpers were removed. `cleanup_failed=false` records
only their successful cleanup, not removal of the preserved target, server or
receipt. Bootstrap/init, snapshot restore API, original-share unseal,
FILE_USABILITY, CURRENT_VERSION_AUTH and CONSUMER_READ are NOT_RUN. The live
OpenBao 2.6 image remains running with restart 0 and OOM=false. Task status
remains blocked; the 19-case local CAP_CHOWN source validation is SOURCE-only.

### W23 Public Native Preparation Receipt — 2026-10-13

Public native preparation is SOURCE-only: the command exited 0 within the
actual native bounds 2026-10-12T23:24:35.376695330Z–2026-10-12T23:25:45.455258032Z.
It preserved OLD03's public RED `configRO` case and showed GREEN for the fixed
functions on OpenBao 2.7.1 amd64 image `a36...`: read-only root, no network,
DropAll, no-new-privileges, UID 100, exact 64 KiB config tmpfs, 16 MiB tmpfs
and mount guards. The native server remained initialized=false and sealed=true
with Raft 2.7.1; CA verification passed and GET health returned 501. This is
not a HOME bootstrap or restore result.

Strict cleanup removed all five names and the scratch root. The archived public
packet is `.agent-work/p01-config-tmpfs-public-native-pass/`, with main input
`0b6d835b5417a4350a8e491a9785df5c3bc2737ce89dff80558ab5cc2081945d` and
driver `c0491cff0b52e25521815b5f1253ef5f77af77e19094ab20a5c9d4967cea4a3d`.
`rtk python3 .agent-work/p01_config_tmpfs_public_fixture.py` exited 0 in
70.078562702s; `rtk python3 .agent-work/p01_home_restore_file_attempt_test.py`
exited 0 with 21 tests (the latest 04-literal packet in 0.033s). Both are
public source preparation; actual 04 was not run.
Earlier `b111`/`896` reports are SUPERSEDED without changing their historical
outcomes. The public native IaC/security packet records the minimal literal 04
proposal; at this public-native checkpoint, attempt 04 had not executed, its
authorization was pending and its execution review was not READY. Unit 21 and
syntax/lint passed. PRIVATE, HOME, FILE_USABILITY, RECOVERY,
CURRENT_VERSION_AUTH and CONSUMER_READ remain NOT_RUN; Task status remains
blocked.

### W23 Actual Selected Empty Restore 04 — 2026-10-13

User authorization for this single FILE_USABILITY attempt, 900-second limit,
180-second reserve and 1 GiB/64 postcondition was observed at
2026-10-13T00:18:01Z (UI timestamp NOT_CAPTURED). No network or live data mount
was authorized. The single `rtk bash .agent-work/run_p01_home_restore_file_attempt.sh`
invocation exited 0 within external UTC bounds
2026-10-13T00:19:10.872801885Z–2026-10-13T00:22:19.787296743Z; actual T0 is
NOT_CAPTURED. Coordinator monotonic events were consumed 0.159s,
unseal-required 42.557s, original-share unseal observed 163.845s and FILE pass
173.108s. The operator entered original shares through the hidden prompt;
no share values are recorded.
These durations are not RPO/RTO or a production-recovery measurement.

The preserved selected target is device 2064, inode 115629820, UID/GID 100:1000,
mode 0700, nlink 4, with nine entries, apparent size 17,093,936 and allocated
size 241,664. The implementer supplied two required databases and two full EOF
passes; private-binding and metadata-unchanged booleans are true. The receipt
directory is device 64512, inode 5383361, UID/GID 1000:1000, mode 0700, with
seven files including protected `bootstrap.json` (0600, CONTENT_UNREAD).
No private bootstrap content, link, hash or raw log is recorded. The attempt is
`p01-home-empty-restore-20261013-04`, target
`/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013-04`,
and receipt
`/home/hyunyoun/backups/p01-openbao-20261013/p01-home-empty-restore-20261013-04`.
It is bound to frozen coordinator SHA-256
`2806d41d149b7a610e6f08e3b6f649e48903e4dbffa0f09fc81940a7c8c2b8bf`, selected source
`7620f2d22d6331566b7d14df7ccd536d011235cb` and tree
`282180b7ae188444670d0b847f5574004cdf646f`.

The temporary 2.7.1 server `p01-home-restore-20261013-04`, image `a36...`, ID
`2119910549cfc5a20b4e20288b99d06119e2da93013231d69e4ca317cb19f76c` started at
2026-10-13T00:19:29.030512028Z and finished at 2026-10-13T00:22:03.469534870Z
with exit 0, OOM=false,
empty error and restart 0. The stopped server is the sole remaining attempt
name; watcher, CHOWN and chmod helpers were removed. Live OpenBao 2.6.2 image
`11fd...` remains unchanged and running with restart 0; attempts 02/03 remain
preserved. Independent IaC actual review passed allowlisted receipt/public
metadata, ledger/limits, no-network/no-port, read-only root, DropAll,
no-new-privileges, exact-tmpfs, target-metadata and live-preservation checks.
The reviewer did not read private contents; file guards are implementer evidence.

Disposition is PASS only for ISOLATED(FILE_USABILITY) and
SELECTED_EMPTY_RESTORE(FILE_USABILITY), with ORIGINAL_SHARE_UNSEAL_OBSERVED.
INDEPENDENT_CUSTODY, SNAPSHOT_AUTHENTICITY, HOME cold boot, WRAPPED_REISSUE,
CURRENT_VERSION_AUTH, CONSUMER_READ, MIGRATION, production cutover,
production RECOVERY and RPO/RTO remain NOT_RUN. W23/P06 holds remain; Task
status remains blocked.

### Isolated Native Rerun — 2026-10-13

The owner asked on 2026-10-13 to review P01 and proceed. On a detached scratch
worktree of `main` `958349408`, the two registered native opt-in commands ran
for the first time since the W23 assessment, both against owned synthetic
`p01-owned-*` containers, volumes and networks, never HOME:

- `HYHOME_OPENBAO_CANDIDATE=1 python3 -m unittest tests.validation.test_openbao_candidate.CandidateNative -v`:
  1 test, OK, 90.5 s.
- `HYHOME_OPENBAO_REHEARSAL=1 python3 -m unittest tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests -v`:
  3 tests, OK, 327.9 s.

No test was skipped, and no `p01-owned-*` container remained afterwards. This
is an ISOLATED result only. HOME issuance and use, the snapshot-only
credential, off-host custody, the reviewed stateful recovery contract and a
real reboot remain the missing inputs that keep this Task blocked.

### Source Corrections — 2026-10-13

The owner asked on 2026-10-13 to review the P01 HOME lane, correct and extend
it, and proceed. No HOME operation, credential read or service change was
made. A read-only review of `main` `338c607d8` found these source points,
re-verified on `ec0877f10`:

- **Outage timing.** RUN-0085 stated a 15-minute service outage limit that no
  policy, requirement or Spec owns. The operator selection recorded in W23
  Current Acceptance Assessment is a 30-minute cutover goal within a
  60-minute maintenance window, as planning estimates. RUN-0085 now uses that
  selection and says it is not an observed RTO.
- **TLS check.** RUN-0085 said the TLS preflight had not run on HOME. W23
  Current TLS and Snapshot Retry Receipt records TLS_PREPARED / NOT_DEPLOYED:
  the three files exist and public certificate checks passed, without a
  server restart. That receipt does not name `check-tls-material.sh`
  itself, so RUN-0085 says the material is prepared and that this exact
  command's HOME run is not recorded.
- **Resolves.** The actual-target FAIL rows 01/02 and 03 were resolved by
  "Public native preparation", a SOURCE-only run on an archived packet. The
  PASS on the same selected target is "Actual selected empty restore 04", so
  that row now resolves them.
- **Stale statements.** The W23 Current Acceptance Assessment tables carry a
  superseded note for TLS and DELIVERY; Review and Completion names the #431
  merge `7620f2d22`.
- **HOME preconditions.** The old row stays as observed; the lanes that remain
  NOT_RUN have their own rows.
- **`.agent-work/` deletion.** The owner decided on 2026-10-13 that the
  git-ignored `.agent-work/` directory will be deleted and its HOME snapshot
  and restore tooling will not move into tracked files. This change does not
  delete it. These Work Log sections and the "Public native preparation"
  Evidence row (Input "archived public packet") point into it:
  - Current P01 Continuation — 2026-10-11 (`integration-proposal/README.md`);
  - W20/W22 Versioned Issuance Continuation — 2026-10-11 (a discovery note);
  - W22 Source Commit and Isolated Attempt — 2026-10-11
    (`integration-proposal/p02-openbao-docs.patch`);
  - W22 Registered Diagnostic Candidate Timeout — 2026-10-11 (a discovery
    note);
  - W22 Source PR and Final Staged Receipt and W22 Accepted Source Delivery —
    2026-10-11 (PR body files, including `p01-pr-body.md`);
  - W22 P02 Catalog Documentation Reconciliation — 2026-10-11
    (`p02-frozen-handoff/p02-openbao-docs.patch`, `p02-views`);
  - W22 P02 Documentation Submission Receipt — 2026-10-11
    (`p01-catalog-pr-body.md`,
    `integration-proposal/p02-catalog-consumer.patch`);
  - W23 Public Native Preparation Receipt — 2026-10-13
    (`p01-config-tmpfs-public-native-pass/`,
    `p01_config_tmpfs_public_fixture.py`,
    `p01_home_restore_file_attempt_test.py`);
  - W23 Actual Selected Empty Restore 04 — 2026-10-13
    (`run_p01_home_restore_file_attempt.sh`).

  Those files become unavailable once the owner deletes the directory. Their
  recorded results stay in this Task as the historical observation; they
  cannot be rerun from those paths.
- **Open gaps, not results.** No Prometheus rule covers OpenBao Agent
  staleness or authentication failure (`alert_rules.openbao.yml`), and
  tampered-HMAC audit verification is NOT_RUN. Adding a rule is an IaC change
  for a separate decision.

Owner HOME checklist, in order; each step needs the approval named:

1. SEC01 accepts the 2.7.1 signature, SBOM and CVE results (SEC01 owner).
2. Decide the preserved attempt targets and containers (explicit approval
   for any deletion). Partly done: see Preserved Attempt Cleanup — 2026-10-13;
   the `-04` target, the base restore target and the snapshot file remain
   undecided.
3. Issue a restricted snapshot-only identity and token with an OIDC session
   long enough for the run (credential issuance).
4. Prove the token cannot read ordinary secrets, prove renewal, then take a
   fresh pre-upgrade snapshot with writes quiesced (backup run). If this uses
   anything other than the tracked backup tooling and RUN-0085 commands, it
   needs a tracked or newly reviewed tool at the time.
5. Attest off-host custody of the unseal shares, offsite key and CA key
   without values (owner attestation).
6. Run a semantic restore to an empty target with a new attempt identity,
   canary read and renderer reauthentication (independent READY review, then
   user approval). Attempt 04 used `.agent-work/` scripts, so this step needs
   a tracked or newly reviewed tool at the time.
7. Measure audit capacity and register logrotate (host change with sudo).
   The running server has no audit mount yet, so this moves to the upgrade
   window in step 8.
8. In the maintenance window: upgrade the server, manual unseal by the named
   operator, then upgrade the Agent with a wrapped reissue (fresh review of
   the authorized runtime-change intent).
9. HOME cold boot (separate approval).
10. Select a consumer and its ACL for current-version authentication and
    consumer read (P06 owner selection).

### Preserved Attempt Cleanup — 2026-10-13

The owner chose "Delete after recording" for the preserved attempt targets
(AskUserQuestion, 2026-10-13). Auto mode refused the deletion to the agent as
irreversible, so the owner ran it personally with `!` commands. This metadata
was captured before deletion; no content was read:

| Object | Identity | Lifecycle | Result | Mounts |
| --- | --- | --- | --- | --- |
| Container `p01-home-restore-20261013-03` | `857395112de2734454864711a15498d435315779af6f911a32a67e8f40997666` | Created 2026-10-12T22:42:19.464Z; started 22:42:19.832Z; finished 22:42:20.312Z | Exit 1, OOM false | `-03/audit` and `-03/raft` (rw); snapshot `raft-pre-2.7.1.snap` and its `.sha256` (ro); TLS CA, server and server key (ro) |
| Container `p01-home-restore-20261013-04` | `2119910549cfc5a20b4e20288b99d06119e2da93013231d69e4ca317cb19f76c` | Created 2026-10-13T00:19:28.244Z; started 00:19:29.031Z; finished 00:22:03.470Z | Exit 0, OOM false | `-04` audit and raft; the same snapshot and TLS mounts |
| Container `p01-home-restore-20261013-chown` | `326a586711e9a1f31d4c9688c718ca64314e582a7253052d241c80e4dafaec3f` | Created 2026-10-12T22:30:34.419Z; never started | - | `p01-empty-restore-20261013` at `/target` (rw) |
| Directory `/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013-03` | Device 2064, inode 115626592, UID 100, mode 0700 | No running container mounted it | Contents not read | - |

All three containers use image
`sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`.

The owner removed the three containers with `docker rm`, emptied the `-03`
directory through a network-less container of the same image running as UID
100, and removed it with `rmdir`. Afterwards no `p01-home-restore-*`
container remains, the `-03` directory is gone, and the live `openbao` and
`openbao-agent` stay healthy.

Kept, because the owner did not decide on them: the `-04` target directory
(UID 100, mode 0700), the base `p01-empty-restore-20261013` target, and
`/home/hyunyoun/backups/p01-openbao-20261013/raft-pre-2.7.1.snap`.

The HOME check of 2026-10-13 also observed that the running `openbao` (2.6.2,
started 2026-10-12T08:45:33Z, unsealed, Raft) has no `/openbao/audit` mount.
The audit file device declared in the repository Compose is therefore not yet
deployed on HOME, and logrotate registration (checklist step 7) moves to the
upgrade window. The snapshot token file is still absent.

### Owner Decisions — 2026-10-13

The owner answered four AskUserQuestion prompts on 2026-10-13 after the HOME
check recorded above.

**Snapshot-only token: combine with the upgrade window.** The owner first ran
the RUN-0021 issuance block in a terminal with the OIDC operator token.
`bao policy write backup-snapshot` was refused with HTTP 403 permission
denied: `operator.hcl` intentionally grants no `sys/policies/acl` write and no
orphan token creation. The token therefore needs a temporary root token from
the recovery-share ceremony (RUN-0085 "Human Login and Normal Root
Recovery"), and the owner chose to issue it in the same ceremony as the fresh
pre-upgrade snapshot and the upgrade (checklist step 8). No partial file was
created; `secrets/backup/openbao` was checked by name only. Until then the
daily backup's OpenBao snapshot keeps failing with "OpenBao snapshot token
absent", the recorded recovery gap.

**Leftovers: delete the targets, keep the snapshot.**

- Base target `/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013`:
  uid 1000, mode 0750, inode 115610180, holding only empty `audit/` and
  `raft/` (uid 1000, mode 0700). No running container mounted it. It was
  removed with `rmdir` on 2026-10-13.
- `-04` target `/home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013-04`:
  device 2064, inode 115629820, uid 100, gid 1000, mode 0700, mtime
  2026-10-13 09:19:17 +0900; no running container mounted it. The agent's
  auto mode refuses irreversible deletion, so the owner deleted it on
  2026-10-13 with
  `docker run --rm --network none --user 100 --entrypoint /bin/sh -v /home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013-04:/t sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005 -c 'rm -rf /t/* /t/.[!.]*' && rmdir /home/hyunyoun/storage/volumes/security/openbao/p01-empty-restore-20261013-04`.
  Afterwards no `p01-*` directory remained under
  `/home/hyunyoun/storage/volumes/security/openbao/`, and live `openbao` and
  `openbao-agent` were both `Up (healthy)`.
- Kept: `/home/hyunyoun/backups/p01-openbao-20261013/raft-pre-2.7.1.snap`, as
  a rollback point until a fresh pre-upgrade snapshot exists.

**Agent alert: record the gap now, separate Spec later.** `openbao-agent`
exposes no metrics: `agent.hcl` has no telemetry or listener, and Prometheus
does not scrape it. Its Docker healthcheck (`scripts/health-agent.sh`) checks
token lookup, KV reads and the rendered byte match, so staleness or auth
failure appears only as Docker `unhealthy`, with no alert. A future Spec adds
Agent telemetry, a scrape job and an alert with IaC review; RUN-0085 lists the
gap.

**Off-host custody: not separated yet.** No independent off-host custody of
the unseal shares, the offsite key or the CA key exists. Checklist step 5 is
NOT_RUN for that reason, and P01 stays blocked.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline | 1, 11 | W19 | status, refs, fetch, scoped baseline diff | 1ee5d6707e3b75b61222baad0c51050c64e1b10d | PASS | W19 Baseline and Boundaries | - |
| Renderer trust | 11 | W20 | Negative token/CA/modes, native clients and Agent restart | e4bde131a34928e19266ddc6dbe86ecc78ccc4ef895d44f39666f60e2e2a9fee | PASS | W20 and W22 | - |
| Audit and recovery | 11 | W21 | Native audit-full denial, snapshot save/empty restore/unseal | e4bde131a34928e19266ddc6dbe86ecc78ccc4ef895d44f39666f60e2e2a9fee | PASS | W21 and W22 | - |
| Public source review | 11 | W22 | Independent security and IaC; code review delta | ef22f5f377a13185fb396e3b65e33debedf67108257dd3098a579c0292b1c35a | PASS | W22 and W22 Regression Contract Follow-up | - |
| HOME preconditions | 11 | W23 | Named host, CA and independent custody; host, target and TLS preparation later observed, the remaining lanes are the rows below | User P01 and `ok` | NOT_RUN | W23 HOME Boundary and P06 Hold | - |
| Versioned journal source | 11 | W22 | Independent code/security; 47 unit tests, 90% coverage | helper `be2343a0...` | PASS | W22 Source Commit and Isolated Attempt | - |
| Changed fixture native metadata | 11 | W22 | v1/v2 exact reconciliation, wrapped login/replay denial | `868e44af22ecf1f5be5c1e6d3b38a292f37a7838141c15bdf00ee07ad490ca0b` | PASS | W22 Changed-Input Native Metadata Receipt | - |
| Scoped regression | 11 | W23 | Five public modules, 77 PASS / 4 skipped | base `62556dc63b66c828c27e9c33017d26cdf70b8542`; patched input `95dc53a900fe7d22ea49e830adc0ff5f69b7a82ab9b4daedd66f33edf5b512ff` | PASS | W23 Current Acceptance Assessment | - |
| Synthetic full rehearsal | 11 | W23 | Exact-image full trust and recovery fixture | `95dc53a900fe7d22ea49e830adc0ff5f69b7a82ab9b4daedd66f33edf5b512ff` | PASS | W23 Current Acceptance Assessment | - |
| Client-mount repair | 11 | W23 | RED/GREEN, selected suite, public Compose render, YAML lint and independent IaC/security review | `f42ea58a66214b32bb1c8d7be589b3ba838d59abbe7610e5e1515008670b4f8e` | PASS | W23 Client-Mount Correction Admission | - |
| Actual pre-restore 01/02 | 11 | W23 | Mode preflight then bounded capability gate; no server start | live HOME target; value-free receipt | FAIL | W23 Actual Pre-Restore Outcomes 01/02 | - |
| Actual pre-restore 03 | 11 | W23 | Entry-point local-config write blocked before bootstrap/restore | live HOME target; value-free receipt | FAIL | W23 Actual Pre-Restore Outcome 03 | - |
| Public native preparation | 11 | W23 | 2.7.1 isolated config-tmpfs preparation and cleanup | archived public packet | PASS | W23 Public Native Preparation Receipt | - |
| Actual selected empty restore 04 | 11 | W23 | Selected empty-target FILE_USABILITY; independent IaC actual review | isolated HOME target; value-free receipt | PASS | W23 Actual Selected Empty Restore 04 | Actual pre-restore 01/02, Actual pre-restore 03 |
| Isolated native rerun | 11 | W23 | Registered CandidateNative (1) and rehearsal (3) opt-in tests, no skips | `958349408` | PASS | Isolated Native Rerun — 2026-10-13 | - |
| HOME snapshot credential | 11 | W23 | Restricted snapshot-only identity and token; ordinary-secret denial; renewal. Operator-token attempt refused with HTTP 403; deferred to the upgrade window's root ceremony by owner decision | Owner checklist steps 3–4 | NOT_RUN | Owner Decisions — 2026-10-13 | - |
| HOME custody attestation | 11 | W23 | Off-host custody of unseal shares, offsite key and CA key, value-free; owner states it is not separated yet | Owner checklist step 5 | NOT_RUN | Owner Decisions — 2026-10-13 | - |
| HOME semantic restore | 11 | W23 | Empty-target restore with canary read and renderer reauthentication | Owner checklist step 6 | NOT_RUN | Source Corrections — 2026-10-13 | - |
| HOME audit capacity | 11 | W23 | Audit filesystem capacity and logrotate registration | Owner checklist step 7 | NOT_RUN | Source Corrections — 2026-10-13 | - |
| HOME upgrade and cold boot | 11 | W23 | Server and Agent 2.7.1 upgrade, manual unseal, wrapped reissue, cold boot | Owner checklist steps 8–9 | NOT_RUN | Source Corrections — 2026-10-13 | - |
| Source corrections | 11 | W23 | Runbook timing and checklist, Task stale points; changed metadata (2 documents, 0 violations), corpus lifecycle (0), links `--mode all` PASS, `test_operations_catalog` OK, markdownlint passed | Branch on `ec0877f10` | PASS | Source Corrections — 2026-10-13 | - |
| Attempt cleanup | 11 | W23 | Owner-run removal of attempt 03, 04 and chown containers and the `-03` target; no container left, live server and Agent healthy | HOME, value-free metadata | PASS | Preserved Attempt Cleanup — 2026-10-13 | - |
| Audit logrotate registration | 11 | W23 | Deferred: the running server has no audit mount, so registration waits for the upgrade window | HOME check 2026-10-13 | NOT_RUN | Preserved Attempt Cleanup — 2026-10-13 | - |
| Leftover target cleanup | 11 | W23 | Empty base target removed with `rmdir`; `-04` target deleted by the owner; no `p01-*` directory left, live server and Agent healthy; pre-2.7.1 snapshot kept | HOME, value-free metadata | PASS | Owner Decisions — 2026-10-13 | - |
| Agent alert gap | 11 | W23 | No Agent metrics or alert; gap recorded, telemetry and alert deferred to a separate Spec | `agent.hcl`, Prometheus config | NOT_RUN | Owner Decisions — 2026-10-13 | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 11 | pending | - | - |

## Review and Completion

Source delivery is merged in PR 421 and in PR #431 (merge `7620f2d22`); the current Task
remains blocked on the named W23 target/custody and runtime residuals. Source
and isolated proof do not complete HOME custody/boot/recovery acceptance or
authorize P06. No secret migration or consumer switch is claimed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [P00 Task](../../0212-request-baseline-and-reconciliation/tasks/tsk-0003-active-contract-and-exclusions.md)
- [OpenBao Runbook](../../../05.operations/runbooks/04-security-and-secrets/0085-openbao.md)
- [Backup Runbook](../../../05.operations/runbooks/10-platform-and-backup/0021-backup-and-restore.md)
