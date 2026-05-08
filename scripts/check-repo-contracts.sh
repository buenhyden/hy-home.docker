#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

failures=0

fail() {
  echo "FAIL: $1" >&2
  failures=$((failures + 1))
}

section() {
  echo
  echo "==> $1"
}

section "Docs top-level structure"
allowed_docs=(
  "00.agent-governance"
  "01.prd"
  "02.ard"
  "03.adr"
  "04.specs"
  "05.plans"
  "06.tasks"
  "07.guides"
  "08.operations"
  "09.runbooks"
  "10.incidents"
  "90.references"
  "99.templates"
)

mapfile -t actual_docs < <(find docs -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
expected_docs="$(printf '%s\n' "${allowed_docs[@]}" | sort)"
actual_docs_text="$(printf '%s\n' "${actual_docs[@]}")"

if [[ "$actual_docs_text" != "$expected_docs" ]]; then
  fail "docs top-level folders do not match the allowed taxonomy"
  echo "Expected:" >&2
  printf '  %s\n' "${allowed_docs[@]}" >&2
  echo "Actual:" >&2
  printf '  %s\n' "${actual_docs[@]}" >&2
fi

section "Required README files"
for d in "${allowed_docs[@]}"; do
  readme="docs/$d/README.md"
  if [[ ! -f "$readme" ]]; then
    fail "missing required README: $readme"
    continue
  fi
  if ! grep -Eiq '(^## (Purpose|Overview|Context and Objective|목적)|^## 1\. Context and Objective)' "$readme"; then
    fail "$readme missing purpose/overview section"
  fi
  if ! grep -Eiq '(^## (Scope|포함할 내용|Requirements and Constraints|Directory Structure|Structure|템플릿-폴더 매핑)|^## 2\. Requirements and Constraints|^## 3\. Directory Structure)' "$readme"; then
    fail "$readme missing allowed content/structure section"
  fi
  if ! grep -Eiq '(^## (Related Documents|Related References|관련 문서)|Related Documents|Related References)' "$readme"; then
    fail "$readme missing related folders/documents section"
  fi
  if ! grep -Eiq '(Example|Examples|예시|Structure|Directory Structure|권장 하위 구조|템플릿-폴더 매핑)' "$readme"; then
    fail "$readme missing examples or structure guidance"
  fi
done

section "Template inventory"
required_templates=(
  "adr.template.md"
  "agent-design.template.md"
  "api-spec.template.md"
  "ard.template.md"
  "data-model.template.md"
  "guide.template.md"
  "incident.template.md"
  "openapi.template.yaml"
  "operation.template.md"
  "plan.template.md"
  "postmortem.template.md"
  "prd.template.md"
  "readme.template.md"
  "reference.template.md"
  "runbook.template.md"
  "schema.template.graphql"
  "service.template.proto"
  "spec.template.md"
  "task.template.md"
  "tests.template.md"
)

for template in "${required_templates[@]}"; do
  [[ -f "docs/99.templates/$template" ]] || fail "missing template: docs/99.templates/$template"
done

mapfile -t misplaced_templates < <(
  find docs -path docs/99.templates -prune -o -type f \
    \( -name '*.template.md' -o -name '*.template.yaml' -o -name '*.template.yml' -o -name '*.template.graphql' -o -name '*.template.proto' \) \
    -print
)
if [[ "${#misplaced_templates[@]}" -gt 0 ]]; then
  fail "templates found outside docs/99.templates"
  printf '  %s\n' "${misplaced_templates[@]}" >&2
fi

section "Banned stale references"
if rg -n 'docs/11|11\.postmortems|\.agent/' README.md AGENTS.md CLAUDE.md GEMINI.md docs infra scripts .github .claude .codex \
  --glob '!graphify-out/**' \
  --glob '!scripts/check-repo-contracts.sh' >/tmp/check-repo-contracts-banned.txt; then
  fail "stale docs/11, 11.postmortems, or .agent references remain"
  cat /tmp/check-repo-contracts-banned.txt >&2
fi
rm -f /tmp/check-repo-contracts-banned.txt

section "GitHub Actions YAML and duplicate workflow steps"
if ! python3 - <<'PY'
from __future__ import annotations

import collections
import pathlib
import re
import sys

try:
    import yaml
except Exception as exc:
    print(f"FAIL: PyYAML is required for GitHub Actions YAML parsing: {exc}", file=sys.stderr)
    sys.exit(1)

failures = 0
workflow_files = sorted(
    list(pathlib.Path(".github/workflows").glob("*.yml"))
    + list(pathlib.Path(".github/workflows").glob("*.yaml"))
)
yaml_files = sorted(
    list(pathlib.Path(".github").rglob("*.yml"))
    + list(pathlib.Path(".github").rglob("*.yaml"))
)

for path in yaml_files:
    try:
        yaml.safe_load(path.read_text())
    except Exception as exc:
        print(f"FAIL: YAML parse failed: {path}: {exc}", file=sys.stderr)
        failures += 1

for path in workflow_files:
    text = path.read_text()
    step_names = re.findall(r"(?m)^\s*-\s+name:\s*(.+)$", text)
    duplicate_steps = [(name, count) for name, count in collections.Counter(step_names).items() if count > 1]
    if duplicate_steps:
        print(f"FAIL: duplicate workflow step names in {path}: {duplicate_steps}", file=sys.stderr)
        failures += 1

    in_jobs = False
    job_ids: list[str] = []
    for line in text.splitlines():
        if re.match(r"^jobs:\s*$", line):
            in_jobs = True
            continue
        if in_jobs and re.match(r"^[A-Za-z0-9_-]+:", line):
            in_jobs = False
        if in_jobs:
            match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
            if match:
                job_ids.append(match.group(1))
    duplicate_jobs = [(name, count) for name, count in collections.Counter(job_ids).items() if count > 1]
    if duplicate_jobs:
        print(f"FAIL: duplicate workflow job ids in {path}: {duplicate_jobs}", file=sys.stderr)
        failures += 1

if failures:
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "GitHub workflow security contracts"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import re
import sys

try:
    import yaml
except Exception as exc:
    print(f"FAIL: PyYAML is required for GitHub workflow contract checks: {exc}", file=sys.stderr)
    sys.exit(1)

failures: list[str] = []
workflow_files = sorted(
    list(pathlib.Path(".github/workflows").glob("*.yml"))
    + list(pathlib.Path(".github/workflows").glob("*.yaml"))
)
sha_re = re.compile(r"^[0-9a-f]{40}$")

for path in workflow_files:
    text = path.read_text()
    data = yaml.safe_load(text) or {}
    jobs = data.get("jobs") or {}
    top_permissions = data.get("permissions")

    if "pull_request_target:" in text:
        failures.append(f"{path}: pull_request_target is not allowed")
    if re.search(r"(?m)^\s*contents:\s*write\s*(#.*)?$", text):
        failures.append(f"{path}: contents: write is not allowed")
    if "git push origin main" in text:
        failures.append(f"{path}: direct push to main is not allowed")

    for line_no, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*uses:\s*([^#\s]+)", line)
        if not match:
            continue
        action = match.group(1).strip("'\"")
        if action.startswith("./"):
            continue
        if "@" not in action:
            failures.append(f"{path}:{line_no}: action reference is missing a pinned ref: {action}")
            continue
        ref = action.rsplit("@", 1)[1]
        if not sha_re.fullmatch(ref):
            failures.append(f"{path}:{line_no}: action reference must use a full commit SHA: {action}")

    if top_permissions is None:
        for job_id, job in jobs.items():
            if isinstance(job, dict) and "permissions" not in job:
                failures.append(f"{path}: job {job_id!r} is missing explicit permissions")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "GitHub governance surface"
if [[ -f ".github/copilot-instructions.md" || -d ".github/instructions" ]]; then
  fail "GitHub-native instruction files are not adopted in this repository"
fi

if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import sys

codeowners = pathlib.Path(".github/CODEOWNERS")
if not codeowners.is_file():
    print("FAIL: missing .github/CODEOWNERS", file=sys.stderr)
    sys.exit(1)

required_patterns = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "RTK.md",
    ".github/**",
    ".claude/**",
    ".codex/**",
    "infra/**",
    "scripts/**",
    "secrets/**",
    "docs/00.agent-governance/**",
}

patterns = set()
for line in codeowners.read_text().splitlines():
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        continue
    patterns.add(stripped.split()[0])

missing = sorted(required_patterns - patterns)
if missing:
    for pattern in missing:
        print(f"FAIL: CODEOWNERS missing required governance pattern: {pattern}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Runtime harness catalog"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []

runtime_agents = sorted(p.stem for p in pathlib.Path(".claude/agents").glob("*.md"))
governance_agents = sorted(p.stem for p in pathlib.Path("docs/00.agent-governance/agents/agents").glob("*.md"))
if runtime_agents != governance_agents:
    failures.append(f"runtime agent catalog mismatch: .claude={runtime_agents} governance={governance_agents}")

runtime_functions = sorted(p.parent.name for p in pathlib.Path(".claude/skills").glob("*/skill.md"))
governance_functions = sorted(p.stem for p in pathlib.Path("docs/00.agent-governance/agents/functions").glob("*.md"))
if runtime_functions != governance_functions:
    failures.append(f"runtime function catalog mismatch: .claude={runtime_functions} governance={governance_functions}")

protocol = pathlib.Path("docs/00.agent-governance/subagent-protocol.md").read_text()
for agent in runtime_agents:
    path = f".claude/agents/{agent}.md"
    if path not in protocol:
        failures.append(f"subagent protocol missing runtime agent: {path}")

stale_patterns = [
    re.compile(r"H100|h100_pattern|examples/harness-100"),
    re.compile(r"AGENTS\.md §3 Agent Catalog|AGENTS\.md §4 Orchestration"),
]
scan_roots = [
    pathlib.Path("AGENTS.md"),
    pathlib.Path("CLAUDE.md"),
    pathlib.Path("GEMINI.md"),
    pathlib.Path(".claude"),
    pathlib.Path(".codex"),
    pathlib.Path("docs/00.agent-governance"),
]

files: list[pathlib.Path] = []
for root in scan_roots:
    if root.is_file():
        files.append(root)
    elif root.exists():
        files.extend(p for p in root.rglob("*") if p.is_file() and "memory" not in p.parts)

for path in files:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for pattern in stale_patterns:
        for match in pattern.finditer(text):
            failures.append(f"{path}: stale runtime/governance reference: {match.group(0)}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Script reference integrity"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import re
import sys

roots = [
    pathlib.Path(p)
    for p in [
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "docs",
        "infra",
        "scripts",
        ".github",
        ".claude",
        ".codex",
        "secrets",
        ".pre-commit-config.yaml",
        "docker-compose.yml",
    ]
    if pathlib.Path(p).exists()
]

failures: list[str] = []
pattern = re.compile(r"(?<![\w./-])(\./)?(scripts/[A-Za-z0-9._/-]+\.sh)")

for root in roots:
    files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file() and "graphify-out" not in p.parts]
    for path in files:
        if path == pathlib.Path("scripts/check-repo-contracts.sh"):
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        for match in pattern.finditer(text):
            ref = match.group(2)
            local_target = path.parent / ref
            root_target = pathlib.Path(ref)
            if local_target.is_file() or root_target.is_file():
                continue
            failures.append(f"{path}: missing script reference {match.group(0)}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Root script inventory"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import sys

readme = pathlib.Path("scripts/README.md")
if not readme.is_file():
    print("FAIL: missing scripts/README.md", file=sys.stderr)
    sys.exit(1)

readme_text = readme.read_text()
failures: list[str] = []

for path in sorted(pathlib.Path("scripts").glob("*.sh")):
    if not path.is_file():
        continue
    if path.name not in readme_text and str(path) not in readme_text:
        failures.append(f"scripts/README.md missing root script inventory entry: {path}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Floating image tag policy"
if ! python3 - <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

exceptions_path = pathlib.Path("infra/image-tag-policy.exceptions.json")
if not exceptions_path.is_file():
    print(f"FAIL: missing image tag exception registry: {exceptions_path}", file=sys.stderr)
    sys.exit(1)

exceptions_data = json.loads(exceptions_path.read_text())
exceptions = {
    item["image"]
    for item in exceptions_data.get("floating_image_exceptions", [])
    if item.get("image") and item.get("owner") and item.get("reason") and item.get("review_cadence")
}

floating_suffixes = (":main", ":latest", ":stable", ":edge", ":nightly", ":dev", ":sts", ":alpine")
failures: list[str] = []

def is_floating(image: str) -> bool:
    tag = image.rsplit(":", 1)[-1] if ":" in image.rsplit("/", 1)[-1] else ""
    if not tag:
        return True
    return image.endswith(floating_suffixes) or "latest" in tag

for path in sorted(pathlib.Path("infra").rglob("*")):
    if not path.is_file():
        continue
    if path.name.startswith("docker-compose") and path.suffix in {".yml", ".yaml"}:
        for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"image:\s*['\"]?([^'\"\s#]+)", stripped)
            if match:
                image = match.group(1)
                if is_floating(image) and image not in exceptions:
                    failures.append(f"{path}:{line_no}: floating image tag requires exception or pinned tag: {image}")
    elif path.name.endswith("Dockerfile") or path.name == "Dockerfile":
        for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"FROM\s+([^@\s]+)", stripped)
            if match:
                image = match.group(1)
                if is_floating(image) and image not in exceptions:
                    failures.append(f"{path}:{line_no}: floating base image tag requires exception or pinned tag: {image}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Tech-stack version drift"
if ! python3 - <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

registry_path = pathlib.Path("infra/tech-stack.versions.json")
if not registry_path.is_file():
    print(f"FAIL: missing tech-stack version registry: {registry_path}", file=sys.stderr)
    sys.exit(1)

try:
    registry = json.loads(registry_path.read_text())
except Exception as exc:
    print(f"FAIL: invalid JSON in {registry_path}: {exc}", file=sys.stderr)
    sys.exit(1)

entries = registry.get("entries")
if not isinstance(entries, list) or not entries:
    print(f"FAIL: {registry_path} must define a non-empty entries list", file=sys.stderr)
    sys.exit(1)

failures: list[str] = []
image_line_re = re.compile(r"(?m)^\s*image:\s*['\"]?([^'\"\s#]+)")
default_image_re = re.compile(r"\$\{[^}:]+:-([^}]+)\}")

def declared_images(path: pathlib.Path) -> set[str]:
    text = path.read_text(errors="ignore")
    images: set[str] = set()
    for match in image_line_re.finditer(text):
        raw = match.group(1)
        images.add(raw)
        default_match = default_image_re.search(raw)
        if default_match:
            images.add(default_match.group(1))
    return images

for index, entry in enumerate(entries, start=1):
    component = entry.get("component")
    images = entry.get("images")
    compose_files = entry.get("compose_files")

    if not component or not isinstance(images, list) or not images or not isinstance(compose_files, list) or not compose_files:
        failures.append(f"{registry_path}: entry #{index} must include component, images, and compose_files")
        continue

    discovered: set[str] = set()
    for compose_file in compose_files:
        compose_path = pathlib.Path(compose_file)
        if not compose_path.is_file():
            failures.append(f"{registry_path}: {component} references missing compose file: {compose_file}")
            continue
        discovered.update(declared_images(compose_path))

    for image in images:
        if image not in discovered:
            failures.append(f"{registry_path}: {component} expected image not declared in listed compose files: {image}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

echo
echo "Repo contract check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: repository Docker/docs contracts are synchronized"
