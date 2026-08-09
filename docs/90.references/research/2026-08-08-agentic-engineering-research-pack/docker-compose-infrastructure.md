---
status: draft
artifact_id: reference:agentic-engineering-research:docker-compose-infrastructure
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Docker Compose and Infrastructure

## Overview

Docker Compose defines an application model from services, networks, volumes,
configs, secrets, profiles, and related file features. This workspace adds an
infrastructure harness around that model: a root include boundary, forty-seven
infra variants across eleven tiers, a shared template library, generated
coverage and image-provenance snapshots, hardening checks, operations
documents, and protected-change rules.

At Task 8 baseline `910ce5f36641635118c64b1aa6cfe48f86ecde14`,
the fresh generated inventory scans 48 Compose files including the root, 47
files with services, 168 service entries, and 25 profile labels including
`default`. Those 168 rows describe declarations across canonical, development,
and cluster variants; they are not 168 unique services or simultaneous runtime
containers. The root actually includes 17 leaf files containing 60 service
entries before profile selection.

## Purpose

Satisfy REQ-07 and REQ-08 with a current, reproducible comparison of Compose
concepts, tracked workspace topology, infrastructure controls, adoption rules,
operations evidence, and explicit runtime limits. The analysis keeps variant
inventory, root-deployable topology, static validation, live execution, and
remote dependencies as separate evidence states.

## Repository Role

This Stage 90 reference is advisory analysis. It does not change Compose,
adopt an upstream example as policy, approve a port or network exception,
create a secret, execute a backup, start a service, or authorize deployment.
Runtime truth remains in approved observations of the tracked Compose owners;
policy and procedures remain in Stage 00 and Stage 05, and implementation gaps
require a separate Stage 03/04 chain.

## Scope

### In scope

- Root and `infra/**/docker-compose*.yml` / `.yaml` declarations, includes,
  services, profiles, networks, ports, volumes, secrets, dependencies, images,
  healthchecks, and shared-template use.
- Fresh generated Compose coverage and image-provenance evidence, plus the
  eleven-tier hardening result.
- Gateway exposure, localhost binding, persistent-volume backup evidence, the
  gateway latency SLO, recovery/rollback ownership, and protected-change rules.
- Current gaps, exceptions, evidence limits, adoption rules, and implications
  for all fourteen normative scopes.

### Out of scope

- `docker compose` or Docker execution, including rendered configuration,
  network/container/volume creation, runtime health, and logs.
- Reading `.env` or secret values, changing secret mappings, or proving host
  filesystem permissions and rotation.
- Live external-network existence, firewall/TLS posture, latency measurement,
  backup success, restore rehearsal, deployment, or rollback execution.
- Repairing the infra README census, Compose files, hardening policy, or any
  generated output.

## Definitions / Facts

### Evidence and topology model

- **Compose file:** root `docker-compose.yml` or one tracked infra file whose
  name begins `docker-compose` and ends `.yml` or `.yaml`.
- **Variant service entry:** one `services` mapping row in one file. Repeated
  names in dev, canonical, and cluster variants count separately.
- **Root-included entry:** a service row in one of the 17 uncommented root
  `include` paths. Profiles still control activation, so inclusion is not
  runtime proof.
- **Static evidence:** tracked definition, deterministic parse, or local
  validator result. It cannot prove a container, network, secret, backup, SLO,
  or external dependency exists at runtime.
- **Registered exception:** an item with a named owner, reason, and cadence in
  a tracked exception registry. A missing control is not an exception merely
  because it may have an operational explanation.

### Re-measured Compose and infrastructure census

The canonical coverage `--check` passed and its `--dry-run` output was parsed
alongside all tracked Compose YAML at the Task 8 baseline. No Compose command
was run.

| Measure | Current value | Interpretation |
| --- | ---: | --- |
| Compose files | 48 | Root plus 47 infra variants; `infra/README.md` says 48 infra variants and is one high. |
| Infra variants | 47 | 40 canonical, 5 development, and 2 cluster files. |
| Files with services | 47 | Every infra variant; root declares resources/includes but no services. |
| Variant service entries / distinct names | 168 / 138 | Duplication across variants is preserved; neither number is a runtime count. |
| Profiles | 25 | 8 default entries and 160 profile-gated entries. |
| Root-active includes / entries | 17 / 60 | Static include topology before profile selection. |
| `infra_net` membership | 168 / 168 | Declared membership only; reachability/isolation is not exercised. |
| `depends_on` / `healthcheck` / `restart` | 92 / 144 / 60 | Key presence only; readiness and recovery behavior remain unverified. |
| `extends` | 164 / 168 across 46 files | Shared-template inheritance is a large transitive change surface. |
| Port-bearing service entries | 39 / 168 | 62 mapping items; 14 port-bearing entries are in root-included files. |
| Volume-bearing service entries | 129 / 168 | 46 are in root-included files. |
| Top-level volume declarations | 102 | Sum across variants; duplicate purposes are not deduplicated. |
| Secret-bearing service entries | 107 / 168 | 240 service grants; 42 secret-bearing entries are root-included. |
| Root secret identifiers | 70 | Identifiers and paths only; values were not read. |

### Inventory is not one deployable topology

The 168 rows span alternatives. The root includes 17 files and 60 uniquely
named entries; optional, standalone, canonical, dev, and cluster variants
remain separate declarations. A reviewer must select one intended file/profile
combination before reasoning about conflicts, resources, or lifecycle. The
generated inventory intentionally does not resolve includes or profiles.

`infra/README.md` currently describes 48 files under `infra/`, while the
generator and `git ls-files` find 47 there and 48 only after adding the root.
Its separate claims of 40 service directories and 17 root-active includes
remain consistent with the tracked tree. This is documentation drift, not a
Compose runtime defect, and is outside Task 8 ownership.

### Networks and port exposure

The root declares ordinary bridge `infra_net` plus three external networks;
no tracked Compose network is declared `internal: true`. All 168 service
entries declare `infra_net`, satisfying the textual membership requirement at
configuration depth. External declarations do not prove host networks exist.

Thirty-nine service entries publish 62 host-port mappings. Thirty-seven of
those services are outside `infra/01-gateway`, and none of the 39 uses an
explicit `host_ip` or `127.0.0.1` binding. Environment-substituted host ports
are still port numbers, not host-IP binds. No tracked port-exposure exception
registry with owner/reason/cadence was found. The 37 are therefore unresolved
configuration conflicts with the infra scope's gateway-only and localhost
review rules, not approved exceptions. Static declarations alone do not prove
the ports are live, reachable through a firewall, unauthenticated, or
exploitable.

Adoption rule: a future service/port change must classify gateway routing,
localhost-only operator access, protocol-required direct publication, or a
time-bounded exception in its approved Spec/Task. It must then validate the
selected rendered topology and record rollback; Stage 90 cannot grant the
exception.

### Volumes, backup, restore, and rollback

The 47 variants declare 102 top-level volumes, and 129 service entries mount a
volume or bind path. No top-level volume declaration contains a backup label.
This does not prove there are 102 unique persistent datasets, and absence of a
label does not prove backups are absent: variants repeat purposes, some mounts
are ephemeral/configuration, and backup behavior can live in Stage 05 or
external operator systems.

The infra scope nevertheless requires automated backup tags for persistent
data. Current configuration does not supply that evidence, and no live backup
or restore was observed. The canonical follow-up is a per-dataset inventory
with persistence class, owner, schedule, retention, recovery objective,
latest successful backup, and restore-rehearsal evidence. Git revert is only a
configuration rollback; it cannot reverse data migration, volume mutation,
external state, or secret rotation.

### Hardening and shared templates

`bash scripts/hardening/check-all-hardening.sh` passed all eleven tier checks.
The shared template supplies `no-new-privileges:true` and `cap_drop: ALL` to
many services through external-file `extends`. The exception registry records
no `no-new-privileges` exception and three named `cap_drop: ALL` exceptions
for `pg-0`, `pg-1`, and `pg-2`; those are registered compatibility exceptions,
not violations. It also records job/restart, developer-healthcheck, and
secret-use exceptions with reasons.

The pass proves only the repository-selected static assertions. It does not
prove fully resolved Compose semantics, daemon/kernel controls, image content,
runtime user identity, or host posture. Because 164 entries inherit through
`extends`, template edits have broad transitive impact and require protected
Compose review rather than isolated file reasoning.

### Images, pins, and exceptions

The tech-stack provenance `--check` passed. Its `--dry-run` reports 18 curated
components and 21 registry images: 20 `declared-pinned` and one approved
floating exception, `lfnovo/open_notebook:v1-latest-single`, owned by the
Laboratory Operator with monthly review. This registry is deliberately narrower
than the four-item floating-tag exception registry. The difference is scope,
not a violation: three approved floating images are not curated tech-stack
entries.

Image declaration parity is not a registry lookup, digest pin, vulnerability
scan, SBOM, signature, attestation, or deployed-image observation. Image and
exception changes need coupled registry/Compose updates and the canonical
freshness check.

### Gateway latency SLO and observability

The infra scope states gateway `LATENCY_SLO < 200ms`. An exact tracked search
found the threshold only in that governance scope and its subagent preamble;
no infra, script, or workflow owner measures or gates the threshold. Existing
metrics, dashboards, and general latency queries do not establish this exact
SLO, an observation window, a percentile, an error budget, or current
compliance.

Adoption requires a Stage 03 definition of request population, percentile,
window, exclusions, data source, alert/error budget, and owner, followed by
runtime evidence in Stage 05. Until then the SLO is a policy target with a
Missing measured implementation, not a performance claim.

### Validation and operations evidence ladder

| Evidence layer | Task 8 state | Limit |
| --- | --- | --- |
| Tracked definitions | Verified at `910ce5f` | Variants and profiles are not resolved runtime. |
| Generated coverage | `--check` PASS; dry-run remeasured | Inventory only. |
| Generated image provenance | `--check` PASS; dry-run remeasured | Declaration parity only. |
| Hardening | Eleven-tier script PASS | Selected static assertions only. |
| Compose render/preflight | Not Run by explicit boundary | Could create `.env`/dummy-secret evidence or depend on Docker. |
| Runtime health/network/ports | `UNVERIFIED` | No Docker/Compose command authorized. |
| Backup/restore/SLO/rollback | `UNVERIFIED` | No operator exercise or telemetry observed. |

### Current gaps and ownership

| Gap | State | Canonical owner / next evidence |
| --- | --- | --- |
| Infra README file count | Tracked drift | Infra documentation owner; correct in a separate approved docs task. |
| Non-gateway published ports without host IP | 37 unresolved declarations | `infra-implementer` plus security/entry review; classify exception or remediate in approved service tasks. |
| Backup labels/evidence | 0 labels across 102 declarations; runtime unknown | Infra/ops owners; per-dataset backup and restore evidence. |
| Exact latency SLO implementation | Missing | Architecture/infra/ops Spec defining measurement and error-budget contract. |
| Runtime prerequisites and recovery | `UNVERIFIED` | Operator-approved preflight, health, dependency, and recovery procedure. |

## Scope Implications

| Scope | Infrastructure implication |
| --- | --- |
| `agentic` | Agents may inventory and validate within approval bounds; they must not turn Compose definitions or a validator pass into runtime claims. |
| `architecture` | Own intended single-host/variant topology, trust boundaries, data durability, SLO semantics, and any production/deployment contract. |
| `backend` | No backend application surface is established; a future service must declare network, port, dependency, secret, persistence, health, and recovery contracts. |
| `common` | Shared templates are a 164-entry transitive surface; common changes need blast-radius evidence and exception compatibility. |
| `docs` | Keep variant inventory distinct from root topology, repair the one-file README drift separately, and route procedures to Stage 05. |
| `entry` | Review all 37 non-gateway port-bearing services, gateway routing, TLS/auth, localhost binding, and explicit exceptions. |
| `frontend` | No product frontend topology is established; future UI exposure belongs behind the entry contract with tested health and rollback. |
| `infra` | Own Compose, templates, registries, exceptions, validation, backup labels, and runtime-approved change/recovery evidence. |
| `meta` | Generated census and provenance metadata need byte-exact freshness and must retain their inventory/runtime exclusions. |
| `mobile` | No mobile runtime surface is present; any future local dependency needs a documented gateway/API boundary rather than direct database exposure. |
| `ops` | Own live prerequisites, health, telemetry, backup/restore, incident response, rollout, and rollback evidence; static checks are insufficient. |
| `product` | Define critical service journeys and acceptable availability/latency before an infrastructure SLO or production-readiness claim. |
| `qa` | Keep file/profile/variant coverage, render validation, hardening, runtime health, recovery, and SLO verification as separate gates. |
| `security` | Review transitive Compose trust, privileges, published ports, external networks, secret grants, images, and registered exceptions without reading values. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [Docker Compose file reference](https://docs.docker.com/reference/compose-file/) | 2026-08-08T18:18:06+09:00 | External mutable | Verified official page; Compose application-model capability only. |
| [Root Compose](../../../../docker-compose.yml) | 2026-08-08 | Workspace tracked at `910ce5f` | Root name, four networks, 70 secret IDs, and 17 active includes read without values. |
| [Generated Compose coverage](../../data/docker/compose-profile-service-coverage.md) | 2026-08-08 | Workspace generated/tracked | `--check` PASS and `--dry-run` verified 48/47/168/25 counts; not runtime evidence. |
| [Coverage generator](../../../../scripts/operations/generate-compose-profile-service-coverage.sh) | 2026-08-08 | Workspace tracked | Candidate/parse rules read directly. |
| [Infra README](../../../../infra/README.md) | 2026-08-08 | Workspace tracked | Root-active and directory claims checked; infra variant count is one high. |
| [Infrastructure scope](../../../00.agent-governance/scopes/infra.md) | 2026-08-08 | Workspace tracked policy | Gateway, network, volume, hardening, secret, backup, SLO, and approval requirements. |
| [Shared template library](../../../../infra/common-optimizations.yml) and [exceptions](../../../../infra/common-optimizations.exceptions.json) | 2026-08-08 | Workspace tracked | Control inheritance and registered exception semantics. |
| [Hardening entry point](../../../../scripts/hardening/check-all-hardening.sh) | 2026-08-08 | Workspace tracked/executed | Eleven tier checks passed; static selected-control evidence only. |
| [Tech-stack registry](../../../../infra/tech-stack.versions.json) and [floating exceptions](../../../../infra/image-tag-policy.exceptions.json) | 2026-08-08 | Workspace tracked | 18 components, 21 curated images, and exception ownership. |
| [Tech-stack provenance](../../data/docker/tech-stack-version-provenance.md) | 2026-08-08 | Workspace generated/tracked | `--check` PASS; dry-run reports 20 pinned and one approved floating row. |
| [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) | 2026-08-08 | Workspace tracked policy | Compose, secret, runtime, validation, rollback, and hard-stop boundaries. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace tracked stale/advisory | Built from `f8a72211`; navigation clues were corroborated and not used as proof. |

## Maintenance

Re-run both canonical `--check` and `--dry-run` generators, the exact tracked
Compose inventory, and the hardening entry point after Compose, templates,
profiles, registries, exceptions, or relevant Docker guidance changes. Keep
variant inventory, selected root topology, rendered configuration, runtime
observation, and operations evidence in separate fields. Owner: Documentation
maintainers with Infra/DevOps, Entry, Security, and Operations review.

## Related Documents

- [Verification and validation](./verification-validation.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Security governance](./security-governance.md)
- [Automation pipeline and workflow](./automation-pipeline-workflow.md)
- [Quality, CI, and formatting](./quality-ci-formatting.md)
- [Compose data index](../../data/docker/README.md)
