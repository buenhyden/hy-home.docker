---
layer: agentic
---

# Lifecycle Status

## Overview

This document defines status values used by template sources, active stage
documents, archive tombstones, and generated files.

It owns the human meaning of the unchanged vocabulary only. Exact allowed
values by profile, transition edges, terminal behavior, and exception evidence
remain solely in the registry and checker.

## Status Vocabulary

| Status | Applies To | Meaning |
| --- | --- | --- |
| `draft` | Template sources and in-progress target docs | The document is not yet the accepted current truth for its target surface. |
| `active` | Current target docs | The document is current guidance, contract, reference, or working evidence. |
| `completed` | Finished execution artifacts and historical-but-valid records | The document records completed work and remains valid evidence until a later task archives or removes it. |
| `superseded` | Replaced active docs retained for transition or reference | The document has a current replacement and must point to it while it remains in the active chain. |
| `archived` | `docs/98.archive/**` tombstones | The original active document was removed from the active chain. |

## Archive-Centered Lifecycle Rules

- `completed` does not automatically mean archived. Completed specs, plans,
  tasks, and audit records may remain active evidence.
- `superseded` is a transitional lifecycle status for a document that still
  exists in the active chain and points to a replacement.
- `archived` is reserved for `docs/98.archive/**` tombstones after the original
  target leaves the active chain.
- A document restructure disposition such as `historical-archive`,
  `duplicate-remove`, `conflict-remove-or-archive`, or `evidence-preserve` is a
  task/audit decision, not a replacement for lifecycle `status`.
- Preserve `evidence-preserve` documents with their historical wording unless a
  future task proves active-consumption conflict.

## Generated Metadata

Generated files may use `generated_by` to identify the generator. Generated
metadata does not replace lifecycle `status` where a status is required by the
target stage.

## Status Selection Rules

- Template sources use `status: draft`.
- Stage 04 plans are `active` until completed, then `completed`.
- Stage 04 tasks are `active` while work is in progress, then `completed`.
- Replaced documents that remain in the active chain may use `superseded` only
  when the body points to a current replacement.
- Archive tombstones use `status: archived`.
- Do not mark a document `completed` merely because it is old.
- Do not mark a document `archived` outside `docs/98.archive/**`.

## Transition Validation

The exact transition graph, terminal-state behavior, exception evidence schema,
and enforcement rules belong only to
[`document-metadata-profiles.yaml`](./document-metadata-profiles.yaml) and the
executable
[`check-document-metadata.py`](../../../scripts/validation/check-document-metadata.py).
Do not infer or restate those semantics from this human vocabulary.

Before changing a status, the author and reviewer should confirm that the
document's real lifecycle evidence supports the proposed state, that historical
execution or decision evidence is preserved, and that any replacement is clear
to readers. If the checker rejects a transition, retain the current status and
route the evidence gap or requested exception through the active Stage 04 task.
Human prose, age, formatting cleanup, or a copied template never authorizes an
exception. Escalate ambiguity before mutation when the registry profile,
current evidence, and intended lifecycle outcome do not agree.

## Related Documents

- [support README](./README.md)
- [frontmatter contract](./frontmatter-contract.md)
- [document metadata profiles](./document-metadata-profiles.yaml)
- [metadata checker](../../../scripts/validation/check-document-metadata.py)
- [template governance](./template-governance.md)
