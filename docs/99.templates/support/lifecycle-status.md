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
| `completed` | Finished execution artifacts and historical-but-valid records | The document records completed work and remains valid evidence. |
| `superseded` | Replaced active docs | The document has a current replacement and should point to it. |
| `archived` | `docs/98.archive/**` tombstones | The original active document was removed from the active chain. |

## Generated Metadata

Generated files may use `generated_by` to identify the generator. Generated
metadata does not replace lifecycle `status` where a status is required by the
target stage.

## Status Selection Rules

- Template sources use `status: draft`.
- Stage 04 plans are `active` until completed, then `completed`.
- Stage 04 tasks are `active` while work is in progress, then `completed`.
- Archive tombstones use `status: archived`.
- Do not mark a document `completed` merely because it is old.

## Related Documents

- [support README](./README.md)
- [frontmatter contract](./frontmatter-contract.md)
- [template governance](./template-governance.md)
