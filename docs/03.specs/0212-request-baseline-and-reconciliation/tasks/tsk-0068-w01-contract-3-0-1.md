---
title: "W01 Contract 3.0.1 Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-15"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0068"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-15"
---

# W01 Contract 3.0.1 Task

## Scope

### Objective and Parent

#### Objective

Own W129/criterion 124, the W01-CONTRACT run of the 3.0.1 package for this
workspace. Compare the current rules, roles, approval and review routes and
the Registry vocabulary with designs D00, D01, D03 and D15. Give each rule a
verdict, change only the rules that conflict with a confirmed requirement,
and change their actual consumers in the same change.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [3.0.1 W00 delta](tsk-0066-w00-delta-3-0-1.md)
- [3.0.1 W00 delta gap closure](tsk-0067-w00-delta-gap-closure.md)

### Inputs and Authority

On 2026-11-15 the user asked to continue after W00; the W00 report named
W01-CONTRACT as ready. Inputs of the git-ignored package
`_workspace/governance/workspace_governance_3_0_1_20261115/`, read as
reference data: the W01-CONTRACT prompt, designs D01 and D03 in full (D00 and
D15 were read in TSK-0066), sources S02 to S07 and S27, `decisions.json` and
`repository-vocabulary.json`.

The same day the owner approved adopting the shared contract
`repository-vocabulary` 3.0.1 in this repository, in answer to a question
naming the contract, its revision and its term differences. Q08 (review by
risk), Q09 (seven vocabulary columns) and Q-DRAFT are the owner's confirmed
decisions in `decisions.json`. The user's request covers commit, push, pull
request and merge.

## Execution Log

### Work Performed

#### Design summary

| Item | Content |
| --- | --- |
| Designs | D00, D01, D03, D15, bundle 3.0.1 |
| Target | One owner per rule; the vocabulary contract the owner adopted; review effort set by risk; drafts never the sole basis for work |
| Choice | Change the rules that conflict, in their current owners; keep every rule that already fits |
| Rejected | Re-deriving roles or sections from their count; a new global draft gate (D03 forbids it); a new Registry field for vocabulary columns (the template table already owns the header) |
| Interface | `vocabulary_contract_findings` gains `vocabulary-row-width` and `vocabulary-korean-missing`; `version_change_findings` skips the raise for `template-source` |
| Risk | Policy and Registry changes are high-risk: independent `rules-engineer` review |

#### Rule verdicts

| ID | Rule | Verdict | Owner and consumers | Enforcement |
| --- | --- | --- | --- | --- |
| R-01 | RFC 2119 and RFC 8174 key words (S27) | KEEP_VERIFIED | `glossary.md` Normative Language | Review only |
| R-02 | No Release document role | KEEP_VERIFIED | `documentation-protocol.md`; guard from PR 1020 | Metadata check |
| R-03 | Native settings are not a second policy owner | KEEP_VERIFIED | `.claude/provider.md`, `.codex/provider.md`; generated projections | Renderer `--check`, drift 0 |
| R-04 | Seven-column vocabulary, contract 3.0.1 | CHANGE, done | `glossary.md` 0.9.0, Registry `vocabulary_contract`, `table_column_definitions`, `vocabulary.template.md`, `registry.py` | Registry test and the template table check |
| R-05 | Review by risk (Q08) | CHANGE, done | `workflows.md` 1.5.0 Review Risk; `sdlc.md` 1.11.0; `workflow-supervisor` role 1.2.0; `task-breakdown-agent` skill 1.3.0 and their projections | Review only; no checker reads the review class |
| R-06 | A draft never authorizes work on its own (Q-DRAFT) | CHANGE, done | `sdlc.md` 1.11.0, one paragraph | Task under a draft Spec or Plan: `spec_packages.py:686-696`; other families: review only |
| R-07 | Template sources cannot be edited under `check-changed` | CHANGE, done | `metadata/version.py` | `test_a_template_source_keeps_its_initial_version` |

R-07 was found while doing R-04: since PR 1006 and 1019 a changed template
needed a higher version, while `invalid-template-version` requires the
registered initial version, so no template edit could pass `check-changed`.

#### Review findings and fixes

The independent `rules-engineer` review of `101b8ec7f..6504d0cd7` reported
two HIGH, two MEDIUM and four LOW findings. Each was fixed in this branch:

| Finding | Fix |
| --- | --- |
| H1 `github-governance.md` said "no separate tier scheme" and required a fresh-context review of every diff | 1.10.0 reads the class from Review Risk; only a high-risk diff needs the fresh-context review |
| H2 Common rows cited 3.0.1 while keeping older meanings | Meaning review below; ten rows rewritten |
| M1 `documentation-protocol.md` Version objects still said `1.1.0` | 5.0.1 says `3.0.1` and records the adoption |
| M2 `quality-standards.md` gave candidate acceptance to independent review for every change | 1.12.1 says review by risk |
| L1 `persona.md` and `agentic.md` required independent review unconditionally | Both limited to high-risk work |
| L2 Design Fitness linked a load order, not a design owner | Linked to SDLC `#sequence` |
| L3 Template drift after the version exemption | Comment names the pin, the tests and the protected-surface review; a provider-binding template is outside the pin and stays with W03-VERSION |
| L4 An exemption in Review Risk named no protected surface | Removed |

A nit moved the cancelled-Spec sentence back out of the draft paragraph.

#### Vocabulary meaning review

Each of the 43 common rows was compared with the contract's Korean
definition, Not to Confuse value and owner role. Rewritten as English
renderings of 3.0.1: Archive and Removal (definition), Contract Version
(definition), Document Revision, Prerelease and Build Metadata (definition
and Not to Confuse), Compatibility, Registry Schema Version and Baseline
Namespace (Not to Confuse), and Design Fitness (owner). The other 33 rows
match. The narrower local meaning of archive stays in "Archive, here".

#### New handoff

| ID | Item | Verdict | Receiving owner |
| --- | --- | --- | --- |
| D-13 | Contract 3.0.1 and Q03 limit document and contract versions to `X.X.X`, so Prerelease and Build Metadata are unused there. `documentation-protocol.md` Version objects and the frontmatter schema accept full SemVer 2.0.0, adopted in W06 (PR 1019) | CHANGE | W03-VERSION |

Roles and sections were not judged by their count. Other repositories adopt
the vocabulary contract in their own Tasks; this Task records only this
repository's adoption.

#### Vocabulary adoption record

| Field | Value |
| --- | --- |
| Contract | `repository-vocabulary` 3.0.1 |
| Source | `dependencies/repository-vocabulary.json`, SHA-256 `a8f595f543f380f992a20a52886d0cc2b4f340c47a449537d2f90ec082f39dfb` |
| Approved by | @buenhyden, 2026-11-15, in this chat |
| Scope | `hy-home.docker` only |
| Changes from 1.1.0 | Korean column; TERM-DRAFT, TERM-READINESS, TERM-DESIGN-FIT added; TERM-HISTORICAL-AUDIT moved to Local Extensions |
| Exceptions | English definitions here; the contract's Korean definitions are not copied, since the glossary is an English document |
| Migration | One change: Registry pin, template header, glossary rows |
| Rollback | Revert the adoption commit; no runtime consumer |

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0068 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0068 | ready | in-progress | #design-summary |

### Blockers and Decisions

The vocabulary revision needed the owner's approval naming it; the owner gave
it on 2026-11-15. No other question was needed.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Vocabulary RED | 124 | W129 | red-green-proof | `VocabularyContractTests` before the change | FAIL | 4 failures: pinned 3.0.1, row width, Korean empty, version regex | required | - |
| Vocabulary GREEN | 124 | W129 | red-green-proof | `test_registry`, `test_template_definition`, `metadata.test_heading`, `metadata.test_lifecycle` at `7713114cd` | PASS | 327 tests OK | required | Vocabulary RED |
| Template version RED | 124 | W129 | red-green-proof | `test_a_template_source_keeps_its_initial_version` before the change | FAIL | `version-unchanged` reported | required | - |
| Template version GREEN | 124 | W129 | red-green-proof | `metadata.test_lifecycle` at `eb60d2a33` | PASS | module OK | required | Template version RED |
| Governance contract | 124 | W129 | governance-contract | `check-agent-governance-contract.py` at `6504d0cd7` | PASS | failures 0 | required | - |
| Renderer parity | 124 | W129 | renderer-parity | `provider_surface_renderer.py --write` then `--check` | PASS | drift 0 | required | - |
| Metadata changed | 124 | W129 | document-metadata | `check-document-metadata.py --mode check-changed --base-ref origin/main` | PASS | selected 6, violations 0 | required | - |
| Links alignment | 124 | W129 | document-links | `check-document-links.py --mode alignment` | PASS | failures 0 | required | - |
| Script manifest | 124 | W129 | script-manifest | `check-script-manifest.py` | PASS | valid | required | - |
| Independent review | 124 | W129 | independent-review | `rules-engineer`, read-only, diff `101b8ec7f..6504d0cd7` | FAIL | 2 HIGH, 2 MEDIUM, 4 LOW; see Review findings and fixes | required | - |

### Resolution Links

Vocabulary RED is resolved by Vocabulary GREEN, and Template version RED by
Template version GREEN.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 124 | pending | Vocabulary GREEN, Template version GREEN, Governance contract, Renderer parity | Awaiting independent review and owner acceptance | SPEC-0212 TSK-0068 |

### Remaining Conditions

Independent `rules-engineer` review of the three commits, hosted candidate
checks and owner acceptance of criterion 124.

## Handoff

### Promotion Receipt

| Criterion | Work Unit | Task result | Target | Consumer update and check |
| --- | --- | --- | --- | --- |
| 124 | W129 | Vocabulary GREEN | `glossary.md`, Registry `vocabulary_contract`, `vocabulary.template.md` | `VocabularyContractTests`; template table check |
| 124 | W129 | Governance contract | `workflows.md`, `sdlc.md`, `workflow-supervisor` role, `task-breakdown-agent` skill | Governance contract; renderer parity |

### Next Owner

@buenhyden accepts criterion 124. W02-DISPOSITION, W03-VERSION, W04-CONTENT,
W07-BRIEF, W07-ADAPTER, W08-MEMORY and W10-REVIEW list W01 as their
prerequisite.
