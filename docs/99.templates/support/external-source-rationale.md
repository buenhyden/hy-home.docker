---
layer: agentic
---

# External Source Rationale

## Overview

This document records the external source rationale behind the local template
system. External sources inform the repository rules, but the repo-local
contracts remain canonical for this workspace.

## Source-Backed Decisions

| Source | Local Decision |
| --- | --- |
| [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) | Use CommonMark as the baseline Markdown syntax model. |
| [GitHub Flavored Markdown](https://github.github.com/gfm/) | Treat GFM as the GitHub rendering extension layer, not as a replacement for CommonMark. |
| [Jekyll front matter](https://jekyllrb.com/docs/front-matter/) | Treat YAML frontmatter as a top-of-file preprocessing convention. |
| [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) | Keep frontmatter fields schema-like and purpose-specific. |
| [GitHub Docs content best practices](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs) | Select a clear audience, purpose, and content type; keep headings and structure scannable. |
| [YAML 1.2.2](https://yaml.org/spec/1.2.2/) | Keep frontmatter JSON-compatible and avoid advanced YAML features in template metadata. |
| [JSON Schema](https://json-schema.org/specification) | Separate metadata validation concerns from Markdown body template shape. |
| [Diataxis](https://diataxis.fr/) | Use documentation-purpose distinctions when separating guides, references, explanations, and procedures. |
| [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) | Keep tracked check definitions separate from the remote rules that may require them. |
| [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | Treat required status checks as remote merge enforcement, not a property inferred from workflow YAML. |
| [GitHub deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) | Distinguish Release evidence from deployment environments, approvals, protected secrets, and promotion controls. |
| [The Good Docs Project templates](https://www.thegooddocsproject.dev/template) | Separate copyable template bodies from adoption and style guidance. |
| [NIST SSDF](https://csrc.nist.gov/projects/ssdf) | Keep security review and validation expectations integrated into SDLC template governance. |
| [Google developer documentation filename guidance](https://developers.google.com/style/filenames) | Use stable, lowercase, hyphenated path components for canonical documentation targets. |
| [Google developer documentation date guidance](https://developers.google.com/style/dates-times) | Keep dates as content or evidence when useful; do not use dates as the primary PRD routing key after numbered path migration. |
| [IEEE 1012-2024](https://standards.ieee.org/ieee/1012/7324/) | Preserve verification and validation traceability when path contracts change. |

## Local Interpretation

- Frontmatter is not CommonMark; parse and validate it before Markdown body
  handling.
- YAML mapping order is presentation, while the data model treats mappings as
  unordered; deterministic serialization must not create semantic priority.
- Frontmatter fields and README metadata are consumer-specific. Do not add a
  key without a declared local consumer and profile.
- Template bodies and metadata contracts are different surfaces and should not
  be governed from the same README paragraph.
- Diataxis informs purpose boundaries, but the repository lifecycle stages
  remain PRD, architecture, spec, execution, operations, reference, archive, and
  template stages.
- Security SDLC expectations appear in template governance and task evidence,
  not as runtime changes inside this template migration.
- Numbered PRD and Spec paths use stable routing identifiers while preserving
  dates in execution evidence, history notes, audit packs, or archive context.
- Path migrations must include verification evidence because they change how
  agents and humans resolve implementation contracts.

## Verification Record

The YAML 1.2.2, GitHub YAML frontmatter and content-practice pages, Diataxis,
CommonMark 0.31.2, GFM, GitHub ruleset/protected-branch guidance, and GitHub
deployment-environment guidance were re-opened on **2026-07-13**. Mutable pages
support retrieval-time rationale only. `diataxis.fr` returned HTTP 429 from the
verification environment, so its four-type model was corroborated against the
[official Diataxis source repository](https://github.com/evildmp/diataxis-documentation-framework)
whose homepage points to the cited site.

## Related Documents

- [support README](./README.md)
- [frontmatter contract](./frontmatter-contract.md)
- [template contract](./template-contract.md)
- [template governance](./template-governance.md)
- [SDLC document contract](./sdlc-document-contract.md)
- [common document contract](./common-document-contract.md)
- [README profile contract](./readme-profile-contract.md)
