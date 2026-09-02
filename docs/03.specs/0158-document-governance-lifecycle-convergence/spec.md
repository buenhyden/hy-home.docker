---
title: Document Governance Lifecycle Convergence Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0158
parent_ids: [REQ-0024, REQ-0025, ADR-0029, SPEC-0157]
created: 2026-08-31
updated: 2026-09-02
---

# Document Governance Lifecycle Convergence Specification

## Overview

The repository's registered document gates pass while semantic and lifecycle
drift remains in the corpus. At the design baseline, the selected stage roots
contain 588 tracked Markdown files. The largest active Plan has 19,023 lines,
the three completed Stage 98 Migrations have 19,878 lines combined, active
Stage 90 material still presents retired Stage 04 and predecessor paths as
current in places, and several Spec Packages have parent and child lifecycle
states that cannot all be true at once.

SPEC-0157 also has implementation commits while its Spec and Plan are `draft`
and it has no Task. This specification therefore starts by restoring an honest
SPEC-0157 chain, then converges the current corpus by lifecycle rather than by
directory. Canonical owners are repaired before non-normative evidence is
retired, compressed, or removed. Git remains the recovery boundary; Stage 98
does not become a copy of deleted bodies. Its current Migration documents are
temporary historical inputs: all current consumers move to canonical owners
before the documents and `migrations/` directory are deleted.

The convergence reduces authority and validation machinery. It creates no new
top-level stage, public suite, public gate profile, document lifecycle, audit
pack, progress document, or compatibility redirect.

## Boundaries and Inputs

### In Scope

- `docs/00.agent-governance/`, `docs/01.requirements/`,
  `docs/02.architecture/`, `docs/03.specs/`, `docs/05.operations/`,
  `docs/90.references/`, `docs/98.archive/`, and `docs/99.templates/`.
- Work in progress whose state affects those stages, beginning with SPEC-0157.
- Stage indexes, metadata, lifecycle, traceability, templates, generated
  provider adapters, and recovery records affected by a disposition.
- Registered document and governance validators, their focused tests, and the
  manifest or workflow routing needed to remove duplicate ownership.
- Fixtures and Git provenance logic that currently validate retired document
  bodies or pin branch and corpus state.

### Out of Scope

- Runtime mutation, deployment, remote systems, secrets, credentials, or live
  infrastructure validation.
- Product or service behavior changes unrelated to document truth.
- Changing the six public suite responsibilities fixed by ADR-0029.
- Creating a replacement taxonomy, a new lifecycle vocabulary, or a second
  provider-independent policy source.
- Preserving obsolete text merely because it is historical.

### Authoritative Inputs

- REQ-0024, Agent Governance Standardization.
- REQ-0025, Operational Readiness Closure.
- ADR-0029, Workspace Governance Authority.
- Stage 00 bootstrap, SDLC, documentation, approval, workflow, and authoring
  policies.
- Stage 99 Registry, schemas, and registered templates.
- The current script manifest and workflow contract.
- Current Git-tracked implementation surfaces, including infrastructure and
  example configuration, scripts, registries, manifests, workflows, provider
  adapters, tests, and the commands operated through Stage 05.
- Git-tracked consumers, current branch state, and regular-blob recovery
  evidence measured at execution time.
- The user preservation ruling for the latest externally researched and saved
  Stage 90 package, `RES-0002`.

## Behavior Contract

### Authority and Disposition

Every tracked target is covered exactly once by an ordered Task-local
disposition rule:

- `keep`: the artifact is current, uniquely owned, and consumed;
- `rewrite`: the owner is correct but its current text is not;
- `consolidate`: unique current content moves into one canonical owner;
- `supersede`: useful point-in-time evidence remains explicitly non-current;
- `delete`: no current authority, consumer, or preservation need remains;
- `tombstone`: a deleted stable path needs a minimal recovery pointer.

These values are execution decisions, not document lifecycle statuses. A
verified `keep` cohort may be covered by one deterministic profile or path rule;
every non-`keep` target is listed by path. The Task records the rule, covered
count, exceptions, current owner, consumers, disposition, replacement, recovery
evidence, and review. The rules and exceptions must cover the measured target
set without overlap or omission. Missing or ambiguous evidence blocks mutation.

### Latest External Research Preservation

The complete set of files existing at the execution baseline under
`docs/90.references/research/0002-agentic-engineering-research-pack/` is one
atomic, Task-local `PROTECT_LATEST` unit. This classification is a user
preservation override, not a Registry lifecycle or disposition value. The
package remains protected from deletion, archival, or loss of its substantive
research body, sources, and claims even if its current consumer set later
becomes empty.

Path, metadata, lifecycle, stale-owner, and link corrections are permitted, as
is non-lossy integration with a current owner. Preservation is semantic rather
than byte-for-byte: no checksum, content digest, or expected Git SHA becomes an
acceptance control. The sole preservation subject is the entire tracked current
execution-baseline package measured by Task 2. Historical commits only
illustrate edit types: `95142c3a` promoted and activated the draft;
`07b94403` later restored and merged substantive content across all 21 files;
`3bf50f94` later added claim-bearing corrections; `65e8dfde` remains the last
new-leaf addition; and `6663f02c` is link-only. Other later governance or path
edits may exist. No named historical commit represents the final protected
content, a restore target, Gate, baseline, or branch-lineage control.

Task 2 records the dynamic path inventory as execution evidence. Before that
Task evidence can be compressed or removed, Task 6 writes a clearly owned,
package-local preservation declaration in the `RES-0002` README. The
declaration records the user retention decision and a path list or selector for
the protected content without hashes, expected SHAs, byte equality, or a pinned
count. Existing reference/document-governance tests derive the declared set,
require equality with the safe tracked files under the package root, verify
presence, and preserve the zero-consumer override; they do not pretend to
automate semantic equivalence of the research body, sources, or claims.

The package and its declaration remain non-normative research evidence. The
declaration records the decision and test input; this Specification's
acceptance contract supplies its authority. Research findings never become
governance policy merely because they are protected.

Amended 2026-09-02: a Stage 90 package governed by a registered Stage 99
profile is retained under that profile. The `audit`, `audit-member`, `data`,
and `generated` profiles now carry registered identity shapes (`AUD-####`,
`AUD-####-m####`, `DATA-####`, `DATA-####-m####`), so those packages have a
current owner and are no longer convergence targets. An unregistered Stage 90
package outside `RES-0002` remains a mandatory convergence target. A package
root is a category child directory under
`docs/90.references/{audits,data,research}/`; root and category READMEs are
structural indexes, not packages. An unregistered package with no current
consumer is deleted; one with a current consumer or unique needed meaning first
migrates that consumer or meaning to its current canonical owner and is then
deleted. At completion, every remaining package root resolves to a registered
Stage 99 profile, with zero unresolved or pending package disposition. Stage 90
root and category READMEs are structural indexes rather than evidence packages
and are regenerated or removed to match the resulting tree. A deletion creates
no redirect or body clone. A minimal package-README Tombstone is allowed only
when an actual live recovery-navigation consumer still requires the retired
stable path.

### Stage Responsibilities

- Stage 00 is the sole provider-neutral AI-agent governance authority. It
  defines policy, system rules, roles, skills, provider boundaries, and the
  common SDLC workflow; no product-stage document or generated adapter may
  redefine them.
- Stage 01 owns current solution-independent SDLC requirements. Substantively
  duplicate packages converge on one owner and use the registered Requirement
  contract.
- Stage 02 owns current SDLC architecture descriptions and the durable ADR log.
  Superseded ADRs remain in that decision log without becoming current rules.
- Stage 03 owns current capability Specs and honest change packets under the
  same SDLC lifecycle. Completed or cancelled execution bodies do not remain
  active guidance.
- Stage 05 owns current operational subjects and organizes them through the
  registered Guide, Incident, Postmortem, Runbook, and related Operations
  profiles. Duplicate procedures converge on one subject owner.
- Stage 90 owns non-normative workspace evidence organized as Audit, Research,
  and Data. In this convergence it keeps only the atomic user-protected latest
  external-research package; every other execution-baseline package migrates
  unique needed meaning and current consumers to canonical owners, then is
  deleted. Structural indexes are regenerated to match.
- Stage 98 owns only explicitly retained historical/archive records for SDLC,
  Operations, and References. Its `migrations/` directory is temporary while
  current consumers are decoupled and is absent at completion. The final tree
  keeps the structural README and only minimal archive/Tombstone records with a
  measured preservation or live recovery-navigation need; it stores no body
  clone, redirect, snapshot, raw Task ledger, or duplicate digest.
- Stage 99 is the sole machine authority for the document and file templates
  used under `docs/`, including paths, profiles, identifiers, sections,
  lifecycle, traceability shapes, and template sources. Provider Registry
  ownership of runtime projection paths is a separate, narrower namespace and
  does not compete with this document-template authority.

### Implemented Truth Promotion

Current implementation is an authoritative input to documentation alignment,
but source code, configuration, validators, workflows, Stage 05 procedures,
and Stage 90 evidence do not become substitute Requirement or Architecture
owners. Every implementation subject is classified by the truth it carries:

- an implemented required behavior, user-visible obligation, invariant, or
  guarantee maps to exactly one active Stage 01 Requirement;
- an implemented structure, component boundary, data flow, or integration
  boundary maps to exactly one current Stage 02 Architecture Description;
- a durable adopted architectural decision and its rationale map to exactly
  one active Stage 02 ADR, while the Architecture Description may reference
  rather than duplicate that decision ownership;
- a change delta and its execution history remain Stage 03 concerns;
- an operational procedure remains Stage 05, but its required behavior and
  structural prerequisites trace to Stage 01 and Stage 02; and
- an observation, audit result, research claim, or generated measurement
  remains non-normative Stage 90 evidence.

Coverage is bidirectional. Every currently implemented required behavior and
structural decision has the appropriate Stage 01 or Stage 02 owner, and every
Stage 01 or Stage 02 statement presented as current agrees with the observed
implementation. Future intent may remain in a Requirement or proposed
architecture only when it is explicitly distinguishable from implemented
current truth; it cannot be described as already implemented. Completed Specs,
validators, tests, Operations procedures, or evidence packages cannot be the
sole durable source for a current requirement or architecture fact.

Promotion translates current truth into the registered Requirement,
Architecture Description, or ADR form. It does not copy source files, test
fixtures, generated output, or execution logs into Stage 01 or Stage 02. The
execution Task records a dynamically measured subject-to-owner inventory and
zero-gap result; no fixed implementation count or new Gate is created.

### Archive Isolation

Documents under Stages 00, 01, 02, 03, 05, and 90 do not cite, link to, or use
any Stage 98 document or file as a source, replacement, related document,
membership input, or recovery lookup. The prohibition covers resolved Markdown
links and explicit archive-file path citations, including generated indexes.
It does not prohibit describing the Stage 98 role in current governance prose.

Recovery navigation is one-way: a retained minimal Stage 98 record may point
to its current replacement or canonical owner, but current authority never
points back to archive evidence. Stage 99 may define the minimal archive record
shape because it owns templates; that machine contract does not make an
archive record a current source.

### SDLC State

- An active Task has active Spec and Plan parents.
- A terminal or superseded parent has no active child.
- A completed Plan has only terminal Tasks.
- A current capability Spec may remain active without a Plan or Task.
- A change-packet Spec becomes terminal when its results have been written to
  current owners and its recovery boundary is known.
- Existing non-conforming work is recorded as discovered and revalidated; it
  is never described as retroactively approved.

### Agent Responsibility

- The user or operator grants approval.
- `workflow-supervisor` coordinates scope, order, handoff, and stop conditions
  without becoming the default writer.
- `doc-writer` edits approved canonical documentation.
- The actual Task owner records its own execution evidence.
- `qa-engineer` owns deterministic validator, fixture, and test changes.
- `eval-engineer` verifies evidence and evaluations but does not impersonate
  the evidence author.
- `rules-engineer` gives an independent governance verdict; that verdict is
  not user approval.
- `code-reviewer` independently reviews the exact diff and acceptance evidence.
- `hook-developer`, `ci-cd-engineer`, and `security-auditor` participate only
  when their protected surfaces change.

### Validation Ownership

The public suite names and the public `changed` and `full` profiles remain
stable. Within that interface:

- Stage 99 Registry owns document validity;
- `scripts/manifest.yaml` owns validator inventory and suite membership;
- `.github/workflow-contract.yml` owns CI routing and execution context;
- each validator owns its domain predicate;
- the current Task owns observed results.

No Task-numbered immutable inventory may restate the manifest.

## Technical Approach

### Wave 0: Restore SPEC-0157

Measure the commits and remaining work on the SPEC-0157 branch. Transition its
Spec and Plan through the registered lifecycle, create a current Task, and
record earlier commits as implementation discovered and revalidated at the
current revision. Do not claim prior approval. Because changed-document
validation compares merge-base endpoints, land the legal SPEC-0157 activation
and implementation while its Spec remains `active`, then close it from an
updated base where `active -> completed` is a legal endpoint. Complete or
explicitly defer the remaining bounded work, run the full gate, and close the
packet before corpus convergence implementation begins. Do not bypass the
merge boundary with a transition override.

### Wave 1: Classify the Corpus

Re-derive the tracked target set and create the complete disposition rule set in
the current Task. Assign `PROTECT_LATEST` atomically to every baseline file in
the `RES-0002` package before applying any disposition. Cover unchanged cohorts
by deterministic rule and list every non-`keep` target explicitly. Measure
profile, lifecycle, authority, consumers, duplicate purpose, retired-path
literals, generated provenance, Gate and fixture references, commit pins, and
recovery. In parallel, classify current implementation subjects and record the
Stage 01 or Stage 02 owner for each implemented obligation, structure,
boundary, and durable decision. Mutation begins only after the document rules
cover the target set exactly once, the implementation inventory has no
unclassified subject, and every destructive disposition has passed recovery
and review checks.

### Wave 2: Converge Canonical Owners

Repair Stage 00 and Stage 99 boundaries first. Then update the affected Stage
01, Stage 02, and Stage 05 owners, including ADR-0029's obsolete statement that
Migration 0003 is a permanent structural review boundary. Amended 2026-09-02:
the Stage 99 Migration profile, template route, lifecycle binding, and
allocation surface are retained. `MIG-####` is a registered identity shape and
`archive/migration.template.md` is a registered template, so the Migration
interface has a current owner; ADR-0029's correction is limited to removing the
review-boundary claim. Clarify that Stage 99 paths are document paths
and provider-registry paths are runtime projection paths. Separate workflow
coordination, mutation, evidence writing, evaluation, review, and human
approval in the existing role and provider contracts. Regenerate registered
provider adapters only after their canonical inputs are correct. Before
deleting duplicate or evidentiary descriptions, promote every observed current
implementation obligation to Stage 01 and every observed current structure or
durable decision to Stage 02, and correct any Stage 01 or Stage 02 statement
that describes an aspirational or obsolete state as current.

### Wave 3: Normalize SDLC Packages

Classify Stage 03 packages as current capability contracts or bounded change
packets. Reconcile actual work and lifecycle status, including the known
SPEC-0136, SPEC-0154, SPEC-0155, and SPEC-0157 inconsistencies. Reassess stale
active Tasks in SPEC-0102, SPEC-0123, SPEC-0134, and SPEC-0135 against current
consumers and branch evidence. Compress or remove obsolete execution detail
only after its current outcome and recovery have been captured.

### Wave 4: Reduce Evidence and Archive

Retain the complete `RES-0002` package under the user-preservation override
even if consumers reach zero. For every other Stage 90 source, migrate unique
needed meaning, citations, generated outputs, and current consumers to their
canonical owners, then delete the source package. Remove current-sounding
predecessor taxonomy without losing the protected research body, sources, or
claims. Remove or rewrite every Stage 98 file citation in the protected package
without treating that path cleanup as permission to reduce its research
meaning. Persist the Task 2 protected path set and user decision in the package
README and make the existing reference-test oracle GREEN before transient Task
evidence is retired. Amended 2026-09-02: the three completed Stage 98 Migrations are retained as
frozen historical evidence under the registered `migration` profile. Their
fenced ledger blocks stay byte-identical and their digest tripwire stays
active; only current authority coupling is removed, never the records. Retain an archive/Tombstone record only for an
explicit preservation need or a stable retired path that still has a measured
live recovery-navigation consumer, and remove its dependency on a Migration
parent or link. Never create a body copy or redirect.

### Wave 5: Simplify Gates, Fixtures, and SHA Tracking

Derive validator inventory from the script manifest and remove duplicate
immutable inventories. Preserve the six public suites and the `changed|full`
profiles. Merge lifecycle and Operations modes only after consumer and
equivalence proof; retain Stage 98 recovery validation.

Document-contract tests use three fixture forms only: a current contract
derived from the Registry, a one-field mutation, and a temporary-Git recovery
case. They do not resurrect deleted documents from a fixed workspace commit,
copy full historical bodies, or pin fixture and corpus counts.

Keep only the existing minimal Stage 98 validation needed for retained archive
or Tombstone records: safe paths, the registered minimal shape, and a
`commit:path` that resolves to a regular Git blob when recovery is claimed.
Amended 2026-09-02: retain the frozen-Migration digest tripwire, which proves
the historical evidence blocks are unmodified. Remove only the section-count,
row-count, topology, and current-membership checks that made a historical
ledger a current authority.

Allow commit identifiers only for supply-chain pins, retained minimal Stage 98
recovery, actual logical implementation commits recorded in the current Task,
and a bounded transition fallback proven to have a live recovery consumer.
Remove branch-tip equality, expected design or implementation SHA chains,
persistent blob or diff digest ledgers, historical byte equality, and test-only
workspace commit pins. This does not remove an ephemeral digest comparison
required by the shared-worktree concurrency policy; that comparison is not
retained as a document lineage control.

### Wave 6: Verify and Close

Run focused checks with each change, then the complete document, governance,
Operations, provider-parity, unit-test, and full CI profiles. Obtain independent
policy and exact-diff review. Write current outcomes back to canonical owners,
close terminal packets, and remove temporary or verbose execution material once
its registered recovery is proven. Re-run implementation alignment in both
directions and require zero implemented subjects without a Stage 01/02 owner
and zero current Stage 01/02 claims that contradict the tracked implementation.

## Interfaces and Data

| Interface | Contract after convergence |
| :--- | :--- |
| Stage 99 Registry | Sole machine source for document contracts and allocation |
| Provider Registry | Typed runtime routing, model, permission, hook, and projection data under Stage 00 policy |
| Stage authoring matrix | One writer, validator, and independent-review mapping per stage |
| Script manifest | Sole validator inventory and suite membership |
| Workflow contract | Public profile and CI execution routing |
| Disposition rule set | Task-local complete coverage rules plus explicit non-`keep` paths; never a lifecycle registry or corpus copy |
| Protected research declaration | Package-local, non-normative record of the user retention decision and protected path selector; SPEC acceptance remains authoritative |
| Implementation truth coverage | Task-local subject-to-owner evidence mapping implemented obligations to Stage 01 and implemented structures or decisions to Stage 02; no corpus copy, fixed count, or durable parallel registry |
| Temporary Migration | In-flight historical source mapping only; every current consumer moves before the interface and directory are deleted |
| Archive/Tombstone | Explicitly retained minimal historical record or stable retired-path recovery pointer; never current authority |
| Fixture | Current generated contract, one-field mutation, or temporary-Git recovery case |

Generated provider adapters may consume Stage 00 sources and provider routing
data but may not define policy, roles, lifecycle, templates, model intent, or
completion. Consumerless generated rules or workflows projections are removed;
retained projections receive an explicit canonical-source mapping.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Needed historical meaning or citations are lost during mandatory package retirement | Require provenance, current-consumer, replacement, recovery, and review decisions before deletion; migrate needed meaning rather than preserving the source package |
| A mechanical link correction is mistaken for the latest research save | Classify Git touches by diff purpose and preserve the atomic `RES-0002` package; never select it with a maximum-timestamp shortcut |
| Consumer cleanup removes the user-protected latest research | Apply `PROTECT_LATEST` before consumer disposition and retain its substantive body, sources, and claims even at zero consumers |
| Transient Task evidence is removed before protection remains enforceable | Persist the dynamic path declaration in the package README and make existing reference tests GREEN before Task retirement |
| Historical evidence remains active guidance | Migrate needed meaning to a current owner, then delete the non-protected Stage 90 package; active owners never defer to Stage 90 |
| Stage 01 or Stage 02 is aspirational, stale, or absent while implementation already exists | Observe the tracked implementation, classify behavior versus structure, promote it to the registered current owner, mark genuinely future intent explicitly, and run the existing implementation-alignment suite in both directions |
| A current SDLC, Operations, or Reference document cites Stage 98 | Move any still-current meaning to its canonical owner, remove the inbound citation or cross-link, and make the existing link/lifecycle suite reject recurrence |
| SPEC-0157 is presented as previously approved | Record the anomaly and current revalidation; preserve the real transition order |
| A Task disposition becomes a new lifecycle | Keep disposition values local to execution; validate document status against Stage 99 only |
| A historical Migration remains a current authority or permanent archive package | Block completion until every current consumer is moved and the Migration profile, files, and directory are removed |
| Stage 98 reduction breaks required recovery navigation | Inventory live consumers first and prove every retained recovery `commit:path` resolves to a regular Git blob before and after mutation |
| Gate reduction drops a live guarantee | Search every registered and direct consumer, add the replacement test, then remove the old path |
| Fixture cleanup removes a real domain oracle | Limit this reduction to document-contract history fixtures; retain agent-output and supply-chain oracles |
| Provider projection becomes a policy source | Correct canonical inputs first, generate through the registered renderer, and verify parity |
| A role grants approval it cannot own | Separate human approval, policy verdict, evidence evaluation, and mutation permissions |
| SHA reduction weakens concurrent-worktree safety | Retain policy-required ephemeral digest comparison but never persist it as lineage evidence |
| A public suite responsibility must change | Stop and require a separate ADR rather than expanding this specification |
| Concurrent or dirty state makes ownership unclear | Stop the Wave, preserve the state, and reclassify before editing |

## Acceptance Contract

1. Ordered Task-local rules and exceptions cover every tracked target at the
   execution baseline exactly once. Every non-`keep` path is explicit and has
   owner, consumer, replacement, recovery, and review evidence; unchanged
   cohorts are not copied into a path-by-path audit pack.
2. Active documents contain no retired Stage 04, predecessor support, rules,
   memory, agent, Spec-path, or template path presented as current procedure.
3. Every currently implemented required behavior has exactly one active Stage
   01 Requirement owner; every currently implemented structure, boundary, or
   data flow has exactly one current Stage 02 Architecture Description owner;
   and every durable adopted architectural decision has exactly one active ADR
   owner. Reverse validation finds no Stage 01 or Stage 02 statement presented
   as current that contradicts implementation; future intent is explicitly
   distinguishable from implemented truth. Stage 03, Stage 05, Stage 90,
   validators, and tests are never the sole durable owner of those current
   facts.
4. No two active Requirement, Architecture Description, Spec, Operations, or
   governance documents own the same purpose or rule.
5. Active Task, Plan, and Spec states are mutually consistent, and only actual
   work in progress remains active.
6. SPEC-0157 is normalized without retroactive approval and passes its full
   completion gate before SPEC-0158 implementation.
7. Every baseline file in the atomic `RES-0002` research pack remains present
   with its substantive research body, sources, and claims semantically
   preserved, even if consumers reach zero. Current path, metadata, owner, and
   link corrections and non-lossy integration are allowed without checksum or
   SHA pinning. Before transient Task evidence is retired, the package README
   persistently declares the user decision and protected path set without a
   pinned count, and existing reference tests derive that declaration and prove
   on-disk equality and presence. Semantic body/source/claim preservation
   remains a review obligation. Amended 2026-09-02: after consumer and
   needed-meaning migration, every remaining Stage 90 package root resolves to
   a registered Stage 99 profile; unresolved and pending unregistered package
   dispositions are both zero.
   Root and category indexes are excluded from this package-root set and match
   the resulting tree.
8. Amended 2026-09-02: Stage 98 retains `migrations/` and its three Migration
   documents as frozen evidence under the registered `migration` profile, with
   no current authority coupling. It otherwise contains only its structural
   index and minimal archive/Tombstone records proven necessary by an explicit
   preservation need or live recovery-navigation consumer; retained recovery pointers use safe paths and resolve to regular
   Git blobs. No Stage 98 artifact contains a deleted body clone, redirect,
   snapshot, raw execution ledger, duplicate digest, frozen topology, or
   current-membership authority.
9. Amended 2026-09-02: no current stage takes authority, membership, or
   control input from a Stage 98 document or file, and no current document
   links to one, measured as `archive_direct_links_total=0`. Because
   item 8 now retains the three Migrations as frozen evidence, a descriptive
   Stage 98 path literal inside a historical execution or decision record is
   permitted and is not an authority dependency. Any retained archive
   navigation points outward to current owners; no current owner points inward
   to archive evidence for a current decision.
10. Stage 99 Registry and templates contain no parallel or unused document
   authority, and every retained template has a registered target role.
11. The six public suites and `changed|full` profiles remain stable, every
   manifest validator executes exactly once in `full`, and no Task-numbered
   immutable validator inventory remains.
12. Document-contract tests contain no fixed-workspace historical document
    resurrection, fixture-count pin, corpus-count pin, or count-bearing test
    name.
13. Active Plans contain no branch-tip equality, expected SHA lineage,
    persistent blob or diff digest ledger, or historical byte-equality control.
    Only approved recovery, supply-chain, actual Task commit evidence, and
    policy-required ephemeral concurrency checks remain.
14. Workflow coordinator, writer, evidence author, evaluator, governance
    reviewer, exact-diff reviewer, and human approver responsibilities are
    distinct in canonical Stage 00 and provider routing.
15. Stage 99 document-path authority and Provider Registry runtime-projection
    authority are explicitly disjoint; renderer and hook inventories are
    derived from their declared owner rather than a second code constant.
16. Generated provider adapters are byte-for-byte fresh and define no policy.
17. Metadata active and contract checks, document graph, document lifecycle and
    recovery, agent-governance repository checks, Operations complete, focused
    unit tests, provider parity, `git diff --check`, and the full CI profile all
    pass.
18. No runtime, remote, deployment, secret, or infrastructure state is changed.

## Traceability

| Parent | Coverage |
| :--- | :--- |
| REQ-0024 | Canonical AI-agent governance, role separation, provider projection boundaries, current Stage terminology, and removal of documentation that conflicts with current implementation truth |
| REQ-0025 | Approved Spec/Plan/Task sequence, targeted and full validation, independent review, recovery, and honest completion |
| ADR-0029 | Stage 00/99 authority split and six public suites, corrected so current authority and structural review no longer depend on temporary Stage 98 Migrations |
| SPEC-0157 | Script and test ownership, reachable validation, current fixtures, derived census, and bounded Git-history behavior |

## Operational Impact

This specification changes tracked documentation, validation, tests, and
generated provider adapters only. It performs no deployment, restart, remote
mutation, credential access, secret inspection, or runtime recovery. Any
discovered runtime discrepancy is recorded as a separate deferred owner rather
than inferred from documentation.

## Related Documents

- [Agent Governance Standardization Requirement](../../01.requirements/0024-agent-governance-standardization.md)
- [Operational Readiness Closure Requirement](../../01.requirements/0025-operational-readiness-closure.md)
- [Workspace Governance Authority ADR](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Script Surface Ownership Convergence](../0157-script-surface-ownership-convergence/spec.md)
- [SDLC](../../00.agent-governance/sdlc.md)
- [Stage Authoring Matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Stage 99 Registry](../../99.templates/registry.json)
