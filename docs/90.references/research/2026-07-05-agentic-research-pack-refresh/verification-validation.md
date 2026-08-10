---
status: active
artifact_id: reference:agentic-research:verification-validation
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-10
---

# Reference: Verification and Validation

## Overview

The words "verification" and "validation" appear in every leaf of this pack and
in most of the repository's tracked policy, but the distinction between them is
stated nowhere. That absence is not cosmetic. Under the standards vocabulary the
two words name different questions, and this repository answers one of them
thoroughly while answering the other only through human judgement.

Verification asks whether a product conforms to the requirements placed on it.
Validation asks whether the product satisfies its intended use. A conformance
checker cannot answer the second question, and the repository's entire tracked
gate population consists of conformance checkers.

This reference establishes the standards distinction from retrievable primary
sources, maps it onto the repository's actual checking surface, and names the
resulting gap. It changes no rule, contract, or validator.

## Purpose

Give the pack and the repository a shared, source-anchored vocabulary for
verification and validation, so that gate coverage claims can be stated in terms
of which question a gate actually answers.

## Repository Role

`.github/workflow-contract.yml` remains the typed gate registry,
`scripts/validation/` remains the checker implementation, and
`docs/00.agent-governance/rules/approval-boundaries.md` remains the approval
policy. This Stage 90 document is a comparison and vocabulary aid only. It
proposes no renaming and requires no change to any existing surface.

## Scope

### In Scope

- The standards distinction between verification and validation
- Where testing sits relative to both
- Static versus dynamic verification techniques
- V&V under non-determinism, which is the agent-first case
- Classification of this repository's tracked gates, tests, and approval gates
- Terminology drift between tracked labels and standards vocabulary

### Out of Scope

- Renaming `scripts/validation/`, `tests/validation/`, or any policy heading
- Adding, removing, or reclassifying any gate
- Proposing a validation programme or an evaluation harness
- Regulated-domain compliance advice
- Secret values, tokens, or raw run output

## Definitions / Facts

The authoritative formulation retrieved for this document is the scope
statement of **IEEE Std 1012**, _IEEE Standard for System, Software, and
Hardware Verification and Validation_. Its abstract defines V&V processes as
assessing whether "development products of a given activity conform to the
requirements of that activity and whether the product satisfies its intended use
and user needs."

Both halves sit in one sentence, and the split is exact:

- **Verification** — does the product conform to the requirements of the
  activity that produced it? The reference point is the specification.
- **Validation** — does the product satisfy its intended use and user needs?
  The reference point is the need, not the specification.

A specification can be implemented perfectly and still fail validation, because
the specification itself can be wrong. This is the entire reason the two words
are not synonyms.

Three further facts from the same source:

- IEEE 1012 specifies "V&V life cycle process requirements … for different
  integrity levels," so V&V rigor is expected to scale with consequence rather
  than being uniform.
- Its V&V processes encompass "analysis, evaluation, review, inspection,
  assessment, and testing of products." **Testing is one technique among six**,
  not a synonym for either V or V.
- The retrieved edition, 1012-2016, is marked superseded by 1012-2024. The 2024
  text was not retrieved and nothing here is attributed to it.

**On the popular formulation.** The widely repeated phrasing "verification: are
we building the product right; validation: are we building the right product" is
a serviceable mnemonic and is commonly attributed to Barry Boehm. That
attribution was not verified for this document and is therefore not cited as a
source. The mnemonic is also weaker than the standard: it implies validation is
a single end-of-line question, whereas IEEE 1012 places V&V across "all
lifecycle phases (development, maintenance, reuse)."

## Where Testing Sits

**ISO/IEC/IEEE 29119** is the software testing standard series. Its own
maintenance site lists eight parts: Part 1 Concepts and Definitions, Part 2 Test
Processes, Part 3 Test Documentation, Part 4 Test Techniques, Part 5 Keyword
Driven Testing, Part 6 Guidelines for Agile Projects, Part 11 Testing of
AI-Based Systems, and Part 13 Testing of Biometric Systems. Parts 1 and 11 are
noted as freely available from ISO; the remainder are paywalled and were not
retrieved.

The existence of a separate testing standard alongside a separate V&V standard
is itself the point. Testing is a technique that can serve either question
depending on what the test is written against. A test asserting that a function
returns the documented value is verification. A test asserting that a documented
procedure achieves its operational purpose when executed is closer to
validation. The same tool, pointed at a different reference, answers a different
question.

**SWEBOK Guide v4.0**, published by the IEEE Computer Society in 2024 and kept
freely accessible, organizes the field into 18 knowledge areas, with Software
Testing and Software Quality as separate areas. That separation reinforces the
same structure: testing is a practice, quality assurance including V&V is a
management discipline that uses it.

## Static and Dynamic Verification

IEEE 1012's enumeration — analysis, evaluation, review, inspection, assessment,
testing — divides naturally into techniques that examine an artifact without
running it and techniques that observe it running.

| Technique              | Executes the artifact | Typical instrument                     |
| ---------------------- | --------------------- | -------------------------------------- |
| Review, inspection     | No                    | Human reading against a checklist      |
| Static analysis        | No                    | Linter, type checker, schema validator |
| Formal analysis        | No                    | Proof or model checker                 |
| Dynamic testing        | Yes                   | Test runner                            |
| Rehearsal in a sandbox | Yes                   | Procedure executed against fixtures    |

This matters for the repository because its checking surface is overwhelmingly
static. Schema conformance, contract conformance, link integrity, and metadata
validation all examine artifacts without running a product — and there is no
product to run.

## V&V Under Non-Determinism

Verification generalizes poorly to systems whose acceptable output is a
distribution rather than a value. A conformance check needs a specified expected
form; agent output has many acceptable forms.

Two standards bodies have begun addressing this, and neither was retrievable in
full for this document:

- **ISO/IEC/IEEE 29119-11**, Testing of AI-Based Systems, exists as a named part
  of the testing series and is listed as freely available from ISO. Its content
  was not retrieved.
- **NIST AI 100-1**, the AI Risk Management Framework, was released
  2023-01-26 and is organized around four functions: Govern, Map, Measure, and
  Manage. The retrieved page describes the framework as "intended for voluntary
  use and to improve the ability to incorporate trustworthiness considerations
  into the design, development, use, and evaluation of AI products, services,
  and systems." Its detailed treatment of measurement and TEVV was not present
  on the retrieved page and is not asserted here.

The structural observation stands regardless of what those documents say. There
are only two ways to make non-deterministic output checkable: constrain the
output until a conformance check applies, or introduce a judgement step. This
repository chose the first, comprehensively. That choice is what the sections
below describe.

## Regulated-Domain Contrast

Regulated domains treat validation as the primary obligation rather than a
secondary one. FDA's _General Principles of Software Validation_, final guidance
Version 2.0 issued in 2002 and superseding a 1997 draft, governs validation of
medical device software and of software used to design, develop, or manufacture
devices. The document itself returned HTTP 404 on direct retrieval and is
recorded here from search metadata only; no definition from it is quoted.

The contrast worth carrying is directional, not detailed: where a commercial
repository can treat validation as a review step, a regulated one must produce
validation evidence as a deliverable, with rigor scaled to risk — the same
principle IEEE 1012 expresses as integrity levels.

## Repository Verification and Validation Surface

The repository operates a large, layered conformance apparatus and almost no
executable validation. Separating the two explains several things the pack
records but does not name. All counts derived at `4122cecf`.

### The gate population is entirely verification

`.github/workflow-contract.yml` registers `schema_version: 2` with 7 workflows,
23 jobs, 80 gate nodes, 16 job roots, 3 profile roots, and 8 pinned actions. All
16 job roots carry `classification: required-quality`, and every one asks a
conformance question.

| Job root                          | Question it answers                                 | Class                 |
| --------------------------------- | --------------------------------------------------- | --------------------- |
| `docs-traceability`               | Does each document link to its declared parent?     | Verification          |
| `docs-implementation-alignment`   | Does documentation match tracked implementation?    | Verification          |
| `repo-contracts`                  | Does the tree satisfy the repository contract set?  | Verification          |
| `agent-output-eval-fixture-gate`  | Does agent output match the governed fixture?       | Verification          |
| `supply-chain-fixture-policy`     | Does the dependency set satisfy declared policy?    | Verification          |
| `dependency-vulnerability-audit`  | Do dependencies carry known advisories?             | Verification          |
| `git-flow-contract`               | Does branch and commit shape satisfy the contract?  | Verification          |
| `compose-validation`              | Does Compose resolve under the core profile?        | Verification          |
| `compose-all-profiles-validation` | Does Compose resolve under every profile?           | Verification          |
| `infrastructure-hardening`        | Do service definitions meet the hardening baseline? | Verification          |
| `template-security-baseline`      | Do templates meet the security baseline?            | Verification          |
| `quickwin-baseline`               | Does the tree hold the declared baseline set?       | Verification          |
| `pre-commit`                      | Do staged files satisfy hook contracts?             | Verification          |
| `frontend-quality`                | Does the sandbox satisfy lint/type/test contracts?  | Verification          |
| `storybook-coverage`              | Does component coverage satisfy the contract?       | Verification          |
| `zizmor`                          | Do workflows satisfy workflow security rules?       | Verification (static) |

Not one job asks whether a delivered capability satisfies a stated need. In IEEE
1012 vocabulary this is a verification battery, not a V&V programme.

### The eval gate is verification, not validation

`ci.agent-output-eval-fixture-gate` is the gate most likely to be read as
validation, because "eval" in agent engineering usually implies judging output
quality. The implementation contradicts that reading.
`scripts/validation/agent_output_eval.py:2` declares itself
`"""Deterministic, model-free semantic evaluation for governed agent outputs."""`

Model-free and deterministic means the gate compares output against a governed
fixture expectation. It answers whether output conforms to a specified shape.
It cannot answer whether the output served the requester, because no judgement
step exists. The gate covers 11 fixtures and 16 synthetic regressions.

This is a deliberate and defensible choice: a deterministic gate is
reproducible, cheap, and cannot drift with a model version. Naming it correctly
matters only because the pack elsewhere calls it the repository's evaluation
loop, which invites a stronger claim than the implementation supports.

### The dynamic test suite verifies the verifiers

`tests/validation/` holds 24 `test_*.py` files and is the entire tracked test
tree. Every file targets a validator or contract engine rather than a product:
`test_document_metadata.py` targets the metadata validator, `test_ci_gate_runner.py`
and `test_ci_gate_contract.py` target the gate engine,
`test_agent_governance_contract.py` targets the governance checker,
`test_document_taxonomy.py` targets the taxonomy engine, and
`test_provider_surface_renderer.py` targets the adapter generator.

Verification is therefore recursive here: the apparatus that checks the
repository is itself checked. That is a genuine strength and is unusual.

Two files break the pattern. `test_postgres_logical_upgrade_rehearsal.py` and
`test_sample_service_delivery_rehearsal.py` execute a procedure in a temporary
sandbox through `subprocess` and `tempfile`, against fixtures under
`tests/fixtures/`. Rehearsing a documented procedure end to end asks whether the
procedure actually works, which is the closest the tracked surface comes to
validation.

### Validation is procedural, not executable

What validation exists lives in human approval gates:

- `docs/00.agent-governance/rules/approval-boundaries.md:46-62` defines 11 Hard
  Stops requiring recorded user approval.
- `docs/00.agent-governance/rules/task-checklists.md:103` opens a Completion
  Checklist asking whether completion criteria for the affected stage are
  satisfied and whether uncertainty was resolved or escalated.
- `docs/00.agent-governance/rules/postflight-checklist.md` groups per-layer
  gates a human confirms.

These ask the validation question. None is executable, so none produces a
machine-checkable result. The repository's validation evidence is a recorded
human judgement in a Stage 04 Task — legitimate evidence, but a different class
from a gate exit code, and it should not be counted alongside gate results.

### Terminology drift in tracked labels

The repository uses "validation" where the standards say verification. This
matches broad industry usage and is not a defect, but it obscures the gap above.

| Location                       | Label                               | What it actually invokes                                                                                                               |
| ------------------------------ | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `approval-boundaries.md:32-44` | Column header "Required Validation" | `validate-docker-compose.sh`, `check-repo-contracts.sh`, `validate-harness.sh`, `check-doc-traceability.sh` — all conformance checkers |
| `scripts/validation/`          | Directory name                      | 41 tracked files (21 shell, 19 Python, 1 JSON contract), predominantly conformance                                                     |
| `tests/validation/`            | Directory name                      | 24 tests, all targeting verification machinery                                                                                         |

A reader taking these labels at face value concludes the repository has a
validation programme. It has a verification programme with human validation
attached at approval points.

## Analysis

The repository resolved the non-determinism problem by constraining agent output
until conformance checking applied — governed fixtures, typed contracts, closed
grammars, deterministic evaluation. That is a coherent and rigorous strategy, and
it is why the eval gate is model-free.

The cost is that no tracked mechanism answers whether a governed output was
useful. Every executable gate answers the specification question. The need
question is answered only by a human at an approval boundary, and only in prose.

This is not an argument for adding a model-judged gate. It is an argument for
labelling the existing evidence accurately, so that "all gates green" is never
read as "the right thing was built."

## Application Notes for This Workspace

- When citing gate coverage, say which question the gate answers. "16 required
  quality jobs" is a verification claim.
- Do not describe `ci.agent-output-eval-fixture-gate` as validation or as
  quality judgement. State that it is deterministic and model-free wherever it
  is cited.
- Treat approval-gate evidence and gate-exit evidence as separate classes, as
  the pack already does for tracked intent versus remote enforcement.
- Read the "Required Validation" column in `approval-boundaries.md` as required
  verification. The column is not wrong in industry usage; it is just not the
  standards term.
- Scale rigor to consequence rather than uniformly, which is what IEEE 1012's
  integrity levels express and what the repository already does implicitly by
  gating protected surfaces harder than documentation.

## Potential Follow-up / Gap

- No tracked gate answers a validation question. Recording this explicitly would
  keep the pack's evaluation-loop language from being read as validation
  coverage.
- The `agent-output-eval` gate's model-free property is a deliberate constraint
  that the pack does not state where it cites the gate.
- The two rehearsal tests are the only executable procedure validation. Whether
  that pattern should extend to other runbooks is a Stage 03 question, not a
  Stage 90 one.
- A glossary entry distinguishing the two terms would remove the ambiguity
  without renaming any directory. Renaming `scripts/validation/` or
  `tests/validation/` is not proposed; the churn would exceed the benefit.
- ISO/IEC/IEEE 12207 and 15288 process definitions could not be retrieved and
  should be obtained through an institutional subscription before any normative
  claim is made from them.

## Source Rules

- External sources were retrieved on **2026-08-10**.
- IEEE 1012 is a fixed, versioned standard. The retrieved 1012-2016 abstract is
  authoritative for what it states; the full text is paywalled and was not read.
  1012-2024 supersedes it and was not retrieved, so no claim is attributed to
  the 2024 edition.
- ISO/IEC/IEEE 12207, 15288, and the paywalled 29119 parts were **not
  retrieved**. `iso.org` returned HTTP 403 to automated retrieval, and the ISO
  publicly-available-standards page now redirects to the paid webstores. No
  definition from those standards is quoted or paraphrased here. This matches
  the ISO catalog 403 already recorded in this pack on 2026-08-07.
- The ISO/IEC/IEEE 29119 part list comes from the standard series' own
  maintenance site, not from ISO, and is treated as descriptive rather than
  normative.
- The FDA guidance is recorded from search metadata only; direct retrieval
  returned HTTP 404 and no definition from it is quoted.
- The "building the right product" mnemonic is recorded as an unattributed
  common formulation because its origin was not verified.
- Repo-local facts derive from tracked contracts, scripts, and tests at
  `4122cecf`; every count is reproducible from the repository.
- No source listed here is adopted policy.

## Sources

- [IEEE Std 1012-2016](https://standards.ieee.org/ieee/1012/5609/) - System, Software, and Hardware Verification and Validation; scope, integrity levels, technique enumeration; abstract only, full text paywalled, superseded by 1012-2024
- [ISO/IEC/IEEE 29119 series site](https://www.softwaretestingstandard.org/) - eight-part structure of the software testing standard series including Part 11 for AI-based systems
- [SWEBOK Guide v4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) - IEEE Computer Society, 2024, freely accessible; 18 knowledge areas separating Software Testing from Software Quality
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - NIST AI 100-1, released 2023-01-26; Govern, Map, Measure, Manage
- [FDA General Principles of Software Validation](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-principles-software-validation) - final guidance Version 2.0, 2002; recorded from search metadata, direct retrieval returned 404
- [Typed workflow contract](../../../../.github/workflow-contract.yml) - 16 job roots and their classification
- [Agent output eval](../../../../scripts/validation/agent_output_eval.py) - deterministic, model-free evaluation
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - Hard Stops and the "Required Validation" column
- [Task checklists](../../../00.agent-governance/rules/task-checklists.md) - Completion Checklist
- [Postflight checklist](../../../00.agent-governance/rules/postflight-checklist.md) - per-layer human-confirmed gates

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when the gate registry, test tree, or approval policy changes, or when IEEE 1012-2024 becomes retrievable
- **Update Trigger**: Re-derive the job-root classification from `.github/workflow-contract.yml` and re-count `tests/validation/`; do not carry a classification forward without re-reading the gate

## Related Documents

- [research pack index](./README.md)
- [quality, CI, CD, QA, and formatting](./quality-ci-formatting.md)
- [harness engineering](./harness-engineering.md)
- [loop engineering](./loop-engineering.md)
- [automation, pipeline, and workflow](./automation-pipeline-workflow.md)
- [github actions platform](./github-actions-platform.md)
- [spec-driven development and SDLC](./spec-driven-sdlc.md)
