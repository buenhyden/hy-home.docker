---
title: "SearXNG 공유 메타검색"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-11-18"
---

# SearXNG 공유 메타검색

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

> 여러 검색 엔진의 결과를 모아 JSON으로 돌려주는 HOME 공유 검색 서비스입니다.

#### Service

##### Purpose

`searxng`는 n8n Assistant, 호스트 Hermes 같은 여러 소비자가 같은 검색 API를 쓰도록
제공합니다. 고정된 검색 엔진만 조회하며 호출자가 준 URL을 가져오지 않습니다. 임의
URL 수집은 [Crawl4AI](../crawl4ai/README.md)가 맡습니다.

###### Audience
<!-- core-payload-level:4 -->

- 검색을 서비스나 호스트 작업에 연결하는 운영자
- `@buenhyden`

###### Scope
<!-- core-payload-level:4 -->

- 포함: SearXNG 컨테이너, 읽기 전용 `settings.yml`, `search_net`과 `searxng_outbound_net`, 호스트 loopback 게시, Prometheus `/metrics`
- 제외: 소비자 쪽 설정(Hermes `~/.hermes/config.yaml`·`.env`, n8n 환경 변수)

###### Structure
<!-- core-payload-level:4 -->

```text
searxng/
├── docker-compose.yml  # searxng 서비스와 search_net, searxng_outbound_net
├── settings.yml        # instance home-searxng, JSON 출력, limiter 끔, metrics 켬
└── README.md           # This file
```

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `http://searxng:8080` (`search_net`) | `searxng` | 승인된 컨테이너(현재 `n8n` main) | `GET /search?q=<query>&format=json` | 소비자의 검색 기능만 실패한다 |
| `http://127.0.0.1:8890` (호스트 loopback) | `searxng` | 호스트 프로세스(현재 Hermes) | 같은 JSON API | Hermes는 Firecrawl 대체 경로를 쓴다 |
| `https://searxng.${DEFAULT_URL}` (Traefik) | `searxng` | 브라우저(SSO), 다른 host의 프로그램(`/search` + Basic) | SSO 또는 htpasswd `INFRA-008` | Traefik이 인증 없는 요청을 거부한다 |
| `http://searxng:8080/metrics` (`obs_net`) | `searxng` | Prometheus job `searxng` | OpenMetrics, basic auth `searxng_metrics_password` | scrape 실패는 `up{job="searxng"} == 0`으로 보인다 |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

호스트로 게시하는 포트는 `127.0.0.1:8890`(컨테이너 `8080`) 하나다. 연결 네트워크는
`search_net`(internal), `searxng_outbound_net`, `obs_net`, `searxng_ingress_net`(Traefik 전용)이다. secret은
`searxng_metrics_password` 하나이며, secret key는 시작마다 무작위로 만든다. 런타임 고정 값은 [Compose](docker-compose.yml) 선언이 소유하고
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증한다.
(출처: `infra/08-ai/searxng/docker-compose.yml`의 `searxng` 서비스)

###### Security Boundary
<!-- core-payload-level:4 -->

SearXNG 자체에는 인증이 없으므로 loopback·internal 망 밖으로는 Traefik을 거쳐서만 노출한다. 브라우저는
SSO로, 다른 host의 프로그램은 `/search`에 Basic 자격 증명(`searxng-api-auth`)으로 들어온다. `search_net`에는 `POL-0110`의
소비자 표에 있는 서비스만 합류한다. `/metrics` 비밀번호는 entrypoint가 tmpfs의 설정
사본에만 쓰며 추적 파일에 남지 않는다. 검색 결과는 데이터이며 명령으로 취급하지 않는다.

#### Usage

##### Prerequisites

- Docker Compose와 저장소 root의 `docker-compose.yml`
- `secrets/observability/searxng/searxng_metrics_password.txt`(따옴표·`|`·`&`·역슬래시 없는 값)
- 공개 검색 엔진에 닿는 인터넷 출구

##### Selected Start

HOME 선택에 포함된다. 단독으로는 아래처럼 선택한다. 기동은 별도 승인을 받는다.

```bash
docker compose --profile searxng up -d searxng
```

#### Checks

##### Readiness

Compose healthcheck가 컨테이너 안에서 `/healthz`를 확인한다. 호스트에서는 아래로 확인한다.

```bash
curl -fsS 'http://127.0.0.1:8890/search?q=test&format=json' | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["results"]))'
```

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- SearXNG 가이드 (`GDE-0110`)
- SearXNG 정책 (`POL-0110`)
- SearXNG 복구 런북 (`RUN-0110`)
- [AI tier README](../README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

Prometheus job `searxng`가 엔진별 요청·오류·응답 시간과 신뢰도를 `/metrics`에서 수집하고,
Alloy가 container log를 수집한다. 영속 데이터가 없으므로 복구는 승인된 Compose 선언으로
재생성하는 것이다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
