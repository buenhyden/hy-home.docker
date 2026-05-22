---
name: block-plaintext-secret-compose
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (docker-compose|compose)[^/]*\.ya?ml$|infra/[^/]*\.ya?ml$
  - field: new_text
    operator: regex_match
    pattern: \b(PASSWORD|SECRET_KEY|API_KEY|ACCESS_TOKEN|PRIVATE_KEY|WEBHOOK_SECRET|DB_PASS(?:WORD)?|POSTGRES_PASSWORD|MYSQL_PASSWORD|REDIS_PASSWORD|GRAFANA_PASSWORD|MARIADB_PASSWORD)(?!_FILE)\s*[:=]\s*(?!\$\{|\$\(\(|/run/secrets/|["']?\$|\s*$|\s*["']{2})[^\s\n"']{6,}
action: block
---

🚫 **Docker Compose 파일에 플레인텍스트 시크릿 감지됨 (프로젝트 규칙)**

`AGENTS.md` — Hard Constraints 정책 위반:

> "Never write plaintext secrets; use Docker Secrets or `secrets/` mounts."

`docs/00.agent-governance/rules/quality-standards.md` — Requirements:

> "Never commit plaintext credentials."

**감지된 패턴 예시:**
```yaml
# ❌ 금지 — 플레인텍스트 시크릿
environment:
  POSTGRES_PASSWORD: mysecretpassword
  MYSQL_PASSWORD: hunter2
  API_KEY: abc123xyz
```

**올바른 대안:**

```yaml
# ✅ 방법 1: Docker Secrets 참조
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  db:
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

# ✅ 방법 2: 환경 변수 참조 (값은 .env 또는 외부 주입)
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

# ✅ 방법 3: .env 파일 사용 (git에서 제외)
env_file:
  - .env
```

**제외 조건:** `_FILE` 접미사, `${...}` 변수 참조, `/run/secrets/` 경로, 빈 값은 감지하지 않습니다.
