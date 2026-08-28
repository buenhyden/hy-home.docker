---
status: draft
artifact_id: reference:agentic-engineering-research-draft:docker-compose-infrastructure
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Docker Compose Infrastructure

## Overview

This leaf separates the repository's declared Compose topology from Compose
execution, container health, network reachability, image resolution, and
secret availability. It is an advisory infrastructure analysis, not a runtime
inventory or an authorization to start, alter, or inspect containers.

## Purpose

Provide a bounded way to investigate a Compose change: identify the exact
declaration, apply only retained source semantics that are actually supported,
and preserve the distinction between a local configuration and an observed
application model.

## Scope

The review is limited to read-only tracked configuration at literal base
`af8de6583ac3bc14bcc8fbe5c3a8a37b3b7fdf1a`, the root Compose file, and the
retained Docker/Compose observations. It excludes Docker commands, environment
or secret values, resolved interpolation, image pulls, running services,
health, ports, networks, volumes, logs, and remote state.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `DCI-001` | The root `docker-compose.yml` declares an application name, networks, file-referenced secret definitions, and an `include`-assembled configuration surface. | tracked configuration | VERIFIED | `docker-compose.yml` at `af8de6583ac3bc14bcc8fbe5c3a8a37b3b7fdf1a` | Investigate the specific root declaration and referenced child file before changing an infrastructure surface; declaration is not execution. |
| `DCI-002` | Retained Docker documentation identifies the Compose file as an application-model reference; its retained `include` observation distinguishes included-project relative paths, project directories, environment precedence, and conflict detection from service-level `extends`, with specification revision `11296e387ba76c77db1db768b9153a4304a3c9bd` retained separately. | retained official observation | HISTORICAL VERIFIED | retained Task 0001 infrastructure ledger and dated DCI source rows | Review an include edge as topology assembly and an extends edge as service-template inheritance; reopen sources under new authority before relying on changed semantics. |
| `DCI-003` | Profiles, `depends_on`, health checks, and secret semantics are not independently established for this draft by the retained external inventory. | evidence boundary | UNVERIFIED | the relevant `docker-compose*.yml` file and its service definition | A change proposing one of these mechanics needs a source-bound, target-specific investigation and approved verification plan; do not infer the behavior from a similarly named field. |

### Investigation sequence

First identify the root or child Compose file and the named service, network,
volume, secret reference, or include edge. Then inspect its tracked consumers
and any declared dependency relationship without reading a secret value or
resolving environment interpolation. Record the literal revision, the intended
adoption condition, and the smallest non-runtime static check that can support
the proposal. Runtime evidence, if later authorized, must separately identify
the target, execution authority, timestamp, and observed result.

The retained inventory does not independently support claims about profiles,
`depends_on`, health checks, or secrets beyond the local definitions that a
tracked file declares. In particular, a secret-file reference is not evidence
that a secret exists, was mounted, or was withheld from logs.

### Infrastructure change surfaces

| Subitem | Supported mechanism or local fact | Exact local investigation target | Adoption condition | Verification limit |
| --- | --- | --- | --- | --- |
| Include | Retained documentation says an included project has its own relative-path base and project directory; conflicts are detected rather than silently merged. | `docker-compose.yml` `include:` entry and the included `docker-compose*.yml` file | Name the include edge, consumer, relative-path base, and collision review. | No resolved model, conflict result, or execution was observed. |
| Extends | Retained analysis distinguishes service-level `extends` from `include`; it is a template-inheritance rather than application-assembly concern. | service `extends:` block and referenced `infra/common-optimizations.yml` entry | Review inherited fields and the exact override before adopting a template change. | The retained external inventory does not independently establish every field-merge outcome. |
| Profiles / dependencies / health / secrets | Local files may declare these fields or references, but their external semantics are not independently located in the retained inventory. | relevant `infra/**/docker-compose*.yml` service block | Obtain source-bound semantics and a target-specific plan before relying on behavior. | This leaf records no profile selection, dependency ordering, health result, secret value, mount, or redaction evidence. |
| Networks and storage | Root configuration declares network and secret-reference surfaces; child files may declare service attachments and volumes. | `docker-compose.yml`, relevant `infra/**/docker-compose*.yml`, and `infra/**/README.md` | Identify consumers, data boundary, retention, and ownership before changing a shared resource. | Declarations do not prove connectivity, persistence, encryption, or data recovery. |
| Backup / recovery | Recovery must be separately specified for a named persistent target. | affected service Compose file and its adjacent `README.md` | Require an owner-approved backup, restore, and rollback plan before operational adoption. | No backup, restore, or failure exercise was performed or inferred. |
| IaC change control | A Compose edit is a tracked configuration change requiring reviewed scope and evidence. | changed Compose path, Task 0004, and relevant owner document | Bind change, reviewer, target, and rollback criteria before any execution authority. | Version control and review records do not prove deployed state. |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DCI-SRC-001` | `DCI-001` | Root Compose configuration / workspace | [docker-compose.yml](../../../../docker-compose.yml) | tracked configuration | `af8de6583ac3bc14bcc8fbe5c3a8a37b3b7fdf1a` | 2026-08-28 | Local configuration does not prove interpolation, file availability, Compose execution, or runtime state. |
| `DCI-SRC-002` | `DCI-002` | Compose file reference / Docker | [Compose file reference](https://docs.docker.com/reference/compose-file/) | retained official observation | [dated DCI leaf, source row 444](../2026-08-08-agentic-engineering-research-pack/docker-compose-infrastructure.md#sources) | 2026-08-08T18:18:06+09:00 | Retained application-model reference; it does not establish local adoption or the unlocated per-feature semantics. |
| `DCI-SRC-003` | `DCI-002` | Include reference / Docker | [include](https://docs.docker.com/reference/compose-file/include/) | retained official observation | [dated DCI leaf, source row 456](../2026-08-08-agentic-engineering-research-pack/docker-compose-infrastructure.md#sources) | 2026-08-14 | Retained include observation only; no new source request occurred. |
| `DCI-SRC-004` | `DCI-002`, `DCI-003` | Compose Specification / compose-spec | [observed revision](https://github.com/compose-spec/compose-spec/tree/11296e387ba76c77db1db768b9153a4304a3c9bd) | retained pinned observation | [dated DCI leaf, source row 457](../2026-08-08-agentic-engineering-research-pack/docker-compose-infrastructure.md#sources); `11296e387ba76c77db1db768b9153a4304a3c9bd` | 2026-08-14 | The retained pin is not a new read or proof that profiles, dependencies, health, or secret behavior was independently located for this draft. |

## Maintenance

Remeasure the specific tracked Compose declaration after a root, include,
service, network, volume, secret-reference, or image-definition change. Reopen
mutable Docker documentation and re-evaluate the pinned specification only
under separately authorized source access. Keep static configuration,
validated composition, executed Compose output, and runtime observation as
separate evidence classes.

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | An agent-proposed Compose edit names one file and one owner-approved task. | Inspect task scope and changed declaration. | A task does not authorize runtime execution. |
| architecture | applies | A system boundary change identifies service, network, data, and recovery effects. | Inspect tracked design and Compose edge. | Static topology is not a deployed architecture. |
| common | applies | Shared networks or reusable fragments have a named consumer and collision review. | Inspect root and referenced Compose files. | Inclusion does not prove compatible execution. |
| docs | applies | Document the literal revision, source state, and non-runtime limit. | Inspect source and claim rows. | Documentation is not operational evidence. |
| infra | applies | The proposed field has a target-specific configuration and source-bound semantic basis. | Inspect the exact `docker-compose*.yml` definition. | Profiles, dependency, health, and secret behavior remain UNVERIFIED here. |
| ops | applies | A runtime change has a separately approved operator, rollback, and observation plan. | Inspect approved runbook and event evidence. | No runtime plan or observation is supplied. |
| qa | applies | A static composition check is selected before a future runtime check. | Record the exact check and target. | No Docker command was run by this leaf. |
| security | applies | Secret references and exposure paths are reviewed without accessing secret values. | Inspect only declaration paths and ownership. | A reference does not prove secure storage, injection, or redaction. |

## Related Documents

- [Security Governance](./security-governance.md)
- [Automation Pipeline Workflow](./automation-pipeline-workflow.md)
- [Verification and Validation](./verification-validation.md)
- [Workspace Baseline](./workspace-baseline.md)
- [Scope Application Matrix](./scope-application-matrix.md)
- [Task 0004](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md)
