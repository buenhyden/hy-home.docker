---
title: "합성 준비 schema"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# 합성 준비 schema

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

네 문서는 closed-object JSON Schema 2020-12입니다. consumer-manifest만 기존 registration schema의 메모리 URN을 사용합니다. caller는 허용 URN mapping을 제공하며 외부 $ref는 거절합니다. consumer의 Qdrant RBAC은 project-scoped collection과 non-admin role을 구조화하고, helper가 trusted caller policy와 project scope를 확인합니다. schema는 입력 형식, helper는 hash·선택·generation 등 교차 필드 정합을 검사합니다.

###### Audience
<!-- core-payload-level:4 -->

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

###### Scope
<!-- core-payload-level:4 -->

준비 문서·기계 schema·합성 검증에 한정합니다.

###### Structure
<!-- core-payload-level:4 -->

[consumer](consumer-manifest.schema.json), [source](source-artifact.schema.json), [job](job-outbox-handoff.schema.json), [blog](blog-data-handoff.schema.json)

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `consumer-manifest.schema.json` | 이 디렉터리 | helper와 caller | 기존 registration schema의 메모리 URN을 쓰며 Qdrant RBAC을 project-scoped collection과 non-admin role로 구조화한다. | 외부 `$ref`는 거절하며 계약이 어긋나면 단위 검사 실패로 드러난다. |
| `source-artifact.schema.json` | 이 디렉터리 | helper | closed-object JSON Schema 2020-12로 입력 형식을 정하고 helper가 교차 필드 정합을 검사한다. | 계약이 어긋나면 단위 검사 실패로 드러난다. |
| `job-outbox-handoff.schema.json` | 이 디렉터리 | helper | closed-object JSON Schema 2020-12로 입력 형식을 정하고 helper가 교차 필드 정합을 검사한다. | 계약이 어긋나면 단위 검사 실패로 드러난다. |
| `blog-data-handoff.schema.json` | 이 디렉터리 | helper | closed-object JSON Schema 2020-12로 입력 형식을 정하고 helper가 교차 필드 정합을 검사한다. | 계약이 어긋나면 단위 검사 실패로 드러난다. |

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

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.

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
