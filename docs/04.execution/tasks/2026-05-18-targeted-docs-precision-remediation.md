---
status: done
---
<!-- Target: docs/04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md -->

# Task: Targeted Documentation Precision Remediation

## Overview (KR)

이 문서는 targeted documentation precision remediation의 실행 상태와 검증 evidence를 기록한다. 작업은 concrete failing condition이 확인된 문서에만 적용한다.

## Inputs

- **Parent Plan**: [Targeted documentation precision remediation plan](../plans/2026-05-18-targeted-docs-precision-remediation.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **README Template**: [README template](../../99.templates/readme.template.md)

## Working Rules

- Every edit must map to a concrete failing condition.
- Do not bulk-retemplate historical leaf documents.
- Keep human-facing docs Korean by default; canonical paths, commands, status values, and governance terms may remain English.
- Do not read or quote secret values, credentials, tokens, certificate bodies, shell history, or raw logs.
- Do not edit or stage unrelated `projects/storybook/mcp/`.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create plan/task execution evidence | doc | Documentation protocol §4 | PLN-001 | New files created with target-relative links | doc-writer | Done |
| T-002 | Classify focused drift scans | audit | Documentation protocol §8 | PLN-002 | Scan outputs classified in Verification Summary | doc-writer | Done |
| T-003 | Repair evidence-gated documentation drift | doc | Documentation protocol §8 R2/R3 | PLN-003 | Edited files listed with failing condition | doc-writer | Done |
| T-004 | Synchronize execution indexes | doc | Documentation protocol §8 R2 | PLN-004 | Parent README links resolve | doc-writer | Done |
| T-005 | Run validators and smoke flows | test | Completion checklist | PLN-005 | Validator outputs recorded below | doc-writer | Done |
| T-006 | Record final progress evidence | memory | Memory progress contract | PLN-006 | Progress log updated | doc-writer | Done |

## Suggested Types

- `audit`
- `doc`
- `test`
- `memory`

## Phase View

### Phase 1

- [x] T-001 Create plan/task execution evidence
- [x] T-002 Classify focused drift scans
- [x] T-003 Repair evidence-gated documentation drift
- [x] T-004 Synchronize execution indexes

### Phase 2

- [x] T-005 Run validators and smoke flows
- [x] T-006 Record final progress evidence

## Verification Summary

- **Initial Scan Evidence**:
  - Missing `## Related Documents`: no actionable output.
  - Real placeholder scan: no actionable output.
  - Stale taxonomy scan: historical `docs/superpowers` references only, preserved as completed migration evidence.
  - Pseudo-link scan: actionable backticked Markdown links found in `docs/05.operations/runbooks/04-data/specialized/neo4j.md`, `docs/05.operations/runbooks/04-data/specialized/qdrant.md`, and `docs/05.operations/runbooks/06-observability/pushgateway.md`.
  - `file://` scan: Qdrant recovery command contains an intentional Qdrant snapshot recovery API file URI, not a documentation link.
  - Operations purpose scans found one exact runbook policy-heading mismatch in `docs/05.operations/runbooks/06-observability/prometheus.md`, ten runbook H1s labeled as policy runbooks, and one runbooks README row pointing into the policies bucket.
- **Edited Files / Failing Conditions**:
  - `docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md`, `docs/04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md`: implementation-phase evidence required by the approved plan and documentation protocol.
  - `docs/04.execution/README.md`, `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`: parent README synchronization for the new plan/task paths.
  - `docs/05.operations/runbooks/04-data/specialized/neo4j.md`, `docs/05.operations/runbooks/04-data/specialized/qdrant.md`, `docs/05.operations/runbooks/06-observability/pushgateway.md`: repaired backticked canonical-reference pseudo-links into target-relative Markdown links.
  - `docs/05.operations/runbooks/04-data/specialized/qdrant.md`: clarified intentional Qdrant snapshot recovery `file://` API payload so readers do not treat it as a document link or host path.
  - `docs/05.operations/runbooks/06-observability/prometheus.md`: removed runbook/policy title ambiguity, narrowed `### Verification` to runbook recovery verification, and replaced duplicate canonical-reference links with target-relative entrypoints.
  - `docs/05.operations/runbooks/04-data/README.md`: corrected the `operational/` runbook inventory link from `policies/` to the sibling runbooks path.
  - `docs/05.operations/runbooks/04-data/nosql/cassandra.md`, `docs/05.operations/runbooks/04-data/nosql/couchdb.md`, `docs/05.operations/runbooks/04-data/nosql/mongodb.md`, `docs/05.operations/runbooks/05-messaging/kafka.md`, `docs/05.operations/runbooks/06-observability/alertmanager.md`, `docs/05.operations/runbooks/06-observability/alloy.md`, `docs/05.operations/runbooks/06-observability/grafana.md`, `docs/05.operations/runbooks/06-observability/loki.md`, `docs/05.operations/runbooks/09-tooling/terraform.md`, `docs/05.operations/runbooks/09-tooling/terrakube.md`: normalized misleading policy-runbook H1s to runbook titles only.
  - `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.html`, `graphify-out/graph.json`: refreshed by `/home/hy/.local/bin/graphify update .` after approved docs edits.
- **Test Commands**:
  - `rg --files-without-match "^## Related Documents$" README.md docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references -g '*.md'`: no actionable output.
  - Focused placeholder, pseudo-link, operations profile-heading, policy-runbook title, and README cross-bucket scans: PASS after scoped repairs.
  - Navigation smoke checks: root `README.md` -> `docs/README.md` -> execution/operations README -> target plan/task/runbook paths verified with `rg` and `test -f`.
  - `bash scripts/validation/check-repo-contracts.sh`: PASS.
  - `bash scripts/validation/check-doc-traceability.sh`: PASS.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`: PASS.
  - `git diff --check`: PASS.
  - `/home/hy/.local/bin/graphify update .`: completed.
  - `bash scripts/knowledge/report-graphify-health.sh`: `status=advisory` due to 3 cross-root inferred edges; no remediation scope taken from inferred edges.

## Related Documents

- **Parent Plan**: [Targeted documentation precision remediation plan](../plans/2026-05-18-targeted-docs-precision-remediation.md)
- **Execution README**: [Execution stage README](../README.md)
- **Root README**: [Root README](../../../README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
