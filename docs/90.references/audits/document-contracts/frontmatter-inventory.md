---
status: active
---

<!-- Target: docs/90.references/audits/document-contracts/frontmatter-inventory.md -->

# Frontmatter Inventory

## Overview

This inventory records the tracked Markdown frontmatter baseline for the
workspace document contract audit pack. It uses repository-local commands only
and records evidence for later gap registration without editing the target
document corpus.

## Scope

In scope: tracked Markdown files, tracked README files, top YAML frontmatter key
distribution, representative example paths, and duplicate-purpose key signals
defined by the frontmatter contract.

Out of scope: normalizing historical documents, editing operations documents,
reading secret values, or changing template contracts.

## Method

| Evidence ID | Command | Measured Purpose |
| --- | --- | --- |
| FM-001 | `git ls-files '*.md' \| wc -l` | Count tracked Markdown documents. |
| FM-002 | `git ls-files '*README.md' \| wc -l` | Count tracked README documents. |
| FM-003 | `git ls-files '*.md' \| rg -n '(^\|/)README\.md$'` | List tracked README surfaces and path categories. |
| FM-004 | `python3 - <<'PY' ... print(f"{key}\t{count}\t{', '.join(examples[key])}") ... PY` | Count top-frontmatter keys, missing frontmatter, unterminated fences, and example paths. |
| FM-005 | `rg -n '^type:\|^owner:\|^links:\|^document_type:\|^template_type:\|^updated:' --glob '*.md'` | Check explicit duplicate-purpose or legacy metadata keys from the frontmatter contract. |

## Findings

| Evidence | Measurement | Representative Paths | Disposition |
| --- | --- | --- | --- |
| Tracked Markdown baseline | 927 tracked Markdown files | `README.md`, `docs/00.agent-governance/README.md`, `infra/README.md` | historical-evidence |
| Tracked README baseline | 206 tracked README files | `.agents/README.md`, `.codex/README.md`, `docs/98.archive/README.md`, `tests/README.md` | historical-evidence |
| README surface coverage | README list includes root, docs, infra, projects, tests, examples, provider, and archive surfaces | `README.md`, `docs/README.md`, `infra/README.md`, `projects/README.md`, `examples/sample-web-service/README.md`, `docs/98.archive/README.md` | no-action |
| Frontmatter coverage | 742 Markdown files have top frontmatter; 185 have no top frontmatter; 0 unterminated fences were found | Missing-frontmatter examples: `.agents/README.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/SECURITY.md`, `.github/rulesets/main-protection.md`, `CHANGELOG.md` | batch-fix |
| Dominant lifecycle and layer keys | `status` appears 516 times; `layer` appears 176 times | `docs/01.requirements/2026-03-26-01-gateway.md`, `docs/00.agent-governance/rules/agentic.md` | no-action |
| Provider and hook metadata keys | `name` 79, `description` 60, `model` 30, `action` 19, `enabled` 19, `event` 19 | `.claude/agents/code-reviewer.md`, `docs/00.agent-governance/rules/hooks/hookify.block-gha-secrets-in-run.md` | no-action |
| Archive and generated metadata | Archive keys each appear 15 times; `generated_by` appears once | `docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md`, `docs/90.references/llm-wiki/llm-wiki-index.md` | no-action |
| Removed duplicate-purpose keys | `type`, `owner`, `links`, `document_type`, and `template_type` each appear 0 times in top frontmatter | Full tracked Markdown corpus | no-action |
| Legacy `updated` metadata | `updated` appears 3 times | `docs/05.operations/guides/06-observability/loki.md`, `docs/05.operations/policies/06-observability/01.retention.md`, `docs/05.operations/policies/06-observability/loki.md` | batch-fix |

## Gaps For Register

| Gap Candidate | Evidence | Disposition | Register Handling |
| --- | --- | --- | --- |
| Profile-specific review needed for files with no top frontmatter | 185 tracked Markdown files report `(none)`, including provider, GitHub, changelog, and other non-stage surfaces | batch-fix | Add to the final register as a profile-routing batch, not as a direct corpus rewrite. |
| Explicit legacy `updated` frontmatter remains in Stage 05 observability documents | The duplicate-purpose key scan found 3 `updated` keys under `docs/05.operations/**/06-observability/` | batch-fix | Record for a future bounded operations metadata cleanup if the target profile does not consume `updated`. |
| Non-standard Stage 05 operational metadata needs a contract decision | `component`, `runtime_state`, and `tier` each appear 3 times; `policy_state` appears once | out-of-scope-gap | Defer to later contract comparison because Task 2 is inventory-only. |
| Previously problematic role keys are absent | `type`, `owner`, `links`, `document_type`, and `template_type` are all 0 | no-action | Keep as closure evidence in the audit register. |

## Related Documents

- [Document contract audit references](./README.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md)
- [Template selection](../../../99.templates/support/template-selection.md)
- [Reference template](../../../99.templates/templates/common/reference.template.md)
