---
title: "SearXNG Recovery Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
artifact_id: "RUN-0110"
parent_ids:
- "GDE-0110"
created: "2026-11-18"
next_review_at: "2027-05-17"
---

# SearXNG Recovery Runbook

## Trigger and Scope

### Trigger

이 런북은 공유 `searxng`(profile `searxng`)의 기동 실패, 소비자의 연결 거부, 빈
검색 결과, 소비자 연결·해제와 제거를 다룬다.

기동 실패, 호스트 소비자의 `connection refused`, JSON API 오류, 소비자 연결·해제 시 사용한다.

### Targets

- [Guide](../../guides/09-ai-and-search/0110-searxng.md) (`GDE-0110`)
- [Policy](../../policies/09-ai-and-search/0110-searxng.md) (`POL-0110`)
- [SearXNG Compose](../../../../infra/08-ai/searxng/docker-compose.yml)

- [SearXNG documentation](https://docs.searxng.org/)

## Preflight

### Authority

승인과 실행 경계는 아래 항목에 따른다.

#### Execution Boundary

저장소 root에서 `searxng` service와 profile만 선택한다. 기동·재생성은 별도 승인을
받는다. `restart`는 바뀐 Compose 설정이나 `settings.yml` bind를 다시 읽지 않으므로
설정 변경은 재생성으로 적용한다. 재생성 중에는 소비자 검색이 실패하므로 정기 작업
시간(Hermes 매일 07:00 KST)을 피한다. Log를 보존할 때 검색어와 결과 본문은 남기지 않는다.
전체 기동·중지는 [cold-start Runbook](../01-common/0098-cold-start-and-reboot.md)을 따른다.

### Environment

작업 전 점검은 아래 항목에 따른다.

#### Service lifecycle prerequisites

durable volume은 없고 cache는 tmpfs다. secret key는 시작마다 새로 만들므로 재생성으로
잃는 상태가 없다. n8n main이 `search_net`에 합류해 있으므로 네트워크를 지우거나 바꾸면
n8n 재생성이 함께 필요하다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 진단: config, ps, logs, health를 확인한다 | `searxng`가 healthy이고 `127.0.0.1:8890->8080` 게시가 보인다 | Stop Conditions에 따라 @buenhyden에게 escalation |
| 2 | 진단: 호스트에서 JSON API를 호출한다 | JSON 응답과 `results` 필드 | 403이면 `search.formats`, 빈 결과면 출구를 확인한다 |
| 3 | 승인된 기동·재생성: `searxng`만 대상으로 한다 | healthy와 JSON 응답 | 이전 선언으로 되돌린다 |
| 4 | 소비자 연결·해제: 정책 소비자 표와 테스트 목록을 같은 변경에서 갱신한다 | 계약 테스트 통과 | 변경을 되돌린다 |
| 5 | 제거 승인 시: 소비자를 먼저 해제하고 include와 문서를 정리한다 | 소비자가 남지 않음 | 중단하고 escalation |

#### 진단과 복구 단계

1. 점검한다.

   ```bash
   docker compose --profile searxng config --quiet
   docker compose --profile searxng ps -a searxng
   docker compose --profile searxng logs --tail=100 searxng
   docker port searxng
   ```

2. `64` 종료는 `searxng_metrics_password`가 없거나 비었거나 따옴표·`|`·`&`·역슬래시를 포함함을 뜻한다. secret 소유자 절차로 값을 고친 뒤 재생성한다. Prometheus에서 `up{job="searxng"}`가 0이면 `obs_net` 합류와 비밀번호 일치를 확인한다.

   Traefik route는 `SEARXNG_API_USERNAME`과 `AI-011` 파일 값을 담은 권한 0600의 netrc 파일로 확인한다. 비밀번호를 명령 인자에 넣지 않는다: `curl -fsS --netrc-file <netrc> 'https://searxng.${DEFAULT_URL}/search?q=test&format=json'`. 자격 증명 없는 `/search`는 SSO로 넘어가고, 틀린 자격 증명은 401이다.

   호스트에서 JSON API를 확인한다. 검색어는 무해한 고정 값만 쓴다.

   ```bash
   curl -fsS 'http://127.0.0.1:8890/search?q=test&format=json' | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["results"]))'
   ```

3. 승인을 받은 뒤 기동하거나 재생성한다.

   ```bash
   docker compose --profile searxng up -d searxng
   ```

4. 소비자를 연결하거나 해제할 때는 정책의 소비자 표와
   `tests.validation.test_p02_service_contracts.SharedSearchContractTests.ADMITTED`를 함께 고친다.
5. 제거 승인을 받으면 호스트 소비자 설정(Hermes `web.search_backend`)과 컨테이너
   소비자(`search_net` 합류)를 먼저 해제한 뒤 include와 문서를 정리한다.

### Stop Conditions

`0.0.0.0`이나 LAN 주소 게시, 인증 없는 Traefik route, `search_net`에 승인되지 않은 서비스
합류, 예상 밖 출력, 복구 실패이면 중단한다.

## Verification

### Expected Results

#### Service Checks

`searxng`가 healthy이고, `docker port searxng`가 `127.0.0.1:8890`만 보이며, 호스트
JSON 호출이 결과를 반환한다. n8n Assistant 검색은 n8n 쪽에서 별도로 확인한다.

#### Evidence

명령, 시각, health 상태, 결과 건수만 기록한다. 검색어 외 결과 본문은 기록하지 않는다.

### Unverified Conditions

이 런북이 아직 관찰하지 못한 항목은 다음과 같다.

- `127.0.0.1:8890` 게시를 포함한 재생성과 호스트 JSON 호출: 승인된 재생성 뒤 관찰이 필요하다.
- 호스트 Hermes의 SearXNG 검색 성공: 재생성 뒤 다음 정기 실행 로그로 확인해야 한다.
- 이름을 바꾼 `search_net`에 n8n main이 합류한 상태의 Assistant 검색: n8n 재생성 뒤 확인이 필요하다.

## Escalation

### Next Owner

공개 노출, 승인되지 않은 합류, 복구 실패이면 중단하고 @buenhyden에게 정제된 증거로 넘긴다.

### Recovery or Forward Repair

자체 영속 데이터가 없으므로 이전 승인 Compose 선언과 image로 되돌린 뒤 재생성한다.
[RUN-0086](../10-platform-and-backup/0086-dependency-version-management.md)의 image 변경 절차를
따른다. 재생성 뒤 health와 JSON 호출을 다시 확인하고, 실패하면 호스트 소비자는 각자의
대체 검색 경로(Hermes는 Firecrawl)로 계속 동작하게 둔 채 에스컬레이션한다.
