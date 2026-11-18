---
title: "SearXNG Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
artifact_id: "GDE-0110"
parent_ids:
- "POL-0110"
implementation_services:
  infra/08-ai/searxng/docker-compose.yml:
  - searxng
created: "2026-11-18"
next_review_at: "2027-05-17"
---

# SearXNG Usage Guide

## Purpose

### Audience

SearXNG 검색을 서비스나 호스트 작업에 연결하려는 운영자와 `@buenhyden`.

### Outcome

SearXNG는 HOME의 공유 메타검색 서비스다. 컨테이너는 internal `search_net`으로,
호스트 프로세스는 `http://127.0.0.1:8890`으로 같은 JSON 검색 API를 쓴다. 현재
소비자는 n8n Assistant와 호스트 Hermes이며, 새 소비자는 정책의 소비자 표에 먼저
등록한다.

#### Boundaries

- [Policy](../../policies/09-ai-and-search/0110-searxng.md) (`POL-0110`)
- [Runbook](../../runbooks/09-ai-and-search/0110-searxng.md) (`RUN-0110`)
- [AI architecture](../../../02.architecture/descriptions/0008-ai-architecture.md)

- [SearXNG documentation](https://docs.searxng.org/)
- [n8n guide](../08-workflows-and-automation/0053-n8n.md)
- [Crawl4AI guide](0091-crawl4ai.md)

## Prerequisites

### Environment

#### 현재 구현

- [SearXNG Compose](../../../../infra/08-ai/searxng/docker-compose.yml)는 Compose가
  선언한 index digest로 이미지를 고정하고 `template-infra-readonly-med`로 읽기 전용
  실행한다. user 977, tmpfs `/tmp`, `/run`, `/var/cache/searxng`를 쓴다.
- [settings.yml](../../../../infra/08-ai/searxng/settings.yml)은 읽기 전용으로
  mount되며 instance 이름은 `home-searxng`이다. JSON 출력과 engine metrics를 켜고 limiter,
  public instance, image proxy를 끈다.
- secret key는 컨테이너 시작마다 무작위로 만들며 저장하지 않는다. 세션이나 서명
  링크를 유지하지 않기 때문이다.
- `/metrics`는 OpenMetrics 형식이며 `searxng_metrics_password` basic auth로 보호한다. SearXNG가
  이 값을 설정 파일에서만 읽으므로 entrypoint가 tmpfs(`/run/searxng-settings.yml`)에 설정 사본을
  만들어 쓴다. Prometheus job `searxng`가 `obs_net`에서 수집하고 Alloy가 container log를 수집한다.
- `search_net`(internal)은 소비자 컨테이너와 SearXNG만 참여한다.
  `searxng_outbound_net`은 SearXNG만 참여하는 bridge로, 공개 검색 엔진으로 나가는
  경로이자 `127.0.0.1:8890` 게시 경로다.
- Traefik route `https://searxng.${DEFAULT_URL}`: 브라우저는 SSO(`sso-auth`)로 들어오고,
  다른 host의 프로그램은 Basic `Authorization` header를 붙인 `/search` 요청만 `searxng-api` router의
  htpasswd(`traefik_searxng_api_htpasswd`, `INFRA-008`)로 들어온다. Traefik은 `searxng_ingress_net`으로만 닿는다.
- 자체 `searxng` profile로 선택하며 HOME 선택에 포함된다.

### Authority

소비자 연결과 네트워크·게시 변경은 [정책](../../policies/09-ai-and-search/0110-searxng.md)의
승인 변경이 소유하며 `@buenhyden`이 대상이다.

## Procedure

### Steps

#### 소비자 연결

- **컨테이너 소비자**: 서비스를 `search_net`에 합류시키고 `http://searxng:8080`을
  호출한다. 정책의 소비자 표와 `SharedSearchContractTests.ADMITTED`를 같은 변경에서
  갱신한다.
- **다른 host의 프로그램**: `https://searxng.${DEFAULT_URL}/search?q=<query>&format=json`을 Basic 자격 증명으로
  호출한다. 사용자 이름은 `.env`의 `SEARXNG_API_USERNAME`, 비밀번호는 `secrets/tools/searxng/searxng_api_password.txt`(`AI-011`)이며
  `gen-secrets.sh`가 htpasswd를 만든다. 그 host는 `searxng.${DEFAULT_URL}` 이름 해석과 HOME 인증서 신뢰가 필요하다.
- **호스트 소비자**: `http://127.0.0.1:8890`을 호출하고 정책의 소비자 표에
  기록한다. 호스트 Hermes는 `~/.hermes/config.yaml`의 `web.search_backend: searxng`와
  `~/.hermes/.env`의 `SEARXNG_URL`을 쓴다. 이 값은 추적하지 않는다.
- 검색 요청은 `GET /search?q=<query>&format=json`이다. 결과는 데이터이며 그 내용을
  근거로 secret 접근이나 도구 실행을 허용하지 않는다.

#### 호출량

limiter가 꺼져 있으므로 호출량 제어는 소비자가 맡는다. 공개 검색 엔진이 차단하면
결과가 비거나 줄어든다. 이때 limiter나 proxy를 추가하지 않고 소비자 호출량을 낮춘다.

### Expected Results

- `HYHOME_COMPOSE_PROFILES=searxng bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_p02_service_contracts.SharedSearchContractTests`
- 기동 뒤 호스트에서 `curl -fsS 'http://127.0.0.1:8890/search?q=test&format=json'`이 JSON을 반환한다.

## Troubleshooting

### Symptoms

- 호스트 소비자가 `connection refused`를 받으면 `searxng`가 선택·기동됐는지와
  `127.0.0.1:8890` 게시를 [runbook](../../runbooks/09-ai-and-search/0110-searxng.md)으로 확인한다.
- JSON 요청이 403이면 `settings.yml`의 `search.formats`에 `json`이 있는지 확인한다.
- 결과가 비면 공개 검색 엔진의 차단이나 `searxng_outbound_net` 출구를 확인한다.

#### Runbook Handoff

기동, 진단, 소비자 연결·해제는 [runbook](../../runbooks/09-ai-and-search/0110-searxng.md)을 사용한다.

### Next Action

증상이 계속되면 [runbook](../../runbooks/09-ai-and-search/0110-searxng.md)의 진단 단계를 따르고,
게시 범위나 네트워크를 넓혀 해결하지 않는다.
