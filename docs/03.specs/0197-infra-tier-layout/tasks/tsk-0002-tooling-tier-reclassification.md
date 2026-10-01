---
title: "Tooling Communication and Laboratory Tier Reclassification"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
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

### Authorized delivery and runtime reconciliation

Delivery exception: the user explicitly approved `ECC_SKIP_PRECOMMIT=1` for the single implementation commit after the global ECC hook misclassified four renamed-file public variable references. Independent security review proved unchanged psql/shell/environment references and no credential values; staged Gitleaks passed after rendering eight public secret IDs as individual backticked references. No scanner configuration or subsequent hook is bypassed. The ordinary first commit attempt remains a recorded hook-blocked attempt.

Operational preflight: six of seven old-source Compose hashes exactly match the running containers. Dozzle differs only by an already-existing image version gap (declared v11.1.1, running v11.1.0): overriding that image reference alone restores the live config hash. Preserve the current v11.1.0 image for this label-only reconciliation; its local tag resolves to the captured live image ID. All seven existing image references resolve to their captured live IDs. This task does not authorize an unrelated Dozzle upgrade.


On2026-10-01 the user explicitly approved operational application, commit/push/PR merge to `buenhyden/hy-home.docker` main, main/origin alignment, removal of the delivered development branch/worktree, and terminal completion of SPEC0197/0198 followed by verification of SPEC0194 completion. This supersedes the earlier source-only delivery boundary for this follow-on action. The remote required check is `validation-changed` (strict); zero approving reviews and no enforced CODEOWNER review were read back. No protection bypass or direct main push is authorized by the delivery procedure.

Runtime scope is the existing Compose deployment affected by the approved35 package relocations and tier labels, plus the installed Restic unit's exact source-path token. Preflight uses value-free container identity/status/tier labels, source mount paths, deployed image IDs, and installed unit paths only. Do not print environment values, secrets, raw logs or full inspect/config. Before any recreation, identify the exact running affected services, validate the merged configuration, preserve image IDs and persistent mounts, and record a concrete rollback. Unchanged/offline optional jobs must not be activated. A failure stops that target; it does not justify credential rotation, image upgrades, data movement or unrelated service changes.

Value-free runtime preflight found99 service identities in moved Compose files,12 currently running in project `hy-home-infra`. Independent operational review limits recreation to seven: `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, then `registry`, `dozzle`, `redisinsight`. The other five (management PostgreSQL/Valkey, their exporters and Qdrant) have no relocated source mounts or changed tier labels and retain their containers. Existing image IDs and mount identities were captured without environment/command/secret output. SeaweedFS S3 has an anonymous `/data` volume; its exact identity must survive. Old bind sources are tracked, unchanged public files. Before execution compare old production service config hashes with live labels, confirm local image resolution equals recorded image IDs, and validate the new source. Use explicit targets with `--no-deps --no-build --pull never --force-recreate --wait`, one at a time, with existing healthchecks. No down/renew-anon-volumes or broad profile startup. Restore only a failed target using preserved pre-merge source and image; do not restore data or credentials.

Installed `hyhome-backup.service` still names the old source token and the timer is enabled/active waiting. Its root-owned0644 file is not writable; noninteractive sudo currently requires authentication. Prepare the exact token-only unit change, preserve timer state, validate and daemon-reload without starting a backup. This host permission constraint is not permission to bypass host authorization.




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

| Acceptance criterion | Plan work unit | Task result | Durable owner |
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

No commit for this extension. Preserve reviewed and in-progress work in the
shared worktree; no reset, branch cleanup or publishing is part of this action.

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

The user approved C and requested the additional implementation Plan. Concrete
steps are now approved in Plan W5.1–W5.4; the previously selected
native same-session method with independent review is preserved. Existing SPEC-0198 W5 body work may continue;
W6 path and tier reconciliation must use the agreed final map. No new runtime
operation or implementation remediation is authorized by the classification.
