---
title: "WireMock Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0092"
parent_ids:
- "GDE-0092"
created: "2026-09-23"
---

# WireMock Recovery Runbook

## When to Use

서비스가 비정상이거나, 스텁이 예상된 위치에서 요청이 404를 반환하거나, 매핑
파일이 로드에 실패하거나, 컨테이너가 메모리 제한에 도달했을 때 사용한다.

## Procedure

1. 점검한다.

   ```bash
   docker compose --profile api-mock config --quiet
   docker compose --profile api-mock ps wiremock
   docker compose --profile api-mock logs --tail=100 wiremock
   curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/health
   ```

2. 파싱에 실패한 매핑은 시작할 때 로그에 나타난다.
   `infra/11-quality/wiremock/mappings/`의 JSON을 수정하고
   `curl -s -X POST http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/mappings/reset`으로
   다시 로드한다.
3. 예상치 못한 404의 경우, 요청을 스텁과 비교한다.
   관리 API의 unmatched/near-misses 결과는 요청 본문·헤더를 포함할 수 있다.
   승인된 비공개 진단에서만 필요한 항목을 제한해 보고, 근거에는 개수·매핑 식별자와
   정제된 불일치 원인만 남긴다.
4. `OOMKilled`는 메모리 종료 신호이지 단일 원인의 증거가 아니다. journal 크기,
   본문·동시 요청, JVM과 컨테이너 한도를 확인한다. 필요한 제한 변경은 영향받는
   테스트 소유자와 검토하고 승인하며 템플릿을 즉시 늘리지 않는다.

### 매핑 변경·기동·재적용

`mappings/` 아래에 매핑 파일을 추가한 다음 서비스를 재시작하거나
`POST /__admin/mappings/reset`을 호출하면 파일이 다시 로드된다. 스텁
본문은 합성 데이터로 유지한다. 매핑은 추적되는 파일이므로 운영 시스템에서
캡처한 실제 응답, 토큰, 개인정보를 포함해서는 안 된다.

| Command | Effect |
| --- | --- |
| `docker compose --profile api-mock up -d wiremock` | 스텁 서버 시작 |
| `curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/health` | 상태, 버전, 가동 시간 |
| 요청 journal 조회 | 승인된 비공개 환경에서 필요한 항목만 확인하고 본문·헤더를 보고서에 출력하지 않음 |
| `curl -s -X POST http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/mappings/reset` | 추적된 매핑을 다시 로드하고 메모리상 매핑은 삭제 |

### 변경 전제·복구·업그레이드

모든 명령은 저장소 루트에서 실행한다. 기동·재시작·mapping reset 전에 영향받는
테스트와 소유자 승인을 확인한다. reset은 메모리 mapping을 바꾸므로 병행 테스트를
중단·조정한 뒤 실행하고 추적된 합성 stub으로 확인한다. 실패하면 추가 reset을
멈추고 검토된 mapping·이미지로 복원한다. 업그레이드는 공식 release와 매핑 호환성을
격리된 합성 요청으로 검증한 뒤 승인한다. journal은 복원하지 않으며 필요한 정제된
집계만 보존한 후 컨테이너를 제거한다.

## Evidence

health 응답, `__admin/mappings`의 매핑 개수, 종료 코드, 소스 커밋을
기록한다. journal의 요청 본문이나 헤더는 기록하지 않는다. 테스트가
크리덴셜을 전송했을 수 있다.

## Rollback or Recovery

서비스는 영속 상태를 갖지 않는다. 추적되는 이미지와 매핑에서 다시 만드는
것이 완전한 복구이며 인메모리 스텁과 journal은 설계상 사라진다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

admin API를 loopback 밖으로 공개하거나, 실제 업스트림에 대한 녹화를
활성화하거나, 캡처된 프로덕션 응답을 커밋하라는 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0092-wiremock.md) (`GDE-0092`)
- [Policy](../policies/0092-wiremock.md) (`POL-0092`)
- [WireMock Compose](../../../infra/11-quality/wiremock/docker-compose.yml)

## Related Documents

- [WireMock 패키지 README](../../../infra/11-quality/wiremock/README.md)
- [WireMock admin API](https://wiremock.org/docs/standalone/admin-api-reference/)
