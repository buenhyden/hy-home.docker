---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md -->

# Task: Agentic Research Pack Consolidation

## Overview

This document tracks the source research, canonical document changes,
supersession work, logical commits, reviews, and verification evidence for the
agentic research pack consolidation defined by Spec 122 and its implementation
plan.

## Inputs

- **Parent Spec**:
  [Agentic Research Pack Consolidation](../../03.specs/122-agentic-research-pack-consolidation/spec.md)
- **Parent Plan**:
  [Agentic Research Pack Consolidation Plan](../plans/2026-07-10-agentic-research-pack-consolidation.md)
- **Canonical Research Pack**:
  [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Duplicate Pack**:
  [2026-07-07 Update](../../90.references/research/2026-07-07-agentic-research-pack-update/README.md)

## Working Rules

- Use tracked repo-local files and active stage documents for workspace truth.
- Use official vendor, standards, original-paper, and official-repository
  sources for external research.
- Apply the provider-model cutoff at 2026-07-10 10:00 KST (01:00 UTC).
- Record source metadata and concise evidence; do not paste raw pages, raw
  command output, diagnostics, shell history, or secret material.
- Keep Stage 90 advisory and record active-policy/runtime changes as follow-up
  gaps.
- Use one sequential implementer and one task-scoped review gate per task.
- Commit each clean reviewed task as one logical unit.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-ARC-001 | Refresh workspace baseline, spec-driven SDLC, document roles, and source evidence | doc | VAL-ARC-002, VAL-ARC-007, VAL-ARC-009 | PLN-ARC-001 | Category/role coverage, validators, commit range, task review | Documentation implementer | Ready for Review |
| T-ARC-002 | Add cutoff-bound provider model landscape and refresh task selection | doc/eval | VAL-ARC-003, VAL-ARC-004 | PLN-ARC-002 | Model/lifecycle totals, cutoff exceptions, provider sources, validators, task review | Documentation implementer | Todo |
| T-ARC-003 | Consolidate harness, loop, provider implementation, and AI agent catalogs | doc | VAL-ARC-002, VAL-ARC-005 | PLN-ARC-003 | Capability sources, stale-claim disposition, validators, task review | Documentation implementer | Todo |
| T-ARC-004 | Refresh QA/CI/formatting and automation/pipeline/workflow research | doc | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-004 | Gate/job inventory, evidence classes, validators, task review | Documentation implementer | Todo |
| T-ARC-005 | Refresh Docker Compose/infrastructure and security-governance research | doc/security | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-005 | Rechecked Compose evidence, security status/gap matrix, validators, task review | Documentation implementer | Todo |
| T-ARC-006 | Finalize indexes, supersede duplicate pack, close lifecycle and validation | doc/eval | VAL-ARC-001, VAL-ARC-005, VAL-ARC-006, VAL-ARC-007, VAL-ARC-008, VAL-ARC-009, VAL-ARC-010 | PLN-ARC-006 | Coverage/disposition matrix, final checks, whole-branch review, closure commit | Workflow supervisor | Todo |

## Phase View

### Phase 1: Workspace and Lifecycle Baseline

- [ ] T-ARC-001 Refresh workspace baseline, SDLC, document roles, and evidence.

### Phase 2: Provider and Agent Research

- [ ] T-ARC-002 Add provider model landscape and task-selection analysis.
- [ ] T-ARC-003 Consolidate harness, loop, provider, and AI agent research.

### Phase 3: Quality, Infrastructure, and Security

- [ ] T-ARC-004 Refresh QA/CI/formatting and automation research.
- [ ] T-ARC-005 Refresh Compose/infrastructure and security research.

### Phase 4: Consolidation Closure

- [ ] T-ARC-006 Supersede the duplicate pack, close indexes/lifecycle, and
      record final evidence.

## Source Evidence Contract

Each task appends a source ledger with these exact fields:

Rows are added only after a task verifies the source. A mutable page that cannot
prove an applicable model cutoff must use `historical state unverified`.

| Source URL / repo path | Owner / source class | Supported claim | Published / updated | Retrieved | Cutoff disposition | Caveat | Task |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax> | GitHub / official mutable documentation | A workflow is YAML automation composed of jobs and steps with triggers and permissions. | Not shown | 2026-07-10 | Not applicable (non-model source) | Mutable page; retrieval-time syntax only, not proof of remote enforcement. | T-ARC-001 |
| <https://csrc.nist.gov/pubs/sp/800/218/final> | NIST / official standard publication page | SSDF v1.1 provides high-level secure-development practices integrable into an SDLC. | 2022-02 | 2026-07-10 | Not applicable (non-model source) | Framework comparison only; no workspace control mapping or adoption. | T-ARC-001 |
| <https://github.github.com/spec-kit/> | GitHub / official mutable project documentation | Current core flow is Spec → Plan → Tasks → Implement, with each Markdown artifact feeding the next. | 2026-05-27 | 2026-07-10 | Not applicable (non-model source) | Page displays “Last updated: May 27, 2026”; mutable retrieval-time content only, and no Spec Kit runtime or policy is adopted. | T-ARC-001 |
| <https://github.com/github/spec-kit/blob/main/spec-driven.md> | GitHub / official repository document | Specifications provide implementation context and a constitution supplies cross-phase principles. | Not shown | 2026-07-10 | Not applicable (non-model source) | `main` is mutable; retrieval-time content only. | T-ARC-001 |
| <https://www.iso.org/standard/63712.html> | ISO / official standards metadata | ISO/IEC/IEEE 12207:2017 identifies software lifecycle-process framing. | 2017-11 | 2026-07-10 | Not applicable (non-model source) | Page now marks the edition withdrawn; historical metadata only, not a current normative basis. | T-ARC-001 |
| <https://www.iso.org/standard/72089.html> | ISO / official standards metadata | ISO/IEC/IEEE 29148:2018 supplies requirements-engineering framing. | 2018-11 | 2026-07-10 | Not applicable (non-model source) | Public metadata/summary is not full standard text; page says the standard is to be revised. | T-ARC-001 |
| <https://www.iso.org/standard/74393.html> | ISO / official standards metadata | ISO/IEC/IEEE 42010:2022 supplies architecture-description framing. | 2022-11 | 2026-07-10 | Not applicable (non-model source) | Public metadata/summary is not full standard text; repo ARD scope is narrower. | T-ARC-001 |
| <https://adr.github.io/> | ADR community / curated primary practice hub | An ADR captures one architectural decision, rationale, trade-offs, and consequences. | Not shown | 2026-07-10 | Not applicable (non-model source) | Curated mutable page, not a workspace mandate. | T-ARC-001 |
| <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions> | Michael Nygard / original practice article | Original ADR practice records status, context, decision, and consequences. | 2011-11-15 | 2026-07-10 | Not applicable (non-model source) | Original essay is practice guidance, not a standard. | T-ARC-001 |
| <https://sre.google/sre-book/managing-incidents/> | Google SRE / official book chapter | Incident command separates command, operations, communications, planning, and live state. | Not shown on page | 2026-07-10 | Not applicable (non-model source) | Book guidance; page has no visible update date and is not adopted incident policy. | T-ARC-001 |
| <https://sre.google/sre-book/postmortem-culture/> | Google SRE / official book chapter | A reviewed blameless postmortem records impact, mitigation, root causes, and preventive actions. | Not shown on page | 2026-07-10 | Not applicable (non-model source) | Book guidance; page has no visible update date and is not adopted policy. | T-ARC-001 |
| <https://csrc.nist.gov/pubs/sp/800/61/r3/final> | NIST / official standard publication page | SP 800-61 Rev. 3 frames incident response as a CSF 2.0 Community Profile. | 2025-04 | 2026-07-10 | Not applicable (non-model source) | Supersedes Rev. 2; comparison only, with no formal workspace mapping. | T-ARC-001 |
| <https://www.pagerduty.com/resources/learn/what-is-a-runbook/> | PagerDuty / vendor practice guide | A runbook is detailed repeatable operational how-to guidance and may be manual or automated. | Not shown | 2026-07-10 | Not applicable (non-model source) | Redirects to `/resources/automation/learn/what-is-a-runbook/`; mutable vendor guidance, not policy. | T-ARC-001 |
| <https://keepachangelog.com/en/1.1.0/> | Keep a Changelog / official convention page | Changelogs communicate notable human-readable changes and maintain an Unreleased section. | 2019-02-15 (v1.1.0) | 2026-07-10 | Not applicable (non-model source) | Convention only; site content includes later maintenance updates. | T-ARC-001 |
| <https://semver.org/> | Semantic Versioning / official specification page | MAJOR, MINOR, and PATCH communicate incompatible, compatible feature, and compatible fix changes. | Not shown (2.0.0) | 2026-07-10 | Not applicable (non-model source) | Requires a declared public API; does not define workspace release approval. | T-ARC-001 |

## T-ARC-001 Evidence

### Status and Scope

Status is **Ready for Review**. The implementation is documentation-only; code
TDD is not applicable. The editable scope was exactly this task record and the
three canonical Stage 90 references below. Per the task completion contract,
`T-ARC-001` remains open until the controller records the independent review.

### Source and Coverage Inventory

- Repo-local baseline: tracked root, docs, Stage 00, templates, scripts, infra,
  Compose, CI workflow, active stage artifacts, and existing research references.
- External baseline: all 13 URLs under the plan's `Spec-driven SDLC and
  document roles` source group plus GitHub Actions workflow syntax and NIST SSDF.
- Workspace comparison map: 25 category rows with the required eight columns.
- Lifecycle matrix: 7 forward/feedback transition records plus a participant
  boundary for Compose, CI, and secure SDLC.
- Document-role matrix: 19 rows, including separate API, agent, data, and test
  supporting contracts.

### Changed Files

- `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md`

### Validation Evidence

The clean pre-edit base passed the same five commands. The final post-edit gate
recorded:

- `git diff --check` — exit 0.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; generated
  index reported fresh.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0; four changed
  template-mapped docs normalized, repository `failures=0`.

### Review-Fix Validation Evidence

After addressing I-1 through I-3 and M-1, the review-fix cycle reran every
covering command:

- `git diff --check` — exit 0.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; generated
  index reported fresh.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=3`, `normalized_changed_template_docs_total=3`,
  repository `failures=0`.

### Commit and Implementer Review Evidence

- Task brief: `.superpowers/sdd/task-1-brief.md`.
- Implementer report: `.superpowers/sdd/task-1-implementer-report.md`.
- Base commit: `341282da13c2ff4aec5c5415dbdde9efeac5b0dd`.
- Closure range: `341282da13c2ff4aec5c5415dbdde9efeac5b0dd..HEAD`
  evaluated immediately after the single Task 1 commit, subject
  `docs(research): refresh workspace and SDLC references`. The immutable head
  hash is recorded in the implementer report because a commit cannot contain
  its own final hash.
- Implementer spec-compliance self-review: **PASS** — exact category/document
  table columns,
  25 requested categories, required lifecycle flow, 7 transitions, 19 document
  roles, 15 required source records, retrieval dates, and caveats are present.
- Implementer document-quality self-review: **PASS** — template headings,
  relative links,
  English stage language, evidence/policy boundaries, ownership, and source
  caveats are explicit.
- Review method: structured implementer self-review; the task brief prohibited
  subagents. Critical findings: none. One Important broken link to
  `./model-selection.md` was fixed to `./agent-model-selection.md`, then the
  repository-contract gate passed. The matching non-link filename was corrected
  during diff review. Remaining Minor findings: none.
- Initial independent review of `6136c57d`: **Spec Compliance: FAIL** and
  **Document Quality: CHANGES_REQUESTED**. Findings I-1 through I-3 and M-1
  are addressed in a separate review-fix commit.
- Independent re-review verdict: **Pending**. The controller will run the
  re-review and owns the final `Done` transition.
- Review-fix range: `6136c57da53a6562cf73600d86d7fc1b159b4879..HEAD`
  evaluated immediately after the review-fix commit; its immutable head hash
  is recorded in the implementer report.

## Task Review Evidence Contract

For each task, record:

- task-brief path;
- implementer report path;
- base and head commits;
- covering commands and summarized results;
- spec-compliance verdict;
- document-quality verdict;
- fixed Critical/Important findings and re-review outcome;
- remaining Minor findings for final review.

## Verification Summary

The implementation records final results for:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-repo-contracts.sh
```

Plan-authoring checks are recorded in the current progress entry and commit;
task-specific results are added here during execution.

## Deviation Notes

No implementation deviation exists at plan creation. Any later deviation must
name the affected task, plan requirement, reason, approval or evidence owner,
verification impact, and final disposition.

For `T-ARC-001`, no plan or content-scope deviation occurred. The broader
bootstrap progress-log update was not made because the task brief restricted
mutation to the four named documentation targets; the required implementer
report is the explicit out-of-band task artifact. Graphify refresh was not
required because no code file changed. No active policy, runtime, CI, template,
script, provider/model configuration, remote state, or unrelated document was
modified.

## Related Documents

- **Parent Spec**:
  [Agentic Research Pack Consolidation](../../03.specs/122-agentic-research-pack-consolidation/spec.md)
- **Parent Plan**:
  [Agentic Research Pack Consolidation Plan](../plans/2026-07-10-agentic-research-pack-consolidation.md)
- **Previous Task Evidence**:
  [Agentic Research Pack Refresh](./2026-07-05-agentic-research-pack-refresh.md)
- **Canonical Research Pack**:
  [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Research Category**:
  [Research References](../../90.references/research/README.md)
