---
title: "Readiness matrix와 인계 경계"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Readiness matrix와 인계 경계

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

| 영역 | 현재 처분 | 후속 소유·전제 |
|---|---|---|
| 기존 엔진·Traefik·OIDC 계약 | VERIFY_RUNTIME | P03의 기존 서비스 endpoint·port 조건과 미래 Wiki exact Task |
| 네 schema·합성 fixture·pure helper | NO_CHANGE | 준비 산출물 소스 수용; 현재 P09 35개와 기존 generic 등록 8개 시험 PASS. 실제 원천·권리·ACL 검증은 미래 구현의 조건 |
| 공통 등록·gate 등록 | NO_CHANGE | 로컬 main에 통합된 manifest·workflow 등록을 실제 검사해 PASS. 현재 준비 범위 독립 검토 승인. 원래 hosted CI 실패는 이력으로 보존하며 현재 전달 경로는 로컬 main |
| 제품 brief/license/main release | BLOCKED_FACTS | 원문·권리·검증된 release 확인 전 bootstrap 금지 |
| 실제 source 권리·ACL·credentials | BLOCKED_FACTS | 독립 승인·발급·회전·복구 경계 |
| 앱/API/UI/검색·embedding·crawler | OUT_OF_SCOPE | 이번 준비 범위에 생성하지 않음 |
| opsflow_dev 독립 배치 연결 자산 | VERIFY_RUNTIME | P04/P05 실제 native 배치 검증 별도 |
| Wiki schedule/workspace/blog-data write | OUT_OF_SCOPE | P09는 생성·실행하지 않음 |
| 실제 복원·native E2E·HOME | VERIFY_RUNTIME | 미래 Wiki exact Task의 backup/custody와 실제 대상; P10은 E2E 수용 기준 자산 |
| 학습 앱/LAB runtime | OUT_OF_SCOPE | 조사·기획·생성·변경하지 않음 |

P02에는 canonical SMTP secret catalog 경계만, P03에는 기존 서비스 endpoint·port 계약 조건만 인계합니다. 미래 Wiki의 namespace/권한, retention/RPO/RTO, delete-priority와 recovery는 별도 exact Task가 소유합니다. P04/P05에는 `fixtures/`의 합성 schema·semantic expectation 연결 자산, P08에는 이 패키지 README·링크와 당시 Stage05 LAB 이동 후보 목록, P10에는 미래 Wiki 구현자가 사용할 E2E 수용 기준과 NOT_RUN 조건을 인계했습니다. P10은 실제 Wiki E2E 구현을 소유하지 않습니다. 당시 목록에 있던 subject 0074의 현재 경로는 `docs/05.operations/01.guides/10.platform-and-backup/0074-laboratory-optimization-hardening.md`, `docs/05.operations/02.policies/10.platform-and-backup/0074-laboratory-optimization-hardening.md`, `docs/05.operations/03.runbooks/10.platform-and-backup/0074-laboratory-optimization-hardening.md`입니다. P08의 경로 정리는 이미 반영되어 있으며, 이 P09는 당시 읽기·목록화만 수행했습니다. 이번에는 현재 경로 안내만 정정하며 새 이동을 수행하지 않습니다. 어떤 영역도 schema PASS를 실제 resource 생성·데이터 이관·복원 성공으로 바꾸어 보고하지 않습니다.

###### Audience
<!-- core-payload-level:4 -->

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

###### Scope
<!-- core-payload-level:4 -->

준비 문서·기계 schema·합성 검증에 한정합니다.

###### Structure
<!-- core-payload-level:4 -->

[준비 패키지](../README.md)

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

현재 산출물은 준비 계약과 합성 검증에 재사용합니다. 앱과 운영 자원 생성은 별도 구현 요청에서 정확한 소유·대상·검증·복구 경계를 정한 뒤 수행합니다.

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
