---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md -->

# Template Application Gaps

## Overview

This report classifies stale template-path guidance and broad Stage 99 template
references found during Task 3. It records application gaps without editing the
matched files.

## Evidence Snapshot Boundary

- **Evidence as of**: 2026-07-03
- **Current implementation route**: [canonical agentic implementation audit](../2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Citation rule**: Preserve the counts, findings, commands, and dispositions below as dated evidence. Do not cite them as the current workspace state without current tracked-source revalidation.

## Purpose

This reference preserves the Task 3 template-application evidence needed for
the final gap register. It distinguishes active drift from broad catalog
references, template-time instructions, historical records, generated artifacts,
and out-of-scope examples.

## Repository Role

This report supports Stage 04 task evidence and future remediation planning. It
does not define the template contract; the active contract remains in
`docs/99.templates/support/` and Stage 00 governance.

## Scope

In scope: matches from root shims, provider surfaces, Stage 00 governance,
Stage 99 templates/support files, active docs, infra/project/script/secret/test
README surfaces, examples, GitHub docs, and generated LLM Wiki references.

Out of scope: editing matched files, reading secret values, normalizing
historical plans/tasks/specs, changing provider runtime behavior, or resolving
non-template taxonomy drift in this task.

## Definitions / Facts

- **Flat template path**: a removed path such as
  `docs/99.templates/readme.template.md` or
  `docs/99.templates/service.template.md`.
- **Canonical nested template path**: a current path under
  `docs/99.templates/templates/`.
- **Broad catalog reference**: a reference to `docs/99.templates/` as a folder
  or template system, without naming a removed flat file.
- **Template-time instruction**: text inside a template source warning users to
  recalculate target-relative links after copying.
- **Approved dispositions**: `direct-fix`, `batch-fix`,
  `historical-evidence`, `out-of-scope-gap`, and `no-action`.

## Method

| Evidence ID | Command | Result Summary | Use |
| --- | --- | --- | --- |
| TAG-001 | `rg -n 'docs/99\.templates/(readme\|service\|runbook\|incident\|postmortem\|plan\|task\|spec\|adr\|prd\|ard)\.template\|type:\|owner:\|updated:\|document_type:\|template_type:' AGENTS.md CLAUDE.md GEMINI.md README.md .agents .claude .codex docs/00.agent-governance docs/99.templates` | 8 regex matches across 4 files; no active flat-template path guidance in those surfaces. | Checked root/provider/governance/template surfaces for actionable drift. |
| TAG-002 | `rg -n --pcre2 'docs/99\.templates/(?!templates/\|support/)\|Use templates from docs/99\.templates\|Read the matching template from docs/99\.templates\|load the mapped template from docs/99\.templates' AGENTS.md CLAUDE.md GEMINI.md README.md docs archive examples infra projects scripts secrets tests .agents .claude .codex .github` | 200 matches across 113 files. | Classified target-surface matches. |
| TAG-003 | `rg -n --pcre2 'docs/99\.templates/(readme\|service\|runbook\|incident\|postmortem\|plan\|task\|spec\|adr\|prd\|ard)\.template' ...` | 8 matching lines across 6 live files; two lines contain both link label and target, yielding 10 regex matches. | Identified concrete flat-template path application gaps. |
| TAG-004 | `rg -n 'frontmatter\|template\|README\|governance\|contract\|policy\|rule\|validation\|validator\|CI\|QA\|Formatting\|formatting\|SDLC' ...` | 5,830 matches across 177 files. | Provided governance-owner context; summarized in `contract-governance-map.md`. |
| TAG-005 | Targeted context reads around each concrete flat-template path. | Confirmed matched files were README/example docs, not secret values. | Classified active, historical, and out-of-scope rows. |

## Active Guidance Drift

| Surface | Evidence | Classification | Disposition | Register Handling |
| --- | --- | --- | --- | --- |
| Project README flat README template path | `projects/README.md:46` tells README updates to follow `../docs/99.templates/readme.template.md`; `projects/README.md:53` repeats the flat link in Related References. | active guidance drift | batch-fix | Include in a project README/template-link cleanup batch with README profile review. |
| Storybook project README flat README template path | `projects/storybook/README.md:67` links to `../../docs/99.templates/readme.template.md`. | active guidance drift | batch-fix | Include with project README template-link cleanup. |
| Storybook Next.js README flat README template path | `projects/storybook/nextjs/README.md:79` links to `../../../docs/99.templates/readme.template.md`. | active guidance drift | batch-fix | Include with project README template-link cleanup. |
| Secret-handling README flat README template path | `secrets/README.md:127` links to `../docs/99.templates/readme.template.md`. | active guidance drift | batch-fix | Fix in a redaction-safe README metadata/link batch; do not read secret values. |

## Broad References With No Action

| Surface | Evidence | Classification | Disposition | Notes |
| --- | --- | --- | --- | --- |
| Root README Stage 99 references | Root `README.md` has 5 Task 3 scan matches, including broad catalog references and current nested `readme.template.md` guidance. | broad catalog reference | no-action | The broad folder reference is allowed by the audit spec when it does not name a removed flat file. |
| Stage 00 governance and provider surfaces | `docs/00.agent-governance`, `.agents`, `.claude`, and `.codex` contain 148 `docs/99.templates/` matches across 39 files. | broad catalog reference | no-action | Most active guidance maps to nested templates or to Stage 99 as the shared template system. |
| Infra README surfaces | `infra/**` contains 18 broad `docs/99.templates/` matches across 18 files. | broad catalog reference | no-action | The lines refer to corresponding templates without naming removed flat files. |
| Stage 99 template-time source text | Template files under `docs/99.templates/templates/**` warn that target-relative links must be recalculated from copied targets, not from `docs/99.templates/`. | template-time instruction | no-action | This is required template guidance, not target-document drift. |
| Generated LLM Wiki index | `docs/90.references/llm-wiki/llm-wiki-index.md` includes `docs/99.templates/README.md` as a generated path entry. | generated artifact | no-action | Regeneration owns this entry; do not hand-edit generated index content. |
| Repository validators | `scripts/validation/check-repo-contracts.sh` references `docs/99.templates/$template` while the required template array contains nested `templates/...` paths. | validator-owned reference | no-action | The resolved paths are current nested template paths. |

## Historical Evidence

| Surface | Evidence | Classification | Disposition | Notes |
| --- | --- | --- | --- | --- |
| Template reorganization plans and tasks | `docs/04.execution/plans/2026-07-02-template-system-reorganization.md` records the move from flat `docs/99.templates/*.template.*` to nested `templates/` and `support/` paths. | historical evidence | historical-evidence | Keep as migration evidence. |
| Older workspace consistency specs/plans | `docs/03.specs/092-workspace-consistency-2026-05b/spec.md`, `docs/03.specs/091-workspace-doc-consistency-2026-05/spec.md`, and older Stage 04 plans mention `docs/99.templates/*.template.md` baselines. | historical evidence | historical-evidence | Do not rewrite completed historical design evidence for style only. |
| Governance progress log | `docs/00.agent-governance/memory/progress.md` records prior template standardization and old-path cleanup work. | historical evidence | historical-evidence | Memory is advisory progress context, not active template policy. |
| Prior execution tasks | Older `docs/04.execution/tasks/**` entries mention template list or old template paths as completed work evidence. | historical evidence | historical-evidence | Preserve unless a future task proves an entry is active guidance consumed today. |

## Out-of-Scope Gaps

| Surface | Evidence | Classification | Disposition | Register Handling |
| --- | --- | --- | --- | --- |
| Example scaffold service template path | `examples/sample-web-service/README.md:61` and `examples/sample-web-service/service.md:3,56` point to `docs/99.templates/service.template.md`. | out-of-scope gap | out-of-scope-gap | Carry forward as an examples-surface decision; Task 2 already classified example README profile drift as out of scope. |
| Non-template stale taxonomy found in matched project README context | `projects/README.md:47` repeats a removed operations-stage path literal. | out-of-scope gap | out-of-scope-gap | Record for a later taxonomy cleanup; this task is limited to template application and governance comparison. |
| Legacy Stage 05 `updated` metadata from Task 2 | `docs/05.operations/guides/06-observability/loki.md:7`, `docs/05.operations/policies/06-observability/01.retention.md:7`, and `docs/05.operations/policies/06-observability/loki.md:7`. | out-of-scope gap | out-of-scope-gap | Keep in the final register as a frontmatter cleanup batch, not a Task 3 edit. |

## Gaps For Register

| Gap ID | Gap Candidate | Evidence | Disposition | Register Handling |
| --- | --- | --- | --- | --- |
| TAG-GAP-001 | Project README surfaces still link to removed flat README template paths. | `projects/README.md`, `projects/storybook/README.md`, and `projects/storybook/nextjs/README.md`. | batch-fix | Batch with the README profile gap from Task 2. |
| TAG-GAP-002 | Secret-handling README still links to removed flat README template path. | `secrets/README.md:127`. | batch-fix | Batch with redaction-safe README link cleanup; do not inspect secret values. |
| TAG-GAP-003 | Example scaffold still links to removed flat service template path. | `examples/sample-web-service/README.md` and `examples/sample-web-service/service.md`. | out-of-scope-gap | Defer until examples/scaffold contract is explicitly in scope. |
| TAG-GAP-004 | Historical docs preserve old template paths. | Older Stage 03/04 specs, plans, tasks, and progress entries. | historical-evidence | Keep as historical evidence unless a future task proves active consumption. |
| TAG-GAP-005 | Broad catalog references are valid and should not be normalized. | 200 Task 3 scan matches include many current broad references to Stage 99. | no-action | Record as closure evidence. |

## Sources

- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md) - Defines Task 3 scope and disposition rules.
- [Contract governance map](./contract-governance-map.md) - Summarizes ownership surfaces for the same scan set.
- [Template contract](../../../99.templates/support/template-contract.md) - Defines template source and target-document rules.
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - Defines duplicate-purpose metadata handling.
- [Template governance](../../../99.templates/support/template-governance.md) - Defines change boundaries.
- [Template selection](../../../99.templates/support/template-selection.md) - Defines canonical nested template paths.
- [Reference template](../../../99.templates/templates/common/reference.template.md) - Defines the required Stage 90 reference structure.
- [Root README](../../../../README.md) - Provides repository-wide broad template references and verification context.

## Maintenance

- **Owner**: Documentation Specialist / `doc-writer`.
- **Review Cadence**: Review when the final gap register is built or when
  template path validators change.
- **Update Trigger**: Update if a later task edits the classified target files,
  changes Stage 99 path policy, or regenerates the LLM Wiki index with new
  report paths.

## Related Documents

- [Document contract audit references](./README.md)
- [Contract governance map](./contract-governance-map.md)
- [Frontmatter inventory](./frontmatter-inventory.md)
- [Section profile inventory](./section-profile-inventory.md)
- [README profile inventory](./readme-profile-inventory.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
