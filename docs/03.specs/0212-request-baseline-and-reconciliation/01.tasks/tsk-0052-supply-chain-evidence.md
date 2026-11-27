---
title: "Supply-Chain Review and Artifact Evidence Task"
version: "0.1.19"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0052"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-10"
---

# Supply-Chain Review and Artifact Evidence Task

## Scope

### Objective and Parent

#### Objective

Finish the supply-chain evidence that TSK-0047 handed off for criteria 86 and
89. Criterion 104 gives every current update-ledger entry a fresh review and a
reviewed decision, so the latest-version gate passes or each unreviewable
entry is an explicit residual. Criterion 105 binds each selected image artifact
to its own signature, provenance and SBOM evidence. At initial issuance no
check had run; current partial source observations are recorded below.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Image supply-chain Task](tsk-0047-image-supply-chain-storybook.md)

### Inputs and Authority

On 2026-11-10 the owner (@buenhyden) set TSK-0047 criteria 86 and 89 to
not-required and approved this dedicated Task for the unfinished work. That
decision opens the Task only. Every network lookup waits for the owner to
approve its host scope in N1 below, under the
[approval boundaries](../../../00.workspace/04.quality/approval-boundaries.md).
No image pull, deployment or HOME change is part of this Task.

The starting state comes from the
[TSK-0047 supply-chain handoff](tsk-0047-image-supply-chain-storybook.md#supply-chain-handoff-2026-11-10):
on 2026-11-10 `security_update_gate` exits 2, with all 89 ledger entries
`blocked-evidence` (`fresh_review` and `reviewed_decision` missing for 89,
`primary_advisory` for 79).

## Execution Log

### Work Performed

#### Order

1. W109: review each ledger entry against its official release and advisory
   source, record the reviewed decision, and rerun the gate.
2. W110: for each selected artifact, verify the publisher signature and
   available provenance and SBOM against its exact digest, and record what the
   publisher does not provide.

Services that HOME runs go first; the rest follow in the same Task.

#### Open owner items

The following table preserves the initial questions. The current request and
public-origin section below records the later N1/N2 resolution.

| Item | Question | Needed by |
| --- | --- | --- |
| N1 | Which hosts may lookups reach? Already approved for earlier work: `github.com`, `api.github.com`, Sigstore, `cgr.dev`, the Alpine mirrors, `proxy.golang.org` and `sum.golang.org`. Registry reads also need Docker Hub, `ghcr.io` and `quay.io` metadata endpoints. | W109, W110 |
| N2 | All 89 entries now, or the services HOME runs first and the rest later? | W109 |

#### Current request and public-origin scope 2026-11-10

The current trusted user explicitly requested implementation of the complete
master change plan on2026-11-10. That request authorizes bounded anonymous
public source research and local ledger/test changes. It resolves N1 for the
actual official origins below and N2 as all89 current entries, prioritizing
HOME services. The earlier opens/NOT_RUN statements remain historical inputs,
not a renewed blanket permission wait. No credential, image layer, image
activation, remote write, paid inference or outside workspace is included.

The actual GET scope is `api.github.com` and `github.com` release metadata for
the48 repository paths in the recorded inventory; vendor pages at
`www.python.org/downloads/`, `www.postgresql.org/support/versioning/`,
`docs.confluent.io/platform/current/release-notes/index.html`,
`neo4j.com/deployment-center/`, and
`raw.githubusercontent.com/aws/aws-cli/v2/CHANGELOG.rst`; and anonymous
`hub.docker.com/v2/repositories/` tag metadata for the named ledger images.
The recorded queries have no pagination, authentication or binary download.
The one direct Docker Hub retry used5-second connect and10-second total limits.
Actual URLs, times, query counts and limits remain in the existing
`release-lookups.json#/master_20261110_public_refresh` source owner.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0052 | draft | ready | #current-request-and-public-origin-scope-2026-11-10 |
| SPEC-0212-TSK-0052 | ready | in-progress | #current-request-and-public-origin-scope-2026-11-10 |

#### Public source refresh result 2026-11-10

The source writer recorded49 GitHub GET attempts over48 repositories:
47 distinct published-final observations and one Searx latest-release404.
The Airflow request was repeated once in the grouped retrieval. Five vendor
pages were read. Five Docker Hub URL probes failed, including an initial
unmatched sandbox-name probe; the exact subsequent subjects and a direct
ollama-exporter retry remain recorded failures. A404 is not proof of absent
product tags, and GitHub non-prerelease metadata is not vendor stable-channel
proof.

All89 current ledger rows were classified:67 GitHub published-final facts,
13 direct Python/PostgreSQL stable-channel facts, four other vendor facts,
two local Storybook producer locations, two lookup failures and one excluded
external source. Only13 direct vendor-table stable fields were refreshed;
prior facts remain historical. No declared image pin changed.

The focused supply-chain regression suite passed88 tests in4.740 seconds and
the static policy check passed five contracts/13 cases. The latest-version
gate still exits2:13/89 have complete current lookup evidence;76 lack fresh
lookup,30 mismatch latest, four are unresolved, ten lack stable-channel proof
and seven lack a primary reference. These reason counts overlap. Missing or
unexpected services are0. All89 exact-subject signature/provenance/SBOM
executions remain NOT_RUN; release asset names/digests show availability only.
n8n full-image signature/scan remains TSK-0041 criterion60, while this Task
owns the other exact artifact residuals under criterion105.

#### Public source refresh continuation 2026-11-11

The 76 rows that previously lacked a fresh lookup were reviewed together with
the 13 rows that already had current lookup fields. The source writer renewed
73 public rows and retained three deliberately unrenewed internal or external
rows (`storybook`, `storybook-mcp`, and `blog-ingestion`). The durable request
and field-level receipt is
`release-lookups.json#/master_20261111_public_refresh`; its gate receipt is
`#/master_20261111_public_refresh/gate_revalidation`. All declared pins,
candidate targets, source bindings, security and artifact fields, and
historical observations remain unchanged.

The source writer made 49 root GitHub requests: 48 published-release responses
and one Searx latest-release 404. Four separate research packets recorded
primary supplier documentation or official tag metadata. A GitHub final-release
response alone was not treated as a stable-channel result. Supplier-specific
normalization recorded explicit stable, GA, current-production, supported-line,
or selected-line facts only where the supplier documentation supported that
meaning. Examples include Gatus stable package 5.38.0, n8n production stable
2.47.3 (separate from beta 2.48.0), and the selected Neo4j 5.26 LTS patch
5.26.33 (separate from global 2026.10.2). Confluent's current 8.4.1 line was
kept distinct from the selected 8.3.2 line. Pact Broker was corrected to the
selected Docker stream 3.0.0 / full image
3.0.0-pactbroker2.121.2, rather than the separately versioned Ruby application
release 2.122.0. These source facts do not verify an image artifact.

The rerun `latest_version_gate` still exits 2 with `ready=false`: 31 of 89
rows are complete and 58 retain one or more residuals. Those residuals are 43
target/latest mismatches, 26 missing stable-channel proofs, four unresolved
latest values, and three each without a fresh lookup or primary release
reference. Counts overlap. The three fresh/reference residuals are the two
local Storybook producers and external `blog-ingestion`; ComfyUI's unknown
target remains one of the four unresolved values. The source closure remains
`44e286a69d910939ba36f59fd65a08a4f4ac7a1ae5dd8e9be11e29af4bfdac84`, with
no missing or unexpected service.

The same revalidation reran `security_update_gate`, which still exits 2 with
zero complete rows: all 89 lack a fresh review and reviewed decision, and 79
lack a primary advisory. Release and channel research is not a security
applicability review, so no decision was fabricated to satisfy that gate.
This continuation ran no new exact-subject signature, provenance, SBOM, scan,
compatibility, recovery, runtime, deployment, or rollback checks. Historical
receipts remain bound to their recorded subjects; criterion105 artifact
verification remains NOT_RUN.

#### Official-advisory applicability continuation 2026-11-11

The durable review receipt is
`release-lookups.json#/master_20261111_advisory_review`; its gate receipt is
`#/master_20261111_advisory_review/gate_revalidation`. Every one of the 89
current ledger subjects now has a `reviewed_at` value, exact declared/source
binding, an official-advisory discovery/decision record or explicit
missing-origin residual, coverage limit, security applicability, separate
source action, and a latest-version disposition. The same records cover all 58
previous latest-version residuals. No declared pin, source input, selected
artifact, signature, provenance, SBOM, scan, compatibility, recovery or
acceptance field changed.

The bounded anonymous GitHub catalogue retrieval made 59 GET requests across
54 repositories and returned 1,088 records representing 688 unique advisory
identifiers; 51 endpoints completed. It is discovery evidence rather than a
claim that an empty or incomplete listing has no vulnerability: n8n returned
the same 100 records for four requested pages, SurrealDB returned the same 100
records for two pages before a 403, and `ollama-exporter` returned 404. The two
subjects without a primary advisory-source result are `ollama-exporter` and
external `blog-ingestion`. The absence of concrete advisory references and the
catalogue limitations are retained independently, so an endpoint failure or
empty result is not treated as absence of a security issue.

The security gate exits 2 with `ledger_complete=false`. It reports 29
ledger-complete rows pending independent verification, 54 `blocked-evidence`
rows, and six `blocked-no-fix` rows (60 blocked rows in total). Of the 89
reviewed classifications, 29 are component-scoped `NOT_AFFECTED`, 18 are
`AFFECTED` (12 patch candidates still need digest, scan, compatibility,
recovery and residual approval; six have no patch), and 42 are `UNKNOWN` and
therefore deferred. The 42 typed `reviewed_decision` residuals mean an
inconclusive classification, not an unreviewed subject. A component-scoped
`NOT_AFFECTED` decision does not assert that its complete image is clean.

The following decisions are source-only and separate normal version currency
from a security patch decision. Five declared image consumers carry the
affected pgBackRest component and require a candidate patch; encrypted
repositories also require a separately approved key/subkey inspection and, if
necessary, a new backup plus restore rehearsal. Qdrant's declared single-node
topology does not show the documented exploit path, but its version range is
affected. SurrealDB requires a candidate move from 2.7 to 4.0.1 with separate
migration, backup and restore planning, and Open Notebook requires the 1.15.1
fix candidate. The two OpenBao rows retain the vendor-unpatched `go-jose/v3`
line residual; existing acceptance is not renewed. SeaweedFS has publisher
no-fix evidence. Gatus lacks sufficient fixed-range evidence and remains
`UNKNOWN` even though normal version work is tracked.

Source binding discrepancies remain explicit residuals. MLflow has a 3.16.1
candidate, 3.17.2 rendered output and 3.18.0 Dockerfile input; OAuth has a
7.15.5 candidate but a 7.15.6 Dockerfile input. Pushgateway's selected 1.11.5
is newer than the reported 1.11.4 and is not downgraded. Neo4j's selected 5.26
LTS line and Confluent's supported 8.3 line are retained independently of
their newer global/current lines. n8n's direct production changelog names
2.47.3 stable and 2.48.0 beta, while the rendered GitHub UI difference remains
recorded; incomplete catalogue coverage and its separate runner product leave
the aggregate security decision `UNKNOWN`.

The revalidated `latest_version_gate` also exits 2 with `ready=false`: 33 of
89 rows are complete and 56 retain residuals. The overlapping reasons are 43
target/latest mismatches, 21 missing stable-channel proofs, four unresolved
latest values, and three each lacking fresh lookup or primary reference. Its
89-service/33-file closure remains
`44e286a69d910939ba36f59fd65a08a4f4ac7a1ae5dd8e9be11e29af4bfdac84`.
Twelve numeric current/candidate pairs are component proposals only, not
selected-image changes. No operational upgrade, image pull, build, scan,
deployment, credential use, recovery action or risk-acceptance renewal ran.

#### Exact artifact and official-source continuation (2026-11-11)

The owner's follow-up authorizes public registry reads and temporary isolated
scans for this review. The [version and artifact receipts](../../../../infra/09-platform-ops/security-updates/release-lookups.json)
record actions for the 56 previous latest-version residuals and the 60 open
security rows under `master_20261111_artifact_review`. The declaration and
target remain bound to the current source. The publisher's Renovate release
advanced to 44.227.4, and n8n's release notes identify 2.47.3 as stable.
Pushgateway has a 1.11.5 tag and matching image while the project's download
page and GitHub Latest still report 1.11.4. The 1.11.5 pin is retained pending
publisher channel confirmation.

The three public patch candidates have exact linux/amd64 manifest and matching
local Syft and Grype receipts. Qdrant's publisher signature verifies the
multi-platform index, which binds the scanned platform and its attached
SPDX and SLSA predicates. Keycloak and Open Notebook expose subject-matching
SLSA predicates. Their publisher signatures and publisher SBOMs are pending.

| Public candidate | Publisher signature | Grype Critical matches | Grype High matches |
| --- | --- | ---: | ---: |
| Keycloak 26.8.2 | Unverified | 1 | 5 |
| Open Notebook 1.15.1-single | Unverified | 48 | 512 |
| Qdrant v1.20.0-unprivileged | Verified index | 0 | 62 |

These counts describe package matches. Compatibility, recovery, and residual
adjudication remain required for all 12 patch rows. Nine rows await a final
custom artifact. SurrealDB, Tempo, OpenTofu, and the Storybook MCP Node runtime
have separately scanned upstream inputs. OpenTofu also has a verified upstream
index signature. For the five pgBackRest consumers the supplier fix floor is
2.59.3. Alpine publishes 2.60.0-r0 on edge; the two tracked build lines use
v3.23 and v3.24, which still list 2.57.0-r0 and 2.58.0-r0 respectively.

The six no-fix rows remain blocked on the applicable OpenBao go-jose v3 and
SeaweedFS advisories. For the 42 deferred rows, the receipt records observed
publisher advisories, lookup failures, and the action for each service. Exact
declared-image scans cover 20 of those services across 17 distinct images.
The Ollama exporter now has official Node.js and OpenSSL evidence for packages
found in its image. Service applicability remains pending. Blog ingestion
still needs evidence from its external producer. GitHub API pagination and
registry access failures are recorded alongside their bounded fallbacks.

### Blockers and Decisions

#### D09 v9 pass (2026-11-27)

On 2026-11-27 the user requested D09 of the v9 prompts
(`_workspace/workspace_task_prompts_20261127_progress_v9/`, prompt
`09_security_versions_resources_storybook.md`), limited to its scope, with
commit, push, PR and merge. Work ran in the primary checkout on branch
`fix/d09-v9-timescale-template1` from `main` `f4375604a`.

- TimescaleDB 2.32.1 regression: the "HOME apply of TimescaleDB 2.32.1" row
  ran `ALTER EXTENSION timescaledb UPDATE` in `postgres` only. `template1`
  kept 2.30.3, whose library the new image does not ship, so every
  `template1` session failed, `pg_dumpall` aborted and the nightly backup
  exited 1 on 2026-11-27 03:34 KST (SPEC-0212 TSK-0046, D08 v9). With the
  owner's approval in this chat the update ran in `template1` as the first
  statement of a fresh session; `opsflow_dev` has no TimescaleDB. The dev-pg
  README now states the every-database step.
- Gates on the current ledger: `latest_version_gate` and
  `security_update_gate` both fail for all 86 entries because no entry has a
  fresh lookup or review (last `checked_at` 2026-11-10, older than the 7-day
  window); 51 entries also differ from the upstream latest. The registered
  `sync-update-ledger.sh` only binds Renovate pin bumps and never contacts
  the network, so a fresh review needs its own official-source round; no
  lookup was invented.
- Rehearsal pins, aligned on 2026-11-27 at the owner's request: every
  native rehearsal now pins the companion images HOME runs, PostgreSQL 18.7
  (`sha256:0115267a…`), Valkey 9.1.4 (`sha256:56729e68…`) and SeaweedFS 4.54
  (`sha256:4b42c212…`), and the n8n notifier rehearsal Mailpit 1.34.0
  (`sha256:23a2ef85…`), in `_opsflow_airflow_native_fixture.py`,
  `_opsflow_native_inputs.py`, `test_opsflow_database_rehearsal.py`,
  `test_supabase_smtp_rehearsal.py` and `test_mng_valkey_acl.py`. The Airflow
  native rehearsals pass 17/17 on them. The n8n notifier base and runner stay
  at the reviewed 2.43.6 SEC01 candidate: its source-binding labels come
  from a reviewed candidate build that the repository has no builder for,
  the HOME image `hyhome/n8n:2.46.6-local` carries no such labels, and the
  runner must match the base, so moving them needs a new reviewed 2.46.6
  candidate build instead of a weaker binding check.
- Fresh upstream review for criterion 104, 2026-11-27 10:00 UTC: the ledger's
  `latest_version` facts are from 2026-11-10, so most `latest_mismatch`
  results compare a newer target with a stale fact (for example `alloy`
  target 1.22.0 against recorded 1.21.3). A read-only lookup of the latest
  release of each of the 54 GitHub-sourced root entries (39 repositories,
  `gh api repos/<owner>/<repo>/releases/latest`) found 28 equal to
  upstream, 21 behind and 5 differing for other reasons; the
  other 32 entries cite non-GitHub sources (for example the PostgreSQL
  versioning page) and are not yet looked up. The entries not equal to
  upstream:

| Service | Repository | Target | Upstream latest (release, date) | State |
| --- | --- | --- | --- | --- |
| `alertmanager` | prometheus/alertmanager | 0.35.0 | v0.35.1 (2026-11-24) | behind |
| `crawl4ai` | unclecode/crawl4ai | 0.9.5 | v0.9.6 (2026-11-20) | behind |
| `dev-valkey` | valkey-io/valkey | 9.1.4 | 9.2.1 (2026-11-26) | behind |
| `dev-valkey-exporter` | oliver006/redis_exporter | 1.97.0 | v1.99.0 (2026-11-24) | behind |
| `gatus` | TwiN/gatus | 5.37.0 | v5.38.0 (2026-10-28) | behind |
| `k6` | grafana/k6 | 2.3.0 | v2.4.0 (2026-11-12) | behind |
| `loki` | grafana/loki | 3.7.8 | v3.7.10 (2026-11-13) | behind |
| `mlflow` | mlflow/mlflow | 3.16.1 | v3.18.0 (2026-11-04) | behind |
| `mng-valkey` | valkey-io/valkey | 9.1.4 | 9.2.1 (2026-11-26) | behind |
| `mng-valkey-exporter` | oliver006/redis_exporter | 1.97.0 | v1.99.0 (2026-11-24) | behind |
| `oauth2-proxy` | oauth2-proxy/oauth2-proxy | 7.15.5 | v7.15.6 (2026-11-05) | behind |
| `opensearch` | opensearch-project/OpenSearch | 3.10.0 | 3.10.1 (2026-11-24) | behind |
| `opensearch-dashboards` | opensearch-project/OpenSearch-Dashboards | 3.10.0 | 3.9.0 (2026-10-12) | differs |
| `opentofu` | opentofu/opentofu | 1.13.1 | v1.13.10 (2026-11-23) | behind |
| `pushgateway` | prometheus/pushgateway | 1.11.5 | v1.11.4 (2026-10-08) | differs |
| `redisinsight` | RedisInsight/RedisInsight | 3.10.1 | 3.10.2 (2026-11-24) | behind |
| `renovate` | renovatebot/renovate | 44.255.1 | 45.1.1 (2026-11-27) | behind |
| `seaweedfs-filer` | seaweedfs/seaweedfs | 4.54 | 4.55 (2026-11-23) | behind |
| `seaweedfs-master` | seaweedfs/seaweedfs | 4.54 | 4.55 (2026-11-23) | behind |
| `seaweedfs-s3` | seaweedfs/seaweedfs | 4.54 | 4.55 (2026-11-23) | behind |
| `seaweedfs-volume` | seaweedfs/seaweedfs | 4.54 | 4.55 (2026-11-23) | behind |
| `surrealdb` | surrealdb/surrealdb | 2.7.0 | v4.0.1 (2026-11-09) | behind |
| `tempo` | grafana/tempo | 3.1.0 | v3.1.1 (2026-10-21) | behind |
| `n8n-sandbox-certs` | n8n-io/n8n-sandbox-service (source not reviewed) | 1.16.0 | no release (404) () | differs |
| `n8n-sandbox-api` | n8n-io/n8n-sandbox-service (source not reviewed) | 1.16.0 | no release (404) () | differs |
| `n8n-sandbox-runner-1` | n8n-io/n8n-sandbox-service (source not reviewed) | 1.16.0 | no release (404) () | differs |

- Update round of 2026-11-27, limited by the owner to releases at least 7
  days old (POL-0086-R59 now applies the R44 release age and R45 major
  approval to manual and agent rounds). Of the six eligible entries, Loki
  3.7.10, Tempo 3.1.1, MLflow 3.18.0 and oauth2-proxy 7.15.6 already run on
  HOME and k6 2.4.0 is declared; their "behind" state is the stale
  `target_version` fact plus version-carrying Compose tags (`hy/loki:3.7.8-
  seaweedfs`, `hy/tempo:3.1.0-seaweedfs`, `hy-home/mlflow:3.17.2-local`) that
  no tool updates. Retagging them is refused by `sync-update-ledger.sh`
  (R52) and needs a ledger update with evidence, so it is left for its own
  change. gatus is built from a commit tarball with a SHA-256 that Renovate
  cannot track; v5.38.0 (`d255d0cd…`, 2026-10-28) fails the build because 3
  of 5 hunks of the local OIDC hardening patch no longer apply to
  `security/oidc.go`, so gatus stays on the reviewed build until the patch is
  rebased and reviewed.
  These are explicit residuals: the ledger facts are not rewritten from this
  read-only lookup, and the behind entries need an update round (Renovate PR,
  SEC01 review, staged HOME apply) before the latest gate can pass.
- Tag cleanup of 2026-11-27 (owner: a tag must not name a past version and
  must reflect the running release). Root cause: Renovate bumps the Dockerfile
  `FROM`, but nothing renamed the Compose tag of the locally built image.
  `scripts/lib/supply_chain/local_image_tags.py` now derives the tag version
  from the same-named `FROM` base; `sync-tech-stack-versions.sh` renames a
  stale tag in `--write` (the existing Renovate post-upgrade command, so the
  R23 command allowlist is unchanged; Compose files joined the
  `fileFilters`) and fails in `--check`; `ledger_rebind` accepts only that
  exact rename as an unverified row (POL-0086-R60). Loki, Tempo and MLflow
  moved to `hy/loki:3.7.10-seaweedfs`, `hy/tempo:3.1.1-seaweedfs` and
  `hy-home/mlflow:3.18.0-local`; their advisory reviews moved to
  NOT_AFFECTED (Tempo `patch_resolved`, Loki and MLflow `defer_resolved`),
  and the test that pinned `hy/tempo:3.1.0-seaweedfs` now derives the tag
  from the Dockerfile. Rows not covered: tags without a version (`hy/gatus:
  local`), a build file chosen by variable (n8n, oauth2-proxy) and bases with
  another name (mng-pg, dev-pg); each already names its running version.
- Gatus v5.38.0 of 2026-11-27. Upstream added OIDC logging, so 3 of 5
  `security/oidc.go` hunks no longer applied. The patch was rebuilt by a
  3-way merge of the 5.37 patched file onto 5.38, keeping PKCE S256, Secure
  and HttpOnly cookies, constant-time state and nonce checks, exact subject
  match, callback cookie clearing and the protected data routes, and taking
  upstream's logs (the IdP `error` values are logged with `%q`). An
  independent security review returned APPROVE. `GATUS_VERSION` in the
  Dockerfile now gives the tag `hy/gatus:5.38.0-local`: `local_image_tags`
  reads an `ARG <NAME>_VERSION` when no same-named `FROM` exists and prefixes
  an unversioned tag. The advisory row moved to `defer_resolved`.
- n8n 2.49.7 of 2026-11-27. HOME's 2.46.6 was affected by eight n8n
  advisories (GHSA-q8rc-7m84-mfvj and GHSA-w6f8-8qh4-h3j4 high); the newest
  release past the 7-day age, 2.48.7, still carried four, so the owner chose
  2.49.7 (released 2026-11-26) through the POL-0086 security fast path, a
  recorded exception to R59. n8n, n8n-worker and the runner moved together;
  OpsflowSmtp moved to the bundled `n8n-workflow` 2.49.5 and both image builds
  now assert that equality. The version tests no longer hardcode 2.46.6: they
  require one version across Compose, both Dockerfiles and the runner tag, a
  digest-pinned runner, and a package and lock that agree with the build
  assertion. The reviewed candidate `hy-home/sec01-n8n:2.49.7-opsflow-
  099418ca2fb4` was built from a `git archive` of `4a5c7fe86` with the
  source-binding, source-tree and revision labels, and the native rehearsal
  inputs were repinned to it and to `n8nio/runners:2.49.7`. The first native
  runs exposed rehearsal environments that the D03 named mng-valkey
  credentials change had left stale (no empty `N8N_VALKEY_USERNAME`, a
  non-`n8n` Bull prefix), so main never became ready; both fixtures now
  follow the entrypoint. The Bull identity probe no longer pins the n8n
  release (2.43.6), only the patched Bull 4.16.4 and ioredis 5.3.2, which
  2.49.7 bundles unchanged. The advisory review stays UNKNOWN for the reasons
  it gave before (incomplete catalog pagination, custom component and
  transitive contents). D11 receives the retirement of the unpublished probe
  workflow `d06e12CodeRunner01` (workflow_entity id), now that the P03 native
  runner scenario, including `code_generation_blocked`, passes on the running
  version, plus the superseded `hy-home/sec01-n8n` 2.42.6 and 2.43.6
  candidate images and the retained failed-attempt directory
  `/tmp/hyhome-retained-n8n-2.49.7-attempt1-cc76d6c8` (synthetic data).
- D09 v9 remaining census of 2026-11-28 (owner re-request of D09; T01 and
  T02 above, T03 to T07 here, read-only on `main` `a8576cc8a`):

| Task | Finding | Verdict |
| --- | --- | --- |
| T01 ledger | 86 entries and 86 expected services. `latest_version_gate` exit 2: 83 lack a fresh lookup (Loki, Tempo and MLflow have one), 47 differ from the latest, 18 lack a stable channel; `security_update_gate` exit 2: all 86 lack a fresh review, 35 a reviewed decision | Criterion 104 needs a full official-source review round of all 86 entries (owner decision on running it); 105 unchanged |
| T03 Bitnami | No Bitnami image, build or vendor label in tracked `infra/` or among running containers | Closed without change |
| T04 common settings | Hardening baseline, Compose validation (62 selections, 287 services, HOME 46) and supply-chain policy pass; all 57 running `hy-home-infra` containers match their effective Compose memory, CPU, PID, read-only, init and cap_drop values; 30 exceptions, none past `review_by`. Two still said "NOT_RUN: not started": the privileged DinD runner and the sandbox certificate job | Verification text of both updated from current observation and D06 v9 (TSK-0123 E04); the DinD exception stays, it proves declared confinement, not host isolation |
| T05 resources | Highest memory use 56% of its limit (Prometheus 1157/2048 MiB, Ollama 4508/8192 MiB), 0 OOM kills and 0 restarts, GPU 3 MiB of 6 GiB idle, host 19 GiB available, disk 76% | No observed bottleneck, so no limit change and no load comparison; `docker stats` returns "page not found" on this daemon, so memory was read from the cgroups |
| T06 Storybook | HOME runs `494d16fe` (no Storybook change since); routes 302, MCP 401, metadata 200. `npm audit` on the current lock: 7 moderate, 0 high, all build-only tooling through `minimatch` GHSA-g3hv-75wg-m249 and `glob` GHSA-3g3m-2fjr-6pw4, which now have fixes (minimatch 11.0.9 of 2026-11-16, glob 14.0.6 of 2026-11-12). In a scratch copy, overrides to those versions give 0 vulnerabilities and clean install, lint, typecheck and `build-storybook` pass | Owner decision: adopting them needs a new Storybook artifact and a HOME redeploy |
| T07 platform tools | Terrakube has no HOME service, include or container; REQ-0010 already calls it an optional isolated experiment. OpenTofu is a one-off `iac` job with no tracked configuration or state. Renovate runs weekly. The 2026-11-27 backup ran `restic check` with no errors over 12 local snapshots and copied the new snapshots to R2 | Closed without change; a Restic restore drill stays with SPEC-0204 TSK-0003 |

## Verification Evidence

### Results

The first two NOT_RUN rows preserve initial issuance. Their N1/N2 wait text
is historical. Later rows record the source observations, partial exact
artifact verification and the current gate results.

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ledger fresh review | 104 | W109 | `security_update_gate` against the update ledger | 89 entries at the start of the Task | NOT_RUN | Waits for N1 and N2. | required | - |
| Artifact verification | 105 | W110 | Per-artifact signature, provenance and SBOM verification | Selected image digests | NOT_RUN | Waits for N1 and W109. | required | - |
| Public metadata refresh | 104 | W109 | anonymous-public-source-research | Source648a78a26, unchanged supply inputs at c463e4ae5 | PASS | Existing release-lookups/update-ledger master_20261110_public_refresh;89 rows classified, stable-channel limits preserved | optional | - |
| Focused source regression | 104 | W109 | supply-chain-regression | Refreshed local source records | PASS | Writer receipt:88 tests in4.740s; static policy five contracts/13 cases | optional | - |
| Current latest-version gate | 104 | W109 | latest-version-gate | Refreshed89-entry source ledger | FAIL | Exit2;13 complete,76 fresh missing,30 mismatch,4 unresolved,10 channel and7 reference residuals | required | - |
| Official source continuation | 104 | W109 | anonymous public release/channel research | 76 former fresh-lookup residuals plus 13 retained current rows | PASS | `release-lookups.json#/master_20261111_public_refresh`; 73 public rows renewed and three internal/external rows retained as residuals | optional | - |
| Revalidated latest-version gate | 104 | W109 | `latest_version_gate` | 89-entry ledger; source HEAD `b17895e7181431b7282f8e95bc6c5e4f44ab4517` | FAIL | Exit2;31 complete,58 residual;43 mismatch,26 channel,4 unresolved,3 fresh and3 reference; counts overlap, service coverage exact | required | - |
| Revalidated security-update gate | 104 | W109 | `security_update_gate` | Same 89-entry ledger | FAIL | Exit2;0 complete;89 fresh-review,89 decision,79 advisory residuals; release facts do not establish security applicability | required | - |
| Revalidation regression | 104 | W109 | focused supply-chain regression | Updated ledger facts | PASS | Initial suite:94 PASS in4.781s. The first post-change run recorded three obsolete n8n-2.46.6 expectation failures in4.839s; a first corrected suite passed94 tests in7.295s. The final robustness run passed94 tests in5.411s; it requires a residual action only for a version mismatch, rather than for every other residual. Ruff, formatting and diff checks passed. Static policy remains PASS (five contracts/13 cases). | required | - |
| Official-advisory continuation | 104 | W109 | anonymous official advisory applicability review | All 89 current ledger subjects and all 58 preceding latest residuals; source base `305d93a8dbb16b71f7c34a55a7b20370f78d6f6f` | PASS | `release-lookups.json#/master_20261111_advisory_review`; 59 GitHub GETs/54 repositories, 1,088 returned records/688 unique identifiers, with incomplete n8n and SurrealDB pagination and `ollama-exporter` 404 retained as limits | required | - |
| Revalidated latest-version gate (advisory continuation) | 104 | W109 | `latest_version_gate` | 89-entry ledger and 33-file source closure | FAIL | Exit2; 33 complete and 56 residual;43 mismatch,21 channel,4 unresolved,3 fresh and3 reference residuals (overlap); exact service coverage and closure hash retained | required | - |
| Revalidated security-update gate (advisory continuation) | 104 | W109 | `security_update_gate` | Same 89-entry ledger | FAIL | Exit2; all89 fresh reviews recorded;29 ledger-complete pending independent verification,54 blocked-evidence and6 blocked-no-fix. No artifact-level security proof or operational acceptance is inferred. | required | - |
| Advisory gate policy check | 104 | W109 | static supply-chain policy | Updated review contract | PASS | Five contracts/13 cases; policy/static result only, not a live artifact or recovery observation | required | - |
| Advisory review regression | 104 | W109 | focused supply-chain gate tests | Frozen `master_20261111_advisory_review` records | PASS | TDD RED: one expected missing-key failure; integration then exposed and corrected three empty-reason failures. Initial GREEN:96 tests in4.970s, including two new tests in0.104s; Ruff, formatting and lint passed. No production gate code changed. | required | - |
| Exact artifact investigation | 105 | W110 | Registry and isolated Cosign, Syft and Grype | 12 patch rows | FAIL | Three exact final scans; one verified final index signature and matched published SBOM. Nine final custom images pending. Scans, publisher evidence and remaining actions are bound to the named subject. | required | - |
| Official evidence and follow-up | 104 | W109 | Public release, security and package sources | 56 latest residuals and 60 security residuals | FAIL | 56 latest actions, six no-fix reviews, 42 deferred decisions, and 20 deferred services with exact scans. One primary advisory reference still missing. | required | - |
| Latest-version gate (artifact continuation) | 104 | W109 | `latest_version_gate` | 89 ledger rows and 33 Compose source files | FAIL | Exit2; 33 complete and 56 residual. Both gates independently match the same 89 services and source closure. | required | - |
| Security-update gate (artifact continuation) | 104 | W109 | `security_update_gate` | Same 89 rows and source closure | FAIL | Exit2; 29 pending independent verification, 54 blocked-evidence, six blocked-no-fix. Exact candidate and scan gaps fell from 12 to nine; the primary advisory gap fell from two to one. | required | - |
| Artifact gate regression | 104 | W109 | Focused supply-chain and CI routing tests | Ledger and lookup references | PASS | RED reproduced the absent artifact evidence. The final focused run passed 97 tests; static policy passed five contracts and 13 cases. | required | - |
| Controller dependency audit | 104 | W109 | `pip-audit` and `npm audit` | Controller lock and Storybook production lock | FAIL | Python audit reported 25 findings across 36 checked requirements. Storybook npm audit reported zero. Both locks match the source baseline; controller findings need separate dependency triage. | optional | - |
| Renovate advisory refresh 2026-11-24 | 104 | W109 | Official advisory listings: GitHub repository advisories, the Go advisory database and the PostgreSQL security page | PR1048 aws-cli 2.40.4; PR1141 alertmanager 0.35.0, alloy 1.22.0, cadvisor 0.61.1, dozzle 11.5.0, grafana 13.3.1, postgres 18.7 (grafana-db-provision), node-exporter 1.13.1, prometheus 3.16.0, pyroscope 2.4.4 | PASS | Each version change got a fresh advisory review bound to its new subject in update-ledger and release-lookups: seven NOT_AFFECTED outside every published range, cadvisor and node-exporter UNKNOWN (no published advisory, no image scan). Rows whose image did not change follow only their Compose input hash; same-tag digest refreshes in PR1047 keep their version-based assessment. No image was pulled, scanned or recreated | required | - |
| Renovate subject rebind regression | 104 | W109 | Focused supply-chain, readiness and restore tests | Each Renovate head after its Renovate rebase plus the evidence commit | PASS | PR1048: update-gate, ledger-rebind and policy tests OK. PR1141: the same 57 tests OK, plus the Prometheus isolated restore test after its image followed the 3.16.0 pin. PR1047: 201 tests OK, with the readiness identity list (keycloak 26.8.2, traefik v3.8.0 latest digests and amd64 config IDs), the sample alpine build material and opensearch-dashboards pins following the update as in b9349ad3e | required | - |
| Renovate PR hosted CI (first PR1141 run) | 104 | W109 | `gh pr checks` on the merged head | PR1141 head 4e6dae3f | FAIL | candidate-core failed `test_image_matches_the_compose_pin`: scripts/operations/prometheus-isolated-restore.py still pinned prometheus v3.15.1; fixed in 1c162e85 | required | - |
| Renovate PR hosted CI | 104 | W109 | `gh pr checks` on the merged head | PR1140 (merged e2839452), PR1048 (d8665e3f), PR1141 (9808e2d4), PR1047 (710645e6); each brought up to date by a Renovate run with the rebase label and merged one at a time, security first | PASS | candidate-core, candidate-quality, candidate-routing, CodeQL and GitGuardian passed on every merged head with none pending. Merge is not application: no HOME service was recreated | required | Renovate PR hosted CI (first PR1141 run) |
| PostgreSQL 18.6 exposure | 104 | W109 | PostgreSQL security page, checked 2026-11-24 | Rows still declaring postgres 18.6: mng-pg (server) and the mlflow, mng-pg-init, mng-pg-monitor-provision and pact-broker provisioning jobs | FAIL | 18.7 fixes CVEs that affect 18.6, including CVE-2026-120139, -120142, -120144 and -120150 (CVSS 8.8, authenticated code execution). The 2026-11-11 assessments predate them and now carry that note; the fix is the per-image data-tier update to 18.7 and an owner-approved recreate, not yet done | required | - |
| HOME apply of the Renovate images | 104 | W109 | Runtime apply: `docker compose -p hy-home-infra up -d --no-deps --no-build --pull never --force-recreate <service>` (RUN-0086 step 11), one service at a time | Owner request 2026-11-24: apply the merged Renovate versions and PostgreSQL 18.7 to the running HOME services; alertmanager, alloy, cadvisor, dozzle, grafana, node-exporter, prometheus, pyroscope, registry, crawl4ai-egress, crawl4ai-loopback (pulled), loki and tempo (rebuilt) | PASS | Pre-check: every target healthy on its previous image. Post-check: each reached healthy on its declared digest before the next started. Rollback: recreate from the previous Compose revision; the old loki/tempo image IDs were no longer present to tag, so their rollback is a rebuild from that revision | required | - |
| HOME apply of PostgreSQL 18.7 | 104 | W109 | Runtime apply of mng-pg and dev-pg with the 18.7 migration steps | Owner request 2026-11-24: apply the merged Renovate versions and PostgreSQL 18.7 to the running HOME services; PR1173 images built locally | PASS | Pre-check: both healthy on 18.6, `pgbackrest check` passed, pre-upgrade diff backups 20261121-184258F_20261124-084853D and 20261121-184346F_20261124-084902D. Both recreated healthy on PostgreSQL 18.7 with `pgbackrest check` passing. No btree index on bpchar and no gist_trgm_ops index exists in any of 14 databases, so no REINDEX was needed. timescaledb in dev-pg postgres and template1 updated 2.30.2 to 2.30.3. New full backups 20261124-085218F (mng) and 20261124-085311F (dev). Rollback: the 18.6 images remain locally with the diff backups. pgBackRest 2.58 stays below 2.59.3 | required | - |
| Storybook ingress rehearsal (first run) | 104 | W109 | `HYHOME_STORYBOOK_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.StorybookIngressRehearsalTests` | PR1174 head with the next 16.4.5 images, before the harness fix | FAIL | Three of four tests raised KeyError in the shared SSO summary helper before any assertion, on main with the old image as well; a harness defect, not a Storybook result | required | - |
| Storybook ingress rehearsal | 104 | W109 | `HYHOME_STORYBOOK_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.StorybookIngressRehearsalTests` | PR1174 head after the summary fix (f35f30ad) | PASS | 4/4: anonymous requests get no content and no login page, non-admins never reach the origin, admins read index, iframe, assets and manifests, and the remote MCP serves readers with a token for its URL only | required | Storybook ingress rehearsal (first run) |
| HOME apply of Storybook next 16.4.5 | 104 | W109 | `storybook_image.py build --push` and `verify --registry`, then the RUN-0086 recreate of storybook and storybook-mcp | Owner request 2026-11-24: apply the merged Renovate versions and PostgreSQL 18.7 to the running HOME services; PR1174 merged cebbfcec | PASS | Pre-check: both healthy on 9cd150bf. Post-check: both healthy on 9a8ccbf3; an anonymous request to storybook.hy.home.arpa gets 302 to Keycloak. Rollback: the 9cd150bf images remain locally and in the local registry. A final comparison finds only openbao and openbao-agent off their declarations, from an earlier change outside this apply | required | - |
| pgBackRest 2.60.1 apply (first run) | 104 | W109 | Runtime apply of mng-pg and dev-pg with pgBackRest 2.60.1 (RUN-0086 recreate) | Owner request 2026-11-24: move the provisioning jobs to 18.7, update pgBackRest and update openbao; PR1176 images | FAIL | Both recreated healthy on PostgreSQL 18.7 with pgBackRest 2.60.1 after pre-upgrade diff backups, but `COPY --chmod=0644` had made /etc/pgbackrest mode 0644, so `pgbackrest check` and WAL archiving failed with permission denied. A runtime `chmod 0755` restored check and archiving (failed_count 0) within minutes | required | - |
| pgBackRest 2.60.1 apply | 104 | W109 | Runtime apply of mng-pg and dev-pg with pgBackRest 2.60.1 (RUN-0086 recreate) | Owner request 2026-11-24: move the provisioning jobs to 18.7, update pgBackRest and update openbao; PR1177 images that create /etc/pgbackrest as 0755 | PASS | Pre-upgrade diff backups, recreate, healthy; /etc/pgbackrest drwxr-xr-x, `pgbackrest check` passes, pg_stat_archiver failed_count 0 on both. Full backups with 2.60.1: 20261124-111938F (mng) and 20261124-112045F (dev). Rollback: the previous 18.7 images with pgBackRest 2.58 remain locally | required | pgBackRest 2.60.1 apply (first run) |
| PostgreSQL 18.7 provisioning jobs | 104 | W109 | Compose pin and image pull | Owner request 2026-11-24: move the provisioning jobs to 18.7, update pgBackRest and update openbao; mlflow-db-provision, mng-pg-init, mng-pg-monitor-provision, pact-broker-db-provision | PASS | PR1176 pins postgres:18.7-alpine@0115267a and the image is pulled; the one-shot jobs were not re-run and take 18.7 at their next start | required | - |
| OpenBao 2.7.3 r4 owned build | 104 | W109 | `prepare-openbao-materials.py --allow-go-proxy`, `build-owned-image.py --phase plan` and `--phase build`, Syft and Grype | Owner request 2026-11-24: move the provisioning jobs to 18.7, update pgBackRest and update openbao; cosign-verified v2.7.3 source 0439ef58, Go 1.27.4 builder, go-jose v4 4.1.9 patch | PASS | Materials PASS (materials.json db042d0f), plan PASS, two-pass build PASS with binary 2e883560 and OCI identity matching, manifest 240e4a88; `bao version` v2.7.3+hyhome.go1.27.4.net0.62.0.r1. Syft 321 packages; Grype (DB 2026-11-24) High 11 and Medium 11: five OpenSSL 3.5.9-r1 CVEs without an Alpine fix and go-jose v3 3.0.5. PR1178 pins r4 | required | - |
| OpenBao r4 HOME window | 104 | W109 | RUN-0105 W3 snapshot, W4 server upgrade with manual unseal, W5 Agent reissue | HOME openbao and openbao-agent on 2.7.1 | NOT_RUN | The SEC01 gate needs the owner's acceptance of the r4 residuals, and W4 needs two unseal shares and a root token in owner custody; the agent cannot run the window. HOME still runs 2.7.1, which three High advisories affect | required | - |
| SEC01 review refresh of the 2026-11-26 Renovate images | 104 | W109 | Supplier GitHub repository advisories per image (`patched_versions` applied), vendor pages for Neo4j and Confluent, registry index and platform manifest reads for OpenSearch 3.10.0 | PRs #1244, #1242, #1249 (squash of #1248), #1243, #1246 | PASS | Qdrant, Open Notebook and Keycloak leave their patch rows (patch_resolved); Traefik leaves defer (new defer_resolved); SeaweedFS 4.54 stays AFFECTED no-fix (four 2026-11-09 advisories without a fixed version); OpenSearch stays UNKNOWN until its custom image has an SBOM and scan; the rest keep their class. Gate tests count four open patch and 41 defer rows | required | - |
| Missed sandbox image pin | 104 | W109 | p02 sandbox release test | #1249 head before the fix | PASS | Renovate left SANDBOX_RUNNER_DOCKER_SANDBOX_IMAGE at 1.8.1 while the api and runner moved to 1.15.0; it moved to the 1.15.0 index digest and the runner reported `sandbox image ready` for it | required | - |
| HOME apply of the 2026-11-26 images | 104 | W109 | Runtime apply: `docker compose -p hy-home-infra up -d --no-deps <service>` after a dry run that named only the target, one service at a time | Owner request 2026-11-26: update every infra service to its latest release and apply it; qdrant 1.20.2, dev/mng valkey exporters 1.97.0, kafka-exporter 1.11.0, mailpit 1.34.0, ollama 0.40.18, n8n and n8n-worker (rebuilt), n8n sandbox 1.15.0, oauth2-proxy (rebuilt), traefik v3.8.0, keycloak 26.8.2, kafka-1 8.4.1, seaweedfs 4.54 | PASS | Each target healthy before the next started. Data checks matched the pre-update baseline: Qdrant 0 collections; Keycloak 2 realms, 24 clients, 7 users and migration_model 26.8.2; Kafka 7 topics and quorum leader 1; SeaweedFS six buckets, Loki and Tempo writes resumed; the three probe routes kept their codes. Backups in `/home/hyunyoun/storage/volumes/backups/upgrade-20261126/`; previous images kept for rollback | required | - |
| Ollama GPU check | 104 | W109 | `ollama run` of minicpm-v4.6:1b, `ollama ps`, load log | GTX 1060 6GB (compute 6.1), driver 580.178.04, before and after 0.40.18 | PASS | Both versions 100% GPU with 25/25 layers on the cuda_v12 backend; 0.40.17 and 0.40.18 notes carry no NVIDIA change | required | - |
| HOME apply of TimescaleDB 2.32.1 | 104 | W109 | `pg_dumpall` backup, dev-pg recreate, `ALTER EXTENSION timescaledb UPDATE` in `postgres` | Owner request 2026-11-26; dev-pg on 18.7-ts2.30.3-pgbackrest2.60.1-r2 | PASS | Extension 2.32.1 on PostgreSQL 18.7 and pgBackRest 2.60.1; opsflow_dev 9 tables and 0 hypertables as before; dev-pg-exporter pg_up 1 | required | - |
| SEC01 review refresh of the 2026-11-27 batch | 104 | W109 | Supplier repository advisories with `patched_versions`, Valkey GHSA-3885-pq5f-788j page | PR #1258 (squash of the batch 2 Renovate PRs) | PASS | kafbat-ui 1.5.1, valkey 9.1.4, postgres-exporter 0.21.1, redisinsight 3.10.1 and the dockerfile 1.29 frontend keep their class; dev-valkey and mng-valkey 9.1.4 fix GHSA-3885-pq5f-788j, which affected 9.1.3 | required | - |
| HOME apply of the 2026-11-27 batch | 104 | W109 | `docker compose -p hy-home-infra up -d --no-deps <service>` after a dry run that named only the target, one service at a time | Owner request 2026-11-26; dev/mng postgres-exporter 0.21.1, kafbat-ui 1.5.1, redisinsight 3.10.1, dev-valkey and mng-valkey 9.1.4 | PASS | Each target healthy before the next; both exporters `pg_up 1`; dev-valkey 0 keys before and after; mng-valkey loaded its append-only file, the SSO route kept 302 and airflow-worker, airflow-scheduler and oauth2-proxy stayed healthy; n8n and n8n-worker each exited once on `EAI_AGAIN mng-valkey` during the recreate (16:35:43 UTC) and the restart policy brought them back, editor reachable at 16:37:11; mng-valkey keys 22 to 20 after the restart, likely TTL expiry, not verified because a per-key check needs credentials | required | - |
| mng-valkey data backup (first run) | 104 | W109 | `tar` of the mng-valkey data directory | mng-valkey 9.1.3 data directory, as the host user before the recreate | FAIL | `tar` exit 2: the host user cannot read `appendonlydir`, which the container user owns; the recreate ran anyway because the steps were chained with `;`, so no complete pre-upgrade copy exists. The partial file is kept as `mng-valkey-9.1.3-data-PARTIAL-no-aof.tar.gz` in `/home/hyunyoun/storage/volumes/backups/upgrade-20261126/` | required | - |
| mng-valkey data backup | 104 | W109 | `tar` of the mng-valkey data directory | mng-valkey 9.1.4 data directory after the upgrade, as the container user (read-only mount, no network) | PASS | `mng-valkey-9.1.4-after-upgrade.tar.gz` (2.4 MB, four append-only entries, mode 600) in `/home/hyunyoun/storage/volumes/backups/upgrade-20261126/`; the restore point is after the upgrade, not before it. Later stateful steps chain with `&&` and back up container-owned data as the container user | required | mng-valkey data backup (first run) |
| n8n opsflow rebuild after the tooling updates | 104 | W109 | n8n and n8n-worker rebuild and recreate | PR #1251 (nodemailer 10.6.0, axios override 1.21.1) | PASS | Both recreated at 15:21 UTC after the 15:00 merge and healthy; the opsflow package installed as `n8n-nodes-opsflow` carries nodemailer 10.6.0 (n8n's own copy stays 10.0.14); loading the node in a workflow was not exercised | required | - |
| Airflow 3.4.0 candidate build | 104 | W109 | Image build with in-image `pip check` and version asserts; `HYHOME_WORKFLOW_REHEARSAL=1 python3 -m unittest tests.validation.test_workflow_version_bundle` | PR #1259; base `apache/airflow:3.4.0-python3.13@sha256:a8d9d19c…`, official 3.4.0 constraints | PASS | Airflow 3.4.0, Keycloak provider 0.13.0, common-compat 1.23.1, Celery provider 3.26.0 (the 4.x major left out); 10 tests OK (8 unit, 2 isolated against index `7f956efc…`); OSV and apache/airflow list no advisory for the four versions, so the custom image stays UNKNOWN without an SBOM | required | - |
| HOME apply of Airflow 3.4.0 | 104 | W109 | `pg_dump -Fc` of `airflow` checked with `pg_restore --list`, `airflow-init` (`airflow db migrate`), then apiserver, scheduler, dag-processor, triggerer and worker one at a time | Owner request 2026-11-26; PR #1259 merged as `0799fac95`; no running Dag run | PASS | `airflow-3.3.2-db.dump` (73 table entries) in `/home/hyunyoun/storage/volumes/backups/upgrade-20261126/`; schema `d2f4e1b3c5a7` to `b4f1a7d2c903`; all five healthy on `hy-home/airflow:3.4.0-keycloak`; health endpoint metadatabase, scheduler, triggerer and dag_processor healthy; 7 Dag runs and 10 XCom rows (`xcom_v1`) as before; task instances 13 to 15 because the migration moved the 2 `task_instance_history` rows; 5 new paused example Dags; `/auth/login` 307 to the Keycloak `home-airflow` client. A new Dag run, Celery cancellation and OTel stay NOT_RUN | required | - |
| Storybook images on Node 26.13.1 | 104 | W109 | `scripts/operations/storybook_image.py build --push`, then `verify --registry` | Commit `494d16fe` (Node 26.13.1 base, Storybook 10.6.7, next 16.4.6); PR #1260 | PASS | Labels, revision.json, lockfile, UI package and manifest hashes match; registry indexes `6685fa70…` and `6d8d8b56…` with SBOM and provenance; storybook-mcp leaves the patch group because Node 26.13.1 postdates the 26.12.1 fix of CVE-2026-111497 | required | - |
| HOME apply of the Storybook images | 104 | W109 | `docker compose -p hy-home-infra up -d --no-deps <service>` after a dry run that named only the target, one service at a time | PR #1260; storybook and storybook-mcp at `494d16fe` | PASS | Both healthy on `494d16fe`; storybook routes 302 to SSO, storybook-mcp `/mcp` 401 and its protected-resource metadata 200, as before; in-image `revision.json` names `494d16fe` and UI package 0.2.0; storybook-mcp runs Node v26.13.1; the static origin keeps no data, so no backup applied | required | - |
| SEC01 review refresh of the round 3 images | 104 | W109 | Supplier repository advisories with `patched_versions`, GitHub Go advisory database for `github.com/grafana/grafana` | PR #1269 (squash of Renovate PRs #1263 to #1266 and #1268) | PASS | Grafana 13.3.2 NOT_AFFECTED: no Go advisory affects 13.3.2; the repository advisories GHSA-8xmm-x63g-f6xv and GHSA-8wjh-59cw-9xh4 (2022, no patched version) were fixed in 9.3.4 and 8.3.4. aws-cli 2.41.2, Renovate 44.255.1 and pact-broker 3.2.0 NOT_AFFECTED; restic 0.20.0 and the n8n sandbox 1.16.0 images UNKNOWN without published advisories. Renovate again left `SANDBOX_RUNNER_DOCKER_SANDBOX_IMAGE` at 1.15.0; it was pinned by hand to 1.16.0. #1262 and #1267 were closed unlanded | required | - |
| Round 3 hosted CI (first run) | 104 | W109 | Hosted CI Quality Gates on the round 3 squash PR | PR #1269 head `d529e2247` | FAIL | candidate-core: `test_runtime_images_are_exact_digest_pins` (traefik) failed because #1262 refreshed only the Traefik line of the frozen core readiness override, whose runner pins index, manifest and config identity | required | - |
| Round 3 hosted CI | 104 | W109 | Hosted CI Quality Gates on the round 3 squash PR | PR #1269 head `77df15736`, override restored to its recorded pin | PASS | 9 checks passed and 2 skipped; merged as `1ea8f898d` | required | Round 3 hosted CI (first run) |
| Grafana data backup (first run) | 104 | W109 | `tar` of the grafana-data volume in a read-only, no-network container of the running image | grafana 13.3.1 stopped, running as the Grafana user 472 | FAIL | `tar` could not create the archive in `/home/hyunyoun/storage/volumes/backups/upgrade-20261126/` (permission denied); the `&&` chain stopped, so Grafana stayed stopped and was not recreated | required | - |
| Grafana data backup | 104 | W109 | `tar` of the grafana-data volume in a read-only, no-network container of the running image | grafana 13.3.1 stopped, running as root with the archive handed to the host user | PASS | `grafana-13.3.1-data.tar.gz` (207 MB, contains `grafana.db`, mode 600) in `/home/hyunyoun/storage/volumes/backups/upgrade-20261126/` | required | Grafana data backup (first run) |
| HOME apply of the round 3 images | 104 | W109 | `docker compose -p hy-home-infra up -d --no-deps <service>` after a dry run that named only the target, one service at a time | Owner request 2026-11-27; grafana 13.3.2, n8n-sandbox-api and n8n-sandbox-runner-1 1.16.0 | PASS | Grafana healthy, `/api/health` database ok on 13.3.2, unified storage migrations completed without errors, route 302 to login as before; sandbox api and runner healthy, the runner registered with the api and is configured for sandbox 1.16.0, n8n and n8n-worker stayed healthy. The sandbox image is fetched on the first sandbox execution, which was not run; aws-cli, Renovate, restic and pact-broker take their pins at their next one-off or deployed run | required | - |
| D09 v9 TimescaleDB template1 update | 104 | W109 | `ALTER EXTENSION timescaledb UPDATE` in `template1`; extension readback in every database; `pg_dumpall --schema-only` | dev-pg on `hy-home/dev-pg:18.7-ts2.32.1-pgbackrest2.60.1-r1`, owner approval 2026-11-27 | PASS | `template1` and `postgres` 2.32.1, `opsflow_dev` none; `pg_dumpall --schema-only` exit 0 (catalog warnings only); the full backup run is the owner step | required | - |
| D09 v9 gate state | 104 | W109 | `python3 -m scripts.lib.supply_chain.latest_version_gate` and `security_update_gate --input infra/09-platform-ops/security-updates/update-ledger.json` | `main` f4375604a | FAIL | Both not ready: 86/86 entries lack a fresh lookup or review; 51 differ from the upstream latest | required | - |
| Rehearsal pins on HOME versions | 104 | W109 | `OPSFLOW_AIRFLOW_NATIVE_IMAGE=sha256:7f956efc… python3 -m unittest -v tests.validation.test_opsflow_airflow_native_rehearsal`; static suites of the five repinned modules | Companions PostgreSQL 18.7, Valkey 9.1.4, SeaweedFS 4.54; Mailpit 1.34.0 in the n8n inputs; 2026-11-27 | PASS | 17/17 native tests, publication, retry, replay and restore PASS, cleanup PASS; 107 static tests OK | required | - |
| Fresh upstream release lookup | 104 | W109 | `gh api repos/<owner>/<repo>/releases/latest` for 39 repositories behind 54 root entries | 2026-11-27 10:00 UTC, read-only | PASS | 28 equal, 21 behind, 5 other; table in Blockers and Decisions | required | - |
| Local tag cleanup and HOME apply | 104 | W109 | `local_image_tags --check`; `docker compose -p hy-home-infra build loki tempo mlflow`; `up -d --no-deps --no-build --pull never <service>` after a dry run naming only the target, one at a time | Owner request 2026-11-27; branch `fix/local-image-tags-follow-base`; backup `hyhome-backup.service` success 19:51 KST | PASS | Check found exactly the three stale tags. Old and new images report the same binaries (loki 3.7.10 c792f585, tempo v3.1.1 9db7df79d, mlflow 3.18.0), so no data-format or database migration. Each healthy before the next; Loki `/ready` and 2,232 lines in the last 2 minutes; Tempo `/ready` and spans received; MLflow `/health` OK with no migration or error log. The old tagged images remain for rollback. Signature, SBOM and scan of the local images stay NOT_RUN | required | - |
| Gatus v5.38.0 rebase and HOME apply | 104 | W109 | Image build (`patch --fuzz=0`, `go test ./api ./security`); `up -d --no-deps --no-build --pull never gatus` after a dry run; HTTPS probes through Traefik | Owner request 2026-11-27 (gatus 진행); commit `d255d0cd…`, archive SHA-256 `b0a5cd58…`; `gatus.db` copied to `/home/hyunyoun/storage/volumes/backups/upgrade-20261127/` first | PASS | Patch applied without fuzz; `api` and `security` tests ok; healthy on `hy/gatus:5.38.0-local` (label 5.38.0); OIDC provider discovered and routes registered; `/oidc/login` 302 to Keycloak with `code_challenge_method=S256`; state, nonce and PKCE cookies HttpOnly, Secure, SameSite=Lax; `/api/v1/endpoints/statuses` 401 anonymously; `/api/v1/config` `oidc:true, authenticated:false`, no announcements; monitors resumed. A full browser login was not run | required | - |
| n8n 2.49.7 candidate build | 104 | W109 | `docker buildx build --load` of `infra/07-workflow/n8n/Dockerfile` from `git archive 4a5c7fe86`, labels `hyhome.source-binding`, `hyhome.source-tree`, `org.opencontainers.image.revision` | Owner choice 2026-11-27 (2.49.7, security fast path); binding `099418ca…` equal in the ledger and build-inputs (a first build labelled `a92e6afb…` was replaced: that hash predated formatting of a bound test file) | PASS | `hy-home/sec01-n8n:2.49.7-opsflow-099418ca2fb4`, `sha256:e4cbed50…`, linux/amd64, user 1000; build-time checks passed (`n8n --version` 2.49.7, OpsflowSmtp loads, peer `n8n-workflow` equals the bundled 2.49.5). OpsflowSmtp unit tests 38/38 with coverage thresholds in `node:26.13.1-alpine3.24` | required | - |
| n8n 2.49.7 native rehearsal | 104 | W109 | `OPSFLOW_N8N_NATIVE_REHEARSAL=1 OPSFLOW_N8N_NATIVE_IMAGE=sha256:<candidate> python3 -m unittest -v tests.validation.test_opsflow_native_rehearsal` | Candidate above, runner `n8nio/runners:2.49.7@sha256:be8031ab…`, companions PostgreSQL 18.7, Valkey 9.1.4, Mailpit 1.34.0 (IDs equal to their pins) | FAIL | Twice `n8n main readiness expired`: the entrypoint refused the stale rehearsal broker selection (`unsupported n8n broker selection`); a third start found the retained evidence directory | required | - |
| n8n 2.49.7 native rehearsal rerun | 104 | W109 | `OPSFLOW_N8N_NATIVE_REHEARSAL=1 OPSFLOW_N8N_NATIVE_IMAGE=sha256:<candidate> python3 -m unittest -v tests.validation.test_opsflow_native_rehearsal` | After the fixture env fix, candidate `sha256:e4cbed50…` (binding `099418ca…`) | PASS | native PASS, cleanup PASS; queue runner, retry and dead letter, scheduled execution, credential rotation, concurrent claims, empty queue, SMTP connect failure, restore, paired restore decrypt and wrong-key fail-closed PASS; exactly-once NOT_CLAIMED and response loss after acceptance NOT_RUN by design | required | n8n 2.49.7 native rehearsal |
| P03 runner boundary on 2.49.7 | 104 | W109 | `P03_RUNNER_NATIVE_REHEARSAL=1 … tests.validation.test_p03_runner_isolation.P03RunnerNativeRehearsal` | Same candidate and runner | PASS | Test OK, cleanup PASS; receipt `native: PARTIAL` (fixture declared NON_EQUIVALENT to HOME, as in TSK-0118 E28); categories builtin_denied 5, module_access_denied 3, environment_access_denied, code_generation_blocked, controlled_workflow_timeout. The first run failed on the same stale broker selection and is resolved by this one | required | - |
| HOME apply of n8n 2.49.7 | 104 | W109 | `pg_dump -Fc` of `n8n` checked with `pg_restore --list`; `up -d --no-deps --no-build --pull never` of n8n, n8n-worker, n8n-task-runner-worker after dry runs naming only the target | Owner request 2026-11-27; no running execution (2 in `error`) | PASS | `n8n-2.46.6-db.dump` (173 table-data entries) in `/home/hyunyoun/storage/volumes/backups/upgrade-20261127/`; each healthy before the next; `n8n --version` 2.49.7; 39 migrations finished without error; workflows 13, credentials 14, executions 2 as before; the worker registered the JavaScript and Python launchers; route 200. Rollback: restore the dump and recreate on `hyhome/n8n:2.46.6-local`, kept locally | required | - |
| D09 v9 remaining census | 104 | W109 | `latest_version_gate` and `security_update_gate --input update-ledger.json`; `check-all-hardening.sh`; `validate-docker-compose.sh`; `check-supply-chain-policy.py --check`; effective Compose against container HostConfig and cgroup memory; `npm audit --package-lock-only` on a Storybook lock copy | `main` `a8576cc8a`, HOME 2026-11-28 | FAIL | Both gates exit 2 (83 without fresh lookup, 86 without fresh review); hardening, Compose and policy checks pass; 57 containers match their limits; no OOM or restart; Storybook audit 7 moderate build-only findings with fixes available; details in the census table | required | - |

### Resolution Links

Nothing was linked here before this Task moved to the common form. "Renovate PR hosted
CI" resolves its first PR1141 run through the same hosted check after the
restore pin fix. "PostgreSQL 18.6 exposure" is closed by the 18.7 jobs pin;
mng-pg and dev-pg run 18.7 since the HOME apply. The second Storybook
ingress rehearsal resolves the first, which failed in the test harness. The
second pgBackRest 2.60.1 apply resolves the first, whose config directory
permission broke archiving. The OpenBao r4 window stays open for the owner. The n8n 2.49.7 native rehearsal rerun resolves the two failed runs whose stale broker environment the fixture fix removed.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 104 | pending | Ledger fresh review, D09 v9 gate state, Fresh upstream release lookup | On 2026-11-27 both gates fail on stale facts (2026-11-10); a fresh lookup of the 54 GitHub-sourced entries finds 28 at upstream latest and 21 behind, recorded per entry as residuals; the behind entries need an update round and the 32 non-GitHub entries their own lookup. | SPEC-0212 TSK-0052 |
| 105 | pending | Artifact verification | Three public final candidates scanned. Qdrant index signature verified; other publisher proofs, final custom artifacts and residual decisions remain pending. | SPEC-0212 TSK-0052 |

### Remaining Conditions

Current source research and isolated artifact checks have run as recorded
above. Both ledger gates still fail. Criteria 104 and 105 remain pending.
Compatibility, recovery and operational execution remain separate and are
recorded as NOT_RUN.

Completion needs a passing latest-version gate or each remaining entry recorded
as a residual, independently verified security dispositions for affected or
blocked components, and a verification row for each selected artifact. A
receipt for one component or artifact never proves another.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

None: nothing was recorded here before this Task moved to the common form.
