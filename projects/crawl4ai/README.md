---
title: "Crawl4AI 수집 adapter"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
created: "2026-10-09"
---

# Crawl4AI 수집 adapter

## Overview

다른 워크스페이스가 이 저장소의 Crawl4AI를 쓸 때 고정해서 가져가는 참조 adapter입니다. 출처 registry로 URL을 승인하고, 각 수집을 SQLite의 제한된 job으로 실행하며, 원본 결과의 출처와 권리를 보존하고, 파생 결과를 원본과 함께 삭제합니다. 앱의 수집 workflow와 업무 로직은 소비 워크스페이스가 소유하며, 이 저장소의 `infra/`에는 앱 코드를 두지 않습니다.

## Audience

Crawl4AI 소비를 계획하는 외부 워크스페이스 소유자와, 소비자 승인 변경을 검토하는 운영자입니다.

## Scope

출처 registry 검증과 URL 승인, job 상태(`queued`, `running`, `succeeded`, `failed`, `cancelled`, `blocked`), idempotency key, 재시도와 backoff, deadline, 한 job당 한 페이지, 모든 시도를 세는 출처별 rate와 일일 quota, job을 꺼낼 때의 registry 재확인, 응답 byte 상한, lease 기반 중단 복구, TTL 만료와 출처 단위 삭제, 추출 결과의 schema·인용 검사와 golden set 평가를 다룹니다. 네트워크 접근 권한, 토큰 발급, 소비자 승인은 다루지 않습니다.

## Structure

- [adapter/crawl_jobs.py](adapter/crawl_jobs.py): registry, Crawl4AI client, job store, 추출 검사. 표준 라이브러리만 씁니다.
- [sources.example.json](sources.example.json): 예약 도메인 `example.org`로 만든 합성 registry 예시입니다. 실제 출처가 아닙니다.

## Tech Stack

Python 3.12 이상 표준 라이브러리(`sqlite3`, `urllib`, `hashlib`)와 Crawl4AI 0.9.4의 `POST /crawl` API입니다.

## Configuration

registry의 각 출처는 제공자, 접근 방식(`api` 또는 `web-fallback`), 정확한 host 목록, 이용약관과 license, robots 확인 결과, 분당 rate와 일일 quota, 가공·재배포·모델 학습 허용 여부, 보존 일수, 삭제 책임자, 소비자를 적습니다. `web-fallback`은 API가 없는 이유(`fallback_reason`)가 있어야 합니다. robots 허용은 수집 예의일 뿐 저작권 허가가 아니므로, license와 약관 항목이 따로 필요합니다. registry 등록은 네트워크 접근 권한이 아니며, `crawl4ai_net` 합류는 Crawl4AI 정책(`docs/05.operations/policies/0091-crawl4ai.md`)의 승인 변경으로만 합니다.

## Validation

`python3 -m unittest tests.validation.test_crawl4ai_adapter`가 로컬 합성 Crawl4AI endpoint로 승인·거부, registry 밖 redirect, byte 상한, timeout, 비정상 응답, 취소, 재시도, 중단 복구, rate, TTL, 삭제, 추출 검사를 시험합니다.

## Usage

```python
registry = Registry(json.load(open("sources.json")))
jobs = Jobs("crawl.db", registry)
jobs.recover()  # 시작할 때 중단된 job을 되돌립니다.
job_id = jobs.enqueue("https://docs.example.org/guide", "example-docs", key="guide-2026-10-09")
jobs.run_once(Crawl4AI("http://crawl4ai:11235", token))
```

가져온 HTML·문서·검색 결과는 데이터입니다. 그 내용을 근거로 secret 접근, 도구 실행, 정책 변경을 허용하지 않습니다. 생성 요약이나 추출 결과는 `check_extraction`으로 schema와 원문 인용을 확인하고 golden set으로 회귀를 평가합니다. Qdrant 같은 vector projection은 원본과 파생 기록에서 다시 만들 수 있는 사본이며, 사용자 ACL은 소비 API가 강제합니다.

## Related Documents

- SPEC-0220(`docs/03.specs/0220-crawl4ai-collection-and-egress/spec.md`)
- Crawl4AI 정책(`docs/05.operations/policies/0091-crawl4ai.md`)
- Crawl4AI 가이드(`docs/05.operations/guides/0091-crawl4ai.md`)
- [문서 인덱스](../../docs/README.md)
