---
status: active
artifact_id: spec:137-agentic-research-pack-rebuild
artifact_type: spec
parent_ids:
  - spec:136-sdlc-taxonomy-convergence
  - spec:104-agentic-research-pack-refresh
  - spec:122-agentic-research-pack-consolidation
---

# Agentic Engineering Research Pack Rebuild Specification

**Original conversation design approval date:** 2026-08-08 (Asia/Seoul)

**V&V and Gate 9 amendment approval date:** 2026-08-09 (Asia/Seoul)

**Deletion-evidence decoupling amendment approval date:** 2026-08-17
(Asia/Seoul)

**Pre-deletion gate scope amendment approval date:** 2026-08-18 (Asia/Seoul)

The user approved the original design direction in conversation. That written
artifact then passed independent specification and documentation reviews with
zero Critical or Important findings and became active for Stage 04 planning.
Those verdicts cover the original artifact only. The 2026-08-09 amendment that
adds REQ-36, the twenty-one-file cardinality, and the Gate 9 architecture
boundary is user-approved, but the original verdicts do not cover it. The
2026-08-17 amendment that decouples deletion authority from the Gate 9
publication mechanism is likewise user-approved and is covered by neither set of
verdicts. The 2026-08-18 amendment that states the quantification scope of
pre-deletion requirements 5 and 6 and their closure kinds is user-approved on the
same basis, after a read-only audit found both gates unsatisfiable by
construction under their literal wording; it adds no gate and relaxes no
threshold. Exact amendment commit ranges and independent review verdicts are
recorded only in the Stage 04 Task and are never asserted by this Spec.
Old-pack deletion authority remains conditional on every pre-deletion gate
below.

## Overview

This specification defines a documentation-only rebuild of the workspace's
agentic engineering research pack. The work creates a new, source-backed pack
under
`docs/90.references/research/2026-08-08-agentic-engineering-research-pack/`,
validates every claim retained from the current 2026-07-05 pack, integrates
verified unique material, switches all active routes, and deletes the old pack
only after explicit migration gates pass.

The rebuilt pack covers harness engineering, loop engineering, Claude and
Codex implementation status, provider-neutral rules and environments,
spec-driven development, Docker Compose, infrastructure, the SDLC and its
document roles, Diataxis, LLM Wiki design, CI/CD, GitHub Actions, QA, security,
verification and validation, external AI-agent catalogs, task-aware model
selection, and short-term, long-term, and domain memory. Each topic combines
current primary external sources with measurements of the tracked workspace
and reports the limits of that evidence.

This is a rebuild rather than an in-place refresh. The current pack contains
valuable evidence, but successive migrations and provider releases have made
some counts, routes, capability claims, and enforcement conclusions stale.
Moving the old files would preserve those defects. The new pack therefore uses
the old pack as an input ledger, not as authoring source text.

The research output remains advisory Stage 90 material. It may identify gaps
and implementation candidates, but it does not itself change active policy,
runtime Compose topology, provider configuration, credentials, remote GitHub
settings, or deployment state.

## Boundaries and Inputs

### Approved scope

- Author one new canonical research pack with exactly twenty-one files: one
  README and twenty new leaf documents.
- Research the requested categories using current official documentation,
  standards, primary papers, and official repositories wherever available.
- Re-measure the workspace surfaces relevant to every topic and all fourteen
  tracked persona scopes instead of inheriting historical counts.
- Compare Claude and Codex harness, loop, agent, hook, instruction, model, and
  memory capabilities, and distinguish upstream capability from local
  adoption.
- Define the systems, environments, rules, evidence, and ownership needed to
  apply harness and loop engineering in this workspace.
- Validate all material in the 2026-07-05 pack, integrate verified unique
  content, record corrections and deliberate omissions, then delete its twenty
  files as one logical migration unit.
- Update the research router, clickable cross-links, generated LLM Wiki
  artifacts, and any current indexes affected by the canonical-path switch.
- Preserve execution evidence in a Plan and Task and commit each logical unit
  separately.

### Excluded scope

- Changing runtime service definitions, images, networks, ports, volumes,
  secrets, or credentials.
- Modifying Claude, Codex, Gemini, or other provider runtime configuration.
- Adopting research recommendations as Stage 00 or Stage 05 policy.
- Mutating remote GitHub settings, dispatching workflows, pushing, merging, or
  opening a pull request without a later explicit user choice.
- Rewriting historical audit, archived specification, completed Plan, or
  completed Task evidence to resemble current state.
- Treating tracked configuration as proof of a live provider, container,
  workflow, branch-protection, deployment, backup, restore, or rollback event.
- Reading secret values, raw logs, shell history, ignored volumes, or private
  provider state.

### Repository baseline

The implementation Plan must pin the exact starting commit. At design time the
isolated worktree is based on `78b60974164ff5427ba8c64aaf3ecde4a7faf41a`.
Graphify's report was built from `f8a72211`, so its graph is advisory and every
graph-derived lead must be corroborated against tracked source, Stage 00
governance, and active stage documents.

The following baseline defects are pre-existing inputs, not evidence that this
work may silently normalize its claims:

- the generated LLM Wiki index passes its freshness check;
- the generated LLM Wiki coverage snapshot fails its freshness check;
- the security automation readiness snapshot fails its freshness check because
  its generator does not fully resolve the typed workflow registry; and
- document implementation alignment reports 184 pre-existing direct links
  from active Stage 01-05 documents to archived specifications; the draft Spec
  137 adds zero findings after routing its archive references through the
  Stage 98 index; and
- the whole repository contract check is blocked in the isolated environment
  by the missing `html5lib` validation dependency.

The Task must distinguish defects corrected within the approved documentation
migration from unrelated or environment-owned predecessors. A known failure
may not be converted into a pass by omission.

Baseline currency, recorded 2026-08-18 from a read-only gate audit. Three of the
defects above have since been resolved and now pass: the LLM Wiki coverage
snapshot, the security automation readiness snapshot, and the repository
contract check, whose dependency is declared in the repository's own
requirements file and was a local environment gap rather than an unowned defect.
Document implementation alignment currently reports 181 findings, below its
pinned 184 predecessor, with zero attributable to this work. The bullets above
are retained as the original baseline record; this note is the current reading,
and a gate must cite a fresh measurement rather than either list. The
no-silent-normalization rule is unchanged and cuts both ways: a resolved defect
is recorded as resolved, and a regression may not be hidden behind a stale
baseline.

One scope limit of that alignment number, so it is not read as broader than it
is: the alignment check scans Stage 01 through 05 only, so it cannot observe the
retiring pack under Stage 90. Zero attributable findings means zero in Stage 01
through 05, not that the pack is clean.

### Normative requirement inventory

The implementation requirement matrix uses the following closed set. A
one-hundred-percent result means all thirty-six identifiers have a reviewed
destination and evidence state; additional discoveries may add rows but may
not remove or merge these rows.

| ID     | Required analysis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Primary owner                           |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| REQ-01 | Harness engineering elements and patterns                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `harness-engineering.md`                |
| REQ-02 | Loop engineering elements and feedback systems                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `loop-engineering.md`                   |
| REQ-03 | Systems, environment, and rules needed to apply harness and loop engineering to this workspace                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `harness-engineering.md`                |
| REQ-04 | Current Claude and Codex harness and loop implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `provider-implementation-comparison.md` |
| REQ-05 | Common Claude/Codex environment, rules, systems, translations, and irreducible provider-native differences                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `provider-implementation-comparison.md` |
| REQ-06 | Spec-driven development concepts, workflow, traceability, and enforcement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `spec-driven-sdlc.md`                   |
| REQ-07 | Docker Compose concepts, current workspace implementation, and adoption rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `docker-compose-infrastructure.md`      |
| REQ-08 | Infrastructure concepts, topology, controls, operations evidence, and adoption rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `docker-compose-infrastructure.md`      |
| REQ-09 | SDLC lifecycle, stage gates, feedback, ownership, and evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `spec-driven-sdlc.md`                   |
| REQ-10 | PRD role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `sdlc-document-roles.md`                |
| REQ-11 | ARD role, purpose, trigger, owner, consumer, system, and rules, including its local-coinage boundary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `sdlc-document-roles.md`                |
| REQ-12 | ADR role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `sdlc-document-roles.md`                |
| REQ-13 | Spec and child-contract roles, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `sdlc-document-roles.md`                |
| REQ-14 | Plan role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `sdlc-document-roles.md`                |
| REQ-15 | Task role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `sdlc-document-roles.md`                |
| REQ-16 | Guide role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `sdlc-document-roles.md`                |
| REQ-17 | Incident role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `sdlc-document-roles.md`                |
| REQ-18 | Postmortem role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `sdlc-document-roles.md`                |
| REQ-19 | Policy role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `sdlc-document-roles.md`                |
| REQ-20 | Release role, purpose, trigger, owner, consumer, system, and rules, including its deployment-evidence boundary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `sdlc-document-roles.md`                |
| REQ-21 | Runbook role, purpose, trigger, owner, consumer, system, and rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `sdlc-document-roles.md`                |
| REQ-22 | Diataxis tutorial, how-to, reference, and explanation analysis and workspace mapping                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `documentation-architecture.md`         |
| REQ-23 | LLM Wiki architecture, safety, generation, freshness, discovery, and implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `llm-wiki-system.md`                    |
| REQ-24 | CI/CD system, rules, implementation, evidence, promotion, deployment, and rollback boundaries                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `quality-ci-formatting.md`              |
| REQ-25 | GitHub Actions workflow, action, permissions, pinning, gate, and remote-enforcement analysis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `quality-ci-formatting.md`              |
| REQ-26 | QA formatting, linting, testing, syntax, type, coverage, and failure-handling analysis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `quality-ci-formatting.md`              |
| REQ-27 | Security governance, secure SDLC, supply chain, secret, approval, runtime, and implementation analysis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `security-governance.md`                |
| REQ-28 | External AI-agent catalog analysis using the official agency-agents repository and local import boundary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `ai-agent-catalogs.md`                  |
| REQ-29 | Task-characteristic agent model, tier, effort, settings, evaluation, fallback, and change rules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `agent-model-selection.md`              |
| REQ-30 | Short-term, long-term, and domain memory plus promotion, retrieval, retention, eviction/deletion, archival, partition, privacy, and management rules                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `memory-hierarchy.md`                   |
| REQ-31 | Current workspace baseline for every research category                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `workspace-baseline.md`                 |
| REQ-32 | Explicit analysis and disposition for all fourteen workspace scopes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `scope-application-matrix.md`           |
| REQ-33 | New authorship plus claim-level validation and integration before old-pack deletion                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | pack README and Task migration ledger   |
| REQ-34 | One-off cleanup, canonical cross-link switch, stale-path control, and affected generated artifacts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Task verification ledger                |
| REQ-35 | Logical-unit commits, independent reviews, final verification, and branch handoff                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Plan and Task                           |
| REQ-36 | Primary-source research and current-workspace implementation-and-gap analysis for verification and validation systems and rules that distinguishes conformance verification from intended-use and stakeholder-need validation and covers V&V planning, entry and readiness criteria, success and exit or completion criteria, static and dynamic methods, evidence and traceability, independence and risk-based depth, environments, data, oracles, defect disposition, acceptance and decision authority, residual-risk acceptance, release acceptance, monitoring, and revalidation across all fourteen scopes | `verification-validation.md`            |

### Source and evidence classes

Every load-bearing claim must identify one of these evidence classes:

| Evidence class      | Minimum record                                                       | Interpretation                                                                                                     |
| ------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| External fixed      | Direct primary URL, title/version or immutable revision, access date | Stable standard, paper, or immutable source; later revision still requires review when normative language changes. |
| External mutable    | Direct official URL, access date/time, product or repository state   | Current observation only; requires freshness and change-history caveats.                                           |
| Workspace tracked   | Tracked path, relevant identifier or command, baseline commit        | Proves repository state, not live runtime or remote enforcement.                                                   |
| Runtime or remote   | Authorized observation, timestamp, target, redaction boundary        | May prove only the observed target and time; absent authorization remains `UNVERIFIED`.                            |
| Historical retained | Prior artifact and immutable commit/blob or archive route            | Preserves provenance without presenting the claim as current guidance.                                             |

If an official source cannot be retrieved or a workspace claim cannot be
reproduced, the document must mark it `UNVERIFIED` and explain the boundary. It
must not infer a current fact from an older pack.

### Minimum external source families

The source ledger must include, as applicable, the official Claude Code,
OpenAI/Codex, Docker Compose, GitHub Actions, Diataxis, NIST, OWASP, SLSA,
OpenSSF, agency-agents, IEEE 1012-2024, ISO/IEC/IEEE 12207:2026, and current
NASA systems-engineering guidance. Technical claims must prefer these primary
sources over commentary. Provider capability pages and standards status routes
are mutable and must be reopened during execution; immutable repository
evidence must pin a commit or release when a precise count or schema is
claimed. Full normative claims from paywalled standards require licensed
access; public route and abstract evidence supports only the claims it exposes.

## Contracts

### Canonical pack contract

The final active route is exactly:

`docs/90.references/research/2026-08-08-agentic-engineering-research-pack/`

The directory contains exactly twenty-one files: one README and these twenty
newly authored leaves:

| Group                       | Leaf documents                                                                                                                                                                                                                          |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Foundation                  | `workspace-baseline.md`, `scope-application-matrix.md`                                                                                                                                                                                  |
| Agentic engineering         | `harness-engineering.md`, `loop-engineering.md`, `provider-implementation-comparison.md`, `agent-instructions-vibe-coding.md`, `provider-model-landscape.md`, `agent-model-selection.md`, `ai-agent-catalogs.md`, `memory-hierarchy.md` |
| SDLC and documentation      | `spec-driven-sdlc.md`, `sdlc-document-roles.md`, `document-metadata-lifecycle.md`, `documentation-architecture.md`, `llm-wiki-system.md`                                                                                                |
| Delivery quality and V&V    | `automation-pipeline-workflow.md`, `quality-ci-formatting.md`, `verification-validation.md`                                                                                                                                             |
| Infrastructure and security | `docker-compose-infrastructure.md`, `security-governance.md`                                                                                                                                                                            |

The pack stays flat to preserve a short and predictable Stage 90 route. The
README supplies grouped navigation, reading order, evidence boundaries, and
the canonical migration statement.

### Leaf contract

Each leaf must contain all of the following, using the exact reference
template headings required by the selected Stage 90 profile:

1. the concept and its current primary external evidence;
2. current tracked workspace implementation evidence;
3. provider or system comparison where the topic has multiple surfaces;
4. the system, environment, and rules required for workspace adoption;
5. an explicit per-scope application analysis;
6. implementation status and verification limitations;
7. concrete gaps, risk, ownership, and a non-normative follow-up route; and
8. direct sources with access dates and mutability classification.

No leaf may claim that Stage 90 advice is active policy. Counts must state
their derivation command or registry owner and baseline. Provider-neutral
recommendations must separate common semantic intent from provider-native
mechanisms.

The REQ-36 leaf must additionally provide one workspace owner table with the
exact tracked path, command, baseline-specific count where applicable,
verification or validation classification, gap, and runtime limit. It must
distinguish `configured`, `reachable`, `selected`, `executed`, `passed`,
`reviewed`, `hosted`, `enforced`, `runtime-observed`, and `UNVERIFIED` states;
remeasure mutable counts during implementation; and state what readers must
not infer about provider behavior, GitHub enforcement, Compose runtime,
security posture, release acceptance, or generated freshness. It must define
the V&V planning boundary, entry and readiness criteria, success and exit or
completion criteria, acceptance and decision authority, defect disposition,
and residual-risk acceptance route. Green CI or Stage 90 advice alone cannot
grant acceptance authority; absent downstream authority and evidence remains
`UNVERIFIED`.

The Stage 90 reference template requires seven H2 headings: `Overview`,
`Purpose`, `Scope`, `Definitions / Facts`, `Sources`, `Maintenance`, and
`Related Documents`. This pack convention adds `Repository Role` and
`Scope Implications`; it is not an additional registry requirement. The
REQ-36 leaf therefore uses exactly these nine H2 headings in order:
`Overview`, `Purpose`, `Repository Role`, `Scope`, `Definitions / Facts`,
`Scope Implications`, `Sources`, `Maintenance`, and `Related Documents`. Its
detailed system model and workspace-adoption rules belong under
`Definitions / Facts` as H3 sections.

### Migration contract

The existing directory
`docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`
contains twenty files. Each file and each unique material claim must receive a
record in the migration manifest with one of four dispositions:

- `retain`: verified and rewritten into an identified new leaf;
- `correct`: rewritten with current evidence and an explicit correction note;
- `omit`: deliberately excluded with a reason and provenance pointer; or
- `supersede`: replaced by a named new claim or document.

The manifest is execution evidence and belongs in the Task, not the research
pack. The old files may be deleted only after all records have a disposition,
all retained material has a canonical destination, and the deletion gates in
Verification pass.

### Gate 9 evidence architecture boundary

The user approved the following high-level boundary for the final deletion
evidence gate on 2026-08-09. The implementation Plan owns the executable
schemas, commands, error taxonomy, finite-attempt state machine, tests, and
review sequence within this boundary.

- Temporary scratch-directory, temporary Git-index, and linked-worktree
  projection mechanisms are eliminated from every Gate 9 helper path.
- The deletion projection is computed pathlessly from the reviewed Git root
  tree with content-addressed tree and blob operations. Package construction
  may append Git objects needed for that projection, but it may not delete or
  rewrite objects, mutate a branch, index, or worktree, or clean up unreachable
  objects; ordinary Git garbage collection owns their eventual reclamation.
- Each generator receives its exact canonical path manifest through a fresh,
  sealed anonymous `memfd`. A filesystem-path, pipe, or unsealed fallback is
  not an authority channel.
- The review package is one canonical, atomically published, read-only bundle
  file whose attachment identities and bytes are verified without extraction.
- No package-build or replay mode mutates generated artifacts, lifecycle
  records, remote state, or Git refs. A separately reviewed create-only
  evidence-ref publication remains the only permitted Gate 9 ref mutation.

### Non-link literal admission amendment

**Approval date:** 2026-08-18 (Asia/Seoul)

Old-path inventory and allowlist names two admission routes for a non-link
retiring-path literal: the claim-ledger route, which requires the literal to
describe a factual old event AND carry an explicit claim-ledger disposition,
and the commit-pinned baseline route. The Task's allowlist contains 39 rows in
14 declared classes, and only 21 of them fall under those two routes. The
remaining 18 were admitted by reading the claim-ledger conjunct as vacuously
satisfied, which is not what the clause says and is not a reading this Spec
had confirmed. That gap, not the rows themselves, was the defect.

This amendment names every admission route explicitly. It does not widen what
may be allowlisted: each route below carries a removal condition, so no route
creates a permanent exception, and the clickable-link prohibition is untouched
and admits no exception under any route.

1. **Historical claim-ledger route** — unchanged. The literal describes a
   factual old event and carries an explicit claim-ledger disposition.
   Removal condition: none; these rows are immutable historical evidence.
2. **Commit-pinned baseline route** — unchanged, including its existing
   requirements to identify the pinned baseline or wave, not to act as a
   current route or migration exception, and to stay covered by the baseline's
   canonical promoted-manifest and summary checks.
3. **Operative retirement-machinery route** — the literal is an operand of the
   retirement work itself: a filter constant, a regression fixture, or a scan
   target that must name the retiring path for the retirement machinery to
   function. Such a row must not resolve to retiring content for a reader and
   must be removed when the retirement completes. A literal that merely
   mentions the path is not an operand and does not qualify.
4. **Active retirement-unit route** — the literal appears in the scope,
   boundary, or evidence statements of the retirement Spec, Plan, or Task that
   owns this retirement. Such a row must be owned by a named active unit and
   must be removed when that unit closes. This route is what the two
   `Active-unit scope boundary` rows require; it is a current-state route, so
   it does not and cannot satisfy the factual-old-event conjunct, and it is
   admitted here on its own terms rather than by stretching that conjunct.
5. **Non-resolving same-slug route** — the literal shares the retiring slug but
   does not resolve to the retiring directory. Such a row must record why it
   does not resolve. This route documents a non-hit; it grants nothing.

Every allowlist row must declare exactly one route, and the route must be
recoverable from its literal class. A row whose class maps to no route is not
admitted. Requirement 4 of the pre-deletion gates is otherwise unchanged, and
the four routes other than the first remain subject to the same reviewed-row
requirement as before.

### Deletion-evidence decoupling amendment

The user approved decoupling deletion authority from the publication mechanism
above on 2026-08-17. This amendment makes exactly these changes and no others:

- Pre-deletion gate 9 is satisfied by the Task recording the before/after file
  manifest, deletion diff, recovery commit, and reviewer verdict directly. That
  is what gate 9's own text already requires, and it is the same evidence route
  every other unit in this Task has used.
- The bundle, sealed-`memfd`, pathless projection, and create-only evidence-ref
  mechanism remains a separately tracked durability enhancement. The boundary
  above continues to govern it in full whenever it is exercised, and its
  no-mutation constraints are unchanged. It simply gates nothing outside itself
  and is not a precondition for deletion or lifecycle reconciliation.

This amendment removes a mechanism dependency, not a safety requirement. All
nine pre-deletion gates stay in force verbatim, including gate 6's zero
unresolved Critical and Important findings and gate 9's four recorded items, and
every post-deletion gate is unchanged. Deletion remains unauthorized until each
gate is independently satisfied and recorded.

The amendment text is ported from a documented amendment of the same name on the
unmerged branch `codex/agentic-research-rebuild-finish`, whose approval carried
recorded wording and a same-day memory corroboration. The separate
tracked-direct-deletion-controller amendment on that branch is **not** adopted
here. Its only repository evidence is a date stamp with no recorded wording, no
memory corroboration, and no Stage 04 approval entry, and the user recorded
uncertainty about it on 2026-08-17. It therefore remains deferred, and no
controller, worker, or confined-runtime subsystem derives authority from this
Spec.

### Route-3 and disposition-vocabulary amendment

**Approval date:** 2026-08-19 (Asia/Seoul)

This amendment makes exactly three changes and no others. Two resolve internal
contradictions in `Non-link literal admission amendment` route 3 and one closes
a gap in `Migration contract`. It widens no allowlist, admits no exception to
the clickable-link prohibition, removes no gate, and lowers no threshold.

**1. Route 3's removal condition excludes the gate-4 scanner's own scan target.**
Route 3 requires an admitted row to be removed when the retirement completes.
`Old-path inventory and allowlist` separately requires that the literal scan and
reviewed allowlist pass before deletion and again after deletion, and states
that a post-deletion scan alone is insufficient. The scanner's scan target is
itself a retiring-path literal: `scripts/validation/old_path_gate_contract.py`
defines `SLUG = "2026-07-05-agentic-research-pack-refresh"` and derives
`RETIRING_DIR` from it. Removing that literal when the retirement completes
would make the mandated post-deletion scan impossible, so route 3's removal
condition as written made another clause of this Spec unsatisfiable by
construction, in the same way requirement 5 and requirement 6 of the
pre-deletion gates were before their recorded carve-outs. The literal that
defines the gate-4 scanner's scan target, and the same literal in that scanner's
own regression fixtures, are therefore carved out of route 3's
removal-on-completion condition. Their removal condition is instead the recorded
completion of the post-deletion literal scan and its reviewed allowlist; until
that is recorded the literal must remain. The carve-out is exhaustive: it covers
the gate-4 scanner and the tests of that scanner, and no other file.

**2. Route 3's operand test is evaluated per mechanism, not by gating status.**
Route 3 admits a literal that must name the retiring path for the retirement
machinery to function. `Deletion-evidence decoupling amendment` states that the
gate 9 durability mechanism gates nothing outside itself and is not a
precondition for deletion or lifecycle reconciliation. Read together, those
clauses appeared to deny route 3 to
`scripts/validation/agentic-research-gate9-evidence.py` and
`tests/validation/test_agentic_research_gate9_evidence.py`, whose `OLD_PACK`
constant is the manifest target the helper projects over and the fixture root
its regression suite builds the synthetic retiring pack under. No other route
admits them. Route 1 requires a factual old event carrying a claim-ledger
disposition, route 2 requires a commit-pinned reviewed historical baseline
selector, route 4 requires the literal to appear in a scope, boundary, or
evidence statement of the owning Spec, Plan, or Task, and route 5 requires the
literal not to resolve to the retiring directory. A live operand in tracked code
satisfies none of the four, so the narrow reading admitted the rows under no
route at all while this Spec continues to keep the track tracked and governed.

Route 3's operand test is therefore evaluated against the mechanism the literal
belongs to: whether that mechanism can function without naming the retiring
path. A mechanism this Spec owns and keeps tracked qualifies whether or not it
gates anything outside itself. Qualifying under route 3 grants that mechanism no
gating role, revives no deletion precondition, and changes nothing in the
decoupling amendment or in requirement 6's scope statement. A row admitted this
way declares route 3 and carries route 3's removal-on-completion condition
unless change 1 above applies to it.

**3. `Migration contract` gains a fifth disposition, `carry`.**
`Migration contract` names four dispositions and defines `retain` as verified
and rewritten into an identified new leaf. Some material claims in the retiring
pack are not reference content with a reference destination. They are live
unremediated repository conditions, corrections whose audit trail matters, or
withdrawn findings that would otherwise be re-raised. For those the canonical
routing owner is `docs/00.agent-governance/rules/documentation-protocol.md`,
which routes a governance, provider, agent-execution, approval-boundary, or
memory-contract gap with no approved policy change to a memory note or task gap,
and which requires that a `docs/90.references/` document not define active
policy, runtime truth, runbook procedure, plan, task evidence, or incident
timeline. Writing such a claim into a successor reference leaf would place task
evidence in Stage 90 against that rule. The four dispositions had no name for
the destination Stage 00 routing actually mandates, so this Spec adds one:

- `carry`: a live unremediated repository condition, a correction whose audit
  trail matters, or a withdrawn finding, verified against the current repository
  and recorded in the owning Task's carried-claims section, where Stage 00
  document-role routing makes a task gap or memory note its canonical owner
  rather than a reference leaf.

A `carry` record must state uniqueness per claim, because the label does not by
itself mean the claim disappears when the retiring pack does, and must name the
owner of any remediation it does not perform. `carry` is not available to
source-backed research or upstream-capability material; that content takes
`retain` and belongs in an identified successor leaf.

Pre-deletion gate 2 quantifies over retained and corrected claims and gate 3
over omissions, so a fifth disposition outside both would weaken the gate set.
It does not: a `carry` claim is evaluated under gate 2 and resolves to a
reviewed destination exactly as a retained claim does, its destination being the
owning Task's carried-claims section rather than a new leaf, and it carries the
two additional requirements named above. The deletion precondition in
`Migration contract` is unchanged and now reads over five dispositions rather
than four.

### Route-1 admission and split-row evaluation amendment

**Approval date:** 2026-08-19 (Asia/Seoul)

An independent review seat found that route 1 of
`Non-link literal admission amendment` is satisfied by no row in the Task's
allowlist, and that gate 4's own scanner cannot evaluate a row that shares a path
with another. This amendment makes exactly two changes and no others. It widens
no allowlist, admits no exception to the clickable-link prohibition, removes no
gate, and lowers no threshold.

**1. Route 1's claim-ledger conjunct is replaced.** Route 1 requires the literal
to describe a factual old event AND to carry an explicit claim-ledger
disposition. The second conjunct cannot be met by any allowlist row, for a
structural reason rather than a drafting one. The claim ledger enumerates the
twenty leaves of the retiring directory and dispositions the claims inside them.
The allowlist, by the definition in `Old-path inventory and allowlist`, covers
literals in tracked text **outside** that directory. A document outside the
retiring pack has no ledger row and cannot be given one without changing what the
ledger enumerates, so the conjunct is unsatisfiable by construction in the same
way requirement 5, requirement 6 and route 3's removal condition were before
their recorded carve-outs. The 2026-08-18 amendment correctly rejected reading
the conjunct as vacuously satisfied; the defect it left open is that no reading
of the conjunct as written can be satisfied at all.

The accounting the conjunct was reaching for is supplied instead by this Spec's
own `Historical-evidence boundary`. Route 1 now reads:

1. **Historical-evidence route** — the literal describes a factual old event, the
   document containing it is historical evidence under `Historical-evidence
   boundary`, and the row states the event and what the record would lose if the
   literal were altered. Qualifying documents are audits, archived
   specifications, archived changes, completed plans and tasks, archive
   tombstones, migration ledgers, and append-preserved progress records. A
   present-tense statement designating a current criteria source, owner, or route
   is a canonical-owner statement, which `Old-path inventory and allowlist`
   denies an allowlist under any route, and it is not admitted here.
   Removal condition: none; these rows are immutable historical evidence, and a
   row under this route may not declare a removal condition that contradicts it.

Measured at the time of amendment: twelve of the fifteen rows in this family
already state the event and what the record preserves, so they satisfy the
amended route without further change.

**2. Requirement 4 is evaluated per declared allowlist row.** Requirement 4 of
the pre-deletion gates is evaluated over the tracked-text universe, and
`Non-link literal admission amendment` requires every allowlist row to declare
exactly one route. Both obligations attach to the **row**. Where several rows
share a path because one document holds literals of different classes, each row
is a separate subject: each declares its own route, carries its own class, and
receives its own review verdict, and a settled verdict on one row settles nothing
for its siblings. A scan implementation that collapses rows sharing a path
reports a state this Spec does not authorize, because it can mark literals
reviewed under a verdict never given to them and can evaluate the forbidden-class
prohibition against one class where several were declared. The allowlist is keyed
by path together with the row's declared line or stable anchor, which is the pair
`Old-path inventory and allowlist` already requires the Task to own.

### Historical-evidence boundary

Audits, archived specifications, completed plans, completed tasks, and archive
tombstones remain historical evidence. Their body text and inline-code paths
must not be rewritten merely because the canonical research path changes.
Clickable links in current documents must resolve to the new pack. A historical
document may keep a factual old path when altering it would falsify the record,
provided a current router or migration record explains the replacement.

### Commit contract

Implementation proceeds through logical commits with no mixed concerns:

1. this Stage 03 design and routing update;
2. the Stage 04 implementation Plan;
3. Task, requirement matrix, source ledger, and migration manifest setup;
4. foundation leaves;
5. harness, loop, and provider comparison leaves;
6. instruction, model, agent-catalog, and memory leaves;
7. spec-driven SDLC, document-role, and metadata leaves;
8. Diataxis and LLM Wiki leaves;
9. automation, CI/CD, GitHub Actions, and QA leaves;
10. Docker Compose, infrastructure, and security leaves;
11. verification and validation leaf plus its requirement, source, scope, and
    routing evidence;
12. pack README and parent research router;
13. clickable-link and generated-artifact switch;
14. deletion of the old twenty-file pack; and
15. final verification, independent review, Task closure, and memory evidence.

Commit boundaries may be split further when independent review finds a
material concern. They may not be collapsed across the old-pack deletion gate.

## Core Design

### End-to-end data flow

The work follows one directional evidence flow:

```text
tracked baseline + approved requirements + primary external sources
                              |
                              v
         requirement / leaf / scope / source ledgers
                              |
                              v
       old claim classification and current re-measurement
                              |
                              v
             newly authored source-backed leaves
                              |
                              v
             independent leaf and pack review
                              |
                              v
       router, cross-link, and generated-index switch
                              |
                              v
              pre-deletion completeness gate
                              |
                              v
                old-pack deletion commit
                              |
                              v
          post-deletion repository verification
```

The old pack is never an unqualified source for new prose. It enters the flow
through the claim-classification ledger so that provenance, corrections, and
deliberate omissions remain inspectable.

### Requirement-to-leaf ownership

| Requirement family                          | Primary owner leaves                    | Required supporting views                                                          |
| ------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------- |
| Harness and workspace application           | `harness-engineering.md`                | workspace baseline, scope matrix, provider comparison, QA, security                |
| Loop and feedback systems                   | `loop-engineering.md`                   | automation, memory, QA, provider comparison                                        |
| Claude and Codex current implementation     | `provider-implementation-comparison.md` | harness, loop, instructions, model landscape                                       |
| Common provider environment and rules       | `provider-implementation-comparison.md` | agent instructions, model selection, memory, security                              |
| Spec-driven development and SDLC            | `spec-driven-sdlc.md`                   | document roles, metadata lifecycle, automation, QA                                 |
| PRD/ARD/ADR and operational document system | `sdlc-document-roles.md`                | metadata lifecycle, documentation architecture                                     |
| Diataxis documentation architecture         | `documentation-architecture.md`         | document roles, LLM Wiki                                                           |
| LLM Wiki implementation                     | `llm-wiki-system.md`                    | documentation architecture, workspace baseline, QA                                 |
| CI/CD, GitHub Actions, QA                   | `quality-ci-formatting.md`              | automation pipeline, security, workspace baseline                                  |
| Docker Compose and infrastructure           | `docker-compose-infrastructure.md`      | security, automation, scope matrix                                                 |
| Security governance and implementation      | `security-governance.md`                | Docker Compose, CI/CD, harness, scope matrix                                       |
| External AI agents and local catalog        | `ai-agent-catalogs.md`                  | model selection, instructions, harness                                             |
| Task-aware models and settings              | `agent-model-selection.md`              | model landscape, provider comparison, AI-agent catalogs                            |
| Memory hierarchy and management             | `memory-hierarchy.md`                   | loop, instructions, provider comparison                                            |
| Verification and validation                 | `verification-validation.md`            | workspace baseline, scope matrix, SDLC, automation, QA, security, release evidence |

The requirement matrix must show every user-requested item, its primary leaf,
supporting leaves, external source status, workspace evidence owner, scope
coverage, review verdict, and final canonical link. Coverage is complete only
when every row has a reviewed destination.

### Scope analysis

`scope-application-matrix.md` is the scope-axis entry point. The normative
scope set is the fourteen tracked persona scopes: `agentic`, `architecture`,
`backend`, `common`, `docs`, `entry`, `frontend`, `infra`, `meta`, `mobile`,
`ops`, `product`, `qa`, and `security`. The matrix must analyze all fourteen,
including the six scopes not admitted by the current typed agent catalog, and
give each a current adoption or explicit not-applicable disposition. It must
distinguish:

- the paths and artifacts owned by the scope;
- the research leaves that apply;
- current implemented, partial, missing, not-applicable, and unverified state;
- adoption rules and exceptions required by that scope;
- evidence and validation owners; and
- unresolved reachability or stale-count findings.

Every topical leaf must also state its own scope implications. A reader must be
able to enter either by topic or by scope without silently losing a
requirement.

### Comparison method

Provider and system comparisons use a semantic capability matrix with separate
columns for upstream capability, local adapter or contract, local execution
evidence, enforcement, and gap. The method prevents two recurring errors:

- treating a provider feature as locally adopted because the vendor documents
  it; and
- treating a locally unsupported mapping as a permanent provider limitation.

Mutable provider facts are observed at execution time. Historical provider
registries and pinned upstream repository commits remain evidence of their own
cutoff and are not rewritten as current facts.

The Claude/Codex construction matrix is a required output, not optional
comparison prose. Its minimum columns are semantic capability,
provider-neutral contract, Claude-native mechanism, Codex-native mechanism,
shared implementation, translation required, irreducibly provider-native,
tracked local state, execution or enforcement evidence, and gap.

### Documentation architecture

The pack uses Diataxis to analyze documentation modes, not to force one folder
per quadrant. Tutorials, how-to guides, reference, and explanation must be
identified by reader need and mode-mixing risk. The analysis must reconcile
that lens with this repository's normative SDLC roles, template profiles,
metadata lifecycle, archive boundary, and LLM-facing navigation.

### Agent-driven implementation

Implementation uses subagent-driven development because the user authorized
subagents and the work divides into reviewable logical units. The controller
coordinates the ledgers, ownership, gates, and commits. For each logical unit:

1. one fresh implementer owns only its assigned files and does not revert
   concurrent or predecessor work;
2. a separate reviewer checks requirement coverage and source fidelity;
3. a separate quality review checks clarity, cross-links, metadata, scope
   completeness, and overclaiming;
4. Critical and Important findings are resolved before the next unit starts;
   and
5. the unit receives a logical commit only after its local checks pass.

The controller does not make overlapping edits while an implementer owns the
same files. A final strong reviewer evaluates the complete branch after the
old-pack deletion.

## Interfaces and Data

### Requirement matrix

The Task owns a table with these minimum fields:

`requirement_id`, `requirement_text`, `primary_leaf`, `supporting_leaves`,
`external_source_state`, `workspace_evidence_owner`, `scopes`,
`implementation_status`, `review_verdict`, and `canonical_link`.

Requirement identifiers are stable through implementation so review findings
can point to a single row even if prose changes.

### Source ledger

Each external source record contains:

`source_id`, `topic`, `authority`, `direct_url`, `version_or_revision`,
`retrieved_at`, `mutability`, `verification_state`, and `claim_ids`.

Each workspace evidence record contains:

`evidence_id`, `tracked_path`, `identifier_or_command`, `baseline_commit`,
`verification_state`, `runtime_limit`, and `claim_ids`.

Secrets and raw private state are forbidden. A command whose safe execution
would create secrets, start services, or mutate remote state is recorded as
not run with the reason.

### Claim migration ledger

Each old-pack record contains:

`old_path`, `old_commit`, `old_blob`, `claim_anchor`, `claim_summary`,
`disposition`, `evidence_state`, `new_path`, `new_anchor`,
`correction_or_omission_reason`, and `review_verdict`.

A file-level row alone is insufficient when a file contains multiple unique
material claims with different dispositions.

### Generated-artifact inventory

The Task owns a generated-artifact table with artifact path, source trigger,
canonical generator, exact freshness check, baseline result, required
disposition, and final result. The initial inventory is closed as follows:

| Artifact                                                                                             | Source trigger                                                                                                                            | Generator                                                                                                                                                                                                  | Freshness check                                                                           | Baseline                                                                                                                                               | Required disposition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Final result                                 |
| ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `docs/90.references/llm-wiki/llm-wiki-index.md`                                                      | Tracked safe-path set or canonical route changes                                                                                          | `scripts/knowledge/generate-llm-wiki-index.sh`                                                                                                                                                             | `bash scripts/knowledge/generate-llm-wiki-index.sh --check`                               | PASS                                                                                                                                                   | Regenerate after the canonical route switch and require PASS.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Not run; Task-owned                          |
| `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`                              | Tracked Stage/category path set changes                                                                                                   | `scripts/knowledge/generate-llm-wiki-coverage.sh`                                                                                                                                                          | `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check`                            | FAIL                                                                                                                                                   | Regenerate after the canonical route switch and require PASS; the baseline FAIL is not acceptable at deletion.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Not run; Task-owned                          |
| `docs/90.references/data/governance/target-surface-delta-manifest.yaml`                              | Changed `.github`, `archive`, `examples`, `infra`, `projects`, `scripts`, `secrets`, or `tests` path since the pinned predecessor closure | Reviewed advisory manifest edited under `check-target-surface-delta-contract.py`                                                                                                                           | `python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory`       | Root baseline already FAILS for three unregistered changed scripts; Task 10b adds two changed LLM Wiki generators and one focused test                 | After the Task 10b commit, add exactly the six missing changed paths with bounded provenance, rollback, and review evidence. Require the advisory contract to PASS before using its sample-service successor handoff to close the target-surface manifest.                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Newly discovered; Task-owned                 |
| `docs/90.references/data/governance/target-surface-delta-summary.md`                                 | Reviewed target-surface delta manifest or tracked target inventory changes                                                                | `check-target-surface-delta-contract.py --write-summary`                                                                                                                                                   | `python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory`       | Stale while the delta manifest has missing changed paths                                                                                               | Regenerate only after the six missing rows are reviewed and the advisory contract has no finding. Require canonical freshness in the post-deletion lifecycle-evidence commit.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Newly discovered; Task-owned                 |
| `docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml`       | Commit-pinned target-surface baseline plus reviewed result mapping                                                                        | Reviewed manifest edited under `check-document-corpus-lifecycle.py`                                                                                                                                        | `check-manifest --wave target-surface-convergence` plus `check-promoted`                  | Root baseline already FAILS with 9 manifest and 25 promoted findings; the Task 10 route adds one Foundation consumer finding for a `9/26/9` checkpoint | Keep the seven baseline selectors and their same-path rows unchanged before deletion. After the independently reviewed twenty-file deletion commit exists, change those seven rows and the already-archived Spec 133 source row to reviewed `delete` results: `target_path: null`, `artifact_type_after: null`, no canonical replacement, preserved baseline identity/status/parents, Git-history preservation, complete evidence, and rollback commands pinned to the real commits. Close the six-row delta predecessor first so the sample-service successor handoff validates. Require the target-surface manifest itself to PASS and permit only the separately identified Foundation promoted predecessor. | Newly discovered; Task-owned                 |
| `docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence-summary.md` | Reviewed target-surface manifest changes                                                                                                  | `check-document-corpus-lifecycle.py --mode generate-summary --wave target-surface-convergence --output docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence-summary.md` | `check-summary --wave target-surface-convergence`                                         | Root baseline already FAILS with the same 9 target-surface manifest findings                                                                           | Regenerate after the eight reviewed delete mappings make the target-surface manifest valid. Require the canonical generator and `check-summary` to PASS in the post-deletion lifecycle-evidence commit.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Newly discovered; Task-owned                 |
| `docs/90.references/data/security/security-automation-readiness.md`                                  | Security controls, scripts, workflows, or typed workflow registry changes                                                                 | `scripts/validation/generate-security-automation-readiness.sh`                                                                                                                                             | `bash scripts/validation/generate-security-automation-readiness.sh --check`               | FAIL                                                                                                                                                   | Preserve the FAIL as a predecessor because the generator misreads the typed workflow registry. Do not regenerate a known-invalid snapshot or cite it as current truth. Fixing the generator requires separately approved non-documentation scope; the new security leaf reports the snapshot as stale and derives tracked evidence directly. This predecessor does not block old-pack deletion when recorded exactly.                                                                                                                                                                                                                                                                                           | Classified predecessor; Task must re-observe |
| `graphify-out/**`                                                                                    | Tracked corpus changes                                                                                                                    | Graphify workspace updater                                                                                                                                                                                 | `bash scripts/knowledge/report-graphify-health.sh` after an explicitly authorized refresh | Advisory and stale at `f8a72211`                                                                                                                       | Keep advisory and unchanged in this documentation-only workstream; do not use the stale graph as current evidence.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | No refresh authorized                        |

If execution discovers another generated artifact whose input set includes the
new or retiring path, it must be added to the table before the route switch.
Passing `check-repo-contracts.sh` never substitutes for any named generator
freshness check.

### Verification ledger

The Task records each command, timestamp, baseline or comparison range, exit
status, result classification, and attributable failure. Pre-existing failures
must be carried forward until corrected or explicitly classified outside the
approved scope.

### Canonical routing

The pack README is the human topic router. The parent research README is the
category router and records the old-to-new canonical path mapping. Generated
LLM Wiki artifacts are machine-facing navigation and must be regenerated from
tracked source using their canonical generators. None of these surfaces may
claim freshness unless its byte-exact check passes.

### Old-path inventory and allowlist

Before deletion, scan every tracked text file outside the retiring directory,
including current documents, archives, completed execution evidence, generated
documents, configuration, and scripts, for the literal retiring directory and
relative variants. Markdown links to the old pack are forbidden everywhere
outside the retiring directory and must be retargeted, including links in
historical documents. Non-link historical literals may remain only when they
describe a factual old event and have an explicit claim-ledger disposition.
The Task owns the exact allowlist by path, line or stable anchor, reason, and
review verdict. Current routers, generated navigation, mutable provider or
configuration routes/exceptions, and canonical-owner statements have no
allowlist. An exact non-link path may remain in a commit-pinned, already
reviewed historical baseline selector, its immutable manifest, or generated
summary only when removing it would rewrite that historical evidence. Such a
row must identify the pinned baseline/wave in the allowlist, must not act as a
current route or migration exception, and must remain covered by the baseline's
canonical promoted-manifest and summary checks.

The deterministic evidence set is:

- the complete retiring-path literal scan over the tracked text universe;
- `bash scripts/validation/check-repo-contracts.sh` for Markdown and
  pseudo-link contracts;
- `bash scripts/validation/check-doc-implementation-alignment.sh` for active
  implementation-link alignment; and
- the canonical LLM Wiki freshness checks named above.

The literal scan and reviewed allowlist must pass before deletion and again
after deletion; a post-deletion scan alone is insufficient.

## Failure Modes and Guardrails

| Failure mode                                  | Guardrail and recovery                                                                                                                                                                  |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mutable source changed                        | Reopen the official source, record the access time and changed behavior, then correct the leaf and source ledger. Do not preserve the old conclusion for apparent consistency.          |
| Official source unavailable                   | Mark affected claims `UNVERIFIED`, retain a provenance pointer, and avoid normative conclusions. A cached or historical source may be labeled historical only.                          |
| External and local documents conflict         | Current tracked implementation wins for workspace-state claims; current official primary documentation wins for upstream capability claims. Record the conflict and its evidence class. |
| Tracked config mistaken for execution         | Separate definition, reachability, local execution, remote enforcement, and runtime evidence into distinct status fields.                                                               |
| Historical count copied forward               | Re-derive the count from a declared owner or command at the pinned baseline; otherwise remove the count or mark it historical.                                                          |
| Unique old claim has no destination           | Stop before deletion. Either retain, correct, or deliberately omit it with reason and review.                                                                                           |
| Broken, orphaned, or stale old-pack link      | Stop the route switch or deletion, repair every clickable link, reconcile the tracked-text literal inventory and historical allowlist, then rerun the named link and path checks.       |
| Generated artifact stale                      | Run only the canonical generator, inspect the diff, and require its `--check` mode to pass before deletion.                                                                             |
| Generator produces a false implementation gap | Correct the generator or explicitly downgrade the affected research conclusion; never regenerate and present a known-invalid snapshot as truth.                                         |
| Validator/template contract conflict          | Stop authoring for the affected document type, reconcile the normative owner and validator, then resume.                                                                                |
| Unrelated repository gate fails               | Preserve the exact failure and attribution in the verification ledger; do not broaden scope without approval and do not claim whole-repository pass.                                    |
| Subagent overwrites another unit              | Enforce file ownership, require status/diff review before commit, and restore only the affected unit from Git history without destructive reset.                                        |
| Deletion begins too early                     | Keep old and new packs side by side until all pre-deletion gates pass; the old-pack deletion is a separate commit and is recoverable from its parent commit.                            |
| Secret or private state appears in evidence   | Stop, avoid committing the value, report the boundary, and use identifiers or redacted metadata only.                                                                                   |

The approved deletion boundary is intentionally asymmetric: authoring may
continue while a non-destructive validation defect is investigated, but the
old pack must remain intact until every deletion gate passes.

## Verification

### Leaf gates

Each leaf must pass:

- the selected Stage 90 metadata and heading contract;
- direct-link and pseudo-link validation;
- requirement and scope ownership review;
- source access-date and evidence-class review;
- tracked-source re-measurement review; and
- independent specification and quality reviews with zero unresolved Critical
  or Important findings.

### Pack gates

Before routing switches, the new pack must pass:

- twenty-of-twenty leaf presence and README routing coverage;
- thirty-six-of-thirty-six requirement-matrix coverage;
- one-hundred-percent coverage of the fourteen normative scopes;
- source-ledger completeness for load-bearing external claims;
- no unsupported live-runtime or remote-enforcement claims; and
- deterministic metadata and local-link validation.

### Pre-deletion gates

Deletion of the old twenty files is authorized only when all of these are true:

1. every old file and every unique material claim is mapped;
2. every retained or corrected claim resolves to a reviewed new destination;
3. every omission has a reason and preserved provenance;
4. clickable references to the old pack are zero across all tracked text
   outside the retiring directory;
5. all thirty-six requirements and all fourteen scopes are complete;
6. independent reviews have zero unresolved Critical or Important findings;
7. changed-document metadata and traceability pass; document implementation
   alignment reports zero findings attributable to this work and no increase
   over its pinned 184-finding archive-link predecessor; and the whole
   repository contract check passes—a missing dependency or other environment
   failure pauses deletion until that gate can run successfully;
8. LLM Wiki and security-readiness artifacts pass their canonical named
   freshness checks, and a repository-contract pass is not accepted as a
   substitute. Before deletion, the commit-pinned target-surface manifest and
   summary remain unchanged and may carry the measured Task 10 checkpoint of
   `9 manifest / 26 promoted / 9 summary`; the one promoted increase over the
   root `9/25/9` baseline is the separately recorded Foundation consumer for
   the new Task index. The seven retiring rows themselves must remain
   unchanged and introduce no new finding. This exception does not apply to
   byte-exact freshness generators; and
9. the Task records the before/after file manifest, deletion diff, recovery
   commit, and reviewer verdict.

Requirement 4 is evaluated over the complete tracked-text universe defined in
Old-path inventory and allowlist. Every permitted historical non-link literal
must appear in the reviewed allowlist; there is no clickable-link exception.

Requirement 5 is evaluated over the requirements and scopes whose delivery
precedes deletion. A requirement whose Spec-assigned owner is a post-deletion
unit is complete for this gate when its pre-deletion portion is satisfied and
its remaining portion is recorded as pending against that named owner. REQ-35 is
the only such requirement: its logical-unit commits and independent reviews are
pre-deletion obligations, while final verification and branch handoff belong to
Task 12, which runs after deletion. Without this rule the gate is unsatisfiable
by construction, because it would require a post-deletion unit to have finished
before deletion.

Requirement 6 quantifies over independent reviews of units inside this gate set.
A separately tracked track that gates nothing outside itself, such as the Gate 9
publication mechanism after the deletion-evidence decoupling amendment, is
outside that quantification: its findings bind that track and do not block
deletion. This is a scope statement, not a threshold change. Every unit bearing
on deletion still requires zero unresolved Critical and Important findings, and
a finding may not be moved out of scope by reclassifying its unit after the
finding is recorded.

Requirement 6 recognizes three closures for a recorded Critical or Important
finding: a re-review of the corrected range returning zero at that severity, an
explicit reviewed disposition closing the finding, or withdrawal of the
finding's subject. Withdrawal applies when the code, design, or contract the
finding was raised against is no longer current. It requires the withdrawal to
be recorded and the finding to be marked closed-by-withdrawal in the Task with a
citation to the withdrawing decision. A withdrawn subject cannot receive a
re-review, so without this closure such findings stay unresolved permanently and
the gate is again unsatisfiable by construction. Withdrawal closes the finding;
it does not assert the finding was wrong, and it does not license withdrawing a
subject in order to escape a finding.

The Task enumerates every closure it relies on for requirement 6, by finding,
closure kind, and citation, so the gate is auditable without re-deriving the
review history.

### Post-deletion gates

After deletion, run and record at least:

- changed-document metadata validation against the pinned base;
- document traceability validation;
- repository contract validation;
- document implementation-alignment validation with zero attributable delta
  and no increase over the pinned 184-finding predecessor;
- the canonical LLM Wiki index and coverage freshness checks;
- the target-surface delta advisory check and canonical delta-summary
  regeneration/freshness check;
- the target-surface convergence manifest and summary checks, requiring the
  target-surface wave to PASS after its eight reviewed delete mappings while
  separately classifying any unchanged Foundation promoted predecessor;
- the complete retiring-path literal scan, historical allowlist reconciliation,
  and broken-link scan covering all tracked text and generated documents;
- `git diff --check` and an exact changed-file review;
- a source/thirty-six-requirement/fourteen-scope/claim-ledger completeness
  audit; and
- final whole-branch specification and quality review.

A pass is valid only for the exact committed range reviewed. If a final fix
changes that range, the affected checks and final review must be repeated.

### Completion and branch handoff

The specification is complete only when the new pack is the sole active
canonical research pack with exactly twenty-one files—one README and twenty
reviewed leaves—the old twenty files are deleted after the gates, current
routes and generated artifacts resolve to the new path, the Task and memory
evidence accurately record results and residual failures, and final review
approves the exact branch range.

The finishing workflow then presents the user with the verified branch state
and explicit integration choices. No push, pull request, merge, or branch
deletion is implied by local completion.

## Agent Role and IO Contract

The Stage 04 artifacts are fixed as
`docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md` with
artifact ID `plan:2026-08-08-agentic-research-pack-rebuild` and direct parent
`spec:137-agentic-research-pack-rebuild`, and
`docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md` with
artifact ID `task:2026-08-08-agentic-research-pack-rebuild` and direct parent
`plan:2026-08-08-agentic-research-pack-rebuild`.

### Controller

- **Inputs:** active specification, Plan, requirement matrix, source ledger,
  migration manifest, repository baseline, and reviewer findings.
- **Outputs:** bounded assignments, accepted logical commits, updated ledgers,
  verification evidence, and final handoff.
- **Guardrails:** no overlapping file ownership, no unreviewed deletion, no
  remote mutation, no secret-value access, and no claim of a pass beyond the
  observed evidence.

### Research implementer

- **Inputs:** assigned requirement IDs, leaf ownership, source families,
  workspace evidence paths, current ledgers, and exact acceptance checks.
- **Outputs:** newly authored leaf documents plus source, requirement, scope,
  and claim-ledger updates for the assigned unit.
- **Guardrails:** verify rather than copy old prose; cite primary sources;
  preserve evidence boundaries; do not edit files outside ownership; do not
  implement the gaps being researched.

### Specification reviewer

- **Inputs:** active spec, assigned requirement rows, old-claim mappings,
  changed files, and source evidence.
- **Outputs:** requirement-by-requirement verdict and severity-ranked findings.
- **Guardrails:** verify source support and workspace derivation independently;
  do not author implementation changes while reviewing.

### Quality reviewer

- **Inputs:** changed files, metadata/profile contracts, route graph, scope
  matrix, and verification results.
- **Outputs:** clarity, consistency, lifecycle, link, evidence-boundary, and
  maintainability verdict.
- **Guardrails:** reject stale counts, semantic link drift, ambiguous ownership,
  and Stage 90 prose that reads as active policy.

### Final reviewer

- **Inputs:** exact base-to-head range, all ledgers, all logical commits,
  deletion evidence, and final validation output.
- **Outputs:** final Critical/Important/Minor findings, approval state, and a
  statement of whether the old-pack deletion and canonical switch are safe.
- **Guardrails:** review the complete committed range; any material follow-up
  fix invalidates the prior final verdict until re-reviewed.

## Related Documents

- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage 03 index](../README.md)
- [Spec template](../../99.templates/templates/sdlc/spec.template.md)
- [Stage 90 research index](../../90.references/research/README.md)
- [Current research pack](../../90.references/research/2026-08-08-agentic-engineering-research-pack/README.md)
- [Stage 98 archive index](../../98.archive/README.md) — canonical route for
  archived `spec:104-agentic-research-pack-refresh` and
  `spec:122-agentic-research-pack-consolidation`
- [Spec 136](../136-sdlc-taxonomy-convergence/spec.md)
- [Agent governance bootstrap](../../00.agent-governance/rules/bootstrap.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
