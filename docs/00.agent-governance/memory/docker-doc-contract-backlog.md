---
layer: agentic
---

# Memory: Docker Documentation Contract Backlog

- Date: 2026-05-09
- Layer: docs
- Status: superseded
- Applies To: `docs/03.specs/`, `docs/90.references/`, Docker docs, script contract checks
- Tags: #docker #documentation #quality
- Retrieval Keywords: docker docs backlog, README coverage, stage templates, script usage audit, service documentation coverage
- Last Verified: 2026-05-22

## Problem

The original Docker documentation contract audit found missing
`docs/03.specs/*` README files and broader template-shape debt. Later
documentation passes closed that backlog. This note remains as historical
context so future agents do not re-open completed cleanup work.

## Context

Missing README coverage was originally observed under:

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

As of the 2026-05-22 bounded re-audit, those listed `docs/03.specs/*`
directories have README coverage and the repository contract reports a clean
target-stage normalization baseline.

Current validator metrics:

- `target_stage_docs_total=465`
- `normalized_target_stage_docs_total=465`
- `legacy_target_stage_docs_skipped=0`
- `infra_service_readmes_rubric_partial=0`

## Resolution

The README coverage backlog is closed. Future work should treat this note as
historical evidence, not an active task list.

## 2026-05-09 Follow-up Audit

A wider template-shape audit found broad legacy drift across stage documents.
That finding was valid on 2026-05-09, but it is superseded by the 2026-05-22
repository contract baseline.

Immediate corrections in this pass:

- Add missing Open Notebook guide, operations policy, and runbook under the
  `11-laboratory` stage paths.
- Add repository-contract validation for service-level guides/policies/runbooks documentation
  coverage.
- Keep `infra/04-data/analytics/ksql` to `ksqldb.md` as an explicit
  implementation-name-to-document-name mapping.
- Keep `infra/06-observability` as an explicit aggregate compose exception.

Current disposition:

- Do not recreate the old README backlog.
- Use current validators and stage templates for any newly edited document.
- Record new gaps in a fresh memory note if future drift is found.

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
- Enforce future script hygiene through `scripts/validation/check-repo-contracts.sh`:
  root scripts must be listed in `scripts/README.md`, non-manual root scripts
  must have an external repository reference, and library scripts must be
  referenced by root scripts.

## Prevention

When a stage subfolder is created or materially changed, update the nearest
stage README or add a local README in the same change. Use current repository
validators as the source of truth for whether this backlog has reopened.

## Evidence

- `docs/03.specs/README.md`
- `docs/90.references/docker/README.md`
- `scripts/README.md`
- `scripts/validation/check-repo-contracts.sh`
- `bash scripts/validation/check-repo-contracts.sh` on 2026-05-22:
  `legacy_target_stage_docs_skipped=0`,
  `infra_service_readmes_rubric_partial=0`
- [Workspace governance bounded re-audit task](../../04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md)

## Related Documents

- [Agent governance memory index](../../../README.md)
- [Documentation stage matrix](../rules/stage-authoring-matrix.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Specs index](../../03.specs/README.md)
- [Workspace governance bounded re-audit task](../../04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md)
