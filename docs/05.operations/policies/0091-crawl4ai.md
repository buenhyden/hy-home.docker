---
title: "Crawl4AI Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0091"
parent_ids:
- "AD-0008"
created: "2026-09-21"
---

# Crawl4AI Operations Policy

## Overview

Crawl4AI는 SSRF가 가능한 서비스다. 검토된 consumer가 필요로 할 때까지 격리하고
인증을 적용한 채 사용하지 않는 상태로 유지한다.

## Policy Scope

활성화, 네트워크 배치, 인증, consumer, provider key, 제거.

## Controls

- `crawl4ai`를 통해서만 선택한다. `ai`, `notebook`, HOME에 절대 추가하지 않는다.
- 선언된 네트워크에 연결하거나 host 포트를 게시하거나 public route를 추가하지
  않는다.
- 항상 token secret과 함께 실행한다. provider key를 추적되는 파일로 전달하지 않는다.
- consumer는 `crawl4ai_net`에 해당 consumer를 추가하고 그 토큰도 설정하는 검토된
  변경으로만 연결한다.

## Exceptions

`GET /health`는 인증되지 않은 upstream 동작이다.

## Verification

정적 렌더링과 template baseline. 런타임: `/health` 200, 다른 endpoint는 토큰 없이 401,
컨테이너에서 `mng-pg`나 `openbao`가 resolve되지 않는다.

## Review Cadence

이미지 업그레이드나 consumer 연결 시, 그리고 service rationalization 검토 때마다
검토한다. consumer가 여전히 없으면 패키지를 제거한다.

## Traceability

- [Guide](../guides/0091-crawl4ai.md) (`GDE-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Related Documents

- [Crawl4AI Compose source](../../../infra/08-ai/crawl4ai/docker-compose.yml)
