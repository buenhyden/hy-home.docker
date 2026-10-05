---
title: "Conftest Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0095"
parent_ids:
- "GDE-0095"
created: "2026-09-23"
---

# Conftest Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

`conftest` 작업이 0이 아닌 상태로 종료될 때 사용한다.

## Procedure

### Procedure

1. 저장소 루트에서 승인된 로컬 컨테이너 작업을 실행하고 첫 실패 단계·줄을 읽는다.
   원본 읽기 전용 작업이어도 컨테이너 생성은 정적 문서 검사와 구분한다.

   ```bash
   docker compose --profile policy-check run --rm conftest
   ```

2. `verify` 요약의 실패는 `infra/11-quality/conftest/policy/`의 깨진 규칙이나
   테스트다. 무엇보다 Rego부터 수정한다.
3. `FAIL - <file> - compose - service <name>: …` 또는 `… - dockerfile - …`는
   선언과 규칙을 명시한다. 선언을 수정한다. 프로파일을 추가하거나, 이미지를
   고정하거나, 리터럴을 Docker secret으로 옮기거나, `--checksum`을
   추가한다.
4. 선언이 의도한 것이면(예: 새 권한 필요), 정책 파일의 allowlist를
   사유와 함께 검토받은 변경으로 바꾼다.
5. 종료 코드만으로 파싱 실패를 단정하지 않는다. CI wrapper의 `2`는 Docker
   불가용일 수도 있고 xargs·shell 상태가 전달될 수 있다. verify/Compose/Dockerfile
   중 실행된 단계와 오류를 확인하고 파싱·규칙·실행 환경 문제를 구분한다.

### 수정·업그레이드·복구

규칙과 파일 수정 전 실패 입력·기존 통제의 소유자를 확인한다. source 위반은 선언을
수정하고, 규칙 결함이면 해당 정책 테스트와 근거를 보존해 검토받는다. 실패를 숨기기
위한 deny 완화는 하지 않는다. 이미지·Rego 변경은 버전에 맞는 release/API와 정책
테스트를 확인하고 검토한 이전 소스로 rollback한다. 작업 자체 데이터·credential·TLS
복원은 적용되지 않으며 Git의 정책 원본과 정제된 검사 근거만 보존한다.

## Verification

### Evidence

실제로 실행된 단계의 요약·exit와 소스 커밋을 기록한다. 첫 실패 뒤 실행되지 않은
단계는 미실행으로 남기며 세 요약을 만들거나 전체 PASS로 해석하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

이 작업은 아무것도 바꾸지 않으며 상태도 갖지 않는다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

`secrets/`, `.env` 또는 Docker 소켓을 작업에 마운트하라는 요청, 또는 실패하는
변경을 통과시키기 위해 `deny`를 `warn`으로 바꾸라는 요청이 있으면 중단한다.

### Traceability

- [Guide](../guides/0095-conftest.md) (`GDE-0095`)
- [Policy](../policies/0095-conftest.md) (`POL-0095`)
- [Conftest Compose](../../../infra/11-quality/conftest/docker-compose.yml)

## Related Documents

- [Conftest 패키지 README](../../../infra/11-quality/conftest/README.md)
