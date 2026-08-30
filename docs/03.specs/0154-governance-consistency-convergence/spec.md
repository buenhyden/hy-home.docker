---
profile_id: spec
status: draft
artifact_id: SPEC-0154
artifact_type: spec
parent_ids: [REQ-0024, ADR-0027, ADR-0029]
created: 2026-08-30
updated: 2026-08-30
---

# Governance Consistency Convergence Specification

## Overview

Stage 00 currently states rules that contradict each other, `roles/` holds two
incompatible document genres under one profile, the `spec` profile has no
terminal status, and 817 relative links across 93 documents resolve to retired
paths. Two Stage 98 migrations carry a status their lifecycle does not define.
The registered full CI gate passes while all of this is true.

It passes for two separate reasons. The link gate reads 342 of the 680 tracked
Markdown documents, so 798 of the 817 dead links are outside its selection.
And `check-document-metadata.py` does detect the two invalid statuses and names
them under `invalid-status`, but exits 0 because its full inventory runs in
advisory mode and blocks only on changed or new files, so a violation that
predates the rule is never raised as a failure.

This specification defines the convergence that removes those contradictions,
retires the superseded taxonomy still described by active documents, and closes
the gate scope hole that allowed the rot to accumulate unobserved. It reduces
authority surface; it does not add a validator, a fixture, or a gate node.

## Boundaries and Inputs

**Measured inputs.** Every figure is re-derivable at the commands in
`## Acceptance Contract`.

| Fact                                            | Value               |
| :---------------------------------------------- | :------------------ |
| Registered full-profile validators              | 22                  |
| Documents read by the link gate                 | 342 of 680          |
| Dead relative links                             | 817 across 93 files |
| Dead links inside Stage 90                      | 798                 |
| Stage 90 audit packs with `status: active`      | 32 of 38            |
| Spec Packages with `status: active`             | 28 of 30            |
| Active Spec Packages with zero Tasks            | 21                  |
| `roles/` documents carrying `agent_id`          | 14                  |
| `roles/` documents without `agent_id`           | 8                   |
| Stage 98 migrations with an invalid status      | 2 of 3              |
| Renderer outputs missing from `generated_roots` | 5                   |
| Metadata full-inventory enforcement state | advisory, guarded by a `ProfileError` |
| Records with metadata findings | 13 of 595 |
| Profiles registering a `Related Documents` section | 8 of 24 |
| Documents carrying that section in practice | 499 of 599 |
| Stage roots outside the link gate | `00`, `90`, `98` |

**In scope.** `docs/00.agent-governance/`, `docs/99.templates/registry.json`,
`docs/00.agent-governance/providers/registry.yaml`, `docs/README.md`,
`docs/90.references/audits/`, `docs/98.archive/migrations/`, the `Stage 04`
residue inside active Stage 03 Specs, the generated provider projections under
`.agents/`, `.claude/`, and `.codex/`, and the selection scope of
`scripts/validation/check-document-links.py`.

**Out of scope.** Validator internals, including the taxonomy-wave enforcement
state and the `docs/04.execution` literals pinned inside
`metadata_validator.py`, and validator and test volume reduction (SPEC-0155); the Compose
enablement model and `infra/` domain alignment (SPEC-0156), and every runtime
asset under `infra/`, `projects/`, `examples/`, and `secrets/`.

## Behavior Contract

1. No two Stage 00 documents state conflicting obligations about the same
   subject, and no Stage 00 document names an artifact type that the Stage 99
   registry does not define.
2. `docs/00.agent-governance/roles/` contains exactly the canonical agent roles.
   Every file there carries `agent_id`, and the Stage 99 `governance-role`
   profile requires the fields that determine runtime routing.
3. Every reusable procedure under `skills/` projects to a provider skill name
   that the runtime can actually surface.
4. A Spec Package can express completion. No Spec Package remains `active`
   solely because the vocabulary offers no terminal status.
5. Every status value present in the corpus is a member of its profile's
   registered lifecycle.
6. A section the Output Style Contract requires of every document is registered
   by every profile that document can carry.
7. No active document describes `Stage 04` or `docs/04.execution` as current
   procedure, and no active document outside Stage 98 publishes a legacy path
   redirect table.
8. Relative links resolve in every tracked Markdown document that is not
   `superseded`, and the registered link gate reads that same set.

## Technical Approach

### 1. Stage 00 canonical repair

Delete the contradicting statement rather than reconcile it, per the workspace
rule that prior content yields to current authority.

Two removals apply to all eight layer documents without triage:

- Every `File Ownership SSOT` table. These are the source of the permission
  contradiction: `roles/common.md` assigns `docs/03.specs/` and
  `.pre-commit-config.yaml` ownership to `code-reviewer`, whose canonical role
  is read-only, and `roles/security.md` lists the same hardening script twice
  in two rows.
- Every `Subagent Bridge` block. They instruct an `@import` of a role document
  into an agent preamble, a mechanism neither provider implements.

The remaining content is triaged section by section. A full read shows the
earlier reading of these files was wrong: six of the eight carry normative
content that no other document states, so none of them can be deleted as
boilerplate.

| Document | Unique normative content | Destination |
| :--- | :--- | :--- |
| `roles/qa.md` | coverage floor and applicability, the local-versus-remote execution boundary, the CI-only pre-commit contract, anti-duplication, the change-type verification matrix, generated-artifact freshness, local QA/CI orchestration | `policies/quality-standards.md` |
| `roles/infra.md` | `infra_net` and exposure rule, volume naming convention, `no-new-privileges` and Docker Secrets requirement, container-build review criteria, Compose review criteria, approved runtime mutation protocol, `docker system prune` consent rule | `policies/environment-constraints.md` |
| `roles/security.md` | identity and secrets constraints, container and network hardening criteria, approved secrets work protocol | `policies/environment-constraints.md` and `policies/quality-standards.md` section 2 |
| `roles/ops.md` | mandatory postmortem for SEV1 and SEV2 | `policies/quality-standards.md` |
| `roles/docs.md` | `doc-writer` edit permission, read-only default for other roles, `rules-engineer` review for policy change | `policies/approval-boundaries.md` |
| `roles/agentic.md` | none; duplicates `policies/agentic.md`, `bootstrap.md`, and `task-checklists.md`, and its blanket language rule conflicts with the role-based routing in `documentation-protocol.md` | delete |
| `roles/architecture.md` | none applicable; asserts gRPC service-to-service calls, a Gateway REST/GraphQL split, Saga and Event Sourcing patterns, quarterly reviews, and Backend/Frontend/Mobile layers that this repository does not have, and names a stale stage range | delete |
| `roles/common.md` | none applicable; `camelCase`, `PascalCase`, and JSDoc conventions for a repository whose code is Python, Bash, YAML, and Markdown; its pre-commit prohibition is already stated in `policies/workflows.md` and `roles/qa.md` | delete |

Claims that no runbook or script supports are removed rather than moved, and
each removal is named in the Task. `roles/ops.md` asserts verified daily
off-site backups and periodic disaster-recovery drills; `roles/infra.md` asserts
a gateway `LATENCY_SLO < 200ms` and automated backup tags. None of these has a
registered check or an operations runbook, so each is deleted as an unverified
claim, not relocated as policy.

Finally, keep one statement of the thin-root-shim rule in
`policies/bootstrap.md` and remove its restatements from `policies/standards.md`
and `policies/environment-constraints.md`, and drop
`PRD, SRS, Interface Requirement` from `policies/standards.md` in favour of
profile names the Stage 99 registry defines.

### 2. Role and skill canonicalization

Narrow the Stage 99 `governance-role` profile so that `agent_id`, `scope`,
`tier`, `status`, `work_profile`, `permission_profile`, and `skill_ids` move
from `optional_frontmatter` to `required_frontmatter`. After step 1 the
directory holds only agent roles, so the profile can describe one genre.

Rename the two Stage 00 skills whose identifiers collide with globally installed
provider skills, because the collision makes the project skills unreachable at
runtime:

| Current                    | New                                 |
| :------------------------- | :---------------------------------- |
| `skills/code-reviewer.md`  | `skills/change-review-execution.md` |
| `skills/test-automator.md` | `skills/test-authoring.md`          |

Update `skill_ids` and `Related Documents` in `roles/code-reviewer.md` and
`roles/qa-engineer.md`, then regenerate the three projections.

### 3. Lifecycle completion

Add a `spec-package` lifecycle to `docs/99.templates/registry.json` with
statuses `draft`, `active`, `completed`, `superseded`, `retired` and transitions
`draft -> {active, retired}`, `active -> {completed, superseded, retired}`. Bind
the `spec` profile to it. The alternative of adding `completed` to `living` is
rejected: `living` governs 26 profiles including `policy` and `readme`, for
which completion has no meaning.

Disposition rule for the 28 active Spec Packages:

| Condition                                                                                    | Status                                                 |
| :------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| Every Task is `completed` or `cancelled` and the outcome is reflected in canonical documents | `completed`                                            |
| No Tasks exist and a later Spec absorbed the content                                         | `superseded`, with `superseded_by` naming the absorber |
| No Tasks exist and no successor absorbed the content                                         | `retired`                                              |
| Work is genuinely in flight                                                                  | `active`                                               |

Correct the two Stage 98 migrations that carry the unregistered value
`archived` to `completed`, matching `migrations/0003`.

Register `Related Documents` as an optional section on the 16 content profiles
that omit it. The Output Style Contract requires the section on every document
and 499 of 599 documents already carry it, but only the 8 Stage 00 and README
profiles declare it, so the corpus follows a rule the registry does not state.

`generated_roots` in `providers/registry.yaml` is a list of managed
**directories**, not a manifest of generated files:
`provider_surface_renderer.py` raises `managed root is not a directory` for any
non-directory entry. Two of the five renderer outputs are directory-shaped and
belong in it, `.agents/rules` and `.agents/workflows`; the other three,
`.agents/README.md`, `.claude/CLAUDE.md`, and `.codex/README.md`, are single
files and cannot be roots. Adding the two directories also requires extending
`EXPECTED_GENERATED_ROOTS` at
`scripts/validation/agent_governance_contract.py:33`, which the renderer imports
and compares exactly.

The three single-file routes stay declared where the renderer already declares
them, at `provider_surface_renderer.py` lines 289 to 293. The Task records that
no field outside the renderer names them, so a reader of `registry.yaml` alone
cannot tell they are generated. Closing that gap needs a generated-file manifest
that does not exist today; it is recorded as a deferred item rather than forced
into a field with different semantics.

### 4. Retired taxonomy removal

Rewrite the `Stage 04` and `docs/04.execution` passages in the six active Specs
that still describe them as current procedure, replacing them with the
co-located Spec Package model. Delete the `Migration Map` table from
`docs/README.md`; Stage 98 `migrations/` is its sole authority and the bootstrap
policy forbids parallel legacy redirects.

Repair links by pattern where the mapping is mechanical, and by inspection
otherwise:

| Pattern                           | Count | Replacement                     |
| :-------------------------------- | ----: | :------------------------------ |
| `ref-####-*.md`                   |   300 | `####-*/README.md`              |
| `00.agent-governance/rules/`      |    96 | `00.agent-governance/policies/` |
| `03.specs/spec-####-`             |    18 | `03.specs/####-`                |
| `99.templates/support/`           |    15 | `99.templates/`                 |
| repository files moved or removed |    72 | current path or removal         |
| individual judgement              |   316 | per document                    |

Stage 90 audit packs whose subject is closed transition to `superseded` with
`superseded_by`; packs that remain current keep `active` and have their links
repaired.

### 5. Gate scope correction

`scripts/validation/check-document-links.py` selects documents from a
`DOC_ROOTS` tuple naming only `docs/01.requirements`, `docs/02.architecture`,
`docs/03.specs`, and `docs/05.operations`, plus eight hand-listed `SUPPORT_DOCS`
paths. `docs/00.agent-governance`, `docs/90.references`, and `docs/98.archive`
are outside it, which is why 798 of the 817 dead links are invisible to the
gate. Replace the tuple and the hand-listed support paths with the full tracked
Markdown corpus, and exempt `superseded` documents, whose links record an
observation rather than a current route.

`SUPPORT_DOCS` names `docs/00.agent-governance/roles/qa.md`, which workstream 1
removes, so this change must land after workstream 1 or the gate breaks.

The advisory-to-blocking flip for the metadata full inventory is **not** in this
Spec. `scripts/lib/document_governance/metadata_validator.py` raises
`ProfileError("sdlc-taxonomy-convergence remains advisory until corpus
migration")` when the wave is not advisory, and pins a baseline commit beside
it. Flipping it requires the corpus-migration completion judgement that
SPEC-0155 owns. This Spec leaves the corpus with zero `invalid-status` records
so that SPEC-0155 can flip it without grandfathering anything.

The same module pins `planned_partitions` to `docs/04.execution/plans` and
`docs/04.execution/tasks`, so the retired Stage 04 survives inside a validator
as well as inside documents. That literal is recorded here and routed to
SPEC-0155 for the same reason.

## Interfaces and Data

| Interface                                                            | Change                                                                   |
| :------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `docs/99.templates/registry.json` `lifecycles`                       | add `spec-package`                                                       |
| `docs/99.templates/registry.json` `transitions`                      | `spec` maps to `spec-package`                                            |
| `docs/99.templates/registry.json` `profiles[governance-role]`        | seven fields move to `required_frontmatter`                              |
| `docs/99.templates/registry.json` `profiles[*].optional_sections` | `Related Documents` added to 16 content profiles |
| `docs/00.agent-governance/providers/registry.yaml` `generated_roots` | 2 directory entries added |
| `scripts/validation/agent_governance_contract.py:33` | `EXPECTED_GENERATED_ROOTS` extended to match |
| Spec frontmatter                                                     | `completed` becomes a valid `status`; `superseded_by` used on retirement |
| `scripts/validation/check-document-links.py`                         | selection scope widened, `superseded` exempted                           |
| `check-document-links.py` `DOC_ROOTS` and `SUPPORT_DOCS` | replaced by full tracked-corpus selection |

No frontmatter field is added or removed. No new identity space is issued.

## Failure Modes and Guardrails

| Failure mode                                                             | Guardrail                                                                                                                      |
| :----------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| A layer document is deleted while still holding unique normative content | Content moves to its policy destination and is cited in the Task before the source file is removed                             |
| Widening the link gate turns a passing gate red mid-change               | Link repair lands before the scope change; the scope change is the final commit of the workstream                              |
| Bulk pattern replacement rewrites a link that is correct as written      | Each pattern class is applied and reviewed as its own logical commit                                                           |
| A Spec Package is marked `completed` although work remains               | The disposition rule requires Task-level evidence; ambiguity keeps `active` and is recorded in the Task                        |
| Skill rename breaks provider projections                                 | `sync-provider-surfaces.sh` runs and `git diff --exit-code` proves the three projections agree                                 |
| Stage 90 evidence is lost                                                | No audit pack is deleted; retirement is a status transition, and Tombstones are written only where a path is genuinely removed |

## Acceptance Contract

1. `python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all` exits 0.
2. `python3 scripts/validation/check-document-metadata.py` exits 0 and reports zero `invalid-status` records.
3. `python3 scripts/validation/check-document-links.py --mode all` reads the full tracked Markdown corpus and reports zero failures.
4. `bash scripts/operations/sync-provider-surfaces.sh` followed by `git diff --exit-code` produces no diff.
5. `python3 scripts/validation/run-ci-gate.py --profile full` exits 0.
6. No `active` document instructs the reader to use `Stage 04` or `docs/04.execution`. Factual records of paths that existed then, inside execution ledgers, evidence tables, and observation inventories, are not violations and are not rewritten.
7. `policies/standards.md` no longer requires traceability across artifact types the Stage 99 registry does not define. The prohibition in `policies/documentation-protocol.md` keeps naming them, which is its purpose.
8. Every file under `docs/00.agent-governance/roles/` carries `agent_id`.
9. Every profile that can carry a `Related Documents` section registers it.
10. Command, result, rollback, and skipped checks for each step are recorded in the owning Task.

## Traceability

| Upstream  | Relation                                                                           |
| :-------- | :--------------------------------------------------------------------------------- |
| REQ-0024  | Agent governance standardization is the durable need this Spec serves              |
| ADR-0027  | Stage 00 canonical adapter model fixes the generated-projection boundary           |
| ADR-0029  | Workspace governance authority fixes Stage 00 as the sole policy owner             |
| SPEC-0155 | Consumes the corrected lifecycle vocabulary when reducing validator surface        |
| SPEC-0156 | Consumes the corrected Stage 90 status set when realigning infrastructure evidence |

## Related Documents

- [Bootstrap policy](../../00.agent-governance/policies/bootstrap.md)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
- [SDLC](../../00.agent-governance/sdlc.md)
- [Stage 99 registry](../../99.templates/registry.json)
- [Provider registry](../../00.agent-governance/providers/registry.yaml)
