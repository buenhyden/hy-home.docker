---
title: "Root resource synthetic fixtures"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-10-11"
---

# Root resource synthetic fixtures

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

[측정 schema](../measurement.schema.json)의 공개 합성 입력입니다. 서비스·소유자·SHA·digest,
시간·측정값·예산·배포의 `observed` 표시까지 모두 가상이며 실제 관측 증거가 아닙니다.
원본 로그, 실제 환경 파일, secret, 실제 사용자의 업무 데이터는 포함하지 않습니다.

###### Audience
<!-- core-payload-level:4 -->

평가기 구현자와 독립 검토자가 거부 동작을 확인합니다.

###### Documents
<!-- core-payload-level:4 -->

| Path | Purpose |
| --- | --- |
| [idle-unknown.synthetic.json](idle-unknown.synthetic.json) | `SYNTHETIC_EVIDENCE`, `UNKNOWN_FACTS`, `IDLE_ONLY_LOWERING` |
| [identity-budget-mismatch.synthetic.json](identity-budget-mismatch.synthetic.json) | `SYNTHETIC_EVIDENCE`, `SOURCE_DEPLOYED_MISMATCH`, `CONTRADICTORY_FACTS` |

두 입력 모두 CLI 종료 코드 `1`, 상태 `BLOCKED`를 반환합니다. 결과의
`SOURCE/UNIT/STATIC`, `runtime_acceptance=false`, `mutation_authorized=false`는
실제 운영 수용이나 변경 권한으로 전환되지 않습니다.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

가상 공개 입력만 사용합니다. 환경 설정과 실제 배포에는 연결하지 않습니다.

###### Security Boundary
<!-- core-payload-level:4 -->

합성 fixture는 가상 데이터만 담으며 원본 로그, 실제 환경 파일, secret, 실제 업무 데이터를 포함하지 않는다. 네트워크, 포트, secret 입력이 없다.

#### Usage

##### Prerequisites

JSON Schema로 검증하는 합성 JSON입니다.

##### Selected Start

저장소 루트에서 실행합니다.

```bash
python scripts/operations/root-resource-assessment.py infra/09-platform-ops/resource-optimization/fixtures/identity-budget-mismatch.synthetic.json
```

시험은 [평가기 시험](../../../../tests/lib/ops/test_root_resource_assessment.py)과
[schema 계약 시험](../../../../tests/validation/test_root_resource_contract.py)이 담당합니다.
실제 서비스 관측의 선행 조건은 [준비 계약](../README.md)을 따릅니다.

#### Checks

##### Readiness

두 fixture의 schema 적합성과 예상 blocker를 확인합니다. 합성 통과는 운영 수용을 뜻하지 않습니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [준비 계약](../README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 정적 합성 JSON이어서 관측 대상 런타임이 없다. 두 fixture의 CLI 종료 코드 `1`(BLOCKED)이 정상 기대 결과이며 파일은 Git에서 되돌린다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
