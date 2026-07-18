---
status: active
artifact_id: reference:agentic-research:document-metadata-lifecycle
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-07-13
review_cycle: on-source-change
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md -->

# Reference: Document Metadata and Lifecycle Criteria

## Overview

This reference defines source-backed criteria for document identity, typed
metadata, relations, lifecycle evidence, freshness, numbering, README and
generated-document exceptions, and semantic validation. It supplies the
criterion vocabulary for the Spec 123 audit and later metadata implementation;
it does not itself activate a schema or change document status.

## Purpose

Give Tasks 4, 7, and 8 one canonical criteria owner so syntax, lifecycle
meaning, document roles, and generator ownership are not conflated.

## Repository Role

Stage 00 and Stage 99 remain authoritative for current authoring and metadata
policy. [SDLC document roles](./sdlc-document-roles.md) owns artifact purpose;
this reference owns metadata/lifecycle comparison criteria. Audit rows must map
these criteria into Spec 123's implementation state, enforcement depth,
disposition, owner, verification, and confidence fields.

## Scope

### In Scope

- Artifact identity, type profiles, direct parent relations, and supersession
- Review freshness, numbering, lifecycle transitions, and reverse-transition evidence
- README exceptions, generated-document ownership, and semantic validation

### Out of Scope

- Enabling the proposed metadata keys or changing current lifecycle states
- Replacing human-readable `Related Documents` with metadata
- Reclassifying or rewriting the historical corpus

## Definitions / Facts

- **Artifact identity** is stable across path or title changes.
- **Type profile** states which keys are required, optional, forbidden, or not
  applicable for one artifact type; the umbrella key list is not a universal requirement.
- **Lifecycle evidence** is evidence of a state change, not merely a valid status word.
- **Freshness** is an evidence-backed review claim, not a filesystem mtime.
- **Generated document ownership** belongs to the generator and its freshness
  contract; hand edits do not establish current truth.
- **Consumer-specific metadata** exists only when a declared consumer assigns a
  type and purpose to a field; visual consistency is not a consumer.
- **Deterministic serialization** stabilizes authored and generated diffs. YAML
  mapping-key order is not semantic priority, and direct-parent array order
  does not rank relations.

## Criteria

| Criterion ID | Practice | Primary source | Workspace applicability | Required evidence | Potential owner |
| --- | --- | --- | --- | --- | --- |
| DML-01 | Give every migrated leaf artifact a stable identifier independent of path and heading. | DCMI `identifier`; Spec 123 typed metadata | Apply to typed/migrated leaves while retaining current numbering as a separate human-navigation concern; historical migration remains separately approved. | Unique `artifact_id`; deterministic manifest resolution; rename test | Stage 99 metadata profiles |
| DML-02 | Apply metadata through artifact-type profiles instead of one universal key set. | DCMI application-profile model; GitHub Docs consumer-specific frontmatter; JSON Schema conditional validation | Implemented for typed and safely selected changed/new enforcement; the full historical inventory remains advisory. | Registry profiles; profile tests; explicit N/A cases | Stage 99 metadata profiles |
| DML-03 | Record only direct upstream artifact IDs as parents, allowing multiple parents and deterministic serialization without priority. | DCMI `relation`, `isPartOf`, and `requires`; YAML 1.2.2 mapping/sequence model; Spec 129 parent contract | Complements, but does not duplicate, `Related Documents`. | Resolvable `parent_ids`; permitted-root rule; missing/cycle diagnostics; stable serialization test | Metadata validator and stage owners |
| DML-04 | Express replacement explicitly and preserve the direction of supersession. | DCMI `replaces` / `isReplacedBy`; W3C PROV `wasRevisionOf` | Use `supersedes` only when replacement evidence exists; a superseded body points to the current replacement. | Resolvable replacement ID; old/new status evidence; replacement link | Stage owner plus Stage 04 task |
| DML-05 | Treat `reviewed_at` and `review_cycle` as type-dependent freshness evidence. | DCMI `modified` and `valid`; Spec 123 typed metadata | Appropriate for freshness-managed policy, runbook, reference, and similar profiles, not every document. | Review result, date, cadence, reviewer/approval evidence in canonical body or task | Artifact owner |
| DML-06 | Keep human numbering schemes type-specific and separate from lifecycle identity. | Workspace documentation protocol; Nygard ADR practice | Preserve three-digit PRD/Spec IDs, four-digit ARD/ADR IDs, dated Plan/Task names, and domain tier numbers. | Path/title conformance; reserved-number check; unique artifact ID | Documentation protocol owner |
| DML-07 | Enforce only registry-declared forward transitions within the approved rollout boundary. | Spec 123 lifecycle state machine; Stage 99 registry | Terminal and archive semantics remain profile-specific rather than inferred from prose. | Before/after status, task evidence, replacement when required | Stage 99 lifecycle contract |
| DML-08 | Require approval, reason, and validator override for reverse transitions. | Spec 123 lifecycle state machine | Prevents a valid vocabulary value from hiding an invalid historical transition. | Stage 04 task, approval source, reason, previous state, override test | Stage 04 task owner |
| DML-09 | Derive README role from path, heading, and folder-index profile unless a real consumer requires metadata. | GitHub Docs audience/content-type guidance; Stage 99 README profile contract | README files are explicit exceptions to leaf-document lifecycle metadata; copied `status: draft` is not valid evidence. | Exactly one README profile match; heading envelope; consumer evidence for any metadata exception | Documentation protocol owner |
| DML-10 | Keep generated metadata and content generator-owned. | W3C PROV generation/provenance terms; Stage 99 frontmatter contract | Use `generated_by` or other generator-owned fields only when emitted by the generator; do not add human lifecycle keys to unprofiled outputs. | Reproducible generator command; freshness check; clean regenerated diff | Generator/script owner |
| DML-11 | Validate semantic relations and transitions in addition to YAML syntax and vocabulary. | JSON Schema conditional/dependent validation; Spec 123 guardrails | Structural parsing alone cannot prove parent resolution, permitted roots, transition history, or replacement coherence. | Parser/profile tests; ID manifest; transition fixtures; deterministic inventory | Metadata validator owner |
| DML-12 | Keep incident, postmortem, runbook, and release records as distinct type profiles. | Google SRE incident/postmortem chapters; PagerDuty runbook; Keep a Changelog; SemVer | Their document roles are canonical in `sdlc-document-roles.md`; metadata may differ because live state, reviewed learning, procedure, and release communication differ. | Type inference test; mapped template/path; role-specific parent and freshness rules | Stage 05 and release owners |
| DML-13 | Make audit criteria stable and preserve row-level evidence rather than a composite score. | Spec 123 Audit Criterion Record | Tasks 4-6 consume these IDs and add implementation state, depth, disposition, evidence, verification, and confidence. | Complete criterion rows linked to tracked evidence | Canonical audit pack owner |
| DML-14 | Roll out advisory-first and block only safely selected changed/new documents after false-positive review. | Spec 123 Metadata Rollout; GitHub required-check and ruleset guidance | Historical corpus cleanup is not authorized by schema introduction, and a tracked check is not remote enforcement. | Advisory inventory; exception review; changed/new tests; tracked CI evidence; separate approval for corpus-wide or remote blocking | Metadata program owner |

## Current Claim Inventory

| Finding | Tracked evidence | Disposition for later tasks |
| --- | --- | --- |
| Current rules enforce a status vocabulary but do not record transition history. | `documentation-protocol.md`, `lifecycle-status.md`, repository contracts | DML-07/DML-08 become semantic validator criteria. |
| Current path-derived roles conflict with the proposed need for stable cross-path identity only if `artifact_type` is treated as duplicate generic `type`. | `frontmatter-contract.md`; Spec 123 typed metadata | Keep generic `type` forbidden; introduce only the profiled `artifact_type`. |
| README profiles and generated outputs are intentional exceptions to ordinary leaf metadata. | `frontmatter-contract.md`; generator scripts | Preserve explicit DML-09/DML-10 profiles rather than normalizing them. |
| Existing numbering schemes differ by artifact family and cannot serve as cross-stage parent keys. | `documentation-protocol.md`; stage templates | Preserve numbering and resolve relations through `artifact_id`. |
| Review freshness and reverse-transition evidence are enforced only for the implemented typed/selected boundary; historical inventory findings remain advisory. | Stage 99 registry and metadata checker; Spec 123 | Preserve the staged boundary and require separate approval before broader blocking. |
| The current registry separates SDLC/common families, README profiles, and deterministic key/parent serialization. | `document-metadata-profiles.yaml`; Spec 129 Task 1 tests | Keep the registry as sole machine owner and link human contracts rather than copying arrays or validator logic. |
| README classification is implemented without bulk README mutation. | Registry profile globs and metadata checker tests | Preserve default-absent frontmatter; require a declared consumer for any allowed exception. |

## 2026-07-13 Canonicalization Analysis

YAML 1.2.2 distinguishes ordered sequences from unordered mappings and requires
serialization to impose presentation details. That supports stable key and
parent serialization for reviewable diffs, but it does not assign meaning to a
mapping's displayed order. GitHub Docs likewise documents frontmatter values by
the consuming site behavior, type, and requirement rather than proposing one
universal Markdown metadata set. The repository therefore keeps typed,
consumer-specific profiles in one registry and keeps Markdown body parsing
separate from frontmatter preprocessing.

Enforcement remains staged: inventory reporting preserves historical deficits;
the safely selected changed/new boundary can block known semantic errors; CI
can execute that local contract; and GitHub branch protection or rulesets are a
separate remote configuration that must be directly observed before claiming
merge enforcement. None of these layers authorizes a bulk historical rewrite.

## Source Rules

- External sources were revalidated on **2026-07-11**. YAML, GitHub
  frontmatter/content guidance, Diataxis, CommonMark/GFM, and GitHub enforcement
  and environment sources were re-opened on **2026-07-13** for this in-place
  canonicalization; the earlier retrieval record remains historical evidence.
- The exact official GitHub rulesets URL was re-opened again on **2026-07-19**;
  no stale claim was confirmed. The other standards and lower-risk sources keep
  their earlier retrieval dates. A passing tracked metadata check remains local
  evidence and is not proof that a remote ruleset requires it.
- DCMI 2020, W3C PROV-O, RFC 8288, and fixed standard/version pages provide
  stable vocabulary or provenance concepts; they do not define this repository's schema.
- Mutable official pages prove retrieval-time guidance only. ISO public pages
  expose metadata and summaries, not full standards text.
- Repo-local applicability is based on tracked files at task baseline
  `84d88ee48085304ad5aa3adce0a9e74b574758b0`; the Graphify report is older and advisory.

## Sources

- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) - identifier, type, relation, modified, valid, version, and replacement vocabulary
- [DCMI Usage Board Review of Application Profiles](https://www.dublincore.org/specifications/dublin-core/application-profile-review/) - official definition of an application profile as a declaration of reused terms with purpose-specific constraints, encoding, and interpretation
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) - generation, invalidation, provenance, and revision relations
- [RFC 8288 Web Linking](https://www.rfc-editor.org/rfc/rfc8288) - explicit relation semantics and registered/extension relation distinction
- [JSON Schema conditional validation](https://json-schema.org/understanding-json-schema/reference/conditionals) - type/profile-dependent requirements
- [YAML 1.2.2](https://yaml.org/spec/1.2.2/) - scalar, sequence, mapping, and serialization semantics
- [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) - consumer-specific fields, types, requirements, and schema validation
- [GitHub Docs content best practices](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs) - audience, purpose, content type, and scannable structure
- [Diataxis](https://diataxis.fr/) - separation of tutorials, how-to guidance, reference, and explanation
- [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) and [GitHub Flavored Markdown](https://github.github.com/gfm/) - Markdown body syntax and GitHub extensions, separate from frontmatter processing
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) and [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) - remote rule and required-check enforcement boundary
- [Michael Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - original ADR record practice
- [Google SRE incident management](https://sre.google/sre-book/managing-incidents/) - live incident state and handoff
- [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) - reviewed learning and action ownership
- [PagerDuty runbook overview](https://www.pagerduty.com/resources/automation/learn/what-is-a-runbook/) - repeatable operations procedure
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) - human-readable release communication
- [Semantic Versioning 2.0.0](https://semver.org/) - public API version signal
- [Spec 123](../../../03.specs/123-agentic-engineering-audit-remediation/spec.md) - approved metadata keys, audit fields, transition state machine, numbering, and rollout
- [Spec 129](../../../03.specs/129-document-contract-canonicalization/spec.md) - canonical families, README profiles, parent serialization, Release, and staged foundation scope
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - current workspace metadata ownership and exceptions
- [Lifecycle status](../../../99.templates/support/lifecycle-status.md) - current status meanings
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - current numbering, templates, and routing
- [Document metadata profiles](../../../99.templates/support/document-metadata-profiles.yaml) - sole machine-readable profile and serialization owner
- [README profile contract](../../../99.templates/support/readme-profile-contract.md) - human README selection and consumer boundary

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Spec 123 metadata implementation, Stage 99 contracts, or cited primary sources change
- **Update Trigger**: Profile, identifier, relation, lifecycle, README, generator, or validation semantics change

## Related Documents

- [research pack index](./README.md)
- [SDLC document roles](./sdlc-document-roles.md)
- [spec-driven SDLC](./spec-driven-sdlc.md)
- [agent instructions and vibe coding](./agent-instructions-vibe-coding.md)
