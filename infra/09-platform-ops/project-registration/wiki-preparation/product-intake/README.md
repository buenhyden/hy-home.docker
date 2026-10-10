---
title: "제품 intake와 제외 범위"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 제품 intake와 제외 범위

## Overview

원천 문서의 출처·권한·최신성을 따라 추후 탐색하고 Literature 후보를 사람이 선택하여 인계하는 제품 준비입니다. 사용자는 권한이 있는 원천을 선택하고 동기화 상태·인용 근거·후보를 확인합니다. 지연 또는 실패 시 최신성 상태를 숨기지 않습니다.

허용 knowledge source는 `buenhyden/blog-data@dev`, `buenhyden/Project-Template@dev`, `buenhyden/hy-home.docker@main`, `buenhyden/hy-home.k8s@main` 네 pinned repository/ref입니다. 각 소비 실행은 해당 ref의 immutable revision을 별도로 기록해야 하며, 이 준비 패키지는 revision을 검증하거나 fetch하지 않습니다. `dev`는 지식 원천이며 미래 앱 생성용 검증된 Project-Template `main` release와 다릅니다. 읽기 전용 intake에서 [Project-Template main](https://github.com/buenhyden/Project-Template)은 `6b1c7394f1e08c0ce566f76b4644c2cad9c89891`(unprotected), README blob은 `0c9c037a98b220b1c5443468a3ddcdb68b0589bd`였습니다. [latest release](https://github.com/buenhyden/Project-Template/releases/latest)는 HTTP 404 (exit 1)여서 verified main release는 `BLOCKED_FACTS`이고, SPDX license는 null이라 rights는 UNKNOWN입니다. language 관측값 Python/Shell은 automation뿐이며 앱 stack은 미결정입니다. README는 강제 language/framework 없이 product·stack intake 뒤 Stage01을 진행하고, `bash scripts/ws.sh bootstrap --dry-run`을 검토한 뒤에만 bootstrap하도록 안내합니다. 이 작업은 bootstrap을 실행하거나 외부 workspace를 만들지 않았습니다. 공유 brief는 제목만 반환되어 원문 본문에 접근할 수 없었으므로 추정으로 채우지 않습니다. 이 상태는 배포·재사용 허가가 아닙니다.

실제 Wiki Core/API/UI/검색·embedding·crawler, 앱 DB·role·collection·bucket·credential·외부 workspace·예약 workflow·blog-data 쓰기는 생성하지 않습니다. 학습 앱과 LAB runtime은 제외합니다. PostgreSQL/object/Qdrant 등 기존 엔진의 존재는 앱이 구현되었다는 증거가 아닙니다.

MVP 단계는 (1) P09의 offline 계약·합성 fixture·future acceptance 준비, (2) 별도 미래 app Task가 승인된 뒤의 권한 있는 source/auth/provenance와 read-only search, (3) 같은 별도 Task의 선택된 Literature handoff 및 recovery acceptance입니다. 이번 P09는 첫 단계로 시작해 그 범위에서 끝나며 2·3단계를 승인하거나 구현하지 않습니다. 비용 책임자는 현재 UNKNOWN이며, runtime·storage·egress·embedding 비용은 resource 승인 전 미래 project owner가 예산과 한도를 수용해야 합니다. P02는 canonical SMTP secret catalog만 소유하고 P03는 기존 서비스 endpoint·port 계약 조건만 소유합니다. 미래 Wiki의 runtime/resource/retention, RPO/RTO, deletion 또는 recovery는 이름 있는 별도 exact Task에서 정합니다. P04/P05는 합성 배치 연결 자산, P10은 미래 E2E 수용 기준 자산을 별도로 소유합니다. P09는 운영 실행자·on-call·resource owner를 배정하지 않습니다.

미결정은 shared brief 본문, license와 verified main release, budget/on-call/resource owner입니다. 위험은 stale ACL 또는 index와 PG/object/Qdrant의 비원자성이므로, 미래 Task는 revoke/delete frontier와 recovery acceptance를 별도 증명해야 합니다. 학습 앱은 어느 MVP 단계에도 포함하지 않습니다.

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
