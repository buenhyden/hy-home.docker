# Infra Team Agent Cross-Validation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a Pipeline Team Agent pattern where every infrastructure change automatically triggers security-auditor then iac-reviewer cross-validation, while integrating performance checks performance checks and hardening settings.json permissions.

**Architecture:** Three existing agents gain a `## Team Communication Protocol` section that defines SendMessage contracts. A new orchestrator skill `infra-cross-validate` wires the pipeline. `settings.json` is reconstructed with a full permission audit. No new agents are created.

**Tech Stack:** Markdown agent/skill files, JSON settings, `.pre-commit-config.yaml` hooks (markdownlint, detect-secrets)

**Spec:** `docs/superpowers/specs/2026-04-10-infra-team-agent-design.md`

---

## Chunk 1: Agent file updates

### Task 1: Add team communication protocol to `infra-implementer.md`

**Files:**

- Modify: `.claude/agents/infra-implementer.md`

- [ ] **Step 1: Verify current state (pre-condition check)**

```bash
grep -n "Team Communication" .claude/agents/infra-implementer.md
```

Expected: no matches (section does not exist yet)

- [ ] **Step 2: Add team communication protocol section**

Append the following section before `## Related Documents` in `.claude/agents/infra-implementer.md`:

```markdown
## Team Communication Protocol

- **Sends to**: `security-auditor` — `"audit-request: <file-list>"` immediately after change is applied and post-flight check passes
- **Receives from**: `security-auditor` — `"BLOCK: <reason>"` (roll back change → escalate to user) or `"audit-complete"` (continue)
- **Receives from**: `iac-reviewer` — `"validate-complete: PASS|WARN <summary>"`
- **On BLOCK**: revert the applied change, record reason in `_workspace/`, escalate to user — do not proceed
- **On WARN**: record findings in `memory/progress.md`, optionally notify user, do not block
```

- [ ] **Step 3: Verify section added correctly**

```bash
grep -n "Team Communication\|audit-request\|BLOCK\|WARN" .claude/agents/infra-implementer.md
```

Expected: 6+ matches showing all key terms present

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/infra-implementer.md
git commit -m "feat(agents): add team communication protocol to infra-implementer"
```

Expected: pre-commit hooks pass, commit succeeds

---

### Task 2: Add team communication protocol + image-audit to `security-auditor.md`

**Files:**

- Modify: `.claude/agents/security-auditor.md`

- [ ] **Step 1: Verify current state**

```bash
grep -n "Team Communication\|image ls\|docker image" .claude/agents/security-auditor.md
```

Expected: no matches

- [ ] **Step 2: Add team communication protocol section**

Append before `## Related Documents` in `.claude/agents/security-auditor.md`:

```markdown
## Team Communication Protocol

- **Receives from**: `infra-implementer` — `"audit-request: <file-list>"`
- **Sends (CRIT)**: `infra-implementer` — `"BLOCK: <reason>"` → pipeline halts immediately
- **Sends (PASS)**: `iac-reviewer` — `"validate-request: <file-list>"`
```

- [ ] **Step 3: Add image-audit to Task Principles**

In the `## Task Principles` section, add as item 6 after the existing GitHub Actions item:

```markdown
6. **Image audit**: for changed services, run `docker image ls <image>` to confirm pinned digest or known tag; flag unpinned `latest` tag as WARN finding.
```

- [ ] **Step 4: Verify**

```bash
grep -n "Team Communication\|audit-request\|BLOCK\|validate-request\|image audit\|docker image ls" .claude/agents/security-auditor.md
```

Expected: 7+ matches

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/security-auditor.md
git commit -m "feat(agents): add team protocol and image-audit principle to security-auditor"
```

---

### Task 3: Update `iac-reviewer.md` — frontmatter, team protocol, performance checks performance checklist

**Files:**

- Modify: `.claude/agents/iac-reviewer.md`

- [ ] **Step 1: Verify current frontmatter**

```bash
head -6 .claude/agents/iac-reviewer.md
```

Expected: `pattern: '26-infra-as-code/drift-detector'`

- [ ] **Step 2: Update frontmatter pattern**

Change line:

```yaml
pattern: '26-infra-as-code/drift-detector'
```

To:

```yaml
pattern: '26+29'
```

- [ ] **Step 3: Add team communication protocol section**

Append before `## Related Documents`:

```markdown
## Team Communication Protocol

- **Receives from**: `security-auditor` — `"validate-request: <file-list>"`
- **Sends to**: `infra-implementer` — `"validate-complete: PASS|WARN <summary>"`
- **On completion**: write findings to `_workspace/cross-validate_<YYYY-MM-DD>.md`
```

- [ ] **Step 4: Extend Drift Detection Checklist with performance checks performance items**

In the `## Drift Detection Checklist` section, append after the existing items:

```markdown
- [ ] **[performance checks]** `LATENCY_SLO < 200ms` — health-check defined for all services that affect gateway latency
- [ ] **[performance checks]** `mem_limit` and `cpus` declared on every container (absent = unconstrained resource use → WARN)
- [ ] **[performance checks]** `restart` policy set (`unless-stopped` or `on-failure`) on all stateful services
- [ ] **[performance checks]** Resource ceiling present on stateful services (PostgreSQL, Kafka, OpenSearch, MinIO)
```

- [ ] **Step 5: Verify all changes**

```bash
grep -n "pattern\|Team Communication\|validate-request\|performance checks\|mem_limit\|LATENCY_SLO" .claude/agents/iac-reviewer.md
```

Expected: 8+ matches covering all changes

- [ ] **Step 6: Commit**

```bash
git add .claude/agents/iac-reviewer.md
git commit -m "feat(agents): add performance checks performance checks and team protocol to iac-reviewer"
```

---

### Task 4: Update `AGENTS.md` catalog row for `iac-reviewer`

**Files:**

- Modify: `AGENTS.md`

- [ ] **Step 1: Find current catalog row**

```bash
grep -n "iac-reviewer" AGENTS.md
```

Expected: line containing `drift checks drift-detector (r/o)`

- [ ] **Step 2: Update catalog row**

Change the `iac-reviewer` row from:

```text
| `iac-reviewer`       | `.claude/agents/iac-reviewer.md`       | `scopes/infra.md`    | drift checks drift-detector (r/o)   |
```

To:

```text
| `iac-reviewer`       | `.claude/agents/iac-reviewer.md`       | `scopes/infra.md`    | drift + performance checks drift+perf (r/o)    |
```

- [ ] **Step 3: Verify**

```bash
grep -n "iac-reviewer" AGENTS.md
```

Expected: `drift + performance checks drift+perf (r/o)` visible

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md
git commit -m "docs(agents): update iac-reviewer catalog to drift + performance checks"
```

---

## Chunk 2: New orchestrator skill

### Task 5: Create `.claude/skills/infra-cross-validate.md`

**Files:**

- Create: `.claude/skills/infra-cross-validate.md`

- [ ] **Step 1: Verify skill does not exist yet**

```bash
ls .claude/skills/
```

Expected: `incident-response.md` and `infra-validate.md` only — no `infra-cross-validate.md`

- [ ] **Step 2: Create orchestrator skill file**

Create `.claude/skills/infra-cross-validate.md` with the following content:

````markdown
---
name: infra-cross-validate
description: >
  인프라 변경 후 security-auditor → iac-reviewer 교차 검증 파이프라인 오케스트레이터.
  infra-implementer가 변경을 적용한 직후, 반드시 이 스킬을 사용하여 보안 감사와
  드리프트+성능 검증을 순서대로 실행할 것.
  CRIT 발견 시 파이프라인을 즉시 중단하고 롤백 지시를 내린다.
---

# infra-cross-validate

security + drift + performance checks — 인프라 변경 후 교차 검증 파이프라인 오케스트레이터.
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

iac-reviewer 수행 항목 (drift checks 기존 + performance checks 신규):

**드리프트 체크 (drift checks):**

- 모든 서비스가 `infra_net` 네트워크 사용 확인
- `no-new-privileges: true` 전 컨테이너 존재 확인
- 시크릿이 `secrets:` 블록으로만 참조 확인
- 볼륨명 `[Service]-[Data]-[Volume]` 규칙 준수 확인
- health-check 정의 여부 확인
- restart policy 설정 여부 확인
- 리소스 제한 (`mem_limit` / `cpus`) 선언 여부 확인

**성능 체크 (performance checks):**

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

````

- [ ] **Step 3: Verify file created and frontmatter valid**

```bash
head -8 .claude/skills/infra-cross-validate.md
```

Expected: frontmatter with `name: infra-cross-validate` and description visible

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/infra-cross-validate.md
git commit -m "feat(skills): add infra-cross-validate pipeline orchestrator skill"
```

Expected: markdownlint passes (all fenced code blocks have language specified)

---

## Chunk 3: settings.json reconstruction + progress record

### Task 6: Reconstruct `.claude/settings.json` with full permission audit

**Files:**

- Modify: `.claude/settings.json`

- [ ] **Step 1: Record current state for comparison**

```bash
cat .claude/settings.json
```

Note which permissions are present. Expected allow list (current):
`ls`, `grep`, `cat`, `git`, `python3`, `bash scripts/validate-docker-compose.sh`, `docker compose ps`, `docker ps`

- [ ] **Step 2: Rewrite settings.json**

Replace the entire `permissions.allow` array with the audited list:

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(python3:*)",
      "Bash(grep:*)",
      "Bash(docker ps:*)",
      "Bash(docker compose ps:*)",
      "Bash(docker compose config:*)",
      "Bash(docker compose logs:*)",
      "Bash(docker inspect:*)",
      "Bash(docker image ls:*)",
      "Bash(bash scripts/validate-docker-compose.sh:*)",
      "Bash(bash scripts/check-all-hardening.sh:*)",
      "Bash(bash scripts/check-doc-traceability.sh:*)",
      "Bash(bash scripts/check-template-security-baseline.sh:*)"
    ],
    "deny": [
      "Bash(docker system prune:*)",
      "Bash(rm -rf:*)",
      "Bash(docker compose down:*)",
      "Bash(docker volume rm:*)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh",
            "timeout": 15
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/docker-compose-pre.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-validate.sh",
            "timeout": 30
          }
        ]
      }
    ]
  },
  "deniedMcpServers": [{ "serverName": "MCP_DOCKER" }, { "serverName": "notebooklm" }]
}
```

Removed: `Bash(cat:*)`, `Bash(ls:*)`
Added: `docker compose config`, `docker compose logs`, `docker inspect`, `docker image ls`, 3 check scripts
New deny: `docker compose down`, `docker volume rm`

- [ ] **Step 3: Validate JSON syntax**

```bash
python3 -c "import json; json.load(open('.claude/settings.json')); print('JSON valid')"
```

Expected: `JSON valid`

- [ ] **Step 4: Verify removed permissions are gone**

```bash
grep -c '"Bash(cat:\*)"\\|"Bash(ls:\*)"' .claude/settings.json
```

Expected: `0`

- [ ] **Step 5: Verify new permissions present**

```bash
grep "docker compose config\|docker compose logs\|docker inspect\|docker image ls\|check-all-hardening\|compose down" .claude/settings.json
```

Expected: 5 allow lines + 1 deny line visible

- [ ] **Step 6: Commit**

```bash
git add .claude/settings.json
git commit -m "chore(settings): full permission audit — add 5 infra cmds, remove cat/ls, add 2 deny entries"
```

---

### Task 7: Append P5 alignment record to `memory/progress.md`

**Files:**

- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Verify current last phase**

```bash
grep "^| P" docs/00.agent-governance/memory/progress.md
```

Expected: last entry is `P4 — GitHub governance alignment`

- [ ] **Step 2: Add P5 phase row to Phase Tracker table**

Append to the Phase Tracker table:

```markdown
| P5 — Infra Team Agent cross-validation | ✅ Done | 2026-04-10 | Pipeline Team Agent: infra-implementer→security-auditor→iac-reviewer; drift + performance checks in iac-reviewer; infra-cross-validate skill created; settings.json reconstructed |
```

- [ ] **Step 3: Add P5 audit section**

Append after the GitHub Governance Alignment Audit section:

```markdown
## Infra Team Agent Alignment Audit (P5 — 2026-04-10)

| Area | Status | Notes |
| ---- | ------ | ----- |
| infra-implementer team protocol | ✅ Updated | SendMessage contracts for audit-request / BLOCK / WARN |
| security-auditor team protocol | ✅ Updated | audit-request receiver; BLOCK/PASS sender; image-audit principle |
| iac-reviewer drift + performance checks | ✅ Updated | Frontmatter updated; performance checklist added; team protocol added |
| AGENTS.md catalog | ✅ Updated | iac-reviewer row updated to drift + performance checks |
| infra-cross-validate skill | ✅ Created | Pipeline orchestrator with error handling and test scenarios |
| settings.json permissions | ✅ Reconstructed | 13 allow (net +5), 4 deny (net +2); cat/ls removed |
```

- [ ] **Step 4: Verify**

```bash
grep -n "P5\|infra-cross-validate\|drift + performance checks" docs/00.agent-governance/memory/progress.md
```

Expected: 4+ matches

- [ ] **Step 5: Commit**

```bash
git add docs/00.agent-governance/memory/progress.md
git commit -m "docs(memory): record P5 infra team agent alignment audit"
```

---

## Final Verification

- [ ] **Run all validation scripts**

```bash
bash scripts/validate-docker-compose.sh && \
bash scripts/check-doc-traceability.sh && \
bash scripts/check-template-security-baseline.sh
```

Expected: all 3 scripts report PASS

- [ ] **Verify no plaintext secrets introduced**

```bash
bash scripts/check-all-hardening.sh 2>&1 | grep -i "secret\|password\|token" | grep -v "^#\|grep\|pattern"
```

Expected: no credential leaks reported

- [ ] **Verify git log shows all 7 commits clean**

```bash
git log --oneline -8
```

Expected: 7 feat/docs/chore commits, all passed pre-commit hooks

---

## Related Documents

- Spec: `docs/superpowers/specs/2026-04-10-infra-team-agent-design.md`
- `docs/00.agent-governance/scopes/infra.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/github-governance.md`
