---
name: incident-response
description: >
  Docker 인프라 장애 대응 절차서. 서비스 다운, SLO 위반, 시크릿 노출, 컨테이너 크래시 등
  모든 인프라 인시던트 발생 시 반드시 이 스킬을 사용할 것.
  H100:25 timeline-reconstructor · rca-investigator · remediation-planner 패턴 적용.
---

# incident-response

H100:25 — 장애 대응 절차서 (docker-specific).
`incident-responder` 에이전트의 오케스트레이션 스킬.

## 심각도 분류

| SEV  | 기준                              | 응답 시한 | 포스트모템 |
| ---- | --------------------------------- | --------- | ---------- |
| SEV1 | 서비스 전체 중단 / 시크릿 노출    | 즉시      | 24h 이내   |
| SEV2 | 핵심 서비스 기능 장애 / SLO 위반  | 30분      | 72h 이내   |
| SEV3 | 부분 기능 저하 / 경고 임계값 초과 | 4h        | 선택       |

## Phase 1 — 탐지 및 분류

```bash
# 전체 서비스 상태 확인
docker compose ps

# 비정상 컨테이너 로그 수집
docker compose logs --tail=100 <service> 2>&1 | tee _workspace/incident_logs_$(date +%Y%m%d_%H%M).txt

# 네트워크 연결 확인
docker network inspect infra_net
```

인시던트 레코드 즉시 생성: `docs/10.incidents/INC-<YYYYMMDD>-<seq>.md`

## Phase 2 — 타임라인 재구성

LGTM 스택 조회 순서:

1. **Loki** — 장애 직전 30분 로그 수집
2. **Grafana** — 해당 시간대 대시보드 스냅샷
3. **Tempo** — 에러 트레이스 ID 수집
4. **Mimir/Prometheus** — 메트릭 이상점 식별

타임라인 형식:

```text
HH:MM:SS | 이벤트 | 출처(로그/메트릭/트레이스)
```

## Phase 3 — 즉각 완화 (SEV1/SEV2)

```bash
# 서비스 재시작 시도
docker compose restart <service>

# 상태 재확인
docker compose ps <service>
docker compose logs --tail=20 <service>
```

재시작 후에도 비정상 → **runbook 조회**: `docs/09.runbooks/<service>.md`

시크릿 노출 의심 시:

- **즉시 HALT** — `security-auditor` 에스컬레이션
- 해당 시크릿 격리 전까지 서비스 중단 고려

## Phase 4 — 근본 원인 분석 (RCA)

RCA 구조:

```text
증상: [관찰된 현상]
근본 원인: [왜 발생했는가 — 5-why]
기여 요인: [복합 원인]
탐지 지연: [왜 늦게 발견됐는가]
```

- 추정 금지 — 증거 기반으로만 작성.
- 개인 책임 배제 — 시스템/프로세스 관점.

## Phase 5 — 복구 및 검증

```bash
bash scripts/validate-docker-compose.sh
docker compose up -d <service>
docker compose ps
```

SLO 복구 확인: LATENCY_SLO < 200ms 기준 정상화 대기.

## Phase 6 — 포스트모템 (SEV1: 24h / SEV2: 72h)

파일 생성: `docs/11.postmortems/PM-<INC-ID>.md`

필수 섹션:

- 타임라인 (Phase 2 결과)
- RCA (Phase 4 결과)
- 재발 방지 액션 (담당자 + 기한)
- `## Related Documents` (INC 링크 포함)

## 에러 처리

| 상황           | 조치                                |
| -------------- | ----------------------------------- |
| runbook 없음   | 임시 대응 후 신규 runbook 작성 요청 |
| 로그 접근 불가 | 타임라인 갭으로 기록; 추정 금지     |
| 복구 후 재발   | 즉시 SEV 상향; RCA 재개             |

## 참고 문서

- `docs/00.agent-governance/scopes/ops.md`
- `docs/00.agent-governance/rules/postflight-checklist.md` §1 §3
- `docs/09.runbooks/`
- `docs/10.incidents/`
- `docs/11.postmortems/`
- `.claude/agents/incident-responder.md`
