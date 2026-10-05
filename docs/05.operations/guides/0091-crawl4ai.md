---
title: "Crawl4AI Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
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

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Purpose and classification

Crawl4AI는 `crawl4ai`로만 선택되는 OPTIONAL 크롤러다. 예정된 소비자는
Open Notebook의 remote-crawler 설정이지만 아직 주석 처리되어 있어 지금은
이를 사용하는 서비스가 없다. 선택하지 않으면 실행 자원을 소비하지 않지만 image/source 관리 비용은 남는다. 다음
검토에도 소비자가 없으면 승인된 제거 절차로 넘긴다.

### Current implementation

- [Crawl4AI Compose](../../../infra/08-ai/crawl4ai/docker-compose.yml)는
  2026-10-03 확인한 [공식 보안 릴리스](https://github.com/unclecode/crawl4ai/releases)에 맞춰 이미지를 고정하고 `template-infra-high`를 4 GiB 메모리와 512
  PID 제한으로 확장하며 tmpfs 작업 경로와 함께 읽기 전용으로 실행한다. 릴리스의 URL·redirect·robots·link preview 수정은 HOME egress 차단이나 실제 요청 검증의 증거가 아니다.
- 서버는 `crawl4ai_api_token`이 필요하다. 토큰이 있으면 업스트림은
  protected data/admin API에 Bearer/JWT 인증을 적용한다. Health, root,
  monitor, token route 및 UI/static shell에는 버전별 예외가 있다. `/token`은
  별도 key/email 검증을 수행하므로 공개 토큰 발급으로 해석하지 않는다.
- `crawl4ai_net`에만 참여한다. 호스트 포트와 Traefik 라우트는 없다.
- 이전에 추적되던 빈 `.llm.env`와 사용하지 않던 로컬 빌드 블록은
  제거했다. 프로바이더 키는 절대 커밋해서는 안 된다.

### SSRF boundary

크롤러는 호출자 URL을 가져오며 SSRF 경계 검증이 필요하다. 기존 공유 서비스 네트워크에 속하지
않으므로 내부 데이터베이스, OpenBao, Kafka Connect, 관리자 API는
컨테이너 이름으로 접근할 수 없다. 호스트와 LAN은 기본 라우트를 통해
여전히 접근 가능하므로, 호출자를 제한하고 네트워크 분리를 URL
허용목록으로 여기지 않는다.

### Common Checks

- `HYHOME_COMPOSE_PROFILES=crawl4ai bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`

### Runbook Handoff

토큰, 시작, 소비자 연결 작업은 [runbook](../runbooks/0091-crawl4ai.md)을 사용한다.

### Traceability

- [Policy](../policies/0091-crawl4ai.md) (`POL-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Related Documents

- [Crawl4AI self-hosting](https://docs.crawl4ai.com/core/self-hosting/)
- [Open Notebook guide](0073-open-notebook.md)
