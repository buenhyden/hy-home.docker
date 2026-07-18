---
status: active
artifact_id: spec:133-target-surface-contract-convergence
artifact_type: spec
parent_ids:
  - spec:131-document-corpus-lifecycle-migration-foundation
---

# Target Surface Contract and Deprecated Runtime Convergence Design Specification

**Date:** 2026-07-18 (Asia/Seoul)

**Status:** Active

## Overview

This specification defines an evidence-gated convergence wave for every tracked
file below `.github/`, `archive/`, `examples/`, `infra/`, `projects/`,
`scripts/`, `secrets/`, and `tests/`, together with the direct Stage 00,
Stage 01 through Stage 05, Stage 90, Stage 99, root-environment, validator, and
generated-output fallout required to keep those targets internally consistent.

The approved approach is contract-first rather than a mechanical corpus
rewrite. Each path is classified by its real consumer and native format before
metadata, sections, lifecycle, duplication, deprecation, or deletion decisions
are made. Shared rules stay in Stage 00 or Stage 99; README files retain only
profile-specific navigation and local usage context; native GitHub, Compose,
YAML, JSON, script, configuration, and MDX surfaces keep their native consumer
contracts.

Read-only inspection at the approved baseline found 422 tracked target files:
15 under `.github`, one under `archive`, eight under `examples`, 273 under
`infra`, 52 under `projects`, 42 under `scripts`, 19 under `secrets`, and 12
under `tests`. The target contains 75 README files. Seventy-four inspected
README files already contain the six core navigation headings, but they expose
50 distinct optional-section combinations. Only four inspected Markdown files
carry frontmatter. These facts require consumer-aware normalization, not bulk
frontmatter insertion or a uniform body copy.

The tracked quality workflow currently defines 15 local job names. The latest
read-only remote observation recorded 12 required contexts and no deployment
environment; that dated difference remains `Needs Revalidation`. This wave may
correct tracked workflow and validator contracts, but it cannot present a
local definition as remote enforcement or add an unapproved CD target.

The user explicitly approved destructive cleanup, protected-surface contract
changes, direct-consumer migration, removal of deprecated implementations, and
Subagent-Driven Development. In particular, the previous compatibility
retention choice for InfluxDB 2 was superseded: the InfluxDB 2 server Compose
variant and its obsolete consumers must be removed, while current InfluxDB 3
Core behavior becomes the sole analytics time-series contract.

## Boundaries and Inputs

### Approved Scope

- Classify every tracked target path in a reviewed migration manifest.
- Reconcile document types, README profiles, frontmatter consumers, section
  envelopes, shared-rule ownership, links, stale prose, and template claims.
- Separate Vault/content archive behavior at root `archive/**` from SDLC
  provenance tombstones under `docs/98.archive/**`.
- Remove deprecated runtime definitions and migrate their direct consumers.
- Remove verified duplicate or orphaned examples and configuration files only
  after consumer and rollback evidence is complete.
- Improve repository validators, fixtures, local QA routing, and tracked
  GitHub Actions definitions needed to enforce the approved contracts.
- Refresh the canonical research, audit, generated, and Stage 04 evidence
  owners affected by the implementation.
- Use logical commits, independent task reviews, whole-branch review, and the
  controlled all-files pre-commit wrapper.

### Direct-Impact Exception

The primary file scope does not authorize unrelated repository cleanup. It does
authorize direct consumers outside the listed roots when leaving them unchanged
would make an approved target change false or broken. The direct-impact set
includes the InfluxDB requirement, architecture, decision, Spec, operations,
and root example-environment surfaces; Stage 00 and Stage 99 contract owners;
Stage 04 Plan and Task evidence; Stage 90 research, audit, and generated data;
and generated Graphify output when the CLI is available.

Every direct-impact path must appear in the wave evidence with the target path
that requires it. An adjacent file is not in scope merely because it is nearby.

### Non-goals

- Starting, stopping, recreating, or probing a Compose service.
- Executing a data migration, backup, restore, deployment, promotion, release,
  rollback, or remote GitHub configuration mutation.
- Reading or recording secret values, credentials, tokens, private keys,
  authentication files, shell history, or raw secret-bearing logs.
- Treating `docker compose config` output as safe persisted evidence when it
  could contain expanded secret-adjacent values.
- Rewriting historical Task, audit, regression, or memory evidence solely to
  remove the words `legacy` or `deprecated`.
- Adding Markdown frontmatter to native platform or machine-readable files for
  visual uniformity.
- Replacing topic-specific README content with unedited template prose.
- Claiming remote required checks, live provider behavior, runtime readiness,
  CD, or supply-chain maturity from tracked definitions alone.

### Canonical Inputs

- [Spec 131: Document Corpus Lifecycle Migration Foundation](../131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Spec 130: Template Contract System Canonicalization](../130-template-contract-system-canonicalization/spec.md)
- [Spec 129: Document Contract Canonicalization](../129-document-contract-canonicalization/spec.md)
- [Data analytics PRD](../../01.requirements/005-data-analytics.md)
- [Data analytics ARD](../../02.architecture/requirements/0012-data-analytics-architecture.md)
- [Analytics engine ADR](../../02.architecture/decisions/0015-analytics-engine-selection.md)
- [Data analytics Spec](../005-data-analytics/spec.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Corpus migration contract](../../99.templates/support/corpus-migration-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)

### External Source Basis

External sources inform the local implementation. They do not define this
repository's path numbers, artifact IDs, lifecycle vocabulary, approval
authority, or secret-handling exceptions. The initial rolling-source review was
performed on 2026-07-18 KST. On 2026-07-19, only the exact high-risk official
URLs for GitHub workflow/security/deployment/rulesets, pre-commit, DORA, Docker
Compose include/profiles/secrets/trust, SLSA v1.2, and NIST SP 800-61 Rev. 3
were re-opened; no stale claim was confirmed. Lower-risk retrieval dates and
the provider-model cutoff remain owned by the canonical research pack.

| Official or primary source | Local design consequence |
| --- | --- |
| [YAML 1.2.2](https://yaml.org/spec/1.2.2/) and [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) | Parse duplicate-safe typed metadata before profile validation; keep required, optional, forbidden, and conditional fields machine-readable. |
| [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) and [GitHub YAML frontmatter guidance](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) | Validate Markdown bodies separately and permit metadata only for a declared consumer. |
| [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) and [secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) | Validate explicit permissions, concurrency, timeouts, full-commit action pins, and untrusted-input boundaries without claiming remote enforcement. |
| [GitHub workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) | Retain the repository's current upload prohibition; this source defines the mandatory name, retention, and integrity review if a later approved contract introduces uploads. |
| [pre-commit](https://pre-commit.com/) | Treat all-files execution as repository-wide and potentially mutating; agents use only the approved clean-worktree wrapper. |
| [Docker Compose file reference](https://docs.docker.com/compose/compose-file/), [profiles](https://docs.docker.com/compose/how-tos/profiles/), [secrets](https://docs.docker.com/compose/how-tos/use-secrets/), and [trust model](https://docs.docker.com/compose/trust-model/) | Validate native Compose syntax and every declared profile statically, preserve per-service secret grants, and treat Compose inputs and rendered output as potentially sensitive. |
| [InfluxDB 3 Core write API](https://docs.influxdata.com/influxdb3/core/api/write-data/) and [Python v3 client](https://docs.influxdata.com/influxdb3/core/reference/client-libraries/v3/python/) | Make database/token and the v3 line-protocol API the sole new-workload contract; remove the unused InfluxDB 2 server and client scaffolding rather than retain an unowned compatibility path. |
| [NIST SP 800-53 Rev. 5.1 AU-11](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), [Git cat-file](https://git-scm.com/docs/git-cat-file), and [Library of Congress preservation glossary](https://www.loc.gov/programs/digital-collections-management/about-this-program/glossary/) | Base retention on explicit need, verify immutable commit/blob provenance, and use fixity only for approved evidence snapshots. |
| [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) and [Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | Record safe ownership and workflow metadata, never secret values or raw diagnostic payloads. |

### Current Implementation Evidence Candidate

At commit `49c4db893a4b53ac6b0e8a4dfe4e76d81c16ddc2`, Tasks 1 through 5 and
the bounded SeaweedFS duplicate disposition are implemented and independently
reviewed. The canonical manifest has 483 rows: 3 delete, 7 migrate, and 473
preserve; exactly the InfluxDB 2, OpenSearch `.example`, and SeaweedFS
`security.toml` rows are `pass/pass`, while 480 remain `pending/pending`.
The retained SeaweedFS `.example` is unmounted and activation is a separate
approved runtime/security chain. Task 6 authored research/audit and fixed-order
generated evidence are complete; full verification, the controlled wrapper,
and whole-branch reviews are not yet closed.
Tracked workflow source names 15 local quality jobs; the dated remote
12-context observation remains unverified and no remote or runtime claim is
promoted by this candidate.

## Contracts

### Canonical Ownership

| Surface | Canonical owner |
| --- | --- |
| Agent authorization, protected paths, workflow, and QA duties | Stage 00 governance |
| Document families, README profiles, metadata, template, archive, retention, deprecation, and migration semantics | Stage 99 support and machine registries |
| Current requirement, architecture, decision, technical, execution, and operations truth | Stages 01 through 05 |
| Source-backed findings and generated inventories | Stage 90 |
| SDLC provenance tombstones and approved immutable snapshots | Stage 98 |
| Vault/content tombstones for non-SDLC content | Root `archive/**` under its distinct content-archive profile |
| Local navigation, setup, inventory, and troubleshooting context | The matched README profile |
| GitHub, Compose, YAML, JSON, MDX, script, and configuration syntax | The native consumer and its repository validator |

README files may summarize a shared rule only enough to route the reader to
its owner. They must not restate lifecycle algorithms, validator schemas,
security policy, deployment policy, or provider-neutral agent policy.

### Metadata and README Contract

- Every tracked target README must match exactly one registry profile.
- Frontmatter remains absent by default. A key is retained only when the
  profile permits it and names a current executable consumer.
- Repository, infrastructure root/tier, project, script, test, and secret
  README profiles forbid frontmatter unless their exact registered subtype
  says otherwise.
- Example README status and infrastructure support `layer` values are reviewed
  individually; no target receives or loses frontmatter by bulk rule.
- Required headings form a minimum navigation envelope. Optional headings are
  present only when the path has topic-specific content for them.
- GitHub-native Markdown and framework MDX remain unsupported/native metadata
  profiles and do not inherit repository README or lifecycle keys.

### Archive Contract Split

The machine registry exposes two path-selected archive profiles while retaining
the common semantic role `artifact_type: archive`:

1. `content-archive` matches root `archive/*.md` and `archive/**/*.md`. It preserves non-SDLC
   Vault/content provenance, has no SDLC parent relation, and does not present
   archived commands or prose as current operational guidance.
2. `sdlc-archive` matches `docs/98.archive/**/*.md`. It preserves a removed
   active-chain artifact and may carry verified parent or replacement relations
   allowed by the existing SDLC tombstone contract.

Both profiles require an immutable commit and blob, archive date and reason,
disposition, and preservation class. Git history is the default preservation
route. An immutable snapshot remains limited to audit, legal, or explicitly
approved evidence-preserve cases and requires confidentiality and fixity
evidence.

`archive/Windows-Network-IP.md` becomes a content tombstone. Its two `netsh`
commands remain retrievable from the pinned Git blob but are removed from the
current body because the file has no owner, prerequisites, validation,
rollback, or active consumer.

### Deprecated and Legacy Contract

`deprecated` is a transitional finding, not an indefinitely supported runtime
state. A current implementation marked deprecated must be resolved by one of
three dispositions in the approved wave:

- migrate every consumer to the replacement and delete the implementation;
- correct a false deprecated label when the implementation is actively
  supported and verified; or
- preserve only qualifying evidence through the matching archive profile.

Historical evidence, standards discussion, migration tests, and negative
fixtures may retain the term when it describes their actual purpose. A blanket
text deletion is prohibited.

InfluxDB 2 is a verified current implementation retirement, not a wording-only
cleanup. The wave removes `infra/04-data/analytics/influxdb/docker-compose.v2.yml`,
all active claims that the v2 server remains supported, v2-only example
environment keys, unconsumed `influxdb-client` image dependency, unconsumed
org/bucket wiring in k6 and Locust, and validators that require the legacy
server. The InfluxDB 3 Compose file, database/token model, HTTP line-protocol
write contract, health semantics, and operations route become canonical.

### Destructive Disposition Contract

Deletion, merge, move, and archive require a reviewed manifest row with the
current source, intended target, consumer scan, canonical replacement where
applicable, preservation class, rollback commands, specification verdict, and
quality verdict. Similar names or identical bytes are candidate evidence only.

- The mounted OpenSearch `userdict_ko.txt` remains; its identical, unreferenced
  `.example` duplicate is deleted.
- The unmounted SeaweedFS `security.toml` is deleted; the `.example` scaffold
  remains. Enabling that security file is a separate runtime decision.
- Empty `.gitkeep` files remain because each path preserves a different
  directory consumer.
- Storybook scaffolding remains unless consumer evidence proves a narrower
  deletion. The nonexistent `projects/storybook/mcp` gitlink claim is removed
  from its READMEs and the two source checks that special-case it.

## Core Design

### Dependency-Ordered Waves

| Task | Implementation boundary | Primary output |
| --- | --- | --- |
| T-TSC-001 | Contract, profile, baseline, and migration-manifest foundation | Distinct archive profiles, deprecated-resolution rule, reviewed path inventory |
| T-TSC-002 | README, example, and Storybook surface migration | Profile-conformant local documentation and canonical example Service |
| T-TSC-003 | Vault/content archive migration | Validated root archive tombstone and provenance coverage |
| T-TSC-004 | Deprecated runtime and duplicate cleanup | InfluxDB 2 retirement, consumer migration, and safe duplicate removal |
| T-TSC-005 | Validator, tests, and static CI/QA | Executable regressions and tracked workflow consistency |
| T-TSC-006 | Research, audit, generated evidence, and lifecycle closure | Current canonical evidence, controlled QA record, and final review ledger |

Each task receives a fresh implementation subagent, a specification reviewer,
and a quality reviewer. A task closes only after both reviews pass and its
logical commits, deviations, rollback, and validation evidence are recorded.
The whole branch then receives a fresh final review.

### Corpus Classification

The manifest begins from the immutable baseline commit and covers all 422
tracked target paths plus approved direct-impact paths. Each path is classified
as one of native platform, generated output, README, typed example, runtime,
configuration, executable script, test/fixture, secret metadata/scaffold,
content archive, or unsupported binary/static asset. Classification precedes
mutation.

The manifest uses schema version 2 while Foundation remains valid schema
version 1. Version 2 keeps the existing top-level identity fields, adds one
required `surface_class` per row, and splits the prior single `artifact_type`
into nullable `artifact_type_before` and `artifact_type_after`. This represents
native/static rows without inventing a document type and represents the root
content transition as `null -> archive`. Binary/static assets and native files
may be preserved or exempted with a real consumer and evidence. An exempt row
is not a permanent policy exception; it states why this wave preserves the
native contract.

### README and Example Migration

The 75 README files retain their topic-specific prose. The implementation
normalizes only conflicting, duplicated, unsupported, or stale sections and
frontmatter. It does not add optional sections merely to create a uniform
outline.

`examples/sample-web-service/service.md` is a copyable example of the canonical
Service form. It receives the registered Service metadata and required section
envelope, with content written specifically for the sample service. A focused
test binds the README's template-alignment claim to the actual registry rather
than comparing prose by eye.

### InfluxDB 3 Consumer Migration

The runtime-definition migration is static and source-based:

1. Remove the v2 server Compose file and every tracked direct reference.
2. Update the PRD, ARD, ADR, data analytics Spec, Spec index, infrastructure
   README, Guide, Policy, and Runbook to one InfluxDB 3 Core contract.
3. Remove v2-only example environment variables, client dependencies, and
   unused k6/Locust wiring after a fixed-string consumer scan confirms no
   executable use.
4. Replace legacy-specific validator expectations with absence, InfluxDB 3
   database/token, endpoint, health, and direct-consumer consistency checks.
5. Render the affected Compose definitions statically without starting a
   service or retaining expanded output.

If implementation discovers an executable v2 query consumer, an unmodeled data
migration need, or a runtime-only compatibility requirement, T-TSC-004 stops.
The task may not manufacture an InfluxDB 3 replacement without a separately
approved design.

## Interfaces and Data

### Migration Manifest

The canonical reviewed manifest lives under
`docs/90.references/data/governance/document-corpus-lifecycle/` and uses the
existing machine contract. Its wave name, baseline commit, generator, blocking
state, and entries are deterministic. Every selected source appears exactly
once.

Each destructive row records the source and target, artifact identity/type when
applicable, before/after lifecycle state, direct parents, disposition,
replacement, active consumers, partition plan, preservation class, safe
evidence, and independent verdicts. Evidence contains bounded paths, commands,
counts, and Git object identities only. It never embeds source bodies, secrets,
raw logs, or rendered Compose payloads.

The manifest is advisory during classification. It becomes blocking only after
every selected row is complete, both independent verdict sets pass, Stage 04
evidence records the exact promotion commits, and the machine validator accepts
the complete wave.

### Archive Metadata Interface

Both archive profiles share canonical provenance field names and ordering.
Their path-selected rules differ:

- content archive forbids SDLC `parent_ids` and requires a root-archive source;
- SDLC archive keeps the existing parent and conditional replacement rules;
- `current_replacement` is absent when no replacement exists, never a sentinel;
- snapshot keys are forbidden for the default Git-history class;
- commit/blob pairs must resolve to the same archived bytes.

### Static CI/QA Interface

Repository validators expose finding codes and safe paths rather than bodies.
The changed-path QA recommender routes modifications to the smallest sufficient
gate set. Workflow jobs use exact stable names so local definitions can be
compared with separately observed remote required contexts without claiming
that the remote state changed. The current repository contract continues to
forbid `actions/upload-artifact`; this work does not introduce an exception.
Any later artifact handoff requires a separately approved contract change with
explicit names, bounded retention, and integrity-aware producer/consumer
semantics. Test reports, traces, screenshots, and diagnostics remain
operational evidence, not content or SDLC archives.

## Failure Modes and Guardrails

| Failure mode | Required response |
| --- | --- |
| Zero or overlapping README profile matches | Stop; correct the registry or path classification before editing the README. |
| Frontmatter key has no executable consumer | Remove it through the reviewed row or preserve the file unchanged; do not invent a consumer. |
| Native file is mistaken for a Markdown lifecycle document | Restore the native schema and add a regression for the classification boundary. |
| Destructive candidate has unresolved consumers or unique content | Block its disposition and retain the source. |
| Archive provenance cannot resolve commit, path, and blob | Do not create or promote the tombstone. |
| Secret-like value or raw diagnostic appears in evidence | Fail closed without echoing the value; remove unsafe evidence and review the exposure path. |
| InfluxDB 2 executable query or data-migration dependency is discovered | Stop T-TSC-004 and request a separate runtime/data migration decision. |
| Static Compose validation requires secret expansion or service startup | Use structural checks only or stop; do not widen authority. |
| Workflow definition passes lint but remote enforcement is unknown | Report tracked-definition success and remote state as unverified. |
| Generated output differs outside declared owners | Restore unrelated output and investigate the owner before commit. |
| Subagent review finds a critical or important issue | Reopen the task, fix with a fresh review loop, and preserve prior verdict evidence. |

No task may use `git reset --hard`, history rewriting, broad deletion without a
manifest row, `--no-verify`, direct agent execution of all-files pre-commit, or
secret-bearing evidence to make a gate pass.

## Verification

### Contract and Unit Verification

- Focused metadata/profile tests cover README exact-one matching, native
  exclusions, content archive, SDLC archive, key order, conditional fields,
  provenance, and unsafe evidence rejection.
- Corpus lifecycle fixtures cover all dispositions, direct-impact consumers,
  deterministic serialization, promotion, and rollback.
- Example fixtures prove the sample Service instantiates the current Service
  contract without copied template instructions.
- Regression fixtures reject the phantom Storybook gitlink, removed duplicate
  files, InfluxDB 2 server path, v2-only environment wiring, and stale active
  documentation claims while permitting historical and negative-test use.

### Static Implementation Verification

- Run the metadata checker in changed/new, impacted-dependent, active advisory,
  and inventory freshness modes required by the current contract.
- Run repository contracts, traceability, implementation alignment, generated
  owner freshness, link checks, and the corpus lifecycle validator.
- Run Actionlint, YAML lint/syntax, ShellCheck/Bash syntax, Hadolint, applicable
  Python/Node tests, and the repository's static Compose validator.
- Validate workflow permissions, action pins, job names, timeouts, concurrency,
  untrusted-input boundaries, and continued absence of artifact uploads; keep
  the 15-local/12-remote comparison explicitly dated and unverified until a
  separate read-only remote revalidation is approved.
- Confirm every declared Compose profile still renders and that no command
  starts a service.
- Run fixed-string consumer scans for every removed path and dependency.
- Refresh Graphify after code changes when the CLI is available, then treat its
  output as advisory and corroborate it against tracked owners.

### Completion Gate

After task-level reviews pass, a fresh whole-branch specification and quality
review must report no unresolved critical, important, or minor findings. Only
then may the approved controlled wrapper execute `pre-commit run --all-files`
from a clean linked worktree. The Task records sanitized before/after snapshots,
hook exit, changed paths, unexpected paths, and formatter mutations. A later
lifecycle-only commit does not reuse or overstate earlier wrapper evidence.

## Agent Role and IO Contract

### Orchestration

- `workflow-supervisor` owns the six-task sequence, stop conditions, review
  independence, commit boundaries, and final branch handoff.
- `doc-writer` and `rules-engineer` implement human contracts and topic-specific
  corpus changes within approved rows.
- `infra-implementer` owns the source-only InfluxDB and configuration cleanup;
  it has no runtime or secret-read authority.
- `qa-engineer` implements validator fixtures, static gates, and sanitized
  evidence.
- `ci-cd-engineer` may change tracked CI definitions; `security-auditor` reviews
  workflow permissions and untrusted-input boundaries.
- Independent specification and quality reviewers remain read-only until a
  bounded remediation task is assigned.

### Inputs

- Approved Spec and later Stage 04 Plan.
- Immutable baseline commit and reviewed migration manifest.
- Current Stage 00/99 contracts and canonical audit.
- Official-source records with retrieval dates.
- Safe tracked paths, consumer scans, and validator diagnostics.

### Outputs

- Logical commits aligned with T-TSC-001 through T-TSC-006.
- Complete Stage 04 Task evidence with commands, results, reviews, deviations,
  rollback, and commit ledger.
- Updated contracts, target surfaces, tests, workflows, generated inventories,
  research, and audit truth.
- A final handoff that distinguishes source/static verification from runtime,
  remote, deployment, and data-migration evidence not collected.

### Permissions

Subagents may read tracked non-secret source and edit only their assigned task
scope. They may not read secret values, mutate remote systems, start services,
push, open a PR, merge, or execute the all-files wrapper before the final gate.
All destructive edits require a reviewed manifest row and reversible logical
commit.

## Related Documents

- [Stage 03 index](../README.md)
- [Spec 131: Document Corpus Lifecycle Migration Foundation](../131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Spec 130: Template Contract System Canonicalization](../130-template-contract-system-canonicalization/spec.md)
- [Spec 129: Document Contract Canonicalization](../129-document-contract-canonicalization/spec.md)
- [Data analytics Spec](../005-data-analytics/spec.md)
- [Canonical audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Common document contract](../../99.templates/support/common-document-contract.md)
- [SDLC document contract](../../99.templates/support/sdlc-document-contract.md)
- [Corpus migration contract](../../99.templates/support/corpus-migration-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
- [Postflight checklist](../../00.agent-governance/rules/postflight-checklist.md)
