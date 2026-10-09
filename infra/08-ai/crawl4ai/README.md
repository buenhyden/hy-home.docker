---
title: "Crawl4AI 웹 크롤러"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
created: "2026-09-21"
---

# Crawl4AI 웹 크롤러

> 토큰으로 보호되는 웹 크롤러로, Chromium으로 페이지를 렌더링하고 LLM에 바로 사용 가능한 Markdown을 반환합니다.

## Overview

Crawl4AI는 요청에 따라 임의의 URL을 가져오므로 서버 측 요청 위조(SSRF)에
악용될 수 있습니다. 그래서 `crawl4ai`는 `internal: true` 네트워크에만 참여하고, 밖으로 나가는 유일한 길은 `crawl4ai-egress` gateway입니다. gateway는 DNS를 중계하면서 AAAA 질의에는 빈 응답을 주고, 전역 라우팅되는 IPv4의 80·443 포트만 허용하며, 확인한 주소로만 연결합니다. 이미지 안의 egress broker가 먼저 대상을 확인하고 고정한 뒤 `CRAWL4AI_UPSTREAM_PROXY`로 gateway에 연결합니다. 의도된 소비자는 Open Notebook의 원격 크롤러 설정이지만 현재는 주석 처리되어 있어 이를 사용하는 서비스가 없습니다. Lifecycle: **OPTIONAL**, `crawl4ai`에서만 선택됩니다. 정확한 이미지로 격리 리허설을 실행해 허용 목적지 수집과 private·metadata·redirect·subresource·호출자 proxy 거절, 직접 경로 없음을 확인했습니다([SPEC-0220](../../../docs/03.specs/0220-crawl4ai-collection-and-egress/spec.md)). HOME 시작과 host 방화벽 적용은 하지 않았습니다.

## Audience

- **Operators**: 크롤러를 활성화하고 소비자를 연결할지 결정합니다.
- **AI agents**: 소유 Guide, Policy, Runbook 아래에서 이 패키지를 변경합니다.

## Scope

- **Included**: digest로 고정한 업스트림 이미지, 토큰 처리, internal 네트워크와 egress gateway, 리소스 제한.
- **Excluded**: LLM provider 키(이전에 추적되던 `.llm.env`는 제거됨), 소비자 연결, 출처 registry와 수집 job. 마지막 두 가지는 [수집 adapter](../../../projects/crawl4ai/README.md)를 쓰는 소비 워크스페이스가 소유합니다.

## Structure

```text
.
├── docker-compose.yml  # crawl4ai, crawl4ai-egress and their three networks
├── egress_gateway.py   # DNS relay and forward proxy run by crawl4ai-egress
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `crawl4ai` | [Compose](docker-compose.yml)에 선언된 업스트림 이미지 | 헤드리스 Chromium을 사용한 크롤링 API |
| `crawl4ai-egress` | 저장소의 `python:3.13.15-alpine`과 [egress_gateway.py](egress_gateway.py) | 크롤러의 유일한 외부 경로: DNS 중계와 forward proxy |

런타임 고정 값은 Compose 선언이 소유하고
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.

2026-10-04 확인한 [선정 버전의 공식 LICENSE](https://github.com/unclecode/crawl4ai/blob/133e1d92e37885dfccc03ea2e3687d06c98b7ceb/LICENSE)는
Apache 2.0 본문과 별도의 공개 사용·배포 출처 표시 조건을 포함합니다. 무료 자체 호스팅과
라이선스 의무를 구분하고 외부 공개 시 해당 조건을 검토합니다.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `crawl4ai`만 해당; `ai`, `notebook`, HOME에서는 선택되지 않음 |
| Network / port | `crawl4ai`는 `crawl4ai_net`(소비자용)과 `crawl4ai_egress_net`(`10.250.200.0/29`)에만 참여하며 둘 다 internal; 내부 `11235`를 `expose`로 노출; 호스트 포트·Traefik 라우트 없음. `crawl4ai-egress`(`10.250.200.2`)만 일반 bridge `crawl4ai_outbound_net`에 참여 |
| Egress | 크롤러의 `dns`와 `CRAWL4AI_UPSTREAM_PROXY`가 gateway를 가리킴; gateway는 전역 IPv4의 80·443만 허용하고 IPv6는 모두 거절하며 host와 주소만 기록 |
| Authentication | 시크릿 `crawl4ai_api_token`(AI-006)이 `CRAWL4AI_API_TOKEN`으로 내보내짐; protected data/admin API의 Bearer/JWT 인증과 health·root·monitor·token·UI/static 예외를 구분함; 정확한 버전별 범위와 `/token` 제한은 GDE/POL-0091 참조 |
| Hardening | `template-infra-high`, `cap_drop: ALL`, `no-new-privileges`, tmpfs 작업 경로를 사용하는 읽기 전용 루트, `mem_limit: 4g`, `pids_limit: 512`, 전용 `shm_size`. gateway는 `template-infra-readonly-low`, `65534:65534`, capability 대신 `net.ipv4.ip_unprivileged_port_start=53` |
| Persistence | 없음; 출력과 캐시는 tmpfs |
| Health | `GET /health` (설계상 인증 없음); API 응답 여부만 증명하며 브라우저 렌더링을 증명하지는 않음 |

## Validation

- `HYHOME_COMPOSE_PROFILES=crawl4ai bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 -m unittest tests.validation.test_crawl4ai_egress` (격리 리허설은 `HYHOME_CRAWL4AI_REHEARSAL=1`)

## Usage

1. 등록된 시크릿 워크플로우를 통해 `secrets/tools/crawl4ai/crawl4ai_api_token.txt`를 생성합니다.
2. 승인된 대상으로만 시작합니다: `docker compose --profile crawl4ai up -d crawl4ai` (gateway가 healthy가 된 뒤 크롤러가 시작됩니다).
3. 소비자는 [Crawl4AI 정책](../../../docs/05.operations/policies/0091-crawl4ai.md)의 승인 변경으로만 `crawl4ai_net`에 추가합니다. 크롤러를 다른 저장소 네트워크에 추가하지 않습니다.

## Related Documents

- **Guide**: Crawl4AI usage guide (`docs/05.operations/guides/0091-crawl4ai.md`)
- **Policy**: Crawl4AI operations policy (`docs/05.operations/policies/0091-crawl4ai.md`)
- **Runbook**: Crawl4AI recovery runbook (`docs/05.operations/runbooks/0091-crawl4ai.md`)
- [Documentation index](../../../docs/README.md)
