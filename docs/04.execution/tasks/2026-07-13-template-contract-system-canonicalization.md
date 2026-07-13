---
status: active
artifact_id: task:2026-07-13-template-contract-system-canonicalization
artifact_type: task
parent_ids:
  - plan:2026-07-13-template-contract-system-canonicalization
---

# Template Contract System Canonicalization Execution Task

## Overview

This Task is the durable execution and review ledger for Spec 130 and its
implementation Plan. It covers Stage 99 registry, support, and copyable forms;
direct Stage 00 and validator fallout; preservation-oriented migration of the
typed baseline; generated evidence; and bounded routing for later corpus
waves.

The work runs serially in the isolated
`codex/template-contract-system-canonicalization` branch. Each of the seven
implementation units receives a fresh implementer, a separate specification
review, and a separate quality review before its logical commit.

## Inputs

- **Approved Spec**:
  [Spec 130](../../03.specs/130-template-contract-system-canonicalization/spec.md)
- **Active Plan**:
  [Implementation Plan](../plans/2026-07-13-template-contract-system-canonicalization.md)
- **Parent foundation**:
  [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- **Canonical audit**:
  [2026-07-05 implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Machine registry**:
  [document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- **Current contracts**:
  [Stage 99 support](../../99.templates/support/README.md)
- **User approvals**:
  destructive Stage 99 contract and governance changes, protected-surface
  fallout, logical commits, staged direct-consumer migration, and
  Subagent-Driven execution were explicitly approved in this task.

## Working Rules

- Follow Spec 130 and the active Plan exactly.
- Run Tasks T-TCS-001 through T-TCS-007 serially.
- Use a fresh implementation agent for each task.
- Run specification review before quality review.
- Resolve all Critical and Important findings before task commit.
- Record Minor findings and their disposition.
- Preserve completed and superseded evidence bodies.
- Do not infer review dates, parents, approvals, incidents, postmortems,
  releases, tests, or runtime truth.
- Keep one machine registry and one canonical owner per rule or form.
- Do not run `pre-commit run --all-files` directly.
- Use the controlled wrapper only from a clean committed worktree after the
  whole-branch review.
- Run `graphify update .` after code changes when available and treat the
  report as advisory.

## Approved Surface Evidence

| Surface | Approval and boundary | Allowed action | Forbidden action | Evidence |
| --- | --- | --- | --- | --- |
| `docs/99.templates/` | Explicit user scope and destructive-change approval | Reorganize contracts, registry, catalogs, and forms; add Audit; delete duplicate forms | Create a second registry or leave two canonical owners | Spec 130 and Plan |
| Stage 00 documentation | Direct governance and reference fallout approved | Update authoring, stage, checklist, Memory, and Progress routes | Add provider-local policy or runtime state | Per-task diff and reviews |
| `scripts/validation/` and `tests/validation/` | Validator implementation required by Spec | TDD changes to metadata and repository gates | Add an unrelated checker or expose raw bodies in diagnostics | RED/GREEN output |
| Typed baseline | Preservation-oriented direct migration approved | Remove template residue and normalize semantically equivalent headings | Rewrite historical commands, counts, verdicts, or decisions | Task 7 disposition |
| Canonical generated evidence | Generator-only update approved | Run named owner scripts and commit deterministic outputs | Hand-edit generated bodies | Generator output and check mode |
| `.github/workflows/ci-quality.yml` | Conditional only | Modify only if a RED integration test proves named routing is missing | Change remote settings or broaden CI without a failing contract | RED test and separate review |
| Runtime and external state | Not in scope | Read tracked documentation required for evidence | Mutate Compose, containers, secrets, deployment, remote GitHub, or global provider state | Whole-branch scope review |

## Task Table

| ID | Deliverable | Dependency | Status | Implementation role | Required review |
| --- | --- | --- | --- | --- | --- |
| T-TCS-001 | Registry and support contract canonicalization | Spec and Plan | Completed | fresh implementer | spec then quality |
| T-TCS-002 | Common, README, and Governance forms | T-TCS-001 | Completed | fresh implementer | spec then quality |
| T-TCS-003 | Stage 01-03 and Spec-child forms | T-TCS-001 | Completed | fresh implementer | spec then quality |
| T-TCS-004 | Stage 04 Plan and Task system | T-TCS-001 through 003 | Completed | fresh implementer | spec then quality |
| T-TCS-005 | Stage 05 Operations forms | T-TCS-001 | Completed | fresh implementer | spec then quality |
| T-TCS-006 | Executable template and target validation | T-TCS-001 through 005 | In Review | fresh implementer | spec then quality |
| T-TCS-007 | Direct consumers, generated evidence, and wave routing | T-TCS-001 through 006 | Queued | fresh implementer | spec then quality |

## T-TCS-001 Implementation Evidence

- Replaced the flat typed-template mapping with 23 exact roles that own unique
  sources, target profiles, target globs, and non-overlapping heading envelopes.
- Added deterministic role matching and fail-closed classification, including
  exact Spec-child paths, README profile delegation, Memory/Progress
  specificity, and generated inventory exclusion.
- Added exact-key, known-profile, safe-path/glob, unique-source, heading, and
  repository source-existence validation. Typed sources retain target-profile
  placeholder checks; README, governance, and Archive keep their distinct
  source/target metadata boundaries.
- Reconciled the ten named human support owners and verified the external
  rationale against official or primary sources on 2026-07-13 without claiming
  that local roles or metadata are international standards.
- Controller-approved dependency correction: Task 1 created the minimal Audit
  source needed by repository-contract existence checks. Its Target and
  target-relative comments are a temporary legacy-shell compatibility exception;
  Task 2 owns final form-only normalization and Task 6 owns removal of the old
  shell requirement.
- Adding the tracked Audit path caused ordinary generated freshness fallout.
  The LLM Wiki index, coverage snapshot, and metadata inventory were refreshed
  only through their canonical generators; Task 7 still owns the final
  branch-wide refresh and disposition.
- The first independent review of `9eca432b...a3ca523e` returned Spec FAIL and
  Quality CHANGES REQUESTED with Important finding I-01: loader validation
  rejected literal duplicate globs but admitted distinct equal-specificity
  patterns with a shared witness.
- I-01 remediation adds a finite product-state intersection check for the
  already-supported segment `*` and whole-segment `**` grammar. It compares
  only distinct roles with the same artifact profile and equal specificity,
  emits both patterns plus a deterministic witness, and does not scan target
  documents. More-specific precedence such as Progress over the generic Memory
  glob remains valid. The independent full-range re-review of
  `9eca432b...ede2b9a2` returned Spec PASS and Quality APPROVED, confirmed I-01
  resolved by `ede2b9a2`, and reported no remaining findings.

## T-TCS-002 Implementation Evidence

- Reduced README, Reference, Audit, Archive, Memory, and Progress to their
  registered Task 2 forms: exact frontmatter, one H1, exact required H2
  envelopes, explicit `{{token_name}}` body tokens, and no Rules blocks,
  Target comments, fixed-depth examples, snippet libraries, or copied
  governance prose.
- Kept the Task 2 source assertions full-strength for the six owned roles.
  Controller-approved sequencing defers the same all-role assertion to Tasks
  3 through 5, with Task 5 responsible for reaching all 23 Markdown roles.
- The Audit source already existed from the Task 1 source-existence correction,
  so its presence assertion passed in RED. RED still proved the README multi-H1,
  Rules/Target, heading-envelope, governance-frontmatter, and Memory-mirror
  defects before implementation.
- Deleted `docs/00.agent-governance/memory/template.md` without a redirect or
  mirror. Active Memory and Progress routes now point to the single Stage 99
  source, and Progress usage prose is owned by the Stage 00 Memory README and
  task checklists.
- Normalized the template, Common, and Governance catalog READMEs to the exact
  template-catalog heading profile while keeping them routing-only and Korean
  by default.
- Applied the controller-approved transitional shell correction only to
  registered Markdown role-source forms. Machine-template Target/Cross-links
  checks, direct target-document Target checks, target heading tables, and
  changed/normalized target semantics remain intact for Task 6. Legacy
  source-form rubric, Memory, and Reference assertions now validate the named
  support owners or Task 2 form envelopes instead of requiring copied rules in
  templates.
- Deleting the tracked mirror caused ordinary generated freshness fallout.
  The LLM Wiki index, coverage snapshot, and metadata inventory were refreshed
  only through their canonical owners; Task 7 still owns the final branch-wide
  refresh.
- Graphify refreshed successfully to 23,102 nodes, 24,208 edges, and 1,543
  communities. The tracked graph outputs were restored after evidence capture,
  and conclusions were corroborated against tracked source, Stage 00, Spec 130,
  and the active Plan/Task because the graph remains advisory.
- The first independent review of `ff4cb021...1bba54fe` returned Spec FAIL and
  Quality CHANGES REQUESTED with Critical 0, Important 2, and Minor 1. I-01
  found that the sole Memory form could not instantiate the seven labels
  required by the active Memory-note consumer; I-02 found that Stage 00 still
  contradicted the registered Governance source metadata; M-01 found that the
  Common confidentiality assertion could pass outside its intended owner and
  section.
- Review remediation restores the seven tokenized Memory fields without
  changing the registered H2 envelope; routes Governance Memory, Progress,
  README, and other typed source metadata through the registry in Stage 00;
  and gives Reference, Audit, generated output, and Repo-support one concise
  confidentiality boundary under Common `Source and Evidence Discipline`.
  The transitional shell assertion now scopes those literals to that section.
  The independent full-range re-review of `ff4cb021...e9a0c8cf` returned Spec
  PASS and Quality APPROVED with Critical 0, Important 0, and Minor 0. I-01,
  I-02, and M-01 are resolved by `e9a0c8cf`.
- No runtime, Compose, infrastructure, deployment, secret, provider, workflow,
  credential, branch-protection, or remote state changed. T-TCS-002 is
  completed; the controlled wrapper and whole-branch review remain later gates.

## T-TCS-003 Implementation Evidence

- Reduced PRD, ARD, ADR, the parent Spec, and the five focused Spec-child
  sources to exact registry-compatible frontmatter, one H1, registered required
  and conditional H2 sections, explicit `{{token_name}}` body tokens, and no
  copied Rules, Target comments, fixed-depth links, lifecycle guidance,
  selection guidance, executable-looking commands, or example prose.
- Preserved the registered conditional concerns. PRD, ARD, and the parent Spec
  retain optional AI headings, and each focused child retains its registered
  optional concern without making that concern a universal target requirement.
- The parent Spec keeps child-contract summary, ownership, and linkage tokens;
  separately reviewable API, Agent, Data, Service, and Test details remain in
  their focused child forms.
- Replaced valid-looking OpenAPI, GraphQL, and Protobuf values with visible
  uppercase `__TOKEN_NAME__` values. Machine Target and Cross-links comments
  remain because the transitional shell contract owns machine-source routing
  until T-TCS-006.
- Normalized the SDLC and Spec-contract catalogs to the exact template-catalog
  README profile. Both are routing-only and Korean by default, with selection
  and contract details delegated to Stage 99 support.
- Controller-approved sequencing correction: the exact one-H1, required,
  forbidden, no-Rules, and no-Target assertions cover only the nine T-TCS-003
  roles: `prd`, `ard`, `adr`, `spec`, `agent-design`, `api-spec`,
  `data-model`, `service`, and `tests`. T-TCS-002 already covers its six roles;
  T-TCS-004 and T-TCS-005 extend coverage, and T-TCS-005 must reach all 23.
  None of the nine owned-role assertions were weakened.
- The first independent review of `48f37eb4...e1a9dccc` returned Spec FAIL and
  Quality CHANGES REQUESTED with Critical 0, Important 4, and Minor 0. I-01
  identified missing explicit PRD information shapes; I-02 identified missing
  Service and Tests child handoffs in the parent Spec; I-03 identified
  native-invalid OpenAPI and GraphQL token positions plus a concrete auth
  selection; and I-04 identified regressions that did not enforce exact body
  and machine contracts.
- Review remediation restores exact PRD semantic tokens; gives API, Data,
  Agent, Service, and Tests children explicit summary/ownership/link handoffs;
  keeps OpenAPI fixed operation/status keys with unresolved values in
  extensions; keeps GraphQL token values in a comment map with non-reserved
  sentinel names; and strengthens the focused regressions with independent
  exact token sets, exact heading multisets, exact frontmatter, native-safe
  structural checks, and bounded negative mutations. I-01 through I-04 are
  implementation-remediated and await independent full-range re-review.
- The independent re-review of `48f37eb4...e026b561` confirmed I-01, I-02,
  and I-03 resolved but returned Spec FAIL / Quality CHANGES REQUESTED with
  Critical 0, Important 1, and Minor 0 for I-04-R1: heading and artifact-profile
  expectations were still derived from the mutable registry. The focused fix
  adds independent literal nine-role heading and profile oracles, compares the
  registry and source separately to those oracles, and rejects coordinated
  registry-plus-source heading or profile drift. I-04-R1 is implementation-
  remediated and awaits independent full-range re-review.
- The final full-range re-review of `48f37eb4...37d52025` returned Spec PASS
  and Quality APPROVED with Critical 0, Important 0, and Minor 0. I-01 through
  I-04 and I-04-R1 are resolved; T-TCS-003 is completed.
- Graphify refreshed to 23,207 nodes, 24,348 edges, and 1,542 communities.
  Its tracked outputs were restored after evidence capture, and conclusions
  were corroborated against tracked sources, Stage 00, Spec 130, and the active
  Plan/Task because the graph remains advisory.
- No target corpus, runtime, Compose, infrastructure, deployment, secret,
  provider, workflow, credential, branch-protection, or remote state changed.
  T-TCS-003 is completed after independent reapproval.

## T-TCS-004 Implementation Evidence

- Reduced Plan to a prospective form that owns context, sequence, intended
  verification, risks, rollback, approval gates, and completion criteria. It
  does not contain actual results, work logs, reviews, or commit evidence.
- Consolidated ordinary and harness execution into one evidentiary Task form.
  Its tokens cover allowed and forbidden paths, Compose/security/operations/
  runtime impact, conditional protected-surface approval, exact commands,
  expected and actual evidence, reviews, commits, controlled-wrapper evidence,
  and deferral routing.
- Deleted the competing Governance harness Task form and removed every active
  route to it. Remaining literal references are deletion assertions,
  instructions, or preserved completed historical evidence, not selectable
  routes.
- Updated Stage 00 authoring, checklist, stage-matrix, approval, and harness-map
  routes plus Stage 99 catalogs and selection guidance. Controlled wrapper and
  high-risk approval policy remain owned by Stage 00 and recorded in Task
  evidence rather than copied into catalogs.
- Narrowly removed the deleted source from the Python transitional exception
  and shell inventory. T-TCS-006 still owns target-body validation; this unit
  does not pre-empt that implementation.
- Added independent literal Plan/Task heading, profile, H1, token, frontmatter,
  prospective-only, negative-mutation, and coordinated registry-plus-source
  drift regressions.
- Refreshed the canonical LLM Wiki index, stage/category coverage, and metadata
  semantic inventory through their owner generators. Graphify also ran after
  code changes, but the interrupted implementer did not retain its numeric
  snapshot; tracked graph outputs were restored and no count is claimed.
- No runtime, Compose, infrastructure, deployment, secret, provider, workflow,
  credential, branch-protection, or remote state changed. The first independent
  review returned Spec FAIL / Quality CHANGES REQUESTED with C0/I1/M0 because
  the recorded changed-mode selected count was stale. I-01 was remediated by
  `b394a671`; the full-range re-review returned Spec PASS and Quality APPROVED
  with C0/I0/M0, so T-TCS-004 is completed.

## T-TCS-005 Implementation Evidence

- Reduced Guide, Policy, Runbook, Incident, Postmortem, and Release to exact
  form-only sources with profile-compatible frontmatter, one H1, registered
  required and conditional H2 sections, explicit `{{token_name}}` body tokens,
  and no copied Rules, Target comments, fixed-depth links, event samples, or
  executable-looking commands.
- Separated routine usage, controls, executable procedures, live response,
  retrospective learning, and real release evidence. Guide has no recovery or
  escalation owner, Policy has no Procedure, and Runbook has exactly one
  Rollback or Recovery section plus evidence and escalation handoff.
- Made Incident a permitted root while retaining Runbook as an allowed direct
  parent. Postmortem remains a strict Incident child, Release remains a strict
  Spec/Plan/Task child, and no Incident, Postmortem, or Release event leaf was
  created.
- Normalized the Operations catalog to the registered template-catalog README
  envelope and aligned the Stage 00 matrix plus the human SDLC relationship
  contract without copying machine arrays into prose.
- Redirected the transitional repository-contract routing assertion from the
  copyable Incident/Postmortem bodies to the canonical Template Selection
  owner. T-TCS-006 still owns removal of duplicate shell template semantics.
- Added independent exact six-role frontmatter, H1, heading, profile, token,
  negative-mutation, and coordinated-drift regressions. The combined literal
  oracle now covers all 23 registered Markdown roles independently of the
  mutable registry.
- Canonical metadata and Wiki generators were run. Their tracked outputs were
  already fresh at 901 metadata records / 2,025 advisory findings, 1,296 Wiki
  index paths, and 1,295 safe coverage paths, so no generated body changed.
- Graphify refreshed to 23,317 nodes, 24,528 edges, and 1,542 communities.
  Tracked graph outputs were restored, and the advisory result was
  corroborated against tracked source, Stage 00, Spec 130, and the active
  Plan/Task.
- No runtime, Compose, infrastructure, deployment, Release event, secret,
  provider, workflow, credential, branch-protection, or remote state changed.
- The first independent review of `34ae2dab...f86db7ac` returned Spec FAIL and
  Quality CHANGES REQUESTED with C0/I1/M0. I-01 found that four evidence-bearing
  Operations forms used placeholders too broad to preserve Spec 130's mandatory
  information shapes.
- I-01 and I-01-R1 are resolved by committed remediations `b09d73bd` and
  `b7b2ec95`: the approved H2 envelopes and frontmatter remain stable while the
  mandatory Operations evidence shapes, Runbook prerequisites, and automation
  invocation/judgment boundaries are explicit in the forms, human SDLC
  contract, and independent all-role plus per-field negative oracles. The final
  full-range re-review of `34ae2dab...b7b2ec95` returned Spec PASS / Quality
  CHANGES REQUESTED, C0/I1/M0, for evidence finding I-02. Commit `c07160a2`
  corrected the Task and Progress ledger; the narrow re-review returned Spec
  PASS / Quality APPROVED with C0/I0/M0. T-TCS-005 is completed.

## T-TCS-006 Implementation Evidence

- Added fenced-block-aware Markdown H1/H2 extraction and registry-owned body
  validation with deterministic missing-role, ambiguous-role, H1-count,
  required-heading, forbidden-heading, README-heading, instruction-residue,
  body-token, machine-token, and machine-example finding codes.
- Applied the exact role/body contract to every registered Markdown source,
  tracked machine source, changed or new typed target, and only the
  template-catalog README profile. Conditional headings remain optional.
- Changed targets reject unresolved body tokens and template-only instruction
  literals outside fenced and inline-code examples. Base-existing body deficits
  are compared at the same path and preserved until Task 7; new documents and
  newly introduced deficits fail closed.
- Removed the incomplete shell template inventory and duplicate
  `heading_requirements` and Operations forbidden-heading tables. The shell now
  orchestrates the Python `check-contracts` owner and, when
  `TEMPLATE_GATE_BASE` is present, the Python changed/new owner.
- CI remains fail closed without workflow modification: its repository-contract
  job derives `TEMPLATE_GATE_BASE` from the pull-request base or push-before
  SHA, validates that commit and merge base, runs the exact Python changed/new
  gate as a dedicated step, and then runs the shell orchestration.
- Removed transitional Target comments from Spec 130, its active Plan, and this
  Task atomically. No Task 7 direct consumer, runtime, Compose, infrastructure,
  deployment, secret, provider, workflow, credential, branch-protection, or
  remote state changed.
- TDD RED ran 39 focused methods with two failures and seven errors. Initial
  GREEN ran the same 39/39; after splitting every brief-required case into an
  independently named oracle, focused GREEN is 44/44. The final complete
  metadata suite passes 155/155 after converting unrelated relation-test
  fixtures to concrete registered bodies.
- Metadata repository contracts report zero violations; explicit changed mode
  from `39809f26` reports four selected, zero violations, zero legacy
  exceptions, and zero transition overrides. Generated Wiki and metadata
  evidence is fresh at 901 records and 2,025 advisory findings; traceability is
  46/0 and implementation alignment is 647 documents / 5,135 links / 0.
- The full repository contract gate ran with `TEMPLATE_GATE_BASE=39809f26` and
  completed with `failures=0`. Graphify refreshed to 23,387 nodes, 24,679
  edges, and 1,542 communities; tracked graph outputs were restored after
  capture, and the advisory result was corroborated against tracked sources,
  Stage 00, Spec 130, and this Plan/Task.
- The first independent review of `39809f26...9bf5b708` returned Spec FAIL /
  Quality CHANGES REQUESTED, C0/I3/M0. I-01 identified set-based suppression
  of added or identity-changed body residue, I-02 identified delimiter-invalid
  fenced and inline-code scanning, and I-03 identified missing bounded native
  credential assignment checks.
- Remediation now compares exact private semantic identities with multiset
  counts while rendering only safe class labels and counts, implements
  delimiter-specific CommonMark fence and equal-run inline-code scanning, and
  adds bounded OpenAPI, GraphQL, and Protobuf credential-value checks without
  treating declarations or numeric Protobuf tags as credentials. The
  remediation RED was 41 methods / 21 expected failures; focused GREEN is
  41/41 and the complete metadata suite is 167/167.
- Implementation status remains In Review. The three fixes await independent
  re-review; no approval, closure, or remediation commit hash is claimed.

## Review Evidence

| Task | Spec review | Quality review | Findings | Disposition |
| --- | --- | --- | --- | --- |
| T-TCS-001 | PASS on `9eca432b...ede2b9a2` | APPROVED on `9eca432b...ede2b9a2` | None; I-01 resolved by `ede2b9a2` | Completed |
| T-TCS-002 | PASS on `ff4cb021...e9a0c8cf` | APPROVED on `ff4cb021...e9a0c8cf` | None; I-01, I-02, and M-01 resolved by `e9a0c8cf` | Completed |
| T-TCS-003 | PASS on `48f37eb4...37d52025` | APPROVED on `48f37eb4...37d52025` | None; I-01 through I-04 and I-04-R1 resolved | Completed |
| T-TCS-004 | PASS on `4c821e86...b394a671` | APPROVED on `4c821e86...b394a671` | None; I-01 resolved by `b394a671` | Completed |
| T-TCS-005 | PASS on `34ae2dab...c07160a2` | APPROVED on `34ae2dab...c07160a2` | None; I-01, I-01-R1, and I-02 resolved | Completed |
| T-TCS-006 | FAIL on `39809f26...9bf5b708`; remediation awaits re-review | CHANGES REQUESTED on `39809f26...9bf5b708`; remediation awaits re-review | C0/I3/M0: I-01 semantic multiplicity/identity, I-02 CommonMark delimiters, I-03 bounded native credential assignments; fixes implemented locally | In Review |
| T-TCS-007 | Not run — dependency is in review | Not run — dependency is in review | None recorded | Await T-TCS-006 |
| Whole branch | Not run — implementation has not completed | Not run — implementation has not completed | None recorded | Await T-TCS-007 |

## Verification Summary

### Planning baseline

| Command | Result | Meaning |
| --- | --- | --- |
| Metadata changed-mode for Spec and Plan | Pass, zero violations | Typed identity, parent, and lifecycle transition are valid |
| Repository contract check | Pass | Current repository contracts remain green before implementation |
| Document traceability check | Pass | Current Stage 04/05 catalogs remain synchronized |
| Documentation implementation alignment | Pass | Current docs and tracked implementation agree within the existing gate |
| LLM Wiki index and coverage check | Pass after generator refresh | Generated knowledge evidence includes the active Plan |
| `git diff --check` | Pass | No whitespace error in the planning commit |

### Required implementation checks

- Focused RED and GREEN tests named by each Plan task.
- Full `tests.validation.test_document_metadata` suite.
- Metadata `check-contracts`, `check-changed`, and applicable active reporting.
- Repository contracts, document traceability, and implementation alignment.
- YAML and machine-template fixture validation.
- Reference searches after every deletion.
- LLM Wiki and metadata inventory generator and check modes.
- Graphify refresh and advisory report corroboration after code changes.
- Final whole-branch specification and quality review.
- Controlled all-files pre-commit wrapper from a clean commit.

### T-TCS-001 RED and GREEN

| Phase | Command | Result |
| --- | --- | --- |
| RED | `python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.TemplateRoleInferenceTests -v` | Expected failure: 10 tests ran with 26 errors because `template_roles` and `classify_template_role()` did not exist. |
| GREEN | Same focused command | Pass: 10/10. |
| Regression | `python3 -m unittest tests.validation.test_document_metadata -v` | Pass: 109/109. |
| Metadata contracts | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | Pass: zero violations. |
| Repository contracts | `bash scripts/validation/check-repo-contracts.sh` | Pass: `failures=0`. |
| Generated freshness | Canonical LLM Wiki index/coverage generators and metadata inventory report mode | Pass: 1,298 index paths, 1,297 safe coverage paths, and 903 metadata records / 2,033 advisory findings. |
| Graph refresh | `graphify update .` | Pass: refreshed to 23,053 nodes / 24,116 edges / 1,540 communities; outputs restored after evidence capture to keep this logical commit scoped, and conclusions were corroborated against tracked source, Stage 00, Spec 130, and this Plan/Task. |
| Diff hygiene | `git diff --check` and Python compilation | Pass. |

### T-TCS-001 I-01 Remediation

| Phase | Command or evidence | Result |
| --- | --- | --- |
| Reviewer reproduction | Mutate Spec to `docs/03.specs/*/s*ec.md` and API Spec to `docs/03.specs/*/sp*c.md` | Confirmed loader accepted two distinct equal-specificity matchers for the same witness before remediation. |
| RED | `python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests.test_template_roles_reject_ambiguous_target_matchers -v` | Expected failure: `ProfileError not raised`. |
| GREEN | Same single regression | Pass: 1/1, with deterministic diagnostic witness `docs/03.specs/x/spec.md`. |
| Focused Task 1 | Profile schema plus template-role inference suites | Pass: 10/10. |
| Metadata regression | Full `tests.validation.test_document_metadata` suite | Pass: 109/109. |
| Scope | Implementation inspection | Finite safe-glob state-space only; no repository-body scan and no Task 6 body-validation expansion. |

### T-TCS-001 Independent Re-review

| Evidence | Result |
| --- | --- |
| Full reviewed range | `9eca432b...ede2b9a2`, including implementation `a3ca523e` and I-01 fix `ede2b9a2` |
| Verdict | Spec PASS; Quality APPROVED; Critical 0, Important 0, Minor 0 |
| I-01 | Resolved; distinct same-profile equal-specificity overlaps reject at load time, same-role redundancy remains valid, and unequal-specificity precedence remains valid |
| Reviewer verification | Focused schema/inference 11 executions; metadata contracts 0 violations; range diff hygiene pass; bounded exhaustive/adversarial witness checks pass |
| Remaining gates | Controlled all-files wrapper and final whole-branch review remain Task 7 responsibilities |

### T-TCS-002 RED and GREEN

| Phase | Command or evidence | Result |
| --- | --- | --- |
| RED | `python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests -v` | Expected failure: 10 tests ran with 12 failures covering the existing mirror, README two-H1 defect, Rules/Target residue across the six owned roles, README/Reference/Progress envelope drift, and missing governance `layer`; Audit presence passed because Task 1 had already created the source. |
| Focused GREEN | `python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests tests.validation.test_document_metadata.ReadmeProfileTests -v` | Pass: 13/13. |
| Metadata regression | `python3 -m unittest tests.validation.test_document_metadata -v` | Pass: 114/114. |
| Metadata contracts | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | Pass: zero violations. |
| Changed mode | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref ff4cb02170ec28a64f6f6574af998bac1bb17822` | Pass: 17 selected, zero violations, zero legacy exceptions, zero transition overrides. |
| Repository contracts | `bash scripts/validation/check-repo-contracts.sh` | Pass: `failures=0`; registered Markdown source transition is GREEN while machine and direct-target checks remain. |
| Generated freshness | Canonical LLM Wiki index/coverage generators and metadata inventory report/check modes | Pass: 1,297 index paths, 1,296 safe coverage paths, and 902 metadata records / 2,031 advisory findings. |
| Reference search | Deleted-mirror search across docs and provider surfaces | Pass: no active route or generated link targets the mirror; remaining literal hits are deletion assertions/instructions and preserved historical evidence. |
| Traceability and alignment | Stage 04/05 traceability and implementation alignment checks | Pass: 46 catalog pairs; 647 stage docs / 5,136 links; zero failures. |
| Graph refresh | `graphify update .` | Pass: 23,102 nodes / 24,208 edges / 1,543 communities; tracked graph outputs restored after evidence capture. |
| Diff and compile | `git diff --check`, Bash syntax, and Python compilation | Pass. |

### T-TCS-002 Review Remediation

| Phase | Command or evidence | Result |
| --- | --- | --- |
| First independent review | `.superpowers/sdd/task-2-review.md` over `ff4cb021...1bba54fe` | Spec FAIL; Quality CHANGES REQUESTED; Critical 0 / Important 2 / Minor 1; findings I-01, I-02, and M-01. |
| RED | Three new `TemplateMetadataTests` regressions for Memory instantiation, Stage 00 source metadata, and Common evidence confidentiality | Expected failure: 3 tests ran with 17 subtest failures: seven missing Memory labels, one Stage 00 policy mismatch, and nine missing Common section literals. |
| Focused GREEN | Same three regressions | Pass: 3/3. |
| Task 2 GREEN | `TemplateMetadataTests` plus `ReadmeProfileTests` | Pass: 16/16. |
| Finding disposition | Independent full-range re-review over `ff4cb021...e9a0c8cf` | Spec PASS; Quality APPROVED; Critical 0 / Important 0 / Minor 0; I-01, I-02, and M-01 resolved. |

### T-TCS-003 RED and GREEN

| Phase | Command or evidence | Result |
| --- | --- | --- |
| RED | `python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests -v` | Expected failure: 2 test methods ran with 12 subtest failures covering all nine owned Markdown roles and all three machine sources. |
| Focused GREEN | `python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests tests.validation.test_document_metadata.TemplateMetadataTests -v` | Pass: 15/15. |
| Metadata regression | `python3 -m unittest tests.validation.test_document_metadata -v` | Pass: 119/119. |
| Native and static syntax | PyYAML safe-load plus bounded GraphQL and Protobuf grammar/static checks | Pass. No local `protoc`, `buf`, GraphQL parser, or formatter was available; parser validation was not claimed. |
| Metadata contracts | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | Pass: zero violations. |
| Changed mode | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 48f37eb4` | Pass: 13 selected, zero violations, zero legacy exceptions, zero transition overrides. |
| Repository contracts | `bash scripts/validation/check-repo-contracts.sh` | Pass: `failures=0`; machine Target/Cross-links compatibility remains intact. |
| Generated freshness | Canonical LLM Wiki index/coverage and metadata inventory check modes | Pass: all outputs fresh; metadata inventory remains 902 records / 2,031 advisory findings. |
| Traceability and alignment | Stage 04/05 traceability and implementation alignment checks | Pass: 46 catalog pairs; 647 stage docs / 5,136 links; zero failures. |
| Graph refresh | `graphify update .` | Pass: 23,207 nodes / 24,348 edges / 1,542 communities; tracked outputs restored after evidence capture. |
| Diff, compile, and self-review | `git diff --check`, Python compilation, exact heading/token scan, and scoped diff review | Pass; no self-review finding remained. |

### T-TCS-003 Review Remediation

| Phase | Command or evidence | Result |
| --- | --- | --- |
| First independent review | `.superpowers/sdd/task-3-review.md` over `48f37eb4...e1a9dccc` | Spec FAIL; Quality CHANGES REQUESTED; Critical 0 / Important 4 / Minor 0; findings I-01 through I-04. |
| RED | Strengthened `TemplateBodyContractTests` for exact role tokens, five Spec-child handoffs, native-safe machine structures, and negative mutations | Expected failure: 4 test methods ran with 5 failures covering PRD semantics, Spec child handoffs, and OpenAPI/GraphQL contract safety. |
| Focused GREEN | `python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests -v` | Pass: 4/4. |
| Task 3 GREEN | `TemplateBodyContractTests` plus `TemplateMetadataTests` | Pass: 17/17. |
| Metadata regression | `python3 -m unittest tests.validation.test_document_metadata` | Pass: 121/121. |
| Native/static contract | Exact machine-source test plus PyYAML safe-load and bounded GraphQL/Protobuf checks | Pass; no native parser availability or parser approval is claimed. |
| Graph refresh | `graphify update .` | Pass: 23,238 nodes / 24,389 edges / 1,544 communities; tracked outputs restored after evidence capture and advisory results corroborated against tracked source and governance/stage documents. |
| Finding disposition | Implementation inspection and regression evidence | I-01 through I-04 implementation-remediated; independent full-range re-review pending. |
| First remediation re-review | `.superpowers/sdd/task-3-review.md` over `48f37eb4...e026b561` | Spec FAIL; Quality CHANGES REQUESTED; Critical 0 / Important 1 / Minor 0; I-01 through I-03 resolved; I-04-R1 remained. |
| I-04-R1 RED | Coordinated registry-plus-source heading and profile drift regressions | Expected failure: 2/2 cases reported `AssertionError not raised`. |
| I-04-R1 GREEN | Independent literal nine-role heading/profile oracles plus coordinated-drift regressions | Pass: coordinated cases 2/2; `TemplateBodyContractTests` 6/6; combined body/metadata 19/19; full metadata 123/123. |
| Final independent re-review | `.superpowers/sdd/task-3-review.md` over `48f37eb4...37d52025` | Spec PASS; Quality APPROVED; Critical 0 / Important 0 / Minor 0; ready to close. |

### T-TCS-004 RED and GREEN

| Phase | Command or evidence | Result |
| --- | --- | --- |
| RED | Combined `TemplateMetadataTests` and `TemplateBodyContractTests` before implementation | Expected failure: 27 methods ran with 11 failures covering two active-route/source-uniqueness defects, six missing Task evidence headings, one remaining harness source, and two exact Plan/Task source contracts. |
| Focused GREEN | `python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests tests.validation.test_document_metadata.TemplateBodyContractTests -q` | Pass: 27/27. |
| Metadata regression | `python3 -m unittest tests.validation.test_document_metadata -q` | Pass: 131/131. |
| Metadata contracts | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | Pass: zero violations. |
| Changed mode | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 4c821e86` | Pass: 18 selected, zero violations, one base-existing legacy exception, zero transition overrides. The exception is the completed 2026-06-05 Task whose historical body is preserved and whose deleted link is minimally repaired. |
| Repository contracts | `bash scripts/validation/check-repo-contracts.sh` | Pass: `failures=0`. |
| Generated freshness | Canonical LLM Wiki index/coverage and metadata inventory check modes | Pass: 1,296 index paths, 1,295 safe coverage paths, and 901 metadata records / 2,025 advisory findings. |
| Traceability and alignment | Stage 04/05 traceability and documentation implementation alignment | Pass: 46 catalog pairs; 647 stage docs / 5,135 links; zero failures. |
| Graph refresh | `graphify update .` | Ran after code changes; tracked outputs restored. Numeric snapshot not retained after the implementation agent interruption, so no count is claimed; conclusions were corroborated against tracked sources, Stage 00, Spec 130, and the active Plan/Task. |
| Diff, compile, and syntax | `git diff --check`, Python compilation, and Bash syntax | Pass. |

### T-TCS-005 Review Remediation

| Evidence | Result |
| --- | --- |
| First independent review | Spec FAIL; Quality CHANGES REQUESTED; Critical 0 / Important 1 / Minor 0 on `34ae2dab...f86db7ac` |
| I-01 RED | Strengthened exact role tokens, the independent all-23 oracle, and mandatory-field removal mutations: 59 test methods ran with 40 expected subtest failures across the four evidence-bearing roles. |
| I-01 remediation | Replaced broad placeholders under the existing H2 envelopes with explicit Runbook safety, ordered-step, expected-result, and verification-record fields; Incident severity, lead, current-state, action, mitigation, resolution, and handoff fields; Postmortem reviewed action ownership, priority, tracking, and verification ownership; and Release immutable identity, artifact, validation, approval, compatibility, rollout/rollback, outcome, and known-issue fields. Added concise durable semantics to the human SDLC contract. |
| Focused and full GREEN | Focused three-class suite 59/59; full metadata regression 140/140; metadata contracts zero violations. |
| Repository gates | Changed mode from `34ae2dab`: 11 selected, zero violations/exceptions/overrides; repository contracts `failures=0`; traceability 46/0; alignment 647 docs / 5,135 links / 0; generated outputs fresh at 1,296 / 1,295 paths and 901 records / 2,025 findings. |
| Scope and static evidence | Release event leaves 0; prohibited Operations-form residue 0; Python compilation and diff hygiene pass; no runtime or other excluded-surface mutation. |
| Graph refresh | `graphify update .` completed at 23,337 nodes / 24,549 edges / 1,542 communities; tracked graph outputs were restored and the advisory result was corroborated against canonical tracked owners. |
| First remediation re-review | Spec FAIL; Quality CHANGES REQUESTED; Critical 0 / Important 1 / Minor 0 on `34ae2dab...b09d73bd`; original I-01 is partial and I-01-R1 identifies implicit Runbook prerequisites plus automation invocation/judgment boundaries. |
| I-01-R1 RED | Added the three missing boundaries to the independent Runbook and all-23 exact token oracles plus mandatory per-field removals: 3 narrow test methods ran with 5 expected failures. |
| I-01-R1 remediation | Added `{{prerequisites}}` under the existing Trigger and Preconditions heading; replaced the broad automation handoff token with explicit candidate/invocation and human-or-operator judgment-boundary fields under the existing conditional heading; retained the existing rollback-or-recovery boundary. Added matching durable human semantics without adding headings, commands, examples, state keys, or runtime claims. |
| I-01-R1 GREEN | Narrow 3/3; focused three-class suite 59/59; full metadata regression 140/140; metadata contracts zero; changed mode from `34ae2dab` 11/0 with zero exceptions/overrides; repository contracts zero; traceability 46/0; alignment 647 docs / 5,135 links / 0; generated evidence fresh; Graphify 23,348 nodes / 24,560 edges / 1,544 communities with tracked outputs restored. |
| Final full-range re-review | Spec PASS; Quality CHANGES REQUESTED; Critical 0 / Important 1 / Minor 0 on `34ae2dab...b7b2ec95`. I-01 and I-01-R1 are resolved by committed `b09d73bd` and `b7b2ec95`; I-02 identifies stale canonical Task review and commit-ledger evidence only. |
| I-02 evidence correction | `c07160a2` records the actual `b7b2ec95` identity and subject in the canonical Task and Progress ledger; no template, support, validator, test, generated, or runtime file changed. |
| Final narrow re-review | Spec PASS; Quality APPROVED; Critical 0 / Important 0 / Minor 0 on `34ae2dab...c07160a2`; I-01, I-01-R1, and I-02 resolved and ready for Task closure. |

### T-TCS-004 Review Remediation

| Evidence | Result |
| --- | --- |
| First independent review | Spec FAIL; Quality CHANGES REQUESTED; Critical 0 / Important 1 / Minor 0 on `4c821e86...b54e76df` |
| I-01 | Replaced the stale 16-document changed-mode claim with the reproducible final result: 18 selected, zero violations, one base-existing legacy exception, and zero transition overrides. |
| Commit ledger | The implementation unit is identified as `b54e76df`; the review-remediation commit is intentionally not claimed before commit. |
| Remediation commit | `b394a671`; evidence-only Task and Progress correction with no template, validator, test, generated, or runtime change. |
| Final independent re-review | Spec PASS; Quality APPROVED; Critical 0 / Important 0 / Minor 0 on `4c821e86...b394a671`; I-01 resolved and ready for Task closure. |

### T-TCS-005 RED and GREEN

| Phase | Command or evidence | Result |
| --- | --- | --- |
| RED | `python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests tests.validation.test_document_metadata.MetadataValidationTests tests.validation.test_document_metadata.TemplateMetadataTests -v` | Expected failure: 58 methods ran with 13 failures covering six exact Operations source contracts, the same six roles in the independent all-23 oracle, and Incident root rejection. |
| Focused GREEN | Same three test classes after implementation | Pass: 58/58. |
| Metadata regression | `python3 -m unittest tests.validation.test_document_metadata -q` | Pass: 139/139. |
| Metadata contracts | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | Pass: zero violations. |
| Changed mode | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 34ae2dab` | Pass: 11 selected, zero violations, zero legacy exceptions, and zero transition overrides. |
| Repository contracts | `bash scripts/validation/check-repo-contracts.sh` | Initial expected integration failure exposed four fixed-routing literals in copyable Incident/Postmortem sources; after routing the assertion to Template Selection, pass with `failures=0`. |
| Generated freshness | Canonical LLM Wiki index/coverage generators and metadata inventory owner | Pass: 1,296 index paths, 1,295 safe coverage paths, and 901 metadata records / 2,025 advisory findings; no generated body diff. |
| Traceability and alignment | Stage 04/05 traceability and documentation implementation alignment | Pass: 46 catalog pairs; 647 stage docs / 5,135 links; zero failures. |
| Operations searches | Release-leaf search plus bounded Rules/Target/fixed-link/command scans | Pass: no Release event leaf and no prohibited form residue. |
| Graph refresh | `graphify update .` | Pass: 23,317 nodes / 24,528 edges / 1,542 communities; tracked outputs restored and advisory conclusions corroborated. |
| Diff, compile, and syntax | `git diff --check`, Python compilation, and Bash syntax | Pass. |
| I-01-R1 narrow RED | Three exact-token methods after adding Runbook prerequisites, automation candidate/invocation, and human-or-operator judgment-boundary expectations | Expected failure: 3 methods ran with 5 failures across the Runbook source, all-23 oracle, and three individual mandatory-field removals. |
| I-01-R1 narrow GREEN | Same three methods after updating the Runbook form and durable human contract | Pass: 3/3. |
| I-01-R1 focused/full GREEN | Focused three-class suite and complete metadata regression | Pass: 59/59 and 140/140. |

### T-TCS-006 RED and GREEN

| Phase | Command or evidence | Result |
| --- | --- | --- |
| RED | `python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests tests.validation.test_document_metadata.RepositoryContractIntegrationTests -v` | Expected failure: 39 methods ran with two failures and seven errors because the executable heading/body API and shell-owned-schema removal did not exist. |
| Focused GREEN | Same focused command after implementation, followed by independently named exact-case normalization | Initial pass 39/39; final pass 44/44 in 20.112 seconds. |
| Relation-fixture adjustment | Three changed-path identity regressions whose subject is relation handling | Pass: 3/3 after preserving concrete registered PRD/Spec bodies during rewrites; no product-gate weakening. |
| Metadata regression | `python3 -m unittest tests.validation.test_document_metadata -q` | Pass: 155/155 in 67.251 seconds. |
| Metadata contracts | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | Pass: zero violations. |
| Changed mode | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 39809f26` | Pass: four selected, zero violations, zero legacy exceptions, and zero transition overrides. |
| Repository contracts | `TEMPLATE_GATE_BASE=39809f26 bash scripts/validation/check-repo-contracts.sh` | Pass: the delegated changed gate reported four selected and zero violations/exceptions/overrides; final `failures=0`. |
| Generated freshness | Canonical LLM Wiki index/coverage and metadata inventory check modes | Pass: Wiki outputs fresh; metadata inventory remains 901 records / 2,025 advisory findings. |
| Traceability and alignment | Stage 04/05 traceability and documentation implementation alignment | Pass: 46 catalog pairs / 0 failures; 647 docs / 5,135 links / 0 failures. |
| Workflow decision | Existing `.github/workflows/ci-quality.yml` integration inspected | No RED routing gap: the validated event base, dedicated Python changed/new step, and shell step already fail closed in CI; workflow unchanged. |
| Graph refresh | `graphify update .` | Pass: 23,387 nodes / 24,679 edges / 1,542 communities; tracked outputs restored and advisory result corroborated against tracked canonical owners. |
| First independent review | Complete range `39809f26...9bf5b708` | Spec FAIL / Quality CHANGES REQUESTED, C0/I3/M0; I-01 through I-03 require remediation. |
| Remediation RED | `TemplateBodyContractTests` plus real-Git `ChangedBodyDeficitGitTests` | Expected failure: 41 methods, 21 failures, and zero errors reproducing exact body-deficit, CommonMark delimiter, and bounded native credential gaps. |
| Remediation focused GREEN | Same 41-method suite | Pass: 41/41 in 6.362 seconds. |
| Remediation metadata regression | Complete `tests.validation.test_document_metadata` suite | Pass: 167/167 in 64.803 seconds; zero failures and zero errors. |
| Remediation repository gates | Metadata contracts, explicit-base changed mode, and `TEMPLATE_GATE_BASE=39809f26` repository contracts | Pass: zero metadata violations; selected 4 / violations 0 / exceptions 0 / overrides 0; repository `failures=0`. |
| Remediation supporting gates | Generated freshness, traceability, alignment, Graphify, Python/Bash syntax, and diff hygiene | Pass: 901 records / 2,025 findings; traceability 46/0; alignment 647 docs / 5,135 links / 0; Graphify 23,430 nodes / 24,817 edges / 1,541 communities with tracked outputs restored; syntax and diff checks pass. |
| Review state | Task table and review ledger | In Review; remediation awaits independent specification and quality re-review. |

## Controlled Agent Pre-commit Evidence

The final wrapper has not run because implementation and whole-branch review
have not completed.

| Field | Current value |
| --- | --- |
| Planned entrypoint | `scripts/validation/run-agent-precommit-all-files.sh` |
| Direct pre-commit invocation | Prohibited |
| Planned prefixes | `docs/`, `scripts/validation/`, `tests/validation/` |
| Preconditions | Clean committed worktree; all task reviews and full validation pass |
| Hook result | Not run |
| Snapshot result | Not run |
| Unexpected paths | Not observed because the wrapper has not run |

## Commit Ledger

| Commit | Logical unit | Validation |
| --- | --- | --- |
| `ff26fd6b` | Approved Spec 130 and generated design evidence | Metadata, repository contracts, traceability, generated freshness, diff |
| `10fe2f9d` | Active Stage 04 Plan and generated planning evidence | Metadata changed-mode, repository contracts, traceability, alignment, generated freshness, diff |
| `a3ca523e` | Task 1 canonical template roles, support contracts, matcher, tests, and generated evidence | Focused 10/10; metadata 109/109; metadata and repository contracts; generated freshness; diff |
| `ede2b9a2` | Task 1 I-01 semantic glob-overlap remediation | I-01 1/1; focused 10/10; metadata 109/109; metadata contracts; independent PASS/APPROVED re-review |
| Closure unit — subject `docs(task): close template registry task`; self hash intentionally omitted | Record the completed independent verdict and close T-TCS-001 | Metadata changed-mode from `ede2b9a2`: 2 selected, 0 violations, 0 exceptions/overrides; diff hygiene pass; evidence-only scope |
| `1bba54fe` | Task 2 forms, catalog routing, mirror removal, transitional source gate, tests, and generated fallout | Focused 13/13; metadata 114/114; changed mode 17/0; repository contracts; generated freshness; traceability/alignment; Graphify; diff/compile |
| `e9a0c8cf` | Task 2 I-01/I-02/M-01 Memory, Stage 00 metadata, and Common confidentiality remediation | Remediation 3/3; focused 16/16; metadata 117/117; metadata and repository contracts; independent PASS/APPROVED re-review |
| Closure unit — subject `docs(task): close common governance forms task`; self hash intentionally omitted | Record the completed independent verdict and close T-TCS-002 | Metadata changed-mode and diff hygiene; evidence-only scope |
| `e1a9dccc` | Task 3 Stage 01-03, focused Spec-child, machine contract, catalog, test, and evidence forms | RED 12 intended subtest failures; focused 15/15; metadata 119/119; metadata/repository contracts; syntax/static checks; generated freshness; traceability/alignment; Graphify; diff/compile |
| `e026b561` | Task 3 I-01 through I-04 PRD semantics, parent-child handoffs, native-safe machine forms, and exact regressions | Remediation RED 4 methods / 5 failures; focused 4/4 and 17/17; metadata 121/121; metadata/repository contracts; native/static checks; generated freshness; traceability/alignment; Graphify; first re-review found I-04-R1 |
| `37d52025` | Task 3 I-04-R1 independent literal heading/profile oracles and coordinated-drift regressions | RED 2/2; GREEN coordinated 2/2, focused 6/6 and 19/19, metadata 123/123; independent PASS/APPROVED re-review |
| Closure unit — subject `docs(task): close design contract forms task`; self hash intentionally omitted | Record the completed independent verdict and close T-TCS-003 | Metadata changed-mode and diff hygiene; evidence-only scope |
| `b54e76df` | Task 4 prospective Plan, evidentiary Task, duplicate harness-form deletion, direct governance/validator fallout, tests, and generated evidence | RED 11 expected failures; focused 27/27; metadata 131/131; metadata/repository contracts zero; changed mode 18/0 with one base-existing legacy exception and zero transition overrides; generated freshness; traceability/alignment; Graphify ran; diff/compile/syntax pass |
| `b394a671` | Task 4 I-01 selected-count evidence correction | Exact changed-mode 18/0 with one base-existing legacy exception and zero overrides; focused 27/27; metadata contracts zero; generated freshness and diff pass; independent PASS/APPROVED re-review |
| Closure unit — subject `docs(task): close stage 04 forms task`; self hash intentionally omitted | Record the completed independent verdict and close T-TCS-004 | Metadata changed-mode and diff hygiene; evidence-only scope |
| `f86db7ac` | Task 5 Operations forms, Incident root relation, catalog/support/direct validator fallout, exact all-role regressions, and evidence | RED 13 expected failures; focused 58/58; metadata 139/139; metadata/repository contracts zero; changed mode 11/0 with zero exceptions/overrides; generated freshness; traceability/alignment; Graphify; diff/compile/syntax pass; first review C0/I1/M0 |
| `b09d73bd` | Task 5 I-01 explicit Operations evidence fields, durable human semantics, and strengthened independent oracles | RED 59 methods / 40 expected subtest failures; focused 59/59; metadata 140/140; metadata/repository contracts zero; changed mode 11/0; generated freshness; traceability/alignment; Graphify; first remediation re-review found I-01-R1 |
| `b7b2ec95` — `fix(operations): make runbook automation boundaries explicit` | Task 5 I-01-R1 Runbook prerequisites, automation candidate/invocation, human-or-operator judgment boundary, durable human semantics, and exact removal oracles | Narrow RED 3 methods / 5 failures; GREEN 3/3; focused 59/59; metadata 140/140; metadata/repository contracts zero; changed mode 11/0; generated freshness; traceability/alignment; Graphify 23,348 / 24,560 / 1,544 with outputs restored; final full-range re-review resolved I-01/I-01-R1 and found evidence-only I-02 |
| `c07160a2` | Task 5 I-02 canonical remediation-ledger correction | Evidence-only Task/Progress delta; changed from `b7b2ec95` 2/0; full Task 5 base 11/0; focused 59/59; metadata contracts and generated freshness pass; independent PASS/APPROVED narrow re-review |
| Closure unit — subject `docs(task): close operations forms task`; self hash intentionally omitted | Record completed independent verdict and close T-TCS-005 | Metadata changed-mode and diff hygiene; evidence-only scope |
| Planned unit — subject `test(validation): enforce template role contracts`; self hash intentionally omitted | Task 6 executable Markdown/machine contracts, changed-target gate, shell delegation, tests, and evidence | RED 39 methods / 9 expected failing methods; final focused GREEN 44/44; metadata 155/155; reviews not yet run |
| Planned remediation unit — subject `fix(validation): preserve exact body deficits`; self hash intentionally omitted | Task 6 I-01/I-02/I-03 exact private multiset comparison, CommonMark-bounded scanning, native credential checks, tests, and evidence | First review FAIL/CHANGES REQUESTED C0/I3/M0; remediation RED 41/21; focused 41/41; metadata 167/167; contracts and supporting gates pass; re-review pending |

Later review-fix and implementation commits will be appended as Tasks 6-7 close.

## Migration Wave Routing

| Wave | Scope | Entry gate | Exit evidence | This branch |
| --- | ---: | --- | --- | --- |
| A | 89 active PRD, ARD, ADR, Spec, and Plan documents | New approved Spec and Plan; parent graph established | Chain-level metadata, body, link, review, and validation evidence | Route only |
| B | 66 Guides, 64 Policies, and 61 Runbooks | New approved Spec and Plan; real review evidence available | Domain-level review, operations links, metadata, and validation evidence | Route only |
| C | 229 completed and one superseded document | New approved preservation Plan | Minimum metadata and link repair with unchanged historical body evidence | Route only |
| D | Five Archive tombstones | Proven origin, reason, date, and replacement | Complete provenance and link validation | Route only |
| E | Six generated documents | Canonical generator identified | Generator output and check mode agree | Route only |

## Deferred and Blocked Items

- Waves A through E are intentionally deferred to independent approved Specs
  and Plans.
- Corpus-wide blocking is deferred until all approved migration waves finish.
- Runtime Compose, infrastructure, security, and deployment remediation stays
  in Specs 124 through 127.
- Remote GitHub enforcement remains outside this branch.
- No implementation blocker is present at Task initialization.

## Related Documents

- [Spec 130](../../03.specs/130-template-contract-system-canonicalization/spec.md)
- [Implementation Plan](../plans/2026-07-13-template-contract-system-canonicalization.md)
- [Stage 99 template system](../../99.templates/README.md)
- [Template support](../../99.templates/support/README.md)
- [Metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Progress log](../../00.agent-governance/memory/progress.md)
