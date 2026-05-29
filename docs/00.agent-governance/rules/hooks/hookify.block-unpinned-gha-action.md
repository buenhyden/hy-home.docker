---
name: block-unpinned-gha-action
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.github/workflows/.*\.ya?ml$
  - field: new_text
    operator: regex_match
    pattern: uses:\s+\S+@(latest|main|master|develop|dev)\b
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

🚫 **GitHub Actions 플로팅 레퍼런스 차단됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/github-governance.md` — GitHub Actions Security Contract: 워크플로우에서 플로팅 브랜치/태그 레퍼런스를 사용하고 있습니다.

**감지된 패턴:** `uses: owner/action@latest` / `@main` / `@master` / `@develop`

**왜 위험한가요?**

- 외부 액션이 언제든지 악의적으로 변경될 수 있습니다
- 공급망 공격(supply chain attack)에 취약합니다
- 재현 가능한 빌드를 보장할 수 없습니다

**안전한 대안:**

```yaml
# ❌ 위험 — 플로팅 레퍼런스
- uses: actions/checkout@main
- uses: actions/setup-python@latest

# ✅ 안전 — 특정 버전 또는 SHA 핀
- uses: actions/checkout@v4.2.2
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Commit SHA 핀이 가장 안전합니다. 버전 태그를 사용할 경우 digest 검증을 권장합니다.

## Related Documents

- `docs/00.agent-governance/README.md`
