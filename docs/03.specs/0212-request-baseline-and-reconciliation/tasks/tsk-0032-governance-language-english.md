---
title: "Governance Language English Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0032"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Governance Language English Task

## Overview

### Objective

Execute W48: make English the language of non-README governance, hook, role,
skill, knowledge, and prompt documents and of the authored provider guidance,
keep every `README.md` Korean, and enforce it. This Task owns criterion 43
only.

## Inputs and Authorization

On 2026-10-29 the owner directed that the governance documents just changed
be written in English, that the rule itself change with them, and that
`README.md` files stay Korean. Asked how far to apply it, the owner chose the
full conversion: change the rule, switch the profiles to English, and
translate the existing Korean passages in the same change. The input is
`main` at merged PR #628. The authorization covers these edits, this branch,
its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0032 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0032 | ready | in-progress | #objective |
| SPEC-0212-TSK-0032 | in-progress | completed | #evidence |

### Rule change

| Surface | Before | After |
| --- | --- | --- |
| `documentation-protocol.md` Document language | New governance and provider prose defaults to Korean; `ko-or-en` lets English and Korean coexist | Priority rule 4: non-README `.agents/` documents and the authored provider documents are English |
| `bootstrap.md` Hard Constraints | New common guidance defaults to Korean | Governance and provider guidance is English; every `README.md` is Korean |
| `standards.md` Language Standard | Stage 01–03 English, READMEs and operations Korean | Adds governance and provider guidance to English |
| Registry `language` of the 8 `governance-*` profiles | `ko-or-en` | `en` |
| `document-profile.schema.json` language enum | `ko`, `en`, `ko-or-en` | `ko`, `en` |
| `language.py` | `ko-or-en` was never judged | Removed; the 8 profiles are now judged as English |
| 8 governance template author prompts | Write new prose in Korean | Write body prose in English |
| `test_language.py`, `test_registry.py` | Expected `ko-or-en` for `governance-*` | Expect `en` |

### Passages translated

About 105 Korean lines became English without changing meaning: the shared
memory store rules in `environment-constraints.md`, the commit-time and local
toolchain rules in `quality-standards.md`, the QA definition trust rule in
`github-governance.md`, the commit-check rule in `git-workflow.md`, the
language bullets in `standards.md` and `bootstrap.md`, and the Scope line of
15 hook rule documents. No remaining non-README document under `.agents/` or
provider document contains Hangul. `README.md` files were not touched.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Language check | 43 | W48 | `check-document-links.py --mode language` | This branch | PASS | 1,165 documents, 0 failures, now judging the 8 profiles as English | required | - |
| Language and registry tests | 43 | W48 | `python3 -m unittest tests.lib.document_governance.test_language tests.lib.document_governance.test_registry` | This branch | PASS | 133 tests OK | required | - |
| Gate and routing tests | 43 | W48 | `python3 -m unittest tests.validation.test_agent_governance_ci_routing tests.lib.gate.test_ci_gate_adapters tests.validation.test_ci_gate_plan` | This branch | PASS | 175 tests OK | required | - |
| Agent governance | 43 | W48 | `check-agent-governance-contract.py` | This branch | PASS | 0 failures | required | - |
| Provider projections | 43 | W48 | `provider_surface_renderer.py --check` | This branch | PASS | 2 providers, 0 drift | required | - |
| Metadata contracts | 43 | W48 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 43 | accepted | Language check, Language and registry tests, Gate and routing tests, Agent governance, Provider projections, Metadata contracts | Governance and provider guidance is English and enforced as English; README files stay Korean. | SPEC-0212 TSK-0032 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Governance gap rules](tsk-0031-governance-gap-rules.md)
