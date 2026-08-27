---
profile_id: spec
status: active
artifact_id: SPEC-0153
artifact_type: spec
parent_ids:
  - SPEC-0136
created: 2026-08-20
updated: 2026-08-21
supersedes:
  - SPEC-0136
---

# Workspace Governance and SDLC Simplification Specification

## Overview

This specification defines the successor taxonomy for repository documentation,
AI-agent governance, templates, validation, and lifecycle evidence. When
activated, it supersedes the target-state design in Spec 0136 without rewriting
that specification's completed migration history. The Operations catalog work
already completed under Spec 0136 is an input to this specification, not work to
repeat.

The design uses a staged, authority-first migration. Stage 99 first becomes the
single machine authority for document paths, profiles, identifiers, sections,
templates, and lifecycle. Stage 00 then converges to provider-neutral policy,
role, provider, and skill ownership. Documentation stages and executable gates
move only after those authorities can validate the destination shape.

The final repository supports Claude and Codex. Gemini and Antigravity governance,
models, adapters, shims, projections, tests, and generated surfaces are retired.
The `.agents/` surface remains only as a generated compatibility projection of
provider-neutral Stage 00 skills used by the supported runtimes.

## Boundaries and Inputs

### In scope

- `docs/00.agent-governance/`
- `docs/01.requirements/`
- `docs/02.architecture/`
- `docs/03.specs/`
- residual `docs/04.execution/` content after its owning work completes
- `docs/05.operations/`
- `docs/90.references/`
- `docs/98.archive/`
- `docs/99.templates/`
- `scripts/`, `tests/`, workflow, hook, and pre-commit consumers
- `.agents/`, `.claude/`, `.codex/`, `.gemini/`, and root provider shims
- root `DESIGN.md` as the UI and design-system authority

### Protected inputs

- Completed Spec 0136 implementation commits and evidence remain historical fact.
- The approved Operations subject meanings and role boundaries remain inputs.
- The concurrently active Spec 137 work is not modified by this specification's
  design commit. Its committed result must be integrated before migration touches
  the same Stage 04 or Stage 90 paths.
- External actions, remote runtime state, secrets, and credentials are out of
  scope unless a later task receives explicit approval.

### Current tracked baseline

The baseline is the committed HEAD from which the isolated design worktree was
created on 2026-08-20. Graphify predates that HEAD and is advisory; all
conclusions below were corroborated against tracked files, Stage 00, Stage 99,
and live stage documents. The implementation plan records commit identity only
where a recovery or provenance boundary requires it.

| Surface | Tracked files | Current state relevant to this design |
| :--- | ---: | :--- |
| Stage 00 | 111 | `rules/`, `scopes/`, `agents/`, `contracts/`, `providers/`, and project memory overlap |
| Stage 01 | 26 | 25 `prd-####` files plus README |
| Stage 02 | 53 | descriptions and decisions exist, but paths retain `ad-`/`adr-` prefixes |
| Stage 03 | 43 | mixed `spec-####` and one nonconforming prefixless package; package contents vary |
| Stage 04 | 7 | residual active execution evidence remains |
| Stage 05 | 209 | 75 current subject directories and 192 Guide/Policy/Runbook role files |
| Stage 90 | 121 | dated paths, redirect/evidence debt, and multiple category shapes remain |
| Stage 98 | 275 | archive volume exceeds the minimal ledger/tombstone target |
| Stage 99 | 49 | templates and support contracts duplicate path/profile rules |
| scripts | 80 | transitional wrappers and policy-owning validators remain |
| tests | 68 | large fixtures and monolithic validation suites remain |
| `.agents` / `.claude` / `.codex` / `.gemini` | 41 / 48 / 16 / 17 | three-provider projection is active even though the target supports two |

The current repository-contract monolith exits nonzero and still requires
deleted `docs/05.operations/guides/...` paths. This is a known baseline ownership
conflict, not evidence that those paths should be restored. The Operations
manifest itself passes its approved structural contract; its final index work is
absorbed by this successor plan.

This specification was initially committed under the legacy prefixed Stage 03
package profile. Task 2 established the prefixless Stage 99 profile, and Task 3
then moved the package natively to
`docs/03.specs/0153-workspace-governance-simplification/`. No compatibility copy
or redirect exists. The canonical lexical ID is `SPEC-0153`; the numeric
identity `0153` did not change during activation.

### External evidence and limits

| Source | Design implication | Limit |
| :--- | :--- | :--- |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Requirements information remains a distinct lifecycle authority. | It does not prescribe this repository's folder names. |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Architecture Description and stakeholder concerns remain distinct from individual decisions. | It does not prescribe `descriptions/` or `decisions/` paths. |
| [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/spec-driven.md) | A feature specification can drive plan, task, and verification artifacts. | Its filenames are an implementation pattern, not an industry mandate. |
| [Diataxis](https://diataxis.fr/) | Explanatory guidance and task-oriented procedures should not be conflated. | It does not require separate top-level role roots. |
| [Google SRE incident response](https://sre.google/workbook/incident-response/) | Incident coordination and operational procedures require roles, records, recovery, and review. | The exact packet shape is repository policy. |
| [AGENTS.md](https://agents.md/) | A concise repository instruction entry point can route agents to scoped guidance. | Provider-native configuration still requires adapters. |
| [Claude Code directory reference](https://code.claude.com/docs/en/claude-directory) | Claude has a provider-native instruction and hook surface. | Claude mechanics do not define provider-neutral policy. |
| [GitHub artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations) | Provenance should bind an artifact to centralized source and workflow identity. | It does not justify copying SHAs into every document. |

The sources support responsibility separation, traceability, lifecycle, and
reviewability. The exact taxonomy below is the workspace's design decision.

## Behavior Contract

### Authority contract

| Concern | Sole authority |
| :--- | :--- |
| Human and AI-agent policy, roles, handoff, provider differences | Stage 00 |
| Document paths, profiles, identifiers, sections, lifecycle, templates | Stage 99 `registry.json` and its schemas |
| Executable validation and generation behavior | `scripts/` registered in `scripts/manifest.yaml` |
| Current requirements, architecture, behavior, and operations | Stages 01, 02, 03, and 05 according to role |
| External evidence, point-in-time audits, structured reference data | Stage 90 |
| Historical path and authority lookup | Git history plus minimal Stage 98 records |
| Runtime syntax and hooks | `.claude/` and `.codex/` adapters |
| Provider-neutral reusable skills | Stage 00 `skills/` |
| Runtime skill projection | Generated `.agents/skills/` and supported provider adapters |

No generated adapter, validator, template, README, migration, tombstone, or
reference document may redefine a rule owned by another row.

### Precedence contract

1. Direct system and user instructions.
2. Stage 00 policy and role authority.
3. Stage 99 typed document authority.
4. Current stage document according to its registered role.
5. Provider adapter syntax and runtime mechanics.
6. Stage 90 evidence and Stage 98 history.

Stage 90 and Stage 98 never override current policy or current product truth.

## Technical Approach

### Target repository taxonomy

This tree is the exhaustive documentation and AI-agent control-plane surface,
not an exhaustive listing of application and infrastructure roots. Runtime
roots such as `infra/`, `examples/`, `projects/`, and `secrets/`, plus repository
mechanics such as `.github/`, remain governed inputs and are not deleted by this
taxonomy.

```text
/
├── AGENTS.md
├── CLAUDE.md
├── DESIGN.md
├── docs/
│   ├── 00.agent-governance/
│   ├── 01.requirements/
│   ├── 02.architecture/
│   ├── 03.specs/
│   ├── 05.operations/
│   ├── 90.references/
│   ├── 98.archive/
│   └── 99.templates/
├── scripts/
├── tests/
├── .agents/
├── .claude/
└── .codex/
```

`docs/04.execution/`, `.gemini/`, `GEMINI.md`, and
`docs/05.operations/releases/` do not exist in the final tree.

### Stage 00 governance

```text
docs/00.agent-governance/
├── README.md
├── sdlc.md
├── policies/
├── roles/
├── providers/
│   ├── README.md
│   ├── registry.yaml
│   ├── claude.md
│   └── codex.md
└── skills/
```

- `rules/` and `controls/` converge into normative `policies/`.
- `scopes/` and canonical agent definitions converge into `roles/`.
- reusable function procedures converge into `skills/`.
- document path/profile/template facts move to Stage 99.
- provider model and capability facts move to `providers/registry.yaml`.
- project `memory/` is removed. Current state belongs to the owning Spec task;
  reusable content moves by meaning to policy, skill, operations, or reference.
- root `AGENTS.md` and `CLAUDE.md` remain concise bootstrap shims.
- `.agents/` owns no policy or skill source. It is a generated compatibility
  projection of Stage 00 skills required by Claude and Codex. Projection parity
  and freshness are executable validation obligations.
- Gemini and Antigravity identifiers, adapters, projections, tests, generated
  outputs, model records, and shims are removed.

### Stage 01 requirements

```text
docs/01.requirements/
├── README.md
└── 0001-<slug>.md
```

One Requirement Package owns the problem, goals, users and stakeholders,
functional and non-functional requirements, constraints, implementation-
independent external interface requirements, acceptance criteria, and links to
Architecture and Spec packages.

- Package ID: `REQ-0001`.
- Functional requirement: `REQ-0001-FR-0001`.
- Non-functional requirement: `REQ-0001-NFR-0001`.
- Interface requirement: `REQ-0001-IF-0001`.
- Cross-document traceability always uses the full ID.
- PRD, SRS, and Interface Requirement profiles and templates are retired.
- OpenAPI, GraphQL, and Proto are Stage 03 implementation contracts, not Stage
  01 requirements.

### Stage 02 architecture

```text
docs/02.architecture/
├── README.md
├── descriptions/
│   └── 0001-<slug>.md
└── decisions/
    └── 0001-<slug>.md
```

- Paths omit `ad-` and `adr-`; the parent directory determines the type.
- Frontmatter IDs remain `AD-0001` and `ADR-0001`.
- Architecture Description owns current boundaries, components, data flow,
  deployment views, and quality views.
- ADR owns one structurally significant choice, alternatives, decision, and
  consequences.
- Superseded ADRs remain in the decision log and cross-link the successor.
- The forbidden Stage 02 requirements subdirectory is not restored.
- Long-lived design material moves from old Stage 03 `design.md` content to an
  ADR or Architecture Description; change-local detail moves into `spec.md`.

### Stage 03 specification and execution

```text
docs/03.specs/
├── README.md
└── 0001-<slug>/
    ├── README.md
    ├── spec.md
    ├── contracts/
    │   ├── openapi.yaml
    │   ├── schema.graphql
    │   └── service.proto
    ├── plan.md
    └── tasks/
        └── tsk-0001-<slug>.md
```

- The package ID remains `SPEC-0001` in frontmatter; the path omits `spec-`.
- The tree above is the active-execution package shape. A completed living
  package normally retains only `README.md` and `spec.md` after the lifecycle
  cleanup described below.
- `design.md` and `tests.md` are not document roles.
- `spec.md` owns goals, exact behavior, Technical Approach, interfaces,
  Acceptance Contract, and failure conditions.
- `contracts/` is optional and contains executable interface contracts owned by
  the package. The registry declares allowed deterministic filenames and media
  types; `spec.md` links every owned contract. These payloads have machine
  profiles and templates but are not additional prose document roles.
- `plan.md` owns implementation sequence, dependencies, risk, verification,
  commit boundaries, rollback, and recovery.
- task documents own bounded execution and review evidence.
- `plan.md` and tasks exist only while the change is being executed.
- After implementation, a current behavioral contract remains as `spec.md`.
  Plan/task evidence is summarized into the current contract, Operations, or
  deployment history as appropriate, then removed from the current tree and
  retained by Git history.
- A completed one-time migration package is removed after its minimal Migration
  or Tombstone record is committed.
- Root `DESIGN.md` is a separate UI/design-system authority for color,
  typography, component, accessibility, and interaction rules only.

### Stage 05 operations

```text
docs/05.operations/
├── README.md
├── catalog/
│   └── <domain>/
│       ├── README.md
│       └── 0001-<subject>/
│           ├── guide.md
│           ├── policy.md
│           └── runbook.md
└── incidents/
    └── <year>/
        └── inc-0001-<slug>/
            ├── incident.md
            └── postmortem.md
```

- The approved domain/subject structure and completed semantic convergence are
  retained.
- Subject paths remove the `ops-` prefix; stable frontmatter IDs remain.
- The subject directory number binds to a registered subject identity. Role
  artifact IDs are independent stable member identities and are not renumbered
  after an approved merge. For example, subject `0051` may retain
  `policy-0052` when the Operations migration manifest records that membership.
  Validators require subject-path-to-subject identity agreement and exact
  registered role membership instead of equating every role ID to the subject
  number.
- Guide, Policy, and Runbook are optional roles. A subject contains only roles
  with distinct owners, purposes, triggers, or verification obligations.
- Role documents merge only when owner, scope, trigger, and validator evidence
  all agree.
- Every retained, renamed, merged, or removed role has one migration-manifest
  row recording source and final route, subject and role identity, owner, scope,
  trigger, verification evidence, active consumers, and body-preservation
  witnesses. A role disposition without that row fails closed.
- Incident year containment and `inc-####` are the only date/path prefix
  exception.
- `releases/` and Release profiles, IDs, templates, indexes, fixtures, and gates
  are removed.
- Deployment procedure and rollback belong to a Runbook. Completion and
  verification belong to the Spec. Durable public change history belongs to the
  repository's existing changelog and Git tags. Historical execution detail
  belongs to Git history.

### Stage 90 references

```text
docs/90.references/
├── README.md
├── research/0001-<slug>/
├── audits/0001-<slug>/
└── data/0001-<slug>/
```

- Package README owns `RES-0001`, `AUD-0001`, or `DATA-0001`.
- Research owns external evidence and analysis.
- Audit owns a point-in-time gap or conformance assessment.
- Data owns repository inventories and structured reference payloads.
- `learning/` moves by purpose to a Stage 05 Guide or Stage 90 Research.
- `res-` and `aud-` path prefixes and dates are removed.
- Deprecated redirect documents are removed.
- References to obsolete paths become Git or Archive evidence, not current
  clickable links.

### Stage 98 archive

```text
docs/98.archive/
├── README.md
├── migrations/0001-<slug>.md
└── tombstones/<original-stage>/0001-<slug>.md
```

- Git history is the default full-content archive.
- Migration records only large path or authority mappings.
- Tombstone records only the previous stable path, replacement, reason, status,
  and recovery commit.
- Full retired Spec/Plan/Task copies are absent unless a separately approved
  legal or audit requirement exists.
- Active documents link to the Archive README or a Migration, not individual
  Tombstones.
- Line-number SHAs and whole-archive snapshot counts are removed.
- Superseded ADRs remain in Stage 02.

### Stage 99 templates and document registry

```text
docs/99.templates/
├── README.md
├── registry.json
├── contracts/
│   ├── frontmatter.schema.json
│   └── document-profile.schema.json
└── templates/
    ├── governance/
    ├── requirements/
    ├── architecture/
    ├── specs/
    ├── operations/
    ├── references/
    ├── archive/
    └── common/
```

`registry.json` is the only machine authority for canonical path patterns,
profile IDs, artifact IDs, internal IDs, issued-ID allocation state, required and
optional sections, lifecycle states and transitions, traceability relationships,
template IDs, and exceptions.
Schemas validate the registry and frontmatter. Templates reference a profile ID
and never hard-code a target path.

`support/` is removed after every live consumer reads the registry. Human
explanation lives in the Stage 99 README. `templates/changes/` converges into
`templates/specs/`. Separate PRD, SRS, Interface Requirement, design, tests,
Release, Gemini, and Antigravity templates are removed.

### Status and identity lifecycle

The registry defines exact status sets rather than combining an implicit common
set with profile-specific additions:

| Profile family | Allowed statuses | Allowed forward transitions |
| :--- | :--- | :--- |
| living Requirement, Architecture Description, Spec, Guide, Policy, Runbook, Research, and Data | `draft`, `active`, `superseded`, `retired` | `draft -> active|retired`; `active -> superseded|retired` |
| ADR | `draft`, `active`, `superseded`, `retired`, `rejected` | `draft -> active|rejected|retired`; `active -> superseded|retired` |
| Plan and Task | `draft`, `active`, `blocked`, `completed`, `cancelled` | `draft -> active|cancelled`; `active -> blocked|completed|cancelled`; `blocked -> active|cancelled` |
| Incident | `open`, `mitigated`, `closed` | `open -> mitigated|closed`; `mitigated -> closed` |
| Postmortem and point-in-time Audit | `draft`, `active`, `superseded`, `retired` | `draft -> active|retired`; `active -> superseded|retired` |
| Migration and Tombstone | `draft`, `completed`, `superseded` | `draft -> completed`; `completed -> superseded` |

Terminal states do not transition backward. An existing completed Spec is
classified deterministically as either an `active` living contract or a retired
one-time package; an existing archived document becomes a Tombstone/Migration or
is removed after Git recovery proof. Completed Plans and Tasks are summarized
and removed according to the Stage 03 lifecycle.

Replacement uses `supersedes` and `superseded_by`. Because Spec 0153 is still a
draft under the legacy profile, `parent_ids` records its current lineage. In the
activation unit, the Stage 99 migration atomically adds the forward
`supersedes: [SPEC-0136]` relation to Spec 0153 and the reverse `superseded_by`
relation to Spec 0136 without changing Spec 0136's completed migration evidence.

Each registry identity space owns monotonic allocation state. Bootstrap computes
the high-water mark from tracked documents and Git history, reserves every value
at or below that mark, and records the next allocatable number. Package-owned
FR/NFR/IF spaces maintain their own high-water marks. Issuance updates allocation
state atomically with the new artifact, and deletion never lowers a mark. This
conservatively prevents reuse even after the current document is removed.

Final canonical package IDs use uppercase `REQ-`, `AD-`, `ADR-`, `SPEC-`,
`RES-`, `AUD-`, and `DATA-`. The migration preserves each numeric identity,
records lowercase-to-uppercase aliases only as migration evidence, rewrites all
active inbound traces atomically, and rejects lowercase aliases afterward.
Numeric path-to-artifact agreement applies to standalone numbered packages.
Operations role members use the explicit subject-membership rule defined above.

## Interfaces and Data

### Document registry record

Each registry profile defines at least:

```json
{
  "profile_id": "requirements-package",
  "path_pattern": "docs/01.requirements/{number:4}-{slug}.md",
  "artifact_id_pattern": "REQ-{number:4}",
  "identity_relation": "direct",
  "template_id": "requirements/package",
  "required_sections": [],
  "optional_sections": [],
  "statuses": ["draft", "active", "superseded", "retired"],
  "traceability": {},
  "exceptions": []
}
```

The registry also contains an `identity_spaces` collection with the canonical
prefix, width, high-water mark, next number, and package-owned child spaces. It
does not reproduce retired document bodies; it records only allocation state
needed to make non-reuse enforceable.

The final schema determines the exact JSON representation. The semantic
requirements above are binding; field spelling that improves schema clarity may
change in the implementation plan without changing this contract.

### Script ownership

```text
scripts/
├── README.md
├── manifest.yaml
├── docs/
├── setup/
├── qa/
├── validation/
└── lib/

tests/
├── docs/
├── setup/
├── qa/
├── validation/
└── lib/
```

- CLIs parse arguments and render results only.
- Side-effect-free logic lives in focused library modules.
- Top-level tests mirror production responsibilities.
- `scripts/manifest.yaml` alone owns script lifecycle, successor, behavioral
  consumers, tests, generator ownership, and explicit write capability.
- One-time migration helpers are removed in the logical commit that consumes
  them.

### Gate topology

The final validation graph exposes exactly six public responsibility suites:

1. `document-contract`
2. `document-graph`
3. `document-lifecycle`
4. `operations`
5. `agent-governance`
6. `repository-integrity`

Each suite is an aggregate over small, focused validators registered in
`scripts/manifest.yaml`; the suite itself contains no validation logic.
`repository-integrity`, for example, composes existing focused Compose,
dependency, frontend, supply-chain, workflow, and repository-syntax validators
without merging their implementations or fixtures. Every atomic validator maps
to exactly one public suite, and `run-ci-gate.py --explain` emits that mapping.

`run-ci-gate.py --profile changed` selects impacted suites and their validators.
`--profile full` runs all suites. Local, pre-commit, PR, push, and final
verification use the same atomic implementations. Hooks and workflows select
profiles and do not reimplement policy.

### Fixture contract

- Registry-driven builders create the smallest valid artifact for each profile.
- A fixture never copies the whole repository tree.
- Tests do not duplicate current file counts or a complete current-path list
  unless that value is the tested invariant.
- Each validator owns one valid fixture and focused boundary mutations.
- Symlink, containment, path traversal, invalid UTF-8, and unsafe write behavior
  retain explicit adversarial coverage.
- Long integration fixtures run only in the full profile.

### SHA and provenance contract

SHAs remain only for external security pins, Migration/Tombstone recovery,
canonical generated-artifact provenance, and runtime CI base/head selection.
Markdown branch snapshots, line-number SHAs, duplicated digests, and fixed-HEAD
fixtures are removed. One canonical provenance record is referenced by identity.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Current validators demand a predecessor path | Stage 99 authority and registry consumers migrate before corpus paths; predecessor paths are never recreated. |
| The migration creates two active authorities | Source paths are accepted only through an approved Migration row, never through a second legacy profile. |
| A bulk replacement corrupts history or unrelated text | Only registry/manifest-selected current consumers are rewritten; Stage 90/98 evidence is classified explicitly. |
| An Operations merge loses unique procedure or policy meaning | Merge requires equal owner, scope, trigger, and verification obligations plus body-level preservation tests. |
| A path move breaks generated outputs | Generator owner runs explicit write once, then check; generated files are never hand-edited. |
| Provider removal deletes neutral skills | Gemini/Antigravity selectors are removed, while shared skills are retained when Claude or Codex consumes them. |
| Stage 00 memory is removed before bootstraps stop loading it | Memory routing, root-shim rewrites, Stage 00 moves, provider projections, and bootstrap validation form one reversible logical unit; no commit may reference an absent memory path. |
| Deleting a current artifact makes its ID reusable | Registry allocation state advances monotonically and is verified against Git history during bootstrap; deletion cannot lower the high-water mark. |
| Stage 04 deletion races active Spec 137 | The Stage 03/04 task waits for the owning Spec 137 result and rebases from its committed state. |
| Archive minimization destroys the only recoverable body | Git object and recovery commit are verified before the current copy is removed. |
| A fixture passes because it mirrors implementation constants | Fixtures derive valid input from the registry and mutate one semantic boundary at a time. |
| Changed-path validation conceals broad breakage | Every task runs focused changed gates; each stage closes with a full responsibility gate; the branch closes with the full profile. |
| Current baseline failures are relabeled as success | The plan records command, exit, finding count, and owner. Nonzero is never described as PASS. |
| Concurrent work is overwritten | Work proceeds in an isolated worktree and does not stage or rewrite paths owned by another active task. |

## Acceptance Contract

### Migration sequence

1. Commit this approved specification and create `ADR-0029: Workspace
   Documentation and Agent Governance Authority` at the current-compatible
   `docs/02.architecture/decisions/0029-workspace-governance-authority.md`;
   move it natively to the prefixless path after the Stage 99/02 profiles permit
   that route.
2. Establish Stage 99 registry/schema/template authority and registry-backed
   validation.
3. In one reversible bootstrap unit, route durable memory content, rewrite root
   shims, converge Stage 00 and provider projections, validate bootstrap parity,
   and remove project memory, Gemini, and Antigravity.
4. Migrate Stage 01 and Stage 02 identities and content roles.
5. Migrate Stage 03 packages and remove Stage 04 after Spec 137 integration.
6. Remove Operations subject prefixes, merge proven duplicate roles, remove
   Releases, and align Incidents.
7. Simplify Stage 90 and Stage 98.
8. Split scripts/tests, reduce gates and fixtures, centralize provenance, and
   delete monoliths and one-time tools.
9. Repair cross-links and generated evidence, remove transition records, run
   full verification, and complete independent review.

### Acceptance Contract

The implementation is complete only when all of the following are true:

1. The final documentation and AI-agent control-plane tree contains only the
   approved documentation stages and supported provider surfaces; unrelated
   runtime and repository roots remain intact.
2. Stage 99 registry/schema/template validation is the sole document-contract
   authority; `support/` no longer duplicates it.
3. Stage 00 has only README, SDLC, policies, roles, supported providers, and
   skills; project memory and duplicate rules/controls/scopes are absent.
4. Gemini and Antigravity identifiers, models, adapters, shims, generated
   projections, tests, and directories are absent.
5. Requirement Packages use `REQ-####` and package-owned FR/NFR/IF IDs; legacy
   PRD/SRS/Interface profiles and prefixes are absent.
6. Architecture paths are prefixless; AD/ADR IDs remain stable; superseded ADRs
   remain linked in Stage 02.
7. Spec paths are prefixless; `design.md`, `tests.md`, and residual Stage 04 are
   absent; current living behavior remains in `spec.md`.
8. Operations retains domain/subject ownership, uses prefixless subject paths,
   has an exact reviewed disposition row for every role, preserves each stable
   role-to-subject membership, contains no role meeting all duplicate criteria,
   and contains no Releases surface.
9. Incident paths use the year/package exception and pass exact role/path checks.
10. Stage 90 contains only Research, Audit, and Data packages with prefixless,
    date-free identities.
11. Stage 98 contains only README, minimal Migrations, and minimal Tombstones;
    no ordinary full-content document archive remains. A pending Migration may
    retain schema-version-2 execution fields and pending/approved state, but its
    schema-version-3 durable rows contain only source, target, artifact, action,
    and non-null recovery commit mappings.
12. Script/test ownership mirrors by responsibility, transitional and duplicate
    tools are absent, and one-time helpers are deleted.
13. The validation graph contains the six canonical public suites, every focused
    validator maps to exactly one suite, and local and CI profiles invoke the
    same atomic implementations.
14. Fixtures are registry-driven and bounded; branch and line-number SHA
    duplication is absent while security/recovery provenance remains.
15. No active authority, generated index, or operational link points to a
    predecessor, Tombstone, removed provider, Release, or Stage 04 path; explicit
    `supersedes` and migration-evidence links remain allowed.
16. Registry allocation state prevents issued-ID reuse, standalone package
    numeric identities agree, Operations subject membership is exact, canonical
    ID case is enforced, and all requirement links use full IDs.
17. All six full-profile suites pass, generated outputs are fresh, diff hygiene
    passes, and independent specification and quality reviews have no Critical
    or Important finding.

### Commit and review contract

Each numbered migration unit is one or more logically reversible Conventional
Commits. Every implementation task uses RED, minimal GREEN, focused verification,
self-review, independent specification review, and independent quality review.
Unrelated files and concurrently owned paths are never staged. A failed gate
stops only its dependent unit; unrelated independent units may proceed when the
plan proves the separation.

## Agent Role and IO Contract

- `requirements-to-design-agent` audits Stage 01 to Stage 02 coverage and
  returns unresolved product choices upstream.
- `execution-plan-agent` creates the implementation plan only after this
  specification is approved and reviewed.
- `ops-runbook-agent` validates that retained Runbooks describe implemented,
  observable procedures with rollback and escalation.
- Stage 00 Rules/Policy engineering owns normative governance convergence.
- Stage 99 document-contract implementation owns registry/schema/template
  authority.
- Each implementation task is assigned to one fresh implementer and receives
  independent specification and quality review before the next dependent task.

No agent may infer approval for destructive external actions, runtime changes,
push, merge, or publication from approval of this repository migration.

## Implementation Evidence

Task 1 registered draft ADR-0029 and Migration 0003 without moving a corpus
source. The Migration began pending and now records exact user approval. The
initial RED proved the control-plane files were absent. That
RED also exposed a representation defect: a transition schema limited to
currently tracked sources could not safely describe an artifact created by one
Task and consumed by a later Task. The bounded Plan/Migration/Test correction
adds typed planned creations and sequential source provenance while preserving
the approved authority, lifecycle, and recovery contract in this specification.

The approved selection is frozen at commit
`889d3868ecd0913cddac79a718584a54a8453525`: `17` planned creations, `903`
structural transition rows, and `3,571` owner-ordered literal/Markdown consumer
edges. The derived-edge SHA-256 is
`2f1840983d98ed93ffdc183305c49b389b17e5c8362538e5df97d451be2b9139`; the
selection SHA-256, bound to the baseline, consumer policy, edge digest,
final-compaction contract, creations, and rows, is
`9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1`.
Focused validation currently passes `11/11`. Final independent specification
and quality re-reviews each report `C0/I0/M0`, with the earlier quality `I5` and
lifecycle `I1` addressed. The user approved the exact selection digest as
`user` on `2026-08-20`; the controller-owned Task 1 commit remains before any
transition executes.

## Traceability

- [Predecessor taxonomy specification](../0136-sdlc-taxonomy-convergence/spec.md)
- [Predecessor implementation plan](../0136-sdlc-taxonomy-convergence/plan.md)
- [Predecessor task evidence](../0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md)
- [Archive and migration lookup](../../98.archive/README.md)
- [Stage 00 governance hub](../../00.agent-governance/README.md)
- [Stage 99 template hub](../../99.templates/README.md)
- [ADR-0029: Workspace Governance Authority](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Migration 0003](../../98.archive/migrations/0003-workspace-governance-simplification.md)

ADR-0029 remains draft and Migration 0003 is approved; both remain uncommitted
until the controller closes the Task 1 control-plane unit.
