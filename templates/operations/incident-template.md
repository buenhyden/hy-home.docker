# Active Incident: [INC-YYYYMMDD-XXX] / 장애 대응 기록

_Target Directory: `docs/operations/incidents/`_
_Note: This document tracks the real-time response to a production event._

**Postmortem Link (사후 분석)**: [장애 종료 후 생성된 포스트모템 링크]

## 1. Incident Metadata / 장애 메타데이터

| Field / 항목          | Value / 내용                                                  |
| :-------------------- | :------------------------------------------------------------ |
| **Incident ID**       | [INC-YYYYMMDD-XXX]                                            |
| **Severity / 심각도** | [SEV-1 / SEV-2 / SEV-3] (범례 참고)                           |
| **Status / 상태**     | [Investigating / Identified / Mitigating / Resolved / Closed] |
| **Detection Time**    | [YYYY-MM-DD HH:MM UTC] (감지 시간)                            |
| **Primary Service**   | [장애 발생 서비스명]                                          |
| **Affected Deps**     | [영향을 받는 상/하위 시스템]                                  |
| **Dashboard Link**    | [모니터링 대시보드 URL]                                       |
| **Runbook Link**      | [관련 서비스 운영 런북 URL]                                   |

> **Severity Legend / 심각도 범례**:
>
> - **SEV-1 (Critical)**: 핵심 서비스 전면 중단 또는 대규모 데이터 유실.
> - **SEV-2 (High)**: 주요 기능의 심각한 성능 저하; 우회 방법 없음.
> - **SEV-3 (Moderate)**: 부분적인 결함 또는 비핵심 기능 장애; 우회 방법 존재.

## 2. Response Roster / 대응 인력

| Role / 역할                  | Name / 성명 | Contact / 연락처  |
| :--------------------------- | :---------- | :---------------- |
| **Incident Commander (IC)**  | [지휘관]    | [@handle / Slack] |
| **Communications Lead (CL)** | [상황 전파] | [@handle / Slack] |
| **Operations Lead (OL)**     | [기술 대응] | [@handle / Slack] |

## 3. Latest Status Update / 최근 상황 보고

_Update Interval: [15m / 30m / 60m] 마다 업데이트 권장_

- **Current Impact (현재 영향)**: [사용자가 겪고 있는 불편함 기술]
- **Current Hypothesis (가설)**: [이유로 추정되는 원인]
- **Mitigation Actions (조치 내용)**: [현재 수행 중인 긴급 복구 작업]
- **Next Update (다음 보고)**: [HH:MM]

## 4. Timeline / 대응 타임라인 (UTC)

| Time (UTC) | Actor / 담당 | Detail / 상세 이벤트 (Detection/Mitigation/Update)     |
| :--------- | :----------- | :----------------------------------------------------- |
| HH:MM      | -            | **[Detection]** 인시던트 발생 선언 (Incident Declared) |
| HH:MM      | [Name]       | **[Action]** 로그 분석 시작 (Investigating logs)       |
| HH:MM      | [Name]       | **[Mitigation]** 특정 파드(Pod) 재시작 수행            |
| HH:MM      | [Name]       | **[Update]** 오류율 감소 확인, 모니터링 지속           |

## 5. End State & Handoff / 종료 및 핸드오프

- **Mitigation Complete (조치 완료)**: [HH:MM UTC]
- **Resolution Verified (검증 완료)**: [HH:MM UTC]

### Follow-up Actions / 후속 조치 과제

- [ ] [예: 임시로 우회한 속도 제한 규칙 원복] - **Owner**: [Name]
- [ ] [예: 누락된 DB 인덱스 생성 티켓 발행] - **Owner**: [Name]

- **Postmortem Required? (사후 분석 필요 여부)**: [Yes / No]

---

> _SEV-1/2인 경우 반드시 `docs/operations/postmortems/`에 보고서를 작성하고 이 파일 상단에 링크하십시오._
