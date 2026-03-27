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
- **Runbook**: [airbyte.md](../../09.runbooks/07-workflow/airbyte.md)
- **Postmortem**: [Postmortems README](../../11.postmortems/README.md)
