---
name: block-gha-secrets-in-run
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.github/workflows/.*\.ya?ml$
  - field: new_text
    operator: regex_match
    pattern: (echo|print)\s+.*\$\{\{\s*secrets\.|run:\s+env\s*$|\$\{\{\s*secrets\.[^}]+\}\}\s*>>\s*\$GITHUB_(OUTPUT|ENV|STEP_SUMMARY)
action: block
---

🚫 **GitHub Actions 시크릿 노출 패턴 차단됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/github-governance.md §4` — 워크플로우 로그에 시크릿이 노출될 수 있는 패턴입니다.

**감지된 위험 패턴:**
- `echo ${{ secrets.* }}` — 시크릿을 로그에 출력
- `run: env` — 모든 환경 변수(시크릿 포함) 덤프
- 시크릿을 `$GITHUB_OUTPUT`, `$GITHUB_ENV`에 직접 쓰기

**왜 BLOCK인가요?**
- GitHub Actions 로그는 기록으로 남습니다
- 시크릿이 로그에 노출되면 마스킹이 우회될 수 있습니다
- `github-governance.md`에서 명시적 BLOCK 등급 위반입니다

**안전한 대안:**

```yaml
# ❌ 위험 — 시크릿 로그 출력
- run: echo ${{ secrets.API_KEY }}

# ✅ 안전 — 마스킹된 환경 변수로 전달
- run: ./script.sh
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

OIDC 기반 클라우드 자격증명을 장기 시크릿 대신 사용하는 것을 권장합니다.
