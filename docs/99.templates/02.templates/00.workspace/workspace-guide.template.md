---
title: '{{TITLE}}'
version: 0.1.0
type: governance/workspace-guide
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
updated: '{{UPDATED}}'
created: '{{CREATED}}'
observed_at: '{{OBSERVED_AT}}'
review_cycle: '{{REVIEW_CYCLE}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: State the local reader task and route to this guide's actual procedure. -->

Readers use the guide payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: Name the workspace subject, owner and applicability without granting execution permission. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: Distinguish required local inputs, observed facts and assumptions. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: Keep the workspace setup or maintenance responsibility in its registered role payload. -->

<!-- Author prompt: Use only the registered workspace-environment or workspace-maintenance path. Write English prose and replace every placeholder; remove author comments from actual guides. Keep optional observation/review metadata only when it describes a real observation/review. -->

#### Purpose

{{READER_TASK_OUTCOME_AND_OWNERS}}

#### Prerequisites

<!-- Author prompt: State the included and excluded subject, local environment and access. Link applicable approval/safety owners. The guide, its lifecycle and a passing check never authorize a command or accept the feature. -->

{{WORKSPACE_BOUNDARY_ENVIRONMENT_AND_AUTHORITY}}

#### Procedure

<!-- Author prompt: Preserve only implemented local setup or harness procedures with their exact inputs, limits, expected signals, stop conditions and next owner. Use topic subsections as needed. Read-only checks and mutations remain distinct; product backup and restore stay with their actual Runbook. Only the registered active maintenance profile may be an eligible harness operation documentation owner. -->

{{IMPLEMENTED_PROCEDURES_AND_FAILURE_HANDOFF}}

#### Verification

<!-- Author prompt: Record actual source provenance, expected checks and refresh triggers. Local/static checks do not prove hosted, provider-runtime or owner acceptance. -->

{{SOURCE_PROVENANCE_CHECKS_AND_REFRESH_TRIGGERS}}

#### Related Documents

{{PURPOSE_BEARING_CURRENT_OWNER_LINKS}}

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: Explain how the reader uses this guide without inventing an operational step. -->

Use the procedures or reading order stated in the role payload.

### 확인 기준

<!-- 작성 규칙: Use this guide's actual checks and keep implementation, verification and acceptance separate. -->

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: Keep purpose-bearing references to the actual owners; reciprocal links are not universal. -->

The role payload retains the current owner and dependency references.

### 외부 근거

<!-- 작성 규칙: State external basis and its limits without treating it as execution approval. -->

External basis and its limits remain those stated in the role payload; a citation grants no authority.
