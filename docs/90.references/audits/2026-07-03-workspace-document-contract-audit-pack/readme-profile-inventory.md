---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md -->

# README Profile Inventory

## Overview

This inventory records tracked README surfaces and counts the expected README
profile headings named by the task prompt. It supports later contract
comparison without changing README content.

## Evidence Snapshot Boundary

- **Evidence as of**: 2026-07-03
- **Current implementation route**: [canonical agentic implementation audit](../2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Citation rule**: Preserve the counts, findings, commands, and dispositions below as dated evidence. Do not cite them as the current workspace state without current tracked-source revalidation.

## Purpose

This reference preserves the Task 2 README-profile measurements for the
workspace document contract audit pack. It gives later comparison and gap
registration tasks a stable baseline for README surface coverage.

## Repository Role

This report supports Stage 04 execution evidence and later Stage 90 audit
references. It is not an active README template, policy source, or approval to
rename README headings across the repository.

## Scope

In scope: tracked `*README.md` files, README path categories, expected profile
heading counts, score distribution, representative surfaces, and README profile
gap candidates.

Out of scope: rewriting README files, changing template-source READMEs, editing
provider runtime surfaces, or modifying secret material.

## Definitions / Facts

- **Tracked README file**: A path returned by `git ls-files '*README.md'`.
- **README profile heading**: One of the expected `##` headings counted by
  `RP-003`.
- **Score distribution**: The count of matched README profile headings per
  tracked README file.
- **Batch-fix disposition**: An observed issue that should be reviewed in a later
  scoped remediation task before any README content changes.

## Method

| Evidence ID | Command | Measured Purpose |
| --- | --- | --- |
| RP-001 | `git ls-files '*README.md' \| wc -l` | Count tracked README documents. |
| RP-002 | `git ls-files '*.md' \| rg -n '(^\|/)README\.md$'` | List tracked README paths and categories. |
| RP-003 | `git ls-files '*README.md' \| while read -r path; do printf '%s\t' "$path"; rg -n '^## (Overview\|Audience\|Scope\|Structure\|How to Work in This Area\|Related Documents\|Current References\|Documentation Standards\|Plan Contract)' "$path" \| sed 's/:.*//' \| wc -l; done` | Count expected profile headings per README. This pipeline was executed under Bash because zsh treats `path` as a special parameter. |

## Findings

| Evidence | Measurement | Representative Paths | Disposition |
| --- | --- | --- | --- |
| Tracked README baseline | 206 tracked README files | `README.md`, `docs/README.md`, `infra/README.md`, `tests/README.md` | historical-evidence |
| README path coverage | The README list includes root, provider, docs, infra, projects, scripts, secrets, tests, examples, and archive-stage surfaces | `.agents/README.md`, `.codex/README.md`, `docs/98.archive/README.md`, `examples/sample-web-service/README.md` | no-action |
| Expected-heading score distribution | Scores were: 1 heading in 2 files, 2 in 6 files, 3 in 1 file, 5 in 5 files, 6 in 169 files, 7 in 22 files, and 8 in 1 file | Distribution examples include `.codex/README.md`, `docs/99.templates/templates/README.md`, `infra/README.md`, `README.md`, `docs/04.execution/plans/README.md` | historical-evidence |
| Root and docs-stage README profiles | Root `README.md` scored 7; `docs/README.md` scored 7; stage roots such as `docs/01.requirements/README.md`, `docs/02.architecture/README.md`, `docs/03.specs/README.md`, and `docs/04.execution/README.md` scored 7 | `README.md`, `docs/README.md`, `docs/04.execution/README.md` | no-action |
| Governance README profiles | Governance READMEs scored 6 | `docs/00.agent-governance/README.md`, `docs/00.agent-governance/agents/README.md`, `docs/00.agent-governance/memory/README.md` | no-action |
| Infra README profiles | Infra folder and service README scores are mostly 6; one sampled service README scored 7 | `infra/README.md` 6, `infra/01-gateway/README.md` 6, `infra/01-gateway/nginx/README.md` 7, `infra/02-auth/keycloak/README.md` 6 | no-action |
| Scripts and archive README profiles | `scripts/README.md` scored 6 and `docs/98.archive/README.md` scored 6, with no direct Task 2 content fix identified | `scripts/README.md`, `docs/98.archive/README.md` | no-action |
| Projects, tests, and secrets README profiles | `secrets/README.md`, `projects/README.md`, and `tests/README.md` scored 5 because they use a related-reference profile instead of the counted related-documents profile | `secrets/README.md`, `projects/README.md`, `tests/README.md` | batch-fix |
| Example scaffold README profile | `examples/sample-web-service/README.md` scored 1 against the expected README heading set | `examples/sample-web-service/README.md` | out-of-scope-gap |
| Template-source README profiles | Template category READMEs scored 2 and use template-source catalog headings | `docs/99.templates/templates/README.md`, `docs/99.templates/templates/common/README.md`, `docs/99.templates/templates/sdlc/README.md` | no-action |

## Gaps For Register

| Gap Candidate | Evidence | Disposition | Register Handling |
| --- | --- | --- | --- |
| Projects, tests, and secrets READMEs use a related-reference profile instead of the counted related-documents profile | `projects/README.md`, `projects/storybook/README.md`, `projects/storybook/nextjs/README.md`, `secrets/README.md`, and `tests/README.md` each scored 5 | batch-fix | Add to the register for later README profile review before renaming any headings. |
| Example README has a scaffold-specific profile | `examples/sample-web-service/README.md` scored 1 against the expected README heading set | out-of-scope-gap | Record as an example-surface README profile decision for a later batch. |
| Provider README profiles are intentionally thinner than folder README profiles | `.codex/README.md` scored 1 and `.agents/README.md` scored 3 | no-action | Treat as provider-surface evidence unless the provider contract comparison in a later task changes the profile. |
| Template category READMEs use template-source headings | Six `docs/99.templates/templates/**/README.md` files scored 2 | no-action | Keep as template-source profile evidence for Task 3 contract comparison. |

## Sources

- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md) - Defines Task 2 scope and README baseline evidence.
- [Template selection](../../../99.templates/support/template-selection.md) - Supports profile routing for README comparison work.
- [README template](../../../99.templates/templates/common/readme.template.md) - Defines the common README section profile used for comparison.
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - Provides supporting metadata contract context for README profiles.
- [Reference template](../../../99.templates/templates/common/reference.template.md) - Defines the required Stage 90 reference structure.

## Maintenance

- **Owner**: Documentation Specialist / `doc-writer`.
- **Review Cadence**: Review when README contract comparisons or remediation
  batches are planned.
- **Update Trigger**: Rerun the inventory when tracked README membership,
  README template requirements, or Stage 90 reference template requirements
  change.

## Related Documents

- [Document contract audit references](./README.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
- [Template selection](../../../99.templates/support/template-selection.md)
- [README template](../../../99.templates/templates/common/readme.template.md)
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md)
