---
title: "System Operations Documentation"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0198-TSK-0002"
parent_ids:
- "SPEC-0198"
- "SPEC-0198-PLAN-0001"
created: "2026-10-01"
---

# System Operations Documentation

## Objective

Implement W2 of the [approved Plan](../plan.md): shared-topic ownership,
system explanation, bounded cross-service triage and existing navigation.
This Task records W2 evidence; it does not complete the service-topic audit.

## Inputs

The user approved SPEC-0198 and its Plan, with tier-scoped implementation and
independent review, on 2026-10-01. The assigned worktree is
`/home/hyunyoun/.codex/worktrees/infra-tier-layout/hy-home.docker`, branch
`codex/infra-tier-layout`, based on c26bc8026254dffd7d51fc45b4081a1f80f855f2.
Reviewed, uncommitted SPEC-0197 layout is an input. W1's
[225-leaf/153-service manifest](tsk-0001-baseline-and-integration.md) was
independently CLEAR before W2. That inventory is not a completed body audit.

W2 owns only the new system-operations leaves, Operations README, three role
READMEs, operations-subject registry allocation and this Task. Existing leaves,
runtime source, frozen history, Git index and commits are excluded. No runtime
command, secret file, local `.env`, image build or recovery rehearsal is part
of this authorization. Repository bootstrap/provider, doc-writer role,
ops-runbook-agent skill and registered Guide/Runbook/Task templates were read.
Other writers' changes are preserved. The user also required inspection of the
actual Dockerfiles behind Compose build services; the source boundary below
records that inspection without asserting a successful build.

## Work Log

### Shared ownership and demonstrated gaps

| Topic | Existing owner inspected | W2 disposition and reason |
| --- | --- | --- |
| System structure | AD-0031 and root Compose | Link architecture; add GDE-0099 explanation of operating paths, tier responsibilities and common failure impact. No duplicate implementation_services binding. |
| Startup/reboot | RUN-0098, POL-0078, common optimization templates | Link existing procedure; distinguish selection, successful jobs, health, authentication and application acceptance. Historical reboot receipt is not a new result. |
| Authentication/secrets | 0013/0014/0015/0079/0085, gateway labels/middleware, OpenBao Compose/agent.hcl | Explain native versus proxy authentication and management state dependencies. Healthy sealed OpenBao and a nonempty Agent token file do not prove readiness or secret delivery. |
| Backup/recovery | 0021 Guide/Policy/Runbook, RUN-0035, Restic orchestration source | Link existing state ownership; snapshot/copy existence is insufficient proof of complete exports, application restore or whole-host recovery. No new stateful recovery sequence. |
| Version/configuration changes | 0086 Guide/Policy/Runbook; POL-0006 Source and lifecycle boundary | Reuse source/version ownership and post-apply control; no duplicated pins or upgrade procedure in the system Guide. |
| Networks | 0077 Guide/Runbook, root networks and actual peer declarations | Link common owner; explain profile selection is not isolation and actual peers differ from Compose startup edges. |
| Capacity | POL-0006, RUN-0035, AI resource declarations | Link host storage/GPU procedures; concurrent workload fit and automatic global capacity adjustment remain unverified, owned by @buenhyden for separately approved measurement/remediation. |
| Cross-service diagnosis | RUN-0098 is reboot-specific; RUN-0077 is network configuration; RUN-0035 is storage capacity; RUN-0086 is version management | Missing symptom-to-shared-dependency-to-service decision flow warrants RUN-0099. It adds bounded status observation and routing only, without service recovery commands or an invented isolation environment. |
| System Policy | POL-0006/POL-0078/0021/0077/0079/0085/0086 already own applicable controls | Omit POL-0099: no uncovered cross-service obligation was demonstrated. GDE-0099 explicitly routes to existing controls. |

### Navigation and identifier receipt

Current and frozen operations artifact IDs were reconciled before allocation.
The registry's high_water=87/next_number=88 cursor was stale: issued active IDs
0088 through 0098 already existed. No current or preserved operations artifact
used 0099. Allocate subject 0099 once for GDE-0099 and RUN-0099; update only the
operations-subject high_water to 99 and next_number to 100. No identifiers,
slugs, existing leaf paths or bodies were changed.

All three role indexes retain identical 01–12 tier categories and use unnumbered
cross-cutting categories for system/lifecycle, workspace and connectivity.
Backup 0021 is cross-cutting despite its service binding: the Guide still owns
its Restic jobs and retains both siblings. The index is not a service registry.
The existing Operations README remains a folder router and links direct-child
role indexes, including anchors, rather than deep leaf links.

| Original index location | Final location | Preservation |
| --- | --- | --- |
| 00 Workspace: 0086; RUN-0098 | Cross-cutting system and lifecycle | Same row target, ID, status and sibling links |
| 00 Workspace: POL-0001/POL-0006/POL-0078 | Cross-cutting system and lifecycle | Same row target, ID, status and sibling links |
| 04 Data: 0021 siblings; RUN-0035 | Cross-cutting system and lifecycle | Same rows; no body move or deletion |
| Remaining 00 Workspace rows | Cross-cutting workspace | Same rows, no misleading tier number |
| Infra Net rows | Cross-cutting connectivity | Same rows and ownership |
| Generic optional-role authoring sentence | Service-bound triplets required; other subjects need applicable roles only | Corrects the ambiguity without weakening the validator |

### Source and version boundary

Read root include/networks/secret path declarations, common-optimizations,
Traefik static/dynamic configuration, Keycloak and OAuth2 Proxy Compose,
OpenBao Compose and agent.hcl, management DB Compose, SeaweedFS Compose,
observability Compose, Airflow/n8n, Ollama/Open WebUI/ComfyUI, Kafka,
Terrakube/Restic, Stalwart/Mailpit, Open Notebook/MLflow and
Trino/Superset/dbt Compose sources. Source inspection includes effective YAML
merge values, profiles, build fields, environment references, mounts, resource
and health declarations, depends_on conditions and network membership.
No referenced secret's contents or private environment override was read.

Dockerfile inspection covered FROM stages, package installation, COPY/ADD,
ENTRYPOINT/CMD and Compose overrides for the linked build subjects below.
No Compose build target is declared for these services. Public variable
fallbacks were inspected; operator-selected private Dockerfile overrides remain
unknown rather than being inferred from defaults.

| Subject/build input | Effective source inspected | Relevant boundary |
| --- | --- | --- |
| OAuth2 Proxy | context `.`, `${OAUTH2_PROXY_DOCKERFILE:-dev.Dockerfile}`, copied docker-entrypoint.dev.sh | Binary copied from upstream into Alpine; entrypoint reads management Valkey credential and starts config path. Private alternate Dockerfile not inspected. |
| Management PostgreSQL | context `pg/backup`, Dockerfile, entrypoint.sh and pgbackrest.conf | PostgreSQL base plus pinned pgBackRest; wrapper starts official entrypoint and supplies protected config. Source archive queue limit can create a PITR gap; no successful restore claim. |
| Airflow services | root context, airflow/Dockerfile, Compose build args | Compose AIRFLOW_VERSION=3.3.1 overrides pre-FROM default 3.3.2; Python constraint arg 3.13 and Keycloak provider arg 0.9.0. No added COPY/entrypoint. W1 remains dated exact-version ledger. |
| n8n and worker | context `.`, `${N8N_DOCKERFILE:-dev.Dockerfile}`, copied docker-entrypoint.dev.sh | Compose N8N_VERSION=2.29.5 overrides Dockerfile default 2.41.3; custom/font copies and secret-presence wrapper inspected. No claim that custom extensions were functionally audited. |
| Loki and Tempo | respective build contexts/Dockerfiles and copied docker-entrypoint.sh | Upstream binaries copied to Alpine; wrapper reads S3 secret file, then starts binary with config expansion. |
| Gatus | gatus/Dockerfile | Checksummed upstream source, local patch, build/test instructions and wrapper COPY are source declarations, not observed build success; system Guide makes no patch-behavior claim. |
| SurrealDB and MLflow | SurrealDB Dockerfile/entrypoint; MLflow Dockerfile/requirements | Source-owned storage entrypoint and PostgreSQL/S3 dependencies; no installed-version claim. |
| Kafka Connect and Stalwart configuration job | Dockerfile.connect; config/Dockerfile | Copied connector and CLI stages; service/job behavior still governed by Compose. |
| Superset and dbt | Dockerfiles/requirements; dbt entrypoint | Metadata DB/auth/Trino packages and dbt adapter inputs inspected; Compose owns initialization/job commands. |
| Spark, Flink, Great Expectations | Dockerfiles | Source image, checksummed engine jars or copied requirements/command; no runtime engine compatibility or data validation claim in W2. |
| ComfyUI and Open WebUI | ComfyUI Dockerfile; Open WebUI mounted docker-entrypoint.sh | ComfyUI Compose uses an image, not an active build stanza: repository Dockerfile is not evidence of the installed image. WebUI wrapper loads OIDC secret and CA. GPU and auth explanations remain source-limited. |

Official documentation read on 2026-10-01:

| Claim | Official evidence | Applicability/uncertainty |
| --- | --- | --- |
| Profile selection and explicit-service targeting | [Docker profiles](https://docs.docker.com/compose/how-tos/profiles/), Auto-starting profiles and dependency resolution | Current Compose documentation; installed Compose version not observed. No executable deployment is authorized by this description. |
| healthy versus completed-successfully dependency conditions | [Docker startup order](https://docs.docker.com/compose/how-tos/startup-order/), Control startup | Explains conditions already present in current source; does not prove application readiness. |
| OpenBao sealed exit code | [OpenBao status](https://openbao.org/docs/2.6.x/commands/status/), exit codes | Version-matched official 2.6.x command reference plus repository declared image 2.6.2 and explicit source predicate. Mutable tag/installed binary unverified; no broader version behavior inferred. |
| Bounded container status output | [Docker inspect](https://docs.docker.com/reference/cli/docker/container/inspect/), [Docker ls](https://docs.docker.com/reference/cli/docker/container/ls/) | Existing Docker CLI formatting/filter surface; no Docker call executed for this task. |

Build/source literals here are dated audit evidence, not a second runtime-version
registry. Detailed release compatibility audits remain assigned to W3–W6.
W2 does not promote missing recovery, bootstrap or capacity implementation to
compliance; it routes limits to the existing subject and @buenhyden.

### Independent W2 review receipt

Reviewer `/root/ops_w2_review` on 2026-10-01: specification compliance PASS;
quality APPROVED/CLEAR; no findings. The scoped before/after diff, all eight
owned paths, source-backed system claims, index preservation, allocation and
153 unique service bindings were checked. W2 complete (uncommitted task-scoped
snapshot; review clean). At that checkpoint W3-W7 and W8 remained open;
the final W8 receipt in Task0001 now records their acceptance;
no runtime/build/recovery evidence is claimed.

## Verification Evidence

Focused checks use the worktree after the integrating parent staged the three
new paths for Git discovery; the implementing worker never staged. All runtime
commands in RUN-0099 remain NOT_RUN.

| Check | Result | Scope/limit |
| --- | --- | --- |
| `check-operations-catalog.py` | PASS, exit 0 | Current catalog, service-owner join and profile vocabulary; no runtime claim |
| W2 exact-path metadata check | Initial FAIL, exit 1: AD-0031 is not an allowed Guide parent | Corrected GDE-0099 parent to existing POL-0006; AD-0031 stays linked architecture authority. Recheck PASS, exit 0: selected=7, violations=0, legacy_exceptions=0, transition_overrides=0. |
| `check-document-links.py --mode all` | PASS, exit 0; 1018 documents, 10194 links, failures=0, warnings=1 | Initial missing numeric index anchor corrected to the index route. Existing 2870 legacy links without capture sources remain historically unverified; frozen files untouched. |
| Filesystem/index membership assertion | PASS, exit 0 | 78 Guides, 75 Policies, 74 Runbooks each linked exactly once; all three indexes have exactly tiers 01–12 |
| Allocation/binding assertion | PASS, exit 0 | operations-subject 99/100; no implementation_services in GDE-0099; registry diff limited to that cursor |
| Documented shell blocks through `bash -n` | PASS, exit 0 | Syntax only; no block executed and no Docker API call |
| Owned-path `git diff --check` | PASS, exit 0 | Whitespace only |
| Manual system-topic route review | PASS for W2 authoring | Startup/reboot, auth, backup/recovery, upgrades, capacity and cross-service diagnosis each have owner links and bounded unverified capabilities. Independent review subsequently passed; see its receipt above. |
| Full changed gate | NOT_RUN by W2 | Reserved to integrating owner on the final package state |

No new executable implementation was added, so unit/integration/E2E tests and
coverage are not applicable to this documentation-only work. The existing
validators and explicit source review supply the relevant static evidence.

| Source acceptance mapping | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 2 | W2 | Navigation, identifier and exactly-once catalog checks PASS | Existing Operations/role READMEs, registry |
| 3 | W2 | All six operating needs mapped; explicit capability limits and owner | GDE-0099, RUN-0099, existing common owners |
| 4 | W2 | No duplicate service binding; service triplet requirement clarified | GDE-0099 and role README authoring guidance |
| 5 | W2 | Shared explanation added; no existing leaf content removed or moved | GDE-0099/RUN-0099; service audit remains W3–W7 |
| 6 | W2 | Catalog/links/metadata PASS; independent review PASS (receipt above) | This Task; W8 owns final integration |
| 7 | W2 | Docs/source reads only; runtime, secrets, staging and commits NOT_RUN | This Task |

## Review Evidence

Pre-review author checkpoint (superseded by the independent receipt above):
W2 semantic review was PENDING. Implementation was prepared for
review and is not package completion. Source and official-document comparison
is static evidence only.

## Commit Ledger

Integrated source commit: `0d42c5edf584fcae7cd78a26fee263492e193885`.
The following worker receipt records the earlier authoring checkpoint.

No W2 commit or index mutation by this worker. Preserve all pre-existing staged
SPEC-0197 and other shared work. Integrating owner controls any authorized
staging, review checkpoint and delivery.

## Rulings

- New documents start draft/0.1.0; existing lifecycle statuses are preserved.
- Reuse controls instead of a symmetric empty system Policy.
- New triage adds no stateful recovery and therefore creates no replacement
  restore procedure or rehearsal environment.
- Existing leaf corrections belong to their waves. For example POL-0006's
  historical inventory wording and RUN-0098's broad restart wording remain W7
  review inputs, not authority for new claims.

## Deferred Items

Full package service audit and integrated W8 gates remain.
Actual startup/auth/resource/backup/recovery observations, builds, deployments,
secret delivery changes and data/credential mutations require their separately
approved execution tasks. The documentation task claims none of them.
