---
status: active
---

<!-- Target: docs/90.references/audits/document-contracts/README.md -->

# Document Contract Audit References

> durable audit reports for workspace document contracts and automation coverage

## Overview

This folder stores reusable audit reports for repository documentation
contracts. It supports active execution evidence in
`docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
without replacing that task evidence.

## Category Role

`docs/90.references/audits/document-contracts` holds document-contract audit
reports as stable reference material. It may store inventories, comparison
matrices, automation coverage maps, and gap summaries, but it is not an
approval gate, active policy source, runtime source of truth, or replacement
for Stage 04 task evidence.

## Audience

This README is for:

- Documentation Specialists
- Agentic Workflow Specialists
- QA Engineers
- Repository Maintainers

## Scope

### In Scope

- Frontmatter, section, and README profile inventories.
- Governance, template, root shim, provider, workflow, and validator comparison.
- CI/CD, QA, and automation coverage mapping.
- Gap disposition records and future implementation batch proposals.

### Out of Scope

- Runtime configuration changes.
- Secret values, credentials, tokens, certificates, private keys, shell history, raw logs, and `.env` values.
- Active task evidence that belongs in `docs/04.execution/tasks/`.
- Historical evidence rewriting.

## Structure

- `README.md`
- `frontmatter-inventory.md`
- `frontmatter-routing-profile.md`
- `section-profile-inventory.md`
- `readme-profile-inventory.md`
- `contract-governance-map.md`
- `template-application-gaps.md`
- `automation-coverage-map.md`
- `gap-register.md`

## Planned References

- `frontmatter-inventory.md`
- `frontmatter-routing-profile.md`
- `section-profile-inventory.md`
- `readme-profile-inventory.md`
- `contract-governance-map.md`
- `template-application-gaps.md`
- `automation-coverage-map.md`
- `gap-register.md`

## How to Work in This Area

1. Keep reports source-attributed with command or file evidence.
2. Classify gaps before proposing edits.
3. Record out-of-scope infra, runtime, secret, remote, and historical-evidence gaps without patching them.
4. Update this README when audit report files are added, renamed, or removed.
5. Refresh the LLM Wiki index after changing tracked report files.

## Related Documents

- Audit references: `docs/90.references/audits/README.md`
- Workspace document contract audit pack spec: `docs/03.specs/workspace-document-contract-audit-pack/spec.md`
- Workspace document contract audit pack plan: `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md`
- Workspace document contract audit pack task: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Template contract: `docs/99.templates/support/template-contract.md`
- Frontmatter contract: `docs/99.templates/support/frontmatter-contract.md`
