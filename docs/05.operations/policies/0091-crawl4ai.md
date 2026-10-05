---
title: "Crawl4AI Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0091"
parent_ids:
- "AD-0008"
created: "2026-09-21"
---

# Crawl4AI Operations Policy

## Overview

### Overview

Crawl4AI는 SSRF가 가능한 서비스다. 검토된 consumer가 필요로 할 때까지 격리하고
인증을 적용한 채 사용하지 않는 상태로 유지한다.

## Scope

### Policy Scope

활성화, 네트워크 배치, 인증, consumer, provider key, 제거.

### Traceability

- [Guide](../guides/0091-crawl4ai.md) (`GDE-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Rules

### Controls

- `crawl4ai`를 통해서만 선택한다. `ai`, `notebook`, HOME에 절대 추가하지 않는다.
- 전용 `crawl4ai_net` 밖의 공유 서비스 네트워크에 연결하거나 host 포트를 게시하거나 public route를 추가하지
  않는다.
- 항상 token secret과 함께 실행한다. provider key를 추적되는 파일로 전달하지 않는다.
- consumer는 `crawl4ai_net`에 해당 consumer를 추가하고 그 토큰도 설정하는 검토된
  변경으로만 연결한다.

### Verification

정적 렌더링과 template baseline을 확인한다. 승인된 런타임 검증은 `/health`와
명시된 공개 shell/토큰 경로를 구분하고, protected data/admin API의 토큰 없는 요청은
401이어야 한다. `mng-pg`/`openbao` DNS 분리만으로 host/LAN egress 차단을
증명하지 않는다. URL/redirect/목적지 통제와 consumer 인증을 따로 검증한다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

이미지 업그레이드나 consumer 연결 시, 그리고 service rationalization 검토 때마다
검토한다. consumer가 여전히 없으면 @buenhyden의 승인된 제거 변경으로 넘긴다. Secret 폐기는 소비자·유출·보존 상태를 확인한 별도 결정이다.

## Exceptions

### Exceptions

선언 버전의 `/health`, `/token`, root/monitor 및 UI/static shell 예외를 인정하되 protected data/admin API 인증은 유지한다. `/token`은 별도 key/email 검증을 하며 임의 token 발급 예외가 아니다. 새로운 예외는 승인된 변경 없이는 추가하지 않는다.

## Related Documents

- [Crawl4AI Compose source](../../../infra/08-ai/crawl4ai/docker-compose.yml)
