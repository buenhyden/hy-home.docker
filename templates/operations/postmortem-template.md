# Postmortem: [INC-YYYYMMDD-XXX] / 장애 사후 분석 보고서

_Target Directory: `docs/operations/postmortems/YYYY-MM-DD-[incident-name].md`_
_Note: This document follows the blameless culture. (비난 없는 사후 분석 문화를 지향합니다)._

## 1. Incident Summary / 장애 요약

- **Incident ID**: [INC-YYYYMMDD-XXX]
- **Date/Time (UTC)**: [YYYY-MM-DD HH:MM]
- **Severity**: [SEV-1 / SEV-2 / SEV-3]
- **Status**: Resolved (해결됨)
- **Owner (IC)**: [대응 지휘관 성함/팀]
- **Incident Doc**: [당시 장애 기록 `docs/operations/incidents/...` 링크]

## 2. Impact / 영향도 분석

- **Affected Users/Services (대상)**: [장애 영향을 받은 사용자군 또는 다운스트림 서비스 기술]
- **Duration (장애 지속 시간)**: [예: 2시간 15분]
- **Business Impact (비즈니스 영향)**: [매출 손실, 서비스 신뢰도 저하, SLA 위반 여부 등]

## 3. Timeline / 타임라인 (UTC)

| Time  | Event / 주요 단계                                        |
| :---- | :------------------------------------------------------- |
| HH:MM | **[Detection]** 처음 인지된 경로 (Alert, 사용자 제보 등) |
| HH:MM | **[Investigation]** 핵심 진단 결과 및 발견 사항          |
| HH:MM | **[Mitigation]** 장애 확산 방지 및 복구를 위해 취한 조치 |
| HH:MM | **[Resolved]** 서비스가 정상 상태로 완전히 복구된 시점   |

## 4. Root Cause Analysis (Five Whys) / 근본 원인 분석

_기저의 시스템적 결함을 찾기 위해 "왜(Why)"를 5번 반복하며 분석합니다._

1. **서비스가 왜 중단되었는가?** -> [예: DB 커넥션 풀이 고갈됨]
2. **왜 고갈되었는가?** -> [예: 최근 배포된 쿼리에 타임아웃 설정이 누락됨]
3. **쿼리에 왜 타임아웃이 없었는가?** -> [예: 새로 도입된 ORM 라이브러리의 기본값이 무제한(Infinite)임]
4. **왜 CI/CD에서 발견되지 않았는가?** -> [예: 부하 테스트가 PR 단위가 아닌 주 단위로만 수행됨]
5. **부하 테스트가 왜 주 단위인가?** -> [예: 테스트 스위트 실행에 45분 이상 소요되어 생산성 저하 우려]

- **Primary Root Cause (최종 근본 원인)**: [시스템적 최종 원인 기술]
- **Detection Gaps (감지 누락 원인)**: [사용자에게 영향이 가기 전 왜 알람이 울리지 않았는가?]

## 5. What Went Well / 좋았던 점

- [예: API 게이트웨이의 자동 롤백이 완벽하게 작동함]
- [내용 추가]

## 6. What Went Wrong / 아쉬웠던 점

- [예: 로그에 상관관계 ID(Correlation ID)가 없어 원인 쿼리 식별에 20분 소요됨]
- [내용 추가]

## 7. Action Items (Remediation) / 재발 방지 대책

| Action / 조치 과제 (교정/예방)             | Owner / 담당 | Priority | Ticket Link | Status  |
| :----------------------------------------- | :----------- | :------- | :---------- | :------ |
| [예: ORM 전역 설정에 5초 타임아웃 강제]    | [Name]       | High     | [Link]      | Pending |
| [예: DB 쿼리 로그에 상관관계 ID 추가]      | [Name]       | Medium   | [Link]      | Pending |
| [예: PR 단위 스모크 부하 테스트(5분) 구축] | [Name]       | Medium   | [Link]      | Pending |

## 8. Follow-up Links / 참고 링크 및 자료

- **Incident Channel**: [당시 협업 채널 대화 로그]
- **Metrics Snapshot**: [장애 당시의 Grafana 대시보드 캡처/링크]
- **Related PRs**: [장애 수정을 위해 제출된 PR 링크]

---

> **참고**: 이 보고서는 비난을 위한 것이 아니라 시스템의 복원력을 높이기 위한 것입니다.
