---
title: "Hermes 수집 전송 합성 시험"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-30"
---

# Hermes 수집 전송 합성 시험

## Overview

로컬 파일 보존과 전송 상태 처리, 비활성 흐름의 보안 경계를 검증합니다.
고정된 Gateway 계약·Fixture에 대한 합성 호환성을 확인합니다. 실제 엔진
가져오기·서버 간 통신과 영속 수신 성공은 별도 증거입니다.

## Scope

임시 합성 산출물과 가짜 전송 연결을 사용합니다. 실제 비밀값·원본 내용·외부
엔드포인트는 필요하지 않습니다. 실제 원본을 사용한 검증을 수행하면 합성 결과와
분리하여 작업 기록에 남깁니다. 기존 조사·이메일·서비스 중단 시험은 실행하지 않습니다.

## Structure

- [test_workflow.py](test_workflow.py): 비활성 흐름과 입력 선별, 분기, 고정 대상,
  영속 수신 응답을 합성 데이터와 빈 Node VM으로 검증합니다.
- [test_gateway_adapter.py](test_gateway_adapter.py)와
  [test_gateway_transport.py](test_gateway_transport.py): 고정 계약 어댑터와
  동일 요청 재전송·Outbox 처리를 합성 방식으로 검증합니다.
- [합성 보고서](fixtures/synthetic-report.json)와 같은 디렉터리의 계약 파일: Blog-data `dev` 커밋
  `a6d0957ad380f179f73bdd2a60ff23792d53f7ae`에서 고정한 계약과 합성 보고서입니다.

그 밖의 준비·대기함·전송 시험 파일은 이 디렉터리의 전체 탐색 명령으로 함께
실행합니다. 실제 검증기의 누락·변경은 의존성 실패로 보고합니다.

## Usage

저장소 루트에서 실행합니다.

```bash
python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -v
```

흐름 소스만 확인하려면 다음 명령을 사용합니다.

```bash
python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p test_workflow.py -v
```

전체 시험 결과·측정 범위·독립 검토는 작업 기록을 따릅니다. 합성 검증은
실제 n8n Queue·외부 Runner·인증 처리나 서버 B의 영속 수신을 증명하지 않습니다.
일부 시험은 별도 고정 검증기 또는 로컬 합성 HTTP/TLS 환경이 필요합니다.

## Related Documents

- [수집 전송 소스](../README.md)
- [로컬 발행기](../publisher/README.md)
