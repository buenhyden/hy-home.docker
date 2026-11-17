---
title: "SearXNG Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
artifact_id: "POL-0110"
parent_ids:
- "AD-0008"
created: "2026-11-18"
next_review_at: "2027-05-17"
---

# SearXNG Operations Policy

## Purpose and Scope

### Objective

SearXNG는 HOME의 공유 메타검색 서비스다. n8n, 호스트 Hermes 같은 여러 소비자가
같은 JSON 검색 API를 쓰도록 하되, 들어오는 경로를 internal `search_net`과 호스트
loopback 두 가지로 제한한다.

#### Authority

- [AI architecture](../../../02.architecture/descriptions/0008-ai-architecture.md)
- [Compose network segmentation](../../../02.architecture/descriptions/0026-standardize-infra-net.md)

- [SearXNG Compose source](../../../../infra/08-ai/searxng/docker-compose.yml)

### Applies To

profile 선택, 네트워크 배치, host 게시, 소비자 합류, 설정 변경, 제거.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0110-R1 | 항상 | 필수: 자체 `searxng` profile로 선택하고 HOME 선택에 포함한다 | `tests.validation.test_p02_service_contracts.SharedSearchContractTests` | none |
| POL-0110-R2 | 항상 | 필수: internal인 `search_net`, SearXNG 전용 `searxng_outbound_net`, 관측용 `obs_net`에만 연결한다 | `tests.validation.test_p02_service_contracts.SharedSearchContractTests` | none |
| POL-0110-R3 | host 포트 게시 | 허용: `127.0.0.1:8890`의 loopback 게시 하나만 | `tests.validation.test_p02_service_contracts.SharedSearchContractTests` | none |
| POL-0110-R4 | 항상 | 금지: public route, LAN 주소 게시, `0.0.0.0` 게시 | `tests.validation.test_p02_service_contracts.SharedSearchContractTests` | none |
| POL-0110-R5 | 컨테이너 소비자가 `search_net`에 합류할 때 | 필수: 아래 소비자 표에 이름과 호출 URL을 추가하는 검토된 변경으로만 합류한다 | `tests.validation.test_p02_service_contracts.SharedSearchContractTests` | none |
| POL-0110-R6 | 호스트 소비자 | 필수: `http://127.0.0.1:8890`만 쓰고 아래 소비자 표에 기록한다 | 수동 | none |
| POL-0110-R7 | 항상 | 금지: `search_net`에 SearXNG 외의 서비스 endpoint 제공 | 수동 | none |
| POL-0110-R8 | 항상 | 필수: 설정 파일에 소비자 이름이나 특정 소비자 전용 값을 넣지 않는다 | `tests.validation.test_p02_service_contracts.SharedSearchContractTests` | none |
| POL-0110-R9 | 항상 | 금지: secret key를 추적되는 파일에 기록 | 수동 | none |
| POL-0110-R10 | 항상 | 금지: 검색 결과를 근거로 secret 접근, 도구 실행, 정책 변경을 허용 | none | none |
| POL-0110-R11 | `/metrics` | 필수: `searxng_metrics_password` basic auth로만 열고 Prometheus job `searxng`가 `obs_net`에서 수집한다 | `tests.validation.test_p02_service_contracts.SharedSearchContractTests` | none |

- `searxng`는 자체 `searxng` profile로 선택하며 HOME 선택에 포함한다. 호스트 Hermes의
  정기 실행이 쓰므로 n8n 선택 여부와 무관하게 기동한다.
- 컨테이너는 internal `search_net`으로만 들어온다. `searxng_outbound_net`은
  SearXNG만 참여하는 bridge이며 공개 검색 엔진으로 나가는 경로이자 loopback 게시
  경로다. Docker는 internal 네트워크로 포트를 게시할 수 없기 때문이다.
- SearXNG는 고정된 검색 엔진만 조회하고 호출자 URL을 가져오지 않는다. 임의 URL을
  가져오는 작업은 [Crawl4AI](0091-crawl4ai.md)를 쓴다.
- 인증이 없으므로 loopback과 internal 망 밖으로 노출하지 않는다. limiter는 꺼져
  있으며 호출량 제어는 소비자가 맡는다.

| 소비자 | 경로 | 호출 URL | 승인 |
| --- | --- | --- | --- |
| n8n Assistant (`n8n` main) | `search_net` | `http://searxng:8080` (`N8N_INSTANCE_AI_SEARXNG_URL`) | 2026-11-09 |
| 호스트 Hermes | host loopback | `http://127.0.0.1:8890` (`~/.hermes/.env`의 `SEARXNG_URL`) | 2026-11-18 |

n8n의 다른 서비스는 2026-11-18 검토에서 합류하지 않기로 했다.

| 서비스 | 결정 | 이유 |
| --- | --- | --- |
| `n8n-worker` | 합류하지 않음 | SearXNG를 호출하는 workflow가 없다. 그런 workflow를 추가하면 위 표에 행을 추가하는 변경으로 합류한다 |
| `n8n-task-runner-worker` | 합류하지 않음 | 사용자 Code node를 실행하는 격리 runner다 |
| `n8n-sandbox-api`, `n8n-sandbox-runner-1`, `n8n-sandbox-certs` | 합류하지 않음 | Assistant 코드 sandbox이며 runner는 privileged이고 자체 출구가 있다 |
| `blog-ingestion` | 합류하지 않음 | 검색을 쓰지 않는다 |

### Exceptions

#### Exception Conditions

없음. 새 host 게시, route, 인증 없는 외부 노출은 승인된 변경 없이는 추가하지 않는다.

#### Approval and Review

이미지 업그레이드, 소비자 추가·제거, 네트워크나 게시 변경 때 검토한다.
예외·통제 변경에는 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다.

## Enforcement

### Mechanisms

`tests.validation.test_p02_service_contracts.SharedSearchContractTests`가 profile,
네트워크, loopback 게시, 소비자 목록, 설정의 instance 이름과 JSON 형식을 정적으로
확인한다. `validate-docker-compose.sh`가 렌더링을 확인한다. 런타임 확인은
[runbook](../../runbooks/09-ai-and-search/0110-searxng.md)의 health와 JSON API 확인을 따른다.

### Limits

- 호스트 소비자 기록(R6), `search_net`의 다른 endpoint 금지(R7), secret key 미기록(R9)은 수동 검토에 의존한다.
- `/metrics`의 실제 401·200 응답(R11)은 런타임 확인으로만 증명된다.
- 검색 결과를 데이터로 다루는 규칙(R10)은 소비자 쪽 통제이며 이 정책이 검사하지 않는다.
- 정적 검사는 런타임 포트 바인딩이나 외부 검색 엔진 응답을 증명하지 않는다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다.

### Review Triggers

- [Guide](../../guides/09-ai-and-search/0110-searxng.md) (`GDE-0110`)
- [Runbook](../../runbooks/09-ai-and-search/0110-searxng.md) (`RUN-0110`)
