---
title: "Reference: Docker Compose and Infrastructure"
version: "1.2.1"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0002-m0005"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
---

# Reference: Docker Compose and Infrastructure

## Overview

### Overview
>
> Historical evidence (not current authority; source: Git history):
>
> Docker Compose defines an application model from services, networks, volumes,
> configs, secrets, profiles, and related file features. This workspace adds an
> infrastructure harness around that model: a root include boundary, forty-seven
> infra variants across eleven tiers, a shared template library, generated
> coverage and image-provenance snapshots, hardening checks, operations
> documents, and protected-change rules.
>
> At Task 8 baseline `910ce5f36641635118c64b1aa6cfe48f86ecde14`,
> the fresh generated inventory scans 48 Compose files including the root, 47
> files with services, 168 service entries, and 25 profile labels including
> `default`. Those 168 rows describe declarations across canonical, development,
> and cluster variants; they are not 168 unique services or simultaneous runtime
> containers. The root actually includes 17 leaf files containing 60 service
> entries before profile selection.
>

## Scope and Method

### Current External Research

What Compose semantics and operating evidence should a Linux home/development server distinguish before a future infrastructure decision?

Repository baseline: `f30b168e2fbb0959e4a31749935568fd5b3942f1`. External sources checked and document updated: 2026-09-27. This refresh is external-only, non-normative research. Internal application, runtime, account and security status: **Not assessed in this run**. Adoption requires the existing owner and an authorized change; historical observations below retain their original dates and scope.

### Model, composition and version support

The Compose Specification describes an application model; implementations may
support different platform attributes. Top-level `version` is obsolete and does
not pin a parser schema. The upstream release page currently exposes v5.5.1;
this is external release evidence, not a measurement of this host. Record the
actual CLI/Engine/platform and required features in a future acceptance packet.

| Mechanism | Intended use | Resolution and trade-off |
| --- | --- | --- |
| `include` | Independently maintained models | 2.20.0+; each included project has its own path base; resources copied after ordinary merge; name conflicts detected rather than silently merged; local environment overrides included defaults. |
| Ordered `-f` merge | Override one application | Maps merge, sequences generally append; command/entrypoint/healthcheck test override. Ports have a compound uniqueness key; mounts use target. `!reset` clears, `!override` replaces on 2.24.4+. |
| `extends` | Reuse service fields | External referenced service is not automatically instantiated; dependent resources must be declared. The guide discusses base paths and conversion of referenced paths: inspect the resulting model instead of assuming include semantics. `stack deploy` differs. |
| Profiles | Optional capability selection | Unprofiled services normally enabled; explicit target activates that service and eligible dependencies, not all profile peers. Selection is not an authorization boundary. |

Interpolation and container environment are separate pipelines. Current model
interpolation precedence is shell, explicit `--env-file`, then project-directory
`.env` when no explicit file is given. Project directory comes from
`--project-directory`, first `-f`, or working directory; a `.env` that changes
`COMPOSE_FILE` can lead to a second lower-precedence file. Container precedence
is CLI `run -e`, interpolated environment/env_file, literal `environment`, service
`env_file`, then image ENV. Host variables are not automatically passed without
mapping. Project naming prioritizes `-p`, `COMPOSE_PROJECT_NAME`, top-level
`name`, project directory, then working-directory fallback. Explicit external
names and host bindings need separate collision review.

### Runtime, state and trust

Dependency order, `service_healthy`, job completion and crash recovery are
different signals. `depends_on.restart` covers Compose-controlled dependency
updates, not runtime crash recovery. Probe success does not establish a usable
workflow. Network attachment is distinct from host publication; omitted host
addresses can bind broadly. `internal` and `external` serve different purposes.
Localhost binding alone does not prove peer authorization or firewall behavior.

Separate disposable container state, persistent volumes, host-dependent bind
mounts, non-secret configs and per-service secrets. Config content/environment
sources require 2.23.1+. A secret declaration does not prove encrypted source
storage, rotation, host permissions or correct application use. No private
values belong in research or render evidence.

Limits, reservations and deploy attributes require compatible runtime support;
a reservation is not a hard ceiling, and declaration is not measured capacity.
Service restart, dependency restart and deploy restart govern different events.
Stop signal/grace period must fit the application; timeout can cause SIGKILL
and incomplete writes. Image/config rollback cannot reverse every data migration.
Digest pins select exact content but require deliberate updates for fixes.
Tags, SBOMs, signatures, provenance and vulnerability results answer different
questions; provenance mode/schema choices matter. Supply-chain trust is detailed
in [m0017](m0017-security-governance.md).

### Operating principles and evidence

These are conditional recommendations. Name ingress, DNS, certificate renewal,
identity and data owners before adding daemons. RFC 9846 (July 2026) now specifies
TLS 1.3 and obsoletes RFC 8446; channel security does not prove application
authorization. ACME challenges prove domain control under protocol conditions;
key custody, renewal and DNS dependency recovery still need operational evidence.
DNS caching/TTLs affect cutover. Use a small set of actionable user checks plus
latency, traffic, errors and saturation where useful.

Recovery design should name RPO (tolerable data loss) and RTO (recovery time),
application-consistent data, configuration/software versions, approved key custody
and dependency order. Corrected NIST SP 800-34 Rev.1 supports planning/testing;
it is federal guidance, not an automatic home-server obligation. Docker's tar
example demonstrates volume mechanics, not running-database consistency.
Same-host replicas do not alone cover host loss.

| Evidence layer | What a future result supports | Separate acceptance |
| --- | --- | --- |
| Static `config` | Selected CLI parses/renders selected model | Runtime support/resource creation/secret delivery |
| Process execution | Named process started | Readiness/user purpose/data correctness |
| Readiness | Named probe passed at a named time | End-to-end purpose/sustained reliability |
| User validation | Representative workflow met acceptance | Backup completeness/disaster recovery |
| Isolated restoration | Selected backup restored with integrity/time/data-loss evidence | Other datasets/future backups/live cutover |

Update/rollback needs a migration compatibility boundary and preserved recoverable
state. Service overlap, licenses, optional selection and operating burden belong
in [m0021](m0021-local-docker-service-consolidation.md#current-external-research).

### Purpose
>
> Historical evidence (not current authority; source: Git history):
>
> Satisfy REQ-07 and REQ-08 with a current, reproducible comparison of Compose
> concepts, tracked workspace topology, infrastructure controls, adoption rules,
> operations evidence, and explicit runtime limits. The analysis keeps variant
> inventory, root-deployable topology, static validation, live execution, and
> remote dependencies as separate evidence states.
>

### Repository Role
>
> Historical evidence (not current authority; source: Git history):
>
> This Stage 90 reference is advisory analysis. It does not change Compose,
> adopt an upstream example as policy, approve a port or network exception,
> create a secret, execute a backup, start a service, or authorize deployment.
> Runtime truth remains in approved observations of the tracked Compose owners;
> policy and procedures remain in canonical agent governance and Stage 05, and implementation gaps
> require a separate Stage 03/04 chain.
>

### Research Ownership
>
> Historical evidence (not current authority; source: Git history):
>
> This member is the canonical owner for Compose topology, include/profile
> semantics, static infrastructure inventory, hardening, image provenance, and
> validation evidence. It does not own the decision that a local service is
> functionally redundant or should be removed. That service-role and license
> question is consolidated in [RES-0002-m0021](m0021-local-docker-service-consolidation.md).
>

### Scope
>
> Historical evidence (not current authority; source: Git history):
>
### In scope
>
> Historical evidence (not current authority; source: Git history):
>
> - Root and `infra/**/docker-compose*.yml` / `.yaml` declarations, includes,
>   services, profiles, networks, ports, volumes, secrets, dependencies, images,
>   healthchecks, and shared-template use.
> - Fresh generated Compose coverage and image-provenance evidence, plus the
>   eleven-tier hardening result.
> - Gateway exposure, localhost binding, persistent-volume backup evidence, the
>   gateway latency SLO, recovery/rollback ownership, and protected-change rules.
> - Current gaps, exceptions, evidence limits, adoption rules, and implications
>   for all fourteen normative scopes.
>
### Out of scope
>
> Historical evidence (not current authority; source: Git history):
>
> - `docker compose` or Docker execution, including rendered configuration,
>   network/container/volume creation, runtime health, and logs.
> - Reading `.env` or secret values, changing secret mappings, or proving host
>   filesystem permissions and rotation.
> - Live external-network existence, firewall/TLS posture, latency measurement,
>   backup success, restore rehearsal, deployment, or rollback execution.
> - Repairing the infra README census, Compose files, hardening policy, or any
>   generated output.
>

### Definitions / Facts
>
> Historical evidence (not current authority; source: Git history):
>
### Evidence and topology model
>
> Historical evidence (not current authority; source: Git history):
>
> - **Compose file:** root `docker-compose.yml` or one tracked infra file whose
>   name begins `docker-compose` and ends `.yml` or `.yaml`.
> - **Variant service entry:** one `services` mapping row in one file. Repeated
>   names in dev, canonical, and cluster variants count separately.
> - **Root-included entry:** a service row in one of the 17 uncommented root
>   `include` paths. Profiles still control activation, so inclusion is not
>   runtime proof.
> - **Static evidence:** tracked definition, deterministic parse, or local
>   validator result. It cannot prove a container, network, secret, backup, SLO,
>   or external dependency exists at runtime.
> - **Registered exception:** an item with a named owner, reason, and cadence in
>   a tracked exception registry. A missing control is not an exception merely
>   because it may have an operational explanation.
>
### Re-measured Compose and infrastructure census
>
> Historical evidence (not current authority; source: Git history):
>
> The canonical coverage `--check` passed and its `--dry-run` output was parsed
> alongside all tracked Compose YAML at the Task 8 baseline. No Compose command
> was run.
>
> | Measure                                  |             Current value | Interpretation                                                                         |
> | ---------------------------------------- | ------------------------: | -------------------------------------------------------------------------------------- |
> | Compose files                            |                        48 | Root plus 47 infra variants; `infra/README.md` says 48 infra variants and is one high. |
> | Infra variants                           |                        47 | 40 canonical, 5 development, and 2 cluster files.                                      |
> | Files with services                      |                        47 | Every infra variant; root declares resources/includes but no services.                 |
> | Variant service entries / distinct names |                 168 / 138 | Duplication across variants is preserved; neither number is a runtime count.           |
> | Profiles                                 |                        25 | 8 default entries and 160 profile-gated entries.                                       |
> | Root-active includes / entries           |                   17 / 60 | Static include topology before profile selection.                                      |
> | `infra_net` membership                   |                 168 / 168 | Declared membership only; reachability/isolation is not exercised.                     |
> | `depends_on` / `healthcheck` / `restart` |             92 / 144 / 60 | Key presence only; readiness and recovery behavior remain unverified.                  |
> | `extends`                                | 164 / 168 across 46 files | Shared-template inheritance is a large transitive change surface.                      |
> | Port-bearing service entries             |                  39 / 168 | 62 mapping items; 14 port-bearing entries are in root-included files.                  |
> | Volume-bearing service entries           |                 129 / 168 | 46 are in root-included files.                                                         |
> | Top-level volume declarations            |                       102 | Sum across variants; duplicate purposes are not deduplicated.                          |
> | Secret-bearing service entries           |                 107 / 168 | 240 service grants; 42 secret-bearing entries are root-included.                       |
> | Root secret identifiers                  |                        70 | Identifiers and paths only; values were not read.                                      |
>
### Inventory is not one deployable topology
>
> Historical evidence (not current authority; source: Git history):
>
> The 168 rows span alternatives. The root includes 17 files and 60 uniquely
> named entries; optional, standalone, canonical, dev, and cluster variants
> remain separate declarations. A reviewer must select one intended file/profile
> combination before reasoning about conflicts, resources, or lifecycle. The
> generated inventory intentionally does not resolve includes or profiles.
>
> `infra/README.md` currently describes 48 files under `infra/`, while the
> generator and `git ls-files` find 47 there and 48 only after adding the root.
> Its separate claims of 40 service directories and 17 root-active includes
> remain consistent with the tracked tree. This is documentation drift, not a
> Compose runtime defect, and is outside Task 8 ownership.
>
### Networks and port exposure
>
> Historical evidence (not current authority; source: Git history):
>
> The root declares ordinary bridge `infra_net` plus three external networks;
> no tracked Compose network is declared `internal: true`. All 168 service
> entries declare `infra_net`, satisfying the textual membership requirement at
> configuration depth. External declarations do not prove host networks exist.
>
> Thirty-nine service entries publish 62 host-port mappings. Thirty-seven of
> those services are outside `infra/01-gateway`, and none of the 39 uses an
> explicit `host_ip` or `127.0.0.1` binding. Environment-substituted host ports
> are still port numbers, not host-IP binds. No tracked port-exposure exception
> registry with owner/reason/cadence was found. The 37 are therefore unresolved
> configuration conflicts with the infra scope's gateway-only and localhost
> review rules, not approved exceptions. Static declarations alone do not prove
> the ports are live, reachable through a firewall, unauthenticated, or
> exploitable.
>
> Adoption rule: a future service/port change must classify gateway routing,
> localhost-only operator access, protocol-required direct publication, or a
> time-bounded exception in its approved Spec/Task. It must then validate the
> selected rendered topology and record rollback; Stage 90 cannot grant the
> exception.
>
### Volumes, backup, restore, and rollback
>
> Historical evidence (not current authority; source: Git history):
>
> The 47 variants declare 102 top-level volumes, and 129 service entries mount a
> volume or bind path. No top-level volume declaration contains a backup label.
> This does not prove there are 102 unique persistent datasets, and absence of a
> label does not prove backups are absent: variants repeat purposes, some mounts
> are ephemeral/configuration, and backup behavior can live in Stage 05 or
> external operator systems.
>
> The infra scope nevertheless requires automated backup tags for persistent
> data. Current configuration does not supply that evidence, and no live backup
> or restore was observed. The canonical follow-up is a per-dataset inventory
> with persistence class, owner, schedule, retention, recovery objective,
> latest successful backup, and restore-rehearsal evidence. Git revert is only a
> configuration rollback; it cannot reverse data migration, volume mutation,
> external state, or secret rotation.
>
### Hardening and shared templates
>
> Historical evidence (not current authority; source: Git history):
>
> `bash scripts/hardening/check-all-hardening.sh` passed all eleven tier checks.
> The shared template supplies `no-new-privileges:true` and `cap_drop: ALL` to
> many services through external-file `extends`. The exception registry records
> no `no-new-privileges` exception and three named `cap_drop: ALL` exceptions
> for `pg-0`, `pg-1`, and `pg-2`; those are registered compatibility exceptions,
> not violations. It also records job/restart, developer-healthcheck, and
> secret-use exceptions with reasons.
>
> The pass proves only the repository-selected static assertions. It does not
> prove fully resolved Compose semantics, daemon/kernel controls, image content,
> runtime user identity, or host posture. Because 164 entries inherit through
> `extends`, template edits have broad transitive impact and require protected
> Compose review rather than isolated file reasoning.
>
### Images, pins, and exceptions
>
> Historical evidence (not current authority; source: Git history):
>
> The tech-stack provenance `--check` passed. Its `--dry-run` reports 18 curated
> components and 21 registry images: 20 `declared-pinned` and one approved
> floating exception, `lfnovo/open_notebook:v1-latest-single`, owned by the
> Laboratory Operator with monthly review. This registry is deliberately narrower
> than the four-item floating-tag exception registry. The difference is scope,
> not a violation: three approved floating images are not curated tech-stack
> entries.
>
> A direct re-scan of `infra/**/docker-compose*.yml` today (`rg -o
> 'image:\s*\S+'`) counts 137 `image:` declarations across the 47 variants, 82
> distinct image references, and zero occurrences of a literal `:latest` tag.
> Exactly one declaration, `image: b4bz/homer` at
> `infra/11-laboratory/dashboard/docker-compose.yml:20`, has no explicit tag at
> all; Docker resolves an untagged reference to the vendor's `latest` channel at
> pull time even though the string `:latest` never appears in the file. Reading
> [`infra/image-tag-policy.exceptions.json`](../../../../infra/image-tag-policy.exceptions.json)
> directly confirms this is a registered, not a hidden, floating pin: all four
> `floating_image_exceptions` entries — `nginx:alpine` (Gateway Operator),
> `portainer/portainer-ce:sts` (Laboratory Operator), `lfnovo/open_notebook:v1-latest-single`
> (Laboratory Operator), and `b4bz/homer` (Laboratory Operator, "pin before
> promoting beyond local admin use") — carry an owner, a reason, and a monthly
> `review_cadence` under `policy_id: OPS-IMAGE-TAG-EXCEPTIONS-001`. None of the
> four registered floating images is root-active by default; homer and
> portainer are laboratory-tier and dashboard-only in `infra/README.md`'s own
> census. This re-derivation confirms the leaf's structural claim (declared
> image pin coverage is effectively complete once registered exceptions are
> subtracted) without upgrading it to a digest, vulnerability, or runtime claim.
>
> Image declaration parity is not a registry lookup, digest pin, vulnerability
> scan, SBOM, signature, attestation, or deployed-image observation. Image and
> exception changes need coupled registry/Compose updates and the canonical
> freshness check.
>
### Resource limits and restart-policy census
>
> Historical evidence (not current authority; source: Git history):
>
> A direct `rg` scan for `deploy:`, `mem_limit:`, and `cpus:` across all 47
> variant files finds exactly **two** files that declare any CPU/memory
> resource control: `infra/08-ai/ollama/docker-compose.yml:36-42` (`deploy.resources.limits.cpus:
> '4.0'`, `limits.memory: 8G`, `reservations.memory: 4G`) and
> `infra/09-tooling/locust/docker-compose.yml:66-67` (`deploy.replicas: 2`, no
> CPU/memory bound at all). No other service in the 168-row inventory declares a
> `deploy.resources` block, a `mem_limit`, or a `cpus` key. Resource governance
> is therefore not a fleet-wide control; it exists only where one operator
> added it locally for a GPU-bound service. A host with limited RAM/CPU has no
> tracked mechanism preventing any of the other 166 service entries from
> consuming unbounded resources, and no exception registry documents this as an
> accepted risk the way `cap_drop`/`restart`/`healthcheck` gaps are documented.
>
> Restart policy is more disciplined: `rg -o "restart:\s*\S+"` finds exactly two
> values in use, `unless-stopped` (45 occurrences) and `'no'` (13 occurrences,
> 19 of the 47 variants declaring at least one `restart:` key). Corrected
> 2026-08-18: the file count previously read 39. Both occurrence counts, 45 and
> 13, reproduce exactly; only the file count was wrong. The scan glob must
> include the single `docker-compose.cluster.yaml`, because a `*.yml` pattern
> silently drops it and undercounts the variant set as 46.
> Cross-referencing the `'no'` occurrences against
> `extends:` blocks shows they concentrate in services extending
> `template-job-low`/`template-job-med` — for example `ksqldb-cli` at
> `infra/04-data/analytics/ksql/docker-compose.yml`, `valkey-cluster-init` at
> `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`, and
> `minio-create-buckets` at `infra/04-data/lake-and-object/minio/docker-compose.yml`.
> [`infra/common-optimizations.exceptions.json`](../../../../infra/common-optimizations.exceptions.json)
> registers this exactly: `template-job-low` and `template-job-med` both carry a
> `restart`/`'no'` `template_exceptions` entry reasoned "One-shot initialization
> and migration jobs," and the same file separately registers a `healthcheck`
> exception for `template-dev-tiny`/`template-dev-small` ("Developer bootstrap
> preset") and `quickwin_baseline.healthcheck_exceptions` for two named one-shot
> services (`pg-cluster-init`, `valkey-cluster-init`). No tracked Compose entry
> uses `restart: always` or `restart: on-failure`; the fleet standardizes on
> `unless-stopped` for long-running services and `'no'` for jobs, with the
> exception registry accounting for every `'no'` case this re-scan found.
>
### Include and extends are two distinct composition mechanisms
>
> Historical evidence (not current authority; source: Git history):
>
> The root `docker-compose.yml` uses the top-level `include` element (17 active
> entries) to assemble independent Compose applications into one model; 164 of
> 168 service entries separately use the service-level `extends` field to
> inherit fields from `infra/common-optimizations.yml`. These are different
> Compose Specification mechanisms with different resolution rules, and
> conflating them understates risk in two directions.
>
> Per the official `include` reference (`docs.docker.com/reference/compose-file/include/`,
> retrieved 2026-08-14): each included path loads as its own Compose application
> model with its own project directory, so **relative paths inside an included
> file resolve against that file's own directory, not the root project's
> directory**; the short syntax (a bare path list, as this repository uses)
> takes the included file's parent folder as its project directory; the local
> (root) project's environment values take precedence over an included file's
> own environment; and Compose detects — but does not silently merge — resource
> name conflicts between the root and an included file. None of this changes
> the 17/60 root-active topology already measured, but it means a future
> `include` addition must be checked for name collisions and its own relative
> path base, not just for the resulting service count.
>
> `extends` is unrelated: it is a service-to-service field merge scoped to one
> file reference (here, always `../../../common-optimizations.yml` or an
> equivalent relative path), and it is why 164 entries share `no-new-privileges`,
> `cap_drop`, and other template defaults through one shared file. The official
> Compose file reference documents `extends` as a separate top-level/service
> concept from `include`; this repository's heavy reliance on `extends` (a
> 164-entry transitive surface, unchanged from the prior measurement) is a
> template-inheritance risk, while `include` is a topology-assembly risk. Both
> require review, but a change to one does not imply a change to the other.
>
> The upstream Compose Specification repository (`compose-spec/compose-spec`)
> carries no tagged releases as of 2026-08-14 (`git ls-remote --tags` returns no
> matches); its `HEAD` resolves to commit `11296e387ba76c77db1db768b9153a4304a3c9bd`.
> Citations to "the Compose Specification" in this leaf mean the specification
> as published on `docs.docker.com/reference/compose-file/` and as of that exact
> upstream commit, not a fixed numbered release — the ecosystem's version signal
> is the Docker Engine/Compose CLI release, not a spec version tag.
>
### Compose validator mechanism and today's re-execution
>
> Historical evidence (not current authority; source: Git history):
>
> [`scripts/validation/validate-docker-compose.sh`](../../../../scripts/validation/validate-docker-compose.sh)
> (244 lines) has two modes, both read directly rather than inferred from prior
> documentation:
>
> - **Default mode** (CI-safe): if `.env` is absent it copies `.env.example` to
>   `.env` and marks it for cleanup; it materializes any Compose-declared secret
>   file that does not already exist as a one-line `dummy` placeholder file
>   (also cleaned up on exit via a `trap`); it resolves
>   `HYHOME_COMPOSE_PROFILES` (default `core`) into `--profile` arguments; then
>   it runs `docker compose <profiles> config >/dev/null` — an actual Docker
>   Compose merge/render, not a text parse — and fails if that render errors or
>   if `docker compose <profiles> config --services` resolves to zero services.
> - **`--preflight` mode**: read-only, creates nothing. It requires a real
>   `.env` and the two Patroni secret files and the three TLS cert files to
>   already exist as files (paths/existence only, values never read); it checks
>   every Compose-declared secret file for existence, treating eight named
>   optional-stack secrets as warnings rather than failures; it checks four
>   `DEFAULT_*_DIR` host bind-mount directories for existence and writability;
>   and it checks whether the `project_net` and `kind` external Docker networks
>   exist, as warnings only.
>
> Both modes were executed directly today at HEAD `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`
> (2026-08-14), upgrading this leaf's own evidence past the "Not Run by explicit
> boundary" state recorded at Task 8:
>
> - Default mode: `Docker Compose validation passed. services_total=5` (exit 0).
>   This is a genuine Docker Compose engine render (Docker 29.7.2 / Compose
>   v5.4.0 confirmed present) of the `core` profile against the 17 root-active
>   includes, not a static text scan. It proves the rendered `core`-profile
>   configuration is structurally valid Compose YAML today. It does not start a
>   container, attach a network, or prove any of the other 24 profiles render
>   cleanly.
> - `--preflight` mode: exited after four `FAIL` lines — the four
>   `DEFAULT_*_DIR` bind-mount directories (`volumes/auth`, `volumes/data`,
>   `volumes/message_broker`, `volumes/obs`) do not exist under this workspace
>   root, only their parent `volumes/` does — plus two `WARN` lines for the
>   `project_net` and `kind` external networks, neither of which exists. All
>   tracked secret files and the three cert files were confirmed present as
>   files (existence only; no content read). This is direct, first-party
>   evidence that **this workspace, as checked out, cannot pass its own
>   operator preflight**: the bind-mount directory tree and the two external
>   networks a full boot depends on are not provisioned here.
>
> Neither run started, attached, or destroyed a container, network, or volume.
> The default-mode run creates and removes only `.env`/dummy-secret files it
> owns; `git status` was confirmed clean before and after. This remains
> config-render evidence, one rung below "Runtime or remote" on the evidence
> ladder below — it is stronger than a text-based YAML read, but it is not
> proof that any container starts, listens, or stays healthy.
>
### Gateway latency SLO and observability
>
> Historical evidence (not current authority; source: Git history):
>
> The infra scope states gateway `LATENCY_SLO < 200ms`. An exact tracked search
> found the threshold only in that governance scope and its subagent preamble;
> no infra, script, or workflow owner measures or gates the threshold. Existing
> metrics, dashboards, and general latency queries do not establish this exact
> SLO, an observation window, a percentile, an error budget, or current
> compliance.
>
> Adoption requires a Stage 03 definition of request population, percentile,
> window, exclusions, data source, alert/error budget, and owner, followed by
> runtime evidence in Stage 05. Until then the SLO is a policy target with a
> Missing measured implementation, not a performance claim.
>
### Validation and operations evidence ladder
>
> Historical evidence (not current authority; source: Git history):
>
> | Evidence layer               | State at 2026-08-14                                                                                                                       | Limit                                                                                                                                        |
> | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
> | Tracked definitions          | Verified at HEAD `ece3eda9`; no infra change since `910ce5f`                                                                              | Variants and profiles are not resolved runtime.                                                                                              |
> | Generated coverage           | `--check` PASS; dry-run re-executed today, counts unchanged                                                                               | Inventory only.                                                                                                                              |
> | Generated image provenance   | `--check` PASS; dry-run re-executed today                                                                                                 | Declaration parity only.                                                                                                                     |
> | Hardening                    | Eleven-tier script PASS (re-executed today)                                                                                               | Selected static assertions only.                                                                                                             |
> | Compose render/preflight     | **Executed today**: default mode PASS (`services_total=5`); `--preflight` FAILED (4 missing bind-mount dirs, 2 missing external networks) | Real Docker Compose render of the `core` profile; proves config validity and exposes unmet host prerequisites, not container runtime health. |
> | Runtime health/network/ports | `UNVERIFIED`                                                                                                                              | No `docker compose up`, container, or network was created.                                                                                   |
> | Backup/restore/SLO/rollback  | `UNVERIFIED`                                                                                                                              | No operator exercise or telemetry observed.                                                                                                  |
>
### Operational concerns Compose does not solve, and their ownership
>
> Historical evidence (not current authority; source: Git history):
>
> Compose (root or infra-level) declares desired state; it does not itself
> supply backup, restore, secret delivery, port ownership, upgrade/rollback, or
> observability behavior. Re-deriving ownership for each of the seven
> operational concerns named in this leaf's charter against tracked repository
> surfaces:
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Concern                  | What Compose supplies                                                                                                             | Tracked owner today                                                                                                                                                                                   | Verdict                                                                                                                                                          |
> | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | Backup                   | Nothing; a volume mount is not a backup mechanism                                                                                 | No tracked backup label, script, or schedule was found for any of the 102 top-level volume declarations                                                                                               | **No tracked owner.** Named gap below.                                                                                                                           |
> | Restore                  | Nothing                                                                                                                           | No tracked restore script or rehearsal evidence was found                                                                                                                                             | **No tracked owner.** Named gap below.                                                                                                                           |
> | Secret delivery          | File-based `secrets:` mount from `./secrets/**` (70 root identifiers); Compose resolves the mapping, not rotation or distribution | `docs/00.agent-governance/rules/approval-boundaries.md` governs _changes_ to secret mappings (values read-forbidden); `.gitignore` excludes `secrets/**/*.txt` and cert material from version control | **Owned for mapping/ignore hygiene; rotation and out-of-band distribution have no tracked owner.**                                                               |
> | Port ownership           | `ports:` mapping only; no binding-policy enforcement                                                                              | `infra` scope states a gateway-only/localhost review rule; no exception registry enforces it                                                                                                          | **Policy stated, not enforced** — 37 non-gateway port-bearing entries remain unresolved against that policy.                                                     |
> | Upgrade and rollback     | `image:` tag pin only; Compose has no built-in rolling-upgrade or version-history mechanism                                       | `approval-boundaries.md` names `git revert` as the rollback route for Compose file changes                                                                                                            | **Config rollback is owned; data/runtime rollback (migrations, volume state, external state) is explicitly out of that route's reach and has no tracked owner.** |
> | Observability            | None; `06-observability` is an included stack (Grafana/Prometheus/Loki/Tempo per `infra/README.md`), not a Compose primitive      | The observability stack is root-active by default (`infra/06-observability/docker-compose.dev.yml`); no tracked dashboard/alert coverage inventory was found for this leaf's re-survey                | **Stack is provisioned; coverage/alerting completeness is `UNVERIFIED`.**                                                                                        |
> | Service level objectives | None                                                                                                                              | Only the gateway `LATENCY_SLO < 200ms` target exists, in `docs/00.agent-governance/scopes/infra.md` policy text only                                                                                  | **No measurement owner; see the SLO subsection above.**                                                                                                          |
>
> Backup and restore are the sharpest gaps: Compose's `volumes:` key persists
> data to a named volume or bind path, but persistence is not backup. No
> tracked script under `scripts/`, no cron/systemd unit, and no Compose service
> in the 168-row inventory performs or schedules a backup of any of the 102
> top-level volume declarations. The canonical closing evidence is a
> per-dataset inventory (persistence class, owner, schedule, retention,
> recovery objective, latest successful backup, restore-rehearsal result) —
> this leaf can name the absence but cannot supply that inventory itself.
>
### Current gaps and ownership
>
> Historical evidence (not current authority; source: Git history):
>
> | Gap                                         | State                                                                                                          | Canonical owner / next evidence                                                                               |
> | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
> | Infra README file count                     | Tracked drift                                                                                                  | Infra documentation owner; correct in a separate approved docs task.                                          |
> | Non-gateway published ports without host IP | 37 unresolved declarations                                                                                     | `infra-implementer` plus security/entry review; classify exception or remediate in approved service tasks.    |
> | Backup labels/evidence                      | 0 labels across 102 declarations; runtime unknown                                                              | Infra/ops owners; per-dataset backup and restore evidence.                                                    |
> | Restore rehearsal evidence                  | None found                                                                                                     | Infra/ops owners; a documented, exercised restore procedure per dataset.                                      |
> | Fleet-wide resource limits (CPU/memory)     | 2/47 files declare `deploy.resources`; no exception registry covers the remaining 166 entries                  | `infra-implementer`; either a resource-governance Spec or a registered rationale for leaving it host-default. |
> | Exact latency SLO implementation            | Missing                                                                                                        | Architecture/infra/ops Spec defining measurement and error-budget contract.                                   |
> | Runtime prerequisites and recovery          | Partially `UNVERIFIED` — preflight now proves the bind-mount/network prerequisites are unmet in this workspace | Operator-approved directory/network provisioning, then health, dependency, and recovery procedure evidence.   |
>
### Carried source-evidence claims
>
> Historical evidence (not current authority; source: Git history):
>
> Source-evidence claims carried forward from the superseded 2026-07-05
> research pack on 2026-08-19. Each states what the upstream evidence supports
> and, where it matters more, what it does not.
>
> - **Rendering a resolved configuration is not a confinement boundary.** The vendor trust-model page names the inheritance directive alongside includes as a transitive-privilege path, states that rendering a resolved configuration offers no confinement guarantee, and warns that file-reference fields surface file contents in that output before any container starts. Resolved-config review must not be treated as a safety guarantee, which matters directly against this workspace's large inheritance surface. **Source named 2026-08-19** after a seat found the page registered in the retiring leaf but nowhere in this one, leaving the rule unrecoverable after deletion: the page is `https://docs.docker.com/compose/trust-model/`, and the mechanisms it names are `extends`, `include`, and the resolved output of `docker compose config`.
>
### Investigation sequence
>
> Historical evidence (not current authority; source: Git history):
>
> First identify the root or child Compose file and the named service, network,
> volume, secret reference, or include edge. Then inspect its tracked consumers
> and any declared dependency relationship without reading a secret value or
> resolving environment interpolation. Record the literal revision, the intended
> adoption condition, and the smallest non-runtime static check that can support
> the proposal. Runtime evidence, if later authorized, must separately identify
> the target, execution authority, timestamp, and observed result.
>
> The retained inventory does not independently support claims about profiles,
> `depends_on`, health checks, or secrets beyond the local definitions that a
> tracked file declares. In particular, a secret-file reference is not evidence
> that a secret exists, was mounted, or was withheld from logs.
>
### Infrastructure change surfaces
>
> Historical evidence (not current authority; source: Git history):
>
> | Subitem | Supported mechanism or local fact | Exact local investigation target | Adoption condition | Verification limit |
> | --- | --- | --- | --- | --- |
> | Include | Retained documentation says an included project has its own relative-path base and project directory; conflicts are detected rather than silently merged. | `docker-compose.yml` `include:` entry and the included `docker-compose*.yml` file | Name the include edge, consumer, relative-path base, and collision review. | No resolved model, conflict result, or execution was observed. |
> | Extends | Retained analysis distinguishes service-level `extends` from `include`; it is a template-inheritance rather than application-assembly concern. | service `extends:` block and referenced `infra/common-optimizations.yml` entry | Review inherited fields and the exact override before adopting a template change. | The retained external inventory does not independently establish every field-merge outcome. |
> | Profiles / dependencies / health / secrets | Local files may declare these fields or references, but their external semantics are not independently located in the retained inventory. | relevant `infra/**/docker-compose*.yml` service block | Obtain source-bound semantics and a target-specific plan before relying on behavior. | This leaf records no profile selection, dependency ordering, health result, secret value, mount, or redaction evidence. |
> | Networks and storage | Root configuration declares network and secret-reference surfaces; child files may declare service attachments and volumes. | `docker-compose.yml`, relevant `infra/**/docker-compose*.yml`, and `infra/**/README.md` | Identify consumers, data boundary, retention, and ownership before changing a shared resource. | Declarations do not prove connectivity, persistence, encryption, or data recovery. |
> | Backup / recovery | Recovery must be separately specified for a named persistent target. | affected service Compose file and its adjacent `README.md` | Require an owner-approved backup, restore, and rollback plan before operational adoption. | No backup, restore, or failure exercise was performed or inferred. |
> | IaC change control | A Compose edit is a tracked configuration change requiring reviewed scope and evidence. | changed Compose path, Task 0004, and relevant owner document | Bind change, reviewer, target, and rollback criteria before any execution authority. | Version control and review records do not prove deployed state. |
>

### Scope Implications
>
> Historical evidence (not current authority; source: Git history):
>
> | Scope          | Infrastructure implication                                                                                                                                   |
> | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
> | `agentic`      | Agents may inventory and validate within approval bounds; they must not turn Compose definitions or a validator pass into runtime claims.                    |
> | `architecture` | Own intended single-host/variant topology, trust boundaries, data durability, SLO semantics, and any production/deployment contract.                         |
> | `backend`      | No backend application surface is established; a future service must declare network, port, dependency, secret, persistence, health, and recovery contracts. |
> | `common`       | Shared templates are a 164-entry transitive surface; common changes need blast-radius evidence and exception compatibility.                                  |
> | `docs`         | Keep variant inventory distinct from root topology, repair the one-file README drift separately, and route procedures to Stage 05.                           |
> | `entry`        | Review all 37 non-gateway port-bearing services, gateway routing, TLS/auth, localhost binding, and explicit exceptions.                                      |
> | `frontend`     | No product frontend topology is established; future UI exposure belongs behind the entry contract with tested health and rollback.                           |
> | `infra`        | Own Compose, templates, registries, exceptions, validation, backup labels, and runtime-approved change/recovery evidence.                                    |
> | `meta`         | Generated census and provenance metadata need byte-exact freshness and must retain their inventory/runtime exclusions.                                       |
> | `mobile`       | No mobile runtime surface is present; any future local dependency needs a documented gateway/API boundary rather than direct database exposure.              |
> | `ops`          | Own live prerequisites, health, telemetry, backup/restore, incident response, rollout, and rollback evidence; static checks are insufficient.                |
> | `product`      | Define critical service journeys and acceptable availability/latency before an infrastructure SLO or production-readiness claim.                             |
> | `qa`           | Keep file/profile/variant coverage, render validation, hardening, runtime health, recovery, and SLO verification as separate gates.                          |
> | `security`     | Review transitive Compose trust, privileges, published ports, external networks, secret grants, images, and registered exceptions without reading values.    |
>

### Scope Application
>
> Historical evidence (not current authority; source: Git history):
>
> | Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
> | --- | --- | --- | --- | --- |
> | agentic | applies | An agent-proposed Compose edit names one file and one owner-approved task. | Inspect task scope and changed declaration. | A task does not authorize runtime execution. |
> | architecture | applies | A system boundary change identifies service, network, data, and recovery effects. | Inspect tracked design and Compose edge. | Static topology is not a deployed architecture. |
> | common | applies | Shared networks or reusable fragments have a named consumer and collision review. | Inspect root and referenced Compose files. | Inclusion does not prove compatible execution. |
> | docs | applies | Document the literal revision, source state, and non-runtime limit. | Inspect source and claim rows. | Documentation is not operational evidence. |
> | infra | applies | The proposed field has a target-specific configuration and source-bound semantic basis. | Inspect the exact `docker-compose*.yml` definition. | Profiles, dependency, health, and secret behavior remain UNVERIFIED here. |
> | ops | applies | A runtime change has a separately approved operator, rollback, and observation plan. | Inspect approved runbook and event evidence. | No runtime plan or observation is supplied. |
> | qa | applies | A static composition check is selected before a future runtime check. | Record the exact check and target. | No Docker command was run by this leaf. |
> | security | applies | Secret references and exposure paths are reviewed without accessing secret values. | Inspect only declaration paths and ownership. | A reference does not prove secure storage, injection, or redaction. |
>

### 2026-09-05 Revalidation
>
> Historical evidence (not current authority; source: Git history):
>
> Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
> The clean full gate rendered all 28 declared profile selections and reported
> 232 selected-service instances in aggregate. DATA-0059 owns the service/profile
> inventory; AUD-0097 separately preserves four domain defects that static
> rendering does not expose.
>
> | Capability | Repository implementation | Evidence depth | Gap | Verification route |
> | --- | --- | --- | --- | --- |
> | Profiles and service boundaries | Root includes service-local Compose files; POL-0078 owns vocabulary | Configured, Repository-enforced | Four domain defects remain | all-profile render plus AUD-0097 owner actions |
> | Network/volume/secret/healthcheck | Declarations and security baselines are tracked | Configured, Repository-enforced | Live connectivity, persistence, and secret delivery unverified | isolated runtime rehearsal without value capture |
> | Runtime/deployment | SPEC-0172 observed Docker reachability but no repository deployment | Unverified for this stack | No exact live target | approved target, health, recovery, rollback evidence |
>
> Recommendation: do not convert a successful `docker compose config` into an
> operational-readiness claim. Route AUD-0097 defects through their service-domain
> owners. Official basis: [Compose services](https://docs.docker.com/reference/compose-file/services/),
> [profiles](https://docs.docker.com/compose/how-tos/profiles/), and
> [secrets](https://docs.docker.com/reference/compose-file/secrets/).
>

### Maintenance
>
> Historical evidence (not current authority; source: Git history):
>
> Re-run both canonical `--check` and `--dry-run` generators, the exact tracked
> Compose inventory, and the hardening entry point after Compose, templates,
> profiles, registries, exceptions, or relevant Docker guidance changes. Keep
> variant inventory, selected root topology, rendered configuration, runtime
> observation, and operations evidence in separate fields. Owner: Documentation
> maintainers with Infra/DevOps, Entry, Security, and Operations review.
>

### Related Documents

- [Verification and validation](./m0019-verification-validation.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- [Security governance](./m0017-security-governance.md)
- [Automation pipeline and workflow](./m0004-automation-pipeline-workflow.md)
- [Quality, CI, and formatting](./m0014-quality-ci-formatting.md)
- [Data index](../../data/README.md)
- [SPEC-0158 preservation contract](../../../98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)

- [Research pack navigation](README.md)

## Findings

### Historical workspace observations — not reassessed in this run

> Historical evidence (not current authority; source: Git history):
> Current routing (2026-09-06): [canonical agent governance](../../../../.agents/README.md) and
> [ADR-0032](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md) own the active source location.
> Earlier Stage 00 paths, inventories, provider projections, and check results
> below remain dated observations, not current instructions or new runtime
> acceptance evidence. Source links now navigate to current owners; the
> original `observed_at`, `reviewed_at`, status, and measured facts are preserved.
>

## Limitations

### Future Internal Checks

| Topic / claim ID | Analysis scope | Applicability condition | Future surface candidate | Concrete question | Required evidence | Future inspection method | Pass / fail criterion | Additional permission / risk | Expected owner role | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0005-01/02/03 | repository, directory, environment × infrastructure | Composition feature or selector change | Known historical reference: root docker-compose.yml; candidate fixtures not inspected | Do supported features, paths, collisions, profiles and precedence match the intended model? | Exact CLI/Engine/platform and dummy-input expected model | Future scoped synthetic render tests | Pass on exact expected model; fail on ignored attributes/unintended resources | Render can expose values; use dummy inputs; runtime separate | iac-reviewer | Not assessed in this run |
| C-m0005-04 | environment × operations/quality | Startup/recovery change | Candidate isolated workload/probe; not inspected | Does readiness cover the actual consumer workflow and recovery? | Probe contract, controlled failure and user-outcome evidence | Future approved isolated startup/failure rehearsal | Pass within accepted recovery bound; fail if probe passes while workflow fails | Runtime/fault injection need approval | infra-implementer | Not assessed in this run |
| C-m0005-05 | environment × security/data | Exposure or persistence change | Candidate network/storage/grant design; not inspected | Are ingress/peer/grant/persistence boundaries enforced? | Sanitized model and isolated reachability/state evidence | Future narrowly authorized review/rehearsal | Pass authorized access and expected persistence only; fail unintended access/grants | Host/network tests and confidential metadata require scope | security-auditor | Not assessed in this run |
| C-m0005-06 | environment × capacity/operations | Resource/lifecycle change | Candidate isolated target; not inspected | Are limits enforced and writes cleanly drained? | Runtime/controller record and integrity after bounded stop | Future approved bounded resource/termination test | Pass agreed ceiling/drain criteria; fail missing enforcement/lost writes | Load/stop affect data; isolate and approve | infra-implementer | Not assessed in this run |
| C-m0005-07 | tool, CI × supply chain | Image promotion | Candidate digest/attestation; not fetched | Can artifact identity bind to approved builder/source/platform? | Digest, provenance subject, trust and residual-risk decision | Future security-owned provenance verification | Pass matching subject/trust; fail mismatch/unverifiable origin | Registry access/paid tools separately scoped | security-auditor | Not assessed in this run |
| C-m0005-08 | environment × ingress/operations | DNS/TLS change | Candidate test-domain/ingress runbook; not inspected | Can hostname, renewal and key/dependency recovery meet the intended contract? | Sanitized DNS/certificate/renewal/recovery evidence | Future approved isolated ingress rehearsal | Pass intended trust and recovery; fail wrong identity or unrecoverable key | DNS changes/issuance/key custody need approval | incident-responder | Not assessed in this run |
| C-m0005-09 | environment × data/operations | Durable data before migration/removal | Candidate backup and empty isolated target; not inspected | Does restoration recover consistent data and workflow within RPO/RTO? | Backup timestamp/checksum, engine version, isolation proof, invariants, last recoverable transaction, duration and owner acceptance | Future separately approved isolated restore; no production overwrite | Pass integrity and agreed loss/time/user outcome; fail missing keys/corruption/exceeded objective | Protected backup access and restoration writes need scoped approval | infra-implementer | Not assessed in this run |
| C-m0005-09/10 | Spec/task, environment × operations/quality | Upgrade acceptance | Candidate update/acceptance packet; not inspected | Does evidence separate each layer and name irreversible migrations? | Version-bound parser/runtime/probe/workflow/recovery results | Future packet review and isolated rollback rehearsal | Pass all required layers plus safe rollback; fail static-pass-only acceptance | Update/cutover/data actions remain future approval | iac-reviewer | Not assessed in this run |

### Limits and recheck conditions

No infrastructure configuration, service inventory, runtime, secrets, backup or
account was inspected. Source pages are mutable; feature minima are not a complete
compatibility matrix. Upstream specification main was opened without a revision
pin. Recheck on CLI/Engine/platform, source or data-schema changes and before
adoption. Historical measurements below are not new acceptance evidence.

## Sources

### Claims and Sources

| Claim ID | Claim | Source ID / detailed section | Published / modified | Actually checked | Product / version / channel | Fact / interpretation / recommendation | Limits, conflicts and recheck trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0005-01 | Implementation support differs; version does not pin schema. | S-docker-compose-spec, optional attributes; S-docker-compose-version-name; S-docker-compose-release | Not stated; tagged release date not extracted | 2026-09-27 | Compose Specification / CLI v5.5.1 release | Fact | No local version measured; recheck target CLI/platform. |
| C-m0005-02 | Include/merge/extends/profile semantics differ. | S-docker-compose-include; S-docker-compose-merge, exceptions; S-docker-compose-extends, paths; S-docker-compose-profiles, target | Not stated | 2026-09-27 | include 2.20.0+; !override 2.24.4+ | Fact | Extends path wording is context-dependent; test selected model later. |
| C-m0005-03 | Interpolation/container environment/project naming have different precedence. | S-docker-compose-interpolation; S-docker-compose-env-precedence; S-docker-compose-project-name | Not stated | 2026-09-27 | Current Compose CLI docs | Fact | Synthetic inputs only; no private .env opened. |
| C-m0005-04 | Startup, readiness and runtime recovery differ. | S-docker-compose-services, depends_on/healthcheck; S-docker-compose-startup; S-docker-container-restart | Not stated | 2026-09-27 | depends_on.restart 2.17.0+; required 2.20.0+ | Fact / interpretation | Probe quality remains target-specific. |
| C-m0005-05 | Network/ports/storage/configs/secrets have distinct trust/lifecycle. | S-docker-compose-networks; S-docker-port-publishing; S-docker-compose-volumes; S-docker-compose-configs; S-docker-compose-secrets; S-docker-compose-use-secrets | Not stated | 2026-09-27 | Config content/environment 2.23.1+; localhost caveat pre-Engine 28 | Fact / interpretation | No exposure, encryption or grant enforcement assessed. |
| C-m0005-06 | Capacity and shutdown/restart need runtime/application evidence. | S-docker-resource-constraints; S-docker-compose-deploy; S-docker-container-stop; S-docker-compose-services, stop_grace_period | Not stated | 2026-09-27 | Linux Engine / optional deploy support | Interpretation | No resource enforcement, utilization or data integrity measured. |
| C-m0005-07 | Pin identity and provenance answer different questions. | S-docker-image-pinning; S-docker-build-provenance, mode/version | Not stated | 2026-09-27 | BuildKit schema v0.2 default; v1 optional | Fact / interpretation | No digest/signature/scan verified. |
| C-m0005-08 | TLS/DNS/ACME need distinct operating contracts. | S-rfc-tls-9846, 1.2; S-rfc-acme-8555, 8; S-rfc-dns-1034, 3.6 | 2026-07; 2019-03; 1987-11 | 2026-09-27 | Standards Track originals | Fact / recommendation | Later RFC updates/errata and target behavior need recheck. |
| C-m0005-09 | Backup/restoration and static/process/readiness/user evidence must remain distinct. | S-docker-volume-recovery; S-nist-contingency-800-34, 3.2/3.5/4.4; S-docker-compose-config; S-google-sre-monitoring | NIST May 2010, updated 2010-11-11; others not stated | 2026-09-27 | Corrected final SP 800-34 Rev.1 / CLI/SRE | Interpretation / recommendation | No backup/restore/runtime observed; federal guidance used proportionately. |
| C-m0005-10 | Updates need application-aware rollback and optional scope. | S-docker-compose-production, updates; C-m0021-03 | Not stated | 2026-09-27 | Single-server Compose operations | Recommendation | No new service decision, update or migration executed. |

| Source ID | Original actually opened and detailed section | Publication / revision / status | Checked |
| --- | --- | --- | --- |
| S-docker-compose-spec | [Specification: optional attributes](https://github.com/compose-spec/compose-spec/blob/main/spec.md#requirements-and-optional-attributes) | Mutable main; specification, no commit pin obtained | 2026-09-27 |
| S-docker-compose-release | [Compose v5.5.1 release](https://github.com/docker/compose/releases/tag/v5.5.1) | Official tagged release; timestamp not reliably extracted | 2026-09-27 |
| S-docker-compose-version-name | [Obsolete version field](https://docs.docker.com/reference/compose-file/version-and-name/) | Mutable official reference; publication date not stated | 2026-09-27 |
| S-docker-compose-include | [Include: short/long syntax](https://docs.docker.com/reference/compose-file/include/) | Requires Compose 2.20.0+; mutable reference | 2026-09-27 |
| S-docker-compose-merge | [Merge: exceptions/reset/replace](https://docs.docker.com/reference/compose-file/merge/) | !override requires 2.24.4+; mutable reference | 2026-09-27 |
| S-docker-compose-extends | [Extends: relative paths](https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/) | Mutable reference; stack deploy differs | 2026-09-27 |
| S-docker-compose-profiles | [Profiles: target/dependencies](https://docs.docker.com/compose/how-tos/profiles/#auto-starting-profiles-and-dependency-resolution) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-compose-interpolation | [Interpolation: source precedence](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#ways-to-set-variables-with-interpolation) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-compose-env-precedence | [Container environment precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-compose-project-name | [Project naming precedence](https://docs.docker.com/compose/how-tos/project-name/#set-a-project-name) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-compose-services | [Services: dependencies/health/resources/stop](https://docs.docker.com/reference/compose-file/services/) | depends_on.restart 2.17.0+, required 2.20.0+; mutable reference | 2026-09-27 |
| S-docker-compose-startup | [Startup and shutdown order](https://docs.docker.com/compose/how-tos/startup-order/) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-compose-networks | [Networks: internal/external](https://docs.docker.com/reference/compose-file/networks/) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-port-publishing | [Host port binding and localhost caveat](https://docs.docker.com/engine/network/port-publishing/) | Mutable Engine reference; localhost caveat before Engine 28.0.0 | 2026-09-27 |
| S-docker-compose-volumes | [Volume definitions/lifecycle](https://docs.docker.com/reference/compose-file/volumes/) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-compose-configs | [Config file/content/environment](https://docs.docker.com/reference/compose-file/configs/) | content/environment sources introduced in 2.23.1 | 2026-09-27 |
| S-docker-compose-secrets | [Secret source and grants](https://docs.docker.com/reference/compose-file/secrets/) | Mutable reference; environment source not supported by stack deploy | 2026-09-27 |
| S-docker-compose-use-secrets | [Per-service secret grants/mounts](https://docs.docker.com/compose/how-tos/use-secrets/) | Mutable reference; publication date not stated | 2026-09-27 |
| S-docker-compose-deploy | [Deploy: resource/restart policy](https://docs.docker.com/reference/compose-file/deploy/) | Optional implementation aspect; mutable reference | 2026-09-27 |
| S-docker-resource-constraints | [Linux resource constraints](https://docs.docker.com/engine/containers/resource_constraints/) | Mutable Engine reference; runtime/platform support matters | 2026-09-27 |
| S-docker-container-restart | [Container restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/) | Mutable Engine reference; publication date not stated | 2026-09-27 |
| S-docker-container-stop | [Stop signals/timeouts](https://docs.docker.com/reference/cli/docker/container/stop/) | Mutable Engine CLI reference; publication date not stated | 2026-09-27 |
| S-docker-compose-config | [Compose config model/options](https://docs.docker.com/reference/cli/docker/compose/config/) | Mutable CLI reference; publication date not stated | 2026-09-27 |
| S-docker-image-pinning | [Build guidance: pin image versions](https://docs.docker.com/build/building/best-practices/#pin-base-image-versions) | Mutable guidance; old develop URL redirects here | 2026-09-27 |
| S-docker-build-provenance | [Provenance: mode/version](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) | BuildKit mode=min and schema v0.2 defaults; v1 optional | 2026-09-27 |
| S-docker-volume-recovery | [Volume backup/restore mechanics](https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes) | Mutable generic tar example; not database consistency proof | 2026-09-27 |
| S-nist-contingency-800-34 | [NIST contingency: 3.2/3.5/4.4](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf) | Final May 2010, updated 2010-11-11; corrected edition confirmed via /r1/upd1/final | 2026-09-27 |
| S-google-sre-monitoring | [SRE: signals and black/white-box monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) | Published book chapter; page revision date not stated; experiential guidance | 2026-09-27 |
| S-rfc-tls-9846 | [TLS 1.3: relationship to RFC 8446](https://www.rfc-editor.org/rfc/rfc9846.html#section-1.2) | July 2026; Proposed Standard / Standards Track; obsoletes RFC 8446 | 2026-09-27 |
| S-rfc-acme-8555 | [ACME: section 8 challenges](https://www.rfc-editor.org/rfc/rfc8555.html#section-8) | March 2019; Standards Track; later updates/errata possible | 2026-09-27 |
| S-rfc-dns-1034 | [DNS: section 3.6 resource records](https://www.rfc-editor.org/rfc/rfc1034.html#section-3.6) | November 1987; foundational DNS RFC with later updates | 2026-09-27 |
| S-docker-compose-production | [Single-server updates](https://docs.docker.com/compose/how-tos/production/) | Mutable guidance; old /compose/production URL redirects here | 2026-09-27 |

>
> Historical evidence (not current authority; source: Git history):
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Source                                                                                                                                          | Accessed                  | Class                             | Verification state                                                                                                                                                                                                                                                                        |
> | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)                                                                | 2026-08-08T18:18:06+09:00 | External mutable                  | Verified official page; Compose application-model capability only.                                                                                                                                                                                                                        |
> | [Root Compose](../../../../docker-compose.yml)                                                                                                  | 2026-08-08                | Workspace tracked at `910ce5f`    | Root name, four networks, 70 secret IDs, and 17 active includes read without values.                                                                                                                                                                                                      |
> | Generated Compose coverage                                                             | 2026-08-08                | Workspace generated/tracked       | `--check` PASS and `--dry-run` verified 48/47/168/25 counts; not runtime evidence.                                                                                                                                                                                                        |
> | `generate-compose-profile-service-coverage.sh`                                               | 2026-08-08                | Workspace tracked                 | Candidate/parse rules read directly.                                                                                                                                                                                                                                                      |
> | [Infra README](../../../../infra/README.md)                                                                                                     | 2026-08-08                | Workspace tracked                 | Root-active and directory claims checked; infra variant count is one high.                                                                                                                                                                                                                |
> | Infrastructure scope (retired path: `../../../00.agent-governance/scopes/infra.md`)                                                                            | 2026-08-08                | Workspace tracked policy          | Gateway, network, volume, hardening, secret, backup, SLO, and approval requirements.                                                                                                                                                                                                      |
> | [Shared template library](../../../../infra/common-optimizations.yml) and [exceptions](../../../../infra/common-optimizations.exceptions.json)  | 2026-08-08                | Workspace tracked                 | Control inheritance and registered exception semantics.                                                                                                                                                                                                                                   |
> | [Hardening entry point](../../../../scripts/hardening/check-all-hardening.sh)                                                                   | 2026-08-08                | Workspace tracked/executed        | Eleven tier checks passed; static selected-control evidence only.                                                                                                                                                                                                                         |
> | [Tech-stack registry](../../../../infra/tech-stack.versions.json) and [floating exceptions](../../../../infra/image-tag-policy.exceptions.json) | 2026-08-08                | Workspace tracked                 | 18 components, 21 curated images, and exception ownership.                                                                                                                                                                                                                                |
> | Tech-stack provenance                                                                     | 2026-08-08                | Workspace generated/tracked       | `--check` PASS; dry-run reports 20 pinned and one approved floating row.                                                                                                                                                                                                                  |
> | [Approval boundaries](../../../../.agents/governance/approval-boundaries.md)                                                                | 2026-08-08                | Workspace tracked policy          | Compose, secret, runtime, validation, rollback, and hard-stop boundaries.                                                                                                                                                                                                                 |
> | Graphify report (`graphify-out/GRAPH_REPORT.md`, untracked local output since 2026-09-08)                                                                                     | 2026-08-08                | Workspace tracked stale/advisory  | Built from `f8a72211`; navigation clues were corroborated and not used as proof.                                                                                                                                                                                                          |
> | [Compose `include` reference](https://docs.docker.com/reference/compose-file/include/)                                                          | 2026-08-14                | External mutable                  | Verified official page; relative-path, project-directory, env-precedence, and conflict-detection rules for `include` confirmed distinct from `extends`.                                                                                                                                   |
> | [compose-spec repository](https://github.com/compose-spec/compose-spec) at `11296e387ba76c77db1db768b9153a4304a3c9bd`                           | 2026-08-14                | External fixed at pinned revision | `git ls-remote --tags` returns no tags (no numbered releases exist); `HEAD` resolved and used as the exact upstream reference instead of mutable `main`.                                                                                                                                  |
> | [Compose validator](../../../../scripts/validation/validate-docker-compose.sh)                                                                  | 2026-08-14                | Workspace tracked/executed        | Read in full (244 lines) and executed in both default and `--preflight` modes at HEAD `ece3eda9`; default mode PASS (`services_total=5`), preflight FAILED on 4 missing bind-mount dirs and 2 missing external networks. No secret value read; `git status` confirmed clean before/after. |
> | [Image-tag floating exceptions](../../../../infra/image-tag-policy.exceptions.json)                                                             | 2026-08-14                | Workspace tracked                 | Read in full; confirmed all 4 registered floating images (`nginx:alpine`, `portainer/portainer-ce:sts`, `lfnovo/open_notebook:v1-latest-single`, `b4bz/homer`) carry owner, reason, and monthly cadence.                                                                                  |
> | Direct `rg` re-scan of `infra/**/docker-compose*.yml` for `image:`, `restart:`, `deploy:`, `mem_limit:`, `cpus:`, `healthcheck:`                | 2026-08-14                | Workspace tracked                 | 137 image declarations / 82 distinct, 0 literal `:latest`, 1 untagged (registered); restart values limited to `unless-stopped` (45) and `'no'` (13); only 2 files declare `deploy.resources`.                                                                                             |
>
