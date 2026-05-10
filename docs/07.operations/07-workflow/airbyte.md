# Airbyte Operations Policy

> Airbyte 커넥터 운영, 동기화 통제, 보안 및 변경 승인 정책.

---

## Overview (KR)

이 문서는 `07-workflow` 계층의 Airbyte 운영 정책을 정의한다. Connector 승인, Sync 주기, 보안 권한, 배포 승격 기준을 통제하여 데이터 동기화 작업의 안정성과 추적성을 보장한다.

## Policy Scope

- Airbyte Connector 생성/변경/폐기 통제
- Sync 주기 및 재시도 정책
- 자격 증명(credential)과 접근 권한 관리
- 장애 시 운영 에스컬레이션 기준

## Applies To

- **Systems**: Airbyte (server, worker, connector jobs)
- **Agents**: 운영 자동화 에이전트, 배포 에이전트
- **Environments**: Development, Staging, Production

## Controls

- **Required**:
  - Connector 생성 시 소유자(owner), 데이터 범위, 목적을 문서화한다.
  - Production Connector는 최소 권한(least privilege) 계정만 사용한다.
  - Sync 실패 로그(에러 원인, 시점, 영향 범위)를 30일 이상 보관한다.
  - 신규 Connector/Sync 정책 변경은 `05.plans`와 `06.tasks` 증적을 남긴다.
- **Allowed**:
  - Dev 환경에서의 임시 Connector 테스트
  - 승인된 점검 창(window) 내 수동 Sync 실행
  - 장애 대응 목적의 일시적 재시도 한도 상향
- **Disallowed**:
  - 승인 없이 Production에서 Full Refresh 강제 실행
  - 공유 계정/공용 토큰의 장기 운영 사용
  - 장애 원인 미확인 상태에서 반복적인 강제 재시작

## Exceptions

- 긴급 복구(Sev1/Sev2) 상황에서는 On-call 승인으로 임시 우회 설정을 허용한다.
- 우회 설정은 24시간 내 원복하고, Incident 기록을 남겨야 한다.

## Verification

- 월간 정책 준수 점검:
  - Connector 인벤토리와 소유자/권한 매핑 검증
  - 최근 Sync 실패 Top N 원인 및 재발 여부 점검
- 릴리스 전 점검:
  - 변경된 Connector 설정 diff 확인
  - 관련 Plan/Task 링크 유효성 점검

## Review Cadence

- Monthly (정책 준수 점검)
- Per release (워크플로 변경 배포 시)

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**:
  - Airbyte 운영 자동화 프롬프트 변경은 PR + 운영 승인 후 적용한다.
- **Eval / Guardrail Threshold**:
  - Production 반영 전, 잘못된 커넥터 삭제/권한 확장 요청을 차단하는 규칙 테스트를 통과해야 한다.
- **Log / Trace Retention**:
  - 자동화 에이전트 실행 로그/감사 추적은 최소 30일 보관한다.
- **Safety Incident Thresholds**:
  - 무단 권한 상승, 데이터 유출 징후, 승인 없는 대량 재동기화는 즉시 Sev1로 분류한다.

## Related Documents

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Procedure**: [airbyte.md](../../07.operations/07-workflow/airbyte.md)
- **Postmortem**: [Postmortems README](../../10.incidents/README.md)

## Usage

> Migrated from `docs/07.operations/07-workflow/airbyte.md` during the 2026-05-10 operations taxonomy consolidation.

### Airbyte Usage

> Airbyte 기반 데이터 동기화 워크플로 설계 및 운영 준비 가이드.

---

#### Overview (KR)

이 문서는 `07-workflow` 계층에서 Airbyte를 도입하거나 운영하기 전에 필요한 준비 절차와 사용 흐름을 안내한다. 현재 저장소 기준으로 `infra/07-workflow/airbyte/` 디렉터리는 존재하지만 실행용 `docker-compose.yml`은 아직 등록되지 않았다.

#### Usage Type

`system-guide`

#### Target Audience

- Data Engineer
- Operator
- Contributor
- Agent-tuner

#### Purpose

- Airbyte 도입 전 필수 확인 사항을 표준화한다.
- Connector 생성, Sync 실행, 실패 원인 점검의 기본 흐름을 정리한다.
- Usage/Operation/Procedure 역할 경계를 유지한다.

#### Prerequisites

- Docker/Compose 실행 환경
- Source/Destination 시스템 접근 정보
- `07-workflow` 티어 문서(PRD/ARD/ADR/Spec) 사전 확인
- `infra/07-workflow/airbyte/` 경로 접근 권한

#### Step-by-step Instructions

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
   - 장애 대응/복구: Procedure

#### Common Pitfalls

- 실행 파일이 없는 상태에서 Airbyte 운영 절차를 즉시 적용하려는 경우
- Incremental key/cursor 설정 없이 Full Refresh를 반복 실행하는 경우
- Connector 권한 범위를 과도하게 부여하는 경우
- Sync 실패 로그를 수집하지 않고 재시도만 반복하는 경우

#### Related Documents

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Plan**: [2026-03-26-07-workflow-standardization.md](../../05.plans/2026-03-26-07-workflow-standardization.md)
- **Tasks**: [2026-03-26-07-workflow-tasks.md](../../06.tasks/2026-03-26-07-workflow-tasks.md)
- **Operation**: [airbyte.md](../../07.operations/07-workflow/airbyte.md)
- **Procedure**: [airbyte.md](../../07.operations/07-workflow/airbyte.md)

## Procedure

> Migrated from `docs/07.operations/07-workflow/airbyte.md` during the 2026-05-10 operations taxonomy consolidation.

### Airbyte Procedure

: Airbyte / Workflow Tier

---

#### Overview (KR)

이 런북은 Airbyte 동기화 실패 또는 워커 장애 발생 시 즉시 실행할 복구 절차를 정의한다. 현재 저장소에서는 `infra/07-workflow/airbyte/`에 실행 자산이 없을 수 있으므로, 실행 전 자산 존재 여부를 먼저 확인한다.

#### Purpose

- Airbyte Sync 실패 원인을 신속히 분류하고 복구한다.
- 장애 증적을 표준 형식으로 수집한다.
- 안전한 원복 절차를 통해 데이터 불일치 위험을 최소화한다.

#### Canonical References

- [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- [0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)
- [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- [2026-03-26-07-workflow-standardization.md](../../05.plans/2026-03-26-07-workflow-standardization.md)

#### When to Use

- Connector Sync가 연속 실패하는 경우
- Worker가 비정상 종료되거나 재시작 루프에 들어간 경우
- 스키마 변경 후 Sync가 중단된 경우
- 배포 직후 Connection이 실행되지 않는 경우

#### Procedure or Checklist

##### Checklist

- [ ] `infra/07-workflow/airbyte/docker-compose.yml` 존재 여부 확인
- [ ] 장애 Connection ID, 영향 데이터셋, 첫 실패 시각 확보
- [ ] 최근 설정 변경(Connector/권한/네트워크) 여부 확인

##### Procedure

1. 실행 자산 존재 여부를 점검한다.

   ```bash
   test -f infra/07-workflow/airbyte/docker-compose.yml && echo "compose:ok" || echo "compose:missing"
   ```

2. 실행 자산이 없는 경우, 즉시 운영 티켓을 생성하고 수동 복구 절차로 전환한다.
   - 영향 범위 기록
   - 데이터 소스/타깃 직접 동기화 여부 검토
   - 승인된 우회 절차만 수행

3. 실행 자산이 있는 경우, 서비스 상태를 확인한다.

   ```bash
   docker compose -f infra/07-workflow/airbyte/docker-compose.yml ps
   ```

4. 장애 서비스 로그를 확인한다.

   ```bash
   docker compose -f infra/07-workflow/airbyte/docker-compose.yml logs --tail=200
   ```

5. 원인별로 조치한다.
   - 인증/권한 오류: Connector credential 교체 후 단건 Sync 재실행
   - 스키마 드리프트: 스키마 refresh 후 full/incremental 전략 재선택
   - 리소스 부족: Worker 리소스 상향 후 재시작

6. 복구 후 대상 Connection을 재실행하고 결과를 기록한다.

#### Verification Steps

- [ ] 실패하던 Connection이 1회 이상 성공 완료됨
- [ ] Source/Destination 레코드 카운트가 허용 오차 내 일치
- [ ] 동일 에러가 30분 내 재발하지 않음

#### Observability and Evidence Sources

- **Signals**:
  - Sync failure rate
  - Worker restart count
  - Connection latency
- **Evidence to Capture**:
  - 장애 시점 전후 로그 200줄
  - 설정 변경 이력(Connector/Connection diff)
  - 복구 실행자, 실행 시각, 검증 결과

#### Safe Rollback or Recovery Procedure

- [ ] 장애 유발 Connector 변경을 이전 버전으로 복원
- [ ] 승인 없는 Full Refresh 실행은 중단
- [ ] 필요 시 마지막 정상 스냅샷 기준으로 재동기화 범위를 축소

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 자동화 에이전트 프롬프트를 직전 안정 버전으로 되돌린다.
- **Model Fallback**: 정책 평가 실패 시 보수적 모델/규칙셋으로 전환한다.
- **Tool Disable / Revoke**: Connector 변경 권한을 일시적으로 차단한다.
- **Eval Re-run**: 복구 완료 후 정책 위반 시나리오를 재검증한다.
- **Trace Capture**: 에이전트 실행 추적과 승인 이벤트를 Incident에 첨부한다.

#### Related Operational Documents

- **Usage**: [airbyte.md](../../07.operations/07-workflow/airbyte.md)
- **Operation**: [airbyte.md](../../07.operations/07-workflow/airbyte.md)
- **Incident examples**: [Incidents README](../../10.incidents/README.md)
- **Postmortem examples**: [Postmortems README](../../10.incidents/README.md)
