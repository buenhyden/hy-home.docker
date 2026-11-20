---
title: "Operations move synthetic fixtures"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-10-11"
---

# 운영 문서 경로 매핑 합성 입력

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

P08 준비 단계에서 정확한 source 경로·artifact ID·target 경로의 결합과 거부 조건을
검증합니다. 실제 문서 전수 분류나 이동 결과의 증거가 아닙니다.

###### Audience
<!-- core-payload-level:4 -->

P08 문서 계약 구현자와 코드·보안 검토 담당자입니다.

###### Scope
<!-- core-payload-level:4 -->

허용된 LAB 문서 목적지는 `docs/05.operations/01.guides/labs/`,
`docs/05.operations/02.policies/labs/`, `docs/05.operations/03.runbooks/labs/`입니다.
저장소 루트 `labs/`와 LAB 런타임·비밀값·데이터는 시험의 이동 대상에서 제외합니다.
학습 앱·Wiki 앱 구현·서비스 실행은 포함하지 않습니다.

###### Structure
<!-- core-payload-level:4 -->

- `reviewed-map.json`: 합성 Guide·Runbook의 같은 번호와 서로 다른 LAB 결정을
  담습니다. 이미 정리된 Policy와 미분류 Guide를 포함합니다.
- 경계 거부 입력은 전용 단위시험이 소유합니다. 합성 번호는 실문서 판정 규칙이 아닙니다.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

호출자가 현재 Registry profile과 허용 domain을 제공합니다. nested target은
제안 경로이며 현행 Registry 수용과 구분합니다. helper는 파일·프로세스·승인
시스템에 접근하지 않습니다.

###### Security Boundary
<!-- core-payload-level:4 -->

helper는 파일·프로세스·승인 시스템에 접근하지 않는다. 저장소 루트 `labs/`와 LAB 런타임, 비밀값, 데이터는 시험의 이동 대상에서 제외한다.

#### Usage

##### Prerequisites

기존 frontmatter·taxonomy API와 Python unittest를 재사용합니다.

##### Selected Start

[순수 helper](../../../../scripts/lib/document_governance/operations_moves.py)에 이미
읽은 공개 문서와 검토된 정확한 path/ID 결정을 전달합니다. 미분류·기존 domain
충돌은 `REVIEW_REQUIRED`이며 숫자로 domain을 추정하지 않습니다. 반환되는 README
folder tuple은 필요한 작성 위치이며 실제 README 생성·metadata 수용을 의미하지 않습니다.

#### Checks

##### Readiness

```sh
python3 -m unittest tests.lib.document_governance.test_operations_moves -v
```

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [합성 입력 family](../README.md)
- [운영 문서](../../../../docs/05.operations/README.md)
- [문서 진입점](../../../../docs/README.md): owning Task는 `SPEC-0204-TSK-0015`입니다.

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 실행되는 서비스가 아니라 시험 입력이므로 관측·복구 대상이 없다. 변경은 Git에서 되돌린다.

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
