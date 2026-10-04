---
title: "Crawl4AI 웹 크롤러"
version: "1.0.5"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-09-21"
---

# Crawl4AI 웹 크롤러

> 토큰으로 보호되는 웹 크롤러로, Chromium으로 페이지를 렌더링하고 LLM에 바로 사용 가능한 Markdown을 반환합니다.

## Overview

Crawl4AI는 요청에 따라 임의의 URL을 가져오므로 서버 측 요청 위조(SSRF)에
악용될 수 있습니다. 따라서 전용 `crawl4ai_net` 이그레스 네트워크에 격리되어
있으며 다른 저장소 네트워크에는 절대 참여하지 않습니다. 의도된 소비자는
Open Notebook의 원격 크롤러 설정이지만 현재는 주석 처리되어 있어 오늘
시점에는 이를 사용하는 서비스가 없습니다. Lifecycle: **OPTIONAL**, `crawl4ai`에서만 선택됩니다.
별도 bridge와 토큰은 실제 호스트·LAN·메타데이터 목적지의 이그레스 거절을 증명하지
않습니다. 정확한 이미지에서 DNS·redirect 거절과 실행 경계를 확인하는 시험은 미실행입니다.

## Audience

- **Operators**: 크롤러를 활성화하고 소비자를 연결할지 결정합니다.
- **AI agents**: 소유 Guide, Policy, Runbook 아래에서 이 패키지를 변경합니다.

## Scope

- **Included**: 고정된 업스트림 이미지, 토큰 처리, 네트워크 격리, 리소스 제한.
- **Excluded**: LLM provider 키(이전에 추적되던 `.llm.env`는 제거됨), 소비자 연결.

## Structure

```text
.
├── docker-compose.yml  # crawl4ai service and crawl4ai_net
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `crawl4ai` | [Compose](docker-compose.yml)에 선언된 업스트림 이미지 | 헤드리스 Chromium을 사용한 크롤링 API |

런타임 고정 값은 Compose 선언이 소유하고
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.

2026-10-04 확인한 [선정 버전의 공식 LICENSE](https://github.com/unclecode/crawl4ai/blob/133e1d92e37885dfccc03ea2e3687d06c98b7ceb/LICENSE)는
Apache 2.0 본문과 별도의 공개 사용·배포 출처 표시 조건을 포함합니다. 무료 자체 호스팅과
라이선스 의무를 구분하고 외부 공개 시 해당 조건을 검토합니다.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `crawl4ai`만 해당; `ai`, `notebook`, HOME에서는 선택되지 않음 |
| Network / port | `crawl4ai_net`만 해당; 내부 `11235`를 `expose`로 노출; 호스트 포트 없음, Traefik 라우트 없음 |
| Authentication | 시크릿 `crawl4ai_api_token`(AI-006)이 `CRAWL4AI_API_TOKEN`으로 내보내짐; protected data/admin API의 Bearer/JWT 인증과 health·root·monitor·token·UI/static 예외를 구분함; 정확한 버전별 범위와 `/token` 제한은 GDE/POL-0091 참조 |
| Hardening | `template-infra-high`, `cap_drop: ALL`, `no-new-privileges`, tmpfs 작업 경로를 사용하는 읽기 전용 루트, `mem_limit: 4g`, `pids_limit: 512`, 전용 `shm_size` |
| Persistence | 없음; 출력과 캐시는 tmpfs |
| Health | `GET /health` (설계상 인증 없음); API 응답 여부만 증명하며 브라우저 렌더링을 증명하지는 않음 |

## Validation

- `HYHOME_COMPOSE_PROFILES=crawl4ai bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`

## Usage

1. 등록된 시크릿 워크플로우를 통해 `secrets/tools/crawl4ai/crawl4ai_api_token.txt`를 생성합니다.
2. 승인된 대상으로만 시작합니다: `docker compose --profile crawl4ai up -d crawl4ai`.
3. Open Notebook을 연결하려면 해당 서비스에 `crawl4ai_net`을 추가하고 `CRAWL4AI_API_URL`과
   토큰을 하나의 검토된 변경으로 설정합니다. 크롤러를 다른 저장소 네트워크에 추가하지 않습니다.

## Related Documents

- **Guide**: Crawl4AI usage guide (`docs/05.operations/guides/0091-crawl4ai.md`)
- **Policy**: Crawl4AI operations policy (`docs/05.operations/policies/0091-crawl4ai.md`)
- **Runbook**: Crawl4AI recovery runbook (`docs/05.operations/runbooks/0091-crawl4ai.md`)
- [Documentation index](../../../docs/README.md)
