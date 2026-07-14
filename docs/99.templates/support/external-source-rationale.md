---
layer: agentic
---

# External Source Rationale

## Overview

This document records the external source rationale behind the local template
system. Only official standards pages, official product documentation, or the
primary project publication are cited. They inform local design; the registry
and repository contracts remain canonical for this workspace.

## Source-Backed Decisions

| Source | Local Decision |
| --- | --- |
| [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) | Supports separating an information item's purpose and content from the repository's chosen presentation and lifecycle controls. |
| [YAML 1.2.2](https://yaml.org/spec/1.2.2/) | Supports duplicate-key rejection and treating mapping order as presentation rather than semantic priority. |
| [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) | Supports consumer-specific frontmatter fields instead of one universal metadata set. |
| [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) and [GitHub Flavored Markdown](https://github.github.com/gfm/) | Support validating Markdown body structure independently from YAML frontmatter and using the repository's selected GFM-compatible presentation rules. |
| [Diataxis](https://diataxis.fr/) | Supports keeping learning, explanation, reference, and procedural purposes distinct; the repository maps those concerns to its local document roles. |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Informs traceable requirements, constraints, acceptance intent, and verification in the local PRD role. |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Informs stakeholder, concern, boundary, viewpoint, and architecture-description content in the local ARD role. |
| [MADR](https://adr.github.io/madr/) | Informs the local separation of decision context, options, outcome, consequences, and confirmation. |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Informs separation among specification, planning, tasks, implementation, and cross-artifact analysis. |
| [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html) | Supports treating lifecycle processes as tailorable and iterative rather than forcing a fixed waterfall. |
| [NASA SWE-052](https://swehb.nasa.gov/spaces/7150/pages/16450285/SWE-052%2B-%2BBidirectional%2BTraceability%2BBetween%2BHigher%2BLevel%2BRequirements%2Band%2BSoftware%2BRequirements) | Supports stable identities, bidirectional traceability, and change-impact review across requirement levels. |
| [ISO/IEC/IEEE 26514:2022](https://www.iso.org/standard/77451.html) and [Kubernetes page content types](https://kubernetes.io/docs/contribute/style/page-content-types/) | Inform purpose-based separation of user guidance, tasks, tutorials, and reference material. |
| [NIST security policy glossary](https://csrc.nist.gov/glossary/term/security_policy) | Informs the local Policy focus on required or prohibited controls and exception authority. |
| [Google SRE On-call](https://sre.google/workbook/on-call/) and [Emergency Response](https://sre.google/sre-book/emergency-response/) | Inform trigger, procedure, verification, recovery, escalation, and automation boundaries in Runbooks. |
| [NIST SP 800-61r3 announcement](https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations) | Supports keeping live Incident evidence distinct from later retrospective analysis. |
| [Google SRE Postmortem Culture](https://sre.google/workbook/postmortem-culture/) | Informs factual, blameless analysis and owned follow-up actions in Postmortems. |
| [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) | Supports treating a Release as evidence tied to an actual tag or commit and associated artifacts, not a readiness template. |
| [SLSA v1.2 provenance](https://slsa.dev/spec/v1.2/provenance) | Informs recording command, tool, commit, result, and evidence location without claiming SLSA conformance. |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Supports distinguishing original entities, derived records, activities, and responsible agents without treating a tombstone or preserved copy as current truth. |
| [Git log](https://git-scm.com/docs/git-log) | Supports using immutable commit and blob identities as the repository's default original-body provenance route. |
| [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | Supports event-driven tracked workflow definitions; this repository separately decides which local contracts are mandatory or advisory. |
| [pre-commit](https://pre-commit.com/) | Supports treating all-files hooks as repository-wide checks; the clean-worktree wrapper and observation boundary are local governance decisions. |

## Local Interpretation

- The repository's role names, numbered paths, status enum, profile schema,
  parent rules, and heading envelopes are local contracts, not international
  standards or claims of conformance.
- External sources justify conservative separation of concerns. They do not
  authorize invented metadata, review evidence, release events, or runtime
  facts.
- Deterministic frontmatter serialization stabilizes diffs but does not assign
  semantic priority.
- Thresholds, wave names, dispositions, path layouts, approval gates, wrapper
  requirements, and snapshot admission are repository-local decisions.
  External sources do not define repository approval authority.
- SLSA, NIST, ISO/IEC/IEEE, GitHub, Kubernetes, MADR, and Google SRE concepts
  are adapted only to the stated local boundary; this repository does not claim
  certification or conformance from these citations.

## Verification Record

The original template-system source set was re-opened from official or primary
publications on **2026-07-13**. Spec 131 approved the lifecycle source-to-local-
consequence additions recorded here on **2026-07-14**. ISO catalog pages verify
the cited edition and scope, not the paywalled full text. Mutable product and
project pages support retrieval-time rationale only; later changes do not
silently alter the local registry.

## Related Documents

- [support README](./README.md)
- [frontmatter contract](./frontmatter-contract.md)
- [template contract](./template-contract.md)
- [template governance](./template-governance.md)
- [SDLC document contract](./sdlc-document-contract.md)
- [common document contract](./common-document-contract.md)
- [README profile contract](./readme-profile-contract.md)
- [corpus migration contract](./corpus-migration-contract.md)
- [archive and retention contract](./archive-retention-contract.md)
