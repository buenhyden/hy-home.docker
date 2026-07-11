---
layer: agentic
---

# Lifecycle Status

## Overview

This document defines status values used by template sources, active stage
documents, archive tombstones, and generated files.

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

The typed profile contract records the default forward transitions separately
from the status vocabulary:

```text
draft -> active -> completed
                -> superseded
completed      -> superseded
```

`superseded` is terminal for active-stage artifacts and `archived` is terminal
for Stage 98 tombstones. A same-status edit is not a transition. Any reverse or
otherwise unlisted transition requires an explicit override manifest containing
the document path, previous and new states, existing Stage 04 task path,
approval, and reason. The validator accepts that manifest only through the
scoped `--transition-override-file` input; the default pre-push hook supplies no
override. Changed/new enforcement therefore blocks undocumented reverse
transitions while the full historical inventory remains advisory.

## Related Documents

- [support README](./README.md)
- [frontmatter contract](./frontmatter-contract.md)
- [document metadata profiles](./document-metadata-profiles.yaml)
- [template governance](./template-governance.md)
