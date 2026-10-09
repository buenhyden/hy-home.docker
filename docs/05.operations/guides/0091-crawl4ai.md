---
title: "Crawl4AI Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "operations"
artifact_id: "GDE-0091"
parent_ids:
- "POL-0091"
implementation_services:
  infra/08-ai/crawl4ai/docker-compose.yml:
  - crawl4ai
  - crawl4ai-egress
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
- `crawl4ai`는 internal인 `crawl4ai_net`(소비자용)과 `crawl4ai_egress_net`에만 참여한다. 호스트 포트와 Traefik 라우트는 없다. 밖으로 나가는 경로는 [egress gateway](../../../infra/08-ai/crawl4ai/egress_gateway.py)를 실행하는 `crawl4ai-egress` 하나다.
- 이미지는 0.9.4 index digest로 고정한다. 2026-10-09 기준 공개 advisory 중 0.9.4를 포함하는 것은 없고, GHSA-6qhc-x826-342c는 `<=0.8.8`에 해당한다([SPEC-0220](../../03.specs/0220-crawl4ai-collection-and-egress/spec.md)).
- 이전에 추적되던 빈 `.llm.env`와 사용하지 않던 로컬 빌드 블록은
  제거했다. 프로바이더 키는 절대 커밋해서는 안 된다.

### SSRF boundary

크롤러는 호출자 URL을 가져오므로 SSRF 방어가 두 겹이다. 이미지 안의 broker는 전역이 아닌 주소를 거절하고, Chromium을 고정 proxy로 보내며, 호출자의 proxy·`extra_args`·script를 막고, redirect와 robots·link preview 요청을 다시 확인한다. 그다음 컨테이너 밖의 `crawl4ai-egress`가 같은 규칙을 다시 적용한다. 크롤러에는 기본 라우트가 없으므로 broker를 우회한 연결은 갈 곳이 없다. gateway는 DNS 중계에서 AAAA에 빈 응답을 주고, proxy에서 이름을 직접 해석해 확인한 주소로만 연결하므로 DNS 응답이 바뀌어도 목적지가 바뀌지 않는다.

남는 위험은 세 가지다. 같은 `crawl4ai_net`의 consumer는 네트워크 계층에서 크롤러에 노출된다. DNS 질의는 relay를 거쳐 밖으로 나간다. 공인 주소가 router NAT로 LAN에 되돌아오는 host는 주소만으로 알 수 없다. 그래서 consumer는 자기 서비스를 인증하고, 등록된 출처만 수집한다.

### 소비자 승인과 출처 권리

consumer 연결은 [정책](../policies/0091-crawl4ai.md)의 승인 변경이 소유한다. 출처 registry, 제한된 job, 원본 출처 보존, 파생 결과 삭제는 소비 워크스페이스가 [수집 adapter](../../../projects/crawl4ai/README.md)로 구현한다. 후보 프로젝트 세 가지(공공 API 문서 변경 감시, 허용 공지·법령 근거 노트, 라이선스 검증 학습자료)의 비교는 [SPEC-0220 계획](../../03.specs/0220-crawl4ai-collection-and-egress/plan.md)에 있으며, 아직 연결된 것은 없다.

### Common Checks

- `HYHOME_COMPOSE_PROFILES=crawl4ai bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 -m unittest tests.validation.test_crawl4ai_egress tests.validation.test_crawl4ai_adapter`

### Runbook Handoff

토큰, 시작, 소비자 연결 작업은 [runbook](../runbooks/0091-crawl4ai.md)을 사용한다.

### Traceability

- [Policy](../policies/0091-crawl4ai.md) (`POL-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Related Documents

- [Crawl4AI self-hosting](https://docs.crawl4ai.com/core/self-hosting/)
- [Open Notebook guide](0073-open-notebook.md)
