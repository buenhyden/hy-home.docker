---
title: "SEC01 Stable Security Integration Task"
version: "0.4.17"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-14"
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

### Actual Local Main Delivery and Preserved Worktree Evidence

Local `main` fast-forwarded from
`a31a38ca29ee8e0683a29e61bf41347bfddc3d62` to
`96f061afa5570affe65877a84f18e3c9cce5162a`, preserving the task authors'
logical commits and coordinator repairs. Main's worktree is
`/home/hyunyoun/data/hy-home.docker/.worktrees/main-local-integration` and
was clean after delivery. Fast-forward receipt SHA-256 is
`a630bd227b4730bfbbbd77f930adaae2b3954c874e686aa0e6e5116082495ee2`.
Two entrypoint checkout modes were normalized from 0775 to 0755; file bytes
were unchanged. The newest read-only remote main still matched `a31a38ca`.
No remote push, PR or `dev` was used.

All five Spec/Plan/Task result documents passed selected metadata with zero
violations and independent review. First staged validation failed because the
isolated Markdown hook removed two redundant empty lines in Task 0005. ROOT
removed only those lines, obtained independent format-only approval and
restaged; the exact replacement staged gate passed before commit `e129c05ba`.
Commit `96f061afa` separately preserves the three dated scanner/Cosign history
keys that remained in SEC01's uncommitted evidence JSON. Existing JSON keys
were unchanged and independent review plus the staged JSON/secret checks passed.
These historical additions never certify the later complete scanner input.

Eleven clean, already merged worktrees were moved whole to
`/home/hyunyoun/data/hy-home.docker/.worktrees/retained-integration-evidence`.
Their ignored evidence, complete checkout directories and inode identities
were preserved, and each was detached before exact-SHA branch deletion.
Archive manifest SHA-256 is
`dd0137f678a6e5ae1d2a5dd0f52c0ad71acc40544a6af93fbb11e71cb399a881`.
The Git worktree registrations remain as detached evidence archives; no forced
worktree removal or private payload deletion occurred.

Eight more merged task branch references were removed with exact main/ref CAS:
three source worktrees were detached at the same HEAD with their dirty files,
index and ignored inventory unchanged, and five refs had no attached worktree.
Receipt SHA-256 is
`40a08beabe159d92517a4df8d7973b96ec609654bca5a318f776f6f47a70443a`.
The first preservation guard stopped before any change because ROOT's ignored
inventory included newly created coordinator receipts and relocated archive
paths. Rechecking confirmed ROOT's source diff, index, status and tracked
inventory were unchanged; the corrected detach-only operation also bound a
fresh full ignored inventory before/after. Other three foreign worktrees'
full fingerprints remained unchanged. Root retains 24 dirty entries, SEC01
10, SMTP01 one and the original P09 checkout 30. Their directories and private
operator evidence stay at their existing absolute paths. No reset, stash,
clean, force push or unrelated P00/P01 branch deletion was used. The active
coordinator branch is retained only until this result commit reaches main.

Fresh source-ledger evaluation on code input
`396b2d907c662dff91c7939caeb5d27908bbac0b` again returned exit 2:
latest `ready=false` and security `ledger_complete=false`, coverage checked,
124 observed entries and no missing/unexpected source services. Latest receipt
SHA-256 is `f9a0c7242d50998f736fb03688771b1650185000e17a3eaceb0d4bd2fc75d1cc`;
security receipt is
`a6325ff3199f1874a24b3575e933f10460a80397669baf701fca6dd9b4a60286`.
SOURCE delivery therefore does not close criterion 15. The next SEC01 work is
supplier/CVE applicability and compatible artifact remediation, full authenticated
artifact coverage and named-service backup/restore/HOME acceptance. P01's final
OpenBao contract and P03's final shared service/environment contract wait for
that relevant verification; P02 may proceed with the merged canonical SMTP
source contract while actual migration waits. CLN01 retains positive/unknown
consumers until their exact backup/restore and consumer evidence supports deletion.
P09 remains preparation only and creates no app or runtime resource.

Task 0005's fourth actual isolated restore was independently accepted after
execution: receipt `74794448811aa3632b707ec8043e67e84033510d6731cb96a3335717a0690699`,
two files/40 bytes in 18.555 seconds, exact container absence, stable target
metadata and four immutable ledger files confirmed without payload reads.
It proves only dated two-file restoreability; SMTP send/authentication,
application/production recovery, external-consumer absence, migration and
rotation remain unaccepted. Current operational retirement is not inferred
from duplicate-file absence. No LAB runtime or learning app change occurred.

### Full Image and HOME Continuation — 2026-10-11

The current user explicitly requests full image validation and HOME deployment,
with latest-version PASS when a successful official stable-channel query proves
that no newer version exists. Existing equal-version gate behavior already
supports that result; nine focused latest/security tests passed. A failed query,
UNKNOWN, a test/RC channel or an unverified submitted claim is not that evidence.
The ledger gate validates submitted completeness, not supplier authentication;
security, compatibility, recovery and actual HOME acceptance remain separate.

The current source baseline is `2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`.
The first cleanup preflight detected remote main changing from `a31a38ca` and
stopped before any mutation. A fresh `ls-remote` and fetch confirmed remote
main at `2b9f5ec82`; ROOT did not push main in this continuation. Independently
reviewed refreshed cleanup then removed seven merged remote refs, four merged
local refs and eleven clean detached worktrees. Exact lease/CAS checks and
non-force worktree removal were used. All 832 ignored leaves were relocated
with inode/mode/size/link identity preserved under private retained evidence;
the four foreign dirty source states remained unchanged. Receipt SHA-256 is
`67472676503512f3c98833d51af7f6d139f02179adcb00eddec975438e71058f`.
Independent post-review confirmed the result; full `git fetch --prune origin`
then removed six older stale remote-tracking refs. The unmerged OpenBao branch
`bb63f27e` retains one unique commit and was preserved. Its retention is not a
claim that the P01 runtime contract passed.

The fifth GoTrue scan used the previously reviewed exact manifest and frozen
scanner contracts; originals and four failed attempts were preserved. Actual
receipt `/tmp/hy-home-sec01-scan.eppsc3db/scan-receipt.json` has SHA-256
`76615d0daa6619c9c634b8dc4b36abc4f7e7481430f5484c5316840c87e3835b`.
It reports SCAN_COMPLETED in 124.51 seconds, 173 packages and 80 matches:
Critical 7, High 39, Medium 16, Low 13, Unknown 5. Exact owned container absence
was confirmed and independently reviewed. Signatures remain UNKNOWN and DB
trust remains same-source HTTPS/SHA256 integrity without a DB publisher
signature. This completes one scan's execution evidence, not security acceptance.
The official current Auth release remains v2.197.0; no forced version bump is
required, but the unresolved findings are not waived by that fact.

Fresh official-channel investigation made 79 fixed public requests: 74 succeeded
and five failures were preserved. The 51 previously unresolved rows were
classified as 24 declared matches, eight new direct candidates, three custom
base matches, two Community/Platform matches and 14 custom/bundle/source
contract cases. Reconciliation receipt SHA-256 is
`01bcddbde5b46643253985fe87665cf27e9b883efff88b0835b092bef39076ad`.
Supabase's current self-hosted bundle and independently newer components have
different pins; this does not authorize a silent downgrade or untested mix.
Gatus's source/hardening patch and custom dependency/base updates remain tasks.

Full public/cache preparation on the same input observed 124 ledger entries,
85 distinct current references and 152 references across current/candidate/build
roles. Its receipt SHA-256 is
`aadc48beb745dae295d51be7129b2e8fa06d243a179a9e769f1a93c5724cabc6`.
This is prepared coverage, not completed scanning. Eighteen unique subjects
were schema-ready; absent cache, custom builds, attestation graph, large-image,
authentication and unresolved inputs remain explicit. The existing 1GiB-image,
2GiB-archive and resource/capacity bounds are not silently widened. The Node
Exporter public/cache subject independently matched, but its actual Quay Docker
schema2 archive was rejected by the OCI/Docker-Hub-only contract. Separate v2
contract/operator copies subsequently passed 44 synthetic tests, 92% combined
coverage, Ruff and independent SOURCE review; frozen originals were retained.
The v2 contract SHA-256 is
`33f3dcdf19e7ef69567fb48736a06b22ba326dee91374d53cfb4ca6927169961`
and the operator SHA-256 is
`c033adbefbeeb6d43c4112384060b7f73469b645a0cab8d12f63cc20aac822c2`.
ROOT's authorized native retry then failed before scanning because the host
memory budget was insufficient; receipt
`/tmp/hy-home-sec01-scan.xtsaz4ym/scan-receipt.json` SHA-256 is
`8345aed4ceea5717c6b2e191eaffa05992bdde901c188cffc29dfa5cfd5c82e2`,
exit 1. This is not completed Node scanning or HOME acceptance. Capacity bounds
were retained and no live service was stopped to free memory. An auto-review
rejected the preparation worker's attempted public archive
export as exceeding its initial inspect-only scope; no such export ran there,
and unaffected public metadata/synthetic SOURCE work continued.

The 18 ready subjects were split into sequential 8/8/2 manifests within the
existing disk gate; none of those batches has executed. Initial build-path
reconciliation resolved 29 tracked Dockerfiles and left one inline declaration
unresolved, preserving Compose-relative contexts. A separate inline supplement
then recorded its exact Dockerfile hash and two public base proofs, both absent
from cache; receipt SHA-256 is
`9c29b5c79a9c84d6a86210489897db2c9b79457392342666608b495c5a7dfe0b`.
Supplemental public metadata preparation for 25
build-base references completed (21 absent cache, three attestation blockers,
one size blocker); receipt SHA-256 is
`4376edefaf71bcae67ceb829a049d275a0f2306e84d12d5de9ca4fd9cbea0f83`.
This metadata neither creates custom images nor closes full scan coverage.

HOME read-only readiness receipt SHA-256 is
`5514c567a1249fec742c0ff282c31ca0f9bc2e0092242682ce1d445433a11cd3`;
the follow-up remediation contract is
`bd0f7b609d9b2ffc6506b71d22f4b20d67cda8e10f190bde76cc16be0d4ff5a1`.
At that observation 59 of 63 root containers were running, 58 were healthy,
none unhealthy, and five had no health/completed-job status. Thirty-one service
references differed from source targets. The last full backup failed with exit 1
and last whole-backup success was stale; the OpenBao snapshot token was absent.
Current state/host catalogs, unseal custody and exact full-service restore
acceptance were unverified. Thus stateful HOME deployment is blocked by actual
backup/restore facts; OpenBao additionally needs its snapshot-only credential
and authenticated snapshot/empty restore contract. The existing two-file SMTP
restore does not close those gaps. Stateless canary preparation selects only
`mng-valkey-exporter`, subject to its exact scan/security and independent
deployment/rollback review; no HOME recreation is claimed here.

RUN-0021 incorrectly described token absence as a successful skip. The source
sets `status=1` and prevents stale staging snapshot reuse. The existing missing
token regression passed after correcting an initial test class-name invocation
error; the runbook now records failure of that unit and final whole-run exit 1,
even when other steps continue. No backup script, secret or live service changed.

P02 Task issuance is a separate logical commit
`953a6c10e5ea7d7883b11f6d7f1a9f6f2104be2d`, delivered to local main with
metadata, staged and independent review. Its dedicated clean branch/worktree
starts at that commit. P02 public catalog/schema/view preparation may proceed;
final runtime mappings and actual migration wait for P01/SEC01/P06/CLN01
contracts. SOURCE/UNIT/STATIC/ISOLATED/DELIVERY observations above do not
assert HOME/MIGRATION/ROTATION/full RECOVERY acceptance. LAB runtime, learning
apps and actual Wiki remain excluded.

### 2026-10-12 stable-source refresh and combined projection

The independently reviewed source branch starts at local main
`640d178ba93a5994456534249a5d1e542a856949`. Logical commits
`b19af5fc533c960b6eb51400af894cc89f470e21` and
`5b7a261a6d9323e0647a05ba4c9a40ff821343d0` update Dozzle 11.3.1,
Mailpit 1.31.5, Ollama 0.40.3, Renovate 44.151.0-full, Stalwart 0.16.26,
Imgproxy 4.0.17 and Open WebUI 0.12.0-cuda using exact index digests.
Stalwart's Compose, custom configuration image and Dockerfile stay aligned.
Supabase receives only the leased Imgproxy image change; the canonical SMTP
wrapper/source and other component pins are preserved.

Fresh official release/channel and exact index/linux-amd64 metadata receipt
SHA256 is `b41edf6b6fa5b2bbdd579d20378cbeedb37c16635a1aa95dceb78b8239f493b2`;
the final source handoff SHA256 is
`a24e81f849f32f2db546dfc99d93cdc3011b77149588490fd8a13b453bcb98fd`.
The source worker's final focused run is 26 PASS and one explicitly skipped
Stalwart native rehearsal. Independent source and committed-range reviews
APPROVE with no remaining Critical/Important source finding.

The Dozzle review first blocked persisted configuration enabling Docker control
through the socket. Exact-tag supported settings now explicitly disable actions,
shell, MCP, self-update, container updates, image checks and the setup wizard;
release checks are manual. A permanent regression verifies the control map.
The Docker socket retains host-control blast radius; a readonly bind does not
make the Docker API readonly. No real HOME persisted settings were changed.
An existing worktree-only 0775 Open WebUI entrypoint failed its security test;
its mode was restored to the Git-recorded 0755 with identical content/blob.
That correction is not a HOME permission result.

The coordinator combines those commits with local main
`df38e9a4acad4915087d3b813ece22dd93bd1593` and uses the existing tech-stack
generator's `--write` followed by `--check`, both exit 0. Eight source projection
records change; repository identities remain stable. The current required
`OPSFLOW_AIRFLOW_IMAGE` input remains unresolved and is not replaced by a pin.
On this combined source, `tests.validation.test_sec01_version_contract`,
`tests.validation.test_service_wiring_contracts` and
`tests.validation.test_tech_stack_version_contract` run 75 tests, all PASS in
40.311 seconds, exit 0. The actual staged gate also exits 0. These are SOURCE,
UNIT and STATIC receipts; final Task metadata/staged/readback follow before
the local integration commit.

The five freshly rechecked primary stable channels OpenBao 2.7.1, Airflow 3.3.2,
n8n 2.42.6, SeaweedFS 4.48 and GoTrue 2.197.0 have no newer stable candidate
at that observation. Only their latest-version dimension passes. Prior GoTrue
Critical/High findings, signatures, SBOM, full-image scan coverage, builder
compatibility and stateful recovery evidence remain unclosed. The historical
124-service ledger/input hashes are not rebound or declared complete by this
seven-product source increment.

The direct user subsequently authorizes moving the complete tracked Supabase
definition, including GoTrue, and infra LAB-only assets to root `labs/`.
TSK-0015/W70 consumes the reviewed Imgproxy commit first, preserves this source
receipt, and rebinds current path/projection/catalog consumers after the rename.
Existing LAB images, running resources, private values and data are not changed
by this source increment. Before Open WebUI 0.12 activation, its database and
secret-key backup, empty restore and pre-migration rollback must be accepted.
All native pulls/builds/start, signatures/SBOM/scans, HOME, MIGRATION, ROTATION
and full RECOVERY for this increment remain NOT_RUN. Task0009 stays in-progress.

### Resumed stable-version and ROOT ledger reconciliation — 2026-10-12

The latest user resume instruction restores current stable-version updates and
investigation of their official documentation and related compatibility/recovery
contracts. This supersedes the intervening warning-only version-update restriction.
Keep existing supply-chain gates and completed P00/source history; no new gate or
scanner framework is introduced. A fresh successful official stable-channel
lookup with no newer release needs no version bump. UNKNOWN or missing/stale
scan/advisory evidence is not a clean result. Scanner source corrections remain
bounded to actual reviewed warnings/defects. Existing reviewed not-affected
security dispositions do not substitute for current stable-version evidence.

At main input `69b070b759e9ca235d5aa9ee31c2ab311df4dffc`, the existing
`expected_from_root` authority independently observed 111 ROOT services across
44 Compose inputs, manifest SHA-256
`f6f30b50738c8ac33e4b6f651082ee1612d4661faa8ad906c89e65deefa29564`.
Those counts are observations, not checker constants. Thirteen former Supabase
ROOT rows now belong to `labs/supabase.yml`; their original rows and former
include census are preserved in the ledger's historical fields. Current rows,
expected set and include hashes match ROOT only. GoTrue's historical scan and
LAB SMTP readiness are excluded from current ROOT completion. This source
scope reconciliation reruns no supplier lookup, native scan or deployment.

The new permanent regression in existing `test_update_gates` independently
compares the submitted ledger with ROOT include discovery and retained LAB
history. RED exited 1 on all thirteen stale LAB rows; after reconciliation,
`python -m unittest tests.lib.supply_chain.test_update_gates tests.validation.test_sec01_next_tool_candidates -q`
passed 33 tests in 1.763 seconds, exit 0. The initial reconciliation inferred a
nonexistent LAB filename and stopped before writing; the current tree/README
supplied the actual `labs/supabase.yml`. No scanner or gate implementation was
changed to satisfy the user instruction.

Independent review required exact historical service/input preservation, rather
than merely a nonempty LAB archive. The permanent regression now compares old
minus current service/input sets, uniqueness/count relations, original row
identity and exact `labs/supabase.yml`. Three in-memory corruption probes
(dropped LAB row, changed LAB path, changed old census) each produced the
expected single assertion failure without changing the ledger. Final system
Python execution passed the same 33 tests in 1.773 seconds; Ruff check and
format-check exited 0. The old temporary QA interpreter was absent and its
three attempted commands exited 1 before execution; no result from that absent
environment is claimed. Final independent seven-file review is APPROVE.

Primary advisory triage identifies Qdrant GHSA-3gph-6c29-p29v, patched in
1.19.2, and SeaweedFS GHSA-99q7-x53r-6j4g, affecting versions from 4.39 with
no listed patched version. Source declares Qdrant 1.19.2 and SeaweedFS 4.48.
Fresh read-only Config.Image/Image/State inspection found running Qdrant
1.19.1 and SeaweedFS filer 4.47; the version warning remains relevant pending
feature/exposure and recovery review. Those observations do not read keys,
render private configuration or prove exploitability. The SeaweedFS TUS-only
mitigation is prepared separately through its existing source/test owners;
the later stable-version update request remains separate from this advisory
triage, and scanner corrections still need a concrete warning/defect.

- [Qdrant advisory](https://github.com/qdrant/qdrant/security/advisories/GHSA-3gph-6c29-p29v)
- [SeaweedFS advisory](https://github.com/seaweedfs/seaweedfs/security/advisories/GHSA-99q7-x53r-6j4g)

A separately approved, freshly hash-checked HOST-only backup metadata query
ran once from controller bf4d9876/operator fc2c6f67/loader d9bf6543. It reused
the pinned earlier STATE receipt 93222aea without a STATE rerun. Restic's query
exited 0; the unchanged strict metadata parser rejected the returned path class
with the closed reason `unexpected_path_class`, so controller and operator
exited 1/FAIL_CLOSED. One owned container was created, started, normally removed
and verified absent; its temporary Docker configuration was CLEANED, with zero
residual blockers. No snapshot/repository write, restore, init, prune, unlock,
rotation or retry ran. Full JSON is private0600; the sanitized result is in
`.agent-work/backup-catalog-actual-20261012/public-summary.json`.

The public backup source explicitly names `/src/host`, while this existing
metadata parser admits only descendants `/src/host/`. The failed reason makes
that declared-source boundary a concrete follow-up; it is not proof of actual
snapshot content or permission to widen accepted paths. Any corrected source
needs negative path tests and independent review before a new exact HOST query.
Backup availability and real restoration are still not accepted.

A subsequent read-only reuse audit found that the approved v2 scanner execution
sources were not preserved when the old SEC01 worktree was removed. This was a
cleanup error: preparation receipts remain, but execution is blocked until the
exact sources are recovered or a current source is freshly reviewed. The missing
operator/contract hashes are c033adbefbeeb6d43c4112384060b7f73469b645a0cab8d12f63cc20aac822c2
and 33f3dcdf19e7ef69567fb48736a06b22ba326dee91374d53cfb4ca6927169961.
The preserved preparation receipt aadc48beb745dae295d51be7129b2e8fa06d243a179a9e769f1a93c5724cabc6
and 8/8/2 subject manifests are input evidence only. The permanent sample-service
script is sample-specific and cannot substitute for the ROOT batch scanner.
A fresh memory observation shows approximately 15 GiB available, so the earlier
12 GiB host-admission failure is historical, not the current blocker. No native
scan was executed after this discovery, and no replacement source is admitted
under the old hashes.

Current ledger advisory applicability and complete image/dependency scan
coverage remain unaccepted. Checked upstream advisory ranges alone cannot
certify an image or its embedded packages clean. Actual ROOT patch/deployment,
P01 authentication/custody, complete backup/restore and P04/P05 native receipts
keep their own unresolved boundaries. SMTP01/CLN01 accepted delivered scope
and P09 preparation remain accepted; no new LAB execution is added.

### Current warning-only ROOT audit — 2026-10-13 KST

The current direct SEC01 request, reiterated as latest-main execution, restricts
future image changes and scanner corrections to confirmed current ROOT-image
security warnings. It supersedes the preceding stable-update continuation for
future work only; its historical observations and completed Tasks are preserved.
Criterion 15 and W31 remain the sole acceptance owner. SPEC and Plan already
state this restriction and are NO_CHANGE. The security-updates README still
allowed blanket stable updates; only that conflicting prospective text changes.

Fresh `git fetch origin main` succeeded twice. Remote main and the isolated
`codex/sec01-warning-audit` input are
`328871a94b42c13f676e61b40f026c906ebbc13d`; the original supplied baseline is
`23e37362b72e98028a4675f282819c0346ae59dc`. The user's original checkout was
clean at `98144b2c0b5738f272b6a628246c901945ba15bf`. All six other existing
worktrees were observed clean and preserved, including both SEC01 worktrees.
GitHub connector open-PR search returned no open PRs. The original-to-current
diff includes Stage 05 document moves, source reconciliation and already
delivered n8n/Renovate projection changes; it does not authorize replaying them.

The existing `expected_from_root` helper independently recalculated 111 services
from 44 public Compose inputs, with manifest SHA-256
`957a9ac7be7d4519107490fc5183a63d093d4afcfd4f5933326f7005c633cb29`.
Submitted ROOT rows have no missing/unexpected services. Source comparison
identified 12 stale image declarations in the evidence ledger: Dozzle, Mailpit,
four n8n services, Ollama, Open WebUI, Renovate, two Stalwart services and
Traefik. Build-only rows without an image field retain UNKNOWN; they are not
evidence of missing services. Current-source metadata reconciliation does not
refresh supplier releases, authenticate packages or promote old candidate
digests, running metadata or tests to a new result.

| Surface / consumer | Current classification | Target / recovery boundary |
| --- | --- | --- |
| Existing ROOT Compose, Dockerfiles, version projection and controls | SOURCE_APPLIED / NO_CHANGE | No image bump, profile/network/role/secret or data change; existing source rollback remains with its owning commit |
| Current-source ledger declarations and README scope | CONFIRMED_GAP | SEC01 is the sole writer; preserve previous evidence and revert this increment's logical commit for source rollback |
| Qdrant source and internal gRPC authentication | NO_CHANGE for GHSA-3gph-6c29-p29v version range | Source already selects the official fixed release; current image package scan and native authentication remain unverified |
| SeaweedFS filer TUS authorization / S3 consumers | SECURITY_WARNING_CONFIRMED at vendor version-range level; source mitigation NO_CHANGE | Advisory has no patched version; source disables unused TUS while retaining filer/S3; effective HOME mitigation is RUNTIME_UNVERIFIED |
| MNG metadata/queue and DEV business data / P04-P05 | NO_CHANGE / CONSUMER_DEPENDENT | Preserve separate roles, networks, secrets and backup owners; no new consumer or native receipt |
| ROOT signature, SBOM and current Grype DB scan | NOT_RUN | Authenticated scanner subjects, fresh validated DB and a preserved independently reviewed ROOT execution route are required |
| LAB runtime, learning apps, Wiki implementation | OUT_OF_SCOPE | No LAB resource mutation or native activation; completed Wiki preparation stays NO_CHANGE |

Fresh read-only Docker observation used `/usr/bin/docker`, explicit
`unix:///var/run/docker.sock`, a new empty client configuration and a minimal
environment. Server metadata returned exit 0, Linux/amd64. ROOT-label discovery
and bounded Config.Image/Image/State/platform/RepoDigests reads found 63 current
ROOT containers: 59 running and four exited. This is a new observation, not a
copy of the old `current_running` fields. No Env, secret, auth file, raw log,
private data, daemon container execution, restart or deployment was read/run.

Qdrant currently reports `v1.19.1-unprivileged`, config/image ID
`sha256:801777072776dc81b2a9dd2007b2ed487571f21ecd30efffd15ddb1671f2193d`.
Its source already selects 1.19.2, outside the advisory's affected range
`>=1.18.0,<1.19.2`. This proves a source-level fixed-version selection, not
the current image's packages or effective internal-auth setting. SeaweedFS
filer reports 4.47, config/image ID
`sha256:ce9e796f1fe6f06968f4c04bdaf8f678dad9c8acdfef3d244133d71bfa6bf882`;
source selects 4.48, within the advisory range `>=4.39`. Both disclosures
were freshly read from their official vendor advisories:
[Qdrant GHSA-3gph-6c29-p29v](https://github.com/qdrant/qdrant/security/advisories/GHSA-3gph-6c29-p29v)
and [SeaweedFS CVE-2026-77368 / GHSA-99q7-x53r-6j4g](https://github.com/seaweedfs/seaweedfs/security/advisories/GHSA-99q7-x53r-6j4g).
The SeaweedFS advisory lists no patched release. The attack concerns
cross-prefix authorization on an existing TUS upload session, requiring a
valid filer write JWT and another session's identifier. A boolean-only Args
query did not observe the explicit `-tusBasePath=` flag on the running filer;
absence of that flag does not prove TUS is enabled or that this attack path
is reachable. No active exploit or private JWT/config query occurred.

Fresh public `docker buildx imagetools inspect <pinned-index> --raw` queries
both exited 0. Response SHA-256 matched the requested indices. Qdrant index
`efb96a9425a90d2d5a1a0a474156280df1892dcdf1af3e8515bd2589b1bfd88b`
selects Linux/amd64 manifest `390ca16351185f9913c23d0c95ded0cdf2ce17e525dd7fbe58d3339c9c80e633`;
SeaweedFS index `4e61d15fd35994cb1e43e1e553dff106794841fd9a99ade2fc8c8bfce4d7872d`
selects manifest `aba492e2a4e4c90bff795745e8e660affa1f09e7650f5981bd7bccd1a06cd931`.
These are public descriptor/integrity receipts, without publisher signatures,
layer pulls, SBOM or native execution. The metadata wrapper's first cleanup
failed because buildx populated its owned client directory; separate exact-path,
owner-checked cleanup exited 0. No Docker service resource was created.

No Syft, Grype or Cosign executable is on PATH. Historical authenticated
extraction receipts do not establish that their subjects or a fresh database
are currently available. The preserved Task records missing ROOT scanner
operator/contract sources; the registered sample-service scanner cannot replace
that ROOT route. Current scan absence remains UNKNOWN / NOT_RUN, not a clean
verdict. No scanner, gate, skip policy or exception is changed.

HOME rollout, data-format migration, rotation, empty restore and real recovery
remain NOT_RUN. The next runtime target is the current ROOT Qdrant/filer
artifact and its owning S3/internal-auth consumers, but a concrete consistent
backup, empty-restore proof, exact artifact scan and approved per-target rollout
contract are still required. Start with the existing value-free read-only
image/flag observations above; stop on digest mismatch or absent recovery input.
No source revert or image tag downgrade guarantees data restoration.

Verification, independent review and delivery receipts for this increment are
recorded below when actually executed; Task status remains in-progress because
global security/native/recovery acceptance has not been achieved.

#### Current source verification and independent review

All following source checks bind main `328871a94b42c13f676e61b40f026c906ebbc13d`
plus the five-file increment. No Compose, Dockerfile, version projection,
scanner, network, role, secret or dependency source changed. The ledger's new
source-only refresh exposed a second test assumption: the old candidate test
treated the last refresh as a vendor lookup. RED reproduced its missing
`public_metadata_receipt_sha256` error. The correction selects the newest
receipt-bearing refresh, retaining exact historical receipt/source assertions;
an independent removal probe still failed with StopIteration. No old vendor
receipt was attached to the new source observation.

| Command / check | Exit | Actual result and limit |
| --- | --- | --- |
| `python3 -m unittest tests.lib.supply_chain.test_update_gates.UpdateEvidencePackageTests.test_current_rows_match_root_compose_source -v` before reconciliation | 1 | RED: exactly 12 stale declaration failures |
| `python3 -m unittest tests.lib.supply_chain.test_update_gates -q` after reconciliation | 0 | GREEN: 26 tests; current declaration/build comparison has zero mismatches |
| `python3 -m unittest tests.validation.test_sec01_next_tool_candidates -q` before/after selector correction | 1 / 0 | RED: KeyError; GREEN: eight tests; independent missing-receipt probe still fails |
| Existing six-module bundle: `test_grype_db_seed`, `test_supply_chain_policy`, `test_sec01_version_contract`, `test_sec01_next_stable_candidates`, `test_sec01_next_tool_candidates`, `test_workflow_version_bundle` | 0 | 86 tests, three native skips, before the appended source-only refresh; later affected module replay above supersedes its candidate-selector slice |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.SeaweedfsContractTests -q` | 0 | Four source mitigation tests; no native TUS/S3 test |
| `bash scripts/operations/sync-tech-stack-versions.sh --check` | 0 | Current projection matches tracked images; one required OPSFLOW image remains an unresolved operator input |
| Empty-client `docker compose --env-file .env.example --profile core --profile seaweedfs --profile qdrant config --quiet` | 0 | Public example-only static render; no private .env, up or secret creation |
| `python3 -m scripts.lib.supply_chain.latest_version_gate --input infra/09-platform-ops/security-updates/update-ledger.json` | 2 | BLOCKED_EVIDENCE: ready=false, no missing/unexpected ROOT rows |
| `python3 -m scripts.lib.supply_chain.security_update_gate --input infra/09-platform-ops/security-updates/update-ledger.json` | 2 | BLOCKED_EVIDENCE: 111 blocked rows, no missing/unexpected services; no current CVE scan |
| `python3 scripts/validation/run-ci-gate.py --profile changed --local-only` | 1 | FAIL, retained below; not an aggregate PASS |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 328871a94b42c13f676e61b40f026c906ebbc13d` with the two changed document paths | 0 | Two selected documents, zero violations |
| `ruff check` and `ruff format --check` on the two changed test modules; `git diff --check` | 0 | Scoped deterministic source checks |
| `uvx --offline --from commitizen==4.15.1 cz check --message-length-limit 75 --message 'fix(sec01): Reconcile current root security evidence'` | 0 | Actual repository-pinned Python Commitizen; PATH's unrelated Node cz first rejected the options and created no commit |

The local aggregate completed supply-chain fixture policy (265 tests),
Conftest policy (18 tests) and document links (1,272 documents, 11,439 links,
zero failures). Links retained one baseline warning: 2,870 legacy historical
links have no capture source and remain unverified. The Compose regression
leaf ran 628 tests with 71 explicitly optional native skips, three failures
and one error. It stopped the aggregate before repository-integrity regression
execution; that leaf is NOT_RUN, not PASS. The diagnostic replay used the same
registered module set and reproduced the same four failing IDs without native
opt-ins. The two changed SEC01 modules were separately GREEN after the fix.

Two failures were local checkout permissions: Open WebUI and Gatus entrypoint
files had mode 0775, although their Git modes are 100755. Only these two
current-user-owned files in the new SEC01 worktree were restored to 0755;
their targeted permission tests passed, exit 0, with no tracked diff. The
remaining unchanged failure is
`QualityObservabilityContractTest.test_locust_lab_is_not_claimed_as_root_observability_coverage`
(Grafana README lacks the test's literal LAB disclaimer). The unchanged error is
`LabInventoryAndSelectionTests.test_each_lab_guide_names_exactly_its_project_and_services`
(the test still opens absent `labs/supabase.md`). Both reproduced in a clean
detached checkout of the exact latest main, two tests, exit 1. These are
existing public documentation/contract debt, not new image warnings or current
remediation. No LAB runtime, image, secret, data or native test ran, and neither
test was skipped or weakened to manufacture an aggregate PASS.

Independent code review approved the original four-file slice and the later
candidate-selector delta, with no findings. Independent security review initially
blocked the stale selector, then approved the corrected five-file diff with no
findings. Both reviewers independently replayed the relevant 26/eight tests;
security recomputed all 44 include hashes without a mismatch. Their approval
covers this metadata/docs/test increment only, not ROOT vulnerability remediation
or HOME acceptance. Current remote protection read-back has zero required
approval count, CODEOWNERS enforcement false and empty required contexts/effective
rules. All five paths still route to `@buenhyden`; no human approval is invented.
The produced candidate-quality and external checks still require actual hosted
observation before any requested source merge; no protection setting changed.

The reviewed five-file index passed
`bash scripts/validation/run-ci-precommit.sh --mode local-staged`, exit 0,
including Markdown, JSON, Ruff and the hardcoded-secret guard. Ordinary commit
`256d5f833af0ead3287832bac9278e1d42aecabc` and
`git push -u origin codex/sec01-warning-audit` both exited 0. The observed
pre-push hook reported no supported checks; that skip is not a QA receipt.
[PR #428](https://github.com/buenhyden/hy-home.docker/pull/428) was opened
against main `328871a94b42c13f676e61b40f026c906ebbc13d` with that head and
attached to the current chat. At this receipt's observation, candidate-quality
run `38273509572` and CodeQL were IN_PROGRESS, GitGuardian was SUCCESS and
PR-context main-security was SKIPPED; GitHub reviews were empty, consistent
with the verified zero-required-approval setting. No final hosted PASS or merge
is inferred. This result-only Task receipt requires its own staged check and
latest PR head CI; prior-head observations are not reused as current acceptance.
Source rollback is a revert of this increment; because no deployed artifact/data
changed, it provides no HOME data recovery.

#### Commit ledger for the current increment

| Commit | Owner / scope | Actual disposition |
| --- | --- | --- |
| `256d5f833af0ead3287832bac9278e1d42aecabc` | SPEC-0204 / W31; five metadata/docs/test paths | Committed and pushed to PR #428; hosted candidate pending at the observation above |
| `eaacf6bb0eb5225471db10ecbff5f2b47517a857` | SPEC-0204 / W31; result-only Task receipt | Staged style and secret guard passed again; committed/pushed, exact-head independent review approved |

Before source merge, fresh check-runs read-back for `eaacf6bb0` confirmed
candidate-quality run `38273774053` SUCCESS, CodeQL including all three Analyze
checks SUCCESS, and GitGuardian SUCCESS. PR-context main-security remained
SKIPPED, not a ROOT scan. A simultaneous `git fetch origin main` found main had
advanced to `9fd0a396c4e0246be778c90fb5ef31435c08e977`. Its only changed path
since the source input was TSK-0007's delivered CLN01 evidence; ROOT Compose,
image/build inputs and the SEC01 five-file source boundary were unchanged.
The coordinator integrates that published main through an ordinary merge,
preserving the other Task body. This receipt records the successful earlier
head, not the new merge head's CI: the updated PR still needs actual latest-head
candidate results, independent evidence-delta review and current-main read-back
before source merge. All blocked local/security and NOT_RUN operational states
above remain unchanged.

### Selected OpenBao Artifact Inspection — 2026-10-14

The user explicitly prioritizes actual OpenBao issuance/upgrade within the
latest authorized operations request. This bounded inspection covers only
source candidate2.7.1 linux/amd64, not all111 ROOT services or the current
2.6.2 runtime. Source main was `1e7e2ba841c4e428a06762a61a570011711bc1ef`.
P01 records the exact publisher-signature verification: index
`sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf`
passed the official `release-images.yml@refs/tags/v2.7.1` identity and GitHub
Actions issuer checks. That signed index's unique amd64 child is
`sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005`,
config `sha256:8b664b4dd46db74a327e373f7b9581e39a1447b7d788b9b69f664896683c14d5`.

Authenticated Syft1.54.1 and Grype0.120.1 archive/binary hashes were verified
against the existing public tool-readiness receipts before execution. Direct
isolated CLI phases used readonly rootfs, no Docker socket/auth/config or
private data mount, all capabilities dropped/no-new-privileges, PID64/CPU1/
memory2GiB/swap2GiB and300-second bounds. SBOM registry extraction exited0
in28.355s:320 packages,985,738 bytes. Exact index/embedded manifest/config/
platform/eight diffIDs and Grype artifact IDs matched. SBOM SHA256:
`48105d750eb7da5017b5731f7372db4b8d336e3a7aa5ec4fc7179061d5ac6930`.

The first public vulnerability DB download failed because its64MiB temporary
filesystem filled. That FAIL is preserved. The narrow retry used temporary
space inside the already-owned public DB cache, with the same resource bounds,
and exited0 in175.605s. Offline DB status was valid, schema v6.1.10, built
2026-10-13T06:35:20Z (about17hours old). Offline SBOM scan exited0 in12.315s,
no OOM:49 matches/29 unique IDs, Critical3/High20/Medium13/Low8/Unknown5.
Grype output SHA256:
`0372f266feaa849b8ed9cbf6256ed024570c916cb02557407b10623ce4b29196`.
All seven invocation-owned containers were removed. Exact argv/client and
container exits, bounds, cleanup and binding receipts remain in the exclusive
public scratch directory `/tmp/hyhome-p01-selected-image-security-20261014`.
Its sanitized immutable `selected-artifact-summary.json` SHA256 is
`846f2ff0efcc4652eff850034e8f195c5574b5e84d245f756e2210338214760e`.

Independent security review verified those three hashes and scoped the two
unique Critical IDs behind the three matches. Official
[GO-2026-6612](https://pkg.go.dev/vuln/GO-2026-6612) applies to this Linux
server: tagged listener advertises h2 and TLS server calls `http.Server.Serve`,
so the vulnerable flow-control/refund path is reachable. Evidence supports
buffer-budget bypass/resource exhaustion, not RCE or disclosure. Its x/net
match is duplicate package evidence; it is not a second unique Critical.
[GO-2026-6604](https://pkg.go.dev/vuln/GO-2026-6604) concerns Windows junction
handling and is not applicable to linux/amd64. The selected binary uses
Go1.27.1 and x/net0.58.0; reported fixed versions include Go1.27.2 and
x/net0.60.0. Other matches are not silently dismissed or fully triaged here.

Security acceptance of this exact official2.7.1 artifact is BLOCKED. It must
not be deployed. Remediation is a vendor artifact with fixed dependencies or
a separately reviewed reproducible owned rebuild with exact source/toolchain
provenance, SBOM/scan and native/recovery evidence. The latest official release
still resolved to2.7.1 at this observation; no accepted replacement was found.
A broad upgrade request is not residual-risk acceptance. The existing ledger
is not rewritten as globally complete, and criterion15 stays pending.

#### Owned OpenBao reproducibility and local import — 2026-10-14

The owner-selected patched build uses signed/authenticated source/toolchain/base
and offline package materials c60926e2. The failed r3/r4 attempts remain in
TSK-0006. Two clean independent r4-attempt2 Go compilations produced identical
binary f0b103b853891539cfe4c01421074077de8b3665b189ecbe3159f7966d876a51
and build-info77b26c30d4d08d41ffb13dad917d73ed98482c898166d9c6100cf7403c12990f;
their whole images failed solely on APK installation wallclock log contents.
R5 source packetc3183267 adds global --no-logfile to the offline recipe.
Independent code/security/IaC approved its seven source hashes and the fixed
one-time action v2 freeze3d966dae, runner78dcadfe and literal launcher31a2dc01.
The actual argv used env-i absolute isolated/no-site Python with the reviewed
runner embedded in memory, never executing a mutable scratch pathname.

The admitted action ran once, exit0. It reused the two independently held and
verified r4 compiler outputs, copied them into separate exclusive files, and
performed two fresh r5 runtime assemblies. Both phase receipts passed with no
OOM and exact-created-ID removal. This is explicitly compile
REUSED_VERIFIED_R4_NOT_RUN, not a new r5 Go compilation or resumed r4 success.
Both normalized layers, config, manifest and full OCI archive bytes match;
apk.log is absent. The final public output uses1,898,971,809 bytes, under4GiB,
with the16GiB filesystem reserve preserved. Independent post-run IaC accepted
the artifact for scan and pinned import only.

| Artifact namespace | Exact SHA-256 |
| --- | --- |
| OCI archive, both191989760-byte independent files | e8b42840819cfbbcb81c3753ad9a0ae4ec7191b35e2ddc9f9eab205fb6646bbc |
| OCI manifest | 46bf9b5c3ae3d26b89f18bb131b8a1ff67c6fedbd25b0cd158b9b1edae891e2e |
| OCI config | 7ee363935e49f667e408afda590dbc60182cea82587fea3a94a1d8a74586e1d1 |
| Uncompressed OCI layer/diff-id | c5d8fbcc0e7a364df2f93193b6524cba8ee10b0dab76213060972abbf656be74 |
| Runtime-only lineage receipt | 7001b288816e3474dd28a38b3c642f735474cc8fd0a2aefb6faa992599ced074 |

Root independently checked held archive FD/path signatures, raw descriptor and
layer hashes, linux/amd64 identity and exact R4-binary/R5-runtime/material labels.
Proof files remain in `/tmp/hyhome-p01-selected-image-security-20261014`.
A single Docker import succeeded under its digest reference, but the first
import validator failed because it assumed the version tag was imported too.
The expected absent owned local tag was then explicitly attached to the same
already imported manifest, without a second load. Actual Docker29 local ID is
the manifest46bf, distinct from OCI config7ee; both the tag and tag@manifest
resolve to46bf. No remote image push or HOME service change occurred.

The first isolated version probe used the wrong /bin/bao path and failed; the
reviewed owned recipe installs /usr/bin/bao. The corrected probe's CLI exited0,
without stderr, and returned the exact owned version, upstream revisiona5db72c
and committed2026-10-01T13:32:54Z. Its validator still failed because it expected
the word built rather than the observed committed. Both original FAIL receipts
remain. A separate pure validator accepted the already recorded exact version
and client exit without another container execution; it does not invent
unobserved Docker state fields. Both exact probe IDs were removed.

Fresh owned SBOM/CVE scans and independent applicability acceptance are still
NOT_RUN at this receipt. The reviewed R5 scan plan is public/offline only and
binds the accepted archive/OCI namespaces. An accepted reproducible build,
import or version string alone does not clear official-image GO-2026-6612 or
admit HOME deployment. candidate_signed_by_upstream_openbao remains false;
upstream signed inputs and owned provenance are separate evidence.

### Declared-versus-running service versions — 2026-10-14

At main7f4c364f, public Docker metadata identified63 project containers:
59 running and4 exited jobs. Thirty match the exact declared local image ID
(including the four exited jobs),32 running healthy targets differ, and one
build-only oauth2-proxy identity is unresolved. Five unlabelled k3d containers
and48 declared-but-unobserved services are excluded from deployment. All107
explicit source image references already match the current version projection
and ledger declarations; this work concerns runtime drift and does not invent
new source version bumps. Public inventory SHA256
5a7a8563f667e6109d5f8a01232deff7cfbca41936cfc37b1bd923e579267749;
its exact32-target analysis SHA256
a990bb49a15e17e1f90c6459508d5ea672a845cd5a3e1f40dd8f53aae59e1597.

The first scoped candidate is MNG valkey-exporter: running redis_exporter
v1.91.1-alpine to declared v1.93.0-alpine index93831cd4, amd64 child5eac4c83.
DEV is a separate later canary. The reviewed direction reuses authenticated
Syft/Grype and existing artifact identity checks, then proves config parity,
native compatibility, exact rollback identity and both Prometheus
up{job="mng-valkey-exporter"}=1 and redis_up{db_scope="mng"}=1.
The public exporter admission plan SHA256 is
fec62095dcd46389b54e0ea8b17eb31e48eab547bdc367641dc83d1c081613b6.
No exporter deployment or fresh candidate SBOM/CVE/native test has run yet.

Read-only publisher research found unsigned BuildKit provenance bound to the
selected child, but no publisher signature/DSSE/SBOM or GitHub subject
attestation at the investigated index/child routes. A verified Git commit and
release archive checksums do not authenticate the different OCI build.
Existing sample-only exceptions are not a production waiver. Concrete fresh
scan/compatibility evidence and independent security disposition must precede
any owner decision on the remaining publisher-authentication residual.

### Actual owned scanner preparation attempt1 — 2026-10-14

After final code/security/IaC approval of action59287064 and33 synthetic tests,
ROOT executed exactly one new-output public/offline attempt. The action exited3
CREATE_RECOVERY_UNPROVEN during db_status create validation, operation
 e65c3188e57f59cf05271b31144b7046:db_status. Exact temporary ID
1e8fe413f849ebd7d437b8f8d2e242f3f7c0e5c87d563c06189d010982c49844
remained created and never started. The validator incorrectly compared Docker's
Env list to only the explicit variables, omitting the signed runner's three
public inherited values and assuming list order. No DB/Syft/Grype process ran.

ROOT obtained independent scoped cleanup review, re-proved exact ID/name/nonce/
image, never-started state and resource/mount/command contract, compared the
full duplicate-free environment map to the exact public runner base plus five
explicit variables, then removed only the full ID without force. Name and
ID filtered lists both returned exit0+empty. The existing attempt output with
two public config files and original failed source remains preserved.
Reconciliation receipt SHA256:
06b1bc8d934df8fdc500e6e7dede11eb57cd64da35fe7014f90f1d6385f2173f.
The already-authenticated exact runner image's public base Env observation is
bound by receipt4311db3c4b3add74e3262be9a914180c4a2b59e571e125eab881797453655305;
it is a ROOT byte observation, not a newly generated publisher signature.

A corrected fresh-output source packet is being prepared and must receive its
own exact review. Actual SBOM/CVE acceptance and HOME deployment remain
NOT_RUN. ROOT also found a related subset-only Env check in the as-yet-unrun
MNG exporter operator; independent security review classified it an action
blocker. Its correction requires full exact Env-map equality and negative
regressions before any exporter execution. The MNG scan/deploy remains NOT_RUN.

### Actual exporter observation and clean-main metadata comparison — 2026-10-14

MNG selected exporter r4 source received exact code/security/IaC action review.
ROOT independently replayed27 synthetic tests, then executed the frozen
launcher9620b06a once. The actual invocation exited0 PASS_OBSERVATION_ONLY.
The64MiB-bounded cached export produced8340992-byte archive SHA256
8349ba2914df08d19664e6c01ca67ac0915d45041eacacc96e0ce57093064035.
Exact index93831cd4, selected child5eac4c83/config8d339939, all three compressed
layers and uncompressed diff IDs were bound. Actual Syft, DB status and Grype
ran offline in the resource-limited pinned runner with exact-owned cleanup.

Public receipt SHA256:
1cca5d86a0cf95fd7bb9183218aff182406e431c874de9fe013b3e9fa1de4511.
SBOM SHA256:
143c83f7c4399f300e266878ccdd842837e337c679ccde96aa0f2c513cfa38fd.
Raw Grype reports44 findings (2 Critical/17 High/13 Medium/8 Low/4 Unknown),
including stdlib Go1.27.1 GO-2026-6612 and GO-2026-6604. Raw package matches
are not proof of applicability to the actual Linux service. Independent
primary-source applicability review is pending. Publisher authentication is
still UNSIGNED_PARTIAL_NOT_ACCEPTED. Native compatibility, configuration
parity, residual acceptance, exporter deployment and metric postchecks remain
NOT_RUN. No Valkey data/credential/init/ACL was read or changed.

Owned OpenBao scan attempt2 passed DB status and Syft, publishing raw SBOM
7f4d8865684adaca230f6509fae436c18e7eebd9695ebab13749ebf8df27d98d.
Grype creation then exited with the action's CREATE_RECOVERY_UNPROVEN because
the namespace transform left the Grype SBOM bind at the absent original output
path. The exact operation label and exact derived container-name filtered lists
both returned exit0+empty. Grype never started by reviewed source sequencing;
its original Docker create exit was not captured and is not invented.
Reconciliation SHA256:
1556ee78c6ebc476bf8dbaa9e68acd28138bd3f62a6760eb3ee2d065813c2aba.
The failed attempt and its successfully published raw DB/Syft outputs remain
preserved. Correcting all derived output paths requires a new source freeze,
review and fresh output; actual owned CVE acceptance is still NOT_RUN.

The build README documentation-only correction passed focused registry body/
frontmatter validation, links, markdownlint and independent review. Its new
SHA256 is7f2870a1b42988afea695d2e6dc400e973b6122d3c400b8beb264b9ba39e5b98;
original c318 README is retained at
/tmp/hyhome-openbao-build-readme-c318-before-doc-only-20261014.md,
SHA256 f953dd2726c8926671c1d54fb185c3b76a2bbeb80c887a35f09f7781fc19ae16.
This does not claim a rebuilt artifact or change historical recipe evidence.
A read-only metadata comparison on clean main7f4c, selecting unchanged
archive migration0001, also exited1/type-mismatch (selected1/violations1).
At least that archive finding predates this work; remaining corpus findings
are not waived. Final registered quality gates remain pending.

### Actual owned OpenBao full scanner attempt3 — 2026-10-14

The corrected all-caller output namespace received exact independent code,
security and IaC approval. ROOT independently ran34 tests, then executed
frozen actionbcb9db285c4cc2ddef3dacf52833aeb2736e45335d2ef2618ada498f11f2a53e
once in the new owned-oci-scan-r5-attempt-3 directory. Actual action exited0
OWNED_OCI_SCAN_R5:PASS. DB status, Syft and Grype each recorded client0,
container0, noOOM, exact-owned cleanup0 and post-removal full-ID absence.
No HOME service, private credential or deployment was involved.

Public scan receipt SHA256:
8008dbf39afbc51968fdf9b5fbec32d50fe3ddec2fe22a153ffc10ff6a0566a9.
Raw SBOM SHA256:
7f4d8865684adaca230f6509fae436c18e7eebd9695ebab13749ebf8df27d98d.
Raw Grype SHA256:
d729f6a20d1d231ca83de3c8f879901825a944199e13ece62cd828382b90c59f.
The archivee8b42840/manifest46bf9b5c/config7ee36393/layerc5d8fbcc binding,
320 Syft packages, all six required runtime Go module versions and all28
actual APK versions passed. Effective scanner visibility retained matches and
ignoredMatches with no user excludes, VEX or hidden matcher suppressions.
The public output before receipt was996170 bytes under96MiB.

Result:0 Critical,0 High,3 Medium package matches of CVE-2025-60876
(busybox/busybox-binsh/ssl_client1.37.0-r31) and1 Unknown module match
GO-2026-5932 (x/crypto0.57.0),0 ignored. GO-2026-6612 is absent on the
patched Go1.27.2/x-net0.60 runtime. Independent primary-source applicability
review of the two remaining unique IDs is pending. This is successful native
scan transport and coverage, not yet candidate security acceptance or HOME
upgrade. The original failed attempts remain retained without promotion.

### Owned candidate admission and current native status — 2026-10-14

Independent security review admitted the owned OpenBao source candidate for
the next bounded native validation. The full scan receipt remains
8008dbf39afbc51968fdf9b5fbec32d50fe3ddec2fe22a153ffc10ff6a0566a9:
0 Critical,0 High, three Medium BusyBox-family matches for CVE-2025-60876 and
one Unknown `golang.org/x/crypto` match for GO-2026-5932. Review confirmed that
the legacy `x/crypto/openpgp` path is absent and the source uses ProtonMail's
implementation. The dormant `wget` Medium residual remains. This admission
binds authenticated build inputs and reproducible owned provenance; it is not
an upstream OpenBao signature or a HOME deployment acceptance.

Current source pins both OpenBao service image references to the owned
manifest46bf9b5c, includes renderer issuance helper5c809c1e and the corrected
TLS-material check, aligns the affected fixtures, and projects the owned pin in
the shared tech-stack data. The focused RED run produced one failure and three
errors. After the source correction,39 tests ran:35 PASS and four explicit
native-opt-in SKIPPED. A fresh native validation then started and observed the
expected full-audit denial with HTTP500 before completion. Its input SHA256 was
d1c59476085763d99798413c402e4fe4d8341ab8fe45fc76b84eee6281db65af.
The final invocation ran13 tests in276.386 seconds:11 PASS, two ERROR and no
skips. Candidate native TLS expiry, audit and snapshot checks and the diagnostic
path passed. Both the native full rehearsal and versioned issuance stopped at
wrapping line540 with `RehearsalFailure: native interrupted issue exact cleanup
failed`. The result is FAIL and unresolved while ROOT diagnoses the synthetic
helper boundary. There is no aggregate native PASS, deployment, issuance or
HOME change to record.

The first actual failure receipt SHA256 is
555afd88b549ff79502a4074eeac10e236b6aa802c4e38d1e5eb0b27aa5754a5.
Diagnosis found `BAO_TLS_SERVER_NAME=openbao` missing only from the synthetic
fixture. The focused RED regression failed once before the correction. After
the minimal fix, Ruff passed and the combined suite ran74 tests in24.939
seconds:70 PASS and four native-opt-in SKIPPED. Independent IaC and security
review approved the exact Runbook version0.10.2 and fixture. The single reviewed
native rerun used fixture input SHA256
2fa9f8b2439d9970ced72cc968567a6066620564c2869709a44b7b15f0f67b73 and
exited0 after454.043 seconds:13/13 PASS, no skips, including all four native
tests. Public log SHA256 is
2466d19f23c35067841b89bf1081e15497f453320d5ced4074d4cdad6675db39;
ROOT observation receipt SHA256 is
2995a9891c7d8bc12550d2b140b8d8ba068f4759e380688cae29466387bdb1a8.
The first FAIL remains historical evidence rather than being promoted. The
second PASS resolves the synthetic fixture failure only and does not establish
HOME custody or deployment.

The MNG exporter observation's44 findings now have a security disposition that
blocks official deployment. GO-2026-6613 is High and its HTTP/1 CONNECT path is
reachable through the selected exporter health/source path. A Go1.27.2 owned
rebuild is the recommended remediation and remains pending. No exporter image
was deployed and no exporter post-deployment metric acceptance ran.

### Owned OpenBao applicability dispositions — 2026-10-14

This follows up the "pending" applicability review recorded under attempt3.
On the owned binary `f0b103b853891539cfe4c01421074077de8b3665b189ecbe3159f7966d876a51`,
extracted read-only from manifest `46bf9b5c`, `go version -m` lists
`golang.org/x/crypto` v0.57.0, `github.com/ProtonMail/go-crypto` v1.4.1 and
`github.com/cloudflare/circl` v1.6.3. `go tool nm` finds 0 symbols under
`golang.org/x/crypto/openpgp` and 568 under
`github.com/ProtonMail/go-crypto/openpgp`; the x/crypto packages present
are acme, argon2, bcrypt, blake2b, blowfish, cast5, chacha20,
chacha20poly1305, cryptobyte, curve25519, hkdf, internal/poly1305, ocsp,
pbkdf2, pkcs12, scrypt, sha3 and ssh, with their subpackages.
`govulncheck` v1.1.4 `-mode=binary` on the same binary reports 0 symbol
and 0 package results and one module result, GO-2026-5932 in
`golang.org/x/crypto@v0.57.0`, fixed in N/A; it lists no entry for
ProtonMail go-crypto v1.4.1.

- **GO-2026-5932** (<https://pkg.go.dev/vuln/GO-2026-5932>, published
  2026-07-07): every symbol of the seven `golang.org/x/crypto/openpgp`
  packages, all versions, no fix; it recommends the ProtonMail fork. Its
  summary, as govulncheck prints it, reads "The golang.org/x/crypto/openpgp
  package is unmaintained, unsafe by design, and has known security
  issues". Disposition: not affected, because the packages are absent from
  the binary.
- **CVE-2025-60876** (<https://security.alpinelinux.org/vuln/CVE-2025-60876>):
  BusyBox wget through 1.37.0; the Alpine tracker lists `busybox`
  1.37.0-r31, the image's version, as possibly vulnerable in every branch
  including edge, with no fixed version. The three matches (`busybox`,
  `busybox-binsh`, `ssl_client`) are the same package and its wget HTTPS
  helper, and the "dormant wget residual" is this same item. No OpenBao
  entrypoint, start, health or backup script runs `wget` or `ssl_client`,
  and the image entrypoint script contains no `wget`. Disposition: affected
  but unreachable. No fixed package version exists; a rebuild could still
  drop `ssl_client` and the `/bin/wget` applet link to remove the surface,
  though the scanner would keep matching `busybox`. It waits for owner
  acceptance.

Both OpenBao ledger rows now carry these URLs and dispositions in
`advisory_urls` and `applicability`. An independent security-auditor
review on 2026-10-14 approved both dispositions with notes: it re-checked
the symbol listing and the absence of any wget or `ssl_client` caller, and
asked for the rebuild option, the advisory summary and a symbol-aware
binary scan, which are recorded above. The rows are marked as awaiting
owner acceptance. The latest and security gates exit 2 before and after
the change. No owner acceptance, HOME change or criterion decision is implied.

### Owned OpenBao SEC01 image acceptance — 2026-10-14

After the review above, the owner was asked, through the interactive
question in this session, whether to accept three residuals of owned
manifest `46bf9b5c`: no image signature, CVE-2025-60876 (BusyBox wget,
unreachable, no fixed version) and the GO-2026-5932 not-affected
disposition. The owner answered "3건 모두 수락" (accept all three). This
accepts the image's residuals for the window only. Criterion 15 stays
pending on the other open gates, the fresh stable lookup before
2026-10-17 is still required, and no HOME change follows from this record.

### Fresh OpenBao stable lookup — 2026-10-14

The fresh lookup due before 2026-10-17 ran on 2026-10-14 at 14:22 UTC:

- GitHub releases list OpenBao v2.7.1 (2026-10-01) as the latest stable,
  the release the owned image `46bf9b5c` rebuilds; v2.6.4 is the newest 2.6
  patch.
- go.dev lists go1.27.2 as the latest Go, the toolchain the image uses.
- The Go module proxy lists `golang.org/x/net` v0.61.0 and
  `golang.org/x/crypto` v0.58.0 (both 2026-10-09), newer than the image's
  v0.60.0 and v0.57.0. In the Go vulnerability database index the newest
  x/net entries are fixed in v0.60.0 and the newest x/crypto entries in
  v0.56.0, so neither newer release carries a fix this image lacks.
- `govulncheck` v1.1.4 `-mode=binary` on the owned binary again reports no
  symbol or package vulnerability and only the module-level GO-2026-5932
  match already dispositioned above.

Both OpenBao ledger rows now carry this `checked_at`. The latest and
security gates still exit 2 for the other open evidence; no HOME change
follows from this record.

## Evidence

The following table preserves the as-received source-only slice and earlier
coordinator repair inputs. It is historical; the current authorized continuation
and its later observations are recorded above.

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SEC01 source and isolated receipts | 15 | W31 | Received six-commit source, focused tests and isolated rehearsal | Recorded branch/input hashes in integration handoff | PASS | security-updates handoff | - |
| Common validator and manifest state | 15 | W31 | Current shared suite and manifest registration | 20 PASS/2 FAIL; two records missing | FAIL | integration handoff | - |
| Reviewed ROOT stable/security evidence | 15 | W31 | Existing stable-version and security-disposition gates | Current ROOT source set; no completed reviewed security ledger | DEFER | Resumed stable-version and ROOT ledger reconciliation | - |
| PR #416 candidate CI | 15 | W31 | candidate-quality, CodeQL, GitGuardian and main-security | Run `38052766613`; candidate-quality failed | FAIL | PR #416 handoff | - |
| Coordinator shared repair | 15 | W31 | Runtime/wiring, inventory, manifest and candidate regression registration | e93e0c822 plus reviewed integration; 93 and 39 tests exit 0 | PASS | #coordinator-common-repair-receipt | Common validator and manifest state, PR #416 candidate CI |
| Public Cosign release bootstrap | 15 | W31 | Offline wheel preparation, TUF refresh, OpenSSL-before-execution, KMS/keyless verification and version | Public receipts under `/tmp/hy-home-sec01-trust.*`; bounded public v3.1.3 binary only | PASS | Public Cosign Bootstrap Receipt | - |
| Public tool publisher checks | 15 | W31 | Two exact OCI subjects and Syft/Grype release checksum authentication | Five actual exits 0; reviewed operator and immutable receipt recorded above | PASS | Public Tool Publisher Authentication Receipt | - |
| Authenticated scanner versions | 15 | W31 | Exact authenticated archive extraction and isolated version-only execution | Syft/Grype exact version/source/platform, client and container exits 0; 11.827 seconds | PASS | Authenticated Scanner Extraction and Native Version Receipt | - |
| HOME, migration, rotation and recovery | 15 | W31 | Initial source-only slice had no operational authorization; later direct authorization covers bounded continuation | Exact per-target execution and acceptance remain pending; read-only observations are recorded above | NOT_RUN | Current TSK-0009 and per-operation contracts | - |
| Selected OpenBao subject and SBOM | 15 | W31 | Authenticated Syft; exact signed-index child/config/platform/diffIDs binding;320packages/exit0 | childa36ea8; SBOM48105d75 | PASS | Selected OpenBao Artifact Inspection — 2026-10-14 | - |
| Selected scanner DB preparation failure | 15 | W31 | First owned64MiB tmpfs download filled and exited1 | Grype0.120.1 exact authenticated binary | FAIL | Selected OpenBao Artifact Inspection — 2026-10-14 | - |
| Selected scanner DB and execution | 15 | W31 | Owned-cache retry/valid fresh DB/offline scan;exit0/noOOM/49matches | summary846f2ff0; Grype0372f266 | PASS | Selected OpenBao Artifact Inspection — 2026-10-14 | Selected scanner DB preparation failure |
| Selected OpenBao security applicability | 15 | W31 | Independent official advisory/tagged server-path review: applicable GO-2026-6612; Windows-only GO-2026-6604 excluded | exact childa36ea8 Go1.27.1/x-net0.58.0 | FAIL | Selected OpenBao Artifact Inspection — 2026-10-14 | - |
| Owned OpenBao packaging reproducibility | 15 | W31 | Two independently verified R4 compiles and two new R5 runtime assemblies; exact fullOCI equality, apk.log absent, independent post-run IaC acceptance | R5packetc318; actionfreeze3d966dae; manifest46bf | PASS | Owned OpenBao reproducibility and local import — 2026-10-14 | - |
| Owned OpenBao import and version validator assumptions | 15 | W31 | Initial absent-tag assumption; wrong /bin/bao path; built vs actual committed output expectation; original failures retained | acceptedmanifest46bf, public exact receipts | FAIL | Owned OpenBao reproducibility and local import — 2026-10-14 | - |
| Owned OpenBao local identity and recorded version | 15 | W31 | One import, absent owned tag attached, tag@digest resolves; separate pure validation of existing exact owned version/client0, exact probe cleanup | archivee8b428/manifest46bf/config7ee | PASS | Owned OpenBao reproducibility and local import — 2026-10-14 | Owned OpenBao import and version validator assumptions |
| Owned OpenBao applicability dispositions | 15 | W31 | Read-only module and symbol listing and govulncheck binary scan of f0b103b8; independent security review APPROVE with notes; primary advisories GO-2026-5932 and CVE-2025-60876; ledger rows updated; gate exits unchanged | Owned manifest 46bf9b5c | PASS | Owned OpenBao applicability dispositions — 2026-10-14 | - |
| Owned OpenBao SEC01 image acceptance | 15 | W31 | Owner decision on the three residuals of manifest 46bf9b5c | Reviewed dispositions above | PASS | Owned OpenBao SEC01 image acceptance — 2026-10-14 | - |
| Fresh OpenBao stable lookup | 15 | W31 | GitHub releases, go.dev, Go module proxy, Go vulnerability index and govulncheck binary scan: v2.7.1 and go1.27.2 current; newer x/net and x/crypto carry no fix the image lacks; ledger `checked_at` refreshed | Lookup 2026-10-14T14:22Z | PASS | Fresh OpenBao stable lookup — 2026-10-14 | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 15 | pending | - | - |

## Review and Completion

Before delivery, integrate only reviewed common changes through their assigned
single writer; regenerate the version projection after preceding SMTP/CLN work;
run the registered changed gate, current common validator/inventory/manifest
checks, existing ROOT latest-version/security-disposition gates and independent
security/code review at that head. A fresh successful stable-channel query with
no newer release needs no version bump. Preserve failed, blocked and unknown
results; source/latest evidence does not prove a deployment. For remaining
future SEC01 work, use the owning-Spec PR after exact-head CI and independent
review; historical local-main receipts remain unchanged.
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
