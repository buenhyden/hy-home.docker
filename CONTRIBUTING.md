# Contributing

Please follow these steps when contributing infra services or configuration changes.

1. Read the PR template: use `.github/PULL_REQUEST_TEMPLATE.md` and fill the checklist before creating a PR.
2. Validate compose: run `docker compose -f Infra/docker-compose.yml config` locally or use `./scripts/validate_compose_change.sh`.
3. If adding a service, use the scaffold script to create a starter: `./scripts/new_infra_service.sh my-service` (or PowerShell `.\scripts\new_infra_service.ps1 my-service`) and then update documentation.
4. Do NOT commit secrets. Add required secret filenames to `secrets/` locally and reference them in `Infra/docker-compose.yml`.
5. CI will run validation and script tests on PRs that touch `Infra/` or `scripts/`.

- CI behavior: CI detects changed `Infra/<service>` dirs and runs smoke-tests for each changed service in parallel. CI will also check that the PR body `Infra/...` list matches the detected services; mismatches fail the build.

If you need help, ask in the issue or open a draft PR for early feedback.

CI workflow: The infra validation pipeline is implemented in `.github/workflows/ci-cd.yaml`.

## 로컬 테스트 실행 방법

- POSIX (Linux/macOS):

```bash
# Compose validation
./scripts/validate_compose_change.sh

# Lint + Shell tests
sudo apt-get install -y shellcheck || true
chmod +x scripts/tests/*.sh
./scripts/tests/test_new_infra_service.sh
./scripts/tests/test_validate_compose_change.sh
```

- PowerShell (Windows):

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
Install-Module PSScriptAnalyzer -Scope CurrentUser -Force
.
.\scripts\tests\test_new_infra_service.ps1
.\scripts\tests\test_validate_compose_change.ps1
```

## PR 본문과 감지된 서비스 일치 확인 (로컬)

다음 명령으로 PR에서 감지되는 서비스 목록을 로컬에서 확인할 수 있습니다:

```bash
BASE=main
CHANGED_FILES=$(git diff --name-only $BASE...HEAD)
# Only match files under Infra/<service>/... so we don't include top-level infra files
SERVICES=$(echo "$CHANGED_FILES" | grep -E '^Infra/[^/]+/' | awk -F'/' '{print $2}' | sort -u | tr '\n' ' ')
echo "Detected services: $SERVICES"
```

그 후 PR 본문에 작성한 `Infra/...` 목록과 비교하세요.
