---
title: "SEC01 Stable Security Integration Task"
version: "0.4.3"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0009"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-10"
---

# SEC01 Stable Security Integration Task

## Objective

Integrate the SEC01 stable/security source ledger and bounded repairs without
treating candidate images, source receipts or isolated recovery rehearsal as
production rollout. This Task owns criterion 15 and W31. It does not replace
CLN01 criterion 12/W24, P09 criterion 13/W25, or SMTP01's criterion 14/W26–W30
reservation.

## Inputs and Authorization

The direct 2026-10-10 request and coordinator authorization issue this Task on
base main `e93e0c8223191bf26aea7578a231b2dbf016fc7c`. SEC01's six-commit source
branch ended at `55a0d4719635f325f1d4ea477dcf50a5ff5ddbf6`; PR #416 was merged
at the base revision, but latest candidate-quality CI run `38052766613` failed.
CodeQL and GitGuardian passed; main-security was skipped. This Task therefore
starts in progress with latest/security acceptance blocked, not complete.

The received ledger is `infra/09-platform-ops/security-updates/integration-handoff.json`.
It is evidence input, not permission to apply proposed common-file patches. The
coordinator serially integrates the shared validator, service inventory, script
manifest and navigation after current-main review. The received source-only
slice made no deployment or private-resource claim. The subsequent direct user
request authorizes full current-stable security and bounded native HOME/recovery
continuation, plus actual SMTP/CLN retirement and recovery under their owners.
Each operation still needs exact inputs, effects, verification and recovery
bounds; existing matching user authorization is reused. LAB runtime, learning
applications and actual Wiki implementation remain excluded.

### Public Cosign Bootstrap Boundary

The coordinator may select one fresh, current-user-owned mode-0700
`/tmp/hy-home-sec01-trust.*` directory for public tooling only. Six exact
hash-pinned prebuilt wheels (tuf 7.0.1, securesystemslib 1.5.1, cryptography
50.0.2, urllib3 2.8.0, cffi 2.1.1, pycparser 3.11) install offline into a new
venv using the existing host tool, without global installation or configuration
changes. Initial Sigstore root 10 is commit-pinned at
`03f9c7e0023c917b60eb7431e87f47e6a636f37a` and SHA-256
`836bff947925edfc23eb9ce17af66fb1e43bb5e2bdd240520985ae52b585eae9`.
This is the official-docs/TLS bootstrap, not independent signing-ceremony or
PyPI-publisher authentication. TUF refresh must reach currently valid signed
root/timestamp/snapshot/targets and verify artifact.pub and trusted_root.json.

Only exact Cosign v3.1.3 linux-amd64 assets are downloaded over HTTPS with
time/size/hash bounds. OpenSSL must verify the TUF artifact-key signature before
the new Cosign binary executes. Modern KMS and keyless bundles are then verified
offline with the TUF trusted root, exact identity
`keyless@projectsigstore.iam.gserviceaccount.com` and issuer
`https://accounts.google.com`; no insecure or identity-regex flags are allowed.
Any ephemeral verifier container uses the existing cached Restic config identity
`sha256:136600b6ff6843d61d355f7f71f460a166429f35de6fd11b568fece3c9a4d510`,
network none, read-only public mounts, no host secret mounts and no daemon socket.
Downloaded code never replaces a host/service binary. Failed owned attempts and
redacted receipts are preserved; only their exact owned containers may be
removed. This does not authenticate the current Cosign container pin, other
scanners, root service artifacts, compatibility, deployment or recovery.
Independent security review supplied the fail-closed sequence. At authorization
time, actual results were `NOT_RUN`; the later public-only observation below
supersedes that statement for the Cosign release bootstrap alone.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0009 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0009 | ready | in-progress | #sec01-received-handoff |
| SPEC-0204 | blocked | in-progress | #sec01-received-handoff |
| SPEC-0204-PLAN-0001 | blocked | in-progress | #sec01-received-handoff |

### SEC01 Received Handoff

The branch reported source/unit/static/isolated receipts for OpenBao issuance
(36 tests, 92-percent helper coverage), workflow bundle (8 tests), supply-chain
gates (71 tests), version contracts and isolated OpenBao rehearsal (2 tests,
177.078 seconds). These receipts are attributed to the handoff's recorded
inputs, not latest-main or production acceptance. The historical common
validator suite was 20 PASS/2 FAIL, the script manifest had two missing records,
both stable/security evidence gates exited 2 as `BLOCKED_EVIDENCE`, and the
changed local gate failed six shared assertions. Those failures remain the
repair boundary until coordinator-owned current-main checks prove otherwise.

On current `e93e0c8223191bf26aea7578a231b2dbf016fc7c` plus the coordinator
integration input, both gate CLIs again exited 2. The latest gate reported
`ready=false`, no missing or unexpected services, `deployed=false` and
`externalfacts=false`; the security gate reported `ledger_complete=false`,
`coverage_checked=true`, 124 observed `blocked-evidence` entries and no missing
or unexpected services. Both bind root input manifest SHA-256
`3a2e7451e6211b43b9d8f9c9760fed0fcf5cdac381e45e1b2323628b60756f66`.
The observed 124 is a receipt, not an inventory constant. An earlier root
aggregate failed four manifest assertions while interpreting authority; retain
that historical failure rather than presenting all aggregate QA as PASS.

PR #416 candidate-quality failed on service-inventory Airflow Env drift. Its
proposal may be reviewed against current main, but apply-check or in-memory
rehearsal is not a shared-suite PASS. The GoTrue v2.197.0 image contract is
read-only input for SMTP01; SEC01 neither converts SMTP secrets nor implements
a native `_FILE` adapter.

### Coordinator Common Repair Receipt

The coordinator used a dedicated `codex/sec01-integration` worktree on
`e93e0c8223191bf26aea7578a231b2dbf016fc7c`; other sessions' worktrees and dirty
root files were untouched. The validator proposal was reviewed and applied to
its two target tests. The existing inventory renderer supplied only the seven
current Airflow Env-cell changes; dated historical inventory stayed unchanged.
The two existing supply-chain libraries were registered under their durable
security-updates README authority, without changing their bytes or weakening
manifest validators. Initial Task-authority/README-consumer registration failed
four assertions; corrected durable ownership and direct consumers passed.

Before repair, the runtime/wiring command ran 30 tests with four failures,
exit 1. After repair, the same suite passed 30 tests; ServiceInventoryTests
passed 15; script-manifest regressions passed 48. The coordinator replay of
all four modules ran 93 tests, exit 0 (18.000 seconds). Manifest/generated
checker and operations-catalog checker also exited 0. Runtime validator hash
is `48ccd21370d2b6557a7dccbe0d9a4ac02143786d21aef955f1a89272fb3e1950`;
wiring validator is `9b61ab1b64399f62d28e261a3da10bf71f55bc69860cca57cba345ca63873870`;
inventory is `8535b63b85068a185cc59646e932e47c67689cbd72563adaa811756c62502951`.

The received SEC regressions were absent from the hosted candidate leafs.
A new routing regression first failed seven assertions, exit 1. The coordinator
registered offline issuance/trust, candidate expiry, version and workflow bundle
selectors in the required Compose leaf and update-gate negatives in the
supply-chain fixture leaf. Native selectors remain separately opt-in; selecting
only offline classes cannot imply native PASS. A first root-rule attempt used
non-optional roots and failed schema checks; those invalid root rules were
removed, preserving the existing operations aggregate owners. Routing plus
workflow-contract regressions then passed 39 tests, exit 0, and
`check-github-workflow-contract.py` exited 0. A guessed nonexistent checker
filename exited 2 before the correct registered checker was used; this is a
command-selection error, not a product regression.

Fresh public-source CLI evaluation used `update-ledger.json` for both
`latest_version_gate` and `security_update_gate`. Both exited 2: latest
`ready=false`, security `ledger_complete=false`, no missing/unexpected source
services, `deployed=false` and `verified_external_facts=false`. Source input
manifest SHA is `3a2e7451e6211b43b9d8f9c9760fed0fcf5cdac381e45e1b2323628b60756f66`.
The observed 124 rows are a result, never a service-count constant. Field/coverage
checks do not verify supplier releases, scans, live compatibility or recovery.
Criterion 15 remains pending; a source repair merge cannot close SEC01.

### Candidate Image Grammar Repair

PR #418 head `3f6aa5e8d4b09d8d270166a19587884ee0612445` failed
candidate-quality run `38056697221` at Tier01 with `invalid compose service
image contract`. The existing parser accepted either tag or digest and rejected
valid `tag@sha256` references. The one-line grammar repair makes the constrained
tag and exact lowercase SHA-256 digest independently optional while preserving
full matching, 255-character bounds and safe YAML parsing. Two new regression
assertions failed before repair; the repaired full version-contract module
passed 49 tests. The actual `01-gateway` hardening check, shell syntax, Ruff
and diff checks passed. Independent code and security reviews found no P1/P2.

Frozen hardening hash is
`068a87dc1cb2c6afb937602f4497c3c467a91d588684aa1be081b925058f702c`;
test hash is `ff6629f6e8a80987c74da9572107c3054c95965f5ae4721ba44c4a64f77cc76b`.
These are offline/source checks. Hosted CI at the new committed head remains
required; run `38056697221` remains a FAIL receipt, not accepted delivery. No
image deployment or HOME verification occurred.

### Delivered Common Repair and Module Registration Follow-up

GitHub confirmed PR #418 merged by the repository owner at
`80c31405df7983dc4b7d8ad8823f73323247d264` on 2026-10-10 14:17:16 UTC.
Its head `d0d15c0662139cb34bbeb7ad1a65e2dc52b719d9` passed hosted
candidate-quality run `38058055919`, CodeQL and GitGuardian. This records
external delivery of the bounded common repair, not SEC01 global completion.

A separate full-profile ownership replay ran seven tests with one FAIL: the
new required class selectors appeared as classes rather than reachable modules.
The coordinator replaces those selectors with their complete containing modules,
each once, and allows skips only for `CandidateNative` and
`WorkflowCandidateRehearsalTests`. Existing expiry and workflow-source tests
remain required; native flags remain explicit opt-ins. The ownership validator
is unchanged. Tests-only RED failed five assertions; the corrected ownership
suite passed seven tests and workflow/routing passed 40 in that initial freeze.
Those receipts were superseded when independent code review reproduced duplicate
native skip receipts: the candidate module exposed an imported foreign TestCase.
The canonical adapter rejected them with `ci-gate-adapter-tests-skipped`, exit 2
(outer regression exit 1; 13 tests, six skips).

The candidate now imports the rehearsal module rather than exposing its TestCase;
two existing references preserve native behavior. The bounded 60-second canonical
adapter regression passed after this correction. Replacement workflow/routing
passed 41 tests; offline modules passed 12 with five expected native skips,
without duplicate receipts. The routing module passed five tests again after
the timeout was added. These are source/unit results, not native verification.
The intermediate duplicate class/module registration failed ownership and was
removed, rather than weakening the invariant. Hosted CI on the follow-up head
remains required. No HOME, deployment or private resource action occurred.

### Full-security continuation — 2026-10-11 KST

The user authorized full SEC security, native HOME and recovery continuation;
this does not remove a target, review or recovery boundary. Current main is
`abe2`, this Task worktree is `caabcfacd`, and PR #419 was externally merged at
`a42` after candidate success. SMTP #413 (`06a5`) merged at `34c` and P09 #417
(`0e696`) merged at `abe2`, but their candidate failures remain under root
repair. Earlier source/input SHAs remain historical inputs, not a claim that
current HEAD is freshly approved.

Read-only runtime observation found 63 root containers: 59 running, four
exited, 57 healthy, one Pyroscope unhealthy and five without health status.
Fourteen references differ across six image identities: Airflow 3.3.1→3.3.2
(six services), n8n/workers/runners 2.41.6→2.42.6, Grafana 13.2.2→13.2.3,
Ollama 0.40.0→0.40.2 and OpenBao/Agent 2.6.2→2.7.1. This is observation, not
deployment or compatibility PASS. Tool pins name Syft 1.54.1, Grype 0.120.1,
Cosign 3.1.3 (addressing GHSA-fx35-mq7g-6g98 through 3.1.2), and Scorecard
5.5.0 unchanged. Fresh local cache inspections found all four current pins
absent (exit 1 each). Separate read-only remote imagetools metadata lookups
succeeded (exit 0 each) and recorded linux/amd64 manifest digests. No image
pull, publisher trust verification, signature verification, SBOM or scan ran.

Registry SHA-256 is `91b114514954245c484454f2e5e45c0874e4596b3a6a1871fbd7c0de12ed3c33`;
readiness root SHA-256 is `2d468beab138e4017bbba0198a31819f2ed7aa2ec40c2f991b68e329d8631069`,
with local-cache absence and successful remote metadata recorded separately,
and superseded history preserved. Old-pin RED had one failure/three
sub-failures, then 105 PASS in 4.342 seconds. Projection-readiness RED failed
the checksum-consistency regression before the projection correction; the
final focused source suite passed 106 tests in 4.865 seconds. Full gates report 124
rows: 43 ready, 81 unresolved; latest exit 2 and security all-124 blocked exit
2. Inventory has 45 entries and manifest SHA
`3a2e7451e6211b43b9d8f9c9760fed0fcf5cdac381e45e1b2323628b60756f66`, with no
missing/unexpected entries. Sixty-eight direct references plus 21 Compose-path
builds yield at most 89 pre-dedup artifacts, a receipt rather than a count
contract.

Capacity observation reports 54 GB root free and Docker image/container/volume/
build-cache use 92.1/0.639/33.09/30.17 GB; no prune ran. Public sanitized
capsule `/tmp/sec01-runtime-matrix.json` has SHA-256
`8c7db527c38516bee6a444ee4a5ac9f4214118e57ba9c5ba932c48fa2a544ece` and no
secret. Encrypted-host-Restic `check --read-data` passed, but its 2026-10-08
snapshot is stale. Actual backup failed due to absent OpenBao snapshot token
file and exceeded state budget; raw journal output is not recorded. Existing
OpenBao role/token, unseal/offsite custody and recovery remain `NOT_RUN`; no
secret was exposed or rotated.

Next executable work is bounded: the public Cosign release bootstrap below is
complete, then bounded fetch/build, SBOM and offline Grype scan with known
database; assess
remaining primary stable/advisory/source/current-container compatibility and
backups; perform isolated restore before per-service HOME deployment. ROOT-wide
operational acceptance remains `NOT_RUN`; this Task is not complete.

### Public Cosign Bootstrap Receipt — 2026-10-11

These are public-tool receipts from owned temporary directories, with no global
setting, service, private value or OCI image change. The first `ensurepip` venv
attempt failed (exit 1). A second attempt failed (exit 1) because `uv` received
mutually exclusive flags; its underlying offline install exited 2. Those
failures are preserved in
`/tmp/hy-home-sec01-trust.k2l4wmpe/failed-receipt.json` and
`/tmp/hy-home-sec01-trust.edbraubz/failed-receipt.json`; Cosign did not execute
in either attempt.

The third attempt used uv 0.12.18 and installed these exact offline wheels,
each with its observed SHA-256:

- `tuf-7.0.1-py3-none-any.whl` — `d30434bda6e079ab303fb30d1b3006d939a10ca34783b1573d61cd9b802fa45c`
- `securesystemslib-1.5.1-py3-none-any.whl` — `ada8bdf817da29ece4ba91654f6a162ce7cfbadbc3ae3f840f7313f9d22675de`
- `cryptography-50.0.2-cp311-abi3-manylinux_2_34_x86_64.whl` — `9dab55f57c74c3cad24c323bacbbd04be4705ba6eb0d92e920b1fc4837ed5079`
- `urllib3-2.8.0-py3-none-any.whl` — `0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3`
- `cffi-2.1.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` — `c1453022f490d2459a11819d83ad1d586e9ff65a12ac3e705ffebd46d3685dcf`
- `pycparser-3.11-py3-none-any.whl` — `51d5a8ba2be0bbe440b99d2112604c95bbbc3c2748a64260186c541e1729cd80`

That preparation exited 0 and did not execute Cosign. It retained the official
docs/TLS root-10 anchor at commit
`03f9c7e0023c917b60eb7431e87f47e6a636f37a`; `10.root.json` SHA-256 is
`836bff947925edfc23eb9ce17af66fb1e43bb5e2bdd240520985ae52b585eae9`.
The authenticated public TUF refresh advanced root 10 to 15 and verified
timestamp 804, snapshot 166 and targets 14 within their recorded expiry
windows. It produced `artifact.pub` SHA-256
`59ebf97a9850aecec4bc39c1f5c1dc46e6490a6b5fd2a6cacdcac0c3a6fc4cbf` and
`trusted_root.json` SHA-256
`6494e21ea73fa7ee769f85f57d5a3e6a08725eae1e38c755fc3517c9e6bc0b66`.

The release sequence used `.agent-work/bootstrap-cosign.py`,
`.agent-work/refresh-cosign-trust.py`,
`.agent-work/verify-cosign-release-openssl.py` and
`.agent-work/verify-cosign-release-offline.py`. For v3.1.3 it verified with
OpenSSL before executing Cosign these three exact assets: `cosign-linux-amd64`
(141,178,250 bytes, SHA-256
`4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71`),
`cosign-linux-amd64-kms.sigstore.json` (3,618 bytes, SHA-256
`9c0e569b65883ac5ccf6e079989355832a3ee083b8cb991b3482d963e97896d9`) and
`cosign-linux-amd64.sigstore.json` (6,406 bytes, SHA-256
`e16547fbee348eb23bd7e5a4d542b540395faea2e7bb1d18da01bbc3cc74d57d`).
OpenSSL exited 0. The cached utility verifier then ran with network none and
config identity `sha256:136600b6ff6843d61d355f7f71f460a166429f35de6fd11b568fece3c9a4d510`:
modern-KMS verification and keyless verification with the exact configured
identity/issuer both exited 0, followed by `cosign version --json` exit 0.

The observed receipts are
`prepare-receipt.json`, `tuf-refresh-receipt.json`,
`openssl-release-receipt.json` and `offline-release-receipt.json` under
`/tmp/hy-home-sec01-trust.g059chnr`. They prove only authentication of the
public v3.1.3 release binary in the bounded verifier. OCI image verification,
SBOM, Grype, advisory remediation, deployment, native HOME security and
recovery remain `NOT_RUN`.

### Next Authenticated Binary Boundary

Before any new tool binary executes, the operator records current root metadata
and refreshes it when stale. The three OCI authentication commands use public
default-bridge egress, which can reach the Docker gateway/host, routable
LAN/RFC1918 networks and the Internet. Expected registry/OAuth/TLS destinations
are determined by authenticated Cosign; no network-enforced destination allowlist
is present. The coordinator accepts this bounded residual for the three fixed
public digest verification commands because the latest authenticated executable
receives no private configuration, credentials, daemon socket or service data,
uses fixed exact publisher identities/claims and runs under the stated limits.
This acceptance never permits an explicit private-service API action. The two checksum-bundle
commands use network none. No verifier mounts host configuration, credentials,
daemon socket or service data. This public-egress phase is distinct from the completed offline bootstrap,
whose verifier network was none.

Cosign OCI verification must authenticate the GCR index through both configured
paths: the Google keyless identity and the source-commit-pinned
`release-cosign.pub` KMS annotations `GIT_HASH=11926fa5bbbbde47e88fc006b625a17769b743b2`
and `GIT_VERSION=v3.1.3`. Scorecard must bind the exact GitHub publish-image
workflow identity for tag `v5.5.0`. Syft and Grype do not gain OCI
authentication from an unsigned image. Their only narrow fallback is
`BINARY_RELEASE_CHECKSUM_AUTH`: authenticate the publisher checksum/bundle,
download a bounded public archive, accept only the expected basename, require a
static ELF64 x86_64 binary with no `PT_INTERP`, set temporary mode 0500, and run
only an isolated version check. The exact release assets, metadata SHA-256 and
source URLs are input contracts that root must revalidate before execution; no
new successful asset verification is claimed here.

Use only the exact reviewed `/usr/bin/docker` binary and explicit local Unix
daemon socket, a new empty mode-0700 client config and a minimal subprocess
environment. Ignore inherited Docker host/context/config/TLS credential settings.
Bind and recheck daemon identity; capture each owned container ID before start
and use that exact ID for cleanup. Each command has a 150-second limit, one CPU,
512 MiB memory, 32 PIDs, read-only rootfs and public proof mounts, dropped caps,
no-new-privileges and private 16-MiB noexec tmpfs. The five commands share an
8-MiB aggregate output limit. The scheduling deadline is 900 seconds with a fixed
120-second cleanup grace plus a separate fixed 10-second final reap allowance,
for an absolute 1,030-second maximum; every allowance and observed duration must be
recorded in the reviewed operator and actual receipt, never omitted from the
maximum. Reject image-declared volumes and any unexpected created mount; cleanup
is limited to exact owned container IDs, including their owned anonymous volumes. Privately retain raw public output and write an
exclusive immutable sanitized success or failure receipt, including bounded
stop/kill/remove cleanup status. Bind the exact earlier bootstrap and asset
receipt bytes and expected record set before execution; `--offline` is embedded
bundle verification, not a live Rekor observation. The default bridge retains the
explicit host/private-network reachability residual described above.

This scope includes only the five exact publisher checks and authenticated
release extraction/version checks. It includes no SMTP or live-service action,
deployment, SBOM, Grype database refresh or advisory remediation. All resulting
OCI/binary authentication outcomes remain `NOT_RUN` until actual receipts; HOME
operation and recovery are separate execution units.

### Public Tool Publisher Authentication Receipt

On 2026-10-10 from 17:13:27.682304Z to 17:14:17.292352Z, the coordinator
executed `/tmp/hy-home-p09-qa/bin/python -B .agent-work/verify-public-tool-publishers.py`
from the isolated SEC01 integration worktree. The independently reviewed operator
SHA-256 was `ccc247414c4725ee1b761c94d44abbc90a324b2fa55cba634b5eea08755c15dd`;
its 24 synthetic tests passed separately. The actual command returned exit 0
in 49.610 seconds. The exclusive mode-0400 public receipt at
`/tmp/hy-home-sec01-scanners.xrq5we4j/publisher-verification-receipt.json` has
SHA-256 `726ecc1afe545da3a4565bd4156ae71c64bf1f0d01b34af600533c7d3a1ce2c1`.

| Check | Actual container exit | Docker client exit | Duration seconds | Result |
| --- | --- | --- | --- | --- |
| Cosign exact GCR digest, keyless Google identity | 0 | 0 | 10.978 | PASS |
| Cosign same GCR digest, pinned release KMS public key | 0 | 0 | 10.953 | PASS |
| Scorecard exact GHCR digest, pinned GitHub release workflow identity | 0 | 0 | 4.199 | PASS |
| Syft release checksum bundle, pinned GitHub release workflow identity | 0 | 0 | 1.426 | PASS |
| Grype release checksum bundle, pinned GitHub release workflow identity | 0 | 0 | 1.907 | PASS |

All five exact owned container IDs were confirmed absent after cleanup. Public
raw output remains in the private scratch directory. This evidence authenticates
the two stated OCI subjects and the two binary checksum releases; it does not
certify unsigned Anchore OCI images, extract or execute Syft/Grype binaries,
refresh the vulnerability database, scan service images, deploy services, or
prove HOME operation or recovery. Those actions remain `NOT_RUN`.

### Authenticated Scanner Extraction and Native Version Receipt

The coordinator executed `/tmp/hy-home-p09-qa/bin/python -B .agent-work/extract-authenticated-scanners.py`
on 2026-10-10 from 17:28:31.606305Z to 17:28:43.432813Z. The reviewed operator
SHA-256 was `0f7e574847d9695737a570d85888f92d581220c6198f218048584469747a1efd`;
22 synthetic tests passed separately. The actual command returned exit 0 in
11.827 seconds. Its immutable public receipt SHA-256 is
`1712a043e18898ea2e9ab103a7b36dbd77e31b5463b26978c3dee0b8b3d20712`.

The exact authenticated archive hashes and single binary hashes, ELF constraints,
source commit identities, full sanitized publisher and scanner receipts are
preserved in `infra/09-platform-ops/security-updates/tool-readiness.json`.
Syft 1.54.1 at `b254e6d92f28c3868a755f62fb3ca8f26e9fee76` and Grype 0.120.1
at `6f8d854af29d3a3086b11a84afa51554a2a245fe` each passed `version -o json`
with the exact application/version/gitCommit and linux/amd64 platform. Both
actual container and client exits were 0 and both exact owned IDs were removed.
Execution used network none, one read-only public binary mount and the bounded
utility contract above. There was no global install, database refresh, SBOM/CVE
scan, service rollout, secret operation or recovery. Anchore OCI images remain
unsigned and are not certified by these binary-release receipts.

## Evidence

The following table preserves the as-received source-only slice and earlier
coordinator repair inputs. It is historical; the current authorized continuation
and its later observations are recorded above.

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SEC01 source and isolated receipts | 15 | W31 | Received six-commit source, focused tests and isolated rehearsal | Recorded branch/input hashes in integration handoff | PASS | security-updates handoff | pending |
| Common validator and manifest state | 15 | W31 | Current shared suite and manifest registration | 20 PASS/2 FAIL; two records missing | FAIL | integration handoff | pending |
| Latest/security evidence gates | 15 | W31 | Current root-bound stable and security gate commands | Both `BLOCKED_EVIDENCE`, exit 2; latest `ready=false`, security `ledger_complete=false`; manifest SHA recorded above | DEFER | SEC01 received handoff | pending |
| PR #416 candidate CI | 15 | W31 | candidate-quality, CodeQL, GitGuardian and main-security | Run `38052766613`; candidate-quality failed | FAIL | PR #416 handoff | pending |
| Coordinator shared repair | 15 | W31 | Runtime/wiring, inventory, manifest and candidate regression registration | e93e0c822 plus reviewed integration; 93 and 39 tests exit 0 | PASS | #coordinator-common-repair-receipt | pending |
| Public Cosign release bootstrap | 15 | W31 | Offline wheel preparation, TUF refresh, OpenSSL-before-execution, KMS/keyless verification and version | Public receipts under `/tmp/hy-home-sec01-trust.*`; bounded public v3.1.3 binary only | PASS | Public Cosign Bootstrap Receipt | pending |
| Public tool publisher checks | 15 | W31 | Two exact OCI subjects and Syft/Grype release checksum authentication | Five actual exits 0; reviewed operator and immutable receipt recorded above | PASS | Public Tool Publisher Authentication Receipt | pending |
| Authenticated scanner versions | 15 | W31 | Exact authenticated archive extraction and isolated version-only execution | Syft/Grype exact version/source/platform, client and container exits 0; 11.827 seconds | PASS | Authenticated Scanner Extraction and Native Version Receipt | pending |
| HOME, migration, rotation and recovery | 15 | W31 | Initial source-only slice had no operational authorization; later direct authorization covers bounded continuation | Exact per-target execution and acceptance remain pending; read-only observations are recorded above | NOT_RUN | Current TSK-0009 and per-operation contracts | pending |

## Review and Completion

Before delivery, integrate only reviewed common changes through their assigned
single writer; regenerate the version projection after preceding SMTP/CLN work;
run the registered changed gate, current common validator/inventory/manifest
checks, both latest/security gates and latest-head CI. Require independent
security and code review at that head. Preserve failed and blocked receipts.
Source rollback is a logical revert of owning commits; HOME rollback requires a
separately approved pre-upgrade backup and recovery proof.

`SOURCE`, `UNIT`, `STATIC` and `ISOLATED` remain distinct from `HOME`,
`MIGRATION`, `ROTATION`, `RECOVERY` and `DELIVERY`. The latter lanes are not
accepted by this Task's received evidence.

## Related Documents

- [SPEC-0204](../spec.md)
- [SPEC-0204 Plan](../plan.md)
- [Security updates ledger](../../../../infra/09-platform-ops/security-updates/README.md)
- [Platform Operations](../../../../infra/09-platform-ops/README.md)
