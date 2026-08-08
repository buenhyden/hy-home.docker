---
status: active
artifact_id: task:2026-08-07-agentic-research-pack-extension
artifact_type: task
parent_ids: []
---

# Task: Agentic Research Pack Extension and Revalidation

## Overview

This Task extends the single canonical agentic research pack at
`docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` with
three new Stage 90 reference leaves and revalidates the fifteen existing
leaves against current repository state and current official external sources.

The Task does not create a new dated research pack. Spec 122 previously
consolidated a duplicate dated pack and demoted
`2026-07-07-agentic-research-pack-update/` to `superseded` precisely to remove
that fragmentation. This Task preserves that outcome by extending the canonical
pack in place.

This Task is the approved successor Task requested by the previous
current-memory handoff. Opening it resolves the current-memory requirement for
an active Task with `draft` or `active` status and releases the lifecycle
boundary that paused
`task:2026-07-26-agent-governance-canonical-convergence`.

## Inputs

- User request to research and record harness engineering, loop engineering,
  workspace application criteria, Claude/Codex implementation status and common
  contract, spec-driven development, Docker Compose, infrastructure, SDLC,
  SDLC document roles, PRD/ARD/ADR roles, guide/incident/postmortem/policy/
  release/runbook roles, documentation architecture including Diataxis,
  LLM-WIKI, CI/CD, GitHub Actions, QA, security, AI agent catalogs, task-fit
  model selection, and memory hierarchy
- Baseline commit `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`
- Task open time `2026-08-07T12:36:55+09:00`
- Existing canonical pack: fifteen leaves and one folder-index README
- [Research category README](../../90.references/research/README.md)
- [Reference template](../../99.templates/templates/common/reference.template.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Goals and Non-goals

### Goals

- Add three new canonical pack leaves that close verified coverage gaps:
  documentation architecture including Diataxis, the LLM-WIKI system, and the
  agent memory hierarchy.
- Revalidate the fifteen existing leaves on two axes: repository-local counted
  facts, and current official external sources.
- Update the pack README and the parent research README so structure, current
  references, and reading order match the new leaf set.
- Record exact verification commands and their observed results.

### Non-goals

- Creating a new Stage 03 specification or Stage 04 plan.
- Creating a new dated research pack directory.
- Preserving the `2026-07-07-agentic-research-pack-update/` pack. A later user
  instruction in the same session directed consolidation of same-purpose
  documents with the latest content preferred, and selected full removal of
  that pack. See T-ARPE-012.
- Changing Stage 00 policy, Stage 03 specifications, Stage 05 procedures, or
  any runtime, Compose, provider, or CI configuration.
- Promoting any currently `unverified` claim without new observation.

## Scope and Change Boundaries

### Allowed Paths

T-ARPE-013 operates under a separate user instruction that authorized source
revalidation, resolution of the heading-contract conflict, and remediation of
the predecessor drift. It narrowly extends the allowed set to
`docs/99.templates/templates/common/reference.template.md`,
`docs/99.templates/support/document-metadata-profiles.yaml`,
`scripts/validation/check-repo-contracts.sh` template-heading list,
`scripts/hardening/check-all-hardening.sh` image-tag expectations,
`infra/tech-stack.versions.json`, and the two Stage 05 comparison guides.

- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/**`
- `docs/90.references/research/README.md`
- `docs/04.execution/tasks/2026-08-07-agentic-research-pack-extension.md`
- `docs/00.agent-governance/memory/current.md` (handoff refresh only)
- Generated artifacts whose freshness contracts the above changes trip, limited
  to regeneration by their registered generators:
  `docs/90.references/llm-wiki/llm-wiki-index.md`,
  `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`, and
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`
- For T-ARPE-012 only, inbound-link repair in
  `docs/03.specs/122-agentic-research-pack-consolidation/spec.md`,
  `docs/03.specs/122-agentic-research-pack-consolidation/README.md`,
  `docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md`,
  and `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`,
  plus removal of
  `docs/90.references/research/2026-07-07-agentic-research-pack-update/**`

### Forbidden Paths

- `docs/00.agent-governance/rules/**`, `scopes/**`, `providers/**`,
  `contracts/**`
- `docs/01.requirements/**`, `docs/02.architecture/**`, `docs/03.specs/**`
- `docs/05.operations/**`
- `infra/**`, `scripts/**`, `.github/**`, `.claude/**`, `.codex/**`,
  `.gemini/**`, `.agents/**`, `secrets/**`

The Stage 03 and Stage 05 entries above were the boundary for T-ARPE-001
through T-ARPE-011. T-ARPE-012 narrowly reopens Spec 122 and the two 2026-07-10
consolidation artifacts for inbound-link repair only, under the separate user
instruction recorded in its approval note.

### Compose Impact

None. This Task does not read, modify, start, stop, or validate any Compose
service, and does not inspect any secret value.

### Security Impact

None to runtime posture. The Task records security-governance references only.
No credential, token, private key, shell history, or raw log is written into
any artifact.

### Operations Impact

None. No runbook, incident, policy, or release procedure changes.

### Runtime Impact

None. No provider runtime surface, hook wrapper, or generated adapter changes.

## Approval Evidence

### Approval Source

Direct user instruction opening this session, which authorized sub-agent use,
authorized writing research output under `docs/90.references/research`, and
required logical-unit commits. Three structural decisions were then confirmed
by the user in-session:

1. Extend the existing canonical pack in place rather than create a new dated
   pack.
2. Revalidate on both axes: repository facts and full external sources.
3. Create a Stage 04 Task only, without a new Spec or Plan.

### Protected Surfaces

No protected surface is touched. No remote mutation, no push, no branch
protection change, no workflow change, and no live provider call beyond
read-only public documentation retrieval.

### Approval Boundary

The approval covers local documentation authoring and local commits on the
current branch. It does not cover push, remote mutation, runtime changes,
Compose operations, or execution of the controlled all-files pre-commit
wrapper.

### Rollback or Recovery

Every change is an ordinary tracked Markdown commit on the current branch.
Recovery is a `git revert` of the listed commits. No generated artifact,
runtime state, or external resource requires cleanup.

### Redaction Boundary

Only public documentation URLs, repository-relative paths, counted facts,
command names, and exit results are recorded. No secret value, token,
credential, private environment diagnostic, or raw log stream is written.

## Work Breakdown

| ID         | Unit                                                | Deliverable                                                                                      | Status |
| ---------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------ |
| T-ARPE-001 | Open Task and fix scope                             | This Task document                                                                               | Done   |
| T-ARPE-002 | Read-only research and fact re-derivation           | Sub-agent findings for three new topics, workspace count drift, and external source revalidation | Done   |
| T-ARPE-003 | New leaf: documentation architecture                | `documentation-architecture.md`                                                                  | Done   |
| T-ARPE-004 | New leaf: LLM-WIKI system                           | `llm-wiki-system.md`                                                                             | Done   |
| T-ARPE-005 | New leaf: memory hierarchy                          | `memory-hierarchy.md`                                                                            | Done   |
| T-ARPE-006 | Revalidate harness, loop, and provider leaves       | Four updated leaves                                                                              | Done   |
| T-ARPE-007 | Revalidate SDLC and document leaves                 | Four updated leaves                                                                              | Done   |
| T-ARPE-008 | Revalidate quality, security, and automation leaves | Four updated leaves                                                                              | Done   |
| T-ARPE-009 | Revalidate baseline, Compose, and catalog leaves    | Three updated leaves                                                                             | Done   |
| T-ARPE-010 | Update pack README and research README              | Two updated indexes                                                                              | Done   |
| T-ARPE-011 | Verification and evidence closure                   | Command results and memory handoff refresh                                                       | Done   |
| T-ARPE-012 | Consolidate same-purpose research documents         | Superseded pack removed, mapping folded into the category index, inbound links repaired          | Done   |
| T-ARPE-013 | Revalidate blocked sources and remediate drift      | Five sources verified, heading conflict resolved, eight of ten drift findings closed             | Done   |

## Work Log

- `2026-08-07T12:36:55+09:00` — Task opened at baseline
  `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`.
- Coverage analysis completed before authoring: of twenty-two requested
  research topics, nineteen already have canonical pack coverage across
  fifteen leaves totalling 3,523 lines. Three topics have no coverage:
  Diataxis-based documentation architecture, the LLM-WIKI system, and the
  agent memory hierarchy. `grep -rn -i diataxis docs/` returned zero matches.
- Six read-only sub-agents dispatched for the three new topics, workspace
  count re-derivation, provider source revalidation, and standards source
  revalidation. Sub-agents do not write files; all authoring is performed by
  the controlling session to avoid concurrent-write conflicts.

- T-ARPE-012 opened on a separate user instruction to consolidate same-purpose
  documents under `docs/90.references/research`, preferring the latest content.
  Investigation found one same-purpose duplication: five leaf filenames existed
  in both packs. The five 2026-07-07 leaves and their index were pure redirect
  stubs carrying no analysis, 416 lines in total. The user selected full removal
  with the canonical destination mapping folded into the category index.
- Path mentions inside the 2026-07-10 Plan's change inventory and verification
  commands are historical execution records and were retained as written; only
  its one Markdown link was repaired. The generated LLM Wiki index fell from
  1,330 to 1,324 path rows.

### T-ARPE-013 Outcome

All five previously unfetchable sources were verified. The earlier record
described three of them as HTTP 429 rate limiting; that diagnosis was wrong.
Those hosts return a Cloudflare bot challenge that uses 429 as its status code,
so retrying later never clears it from an automated client. Each was resolved
through its upstream source of record instead.

- Diataxis: the pinned upstream commit is the current upstream head with no
  later change to the source tree, so every quotation is re-verified.
- EditorConfig: version 0.17.2 confirmed, and the specification defines a ninth
  property, `spelling_language`, that the earlier summary omitted.
- pytest fixtures: concept, dependency injection, scope, and the xUnit
  comparison all confirmed.
- OpenAI practical guide: verified from the official CDN copy after the
  marketing page refused automated retrieval; the earlier caveat is lifted.
- ISO: the withdrawal of ISO/IEC/IEEE 12207:2017 is confirmed from the
  ISO-operated committee catalog at stage 95.99, with ISO/IEC/IEEE 12207:2026
  named as successor. 29148:2018 and 42010:2022 remain current.

The heading-contract conflict is resolved by aligning the two outliers to the
corpus rather than migrating documents. No document in `docs/90.references` had
ever used `## Facts and Definitions`; 69 used `## Definitions / Facts`. The
reference template, the reference role required headings, and the
template-source heading list in the repository contract check now use the
corpus heading. The audit role's forbidden-heading entry was left unchanged
because 34 audit documents already carry that heading.

Predecessor drift fell from ten findings to two. The six tech-stack registry
entries, the tech-stack provenance snapshot, and two hardcoded image-tag
expectations in the hardening script were catch-up corrections only: every
Compose file already declared the newer image, so no service version changed.
A seventh drifted image, dozzle, surfaced only after the Keycloak expectation
was corrected. The two Stage 05 comparison guides now record measured counts.

## Verification Evidence

### Exact Commands

- `bash scripts/validation/check-repo-contracts.sh`
- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base <safe-base>`
- `bash scripts/validation/check-doc-traceability.sh`
- `git diff --check`

### Expected Evidence

- Repository contract check reports no failure attributable to a changed path.
- Changed-document metadata validation passes except for the recorded
  heading-contract conflict.
- Traceability check resolves every new and updated cross-link.
- No whitespace or newline drift in the final diff.

### T-ARPE-012 Approval Note

Spec 122 contemplated this disposition. Its risk table pairs the failure mode
"Consolidation would erase unique historical evidence" with the escalation
"Required before deletion or archive migration", and that escalation is
satisfied by the user's explicit instruction in this session. Two consequences
are recorded rather than hidden. Spec 122 line 173 states that the pack
"remains at its current path", which this removal supersedes. Acceptance
criterion VAL-ARC-006 refers to the pack and its children, which no longer
exist; the canonical destination mapping it protected is preserved in the
Superseded Paths table of the research category index. Spec 122 stays
`completed` and is not reopened beyond inbound-link repair.

### Observed Evidence

- `bash scripts/validation/check-repo-contracts.sh` exits 1 with
  `failures=10`. Every failing subject is untouched by this Task: the private
  environment key comparison pair, the missing `html5lib` validation-runtime
  dependency, the Keycloak hardening image tag, the stale tech-stack provenance
  snapshot, and version drift for Traefik, Keycloak, PostgreSQL, Prometheus,
  Alloy, and Ollama. No `infra/`, `scripts/`, or `.github/` path was changed by
  this Task, which is verifiable from the changed-path list of
  `19ee4727..HEAD`. The count fell from 13 to 10 during this Task because the
  three generated-artifact freshness failures this Task introduced were
  resolved by regeneration.
- `python3 scripts/validation/check-document-metadata.py --mode check-changed
--base 19ee47270e3897073ab9a3f86dfd4cce0f4b2e74` reports `selected=24
violations=3`. All three are the same `body-heading-missing` finding on the
  three new leaves, caused by the recorded heading-contract conflict between
  the two validators. No other changed document has a finding.
- `bash scripts/validation/check-doc-traceability.sh` passes with
  `catalog_pairs_total=46 failures=0`.
- `git diff --check` reports no whitespace or newline drift.

## Review Evidence

### Specification Review Verdict

Not requested. This Task authored Stage 90 reference material under an explicit
user instruction and did not create or change a specification.

### Quality Review Verdict

Independent review has not been performed. This Task's authoring and its
verification were both carried out by the controlling session, so the recorded
verdicts are self-reported and do not satisfy an independent review boundary.

### Review Findings and Disposition

One blocking defect was found by this Task's own verification and is recorded
rather than fixed, because the fix touches this Task's forbidden paths. See
Blocked Items.

## Commit Ledger

### Commit Identity

Ten commits on the current branch, from baseline
`19ee47270e3897073ab9a3f86dfd4cce0f4b2e74` to
`46482182632b14ff475b4dac23ae609a6c7a7cba`:

| #   | Commit     | Unit                                                         |
| --- | ---------- | ------------------------------------------------------------ |
| 1   | `867a8146` | Task open                                                    |
| 2   | `dabd4a5d` | New leaf: documentation architecture                         |
| 3   | `c549bbdb` | New leaf: LLM-WIKI system                                    |
| 4   | `9e8a21d9` | New leaf: memory hierarchy                                   |
| 5   | `cbe87555` | Revalidate harness and provider leaves                       |
| 6   | `98564c16` | Revalidate SDLC and document leaves                          |
| 7   | `ddb78004` | Revalidate quality and security leaves                       |
| 8   | `b7fbf151` | Revalidate baseline and infra leaves                         |
| 9   | `23d6e31c` | Update research pack indexes                                 |
| 10  | `46482182` | Stage-contract heading alignment and generated-index refresh |

### Commit Logical Unit

One commit per work-breakdown unit: Task open, each new leaf, each
revalidation group, index updates, and evidence closure.

### Commit Validation

Each commit was preceded by changed-file metadata validation. Full repository
contract validation ran three times: once before regeneration, once after the
LLM Wiki regeneration, and once after the semantic inventory regeneration.

## Deferred and Blocked Items

### Deferred Items

- A typed domain-memory taxonomy with validator-enforced promotion, retention,
  archival, and deletion remains outside this Task. This Task records the
  research basis for it in `memory-hierarchy.md` but does not implement policy.
- Predecessor runtime drift for Keycloak, Traefik, PostgreSQL, Prometheus,
  Alloy, and Ollama versions remains routed to a separate approved runtime
  Task.

### Blocked Items

- Resolved in T-ARPE-013. Previously: **a new Stage 90 reference cannot satisfy
  both heading contracts.**
  `scripts/validation/check-repo-contracts.sh` hard-requires the literal
  `## Definitions / Facts`, while the reference role in
  `docs/99.templates/support/document-metadata-profiles.yaml` requires the H2
  `## Facts and Definitions`. Both were exercised against the three new leaves:
  each heading choice fails the other gate with exactly three findings. The
  leaves use `## Definitions / Facts` to match their fifteen siblings and the
  continuous-integration-enforced stage contract, and carry the metadata
  finding. Both candidate fix sites are in this Task's forbidden paths, so the
  correction requires separate approval.
- Provider acceptance and entitlement, live comparative model evaluation, and
  authenticated remote GitHub enforcement remain unverified. This Task records
  them as unverified and does not promote them.
- Resolved in T-ARPE-013. All five sources are verified through upstream
  sources of record.
- Two drift findings remain open and both need an action outside this Task.
  The private `.env` carries three InfluxDB keys that `.env.example` does not,
  which the user chose to leave as an environment fact. The `html5lib`
  validation-runtime dependency is declared in `scripts/requirements.txt` but
  is not installed, and installation is blocked by PEP 668 in this
  externally-managed Python environment.
- Independent review of this Task has not been performed.

### Deferral Destination

- Domain-memory taxonomy: a future Stage 03 memory-governance specification.
- Runtime and Compose drift: a separate approved runtime Task.
- Reference heading-contract conflict: a change to either
  `scripts/validation/check-repo-contracts.sh` or
  `docs/99.templates/support/document-metadata-profiles.yaml`, both outside this
  Task's allowed paths.

## Related Documents

- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Research category README](../../90.references/research/README.md)
- [Spec 123 audit remediation](../../98.archive/03.specs/123-agentic-engineering-audit-remediation/spec.md)
- [Predecessor convergence Task](./2026-07-26-agent-governance-canonical-convergence.md)
- [Current project memory](../../00.agent-governance/memory/current.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
