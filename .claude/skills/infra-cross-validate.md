---
name: infra-cross-validate
description: >
  인프라 변경 후 security-auditor → iac-reviewer 교차 검증 파이프라인 오케스트레이터.
  infra-implementer가 변경을 적용한 직후, 반드시 이 스킬을 사용하여 보안 감사와
  드리프트+성능 검증을 순서대로 실행할 것.
  CRIT 발견 시 파이프라인을 즉시 중단하고 롤백 지시를 내린다.
---

# infra-cross-validate

인프라 변경 후 교차 검증 파이프라인 오케스트레이터.
`infra-validate`(단일 에이전트 pre/post-flight) 실행 완료 후 호출한다.

## 실행 순서

```text
infra-implementer 변경 완료
        │
        ▼
Phase 1 — security-auditor 감사
Phase 2 — iac-reviewer 드리프트+성능 검증
Phase 3 — 결과 통합 및 기록
```

### Phase 1 — Security Audit (security-auditor)

`infra-implementer`가 security-auditor에 SendMessage:

```text
"audit-request: <변경된 파일 목록>"
```

security-auditor 수행 항목:

- OWASP Top 10 + ASVS L2 기준 컨테이너 보안 감사
- GitHub Actions 워크플로 파일 존재 시 `rules/github-governance.md` §4 적용
- 이미지 태그 고정 여부 확인 (`docker image ls <image>`)
- 시크릿 노출 패턴 탐지

**CRIT 발견 시 → HALT:**

```text
security-auditor → infra-implementer: "BLOCK: <사유>"
```

infra-implementer는 즉시 변경을 롤백하고 사용자에게 에스컬레이션. Phase 2 진행 금지.

**CRIT 없을 시 → Phase 2 진행:**

```text
security-auditor → iac-reviewer: "validate-request: <파일 목록>"
```

### Phase 2 — Drift + Performance Check (iac-reviewer)

iac-reviewer 수행 항목:

**드리프트 체크:**

- 모든 서비스가 `infra_net` 네트워크 사용 확인
- `no-new-privileges: true` 전 컨테이너 존재 확인
- 시크릿이 `secrets:` 블록으로만 참조 확인
- 볼륨명 `[Service]-[Data]-[Volume]` 규칙 준수 확인
- health-check 정의 여부 확인
- restart policy 설정 여부 확인
- 리소스 제한 (`mem_limit` / `cpus`) 선언 여부 확인

**성능 체크:**

- `LATENCY_SLO < 200ms` 영향 서비스에 health-check 누락 시 WARN
- `mem_limit` / `cpus` 미선언 컨테이너 → WARN
- `restart` policy 미설정 stateful 서비스 → WARN
- PostgreSQL, Kafka, OpenSearch, MinIO 리소스 상한선 부재 → WARN

결과를 `_workspace/cross-validate_<YYYY-MM-DD>.md`에 기록 후:

```text
iac-reviewer → infra-implementer: "validate-complete: PASS|WARN <요약>"
```

### Phase 3 — 결과 통합 (infra-implementer)

infra-implementer 수행:

1. `_workspace/cross-validate_<YYYY-MM-DD>.md` 내용 확인
2. `docs/00.agent-governance/memory/progress.md`에 검증 결과 기록
3. WARN 항목이 있으면 사용자에게 알림 (파이프라인은 계속 진행)
4. BLOCK 항목 없음 → 태스크 완료

## 에러 처리

| 상황 | 조치 |
| ---- | ---- |
| Phase 1 CRIT | 즉시 HALT · infra-implementer에 BLOCK 메시지 · 롤백 지시 |
| Phase 2 WARN | 계속 진행 · 결과 파일에 기록 · 사용자 통보 |
| 에이전트 응답 없음 | `_workspace/`에 미응답 기록 · 사용자 에스컬레이션 |

## infra-validate와의 관계

| 스킬 | 목적 | 실행 시점 |
| ---- | ---- | --------- |
| `infra-validate` | 단일 에이전트 pre/post-flight | 변경 전후 |
| `infra-cross-validate` | 팀 교차 검증 오케스트레이터 | 변경 후 (infra-validate 완료 후) |

전체 순서: `infra-validate(pre)` → 변경 적용 → `infra-validate(post)` → `infra-cross-validate`

## 테스트 시나리오

**정상 흐름:**

1. infra-implementer가 서비스 추가 후 audit-request 발송
2. security-auditor: CRIT 없음 → validate-request 발송
3. iac-reviewer: WARN 1건(mem_limit 누락) → validate-complete WARN 발송
4. infra-implementer: progress.md 기록 + 사용자 WARN 알림 → 완료

**CRIT 차단 흐름:**

1. infra-implementer가 환경변수에 평문 비밀번호 포함 서비스 추가
2. security-auditor: CRIT 탐지 → BLOCK 발송
3. infra-implementer: 변경 롤백 → 사용자 에스컬레이션 → 파이프라인 중단

## 참고 문서

- `docs/00.agent-governance/scopes/infra.md`
- `docs/00.agent-governance/scopes/security.md`
- `docs/00.agent-governance/rules/github-governance.md` §4
- `.claude/skills/infra-validate.md`
- `.claude/agents/infra-implementer.md`
- `.claude/agents/security-auditor.md`
- `.claude/agents/iac-reviewer.md`
