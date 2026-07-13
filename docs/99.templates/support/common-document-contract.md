---
layer: agentic
---

# Common Document Contract

## Overview

This contract explains human authoring boundaries for common and repository
documentation. Exact metadata profiles, exception rules, path matching, value
types, and validation behavior belong only to
[`document-metadata-profiles.yaml`](./document-metadata-profiles.yaml).

README-specific profile selection is owned separately by
[`readme-profile-contract.md`](./readme-profile-contract.md).

## Common Roles

| Surface | Human purpose | Authority and lifecycle boundary |
| --- | --- | --- |
| Reference | Preserve stable, source-backed facts, vocabulary, inventory, research, or explanatory context. | Supports active work but does not become policy, procedure, execution evidence, or runtime truth. Mutable claims need review evidence and a source date. |
| Audit | Record a bounded assessment against explicit criteria, evidence, findings, severity, and disposition. | Reports observed state; it routes gaps to canonical owners and does not silently change those owners. Dated counts and verdicts remain historical evidence. |
| Archive | Preserve a concise tombstone for an active document removed from the current chain. | Records origin, reason, date, and current replacement; it does not retain stale current-truth prose or receive active back-links. |
| Governance | Define agent execution, authoring, approval, provider, or repository policy in its approved governance surface. | Uses governance metadata conventions and must not be projected into ordinary lifecycle artifacts or catalog README files. |
| Generated output | Present deterministic output owned by a named generator and freshness contract. | Regenerate through the canonical owner; do not hand-edit or add human lifecycle claims the generator does not emit. |
| Template source | Provide a copyable shape with target guidance and explicit placeholders. | Remains a source artifact under Stage 99; copied targets must resolve placeholders and select an honest target profile. |
| Repo-support | Define the narrow tracked support boundary or hold ignored, non-secret transient handoff material. | It is neither an active documentation stage nor a substitute for canonical task, review, or evidence artifacts. Promote durable outcomes to the owning stage. |
| Unsupported or native platform surface | Serve a tool-owned path whose consumer is outside the repository documentation model, such as a GitHub-native instruction or configuration surface. | Preserve the native consumer contract. Do not add repository metadata merely for visual uniformity; classify ambiguity before editing. |

## Ownership Rules

- Put reusable human rules in the named support contract, copyable form in a
  template, machine semantics in the registry, current policy in governance,
  and observed results in a Task, Audit, Incident, Postmortem, or Release as
  appropriate.
- A Reference or Audit may compare external guidance with repository evidence,
  but adoption requires an approved canonical owner outside Stage 90.
- Archive and deletion decisions require replacement and link review. Historical
  evidence is preserved in its evidence owner rather than restyled as current
  guidance.
- Generated and native platform surfaces are consumer-specific exceptions, not
  a reason to weaken fail-closed classification.
- Repo-support artifacts must not contain credentials, secret values, raw logs,
  auth material, or runtime state that belongs outside the tracked contract.

## Source and Evidence Discipline

- Use primary sources for normative external claims and record the access date.
- Distinguish a fixed standard from a mutable product page and a repository
  inference from an observed runtime or remote fact.
- Preserve dated commands, counts, verdicts, and results in audit and research
  evidence. Add current interpretation around them instead of rewriting their
  historical meaning.
- Link to the current canonical policy, runtime, or generator owner rather than
  presenting a support document as that owner.

## Ambiguity Handling

If a path could match more than one family or exception, stop classification
and consult the registry and current Stage 04 scope. Do not infer a profile from
frontmatter resemblance, create a new exception in prose, or convert a native
surface into a repository document without approval.

## Related Documents

- [document metadata profiles](./document-metadata-profiles.yaml)
- [SDLC document contract](./sdlc-document-contract.md)
- [README profile contract](./readme-profile-contract.md)
- [template governance](./template-governance.md)
- [frontmatter contract](./frontmatter-contract.md)
- [template contract](./template-contract.md)
