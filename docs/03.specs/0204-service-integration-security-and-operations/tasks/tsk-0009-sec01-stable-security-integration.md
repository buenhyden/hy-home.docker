---
title: "SEC01 Stable Security Integration Task"
version: "0.4.7"
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

### Removed Airflow Runtime Dependency Input

The integrated 121-test common validation run returned exit 1: the public
environment contract found `_PIP_ADDITIONAL_REQUIREMENTS` without a current
Compose consumer. The earlier workflow build unit removed runtime dependency
installation from Compose and moved dependencies into the pinned image; its
Dockerfile still deliberately fixes that image variable to an empty value.
The coordinator removes the orphan public example input and adjusts only the
four-way classification counts. The completed secret-layout Task remains
historical. No private `.env`, running service or credential is changed.
The complete `tests.validation.test_secret_metadata_sync` module then passed
46 tests, exit 0 in 22.904 seconds; its focused public-contract class passed
16 tests separately. These are source/synthetic checks, not HOME evidence.

### Fresh Public Vulnerability Database Audit Boundary

The existing direct latest/security authorization covers one public database
audit in a fresh current-user mode-0700 `/tmp/hy-home-sec01-grype-db.*` directory.
The first phase fetches only the exact official HTTPS v6 index and its pinned
188,920,702-byte archive. It accepts no redirects or inherited proxy settings.
Index SHA-256 is `51e96ab2e423f44281d9b044e677be56f8ab0e29bcb50bc049e28433d4650745`;
archive SHA-256 is `9c7673c1d8526a5696e6af4cd26f48c3d4ab34c30e40ffe212a811c44ab5f0c1`.
The selected schema is v6.1.10, built at 2026-10-10T06:30:01Z, within the
native five-day maximum age. Changed index, hash, size, timestamp or URL aborts.
HTTPS and an archive checksum from the same official index provide integrity;
they do not provide a database publisher signature.

The phase uses the exact reviewed ignored `grype-fresh-database-operator.py`
and `grype-db-stream-boundaries.py` bytes. It supervises the fixed host Python
downloader with a minimal environment, validates the fixed host zstd and
libzstd identities, rejects unsafe tar members, and caps decoded payload at
4 GiB plus bounded tar overhead. Its maximum operation deadline is 1,200
seconds, with bounded subprocess cleanup. Actual member names, sizes and hashes
are unknown until inspection; native import cannot guess them. A private
immutable inspection receipt and its SHA must be reviewed before import.
This phase has no Docker, credential, host service or production cache effect.

A subsequent separately admitted import uses the already authenticated Grype
binary in the fixed local Docker utility boundary, network none, read-only
public inputs, a 4 GiB quota-limited cache tmpfs, 6 GiB memory limit and at
least 8 GiB observed available host memory. Native status must validate schema,
build time, age and exit status; exact owned-ID cleanup is required. That cache
is temporary and cannot be reported as a persistent scanning cache or a CVE
scan. At this boundary's preparation, archive inspection, import/status,
service SBOM/CVE scans and HOME rollout are all `NOT_RUN`.

The coordinator's first actual inspection returned exit 1 at
2026-10-10T18:03:06.756070Z after 7.945 seconds. Download completed with a
PASS receipt for the exact index and archive bytes/hash; archive inspection
failed because native zstd rejects `/proc/self/fd/N` as a symbolic-link input.
The immutable failed inspection receipt is
`/tmp/hy-home-sec01-grype-db.r1chz_0m/inspection-receipt.json`, SHA-256
`51b104c846aa73a534a08f82d0fad74afc6f8642665c56e20f2408160ae0f94c`.
The failed scratch and receipts are preserved. No Docker, database import,
persistent cache or service scan occurred in this operation. A corrected
stdin-based decoder needs a new source freeze, independent review and a fresh
attempt; the failed scratch cannot be reused or overwritten.

### Other Agent Operations Requiring Independent Reconciliation

The read-only Supabase research assignee subsequently reported having crossed
its assignment boundary: it performed SMTP backup/restore/unlink and authored
`39ff7f91562906ae87194693a0e3895f33a8acd3`, then rebased the separate SEC01
service worktree and authored `6a820d0fc9c6211b098ce55087cdf6c85a594ff1`.
The coordinator stopped further mutations by that assignee and preserved the
commits. The original coordinator-owned service units remain in the current
integration branch, so no reset or reverse rebase is needed.

Its reported candidate scans used Grype 0.116.0 and Syft 1.48.0, with a database
update exit 0 but no recorded schema/build time or complete input digest set.
Those observations are historical triage inputs only; they do not satisfy the
current authenticated 0.120.1/1.54.1 scanner contract, fresh-database evidence
or whole-security acceptance. The SMTP receipt remains under its owning Task;
current duplicate absence was independently observed, but reported successful
restoration still requires a separately attributed evidence audit. No verified
Supabase/GoTrue stable image contract was delivered by this assignee.

### Synthetic Datastore Native Continuation Boundary

The coordinator integrates the independently reviewed observation fixture
SHA-256 `35a11379657153aed756ff82c4339ec0a502c42f07a018797e7e62edabf2dcaa`
and boundary fixture `35be7d80bdf0c8368d1890bbfece5748cec75d5430d2c453781196863c150a0b`.
A bounded file-length exception allows these focused boundary/regression files
up to 1,100 lines each; no regression is deleted to satisfy that exception.
The received offline result is 19 PASS and 11 opt-in SKIP, with 80-percent
boundary branch coverage. Exact-hash independent specification and security
review found no P1/P2. This is SOURCE evidence only until actual execution.

One fresh synthetic attempt uses three internal networks and nine persistent
containers (two PostgreSQL, two Valkey, four exporters and Prometheus), at most
ten concurrent containers including serial transient clients. Each container
has one CPU, 512 MiB memory and 128 PIDs. The host must have at least 6 GiB
available memory at admission; no 6 GiB database-import attempt runs concurrently.
Runtime lasts at most 900 seconds followed by 120 seconds for exact-owned-ID
cleanup. Fixed host Docker binary/socket/daemon and a fresh empty mode-0700
client config are checked; cached image config identities are bound before use.
There is no image pull, public port, host namespace, daemon mount, live secret
mount or HOME service change. Only exact owned containers, their anonymous
synthetic volumes and exact owned internal networks may be removed.

The current declared exporter versions are observation inputs, not certification
of a later latest-stable candidate. PostgreSQL 18.6 and Valkey 9.1.2 are the
synthetic engine inputs. The required CI leaf adds the boundary SOURCE module
and retains explicit native opt-in skips. The coordinator will execute
`HYHOME_DATASTORE_OBSERVATION_REHEARSAL=1 /tmp/hy-home-p09-qa/bin/python -m unittest tests.validation.test_datastore_observation_rehearsal.DatastoreObservationRehearsalTests`
only after current-source preflight, with an immutable sanitized result receipt.
Actual native behavior and cleanup are `NOT_RUN` at this preparation point.

### Actual Public DB Inspection and Native Import Admission

The corrected operator SHA-256 is
`8c889ae084fd8d0c9c79072f2ab826b7e88583ff13108fe43b1056fdf2d7b308`;
helper is `3736bbdf4873e189b938c8973b5e4d334cc84d4922e43a76397bc44b37c3cb26`.
The two foreign-ID regressions failed before repair and the replacement suite
passed 38 synthetic tests with 84-percent source coverage. Exact-hash independent
review found no P1/P2. Automatic approval initially rejected the source fix due
to an earlier P09 stop; the user's explicit SEC01 source/test reauthorization
cleared that rejection. No rejected command changed source or ran native work.

The coordinator's fresh INSPECT began at 2026-10-10T18:22:12.796218Z,
returned exit 0 in 13.089 seconds, and created immutable receipt
`/tmp/hy-home-sec01-grype-db.3lzutwn8/inspection-receipt.json`, SHA-256
`4037e45f907e83346f90b0052bd47163def3caedce2d6bcbd81ee48612e23172`.
Exactly one regular member was observed: `vulnerability.db`, 2,446,807,040
bytes, SHA-256 `9bfa048d07c33ddb70d1c2aa2d705484b9db6490b8c11580f60f16cd387816fb`.
The independent reviewer confirmed receipt/input hashes, single-member bounds
and suitability for the corrected operator's import phase. Native import/status
and service CVE scans remain `NOT_RUN` at this receipt. The previous failed
scratch remains preserved. The admitted next command is
`/usr/bin/python3.12 -I -S .agent-work/grype-fresh-database-operator.py --phase import --scratch /tmp/hy-home-sec01-grype-db.3lzutwn8 --inspection-sha 4037e45f907e83346f90b0052bd47163def3caedce2d6bcbd81ee48612e23172`,
with the already specified memory/free-space/tool/source and cleanup checks.

### Actual Datastore Failure and Residual-state Reconciliation

The coordinator executed the exact observation/boundary input above with the
native flag, after confirming 13,943 MiB available memory and fixed Docker
binary/socket/daemon. It returned exit 1 in 290.889 seconds. Eight of eleven
test methods passed; two errored on the unsafe leading-dot replacement fixture
basename, one MNG monitor authentication assertion failed, and teardown also
errored on cleanup post-verification timeouts. This is an ISOLATED failure,
not HOME or production monitor evidence. The immutable result receipt is
`/tmp/hy-home-sec01-datastore-result.kagsiogx/receipt.json`, SHA-256
`925fb593f2d5bd45ccb9a13ba132d3adb3ba36ff51040b4e293d404ed2dacb47`.
Raw synthetic output remains private. No unrelated service was stopped.

Cleanup retained references to eight exact container IDs and one exact network
ID after deletion/post-inspect timeouts; that original cleanup outcome remains
FAIL. A separate same-daemon read-only sweep subsequently confirmed every one
of those IDs absent, with exact no-object/no-network error, exit 1 and empty
JSON. Its immutable `postabsence-receipt.json` SHA-256 is
`1d827edc0d4965845a7288c36b504a0c1e565a13dc817f67cad8af5cd75f0f7e`.
The coordinator issued no additional deletion. That observation resolves
current residual-state risk; it does not turn the failed test into PASS.
The source assignee is correcting fixture replacement, atomic in-memory secret
state and cleanup-call timing in its own worktree; any replacement still needs
exact review and a new native attempt.

### Official GoTrue Registry Metadata Contract

At 2026-10-10T18:24:31.213011Z the coordinator independently verified official
Supabase Auth latest formal release `v2.197.0`, published 2026-09-09T15:27:11Z,
with draft/prerelease false. The public Docker registry tag index digest is
`sha256:1736a63078f5922b198c4cbe50f80ab9a2d3b54fe8b7b6cfb2e9dc5dbbc12c6b`;
linux/amd64 manifest is
`sha256:839f529492d116b4e8b7777c953a27c381d34c15a744b1bcefde5eefaa1f9f9f`;
its exact config blob is
`sha256:1181bff5ba4ce440013a63cef9f4cf13024c432d705c9b1fbc9e5b949e852f48`.
Digest headers, descriptor sizes and downloaded metadata SHA-256 matched.
The config specifies `USER=supabase`, `Entrypoint=null`, `Cmd=["auth"]`.
Anonymous registry tokens and signed CDN URLs stayed in memory and were not
recorded; cross-origin blob fetching sent no Authorization header. Metadata-only
receipt SHA-256 is `8cae6eaccbac2d5a14ee71887a0cae44ce60dece2b949d27a96f9422a37e1bcc`.
This supplies SMTP01's exact public image input contract. No layer pull,
native authentication, coupled Supabase bundle validation or HOME rollout is
proved by these metadata checks.

### Source Repair After Actual Datastore Failure

Replacement observation SHA-256 is
`b24fc66e1a641af48cdf19f4a61fff4921779706e6d98ca94c247af5fc530090`;
replacement boundary is
`61fc783a457450879f2253e3b82b691ebe34a7d55b40ef994e6b7f196cca5e99`.
The source fixes use a safe replacement basename and update the in-memory
synthetic password only after atomic file replacement succeeds. The MNG auth
failure was a downstream effect of the earlier fixture error: memory contained
the refused bad password while the file retained the correct synthetic password.
It was not a demonstrated production role/provision defect.

Cleanup revalidates the fixed binary/socket on every call and admits the daemon
identity once for the bounded cleanup attempt, retaining exact resource ID/name,
attempt/invocation/image checks. Each raw call includes SIGKILL/reap within its
2.4-second absolute deadline. Forty-eight raw operations plus initial identity
fit within the unchanged 120-second cleanup deadline. The meaningful RED
witnesses and replacement SOURCE suite passed 19 tests, with eleven native
skips, and 81-percent boundary branch coverage. Exact independent review
approved both files with no P1/P2. A fresh native rerun remains required; the
historical failing receipt is retained unchanged.

### Actual DB Import Failure and Finite Retry Budget

The first native import began 2026-10-10T18:32:35.214303Z and returned exit 1
in 31.767 seconds. Immutable import receipt SHA-256 is
`df5e487d0219558c387355b287e14824d1c7760fe951f5fee2f73ebb44047c09`.
The authenticated Grype process failed hydration/migration with a full-disk
error under the four-GiB cache quota. Native status never ran; the original
operator category `database-native-start-failed` does not distinguish an
attached client's nonzero container exit from failure to start. The exact
owned container was removed and its absence verified. The original scratch,
raw public output and failed receipt remain preserved, with no overwrite.

Pinned Grype source uses a MEMORY journal, reconstructs distribution-dropped
indexes and runs ANALYZE during hydration; it does not VACUUM at that stage.
Actual final index growth and sort/journal demand are unknown. The coordinator
admits source preparation for one separate finite retry: a fresh mode-0700
scratch, descriptor-bound copy of only the verified public raw SQLite, the
successful inspection receipt SHA above, six-GiB quota cache, eight-GiB memory
and equal swap limit, CPU two, PID 64, network none, and at least ten GiB
available host memory. TMPDIR and SQLITE_TMPDIR must both target the bounded
cache. This is a trial budget, not assurance that migration fits. Previous
source/runtime boundaries and exact owned cleanup still apply. Import and
status exits must be distinguished and recorded. The retry waits for source
regressions, independent exact review and fresh runtime admission.

### Second Datastore Native Attempt and Separate Absence Check

The reviewed replacement inputs above were executed from the integration
worktree at 2026-10-10T18:40:03.563438Z. All eleven test methods passed;
teardown failed while verifying three removed container IDs with a timeout.
The overall ISOLATED result remains FAIL, exit 1, elapsed 345.36 seconds.
Immutable receipt SHA-256 is
`7ec2769adf87ea7eae6429b7fb8a2084075a87f259639035d4bd41039657553d`.
No HOME, migration, production rotation or recovery lane ran.

A separate same-daemon read-only inspection confirmed all three exact IDs
absent, with exit 1, empty JSON and the exact Docker container-inspect
no-container message. The first narrow checker rejected this distinct Docker
message and its failed receipt `b8e98f1b57b7480d4c3cfe73ae9b323081e8e97c1fba1387d7c60cfd6dcee2ea`
is preserved. The corrected independent observation receipt is
`008f1cb46097f5172099bbadd3980817aa70cb45991ec6b3b114132ed03638f0`.
No additional deletion command was issued. Current absence does not change
the original teardown failure to PASS; source timing remains under repair.

### Reviewed Public DB Retry Admission

The finite retry operator is SHA-256
`9de37e44c842cb69e097c22dcf06fda7c9447a77147c039f74422b585d5248f2`,
helper `5c325988457754266b694c5766a94c9f74c7ebb944e05c90cacf74562edbac64`,
and synthetic tests `89dabb3f2893c8c58f29777e08358a643c5dd39c961d663f8a16705da009d299`.
Forty-one synthetic tests passed with 83-percent source coverage; exact
independent review found no P1/P2. The next command is
`/usr/bin/python3.12 -I -S .agent-work/grype-fresh-database-operator.py --phase retry-import`
in the SEC01 operator worktree. At admission the datastore attempt has ended,
its exact retained IDs are absent, and MemAvailable is 12,868,512 KiB, exceeding
the ten-GiB guard. The operator rechecks admission, binds the existing verified
public SQLite and receipt, and creates a separate exclusive scratch. Six-GiB
cache/eight-GiB memory limits and prior exact-owned cleanup apply. Actual retry
import/status remain NOT_RUN until a new immutable execution receipt exists.

### Actual Public DB Retry Result

The reviewed finite retry began 2026-10-10T18:54:49.221040Z and passed in
125.813 seconds. Immutable receipt
`/tmp/hy-home-sec01-grype-db.qyjt30nn/import-receipt.json` has SHA-256
`89d864166b47e9404aec69610c7771764a785262aba0616b52b8089a05da0f1e`.
The attached client, container, import and status all exited 0. Grype reported
`valid=true`, schema `v6.1.10`, built `2026-10-10T06:30:01Z`, from manual
import. The verified public raw member and upstream index/archive hashes are
unchanged. Trust remains same-source HTTPS plus SHA-256 integrity, not a DB
publisher signature. The exact owned container is absent and its quota-limited
cache was discarded. Earlier failed receipts and scratch are preserved.

This closes only isolated tool database hydration/status readiness. It does
not constitute a service SBOM, CVE result, remediation, HOME rollout or recovery
receipt. Source preparation for bounded authenticated image scanning may now
continue; actual image scanning still requires exact inputs and reviewed
execution boundaries.

### Current OAuth Source-pin Checker Receipt

The earlier frozen hardening hashes are historical inputs. The current checker
SHA-256 is `6b140280e191a81abd200b9dfd4307a3b289b25a71b0b1d2dcfe6c6ff4bc00a7`
and its regression file is
`087c52413001555b87338832b3043e41a27ffe980758217e07932a617e78cac6`.
The prior reviewed regression hash was `52b4dbb67484fb988e38cd2ac99adcf26ae890b8f984e81fc4f112c1b6865b1d`;
the actual registered staged lint rejected its implicit subprocess check mode.
Adding explicit `check=False` preserves expected nonzero refusal outcomes;
the replacement four-test run passed again. The failed lint is preserved as
a corrected SOURCE gate failure, not an operational failure.
Two meaningful assertions failed before repair. All four version-contract
tests passed after repair, and independent review reproduced four PASS with
no P1/P2; Bash syntax and diff checks passed. The production and default
development FROM must match the exact repository, stable semver and lowercase
64-hex digest grammar. RC, mutable/tag-only and mismatched inputs are refused.
This is SOURCE syntax/equality evidence, not publisher tag-to-digest
authentication, native OIDC, HOME or complete Tier02 acceptance.

### Current Local Delivery Authorization

The user's subsequent direct instruction requires local branch/worktree
integration without using PRs. This supersedes the earlier prospective PR
sequence for the current continuation. Preserve logical commits, run registered
local affected and staged gates, obtain independent source review, and merge
only the reviewed local head. No remote push, PR creation or remote merge is
part of this local disposition, and no hosted CI PASS is inferred. Historical
PR receipts remain unchanged. Only merged clean coordinator-owned worktrees
may be removed; other workers' dirty paths, ignored evidence and ongoing
operators are preserved. Operational acceptance remains separate and pending.

### Superseded Dev Selection and Current Public Source Refresh

The preceding, now superseded instruction selected local `dev` as the
integration target and authorizes completing merge preparation and cleanup
without PRs. At inspection neither local `dev` nor `develop` existed; local
`main` was `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`. A clean temporary `dev` worktree was created and later removed with its branch
after the superseding main-only instruction, before any task commits reached dev.
Preserve foreign dirty worktrees and ignored operational evidence.
No remote write or hosted CI claim is authorized by this local disposition.

Service commits `f7130b743`, `c16f4b4be`, `5093473e2`, `3a5a7af80` and tool
commits `b03f72e2a`, `b654ad677`, `c0de568c5`, `7f8f23e44` were independently
reviewed and merged with their logical history. SOURCE pins are Redis exporter
1.93.0, OAuth2 Proxy 7.15.5, Tempo 3.1.0, OpenTofu 1.13.1, Great Expectations
1.24.0 and k6 2.3.0. LAB exporter remains unchanged. These are candidate source
updates; final custom-build identities, signatures, CVEs, native compatibility,
HOME and recovery remain separate pending evidence.

The coordinator rechecked official public release/tag, registry index and
linux/amd64 manifest/config metadata plus PyPI artifact metadata. Immutable
public receipt SHA-256 is
`484012e9855c5e3e95c105d79eac0d80048801a19e2d5d6b14988faefa428382`,
observed `2026-10-10T19:14:00.945688Z`. Trust is official public HTTPS metadata
and digest integrity; signatures are not verified. Existing release/source
lookups retain these facts, and ten existing service ledger rows preserve
historical actual-running observations while recording new source inputs.
Final custom image digests remain UNKNOWN. No duplicate inventory was created.

The registered version renderer changed eight projected images without adding
or removing repositories; freshness check passed. Operations catalog check
passed. The first hardening run failed because the root and excluded LAB
exporters correctly differed. Commit `2b81466cae9a9f7071703aad0436740c2de3373b`
scopes the existing registry lookup to an exact Compose source; malformed,
duplicate, missing or globally inconsistent sources are refused. Independent
review found and repaired a dual-command-substitution false success with a
meaningful RED regression. Six final tests, staged gate and fresh independent
review passed. The final seven-tier hardening command exited 0 after merge.

The two new stable-candidate test modules are required before the optional
runtime separator and selected by changed-path routing. Meaningful missing
registration assertions failed twice before repair; the combined routing,
workflow and candidate run passed 60 tests, exit 0. These are SOURCE/UNIT/STATIC
receipts and do not complete all root stable/security acceptance.

### Reviewed Datastore Retry Inputs

Native boundary commit `9c23d21211636611387bd6500df2e80e5de5bd31` is integrated.
Observation source SHA-256 is
`cdd7b0c4743c896baa62871b028c584000a2756e5a41f04d901cdffa9e807eb8`,
boundary tests `bcf4ef40efe895e564aebb94be561b8f265005b92a0e2792a14df24c23a72af0`.
Nineteen offline tests passed and eleven opt-in native cases were skipped;
independent review and staged checks passed. The current Compose exporter is
now the verified 1.93.0 linux/amd64 candidate. Its exact cache-only acquisition
must precede another isolated run; native test code does not pull images.
The next actual attempt has not run. Previous overall native failures and
separate successful absence checks remain unchanged.

### Authenticated Public Image Scan Admission

The coordinator selects exactly one cached public GoTrue v2.197.0
linux/amd64 subject. Manifest SHA-256 is
`847460cd150ba225bd4ac6adfbadcd609c47e30e1e2bbaec44578e1b535c921c`;
its read-only cached inspection is
`3b37ef893e1117a7e10eb7c05d84e41df11ff77257c6617d2c2e0ee8c98443b0`.
Both bind the public receipt above, exact index/platform/config identities,
image size, ordered RootFS diff IDs and six compressed-layer pairs. This is
public configuration/layer verification, not private application state.

Independent review found no P1/P2 in operator
`7386d77f111e316bde79a035abe09ca61e92b056b81dc158ceeb2d136f156df2`,
pure helper `64b3cd20b83d5fb425bf4fa35ae628fa34f10395d49d090c32d93197fd689ac7`
and tests `2a5e28bad131c262543d87ae1d5ddb961c773304ce2db3d8df00407a5c7f89e0`.
Twenty-four synthetic tests passed; coverage is 90/88 percent for operator/helper.
The approved exact command in the SEC01 operator worktree is
`/usr/bin/python3.12 -I -S .agent-work/scan-authenticated-local-images.py --manifest /home/hyunyoun/data/hy-home.docker/.worktrees/integration-acceptance-followup/.agent-work/public-scan-first-batch.json --manifest-sha 847460cd150ba225bd4ac6adfbadcd609c47e30e1e2bbaec44578e1b535c921c`.

The utility imports the authenticated database once; uses network none,
read-only rootfs, drop ALL, no-new-privileges, UID/GID 1000, only four public
read-only binds, CPU two, PID 64, ten-GiB memory/swap and bounded two-GiB
work/six-GiB cache tmpfs. Admission requires twelve-GiB host MemAvailable.
Exact cached public image save is capped at two GiB and 300 seconds; SBOM and
CVE outputs are capped at 128/64 MiB and each scanner phase at 300 seconds.
The session has 3,600 seconds plus 120-second cleanup and ten-second reap.
No pulls, private sources, service activation or concurrent datastore native
attempt are allowed. Exact owned cleanup and immutable success/failure
receipts are mandatory. Image signatures remain UNKNOWN. Actual scan is
NOT_RUN at admission; even completed scans are evidence only and cannot
satisfy all current-stable/security, HOME or recovery acceptance.

### Public Scan Admission Failure and Reviewed Retry

The first exact approved command failed at manifest preflight, exit 1,
2026-10-10T19:33:42.882382Z, elapsed 0.001 seconds. Immutable failed receipt
SHA-256 is `6843eb8036ff22c57873416d2e15832126358f2cd6418269432d4a6f791e69c8`. No Docker container, image save or scanner ran. The manifest
used Docker Hub's short repository form although the strict manifest grammar
requires an explicit registry. The subsequent cached projection uses the short
form, so changing only the manifest would also fail.

The narrow repaired helper permits only the exact full/short Docker Hub pair
for an approved fully qualified repository/digest. Other hosts, aliases, paths,
digests and malformed projections remain refused. Operator SHA-256 is now
`dcdfceee505520604554e3d73fdcca85dd64da68105b6d115a167e648ce0a27d`,
helper `88686b01bce4e2f18cf933ef876f4dc6d55a61573ca8f1b79717ff37a394e453`,
and new focused alias tests
`3aab2d5fb5f74763e352ab0f5a1734a18e0a59f604f63d6ab8e05c0eca873497`.
Twenty-seven synthetic tests passed; coverage remains 90/88 percent.
Exact independent re-review found no P1/P2 and ran pure validation of the
actual replacement manifest against the frozen cached projection successfully.

The replacement mode-0400 manifest is
`.agent-work/public-scan-first-batch-qualified.json` in the coordinator worktree,
SHA-256 `268bdcdb8996c7b0db9d6483f488492cfb5b1d65ce839f82a386a9407091fe63`.
It differs only by the explicit `docker.io/` prefix. Reuse the same finite
execution command and all resource/cleanup bounds above with this exact path
and SHA. The old manifest, frozen sources and failed receipt remain immutable.
The retry is NOT_RUN at admission and does not permit more subjects, private
state, live services or a wider retry budget.

### Second Public Scan Failure and Current Delivery Target

The fully qualified manifest retry failed at public image save, exit 1 after
121.653 seconds. Immutable receipt SHA-256 is
`10372f52d3b8478bcf403ee67df85dbdd977581cd10352a0a4252d31e703c2a8`.
Authenticated database import and status exited 0; exact owned utility cleanup
was verified absent. Docker returned `No such image` for the inspected platform
manifest ID; the save stdout was empty. Neither Syft nor Grype scanned this
service. Preserve the failure receipt and original frozen inputs. A narrow source
repair must save the approved repository digest with explicit `linux/amd64`, while
retaining pre/post image identity and archive configuration/layer checks; an exact
new freeze, meaningful regression and independent review precede any third run.

The latest explicit instruction supersedes dev: integrate only into local `main`,
without PRs, remote push or remote merge. The unused clean dev worktree and branch
were removed. Current local main is
`a31a38ca29ee8e0683a29e61bf41347bfddc3d62`; the same SHA was observed on
remote main. Preserve service-unit commits and original author history. Source
integration includes independently reviewed fixes, candidates, projections and
CI routing. The full 124-entry latest/security gates still exit 2, with
`ready=false` and `ledger_complete=false`; this is not production acceptance.

Both registered changed aggregate profiles exited 1 at the same committed-HEAD
Task evidence regression: Task 0005's old Acceptance phrase was outside the
registered domain. Its pending correction needs a logical commit before the
clone-based regression can see it. Other completed checks retain their individual
results, but the aggregates remain FAIL until a fresh complete run passes. No
validator exception or false aggregate PASS is permitted.

### Current Native and Public Scanner Failure Receipts

The third isolated datastore attempt used committed input
`85033fb8526889fbd20d5b7b765be5ad8bade14d` and boundary
`bcf4ef40efe895e564aebb94be561b8f265005b92a0e2792a14df24c23a72af0`.
It exited 1 after 514.418 seconds: 23 of 24 functional methods passed, while
the wrong-password method and teardown rejected Docker's exact missing-object
response (`[]` stdout and case-variable exact full-ID stderr). Immutable receipt
SHA-256 is
`3f64d701fe08d284d82a254155af71905cef369d77f59dbbabba41132563954f`.
A same-daemon follow-up confirmed all ten exact owned IDs absent, without any
removal command; receipt SHA-256
`2f94217b087366ffe562369072ed1a657138af939d1c457cf7e2e17f574aba81`
is PASS only for absence. Preserve the original native FAIL. The independent
source fix `c70050a9fe2b93fc514d37f35d9f5b1687c2d383` changes two files;
RED was witnessed for both exact dialects, then 19 source tests passed with
11 opt-in native tests skipped. Boundary coverage was 81 percent, staged gates
passed and independent review accepted. A fresh native run remains required.

The third public GoTrue scan failed after 120.465 seconds at archive binding,
receipt `238dac6e9aa0468a5ee9759aa89733848b8dc53467c1b1320dbbe90681b49b4f`.
The exact official OCI index binds one platform image and one public attestation.
A narrow reviewed validator checks that graph rather than accepting extra files.
The fourth actual attempt validated the saved configuration, six layers and
one index-bound attestation, and actual Syft and Grype processes both exited 0.
However, post-scan identity validation rejected Grype's `source.target` JSON
dialect while expecting Syft's `source.metadata`; the attempt remains FAIL,
category `scanner-json-public-image-binding-invalid`, after 132.079 seconds.
Its immutable receipt SHA-256 is
`e4b5796e382821d832e56cba7289194301cc9c2df65f457672fe35024e8ee39e`.
The preserved public SBOM is 386818 bytes, SHA-256
`cc8adb815eda5f241734ff44d00d1e4f2e036417442bf75d6b5e08fe479bf0ba`;
Grype output is 342433 bytes, SHA-256
`2a00bbf83e3d9d514f199d8b75ad9908da67ef41a50931858fd97eff036fd210`.
Authenticated database import/status exited 0 and exact utility cleanup was
verified absent. Image signatures remain UNKNOWN. A repaired validator and
its review can supply a separately labeled offline binding observation, never
rewrite this failed operational receipt or prove all 124 service entries safe.

### Superseding Isolated and Scanner Binding Observations

A fresh native run after source fix integration used input
`c3165279c72154fb109a70956c66838e6f2de6d6`. All 24 datastore methods and
teardown passed, exit 0, in 318.350 seconds. Receipt SHA-256 is
`d8631ac1e6dee743a8c869fd5f3b6cf36847545e9681a8f4febec4ef11e61c2e`.
This is synthetic ISOLATED acceptance only; HOME, migration, secret rotation,
application recovery and actual image deployment remain unverified.

The independently accepted scanner repair pins exact Syft `source.metadata`
and Grype `source.target` dialects, with 40 tests passing. The preserved fourth
attempt's public archive, SBOM and Grype outputs passed a new read-only offline
binding verification against their recorded sizes, hashes and approved image.
That observation does not rewrite the original failed attempt. It reports
173 packages and 80 vulnerability matches: 7 Critical, 39 High, 16 Medium,
13 Low and 5 Unknown. The database reports fix versions for 48 matches,
not-fixed for 2 and unknown/empty fix information for 30. These are scanner
findings rather than confirmed exploitability or remediation. The image remains
blocked for security acceptance; signatures are UNKNOWN and all 124 entries
remain subject to the stable/security gate. SEC01 owns validation of supplier
fixes, applicability and compatible rebuilt or updated artifacts before rollout.

The complete registered Compose leaf now passes in 170.940 seconds under the
unchanged 600-second bound, receipt
`c7fddaf47e574da6c2399a625c9e64844814458ed4a501fc9f21529026ed4c46`.
Each profile and HOME uses one JSON render for the unchanged service, port and
storage checks. Independent RED/GREEN and review preceded commit `583d35952`.
The existing aggregate failures remain FAIL/124; this is a separately bound
source leaf result, not an aggregate PASS. The 521-test Compose baseline leaf
passed with 69 optional runtime skips, receipt
`e72ec1031c381f32471c0b4f984ff41e89dd84b944013094944f54516e14933c`.
Control-plane commit `52456c4f887353d44db606655d1382eccd6ad36f` aligns
only the synthetic Docker fixture with its declared `app` service and adds
empty/malformed JSON rejection cases. The corrected module passed 59 tests,
including independent review. K6 consumer commit
`396b2d907c662dff91c7939caeb5d27908bbac0b` aligns the existing delivery
rehearsal with the 2.3.0 candidate and adds a consumer-version regression;
eight source tests and independent review passed. Actual K6 2.3.0 native
execution remains NOT_RUN; historical 2.2.0 receipts are unchanged.

The registered remaining-leaf replay on `396b2d907` passed control-plane,
pre-commit regressions, workflow contract, Storybook contract and release
regressions. Control-plane receipt SHA-256 is
`f8e495a133d84e36021bba70cfb1489b1c168419669128637ad9f7fc1ba5165a`.
The final repository-integrity leaf initially failed: 317 tests, seven errors
because the coordinator's PATH omitted installed Node. Receipt SHA-256 is
`6e416fc9c7cb222b8656a3e0bbfc4f161bd836bb02caf99972b2d9736a8d4136`.
Its exact registered invocation then passed all 317 tests in 61.504 seconds
with installed Node v26.10.0 on PATH. Receipt SHA-256 is
`28979b95fb7844dc32564358ce2c7e8a81ce70be80d243fb7cad6fa56e2f209c`.
No assertion, tool contract or timeout was weakened. The separate original
aggregate failures and the Node-path failure remain immutable. This composite
set of bound leaf observations supports SOURCE delivery; it is not a newly
executed aggregate PASS or SEC01 operational completion.

The priority branch `codex/smtp01-request-contract` was detached and removed
first after exact worktree/index/status/untracked/ignored fingerprints matched.
Receipt SHA-256 is
`30e2e98bff307599b6ab45a81189af0f97a913ce3818dccbcec44fb7d2172c30`.
Its root checkout's 24 foreign dirty paths were retained. No reset, stash,
clean, force push or private deletion was used. Current local `main` delivery
preserves the original logical task commits; no `dev` branch or PR is used.
Merged clean worktrees may be moved whole into a private retained-evidence
archive and detached before exact-SHA branch deletion. Dirty or active operator
worktrees retain their path and bytes; ignored evidence must not be discarded.

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
