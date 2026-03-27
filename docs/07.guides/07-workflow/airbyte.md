# Airbyte Guide

> Airbyte 기반 데이터 동기화 워크플로 설계 및 운영 준비 가이드.

---

## Overview (KR)

이 문서는 `07-workflow` 계층에서 Airbyte를 도입하거나 운영하기 전에 필요한 준비 절차와 사용 흐름을 안내한다. 현재 저장소 기준으로 `infra/07-workflow/airbyte/` 디렉터리는 존재하지만 실행용 `docker-compose.yml`은 아직 등록되지 않았다.

## Guide Type

`system-guide`

## Target Audience

- Data Engineer
- Operator
- Contributor
- Agent-tuner

## Purpose

- Airbyte 도입 전 필수 확인 사항을 표준화한다.
- Connector 생성, Sync 실행, 실패 원인 점검의 기본 흐름을 정리한다.
- Guide/Operation/Runbook 역할 경계를 유지한다.

## Prerequisites

- Docker/Compose 실행 환경
- Source/Destination 시스템 접근 정보
- `07-workflow` 티어 문서(PRD/ARD/ADR/Spec) 사전 확인
- `infra/07-workflow/airbyte/` 경로 접근 권한

## Step-by-step Instructions

1. 현재 인프라 상태를 먼저 확인한다.

   ```bash
   ls -la infra/07-workflow/airbyte
   ```

2. Airbyte 실행 자산(`docker-compose.yml`, `.env`) 존재 여부를 확인한다.

   ```bash
   test -f infra/07-workflow/airbyte/docker-compose.yml && echo "compose:ok" || echo "compose:missing"
   ```

3. 실행 자산이 준비된 경우, 표준 워크플로를 따른다.
   - Source Connector 생성
   - Destination Connector 생성
   - Connection 생성 및 Sync 주기 설정
   - 첫 Full Refresh 실행 후 Incremental 전략 적용

4. Sync 실패 시 즉시 원인을 분류한다.
   - 인증 실패(credential/permission)
   - 스키마 드리프트(source schema changed)
   - 리소스 부족(worker memory/cpu saturation)

5. 운영 통제와 복구 절차는 각각 아래 문서를 사용한다.
   - 정책/승인/예외: Operations Policy
   - 장애 대응/복구: Runbook

## Common Pitfalls

- 실행 파일이 없는 상태에서 Airbyte 운영 절차를 즉시 적용하려는 경우
- Incremental key/cursor 설정 없이 Full Refresh를 반복 실행하는 경우
- Connector 권한 범위를 과도하게 부여하는 경우
- Sync 실패 로그를 수집하지 않고 재시도만 반복하는 경우

## Related Documents

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Plan**: [2026-03-26-07-workflow-standardization.md](../../05.plans/2026-03-26-07-workflow-standardization.md)
- **Tasks**: [2026-03-26-07-workflow-tasks.md](../../06.tasks/2026-03-26-07-workflow-tasks.md)
- **Operation**: [airbyte.md](../../08.operations/07-workflow/airbyte.md)
- **Runbook**: [airbyte.md](../../09.runbooks/07-workflow/airbyte.md)
