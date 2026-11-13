---
title: "Synthetic fixture family"
version: "0.2.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-10-11"
---

# 합성 fixture

## Purpose

### Service Role

독립 CLI·schema consumer가 공유하는 비밀값 없는 고정 입력입니다.

#### Audience

저장소 계약의 구현·검토 담당자입니다.

#### Scope

운영 secret·dotenv·인증자료·원문 로그는 보관하지 않습니다.

#### Structure

- [port-contract/](port-contract/README.md): P03 네 위치 포트 선언·합성 config 입력.
- [document_governance/](document_governance/README.md): 문서 경로·정체성 계약의
  비밀값 없는 합성 입력.

- [opsflow-acceptance/](opsflow-acceptance/README.md): P10 게시·통지 seam의
  오프라인 합성 수용 입력.

### Supported Environment

기존 Python unit/contract 검증을 사용합니다.

## Interfaces

### Inputs and Outputs

각 하위 README와 owning Task가 합성 입력의 의미와 허용 경계를 설명합니다.

### Security Boundary

비밀값이 없는 고정 입력만 보관하며 운영 secret, dotenv, 인증자료, 원문 로그는 두지 않는다. 포트와 network 선언이 없다.

## Development

### Local Workflow

각 consumer에 필요한 명명된 합성 입력만 선택합니다.

### Checks

[검증 진입점](../README.md)의 현재 등록된 시험 owner를 사용합니다.

## Operations

### Runbook Links

- [Test surface](../README.md)

### Observability and Recovery

없음: 실행되는 서비스가 아니라 시험 입력이므로 관측·복구 대상이 없다. 변경은 Git에서 되돌린다.
