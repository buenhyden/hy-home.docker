---
title: "Crawl4AI Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0091"
parent_ids:
- "POL-0091"
implementation_services:
  infra/08-ai/crawl4ai/docker-compose.yml:
  - crawl4ai
created: "2026-09-21"
---

# Crawl4AI Usage Guide

## Usage

### Purpose and classification

Crawl4AI는 `crawl4ai`로만 선택되는 OPTIONAL 크롤러다. 예정된 소비자는
Open Notebook의 remote-crawler 설정이지만 아직 주석 처리되어 있어 지금은
이를 사용하는 서비스가 없다. 선택되기 전까지 유지 비용은 없으며, 다음
검토까지 연결된 소비자가 없으면 제거한다.

### Current implementation

- [Crawl4AI Compose](../../../infra/08-ai/crawl4ai/docker-compose.yml)는
  업스트림 이미지를 고정하고 `template-infra-high`를 4 GiB 메모리와 512
  PID 제한으로 확장하며 tmpfs 작업 경로와 함께 읽기 전용으로 실행한다.
- 서버는 `crawl4ai_api_token`이 필요하다. 토큰이 있으면 업스트림은
  `GET /health`를 제외한 모든 엔드포인트에서 `Authorization: Bearer`를
  요구한다.
- `crawl4ai_net`에만 참여한다. 호스트 포트와 Traefik 라우트는 없다.
- 이전에 추적되던 빈 `.llm.env`와 사용하지 않던 로컬 빌드 블록은
  제거했다. 프로바이더 키는 절대 커밋해서는 안 된다.

### SSRF boundary

크롤러는 호출자가 보낸 URL을 그대로 가져온다. 선언된 네트워크에 속하지
않으므로 내부 데이터베이스, OpenBao, Kafka Connect, 관리자 API는
컨테이너 이름으로 접근할 수 없다. 호스트와 LAN은 기본 라우트를 통해
여전히 접근 가능하므로, 호출자를 제한하고 네트워크 분리를 URL
허용목록으로 여기지 않는다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=crawl4ai bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`

## Runbook Handoff

토큰, 시작, 소비자 연결 작업은 [runbook](../runbooks/0091-crawl4ai.md)을 사용한다.

## Traceability

- [Policy](../policies/0091-crawl4ai.md) (`POL-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Related Documents

- [Crawl4AI self-hosting](https://docs.crawl4ai.com/core/self-hosting/)
- [Open Notebook guide](0073-open-notebook.md)
