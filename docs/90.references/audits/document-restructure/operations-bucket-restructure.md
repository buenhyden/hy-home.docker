---
status: active
---

<!-- Target: docs/90.references/audits/document-restructure/operations-bucket-restructure.md -->

# Reference: Operations Bucket Restructure

## Overview

This report inventories the current operations buckets under guides, policies,
and runbooks. It records candidate evidence for an operations restructure batch
without moving or rewriting operations content in the audit section.

## Purpose

The approved design requires historical operations bucket restructuring while
keeping guide, policy, and runbook roles separate. This report establishes the
full `00-workspace`, `01-*` through `12-*`, and `90-knowledge` boundary and
records which groups need implementation.

## Repository Role

This report supports `PLN-DRA-002` and the `PLN-DRA-005` operations bucket
batch. It is not an operations policy, guide, or runbook.

## Scope

### In Scope

- `docs/05.operations/guides/{00-workspace,01-*...12-*,90-knowledge}`
- `docs/05.operations/policies/{00-workspace,01-*...12-*,90-knowledge}`
- `docs/05.operations/runbooks/{00-workspace,01-*...12-*,90-knowledge}`
- Direct child Markdown files under those bucket directories.

### Out of Scope

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
| DRA-OPS-001 | `find docs/05.operations/guides docs/05.operations/policies docs/05.operations/runbooks -mindepth 1 -maxdepth 1 -type d \| sort \| wc -l` | 42 operations bucket directories exist across guides, policies, and runbooks. | Bucket baseline. |
| DRA-OPS-002 | `git ls-files 'docs/05.operations/guides/*/*.md' 'docs/05.operations/policies/*/*.md' 'docs/05.operations/runbooks/*/*.md' \| wc -l` | 262 tracked Markdown files exist directly under top-level operations buckets. | Candidate document baseline. |
| DRA-OPS-003 | Bucket file-count scan by role and bucket | `00-workspace`, `01-*` through `12-*`, and `90-knowledge` are present in all three role buckets. | Role classification. |
| DRA-OPS-004 | Reads of operations templates and Stage Authoring Matrix | Guide, policy, and runbook roles have distinct template expectations. | Prevents role collapse. |
| DRA-OPS-005 | Reads of `90-knowledge/llm-wiki-maintenance.md` guide, policy, and runbook | The content is repository-wide LLM Wiki operation, not a service-tier `90` domain. | Identifies move target. |

## Bucket Inventory

| Role | Buckets | Direct Markdown Files | Preliminary Disposition | Notes |
| --- | ---: | ---: | --- | --- |
| `guides` | 14 | 89 | `active-canonical` / restructure review | Includes `00-workspace`, `01-*` through `12-*`, and `90-knowledge`. |
| `policies` | 14 | 85 | `active-canonical` / restructure review | Includes `00-workspace`, `01-*` through `12-*`, and `90-knowledge`. |
| `runbooks` | 14 | 88 | `active-canonical` / restructure review | Includes `00-workspace`, `01-*` through `12-*`, and `90-knowledge`. |

## Bucket Group Inventory

| Bucket | Guide Files | Policy Files | Runbook Files | Preliminary Disposition | Notes |
| --- | ---: | ---: | ---: | --- | --- |
| `00-workspace` | 6 | 4 | 3 | `active-canonical` / integration target | Workspace-level operations bucket. |
| `01-gateway` | 4 | 3 | 3 | `active-canonical` | Gateway service operations. |
| `02-auth` | 3 | 3 | 3 | `active-canonical` | Auth service operations. |
| `03-security` | 2 | 2 | 2 | `active-canonical` | Vault/security operations. |
| `04-data` | 25 | 27 | 27 | `active-canonical` | Data service operations with nested subdomains. |
| `05-messaging` | 4 | 4 | 4 | `active-canonical` | Messaging service operations. |
| `06-observability` | 11 | 11 | 11 | `active-canonical` | Observability service operations. |
| `07-workflow` | 6 | 5 | 5 | `active-canonical` | Workflow service operations. |
| `08-ai` | 5 | 4 | 5 | `active-canonical` | AI service operations. |
| `09-tooling` | 10 | 11 | 10 | `active-canonical` | Tooling service operations. |
| `10-communication` | 2 | 2 | 2 | `active-canonical` | Communication service operations. |
| `11-laboratory` | 7 | 7 | 7 | `active-canonical` | Laboratory/admin operations. |
| `12-infra-net` | 2 | 2 | 2 | `active-canonical` | infra_net cross-service operations. |
| `90-knowledge` | 2 | 2 | 2 | `historical-archive` / integration candidate | Legacy knowledge bucket; LLM Wiki maintenance should move to `00-workspace`. |

## Candidate Files

| File | Role | Current Evidence | Preliminary Disposition | Future Batch |
| --- | --- | --- | --- | --- |
| `docs/05.operations/guides/90-knowledge/llm-wiki-maintenance.md` | Guide leaf | `status: active`; workspace-wide LLM Wiki maintenance usage guide. | move to `guides/00-workspace/` | `PLN-DRA-005` |
| `docs/05.operations/policies/90-knowledge/llm-wiki-maintenance.md` | Policy leaf | `status: active`; workspace-wide LLM Wiki maintenance controls. | move to `policies/00-workspace/` | `PLN-DRA-005` |
| `docs/05.operations/runbooks/90-knowledge/llm-wiki-maintenance.md` | Runbook leaf | `status: active`; workspace-wide LLM Wiki maintenance procedure. | move to `runbooks/00-workspace/` | `PLN-DRA-005` |
| `docs/05.operations/*/90-knowledge/README.md` | Bucket indexes | README profile headings for a legacy knowledge bucket. | remove after move if empty | `PLN-DRA-005` |

## Findings

| ID | Surface | Finding | Disposition | Recommended Batch |
| --- | --- | --- | --- | --- |
| DRA-OPS-001 | Operations bucket taxonomy | The actual restructure surface is all 42 top-level role buckets, not only `01-gateway`. | `active-canonical` / restructure review | `PLN-DRA-005` |
| DRA-OPS-002 | Guide/policy/runbook leaves | Service and workspace leaf documents are active and role-specific; no broad duplicate-remove action is justified without per-file comparison. | `active-canonical` | No broad move in audit pack. |
| DRA-OPS-003 | Bucket README files | Bucket READMEs are index profiles and may omit top lifecycle frontmatter under current routing. | `active-canonical` | Preserve unless future contract changes. |
| DRA-OPS-004 | `90-knowledge` bucket | LLM Wiki maintenance is workspace-level operations material and should move into `00-workspace`; reference facts remain under `docs/90.references/llm-wiki/`. | `historical-archive` / integration candidate | `PLN-DRA-005` |

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
