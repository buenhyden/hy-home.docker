---
title: "Readiness matrix와 인계 경계"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# Readiness matrix와 인계 경계

## Overview

| 영역 | 현재 처분 | 후속 소유·전제 |
|---|---|---|
| 기존 엔진·Traefik·OIDC 계약 | VERIFY_RUNTIME | P03의 기존 서비스 endpoint·port 조건과 미래 Wiki exact Task |
| 네 schema·합성 fixture·pure helper | IMPLEMENT | P09 순수 검증 및 기존 generic validator harness 실행 |
| 공통 등록·gate 등록 | IMPLEMENT | manifest·workflow·changed/staged controller 통합 및 Qdrant parity 수정 후 replacement frozen QA 35 PASS 완료; latest-head CI·독립 review·PR·merge 대기 |
| 제품 brief/license/main release | BLOCKED_FACTS | 원문·권리·검증된 release 확인 전 bootstrap 금지 |
| 실제 source 권리·ACL·credentials | BLOCKED_FACTS | 독립 승인·발급·회전·복구 경계 |
| 앱/API/UI/검색·embedding·crawler | OUT_OF_SCOPE | 이번 준비 범위에 생성하지 않음 |
| opsflow_dev 독립 배치 연결 자산 | VERIFY_RUNTIME | P04/P05 실제 native 배치 검증 별도 |
| Wiki schedule/workspace/blog-data write | OUT_OF_SCOPE | P09는 생성·실행하지 않음 |
| 실제 복원·native E2E·HOME | VERIFY_RUNTIME | 미래 Wiki exact Task의 backup/custody와 실제 대상; P10은 E2E 수용 기준 자산 |
| 학습 앱/LAB runtime | OUT_OF_SCOPE | 조사·기획·생성·변경하지 않음 |

P02에는 canonical SMTP secret catalog 경계만, P03에는 기존 서비스 endpoint·port 계약 조건만 인계합니다. 미래 Wiki의 namespace/권한, retention/RPO/RTO, delete-priority와 recovery는 별도 exact Task가 소유합니다. P04/P05에는 `fixtures/`의 합성 schema·semantic expectation 연결 자산, P08에는 이 패키지 README·링크와 Stage05 LAB 이동 후보 목록, P10에는 미래 Wiki 구현자가 사용할 E2E 수용 기준과 NOT_RUN 조건을 인계합니다. P10은 실제 Wiki E2E 구현을 소유하지 않습니다. P08 후보는 `docs/05.operations/guides/0074-laboratory-optimization-hardening.md`, `docs/05.operations/policies/0074-laboratory-optimization-hardening.md`, `docs/05.operations/runbooks/0074-laboratory-optimization-hardening.md`이며, 이 P09는 읽기·목록화만 했고 이동·링크 변경은 하지 않습니다. 어떤 영역도 schema PASS를 실제 resource 생성·데이터 이관·복원 성공으로 바꾸어 보고하지 않습니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[준비 패키지](../README.md)

## Tech Stack

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Configuration

비밀값과 실제 환경 변수는 입력하지 않습니다.

## Validation

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

## Usage

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

## Related Documents

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.
