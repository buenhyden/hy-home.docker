---
name: infra-validate
description: >
  Docker Compose 인프라 변경 전/후 검증 파이프라인. compose 파일 수정, 서비스 추가/제거,
  네트워크·볼륨·시크릿 변경 시 반드시 이 스킬을 사용할 것.
  validate-docker-compose.sh 실행, 드리프트 감지, SLO 체크, 헬스 확인을 순서대로 수행.
---

# infra-validate

H100:20+26 — Compose 검증 파이프라인 (progressive disclosure).
`infra-implementer`와 `iac-reviewer`가 공유하는 오케스트레이션 스킬.

## 실행 순서

```text
Pre-flight → Static validate → Apply → Post-flight → Health
```

### Phase 1 — Pre-flight (변경 전 필수)

```bash
bash scripts/validate-docker-compose.sh
```

실패 시 **HALT** — 변경 적용 금지.

### Phase 2 — Static validate (compose 구문 검사)

```bash
docker compose config --quiet
```

- 오류 없어야 함 (exit 0).
- 경고 메시지도 파일:라인 기록.

### Phase 3 — Drift check (선택: 라이브 환경)

라이브 환경이 접근 가능한 경우에만 실행:

```bash
docker compose ps --format json 2>/dev/null | python3 -c "
import json, sys
services = json.load(sys.stdin)
for s in services:
    if s.get('State') != 'running':
        print(f'DRIFT: {s[\"Name\"]} state={s[\"State\"]}')
"
```

드리프트 발견 시 `_workspace/drift_<date>.md`에 기록.

### Phase 4 — Apply (변경 적용)

- In-place 수정만.
- 시크릿: Docker Secrets / `secrets/` 마운트만.
- 네트워크: `infra_net` 전용.

### Phase 5 — Post-flight (변경 후 필수)

```bash
docker compose ps
```

모든 서비스 `running` 상태 확인. 비정상 서비스는 즉시 로그 확인:

```bash
docker compose logs --tail=50 <service>
```

## SLO 체크리스트

- [ ] `LATENCY_SLO < 200ms` 영향 서비스에 health-check 정의됨
- [ ] 모든 stateful 서비스에 restart policy 설정됨
- [ ] `no-new-privileges: true` 전 컨테이너에 존재
- [ ] 볼륨명: `[Service]-[Data]-[Volume]` 규칙 준수

## 시크릿 가드

변경 파일에서 아래 패턴 검출 시 **HALT**:

```bash
grep -nE '(password|secret|token|key)\s*[:=]\s*[A-Za-z0-9+/]{8,}' <file>
```

발견 시 `security-auditor`에 에스컬레이션. 절대 커밋하지 말 것.

## 에러 처리

| 상황                  | 조치                                 |
| --------------------- | ------------------------------------ |
| Phase 1 실패          | HALT — 원인 수정 후 재실행           |
| Phase 2 경고          | 기록 후 계속                         |
| Phase 5 서비스 비정상 | 변경 롤백 → 로그 수집 → 에스컬레이션 |
| 시크릿 검출           | HALT — `security-auditor` 호출       |

## 참고 문서

- `docs/00.agent-governance/scopes/infra.md` §3 Implementation Flow
- `docs/00.agent-governance/rules/postflight-checklist.md` §1 Infrastructure Gate
- `.claude/agents/infra-implementer.md`
- `.claude/agents/iac-reviewer.md`
