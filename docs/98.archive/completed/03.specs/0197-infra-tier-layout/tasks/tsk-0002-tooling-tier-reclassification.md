---
title: "Tooling Communication and Laboratory Tier Reclassification"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0197-TSK-0002"
parent_ids:
- "SPEC-0197"
- "SPEC-0197-PLAN-0001"
created: "2026-10-01"
---

# Tooling Communication and Laboratory Tier Reclassification

## Objective

Investigate every package under `infra/{09-tooling,10-communication,11-laboratory}`,
assess suitable capability
tiers and include the resulting relocation in [SPEC-0197](../spec.md) and its
[Plan](../plan.md), as requested by the user on 2026-10-01. Preserve the already
reviewed Data/Analytics work and all execution/persistence invariants.

## Inputs

Current worktree: `/home/hyunyoun/.codex/worktrees/infra-tier-layout/hy-home.docker`,
branch `codex/infra-tier-layout`, original base
`c26bc8026254dffd7d51fc45b4081a1f80f855f2`. Read the Spec, Plan, Task0001,
infra tier indexes and all current Compose declarations in the three tiers. The user also
requires selected Dockerfile inspection for built services. Existing SPEC-0198
work continues on disjoint files; its final navigation must consume the decision.
No private configuration, runtime, build, data movement or remote action is
needed for this research. The user approved the written C destination design on 2026-10-01 and requested
the concrete additional Plan. The user subsequently approved Plan W5.1–W5.4
and retained native execution plus independent review.

## Work Log

### Observed operational application on2026-10-01

[PR326](https://github.com/buenhyden/hy-home.docker/pull/326) passed required
`validation-changed` run `36849676246` and was normally merged as
`ad6d1f7971ec707fa4113884e6ea7e4b7b448c59`. The agent verified the current head,
required check and authenticated protection before merging without bypass.
Local main was fast-forwarded to that exact commit. The four original planning
files matched their bytes in `fcf079c87451cad8d79f4fd7188d24a947764752` before
only their task-owned duplicate working copies were cleared.

At11:09:38UTC, all seven approved service recreations passed. Each invocation
used the existing `hy-home-infra` project and merged main root Compose file,
`up -d --no-deps --no-build --pull never --force-recreate --wait`, one named
service at a time in master/volume/filer/S3/registry/dozzle/redisinsight order.
Preflight checked the exact merged HEAD, unchanged tracked deployment source,
resolved image reference and its local image ID, existing healthy container and
mount identities. Postflight checked a new target ID, healthy state, exact
preserved image ID, intended tier and every mount's type/source/name/target/RW.
Only the approved public SeaweedFS source prefix changed. No rollback was needed.

| Service | Previous ID | New ID | Observed tier | Preserved image reference |
| --- | --- | --- | --- | --- |
| `seaweedfs-master` | `1edcc1763828` | `450210b769ff` | `data` | `chrislusf/seaweedfs:4.47` |
| `seaweedfs-volume` | `f06eacaa0389` | `d6280b49414a` | `data` | `chrislusf/seaweedfs:4.47` |
| `seaweedfs-filer` | `18a0e415af58` | `e21285617c81` | `data` | `chrislusf/seaweedfs:4.47` |
| `seaweedfs-s3` | `0c0ffd2a7ecc` | `539f5c33ea62` | `data` | `chrislusf/seaweedfs:4.47` |
| `registry` | `a82963c3709e` | `9e6629929747` | `platform-ops` | `registry:3` |
| `dozzle` | `0c563060c87a` | `f420f386e466` | `observability` | `amir20/dozzle:v11.1.0` |
| `redisinsight` | `2410d23def4f` | `52916a9f0ac1` | `data` | `redis/redisinsight:3.8.0` |

The existing S3 anonymous `/data` volume remains
`e07dd8673f077936038dc8dbc82640e86abc01022ef17db73bd753d6a9fe1b40`.
All other persistent volume names and bind source/target/RW pairs are preserved,
except the approved public SeaweedFS config path relocation. The other74
containers retain their IDs and running/exited states; no unrelated container
was created or removed. In particular, the five running management DB/cache,
exporter and Qdrant identities were not recreated. This proves observed health
and preservation boundaries, not an unperformed database restore or data audit.

Dozzle retains its captured running `v11.1.0` image through the reviewed
one-service temporary override. The pre-existing source declaration `v11.1.1`
was not deployed; resolving that version gap remains a separately scoped upgrade.
No pull, build, data movement, credential change, broad profile startup, volume
renewal or prune was performed.

The owner executed the reviewed root helper and reported PASS. Independent
read-back verified installed unit SHA256
`462c414628fa64ac423659f1ba4b4a5e255e4b0495f10518c3ba5d5fba4f38a5`, root:root0644,
and loaded ExecStart resolving to
`infra/09-platform-ops/restic/bin/hyhome-backup.sh`. The timer remains enabled,
active and waiting; the backup service is inactive. The helper did not start a
backup. The byte-identical old-path public script bridge and its empty parents
were removed after that read-back; local main is clean. Required root
authentication was supplied in the owner's host terminal, never in the chat.

Independent read-only runtime review ACCEPTED these live observations on
2026-10-01: all seven healthy targets, exact images and mounts, unchanged other
container identities/states, installed unit hash/ownership/loaded path, preserved
timer, absent temporary bridge and clean main. The independent acceptance audit
also ACCEPTED the source and operational scope with no remaining implementation
finding. Neither verdict claims an unperformed restore, data audit or cleanup.

The first active-stage local changed profile failed one of628 regressions, log SHA256
`46394d4fbdc1b4ca68688cf395ec6b13c1430d2a25fa2d4c2932fabe9e6fb18d`. Both newly active Specs contained retired unqualified requirement child IDs.
Qualified them with their actual REQ parents; no requirement or validator was
changed. A fresh changed-profile run is required before merge and final completion.
The subsequent W7 checkbox/authentication wording repair records
already observed outcomes; scoped Markdown, diff and lifecycle checks cover
that documentary correction. Final protected completion publication and owned
branch/worktree cleanup remain mandatory follow-through, not observed PASS.

PR327 required run `36852983331` passed and the approval-stage PR merged normally
as `180f733dac14e3a21ec5b2cf9d7f3a7fae2764e4`. The corrected requirement
suite passed all21 tests; scoped Markdown reports zero errors. Independent
lifecycle/evidence review accepted the13-file activation packet. Draft publication
may overlap local and hosted validation, but merge requires both to pass.

### Completion receipt on2026-10-01

Final staged completion validation passed: explicit active-base metadata selected14, violations0; Markdown14, errors0; independent final acceptance CLEAR; public `full` exit0, log SHA256 `e6e9d02d9c22c3887133d66ca3bdecc942c5f729f34d3a3506eb054f5effa078`. This final factual receipt receives scoped Markdown/diff checks; required CI for its publication remains pending. The earlier clean-worktree `changed` exit0 did not select document tests and is not used as their acceptance evidence; the two recorded full runs cover them.

The corrected active-stage full profile passed, exit0, log SHA256
`fb567f968919446c4d7e063fa4efc97650a282e17dc8fb29259c1538a6de27db`. Required hosted run `36856261863` passed; PR328 merged normally as
`3f7139ea5c361a659de9f16d7e56627f47bee1f2`. The complete implementation and bounded operational acceptance are
recorded above and independently accepted. Both SPEC0197/0198 packages now
record completed Specs, Plans and all nine Tasks. This receipt publication still
requires its own passing protected PR, followed by main synchronization and
clean owned branch/worktree removal; those mandatory post-merge actions are not
claimed as already observed. No archive disposition or SPEC0182 change is made.

### Historical delivery checkpoints

### Authorized delivery and runtime reconciliation

Remote reconciliation on2026-10-01: authenticated read-back shows PR325 merged by `buenhyden` at10:18:15UTC as `3e2c026d7f25850e826be850fce7da6acb036a5b`, with head `b9eeceee9aa6c7f55a22831134d87638a157cb27` and required run `36844584749` still FAILURE. The agent did not execute that merge or claim passing CI. The corrected Ruff commit `f61e4b270d582375a92a7ae5929f2b56cf124f3a` and this review-stage promotion proceed through a new ordinary PR; origin/main was merged without rewriting recovery objects.

Review-stage local `changed` gate passed after an externally signalled attempt was retried: exit0, log SHA256 `e6406a1f127a060ec29d402f746e11e9c9ff180025672ed0b6c8667dc19b0646`. The earlier attempt received SIGTERM(-15) after passing tests and is incomplete, not a repository test failure or a pass. Subsequent test-only Ruff changes passed the focused tests and AST-preservation review above. Actual runtime and installed-unit application remain pending.

Hosted run `36844584749` passed Markdown validation but failed Ruff on two test files. Applied registered Ruff0.15.12 formatting, removed one unused import and made eight default `check=False` arguments and one default `strict=False` explicit. Normalized AST comparison proves no test behavior change; all135 tracked Python files pass Ruff check and format-check. No validator, failure assertion or production code is weakened. The next required hosted run must pass before merge. Independent code/security review ACCEPTED the three-file repair. Focused unittest result:104 discovered,83 passed and21 explicitly opt-in Docker PostgreSQL/backup/SeaweedFS/mail rehearsals skipped; no live recovery is inferred.

PR325 hosted run `36840244725` passed the preceding validation suites but failed the registered Markdown formatter because it changed document bytes. Applied the registered formatter to all326 changed Markdown files and escaped the literal shell OR operator in the Task1980004 evidence table. Two subsequent lint passes report zero errors; no operational instruction, lifecycle state, validator or protection is changed. The required hosted gate will be rerun on the repair commit.

Delivery preparation: normal-hook commit `49de994ac0e1e0bda16214c6e657ca8f32e1601f`
records the approved W7 plan. The frozen pre-push `full` gate passed (exit0),
log SHA256 `d2986a64d5f9297c3f8e92b628a02cd26e114f40892fae16db39d516566a097a`.
The branch was pushed and [PR325](https://github.com/buenhyden/hy-home.docker/pull/325)
created; hosted acceptance remained pending at that publication checkpoint.
Independent lifecycle review identifies30 task-owned living documents for
review/active transitions and two approved decisions for acceptance. This restores
26 previously active moved READMEs and promotes four new reviewed documents;
eleven originally draft READMEs remain draft. No unrelated document is promoted.

PR325 first hosted attempt (`36838896437`) failed metadata comparison against
`c26bc8026254dffd7d51fc45b4081a1f80f855f2`: nineteen W5 Runbooks introduced an
unregistered H2 `Execution Boundary`. Local full validation passed but did not
prove this PR-base delta. The boundary text is preserved verbatim under Procedure
as an H3, with all non-heading content unchanged. The original CI failure is
retained; explicit PR-base metadata and subsequent required CI must pass before
merge. No schema, validator, protection or runtime rule is weakened.
Independent integration review ACCEPTED the exact nineteen transformations.
Explicit `check-document-metadata.py --mode check-changed --base-ref origin/main`
then passed: selected332, violations0, no exceptions or transition overrides.

W7 follow-on independent review: `/root/runtime_relocation_review` ACCEPTED the
written Spec/Plan amendment and seven-target operation. Before mutation, two
byte-identical public source files were preserved under
`/tmp/hyhome-delivery-jytn6d37/rollback-public`; seven target-only temporary
Compose overrides retain captured image IDs and old tier labels. SeaweedFS
rollback binds use those preserved public bytes at unchanged container targets;
S3 rollback explicitly reuses its captured existing anonymous volume through
an external-volume name. Secret bindings and other configuration remain inherited.
These are prepared recovery inputs, not an executed rollback or deployment.

Delivery exception: the user explicitly approved `ECC_SKIP_PRECOMMIT=1` for the single implementation commit after the global ECC hook misclassified four renamed-file public variable references. Independent security review proved unchanged psql/shell/environment references and no credential values; staged Gitleaks passed after rendering eight public secret IDs as individual backticked references. No scanner configuration or subsequent hook is bypassed. The ordinary first commit attempt remains a recorded hook-blocked attempt.

Operational preflight: six of seven old-source Compose hashes exactly match the running containers. Dozzle differs only by an already-existing image version gap (declared v11.1.1, running v11.1.0): overriding that image reference alone restores the live config hash. Preserve the current v11.1.0 image for this label-only reconciliation; its local tag resolves to the captured live image ID. All seven existing image references resolve to their captured live IDs. This task does not authorize an unrelated Dozzle upgrade.

On2026-10-01 the user explicitly approved operational application, commit/push/PR merge to `buenhyden/hy-home.docker` main, main/origin alignment, removal of the delivered development branch/worktree, and terminal completion of SPEC0197/0198 followed by verification of SPEC0194 completion. This supersedes the earlier source-only delivery boundary for this follow-on action. The remote required check is `validation-changed` (strict); zero approving reviews and no enforced CODEOWNER review were read back. No protection bypass or direct main push is authorized by the delivery procedure.

Runtime scope is the existing Compose deployment affected by the approved35 package relocations and tier labels, plus the installed Restic unit's exact source-path token. Preflight uses value-free container identity/status/tier labels, source mount paths, deployed image IDs, and installed unit paths only. Do not print environment values, secrets, raw logs or full inspect/config. Before any recreation, identify the exact running affected services, validate the merged configuration, preserve image IDs and persistent mounts, and record a concrete rollback. Unchanged/offline optional jobs must not be activated. A failure stops that target; it does not justify credential rotation, image upgrades, data movement or unrelated service changes.

Value-free runtime preflight found99 service identities in moved Compose files,12 currently running in project `hy-home-infra`. Independent operational review limits recreation to seven: `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, then `registry`, `dozzle`, `redisinsight`. The other five (management PostgreSQL/Valkey, their exporters and Qdrant) have no relocated source mounts or changed tier labels and retain their containers. Existing image IDs and mount identities were captured without environment/command/secret output. SeaweedFS S3 has an anonymous `/data` volume; its exact identity must survive. Old bind sources are tracked, unchanged public files. Before execution compare old production service config hashes with live labels, confirm local image resolution equals recorded image IDs, and validate the new source. Use explicit targets with `--no-deps --no-build --pull never --force-recreate --wait`, one at a time, with existing healthchecks. No down/renew-anon-volumes or broad profile startup. Restore only a failed target using preserved pre-merge source and image; do not restore data or credentials.

Installed `hyhome-backup.service` still names the old source token and the timer is enabled/active waiting. Its root-owned0644 file is not writable; noninteractive sudo currently requires authentication. Prepare the exact token-only unit change, preserve timer state, validate and daemon-reload without starting a backup. This host permission constraint is not permission to bypass host authorization.

Main handoff preparation: while the root-owned unit awaits authenticated installation, retain only the byte-identical public backup script temporarily at its old source path. Its relative repository-root resolution is unchanged. Do not commit or ignore this bridge; remove the exact file and empty old directories only after the loaded unit points to the new executable. Independent runtime review accepted this bounded continuity measure. The prepared root helper verifies source/unit hashes, preserves timer state and runs daemon-reload without starting a backup; its error path restores the invocation-current unit. Runtime application and helper execution remain pending.

Expanded source inventory: eighteen packages/twenty-seven Compose identities
(Tooling11/17, Communication2/3, Laboratory5/7). Selected builds cover eight
identities through seven source definitions: k6, Locust master/worker,
OpenTofu inline, Stalwart configuration helper, JupyterLab, MLflow and SurrealDB.
dbt has already moved to
Analytics under Task0001 and is not counted again.

| Current tier / package | Exact current service identities |
| --- | --- |
| 09-tooling/conftest | conftest |
| 09-tooling/k6 | k6 |
| 09-tooling/locust | locust-master, locust-worker |
| 09-tooling/opentofu | opentofu |
| 09-tooling/pact-broker | pact-broker-db-provision, pact-broker |
| 09-tooling/registry | registry |
| 09-tooling/renovate | renovate |
| 09-tooling/restic | restic, restic-offsite, backup-sqlite-export |
| 09-tooling/sonarqube | sonarqube |
| 09-tooling/terrakube | terrakube-api, terrakube-ui, terrakube-executor |
| 09-tooling/wiremock | wiremock |
| 10-communication/mailpit | mailpit |
| 10-communication/stalwart | stalwart, stalwart-config |
| 11-laboratory/dozzle | dozzle |
| 11-laboratory/jupyterlab | jupyterlab |
| 11-laboratory/mlflow | mlflow-db-provision, mlflow |
| 11-laboratory/open-notebook | open_notebook, surrealdb |
| 11-laboratory/redisinsight | redisinsight |

Read-only architecture research is assigned to `/root/tooling_tier_design_research`.
The user expanded the initial Tooling-only request before a destination decision;
the research now compares all three tiers together, including retention,
existing-tier reuse and justified new capability tiers.
The integrating owner traces consumers and records the resulting design here.
The initial Tooling-only nonhidden path search found76 files; this is only discovery, not a
complete active-reference classification. Hidden workflow paths, generated
projections and dated historical mentions require separate disposition.

### Research outcome and proposed decision

Read-only research completed by `/root/tooling_tier_design_research` on
2026-10-01: all18 packages/27 identities, seven selected build definitions/eight
built identities and official product roles reviewed. The exact proposed map
is owned by the Spec, not duplicated here. Alternative A retains current paths;
B moves six packages/eight labels into existing capabilities; recommended C
reuses11 as Quality and moves twelve packages/sixteen labels. Destination approval was subsequently explicit in the user's written-spec
response on 2026-10-01. No relocation had been performed at that design checkpoint.

C groups k6/Locust/WireMock/Pact/SonarQube/Conftest/Mailpit as software and
configuration verification; distributes Dozzle, RedisInsight, Open Notebook,
MLflow and JupyterLab by capability; retains platform operations and Stalwart.
A moving experimental/optional usage label is not a primary capability.
Restic's cross-platform orchestration is explicitly outside AD-0004's storage
ownership, supporting retention. Great Expectations remains data-quality in
Analytics, distinct from software/configuration Quality.

Official retained-role references checked:
[OpenTofu](https://opentofu.org/docs/intro/),
[Terrakube](https://docs.terrakube.io/),
[Distribution](https://distribution.github.io/distribution/about/),
[Renovate](https://docs.renovatebot.com/), [Restic](https://restic.net/) and
[Stalwart](https://stalw.art/). Moving-role official references are in the Spec.
The parent directly rechecked Mailpit, Conftest, Dozzle and MLflow role pages.
These sources establish roles; local destinations are design judgments.

Concrete migration risks: exact Conftest entrypoint path is part of the command
model, not only bind/build paths; Dozzle adds a leaf to the aggregate-Compose
Observability tier; current hardening assertions must follow moved packages.
Keep source environment keys/host volumes, profile memberships, image/build
selection and helper cohesion. Later current AD/REQ navigation reconciliation
must preserve accepted historical ADRs and SPEC-0198's reviewed document bodies.

### Execution authorization and preflight

The user explicitly approved the additional Plan on 2026-10-01. W5.1 produces
the fixed comparator contract consumed by W5.2; W5.2 stable source paths are
consumed by W5.3 document reconciliation and SPEC-0198 W6/W7. No interface
conflict was found. W5.1 preserves current SPEC-0198 author corrections and
waits for its W5 review and Korean correction checkpoint before relocation.
Ruling: public-source capture and regression preparation can proceed during
SPEC-0198 documentation-only review because they neither move source paths nor
edit the active author's files. Source hashes are checked around capture; actual
relocation still awaits the approved documentation checkpoint. This reorders
preparation only, with no change in acceptance or runtime boundaries.
Canonical Task evidence remains the sole execution ledger; no parallel ledger
is introduced. Source/runtime and remote-action boundaries are unchanged.

### Naming research added after C migration

The user requested renaming the remaining09-tooling capability. Preliminary
consumer scan found71 non-archive/non-Spec paths,45 research/archive paths and
seven Spec paths; these are discovery buckets, not71 files all requiring edits.
Retired-route fixtures and accepted decisions require historical classification.
An extension-independent Git search also found the Restic `.service` ExecStart
path; suffix-filtered Markdown/code discovery alone was insufficient.

Proposal:09-platform-ops / platform-ops / Platform Operations, retaining five
packages and nine identities. Existing tooling Compose selector remains intact.
The Spec contains exact destinations, exceptions, rule/doc consumers and the
installed backup-unit handoff boundary. Official-role research and independent
naming review passed; the user approved the written Spec. Naming implementation was initially deferred pending Plan approval; the user
subsequently approved W6.1–W6.4 and implementation is now complete.
Independent naming review is APPROVED; SPEC0198 W6/W7 may consume final paths. Prior C source review is CLEAR after
OPTIONAL classification and historical-inventory suffix fixes. The restored
post-marker historical suffix matches all87,402 indexed bytes; the separate
three historical links are pinned to their actual original source commit.

The user approved Plan W6.1–W6.4 and retained native implementation plus independent review. Baseline:23 tracked files,153 services and six HOME/affected selections; no ignored/untracked source names or destination collisions. RED:12 tests with exactly three intended new failures; existing nine passed. Comparator GREEN:5/5, then full naming module GREEN:12/12. The mapped23 files survive; full public model has zero unexpected differences. Installed units and runtime remain untouched.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 6 | W7 | PASS: required CI and normal PR326 source delivery, seven healthy target recreations with preserved images/mounts,74 other container identities/states preserved, and installed backup unit/timer independently read back; final publication and cleanup remain finishing checks | [Platform Operations](../../../../infra/09-platform-ops/README.md) |

Initial design checkpoint: static inventory and role research only, before
migration. No runtime claim was made. Initial
metadata check selected4 files and found one forbidden extra Task0001 heading.
The receipt was moved into its registered Work Log; focused retry selected1,
violations0. The other three files passed the initial check. Final amended
text passed the focused metadata check (selected3, violations0). The amended
Plan was self-reviewed against all seven acceptance criteria, exact path/label
exceptions, authoring dependencies and rollback boundaries; original-only
approval wording and the expanded hardening verification row were corrected.
All11 local Markdown file targets resolved, and package `git diff --check`
passed. These are Plan-authoring checks, not migration acceptance. Public-model and source-content
validation was pending at that checkpoint; implementation receipts follow below.

| Source acceptance mapping | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 7 | W5 | C migration implemented and independently accepted;12 packages/16 labels preserved | Spec, tier/package READMEs and this Task |
| 2, 3, 4, 6 | W5, W6 | Scoped model/source, hardening, test and documentation checks PASS | Existing model comparison, hardening and document checks |
| 8 | W6 | Five packages/nine labels renamed; scoped independent review APPROVED | Platform Operations sources and this Task |
| 5 | W5, W6, SPEC0198 W8 | PASS: final frozen changed gate exit0; all scoped reviews accepted | This Task and SPEC0198 integration Task |

### W5.1 preparation evidence

Public `.env.example` capture with inherited configuration variables excluded:
153 services, 45 HOME services, 17 HOME/affected-profile selections and41 tracked
package files. Model SHA-256:
`c5a242c67a959f08f8d8ca0075dc62b2a61a11b6d4e861a278b105397629a187`.
No destination collisions or ignored/untracked names exist inside the twelve
moving packages. Tracked Compose input hashes stayed equal throughout capture.

The eight built identities use seven selected definitions. Every selection has
no Compose build-argument override and selects the final stage; declarations
are source evidence, not a successful build or installed runtime observation.

| Identities | Selected definition and preserved inputs |
| --- | --- |
| k6 | package context `.`, Dockerfile FROM `grafana/k6:2.2.0`; Compose command selects the existing scenario/output |
| locust-master, locust-worker | shared package context `.`, Dockerfile FROM `locustio/locust:2.46.6`; distinct existing master/worker commands |
| opentofu | retained inline build: OpenTofu1.12.6-minimal binary copied into Alpine3.24 with bash/CA/curl/git/SSH packages; Compose entrypoint preserved |
| stalwart-config | retained `./config/Dockerfile`: CLI1.0.12 binary copied into Stalwart0.16.22; existing reconciliation wrapper preserved |
| jupyterlab | package Dockerfile uses default JUPYTER_BASE_TAG2026-07-28, copies pinned requirements with NB_UID/NB_GID and installs them; Compose notebook command preserved |
| mlflow | package Dockerfile FROM MLflow3.16.1, COPY/installation of existing psycopg2-binary/boto3 pins; Compose secret-reading entrypoint/command preserved |
| surrealdb | nested `./surrealdb/Dockerfile`: mutable v2 binary copied into Debian bookworm-slim with CA/bash; copied secret-reading entrypoint preserved |

RED: nine regression tests ran; the six existing tests passed. New comparator,
layout and transferred-control tests reported15 expected assertions because
approved labels/entrypoint and destinations were not yet implemented. An initial
missing-directory iteration exception was corrected to an explicit assertion
before accepting the RED receipt. Comparator GREEN: all four model-comparison
tests pass, including input immutability and rejection of extra/wrong Conftest
arguments, other entrypoints, unknown-service labels, profiles, host volumes,
images and build-argument drift. Layout/control tests await the actual move.

### W5.2–W5.3 source implementation evidence

Twelve packages moved with all41 tracked files preserved. Relative build/COPY,
provisioning and source-mount paths resolve at their mapped destinations. Public
all-profile rendering retains153 services and reports zero unexpected model
differences; HOME45 and all17 affected selections match the baseline. The sixteen
tier labels and exact Conftest entrypoint/run.sh path are the only executable
changes within moved packages; other changed package files are READMEs.
Version projection retains92 repositories and unchanged image tags.

| Previous package prefix under infra | Final package prefix under infra |
| --- | --- |
| 09-tooling/k6 | 11-quality/k6 |
| 09-tooling/locust | 11-quality/locust |
| 09-tooling/wiremock | 11-quality/wiremock |
| 09-tooling/pact-broker | 11-quality/pact-broker |
| 09-tooling/sonarqube | 11-quality/sonarqube |
| 09-tooling/conftest | 11-quality/conftest |
| 10-communication/mailpit | 11-quality/mailpit |
| 11-laboratory/dozzle | 06-observability/dozzle |
| 11-laboratory/redisinsight | 04-data/redisinsight |
| 11-laboratory/open-notebook | 08-ai/open-notebook |
| 11-laboratory/mlflow | 08-ai/mlflow |
| 11-laboratory/jupyterlab | 12-analytics/jupyterlab |

Existing controls moved to their capability tiers; the five retained Tooling
packages receive explicit existence checks. Current requirements retain issued
IDs; optional administration obligations span their new owners. ADR0046 is
registered under AD0009 with initial proposed status; ADR0045 and accepted
historical decisions remain intact. The marked current-service inventory uses
the existing renderer. Three historical research links are pinned to their
original source commit without changing the recorded historical conclusions.

Focused regression:152 tests total,131 executed PASS and21 opt-in runtime checks
SKIPPED. All seven affected hardening tiers PASS. Operations catalog PASS.
Current requirement/architecture/ADR metadata:15 selected, zero violations.
ADR taxonomy:18 tests PASS. Comparator bytecode-line coverage30/35=85.71%;
new Tooling loop Bash command coverage5/5=100%. Relocated unchanged controls
are not counted as new logic. Full link check first found five stale targets
and one README descendant-navigation violation; all six were corrected and
fix1 recheck passed:1,023 documents/10,766 links, zero failures and one existing historical-source warning. Public Compose validation passed all72 selections, HOME45 and360 cumulative services.
No runtime/build/recreation, private-input read, commit or remote action occurred.

### W6 naming implementation and scoped validation

All five packages and23 tracked files are preserved at09-platform-ops; the nine
exact identities use platform-ops labels. HOME45 and five affected profile
selections are unchanged; all153 public service models have zero unexpected
differences. Restic unit bytes differ only at the approved ExecStart source token.
Current consumers include the exact Renovate OpenTofu regex, hardening dispatch,
labeler, includes, tests and documentation. Issued filenames remain stable.
The current inventory renderer preserves outside-marker bytes except two
separately verified historical links pinned to their source revision. Twenty-four
single-destination authored tier projection values were aligned; generator check
passes92 repositories with unchanged image versions.

Regression:223 total,202 executed PASS,21 opt-in runtime cases SKIPPED. All72
public Compose selections PASS (360 cumulative service selections); seven
affected hardening tiers and operations catalog PASS. Comparator coverage is
30/35 executable lines (85.71%); no new production checker was added. Link check:
1,023 documents/10,762 links, zero failures, one existing historical-source
warning. Metadata initially reported five violations; exact-path draft lifecycle
and existing Structure heading fixes pass all five affected files with zero
violations, no overrides or validator changes. Runtime, installed-unit refresh,
hosted CI and publication remain NOT_RUN. At that checkpoint the combined changed gate awaited final
SPEC0198 writers and a frozen index; final integrated acceptance is recorded below.

### Final integrated gate correction

The first frozen `changed` run failed in the quickwin136-test batch (2 failures,23 skips) after metadata, links,628 document regressions, catalog, supply-chain, Compose/security and Conftest had passed. Analytics hardening test subprocesses inherited a gate directory-FD variable without that descriptor; the Open WebUI hardening fixture omitted the Open Notebook Compose file after its approved AI-tier relocation. Both are test-fixture defects. The existing environment-filter pattern now applies to both analytics child calls; the existing AI fixture includes the moved public Compose source. The production root-identity guard and all negative security assertions remain unchanged; only the obsolete Tier09 comment also changed. Focused RED evidence is the actual gate failure; GREEN: both complete test modules passed19 tests with `HYHOME_CI_GATE_ROOT=/proc/self/fd/99999`, including positive and broken-SigV4/password-auth negative cases. Independent reviewer `/root/platform_ops_final_review` APPROVED the exact fixture and comment corrections after checking the19-test GREEN receipt; production guards and exact negative assertions remain intact. At that first failed-gate checkpoint a complete frozen `changed` rerun remained required.

The second frozen integrated gate passed the136-test quickwin batch (23 skips), including both corrected fixtures. A later SPEC0198 script consumer-map failure required four declaration updates; the independent integration reviewer accepted them, and manifest/workflow/Storybook focused checks passed. At that second-gate checkpoint the full rerun remained pending; no additional infrastructure source defect was found.

Final integrated acceptance, 2026-10-01: third frozen `changed` gate exit0, including all13 selected public entrypoints and both previously failing fixture cases. The script consumer-map correction also passed. Log SHA-256 `4a3071ff1b9502e877bd96a439fe1912f2cd7b073d8f8448f8d98c557f886669`. All eight source criteria are accepted; prior failed attempts remain historical evidence. Live runtime reconciliation, installed-unit refresh, recovery/build execution and hosted CI remain NOT_RUN.

## Review Evidence

Independent architecture research complete. `/root/spec0197_three_tier_review`
verified the full inventory, proposed map, selected builds and preservation
contract. Initial review found one material comparison-allowlist contradiction
and one approval-wording ambiguity. The author aligned Spec acceptance and Plan
constraints to the exact conditional allowlists/Conftest token exception, and
limited the old approval receipt to Data/Analytics. Scoped fix1 re-review on
2026-10-01: CLEAR, both findings addressed and no new defect. This accepts the
written proposal for user review, not destinations or implementation. Task0001's
approvals cover its original scope only.

Naming amendment independent review, 2026-10-01: CLEAR; the five packages,
nine identities, profile preservation and Restic installed-unit handoff boundary
are explicit. Focused Spec/Task metadata selected2, violations0; both English
prose checks and scoped diff check passed. The user subsequently approved the written naming Spec and requested its
implementation Plan. W6.1–W6.4 now records baseline/regressions, atomic rename,
document/host-unit handoff and final checks. The user subsequently approved the Plan and implementation is complete;
native execution plus independent final review is preserved. The full changed gate remains deferred until all0198 writers finish.

Platform Operations Plan authoring verification: W6.1–W6.4 covers acceptance8
and criteria2–6, exact file ownership, comparator/dispatch interfaces, witnessed
RED/GREEN sequence, backup-unit handoff, rollback and independent review.
Self-review found no unresolved scope/interface gap. Focused metadata selected3,
violations0; eleven local Markdown targets resolved; all three package documents
remain English; scoped diff check passed. These are Plan-authoring results, not
naming implementation acceptance. Written Plan approval was subsequently received.

Independent naming implementation review,2026-10-01: APPROVED. Four initial
findings (Renovate regex, stable document link targets, curated projection tiers,
and active scope references) were corrected and rechecked. The reviewer also
verified final lifecycle/heading fixes, exact mapped source/model preservation,
historical payloads and the sole unit-token exception. No material documentary
or source finding remains in the naming scope. This releases SPEC0198 W6/W7
final-path handoff; it does not claim the combined gate or runtime acceptance.

## Commit Ledger

`fcf079c87451cad8d79f4fd7188d24a947764752` preserves the four exact original
main planning files. `0d42c5edf584fcae7cd78a26fee263492e193885` records the
reviewed source implementation and delivery preflight. The user-approved
single-commit ECC false-positive exception was consumed by that implementation
commit; all subsequent hooks run normally. The observed operational application above supersedes that checkpoint's pending runtime state. `f61e4b270d582375a92a7ae5929f2b56cf124f3a` fixes the test lint findings; PR326 delivers the corrected tree and review-stage records. Final protected completion publication and branch/worktree cleanup are still finishing checks.

## Rulings

Ruling: the existing metadata lifecycle resolves previous state by exact path,
not Git rename detection. Register the new Platform Operations root/Registry/
Terrakube README paths and newly created Quality index as draft, as required by
their profile; preserve original active records in Git. The same exact-path rule was subsequently applied to all other moved README
paths after the W6 README check reproduced six further violations. Original
active records remain in Git; these new-path draft registrations do not claim
runtime acceptance. No lifecycle bypass or validator change. Move the tier table into the existing Structure section to
avoid introducing an unregistered top-level heading. Content remains intact.

Capability ownership determines placement; dependencies, activation profiles and
container counts alone do not establish a tier. Package and helper cohesion,
source-path correctness and persistence preservation remain mandatory.

## Deferred Items

Source implementation and the separately authorized runtime reconciliation are observed above. Final lifecycle publication, main/origin alignment and owned branch/worktree cleanup remain finishing checks; no future cleanup is recorded as PASS. The earlier classification approval alone did not authorize runtime changes. Existing implementation limitations documented by SPEC0198 do not authorize unrelated remediation, and SPEC0182 remains outside scope.
