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
thoroughly and the other in exactly one place.

Verification asks whether a product conforms to the requirements placed on it.
Validation asks whether the product satisfies its intended use. A conformance
checker cannot answer the second question. Fifteen of the repository's sixteen
required-quality job roots are conformance checkers; the sixteenth also runs two
procedure rehearsals, and those are the only executable validation the
repository has.

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

The authoritative formulation retrieved for this document is the abstract of
**IEEE Std 1012**, _IEEE Standard for System, Software, and Hardware
Verification and Validation_. Only that abstract was read; the full text is
paywalled. It defines V&V processes as assessing whether "development products of a given activity conform to the
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
described by that site as freely available from ISO; the remainder are paywalled
and were not retrieved.

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
  of the testing series. The same maintenance site describes it as freely
  available from ISO. That is a claim about ISO's distribution policy which could
  not be confirmed against ISO itself, because `iso.org` refused automated
  retrieval. Its content was not retrieved either.
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
recorded here from search-result metadata only. The version, year, supersession,
and scope above come from that metadata and were not read in the document
itself; no content from its body is asserted.

The contrast worth carrying is directional, not detailed: where a commercial
repository can treat validation as a review step, a regulated one must produce
validation evidence as a deliverable, with rigor scaled to risk — the same
principle IEEE 1012 expresses as integrity levels.

## Repository Verification and Validation Surface

The repository operates a large, layered conformance apparatus and almost no
executable validation. Separating the two explains several things the pack
records but does not name. All counts derived at `4122cecf`.

### The gate population is verification, with one exception

`.github/workflow-contract.yml` registers 16 job roots, all carrying
`classification: required-quality`. The counts behind that registry —
7 workflows, 23 jobs, 80 gate nodes, 3 profile roots, 8 pinned actions — are
owned by [automation, pipeline, and workflow](./automation-pipeline-workflow.md)
and are not re-derived here.

Fifteen of the sixteen roots ask a conformance question. One does not, and it
is the most interesting row in the table.

| Job root                          | Question it answers                                    | Class                   |
| --------------------------------- | ------------------------------------------------------ | ----------------------- |
| `docs-traceability`               | Does each document link to its declared parent?        | Verification            |
| `docs-implementation-alignment`   | Does documentation match tracked implementation?       | Verification            |
| `repo-contracts`                  | Does the tree satisfy the repository contract set?     | Verification            |
| `agent-output-eval-fixture-gate`  | Is the fixture catalog self-consistent and calibrated? | Verification            |
| `supply-chain-fixture-policy`     | Five subjects, two of which rehearse a procedure       | **Mixed**               |
| `dependency-vulnerability-audit`  | Do sandbox dependencies carry known advisories?        | Verification (arguable) |
| `git-flow-contract`               | Does branch and commit shape satisfy the contract?     | Verification            |
| `compose-validation`              | Does Compose resolve under the core profile?           | Verification            |
| `compose-all-profiles-validation` | Does Compose resolve under every profile?              | Verification            |
| `infrastructure-hardening`        | Do service definitions meet the hardening baseline?    | Verification            |
| `template-security-baseline`      | Do templates meet the security baseline?               | Verification            |
| `quickwin-baseline`               | Does the tree hold the declared baseline set?          | Verification            |
| `pre-commit`                      | Do staged files satisfy hook contracts?                | Verification            |
| `frontend-quality`                | Does the sandbox lint, typecheck, and build?           | Verification            |
| `storybook-coverage`              | Does component coverage satisfy the contract?          | Verification            |
| `zizmor`                          | Do workflows satisfy workflow security rules?          | Verification (static)   |

Every technique in this table except the two rehearsals is static in the IEEE
1012 sense: it examines an artifact without running a product. The `zizmor` row
is marked static only because static analysis is its named category, not
because the others execute anything.

**The `supply-chain-fixture-policy` exception.** This root expands to three
leaves. Two are `--check` invocations on deterministic supply-chain policy and
summary freshness. The third runs five unittest modules:

```
run-unittest tests.validation.test_compose_core_readiness
             tests.validation.test_postgres_logical_upgrade_rehearsal
             tests.validation.test_grype_db_seed
             tests.validation.test_supply_chain_policy
             tests.validation.test_sample_service_delivery_rehearsal -v
```

Two of those five are the procedure rehearsals described below. So the
rehearsals are not merely present in the tree — they execute inside a
required-quality CI gate on every push and pull request to `main`. Dependency
policy is one subject of five, and describing this root as a dependency check
hides the rehearsals entirely.

That single root is the repository's only executable validation. Fifteen of
sixteen roots ask a conformance question; the sixteenth asks a conformance
question about three subjects and a does-it-actually-work question about two.

The remaining seven of the repository's 23 jobs sit in non-gating workflows —
`document-corpus-lifecycle`, `changelog`, `issue-greeting`,
`pull-request-greeting`, `triage`, `stale`, and `drift-gate`. None asks a
validation question either.

### The eval gate is verification, not validation

`ci.agent-output-eval-fixture-gate` is the gate most likely to be read as
validation, because "eval" in agent engineering usually implies judging output
quality. The implementation contradicts that reading.
`scripts/validation/agent_output_eval.py:2` declares itself
`"""Deterministic, model-free semantic evaluation for governed agent outputs."""`

The gate is weaker than even that docstring suggests. In CI it scores no agent
output at all. `scripts/validation/ci_gate_adapters.py` runs
`run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions` and
then asserts that stdout contains `fixtures_check=pass` and
`regressions_check=pass`. Those two modes check that the fixture catalog is
internally consistent and that its 16 synthetic regressions still classify as
calibrated. Scoring a real output requires `--fixture` and `--classification`
arguments on stdin, which no gate supplies.

So the gate verifies the measuring instrument, not any measurement. It is two
levels removed from validation: it does not judge whether output served the
requester, and it does not even score output. It covers 11 fixtures and 16
synthetic regressions.

This is a deliberate and defensible choice: a deterministic gate is
reproducible, cheap, and cannot drift with a model version. Naming it correctly
matters only because the pack elsewhere calls it the repository's evaluation
loop, which invites a stronger claim than the implementation supports.

### The dynamic test suite verifies the verifiers

`tests/validation/` is the entire tracked test tree and holds 26 tests: 24
`test_*.py` files plus two shell tests, `test_run_ci_precommit.sh` and
`test_run_agent_precommit_all_files.sh`. Nearly every one targets a validator or
contract engine rather than a product:
`test_document_metadata.py` targets the metadata validator, `test_ci_gate_runner.py`
and `test_ci_gate_contract.py` target the gate engine,
`test_agent_governance_contract.py` targets the governance checker,
`test_document_taxonomy.py` targets the taxonomy engine, and
`test_provider_surface_renderer.py` targets the adapter generator.

Verification is therefore recursive here: the apparatus that checks the
repository is itself checked. That is a genuine strength and is unusual.

Three files break the pattern. `test_postgres_logical_upgrade_rehearsal.py` and
`test_sample_service_delivery_rehearsal.py` execute a procedure in a temporary
sandbox through `subprocess` and `tempfile`, against fixtures under
`tests/fixtures/`. `test_run_agent_precommit_all_files.sh` does the same for the
controlled all-files wrapper, driving it end to end in a temporary repository
against a fake pre-commit binary.

Rehearsing a documented procedure end to end asks whether the procedure actually
works. That is a validation question, and these three are where the repository
asks it. The first two run inside the `supply-chain-fixture-policy` gate. The
third is registered in no gate node — `leaf.ci-precommit-regressions` runs the
sibling `test_run_ci_precommit.sh` — so it executes only when a Stage 04
procedure invokes it by hand.

### The rest of validation is procedural

Outside the three rehearsals, validation lives in human approval gates:

- `docs/00.agent-governance/rules/approval-boundaries.md:46-62` defines 11 Hard
  Stops requiring recorded user approval.
- `docs/00.agent-governance/rules/task-checklists.md:103` opens a Completion
  Checklist asking whether completion criteria for the affected stage are
  satisfied and whether uncertainty was resolved or escalated.
- `docs/00.agent-governance/rules/postflight-checklist.md` groups per-layer
  gates a human confirms.

These ask the validation question about scope and need, which no rehearsal can
answer: a procedure can work perfectly and still be the wrong procedure. None of
them is executable, so each produces a recorded human judgement rather than a
gate exit code. That is legitimate evidence of a different class, and it should
not be counted alongside gate results.

The accurate summary is therefore narrower than "validation is not executable":
procedure validation is executable and enforced for three procedures, and
everything else — whether a capability meets a need — is human judgement.

### Terminology drift in tracked labels

The repository uses "validation" where the standards say verification. This
matches broad industry usage and is not a defect, but it obscures the gap above.

| Location                       | Label                               | What it actually invokes                                                                                                                                                                                                                            |
| ------------------------------ | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `approval-boundaries.md:32-44` | Column header "Required Validation" | Five conformance checkers — `validate-docker-compose.sh`, `check-repo-contracts.sh`, `validate-harness.sh`, `check-doc-traceability.sh`, and `check-agent-governance-contract.py --mode contract` — plus one non-script entry, "Doc link integrity" |
| `scripts/validation/`          | Directory name                      | 41 tracked files (21 shell, 19 Python, 1 JSON contract), predominantly conformance                                                                                                                                                                  |
| `tests/validation/`            | Directory name                      | 26 tests, 23 of which target verification machinery                                                                                                                                                                                                 |

A reader taking these labels at face value concludes the repository has a
validation programme. It has a verification programme with human validation
attached at approval points.

## Analysis

The repository resolved the non-determinism problem by constraining agent output
until conformance checking applied — governed fixtures, typed contracts, closed
grammars, deterministic evaluation. That is a coherent and rigorous strategy, and
it is why the eval gate is model-free.

The cost is that no tracked mechanism answers whether a governed output was
useful. The one executable exception, procedure rehearsal, answers a narrow
validation question — does this documented procedure work — and does not
generalise to agent output. The broader need question is answered only by a
human at an approval boundary, and only in prose.

One gate resists even the specification framing. `dependency-vulnerability-audit`
runs `npm audit --audit-level=high` against a single sandbox project, and its
reference point is an external, mutable advisory database rather than a
repository-authored specification. Its verdict can flip with no change to any
tracked artifact — precisely the drift property the model-free eval gate was
designed to avoid. It is classified as verification here because it checks a
declared dependency set against a stated threshold, but the classification is
genuinely arguable.

This is not an argument for adding a model-judged gate. It is an argument for
labelling the existing evidence accurately, so that "all gates green" is never
read as "the right thing was built."

## Application Notes for This Workspace

- When citing gate coverage, say which question the gate answers. "16 required
  quality jobs" is a verification claim for fifteen of them and a mixed claim
  for `supply-chain-fixture-policy`.
- Do not describe `ci.agent-output-eval-fixture-gate` as validation or as
  quality judgement. In CI it checks its own fixture catalog and regression
  calibration and scores no agent output; state that wherever it is cited.
- Do not infer a gate's subject from its name. `supply-chain-fixture-policy`
  runs two procedure rehearsals among five unittest modules, and
  `leaf.ci-precommit-regressions` runs `test_run_ci_precommit.sh` rather than
  the similarly named all-files wrapper rehearsal. Resolve the gate through
  `.github/workflow-contract.yml` before describing it.
- Treat approval-gate evidence and gate-exit evidence as separate classes, as
  the pack already does for tracked intent versus remote enforcement.
- Read the "Required Validation" column in `approval-boundaries.md` as required
  verification. The column is not wrong in industry usage; it is just not the
  standards term.
- Scale rigor to consequence rather than uniformly, which is what IEEE 1012's
  integrity levels express and what the repository already does implicitly by
  gating protected surfaces harder than documentation.

## Potential Follow-up / Gap

- Exactly one job root carries executable validation, and it is not named for
  it. `supply-chain-fixture-policy` runs two procedure rehearsals among five
  unittest modules, so the repository's only enforced validation is invisible
  from the gate name.
- The `agent-output-eval` gate does not score agent output in CI; it checks its
  own fixture catalog and regression calibration. The pack cites it as the
  repository's evaluation loop without stating this.
- Three rehearsals exist and only two are gated.
  `test_run_agent_precommit_all_files.sh` is registered in no gate node; the
  registered `leaf.ci-precommit-regressions` runs the sibling
  `test_run_ci_precommit.sh` instead. The all-files wrapper rehearsal is invoked
  only by Stage 04 plan procedures, so the repository's most safety-relevant
  rehearsal is the one nothing enforces. Whether the rehearsal pattern should
  extend to other runbooks, and whether this one should be gated, are Stage 03
  questions rather than Stage 90 ones.
- A glossary entry distinguishing the two terms would remove the ambiguity
  without renaming any directory.
  `docs/90.references/data/glossary/stable-reference-terms.md` is the existing
  destination and currently defines neither term. Renaming
  `scripts/validation/` or `tests/validation/` is not proposed; the churn would
  exceed the benefit.
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
- The FDA guidance is recorded from search-result metadata only, including its
  version, year, and scope; direct retrieval
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
