---
title: "BLOCKED: whole-stack Compose start"
version: "2.0.0"
type: "governance/rule"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: 'BLOCKED: whole-stack Compose start'
  layer: agent
updated: "2026-11-20"
action: "block"
enabled: true
event: "bash"
name: "block-whole-stack-compose-start"
pattern: "(?:\\bdocker[ -]compose\\b[^;&|\\n]*?--profile(?:\\s+|=)(?:'\\*'|\"\\*\"|\\\\\\*|\\*)(?=[\\s;&|'\"]|$)[^;&|\\n]*\\b(?:up|start|create)\\b|\\bdocker[ -]compose\\b[^;&|\\n]*\\b(?:up|start|create)\\b[^;&|\\n]*--profile(?:\\s+|=)(?:'\\*'|\"\\*\"|\\\\\\*|\\*)(?=[\\s;&|'\"]|$)|COMPOSE_PROFILES=['\"]?(?:[\\w-]+,)*\\*(?:,[\\w-]+)*['\"]?(?=[\\s;&|]).*?\\bdocker[ -]compose\\b[^;&|\\n]*\\b(?:up|start|create)\\b)"
---

# BLOCKED: whole-stack Compose start

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the rule payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

##### Objective

Apply the declared `block` action for block-whole-stack-compose-start.

##### Authority

[Environment constraints](../environment-constraints.md#2-infrastructure-constraints),
ENVIRONMENT-CONSTRAINTS-R149 and R150: services on this server start only
by name or by a named profile, never every profile at once.

#### Scope

##### Applies To

The declared `bash` event and `pattern` match `docker compose` or
`docker-compose` with `up`, `start` or `create` when the command selects
every profile: `--profile '*'` in any quoting, `--profile=*`, or
`COMPOSE_PROFILES` holding `*`, including an earlier `export` in the same
command. Every service in the root project sits behind a profile, so these
are the forms that start the whole stack.

##### Exclusions

Rendering and inspection with every profile (`config`, `ps`) stay allowed,
as do starts by named profile or named service.

#### Rules

##### Requirements

```bash
# BLOCKED: every profile at once
docker compose --profile '*' up -d
COMPOSE_PROFILES='*' docker compose up -d

# ALLOWED: render everything, start a named set
docker compose --profile '*' config --quiet
docker compose --profile core up -d keycloak
```

The declared action applies when the pattern matches.

##### Enforcement

The shared dispatcher evaluates the rule before a provider runs the command.
A command assembled at run time, a profile list read from an environment
file, or a hook bypass is outside what the text shows; the operator rule in
environment constraints still applies.

#### Exceptions

##### Exception Conditions

No exception is declared by this rule.

##### Approval and Review

None.

#### Ownership

##### Responsibilities

`@buenhyden`.

##### Change and Adoption

Changes land with their Task evidence and the rule test
`tests/lib/hooks/test_compose_start_rule.py`.

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
