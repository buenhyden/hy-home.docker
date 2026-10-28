---
title: "OpenBao Trust Bootstrap and Recovery Task"
version: "0.2.37"
type: "sdlc/task"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0006"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-10"
---

# OpenBao Trust Bootstrap and Recovery Task

## Overview

### Objective

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

The 2026-10-14 direct user request supersedes the earlier source-only operation
limit: execute deployment, issuance, migration, retirement and recovery, then
clean related development branches/worktrees. The latest steering prioritizes
OpenBao issuance and upgrade. This authorizes concrete preparation and the
named maintenance operations; it supplies no missing cryptographic quorum,
independent custody or authenticated input. The user's current answer is
"independent custody or holders need preparation" and asks for investigated
resource choices before migration/retirement/restore selection. Secrets remain
outside chat, Git, argv and ordinary logs.

The latest trusted reply assigns the operator to `buenhyden` and confirms that
unseal shares and off-host custody are prepared. This supersedes the earlier
preparation-needed answer. It is an owner readiness attestation, not observed
secret input, a named custody-location receipt or completed recovery evidence.
Two distinct shares and current OIDC authentication still enter only through
the reviewed protected client.

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

### Maintenance Window Plan — 2026-10-13

The owner chose on 2026-10-13 (AskUserQuestion) to prepare a maintenance
window for the remaining HOME steps. RUN-0085 now has "HOME 유지보수 창 계획":
off-host custody (step 5) as the precondition, then W0 pre-flight, W1 root
ceremony through `bao operator generate-root` with two shares on hidden input,
W2 the RUN-0021 snapshot token with denial and renewal checks, W3 a fresh
pre-upgrade snapshot with the Agent stopped, W4 server upgrade to the compose
pin and manual unseal, W5 Agent upgrade and wrapped SecretID reissue, W6 audit
mount and logrotate, W7 post-checks and root revocation, and W8 cold boot in a
separate window. Each step names its command, expected signal, stop condition,
rollback limit (no in-place Raft downgrade; a failed upgrade restores the W3
snapshot to an empty target with the previous image) and approver. The
`generate-root` flags were checked against the OpenBao command reference on
2026-10-13. The timing table keeps the recorded 30-minute cutover inside the
60-minute window as planning estimates. The semantic restore (step 6), the P06
consumer and ACL (step 10) and the Agent alert Spec stay after the window.
This is a document; no HOME step ran.

### Maintenance-window input correction — 2026-10-14

Current ALL_PROMPTS authorizes a safe Runbook correction only. Independent
security review found that the window promised stdin-only sensitive values,
then passed OTP through CLI arguments and assumed the running server container
had no observing process. This is a source-plan defect; W1 was NOT_RUN and no
credential exposure, issuance or rotation is claimed.

The unsafe CLI block is removed. W1 now delegates to the existing protected
authenticated API contract and remains blocked until an actual reviewed client,
exact target/permissions/recovery and independent custody exist. Neither a
container shell nor encoded-token stdin makes the OTP argument private. The
original maintenance-plan and owner-decision receipts remain historical;
off-host custody, snapshot token, upgrade, audit, cold boot and semantic restore
remain NOT_RUN, and criterion 11/Task state remain pending/blocked.

The controller owns only RUN-0085 and this Task for this logical document unit.
No helper, policy, credential, container, backup or host state is changed.

Independent security review approved RUN-0085 SHA256
`81ce399fead9074dd92f06b37094e9cc30a987709fa5cbe24e6e209e4d03521b` and
this Task's pre-receipt SHA256
`526a6916eb5847cd6b2a0b7a597156e6209683fd801ad8572a297d47f8ca0cdc`.
The reviewer verified the protected API/client/custody preconditions, no
executable OTP argv block, no runtime claim, and pending criterion 11/blocked
Task. QA's explicit metadata selection of these two plus twelve P08 documents
passed 14/0; operations catalog and navigation checks passed, exit 0. These
checks precede this result-only receipt, whose final document validation and
staged hooks remain required. Source correction acceptance does not admit W1
or supersede any HOME, maintenance or recovery finding.

### Off-host Custody Procedure — 2026-10-14

On 2026-10-14 the owner asked to review and proceed with off-host custody
separation, and chose (AskUserQuestion) to prepare the procedure first.
RUN-0085 0.8.0 adds "off-host custody 분리 절차": the items (unseal shares 1
to 3, offsite key BKP-003, R2 credentials BKP-004 and BKP-005, the CA private
key), the rule that no place holds two or more shares, that host disk, host
backups and the R2 copy do not count as off-host, and a value-free
confirmation table the owner fills. The agent read no value and moved nothing.
Checklist step 5 stays NOT_RUN until the owner returns the filled table; the
single-file exception and any deletion of that file remain a separate owner
decision. Criterion 11 and this Task stay pending and blocked.

An independent security review of the first draft (PR #461) returned FAIL:
the Restic host backup holds all of `secrets/`, including the single unseal
file, and `restic-offsite` copies it to R2, so the offsite key BKP-003 with
R2 read access yields all three shares; the draft let the offsite key share a
place with a share. The procedure now treats BKP-003 as equal to the full
share set, keeps it apart from every share and from the R2 credentials,
records a step 5 result only as `owner-attested` when every answer is yes
(`FAIL` on any no), says a pass does not close the POL-0085 exception, and
says copy rather than move. Excluding the unseal file from the host backup
needs a separately approved IaC change; that coupling stays open.

### Unseal File Exposure Decisions — 2026-10-14

After PR #461 merged, a re-review of the procedure found the Cloudflare
account (which can reissue the R2 credentials) missing from the confirmation
table and a place left undefined. On 2026-10-14 the owner asked to review and
proceed with the exposure finding and chose (AskUserQuestion) to exclude the
unseal file from the host backup and to rekey, and to correct POL-0085's
"only copy" statement. SPEC-0240 carries the exclusion, the POL-0085 and
ADR-0042 corrections and RUN-0085 0.9.0: the Cloudflare account row, the
place definition, the merge gate (merge only after step 5 is
`owner-attested`) and W1b unseal rekey right after W1 and before any new
snapshot, BLOCKED until a reviewed protected output path exists. A rekey does
not change the keys a pre-rekey Raft snapshot opens with, so the exposure ends
only when pre-exclusion host snapshots are deleted. Nothing ran on HOME; step 5 and
criterion 11 stay as before.

### Agent Alert Source — 2026-10-14

SPEC-0239 added the Agent telemetry, scrape and alerts the 2026-10-13 gap
record deferred: a `metrics_only` listener, Prometheus job `openbao-agent`,
`OpenBaoAgentMetricsScrapeFailing` and `OpenBaoAgentAuthFailure`. It merged
in PR #463 and its review fixes in PR #466, whose `candidate-quality` passed.
It is not deployed: the Agent recreate needs a fresh wrapped SecretID, then a
Prometheus restart, both separately approved. A render that goes stale while
authentication works still shows only as Docker `unhealthy`. RUN-0085 0.9.1
states this; the gap row stays NOT_RUN until deployment.

### Single-Administrator Custody Places — 2026-10-14

The owner stated that one administrator holds every place and chose three
places with a condition (AskUserQuestion). RUN-0085 0.10.0 now counts places,
not people: three places, one share each; BKP-003 apart from the R2
credentials and Cloudflare account access, and from every share until the
exclusion is confirmed (SPEC-0240 criterion 4) and listings of the local host
and R2 repositories show no pre-exclusion host snapshot. The first storage still needs a fourth, share-free
place. Step 5 is attested against that table; SPEC-0240 W5 holds the record.

### Current Operation Preparation — 2026-10-14

Local main and fetched origin/main were clean at
`1e7e2ba841c4e428a06762a61a570011711bc1ef`. PR459 and PR460 had already
merged externally; their merge receipts are not an agent-run deployment.
The integration writer uses `codex/openbao-maintenance-integration`; P01 owns
only the protected client/tests, P06 its bounded copy primitive/tests, and
this writer owns shared CI, manifest, Plan, Task and Runbook updates.

Read-only HOME preflight observed server `d2943ebb0619` and Agent
`0f0a8494f289`, both healthy on the historical 2.6.2 image. Auth-free status
reported initialized/unsealed, Raft, Shamir threshold2/shares3 and cluster
`51fbfa38-a715-7dca-629f-3f07233749f4`. The selected server mount was
`hy-home-infra_openbao-data`; the current server has no selected TLS/audit
mount. The current backup unit reported `Result=exit-code`, `ExecMainStatus=1`
and failed state at 2026-10-14 03:43:29 KST. Raw logs and credentials were not
read. The preserved 2026-10-13 snapshot remains a 58,396-byte regular 0600
file; metadata inspection is not a fresh snapshot or successful recovery.

Actual candidate preparation pulled the approved linux/amd64 child
`sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`
of source index
`sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf`.
The isolated `bao version` probe had no mounts/network, readonly filesystem,
all capabilities dropped, no-new-privileges, PID32/memory128MiB/CPU1 bounds;
exit0 reported 2.7.1 revision `a5db72cef75c24b920ade02065b18dd8eb666bac`.
The invocation-owned transient container was removed. No server was started.

Publisher verification used authenticated pinned Cosign OCI
`sha256:9e5c2f2edc34351160407ca3416c61855bdf9403c3c5936e0f0be7fc261611b8`.
The first attempt failed because the tool's `.sigstore` cache was readonly.
An ephemeral cache fixed that environmental failure; the next attempt still
failed because the binary-checksum `release.yml` identity did not match OCI
images. Official tagged `release-images.yml` confirmed the distinct image
workflow. The final exact image identity
`https://github.com/openbao/openbao/.github/workflows/release-images.yml@refs/tags/v2.7.1`
and issuer `https://token.actions.githubusercontent.com` verified the exact
index: exit0, four signature rows, certificate trust and transparency claims
verified. Identity checks were retained; neither failure is a vulnerability
scan result. Selected SBOM/CVE acceptance remains separate.

The exact external gateway is `https://openbao.hy.home.arpa:443`, numeric
connect IP `192.168.0.13`. Its public CA is
`/home/hyunyoun/data/hy-home.docker/secrets/certs/rootCA.pem`, SHA256
`6b7c5c752a6dee074b7f9c83da98b2b8784831edde3d8f50b694acd0e280af87`,
UID1000/GID1001, mode0644, one link, 1,700 bytes. A token-free TLS probe
verified CA/SAN with TLSv1.3; certificate expiry was 2028-12-17. This public
hash pins gateway trust and does not hash a key or unseal share. Internal
OpenBao backend trust and its planned audit deployment remain distinct.

The initial protected client passed 34 synthetic tests/94% coverage but
independent reviews rejected it: decoded root was not authenticated; CA
provenance was unpinned; secret roles could contain equal bytes; deep JSON
could escape sanitized errors; cleanup/output could downgrade post-mutation
uncertainty to BLOCKED. These source findings are preserved pending the
corrected exact-input review. No actual ceremony occurred.

The corrected frozen client is SHA256
`640a3bd7cc913028d0e9c67ab31bed385341339386b4c4e572c0b14544a17506`;
base tests are `c8cba04c8246835646523c239a48677ea40fbe9e4762f4df06a211bfd65c5f5c`
and review tests `6b68869c1e13745a41bde58c4c07b5640032a4a2da11056759c237e3367d9964`.
Correction RED recorded six failures/three errors before fixes; a companion
fixture/import error was corrected before the final unique test collection.
Independent QA command:

```sh
rtk /tmp/hyhome-p04-qa-tools/bin/python -m unittest tests.validation.test_openbao_protected_maintenance tests.validation.test_openbao_protected_maintenance_review -v
```

Exit0: 46/46 PASS, skip0, 4.015s. Independent branch coverage was93%
(408 statements,22 misses,146 branches,13 partial); scoped Ruff/format/diff
passed. Code and security reviewers independently approved the exact three
hashes after verifying separate decoded-root lookup, public CA provenance
before secret input, distinct role bytes, bounded JSON and post-mutation
cleanup/output uncertainty. This resolves the initial source review defects,
not any HOME prerequisite or historical backup/restore failure. The Runbook
uses only public flags, approved-blob private copy and hidden input.

The next separately reviewed compatibility delta admits only the exact owned
version `2.7.1+hyhome.go1.27.2.net0.60.0.r1`. Current parent source is
`2c6101572dca382752cc5cef25f9d5d1ed18804e40c43984f41ea6e5d80734a2`;
base tests remain `c8cba04c8246835646523c239a48677ea40fbe9e4762f4df06a211bfd65c5f5c`
and review tests are
`13feeb75590ded2cba39c0f44189c6bac81ed9b6d29a81b9f497ab5e0caf3b8a`.
Focused RED rejected the owned version before the change; the combined suite
then passed47. Independent security replay passed47/3.137s; code review
approved the exact delta, while its sandbox replay failed before collection
and supplies no test PASS. Arbitrary owned suffixes and r2 remain rejected.
This allowlist does not authenticate an image: native version, provenance and
selected security acceptance remain required before operational use.

The new separate TokenOps unit implements only restricted snapshot-token
issuance and temporary-root revocation. Initial source `3b3f0f8c` passed85
synthetic tests but independent review rejected optional recovery-operator
authentication, arbitrary HOME/custody aliases, method-insensitive status
admission, malformed response schemas and an inadequate operator lifetime.
That test PASS is not review acceptance. One combined correction recorded
RED4 failures/2 errors and froze helper
`eecf50f6d3f3bbe419c6213216d57715f4ae32069dbed4eb08c8780ea2c2e688`,
base tests `38f109095f582fd7b3f35837f9e3666053efe4d04159e4a49c1f2e92a57563ca`,
review tests `41ff32b01c79ec13aac2934a40cd839f3002bcb4acde21afded1eaf575efa79c`
and policy `1aa658e05aee76127c7961abd218020fe6a319fd26253c78ecefb3ae99d4b622`.
Independent QA passed99 unique tests/skip0/6.545s, branch coverage87%, scoped
Ruff/format/diff and unchanged hashes. Independent code and security reviews
approved that correction. The exact fixed destination is absent token and
absent issuance lock under `secrets/backup/openbao`; metadata-only preflight
observed this directory device64512/inode5260267, UID/GID1000, mode0700.
Canonical HOME was device64512/inode4338469. Expected identity inputs come
from this pre-recorded public receipt, not the caller's self-authorization.

Issuance authenticates actual root, permits only the absent/known prior/exact
policy, creates one no-default-policy 720-hour orphan service token, proves
exact capabilities, ordinary-secret denial and renewal, and delivers once
without overwrite. Revocation requires separate protected root/OIDC inputs,
an exact renewable service operator with at least600 seconds TTL immediately
before POST and afterward, and root403 afterward. The current root remains
in protected custody on ambiguity; no credential has actually been issued,
read, renewed or revoked by this source preparation.

Initial protected snapshot source `062e929b` passed76 synthetic tests and83%
branch coverage, but independent code/security review rejected fabricated
renewal fields, incomplete native metadata validation, output-path rebinding,
receipt namespace and final digest binding, source/output aliases and
post-effect cleanup/uncertainty handling. Its correction remains pending;
these tests do not admit W3 or provide a fresh backup.

Seven clean merged related worktrees/local branches and five remaining remote
branches were removed with normal non-force operations after exact SHA,
ancestry and ownership checks. COORD's ignored handoff directory was moved
without reading its contents to
`.agent-work/retained-development-handoffs/20261014/coord-current-handoff-repair`;
filesystem identity was preserved. Dirty foreign worktrees, unmerged drafts
and operational receipts remain held. No volume, private source credential or
snapshot was deleted by this development cleanup.

Independent current IaC review found three executable-plan gaps: semantic
restore had been deferred after the window despite being a pre-upgrade gate;
W3's bare snapshot command supplied no restricted token or atomic host artifact;
audit setup was deferred until after server creation. RUN-0085 now requires
W3a before W4, delegates W3 to the tracked protected backup flow and requires
audit/rotation preparation plus ordered gateway/monitoring trust rollout.
No new restore CLI is invented. Current exact artifact/empty-target/restore
executor admission remains missing, and the protected client does not implement
snapshot-token issuance or restore.

Actual bounded audit-directory preparation followed independent IaC READY.
The first exact noninteractive sudo command failed exit1 without creating the
directory; a fixed-image direct-mkdir alternative was independently reviewed.
Its first Docker argument attempt failed exit125 and left the path absent.
After correcting the mount syntax, the same current2.6.2 image, UID100:GID1000,
network-none/readonly rootfs/all-caps-dropped/no-new-privileges/PID16/memory32MiB/
CPU0.25 invocation created only the absent audit directory, exit0. Exact target
`/home/hyunyoun/storage/volumes/security/openbao/audit` now has device2064,
inode115609395, UID100/GID1000, mode0700 and 2,742,595,534,848 available bytes.
Parent identity stayed unchanged; the transient was removed. Audit file,
named volume, logrotate and server mounts were not created or modified.
Rollback is only rmdir of that same empty unmounted inode; private sibling
contents were not read and no recursive ownership change occurred.

The dedicated host audit-rotation rule is source-approved at SHA256
`2ad4473a4f7f3fcaae37a9ad430b32a8ebf9398853ea8b0090233c74b2eaf765`;
focused tests are `e0c36c1ffb2e3ec27fca6513629e9b573711eaad40da3006c22db2a74ffee212`.
The first name-based inspect/kill race was reproduced with2 RED failures;
the correction captures a full immutable container ID, verifies running and
exact Compose labels on that ID, then signals that same ID. Seven meaningful
shell/static tests passed; the coordinator's pre-NSS replay passed7/0.032s.
The subsequent native parser rejected both numeric group forms. The final
rule uses the actual public host mapping `dhcpcd`→UID100 and `hyunyoun`→GID1000,
retaining mode0600, rename/create, no copytruncate and delayed compression.
Independent IaC re-review approved the final exact two-file source delta.

An initial host probe observed no logrotate package/config/units. A later
independent probe and controller metadata recheck observed executable/config
and an enabled active daily timer, with file ctime2026-10-14 09:40:51 KST.
Actor/cause is unknown; no agent installation is claimed. Current package is
3.21.0-2build1. Host debug parsed the rule but failed its unprivileged UID
transition with EPERM; noninteractive sudo failed. Public-only Alpine package
preparation retained its initial bind-permission failures before successful
signature-enforced offline installation. An independently matching official
key hash207e4696 authenticated the selected key; no allow-untrusted was used.
Final isolated logrotate3.22.0 debug used network-none, readonly root/package/
rule/public NSS inputs, UID100:GID1000 and no capabilities: exit0, one rule,
daily/maxsize268435456/rotate14, absent audit file skipped. Postrotate, actual
host state-file access and rotation were never executed. The different tool
version and host privilege failure remain visible.

The rule's256MiB/14-file sizing is provisional, not measured retention or a
hard file-size bound. W0 still requires atomic root-owned registration,
privileged host parser and hourly scheduling using the same global state and
lock; W6 requires actual inode/reopen/growth/failure-alert evidence. None is
supplied by isolated debug or Docker HUP delivery. Public preparation receipts
remain under `/tmp/hyhome-p01-logrotate-parser-20261014`; no private audit
contents were read and no host rule, timer or audit file was installed.

The snapshot b390 intermediate passed88 synthetic tests but review found
overwrite/publication, post-save uncertainty and source-directory binding
defects. The fbaf intermediate passed95 tests but its link-then-unlink
publication could lose the sole verified copy after a concurrent final-name
replacement. These remain failed reviewed inputs despite their test counts.
The final main2779382f/archive48ff7d0e/custodyfd266cdd packet replaces that
publication with typed dirfd-bound Linux renameat2(RENAME_NOREPLACE), without
fallback. Both snapshot and receipt retain partials on EEXIST/ENOSYS, bind the
held FD to the final inode and revalidate/fsync. No code separately unlinks
the last verified partial after binding. Save/final-check/close/success-output
interruptions conservatively report INDETERMINATE. Independent code/security
approval and QA100unique/0skip passed; branch coverage85%/83%/89% for the
three sources. RUN-0085 installs these exact approved blobs and uses the
authenticated standalone save, while preserving separate writer-quiescence,
offsite and semantic-restore evidence requirements. No HOME snapshot ran.

Selected SEC01 inspection completed successfully as tool execution and
artifact binding, but independent review confirmed the candidate's Linux
HTTP/2 GO-2026-6612 applicability. TSK-0009 owns exact scanner hashes and
security disposition; this official2.7.1 artifact is BLOCKED for deployment.
A patched accepted artifact is needed in addition to physical custody and
recovery inputs. The current2.6.2 runtime was not scanned by that result.

The user explicitly chose an owned rebuild using patched Go and x/net, twice
through the current trusted question-reply channel. This authorizes the
selected public source/build preparation, not acceptance of the vulnerable
official image or completion of physical custody. SEC01 owns the authenticated
source, minimal module closure, bounded offline build and fresh artifact scan.
Neither an uncompiled recipe nor a synthetic source test admits W4/W5.

The frozen owned-build r3 source packet
`e2487b5b6822162eaf8aad603630167f7f80c3672f8f6e618ee98f07c8f38b53`
passed independent code/security/IaC review and 41 unique unit tests, with
independent branch coverage88%/85% for the builder/OCI helper. All seven
native-input files were intentionally staged. The existing Git attributes
pattern for unified-diff context markers was reused for the module patch;
cached diff checking then passed without changing native inputs. A fresh
read-only plan and immediate resource/output-absence preflight passed.

Actual compile pass1 failed after53.649s with exit1: Go used the bounded128MiB
`/tmp` tmpfs for its work directory and reported ENOSPC. The container was not
OOM-killed and its exact created ID was removed. The failed output, public
compiler diagnostics and receipt remain under
`/tmp/hyhome-p01-selected-image-security-20261014/owned-build-frozen-r3`.
This is an execution failure, not an accepted artifact. The affected fix uses
the existing fresh disk-backed cache mount for Go temporary work; no HOME
mount, network access or increased container limit is authorized by this result.

R4 packet2370a5d3 adds only a fresh0700 cache/tmp and GOTMPDIR on the existing
writable cache mount. Independent affected code/security/IaC reviews and42
unit tests passed. Actual compile1 passed in446.855s and runtime1 in14.873s,
both without OOM and with exact-created-ID cleanup. The wrapper then failed
before pass2. A complete first-pass OCI exists, but reproducibility is NOT_RUN;
the remaining post-runtime resource/material/source guards are under diagnosis.
The wrapper's generic Blocked output does not prove a specific historical
resource measurement, so no inferred cause is accepted as an observed result.

Common-integration r1 failed independent review: ambient Git/Python execution
did not bind the actual credential-bearing process; exact W3 off-host artifact
custody was not a mandatory W4 stop; and RUN-0021 used a nonexistent anchor.
Light QA separately found a runtime-literal deficit, unsorted manifest rows
and untracked source references. The r2 edits began after code/security review
but before QA's final hash comparison, so its input mismatch is also preserved
as a failed input rather than frozen acceptance. The correction uses explicit
system tools, cleared Git/Python environment, canonical HOME/Git identities, a resolved full commit and isolated/no-site Python; W3b now gates W4 on the
exact snapshot and receipt's independent copy. Source paths are intentionally
staged, manifest rows sorted and the pre-upgrade observation explicitly
distinguished from a deployment pin. Fresh final checks remain required.

Common r2 code/security re-review accepted its process and custody corrections,
but independent QA still rejected the P06 authority: RUN-0085 was draft and did
not directly govern the two runtime modules. Three README links also resolved
against repository-root scripts instead of the OpenBao directory. The links
now use explicit relative paths. Independent rules review confirmed the
Registry's operational-policy draft-to-active edge and existing direct-owner
authorization for source and actual operations. The owner is @buenhyden, who
accepted the manual operator role and selected the isolated recovery target;
the trusted user messages remain the authorization record, not this Task's
assertion alone. This unit activates RUN-0085 as the reviewed current reusable
procedure and directly binds the P06 runtime modules. It does not activate a
production copy CLI or claim any actual maintenance/recovery acceptance.
The RUN-0085 source activation is recorded in this Work Log, not in the
Spec Package lifecycle-event table: RUN-0085 is an operations artifact outside
this package. The table retains only the package member's Task transitions.
Exact common r2 review input was b617d339749106f7dadd8de9305aa9d43500bac15384d63906edb7128e40b561;
the activation/link delta requires its own fresh freeze, independent review
and registered gates before delivery. Every W3a/W3b/P06 runtime stop remains.

Common r3 security review accepted the unchanged command/custody boundary,
but rules review rejected wording that implied the controller grants approval.
The r4 correction says the controller verifies and binds the actual trusted
user/native authorization. Independent exact-hash rules review passed r4
manifest10eb5361 (RUN-0085 f3b44449); its other eleven rows equal r3. This
resolves that wording finding only. Registered aggregate gates and delivery
remain pending, and the earlier r1/r2 failures remain preserved.

The separately admitted r4 native attempt2 completed both independent clean
Go compilations and both runtime assemblies without OOM. The two binary
SHA-256 values equal f0b103b853891539cfe4c01421074077de8b3665b189ecbe3159f7966d876a51;
both build-info digests equal77b26c30d4d08d41ffb13dad917d73ed98482c898166d9c6100cf7403c12990f.
Whole-image reproducibility nevertheless FAILED: the sole normalized-layer
member difference is var/log/apk.log content containing installation wallclock
stamps. Exact differences are retained in the public selected-image inspection
directory's owned-build-r4-attempt-2-repro-differences.json. No accepted owned
artifact, image load, scan or HOME change follows from those compiler passes.
R5 is a separately reviewed packaging correction; no failed attempt is resumed
or relabeled as a whole-build PASS.

The renderer token-file source slice initially passed55 synthetic tests but
independent security review found a mutable request-shell reopen after receipt
validation. The corrected source must execute the same held verified peer bytes
before any credential input; the old packet2f671fe3 remains REVIEW_FAIL.

The user's off-host reply is investigation then review, not a selected transfer
destination. Public backup sources identify existing restic-offsite/Cloudflare
R2 as a candidate. Local metadata observations do not prove account, endpoint,
connectivity or independent custody. The first ephemeral readiness inspector
failed review on semantic dotenv duplicates, unchecked argv, mixed-file binding
and pathname execution. Its R2 source91a177f6 and tests e41a7033 passed13
synthetic tests; execution awaits exact-source and byte-snapshot-launcher review.
No actual configuration/credential contents or remote repository were opened.

A fresh remote read found main had advanced to
`f1af4b59e9a746d4d25ec5e5e2ff6cf9a8ec1416`. The previous39-path public
integration diff was preserved as `/tmp/hyhome-openbao-integration-before-upstream-20261014.patch`
(SHA-2563658925b6b3182715cfeb795179fb4ab2c6ab31450566fdc35f60a77876664de).
A new owned integration worktree/branch starts from that main. Three-way
application preserved the other writer's custody procedure, Agent alert source,
Registry and SPEC-0235 updates; the two document conflicts retained both Work
Log sections and the established Maintenance Window Plan anchor. This is a
source reconciliation, not runtime acceptance of those upstream changes.
The original dirty integration worktree remains preserved until delivery.

The approved offsite R2 inspector and exact embedded verified launcher ran once
against the five named local inputs: exit2, LOCAL_INPUTS_BLOCKED:ENV_BINDING.
Only that fixed code was emitted. No private value, length or digest was
recorded and no network or transfer ran. R2 connectivity and independent custody
remain unproved. A narrower parser-reason diagnostic requires its own reviewed
source; no parser weakening or automatic configuration change is authorized.

Renderer R2's necessary test scope also includes
`tests/lib/ops/test_openbao_issuance_custody.py`; focused custody tests move there
without dropping assertions. The existing registered issuer suite must select
that module. Installer and request-peer fixes remain source review inputs.

Renderer R2 packet794fb462 passed exact independent code/security review:
helper4fc09f12, peerbe186532, installer27a097f1 and three focused test modules
all match their frozen manifest. The existing55 tests passed with90% branch
coverage. The Runbook bootstrap now verifies the exact installer bytes in
memory with isolated clean-environment system tools, fixed HOME/Git identity,
no replacements and exact full OID; independent code/security approved the
frozen Runbook c2c94d0f and bootstrap be3e5004. Neither result issues credentials.

Root integration's first90-test invocation failed one Agent fixture: its old
Docker stub did not implement the new explicit request argv/token-file framing.
After that correction, a24-test invocation exposed cross-case journal reuse in
the failure-injection loop: a later case reconciled the preceding uncertain
attempt instead of testing a new issuance. Splitting those three scenarios into
independent fixtures preserved the durable-journal behavior. The focused26
Agent tests then passed. The combined current renderer/Agent/rehearsal/owned
source suite ran134 tests:131 PASS, three explicit native-opt-in SKIPPED,
exit0. This is not native or HOME acceptance. An initial Ruff module invocation
failed because that interpreter has no ruff module; the existing standalone
Ruff lint/format checks on both changed fixtures passed unchanged thereafter.

R3 local offsite diagnosis used exact approved embedded launcher6874b957 and
inspector ddc03549: exit2, LOCAL_INPUTS_BLOCKED:ENV_ACCOUNT_SYNTAX. The accepted
literal grammar was not weakened. This result says only that local syntax was
not accepted; it does not prove the actual Cloudflare account is invalid.
Remote access, transfer and custody remain NOT_RUN/NOT_PROVEN. The user was
presented the existing R2 candidate for local setting review or another named
off-host target; no selection is inferred while awaiting a reply.

The W23 semantic recovery source lease is one minimal coordinator at
`infra/03-security/openbao/scripts/protected-semantic-restore.py` and one focused
unit module at `tests/validation/test_openbao_protected_semantic_restore.py`.
Independent review requires the focused execution/custody peer
`infra/03-security/openbao/scripts/protected-semantic-execution.py` and its
`tests/validation/test_openbao_protected_semantic_execution.py`; the source
lease includes these exact four paths and no generic target or HTTP framework.
The assigned infrastructure implementer owns those four paths only; the root
integration writer owns any Plan/Task/manifest/runbook/fixture updates. Reuse
reviewed protected maintenance/archive helpers rather than import test code or
add generic HTTP/target frameworks. Independently reviewed source and an exact
runtime recovery contract must precede the one selected attempt. Required
checks cover held-FD snapshot validation and private tmpfs filename delivery,
exclusive durable no-retry ledger before target creation, exact identities and
resource bounds, protected distinct credentials, metadata-only storage watcher,
old-image shutdown before same-target candidate startup, original-share unseal,
canary comparison, isolated renderer/Agent acceptance, isolated root revocation
and exact-owned cleanup. Retain the selected target and ledger on every outcome.
This source lease creates no directory, authorizes no extra recovery attempt,
and supplies no actual W3 snapshot or secret input.

W1 credential issuance, W2 snapshot-only token, W3 fresh snapshot, W4/W5
server/Agent upgrade, W6 audit/logrotate and semantic restore remain NOT_RUN.
The latest trusted reply assigns manual execution to `buenhyden`. This names
the operator; the subsequent reply confirms unseal-share and off-host readiness.
Custody location references and protected current OIDC/two-share input have
not been observed. The next ceremony uses those protected inputs; the owner
attestation does not by itself perform issuance or semantic restore. A prepared
client, healthy unsealed current server and downloaded candidate do not
supply those inputs. Criterion11 remains pending and this Task blocked.

The operator selected the currently absent
`/home/hyunyoun/storage/volumes/security/openbao/p01-restore-20261014-05`
for one isolated recovery of this new W3 snapshot. The read-only parent
observation was device2064/inode115612004, UID/GID1000, about2.5TiB free.
This supplies the target choice, not an actual target inode or completed
recovery contract; no directory or restore was created by that investigation.

The first semantic-restore freeze327ab851/e597962e changed after review handoff
and is a failed review input, never frozen acceptance. The explicit next freeze
4ffd0ec3/8ba3a111 passed28 synthetic tests at80% branch coverage but failed all
three independent reviews: mutable helper/bundle/contract bytes after hash,
unused lease digest and future/start-after-W3 admission, unbounded subprocess
capture, ineffective storage watcher/main-deadline cleanup, and post-effect
exceptions escaping INDETERMINATE. The correction extends only the exact four
source/test paths above, uses captured verified bytes, fixed bounded process
supervision, exact created object IDs and independent cleanup deadline. Target05,
ledger retention and one actual attempt remain unchanged and NOT_RUN.

The owner's subsequent answer selected existing R2 local review. Final diagnosis
identified a valid quoted account literal; earlier syntax refusals were a parser
compatibility limit, not proof of invalid Cloudflare configuration. Docker's
Compose environment documentation admits these matching quoted literals. The
minimal normalizer strips one matching ASCII quote pair before the same strict
account/bucket fullmatch; escapes, interpolation, duplicates and other forms
remain blocked. Independent code/security approved final inspectorff6bae4f and
launcher5f75e150 after14+10 synthetic PASS. Exact embedded execution completed
exit0 at2026-10-14T03:19:47.833Z: LOCAL_INPUTS_READY, account/bucket syntax,
credential presence and filesystem binding true. Values were not emitted or
changed. Public receipt is in the existing /tmp readiness directory. Remote
reachability is NOT_CHECKED and off-host custody NOT_PROVEN; no R2 transfer
selection or execution is inferred from this local result.

The semantic packet18f10be9/3ed79ab6/3289564c/1cc2842b passed the prior
correctness fixes but failed security/IaC review because the captured helper
receipt was not materialized beside the three renderer payloads. The final
four-file packet is restore18352557360b0dc730269714be45377a084e88b6cf5810a23805eb4e09a7798e,
execution3ed79ab6b43663bc8788c583578a469c3d8c81ee8d71c0310bdd605ec5474bca,
restore-test4eb946693b5546ebcdf3ff4c3a8a25cb27b4a1ec1db2c5e44ff6f2ef695f775b
and execution-test1cc2842b4851127eeba4d248dbce0a183081050732650bc8265fd47157aab7aa.
It installs the same held helper receipt mode0400 and tests actual materialized
R2 three-file validate_receipt. All three independent reviews approved source;
38 tests passed independently, branch coverage82%. ROOT integration first
failed test discovery with Python-I, then failed one of38 tests because its
two dependency source files were mode0664 from patch application. Removing
group-write on those two owned worktree files restores the loader's existing
0644 contract; no source or HOME permissions were widened.
ROOT then reran the same38 tests against the integrated current renderer and
dependencies: PASS38/38 in1.683s, no skips. Ruff passed all four semantic paths.
The combined protected maintenance/token/snapshot/semantic/P06/audit invocation
first failed when another imported custody peer retained patch-created0664
permissions; its test interrupt was not an actual runtime interruption. After
removing group-write from the five remaining owned public modules, the exact
11-module rerun passed253 tests in43.375s, no skips. These are synthetic/unit
results and do not establish HOME issuance, snapshot or recovery.
The existing script-manifest suite ran51 tests and failed two assertions because
its explicit mutation expectation table omitted P06's actual runtime transport
and migration coordinator. Adding those two runtime entries makes the exact
failing mutation test PASS; this corrects the test inventory rather than
weakening the manifest's runtime classification. Full suite rerun is pending.

The owned scan operator3e72bbb6 passed18 synthetic tests but failed all three
reviews for mutable tools/DB, ambiguous create cleanup, runner identity,
deadline/output bounds and package coverage; Ruff also failed. A corrected
frozen packet is required before any scan. ROOT independently captured the
existing hydrated DB's exact three public files and acquisition receipt in
owned-r5-db-custody-manifest.json, SHA3261664a685eb495cc749dc4ba82937df83b8087d768ffb60f128ad849bd3f00.
The first manifest attempt failed on sibling-sensitive shared-directory
timestamps and wrote no manifest. The corrected manifest checks stable held
directory identities and full file signatures/content, limits the read-only
mount to db-cache/6 and excludes the unused empty tmp sibling. Security approved
this post-hydration byte custody; it does not claim a publisher-signed SQLite
database. The fresh owned-image CVE scan remains NOT_RUN.

After LOCAL_INPUTS_READY, the operator explicitly selected the existing R2
Restic repository for this new snapshot and receipt, beginning with read-only
remote verification. A separate bounded public operator is being prepared;
no remote connection, repository lock, upload or verification has run yet.

### Latest main reconciliation and PGP preparation — 2026-10-14

ROOT refreshed clean main and origin/main to
`7f4c364f8681ea0db091f05ab6077c594661dfff`, then reapplied the task-owned staged
packet into `codex/openbao-maintenance-integration-latest`. The earlier dirty
integration worktree remains preserved. The full pre-refresh public patch is
`/tmp/hyhome-openbao-integration-before-main-7f4c-20261014.patch`,
SHA256 a39d88a76e90d871cf56a6903cca60cff56ac808655281cf549ec79dfa56fc4f.
The two document conflicts retain both main's exposure/custody and Agent-alert
records and this operation's actual evidence. Main's W1b now precedes W2/W3;
SPEC-0239 source delivery remains distinct from actual Agent deployment.

The operator answered that PGP setup is needed and requested beginning-to-end
instructions. RUN-0085 W1b now explains three independent off-host recipient
units, binary public exports and full fingerprints, native authenticated
rotate-keys with W1 protected token-file input, hidden-TTY old/new shares,
recipient-ordered encrypted output, verification, cancellation and old-snapshot
custody. This supersedes the inherited no-root/legacy-rekey and
verify-cancel-as-full-cancel text. Three recipient public-key paths/fingerprints
and custody references are still missing. W1b, W2/W3, HOME upgrade and recovery
are NOT_RUN; unrelated source/security work continues.

R2 read-only attempt1 failed IMAGE_CONTRACT before create; private inputs were
read and private copies cleaned. Attempt2 used frozen operator fbac6359 and
receipt5ee7, then returned exit3 CONTAINER_UNVERIFIED with operation nonce
3088df92292f15bf7857a8d48caca748. Docker created exact ID
b4498a5067f65b55de0081d28644c3dfc5bad2667faaf9ab064470528ed4f8f7
but never started it. The full-mount dictionary omitted native Mode empty;
the created network map also has an empty NetworkID before start, while
HostConfig.NetworkMode already equals the exact approved network ID.

Independent code/security review approved a narrowly bounded reconciliation.
The first cleanup preflight stopped on an assertion before mutation because
the worker's corrected pathname had changed; the retained frozen source was
then used. ROOT freshly proved exact ID/name/nonce/image, created-never-started
state, resources/mounts and existing network identity, removed only that full ID
without force, and observed exit0+empty lists by both ID and anchored name.
The private tmpfs root was absent. Public reconciliation receipt SHA256 is
c8a686601fa8e7ed6c5de4e94fae121d3ff235020833ac0d607b27120b70e7bf.
No Restic process or remote query ran; cleanup does not convert either failure
to remote acceptance. The next corrected-source action needs its own frozen
review and fresh bounded attempt; historical receipts remain preserved.

### Actual R2 read-only result and incorporated-worktree cleanup — 2026-10-14

R2 attempt3 used frozen operator40ba8184, launcher ebdaeb8b and source receipt
d2930cfa after independent code/security/IaC approval and ROOT's35-test replay.
The actual bounded invocation exited0 with R2_READ_ONLY_READY: JSON valid,
repository reachable,45 snapshots, latest_present=true. Its reviewed exit0
control flow includes exact-owned-container removal and private-copy cleanup.
Public observation receipt SHA256:
20bbd98bfb8b941f033a57e90d644687b81c1a1bccbe908aa5fb152e45e22e2c.
The existing bridge provides broad egress, not an R2-only firewall. This action
ran only snapshots --json --no-lock; it proves neither repository write nor
upload of a new OpenBao snapshot, restore, or independent custody completion.

The user then explicitly requested removal of codex branches/worktrees already
incorporated into codex/openbao-maintenance-integration-latest. ROOT compared
effective changed files, staged/unstaged patches and ancestry. Three P01 trees
(owned-rebuild, protected-semantic-restore, protected-snapshot) disappeared
through an external concurrent actor during preparation; ROOT did not remove
them. Their source had matched latest at the preceding inventory.

For the still-present original and -current integration trees, ROOT preserved
all effective public changed files plus HEAD/staged/unstaged patches under
.agent-work/retained-development-handoffs/20261014/incorporated-worktree-cleanup-20261014
(private0700 directory). Independent code review confirmed incorporation and
exact patch-manifest matches. ROOT rechecked unchanged status/content/ancestry
and only generated ignored caches, removed those two exact worktrees, then
used git branch -d for their two ancestor branches. Result receipt SHA256:
da25c11d3404c9e4c915ad87a87b50cc042b93c056c582647a3b40c082db1f17.

Fresh worktree listing contains only main, active -latest integration and
p01-renderer-token-custody. The renderer branch retains the unique accepted
but not-yet-applied5c809c1e image-pin delta; its preservation is intentional.
Remote origin codex/* heads query succeeded with no refs. Root main remains
clean7f4c364f. The public scanner's build-input path was separately updated to
-latest with unchanged input bytes SHA1e8b356a before removing -current;
its own new exact-hash review remains separate from this cleanup evidence.

### Current documentation verification — 2026-10-14

RUN-0085 W1b full guide passed exact source/security/IaC review at06c64ba0.
The later7c8b35a8 change adds only the required fixed-pre-upgrade CLI citation
annotation; it does not change commands. Six W1b bash fences passed bash -n
without executing a command. Operations catalog passed. Full document-link
check passed1306 documents/11606 links, with the existing2870 uncaptured legacy
archive-link warning retained as historical-resolution unverified.

The first changed metadata check exited1: selected9,154 violations. It reported
the evidence-table blank separator, one fixed-version citation annotation,
new build README structure/version-authority gaps, and archive migration/
tombstone type mismatches outside this task's changed files. ROOT corrected
the table separator/citation; the build README has a bounded documentation-only
owner. Archive findings are not yet classified against a fresh clean-main
comparison and are not silently waived or edited. Final registered gates and
source delivery remain pending; this is not an all-checks PASS claim.

### Main 4c33 reconciliation, custody state, and renderer cleanup — 2026-10-14

ROOT reconciled the canonical integration worktree from clean main7f4c364f to
clean main4c33d6ce. Main's six documentation changes were retained. Before
application, ROOT preserved59 changed paths in manifest
1e8dd9643a1490e8c76512f51a32bfac15991ba4f77a9c7f7631499d021fcb16 and full
patch40bfefb2f68f88f18f77d1bc118adee849b20601fe117dc2b5efdee1016ceafa.
Post-apply preservation records57 non-conflict paths byte-exact, no unmerged
entry and SPEC-0240 retained. This supersedes neither the older reconciliation
receipts nor their failed and pending runtime results.

The current custody design conditionally uses three separate places for the
three share holders and an initially separate fourth off-host place for the
key material. The protected PGP procedure remains pending the three actual
public-key paths, full fingerprints and custody-location references. No public
key was selected, no share or key was processed, and no HOME operation changed.

The renderer cleanup archive manifest
874ba02f9ca21c313f199a29dc7dba31a98ee7344ab65a6706f677efd8b38cc5
contains all six effective source/test files, including the two files that had
been untracked in the renderer worktree; every file is byte-equal to canonical
latest. After independent code review and fresh status/hash checks, ROOT removed
only the temporary before-main4c33 worktree/local branch and the incorporated
renderer worktree/local branch. Cleanup receipt SHA256 is
db8b4598d65f53085362c561454416b6787e1bca5820e5deeb8eabcd37f0c6d0.
Root main is clean at4c33d6ce, and only main plus the canonical latest worktree
remain. Archives are retained; no HOME or runtime effect followed from cleanup.

The fresh native candidate/rehearsal invocation used input SHA256
d1c59476085763d99798413c402e4fe4d8341ab8fe45fc76b84eee6281db65af
and finished after276.386 seconds with13 tests:11 PASS, two ERROR and no skips.
Candidate native TLS expiry, audit and snapshot checks passed, as did the
diagnostic path. Both the native full rehearsal and versioned issuance stopped
at wrapping line540 with `RehearsalFailure: native interrupted issue exact
cleanup failed`. This actual result is FAIL and unresolved; it supplies no
aggregate native or HOME acceptance. Its public failure receipt SHA256 is
555afd88b549ff79502a4074eeac10e236b6aa802c4e38d1e5eb0b27aa5754a5.

Diagnosis found the synthetic fixture omitted
`BAO_TLS_SERVER_NAME=openbao`. The focused RED regression failed once, then
passed after the minimal fixture correction; Ruff passed. The combined source
suite ran74 tests in24.939 seconds:70 PASS and four native-opt-in SKIPPED. IaC
and security read-only review approved the exact Runbook version0.10.2 and
fixture: the two active image arguments now use owned manifest46bf and the TLS
server-name input matches the Compose/request-helper contract. The reviewed
second native attempt used fixture input SHA256
2fa9f8b2439d9970ced72cc968567a6066620564c2869709a44b7b15f0f67b73 and
exited0 after454.043 seconds:13/13 PASS, no skips, including all four native
tests. Public log SHA256 is
2466d19f23c35067841b89bf1081e15497f453320d5ced4074d4cdad6675db39;
ROOT observation receipt SHA256 is
2995a9891c7d8bc12550d2b140b8d8ba068f4759e380688cae29466387bdb1a8.
This resolves the diagnosed synthetic fixture failure only. It does not prove
HOME custody or deployment, and no HOME state changed.

### Registered source-delivery checks — 2026-10-14

The canonical changed metadata gate against main4c33 first failed on the
appended RUN-0085 lifecycle row's malformed anchor, then on its out-of-package
Artifact. Neither was a baseline exception. The invalid row was removed;
the three original Task events remain unchanged and the Runbook source
activation/review/authorization stays in Current Operation Preparation.
Independent rules review approved that placement. The final registered
`check-document-metadata.py --mode check-changed --base-ref main` exited0:
selected9, violations0, legacy_exceptions0, transition_overrides0.

The final exact staged `run-ci-precommit.sh --mode local-staged` exited0;
Markdown, shell, Python, Dockerfile and secret-scan checks passed. Earlier
Markdown list/heredoc indentation and a P06 blank separator were fixed.
Two generic-api-key hits were independently verified public Go/Alpine
integrity checksums. Exact path-and-value AND allowlists passed the redacted
staged scan; a changed neighboring value remained detected. The first
isolated directory-mode self-check failed on absolute-path projection;
the corrected native Git-staged self-check passed, without printing values.

The full document-link check exited0:1306 documents,11620 links, failures0;
the existing2870 uncaptured legacy links remain historical-resolution
unverified. The script-manifest module passed51 cases. A combined invocation
also misnamed the catalog module and recorded one import error; the corrected
catalog invocation passed128 cases in308.694s. The focused source/Agent/gate
suite passed70 of74, with four opt-in native skips; the separate actual
13-case native rerun supplies the current native proof, not those skips.

Source and retained verification receipts remain available under
.agent-work/retained-development-handoffs/20261014/main-4c33-reconciliation.
Fresh token-free state projection found no remaining p01 fixture container;
HOME server and Agent still run healthy on the original11fd image. The source
candidate is ready for its owning-Spec draft PR; no HOME gate is promoted.

### Source PR delivery and hosted field-metadata finding — 2026-10-14

The reviewed source candidate was committed as932508be4 and delivered in
[draft PR472](https://github.com/buenhyden/hy-home.docker/pull/472) from
codex/openbao-maintenance-integration-latest against main4c33.
The initial hosted
[candidate-quality run](https://github.com/buenhyden/hy-home.docker/actions/runs/38522461732/job/115715081494)
passed. The same head's GitGuardian check failed with one Generic Password
finding in protected-semantic-restore.py; no annotation or value was copied
into this Task. Independent security inspection confirmed the two public
KV-route/field-selector pairs contain no source credential or expected value.
The semantic client reads actual values only through protected runtime inputs.

The source-only clarity correction names the common public field explicitly
with CANARY_FIELD_NAME and references it from the same two pairs. Routes,
field bytes, tuple values, consumers and protected handling remain unchanged.
New exact module SHA256:
1a259ef01a762656a9eeef18917b511b301c7db10f888527cd3cffb0fe67fde7.
RUN-0085 0.10.3 updates its one live W1 source binding; the prior18352557
review packet above remains historical. No detector/path suppression,
dashboard mutation or credential rotation was performed or is indicated.

The first semantic regression invocation ran38 with37 PASS/1 ERROR because
its unchanged approved public dependencies were0664 and the loader refused
group-write. Only four owned public source modes were restored to0644;
content hashes and loader policy stayed unchanged. The exact rerun passed38/38,
0 skips,1.892s; Ruff and independent code/security/IaC delta reviews passed.
The earlier native34-file digest was recomputed unchanged at2fa9f8b2;
this module is outside that fixture, so no native rerun or new HOME semantic
restore is claimed. Hosted checks on the clarified follow-up remain pending
at publication; the source PR stays draft and no merge/deployment is claimed.

### PR review and synthetic TLS server minimum — 2026-10-14

The owner's subsequent PR-review request examined latestcbe95c588 against
main4c33. Hosted CodeQL analysis jobs succeeded, but its aggregate failed
with two new High py/insecure-protocol alerts:
[test copy runtime](https://github.com/buenhyden/hy-home.docker/security/code-scanning/33)
and [test snapshot](https://github.com/buenhyden/hy-home.docker/security/code-scanning/34).
The two loopback synthetic HTTPS fixture servers constructed
SSLContext(PROTOCOL_TLS_SERVER) without an explicit minimum. The production
copy/maintenance clients already enforce TLS1.2; no HOME credential exposure
was found. The exact two-line correction sets minimum_version=TLSv1_2 on
each server context before certificate loading and socket wrapping.

The first full two-module regression ran51 in20.516s and failed with1 failure
and12 errors because the approved custody dependency was0664 and its loader
refused group-write. That log is retained at
/tmp/hyhome-pr472-codeql-tls-regression-20261014.log. Exact content hashes
were confirmed and only the three remaining owned public-module group-write
bits were removed; seven protected modules are now0644, with no content or
loader-policy change. The identical rerun passed51/51,0 skip,21.603s;
/tmp/hyhome-pr472-codeql-tls-regression-attempt2-20261014.log. Ruff and
independent exact-delta code/security reviews passed. The native34 inputs,
owned image, Compose, W4 and HOME state are unchanged.

The same review confirmed GitGuardian's latest check still names historical
commit932508be4, not currentcbe95. Its Generic Password report concerns only
public field-selector metadata, and checks inspect every PR commit. The owner
selected direct dashboard false-positive handling. This is an operator intent,
not completed external-state proof: no dashboard change, ignore rule,
credential rotation or history rewrite was performed by the agent. A fresh
hosted check must confirm clearance after that action. The TLS follow-up is
prepared for the existing draft PR; no merge or runtime acceptance is claimed.

### Source merge and remaining review fix — 2026-10-14

The owner reported merge completion. GitHub confirms PR472 merged at
2026-10-14T06:48:39Z as5cdf684902b88bb68f048e99ed88e5525d4755c0,
with headcbe95c588. Local main, origin/main and fetched main match5cdf;
its tree exactly equalscbe95, and the root checkout is clean. The two TLS
fixture minimum-version edits and their Task receipt were still staged
locally when the owner merged and therefore are absent from that merge.

Those three public files and full/index/worktree patches were preserved in
.agent-work/retained-development-handoffs/20261014/pr472-post-merge-tls-followup,
manifest SHA25673d0337962b3c5055e5f2ccc360741cde64fbacc6f00725f00719f7a85b099a9.
They were applied byte-identically to codex/openbao-pr-review-tls-minimum,
a fresh worktree based at5cdf, for a small follow-up PR. No history rewrite,
production code change or runtime mutation is required. The user's intended
GitGuardian dashboard action remains separate from observed check clearance.

### Host Custody for One Administrator — 2026-10-14

The owner withdrew the separated-place layout and the SPEC-0240 exclusion and
chose host custody (SPEC-0242): shares and the CA key on the host and in the
host backup, and only BKP-003, the R2 credentials, BKP-002 and Cloudflare
account access in one password manager account; no W1b rekey. RUN-0085 0.11.0
holds the procedure and the step 5 table. The "HOME custody attestation" row
keeps its earlier off-host check and stays NOT_RUN as history; the owner's
step 5 table for the host layout will be recorded as a new row.

### Step 5 Owner Record — 2026-10-14

The owner returned the RUN-0085 step 5 table, value-free, on 2026-10-14, and
clarified it the same day: the R2 account ID and bucket name, the R2
credentials, BKP-003 and BKP-002 are kept only on the owner's separate
desktop, off the host; Cloudflare account access is in password manager
account hyunyoun; a read-only R2 snapshot listing with values taken from
those places succeeded; the host second copy is at
`/home/hyunyoun/data/hy-home.secrets`; and the recovery means for those
places (desktop login and disk-encryption recovery, account recovery) are
kept outside them and the host, for example on paper. Each was checked that
day. RUN-0085 0.12.2 names the off-host place "place A", a password manager
account or the owner's separate desktop. Every answer is yes, so step 5 is
`PASS`, owner-attested. This is the owner's statement; the agent read no
value, and the repository cannot certify where values are kept.

### v29 current window and residual handoff — 2026-10-22

The v29 local request reuses completed work on main
`49fd95a6ed482d7194c840b43b73a030be6f3d5d` and reconciles this active P01
handoff with [SPEC-0243's dated window records](../../0243-openbao-window-readiness/tasks/tsk-0001-openbao-window-readiness.md).
The 12:30 attempt records W1 delivery, unchanged role targets, W1c/W2 skips,
protected W3 Snapshot and W3b R2 dump agreement, accepted W3a `-06` restore,
W4 HOME 2.7.1 transition, W5 typed-JSON issuance and Agent rendering, and W6
TLS/audit/observation and writer restoration. W2 delivery and the 07:49 and
13:00:31 manual backup successes retain their original times and scope.
The failed `-05` attempt remains INDETERMINATE and preserved. No step was
repeated to produce this document correction.

Reuse the implemented A2 writer handoff, B1 Snapshot empty-entity and operator
nonempty-entity guards, B2 opt-in restore harness, B3 bounded TLS probe and C1
receipt/source assessments within their dated inputs. All 47 recorded file
hashes matched before this edit; the RUN-0085 prose correction changes that
document's hash, while helper/config bytes remain unchanged. The assessment's
Native validity remains false, and this review supplies no raw invocation
evidence or new Native acceptance. SPEC-0243's completed Task closes its approved
readiness/source-document scope; its terminal record is unchanged and does not
complete this Task's criterion 11 or P06's criterion 20.

Remaining owners must resolve A1's unknown ESO403 cause and all-six versus
failed-only refresh decision, B1's exact OIDC entity/alias/provider and identity
policy contract, A3's exact cleanup/retention inputs, B4's approved sensitive
old-token generation custody and implementation, and the three D1 owner
decisions before 2026-11-15. Current-source Native checks, sustained renewal,
cold boot, actual timer/26-hour freshness and remaining independent recovery
and P06 consumer acceptance retain their separate evidence gates. No token
revocation, new issuance, cleanup, cluster write or HOME change is performed.
Existing Evidence, Criterion Acceptance and lifecycle events remain unchanged;
combined metadata, links, lifecycle and independent review are recorded by the
v29 coordinator.

### v30 B2 anonymous-volume cleanup source continuation — 2026-10-26

The current v30 sections 10.3.4–5 authorize bounded local source, regression
and separately admitted isolated Native work. Independent read-only preflight
of cached old-image metadata confirmed inherited `/openbao/file` and
`/openbao/logs` volume declarations. Label-filtered discovery cannot prove
those unlabelled anonymous volumes absent. This is a newly confirmed cleanup
defect, not a reason to repeat the completed restore or upgrade window.

The exclusive writer lease is the existing rehearsal fixture, the protected
semantic execution and restore modules, their four existing regression modules
(`test_openbao_rehearsal`, `test_openbao_protected_semantic_execution`,
`test_openbao_protected_semantic_restore`, `test_openbao_protected_restore_inputs`),
RUN-0085 and this Task. Other concurrent writers retain their own files and the
integration writer alone owns the Git index. The independent IaC prereview
admitted this exact nine-path boundary before implementation.

All three exact owned-container removal paths now include `--volumes`.
Explicitly named volumes and bind data remain preserved by Docker's container
removal semantics; the fixture's existing explicit owned named-volume cleanup
remains separate. The fixture keeps its name-return and membership API but
registers each create-returned immutable ID before inspecting actual mounts.
Cleanup never falls back to an unverified name. Only actual volume `Name`
fields enter mount tracking; bind/tmpfs paths do not become volume deletion
targets. Every captured mount name is checked once after all container and
explicit owned-volume removals. An unknown ID, incomplete mount capture,
remaining volume or ambiguous/daemon/permission failure prevents cleanup PASS
while remaining owned cleanup is attempted. Existing Native full-perform tests
capture actual restore mount names through the existing creation registration,
including the old server removed before candidate start, and verify absence
individually before accepting label-filtered discovery as supplementary evidence.

RED selected six regression methods: seven expected assertions failed and one
missing new tracking attribute errored. The first combined run then exposed
five errors in an old synthetic cleanup setup without the new tracking maps;
that setup was corrected without changing the tested cleanup requirements.
The following combined run passed 85 tests with seven default Native opt-in
skips. Further metadata-shape and cleanup-continuation cases are part of the
final scoped regression recorded below. None of these default runs invoked
Docker or supplies Native/HOME acceptance.

Final scoped validation of the four modules ran 86 tests in 2.662 seconds:
79 PASS, zero failures/errors and seven default opt-in Native SKIPs, exit 0.
The standard-library trace run covered 58/64 changed executable fixture lines
(90.62 percent), 2/2 execution-module lines and 2/2 restore-module lines. This
is changed-line coverage only, not branch, whole-file or repository coverage.
Ruff check, Ruff format check of all seven Python inputs and diff whitespace
checks passed. Registered document metadata and normal staged hooks remain
pending the integration writer's combined freeze; no interim metadata result
is substituted for those final checks.

Frozen source SHA256 values are fixture
`6f01d52858be61d086713472473e86d9181dbba045d40ef7b29b797445351f9e`,
execution
`b5aa92bdf528eb92993fc46061ead65b72bf71efe30182cca7cc5b5706ab396e`
and restore
`4c2d0732efb2c63fd991499419d830d70159672dafcb54385ef948ae7b37681d`.

The separate CI caller companion preserves the existing required full TLS
module and adds only the new `TLSMaterialNativeDelayTests` class to the
existing optional-runtime skip list. Its writer reported RED two failures,
then GREEN 2/2 PASS without skips in 0.030 seconds; the actual workflow
validator passed five workflows, seven jobs and nine action pins. Frozen
workflow-contract SHA256 is
`0ff07f00d051607330f9b7415aaaa2081b1a2294cf27b5e36e5ba5ddf2c8c374`;
its existing regression module SHA256 is
`0d581ffc20323f8eba6dd6b34e86244091eac5ed3bd802437128d6c4a13045d4`.
This is source-routing evidence only. The CI writer changed no allowed
environment key, adapter, route or gate; B3 actual Native results remain with
the independent QA execution. Actual-diff review and combined gates remain
pending and this companion grants no runtime authorization.

The execution module's pinned hash in the restore module and both current
RUN-0085 manifest rows are synchronized. Historical hashes and accepted window
receipts remain unchanged. No actual `P01_APPROVED_COMMIT`, installed client,
credential, HOME service, retained target, old residue or remote state changed.
The next operational window still needs its new exact approved commit,
manifest, source review and installation. Native execution remains NOT_RUN
until frozen source, independent actual-diff review and the controller's
separate bounded execution admission. Criterion 11 and lifecycle stay pending.

### v30 selected isolated Native observations — 2026-10-27

The final code revision is
`f4698d1e15212117dafb5809fb6c5c7596686be4`. All 55 declared source
inputs matched both the working files and committed blobs at execution. Their
manifest SHA256 is
`ed54fd86023f171515860c6e532356c1441e6a904f6427c16ee92cb1df929f6a`.
The observed revision and last verified source revision describe these actual
inputs; later result-only document commits require a source-manifest comparison.

B2 ran the following existing methods as three separate actual processes,
each once with one PASS, exit 0, zero errors/failures/skips and stable source
inputs. These are selected-method observations, not a whole-module run.

| Existing NativeRehearsalTests method | Actual process elapsed seconds | Recorded known absence counts: exact containers / generated names / volumes / networks |
| --- | ---: | --- |
| `test_full_perform_restores_upgrades_and_renders` | 282.877849 | 10 / 1 / 19 / 2 |
| `test_full_perform_preserves_trailing_newlines` | 316.400139 | 10 / 1 / 19 / 2 |
| `test_live_canary_refuses_an_empty_value_before_restore` | 78.428028 | 4 / 0 / 10 / 1 |

Every recorded identity in those counts was confirmed absent. Each of the first
two processes intentionally retains one UID 100 Raft directory and one UID 1000,
mode 0600 operator ledger. The third retains neither. These retained data were
not read, deleted or included in evidence copies. Issuer helper container identity
was not retained and its kernel resource clamps were not set. Reclaim helper
container and inherited volume identities were not retained; only its generated
name absence was observed. These gaps prevent an overall cleanup or
all-containers-bounded claim.

B3 ran all five existing TLS delay methods in one actual process: five PASS,
zero failures/errors/skips/not-run, exit 0. Each method confirmed both recorded
container identity absence and exact name/label absence, with no fallback cleanup.
The first-to-last case observation spans 226.326122 seconds; outer process
start/end timestamps were not recorded. The 61-second timeout and controlled
late-dispatch scenarios retain their expected nonzero checker outcomes. The
late scenario passes its controlled reconciliation assertions after its helper
is closed, reaped, absent and unable to dispatch again; this does not turn the
source failure into production cleanup acceptance. Other destroy observations
without a successful source removal receipt remain explicitly unattributed.

The B2 runner SHA256 is
`399b2376fe472deb7aba889c7c2bb411de1b8a18b0252b88d60557c4e1db149d`;
its nine-input admission manifest SHA256 is
`71a525644ff916a8ac8177c8760387cb7adebc4aea91975566ef9f9164faf79c`.
The B3 capture runner SHA256 is
`a25670486cfe2947a017c41c78109cf0c026c551c9a219bcebd90115bb49ff8e`.
The reviewed environment substitution provides a fresh empty Docker client
configuration only to approved Docker and the exact verified issuer invocation;
actual arguments, standard input and results remain real. This is synthetic
isolation evidence, not unmodified production-environment acceptance.

Historical observations remain separate. The original B2 attempt on revision
`31a4b0710eebbb97615dee0f1f8515dcb5284f4f` failed during initial health/setup
before restore; its precise cause was not recorded by that run. Its first diagnostic observed an immediate connection refusal;
that alone did not establish a persistent routing failure. The second preserved
the original readiness loop and identified strict X509 verification code 92:
the synthetic CA lacked its key-usage extension. Commit
`59ee7e0cb6b2da4e2fb667161866545c139fd037` adds explicit critical CA
basic constraints and certificate/CRL signing key usage to both synthetic CAs.
The strict-chain regression was RED then GREEN; wrong CA and wrong hostname
remain rejected. No TLS verification flag or production trust rule was weakened.
The three subsequent B2 passes on that revision and their historical source
manifest remain historical, rather than being stitched into the final result.

The five earlier B3 attempts retain their original counts: 0/1/4, 0/1/4,
0/1/4, 1/1/3 and 4/1/0 PASS/FAIL/NOT_RUN. Their observer, event-evidence,
cleanup and bounded late-client failures remain failures. Separate read-only
absence supplements resolve only the recorded resource uncertainty; they do
not rewrite an earlier process exit or promote an indeterminate request.
Prepared but unexecuted B2 source candidates remain NOT_RUN.

The existing [verification receipt](../../../../infra/09-platform-ops/security-updates/verification.json)
adds only a separate `observed_native_executions` member with minimized current
and historical facts. Every prior top-level value and original byte prefix is
preserved, including the old aggregate false/null assessments. Public minimized
B2 and B3 projection SHA256 values are respectively
`20887c32f6dfad0c6fcff0bb156b1354cbb9b01dec6a013d329959a90cfb8726`
and `89f2e72e8dba09019420922484795e02c759564b7775d74f045a99704a15ea96`.
The separately reviewed fixed local retention allowlist copied seven public
source/hash artifacts and minimized projections to the ignored
`_workspace/openbao-native-evidence/2026-10-27-f4698d1e` evidence area.
Every source and destination hash matched; new directories use mode 0700 and
files mode 0600, with no overwrite or unlisted copy. The local index SHA256 is
`c74af01811bcf2df74d6aca18915c431967e849926d056969a677a405daa99d5`.
The allowlist excludes all raw receipts/logs, actual
resource identities, environment values, private paths, fixture credentials,
keys, Docker configuration and retained Raft/ledger data. Originals remain
private temporary evidence, so the minimized artifacts are not lossless copies.

No HOME-input method, installed service, credential custody or approved owner
window was executed or changed. The literal HOME-input method remains excluded.
The old twelve/fourteen-case aggregate is not promoted. A future HOME window
still needs an owner decision, its exact newly approved commit and manifest,
installation and separate operational acceptance. Existing Evidence, Criterion
Acceptance, review status and blocked lifecycle remain unchanged.

### v30 A3 runtime cleanup and B4 scheduling — 2026-10-27

SPEC-0243 TSK-0001 is terminal, so its A3/B4 handoffs are continued here. The
owner chose "preserve then delete" for the runtime copies, a prepared sudo
command for the accepted `-06` target, retention for `-05`, and B4 in a later
session.

**Runtime copies — DONE.** Under `/run/user/1000` the four directories
`p01-client.F2pewN`, `p01-client.UPX6k2`, `p01-inputs.Nr6uDg` and
`p01-inputs.p0Dj20`, plus 16 `p01-blk-*.sh` window scripts, were user-owned.
A pattern scan found no credential (the only hit was a `-----BEGIN
CERTIFICATE` source literal); JSON receipts were read by key name only.
`p01-inputs.p0Dj20` held the only copy of the accepted `-06` restore contract
(`a07fe0ae…`) and its security receipt, and `p01-inputs.Nr6uDg` held `-05`'s.
Both input directories and the 16 scripts were copied to the owner-only
`/home/hyunyoun/storage/ops-snapshots/openbao-p01-20261022/` (mode 0700) with a
40-row `MANIFEST.sha256`; source and copy both verified against it, and each
script compared equal. The exact list was then deleted; no `p01-*` entry
remains under `/run/user/1000`. The two `p01-client` directories held only
repository script/policy copies and were not preserved.

**`-06` target — REMOVED by the owner.** Read-only metadata:
`p01-restore-20261022-06` is a directory on device 2064 (inode 115608705),
UID 100, mode 0700, unreadable to the agent; no Compose container mounts it
and its ledger `.p01-restore-20261022-06.attempt.json` is present and kept. The
owner script re-checks parent identity, target identity, ledger presence, no
mount, no container mount, no symlink or hard link inside and no process
cwd/root/fd under it, then runs one `sudo rm -r --one-file-system` on that
exact path and confirms the ledger remains. The first owner attempt ran through
the session's `!` prefix, which has no terminal: every sudo call failed, the
original script treated those failures as "nothing found", printed `checks
PASS` and its `sudo rm` also failed, so nothing changed (target inode
115608705 and ledger confirmed afterwards). The corrected script refuses to run
without a terminal, authenticates sudo first, and stops when any check command
fails or the sudo count is empty. The owner then ran it in a terminal:
`checks PASS; entries: 5` and `REMOVED …p01-restore-20261022-06; ledger kept`.
A listing afterwards shows `p01-restore-20261014-05` and both attempt ledgers
only.

**`-05` target — REMOVED by the owner (2026-10-27).** The owner later chose deletion. The same guarded script, with only the path and identity (inode 115608830) changed, printed `checks PASS; entries: 5` and `REMOVED …p01-restore-20261014-05; ledger kept` in a terminal. A listing afterwards shows only the two attempt ledgers. Earlier record: The owner kept `p01-restore-20261014-05` until the
next window or review. Root custody, W2 locks and both ledgers are outside this
cleanup.

**B4 — deferred to a new session.** Review confirmed the SPEC-0243 handoff. The
P06 Grafana consumption verifier now exists as synthetic-tested source
(TSK-0014 W49); Keycloak has no consumer verifier, and the cutover it would
verify has not run. The approved custody location is owner-only 0600 tmpfs
under `$XDG_RUNTIME_DIR`. Still open before the v3 journal: the custody
retention/destruction point, child-lease/rollback disposition, the
selected-version revoke-self check, and a new P01 approval for the changed
helper hash.

**B4 owner inputs — 2026-10-27.** The owner settled two of the open inputs. The
captured old token is destroyed at phase `complete`: the owner-only 0600 tmpfs
custody file is unlinked right after a confirmed revoke-self. Any interruption
keeps it for bounded reconciliation, and a reboot destroys it with the tmpfs.
On rollback (the new token fails verification), the old generation stays live
with its child leases untouched, the new token is revoked with revoke-self, and
the journal records `rolled_back`. A pre-flight confirms that the selected
OpenBao version supports token revoke-self. A new P01 approval for the changed
helper hash is still required before any window. Implementation remains in a
new session.

### W5 Agent re-issue for the Grafana delivery — 2026-10-27

After PR #572 merged at `2289dcff8`, the owner ran the RUN-0085 SecretID
Delivery block from a guarded script. It had the 10-22 inputs: issuer
`090352d05` installed under the operator tools root, the journal directory and
`hy-home-infra_openbao-agent-data`. Preflight passed, the Agent stopped at
07:45:17Z, both 5-minute tokens were minted, and the helper returned 1:
`W5 issuance FAILED rc=1`.

Read-only reconstruction:

- The journal was written at 16:45:56. By 16:46:20 KST the anchor read
  `state: complete` and the active journal was gone, so the helper had rolled
  back from `issuing`.
- The server revoked the `hy-home-renderer` SecretID wrapping lease at
  07:47:01Z, when the 60-second wrap expired unused.
- The Agent volume held a fresh `secret_id` file written at 07:46. The
  delivery container had written it, but the helper never recorded
  `delivered`.

Root cause: `deliver()` and `start()` used `command()`'s default 20-second
timeout. A probe of the same `docker run --rm` invocation, writing and
removing only a temp file, took 18.9, 11.2 and 16.9 s at load average about
12 with 66 containers. On this run the container wrote the file but did not
exit within 20 s, so the helper correctly treated delivery as uncertain and
destroyed that exact SecretID. No credential is left valid. The stale wrapped
file is overwritten by the next delivery. The Agent stays stopped until a
successful issuance.

Fix (owner choice "Fix timeout, then re-run"). The first cut gave `deliver()`
and `start()` 55 s each. An independent review rated that High: the 60 s wrap
TTL covers delivery, start and the Agent's unwrap together, so both could
succeed after expiry and leave a `delivered` journal with an unrevoked SecretID.
The final design:

- `issue()` records one wrap deadline 45 s from just before its request.
- `deliver()` and `start()` share what remains of it, never beyond the
  240-second operation deadline.
- `deliver()` raises while still journaled as `issuing` if less than 8 s would
  remain for the unwrap, so the exact-ID reconcile destroys the SecretID.

A fake-clock test covers the shared budget, the post-delivery reserve and the
exhausted-budget block. Issuance, custody, trust, Agent, semantic restore and
rehearsal suites: 137 OK, 3 skipped. A new issuer commit
needs owner approval and installation before the re-run.

### W5 re-run, journal recovery and Agent restart — 2026-10-27

The owner approved `422b4adfd` (PR #573) as the issuer commit, and it was
installed with the 10-22 bootstrap. The three installed files are
byte-identical to that commit.

**Second run — rc=1.** The run issued, delivered and started the Agent at
08:14:02Z. The Agent unwrapped the SecretID at 08:14:07Z (`secret_id_num_uses`
1, so it was consumed) and wrote a new sink. Readiness still failed, and the
helper stopped the Agent at 08:15:26Z. Cause: the Agent does not rewrite an
unchanged destination, so the Grafana `.txt` kept mode `600` from 2026-09-19
and the new `640` health requirement could not pass. The journal stayed at
`delivered` for a start that no longer existed. With the SecretID consumed, the
helper's reconcile could only block, as designed.

**Owner recovery.** On the owner's choice, an owner-run script checked the
state and changed only the journal:

- It confirmed the Agent was stopped and the journal matched `delivered` with
  an `active` anchor.
- With a 5-minute `renderer-cleanup` token, it listed the `hy-home-renderer`
  accessors. Accessor values went in on stdin only. Result: total 0 and 0
  matching.
- It archived `issuance.json` as `issuance.json.recovered-20261027T172054` and
  wrote the `complete` anchor atomically, as the helper's `clear()` does.

Deleting the stale rendered file was refused as irreversible. Instead, the file
was set to `0640` in place by its owner (UID 100, no network, read-only root);
its content is the Agent's own render.

**Third run — rc=0.** The Agent started at 08:21:50Z and is healthy. The journal
anchor is `complete`.

Residuals:

- Two unused renderer-generation tokens remain valid, the one from the 08:14
  start and the one from 10-22 (B4).
- Changing a template's `perms` takes effect only on a re-render. The
  consumer-migration README now says so, and a source-level fix is not decided.

### v30 B4 renderer issuance journal v3 source — 2026-10-28

Source only. No live token, root, lock or Agent was touched, and no window ran.
The work was done in a worktree on `origin/main` `463eb3b0a`, which contains
`68a4b4753`, and implements the two B4 owner inputs above unchanged.

**What v3 does.** `renderer-issuance.py` writes new journals as
`schema_version: 3`. A run moves through `prepared`, `issuing`, `delivered`,
`verified`, `revoking` and then `complete`. A failed run moves through
`rolling_back` to a `rolled_back` anchor.

1. While the Agent is stopped, the helper reads the old sink token. It uses a
   `docker run` with no network, a read-only volume and `--log-driver=none`.
2. It checks that the token is a live renderer AppRole token and passes a
   revoke-self pre-flight (`sys/capabilities-self`).
3. It stores the token in owner-only 0600 custody under `/run/user/<uid>`.
   The custody file name is bound to the server, the volume and the journal
   directory's device and inode. The journal records only the old token's
   creation time, never a token or an accessor.
4. After the new generation passes readiness and its SecretID is consumed, the
   helper checks that the current sink token is distinct from the old one and
   was created after the issuance started. It then saves `verified`.
5. It checks again that the old token is live, is exactly the captured
   generation, and passes the pre-flight. Only then does it save `revoking`,
   send revoke-self and confirm denial. It writes the `complete` anchor and
   destroys custody.
6. If verification fails, the helper stops this run's Agent and destroys an
   unconsumed SecretID. After a pre-flight, it revokes only a sink token that
   this run minted. The old token and custody are kept.

**v1/v2 compatibility.** The current HOME journal shape, a v2 `complete` anchor
plus `issuance.json.recovered-20261027T172054`, loads as idle, and the next run
writes v3. A `delivered` journal whose Agent is stopped and whose SecretID is
consumed or expired no longer blocks. That is the 2026-10-27 second-run case:
the helper rolls it back by itself, revokes only the token created after
issuance started, and anchors v2 records `complete`. In that case the token is
the 08:14 one; the 10-22 generation is left alone.

**Independent security review (security-auditor, read-only).**

- **First pass — REJECT** with one High and two Medium findings:
  - High: one fixed custody file per UID, so the semantic-restore rehearsal
    could read or destroy HOME's custody.
  - Medium: the sink read went through the Docker log driver.
  - Medium: a 403 before any revoke-self was taken as revoke proof.
  - Medium: rollback could stop a later, foreign Agent generation.
- **Fixes.** All of these were fixed, along with a stale custody `.pending` file
  and a comment.
- **Re-review — APPROVE_WITH_FINDINGS,** with nothing above Low. Two of its
  Lows were then fixed and tested: the journal binding now comes from the open
  journal descriptor, and a resumed rollback with no saved generation blocks
  instead of stopping a running Agent.

**Verification.**

- 167 tests across the issuance, issuance trust/custody, Agent contract,
  rehearsal and semantic-restore suites: OK, with 3 native opt-in tests
  SKIPPED.
- The Agent contract test now runs the real helper end to end through stubs
  that model distinct old and new renderer tokens, revocation (403), custody
  and the read-only sink read.
- A mutation of each new guard fails the suite.
- Ruff: no findings. The changed-profile gate result is recorded in the PR.

**NOT_RUN.**

- Native OpenBao 2.7.1 behaviour of `sys/capabilities-self`,
  `write -force auth/token/revoke-self`, the lookup-self 403 text, and AppRole
  `meta.role_name`. If any of these differs, the helper blocks.
- P06 consumer verification and renewal readback before revoke.
- Any HOME window.

**Residuals (owner).**

- A 403 during capture or rollback is still read as "unusable, skip". That
  token is left unrenewed and expires in about 24 h. Treating it as a block
  would stop issuance after any long Agent stop, so the choice is the owner's.
- Custody is kept after `rolled_back` until the next run, completion or a
  reboot.
- Recreating the journal directory or renaming the server or volume orphans
  custody; a `revoking` journal then blocks.
- A Docker restart of this run's Agent, or expiry between capture and
  `verified`, blocks for owner reconciliation.
- Deadline pressure can roll back a healthy generation.
- Running v1/v2 `delivered` journals with an Agent that is not ready are now
  rolled back instead of left blocked.
- RUN-0103 still describes the v2 contract. Update it when v3 is installed.

**Owner acceptance.**

- The helper hash changes, so a new P01 approval of the merged issuer commit,
  and its installation, are required before any W5.
- The owner runs W5 in a terminal.

### Unused renderer tokens: expiry observation — 2026-10-28

The 2026-10-27 residuals left two unused renderer-generation tokens valid. One
came from the 08:14 start and one from 10-22. Neither is renewed: their Agent
generations stopped, and the period is 24 hours. Each should therefore expire
within 24 hours of its last renewal. The 08:14 token is expected near 08:14Z on
2026-10-28. The 10-22 token's last renewal came before the Agent stopped at
07:45:17Z on 2026-10-27, so it expires earlier.

The owner ran this value-free count on HOME on 2026-10-28:

```text
docker logs openbao --since 2026-10-27T07:45:00Z 2>&1 | grep -c 'revoked lease: lease_id=auth/approle/login/'
1
```

Value-free follow-ups printed only timestamps and never a lease ID.

| Read | Result |
| --- | --- |
| Revocation timestamps (owner) | `2026-10-28T01:39:08.159Z` |
| Retained log start for the window (owner) | `2026-10-27T07:47:01.568Z`, the W5 wrap expiry |
| Log configuration (owner) | `json-file`, `max-file` 3, `max-size` 10m |
| Same timestamp read at `2026-10-28T08:56:59Z` (agent) | Still only `2026-10-28T01:39:08.159Z` |

The retained log starts within two minutes of `--since`, so no line in the
window was lost to rotation. The single revocation at 01:39:08Z fits the 10-22
token: its Agent was renewing until the 07:45:17Z stop, and an unrenewed
24-hour period then ends about 24 hours after the last renewal. **The 10-22
token is recorded as expired.**

The 08:14 token had no renewal before its Agent stopped at 08:15:26Z, so it
was expected to expire near 08:14Z on 2026-10-28. By 08:56:59Z no revocation
appeared, so its state is **UNKNOWN** and it may still be valid. The recording
rule set two outcomes: natural expiry of both at 2 or more, and report-only at
0. This result is 1, so it is recorded and reported to the owner, not recorded
as natural expiry of both. Confirming the 08:14 token needs an accessor
lookup with a management credential, which is the owner's decision.

The current healthy generation, started 08:21:50Z on 2026-10-27, is renewed
and is not expected in this count. Attribution needs the event timestamps and
the log retention start only, never the lease ID. Root and the other
residuals stay out of scope. Source journal v3 (B4) will revoke the old
generation at a future W5 instead of waiting for expiry.

### OpenBao outage and v2 recovery (2026-10-28)

**What happened.**

- **Trigger.** At 16:33:02 KST (07:33Z) a `sudo apt-get upgrade` ran from
  another terminal. systemd stopped `containerd.service` at 07:33:28Z, and
  Docker became active again at 08:06:29Z.
- **Server.** `openbao` exited 255 at 07:34:18Z, with no OOM and no error
  recorded. Its `unless-stopped` policy did not restart it.
- **Other containers.** `crawl4ai-egress` (255) and `airflow-dag-processor`
  (exit 1) also stopped at that moment.
- **Agent.** `openbao-agent` restarted at 07:35:09Z. `start-agent.sh` removed
  its sink, and the 10-27 SecretID had been consumed, so it looped on
  `no known secret ID`. `OpenBaoAgentAuthFailure` fired from 07:42:53Z.
- **Consumers.** Rendered files stayed in place throughout.

The diagnosis used only container state, the systemd journal and redacted
Agent log lines; no value was read. Nothing was started, stopped or unsealed
by the agent.

**Owner recovery, 09:32–09:35Z, on the owner's choice to use the installed
v2 issuer.** The owner ran `docker start openbao`. Before unseal, `bao status`
could not connect. Two of three shares were entered through the hidden prompt,
and the server became active at 09:32:39Z on version
`2.7.1+hyhome.go1.27.3.net0.60.0.r1`.

The owner then ran RUN-0103 `agent-restart` through `p01_run` on reviewed
script commit `977baee0bb24ae693381412da74059a7db0c43de` with these inputs:

- issuer `422b4adfd108429e2acc5c4df313761227d36f4d`;
- the operator tools root;
- `hy-home-infra_openbao-agent-data`;
- the existing journal, whose anchor was v2 `complete`.

Results:

- **Issuance.** It printed `issue rc=0` and `agent: healthy`. Every rendered
  `.txt` is `-rw-r-----` and every `.version` is `-rw-------`; the Grafana
  client secret has no version template.
- **Value-free postcheck.** The journal anchor is v2 `complete`. `openbao` and
  `openbao-agent` are both healthy, the Agent since 09:34:17Z.

**Residuals.**

- **Orphaned 10-27 08:21 Agent token.** Its sink copy was removed at 07:35Z
  without revocation. It is no longer renewed, so it should expire within the
  24-hour period. Like the 08:14 token, it is UNKNOWN until an expiry is
  observed, and no owner-held policy can look it up.
- **OpenBao server metrics.** Server metrics have not been scraped since
  2026-10-24 10:04Z, and `OpenBaoMetricsScrapeFailing` keeps firing. This is
  separate from the outage. The cause given here at first, a Prometheus DNS
  failure, was wrong; see the correction in the follow-ups entry below.
- **Other stopped containers.** The owner decides on restarting
  `crawl4ai-egress` and `airflow-dag-processor`.

**B4 v3 install packet.** These are the inputs for a new P01 approval; they
are not an approval.

| Input | Value |
| --- | --- |
| Issuer commit | `4f2e7f9badf2db592de91d20146d68f87a228213` (PR #602) |
| `issue-renderer-secret-id.sh` | `d92ed0353fc6885ec803a223cb1eeb845d78b3f86cde4e2ed700c9a276df1878` (same as v2) |
| `renderer-issuance.py` | `b20015ab047255d7af0c6e97e2b613faef0db220b2e513805bff40e881122f50` (v2: `8175070b…`) |
| `renderer-request.sh` | `be1865325138679ab8cac82e0203cdbe308c2f66651b920c0f2c4cb9ae103014` (same as v2) |
| Installer `install-renderer-issuer.sh` | `27a097f133ced7bc1d3657c401a16fa923d464878a10b38d69d5e0e7033343c9` (unchanged; RUN-0103 step 2 pin) |

Installation runs RUN-0103 step 2 with `issuer_commit` set to the commit above
and the existing operator tools root. A later W5 then passes that commit to
`agent-restart`. RUN-0103 now describes v3 and this outage pattern.

### Outage follow-ups and v3 install (2026-10-28)

**v3 issuer installed.** The owner approved B4 v3 for P01 on 2026-10-28
("Approve v3 for P01, then install it"). RUN-0103 step 2 ran verbatim from the
runbook with:

- `issuer_repository=/home/hyunyoun/data/hy-home.docker`;
- `issuer_commit=4f2e7f9badf2db592de91d20146d68f87a228213`;
- the existing operator tools root.

It exited 0. The new directory holds the wrapper (mode 0500), the helper and
request shell (0400), and `source-receipt.json` (0400). The receipt names the
same commit, and all three file hashes match the install packet above. No W5
ran, because the Agent was healthy after the v2 recovery; the next W5 passes
this commit to `agent-restart`. The v2 directory `422b4adfd…` is left in place.

**Stopped containers restarted.**

- **`airflow-dag-processor`.** It had exited 1 at 07:47:32Z because `mng-pg`
  reported "the database system is starting up". With `mng-pg` healthy,
  `docker start` brought it back healthy.
- **`crawl4ai-egress`.** Its first start failed with `Address already in use`.
  `crawl4ai`, which had a dynamic address on `crawl4ai_egress_net`, came back
  first at 07:35:17Z and took the gateway's static `10.250.200.2`. Stopping
  `crawl4ai`, starting the gateway, then starting `crawl4ai` restored `.2` for
  the gateway (healthy) and `.3` for the crawler.
- **Source fix.** The crawler now has a fixed `10.250.200.3`. The egress test
  first failed with an error, then passed with 15 OK and 6 native tests skipped,
  and the public Compose config passed. The running crawler already holds
  `.3`; the configuration takes effect at its next recreate.

**OpenBao server metrics.**

- **Root cause: the metrics token expired.** The owner printed only the
  custody file's `expires=` line: `2026-10-24T10:04:32.941302101Z`. That is
  21 seconds before the first failed scrape at 10:04:53Z.
- **Correction.** The earlier "Prometheus DNS since 10-24" diagnosis was
  wrong. The `lookup openbao … server misbehaving` error seen at 09:28Z
  existed only because `openbao` was down during today's outage. Once the
  server was restarted, Prometheus resolved `openbao` on the shared networks,
  and the scrape returned `403 Forbidden`, the expired token.
- **Boundary.** The agent's own attempt to read that `expires=` line was denied
  by the `secrets/` boundary and was not worked around.
- **Owner steps.** RUN-0104 rotation needs the temporary root session of
  RUN-0096 5.2/5.4, because the operator policy cannot mint a `prometheus`
  token. This stays an owner step.

**Host upgrades.** RUN-0085 now treats `containerd.io` and `docker-ce` upgrades
as an OpenBao maintenance window, with a pre-check, an optional package hold,
and the recovery order.

**Owner decisions after review, 2026-10-28.**

- **RUN-0104 fixes.** RUN-0104 gains an expired-old-token branch. When the
  custody expiry has passed, the procedure no longer stops at the pre-revoke
  lookup. Instead it requires the server's explicit `invalid accessor`, plus a
  working management caller and server, then records `old: expired` and skips
  the revoke. RUN-0104 also gains a least-privilege throwaway client that
  mounts only the CA, the policies and the work directory.
- **Metrics token TTL.** The metrics token TTL becomes 1 year (`8760h`). In the
  same temporary root session, the `token/` mount maximum is tuned to `8760h`
  first. A non-expiring ordinary service token is not possible: TTL 0 follows
  the mount maximum, and a periodic token expires unless renewed.
- **New `status` step.** A new read-only `owner-window.sh status` step prints
  states and dates only. It covers container health, seal state, the journal
  anchor, the metrics token expiry with a 30-day warning, OpenBao alerts and
  targets, and stopped containers. It exits 1 on any problem.
  - **Test.** The owner-script test covers healthy and problem cases, and
    asserts that the custody accessor is never printed.
  - **Live run.** The agent ran it read-only with the custody path pointed
    away from `secrets/`. It reported the 403 target and the firing alert.
  - **Owner run.** The owner's run reads the real expiry.
- **Rotation itself.** The rotation stays an owner root-session step: RUN-0104
  with the expired branch.

**Independent security review (security-auditor, read-only).** The verdict was
APPROVE_WITH_FINDINGS, with nothing Critical or High. `status` cannot print a
token, accessor or value, and it mutates nothing. Each finding was fixed:

- **Expired-token branch (Medium).** Its silent guards could let a malformed
  custody file be recorded as `old: expired`. The guards now print, and
  acceptance also needs the deployed token, copied before the file swap, to
  fail lookup with `bad token`.
- **Journal path (Medium).** `status` used an invented default journal path.
  It now requires `issuance_journal` and also warns on `*.pending` files.
- **Lower findings.** These were also fixed:
  - every problem now prints `WARN`;
  - a missing container is reported;
  - the Docker host and context are unset;
  - containers stopped by signal are not counted;
  - a clean exit-0 test and a nonce no-leak check were added;
  - the new token is bound with `-explicit-max-ttl=8760h -renewable=false`;
  - the work-directory ownership is checked;
  - expected results accept `old: expired`;
  - host upgrades refresh the package list first, keep the hold by default,
    name unattended-upgrades and reboots, and use `docker start` rather than
    `up -d`.

**Placement fix (hosted CI).** Hosted `candidate-quality` failed on the
status test. The reviewed status body had been inserted at the end of the `w4`
step, so `w4` ran it after the unseal, and `status` still ran the first draft.
The body now sits only under `status`, and the first draft is deleted. A
target with an empty `lastError` was also warned as a problem, because `read`
strips the trailing space; the step now matches the job and health fields. The
agent's earlier live run used the first draft. The RUN-0105 manifest pin
follows the new script hash. The Crawl4AI runtime test now reads the network
names from the new map form. The seal probe now uses `docker exec`, as the
Prometheus probe does, because the Compose form changes into the fixed host
checkout, which hosted CI does not have.

**Residual (owner decision).** Tuning the `token/` mount to `8760h` is
persistent. Any caller allowed on `auth/token/create*` can then get an
explicit TTL of up to one year. Today the renderer roles pin 5 minutes and
`k8s-bootstrap` has a 2-hour explicit maximum. The operator policy's
`auth/token/create/k8s-bootstrap` path, however, has no parameter limit, so
that role's explicit maximum becomes the only bound.

### Owner steps as scripts (2026-10-28)

The owner asked for each follow-up as a working script. Three steps join
`owner-window.sh`:

- **`metrics-rotate`.** It runs RUN-0104 end to end with the root that the
  RUN-0105 W1 ceremony leaves in custody. W7 `revoke-root` then revokes that
  root. The step:
  - issues the 1-year token and checks its shape and least privilege;
  - classifies the old token (valid, expired, stale custody or
    INDETERMINATE);
  - swaps the deployed file and recreates Prometheus alone;
  - waits for `up{job="openbao"}` to equal 1, revokes a valid old token and
    rewrites the custody.

  Tokens and accessors travel over stdin only. A failure before the target is
  up revokes the new token and restores the old file. The RUN-0105 manifest
  now pins `prometheus.hcl` so that the bootstrap copy carries the reviewed
  policy.
- **`renderer-expiry <since>`.** It prints only the timestamps of revoked
  renderer AppRole login leases, plus the time the server became active.
- **`metrics-revoke`.** It retries what `metrics-rotate` could not confirm,
  before W7.
- **`host-hold`.** It holds `containerd.io`, `docker-ce` and `docker-ce-cli`
  and, when needrestart is installed, excludes containerd and Docker from its
  restarts.

**Independent security review (security-auditor, read-only).** The verdict
was APPROVE_WITH_FINDINGS, and it found no path that prints or passes a
value. Each finding was fixed:

- **Custody that names another token (High).** The valid branch could revoke
  a custody accessor that belongs to some other token. The deployed file is
  now the truth: its lookup must match the custody accessor and policy.
- **Unchecked revocation (Medium).** "Revoked" now needs the server to refuse
  a lookup afterwards. The new token is revoked by value through stdin, so the
  two early failures after creation also revoke it.
- **Stale target sample (Medium).** Only an `up` sample taken after the
  recreate counts.
- **Rollback (Medium).** A failed restore is reported and leaves the new
  token unrevoked. With an expired old token, the verified new token stays
  deployed and goes into custody instead of being rolled back.
- **Lower findings.** These were also fixed:
  - custody is written before the old token is revoked, so a re-run does not
    deadlock;
  - an unconfirmed token leaves an `*.unrevoked` marker, and `cleanup`
    refuses to delete its directory without `--discard-metrics`;
  - leftover temporary files are removed;
  - positive controls (root lookup, unsealed server) back the expired and
    revoked verdicts;
  - `renderer-expiry` fails when `docker logs` fails, and prints a count and
    the start of the retained log;
  - the runbook wording on mode and group was corrected.
- **Informational.** dockerd debug is off, so the exec environment is not
  logged. `host-hold` writes only constant text.
- **Test gap (recorded).** `bao_as` calls `/usr/bin/docker` by absolute path
  on purpose, so tests cannot stub the token classification and rollback
  branches. The tests cover the preconditions, `cleanup`, and the
  value-free output of `renderer-expiry` and `host-hold`. The first live run
  is the owner's.

**Re-review (same auditor).** The verdict was APPROVE_WITH_FINDINGS, with
F1–F3 and F5–F10 closed. It reopened the stale-sample finding: an instant
query's `value[0]` is the evaluation time, not the sample time. Fixes:

- **Sample time.** The wait now uses `timestamp(up{job="openbao"} == 1)`. A
  read-only live check showed a fresh timestamp for the `prometheus` job and
  an empty result for `openbao`, whose `up` is 0.
- **Failed restore.** A failed file restore records the deployed new token in
  custody and marks the still-valid old token. A restored file with
  Prometheus still down is reported as such, and the new token is revoked.
- **Recovery step.** `metrics-revoke` retries an unconfirmed revocation or
  custody write with the W1 root, and must run before W7 `revoke-root`.
  `cleanup` refuses while a marker exists, and its flag can no longer come
  from the environment.
- **Empty file.** An empty deployed token file stops the run.

**Why the manual root session stopped.** The owner had started the manual
RUN-0096 client. `R` stopped with `missing root token; STOP` because no
runbook gives commands to issue the temporary root. The guard worked: no root
command ran, and OpenBao was not changed. The scripted path replaces that
manual root step.

**Handover from the hy-home.k8s session (read-only, 13:10Z).** Two facts came
in:

- `openbao` has `unless-stopped` and a restart count of 0. It started at
  09:31:43Z, so the owner started it. Docker did not restart it when dockerd
  returned, while `openbao-agent` and Crawl4AI did. The cause is UNKNOWN. With
  a Shamir seal and no auto-unseal, a restart would only have brought it back
  sealed. Detection is the `status` step plus the existing `OpenBaoSealed`
  and `OpenBaoMetricsScrapeFailing` alerts, so no new alert is added.
- The 10-27 08:21 Agent generation lost its sink at 07:35Z on 10-28. Its
  token should expire by about 07:35Z on 10-29. `renderer-expiry
  2026-10-28T07:35:00Z` after that time records it as expired or UNKNOWN.

**08:14 token: agent run of `renderer-expiry 2026-10-27T07:45:00Z`, about
13:20Z, read-only.** The output was:

```text
2026-10-28T01:39:08.159Z
2026-10-28T09:32:41.749Z
2026-10-28T09:32:41.847Z
server active since: 2026-10-28T09:32:39.599407309Z
```

The 08:14 token's expiry near 08:14Z on 10-28 fell while the server was
down, from 07:33Z to 09:31Z. The server revokes such leases when it becomes
active, and two revocations follow activation by two seconds. With 01:39:08Z
(the 10-22 token) the count is 3. Under the owner's rule (2 or more), the
08:14 token is **recorded as natural expiry** at 09:32:41Z. The second
startup revocation is not attributed: timestamps cannot tell which lease it
was. If it was the 08:21 generation's token, the check after 07:35Z on 10-29
shows no new line, and that token is then recorded from this line, not as
UNKNOWN.

### OpenBao runbooks: headings and script files (2026-10-28)

The owner asked to give each OpenBao runbook proper headings, and to move the
scripts written in them into script files.

**Headings.** RUN-0085, 0103, 0104, 0105 and 0106 gained H3 to H5 headings for
each step and rule. Bold run-in labels became headings. Body text and every
linked anchor stayed the same; a line-by-line comparison showed only the
removed labels. RUN-0106's P02 catalog checks moved under Procedure, and its
Verification now names the expected results. In RUN-0105, two sections moved
to the place the text already gave them: the previous-root sweep now follows
W1, and W7 root revocation now precedes Finish.

**Scripts (owner decisions).** Only `p01_run` stays as pasted code:

- **`p01_run`.** It now lives in RUN-0085 "Reviewed Script Runner" and gained
  the checks the removed inline blocks had: the repository path is not a
  symlink, the repository and `.git` match their recorded device, inode and
  owner, and the `LD_*` and `PYTHON*` variables are unset.
- **`p01-bootstrap.sh`.** The RUN-0105 W1 source bootstrap block became this
  script, with the hash manifest inside it. `p01_run` runs it from the
  approved commit, never from the checkout. The tests now read the manifest
  from the script.
- **Issuer installer.** RUN-0103 step 2 now runs
  `install-renderer-issuer.sh` through `p01_run`. The approved commit pins
  the installer instead of the separate hash `27a097f1…`, and the installer
  still runs itself under `env -i`.
- **`preflight`.** The RUN-0105 W0 checks became an `owner-window.sh` step.
  It ends by clearing the window's path variables, as the block did.
- **RUN-0104.** The manual commands were removed. The rules stay, and
  `metrics-rotate` and `metrics-revoke` are the only executable path. The
  steps now start with `preflight` and the bootstrap, and include
  `root-sweep`.

**Independent security review (security-auditor, read-only).** The verdict
was APPROVE_WITH_FINDINGS, with nothing Critical or High. The trust chain held
for an honest object store and a clean environment. Each finding was fixed:

- **Failed bootstrap kept going (Medium).** A pasted block's `exit` used to
  close the owner's shell. A script's `exit` only ends the script, and the
  vars file had been written before the pins were checked. The bootstrap now
  records the path variables only after every pin passes, and it removes the
  copy on failure. The runbooks load the vars only on success (`&&`).
- **Inherited environment (Low-Medium).** The window shell now starts from
  `env -i` with absolute paths. `p01_run` runs `/usr/bin/bash` and unsets
  `BASH_ENV` and `ENV`.
- **Object store as the anchor (Low).** `p01_run` re-hashes the copied blob
  against the commit's object ID. A replaced tree object behind the same
  commit stays a residual risk: only a process running as the owner's UID can
  do that, and that same UID can already read W1 custody.
- **Lower findings.** These were also fixed:
  - the bootstrap writes no readonly variables, so a retry in the same shell
    takes the new commit;
  - `preflight` counts failed checks, exits 1, and refuses to clear the vars
    file while an earlier window's custody exists;
  - `p01_run` checks that `XDG_RUNTIME_DIR` is an owner-only tmpfs;
  - the window-shell text and RUN-0104's step split were corrected;
  - tests pin `p01_run`'s checks, and check that the bootstrap writes the vars
    file only after the manifest.
- **Live check (read-only).** In a clean bash, the new `p01_run` ran the
  merged main commit's `owner-window.sh nope`, which returned the usage exit 2.
  A short commit was refused with exit 1, and no temporary file was left.
- **Re-review (same auditor).** The verdict was APPROVE_WITH_FINDINGS, Low
  and Info only. Three items were fixed:
  - `preflight`'s image and R2 checks now run under `bash -o pipefail`, so
    their status is no longer `tail`'s;
  - the bootstrap sets `ok=0` before its trap, so the environment cannot keep
    a copy that failed a pin;
  - the `p01_run` text now claims only blob re-hashing. Tree substitution is
    named as the accepted residual risk.

### Metrics token rotation: owner run (2026-10-28)

The owner ran the scripted RUN-0104 rotation in a clean `env -i` bash, using
`P01_APPROVED_COMMIT` `67357246f1afae063878cc757aaa466a8747e75f` (PR #607).
This was the first live run of `preflight`, `p01-bootstrap.sh`,
`metrics-rotate` and the new `p01_run`. The output below is value-free.

| Step | Result |
| --- | --- |
| `preflight` (run twice) | `problems: 0`; `Sealed false`, image `a58fb110…`, dockerd debug false, Linger yes, R2 60 snapshots |
| `p01_run` with `p01-bootstrap.sh` | 20 × `OK`, `bootstrap ok` |
| `token w1` and `check-token w1` | policies `default` and `hy-home-operator`, path `auth/oidc/oidc/callback`, `started:false` |
| `w1` | `DELIVERED` |
| `root-sweep` | `revoked=0`, `remaining=0` |
| `metrics-rotate` | `metrics: allowed`, `policy list: denied`, `old token: expired`, `target: openbao up` |
| New token | `new: expires 2027-10-28T14:31:33Z` |
| Old token | `old: expired (2026-10-24T10:04:32Z)` |
| `status` | `problems: 0`; metrics token 364 days; targets `openbao` and `openbao-agent` up |
| `revoke-root` | `ROOT_REVOKED_OPERATOR_HEALTHY` |
| `cleanup` | `revoked p01-op-w1.token`; `revoke failed p01-op-w7.token` |

Notes:

- **Prometheus restored.** OpenBao server metrics are back, so the 2026-10-24
  outage is closed. An agent read-only check afterwards showed `up` = 1 for
  both jobs and no OpenBao alert active.
- **Pending alert.** `OpenBaoTooManyPendingTokens` was pending at 14:32:53Z,
  when metrics first returned after the outage. It cleared within its
  5-minute `for` window. Its expression read -1 afterwards.
- **`jq` noise.** `metrics-rotate` printed two `null cannot be parsed as a
  number` lines. They came from the wait loop, while Prometheus had no
  post-recreate `up == 1` sample yet. The wait still worked. The empty result
  now counts as "not up" without an error.
- **w7 revoke.** `revoke-root` confirmed the w7 operator healthy right after
  root was revoked. The w7 token therefore became invalid only between that
  check and `cleanup`. The likely cause is that it came from the same UI
  login as w1, so revoking w1 already revoked it. If it was a separate login,
  it expires within its 1-hour TTL (4-hour maximum). The value was shredded
  with the file.
- **Leftover client copies.** `cleanup` left four `p01-client.*` directories.
  They hold only reviewed source copies and no secret.
- **Garbled paste.** In the owner's paste, the last lines of `p01_run` were
  redrawn out of place by the terminal. The function still ran, as the
  bootstrap's `OK` lines show.

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
| HOME custody attestation | 11 | W23 | Off-host custody of unseal shares, offsite key, R2 credentials, Cloudflare account access and CA key, value-free; owner states it is not separated yet | Owner checklist step 5 | NOT_RUN | Owner Decisions — 2026-10-13 | - |
| Host custody step 5 | 11 | W23 | owner-attested RUN-0085 step 5 table (SPEC-0242), value-free: BKP-002, BKP-003, R2 credentials and R2 account ID and bucket on the owner's separate desktop, Cloudflare access in password manager account hyunyoun, all off the host; R2 listing with those values; host second copy; recovery means outside those places and the host; each checked 2026-10-14 | Owner statement 2026-10-14; RUN-0085 0.12.2 | PASS | Step 5 Owner Record — 2026-10-14 | - |
| HOME semantic restore | 11 | W23 | Empty-target restore with canary read and renderer reauthentication | Owner checklist step 6 | NOT_RUN | Source Corrections — 2026-10-13 | - |
| HOME audit capacity | 11 | W23 | Audit filesystem capacity and logrotate registration | Owner checklist step 7 | NOT_RUN | Source Corrections — 2026-10-13 | - |
| HOME upgrade and cold boot | 11 | W23 | Server and Agent 2.7.1 upgrade, manual unseal, wrapped reissue, cold boot | Owner checklist steps 8–9 | NOT_RUN | Source Corrections — 2026-10-13 | - |
| Source corrections | 11 | W23 | Runbook timing and checklist, Task stale points; changed metadata (2 documents, 0 violations), corpus lifecycle (0), links `--mode all` PASS, `test_operations_catalog` OK, markdownlint passed | Branch on `ec0877f10` | PASS | Source Corrections — 2026-10-13 | - |
| Attempt cleanup | 11 | W23 | Owner-run removal of attempt 03, 04 and chown containers and the `-03` target; no container left, live server and Agent healthy | HOME, value-free metadata | PASS | Preserved Attempt Cleanup — 2026-10-13 | - |
| Audit logrotate registration | 11 | W23 | Deferred: the running server has no audit mount, so registration waits for the upgrade window | HOME check 2026-10-13 | NOT_RUN | Preserved Attempt Cleanup — 2026-10-13 | - |
| Leftover target cleanup | 11 | W23 | Empty base target removed with `rmdir`; `-04` target deleted by the owner; no `p01-*` directory left, live server and Agent healthy; pre-2.7.1 snapshot kept | HOME, value-free metadata | PASS | Owner Decisions — 2026-10-13 | - |
| Agent alert gap | 11 | W23 | No Agent metrics or alert; gap recorded, telemetry and alert deferred to a separate Spec | `agent.hcl`, Prometheus config | NOT_RUN | Owner Decisions — 2026-10-13 | - |
| Agent alert source | 11 | W23 | SPEC-0239 telemetry, scrape and alerts merged (PR #463, #466; candidate passed); deployment NOT_RUN | `main` `b4291bb43` | PASS | Agent Alert Source — 2026-10-14 | - |
| Maintenance window plan | 11 | W23 | RUN-0085 window plan with commands, signals, stops, rollback and approvers; HOME execution NOT_RUN | Branch on `origin/main` | PASS | Maintenance Window Plan — 2026-10-13 | - |
| Maintenance OTP argument defect | 11 | W22 | Independent source inspection: stdin-only claim conflicted with executable OTP arguments and unsupported process-isolation assumption | RUN-0085 SHA256 0db6f3d23ec0e93a00a1276c29d57603937294c543b4546c623f5c7baa9a9785 | FAIL | Maintenance-window input correction | - |
| Maintenance protected-input correction | 11 | W22 | Remove unsafe OTP CLI block; retain protected authenticated API/custody boundary and explicit BLOCKED/NOT_RUN | RUN-0085 SHA256 81ce399fead9074dd92f06b37094e9cc30a987709fa5cbe24e6e209e4d03521b | PASS | Maintenance-window input correction | Maintenance OTP argument defect |
| Maintenance correction review and frozen QA | 11 | W22 | Independent exact-hash security approval and metadata selection 14/0; catalog/navigation exit 0; no credential/native action | RUN-0085 81ce399fead9074dd92f06b37094e9cc30a987709fa5cbe24e6e209e4d03521b; Task pre-receipt 526a6916eb5847cd6b2a0b7a597156e6209683fd801ad8572a297d47f8ca0cdc | PASS | Maintenance-window input correction | - |
| Current HOME preflight | 11 | W23 | Auth-free status, selected mount and backup unit metadata | main1e7e2ba; cluster51fbfa38-a715-7dca-629f-3f07233749f4 | PASS | Current Operation Preparation — 2026-10-14 | - |
| Current backup unit failure | 11 | W23 | Result exit-code, status1; fresh pre-upgrade snapshot absent | hyhome-backup.service 2026-10-14 03:43:29 KST | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Candidate pull and CLI probe | 11 | W23 | Exact amd64 child pull; bounded network-none version probe; transient removed | index6d2b938; childa36ea8; revisiona5db72c | PASS | Current Operation Preparation — 2026-10-14 | - |
| Image signature cache failure | 11 | W23 | Public pinned Cosign verify failed on readonly tool cache | CosignOCI9e5c2f; OpenBaoindex6d2b938 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Image signature identity mismatch | 11 | W23 | Binary checksum workflow identity refused OCI image workflow | OpenBaoindex6d2b938 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Exact image publisher signature | 11 | W23 | Correct official image identity; issuer/certificate/transparency and exact digest; exit0/four rows | OpenBaoindex6d2b938; release-images.yml tagv2.7.1 | PASS | Current Operation Preparation — 2026-10-14 | Image signature cache failure, Image signature identity mismatch |
| Current gateway trust | 11 | W20 | Protected public CA hash plus token-free TLS CA/SAN verification | publicCA6b7c5c75; 192.168.0.13:443 | PASS | Current Operation Preparation — 2026-10-14 | - |
| Initial protected client review | 11 | W20 | Independent code/security found five input/identity/uncertainty defects despite34 unit PASS | client2013e441; test23703ee0 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Corrected protected client review and QA | 11 | W20 | Exact-hash independent code/security approvals;46 unique tests PASS/0skip;93% branch coverage;Ruff/format/diff | client640a3bd7; testsc8cba04c/6b68869c | PASS | Current Operation Preparation — 2026-10-14 | Initial protected client review |
| Exact owned-version client compatibility | 11 | W20 | Focused RED then47 PASS; exact-delta code approval and independent security replay; no native image claim | client2c610157; testsc8cba04c/13feeb75 | PASS | Current Operation Preparation — 2026-10-14 | - |
| Initial protected token operations review | 11 | W20 | Recovery access, HOME/custody identity, HTTP/schema and TTL findings despite85 unit PASS | client3b3f0f8c | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Corrected protected token operations review and QA | 11 | W20 | Independent code/security approvals;99 unique PASS/0skip;87% branch coverage; source hashes stable; no actual credential action | clienteecf50f6; tests38f10909/41ff32b0; policy1aa658e0 | PASS | Current Operation Preparation — 2026-10-14 | Initial protected token operations review |
| Snapshot token destination metadata | 11 | W23 | Exact owned0700 directory, token and issuance lock absent; no private contents read | HOMEdev64512/inode4338469; destinationinode5260267 | PASS | Current Operation Preparation — 2026-10-14 | - |
| Initial protected snapshot review | 11 | W21 | Independent native-schema, path/namespace/digest/alias and uncertainty findings despite76 unit PASS | client062e929b; test7aaadcad | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Intermediate snapshot publication review | 11 | W21 | Overwrite, post-save uncertainty and source binding defects despite88 unit PASS | clientb390; archive48ff7d0e | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Snapshot link publication review | 11 | W21 | Concurrent final-name replacement can lose sole verified copy despite95 unit PASS | clientfbaf9d74; custody29ef5cf3 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Final protected snapshot review and QA | 11 | W21 | Independent code/security approvals;100 unique PASS/0skip;85/83/89% branch; no native/HOME action | client2779382f; archive48ff7d0e; custodyfd266cdd; testsc2acc33f/314ea3b8 | PASS | Current Operation Preparation — 2026-10-14 | Initial protected snapshot review, Intermediate snapshot publication review, Snapshot link publication review |
| Maintenance execution-order review | 11 | W23 | Semantic restore order, missing snapshot authentication/artifact and precreate audit findings | base1e7e2ba Run0085 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Audit directory preparation failed attempts | 11 | W23 | Noninteractive sudo exit1; Docker argument exit125; final path remained absent | exact audit path; current2.6.2 image | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Audit directory prepared | 11 | W23 | Independently READY direct-mkdir; exit0, exact dev/inode/100:1000/0700/capacity; transient removed | device2064 inode115609395 | PASS | Current Operation Preparation — 2026-10-14 | Audit directory preparation failed attempts |
| Audit rotation target race | 11 | W21 | Name-based inspect/kill can target a replacement; meaningful RED2fail | rule67a306be; testbf0348d7 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Audit rotation parser group failure | 11 | W21 | Actual isolated parser rejected numeric group forms | rule57ee84e7 and intermediate group correction | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Audit rotation source and isolated parser | 11 | W21 | Immutable ID/label guard, native NSS correction, seven tests and exact-hash IaC approval; isolated3.22 debug one-rule exit0; no host mutation | rule2ad4473a; teste0c36c1f | PASS | Current Operation Preparation — 2026-10-14 | Audit rotation target race, Audit rotation parser group failure |
| Audit rotation host privilege | 11 | W23 | Host3.21 debug EPERM and noninteractive sudo failure; registration and actual rotation not performed | current host package/NSS, exact rule | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Current operation physical inputs | 11 | W23 | User reports custody or actual holders still need preparation | Direct 2026-10-14 user answer | NOT_RUN | Current Operation Preparation — 2026-10-14 | - |
| Current operator readiness attestation | 11 | W23 | buenhyden confirms shares and off-host preparation; no values or actual ceremony processed | Latest direct 2026-10-14 user answer | PASS | Current Operation Preparation — 2026-10-14 | - |
| Owned-build r3 source admission | 11 | W23 | Independent code/security/IaC, 41 unique unit tests, frozen seven inputs, fresh plan/preflight | packet e2487b5b; materials c60926e2 | PASS | Current Operation Preparation — 2026-10-14 | - |
| Owned-build r3 native compile | 11 | W23 | Pass1 exit1 after53.649s, bounded tmpfs ENOSPC, no OOM, exact-ID cleanup | packet e2487b5b; preserved owned-build-frozen-r3 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Owned-build r4 native attempt | 11 | W23 | Compile1/runtime1 PASS, wrapper failure before pass2; first OCI retained, cause diagnosis pending | packet2370a5d3; preserved owned-build-frozen-r4 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Common integration r1 review and QA | 11 | W23 | Process trust, exact off-host gate, anchor, literal, manifest order/tracking and concurrent-input mismatch | common manifest13685533 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Common integration r2 authority and links | 11 | W23 | Draft/non-governing runtime authority and three root-prefixed README targets; r2 hashes stable | common manifestb617d339 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Common integration r3 authorization wording | 11 | W23 | Rules rejected wording implying controller-granted approval | common manifest7d2eff2e | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Common integration r4 rules correction | 11 | W23 | Independent exact-hash rules PASS; controller verifies trusted origin, eleven unchanged rows; aggregate pending | common manifest10eb5361; Runf3b44449 | PASS | Current Operation Preparation — 2026-10-14 | Common integration r3 authorization wording |
| Owned-build r4 attempt2 reproducibility | 11 | W23 | Two clean compiler and runtime passes; identical binaries/build-info, whole OCI differs only apk.log wallclock bytes | packet2370a5d3; retained owned-build-frozen-r4-attempt-2 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Renderer request peer source integrity | 11 | W20 | Independent security found mutable pathname reopen after verified receipt despite55 unit PASS | packet2f671fe3 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Offsite readiness inspector r1 review | 11 | W23 | Semantic duplicate, argv, mixed-file and executable-source binding defects; actual private reads zero | inspector3f972975; nine synthetic PASS | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Renderer protected peer and installer r2 | 11 | W20 | Independent exact6-file code/security approvals;55 PASS90%branch; Runbook held-byte bootstrap separately approved | packet794fb462; Runc2c94d0f | PASS | Current Operation Preparation — 2026-10-14 | Renderer request peer source integrity |
| Integrated Agent fixture compatibility | 11 | W22 | Two actual failed test inputs, then corrected request framing and independent journals;26 PASS | current integration onf1af4b59 | PASS | Current Operation Preparation — 2026-10-14 | - |
| Current combined synthetic source regression | 11 | W22 |134 run:131 PASS/3 native-opt-in SKIPPED; exit0, no native/runtime claim | R5productc318; rendererR2; root fixtures | PASS | Current Operation Preparation — 2026-10-14 | - |
| Actual offsite local readiness r2/r3 | 11 | W23 | Fixed-code local input refusals ENV_BINDING then ENV_ACCOUNT_SYNTAX; no network/transfer/private output | inspectorddc03549; launcher6874b957 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Semantic restore moving initial review input | 11 | W23 | Author changed frozen source/test before independent review; old hashes not accepted | source327ab851/e597962e | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Semantic restore source independent review | 11 | W23 | Code/security/IaC blockers despite28 synthetic PASS80%branch; actual recovery NOT_READY | source4ffd0ec3/tests8ba3a111 | FAIL | Current Operation Preparation — 2026-10-14 | - |
| Actual quoted R2 local readiness correction | 11 | W23 | Minimal Compose literal normalization, independent exact review,14+10 synthetic PASS; actual exit0 LOCAL_INPUTS_READY; no remote/custody proof | inspectorff6bae4f/launcher5f75e150 | PASS | Current Operation Preparation — 2026-10-14 | Actual offsite local readiness r2/r3 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 11 | pending | - | - |

## Review and Completion

Prior source delivery merged in PR421 and PR431 (merge `7620f2d22`). The
current protected-client/common integration and field-metadata clarification
were merged in PR472 as5cdf684902. The two reviewed test-fixture TLS minimum
fixes were not part of that merge and are carried in the follow-up source
branch recorded above. Hosted clearance is assessed per exact head.
The current Task remains blocked on the exact identity, custody/cleanup,
Native, renewal/boot/recovery and consumer residuals recorded in the v29 handoff
above. Reuse the dated accepted `-06` restore and HOME 2.7.1/Agent window
outcomes; do not treat the earlier unperformed window steps as current failures
or repeat issuance to close this document. Those scoped outcomes do not close
criterion 11, accept all P06 migration/rotation or provide new operating authority.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [P00 Task](../../0212-request-baseline-and-reconciliation/tasks/tsk-0003-active-contract-and-exclusions.md)
- [OpenBao Runbook](../../../05.operations/runbooks/04-security-and-secrets/0085-openbao.md)
- [Backup Runbook](../../../05.operations/runbooks/10-platform-and-backup/0021-backup-and-restore.md)
