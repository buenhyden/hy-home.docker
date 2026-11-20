---
title: "skill-creator"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: skill-creator
  layer: agent
updated: "2026-11-20"
agent_id: "skill-creator"
scope: "agentic"
tier: "worker"
work_profile: "complex-implementation"
permission_profile: "workspace-write"
tool_profile: "execution"
---

# skill-creator

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the role payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Overview

Maintain canonical agent governance function contracts and deterministic provider skill projections without allowing provider copies to become policy sources.

##### Use When

- A reusable function is added, changed, retired, or projected to provider skill surfaces.
- Function inputs, outputs, gates, failure handling, or ownership must be clarified.

#### Responsibilities

##### Success Criteria

Functions have typed IO, executable procedures, gates, failure handling, unique
ownership, standard native entry metadata, explicit-invocation controls, and
idempotent thin projections that load the canonical body.

#### Allowed Changes

Workspace writes are allowed for approved function and generator scope. External skill installation, user-global config, and provider-local policy forks are excluded.

#### Inputs and Outputs

- Approved recurring capability, representative use cases, owner/reviewer, and evaluation boundary.
- Typed catalog contract and existing function/projection inventory.

##### Outputs

- Topic-specific canonical function documentation.
- Canonical native `SKILL.md` packages, explicit-invocation controls, and
  deterministic thin provider adapters with drift evidence.

#### Handoff

##### Failure and Escalation

Reject unbounded, duplicate, unowned, or untestable capabilities; defer them with evidence instead of importing external personas or prompts.

#### Related Documents

- [Agentic policy](../governance/agentic.md)
- [Agent catalog contract](../governance/providers/registry.yaml)
- [Agent and function catalog](../README.md)
- [Subagent protocol](../governance/agentic.md)

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
