---
title: "LAB Promotion Contract Specification"
version: "0.4.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0263"
parent_ids:
- "REQ-0004"
- "AD-0026"
created: "2026-11-05"
---

# LAB Promotion Contract Specification

## Overview

### Intent

A LAB under `labs/` is a service that does not yet run in `infra/`. It is run
there to test it and later move it into `infra/` for continuous operation.
Today every LAB has a different shape, no LAB records where it would go, and
promotion means re-sorting files, documents, secrets and catalog rows by hand.
This Spec defines four things:

- the structure every LAB keeps;
- the three kinds of promotion;
- the check that decides whether a LAB may be promoted;
- the procedure for each kind.

#### Observed state

Observed on 2026-11-05 at `c1db5ef65`:

- **LAB entrypoints are inconsistent.**
  - Each LAB is a flat `labs/<name>.yml`.
  - Some LABs also have an asset folder `labs/<name>/`, some a guide
    `labs/<name>.md`, and some neither.
  - Loose helpers sit at the `labs/` root: `couchdb-cluster-init.sh` and
    `opensearch-cluster-dashboards.config`.
- **Operations documents are uneven.**
  - Thirteen LABs have a Guide and a Runbook under
    `docs/05.operations/{guides,runbooks}/15-labs/`, sharing one number.
  - The Kafka and OpenSearch cluster LABs have only `labs/<name>.md`.
- **infra services follow one pattern.** A service in `infra/` lives in
  `infra/<tier>/<service>/` with its `docker-compose.yml`, `README.md` and
  assets. It is included by the root `docker-compose.yml` and has profiles in
  the POL-0078 vocabulary.
- **Four LABs are cluster forms of HOME single-node services.**
  `valkey-cluster`, `postgresql-ha`, `opensearch-cluster` and `kafka-cluster`.
  The rest are new services.
- **supabase uses HOME resources.**
  - It reads ten secrets from HOME paths under `secrets/data/supabase/` and
    `secrets/db/mng-pg/`, plus HOME's SMTP password.
  - It binds the Docker socket.
  - `scripts/operations/lab.py check` (PR #752) refuses all of these.

### Owning Requirements

The owner stated the following on 2026-11-05:

- **Purpose of a LAB.** LAB services are services not run from `infra/`. They
  exist to test continuous operation before they move into `infra/`.
- **What promotion involves.** It means:
  - wiring the LAB to the services already integrated in `infra/`;
  - moving its scattered files and contents into the `infra/` structure;
  - arranging its documents in `docs/05.operations`;
  - checking that the tier is right and that its configuration fits the
    environment and its purpose.
- **What the fit check covers.** The current service composition, Linux,
  Docker and the current server. Above all: whether the server's CPU, memory
  and disk headroom allow the service to run together with the services
  already running.
- **Three promotion kinds.** Add a new service; replace an existing service
  with another form of the same service, for example a single node with a
  cluster; or replace a service with a different service for the same
  purpose. The two replacement kinds include data migration and consumer
  cutover as a defined procedure.
- **LAB secrets.** A LAB uses its own secret copies under
  `secrets/labs/<name>/`, and promotion moves them to their `infra` location.
- **supabase.** It stays a LAB and is brought into this structure.

The owner answered three open questions on 2026-11-05:

- **Host budget.** The budget is the measured host capacity minus a reserve
  for the OS and Docker. Only running services count, and a replacement
  subtracts the resources of the service it retires.
- **supabase secret copies.** They copy the HOME values. The secrets only
  supabase uses move into the LAB location, `secrets/labs/supabase/`.
- **Docker socket.** supabase's Docker socket bind is allowed by the LAB
  check.

The owner amended the resource rule and the section 5 scope on 2026-11-06,
after the first readiness runs. Those runs showed that HOME's declared limits
already total about 64 CPUs on a 12-CPU host, while the running containers use
about 3 CPUs and 9 GiB:

- **Reservations, not limits.** The resource budget sums declared
  reservations. HOME declares them in the shared resource templates of
  `infra/common-optimizations.yml`, sized from measured usage plus a margin.
- **External containers.** Containers outside the HOME and LAB Compose
  projects, such as k3d, count as a fixed allowance set in the operations
  policy.
- **Owner check items.** Groups and file modes, and profile and consumer
  clashes, are owner check items in each promotion Task, not readiness
  measurements.

The owner removed the supabase LAB on 2026-11-06 (version 0.4.0, work unit
W8). This supersedes the 2026-11-05 supabase statements above: `labs/supabase/`,
its operations documents, catalog rows and Docker socket allowance are gone,
and no LAB binds the Docker socket.

This Spec makes concrete REQ-0004 and AD-0026, its frontmatter `parent_ids`. The body cites no REQ-####-FR or REQ-####-NFR identifier.

## Scope

### In Scope

- The standard LAB layout and the promotion manifest every LAB carries.
- LAB secret copies and their catalog and registry rows.
- The rules that map a LAB's files, documents and secrets to their `infra/`
  and `docs/05.operations` destinations.
- The promotion readiness check and its report.
- Procedures for the three promotion kinds. The two replacement kinds include
  data migration, consumer cutover and rollback.
- Bringing the 15 LABs present on 2026-11-05 into the standard layout, and
  retiring the supabase LAB on 2026-11-06.

### Non-goals

- Promoting any LAB. Each promotion is a later Task under this Spec with its
  own owner approval and operating window.
- Starting, stopping or recreating a container, moving live data, or changing
  OpenBao KV contents.
- Container-escape options that `lab.py` does not check (`devices`,
  `volumes_from`, host `pid` or `network_mode`, `cap_add`). These stay a
  recorded residual risk.

## Behavior Contract

### Normal Behavior

#### 1. Standard LAB layout

Every LAB is one folder, `labs/<name>/`, shaped like an `infra/` service
folder. It contains:

- `docker-compose.yml`, the LAB entrypoint. It replaces the flat
  `labs/<name>.yml` and is the file `lab.py` resolves.
- `README.md`, the service README, following the infra Service Documentation
  Rubric in `infra/README.md`.
- Every build source, mounted configuration file, helper and Grafana
  dashboard the LAB uses. Only `labs/README.md` and the shared
  `labs/.env.example` stay at the `labs/` root.
- `promotion.yaml`, the promotion manifest (section 2).

A LAB keeps its own Compose project `hy-home-lab-<name>`, its LAB networks,
its `LAB_*` endpoint inputs, its data under `LAB_DATA_DIR`, and the isolation
that `lab.py check` enforces.

#### 2. Promotion manifest

`labs/<name>/promotion.yaml` declares where and how the LAB would be promoted:

| Field | Content |
| --- | --- |
| `kind` | `add`, `replace-same`, `replace-substitute`, or `undecided` for a LAB with no promotion target yet; `undecided` has no `target` and the readiness check refuses it |
| `target` | The destination folder `infra/<tier>/<service>/` and the POL-0078 profile the service would join |
| `replaces` | For the two replacement kinds: the HOME services and Compose paths that are retired, and their consumers |
| `integrations` | Each `infra` integration the service needs, with its `infra` owner |
| `secrets` | Each LAB secret copy and its `infra` destination path, by catalog row |
| `documents` | The Guide and Runbook, with their current `15-labs` paths and their target `docs/05.operations` role folders |
| `resources` | The declared CPU and memory of every service, and the disk the service needs for data and images |
| `host` (optional) | Host requirements Compose cannot express: minimum Docker and Compose versions and required kernel features |

The integrations an `integrations` entry can name are a gateway route, an
OIDC client, a database role and its provisioning, observability scrape and
logs, OpenBao secret delivery, and shared networks.

`lab.py check` validates the manifest. It reports a problem for a missing or
inconsistent manifest, including:

- an unknown `kind`;
- a `target` outside `infra/<tier>/`;
- a secret without a catalog row;
- `resources` that disagree with the rendered limits.

#### 3. Secrets

During the LAB phase every secret file is a LAB copy under
`secrets/labs/<name>/`. Each copy has its own catalog row (`LAB-*`, scope
`lab`) and its own placeholder row in the public registry.

A LAB never reads a HOME secret path. A secret HOME also uses, such as SMTP,
is copied into the LAB location with the HOME value. A secret only the LAB
uses moves into the LAB location. The owner copies and moves the files. The
agent changes Compose, catalog rows and tests, and prepares the registry
edits.

No LAB binds the Docker socket. `lab.py check` refuses every socket bind,
read-only or writable.

On promotion:

- LAB secret values are never promoted. The promoted service receives
  `infra` secrets at the destination paths in the manifest. These are new
  values, or for a replacement the existing HOME secrets, rotated under the
  secret policy.
- each LAB copy and its catalog row are retired, and the registry follows;
- each destination gets a new `root` catalog row, or an existing one gains the
  new consumer.

#### 4. Destination rules

| LAB source | Destination on promotion |
| --- | --- |
| `labs/<name>/docker-compose.yml` | `infra/<tier>/<service>/docker-compose.yml`, included by the root, with LAB-only inputs replaced by `infra` integrations |
| `labs/<name>/README.md` | the service README in the destination folder |
| `labs/<name>/` assets | the destination folder, at the same relative paths |
| Guide and Runbook in `15-labs` | the target role folders, keeping their artifact identifiers and creation dates |
| `secrets/labs/<name>/*` | retired; the service uses the `infra` secrets named in the manifest |
| `promotion.yaml` | removed; its facts are recorded in the promotion Task |

The tier follows the function of the service. Operations documents follow the
domain of the service, which need not share the tier number. No LAB copy of a
file, document, secret or catalog row is left behind.

#### 5. Promotion readiness check

Before any promotion, a readiness check produces a report and fails closed.
It covers:

- **Tier fit.** The target tier matches the service function. The target
  folder either does not exist or is a declared replacement.
- **Service composition.** The candidate does not clash with the HOME-selected
  services in names, ports or networks. Each integration it needs exists in
  `infra`. Profile and consumer clashes are owner check items, which the
  promotion Task records.
- **Linux.** The kernel and cgroups support the declared limits and
  reservations, and the users the service runs as are valid. The check
  derives these from the rendered Compose (`user`, limits, reservations) and
  the manifest `host` field. Groups and file modes are owner check items,
  which the promotion Task records.
- **Docker.** The required Docker and Compose versions, the network and volume
  drivers, and the location of Docker's data root are all compatible. The
  requirements come from the same sources.
- **Server resources.** Measured on the HOME host:
  - the host budget is the measured CPU count and memory minus the OS and
    Docker reserve set in an operations policy;
  - the declared CPU and memory reservations of every running container in a
    HOME or LAB Compose project, plus the candidate, minus the services a
    replacement retires, plus the external-workload allowance from the same
    policy, stay within that budget;
  - every service, including the candidate, also declares limits, and its
    reservation does not exceed its limit;
  - free disk on the data root and on Docker's data root covers the declared
    need.

  This is the deciding criterion: a candidate that cannot run together with
  the services already running is not promoted.

The report records each measured value and its source. A value that cannot be
measured is `NOT_RUN`, not passed. A running Compose container or a
candidate service without declared reservations cannot be summed, so it
makes the resource criterion `NOT_RUN` until it declares them. An owner check
item is reported as owner judgment; it is neither a measurement nor a block.
The LAB check (`lab.py check`) sums the same reservations against its host
budget.

#### 6. Promotion procedures

**`add`:**

1. Move the files, documents and secrets by the destination rules.
2. Wire the integrations.
3. Run the readiness check.
4. Render and test.
5. Start the service in an approved window.

**`replace-same` and `replace-substitute`** add these steps to `add`:

- an inventory of every consumer of the replaced service;
- a data migration plan: what is exported, how it is imported, and how it is
  verified;
- a cutover sequence that moves each consumer;
- a rollback that restores the replaced service and its data;
- a retirement step that removes the replaced service only after the new one
  is verified.

**`replace-substitute`** also needs a mapping from the old configuration and
data format to the new one, because the products differ.

Each procedure is a Runbook in the target role folder. The promotion Task
records the actual results.

The POL-0078 profile vocabulary, the `infra/` tier layout tests and the LAB
isolation tests stay authoritative. Document moves keep artifact identifiers
and creation dates. No secret value is read or written.

#### 7. Drafting calls

These were decided while drafting the Spec, not by the owner:

- the names `promotion.yaml`, `docker-compose.yml`, `add`, `replace-same`,
  `replace-substitute` and `undecided`;
- the rule that LAB secret values are never promoted;
- the OS and Docker reserve is a value in an operations policy, with its
  first value proposed in the Plan;
- the external-workload allowance is a value in the same policy, with its
  first value proposed in the Plan from a measurement;
- reservations are declared next to limits in the shared resource templates;
- dashboards move into each LAB folder;
- Linux and Docker requirements come from the rendered Compose plus the
  optional `host` field.

Moving each Compose file one folder deeper changes the base that relative
paths resolve against, so every relative path in a moved LAB is adjusted.

Bringing LABs into the standard layout moves sources, documents and catalog
rows only, and starts nothing.

The public registry `secrets/SENSITIVE_ENV_VARS.md.example` is outside the
agent's permitted paths. The agent prepares its placeholder edits and the
owner applies them.

### Failure and Edge Cases

`lab.py check` refuses a LAB that is not in the standard layout, has no valid
manifest, or reads a HOME secret path. The readiness check refuses a promotion
when any criterion fails or cannot be measured.

**Observable failures.**

Any of these is a failure:

- a LAB file outside its folder;
- a LAB without a manifest, or with a manifest that disagrees with its
  rendered limits;
- a LAB reading a HOME secret;
- a promotion procedure without a rollback;
- a readiness report that passes a value it did not measure.

**Stop boundaries.**

This Spec promotes no LAB and starts no container. The owner applies every
change to `secrets/SENSITIVE_ENV_VARS.md.example`.

## Acceptance Criteria

### Criteria

1. Every LAB lives in `labs/<name>/` with its `docker-compose.yml`, `README.md`
   and assets. Only `labs/README.md` and `labs/.env.example` remain at the
   `labs/` root.
2. Every LAB has a valid `promotion.yaml`, and `lab.py check` refuses a missing
   or inconsistent one.
3. No LAB reads a HOME secret path; each LAB uses `secrets/labs/<name>/` for
   every secret, each with its catalog and registry rows. No LAB binds the
   Docker socket.
4. The destination rules and the three promotion procedures are written as
   operations documents. The replacement procedures cover data migration,
   consumer cutover, rollback and retirement.
5. A readiness check produces the section 5 report against the measured HOME
   host, and refuses a candidate that cannot run together with the running
   services.
6. Every LAB has a Guide and a Runbook in `15-labs`, including the Kafka and
   OpenSearch cluster LABs.
7. Document, hardening, LAB and unit checks pass, and hosted CI passes, with
   actual results in the Task.
8. The shared resource templates in `infra/common-optimizations.yml`, and
   every HOME and LAB service that sets its own limits, declare reservations
   sized from recorded measurements. The readiness check and `lab.py check`
   sum reservations plus the external-workload allowance, and report owner
   check items as owner judgment.

### Evidence Requirements

- Criteria 1 and 2 are verified by the layout tests and the manifest and `check` tests (`layout tests`, `manifest and check tests` rows in TSK-0001).
- Criterion 3 is verified by the LAB and secret suites, the catalog and owner registry checks, the root render and `lab.py check` runs (TSK-0001 and TSK-0003); a check needing owner inputs that was not run stays `NOT_RUN`.
- Criteria 4 and 6 are verified by the LAB suites, the operations catalog check, metadata, links and lifecycle checks and the static and HOME renders of the cluster LABs; criterion 5 by the LAB suites and the `lab.py readiness` runs on HOME.
- Criterion 8 is verified by the LAB suites, Compose acceptance, `common-optimizations` controls, hardening, HOME readiness and `lab.py check` rows in TSK-0002.
- Per the package [Plan](plan.md), criterion 7 is verified by the root and LAB `docker compose config` renders, the full unit suite, `check-all-hardening.sh`, the metadata, links, lifecycle, operations catalog and script manifest checks, and the hosted CI row.
- The frontmatter owner (`@buenhyden`) judges each criterion and records the decision in the Task's Criterion Acceptance table; a failed, blocked or skipped check is reported as such and does not count as met.

## References

### Normative and Evidence

- [LAB operations guides](../../05.operations/guides/15-labs/README.md)
- [Analytics LAB migration](../0262-analytics-labs-migration/spec.md)

### Historical and Navigation

- [LAB README](../../../labs/README.md)
- [infra README](../../../infra/README.md)
