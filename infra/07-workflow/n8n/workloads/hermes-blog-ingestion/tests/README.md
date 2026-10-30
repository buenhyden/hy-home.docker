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
실제 게이트웨이 호환성·엔진 가져오기·서버 간 통신 성공은 별도 증거입니다.

## Scope

임시 합성 산출물과 가짜 전송 연결을 사용합니다. 실제 비밀값·원본 내용·외부
엔드포인트는 필요하지 않습니다. 실제 원본을 사용한 검증을 수행하면 합성 결과와
분리하여 작업 기록에 남깁니다. 기존 조사·이메일·서비스 중단 시험은 실행하지 않습니다.

## Structure

- [test_workflow.py](test_workflow.py): 인증 선언, 정적 오류 경로, 실행 저장 제한,
  비활성 상태와 인증 참조·본문·표현식 부재를 확인하는 다섯 시험입니다.

그 밖의 준비·대기함·전송 시험 파일은 이 디렉터리의 전체 탐색 명령으로 함께
실행합니다. 실제 검증기의 누락·변경은 의존성 실패로 보고합니다.

## Usage

저장소 루트에서 실행합니다.

```bash
python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -v
```

차단 흐름만 확인하려면 다음 명령을 사용합니다.

```bash
python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p test_workflow.py -v
```

흐름 소스가 없을 때 다섯 시험의 실패를 먼저 확인했고, 소스 추가 후 같은
명령에서 다섯 시험이 통과했습니다. 전체 결과·측정 범위·독립 검토는 작업 기록을
따릅니다. 정적 통과는 실제 엔진의 인증 처리나 오류 응답 코드를 증명하지 않습니다.

## Related Documents

- [수집 전송 소스](../README.md)
- [로컬 발행기](../publisher/README.md)
