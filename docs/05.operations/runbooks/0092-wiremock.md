---
title: "WireMock Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
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
   `infra/09-tooling/wiremock/mappings/`의 JSON을 수정하고
   `curl -s -X POST http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/mappings/reset`으로
   다시 로드한다.
3. 예상치 못한 404의 경우, 요청을 스텁과 비교한다.
   `curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/requests/unmatched`는
   어떤 스텁과도 일치하지 않은 요청을 나열하고,
   `__admin/requests/unmatched/near-misses`는 각각에 가장 가까운 스텁을
   보여준다.
4. `OOMKilled` 상태는 journal 상한이나 큰 스텁 본문이 제한을 초과했음을
   의미한다. 템플릿을 늘리기 전에 `--max-request-journal-entries`를
   낮추거나 본문을 줄인다.

## Evidence

health 응답, `__admin/mappings`의 매핑 개수, 종료 코드, 소스 커밋을
기록한다. journal의 요청 본문이나 헤더는 기록하지 않는다. 테스트가
크리덴셜을 전송했을 수 있다.

## Rollback or Recovery

서비스는 영속 상태를 갖지 않는다. 추적되는 이미지와 매핑에서 다시 만드는
것이 완전한 복구이며 인메모리 스텁과 journal은 설계상 사라진다.

## Escalation

admin API를 loopback 밖으로 공개하거나, 실제 업스트림에 대한 녹화를
활성화하거나, 캡처된 프로덕션 응답을 커밋하라는 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0092-wiremock.md) (`GDE-0092`)
- [Policy](../policies/0092-wiremock.md) (`POL-0092`)
- [WireMock Compose](../../../infra/09-tooling/wiremock/docker-compose.yml)

## Related Documents

- [WireMock 패키지 README](../../../infra/09-tooling/wiremock/README.md)
- [WireMock admin API](https://wiremock.org/docs/standalone/admin-api-reference/)
