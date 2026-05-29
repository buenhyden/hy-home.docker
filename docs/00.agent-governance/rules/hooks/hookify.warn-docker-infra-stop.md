---
name: warn-docker-infra-stop
enabled: true
event: stop
pattern: .*
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

🐳 **Docker 인프라 완료 체크리스트 (프로젝트 규칙)**

`docs/00.agent-governance/rules/postflight-checklist.md` — 인프라 레이어 완료 전 확인사항:

**Infrastructure Gate (infra 레이어 변경 시):**

- [ ] `bash scripts/validation/validate-docker-compose.sh` 통과
- [ ] 플레인텍스트 시크릿이 변경 파일에 없음 (Docker Secrets 또는 `secrets/` 마운트 사용)
- [ ] Named 볼륨이 `[Service]-[Data]-[Volume]` 규칙을 따름

**Settings Gate (settings 변경 시):**

- [ ] `settings.json` = 팀 공유 설정만 (git tracked)
- [ ] `settings.local.json` = 개인 오버라이드만
- [ ] 두 파일 간 중복 없음

**Governance Memory 업데이트:**

- [ ] `docs/00.agent-governance/memory/progress.md` 작업 로그 기록
- [ ] 변경 파일, 검증 증거, 미해결 리스크 기록

**Completion Blockers (HALT 조건):**

| 조건 | 조치 |
|------|------|
| `validate-docker-compose.sh` 실패 | compose 수정 후 재실행 |
| 설정 중복 | `settings.local.json`에서 제거 |
| 플레인텍스트 시크릿 발견 | Docker Secret 참조로 교체 |

PR 관련 작업이라면 `docs/00.agent-governance/rules/github-governance.md`의 Completion Gate도 확인하세요.

## Related Documents

- `docs/00.agent-governance/README.md`
