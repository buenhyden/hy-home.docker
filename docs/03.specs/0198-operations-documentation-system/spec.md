---
title: "Operations Documentation System and Service Coverage"
version: "0.1.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0198"
parent_ids:
- "REQ-0026"
- "REQ-0027"
- "AD-0030"
- "AD-0031"
created: "2026-10-01"
---

# Operations Documentation System and Service Coverage

## Overview

Make Stage 05 explain how to operate both individual infrastructure services
and the integrated HOME/development system. Retain the role-first Guide,
Policy and Runbook directories and issued document identities. Connect shared
operating rules and procedures once, and write service-specific differences
where they belong.

The user additionally required exhaustive completeness, lossless content
consolidation and version-grounded contradiction resolution on 2026-10-01.
The user approved this design on 2026-10-01 after explicitly selecting shared
canonical documents plus service-specific content. This approval authorizes
this written specification, not its implementation. The user subsequently
approved the written Spec on 2026-10-01 and requested this package's Plan.
The user subsequently approved the written Plan and selected tier-scoped
agent implementation with independent review on 2026-10-01.

## Boundaries and Inputs

Inputs are the current Compose application, package READMEs, current Stage 01
and 02 owners, SPEC-0197's reviewed tier layout, Stage 05 role documents and
the Stage 99 registry. Reconcile the actual implementation base before
execution; the research counts below are dated observations, not new constants.

Research on 2026-10-01 found 225 role documents: 77 Guides, 75 Policies and
73 Runbooks, covering 87 subjects (68 triplets, two Guide/Policy pairs and
17 single-role subjects). The current source inventory covers 153 service
identities across twelve tiers: 45 HOME, 12 DEV, 55 OPTIONAL and 41 LAB.
SPEC-0197 provides twelve flat Data packages and six Analytics packages.
These figures do not describe running-container counts or recovery readiness.

In scope: every current Guide, Policy and Runbook; their indexes; the Operations
entrypoint; related current architecture links; existing document automation
where a demonstrated structural gap needs a bounded correction. Review incident
navigation and handoff links, but do not rewrite factual incident/postmortem
records. Review existing system-wide procedures before adding a missing topic.

Out of scope: service deployment or configuration changes, new runtime behavior,
secret access, data migration, recovery rehearsals, reboots, remote publishing,
archival disposition, changing agent approval rules, and unrelated SPEC-0182
or SPEC-0193 implementation. Frozen Stage 98 bodies remain unchanged. Document
ownership changes do not grant authority to perform the documented operations.

## Behavior Contract

Write Spec, Plan and Task prose in English. Write Stage05 Guide, Policy and
Runbook explanatory prose, and README prose, in Korean. Preserve registered
headings, identifiers, commands, paths, metadata and technical names. Preserve
actual historical quotations with source context and the required explicit
quotation marker; a dated heading alone does not exempt current instructions.
Numeric language checks supplement semantic review rather than replace it.

### Stable role-first structure

Keep these canonical paths and their existing identifier rules:

- `docs/05.operations/guides/####-<slug>.md`
- `docs/05.operations/policies/####-<slug>.md`
- `docs/05.operations/runbooks/####-<slug>.md`
- Existing incident packets and their paired postmortems.

Do not introduce tier/service subdirectories, a parallel catalog, a new
playbook document type, redirects, or a separate service registry. The
Operations README and existing role READMEs remain the discovery surfaces.
Every role leaf is linked exactly once from its role index. Indexes classify
all twelve current tiers consistently; cross-cutting subjects are not assigned
a misleading tier number. Keep existing IDs, subject slugs and filenames.
Any necessary retirement requires its own preservation decision; ordinary
content improvements happen in place.

### System, tier and service navigation

The Operations entrypoint presents operator needs at three scales:

1. Whole system: understand dependencies and user paths; select HOME or
   optional workloads; start/reboot safely; handle authentication/secrets,
   capacity, backups, upgrades, and cross-service incidents.
2. Tier: understand its operational responsibilities, dependencies and
   failure impact, then find the applicable service subjects and common controls.
3. Service subject: find the implementation owner, normal-use Guide,
   applicable Policy and executable Runbook, including helper jobs and shared
   dependencies where those affect an operator's decision.

README content remains navigation and concise directory context. Detailed
system operating knowledge belongs in one new `system-operations` Guide,
linked to AD-0031 rather than copying architecture definitions. It explains
actual request/authentication/data paths, shared host/storage/GPU constraints,
profile selection and readiness boundaries, and routes to existing procedures.
A compact tier responsibility/dependency table belongs in that Guide; it does
not become another machine service inventory.

Reuse existing controls and procedures, especially POL-0006, POL-0078,
RUN-0098 and subjects 0021, 0077 and 0086. Add a system-level cross-service
triage Runbook only where existing procedures do not cover the symptom and
decision flow. It must connect observations to existing service procedures,
not copy their commands. A new system Policy is justified only by a concrete
cross-service control absent from current policies; otherwise the system
Guide explicitly links the applicable policies. Do not create twelve generic
tier triplets or three documents per Compose container merely for symmetry.

### Common ownership and service-specific differences

Preserve the existing `implementation_services` mapping on the owning Guide.
Each Compose service identity has exactly one operational subject owner;
shared system/tier Guides link that owner without claiming the identity again.
A subject may cover several tightly related service identities, as the
lakehouse subject already does. Keep its shared catalog/engine procedures
coherent rather than manufacturing a separate manual for every helper.

Service-bound subjects retain the existing required Guide/Policy/Runbook
siblings. Shared content reuse means linking common owners and stating local
applicability, prerequisites, exceptions and unique behavior within those
siblings; it does not remove required siblings or silently weaken the
validator. Non-service subjects retain only the roles they actually need.
Clarify this distinction in current authoring/navigation wording.

For each service subject, an operator can identify the applicable common
controls, unique data and access boundaries, selected profiles, dependencies,
normal observations, safe diagnostic route and recovery limits. Preserve
source-owned versions, ports and settings by linking their implementation
owner; duplicate exact values only when an executable instruction requires
them and validation can catch drift.

### Exhaustive service completeness and version reconciliation

The user's additional direction on 2026-10-01 requires a full service audit,
not a sample-only cleanup. For every current service identity, inspect the
owning subject's three role documents together with its Compose declaration,
package README, scripts, image/build source and applicable shared owners.
For every Compose-built service, inspect the selected Dockerfile and effective
build context, Dockerfile selector, build arguments and target. Trace FROM,
installed packages, copied configuration/scripts and ENTRYPOINT/CMD, including
referenced source needed to explain behavior. An image label alone cannot prove
the built service's version or behavior. This explicitly incorporates the user's
Dockerfile-inspection clarification during implementation.
Helper and provisioning jobs remain part of their subject but are explicitly
accounted for. A subject-level review cannot silently omit one of its services.

Use a service-by-topic evidence matrix in the implementation Task. For each
required topic, record the current implementation/source, applicable declared
version, official documentation evidence, current document/section, finding
(missing, incomplete, duplicate, contradictory or consistent), resolution and
final content owner. Shared rows may cover named services only when the
applicability and absence of differences are explicit. This is execution
evidence, not a new live service registry.

Audit at least these topic groups for every service:

| Required topic | Authoritative document role |
| --- | --- |
| Purpose, users, HOME/DEV/OPTIONAL/LAB applicability, limitations | Guide |
| Implementation entrypoint, declared image/build version, profiles, dependencies and startup/readiness behavior | Guide |
| Access path, protocol, ports/routes, authentication/authorization and credentials without secret values | Guide explains; Policy owns constraints |
| Configuration inputs, required variables/files, mounts, data ownership and persistence | Guide explains; Policy owns retention/access constraints |
| Normal usage, expected signals, health, metrics/logs and resource/capacity limits | Guide explains; Policy owns required limits and review triggers |
| Allowed/prohibited operations, approvals, exceptions, accountable owner | Policy |
| Installation/provisioning or startup, safe shutdown/restart, configuration changes and upgrades supported by this implementation | Runbook |
| Symptom diagnosis, expected result, failure/stop conditions and escalation | Runbook |
| Backup, restore, rollback, credential/certificate maintenance, deletion and cleanup where applicable | Policy defines boundaries; Runbook owns executable steps |

A topic is satisfied by complete local content or an explicit applicable link
to its common owner. Mark non-applicable topics with a concrete implementation
reason (for example, a one-shot stateless job has no HTTP health endpoint),
not a blank section. A missing implementation capability is recorded as a
limitation and routed to a separate requirement; do not invent a procedure to
make the matrix appear complete.

Resolve version-specific statements against the repository's declared image
version/digest, Dockerfile/package pin or build source and the corresponding
official product documentation/release notes. Do not substitute the upstream
latest version or silently upgrade a service. Record the exact release/range
covered and URL/section supporting a correction. When the declaration is
mutable/unpinned or official historical evidence is unavailable, state that
uncertainty and restrict the claim to verified source behavior; never imply
runtime version observation from a source pin. Historical run evidence remains
dated evidence rather than being rewritten to match a newer declaration.

Preserve every meaningful existing instruction, constraint, exception and
warning while consolidating. Record old section -> final owner/section for
content that moves. Remove a duplicate only after its canonical version and
links preserve its substance. For contradictory statements, record both claims,
current implementation/version evidence and the chosen correction; do not
silently discard the inconvenient claim. Resolve material contradictions before
source acceptance, or explicitly mark the package incomplete when evidence is
insufficient. No conflicting active instruction may be left merely because
its Markdown links pass.

If the implementation fails an existing required control, classify that as
implementation nonconformance, not an editorial choice. Preserve the policy,
state the actual behavior and operational limitation, and route remediation
through a separately approved implementation change. A documentation fix may
resolve a misleading claim; it cannot assert that the underlying control now
works. Obtain an independent security review for suspected security defects.
Do not mark an affected procedure safe/compliant until evidence supports it.

### Role-specific content and evidence

- Guide: state the primary reader need and explain normal use, dependencies,
  expected behavior and common checks. Move ordered recovery procedures to
  the existing Runbook and link them; keep legitimate simple usage examples.
- Policy: define scope, mandatory/prohibited actions, exceptions, accountable
  owner and review triggers. Link shared controls instead of copying them.
  Do not hide command sequences or one-off execution evidence in a Policy.
- Runbook: identify trigger, target/selection, prerequisites, working directory,
  necessary access, side effects, ordered commands, expected observations,
  decision points, stop conditions, validation, recovery and escalation.
  Distinguish restarting a service from restoring data or credentials.

System startup/recovery uses actual dependency and readiness conditions;
tier numbering is not an execution order. Do not claim availability, data
recovery, authentication or failover from syntax checks. Diagnostic output
must follow current redaction rules. Record the responsible repository owner
and concrete escalation trigger; do not invent an on-call team or SLA.

## Technical Approach

Audit all current role documents, not just filename coverage. The implementation
Task records each artifact's review disposition: retain, revise or consolidate
content into an existing owner, with the owner and reason. Structural grouping
can be automated; semantic findings require author-independent read-only
review. Representative research findings are starting points, not a claim
that all 225 bodies have already passed semantic review.

Known starting points: duplicated Nginx recovery steps across its Guide and
Runbook and within that Runbook; generic escalation wording; scattered
system material; dated inventory/roadmap text in POL-0006; misleading statements
that all subjects may omit roles despite service-bound triplet enforcement.
SPEC-0197 owns the immediate Analytics index/path corrections. This package
consumes those corrections without duplicating their implementation evidence.

Prefer in-place role/content corrections and existing automation. Reuse
`check-operations-catalog.py`, metadata, links, lifecycle checks and the
registered changed CI profile. Its service-inventory projection is derived
from Compose plus Guide bindings; do not add a second coverage registry.
If a new structural invariant needs code, extend the existing checker and
write a failing-before/passing-after regression. Do not attempt to classify
semantic usefulness using keyword counts or heading presence alone.

## Interfaces and Data

Existing artifact IDs, relative links, subject slugs, frontmatter schemas,
service bindings and current generated inventory are compatibility surfaces.
New documents receive the next issued subject number at implementation time
under the registry; this Spec does not reserve unneeded Guide/Policy/Runbook
triplets. Preserve existing status honestly: edited active documents stay
active unless the normal lifecycle requires otherwise; new documents enter
through their registered initial state.

The Task owns temporary audit progress and verification receipts. Long-lived
operating knowledge is promoted to Stage 05; architecture explanations remain
in Stage 02. External research informs design and does not authorize commands.

## Failure Modes and Guardrails

- Missing service coverage: fail the existing service-owner join; fix the
  owning subject rather than adding duplicate bindings to system Guides.
- Divergent shared controls: select the existing canonical owner and replace
  copies with explicit applicability links, preserving meaningful differences.
- Unimplemented recovery: document the limitation and route missing behavior
  to a future Spec; do not publish an invented executable recovery procedure.
- Historical counts or paths: mark them as dated provenance or update a current
  assertion from its source. Do not silently rewrite historical evidence.
- Bulk movement or ID churn: stop and return to this approved structure;
  directory rearrangement is not required for this design.
- Unverified operational result: record NOT_RUN, blocked or failed honestly.
  Automated checks plus independent semantic review do not equal live rehearsal.

## Acceptance Contract

1. Every current role document is inventoried by artifact ID with a recorded
   content-review disposition; all 225 baseline documents are accounted for,
   with additions/removals reconciled to the actual execution base. Each service
   identity also has a complete service-by-topic matrix; no service or required
   topic is omitted through sampling or an unexplained empty field.
2. Role-first paths and issued IDs remain stable. All twelve tiers and
   cross-cutting subjects are navigable through existing indexes; every role
   leaf appears exactly once, and source/service ownership checks pass.
3. An operator can navigate from whole-system needs to tier responsibilities,
   common policies and service procedures for startup/reboot, authentication,
   backup/recovery, upgrades, capacity and cross-service diagnosis. Missing
   executable capability is stated as a limitation, not presented as verified.
4. Each retained service identity has one subject owner and an applicable
   Guide/Policy/Runbook triplet. Common rules and procedures have one content
   owner; service-specific applicability and differences are explicit.
5. Every missing/incomplete applicable topic is filled from implemented behavior
   and version-matched official evidence. Non-applicable topics and unsupported
   capabilities have explicit reasons/limits. Moved or consolidated content has
   an old-to-new section mapping that preserves meaningful instructions.
   Conflicts across Guide/Policy/Runbook are resolved with recorded current
   implementation/version evidence; no unresolved material contradiction remains.
   Audited role mixing, duplication, stale assertions and unsupported recovery
   claims are corrected. Runbook steps have
   observable success/stop criteria and grounded recovery/escalation boundaries;
   non-applicable recovery actions are explained rather than filled with boilerplate.
6. Existing operations, metadata, link, lifecycle and changed CI checks pass.
   New nontrivial checker code, if needed, has RED/GREEN evidence and at least
   80% changed executable-line coverage. Independent read-only semantic review
   reports no unresolved material discrepancy between docs and implementation.
7. Task evidence distinguishes source/static verification from actual runtime
   or recovery results. No secret values, runtime mutations, duplicated service
   registry, unapproved document disposition or unrelated package changes occur.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md): FR-0003,
  FR-0004, FR-0007, FR-0008 and maintainability/verifiability requirements.
- [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md):
  preserve document identity and current versus historical authority.
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md):
  current integrated host architecture.
- [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
  and [ADR-0043](../../02.architecture/decisions/0043-operations-role-layout.md):
  document contracts and role-first layout.
- [SPEC-0197](../0197-infra-tier-layout/spec.md): reviewed tier-layout dependency.
- [Diataxis](https://www.diataxis.fr/how-to-use-diataxis/): improve useful content
  without creating empty document structures; role mapping here is project-specific.
- [AWS runbooks](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html)
  and [playbooks](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_playbooks.html):
  routine execution versus diagnostic decision flows, permissions and validation.
- [Google SRE incident response](https://sre.google/workbook/incident-response/):
  impact, mitigation, responsibilities and cross-service dependencies.
- [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/):
  dependency ordering and readiness are distinct.

## Open Questions

No unresolved design choice blocks written-spec review. The user selected
shared content links plus service-specific differences and approved retaining
role-first paths. Whether an actual content gap justifies a new system Policy
or diagnostic Runbook is resolved by the bounded audit criteria above; it does
not authorize a new document type or runtime behavior.

## Operational Impact

Documentation becomes easier to use for individual services and integrated
system operations. Runtime configuration and data remain unchanged. Source
checks and independent review establish document consistency; live recovery
readiness remains separately observed evidence. Implementation begins only
after approval of this written Spec and its subsequent Plan.
