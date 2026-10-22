---
title: "Cross-tier Contracts Second Round Task"
version: "0.6.13"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0005"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-08"
---

# Cross-tier Contracts Second Round Task

## Overview

### Objective

Re-run prompt 04 against the current tree: observe authentication, workflow,
CDC and backup state on the HOME host, close the source gaps that can be
proven with tests, and name each remaining gap with the owner action it needs.

## Inputs and Authorization

The current user request on 2026-10-08 asks to execute prompt 04 of the
analysis pack ("connect authentication, variables, workflows and backup
across tiers") with per-unit commits and a per-Spec PR merge, reusing
SPEC-0204. The request takes precedence over this package's earlier
source-only limits, so read-only HOME observation and isolated containers
are in scope. HOME data changes, realm changes, credential issuance and
image pulls onto a 90%-full disk are not. Baseline `main` `f88eb6601`; the
branch was rebased onto `670b39e53` after PR #386 (SPEC-0215) merged.

The direct 2026-10-10 SMTP01 integration request authorizes W26–W30 source,
synthetic isolation, logical commits and owning-Spec delivery. Private retirement
requires separately established exact operator facts and remains NOT_RUN.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0005 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0005 | ready | in-progress | #coordinator-required-regression-registration |

### W8 Baseline, Owner Map and HOME Observations

Files this round writes, and the owners whose work it must not overwrite:

| File | Owner it touches | Reason |
| --- | --- | --- |
| `infra/09-platform-ops/restic/bin/hyhome-backup.sh`, RUN-0021 | SPEC-0204 TSK-0003 | Adds the dev-valkey export next to mng-valkey |
| `infra/02-auth/keycloak/docker-compose.yml` | SPEC-0204 TSK-0001 | Wrapper refuses empty secrets |
| `infra/secret-file-support.json` | New | Per-image verdicts |
| `tests/validation/test_service_runtime_compatibility.py`, `test_compose_baseline_gates.py` | SPEC-0204 | New regressions |
| RUN-0070 | SPEC-0204 contract 10 | Mail outcome states |

SPEC-0213 (DEV data), SPEC-0214 (quality) and SPEC-0215 (LAB, merged as
PR #386) own none of these files. POL-0078 is read, not written.

HOME observations, read-only, 2026-10-08:

- **OIDC.** From inside `oauth2-proxy`, the discovery issuer equals its
  configured issuer, `S256` is offered, JWKS holds two keys (RS256 `sig`,
  RSA-OAEP `enc`) and an end-session endpoint exists. The realm also offers
  `plain` PKCE and the implicit and password grants. Of the nine `home-*`
  clients, all are confidential with implicit off; only `home-airflow`
  allows the password grant; `home-airflow`, `home-dozzle`, `home-grafana`,
  `home-kafbat` and `home-proxy-client` have service accounts; none enforces
  PKCE on the server. Client fields were read with a field-limited `kcadm`
  query; no secret was printed.
- **Browser and machine paths.** Unauthenticated Grafana returns 302 to
  `/login` in a browser and 401 JSON on its API. Airflow's root returns 200
  with its own login page, which is not API success. User A to B denial was
  not run: no test users exist.
- **n8n.** `n8n`, `n8n-worker` and both runners run 2.41.6 in queue mode
  with `N8N_RUNNERS_TASK_TIMEOUT=300`. Compose, both Dockerfiles and the
  tech-stack row already share one version, and an existing test pins it;
  Renovate is off for both images. Upstream stable is 2.42.5, released the
  same day; the pin is kept.
- **Airflow.** The worker, not only the scheduler, resolves its metadata DB,
  broker, result backend, Fernet key and API JWT secret through `_CMD`; the
  API server resolves the Keycloak client secret. No DEV DB or S3
  connection and no DAG is tracked, and `AIRFLOW__CORE__LOAD_EXAMPLES` is on.
- **CDC.** `cdc` is not in the HOME selection. `dev-pg` has no
  `platform_dev` database, Kafka Connect has no connector, and Schema
  Registry holds four heartbeat subjects under the old `hyhome.app` prefix,
  while the tracked connector uses `hyhome.platform`. The connector and
  provisioning names are already pinned by an existing test.
- **Backup.** `dev-valkey` had no backup. OpenBao has no snapshot job, and
  OpenSearch has no snapshot repository.
- **Images.** No active Compose file, LAB or Dockerfile uses a Bitnami image.

### W9 Dev-valkey Snapshot and Queue Replay

The nightly run now exports a `dev-valkey` RDB as the `devadmin` ACL user
under the same 300 s in-container limit as `mng-valkey`, drops a partial
file and fails the run on error, and skips a stopped DEV. An export from
HOME `dev-valkey` returned 212 bytes (the DEV store is empty). In an
isolated `valkey/valkey:9.1.2-alpine` pair with no network, a key and a
stream with a consumer group were exported with `--rdb`, loaded into a new
container, and came back with both stream entries and the one pending
entry; `XAUTOCLAIM` handed that entry to a new consumer. RUN-0021 states
that replay is at-least-once. The new assertion failed against the previous
script (RED) and passes now. Commit `abcc1d7a7`.

### W10 Secret File Support Matrix

`infra/secret-file-support.json` gives each of the 73 image and key pairs
in the rendered root a verdict:

| Verdict | Pairs | Evidence |
| --- | --- | --- |
| native | 23 | Upstream source at the pinned tag, or a HOME runtime signal: `pg_up 1`, a Grafana admin login with the file password, Airflow values resolved non-empty |
| wrapper | 5 | The repository entrypoint or Compose command that reads the file |
| unsupported | 45 | The Supabase stack (35, Kong and PostgREST included), Terrakube (9) and SonarQube (1) images ignore the key |

The Supabase stack also gives GoTrue, Storage and Supavisor no database URL,
so it cannot start as declared; PostgREST's native form is `@file`, and
Terrakube's is Spring `configtree`. These services are outside the HOME
selection, and the new test keeps every unsupported key there and fails on a
key without a row. Two mutations, a removed row and a HOME service marked
unsupported, each fail the test.

The Keycloak wrapper now refuses an empty admin or database password; with
an empty mounted file the exact image exits 1 before `kc.sh`. Commit
`4630384fe`.

### W11 Image Residue and Mail Outcomes

A test refuses any `bitnami/` image across tracked Compose, LAB and
Dockerfiles; it failed after a Bitnami base was injected. Commit
`ea6c69d59`. RUN-0070 separates accepted, delivered, failed and unknown per
recipient, ties retries to a fixed `Message-ID`, and keeps Mailpit as
capture only. Commit `b84b2b87c`.

### W12 Validation and Handoff

The changed-profile local gate ran in a throwaway worktree holding the
branch diff against `670b39e53` as staged changes, with the checkout's group
write bits cleared. It selected the docs-traceability, supply-chain fixture,
conftest, Compose baseline and repository integrity leaves and exited 0
(689 tests, including the four new ones). Its 23 skips are the opt-in Docker
rehearsals; the backup rehearsal covers pgBackRest and Restic round trips,
not the Valkey export, so it was not run for this change.
`pre-commit run --from-ref origin/main --to-ref HEAD` exited 0.

### Third Round Inputs

The user pasted prompt 04 again on 2026-10-08 after PR #387 merged at
`b0a72d2e5`, which this round reads as a request to close the open items.
The owner had freed the host disk to 64%, so image pulls and the OpenSearch
LAB rerun became possible. Branch `claude/spec-0204-round3` started at `b0a72d2e5` and was rebased onto
`fb468bba5` after PR #389 (SPEC-0215) merged.

### W13 OpenBao Raft Snapshot

The nightly run reads a token from
`secrets/backup/openbao/snapshot_token.txt`, passes it on stdin, renews it
and saves a Raft snapshot to staging. Policy `backup-snapshot` grants only
`read` on `sys/storage/raft/snapshot`. With the exact image in isolation:

| Case | Result |
| --- | --- |
| Token absent | Gap message, run not failed, no file |
| Valid periodic token (`-period=720h`) | Status 0, snapshot written, token renewed |
| Wrong token | Status 1, file dropped |
| Sealed vault | Status 1, file dropped |
| Scoped token reads a secret | Denied |
| Restore into a fresh node | Comes back sealed; original unseal key and root token return the synthetic secret |

The test fails against the previous script and passes now. HOME OpenBao was
sealed again when observed, and no token exists yet, so HOME runs report the
gap until the owner creates one (RUN-0021 gives the steps). Commit
`4ef6d3f7d`.

### W14 Open WebUI Key

The image sets `WEBUI_SECRET_KEY` empty, so `start.sh` generated the key in
the container layer and each recreation replaced it. `WEBUI_SECRET_KEY_FILE`
now points into the data volume, and the state allowlist includes the key
next to `uploads/`; `webui.db` already comes from the SQLite export. In the
exact image two containers on one volume kept the same key. The first HOME
recreation after this change logs users out once. Commits `06d2a8953`,
`b325dec30` (matrix row).

### W15 CDC Stream Rehearsal

`CdcStreamRehearsalTests` (opt-in `HYHOME_CDC_REHEARSAL=1`) runs dev-pg,
Kafka, Schema Registry and Connect on an internal network with synthetic
data. It provisions with the tracked SQL and registers the tracked connector
with a password holding Properties-significant and non-ASCII characters. It
passed in 260 s:

- snapshot and streamed rows decode through the registry;
- an added column registers schema version 2;
- after a worker restart the stream resumes from its offset, so ids 1 to 5
  each appear once;
- the heartbeat writes its row and advances the slot's flushed LSN.

Topics have three partitions, so order holds only per key. Commit
`619c984cb`.

### W16 Gateway Machine Path

A machine client with `Accept: application/json` got the same 302 to the
Keycloak login page as a browser on every route behind `sso-errors`, and a
client that follows redirects would read a 200 login page as success.
`SsoRehearsalTests` (opt-in `HYHOME_SSO_REHEARSAL=1`) runs Traefik,
oauth2-proxy built from its Dockerfile and Keycloak with a synthetic realm,
the tracked middleware and the tracked proxy config. Against the previous
middleware the machine client got 302 (RED). ForwardAuth now calls the
oauth2-proxy root with its static upstream and `sso-errors` handles only
403. The rehearsal then passed:

- a browser gets 302 with PKCE `S256`, state and the tracked callback;
- a JSON client gets 401 JSON;
- the group member gets 200 with the identity header and a `Secure`,
  `HttpOnly` cookie, and sign-out returns her to the redirect;
- the non-member is refused at the callback and gets no cookie.

The dynamic directory is live on HOME, so the change applied on write. HOME
then showed 302 to Keycloak for browsers and 401 for JSON on Qdrant and
Schema Registry, with the same authorize parameters; Grafana, which has its
own login, was unchanged. A signed-in HOME session was not exercised. The
unused `sso-auth-open-webui` middleware is retired. Commit `e342aaa9d`.

### W17 SonarQube Secret

The image ignores `SONAR_JDBC_PASSWORD_FILE`. A wrapper now reads the
secret, refuses an empty one and execs the image entrypoint. In isolation
with PostgreSQL and a password holding spaces and symbols, SonarQube created
its JDBC source and passed its UTF-8 charset check against the database,
which needs a successful login; it had not reported `UP` within 450 s on the
loaded host. An empty secret stopped the container before start. Commit
`a677d609c`.

### W18 Validation

The changed-profile gate ran in a throwaway worktree holding the branch diff
against `fb468bba5` as staged changes. Its runs exposed three things:

- Before the rebase, the lifecycle check saw SPEC-0217, merged meanwhile, as
  removed; rebasing onto `fb468bba5` cleared it, and `main` itself has no
  violation.
- The compose baseline leaf accepts a skip only from a declared optional
  runtime class, so the two new rehearsals were added to
  `.github/workflow-contract.yml` (`5001c7896`).
- The contract test pins the number of those classes; it now counts seven
  (`9bf20d195`).

The final run exited 0 with 911 tests across the selected leaves.

### W26–W30 SMTP01 Current Increment

The current 2026-10-10 request supersedes only active contradictory contracts;
W8–W18 above remain historical evidence. Baseline main/origin/main/HEAD was
`a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`, initially clean. The requested
analysis baseline is `860ac1c3633eac9ad416fb1abd8a61a6e617ebd8`; applied OpenBao
PR #409/#410 source is preserved. Current branch is `codex/smtp01-canonical`
in `/tmp/hy-home-smtp01`. The shared original tree is not reset or stashed.

SMTP01 owns source/consumer/catalog/generator; SEC01 owns versions/images;
CLN01 owns the final duplicate deletion after transition. Common Compose,
catalog, validation and Spec/Plan/Task changes are handed to the integration
coordinator and are not independently merged. Actual HOME deployment, private
comparison/metadata rewriting/unlink, rotation and real restore are NOT_RUN.

| Lane | Decision | Current evidence and limit |
| --- | --- | --- |
| SOURCE | IMPLEMENT | One canonical root source, preserved auth target; Alertmanager and SMTP account parameters unchanged |
| UNIT | IMPLEMENT | Source RED then GREEN; model/retirement tests include immutable inputs, drift, collision, equality, mismatch, symlinks, races and no secret output |
| STATIC | IMPLEMENT | Synthetic Compose selection and existing metadata/manifest/document/gate checks; final commands below |
| ISOLATED | IMPLEMENT | Digest-fixed GoTrue/Mailpit/PostgreSQL fixture; native baseline and wrapper evidence separate |
| HOME | VERIFY_RUNTIME | NOT_RUN; integration coordinator controls selected activation; full Supabase is not enabled |
| MIGRATION | VERIFY_RUNTIME | NOT_RUN; no actual file comparison/private catalog changes; CLN01 verifies source/runtime/job/backup/external facts |
| ROTATION | NO_CHANGE | NOT_RUN; no password or account change |
| RECOVERY | VERIFY_RUNTIME | NOT_RUN for real Restic recovery; canonical-only source/consumer rollback is documented |
| DELIVERY | IMPLEMENT | PR #412 merged; PR #413 open on main; latest-head implementation delivery remains pending |
| Wiki and batches | OUT_OF_SCOPE | Wiki preparation and independent opsflow_dev batch are later owning work; no engine/app created |
| LAB runtime and learning apps | OUT_OF_SCOPE | No service/data/image/credential change or learning-app investigation |

The only eventual unlink target is
`/home/hyunyoun/data/hy-home.docker/secrets/communication/supabase/supabase_smtp_password.txt`.
The owning operator must supply host, current source SHA, exact public Compose
input hashes, zero old-mount consumers, verified job/backup/external consumers
and canonical restore mapping in the sanitized receipt described by RUN-0029.
The receipt records operator attestations; structural checks do not verify
their truth or authorize execution by themselves. Current
integration instructions hold deletion to CLN01/the coordinator. The helper
rejects mismatches, links and source drift, preserves canonical bytes and other
private rows, and rewrites COMM-003 only as a two-column alias before unlink.
No persistent plaintext recovery copy is created. Existing encrypted backup
custody and an actual selected restore remain unverified; no recovery PASS is
inferred from tests. Restore/revert scope is canonical mapping plus the affected
consumer, with no entire-stack restart, volume initialization or bulk rotation.

#### Current session ownership and interfaces

SMTP01 reserves criterion 14 and W26–W30 in this isolated increment. The
integration coordinator owns the intervening allocation: CLN01 criterion 12/W24
and P09 criterion 13/W25. Their bodies are not duplicated here; gaps remain
until the owning changes are integrated.

The resumed user instruction keeps `gen-secrets.sh` and the SMTP helper under
SMTP01 alone. CLN01's initial SMTP draft was selectively read, not applied:
it changed the container target to `smtp_password` and kept SMTP unsupported.
The accepted contract preserves `supabase_smtp_password` as the target and
promotes only SMTP to `wrapper` after exact-image proof; other unsupported
Supabase keys and whole-platform readiness remain unresolved.

SEC01 supplied the final read-only GoTrue contract in its handoff: v2.197.0,
OCI index sha256:1736a63078f5922b198c4cbe50f80ab9a2d3b54fe8b7b6cfb2e9dc5dbbc12c6b,
linux/amd64, USER supabase (uid 1000), Entrypoint null and Cmd auth. It matches
the frozen rehearsal fixture. The coordinator ran the current integrated
fixture again: 10 PASS in 48.635 seconds, exit 0, on e7bff9149 with e93e0c822
merge inputs; helper d6b8c9c1, Compose 6a9c289a, fixture 794e314f. This is
ISOLATED evidence and does not prove latest-version, security or HOME migration
completion. P09 writing belongs to the separately assigned sole writer under
SPEC-0204-TSK-0008; SMTP01 authors no P09 package or production Wiki client. Its future interface is COMM-002 ownership, the canonical
file and service-specific render of the same entry. COMM-003 remains a value-free
alias; future OpenBao render must not create another SMTP value.

SMTP01 apply binds the exact actual root identity to its persistent
`secrets/.smtp01-retirement.lock`. CLN01 uses a separate lock; the compatibility
probe acquired both and therefore failed. CLN01 rejects COMM-003 by ID and exact
path, leaving SMTP01 as its sole proposed unlink executor. No shared-lock
interoperability or operational exclusion is accepted from that probe.
The receipt adds `root_identity` (device/inode), `consumer_creation_quiesced`
and `source_private_mutation_quiesced`. These are facts, not authorization; the
operator must freeze the exact consumer-creation and public/private writer paths.
Current host quiescence, backup/restore and external consumer evidence are UNKNOWN.
Current actual comparison, lock acquisition, apply and deletion are NOT_RUN.
RUN-0029 owns partial-failure handling and exact named-host recovery boundaries.

#### Coordinator proof and isolation replacement

The coordinator merged main `e93e0c8223191bf26aea7578a231b2dbf016fc7c`
into the received `e7bff9149f29a4bbb23d977dadf01f5988ee12fc`, preserving
SEC01/CLN01/P09 sources and uncommitted changes in their separate worktrees.
The merge commit is `8fc5f8089`; common-file delivery remains coordinated.

Independent review found the earlier retirement receipt accepted stale,
unowned/symlinked proof and an unverified read-only Restic parent mount. New
negative tests reproduced 17 failures against the old reader; a malformed
COMM-002 duplicate also failed its focused regression. The replacement requires
an external owner-only descriptor-read receipt with exact unique JSON keys,
operation/target, observation/expiry, clean tracked HEAD/index and no old-path
ancestor mount. Documentary approval identifiers are not authentication.
RUN-0029 uses a fresh unpredictable `mktemp` directory. It no longer claims
CLN01 and SMTP01 share a lock; CLN01's COMM-003 ID/path hard hold prevents a
second executor. Same-UID noncooperative writes, private authority authenticity,
complete live consumers and actual backup/restore facts remain unverified.

The frozen helper is
`e00cbb01c73a6d4364d72f245585c3fa587431ecf3010392a39617a15f361b4b`;
existing unit is `72c22ebc73216eee1dd1d87b2c33bca2db27aea22fa896b3ed8cfea65cae937f`;
new proof unit is `e2ab26793ed38ff1e828737201411574372b02ab579eeca800b1c968463bab0e`;
RUN-0029 is `61ba24acedee6128f3bbde46abef90aaaa5ea2933a0061aa528563b81051d98a`.
The coordinator and independent reviewers ran
`python -m unittest tests.lib.ops.test_smtp_contract tests.lib.ops.test_smtp_proof tests.validation.test_smtp_generator -q`:
45 PASS, exit 0. Helper coverage replay: statements 94.81 percent, branches 89.38
percent, combined 93.21 percent (540 statements,
28 missed; 226 branches, 24 missing). This is
not a native/HOME claim.
Ruff, size and diff checks passed; every modified source function has fewer
than 50 lines and files fewer than 800.

The rehearsal fixture was separately refactored without changing its public API
or startup contract. Replacement hash is
`141341830bc2aa1e40b984d51b50dc686e77899278b843b534f0bddd68cc997d`.
The coordinator ran `HYHOME_SUPABASE_SMTP_REHEARSAL=1 python -m unittest tests.validation.test_supabase_smtp_rehearsal -v`
on the current merged inputs and frozen fixture: 10 PASS, exit 0, 52.076 seconds.
This supersedes the historical 48.635-second coordinator run on fixture 794e314f.
Compose hash remains `6a9c289a24c1bc2a0e4b846dddf2719bc917595de2c21734d80003a2188dedf9`;
GoTrue index/USER/Entrypoint/Cmd match SEC01's read-only contract. This uses only
owned temporary synthetic resources; actual HOME/private comparison, catalog
mutation, COMM-003 deletion, rotation and real recovery all remain NOT_RUN.

#### Operational continuation — 2026-10-10 UTC 14:45–14:50

The user authorized full SEC security plus SMTP/CLN retirement and recovery
continuation, including investigation of backup facts. Read-only observations
found root HEAD `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b` with 23 foreign dirty
paths preserved, the SMTP integration worktree clean at `06a5` before QA, and
main `a42` after externally merged PR #419 at 14:41:59 UTC. PR #413 head
`06a5` and PR #417 head `0e696` are not merge-ready while fresh CI has a
CodeQL HIGH synthetic-fixture write-permission finding under repair. These are
continuation facts, not delivery acceptance.

Read-only Restic evidence is sanitized: an encrypted repository configuration
exists on `/home/hyunyoun/storage/backups/restic` (2.75 TB free), while the
local state path is on the OS disk; the password-file reference is
`secrets/backup/restic/restic_password.txt`; Restic consumed the key through its
read-only file mount, and no value or secret-content hash was printed. The
selected snapshot is `cea13cbd8b1569d9e7a6359122e9f81d48e3d8aade3b5a54c3f89170aa4761de`
from 2026-10-08T19:00:51.270866861Z, tag `hyhome-host`, path `/src/host`.
It lists canonical and old SMTP paths as regular uid/gid 1000, mode 0640,
size 20, without recording content or a content hash. Read-only snapshot,
list and `check --read-data` exited 0 with no errors after an initial UID-1000
permission failure; a pinned cached Restic 0.19.1 image (config
`sha256:136600b6ff6843d61d355f7f71f460a166429f35de6fd11b568fece3c9a4d510`),
read-only repository and password mounts, `--pull=never`, no network/cache/lock,
dropped capabilities plus
`DAC_READ_SEARCH`, and no-new-privileges then completed the read. This proves
snapshot readability only. Independent offsite key custody is `NOT_RUN`.

The current `hyhome-backup` service last failed around 03:35–03:36 KST; its
timer is active with next run 2026-10-11T03:34:20KST. The selected snapshot is
about two days old, so the 24-hour RPO objective is not met; the 300-second RTO
is unobserved. Read-only ancestor mounts by node-exporter and cAdvisor remain
and require exact-container removal without volumes in a later window; they are
not evidence of quiescence. No private comparison, catalog mutation, deletion,
runtime update or actual restore has run.

The initial bounded recovery proposal below was not executed and is superseded
by the exact FIRST contract recorded later in this section. It remains historical
input, including its former destination and inadequate host-quota wording.
The first bounded recovery action remains `NOT_RUN` pending independent
readiness review. The direct user authorization from `buenhyden` covers actual
SMTP/CLN recovery and investigating these exact backup facts; it is distinct
from the review and is not being requested again. Create only if absent the
exclusive mode-0700 target
`/home/hyunyoun/storage/backups/smtp01-recovery-20261010T145500Z`; restore only
the canonical and old SMTP paths from the selected snapshot into that empty
owned target; use one exact pinned container with the encrypted repository and
password mounts read-only, no network/cache/lock, target only writable, a
300-second and 1-MiB limit; then verify owner/mode and silent expected-value
equality without outputting a value or hash. Preserve a partial target for
quarantine on failure and never delete it automatically. This would prove only
bounded file recoverability, not provider SMTP authentication, HOME restore,
pre-delete freshness or independent key custody. The root coordinator executes;
an independent IaC reviewer reviews readiness; `buenhyden` is the separate
human approver under that direct authorization. Actual retirement stays blocked by a clean root,
fresh full backup, five-axis/external-consumer evidence and quiescence.

#### Current bounded continuation receipt — 2026-10-11

The actual read-only SMTP `--retire-check` receipt exited 1. It recorded
`applied=false`, equality as true and retirement as pending; it did not apply,
delete, rotate or expose either value. This is a precondition result, not
evidence that the old path is retired.

The native replacement frozen inputs identified by the coordinator as `3fa1`,
`7e1` and `6a06` passed 21 tests, including six native cases, in 51.189
seconds. Independent code and security review passed for that frozen source
input. The result is SOURCE/UNIT/ISOLATED evidence only; it does not prove
provider SMTP authentication, HOME activation, recovery or retirement.

Current backup-directory usage is 5,377,096 KiB, below 8 GiB after cleanup.
The historical journal guard had triggered at 8 GiB and `snapshot_missing` is
true. This is neither free capacity nor a quota: read-only host evidence remains
2.75 TB free on the backup disk and 54 GB free on the system disk. The FIRST
proposal has passed canonical v3 review; this Task does not assert a 1 MiB
global quota.

The prospective FIRST procedure v1.1/v3 and a separately generated Claude
projection are owned in the recovery-review worktree on
`codex/first-restoreability-review`, based on `abe2`. Its exact prospective
files are `.agents/skills/stateful-recovery-contract-review/SKILL.md`,
`.agents/skills/stateful-recovery-contract-review/assets/verdict.md`,
`.agents/skills/stateful-recovery-contract-review/references/recovery-contract.md`
and `.claude/skills/stateful-recovery-contract-review/SKILL.md`. The v1
historical readiness remains `BLOCKED`; logical blockers 3 and 2 were fixed,
and independent rules and IaC v3 review passed on reported inputs `891ff…`,
`9d114…`, `15ee…` and `8406…`. Production strict-default behavior remains
verbatim and no operational readiness is inferred. FIRST restore is `NOT_RUN`
until its concrete execution contract, independent review and a separate
SPEC-0204 policy follow-up PR are complete.

Full restore and apply remain `NOT_RUN`. The existing v1 readiness is
`BLOCKED`; the exact FIRST attempt below requires its independent readiness
verdict and reuses the matching current direct user authorization. No additional
approval is inferred from a Task field, receipt or CLI flag.

#### Exact FIRST attempt contract — observed 2026-10-10T16:17:49Z

The coordinator selects single-use attempt `smtp01-first-20261011T003500KST`
and the absent target
`/home/hyunyoun/storage/backups/smtp01-recovery-20261011T003500KST`.
This name identifies the attempt; it is not an asserted execution timestamp.
The earlier `smtp01-recovery-20261010T145500Z` destination is withdrawn and was
never created by this work. Selection follows the current user's full SMTP/CLN
recovery request and the direct reply delegating investigation of the repository,
snapshot and empty restore destination. These trusted chat messages, rather than
this structural record, supply authorization. Scope is one reversible isolated
file-usability attempt on the discovered current host, with no source, live
consumer, credential, external-host or production-destination write. The root
Integration Coordinator selects and implements; `/root/smtp_recovery_readiness`
independently reviews; the current user is the separate human approver. No
withdrawal is present. The exact sanitized contract SHA-256 is
`acb1e61d962f247fddb28102d8f2622698b688269a9e8659a08536e620fec142`.

Only the empty metadata ledger directory was created before review:
`/home/hyunyoun/storage/backups/smtp01-recovery-attempts`, device `2064`,
inode `174588180`, uid/gid `1000`, mode `0700`, observed attempt records `0`.
No attempt has been claimed and no restore has executed. At execution an
exclusive `<attempt-id>.claim.json` is created before starting; an exclusive
immutable `<attempt-id>.outcome.json` records every outcome. Neither record or
ID may be rewritten or reused. An existing target, container, claim or outcome
aborts. Receipt retention ends no earlier than `2026-11-10T16:10:47Z`.

The trusted parent `/home/hyunyoun/storage/backups` is device `2064`, inode
`174587905`, uid/gid `1000`, mode `0775`, non-symlink and resolves to this same
absolute path. Its primary group has one current host user and no supplementary
members. Free capacity observed is `2749703262208` bytes, independently of the
5,377,096-KiB state-directory usage. Recheck the parent, then atomically create
the target through its verified directory descriptor. Target device/inode,
uid/gid `1000`, mode `0700`, emptiness, stability, exclusivity and non-symlink
checks are `NOT_RUN_BY_DESIGN` during review and mandatory before restored bytes.

Bind snapshot
`cea13cbd8b1569d9e7a6359122e9f81d48e3d8aade3b5a54c3f89170aa4761de`
captured `2026-10-08T19:00:51.270866861Z` to the encrypted repository
`/home/hyunyoun/storage/backups/restic`: device `2064`, inode `174587911`,
uid/gid `1000`, mode `0700`. Its config is inode `174588179`, uid/gid `0`,
mode `0400`, nlink `1` on device `2064`. Key reference
`secrets/backup/restic/restic_password.txt` is device `64512`, inode `5276708`,
uid/gid `1000`, mode `0640`, nlink `1`; no key or secret content hash is
published. The project owner remains the named host-key custodian; independent
offsite custody remains `NOT_RUN`.

The fresh read-only cached Restic preflight completed at
`2026-10-10T16:17:49.403971Z`: `--no-lock --no-cache check --read-data`
exit `0`, then `ls --json <exact-snapshot>` exit `0`, duration `4.155` seconds.
Only sanitized selected metadata was retained. The exact two regular files are
`/src/host/secrets/communication/smtp/smtp_password.txt` and
`/src/host/secrets/communication/supabase/supabase_smtp_password.txt`, each
20 bytes, uid/gid `1000`, mode `0640`. Two earlier preflight attempts exited
`1` because the operator parser compared Restic's textual `permissions` field
to a numeric mode; using the documented numeric `mode` corrected the parser.
They neither changed backup data nor claimed a restore attempt. This proves
current integrity and metadata readability, not prior actual restoreability.

The snapshot is intentionally historical for this first exact artifact's
file-usability check. It fails the production 24-hour RPO objective and makes
no fresh current-state or quiesced live-capture claim. Configured local retention
keeps daily snapshots for 30 days; the scheduled backup does not forget/prune,
and those routes require separate confirmation. This attempt performs neither.
Immediately before any restore read/write, recheck source/config/key identities,
the immutable snapshot/tree and included two-file scope, full integrity and
read-only boundaries. Any mismatch or missing source aborts.
Hold an exclusive nonblocking flock on the existing read-only-opened
`/home/hyunyoun/backups/.hyhome-backup.lock`, device `64512`, inode `5296877`,
uid/gid `1000`, mode `0600`, to exclude the scheduled backup writer. No lock
replacement or backup-timer change is authorized by this attempt.

The source artifact remains read-only. The sole administrative source-side
effect is a native shared reader lease in
`/home/hyunyoun/storage/backups/restic/locks`, device `2064`, inode `174587918`,
uid/gid `0`, mode `0700`, non-symlink. Bind only that exact directory RW at
`/repo/locks`; repository config/data/index/keys/snapshots remain RO. Native
Restic may create temporary/final locks, fsync/rename, refresh and remove its own
lease. No broad `unlock` or orphan deletion is allowed. Private lock metadata
never appears in the receipt. Restore omits `--no-lock`: the same child holds
the native read lock from snapshot lookup through restore and `--verify`.
Normal forget/prune require an incompatible exclusive lock. The writer flock
also excludes scheduled append activity. Direct filesystem mutation or deliberate
protocol bypass remains a residual boundary; inspect active processes/routes and
abort on a detected conflict. An orphan lease means failed/partial quarantine.

Use only cached Restic `0.19.1` config
`sha256:136600b6ff6843d61d355f7f71f460a166429f35de6fd11b568fece3c9a4d510`
with `--pull never`, container `hy-home-smtp01-first-20261011t003500kst`,
network `none`, read-only rootfs, no-new-privileges, exact repository/key
read-only mounts, plus only the identity-validated native lock namespace RW,
and no Docker socket. Drop all capabilities and add only
`DAC_READ_SEARCH`, `DAC_OVERRIDE`, `CHOWN` and `FOWNER` for the root restore
process inside the tmpfs. Use only reviewed `/usr/bin/docker` SHA-256
`5fbf1d65d05315a4e89f561fee89731cec1f95094b86a56fac47e240edbf7bac`,
root-owned mode `0755`. Recheck the host uid/gid `1000` and exact observed
process groups `[4,24,27,30,46,101,989,990,1000]`; a former reference to zero
supplementary groups confused the group-1000 member list with process groups and
is corrected here. Parent owner/write group `1000` still has exactly one primary
account and no explicitly listed additional members. Use explicit
`--host unix:///run/docker.sock`, a new
empty current-owner mode-0700 client config and minimal PATH/LANG/LC_ALL. Do not
inherit Docker host/context/config/TLS credentials. The canonical socket is
device `26`, inode `2201276`, uid `0`, gid `989`, mode `0660`, type socket.
At `2026-10-10T16:48:01.179901Z`, the fixed local daemon was `29.8.2`, identity
SHA-256 `83cede88521d72b519a7349fef6c65914840fa8cca351169d0597c5d5799e3f7`.
Recheck the binary/socket/daemon identity before every operation; mismatch aborts.
CPU is `1`, memory `512 MiB`, PIDs `64`, `/tmp`
`16 MiB`, `/restore` `1 MiB`, work deadline `300` seconds plus a fixed `20`-second failure cleanup grace
(maximum `320` seconds). The measured RTO objective remains `300` seconds. Source
and target Restic are identical; there is no format migration. Runtime image,
mount, cap, memory/tmpfs and network checks must precede restore.

The exact Entrypoint is `[/bin/sh]` and Cmd is `[-c, exec sleep 86400]`.
This independent hold-alive process is PID1. Restore runs via `docker exec`
against the captured exact container ID as a child whose PID and `/proc` start
time are recorded in private tmpfs before `exec /usr/bin/restic`. Recheck
container identity before every exec, pause and success cleanup. On timeout,
validate child PID/starttime/exact NUL argv, send child-only TERM, wait boundedly
for deferred unlock, revalidate before KILL if needed, and confirm owned lease
removal or record an orphan. Then pause the same still-running container. Never
signal PID1; identity mismatch pauses without signaling. The 24-hour hold-alive
limit exceeds the existing independent failure review deadline. Ordinary
SIGINT/SIGTERM becomes categorical `INTERRUPTED`, follows bounded cleanup and
records an immutable outcome; defer repeated ordinary signals during cleanup.
Hard SIGKILL or host failure cannot create an outcome: the exclusive claim
consumes the attempt ID and requires coordinator quarantine review before the
24-hour hold-alive exits. Never present a claim-only crash as a complete receipt.

Restic receives no writable host destination. Execute
`restic --no-cache restore <exact-snapshot> --target /restore --verify`
with `--exclude-xattr '*'` and two separate `--include` arguments naming exactly
the two absolute paths above. Require only allowlisted ancestor directories and the two regular files;
reject links, devices, sockets, extra paths and oversized payloads. Verify each
20-byte file against Restic's encrypted metadata internally, then owner/mode and
silent pair equality as uid `1000`. No value or secret content hash is output.
Only the prevalidated exact regular files may be copied into owned mode-0700
host ancestors. Recheck target/container/source stability and require exactly
two files, total `40` bytes, uid/gid `1000`, mode `0640`, and silent equality.
There is no claim of a 1-MiB hard quota on the host filesystem; persistent payload
write is restricted to `2 × 20` bytes.
Record restored xattrs as `EXCLUDED_BY_DESIGN` and source xattrs as
`NOT_OBSERVED`; the fresh host leaves must return an empty `os.listxattr(fd)`
after final metadata changes. Any attribute, unsupported inspection or error
fails closed and preserves the partial output. No extra utility is installed.

On success remove only the owned utility container and retain the restored
private files plus immutable redacted receipt. Private cleanup is owned by the
coordinator, no earlier than `2026-10-11T16:10:47Z` and after receipt review,
limited to exact owned files/ancestors. On failure, timeout or partial result,
follow the validated child-only signal/wait/lease sequence above and pause
the owned non-`--rm` container to
preserve its bounded tmpfs; retain any already-copied target subset. Never copy
unexpected nodes or automatically erase quarantine. The coordinator reviews the
failure by `2026-10-11T16:10:47Z`, preserves immutable failure evidence and
escalates to the project owner. A retry needs a new ID and independent review.

The future receipt records actual start/finish/duration, all runtime identities,
checks, file count/bytes, limits and outcome without private payloads. Expected
acceptance is exact cryptographic file verification, paths/types/owner/mode,
count/bytes and equality. Actual outcomes are `NOT_RUN_BY_DESIGN`; no GoTrue,
provider SMTP authentication, HOME activation, today's canonical-value equality,
RPO/RTO result, custody proof or production recovery readiness is claimed.
Retirement still requires clean-root ownership reconciliation, a fresh pre-delete
backup and actual current-state restore, five-axis consumer evidence and quiescence.

The procedure-only PR #420 head
`ff289fbbb37a523f75550975fe0ac0de3c13fe02` has candidate-quality run
`38065653867` PASS, CodeQL PASS and GitGuardian PASS. Independent V3 rules/IaC
review covers the four exact procedure file hashes, not this new execution
contract. Independent five-file review also passed on that exact HEAD. The
coordinator merged it without bypass at `2026-10-10T16:22:01Z`, merge/main
`a31a38ca29ee8e0683a29e61bf41347bfddc3d62`, preserving both logical commits.
Procedure delivery and the execution verdict remain distinct gates;
this attempt remains `NOT_RUN` until its exact contract and operator review complete.
The earlier deadline-expiry finding was withdrawn: actual clock
`2026-10-10T16:33:08Z` precedes deadline `2026-10-11T16:10:47Z`. The native
reader-lease design was independently accepted in principle; this is not an
execution verdict or a successful restore receipt.

#### Command receipts

The source receipts below use synthetic fixtures or public tracked source in
this worktree. The dated operational continuation above separately records
read-only access to the real encrypted backup and planned private recovery.
Each receipt names its actual input HEAD; public file hashes identify uncommitted
candidates. Earlier PASS rows are historical, not fresh final-source evidence.

| Command | Exit | Result and scope |
| --- | --- | --- |
| `python3 -m unittest tests.validation.test_service_runtime_compatibility.RuntimeCompatibilityTests.test_supabase_smtp_wrapper_consumes_file_and_preserves_arguments` | 1 then 0 | RED against previous source, then wrapper unit GREEN |
| `python3 -m unittest tests.validation.test_smtp_generator -q` | 1 then 0 | Two generator regressions RED then GREEN |
| `python3 -m unittest tests.lib.ops.test_smtp_contract -q` | 0 | 17 tests and 43 subtests; synthetic retirement only |
| `uv run --with pytest --with pyyaml --with pytest-cov python -m pytest tests/lib/ops/test_smtp_contract.py --cov=scripts.lib.ops.smtp_contract --cov-branch` | 0 | Reported aggregate coverage 94%; no private files |
| `python3 -m unittest tests.validation.test_secret_metadata_sync -q` | 0 | 46 scanner/catalog tests |
| `python3 -m unittest tests.validation.test_supabase_smtp_rehearsal -q` | 0 | Final fixture: 4 unit PASS, 6 native SKIP by default; opt-in receipt below |

#### Historical Worker Source and Delivery Receipt

The three initial independent regressions and later fixture failures were genuine
FAIL results. Service-less includes and duplicate definitions now fail closed;
retirement rechecks source/runtime before and after mutation and preserves raced
metadata with NOREPLACE quarantine. Synthetic wrong-password and bad-TLS cases
must report an explicit SMTP failure, not a database or transport failure.

Native fixture failures were corrected in the fixture: BusyBox HTTP EOF cancelled
the request, the synthetic database search path omitted the migrated auth schema
(SQLSTATE 42P01), and startup-rejection cases looked up an already exited
container. A later independent review reproduced a cleanup gap after Docker
create timeouts; its two regression tests were RED before intent registration.
The final fresh rehearsal receipt is recorded after that correction, below.
None of those FAIL runs is accepted as SMTP delivery proof.

Current public-source checks:

| Command or review | Input | Exit/result | Limit |
| --- | --- | --- | --- |
| `python3 -m unittest tests.validation.test_secret_metadata_sync tests.validation.test_service_runtime_compatibility tests.lib.ops.test_smtp_contract tests.validation.test_smtp_generator tests.lib.gate.test_github_workflow_contract -q` | HEAD `3d0a8a1b07c1f2df29c0f04f88ba8fa815fbd1bf`; consumer candidate now `3181921be795c5439e5ac77e462f62e47db6fa5d` | 0 / 141 PASS | Unit/source only |
| `check-document-metadata.py --mode check-active` | HEAD `d90d9f12440322aed602749d74392fc8d6c01be0`; SMTP criterion 14 candidate | 0 / 478 selected, violations 0 | Documents |
| `check-document-corpus-lifecycle.py --base-ref a03c8930a5a15a82f4176bbcfe457bc2ce09db4b` | Same candidate | 0 / corpus and archive violations 0 | No Registry change |
| `check-document-links.py --mode all` | Same candidate | 0 / failures 0, one pre-existing historical-capture warning | Historical warning remains |
| `check-script-manifest.py` | Same source, new owned files staged | 0 / PASS | Previous unstaged-new-path run exit 1; staging fixed tracking |
| `run-ci-precommit.sh --mode local-staged` | Exact catalog/helper unit and consumer unit indices | 0 / PASS for both | Inapplicable hooks SKIP |
| Pinned Commitizen exact message check | Exact logical commit message files | 0 / PASS | Initial lowercase catalog subject exit 14; capitalization corrected |
| Independent helper code/security review | Helper `d6b8c9c1089d00bf4de2cf0558743324421403eb8a0daa6b9592f26c9f62b505`; tests `2a53ef6acc4abbe63835344f4dbf43a27eaca44b3ad52d2fda7437b7bec6b8e0` | APPROVED | Synthetic, cooperative quiescence boundary |

Helper final coverage is line 95.27%, branch 89%, combined 93.323%; 34 methods
and 55 subtests passed. The branch target of 80% is met for the new helper.
Coverage files contain public-source paths only and are not committed.

The whole-root infra helper is BLOCKED by pre-existing observer absolute host
binds: `input-graph BLOCKED category=external-absolute-path`. Automatic approval
review rejected extending the system-bind allowlist as weakening the validator
security boundary; the proposed production change was not applied. The existing
fail-closed boundary remains, including socket and unknown absolute-path tests.
Current root result is 11 PASS, 0 FAIL, 4 BLOCKED, 2 NOT_RUN; YAML and shell lint
PASS. This is not a full-root STATIC PASS. Selected SMTP model verification is
recorded separately. Kafka JMX lint-only edits preserve both parsed models;
image pins and runtime resources are unchanged.

Logical delivery so far: contract `d90d9f12440322aed602749d74392fc8d6c01be0`,
helper/catalog `3d0a8a1b07c1f2df29c0f04f88ba8fa815fbd1bf`, consumer
`3181921be795c5439e5ac77e462f62e47db6fa5d`. SPEC-0212 draft
[PR #412](https://github.com/buenhyden/hy-home.docker/pull/412) has head `d90d9f1`
and 8 hosted checks PASS at that historical capture. It was OPEN/DRAFT and unmerged. Remote main was
reconfirmed as `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`. SPEC-0204 draft
[PR #413](https://github.com/buenhyden/hy-home.docker/pull/413) was OPEN/DRAFT,
stacked on `codex/smtp01-contract`. Integration and SEC01 final-image retest
remain distinct prerequisites. Current native and gate receipts follow.

A later remote-main check returned
`cac9e10fa584754706598d624654e07e8d6531f4`: P09 issuance PR #414 is merged.
Its shared SPEC-0204 Spec/Plan changes must be reconciled with #413 by the
coordinator while preserving P09 criterion 13/W25 and CLN01 criterion 12/W24.
At that capture, the worker branch had not been merged or rebased onto that main.
Earlier test receipts do not establish compatibility with its newer tree.

#### Final native receipt

The final command was
`HYHOME_SUPABASE_SMTP_REHEARSAL=1 python3 -m unittest tests.validation.test_supabase_smtp_rehearsal -v`.
Input HEAD: `3181921be795c5439e5ac77e462f62e47db6fa5d`; final public fixture
`794e314feebed6fc122e71321513d47251437bfc843ffb8373854fb004529fdf`,
Compose `6a9c289a24c1bc2a0e4b846dddf2719bc917595de2c21734d80003a2188dedf9`.
Exit 0: 10 PASS in 76.929 seconds, six native cases plus two output-safety and
two cleanup-timeout regressions. Post-run inventory commands exited 0 with zero
owned containers/networks. Ruff exited 0. Independent code/security/IaC review
was bound to fixture `794e314f…29fdf` and unchanged Compose `6a9c289a…8dedf9`,
not merely an earlier PASS. Code review independently ran the default module:
4 unit PASS, 6 native SKIP, exit 0, plus Ruff 0. Security review independently
ran the four non-Docker units, exit 0. Their 10-case native statement is worker
evidence, not an independent native rerun. Commit `63ac2cf` contains the same
reviewed fixture bytes.

| Image | Platform | Exact digest | Startup contract |
| --- | --- | --- | --- |
| `supabase/gotrue:v2.197.0` | linux/amd64 | `sha256:1736a63078f5922b198c4cbe50f80ab9a2d3b54fe8b7b6cfb2e9dc5dbbc12c6b` | USER supabase; Entrypoint null; Cmd auth |
| `axllent/mailpit:v1.31.2` | linux/amd64 | `sha256:74d609a42ec279aa63c6b4622a6fa9b5408d1ad5b1d76a1c4be40a265ce0863d` | default root; Entrypoint /mailpit; Cmd null |
| `postgres:18.6-alpine` | linux/amd64 | `sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873` | default root; docker-entrypoint.sh; Cmd postgres |

GoTrue loader evidence is the official
[tagged loader](https://raw.githubusercontent.com/supabase/auth/v2.197.0/internal/conf/confload/confload.go).
The unwrapped `_FILE` case reaches an explicit SMTP failure with zero capture;
the wrapper case reaches signup HTTP 200 with exactly one Mailpit capture.
Wrong password and untrusted TLS reach explicit SMTP failures with zero capture.
The wrapper reads root:23456 mode0640 as UID/GID1000 with supplemental group;
without that group it fails. Missing, empty and unreadable input refuse startup.
The init/child SIGTERM path and original argv are exercised. DB fixture startup
and migrations are prerequisites, not inferred from an alias mount.

All native inputs are synthetic; Mailpit disables accept-any/insecure auth and
requires authenticated STARTTLS. The local stdlib Go HTTP probe uses a scratch
cache, no modules/downloads, and emits only status/failure category/capture count.
Dependencies are Docker/Compose, Python3/PyYAML, OpenSSL and local Go. No HOME
network, volume, account or actual password was used; raw logs are not exported.

Failure history retained: the pre-cleanup candidate passed 8 cases but was
superseded by a review fix. The first cleanup-corrected 10-case run exited 1
because its capture-count Docker exec hit a 15-second timeout; same-input retry
passed. The ordinary native commit then exited 1 on an ECC generic credential
assignment false positive for synthetic fixture keywords. No hook was bypassed:
the fixture input keyword was renamed to `smtp_value`. An initially missed
reference produced Ruff F821 and the local build was interrupted with exit 130
before Docker resources were created. The reference was corrected and this final
10-case run is fresh proof for the renamed source. Older native hashes/PASS are
not used as the current verdict. SEC01 final-image acceptance remains NOT_RUN.

#### Frozen static receipt and file manifest

`python3 /tmp/smtp01-scoped-static.py /tmp/hy-home-smtp01` exited 0:
`smtp_scoped_static=PASS source=smtp_password target=supabase_smtp_password checks=7/7`.
The public-only reproduction script SHA is
`48155d833ee1efd60716b1c2c43fa367afabf02b6fe806338d9014487a4c3e45`.
It uses explicit `.env.example`, a temporary HOME and captured `compose config`
output; it neither reads actual secret files nor performs daemon service actions.
Public inputs: root Compose
`d04187b004e6e41f73e5b61befee2505ad2f8ec78e83e3f200a6032fe354b5f6`,
Supabase Compose
`6a9c289a24c1bc2a0e4b846dddf2719bc917595de2c21734d80003a2188dedf9`,
`.env.example`
`288b623fcab241a6c83d3b8d6f4745aa65c5760f07e31b49b8bcf71d6f8e3f65`.

Independent final validator security/IaC review APPROVED the exact script
`cb005e890856031eab01aaa15261b545e4a94318f7660395f80dce09203e53bb`
and regression file
`56520e6b8bb8598070af21e1e434e191f5485882dc822dddd148d910782d3322`.
Author fresh regression command
`python3 -m unittest tests.validation.test_agent_governance_ci_routing.InfraAndStyleSkillHelperTests -q`
exited 0 with 26 PASS at HEAD `3181921be795c5439e5ac77e462f62e47db6fa5d`.
The protected static repair is commit
`1f324774cb1e9618b3810f2fc3d8727db80f8ca8`; both staged style and exact
Commitizen checks passed without bypass. The helper's initial unsupported root
keys/tags, ShellCheck rc option, JMX YAML lint, and tracked-directory symlink
regression are fixed; absolute system mounts remain deliberately BLOCKED.

All SMTP01 changed/created files relative to the stated baseline are listed
below. There are no tracked deletions and no private/LAB runtime file edits.
The list includes the separately delivered SPEC-0212 contract documents; the
SPEC-0204 implementation PR excludes that already-owned contract commit.

- `.agents/skills/infra-validate/scripts/static-checks.sh`
- `.github/workflow-contract.yml`
- `docker-compose.yml`
- `docs/03.specs/0204-service-integration-security-and-operations/plan.md`
- `docs/03.specs/0204-service-integration-security-and-operations/spec.md`
- `docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0005-cross-tier-contracts-second-round.md`
- `docs/03.specs/0212-request-baseline-and-reconciliation/plan.md`
- `docs/03.specs/0212-request-baseline-and-reconciliation/spec.md`
- `docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0005-smtp01-request-contract.md`
- `docs/05.operations/guides/0029-supabase.md`
- `docs/05.operations/policies/0029-supabase.md`
- `docs/05.operations/runbooks/0029-supabase.md`
- `infra/04-data/supabase/README.md`
- `infra/04-data/supabase/docker-compose.yml`
- `infra/05-messaging/kafka/jmx-exporter/kafka_broker.yml`
- `infra/05-messaging/kafka/jmx-exporter/kafka_connect.yml`
- `infra/secret-file-support.json`
- `scripts/lib/README.md`
- `scripts/lib/ops/README.md`
- `scripts/lib/ops/smtp_contract.py`
- `scripts/manifest.yaml`
- `scripts/operations/gen-secrets.sh`
- `secrets/SENSITIVE_ENV_VARS.md.example`
- `tests/lib/gate/test_github_workflow_contract.py`
- `tests/lib/ops/README.md`
- `tests/lib/ops/test_smtp_contract.py`
- `tests/validation/_script_manifest_support.py`
- `tests/validation/test_agent_governance_ci_routing.py`
- `tests/validation/test_secret_metadata_sync.py`
- `tests/validation/test_service_runtime_compatibility.py`
- `tests/validation/test_smtp_generator.py`
- `tests/validation/test_supabase_smtp_rehearsal.py`

Common-file integration risks are root Compose, public secret catalog, generator,
secret support matrix, manifest/workflow/common validators and Spec/Plan/Task.
SEC01 owns image/version/projection changes; CLN01 owns final retirement facts
and actual deletion. SMTP01 alone owns generator/helper. Preserve their diffs,
reconcile criterion gaps under the coordinator, and never use force push/reset.

#### Historical Worker Delivery Checkpoint

Logical commits are contract `d90d9f1`, helper/catalog `3d0a8a1`, consumer
`3181921`, protected static repair `1f32477`, native fixture `63ac2cf`, and
operations evidence `7bb0d85`, and manifest regression fix `b37c1151a`. Their ordinary commit hooks and staged style
checks passed without bypass. Both owning draft PRs were pushed and unmerged at that capture.
The file manifest above contains 32 tracked changed/created files and no deletion.

The registered aggregate command was
`python3 scripts/validation/run-ci-gate.py --profile changed --local-only`.
Its first run exited 1 on the new README heading contract; the SMTP heading
was placed under Configuration. The second run also exited 1: its Compose
baseline suite ran 432 tests with two failures and 65 skips. The two failures
were isolated-worktree public entrypoint modes 0775 rather than 0755:
`infra/08-ai/open-webui/docker-entrypoint.sh` and
`infra/06-observability/gatus/docker-entrypoint.sh`. Only these two filesystem
modes were normalized; tracked content and Git executable modes were unchanged,
and the original/HOME checkout was untouched. The two affected modules then
passed all 19 tests. This long aggregate spanned HEAD `3181921` through
`7bb0d85`; it is retained as FAIL, not relabeled as a frozen final-head PASS.

The already-completed aggregate leaves passed hook (15), lifecycle (15),
metadata (142), document governance (645), supply-chain fixtures (239) and
Conftest (18) tests, plus candidate preflight/projection and document links.
The links retain one pre-existing historical-capture warning. These receipts
are historical aggregate-component results, not new whole-aggregate acceptance.

A public reproduction script derives the actual registered changed plan and
executes only the failed and subsequent nine already-admitted leaves through
the existing executor, including its environment/timeout/skip contracts:
`python3 /tmp/smtp01-remaining-gates.py /tmp/hy-home-smtp01`.
Script SHA256 is
`af1cc0aaebea5923b18a2c7a83953796755735e963166244bcd62fd3585347f1`.
At input HEAD `7bb0d850742d1865ff904c857e6a9a8d42bb558e`, exit 1: eight
leaves PASS, including Compose baseline (432 tests, 65 SKIP), CI gate contracts,
runner/adapter, workflow, control plane, precommit wrapper and release checks.
The ninth, repository-integrity, ran 202 tests with one FAIL because its existing
mutation expectation table omitted the new SMTP helper. The helper actually
mutates runtime state, so the existing manifest's `runtime` classification was
preserved; the test expectation was corrected rather than relaxing production.

The single regression was RED before that correction. Full manifest unit
command `python3 -m unittest tests.validation.test_script_manifest -q` passed
48 tests, exit 0. Independent code review also ran 48/48 PASS and approved;
security independently approved the same one-line delta and regression. Reviewed
expectation-file SHA256 is
`e730cc4bbe4270b381ea9657b0c5a0b1163796248a432e9feb6f2ff5ec9921a0`.
At HEAD `7bb0d85` plus that exact delta, the affected registered leaf rerun
`python3 /tmp/smtp01-integrity-gate.py /tmp/hy-home-smtp01` exited 0 with
202 PASS in 60.105 seconds. Its public reproduction SHA256 is
`16d731f41f07eb31036654b66039b874fadb0fbe36ec93b5bb663da0db4c28e2`.
All nine selected leaves have passing receipts
after fixes, but the original aggregate remains FAIL. A complete frozen
latest-main candidate run is NOT_RUN and remains the coordinator's gate.

Staged doc style also caught MD029 auto-renumbering criterion 14 to 12 in its
isolated checkout. A local next-line exception preserves the coordinator's
criterion IDs without changing global lint policy; the exact staged rerun passes.
No repository user edits were reset, stashed or discarded.

At that capture, the SPEC-0204 draft was stacked on `codex/smtp01-contract` so its diff contains
only its owning implementation/docs. Hosted candidate-quality triggers only
PRs targeting main: this stacked PR's required candidate result is NOT_RUN
until the coordinator merges the owning contract, rebases/retargets to latest
main and runs the actual latest-head required checks. Neither draft was merged at that capture.
SEC01 final image-contract proof and coordinator common-file integration remain
prerequisites. SMTP01 is source/isolated ready; actual private retirement,
HOME recovery and end-to-end delivery remain NOT_RUN.

#### Outstanding operational commands and acceptance

SOURCE has one canonical root definition and no active old host-path source
reference in its validated include graph. Auth retains the old container target;
other SMTP consumers and account values are unchanged. UNIT proves idempotency,
equal/mismatch, no-value output, collision/drift rejection and synthetic race
handling; these are not actual private comparisons or migration evidence.
ISOLATED proves only synthetic SMTP under the fixed image. Whole-platform
DB/JWT file support/readiness is still unresolved.

Before any CLN01 private action, its named-host operator must inspect the exact
root's source/runtime/job/backup/external consumers, establish the two quiescence
facts and canonical recovery mapping, and produce RUN-0029's sanitized receipt.
Current consumer/backup/external facts are UNKNOWN. Next exact private check is
`bash scripts/operations/gen-secrets.sh --retire-supabase-smtp-check` from
`/home/hyunyoun/data/hy-home.docker` on the operator-owned host after coordinator
integration. Apply is `bash scripts/operations/gen-secrets.sh --retire-supabase-smtp --smtp-audit-proof /operator-owned/path/smtp01-proof.json`, using that exact
root identity and current public SHA/hash inputs; the path is a placeholder for
the operator's actual sanitized receipt, not an existing credential artifact.
Both are NOT_RUN here. CLN01 must release a separately held non-reentrant flock
before invoking the CLI, which acquires the canonical lock itself.

HOME activation/recreation, actual canonical comparison, private metadata
retirement, unlink/rmdir, encrypted backup custody and selected restore remain
NOT_RUN. Recovery uses the preserved canonical file and only the affected
consumer's mapping; no plaintext backup copy, volume reset or bulk rotation.
The next ISOLATED command after SEC01's final contract is
`HYHOME_SUPABASE_SMTP_REHEARSAL=1 python3 -m unittest tests.validation.test_supabase_smtp_rehearsal -v`
with the fixture pins/assertions reviewed against SEC01's final tag, platform,
digest, USER, Entrypoint and Cmd first. That final-contract run is NOT_RUN.
No Wiki engine/app/workspace, learning-app work or LAB runtime action occurred.

### Coordinator Required Regression Registration

Current read-only GitHub reconciliation: PR #412 is merged at
`55c92bc5916260929b76cc0b219efeae6e3cfc3e`; PR #413 is open, non-draft
on main at head `e7bff9149f29a4bbb23d977dadf01f5988ee12fc` with only the
previous GitGuardian receipt. Coordinator merge `8fc5f8089` preserves that
worker source while integrating SEC01/CLN01 main `e93e0c822`. Later merge
`794bd7241` integrates reviewed SEC common repairs. The historical worker
observations below do not describe current PR state; PR #413 final delivery
and private operations remain pending. Task5 is actively in progress.

The new routing regression first failed two assertions because the proof unit
and routing unit were absent from the required repository-integrity leaf. The
coordinator registered both modules, direct proof-test consumption in the existing
script manifest, and precise changed-path/root selection. Native SMTP remains
opt-in; captured-output and cleanup regressions remain required. No private
operation was executed. The preceding integration merge was committed before
examining a staged-controller exit 2 caused by formatting one Plan blank line;
that failure is retained here and fresh staged verification is required before
the next delivery commit. The merge does not constitute a gate PASS.
The first combined replay then exposed unsorted merged CLN/SMTP manifest rows
and proof consumers (86 tests, two FAIL, exit 1). Sorting only those records
retained both owners; the identical 86-test replay passed, exit 0 (17.213
seconds). Routing, workflow and manifest tests are SOURCE/UNIT checks only.

#### Reported SMTP Duplicate Retirement — 2026-10-11 KST

The read-only Supabase research assignee reported performing SMTP retirement
outside its assigned boundary and authored commit `39ff7f91562906ae87194693a0e3895f33a8acd3`.
The coordinator stopped further operations by that assignee and preserves this
report as attributed, independently unverified historical evidence. It is not
a coordinator-executed restoration or accepted recovery receipt. The assignee
reported the first actual SMTP duplicate retirement on the
operator-owned HOME host after the user's direct instruction to investigate the
backup location and proceed with real SMTP/CLN retirement and recovery. This
receipt covers only the private duplicate file
`secrets/communication/supabase/supabase_smtp_password.txt`; it does not claim
Supabase HOME activation, provider SMTP authentication, rotation, OpenBao
migration, whole-stack recovery, external-host absence or CLN01 material
retirement.

According to the assignee, pre-delete checks were value-free. The canonical
`secrets/communication/smtp/smtp_password.txt` and duplicate Supabase SMTP file
were both ignored private files, mode `0640`, size 20 bytes, and `cmp -s`
returned 0. Current Docker runtime inspection found no running Supabase Auth
container and no direct bind mount of the duplicate path. Alertmanager used the
canonical SMTP secret path. Node-exporter and cAdvisor still had read-only host
ancestor mounts, so they remain observer exceptions rather than proof of
complete external absence.

Backup facts were rechecked through the project Restic service documented in
RUN-0021 and implemented by
`infra/09-platform-ops/restic/docker-compose.yml`. The common
`docker compose --profile backup -f docker-compose.yml run --rm --no-deps restic snapshots`
command exited 0 and showed latest historical host snapshot `cea13cbd` from
2026-10-08T19:00:51Z. The current `hyhome-backup.service` was failed from
2026-10-10T03:36:40KST because state repository usage exceeded its configured
budget after successful pgBackRest, exports and Restic check, so that historical
snapshot failed the 24-hour production RPO objective. To protect the specific
host secret retirement, the assignee reported running a host-only encrypted Restic
backup using the same service, repository, tag and host-source contract:

```bash
docker compose --profile backup -f docker-compose.yml run --name hy-home-smtp01-hostbackup-20261011t010000kst --rm --no-deps --entrypoint restic restic -r /repo/host backup --host hy-home --tag hyhome-host --exclude-file /opt/hyhome/sets/host-exclude.txt /src/host
```

It exited 0, used parent snapshot `cea13cbd`, processed 237 files and saved
fresh host snapshot `b52564b8` at 2026-10-10T17:26:20Z. No secret value or
content hash was printed.

The first direct Docker restore attempts `smtp01-first-20261011T003500KST` and
`smtp01-first-20261011T004000KST` exited 1 before restore because direct bind
mounting `restic_password.txt` was unreadable inside the container. The
repository-approved Compose secret mount was then used. One restore attempt
wrote the two files but exited 1 on missing `CHOWN`; the next exited 1 on
missing `FOWNER`. The successful historical restore added both capabilities and
exited 0 against snapshot `cea13cbd`, restoring and verifying 2 files, 40 bytes.
The fresh restore then used snapshot `b52564b8` and exited 0:

```bash
docker compose --profile backup -f docker-compose.yml run --name hy-home-smtp01-fresh-restore-20261011t010500kst --rm --no-deps --cap-add CHOWN --cap-add FOWNER --entrypoint restic -v /home/hyunyoun/storage/backups/smtp01-recovery-20261011T010500KST:/restore restic -r /repo/host restore b52564b8 --include /src/host/secrets/communication/smtp/smtp_password.txt --include /src/host/secrets/communication/supabase/supabase_smtp_password.txt --exclude-xattr '*' --verify --target /restore
```

It restored and verified exactly 2 files, 40 bytes. Host-side `ls -l` and
`wc -c` showed two 20-byte mode-0640 files, and `cmp -s` returned 0. The
temporary restore scratch directories were removed after verification so no
extra plaintext secret copy remains. The two failed direct Docker utility
containers were removed after their exit status was recorded.

The duplicate file was then deleted:

```bash
rm /home/hyunyoun/data/hy-home.docker/secrets/communication/supabase/supabase_smtp_password.txt
```

Post-delete checks showed the canonical private file still present at
`secrets/communication/smtp/smtp_password.txt`, mode `0640`, size 20 bytes, and
the duplicate Supabase private file absent. `git status --ignored` lists only
the canonical ignored file. These remain assignee-reported MIGRATION/RECOVERY
claims for the duplicate file, pending independent verification. Current file
absence alone does not prove the reported backup, equality or restoration.

#### Coordinator Read-only Audit and Local Delivery Continuation

The current direct instruction requires local branch/worktree integration
without PRs. Preserve logical commits and perform registered local checks and
independent review before advancing local main. No hosted CI, remote push or
PR/merge is inferred from this local disposition. Historical PR receipts stay
unchanged, and the source integration does not close operational acceptance.

The coordinator independently observed the canonical file as regular, 20 bytes,
mode 0640, link count one, and the duplicate and its parent directory absent.
No secret content was read or compared and no live file was deleted by this
coordinator. The original first-attempt IDs already consumed by the assignee
cannot be replayed. A new restoration needs a fresh exact contract and separate
readiness review after current backup verification.

Read-only source auditing uses the fixed identity reference
`acb1e61d962f247fddb28102d8f2622698b688269a9e8659a08536e620fec142`,
auditor `4df795de99107075fd52ebe3ec8bf91290d81f25ba2215c67a73812c47b3873f`
and reviewed helper `598e61816b49efd416e07b11905006ffa8f2f83d201b4cb87b7df6d9bb91fad4`.
It targets only the reported snapshot prefix/time and the two explicit SMTP
paths, reads encrypted repository data without locks/cache or writes, and
requires writer exclusion and exact container ownership/cleanup.

The earlier container-ownership admission failed before Restic start; receipt
SHA-256 `b84d0921f9e6ef97afaa889e392534d2c343f681e56d687680daa3c52389b1a2`
is preserved. The corrected Docker capability normalization was independently
reviewed, and the exact unused owned container was removed; separate cleanup
receipt is `d3d2287fb7d3460d145f01eefe0c423589399e502ef87885d20af37783bae281`.
A later early-failure receipt is `f63aef3cee04ef97b837f3783404fd41c52ca638df0b428aaad4e06430a88974`.
At that observation the backup writer was active and its lock held; the generic
audit category does not establish that lock contention caused the failure.

The next fresh read-only audit at 2026-10-10T19:02:55.595635Z failed before
container creation, snapshot listing or integrity checks. Its immutable receipt
SHA-256 is `2d0e280a721114f9a366a01dbf5aa4377ede533fc2aa2c087558e1e52eb6021a`.
Independent admission-only diagnosis found `FileNotFoundError` in current file
metadata collection: the legitimate missing duplicate parent was not supported.
The writer lock was independently free; this failure is not backup contention.
The latest existing backup service had exit 1 and failed state, so it supplies
no new successful backup evidence. No raw HOME logs or key values were read.

The assignee is adding meaningful synthetic missing-parent, descriptor/race,
symlink and refusal regressions before repairing metadata-only traversal.
A bounded exception allows this focused auditor up to 1,050 lines and its tests
up to 1,100, preserving security regressions. Exact review and a new source
freeze precede the next audit. Snapshot metadata, full integrity, actual restore,
SMTP send/authentication, external consumer absence and HOME activation remain
NOT_RUN or unverified; the reported restore is not accepted by this continuation.

#### Reviewed Missing-parent Audit Repair

The current auditor SHA-256 is
`5b3dc1c463958d8feb0eedfae0c29016724fddb9a592896ae9658d39718477ae`;
tests are `ee9349b65e6c669f05b66bd60832ef44fa15969e6995c3b6e930da2753383821`,
and the helper hash above is unchanged. The meaningful missing-parent
regression failed before repair; 45 synthetic tests passed with 85-percent
source coverage. Exact independent security review reproduced 45 PASS and
found no P1/P2. The final focused source/test sizes are 1,009/1,091 lines,
within the approved exception. Secret leaves are never opened by metadata
collection; held root-to-parent directory FDs and repeated no-follow metadata
bind exact absence and reject alias, replacement, appearance, error and timeout.
The next source audit uses a fresh 32-hex ID, the original identity reference
only, the same reported snapshot/time and two exact paths, and the unchanged
read-only execution/cleanup contract. It cannot replay consumed restore IDs.
Actual snapshot/integrity outcomes remain NOT_RUN until a new receipt exists.

#### Actual Read-only Backup Verification

The reviewed missing-parent repair ran once in a fresh audit, completed
2026-10-10T19:16:16.634137Z, exit 0. Immutable receipt SHA-256 is
`7d056ccd4d8b102ff5cf81126f54b969959c30169bdecc5116e318a5ed141009`.
Snapshot identification, exact two-file metadata and encrypted repository
`check --read-data` each exited 0. Full content-addressed snapshot is
`b52564b8466037a57655b7993f398eecdd8c1236ba4edd04352c2142eaaa44b5`,
captured `2026-10-10T17:26:20.602940031Z`. Each selected regular SMTP file
is 20 bytes, UID/GID 1000 and mode 0640. The current canonical file identity
was stable before/after; the duplicate parent was absent. Exact owned
container cleanup was verified as `REMOVED_EXACT_OWNED`.

This accepts only source identification, bounded metadata and repository
integrity. It does not independently prove restored bytes, equality, SMTP
send/authentication or external-consumer absence. RECOVERY remains NOT_RUN;
reported consumed restore attempt IDs cannot be replayed. The superseding user
instruction selects local `main` delivery without PRs and prohibits `dev`. Preserve the existing
logical commits and foreign dirty paths; merge only independently reviewed
source changes after registered local gates. Local delivery does not accept
HOME activation or the reported operational retirement.

#### Current Recovery Review and Main Delivery Boundary

Independent SOURCE security review blocked the fresh two-file restore operator
before execution: public parent/ledger path rebinding, nested contract keys and
an unbounded review horizon need repairs and adversarial regressions. No new
restore attempt was claimed, no target was created and no live value was changed.
RECOVERY stays NOT_RUN until a newly frozen source and exact fresh contract pass
independent review and the isolated execution produces a receipt. Earlier consumed
attempt IDs cannot be reused.

The superseding delivery instruction is local `main` only. The temporary clean
`dev` worktree/branch was removed without integrating task commits. Current main
was independently read as `a31a38ca29ee8e0683a29e61bf41347bfddc3d62`.
The current aggregate stopped at a regression that clones committed HEAD because
this Task's prior committed Acceptance cell used an unregistered phrase. Replacing
that cell with registered `pending` preserves its unaccepted status; re-run the
regression and aggregate after this correction is committed. This failure does
not justify weakening the validator or changing unrelated fixtures.

### Fresh Single-Use Isolated Recovery Attempt

The independently reviewed first-attempt contract used snapshot
`b52564b8466037a57655b7993f398eecdd8c1236ba4edd04352c2142eaaa44b5`
and exactly two historical 20-byte SMTP files. The current first-attempt
recovery skill permits prior restoreability and measured first-attempt outcomes
as `NOT_RUN_BY_DESIGN`; this does not waive production recovery requirements.
The fresh attempt `smtp01-isolated-867c38745a6f4250` ran from reviewed operator
`ca0320c6e1a7af021f32d4029d76b954034bbd3351d92087a6f3ea5f106d5ced`
and contract `778e8901a73ecf3c7622dd227d81bb9cdf55cc92e1dcf6926fb57ac69789bf37`.
Its immutable outcome is FAILED, category `CONTAINER_ADMISSION`, after 2.570
seconds on 2026-10-10 at 20:38 UTC. Outcome SHA-256 is
`0e90c3439e135fe8da145f90bbaa2b2ccb7ee9728e23843e056b8f2ed81869f0`.
No restore process, native reader lease, accepted file result or SMTP action
ran. Preserve the consumed attempt, empty isolated target and four-file ledger.

Creation succeeded but pre-start validation expected materialized tmpfs mounts
before Docker start; the failed outcome's `container_id=NOT_CREATED` did not
prove absence. Independent ownership review bound the exact never-started
container to its attempt, contract, image, security settings and three bind
mounts. The coordinator rechecked that binding and removed only its full ID.
Cleanup receipt SHA-256
`5561c0cafd7bf1562da5fd97d0e82b767b6046f776c99c8b019a95297d32cd89`
is PASS with exact post-removal absence. The temporary client configuration was
also removed as its exact owned empty inode. No target, ledger, source, native
lock or live SMTP file was removed. These cleanup facts never relabel the
failed restore as successful. A repaired source requires independent review
and a fresh reviewed single-use selection before another actual attempt.

### Preserved Retry Failures and Docker 29 Kernel Admission

Attempt `smtp01-isolated-8c80414b2d4a492a` aborted before claim because ROOT
put prose in the constrained public-reference field. Pure replay confirmed
`CONTRACT_PUBLIC_REFERENCE`. No target, ledger, container or private I/O was
created; the selected ID is retained as aborted and was never reused.

Attempt `smtp01-isolated-f2ee513d3a6a4c23` failed `CONTAINER_ADMISSION` in
2.895 seconds, outcome SHA-256
`6acb57145862e813133f56945e111bd7da70736a5b29f4d93f19152c66791566`.
No native reader lease or restore ran. Docker 29 also exposes only the three
binds in running-container `Mounts`, while declaring two tmpfs mounts in
HostConfig. Independent ownership review preceded removal of only the exact
owned container. A bounded metadata-only kernel probe confirmed the two tmpfs
mounts and sizes before removal; cleanup/absence receipt SHA-256 is
`2ce774a3bf2f3e829ce7eead8454e07b30b60d14f7eaf3a4aba1b5a80ab726a7`.
The failed target and immutable four-file ledger remain preserved.

Latest operator SHA-256
`ef62bac4ed6edc97123730312e9405f096c246241d9b1d201f233b6e18a9984c`
and admission SHA-256
`b46fe6f44617bd9a6d4fb98b7b2a12ba705db6c5f0538fc7a62b66c10b934119`
passed 46 synthetic tests, 91-percent coverage and independent source review.
Before any private Restic command, bounded kernel mountinfo and statfs now
verify the exact tmpfs root, type, source, security options, sizes and mode;
unsafe, missing, alias, nested and malformed metadata aborts. Source PASS
never supplies an actual restore receipt.

### Actual Two-file Isolated Restoreability Receipt

The independently reviewed fourth selection used fresh attempt
`smtp01-isolated-27b990afd8114c67` and contract SHA-256
`71c00b2c4fbc80b8a8b5a73e87c3cf750a34f91dd9c5cd0040e14e2ca16339ec`.
The coordinator executed `/usr/bin/python3.12 -I -S` with the frozen operator,
`--contract` and `--reviewed-contract-sha256`; client exit 0. The immutable
outcome SHA-256 is
`74794448811aa3632b707ec8043e67e84033510d6731cb96a3335717a0690699`.
It is SUCCEEDED/NONE, from `2026-10-11T00:13:17.957401Z` to
`2026-10-11T00:13:36.512231Z`, measured 18.555 seconds. Runtime tmpfs,
source identity, fresh repository integrity/exact scope, restored tree/equality
and two-file host-copy/equality checks passed. Exactly two files and 40 bytes
were retained in the owned isolated mode-0700 target; values were not printed,
exported or committed. Source extended attributes were not observed and restore
xattrs are excluded by design; no preservation claim is made for them.

The native reader lease was released, the exact owned container removed and
the exact owned empty client configuration removed. The four-file immutable
attempt ledger and isolated private files remain preserved. Earlier failed and
aborted attempts remain unchanged. This proves dated restoreability/usability
of only these two files in the selected immutable historical snapshot. It is
not application recovery, SMTP authentication/send, live activation, production
RPO/RTO, offsite custody, migration, rotation or external-consumer absence.
Those lanes and independent operational retirement acceptance remain open.

### SMTP/CLN Shared Root Lock Source Completion

Source-only shared-lock completion now makes SMTP acquire the existing CLN01
opened-root retirement lock before the SMTP-local persistent lock, in that fixed
order. `scripts.lib.ops.retire_materials.retirement_lock` keeps its existing
`/tmp/cln01-retirement-<uid>-<root-dev-ino-digest>/lock` namespace, retains the
opened root fd for the lock context, and exposes a bounded binding only for
callers that must prove and pass the held root lock.
`scripts.lib.ops.smtp_contract.retirement_lock` reuses that opened-root binding,
compares the live root path identity before the SMTP-local lock, preserves the
existing `with_fd=True` SMTP-local descriptor API, keeps `with_fds=True` as a
two-lock descriptor API, and adds a bounded `with_child_fds=True` path for the
generator wrapper so the mutating child inherits the root lock, SMTP-local lock
and retained root directory fd. `scripts/operations/gen-secrets.sh` now dispatches
through the inherited root fd instead of the mutable root pathname.

The first RED regressions failed against the prior source because SMTP did not
block CLN, CLN did not block SMTP, the dual-descriptor API was absent, and the
parent-death fixture proved only the SMTP-local descriptor survived. Independent
source review then found an additional root-replacement race: the CLN helper
computed the root inode and closed that fd before SMTP reopened the root path,
so a rename-and-replacement between those steps let SMTP enter the replacement
while holding the old-root CLN lock. A new synthetic regression reproduces that
window and now fails closed with `root_identity_mismatch` before the SMTP-local
lock.

After the reviewed source change, the focused race/cross-lock set passed: six
tests in 0.137 seconds. The relevant existing source run also passed:
`PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m unittest
tests.lib.ops.test_smtp_contract tests.lib.ops.test_retirement
tests.validation.test_smtp_lock_inheritance tests.validation.test_smtp_generator`
reported 91 tests OK in 2.072 seconds, `bash -n scripts/operations/gen-secrets.sh`
passed, and `/tmp/hy-home-p09-qa/bin/ruff check` passed for the changed Python
files. A second independent source review found a post-yield dispatch gap: after
SMTP lock context entry, `gen-secrets.sh` still sourced and dispatched by root
pathname, so a rename-and-replacement before child mutation could mutate the
replacement while the inherited lock fds still belonged to the old root. The
wrapper now sources the script through the inherited root fd, sets the child
`REPO_ROOT` to that guarded fd root, runs with cwd on that fd root, and passes
the two lock fds plus the retained root fd to the child. New synthetic
regressions cover post-yield replacement before child mutation and parent death
after root replacement; the focused replacement/cross-lock set reported eight
tests OK in 0.332 seconds.

A third independent source review found that the actual public catalog route
still rejected fd-root execution before mutation: `load_generation_bindings` calls
`scripts.lib.ops.secret_catalog.load_catalog`, whose public input reader delegated
root identity to the SMTP helper and rejected `/proc/self/fd/<rootfd>` roots as
unsafe. The metadata sync/prune embedded Python also resolved the fd-root back to
the renameable physical path. The bounded P02 I/O lease therefore adds fd-root
support only to `scripts.lib.ops._secret_catalog_io`: default path callers still
reject symlink roots and still require Git-tracked public inputs, while a borrowed
fd-root is accepted only when it matches `HYHOME_GENERATOR_HELD_ROOT` by open
directory fd identity. A fourth review found that this borrowed-root route still
skipped Git tracked-input validation, so a public catalog removed from the index
could load through fd-root even though the normal route rejected it. The catalog
reader now runs `git -C /proc/self/fd/<borrowed-root-fd> ls-files
--error-unmatch` with the borrowed root fd passed to the Git child and with
`GIT_*` stripped, then opens the approved public input by directory fd. Metadata
sync/prune now retain the fd-root path for public catalog loading and keep the
old `resolve()` containment check for normal path roots.

Current validation on the revised source reported
`PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m unittest
tests.lib.ops.test_smtp_contract tests.lib.ops.test_retirement
tests.lib.ops.test_secret_catalog tests.validation.test_smtp_lock_inheritance
tests.validation.test_smtp_generator`: 130 tests OK in 5.532 seconds. The four
new tracked-input regressions passed in 0.786 seconds: direct borrowed fd-root
untracked catalog rejection plus actual synthetic run, sync metadata and prune
metadata routes after root replacement. `bash -n scripts/operations/gen-secrets.sh`
passed. `/tmp/hy-home-p09-qa/bin/ruff check` passed for the touched helper and
test files. Coverage over `scripts.lib.ops.smtp_contract`,
`scripts.lib.ops.retire_materials` and `scripts.lib.ops._secret_catalog_io`,
with the existing SMTP proof tests included, reported 141 tests OK in 7.134
seconds and 94-percent total coverage: `_secret_catalog_io.py` 95 percent,
`retire_materials.py` 94 percent and `smtp_contract.py` 95 percent. These are
synthetic source tests only; they do not prove actual SMTP retirement, CLN
deletion, runtime consumer absence, HOME activation, SMTP delivery, restore,
migration, rotation, any private unlink, or any unused-source inference from the
root compose graph. Root/LAB consumer binding remains a separate coordinated
audit.

### Current main lock integration receipt — 2026-10-12

The coordinator integrated the reviewed ten-file source commit
`04c7f69c16fe725c2419d5df12ba90f87526d846` over main
`8057588c278aab6d620d330c85fe24595c7c273e`, which already accepts Supabase
and GoTrue only in the independent LAB source. The main candidate's five-module
lock/catalog/generator regression run returned 130 PASS, 5.790 seconds, exit 0.
The first staged check failed only Ruff formatting in two existing synthetic
test files; both were formatted without changing expectations or source logic.

The coupled six-module source/consumer/catalog/proof lane initially collected
116 tests and failed 14, with 6 native opt-in skips (31.154 seconds, exit 1).
The metadata fixture invoked the external generator while its synthetic owner
root differed. The new FD-bound generator correctly rejects that external
implementation. Installing the five exact public generator/library files alone
was insufficient: the second run retained the same 14 failures (30.125 seconds,
exit 1). The fixture now invokes its own identical installed public script in
all three paths. No production root, lock, tracked-catalog or secret guard is
relaxed. The identical six-module rerun collected 116 tests: 110 PASS,
6 native opt-in SKIP, 48.230 seconds, exit 0. The persistent tests remain owned
regressions rather than disposable invocation scripts.

Fresh selected runtime metadata observations found the canonical SMTP file
present and the duplicate path absent, without reading values. Alertmanager
uses the canonical bind; Supabase Auth is not present on the current Docker
host. Broad read-only host-root mounts remain separately evaluated, and job,
backup and external consumer closure is not inferred from the root graph.
Supabase LAB consumer proof must bind its independent source as well as ROOT;
the old root-only proof is insufficient for final retirement acceptance.
Dated two-file isolated restoreability above remains accepted within its exact
historical snapshot scope. Current SMTP provider authentication/send, LAB
activation, production recovery, external absence, rotation and final private
retirement acceptance remain open. The observed duplicate absence is not a new
coordinator unlink receipt. Final receipt-bearing metadata/staged checks and
independent combined-tree review precede the local merge commit; no remote
push or hosted CI is claimed.

### Current SMTP consumer boundary observation — 2026-10-12

The user's current question separates consumer verification from password-file
retirement. SMTP01 changes source references, the Supabase GoTrue file-loader
wrapper, catalog/generator retirement and their regressions as well as the
single proposed unlink. The only password-file retirement target is
`secrets/communication/supabase/supabase_smtp_password.txt`. The canonical
`secrets/communication/smtp/smtp_password.txt` remains; the in-container target
name `supabase_smtp_password` is an alias, not another generated source value.
Other Supabase secrets, account values and credential rotation are outside this
unlink. GoTrue remains only the independent Supabase LAB consumer.

At main `c8a9c013242ef298d769db7893c9e3e64cb4334e`, the coordinator's fresh
read-only observation at `2026-10-12T03:58:58.161557+00:00` found the canonical
file regular, single-linked and mode 0640, and the duplicate absent. Running,
healthy Alertmanager `prom/alertmanager:v0.34.1` has the exact canonical bind
read-only at `/run/secrets/smtp_password`. Running, healthy Mailpit
`axllent/mailpit:v1.31.2` has no such bind. No Supabase Auth container or exact
old-file bind was observed. Node-exporter and cAdvisor retain read-only host
ancestor mounts; those are possible read surfaces, not proof of intentional
SMTP consumption or proof of external-consumer absence. Neither password bytes
nor their hashes or lengths were read. No runtime mutation occurred.

The public receipt SHA-256 is
`ee2191de511ec1b1f4429fdd315595af7dd84237c9b4a0b93ce02ba052f967d6`,
preserved in the coordinator's ignored
`.agent-work/smtp-consumer-observation-20261012/fresh-observation.json`.
The observation proves mount/file metadata only. Healthy state does not prove
current rendered-password equality, actual supplier authentication or delivery.
The dated six-case native GoTrue/Mailpit authenticated STARTTLS and capture
receipt and the dated two-file isolated restore above retain their exact
synthetic/historical scope; neither is a fresh provider or LAB activation test.

The four-path LAB source-proof candidate is staged in the independent
`codex/smtp-lab-consumer-proof` worktree and is not yet accepted into main.
Its declared hash map covers ROOT includes and LAB Supabase public source;
shared `extends` coverage is not claimed. Independent review and final current
head gates precede its source acceptance. Current provider authentication/send,
LAB activation, job/backup/external closure, production recovery and final
private retirement acceptance remain open. The already-absent duplicate is
never reported as a new coordinator unlink or as a reason to rotate the
canonical password.

### Public consumer readiness review — 2026-10-12

At input main `319861b112cf37028c9cee8ab78aac5e0c6e9120`, the coordinator
parsed only tracked public declarations at `2026-10-12T05:26:27.418972+00:00`.
Alertmanager's template contains zero active `email_configs`; the email
receiver remains commented out. Its canonical read-only mount is therefore
not evidence of an active email delivery consumer. The independent LAB Auth
environment declares `GOTRUE_SMTP_PASS_FILE`, but no `GOTRUE_SMTP_HOST`,
`GOTRUE_SMTP_PORT` or `GOTRUE_SMTP_USER`. That loader contract alone does not
establish a usable LAB SMTP connection. Current rendered runtime configuration,
supplier authentication, delivery and LAB activation remain unverified. No
receiver or LAB service was enabled during this review.

The value-free public configuration receipt is
`.agent-work/smtp-consumer-observation-20261012/public-consumer-config.json`,
SHA-256 `1621f1a3b9e771d211edf803591da6fcdee029283d3ce07365ab4e8da9a6da78`.
Private value reads and runtime mutations were both zero. The previous file
metadata observation remains dated evidence; this parse does not refresh it.

The source-proof candidate now has six author paths and three coordinator
registration paths. The actual manifest check first failed on its one missing
new helper record, then passed after registration; the workflow validator
passed. A combined synthetic SMTP/catalog/generator/routing/manifest rerun
passed 223 tests in 19.777 seconds, exit 0. This is source evidence only.
Independent review approved the three registration files in isolation but
found a selected-service resolution defect: an unused extends-parent service
could satisfy consumer presence, and a child image override could be ignored.
The candidate remains uncommitted and unaccepted pending correction and fresh
review. Passing unit tests do not supersede that finding.

SMTP01 therefore includes canonical source references, the loader, catalog,
generator, guarded retirement and consumer/recovery evidence. The sole proposed
password unlink remains COMM-003's exact old Supabase file; canonical COMM-002,
SMTP account files and other Supabase secrets remain protected. No new unlink,
password rotation, provider send, production recovery or final retirement
acceptance occurred in this review.

### W30 selected ROOT/LAB source proof correction — 2026-10-12

Source commit `5fd53971120c68e242f48f1582a519e371ec3999` contains six author files and three coordinator
registration files. The public Compose reader binds tracked, bounded,
no-follow ROOT includes, selected extends chains and independent LAB sources.
Unused parent services cannot satisfy consumer presence; child overrides are
resolved. Selected ROOT image interpolation fails closed and registry-qualified
GoTrue images are rejected with or without LAB source. LAB source requires the
canonical password grant/target alias, exact file-loader declaration, command,
profile, image and selected common template. This is source wiring validation,
not configured SMTP endpoint/account or runtime readiness.

The coordinator witnessed the missing-helper manifest RED, then registration
GREEN. Independent review found and the author corrected unused-parent and
child-override errors, Docker Hub alias bypass and an interpolated/registry
GoTrue bypass. The direct-file unittest guard was moved after all test classes.
The first final staged gate failed Ruff formatting on four Python files; official
formatting preserved their ASTs. Fresh formatted-input rerun passed 229 tests
in 42.494 seconds, exit 0. Dedicated combined statement/branch coverage is
95% for `smtp_contract.py`, 82% for `smtp_public_source.py`, 90% overall.
A pre-format coverage database interpreted against formatted line numbers was
not a valid measurement and is not used for acceptance.

The actual changed metadata gate selected one governed document with zero
violations; the supplied Runbook and common README paths are not represented
as two selected governed records. Actual staged style/secret checks passed.
Manifest and workflow validators passed; existing SMTP/catalog routing and
permissions were preserved. Independent final specification/quality review
approved the exact staged source, including its semantic-equivalent formatting.
Main candidate checks and logical merge follow separately; no hosted CI or
remote delivery is inferred from these local checks.

The public real-source probe binds 46 files and selected ROOT images contain
no unresolved interpolation. It does not read private files or actual rendered
container configuration. Canonical COMM-002 stays protected; COMM-003 remains
the only proposed password-file unlink. Provider authentication/delivery, LAB
activation, external/job closure, current production recovery, rotation and
final operational retirement acceptance remain open. No new private unlink or
credential/runtime change occurred in this source correction.

### User acceptance and LAB GoTrue exclusion — 2026-10-12

At clean main `2773a20c1c24ce1b70f64b36fe8f6f5108f49542`, the user confirmed
acceptance of the delivered SMTP01/CLN01 changes and clarified that actual LAB
GoTrue SMTP connection configuration is not assigned by this Spec/Plan/Task.
The earlier coordinator summaries incorrectly listed missing LAB connection
settings and activation as outstanding SMTP01 completion conditions. They are
superseded here; no GoTrue connection, account provisioning, LAB activation or
LAB send is required to close this accepted increment.

Canonical COMM-002 wiring, the preserved LAB-only source mapping/wrapper,
COMM-003 retirement ownership and the attributed isolated test/restore
receipts retain their exact scopes. The 229-test combined source receipt and
local-main merge `2773a20c1` remain actual evidence; this user acceptance is not
another unit/native run, provider authentication, send, unlink or restore.
The canonical password remains protected and the already-absent duplicate is
not counted as a new deletion. Unresolved independently scoped material or
ROOT/P05 operational evidence is not silently converted to PASS.

The user also selected one existing mailbox for genuine sender/recipient tests.
Its address is held in the current user instruction, not reproduced in Git,
public fixtures or workflow exports. Selection does not itself send a message.
A future bounded ROOT/P05 send must record its actual provider outcome and
recipient/capture result; it must not enable LAB GoTrue to obtain that receipt.
No secret, runtime, account, credential, message or data changed in this unit.

Documentation verification used
`python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD`
with the five explicit owned document paths: five selected, zero violations,
exit 0. `bash .agents/skills/style-validation/scripts/classify-changed-files.sh`
selected only five authored Markdown files, exit 0. The existing
`bash scripts/validation/run-ci-precommit.sh --mode local-staged` passed style
and secret-leak checks, exit 0. Independent review found stale CLN source/PR
acceptance and SMTP W26 acceptance cells; they were corrected without changing
operational results. The final corrected document input requires its scoped
metadata/staged checks before the normal local-main commit. Implementation
UNIT, native/provider, recovery and HOME checks were not rerun for this
text-only correction; no new result is attributed to those lanes.

### SMTP01 latest-main reassessment — 2026-10-13

The current request supersedes the earlier local-only delivery instruction for
this increment: an owning-Spec PR needs fresh candidate checks and independent
review before merge. It does not reopen user-accepted source or completed Tasks.
`git fetch origin main` succeeded; the starting remote main was
`328871a94b42c13f676e61b40f026c906ebbc13d`, compared with supplied input
`23e37362b72e98028a4675f282819c0346ae59dc`. The original checkout was clean at
`98144b2`; concurrent dirty CLN01/SEC01 worktrees were preserved. No open remote
PR was observed. During the audit, main advanced to
`9fd0a396c4e0246be778c90fb5ef31435c08e977` through CLN01 PR #427; this receipt's
branch was fast-forwarded before editing. That change touched TSK-0007 only,
so the SMTP source checks below retain their actual `328871a` input.
Before delivery, the branch was fast-forwarded again to
`62556dc63b66c828c27e9c33017d26cdf70b8542` after SEC01 PR #428; its five
owned files changed no SMTP implementation or this Task.

| Scope | Classification | Owner / consumer / target | Recovery boundary |
| --- | --- | --- | --- |
| Root canonical source, public catalog, generator and preserved wrapper/alias | NO_CHANGE | SMTP01; COMM-002 sole value source; COMM-003 alias/tombstone | Preserve canonical file and exact consumer mapping |
| Fresh native/HOME authentication | RUNTIME_UNVERIFIED | Named HOME consumer and operator proof required | No send, restart or deployment performed |
| Private retirement and restore | CONSUMER_DEPENDENT | SMTP01 executor after CLN01 lease and consumer/custody proof | Independent canonical restore acceptance required |
| LAB runtime/tests, Wiki/apps, root images/scanner | OUT_OF_SCOPE | LAB excluded; Wiki preparation complete; no security warning confirmed | No resource or version change |

Root `smtp_password` still has one source at
`secrets/communication/smtp/smtp_password.txt`. The former
`infra/04-data/supabase/docker-compose.yml` is absent; current source is
`labs/supabase.yml`, retaining the target alias and wrapper. LAB execution is
excluded. Relative to supplied input, the selected SMTP files changed only
root Compose documentation routing and `test_smtp_proof.py` runbook routing;
no SMTP behavior fix was needed. PR #413 merged as
`34c7d4644fee6541d0d969390abf1bb54c16fd27`; that fact supplies no fresh delivery,
native authentication or private deletion receipt.

Read-only metadata identified `hy-home-server`, the matching default Docker
engine, checkout `/home/hyunyoun/data/hy-home.docker` and executor UID/GID 1000.
The canonical file was regular, not a symlink, UID/GID 1000, mode 0640,
link count 1 and executor-readable. The exact old file was absent.
Alertmanager was running with the matching checkout label and one canonical
read-only bind; no Supabase Auth consumer was observed. Exact old-path mounts
were zero; two read-only ancestor binds belonged to node-exporter/cadvisor,
with zero writable ancestor binds. No values, hashes, lengths or private rows
were read or recorded. Absence proves no new unlink, equality or row retirement.

The coordinator ran the SMTP-only unittest selection (contract, proof, public
source, generator, lock inheritance, captured-output safety and cleanup-timeout
cases) at `328871a`: 103 synthetic tests PASS, exit 0; LAB source/native cases
were excluded. Root Compose `config --quiet` with `.env.example` and
`git diff --check` passed, exit 0. Full document-link validation passed, exit 0,
with one retained historical-links-unrecorded warning. Independent source review
found no defects. Candidate documentation gates and remote delivery remain
separate from those baseline results. Independent security review at `62556dc6`
first returned exit 1 in 99 tests because system Python lacked `referencing`.
The same five SMTP modules then passed 99 tests, exit 0, with the installed
QA Python and system dist-packages used below; no source correction was needed.
Independent code/security reviews passed. Code review corrected a stale active
local-only delivery clause to historical wording without rewriting its evidence.

The exact SMTP-only command was:

```bash
rtk proxy env PYTHONPATH=/usr/lib/python3/dist-packages /home/hyunyoun/.hy-home-qa-tools/spec-0107-20261007/bin/python -m unittest tests.lib.ops.test_smtp_contract tests.lib.ops.test_smtp_proof tests.lib.ops.test_smtp_public_source tests.validation.test_smtp_generator tests.validation.test_smtp_lock_inheritance tests.validation.test_supabase_smtp_rehearsal.CapturedOutputSafetyTests tests.validation.test_supabase_smtp_rehearsal.FixtureCleanupTimeoutTests -q
```

Scoped Task metadata passed (one selected, zero violations, exit 0).
`python3 scripts/validation/run-ci-gate.py --profile changed --local-only`
passed using that installed QA environment at `62556dc6` plus this receipt
before result-only recording (exit 0): candidate metadata/version preflight
and document links. The existing unresolved `OPSFLOW_AIRFLOW_IMAGE` input
remained an unresolved input, not a pin or security verdict. The historical
archive-link warning remained. The final reviewed index still requires
`bash scripts/validation/run-ci-precommit.sh --mode local-staged` immediately
before the logical commit; remote candidate checks and merge remain separate.

`COMPOSE_CANONICAL_PASS` is source-graph PASS. `OLD_PATH_ZERO` records only exact
old-path absence. `WRAPPER_NATIVE_PASS`, `HOME_CONSUMPTION_PASS`,
`PRIVATE_DELETION_PASS`, `RESTORE_PASS`, HOME/MIGRATION/RECOVERY and new
`DELIVERY_PASS` are NOT_RUN in this receipt; historical receipts are preserved.
The retirement check was NOT_RUN because it reads canonical bytes/private
metadata. Two ancestor binds, missing CLN01 lease and unconfirmed jobs,
external consumers and restore custody prevent fresh helper apply.
The next bounded operation needs that lease and truthful consumer/recovery
proof. Preserve the canonical file/mapping; never implicitly recreate the old
plaintext duplicate. Reverting this logical receipt commit restores only text,
without claiming private data or runtime recovery.

### v29 current OpenBao handoff reconciliation — 2026-10-22

The v29 local request reuses completed verification and corrects the current
handoff against main `49fd95a6ed482d7194c840b43b73a030be6f3d5d`.
[SPEC-0243's recorded window outcomes](../../0243-openbao-window-readiness/tasks/tsk-0001-openbao-window-readiness.md)
include the 07:18 W2 Snapshot-token delivery, the 07:49 manual backup success,
the later protected Snapshot/R2 dump match, accepted `-06` restore, HOME 2.7.1
transition, W5 Agent rendering, W6 checks and 13:00:31 manual backup success.
These are reused dated records, not new observations from this reconciliation.
The current completion summary therefore no longer requests another Snapshot
token to remedy the historical token-absence failure.

The actual timer run, 26-hour freshness, sustained backup success and independent
data recovery remain separately unverified. Accepted SMTP01 source and bounded
restoreability evidence are unchanged; neither the OpenBao window nor the
completed SPEC-0243 readiness/source Task accepts all P06 consumers or the
outstanding exact SMTP retirement evidence. This prose-only correction changes
no Evidence, Criterion Acceptance, lifecycle event, credential or runtime.
Current metadata, links and lifecycle checks belong to the combined v29 local
validation recorded by the coordinator.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ledger rows | 1 | W8 | SPEC-0212 TSK-0002 items 03, 04 and 08 updated | This branch | PASS | W8 Baseline, Owner Map and HOME Observations | - |
| Owner map and HOME observations | 1 | W8 | Read-only probes and file map | HOME host 2026-10-08 | PASS | W8 Baseline, Owner Map and HOME Observations | - |
| Dev-valkey snapshot and replay | 7, 9 | W9 | Test RED then GREEN; HOME export; isolated restore | `abcc1d7a7` | PASS | W9 Dev-valkey Snapshot and Queue Replay | - |
| Secret file matrix | 4, 9 | W10 | Matrix test with two mutations; exact-image empty secret run | `4630384fe` | PASS | W10 Secret File Support Matrix | - |
| Residue and mail | 3, 6 | W11 | Mutation of the Bitnami test; runbook text | `ea6c69d59`, `b84b2b87c` | PASS | W11 Image Residue and Mail Outcomes | - |
| OpenBao snapshot | 7, 9 | W13 | Test RED then GREEN; six isolated cases | `4ef6d3f7d` | PASS | W13 OpenBao Raft Snapshot | - |
| Open WebUI key | 7, 9 | W14 | Test; exact-image key reuse | `06d2a8953` | PASS | W14 Open WebUI Key | - |
| CDC rehearsal | 6 | W15 | Opt-in rehearsal run | `619c984cb` | PASS | W15 CDC Stream Rehearsal | - |
| Gateway machine path | 4 | W16 | SSO rehearsal RED then GREEN; HOME anonymous probes | `e342aaa9d` | PASS | W16 Gateway Machine Path | - |
| SonarQube secret | 4, 9 | W17 | Isolated database login; empty-secret refusal; test | `a677d609c` | PASS | W17 SonarQube Secret | - |
| Third-round validation | 8 | W18 | Changed gate in a clean worktree | `9bf20d195` | PASS | W18 Validation | - |
| Validation | 8 | W12 | Changed gate in a clean worktree; pre-commit over the range | `c68df1daa` | PASS | W12 Validation and Handoff | - |
| SMTP01 baseline and RED | 14 | W26 | New source regressions failed on prior implementation | `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`; public source | PASS | W26–W30 SMTP01 Current Increment | - |
| SMTP source and wrapper | 14 | W27 | Canonical source/target, wrapper and fresh 141-test unit run | `3181921be795c5439e5ac77e462f62e47db6fa5d` | PASS | Current-source verification and delivery receipt | - |
| Catalog and guarded retirement | 14 | W28 | Exact alias, lock/root identity, race regressions and independent approval | `3d0a8a1b07c1f2df29c0f04f88ba8fa815fbd1bf`; synthetic files | PASS | Current session ownership and interfaces | - |
| Native SMTP boundary | 14 | W29 | Fresh six native plus four unit cases; exact image/platform and review | Fixture `794e314f`; digest-fixed synthetic inputs | PASS | Final native receipt | - |
| SMTP delivery and handoff | 8, 14 | W30 | Reviewed local-main source delivery and explicit user acceptance of the delivered scope | Main `2773a20c1`; user clarification 2026-10-12 | PASS | User acceptance and LAB GoTrue exclusion | - |
| Reported duplicate SMTP retirement | 14 | W30 | Assignee report of snapshot, restore, comparison and unlink; current canonical presence/duplicate absence independently observed only | Assignee commit `39ff7f915`; no independent restore receipt | DEFER | Reported SMTP Duplicate Retirement — 2026-10-11 KST | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 6 | accepted | Residue and mail, CDC rehearsal | Generation 5 row acceptance |
| 7 | accepted | Dev-valkey snapshot and replay, OpenBao snapshot, Open WebUI key | Generation 5 row acceptance |
| 9 | accepted | Dev-valkey snapshot and replay, Secret file matrix, OpenBao snapshot, Open WebUI key, SonarQube secret | Generation 5 row acceptance |
| 14 | pending | - | - |

## Review and Completion

The delivered SMTP01/CLN01 increment is user-accepted. This broader
second-round Task still contains separate owner work below; excluded LAB
GoTrue connection/activation is not an SMTP01 completion condition.

- Historical W10 Supabase secret-support gaps remain dated LAB evidence,
  outside the accepted SMTP01 increment; they require no LAB repair or
  activation here. Terrakube's 9 keys still need its separately owned Spring
  `configtree` verification and remain outside the HOME selection by test.
- The canonical SMTP file remains and the duplicate is absent. Assignee-reported
  retirement still needs external-consumer and exact unlink evidence; dated
  two-file isolated restoreability is now observed under the bounded contract;
  historical source delivery used local gates/review without PRs. This
  reassessment follows the current owning-Spec PR contract above. External-host
  absence remains unverified; excluded Supabase LAB activation is not required.
- Reuse the recorded 2026-10-22 W2 Snapshot-token delivery and subsequent manual
  backup successes described in the v29 reconciliation above. The historical
  missing-token failure does not require reissuance. Actual timer execution,
  26-hour freshness, sustained success and independent recovery remain open;
  manual backup success does not close those acceptance conditions.
- Decide whether `home-airflow` needs the password grant and which service
  accounts are used; enforce server-side PKCE `S256` per client after its
  login is checked. Sign in once through a protected route to confirm the
  new gateway path with a real session.
- n8n execution paths are verified only with an upgrade, which this round
  did not make. Airflow needs a DEV dataset, connection and DAG before
  watermark, backfill, retry, dead letter and quality gates can be tested.
- OpenSearch is not in the HOME selection and its indexes are rebuildable;
  a snapshot repository is needed only once a project registers a
  collection that cannot be rebuilt.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
