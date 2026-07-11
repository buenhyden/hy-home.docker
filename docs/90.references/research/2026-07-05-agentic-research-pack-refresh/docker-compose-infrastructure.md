---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md -->

# Reference: Docker Compose and Infrastructure Harness

## Overview

This reference compares the tracked Docker Compose and infrastructure harness
with current official Docker guidance. It is a point-in-time evidence map, not
runtime configuration, deployment approval, or an operations procedure.

## Purpose

Give reviewers a reproducible infrastructure topology and an advisory control
matrix without copying Compose declarations into policy or treating upstream
examples as workspace mandates.

## Repository Role

This document supports Stage 00 governance, infrastructure reviews, Stage 04
evidence, and future approved Stage 03/05 work. Runtime truth remains in tracked
Compose and infrastructure files; procedures remain in Stage 05.

## Scope

### In Scope

- Tracked root and `infra/**/docker-compose*.yml` / `.yaml` topology
- Canonical generated service/profile coverage and validation surfaces
- Docker Compose overview, include, profiles, networking, secrets, dependency,
  production, and trust-model comparisons
- Advisory gaps with one canonical owner and an approval boundary

### Out of Scope

- Compose, infrastructure, workflow, script, policy, or runtime changes
- Starting, stopping, deploying, backing up, or restoring services
- Secret values, `.env` values, runtime logs, or live network inspection
- Formal adoption of a Docker example as workspace policy

## Definitions / Facts

- **Tracked Compose file**: the root `docker-compose.yml` or a Git-tracked
  `infra/**/docker-compose*.yml` / `.yaml` file.
- **Include entry**: one uncommented root `include` item. It is not a service,
  profile, or proof that the leaf's profile-gated services are running.
- **Variant**: one tracked infra Compose file. Canonical, dev, cluster, and v2
  filenames remain separate declarations even when they repeat service names.
- **Declared service entry**: one service mapping in one scanned Compose file;
  it is not a deduplicated runtime container count.
- **Ordinary network**: a declared network without `internal: true` or
  `external: true`. An ordinary bridge is not an internal network.
- **External network**: pre-existing lifecycle outside Compose; declaration does
  not prove that it exists on the current Docker host.

## Tracked Topology Census

The census was recomputed on `2026-07-11` from `git ls-files`, safe YAML parsing,
the root include block, and the canonical generated coverage. The generator
check passed; none of the prior 17/48/40 observations was copied without this
recount.

| Census item | Recomputed value | Derivation / boundary |
| --- | ---: | --- |
| Tracked Compose files | 49 | Root file plus 48 infra variants selected by the canonical generator. |
| Infra Compose variants | 48 | 40 canonical `docker-compose.yml`, 5 `.dev.yml`, 2 `.cluster.yml`/`.yaml`, and 1 `.v2.yml`. |
| Compose files with services | 48 | Every infra variant has services; the root file aggregates resources/includes and declares no services. |
| Compose service directories | 40 | Distinct parent directories of the 48 infra variants. |
| Active root include entries | 17 | Un-commented items parsed from root `include`. |
| Commented optional include entries | 20 | Commented `infra/**/docker-compose*.yml` items in the root include section; comments are not runtime configuration. |
| Service entries across all files | 169 | Canonical generated coverage; repeated names across variants count separately. |
| Service entries in active included leaves | 60 | Sum of declarations in the 17 included files before profile selection; not a simultaneous runtime count. |
| Profile labels | 25 | 24 named labels plus generated `default` for services with no `profiles` key. |
| Root project-name declarations | 1 | Root `name: hy-home-infra`; no infra leaf declares a top-level project name. |
| Root network declarations | 4 | 1 ordinary bridge (`infra_net`), 0 internal, and 3 external networks. |
| Top-level network entries across all files | 5 | Two ordinary `infra_net` entries across separate files, zero internal entries, and the same three root external keys. |
| Root secret declarations | 70 | Secret identifiers and file paths only; no value was read. |
| Service definitions with `healthcheck` | 145 / 169 | Static key presence across all tracked variants. |
| Service definitions with `depends_on` | 94 / 169 | Static key presence; condition semantics vary by service. |
| Service definitions with `restart` | 60 / 169 | Static key presence; active rendered profiles have separate validator coverage. |
| Service definitions with `ports` | 39 / 169 | 14 of the 60 entries in root-included leaves declare ports. |
| Service definitions with `volumes` | 130 / 169 | 46 of the 60 entries in root-included leaves declare volumes. |
| Service definitions with `secrets` | 112 / 169 | 42 of the 60 entries in root-included leaves declare secret access. |

`compose-profile-service-coverage.md` is fresh generated evidence for file,
service, and profile counts. It deliberately does not resolve includes, start
services, prove health, or inspect secret values. The 60 root-included service
entries are therefore a separate tracked-source derivation.

## External Guidance by Applicability

External sources were revalidated on `2026-07-11`. They support comparison
scope only.

| Guidance | Applicable scope | Supported comparison | Caveat |
| --- | --- | --- | --- |
| Compose overview and file model | Local development and shared application definition | Compose defines applications through services, networks, volumes, configs, and secrets. | The model does not prove this workspace's rendered or live state. |
| `include` | Modular tracked application model | Each include loads an application model with its own project directory and copies resources into the current model. | Included or remote content is trusted input and conflicts are not silently merged. |
| Profiles | Optional/local environment selection | Services without profiles are enabled by default; assigned services require an active profile. | A profile label is not a production-readiness or resource-isolation guarantee. |
| Networking | Development, custom isolation, and multi-project communication | Service-name DNS works on shared networks; internal networks remove a default external gateway; external networks support shared projects and must pre-exist. | Root external declarations do not prove existence; static IPs remain workspace choices. |
| Secrets | Secret delivery | A service receives only secrets explicitly granted to it as mounted files. | File-backed Compose secrets do not establish rotation, Vault use, or host-file protection by themselves. |
| Startup order | Dependency/readiness behavior | `depends_on` controls order; readiness requires health conditions rather than mere container start. | Static key presence cannot prove application-level readiness. |
| Production | Single-host production and environment overlays | Docker suggests production-specific changes and an additional override file where appropriate. | This is an example pattern, not a workspace mandate or multi-host production design. |
| Trust model | Untrusted Compose execution and CI | Compose applies trusted files as executable host-affecting input; review resolved configuration and transitive includes. | `docker compose config` aids review but does not make untrusted content safe. |

## Infrastructure Comparison

The status vocabulary is the shared Task 1 vocabulary. Confidence includes the
approval boundary because the required infrastructure schema has no separate
approval column. `High; evidence-only` means the comparison is direct, while
any Compose/runtime mutation still requires its canonical approval path.

| Infrastructure concern | Workspace evidence | Docker/external basis | Status | Risk / limitation | Required harness/control | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Root includes | Root declares 17 active includes and 20 commented optional entries; included leaves contain 60 service entries before profile selection. | Compose `include` loads each application model and copies resources after base-file merge. | Implemented | Include count is not runtime service count; transitive or future remote includes enlarge trust. | Keep includes local/tracked, render before execution, and review any include change as protected. | `docker-compose.yml` | High; any include mutation requires explicit approval. |
| Variant inventory | 48 infra variants in 40 service directories: 40 canonical, 5 dev, 2 cluster, 1 v2; the canonical generator scans all 49 files including root. | Compose supports multiple files and reusable application models. | Implemented | Repeated service names across variants make 169 entries unsuitable as a unique-container count. | Keep `infra/README.md` classifications and generated coverage synchronized. | `infra/README.md` | High; inventory edits require scoped doc/runtime approval. |
| Profiles | Generated coverage reports 25 labels including `default`: 9 default and 160 profile-gated service entries. | Unassigned services are enabled by default; assigned services activate only with profiles. | Implemented | Profile assignment controls activation, not hard isolation, least privilege, or live capacity. | Validate governed root profiles and keep generated profile coverage fresh. | `docs/90.references/data/docker/compose-profile-service-coverage.md` | High; profile mutation is a protected Compose change. |
| Project names | Only the root declares `name: hy-home-infra`; validation uses the root entrypoint. | Compose project name scopes application resources and can also be overridden by CLI/environment precedence. | Implemented | Operator CLI/environment overrides and standalone leaf invocation can change effective names. | Treat the root name as tracked default and record any operational override in approved task/runbook evidence. | `docker-compose.yml` | High; runtime invocation remains operator-approved. |
| Ordinary, internal, and external networks | Root has one ordinary bridge, zero `internal: true`, and three external networks; all tracked files have no internal declaration. | Docker distinguishes default/custom, internal, and pre-existing external networks; shared external networks enable cross-project DNS. | Partially Implemented | Ordinary does not mean internal; external networks widen reachability and their host existence/ACLs are unknown. | Verify network membership/existence in approved preflight and separately design isolation if required. | `docker-compose.yml` | High for declarations; live network state requires operator approval. |
| Service discovery | All 169 service definitions attach networks; Compose DNS names coexist with many tracked static `ipv4_address` assignments. | Docker recommends service-name discovery because container IPs can change. | Partially Implemented | Static IP dependencies can drift or couple services to IPAM while external-network DNS depends on shared membership. | Prefer service names where compatible and keep exceptions/IPAM governed by the infra-net policy. | `docs/05.operations/policies/12-infra-net/standardize-infra-net.md` | Medium; any addressing change is protected. |
| Ports | 39/169 service entries declare `ports`; 14 are in active included leaves. | Container ports support intra-network traffic; published host ports create an external access path. | Partially Implemented | Static census does not evaluate host binding, firewall, TLS, or whether a port is live. | Review each host publication against ingress policy and validate rendered mappings before approved deployment. | `infra/README.md` | High for key presence; runtime exposure is unknown. |
| Volumes | 130/169 service entries declare volumes; 46 are in active included leaves; the infra rubric requires backup-relevant paths. | Production guidance recommends removing development code bind mounts where appropriate. | Partially Implemented | Bind/persistent volume type, ownership, backup coverage, and host permissions require service-level review. | Keep volume purpose/read-only mode/backup handoff in service docs and operations controls. | `infra/README.md` | High for declarations; data handling requires operator approval. |
| Secrets | Root declares 70 secret IDs; 112/169 service entries and 42/60 root-included entries request secrets. No value was read. | Compose grants explicitly named secrets to services as mounted files. | Partially Implemented | File-backed declaration does not prove rotation, file permission, Vault integration, or absence of other plaintext paths. | Preserve file-based injection, metadata-only evidence, secret scanning, and approved rotation/runbook handoff. | `docs/00.agent-governance/scopes/security.md` | High; values remain protected and policy conflict is tracked in the security reference. |
| Healthchecks | 145/169 service definitions have a healthcheck; active rendered profiles are covered by QuickWin exceptions/control. | Health checks can support readiness conditions for dependent services. | Partially Implemented | 24 declarations lack a key; presence does not prove endpoint correctness or live health. | Keep approved exceptions explicit and pair static checks with runtime health evidence in operations tasks. | `scripts/validation/check-quickwin-baseline.sh` | High for static coverage; live checks require approved execution. |
| Dependencies | 94/169 service definitions declare `depends_on`; hardening checks assert selected `service_healthy` conditions. | Compose starts dependencies in order but waits for readiness only with appropriate conditions. | Partially Implemented | Absence can be valid; presence without health conditions may still race; static scan does not validate every edge. | Validate dependency conditions for stateful/auth paths and document intentional asynchronous dependencies. | `scripts/hardening/check-all-hardening.sh` | High for key coverage; semantic changes require review. |
| Restart behavior | 60/169 service entries declare `restart`; the root-profile QuickWin gate enforces rendered active coverage with exceptions. | Docker production guidance cites restart policies as one production consideration. | Partially Implemented | Cross-variant key count is sparse and one-shot jobs legitimately differ; policy cannot replace recovery behavior. | Keep rendered-profile enforcement and exception rationale; test service-specific failure/recovery in runbooks. | `scripts/validation/check-quickwin-baseline.sh` | High for tracked checks; restart/deploy requires operator approval. |
| Production overlays | Dev, cluster, and v2 alternatives exist, but no tracked `compose.production.yaml` or workspace production-overlay contract was found. | Docker suggests a production-specific override for ports, bind mounts, environment, restart, and extra services where useful. | Missing | Variant names do not prove production suitability; single-host guidance does not cover every topology. | If production Compose is intended, approve a Stage 03 contract defining environment, security, validation, rollback, and ownership before implementation. | `docs/03.specs/README.md` | High for absence; any adoption requires human approval. |
| Hardening | One tiered script covers all 11 infra tiers and CI invokes it; template/security and QuickWin scripts enforce selected controls. | Docker trust guidance calls for review of privilege, capabilities, mounts, networks, devices, images, and file references. | Implemented | Checks are repository-selected assertions, not exhaustive host/container security certification. | Keep the tier registry, exception files, and CI job coupled; add controls only through approved spec/task work. | `scripts/hardening/check-all-hardening.sh` | High; script/control changes are guarded. |
| Validation | Root core render, all governed profiles in CI, generated coverage freshness, implementation alignment, and repository contracts are tracked. | Docker recommends inspecting fully resolved `docker compose config` before executing untrusted or changed input. | Implemented | Render success does not prove external prerequisites, live health, data safety, or production readiness. | Retain core and all-profile gates; use `--preflight` only for approved local prerequisite evidence. | `scripts/validation/validate-docker-compose.sh` | High; validation is non-deployment evidence. |
| Observability | Root includes the dev observability variant; tracked full/dev variants contain 18 service entries and the Stage 05 observability set exists. | Production guidance identifies logging/aggregation as an environment-specific concern. | Partially Implemented | Declared services and dashboards do not prove ingestion, retention, alerts, SLOs, or live visibility. | Route live metrics/log/trace and retention proof through the observability policy/runbooks. | `docs/05.operations/policies/06-observability/README.md` | High for tracked surfaces; runtime telemetry is unknown. |
| Backup / restore handoff | Volume rubrics, data policies, backup references, and recovery runbooks are tracked; no backup or restore was executed in this task. | Docker production guidance leaves application/data protection environment-specific. | Partially Implemented | Stage 00/05 requirements are normative; current off-site backup success and restore-drill evidence remain unknown. | Record schedule, scope, retention, restore test, evidence owner, and failure escalation in Stage 05 per data service. | `docs/05.operations/policies/README.md` | Medium; backup/restore execution requires operator approval. |
| Rollback | Git revert, task evidence, and service runbooks provide configuration/recovery paths; deployment was not exercised. | Compose can recreate services after config/image changes, but application/data rollback is service-specific. | Partially Implemented | Git rollback cannot reverse data migration, volume mutation, external dependency, or secret rotation. | Require service-specific safe rollback/recovery and data compatibility evidence before approved changes. | `docs/05.operations/runbooks/README.md` | High for ownership; any live rollback is human/operator controlled. |
| Runbook linkage | Infra README rubric requires operations links and doc alignment validates many guide/policy/runbook pairs. | Docker pages describe mechanics, not this workspace's incident/recovery ownership. | Partially Implemented | Link presence does not prove procedural completeness, currency, rehearsal, or coverage of every variant. | Keep service-to-Stage-05 links aligned and route missing recovery evidence to one runbook owner. | `docs/05.operations/runbooks/README.md` | Medium; procedure changes and executions require approval. |

Status totals: **19 concerns — 6 Implemented, 12 Partially Implemented,
1 Missing, 0 Not Applicable**.

## Potential Follow-up / Gap

- A separately approved Stage 03/04 effort may define whether a production
  overlay is required and what environment it targets.
- Network isolation, static-IP reduction, backup verification, and runbook
  completeness remain service-specific controls; this reference does not
  authorize their implementation.
- Remote external-network state, live service health, runtime ports, volumes,
  and backups remain unknown because this task performed no runtime mutation or
  secret-value read.

## Source Rules

- Repo-local claims use tracked files at base `34fc342e` and the fresh canonical
  coverage generator; Graphify (`30df271a`) is stale/advisory only.
- External sources were retrieved on `2026-07-11`; pages without visible dates
  provide retrieval-time guidance only.
- Docker examples are comparison material and do not create workspace policy.
- Secret evidence is limited to identifiers, paths, counts, and control state.

## Sources

- [Docker Compose overview](https://docs.docker.com/compose/) - Compose product and application-model entry point
- [Compose file reference](https://docs.docker.com/reference/compose-file/) - services, resources, profiles, secrets, and healthcheck syntax
- [Compose include](https://docs.docker.com/reference/compose-file/include/) - modular application model and relative-path behavior
- [Using profiles](https://docs.docker.com/compose/how-tos/profiles/) - default and profile-gated activation semantics
- [Compose networking](https://docs.docker.com/compose/how-tos/networking/) - service DNS, internal/external networks, and multi-project communication
- [Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/) - explicit service grant and file-mount model
- [Startup order](https://docs.docker.com/compose/how-tos/startup-order/) - dependency and health-condition behavior
- [Compose production](https://docs.docker.com/compose/how-tos/production/) - single-host production considerations and optional override pattern
- [Compose trust model](https://docs.docker.com/compose/trust-model/) - trusted-input, transitive dependency, and resolved-config review boundary
- [Root Compose](../../../../docker-compose.yml) - root name, networks, secrets, and active includes
- [Infra README](../../../../infra/README.md) - variant/service-directory inventory and documentation rubric
- [Generated Compose coverage](../../data/docker/compose-profile-service-coverage.md) - canonical file, service, and profile snapshot
- [Coverage generator](../../../../scripts/operations/generate-compose-profile-service-coverage.sh) - deterministic tracked-file derivation
- [Compose validator](../../../../scripts/validation/validate-docker-compose.sh) - rendered profile validation and preflight boundary
- [Hardening entry point](../../../../scripts/hardening/check-all-hardening.sh) - tiered infrastructure checks
- [QuickWin baseline](../../../../scripts/validation/check-quickwin-baseline.sh) - rendered restart, healthcheck, resource, and secret checks

## Maintenance

- **Owner**: Documentation maintainers with Infra/DevOps and Security review
- **Review Cadence**: Review after Compose, infra inventory, generated coverage,
  hardening, validation, or relevant Docker guidance changes
- **Update Trigger**: Recompute all counts and revalidate external sources; do
  not copy prior census values

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [security governance](./security-governance.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [HAFE spec](../../../03.specs/094-harness-agent-first-engineering/spec.md)
