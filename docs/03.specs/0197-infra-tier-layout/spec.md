---
title: "Infrastructure Tier Layout and Documentation Consistency"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0197"
parent_ids:
- "REQ-0005"
- "REQ-0027"
- "AD-0004"
- "AD-0012"
created: "2026-10-01"
---

# Infrastructure Tier Layout and Documentation Consistency

## Overview

Flatten twelve storage and data-platform packages under `infra/04-data`,
create `infra/12-analytics` for five processing, query, quality and BI packages,
and move PostgreSQL-based dbt there from `infra/09-tooling`. Also investigate
every remaining Tooling, Communication and Laboratory package and relocate
packages to justified capability
tiers under an explicitly reviewed destination map. Correct the documented
inventory drift without changing runtime behavior.

The user approved the original Data/Analytics design and requested its written
specification on
2026-10-01. The user subsequently approved that original written specification and requested the
implementation plan on 2026-10-01. Frontmatter remains draft for initial
registration; the user also approved the original written Plan and selected native execution
with independent final review on 2026-10-01.

## Boundaries and Inputs

Reuse REQ-0027's discovery and consistency requirements, REQ-0005's optional
analytics boundary, and AD-0004, AD-0012 and AD-0031 as current architecture
inputs. The approved scope covers structure, classification, configuration
references and documentation, including dbt's change of tier ownership.

Preserve service behavior, activation, images, credentials, resource limits and
persistent data. Do not deploy, restart, consolidate or retire services, move
host data, or split the root Compose project. SPEC-0182 and other concurrent
packages retain their scope. Frozen archives and dated research snapshots
are not rewritten to make their historical paths look current.

On 2026-10-01, tracked source contained 49 included Compose fragments and 153
service declarations. Data owned 17 fragments/72 declarations; its five
Analytics candidates owned eight declarations. These are dated source counts,
not running-container counts or constants to add to operational READMEs.

### Tooling, Communication and Laboratory scope extension

On 2026-10-01 the user added a complete investigation of the subservices in
`infra/09-tooling`, then explicitly expanded the request to
`infra/{09-tooling,10-communication,11-laboratory}`. Assess appropriate tiers
and include structural relocation in this Spec. The current post-dbt layout
contains eighteen packages and twenty-seven Compose identities: Tooling11/17,
Communication2/3 and Laboratory5/7 (packages/identities). The review includes helpers and
provisioners, selected Dockerfiles (including inline builds), mounted scripts,
state ownership, dependencies, activation profiles and downstream path consumers.

Classify by primary operational capability, not by the word "tool", deployment
frequency, shared database dependency or profile name. Compare retaining a
precisely bounded current tiers, reusing other existing capability tiers, and
adding a tier only
where its distinct responsibility justifies it. Record a retain-or-move decision
and rationale for every package. Keep each package and its helpers together;
no service split, retirement or newly deployed service is implied.

Evaluate production mail versus mail testing, operational log viewing, database
administration, notebooks and ML lifecycle in addition to backup, IaC, artifact
registry, dependency maintenance and software testing/quality. Laboratory usage
is not by itself a capability: retain or replace that boundary explicitly.

The user approved the written alternative C amendment on 2026-10-01, using
`11-quality` instead of the usage-based Laboratory boundary, and requested the
additional implementation Plan. The user subsequently approved that amended
Plan and retained native execution plus independent review. The previously
approved eighteen-package Data/Analytics map remains valid. Further
relocation follows the approved concrete amended implementation Plan. Prior Data/Analytics results do not prove the additional migration.
SPEC-0198 must consume the final paths and tier navigation while retaining its
service/topic audit and original-content preservation evidence.

## Behavior Contract

### Package placement

All paths below are relative to `infra/`. Move each package as a unit with its
Compose file, README, build sources, scripts and configuration. Helper
containers and provisioning jobs stay with their package.

| Existing package | Destination |
| --- | --- |
| `04-data/operational/mng-db` | `04-data/mng-db` |
| `04-data/operational/supabase` | `04-data/supabase` |
| `04-data/relational/postgresql-cluster` | `04-data/postgresql-cluster` |
| `04-data/cache-and-kv/valkey-cluster` | `04-data/valkey-cluster` |
| `04-data/nosql/cassandra` | `04-data/cassandra` |
| `04-data/nosql/couchdb` | `04-data/couchdb` |
| `04-data/nosql/mongodb` | `04-data/mongodb` |
| `04-data/lake-and-object/seaweedfs` | `04-data/seaweedfs` |
| `04-data/analytics/influxdb` | `04-data/influxdb` |
| `04-data/analytics/opensearch` | `04-data/opensearch` |
| `04-data/specialized/neo4j` | `04-data/neo4j` |
| `04-data/specialized/qdrant` | `04-data/qdrant` |
| `04-data/lakehouse/flink` | `12-analytics/flink` |
| `04-data/lakehouse/spark` | `12-analytics/spark` |
| `04-data/lakehouse/trino` | `12-analytics/trino` |
| `04-data/lakehouse/great-expectations` | `12-analytics/great-expectations` |
| `04-data/analytics/superset` | `12-analytics/superset` |
| `09-tooling/dbt` | `12-analytics/dbt` |

### Approved additional placement: bounded Tooling and Quality

All paths below are relative to `infra/`. This table accounts for all eighteen
current packages in the three reviewed tiers, including six retain decisions.
It adds twelve moves to the original eighteen: thirty total mapped relocations
for the combined approved Spec. No ordinal renumbering,
new service or increase in the current twelve-tier count is proposed.

| Current package | Destination | Owning capability and rationale |
| --- | --- | --- |
| `09-tooling/k6` | `11-quality/k6` | Load/performance verification; telemetry export does not make it an observability backend. |
| `09-tooling/locust` | `11-quality/locust` | Distributed load generation; preserve master/worker and shared build together. |
| `09-tooling/wiremock` | `11-quality/wiremock` | Synthetic HTTP dependency stubbing. |
| `09-tooling/pact-broker` | `11-quality/pact-broker` | Contract/verification-result exchange; keep its database provisioner. |
| `09-tooling/sonarqube` | `11-quality/sonarqube` | Static code quality/security analysis, not runtime security infrastructure. |
| `09-tooling/conftest` | `11-quality/conftest` | Structured configuration/policy verification. |
| `09-tooling/opentofu` | retain | Infrastructure desired-state CLI; preserve inline Dockerfile and workspace contract. |
| `09-tooling/terrakube` | retain | Specialized IaC platform; keep API/UI/executor and state dependencies. |
| `09-tooling/registry` | retain | Software artifact distribution, distinct from general application data storage. |
| `09-tooling/renovate` | retain | Development dependency maintenance, not a general workflow scheduler. |
| `09-tooling/restic` | retain | Platform-wide backup orchestration across Data, AI, Observability and host configuration. |
| `10-communication/mailpit` | `11-quality/mailpit` | Test-email capture/API, distinct from operational mailbox service. |
| `10-communication/stalwart` | retain | Mail protocols/mailboxes; keep configuration helper and current internal-only operation. |
| `11-laboratory/dozzle` | `06-observability/dozzle` | Operational container-log visibility; retain independent leaf Compose. |
| `11-laboratory/redisinsight` | `04-data/redisinsight` | Optional data-store administration; target data remains owned by its database engines. |
| `11-laboratory/open-notebook` | `08-ai/open-notebook` | AI-assisted knowledge application; dedicated nested SurrealDB stays with it. |
| `11-laboratory/mlflow` | `08-ai/mlflow` | Model/experiment lifecycle metadata and artifacts; keep its database provisioner. |
| `11-laboratory/jupyterlab` | `12-analytics/jupyterlab` | Interactive data analysis/computation; MLflow is a dependency, not its tier owner. |

The reviewed subset then has Tooling5 packages/9 identities, Communication1/2,
Quality7/9, and seven former Laboratory identities distributed across their
capability owners. These are dated design counts, not runtime inventory constants.
Remove the obsolete `11-laboratory` directory index only after transferring its
useful content. Preserve all governed stage records and issued document IDs.
A current LAB operating classification or `admin`/`data-science` profile remains
valid outside a Laboratory directory; neither is silently renamed or expanded.

Exact additional `hy-home.tier` assignments are:

| Label | Exact service identities |
| --- | --- |
| `quality` | `k6`, `locust-master`, `locust-worker`, `wiremock`, `pact-broker-db-provision`, `pact-broker`, `sonarqube`, `conftest`, `mailpit` |
| `observability` | `dozzle` |
| `data` | `redisinsight` |
| `ai` | `open_notebook`, `surrealdb`, `mlflow-db-provision`, `mlflow` |
| `analytics` | `jupyterlab` |

Within the approved C checkpoint, all other labels remain unchanged except
the original approved Analytics map. The approved naming amendment below adds its own exact nine-label allowlist
for the subsequent implementation Plan.
All twenty-seven identities and eight built identities remain accounted for.
The seven selected build definitions, including inline OpenTofu and nested
SurrealDB/Stalwart sources, retain their context, arguments, stage selection,
package inputs and effective startup behavior after exact source-path mapping.

### Approved naming amendment: Platform Operations

The user subsequently requested investigation and application of a more precise
name for the retained `09-tooling` folder and tier. This written amendment
proposes `09-platform-ops`, display name **Platform Operations**, and
`hy-home.tier: platform-ops`. The user approved this written naming amendment on2026-10-01 and requested
the additional implementation Plan. Earlier C approvals cover the implemented
thirty-package relocation. The user subsequently approved naming Plan W6.1–W6.4
and retained native implementation plus independent final review.
The earlier tables are the approved C checkpoint; this amendment would supersede
only the five Tooling retain destinations and their nine tier labels.

| Existing package | Proposed destination | Exact service identities |
| --- | --- | --- |
| `09-tooling/opentofu` | `09-platform-ops/opentofu` | `opentofu` |
| `09-tooling/terrakube` | `09-platform-ops/terrakube` | `terrakube-api`, `terrakube-ui`, `terrakube-executor` |
| `09-tooling/registry` | `09-platform-ops/registry` | `registry` |
| `09-tooling/renovate` | `09-platform-ops/renovate` | `renovate` |
| `09-tooling/restic` | `09-platform-ops/restic` | `restic`, `restic-offsite`, `backup-sqlite-export` |

The capability provides shared infrastructure lifecycle operations: desired-state
planning/apply, artifact distribution, dependency maintenance and recoverable
cross-platform backup orchestration. It is not a catch-all for every utility.
Workflow remains application/job orchestration; Quality remains software and
configuration verification; Data owns storage engines; Security owns secret and
security services; Observability owns telemetry. Restic stays with its backup
helpers, and Terrakube API/UI/executor remain one package. No additional tier,
service split or reclassification of HOME/DEV/OPTIONAL/LAB is introduced.

Compared names:

- `09-platform-ops` is recommended: names the shared platform lifecycle and
  operational support responsibility, including recovery.
- `09-platform` is shorter but ambiguous because all infrastructure tiers form
  the platform; it obscures the ownership boundary.
- `09-delivery` captures IaC/artifact/dependency delivery but excludes Restic's
  platform-wide backup and recovery purpose.

If approved, migrate the five packages intact and their nine exact tier labels.
The combined Spec would then cover thirty-five package relocations. Preserve
existing root project/service/container/volume/network identities, image pins,
secret references, environment keys, persistent host paths and profiles.
In particular `tooling` remains the current cross-tier Compose selector for
Registry and SonarQube; it is not renamed to match a directory. Existing `iac`,
`registry`, `dependency-update` and `backup` selectors keep their membership.

Apply the name consistently to root includes, tier/package navigation, current
requirements and architecture terminology, Operations links/bindings/indexes,
Grafana's service-owner table, labeler glob/key, version projection, and the
marked current-service inventory. Hardening owns `09-platform-ops|platform-ops`
and `check_09_platform_ops`; retire its old `09-tooling|tooling` CLI names while
preserving Compose's unrelated `tooling` selector. Change no assertion merely to
make naming validation pass. The existing model comparator adds only the five
path-prefix mappings and exact nine-label allowlist; negative regressions must
still reject unrelated profile, image, host-path, identity and command drift.

Preserve issued document IDs and filenames such as REQ0010, AD0009/0024 and
Operations0063. Update their current role descriptions without renumbering the
requirements or erasing software-verification obligations now implemented in
Quality. Generic references to tooling, secret paths under `secrets/tools`,
retired-route records, archive fixtures, accepted historical ADR decisions and
dated observations are not global-replacement targets. Preserve historical
links through their actual source revisions where paths cease to resolve.
Record the additional rationale in the existing uncommitted ADR0046 proposal
when approved rather than allocating an unrelated decision record.

The tracked Restic systemd unit is an executable consumer outside Compose:
`hyhome-backup.service` has an absolute `ExecStart` script under `09-tooling`.
Change only that repository source prefix to `09-platform-ops`; preserve unit
names, timer schedules, user/group, working directory and command arguments.
Statically verify the mapped target exists and all other unit bytes remain equal.
Installed host units may retain the old path: later delivery requires an explicit
owner-controlled unit refresh and daemon-reload handoff before relying on the
next scheduled backup. This source task does not inspect/modify installed units,
enable a timer, trigger a backup, recreate a container or claim deployment safety.
The same boundary applies to future source-mount reconciliation.

SPEC0198 W6/W7 authoring waits for the final stable naming handoff. Preserve their
completed read-only source audits; compare only the actual relocation delta.
Spec/Plan/Task prose remains English; Operations and README explanations remain
Korean under the existing language contract.

### Responsibilities

Data owns storage and data-platform packages. SeaweedFS remains shared storage
for observability, AI and analytics consumers; Supabase remains intact.
Analytics owns data processing, transformation, SQL queries, data quality, BI
and interactive data analysis. Quality owns software/configuration verification;
Great Expectations remains Analytics because its subject is data quality.
Flink checkpoints and Superset metadata remain persistent state even though
the packages move. dbt keeps its PostgreSQL adapter; no new pipeline or Trino
adapter is introduced.

Messaging transports events; Workflow schedules and coordinates jobs;
Observability handles operational telemetry. The approved Tooling boundary owns platform development/operations, including
IaC, artifact distribution, dependency maintenance and cross-platform backup.
Communication retains operational mail; AI includes the existing model/experiment
lifecycle and knowledge applications alongside inference/interfaces. This adds
no model training/serving feature, email delivery or new runtime isolation. Tier numbers do not define startup order, isolation or
independent deployment. Tier READMEs provide navigation and role/classification
summaries; package READMEs and existing operations owners retain exact selectors
and dependency details. Do not add a competing service registry.

## Technical Approach

### Alternatives and decision

The eight current Data categories mix operational role, database model and
workload. Flattening all seventeen packages removes nesting but still mixes
BI/processing with storage. The approved split adds one capability tier and
keeps both tiers flat. Further database-type, BI-only or single-platform tiers
have no demonstrated need in this change.

The extension compared three alternatives: A keeps all three tiers and clarifies
only their documentation; B moves Mailpit to Tooling and distributes the five
Laboratory packages to existing capability tiers (six moves/eight labels),
leaving slot11 unused; C additionally groups seven existing verification
packages under `11-quality` (twelve moves/sixteen labels). C is recommended
for clearer long-term ownership across all three requested tiers. B is a valid
lower-migration alternative. Neither creates services or operational guarantees.
A retains the main capability-versus-usage ambiguity. `11-quality` also includes
static code/config checks, so its name is more precise than `11-testing`.
Restic stays Tooling because it orchestrates cross-platform recovery; AD-0004
currently excludes backup orchestration, and a one-package backup tier adds
no demonstrated value.

Root `docker-compose.yml` remains the entry point and
`infra/common-optimizations.yml` remains the shared template. Update includes,
relative `extends.file`, build contexts, repository-owned bind sources and
cross-package provisioning references together. Preserve package contents
except for reviewed path and classification adjustments.

For the original Data/Analytics scope, set `hy-home.tier` to `analytics` for
the six Analytics packages and retain Data labels for the twelve retained
packages. The additional sixteen assignments in the approved placement table
apply to the extension. Trace all affected label consumers so
monitoring/discovery loses no services. All labels outside these explicit
allowlists and all profile memberships remain unchanged.

Update active consumers: hardening tier dispatch/checks, `.github/labeler.yml`,
existing image projection, operations Guide implementation bindings,
source-path tests, README links and architecture descriptions. In particular,
update the tier table and directory tree in `infra/README.md` and the Data
and Tooling entries. Use registered generators for derived files. Transfer
useful content from the seven existing Data category READMEs to the surviving
tier/package READMEs, then remove those obsolete directory indexes. They are
`infra/` navigation files, not active-stage records requiring Stage 98 bodies;
Git history retains their previous contents. Existing stage documents still
follow their own retention rules. Do not leave compatibility symlinks or
duplicate current package copies.

Align AD-0004 with HOME storage versus LAB clusters and remove unsupported
tier-wide HA/latency guarantees. AD-0012 describes the current Data analytics
sub-tier, not an existing physical tier 12. Record the new boundary in an
architecture decision and align descriptions and REQ-0005 path references
without changing requirement identifiers or engine responsibilities.
ADR-0039's separation of InfluxDB/OpenSearch from lakehouse processing remains.

Correct the existing cross-tier drift: replace the stale HOME count in
`infra/README.md` with a source query, reconcile Observability service/profile
summaries, include `restic-offsite` in Tooling's backup map, and describe flat
package layout plus Observability's tier-level Compose exception. The old
lakehouse category disappears, so no README is added at its old path.

For the approved extension, preserve every current hardening assertion while
transferring dispatch to its capability owner; add Quality routing and cover
Dozzle's separate leaf beside Observability's existing aggregate Compose.
Update actual path consumers, including Conftest's launcher/validator, source
path tests, labeler and registered projections. Do not rewrite retained
OpenTofu/Renovate paths gratuitously; their only proposed later relocation is
the explicitly scoped naming amendment above. Preserve profile vocabulary across tiers:
`tooling` still selects Registry and SonarQube, `admin` Dozzle and RedisInsight,
and `data-science` JupyterLab and MLflow with their current dependency closure.
Keep host environment keys, mounted data paths and volume identities unchanged.

Align current REQ-0010/0011/0012 obligations and AD-0009/0010/0011, AD-0024/0025,
destination AD-0004/0006/0008/0012 and host AD-0031 where applicable. Preserve
requirement identifiers and accepted historical ADR bodies; record the new
allocation through the applicable architecture-decision lifecycle. Correct
current contradictory mail exposure, Open Notebook/SurrealDB placement and
HOME Registry statements from source, without rewriting dated evidence.
SPEC-0198 owns semantic body improvements; coordinate path/navigation changes
with its author so neither branch of work discards the other's corrections.

### Research basis

Official sources were consulted on 2026-10-01. They establish tool semantics;
the placement recommendation is a repository-specific inference.

- [Docker include](https://docs.docker.com/reference/compose-file/include/):
  included models resolve paths from their own project directories.
- [Docker extends](https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/):
  shared configuration and relative paths require explicit checking.
- [Docker config](https://docs.docker.com/reference/cli/docker/compose/config/):
  resolved-model comparison.
- [Flink](https://flink.apache.org/what-is-flink/flink-architecture/) and
  [Trino](https://trino.io/docs/current/overview.html): processing and query
  engines have roles distinct from their external storage.
- [GX](https://docs.greatexpectations.io/docs/core/introduction/),
  [Superset](https://superset.apache.org/) and
  [dbt](https://docs.getdbt.com/docs/introduction): quality, BI and transformation.

The expanded classification uses official role descriptions for
[Mailpit](https://mailpit.axllent.org/), [Conftest](https://www.conftest.dev/),
[k6](https://grafana.com/docs/k6/latest/),
[Locust](https://docs.locust.io/en/stable/what-is-locust.html),
[WireMock](https://wiremock.org/docs/), [Pact Broker](https://docs.pact.io/pact_broker),
[SonarQube Community Build](https://docs.sonarsource.com/sonarqube-community-build),
[Dozzle](https://dozzle.dev/guide/what-is-dozzle),
[Redis Insight](https://redis.io/docs/latest/develop/tools/insight/),
[Open Notebook](https://www.open-notebook.ai/),
[MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/) and
[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html).
Official capabilities support the comparison; exact tier destinations are a
repository-specific inference, not vendor instructions. Retained-role evidence
and all source-specific limits are recorded in Task0002.

For the naming amendment, official product roles were checked on
2026-10-01: [OpenTofu](https://opentofu.org/docs/intro/),
[Terrakube](https://docs.terrakube.io/),
[Distribution Registry](https://distribution.github.io/distribution/about/),
[Renovate](https://docs.renovatebot.com/) and
[Restic](https://restic.readthedocs.io/en/stable/010_introduction.html).
The [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
describes a broader cross-cutting platform concept; qualifying the local tier
as Platform Operations avoids claiming ownership of that entire concept.
The recommended name is a repository-specific inference, not a vendor mandate.

## Interfaces and Data

For the reviewed Data/Analytics portion, allowed resolved-model differences
are the eighteen mapped source relocations and Analytics tier labels. Any
additional three-tier relocation requires its exact source/destination map and
affected service-label allowlist; do not normalize arbitrary tier changes. Compare corresponding repository bind/build/config
paths through that explicit map and verify destination contents. Do not
normalize arbitrary differences. Persistent host paths, named-volume names
and options, project/service/container names, ports, networks, dependencies,
commands, healthchecks, profiles, secret references and resource limits must
otherwise remain equal. The sole additional command-path exception is the exact
Conftest entrypoint token `/project/infra/09-tooling/conftest/run.sh` becoming
`/project/infra/11-quality/conftest/run.sh`, with its corresponding script policy path.
Do not ignore arbitrary entrypoint or command differences. This narrow exception belongs to the approved Quality map; it does not
authorize any other command change.

Render with `.env.example` for public reproducibility. Do not read or emit
private environment or secret values. Public-model equality does not prove
private overrides or running containers use the new paths.

## Failure Modes and Guardrails

- A moved mount can resolve to the wrong existing file. Check resolution and
  mapped source contents, not just syntax.
- Tier dispatch and label filters can omit Analytics. Retain all existing
  checks for moved services and verify both Data and Analytics selection.
- Broad replacements can corrupt history. Update active consumers selectively
  and preserve archived bytes and dated observations.
- Moving mounted source directories affects later container recreation.
  Inventory these mounts before implementation and report any need for a
  separately approved operational step; do not claim live acceptance.
- Stop on unapproved model differences and correct the migration. Do not
  weaken checks or expand into service redesign to obtain PASS.

## Acceptance Contract

1. The original eighteen packages have their exact mapped destinations: twelve Data and
   six Analytics. No service is added, removed or duplicated. Obsolete paths
   have no active executable/navigation consumers; historical provenance is
   distinguished from current references.
2. Root include and shared template resolution succeed. Public resolved-model
   comparisons preserve execution/storage identities and settings except
   the explicitly approved source-path and service-label allowlists, plus the
   sole exact Conftest entrypoint token exception in Interfaces and Data. All other command/entrypoint tokens stay equal.
   Compare the full declared model, HOME and affected profile selections.
3. Existing hardening, operations catalog, image projection, tier-label
   consumers and source-path tests recognize the layout without dropping
   previous checks. New nontrivial checker logic has failing-before and
   passing-after regression evidence and at least 80% changed-line coverage.
4. Tier/package READMEs, operations bindings, current requirement paths and
   architecture descriptions agree with the new boundary. HOME count,
   Observability selector and backup inventory defects are corrected;
   the seven obsolete category indexes are removed after content transfer,
   while governed stage records follow existing retention policy.
5. Scoped Compose/catalog checks, affected hardening/tests, document
   metadata/link/lifecycle checks and the registered changed CI profile pass.
   Author-independent read-only review finds no unresolved material omissions
   or unsupported completion claims.
6. The eventual Task records baseline, allowed comparison exceptions,
   commands/results and acceptance-to-durable-document mapping. It separates
   source verification from unperformed runtime reconciliation. No private
   values, host-data moves, restarts or unrelated SPEC-0182 changes occur.

7. All eighteen packages and twenty-seven identities from the three reviewed
   tiers have an
   evidence-backed placement decision, including retained packages and helpers.
   Every approved additional destination and label is explicit; references,
   build/mount resolution, hardening and service-owner navigation are reconciled.
   Public model and source-content comparisons demonstrate unchanged execution,
   profiles and persistence after the additional moves. No package disappears
   into a generic "other tools" exemption.

8. If the naming amendment is approved, all five retained Tooling packages
   exist only under `09-platform-ops`, all nine exact tier labels agree, and
   active rules, executable references, systemd source unit, tests, projections
   and current documentation use the final name. Existing Compose profiles and
   runtime/persistence contracts remain equal. Negative regression, source-file
   preservation and independent read-only review prove the bounded migration;
   installed-unit refresh and runtime reconciliation remain explicitly NOT_RUN.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md):
  FR-0001, FR-0003, FR-0004, FR-0005; NFR-0001, NFR-0003, NFR-0004.
- [REQ-0005](../../01.requirements/0005-data-analytics.md): preserve
  FR-0001, FR-0003, FR-0005, FR-0006 and opt-in activation.
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md),
  [AD-0012](../../02.architecture/descriptions/0012-data-analytics-architecture.md),
  [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md):
  current architecture inputs and boundary alignment targets.
- [ADR-0039](../../02.architecture/decisions/0039-analytics-engines-after-lakehouse-convergence.md):
  retained engine responsibilities.
- [POL-0078](../../05.operations/policies/0078-compose-profile-vocabulary.md):
  unchanged activation vocabulary.

## Open Questions

The original Data/Analytics design and Plan were approved on 2026-10-01.
The written Tooling/Communication/Laboratory C amendment was approved on
2026-10-01. Its exact destinations are settled; the additional implementation
Plan is approved with the existing execution method retained, tracked in
[Task0002](tasks/tsk-0002-tooling-tier-reclassification.md).
The user approved the written `09-platform-ops` naming amendment on2026-10-01
and subsequently approved Plan W6.1–W6.4. Naming implementation and scoped
independent review are complete. The final frozen combined `changed` gate passed
on2026-10-01 after SPEC0198 integration; both Tasks record source acceptance.
The previous implementation evidence remains valid for its original scope,
and the final integrated receipts complete the expanded source package. Runtime changes remain excluded.

## Operational Impact

On2026-10-01 the user separately authorized delivery and operational application
of the reviewed implementation. This follow-on authorization supersedes the
source-only exclusions above for the bounded operation in Plan W7 and Task0002.
Reconcile only seven running containers whose source mounts or tier labels
changed, preserve their exact existing images and persistent mounts, and refresh
the installed Restic unit's source-path token without starting a backup.
Publication uses a protected-main PR and required checks; cleanup covers only
the delivered branch and its clean worktree. Completion requires observed
postflight results, not source checks alone. SPEC0198 shares delivery evidence;
SPEC0194's already-completed record is verified afterwards without reopening it.

The following paragraph records the original source implementation boundary:


This is a repository migration, not deployment. The root Compose project,
opt-in selectors and persistent data remain intact. Running containers are not
recreated by the implementation task. Repository rollback restores moved
files and references together; it is not data restoration. Later runtime
reconciliation must account for moved source mounts and labels under its own
scoped authorization.
