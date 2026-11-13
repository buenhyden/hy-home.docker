---
title: "Document governance synthetic fixtures"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-10-11"
---

# 문서 계약 합성 입력

## Purpose

### Service Role

문서 경로·정체성 계약을 운영 값 없이 검증하는 합성 입력 모음입니다.

#### Audience

문서 도구 구현자와 독립 검토 담당자입니다.

#### Scope

문서 이동·Registry 등록·운영 실행을 수행하지 않습니다. 실제 전수 문서 분류와
승인된 변경 경로는 owning Task가 관리합니다.

#### Structure

- [operations-moves](operations-moves/README.md): 정확한 경로·ID 매핑과 유형별 LAB
  문서 목적지의 합성 시험 자산입니다.

### Supported Environment

기존 Python unittest와 JSON 입력을 사용합니다.

## Interfaces

### Inputs and Outputs

합성 자료만 추가합니다. 비밀값·개인 식별자·실제 운영 로그를 넣지 않습니다.

### Security Boundary

합성 자료만 두며 비밀값, 개인 식별자, 실제 운영 로그를 넣지 않는다. 문서 이동, Registry 등록, 운영 실행을 수행하지 않는다.

## Development

### Local Workflow

하위 폴더 README에서 시험 범위와 입력을 확인합니다. 새 합성 자산은 해당 계약의
시험 소유자가 관리하고 상위 fixture 진입점을 함께 갱신합니다.

### Checks

```sh
python3 -m unittest tests.lib.document_governance.test_operations_moves -v
```

## Operations

### Runbook Links

- [Fixture 진입점](../README.md)
- [문서 진입점](../../../docs/README.md)

### Observability and Recovery

없음: 실행되는 서비스가 아니라 시험 입력이므로 관측·복구 대상이 없다. 변경은 Git에서 되돌린다.
