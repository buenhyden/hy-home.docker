---
title: "Cross-tier Contracts Second Round Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0005"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-08"
---

# Cross-tier Contracts Second Round Task

## Objective

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

## Work Log

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
| DELIVERY | IMPLEMENT | Logical commits pushed; draft owning PRs #412/#413; latest-main hosted acceptance and integration NOT_RUN |
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

#### Command receipts

All commands use synthetic fixtures or public tracked source in this worktree.
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

#### Current-source verification and delivery receipt

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
and 8 hosted checks PASS. It remains OPEN/DRAFT and unmerged. Remote main was
reconfirmed as `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`. SPEC-0204 draft
[PR #413](https://github.com/buenhyden/hy-home.docker/pull/413) is OPEN/DRAFT,
stacked on `codex/smtp01-contract`. Integration and SEC01 final-image retest
remain distinct prerequisites. Current native and gate receipts follow.

A later remote-main check returned
`cac9e10fa584754706598d624654e07e8d6531f4`: P09 issuance PR #414 is merged.
Its shared SPEC-0204 Spec/Plan changes must be reconciled with #413 by the
coordinator while preserving P09 criterion 13/W25 and CLN01 criterion 12/W24.
This branch has not been automatically merged or rebased onto that main.
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

#### Delivery checkpoint

Logical commits are contract `d90d9f1`, helper/catalog `3d0a8a1`, consumer
`3181921`, protected static repair `1f32477`, native fixture `63ac2cf`, and
operations evidence `7bb0d85`, and manifest regression fix `b37c1151a`. Their ordinary commit hooks and staged style
checks passed without bypass. Both owning draft PRs are pushed and unmerged.
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

The SPEC-0204 draft is stacked on `codex/smtp01-contract` so its diff contains
only its owning implementation/docs. Hosted candidate-quality triggers only
PRs targeting main: this stacked PR's required candidate result is NOT_RUN
until the coordinator merges the owning contract, rebases/retargets to latest
main and runs the actual latest-head required checks. Neither draft is merged.
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ledger rows | 1 | W8 | SPEC-0212 TSK-0002 items 03, 04 and 08 updated | This branch | PASS | W8 Baseline, Owner Map and HOME Observations | accepted |
| Owner map and HOME observations | 1 | W8 | Read-only probes and file map | HOME host 2026-10-08 | PASS | W8 Baseline, Owner Map and HOME Observations | accepted |
| Dev-valkey snapshot and replay | 7, 9 | W9 | Test RED then GREEN; HOME export; isolated restore | `abcc1d7a7` | PASS | W9 Dev-valkey Snapshot and Queue Replay | accepted |
| Secret file matrix | 4, 9 | W10 | Matrix test with two mutations; exact-image empty secret run | `4630384fe` | PASS | W10 Secret File Support Matrix | accepted |
| Residue and mail | 3, 6 | W11 | Mutation of the Bitnami test; runbook text | `ea6c69d59`, `b84b2b87c` | PASS | W11 Image Residue and Mail Outcomes | accepted |
| OpenBao snapshot | 7, 9 | W13 | Test RED then GREEN; six isolated cases | `4ef6d3f7d` | PASS | W13 OpenBao Raft Snapshot | accepted |
| Open WebUI key | 7, 9 | W14 | Test; exact-image key reuse | `06d2a8953` | PASS | W14 Open WebUI Key | accepted |
| CDC rehearsal | 6 | W15 | Opt-in rehearsal run | `619c984cb` | PASS | W15 CDC Stream Rehearsal | accepted |
| Gateway machine path | 4 | W16 | SSO rehearsal RED then GREEN; HOME anonymous probes | `e342aaa9d` | PASS | W16 Gateway Machine Path | accepted |
| SonarQube secret | 4, 9 | W17 | Isolated database login; empty-secret refusal; test | `a677d609c` | PASS | W17 SonarQube Secret | accepted |
| Third-round validation | 8 | W18 | Changed gate in a clean worktree | `9bf20d195` | PASS | W18 Validation | accepted |
| Validation | 8 | W12 | Changed gate in a clean worktree; pre-commit over the range | `c68df1daa` | PASS | W12 Validation and Handoff | accepted |
| SMTP01 baseline and RED | 14 | W26 | New source regressions failed on prior implementation | `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`; public source | PASS | W26–W30 SMTP01 Current Increment | pending |
| SMTP source and wrapper | 14 | W27 | Canonical source/target, wrapper and fresh 141-test unit run | `3181921be795c5439e5ac77e462f62e47db6fa5d` | PASS | Current-source verification and delivery receipt | accepted |
| Catalog and guarded retirement | 14 | W28 | Exact alias, lock/root identity, race regressions and independent approval | `3d0a8a1b07c1f2df29c0f04f88ba8fa815fbd1bf`; synthetic files | PASS | Current session ownership and interfaces | accepted |
| Native SMTP boundary | 14 | W29 | Fresh six native plus four unit cases; exact image/platform and review | Fixture `794e314f`; digest-fixed synthetic inputs | PASS | Final native receipt | accepted |
| SMTP delivery and handoff | 8, 14 | W30 | Fresh aggregate, independent review, logical commits and owning PR | Current SMTP01 branch | NOT_RUN | W26–W30 SMTP01 Current Increment | pending |

## Review and Completion

Not complete. These remain open, each with its owner action:

- Historical W10 result: the Supabase stack ignored 35 secret keys. SMTP01
  supplies only GoTrue SMTP consumption; DB/JWT/other support is still unresolved.
  Rebuild or retire the remaining stack source, which
  it lacks database URLs. Terrakube's 9 keys need Spring `configtree`, not
  yet verified. Both stay outside the HOME selection by test.
- Create the OpenBao snapshot token (RUN-0021) after unsealing; until then
  each run reports the recovery gap.
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
