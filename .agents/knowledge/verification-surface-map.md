---
title: "Verification Surface Map"
version: "1.0.0"
type: "governance/control"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: Verification Surface Map
  layer: agent
updated: "2026-11-20"
created: "2026-09-06"
observed_at: "2026-10-07"
review_cycle: "on-gate-change"
---

# Verification Surface Map

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the knowledge payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Overview

Locate the one owner of a quality decision. This navigation map does not copy
job inventories, exclusion constants, path rules or execution status.

#### Scope

Current document and Docker/Compose QA plus the supporting selector, style and
release implementation. Actual execution/acceptance belongs to the current Task;
remote protection and runtime observations require their own receipts.

#### Rules

##### Public Entrypoints

| Purpose | Current owner |
| --- | --- |
| Inspect changed selection without execution | `python3 scripts/validation/run-ci-gate.py --profile changed --explain` |
| Local-only document links | `check-document-links.py --mode all`; Task-bound final document input |
| Remote PR candidate acceptance | `run-ci-gate.py --profile changed`, scheduled by the quality workflow |
| Explicit comprehensive maintenance/audit | `run-ci-gate.py --profile full`, with Task-bound budget and authorization |
| Scoped format/lint modes and tool pins | `.pre-commit-config.yaml` and the changed-style controller |
| Provider/native document projection | `provider_surface_renderer.py --check`, only when its source is affected |
| Explicit all-files authoring maintenance | Controlled `run-agent-precommit-all-files.sh`; no routine commit/push/PR invocation |

##### Current Guarantees and Composition

- Stage 99 Registry owns profile, template, identity and lifecycle contracts.
  Metadata/corpus readers enforce current content and preservation remotely;
  the link reader owns the local-only document-link lane.
- Compose/service owners define configuration, hardening and operator recovery.
  Preflight, temporary rendering and live runtime have different inputs and effects.
- The machine [workflow contract](../../.github/workflow-contract.yml) owns suite,
  leaf, dependency, prefix and prerequisite selection. Inspect its actual plan;
  this map deliberately maintains no second transcribed inventory.
- The [quality policy](../../docs/00.workspace/04.quality/quality-standards.md#canonical-delivery-phase-matrix)
  owns authoring/commit/push/PR/main/release responsibility and check admissibility.
- Ordinary authored documents select content/form checks. Their implementation
  suites are selected only for relevant validator/contract changes. Frontend QA
  follows the frontend project. Unknown inputs fail closed.
- Identical invocation execution is unique within a declared input/tool/mode/trust
  context. Raw immutable Git input sharing is not reuse of PASS or acceptance.
- One-time event-specific counts/hashes and agent answer scores are retired QA;
  generic frozen-byte, unsafe-path and lifecycle guards remain current.

##### Test Ownership

| Layer | Location and purpose |
| --- | --- |
| Document implementation | `tests/lib/document_governance/`, current parser/contract boundaries |
| CLI and selector | `tests/lib/gate/`, `tests/validation/`, admitted composition/trust/failure/cleanup |
| Docker operations | Reusable service tests and `examples/operations/`, separate operator approval |
| Supporting release/style | Focused regression for current changelog/producer and read-only tool routing |
| Synthetic helpers | Underscore-prefixed test support; no production imports |

#### Evidence

##### Provenance

The source owners were read on 2026-10-07 in the SPEC-0211 worktree based on
main `849ef009a`. The current Task owns actual patch inputs, tests, independent
review and hosted results. This map does not promote source configuration into
an executed workflow or runtime acceptance.

##### Knowledge Validity

Use only while named sources agree. Source changes invalidate affected facts
until re-read; approval, secrets and user-global configuration are outside this
navigation record.

##### Refresh Triggers

Refresh when the public entrypoint, admitted QA purpose, composition owner,
execution-context boundary, test location or release producer changes.

#### Related Documents

- [Knowledge index](README.md)
- [Repository authority map](repository-map.md)
- [Quality standards](../../docs/00.workspace/04.quality/quality-standards.md)
- [Environment constraints](../governance/environment-constraints.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
