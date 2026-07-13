---
status: active
artifact_id: task:2026-07-13-template-contract-system-canonicalization
artifact_type: task
parent_ids:
  - plan:2026-07-13-template-contract-system-canonicalization
---

<!-- Target: docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md -->

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
| T-TCS-003 | Stage 01-03 and Spec-child forms | T-TCS-001 | In Review | fresh implementer | spec then quality |
| T-TCS-004 | Stage 04 Plan and Task system | T-TCS-001 through 003 | Queued | fresh implementer | spec then quality |
| T-TCS-005 | Stage 05 Operations forms | T-TCS-001 | Queued | fresh implementer | spec then quality |
| T-TCS-006 | Executable template and target validation | T-TCS-001 through 005 | Queued | fresh implementer | spec then quality |
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
  T-TCS-003 remains `In Review`; no independent reapproval is claimed.

## Review Evidence

| Task | Spec review | Quality review | Findings | Disposition |
| --- | --- | --- | --- | --- |
| T-TCS-001 | PASS on `9eca432b...ede2b9a2` | APPROVED on `9eca432b...ede2b9a2` | None; I-01 resolved by `ede2b9a2` | Completed |
| T-TCS-002 | PASS on `ff4cb021...e9a0c8cf` | APPROVED on `ff4cb021...e9a0c8cf` | None; I-01, I-02, and M-01 resolved by `e9a0c8cf` | Completed |
| T-TCS-003 | PASS on `48f37eb4...37d52025` | APPROVED on `48f37eb4...37d52025` | None; I-01 through I-04 and I-04-R1 resolved | Completed |
| T-TCS-004 | Not run — dependencies are queued | Not run — dependencies are queued | None recorded | Await T-TCS-001 through 003 |
| T-TCS-005 | Not run — dependency is queued | Not run — dependency is queued | None recorded | Await T-TCS-001 |
| T-TCS-006 | Not run — dependencies are queued | Not run — dependencies are queued | None recorded | Await T-TCS-001 through 005 |
| T-TCS-007 | Not run — dependencies are queued | Not run — dependencies are queued | None recorded | Await T-TCS-001 through 006 |
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

Later review-fix and implementation commits will be appended as Tasks 3-7 close.

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
