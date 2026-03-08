# Service Runbook / 서비스 런북: [Service Name]

_Target Directory: `docs/runbooks/[service]-runbook`_
_Note: This template follows [REQ-RBK-STR-01] in `0381-runbooks-oncall.md`._

---

## 1. Service Overview & Ownership / 서비스 개요 및 소유권

- **Description (설명)**: [서비스의 핵심 기능 및 비즈니스 중요도 기록]
- **Owner Team (소유팀)**: [서비스를 책임지는 팀 명칭]
- **Primary Contact (비상 연락처)**: [Slack 채널, 이메일 또는 호출 핸들러]

## 2. Dependencies / 의존성

| Dependency / 항목   | Type / 유형 | Impact if Down / 장애 영향 | Link to Runbook / 링크 |
| :------------------ | :---------- | :------------------------- | :--------------------- |
| [예: PostgreSQL]    | Database    | 전체 서비스 중단           | [Link]                 |
| [예: Analytics API] | External    | 일부 부가 기능 저하        | [Link]                 |

## 3. SLOs & SLIs / 성능 및 가용성 목표

- **Availability (가용성)**: [예: 가동 시간 99.9% 이상]
- **Latency (지연 시간)**: [예: P95 < 200ms]
- **Errors (오류율)**: [예: 월간 성공률 99.99%]

## 4. Dashboards & Observability / 대시보드 및 관측성

- **Primary Dashboard (기본 대시보드)**: [Grafana/Datadog RED 메트릭 링크]
- **Alert Definitions (경보 설정)**: [해당 서비스에 설정된 알람 규칙 페이지 링크]
- **Routing (알람 수신처)**: [PagerDuty/Slack/Email]

## 5. Common Failures & Fixes / 주요 장애 및 조치 방법

_확인된 알람 및 빈번한 실패 사례에 대해 즉시 실행 가능한 체크리스트를 제공하십시오._

### Scenario A: [예: High Latency / 지연 시간 증가]

- **Symptoms (증상)**: [어떤 알람이 발생하며 어떤 메트릭이 상승하는가?]
- **Investigation (조사 단계)**:
  1. [대시보드 Y에서 메트릭 X 확인]
  2. [데이터베이스 부하 확인을 위한 쿼리 Z 실행]
- **Remediation (조치)**:
  - [ ] Action 1: [예: 배포 스케일 아웃] `kubectl scale deployment <name> --replicas=5`
  - [ ] Action 2: [조치 1의 기대 결과 확인]

## 6. Safe Rollback Procedure / 안전한 롤백 절차

_중요: 배포나 설정 변경 실패 시 서비스를 이전 상태로 원복하는 결정론적 명령을 제공하십시오._

- [ ] **Step 1**: [예: 마지막으로 성공한 안정적인 Git SHA 식별]
- [ ] **Step 2**: [예: CI/CD 또는 CLI를 통한 롤백 트리거 실행]
- [ ] **Step 3**: [기대 결과: 서비스가 이전 이미지 버전으로 정상 복구됨]

## 7. Data Safety Notes / 데이터 안전 유의사항 (Stateful 환경인 경우)

- [데이터 손실 위험, 재시작 시의 오염 가능성 또는 수동 수동 마이그레이션 제약 사항 기록]

## 8. Escalation Path / 에스컬레이션 경로

_1차 온콜 담당자가 해결할 수 없는 경우 다음 단계로 전달하십시오._

1. **Primary On-Call (1차)**: [팀 슬랙 / 담당 팀원]
2. **Secondary Escalation (2차)**: [테크 리드 / 시니어 엔지니어]
3. **Management Escalation (관리자/SEV-1)**: [엔지니어링 매니저 / CTO]

## 9. Verification Steps / 최종 검증 (Post-Fix)

_조치 후 서비스가 완전히 정상화되었는지 어떻게 확인합니까?_

- [ ] [예: 대시보드의 에러율이 1% 미만으로 감소함]
- [ ] [예: Synthetic 모니터링 결과가 200 OK로 확인됨]
- [ ] [예: 로그에서 DB 재연결 성공 메시지 확인]
