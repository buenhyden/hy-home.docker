---
title: "Home and Development Server Convergence Plan"
version: "0.6.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0180-PLAN-0001"
parent_ids:
- "SPEC-0180"
created: "2026-09-19"
---

# Home and Development Server Convergence Plan

## Objective

This Plan ran in rounds. The first follow-up round closed [Spec](spec.md) gaps against main
`dffc2ed8bc3bf4b2538b03884ad7ab5d7587375b` in
`codex/home-dev-convergence-followup`. Preserve delivered implementation and
historical Tasks; do not replay the original baseline or its runtime approvals.
[Task 0005](tasks/tsk-0005-current-main-convergence.md) owned the acceptance
assessment for that round; Tasks 0007 and 0008 own the later rounds (Task 9
and Task 10 below), and [Task 0008](tasks/tsk-0008-storage-security-lakehouse-convergence.md)
will hold the completion receipt.

## Dependencies

REQ-0027 and AD-0031 govern the target. Current tracked Compose/configuration,
POL-0078, Stage 99, the existing scripts and tests, public environment/secret
schemas, and official upstream sources govern their respective contracts.
Required local tools include Python with YAML support, Docker/Compose and the
registered CI dependencies. Tool availability is a preflight result, never an
assumption that an unexecuted gate passed.

The original plan used main `d1e6ded52808b02392c52472d5416518a3b959d6`.
Task 0001 retains that execution; Tasks 0002–0004 retain later OpenBao,
metadata and native OIDC evidence. Their completed scope is an input to the
current comparison, not an instruction to repeat it.

### Shared interfaces and ownership

- A supplies measured paths, names, counts, candidate dispositions and gaps to
  B–G/R. A is read-only; R separately owns evidence-backed lifecycle decisions
  and any justified repository lifecycle implementation.
- B owns Compose/profile activation and dependency-closure changes; POL-0078
  remains the only profile vocabulary. A HOME candidate is a selection, not a
  second vocabulary or a rollout authorization.
- C owns dependency source/update-owner/projection relationships and version
  checks. Compose/Dockerfile pins remain runtime authority; 0086 owns repository
  version operations and 0083 owns the Renovate component.
- D owns necessary Stage 99 contracts before E authors dependent documents.
  E owns root/tier/service navigation and Stage 05; links route to existing
  owners rather than copying policy or runtime patch tables.
- F owns public key and secret-ID consumer mappings and safe synchronization
  regressions. Other units report required schema changes to F and never edit
  private values or independently prune keys.
- R owns service rationalization after actual-consumer evidence review; it
  coordinates exact add/move/remove/replace paths with B–F and never assumes
  removal from low usage or a missing observation.
- G integrates existing validator owners and reviews; it coordinates edits to
  shared operations-catalog and test files instead of accepting concurrent
  writers. Existing generation and CI entry points remain canonical.

## Execution Sequence

### Preflight and comparison

1. Confirm isolated branch/base and clean starting status; read bootstrap,
   provider, active Requirements/Architecture/Spec and Task, selected roles,
   procedures and registered CLI help.
2. Read Tasks 0001–0004 and classify all nine criteria and W1–W9 as completed,
   partially completed, stale, not implemented, superseded or new gap using
   cited current source and dated evidence. A previous PASS is not a fresh run.
3. Inspect only public tracked schemas and safe read-only host summaries.
   Keep private values, raw environment renders and credentials out of output.
4. Record initial operations-catalog and version-projection checks, required
   tool availability, current service inventory and independent audit findings.
   Freeze each bounded unit's files and acceptance checks before dispatch.

### Work units

These are the Spec's work units. Tasks 0001–0008 carry them in turn, and the
completion receipt that [Task 0008](tasks/tsk-0008-storage-security-lakehouse-convergence.md)
will hold maps each acceptance criterion to one of them.

1. W1: Inventory and research: measured service, profile, config, version,
   env/secret and document inventory with official evidence (A; Tasks 0001,
   0005 and 0008 S00–S01).
2. W2: Architecture and profile: service dispositions, POL-0078 vocabulary,
   root includes, dependency closure and HOME exclusions (B/R; Tasks 0005,
   0007 and 0008 S04–S05, S07–S08, S19).
3. W3: Stage 99 contracts: template and registry gaps with focused contract
   tests, and the per-stage template ledger (D; Tasks 0005 and 0008 S02, S19).
4. W4: Navigation and operations: root, tier and service READMEs and the
   retained services' Guide/Policy/Runbook (B/E; Tasks 0005, 0007 and 0008
   S03–S19).
5. W5: Version governance: runtime pins, registry projection, single update
   owner, disabled infrastructure automerge (C; Tasks 0005 and 0006).
6. W6: Environment and secret contracts: public schemas, unique identities and
   value-preserving private synchronization (F; Tasks 0002, 0005, 0007 and
   0008).
7. W7: Validation and review: focused regressions, changed/full, Compose,
   hardening, links, registry and Renovate checks, and independent reviews (G;
   every Task).
8. W8: Deployment and recovery: approved live activation and its health,
   persistence and backup/restore evidence, kept apart from pending and
   unverified items (F/G; Tasks 0002, 0004, 0007 and 0008).
9. W9: Delivery: reviewed logical commits and PR reports with residual risks
   and recovery (G; the PRs in each Task's commit or delivery ledger).

### Bounded current work units

| Unit | Scope and output | Depends on | Completion checkpoint |
| --- | --- | --- | --- |
| A — inventory and disposition | Current Compose/include/profile/service, version, env/secret identity and docs inventory; consumer-based HOME/DEV/OPTIONAL/LAB/REMOVE/MIGRATE matrix; safe host snapshot and external evidence gaps | Preflight | Every tracked service has all twenty required inventory fields; observations separated from inferred disposition and runtime proof |
| B — profile convergence | Evidence-backed POL-0078, Compose selection and companion/exclusion repairs; regression tests for maintenance isolation and actual names | A | Exact vocabulary, explicit profiles, root coverage, closure and port checks; ordinary HOME excludes maintenance and legacy |
| C — version convergence | Source/projection drift, Dockerfile extraction, manager uniqueness, literal exceptions, digest/floating policy, Renovate configuration/extraction evidence | A | Existing sync tests and real check, official strict validator and safe extraction; no owner overlap or unexplained literals |
| D — documentation contracts | Only demonstrated Stage 99 template/registry/README responsibility gaps and their focused contract tests | A, B/C interface decisions | Contracts distinguish implementation navigation from operator knowledge and runtime authority |
| E — documentation convergence | Retained-service Guide/Policy/Runbook adequacy, root/tier/service README maps, current upstream evidence and lifecycle routing | A, B, C, D | Coverage and substantive current operating/recovery guidance; metadata/links/catalog checks |
| F — environment and secrets | Public schema classifications and metadata consumer closure; deterministic value-preserving sync behavior and negative tests | A, B/C/R consumer changes | Five key classes, unique keys/IDs, complete grants, ID-based preservation, atomic mode 0600 writes, symlink/non-regular rejection and no value output |
| R — service rationalization | Actual-consumer/evidence review, disposition decisions and justified add/move/remove/replace implementation with exact lifecycle path handoff | A; B/C/F interfaces | Every decision cites consumers, data/recovery and resource evidence; no assumed removal, no runtime mutation or secret-file deletion |
| G — validators and review | Existing validator integration, focused RED/GREEN evidence, changed/full gates, independent unit and whole-branch review, final report and PR preparation | B–F, R | Actual command/exit/limitations recorded; blocking findings corrected and re-reviewed |

A is read-only. Independent units may proceed after their inputs stabilize, but
only one implementer owns a file at a time. B/C/F identify shared-file requests
before mutation; D precedes E when a template contract changes. R consumes A's inventory for lifecycle decisions and implementation, and E
records the approved result in operator documents; neither creates a competing
inventory owner. Every implementation unit follows
implementation → specification review → quality/security review → targeted
correction → scoped re-review. In the A–G/R round, review results and rulings
went in Task 0005.

### Task 1: A — Baseline inventory and service disposition

Read-only input scope: root and tracked infra Compose/Dockerfiles, POL-0078,
public env/secret schemas, updater files and retained-service docs. Output the
current source inventory, consumer/disposition matrix and evidence gaps to this
Task and the existing Stage 90 convergence research owner. No implementation
file is owned by A. Check every tracked service/include and safe host observation;
B–F consume only the measured interface, with uncertainty explicitly marked.
The inventory checkpoint requires every service row to carry all twenty mission
fields: Domain, Component, Compose path, Service, Profiles, Runtime
classification, Consumer, Dependencies, Network, Ports, Persistence, Env, Secret
metadata, Resources, Security, Backup (required for stateful services), Operations
docs, Runtime version authority, Update owner and Disposition. Explicit evidence
gaps are valid observations but cannot be silently omitted or counted as complete
consumer/recovery proof. Specification and quality reviewers verify coverage and
evidence provenance.

### Task 2: B — Profile governance

Own only assigned Compose/profile-policy repairs after A proves a gap, including
POL-0078's catalog package. Coordinate operations-catalog implementation/tests
with G before editing shared files. Verify explicit profiles, exact vocabulary,
HOME selection, dependencies, mutual exclusions and maintenance/legacy isolation.
Send changed consumer/profile interfaces to E/F. Specification and security
review must precede any claim of activation safety; live activation is deferred.

### Task 3: C — Version governance

Own assigned changes to `renovate.json5`, `.github/dependabot.yml`,
`infra/09-tooling/renovate/`, existing tech-stack synchronization and its tests,
version exception sources and the 0086 version-operations package. The runtime
source/projection/updater matrix is the interface to E/G. Prove source coverage,
missing/ambiguous-source rejection and non-overlap with focused regressions;
run projection checks, official strict validators and safe dependency extraction.
Specification and quality/security reviews check digest/floating and automerge
policy against actual configuration before closure.

### Task 4: D — Stage 99 documentation contracts

Own only demonstrated gaps in assigned Stage 99 templates/registry fields and
focused contract tests. A/E's coverage audit is input; the typed document and
README responsibility contract is output to E. Coordinate operations-catalog
changes with G. Test valid and invalid fixtures if an invariant changes, then
run metadata/contracts checks. Specification and document-quality reviewers must
confirm one canonical owner and no new filler obligations.

### Task 5: E — Stage 05 and README convergence

Own assigned `infra` root/tier/service READMEs and retained-component Stage 05
Guide/Policy/Runbook text after A/B/C/D interfaces stabilize. Consume measured
profiles, runtime authority, current native/gateway auth and public schemas.
Do not change C's 0086 or B's POL-0078 files concurrently. Check actual paths,
substantive normal operation/recovery coverage, runtime-literal exceptions,
metadata, links and catalog. Specification and documentation/security reviews
verify commands and authentication claims against current implementation.

### Task 6: F — Environment and secret metadata

Own assigned public `.env.example`, public registry example, existing
`gen-secrets.sh` synchronization and focused tests. A's key/ID/grant inventory
and B/C/R's changed consumers are input; unique current mappings and safe sync
contract are output to E/G. Classify every public key as `ACTIVE_REQUIRED`,
`ACTIVE_OPTIONAL`, `MIGRATION_ONLY`, `DEPRECATED` or `ORPHAN`; verify consumers
and migration-only confinement instead of treating schema shape as closure.
Test duplicate/orphan/missing mappings and literal service-secret references.

Require ID-based merge and existing value preservation, with the private
registry otherwise identical to the public one (order, dates and text; owner
decision 2026-09-24), unknown and removed IDs retained by default, and no secret-file deletion. Pruning is permitted only
as an exact explicit exception; prior prune approval is not blanket permission.
Check mode must reject private targets unless they are regular non-symlink files
with mode exactly `0600`; write mode must use atomic replacement and normalize
both existing targets to `0600`. Test `0644`/`0660`, symlinks and non-regular
targets for both files, synthetic value preservation, rollback and zero value
output. Actual local private
sync is a separately bounded execution checkpoint, never a request to copy
private files into this worktree. Specification and security review must confirm
preservation and exact authorization before any private metadata write.

### Task 7: G — Validator integration and whole-branch review

Own assigned existing operations-catalog/validation integration and shared tests,
with explicit file handoff from B/C/D/F/R; do not create a duplicate checker.
G accepts R's lifecycle validator, shared-test and example changes through an
exact-path handoff and coordinates the relevant checks before integration.
Coordinate each unit's specification review, quality/security review, corrections
and scoped re-review. Run focused tests, registered changed/full gates, Compose,
metadata/links, relevant hardening and external validator checks. Record actual
exit codes and unavailable prerequisites in Task 0005 (A–G/R round). A distinct final reviewer
examines the whole branch and all nine criteria; the controller then prepares
reviewed logical commits and the PR report within the granted delivery scope.

### Task 8: R — Service rationalization and lifecycle implementation

R is a distinct implementer, not the read-only inventory unit. Consume A's
current 140-service inventory and compare actual consumers, declared dependencies,
data ownership, resource evidence, security, backup/recovery and official
upstream guidance before deciding HOME, DEV, OPTIONAL, LAB, REMOVE or MIGRATE.
Mark unknown actual usage explicitly; no removal follows merely from a missing
runtime observation or an OPTIONAL/LAB classification.

Own the authored disposition/decision cells in the existing
`docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`
only after explicit handoff from the inventory/documentation implementer. Before
any justified add/move/remove/replace, record the exact affected paths in Task
0005: `infra/<tier>/<component>/`, root `docker-compose.yml`, POL-0078, public
env/secret metadata, version/update sources and projections, root/tier/service
READMEs, applicable Requirement/Architecture/ADR and Stage 05 subjects, Stage 90,
validators/tests/examples. Transfer each shared path from its B–G owner or route
that part of implementation to that owner. Route lifecycle validators, shared
tests and examples explicitly to G; G accepts that exact-path handoff before
editing or integrating them. No concurrent writers or second inventory authority. If current evidence justifies no lifecycle change, document
that decision and its uncertainty rather than inventing a removal.

Acceptance: each disposition has cited consumer/data/resource/recovery rationale,
all lifecycle interfaces remain closed, and relevant include/profile/env/secret,
version and documentation checks pass. Independent specification and
quality/security reviews cover both decisions and resulting diffs, followed by
correction and scoped re-review. Persistent data, secret files and live services
remain untouched; a repository decision cannot authorize runtime migration,
credential rotation, volume deletion or rollout.

### Task 9: Optional capability restructure (2026-09-21 follow-up)

Base main `ea3a7480d567acefa038417a2620aff497a30b72`, isolated branch
`claude/home-dev-restructure`. Scope: recover `validation-full`, then apply the
domain-selective restructure chosen in
[Task 0007](tasks/tsk-0007-optional-capability-restructure.md) over the
keep-and-patch and full-separation alternatives. The shared base (management
database, MinIO, Kafka Connect, gateway) keeps its data, identifiers and
activation; MLflow, dbt and Debezium each own a provisioning job, SQL, grants,
secret and Stage 05 triplet, sharing only an input-validating runner. Security
corrections (SSO bypass, token forwarding, Grafana anonymous access) are separate
logical commits. Task 0007 owns the before/after tree, file move table,
dispositions, verification, rulings and the approval-gated activation list;
activation, private secret synchronization, builds and CDC registration remain
separately approved.

### Task 10: Storage, secret custody, network and lakehouse convergence (2026-09-22)

Base main `1ac49fd3534ddf5ca324ea5874403513bd0c2592`, isolated branch
`refactor/spec-0180-platform-convergence`. Stages S00→S19 run strictly in
sequence; each stage re-reads the shared files changed by the previous stage,
updates code, README, Stage 05, env/secret metadata, profiles, version
projection and tests together, runs its unit and negative checks plus the
accumulated regression set, and is reviewed before the next stage starts.
A stage may end `SOURCE_READY/LIVE_PENDING`; that never satisfies a later
stage's cutover or data-disposal condition. The earlier A–G/R parallel units do
not apply. [Task 0008](tasks/tsk-0008-storage-security-lakehouse-convergence.md)
owns the move table, duplicate rulings, communication table, evidence and the
approval-gated live list.

### Original work-unit correspondence

W1 inventory/research maps to A; W2 architecture/profile maps to B/R; W3 Stage 99
maps to D; W4 profiles/navigation/operations maps to B/E; W5 version governance
maps to C; W6 environment/secret contracts maps to F; W7 validation/review maps
to G. W8 metadata/deployment preparation maps to F/G with live execution deferred
until concrete approval; Tasks 0007 and 0008 later ran approved live steps. W9 delivery maps to G after review and gates; prior
PR/commit evidence remains in its original Task. No identifier is reused or
historical execution result overwritten.

## Risk and Rollback

Profile changes can activate persistent services or maintenance jobs. Validate
activation sets statically before any live action. Preserve configuration in Git;
restore reviewed paths from the baseline only after checking concurrent edits.
Configuration rollback cannot reverse a database migration or substitute for a
verified backup. Preserve existing data volumes and private values. A storage
or memory snapshot does not prove a sustainable HOME workload.

Repository edits do not authorize start/stop/restart/recreate, pull/build,
update jobs, IaC apply, secret rotation, migration, volume mutation, reboot,
DNS/firewall or remote settings. Present exact targets, blast radius, preflight,
verification and recovery before requesting any newly necessary runtime action.
Do not prune Docker data or change the running main-worktree bind sources.

## Verification

Run meaningful negative/positive regressions before validator repairs. Inspect
current CLI help, then use existing Compose, operations-catalog, document
metadata/links, changed/full CI, relevant hardening and version registry gates.
Secret `--check`/`--dry-run` evidence must state whether the public-only isolated
worktree can satisfy private-file prerequisites. Do not copy secrets into it to
make a check pass. Use the official Renovate strict repository/global validators
and safe dependency extraction without networked PR creation. Tool/environment
blocks remain named limitations with actual exit codes.

Independent reviews cover specification and quality/security for each changed
unit, then the complete branch. Re-run affected checks after corrections;
record the tested revision and subsequent evidence-only edits. Finishing the
branch requires reviewed logical commits, final diff/gate evidence and a PR
report with residual risks. Push/PR actions follow the owner's exact granted
scope and repository boundary; merge remains separately authorized.

## Rulings

The owner explicitly selects subagent-driven implementation. Apply
`executing-plans` for critical plan review, checkpoints and tracking even though
the installed procedure recommends inline execution; the explicit workflow
choice governs. Routine repository design choices already have approval.
Task 0005 (A–G/R round), then Tasks 0007 and 0008, record each ruling's decision, evidence, what could be wrong and cost
if wrong. Skills and scratch coordination files do not create another Plan or
execution authority. Completed OpenBao/OIDC acceptance stays completed within
its historical scope; broader HOME cold-start/reboot/restore and measured
resource acceptance remain independently unverified.
