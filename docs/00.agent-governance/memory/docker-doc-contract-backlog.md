---
layer: agentic
---

# Memory: Docker Documentation Contract Backlog

- Date: 2026-05-09
- Layer: docs
- Tags: #docker #documentation #quality

## Problem

The Docker documentation contract audit found that several `docs/03.specs/*`
feature folders do not have local README files. This is a documentation
navigability gap, but creating all missing README files in the current pass
would broaden a contract-repair change into a larger docs normalization sweep.

## Context

Missing README coverage was observed under:

- `docs/03.specs/01-gateway`
- `docs/03.specs/02-auth`
- `docs/03.specs/03-security`
- `docs/03.specs/04-data`
- `docs/03.specs/04-data-analytics`
- `docs/03.specs/05-messaging`
- `docs/03.specs/06-observability`
- `docs/03.specs/07-workflow`
- `docs/03.specs/08-ai`
- `docs/03.specs/09-tooling`
- `docs/03.specs/10-communication`
- `docs/03.specs/11-laboratory`
- `docs/03.specs/standardize-infra-net`

The current Docker contract repair focused on profile-aware Compose validation,
hardening script wrappers, stale top-level documentation links, and relocation
of non-active learning material into `docs/90.references/learning/`.

## Resolution

Defer scoped README generation for `docs/03.specs/*` as a follow-up backlog
item. The current implementation keeps the taxonomy intact and repairs broken
runtime/documentation contracts without expanding into broad docs consolidation.

## 2026-05-09 Follow-up Audit

A wider template-shape audit found broad legacy drift across stage documents:
many existing `docs/01` to `docs/10` and `docs/90` markdown files predate the
current templates and therefore lack `status: draft` front matter, while some
older README files do not yet expose the full `readme.template.md` base section
set. The active remediation pass intentionally limits edits to the current
service coverage and runtime-hook gaps.

Immediate corrections in this pass:

- Add missing Open Notebook guide, operations policy, and runbook under the
  `11-laboratory` stage paths.
- Add repository-contract validation for service-level 07/08/09 documentation
  coverage.
- Keep `infra/04-data/analytics/ksql` to `ksqldb.md` as an explicit
  implementation-name-to-document-name mapping.
- Keep `infra/06-observability` as an explicit aggregate compose exception.

Deferred work:

- Normalize legacy stage documents to include template front matter where
  appropriate.
- Normalize older nested README files to the complete `readme.template.md`
  base section set.
- Avoid mass front matter insertion until each stage folder has an explicit
  owner and review scope.

## 2026-05-09 Script Usage Audit

The `scripts/` audit found 21 root shell scripts and one library script. No
unused root script was identified as a deletion candidate. The low-risk gap was
discoverability for the manual local TLS utility.

Current disposition:

- Keep all existing root scripts.
- Keep tier hardening wrappers as stable user, document, and CI entrypoints;
  they are not treated as duplicate implementations.
- Classify `generate-local-certs.sh` as a manual operations script and document
  it in the developer setup flow.
- Enforce future script hygiene through `scripts/check-repo-contracts.sh`:
  root scripts must be listed in `scripts/README.md`, non-manual root scripts
  must have an external repository reference, and library scripts must be
  referenced by root scripts.

## Prevention

When a stage subfolder is created or materially changed, update the nearest
stage README or add a local README in the same change. Future README generation
should be a separate docs pass with a clear template and folder-by-folder
ownership.

## Related Documents

- [Agent governance memory index](../../../README.md)
- [Documentation stage matrix](../rules/stage-authoring-matrix.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Specs index](../../03.specs/README.md)
