---
title: "Conftest Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0095"
parent_ids:
- "GDE-0095"
created: "2026-09-23"
---

# Conftest Recovery Runbook

## When to Use

`conftest` 작업이 0이 아닌 상태로 종료될 때 사용한다.

## Procedure

1. 실행하고 첫 실패 줄을 읽는다.

   ```bash
   docker compose --profile policy-check run --rm conftest
   ```

2. `verify` 요약의 실패는 `infra/09-tooling/conftest/policy/`의 깨진 규칙이나
   테스트다. 다른 무엇보다 Rego를 먼저 수정한다.
3. `FAIL - <file> - compose - service <name>: …` 또는 `… - dockerfile - …`는
   선언과 규칙을 명시한다. 선언을 수정한다. 프로파일을 추가하거나, 이미지를
   고정하거나, 리터럴을 Docker secret으로 옮기거나, `--checksum`을
   추가한다.
4. 선언이 의도된 것이면(예: 새로운 권한 필요), 정책 파일의 allowlist를
   사유와 함께 검토된 변경으로 바꾼다.
5. 종료 `2` 또는 `exceptions` 개수가 0보다 크면 파일이 파싱되지 않았음을
   의미한다. 명시된 파일이 잘못된 YAML이나 Dockerfile 문법이다.

## Evidence

세 요약 줄(verify, compose, dockerfile)과 소스 커밋을 기록한다.

## Rollback or Recovery

이 작업은 아무것도 변경하지 않으며 상태를 갖지 않는다.

## Escalation

`secrets/`, `.env` 또는 Docker 소켓을 작업에 마운트하라는 요청, 또는 실패하는
변경을 통과시키기 위해 `deny`를 `warn`으로 바꾸라는 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0095-conftest.md) (`GDE-0095`)
- [Policy](../policies/0095-conftest.md) (`POL-0095`)
- [Conftest Compose](../../../infra/09-tooling/conftest/docker-compose.yml)

## Related Documents

- [Conftest 패키지 README](../../../infra/09-tooling/conftest/README.md)
