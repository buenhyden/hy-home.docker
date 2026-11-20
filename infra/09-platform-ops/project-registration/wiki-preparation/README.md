---
title: "Wiki 준비 패키지"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Wiki 준비 패키지

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

실제 Wiki 구현 전의 합성 계약과 미래 수용 기준을 정의합니다. SOURCE·UNIT·STATIC만 검증하며 ISOLATED·HOME·MIGRATION·ROTATION·RECOVERY·DELIVERY는 NOT_RUN입니다. owning Spec은 `SPEC-0204`이고 현재 Task ID는 `SPEC-0204-TSK-0008`입니다.

###### Audience
<!-- core-payload-level:4 -->

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

###### Scope
<!-- core-payload-level:4 -->

준비 문서·기계 schema·합성 검증에 한정합니다.

###### Structure
<!-- core-payload-level:4 -->

[제품 intake](product-intake/README.md), [consumer](consumer-contract/README.md), [원천·artifact](source-artifact-contract/README.md), [job·복구](job-outbox-generation/README.md), [blog 인계](blog-data-handoff/README.md), [미래 흐름](future-flows/README.md), [readiness](readiness/README.md), [준비 계약](contracts/README.md), [schema](schemas/README.md), [fixture](fixtures/README.md), [통합 제안](integration-proposal/README.md)

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

비밀값과 실제 환경 변수는 입력하지 않습니다.

###### Security Boundary
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 Markdown 문서와 합성 JSON만 두며 Compose 서비스·포트·네트워크·Docker Secret·접근 제어를 정의하지 않는다. 비밀값과 실제 환경 변수는 입력하지 않는다.

#### Usage

##### Prerequisites

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

##### Selected Start

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

#### Checks

##### Readiness

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

[문서 진입점](../../../../docs/README.md), [project registration 계약](../README.md), 현재 Task ID는 `SPEC-0204-TSK-0008`입니다.

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 실행되는 서비스가 아니므로 헬스체크·지표·로그가 없고, 이 패키지를 대상으로 하는 운영 런북도 `docs/05.operations/03.runbooks`에 없다. 계약 문서가 어긋나면 위 Checks의 단위 검사 실패로 드러나며, 복구는 Git 이력에서 해당 문서 변경을 되돌리는 것이다.

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
