---
layer: agentic
---

# Memory: Docker Documentation Contract Backlog

- Date: 2026-05-09
- Layer: docs
- Tags: #docker #documentation #quality

## Problem

The Docker documentation contract audit found that several `docs/04.specs/*`
feature folders do not have local README files. This is a documentation
navigability gap, but creating all missing README files in the current pass
would broaden a contract-repair change into a larger docs normalization sweep.

## Context

Missing README coverage was observed under:

- `docs/04.specs/01-gateway`
- `docs/04.specs/02-auth`
- `docs/04.specs/03-security`
- `docs/04.specs/04-data`
- `docs/04.specs/04-data-analytics`
- `docs/04.specs/05-messaging`
- `docs/04.specs/06-observability`
- `docs/04.specs/07-workflow`
- `docs/04.specs/08-ai`
- `docs/04.specs/09-tooling`
- `docs/04.specs/10-communication`
- `docs/04.specs/11-laboratory`
- `docs/04.specs/standardize-infra-net`

The current Docker contract repair focused on profile-aware Compose validation,
hardening script wrappers, stale top-level documentation links, and relocation
of non-active learning material into `docs/90.references/learning/`.

## Resolution

Defer scoped README generation for `docs/04.specs/*` as a follow-up backlog
item. The current implementation keeps the taxonomy intact and repairs broken
runtime/documentation contracts without expanding into broad docs consolidation.

## Prevention

When a stage subfolder is created or materially changed, update the nearest
stage README or add a local README in the same change. Future README generation
should be a separate docs pass with a clear template and folder-by-folder
ownership.

## Related Documents

- [Agent governance memory index](README.md)
- [Documentation stage matrix](../rules/stage-authoring-matrix.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Specs index](../../04.specs/README.md)
