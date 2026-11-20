---
title: OpenAPI 3.1 contract (openapi.yaml) in a Spec Package
version: 0.1.0
type: common/template-source
status: draft
owner: '@buenhyden'
document_scope:
  subject: sdlc/openapi output definition
  layer: template
updated: '2026-11-20'
template_id: sdlc/openapi
---

# OpenAPI 3.1 contract (openapi.yaml) in a Spec Package

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the native-asset payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: Name the maintained subject, scope and owner; do not grant authority through document metadata. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: State actual inputs, constraints or preconditions, and distinguish facts from assumptions. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: Keep the kind-specific payload here with its conditions, tables and one canonical responsibility. -->

#### Native Payload

The single authored native output source is `docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml`.
Its syntax and supported fields are consumed by the registered producer;
the common definition is never injected into that output.

#### Consumption

Read the native payload through `template_payload` and parse it with its
actual YAML, TOML, Markdown or interface consumer.

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: Explain how the intended reader uses this document or its native output; do not invent an operational step. -->

Use the procedures or reading order stated in the role payload.

### 확인 기준

<!-- 작성 규칙: Use only checks appropriate to this kind; distinguish implementation, verification and actual acceptance. -->

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: Use purpose-bearing owner and dependency references; reciprocal links are not universally required. -->

The role payload retains the current owner and dependency references.

### 외부 근거

<!-- 작성 규칙: Identify external basis and its application or limits; a citation grants no execution or approval authority. -->

External basis and its limits remain those stated in the role payload; a citation grants no authority.
