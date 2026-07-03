---
status: active
---

<!-- Target: docs/90.references/audits/document-restructure/operations-bucket-restructure.md -->

# Reference: Operations Bucket Restructure

## Overview

This report inventories the current operations `01-*` buckets under guides,
policies, and runbooks. It records candidate evidence for a future operations
restructure batch without moving or rewriting any operations document.

## Purpose

The approved design requires historical operations bucket restructuring while
keeping guide, policy, and runbook roles separate. This report establishes the
current `01-gateway` boundary and records which documents need future
classification.

## Repository Role

This report supports `PLN-DRA-002` and the future `PLN-DRA-005` operations
bucket batch. It is not an operations policy, guide, runbook, or approval to
move active operations documents.

## Scope

### In Scope

- `docs/05.operations/guides/01-*`
- `docs/05.operations/policies/01-*`
- `docs/05.operations/runbooks/01-*`
- Direct child Markdown files under those bucket directories.

### Out of Scope

- Operations buckets outside `01-*`.
- Runtime Nginx, Traefik, or Docker Compose changes.
- Moving files, changing operational commands, or rewriting procedures.
- Incident and postmortem packet routing.

## Definitions / Facts

- **Guide**: usage and common-check documentation.
- **Policy**: control, exception, verification, review-cadence, and
  enforcement documentation.
- **Runbook**: procedural response, evidence, rollback, and escalation
  documentation.
- **Bucket restructure**: path/routing cleanup after a candidate report, not a
  role merge.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| DRA-OPS-001 | `find docs/05.operations/guides docs/05.operations/policies docs/05.operations/runbooks -type d -name '01-*' \| sort \| wc -l` | 3 operations `01-*` directories exist. | Bucket baseline. |
| DRA-OPS-002 | `git ls-files 'docs/05.operations/guides/01-*/*.md' 'docs/05.operations/policies/01-*/*.md' 'docs/05.operations/runbooks/01-*/*.md' \| wc -l` | 10 tracked Markdown files exist directly under those buckets. | Candidate document baseline. |
| DRA-OPS-003 | Targeted heading scan across the 10 files | Leaf docs use active guide, policy, and runbook headings; bucket READMEs are index profiles without top lifecycle frontmatter. | Role classification. |
| DRA-OPS-004 | Reads of operations templates and Stage Authoring Matrix | Guide, policy, and runbook roles have distinct template expectations. | Prevents role collapse. |

## Bucket Inventory

| Bucket | Files | Preliminary Disposition | Notes |
| --- | ---: | --- | --- |
| `docs/05.operations/guides/01-gateway` | 4 | `active-canonical` / restructure review | Contains one README index and three active guide leaves. |
| `docs/05.operations/policies/01-gateway` | 3 | `active-canonical` / restructure review | Contains one README index and two active policy leaves. |
| `docs/05.operations/runbooks/01-gateway` | 3 | `active-canonical` / restructure review | Contains one README index and two active runbook leaves. |

## Candidate Files

| File | Role | Current Evidence | Preliminary Disposition | Future Batch |
| --- | --- | --- | --- | --- |
| `docs/05.operations/guides/01-gateway/README.md` | Guide bucket index | README profile headings; no top lifecycle frontmatter. | `active-canonical` / index review | `PLN-DRA-005` |
| `docs/05.operations/guides/01-gateway/01.setup.md` | Guide leaf | `status: active`; `## Usage`, `## Common Checks`, `## Runbook Handoff`. | `active-canonical` / duplicate review | `PLN-DRA-005` |
| `docs/05.operations/guides/01-gateway/nginx.md` | Guide leaf | `status: active`; Nginx usage guide. | `active-canonical` / duplicate review | `PLN-DRA-005` |
| `docs/05.operations/guides/01-gateway/traefik.md` | Guide leaf | `status: active`; Traefik usage guide. | `active-canonical` / duplicate review | `PLN-DRA-005` |
| `docs/05.operations/policies/01-gateway/README.md` | Policy bucket index | README profile headings; no top lifecycle frontmatter. | `active-canonical` / index review | `PLN-DRA-005` |
| `docs/05.operations/policies/01-gateway/nginx.md` | Policy leaf | `status: active`; policy scope, controls, exceptions, verification. | `active-canonical` / duplicate review | `PLN-DRA-005` |
| `docs/05.operations/policies/01-gateway/traefik.md` | Policy leaf | `status: active`; policy scope, controls, exceptions, verification. | `active-canonical` / duplicate review | `PLN-DRA-005` |
| `docs/05.operations/runbooks/01-gateway/README.md` | Runbook bucket index | README profile headings; no top lifecycle frontmatter. | `active-canonical` / index review | `PLN-DRA-005` |
| `docs/05.operations/runbooks/01-gateway/nginx.md` | Runbook leaf | `status: active`; procedure, evidence, rollback, escalation. | `active-canonical` / duplicate review | `PLN-DRA-005` |
| `docs/05.operations/runbooks/01-gateway/traefik.md` | Runbook leaf | `status: active`; procedure, evidence, rollback, escalation. | `active-canonical` / duplicate review | `PLN-DRA-005` |

## Findings

| ID | Surface | Finding | Disposition | Recommended Batch |
| --- | --- | --- | --- | --- |
| DRA-OPS-001 | Operations `01-*` buckets | Only `01-gateway` currently appears in guide, policy, and runbook buckets. | `active-canonical` / restructure review | `PLN-DRA-005` |
| DRA-OPS-002 | Guide/policy/runbook leaves | Leaf documents are active and role-specific; no duplicate-remove action is justified without deeper content comparison. | `active-canonical` | No move in audit pack. |
| DRA-OPS-003 | Bucket README files | Bucket READMEs are index profiles and may omit top lifecycle frontmatter under current routing. | `active-canonical` | Preserve unless future contract changes. |
| DRA-OPS-004 | Future restructure | A future operations batch must compare current links and operational replacements before archive or removal. | `evidence-preserve` | `PLN-DRA-005` |

## Source Rules

- Keep guide, policy, and runbook roles separate.
- Treat operations README files as folder indexes unless a future contract says
  otherwise.
- Do not change operational commands or procedures in a restructure batch
  unless the task explicitly expands into operations content remediation.
- Do not archive active operations leaves without replacement, tombstone, and
  link evidence.

## Sources

- [Document restructure design spec](../../../03.specs/document-restructure-audit-contract-archive/spec.md) - Defines operations bucket restructure scope.
- [Operations guide template](../../../99.templates/templates/operations/guide.template.md) - Defines guide role.
- [Operations policy template](../../../99.templates/templates/operations/policy.template.md) - Defines policy role.
- [Operations runbook template](../../../99.templates/templates/operations/runbook.template.md) - Defines runbook role.
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - Defines stage boundaries.
- [Frontmatter routing profile](../document-contracts/frontmatter-routing-profile.md) - Supplies README/index frontmatter routing evidence.

## Maintenance

- **Owner**: Documentation Specialist / Operations Maintainer.
- **Review Cadence**: Review before any operations `01-*` move, archive, or
  remove batch.
- **Update Trigger**: Update when operations `01-*` files are added, removed,
  renamed, or reclassified.

## Related Documents

- [Document restructure audit references](./README.md)
- [Restructure gap register](./restructure-gap-register.md)
- [Document restructure task evidence](../../../04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md)
- [Operations README](../../../05.operations/README.md)
