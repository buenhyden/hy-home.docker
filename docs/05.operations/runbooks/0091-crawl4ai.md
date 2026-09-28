---
title: "Crawl4AI Recovery Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0091"
parent_ids:
- "GDE-0091"
created: "2026-09-21"
---

# Crawl4AI Recovery Runbook

## When to Use

시작 실패, 토큰 노출, 메모리 압박, 컨슈머 연결/해제 시 사용한다.

## Procedure

1. 점검한다.

   ```bash
   docker compose --profile crawl4ai config --quiet
   docker compose --profile crawl4ai ps -a crawl4ai
   docker compose --profile crawl4ai logs --tail=100 crawl4ai
   ```

2. `64` 종료는 토큰 시크릿이 없거나 16자 미만임을 의미한다.
3. 토큰 노출 시: 서비스를 정지하고, `secrets/tools/crawl4ai_api_token.txt`를
   교체하고, 컨슈머의 토큰을 업데이트한 뒤 다시 시작한다.
4. 반복적인 메모리 부족 재시작 시, `mem_limit`을 올리기 전에 호출자 측에서
   crawl 동시성을 낮춘다.
5. 서비스를 제거하려면 정지하고, 하나의 검토된 변경으로 include와 패키지를
   삭제하고, AI-006 시크릿 행을 폐기한다. 이는 데이터를 담고 있지 않다.

## Evidence

종료 코드, 이미지, 소스 커밋을 기록한다. 토큰이나 크롤링된 내용은 기록하지
않는다.

## Rollback or Recovery

영속 상태가 존재하지 않는다. 롤백은 Compose 되돌리기와 재시작이다.

## Escalation

크롤러를 선언된 네트워크에 연결하거나 공개적으로 노출하라는 요청이 있으면
중단한다.

## Traceability

- [Guide](../guides/0091-crawl4ai.md) (`GDE-0091`)
- [Policy](../policies/0091-crawl4ai.md) (`POL-0091`)
- [Crawl4AI Compose](../../../infra/08-ai/crawl4ai/docker-compose.yml)

## Related Documents

- [Crawl4AI self-hosting](https://docs.crawl4ai.com/core/self-hosting/)
