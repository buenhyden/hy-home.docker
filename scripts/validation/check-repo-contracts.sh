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
  "01.requirements"
  "02.architecture"
  "03.specs"
  "04.execution"
  "05.operations"
  "90.references"
  "98.archive"
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
  "templates/common/archive.template.md"
  "templates/common/readme.template.md"
  "templates/common/reference.template.md"
  "templates/governance/harness-task-contract.template.md"
  "templates/governance/memory.template.md"
  "templates/governance/progress.template.md"
  "templates/operations/guide.template.md"
  "templates/operations/incident.template.md"
  "templates/operations/policy.template.md"
  "templates/operations/postmortem.template.md"
  "templates/operations/runbook.template.md"
  "templates/sdlc/adr.template.md"
  "templates/sdlc/ard.template.md"
  "templates/sdlc/plan.template.md"
  "templates/sdlc/prd.template.md"
  "templates/sdlc/spec.template.md"
  "templates/sdlc/task.template.md"
  "templates/spec-contracts/agent-design.template.md"
  "templates/spec-contracts/api-spec.template.md"
  "templates/spec-contracts/data-model.template.md"
  "templates/spec-contracts/openapi.template.yaml"
  "templates/spec-contracts/schema.template.graphql"
  "templates/spec-contracts/service.template.md"
  "templates/spec-contracts/service.template.proto"
  "templates/spec-contracts/tests.template.md"
)

for template in "${required_templates[@]}"; do
  [[ -f "docs/99.templates/$template" ]] || fail "missing template: docs/99.templates/$template"
done

mapfile -t misplaced_templates < <(
  find docs -type f \
    \( -name '*.template.md' -o -name '*.template.yaml' -o -name '*.template.yml' -o -name '*.template.graphql' -o -name '*.template.proto' \) \
    ! -path 'docs/99.templates/templates/*' \
    -print
)
if [[ "${#misplaced_templates[@]}" -gt 0 ]]; then
  fail "templates found outside docs/99.templates/templates"
  printf '  %s\n' "${misplaced_templates[@]}" >&2
fi

section "Stage 99 template and frontmatter contracts"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
templates_root = pathlib.Path("docs/99.templates/templates")
stage99_root = pathlib.Path("docs/99.templates")
legacy_frontmatter_keys = {
    "type",
    "owner",
    "updated",
    "links",
    "document_type",
    "template_type",
}
frontmatter_key_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:")
durable_marker_re = re.compile(
    r"\b("
    r"allowed\s+keys|required\s+keys|must\s+not|must|required|forbidden|"
    r"disallowed|shall|never"
    r")\b",
    flags=re.I,
)


def top_frontmatter(text: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return []
    for index, line in enumerate(lines[1:], start=2):
        if line == "---":
            return [
                (line_no, value)
                for line_no, value in enumerate(lines[1 : index - 1], start=2)
            ]
    return []


def first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def line_routes_to_support(line: str) -> bool:
    return bool(
        re.search(r"\[[^\]]+\]\([^)]*support/[^)]*\)", line)
        or "docs/99.templates/support/" in line
        or "../support/" in line
        or "../../support/" in line
        or "./support/" in line
    )


def nearby_routes_to_support(lines: list[str], index: int, window: int = 2) -> bool:
    lower_bound = max(0, index - window)
    upper_bound = min(len(lines), index + window + 1)
    return any(line_routes_to_support(line) for line in lines[lower_bound:upper_bound])


for path in sorted(templates_root.rglob("*.template.md")):
    text = path.read_text(errors="ignore")
    first_three = text.splitlines()[:3]
    if first_three != ["---", "status: draft", "---"]:
        failures.append(
            f"{path}: Markdown template must start exactly with '---', 'status: draft', '---'"
        )
    if "Target:" not in text:
        failures.append(f"{path}: Markdown template missing Target path guidance")
    if "target-relative" not in text.lower():
        failures.append(f"{path}: Markdown template missing target-relative guidance")
    if "## Related Documents" not in text:
        failures.append(f"{path}: Markdown template missing ## Related Documents")

for path in sorted(templates_root.rglob("*.template.*")):
    if path.suffix == ".md":
        continue
    text = path.read_text(errors="ignore")
    if first_non_empty_line(text) == "---":
        failures.append(f"{path}: machine-readable template must not use YAML frontmatter")
    if "Target:" not in text:
        failures.append(f"{path}: machine-readable template missing Target path guidance")
    if "Cross-links:" not in text:
        failures.append(f"{path}: machine-readable template missing Cross-links ownership note")
    if "## Related Documents" in text:
        failures.append(f"{path}: machine-readable template must not include Markdown ## Related Documents")

for path in sorted(stage99_root.rglob("*.md")):
    text = path.read_text(errors="ignore")
    for line_no, line in top_frontmatter(text):
        match = frontmatter_key_re.match(line)
        if match and match.group(1) in legacy_frontmatter_keys:
            failures.append(
                f"{path}:{line_no}: legacy duplicate-purpose frontmatter key is not allowed: {match.group(1)}"
            )

for path in sorted(stage99_root.rglob("README.md")):
    if path == pathlib.Path("docs/99.templates/support/README.md"):
        continue
    text = path.read_text(errors="ignore")
    lines = text.splitlines()
    in_fence = False
    for index, line in enumerate(lines):
        line_no = index + 1
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if (
            durable_marker_re.search(line)
            and not nearby_routes_to_support(lines, index)
        ):
            failures.append(
                f"{path}:{line_no}: Stage 99 README asserts a durable template rule; route it to support instead"
            )

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Approved surface evidence template"
if ! grep -q "^## Approved Surface Evidence" docs/99.templates/templates/sdlc/task.template.md; then
  echo "FAIL: docs/99.templates/templates/sdlc/task.template.md must include Approved Surface Evidence for high-risk work" >&2
  failures=$((failures + 1))
fi
if ! grep -q "policy, runtime, CI, templates, secrets, remote GitHub, model policy, or provider" docs/99.templates/templates/sdlc/task.template.md; then
  echo "FAIL: task.template.md Approved Surface Evidence must name high-risk surface classes" >&2
  failures=$((failures + 1))
fi

section "Execution evidence status wording"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []

execution_readmes = [
    pathlib.Path("docs/04.execution/README.md"),
    pathlib.Path("docs/04.execution/plans/README.md"),
    pathlib.Path("docs/04.execution/tasks/README.md"),
]

completed_docs: list[pathlib.Path] = []
for root in [
    pathlib.Path("docs/04.execution/plans"),
    pathlib.Path("docs/04.execution/tasks"),
]:
    if not root.exists():
        continue
    for path in sorted(root.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(errors="ignore")
        head = "\n".join(text.splitlines()[:8])
        if re.search(r"(?m)^status:\s*completed\s*$", head):
            completed_docs.append(path)

for readme in execution_readmes:
    if not readme.is_file():
        failures.append(f"missing execution README for status wording check: {readme}")
        continue
    for line_no, line in enumerate(readme.read_text(errors="ignore").splitlines(), start=1):
        for doc in completed_docs:
            if doc.name in line and re.search(r"\bactive\b", line, re.I):
                failures.append(
                    f"{readme}:{line_no}: completed execution artifact {doc.name} is described as active"
                )

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Target-stage frontmatter status vocabulary"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
stage_roots = tuple(
    pathlib.Path(path)
    for path in [
        "docs/01.requirements",
        "docs/02.architecture",
        "docs/03.specs",
        "docs/04.execution",
        "docs/05.operations",
        "docs/90.references",
        "docs/98.archive",
    ]
)
active_statuses = {"draft", "active", "completed", "superseded"}
archive_statuses = {"archived"}


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


for path in sorted(pathlib.Path("docs").rglob("*.md")):
    if path.name == "README.md":
        continue
    if not any(is_relative_to(path, root) for root in stage_roots):
        continue
    text = path.read_text(errors="ignore")
    head = "\n".join(text.splitlines()[:12])
    match = re.search(r"(?m)^status:\s*([A-Za-z0-9_-]+)\s*$", head)
    if not match:
        failures.append(f"{path}: missing target-stage frontmatter status")
        continue
    status = match.group(1)
    allowed_statuses = archive_statuses if is_relative_to(path, pathlib.Path("docs/98.archive")) else active_statuses
    if status not in allowed_statuses:
        allowed = ", ".join(sorted(allowed_statuses))
        failures.append(f"{path}: unsupported target-stage status {status!r}; expected one of: {allowed}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "English-only closed doc surfaces"
if rg -n '[가-힣]' \
  docs/03.specs docs/04.execution/plans docs/04.execution/tasks docs/90.references \
  --glob '*.md' \
  --glob '!**/README.md' \
  --glob '!docs/90.references/llm-wiki/llm-wiki-index.md' >/tmp/check-repo-contracts-english-only-surfaces.txt; then
  fail "closed English-only doc surfaces contain Korean text"
  cat /tmp/check-repo-contracts-english-only-surfaces.txt >&2
fi
rm -f /tmp/check-repo-contracts-english-only-surfaces.txt

section "Banned stale references"
if rg -n 'docs/11|11\.postmortems|\.agent/|docs/(01\.prd|02\.ard|03\.adr|04\.specs|05\.plans|06\.tasks|07\.operations|07\.guides|08\.operations|09\.runbooks|10\.incidents)|(^|[^[:alnum:]_/-])(01\.prd|02\.ard|03\.adr|04\.specs|05\.plans|06\.tasks|07\.operations|07\.guides|08\.operations|09\.runbooks|10\.incidents)([^[:alnum:]_/-]|$)|harness catalog|Runtime harness catalog' README.md AGENTS.md CLAUDE.md GEMINI.md docs infra scripts .github .claude .codex \
  --glob '!graphify-out/**' \
  --glob '!docs/README.md' \
  --glob '!docs/00.agent-governance/memory/**' \
  --glob '!scripts/validation/check-repo-contracts.sh' \
  --glob '!scripts/validation/check-repo-contracts.sh' >/tmp/check-repo-contracts-banned.txt; then
  fail "stale docs taxonomy, removed operations-stage, harness-catalog, or .agent references remain"
  cat /tmp/check-repo-contracts-banned.txt >&2
fi
rm -f /tmp/check-repo-contracts-banned.txt

section "Numbered SDLC path contracts"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
slug = r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
prd_name = re.compile(rf"[0-9]{{3}}-{slug}\.md")
spec_dir = re.compile(rf"[0-9]{{3}}-{slug}")

prd_root = pathlib.Path("docs/01.requirements")
for path in sorted(prd_root.glob("*.md")):
    if path.name == "README.md":
        continue
    if not prd_name.fullmatch(path.name):
        failures.append(f"{path}: PRD filename must match NNN-feature-or-system.md")

spec_root = pathlib.Path("docs/03.specs")
for path in sorted(child for child in spec_root.iterdir() if child.is_dir()):
    if not spec_dir.fullmatch(path.name):
        failures.append(f"{path}: Spec folder must match NNN-feature-id")

legacy_patterns = [
    re.compile(r"docs/01\.requirements/YYYY-MM-DD-[^\s`)]+"),
    re.compile(r"\.\.?/01\.requirements/YYYY-MM-DD-[^\s`)]+"),
    re.compile(r"docs/03\.specs/<feature-id>/"),
    re.compile(r"docs/03\.specs/feature-id/"),
    re.compile(r"(?<![0-9])03\.specs/<feature-id>/"),
    re.compile(r"(?<![0-9])03\.specs/feature-id/"),
]
for path in sorted(pathlib.Path("docs/99.templates").rglob("*")):
    if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".graphql", ".proto"}:
        continue
    text = path.read_text(errors="ignore")
    for pattern in legacy_patterns:
        match = pattern.search(text)
        if match:
            failures.append(
                f"{path}: legacy PRD/Spec target guidance remains: {match.group(0)}"
            )

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Active docs taxonomy shorthand"
if rg -n 'docs/(0[1-9]~0?9|01~09|01~10|01-03|01-09)|(^|[^[:alnum:]_/.-])01~09([^[:alnum:]_/.-]|$)|PRD~Runbook[[:space:]]*\(01~09\)|문서 계층[[:space:]]*\(01~09\)|문서 체계[[:space:]]*\(01~09\)|optimization-hardening 문서 세트[[:space:]]*\(01~09\)|docs/01[[:space:]]*[–-][[:space:]]*docs/10|docs/01.?to.?docs/10|Stage (06|07|10)|docs/07([^[:alnum:]_.-]|$)|docs/08([^[:alnum:]_.-]|$)|docs/09([^[:alnum:]_.-]|$)|05/08/09|07/08/09' README.md AGENTS.md CLAUDE.md GEMINI.md docs infra scripts .github .claude .codex \
  --glob '!graphify-out/**' \
  --glob '!docs/README.md' \
  --glob '!docs/00.agent-governance/memory/**' \
  --glob '!scripts/validation/check-repo-contracts.sh' \
  --glob '!scripts/validation/check-repo-contracts.sh' >/tmp/check-repo-contracts-taxonomy-shorthand.txt; then
  fail "active docs taxonomy shorthand or legacy stage shorthand remains"
  cat /tmp/check-repo-contracts-taxonomy-shorthand.txt >&2
fi
rm -f /tmp/check-repo-contracts-taxonomy-shorthand.txt

section "Stage docs IP placeholder drift"
if rg -n 'ipv4_address:[[:space:]]*172\.(18|19)\.0\.X{1,3}|172\.19\.0\.X{1,3}|172\.18\.0\.X{1,3}' \
  docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations \
  --glob '*.md' >/tmp/check-repo-contracts-ip-placeholders.txt; then
  fail "stage docs contain concrete-network IP placeholders; use authoritative mapping examples instead"
  cat /tmp/check-repo-contracts-ip-placeholders.txt >&2
fi
rm -f /tmp/check-repo-contracts-ip-placeholders.txt

section "Metadata comparison guide drift"
env_comparison_doc="docs/05.operations/guides/00-workspace/env-key-comparison.md"
if [[ -f ".env.example" && -f ".env" && -f "$env_comparison_doc" ]]; then
  env_example_keys="$(awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{count++} END{print count+0}' .env.example)"
  env_actual_keys="$(awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{count++} END{print count+0}' .env)"
  if ! grep -Eq "\\| \`\\.env\\.example\` 키 수[[:space:]]*\\|[[:space:]]*${env_example_keys}[[:space:]]*\\|" "$env_comparison_doc"; then
    fail "$env_comparison_doc does not record current .env.example key count: $env_example_keys"
  fi
  if ! grep -Eq "\\| \`\\.env\` 키 수[[:space:]]*\\|[[:space:]]*${env_actual_keys}[[:space:]]*\\|" "$env_comparison_doc"; then
    fail "$env_comparison_doc does not record current .env key count: $env_actual_keys"
  fi
  mapfile -t env_example_only < <(comm -23 <(awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' .env.example | sort) <(awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' .env | sort))
  mapfile -t env_actual_only < <(comm -13 <(awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' .env.example | sort) <(awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' .env | sort))
  if [[ "${#env_example_only[@]}" -gt 0 || "${#env_actual_only[@]}" -gt 0 ]]; then
    fail ".env.example and .env key sets differ; update keys or env-key-comparison.md"
    printf '  only in .env.example: %s\n' "${env_example_only[*]:-(none)}" >&2
    printf '  only in .env: %s\n' "${env_actual_only[*]:-(none)}" >&2
  fi
fi

sensitive_comparison_doc="docs/05.operations/guides/00-workspace/sensitive-env-vars-comparison.md"
if [[ -f "secrets/SENSITIVE_ENV_VARS.md.example" && -f "secrets/SENSITIVE_ENV_VARS.md" && -f "$sensitive_comparison_doc" ]]; then
  sensitive_example_lines="$(wc -l <secrets/SENSITIVE_ENV_VARS.md.example | tr -d '[:space:]')"
  sensitive_actual_lines="$(wc -l <secrets/SENSITIVE_ENV_VARS.md | tr -d '[:space:]')"
  sensitive_example_ids="$(rg -o '\b[A-Z]+-[0-9]{3}\b' secrets/SENSITIVE_ENV_VARS.md.example | sort -u | wc -l | tr -d '[:space:]')"
  if ! grep -Eq "\\| Example 파일 라인 수[[:space:]]*\\|[[:space:]]*${sensitive_example_lines}[[:space:]]*\\|" "$sensitive_comparison_doc"; then
    fail "$sensitive_comparison_doc does not record current sensitive example line count: $sensitive_example_lines"
  fi
  if ! grep -Eq "\\| 실제 파일 라인 수[[:space:]]*\\|[[:space:]]*${sensitive_actual_lines}[[:space:]]*\\|" "$sensitive_comparison_doc"; then
    fail "$sensitive_comparison_doc does not record current sensitive local line count: $sensitive_actual_lines"
  fi
  if ! grep -Eq "\\| 총 secret ID 수 \\(example\\)[[:space:]]*\\|[[:space:]]*$sensitive_example_ids unique IDs[[:space:]]*\\|" "$sensitive_comparison_doc"; then
    fail "$sensitive_comparison_doc does not record current sensitive example unique ID count: $sensitive_example_ids"
  fi
fi

section "Operations target comments"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
allowed_prefixes = (
    "docs/05.operations/guides/",
    "docs/05.operations/policies/",
    "docs/05.operations/runbooks/",
    "docs/05.operations/incidents/",
    "docs/05.operations/{guides,policies,runbooks}/",
)
pattern = re.compile(r"<!--\s*Target:\s*(docs/05\.operations/[^ >]+)\s*-->")

for path in sorted(pathlib.Path("docs").rglob("*.md")):
    if "graphify-out" in path.parts:
        continue
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = pattern.search(line)
        if not match:
            continue
        target = match.group(1)
        if not target.startswith(allowed_prefixes):
            failures.append(f"{path}:{line_no}: operations target must use guides/policies/runbooks/incidents: {target}")
        if path.parts[:2] == ("docs", "05.operations") and target != path.as_posix():
            failures.append(f"{path}:{line_no}: operations target must match file path: {target}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Operations purpose profile contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

required = {
    "guides": ["## Usage", "## Common Checks", "## Runbook Handoff"],
    "policies": ["## Policy Scope", "## Controls", "## Verification", "## Review Cadence"],
    "runbooks": ["When to Use", "Procedure", "Evidence", "Escalation"],
}
forbidden = {
    "guides": ["## Policy Scope", "## Controls", "## Exceptions", "## Review Cadence", "### When to Use", "#### Procedure"],
    "policies": ["## Usage", "## Runbook Handoff", "### When to Use", "#### Procedure"],
    "runbooks": ["## Usage", "## Policy Scope", "## Controls", "## Exceptions", "## Review Cadence"],
}

failures: list[str] = []
for bucket in ["guides", "policies", "runbooks"]:
    root = pathlib.Path("docs/05.operations") / bucket
    for path in sorted(root.glob("*.md")):
        if path.name != "README.md":
            failures.append(
                f"{path}: operations bucket root must contain README.md only; move leaf docs into a purpose folder"
            )
    for path in sorted(p for p in root.rglob("*") if p.is_dir()):
        direct_leaf_docs = sorted(
            child for child in path.glob("*.md") if child.name != "README.md"
        )
        direct_dirs = sorted(child for child in path.iterdir() if child.is_dir())
        if direct_leaf_docs and direct_dirs:
            failures.append(
                f"{path}: operations folder mixes direct leaf docs and child folders; move leaf docs into a purpose folder"
            )
    for path in sorted(root.rglob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(errors="ignore")
        rel = path.relative_to(root)
        expected_tier = rel.parts[0] if len(rel.parts) > 1 else None
        if expected_tier:
            for match in re.finditer(r"<!--\s*\[ID:([^\]]+)\]\s*-->", text):
                actual_tier = match.group(1).split(":", 1)[0]
                if actual_tier != expected_tier:
                    failures.append(
                        f"{path}: operations ID tier {actual_tier!r} does not match path tier {expected_tier!r}"
                    )
        if bucket == "guides":
            usage_type_count = sum(1 for line in text.splitlines() if line.strip() == "### Usage Type")
            if usage_type_count > 1:
                failures.append(
                    f"{path}: guide document must not contain duplicate ### Usage Type headings; found {usage_type_count}"
                )
        if bucket == "policies":
            policy_scope_count = sum(1 for line in text.splitlines() if line.strip() == "## Policy Scope")
            if policy_scope_count != 1:
                failures.append(
                    f"{path}: policy document must contain exactly one ## Policy Scope heading; found {policy_scope_count}"
                )
        for literal in required[bucket]:
            if literal not in text:
                failures.append(f"{path}: missing {bucket} profile heading: {literal}")
        for literal in forbidden[bucket]:
            if literal in text:
                failures.append(f"{path}: {bucket} document contains cross-profile heading: {literal}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Operations postmortem routing contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


failures: list[str] = []
incidents_root = pathlib.Path("docs/05.operations/incidents")
year_re = re.compile(r"^20[0-9]{2}$")
packet_re = re.compile(r"^INC-[0-9]{3}-[a-z0-9][a-z0-9-]*$")

if not incidents_root.is_dir():
    failures.append(f"missing incidents root: {incidents_root}")

if incidents_root.exists():
    for child in sorted(incidents_root.iterdir()):
        if child.name == "README.md":
            continue
        if not child.is_dir() or not year_re.match(child.name):
            failures.append(f"{child}: incidents root may contain only README.md and YYYY folders")
            continue
        for packet in sorted(child.iterdir()):
            if not packet.is_dir() or not packet_re.match(packet.name):
                failures.append(f"{packet}: incident year folders may contain only INC-###-<title> packet folders")
                continue
            expected_incident = packet / f"{packet.name}.md"
            expected_postmortem = packet / "postmortem.md"
            markdown_files = sorted(path for path in packet.glob("*.md"))
            allowed_files = {expected_incident, expected_postmortem}
            for path in markdown_files:
                if path not in allowed_files:
                    failures.append(
                        f"{path}: incident packet markdown files must be {expected_incident.name} or postmortem.md"
                    )
            if markdown_files and not expected_incident.is_file():
                failures.append(f"{packet}: incident packet is missing {expected_incident.name}")
            if expected_postmortem.is_file() and not expected_incident.is_file():
                failures.append(f"{expected_postmortem}: postmortem requires paired incident file {expected_incident.name}")
    for stale in sorted(incidents_root.rglob("*postmortem*.md")):
        if stale.name != "postmortem.md":
            failures.append(f"{stale}: postmortem file must be named postmortem.md inside the incident packet")

literal_requirements = {
    pathlib.Path("docs/05.operations/incidents/README.md"): [
        "YYYY/INC-###-incident-title/",
        "postmortem.md",
    ],
    pathlib.Path("docs/99.templates/templates/operations/incident.template.md"): [
        "docs/05.operations/incidents/YYYY/INC-###-<incident-title>/INC-###-<incident-title>.md",
        "./postmortem.md",
    ],
    pathlib.Path("docs/99.templates/templates/operations/postmortem.template.md"): [
        "docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md",
        "./INC-###-incident-title.md",
    ],
    pathlib.Path("docs/00.agent-governance/rules/documentation-protocol.md"): [
        "docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md",
    ],
    pathlib.Path(".claude/skills/ops-runbook-agent/skill.md"): [
        "incidents/YYYY/INC-###-<incident-title>/",
        "Filename: `postmortem.md`",
    ],
    pathlib.Path(".claude/skills/incident-response/skill.md"): [
        "docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md",
    ],
}
for path, literals in literal_requirements.items():
    if not path.is_file():
        failures.append(f"missing file for postmortem routing contract: {path}")
        continue
    text = path.read_text(errors="ignore")
    for literal in literals:
        if literal not in text:
            failures.append(f"{path}: missing postmortem routing literal: {literal}")

for path in [
    pathlib.Path("docs/99.templates/templates/operations/incident.template.md"),
    pathlib.Path("docs/99.templates/templates/operations/postmortem.template.md"),
    pathlib.Path(".claude/skills/ops-runbook-agent/skill.md"),
    pathlib.Path(".claude/skills/incident-response/skill.md"),
]:
    if not path.is_file():
        continue
    text = path.read_text(errors="ignore")
    for forbidden in [
        "docs/05.operations/incidents/postmortems/",
        "PM-<INC-ID>-postmortem.md",
        "place both files under `incidents/YYYY/`",
        "YYYY-MM-DD-<incident-title>-postmortem.md",
    ]:
        if forbidden in text:
            failures.append(f"{path}: stale postmortem routing literal remains: {forbidden}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "GitHub Actions YAML and duplicate workflow steps"
if ! python3 - <<'PY'; then
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

    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if not re.match(r"^-\s+", stripped):
            continue
        if re.match(r"^-\s+\*[A-Za-z0-9_-]+\s*$", stripped):
            continue

        indent = len(line) - len(stripped)
        block = [line]
        for next_line in lines[index + 1 :]:
            next_stripped = next_line.lstrip()
            next_indent = len(next_line) - len(next_stripped)
            if next_stripped and next_indent <= indent and re.match(r"^-\s+", next_stripped):
                break
            if next_stripped and next_indent < indent:
                break
            block.append(next_line)

        block_text = "\n".join(block)
        has_uses = bool(
            re.search(r"(?m)^\s*uses:\s*", block_text)
            or re.search(r"(?m)^\s*-\s+(?:&[A-Za-z0-9_-]+\s+)?uses:\s*", block_text)
        )
        has_name = bool(
            re.search(r"(?m)^\s*name:\s*\S", block_text)
            or re.search(r"(?m)^\s*-\s+(?:&[A-Za-z0-9_-]+\s+)?name:\s*\S", block_text)
        )
        if has_uses and not has_name:
            print(f"FAIL: unnamed action step in {path}:{index + 1}", file=sys.stderr)
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
  failures=$((failures + 1))
fi

section "GitHub workflow security contracts"
if ! python3 - <<'PY'; then
from __future__ import annotations

import json
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

    if top_permissions is None:
        failures.append(f"{path}: workflow is missing top-level permissions")
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

ci_quality = pathlib.Path(".github/workflows/ci-quality.yml")
# COUPLING CONSTRAINT: required_jobs must stay in sync with:
#   (1) job IDs in .github/workflows/ci-quality.yml
#   (2) Required Status Checks in .github/rulesets/main-protection.md
#   (3) CI/CD Job Taxonomy in docs/00.agent-governance/rules/github-governance.md
# When adding a new CI job: update all three locations simultaneously.
# GitHub-native-only jobs (greetings, stale, pr-labeler, generate-changelog)
# must NOT be added here — they are not script-backed QA gates.
required_jobs = {
    "docs-traceability",
    "docs-implementation-alignment",
    "repo-contracts",
    "git-flow-contract",
    "compose-validation",
    "compose-all-profiles-validation",
    "infrastructure-hardening",
    "template-security-baseline",
    "quickwin-baseline",
    "pre-commit",
    "frontend-quality",
    "zizmor",
    "storybook-coverage",
}
ci_jobs: set[str] = set()
if ci_quality.is_file():
    data = yaml.safe_load(ci_quality.read_text()) or {}
    ci_jobs = set((data.get("jobs") or {}).keys())
    missing_jobs = sorted(required_jobs - ci_jobs)
    for job_id in missing_jobs:
        failures.append(f"{ci_quality}: missing required QA/CI job: {job_id}")
    unexpected_jobs = sorted(ci_jobs - required_jobs)
    for job_id in unexpected_jobs:
        failures.append(f"{ci_quality}: unexpected QA/CI job outside the ruleset contract: {job_id}")
else:
    failures.append("missing required workflow: .github/workflows/ci-quality.yml")

ruleset = pathlib.Path(".github/rulesets/main-protection.md")
if ruleset.is_file():
    text = ruleset.read_text()
    for literal in [
        "local GitHub settings proposal only",
        "does not apply remote repository settings by",
        "explicit owner approval",
        "audited `gh api` command",
    ]:
        if literal not in text:
            failures.append(f"{ruleset}: missing remote enforcement boundary literal: {literal}")

    match = re.search(r"(?ms)^## Required Status Checks\s*(.*?)(?:\n## |\Z)", text)
    if not match:
        failures.append(f"{ruleset}: missing Required Status Checks section")
    else:
        listed_checks = set(re.findall(r"(?m)^-\s+`([^`]+)`\s*$", match.group(1)))
        expected_checks = ci_jobs or required_jobs
        missing_checks = sorted(expected_checks - listed_checks)
        extra_checks = sorted(listed_checks - expected_checks)
        for check in missing_checks:
            failures.append(f"{ruleset}: missing required status check from CI Quality Gates: {check}")
        for check in extra_checks:
            failures.append(f"{ruleset}: status check is not a CI Quality Gates job: {check}")
else:
    failures.append("missing local branch protection proposal: .github/rulesets/main-protection.md")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "GitHub governance surface"
if [[ -f ".github/copilot-instructions.md" || -d ".github/instructions" ]]; then
  fail "GitHub-native instruction files are not adopted in this repository"
fi

if ! python3 - <<'PY'; then
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
  failures=$((failures + 1))
fi

section "PR template strategy fields"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []
template = pathlib.Path(".github/PULL_REQUEST_TEMPLATE.md")
required_literals = [
    "Draft/WIP",
    "remaining work",
    "Coverage target",
    "Coverage rationale",
    "Fix/Refactor evidence",
    "Commits are small, logical, and reviewable",
]

if not template.is_file():
    failures.append("missing PR template: .github/PULL_REQUEST_TEMPLATE.md")
else:
    text = template.read_text(errors="ignore")
    for literal in required_literals:
        if literal not in text:
            failures.append(f"{template}: missing PR strategy field: {literal}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Storybook coverage contract"
if ! bash scripts/validation/check-storybook-contract.sh; then
  failures=$((failures + 1))
fi

section "Root shim and hook parity drift"
if ! python3 - <<'PY'; then
from __future__ import annotations

import json
import pathlib
import re
import sys

failures: list[str] = []

claude_md = pathlib.Path("CLAUDE.md")
if claude_md.is_file():
    text = claude_md.read_text(errors="ignore")
    if re.search(r"(?m)^##\s+graphify\s*$", text):
        failures.append("CLAUDE.md: duplicate root-local Graphify policy block remains")
else:
    failures.append("missing root CLAUDE.md")

def matchers(path: pathlib.Path, event: str) -> str:
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        failures.append(f"{path}: JSON parse failed: {exc}")
        return ""
    hooks = data.get("hooks", {}) if isinstance(data, dict) else {}
    entries = hooks.get(event, []) if isinstance(hooks, dict) else []
    values: list[str] = []
    if isinstance(entries, list):
        for entry in entries:
            if isinstance(entry, dict):
                values.append(str(entry.get("matcher", "")))
    return "|".join(values)

claude_post = matchers(pathlib.Path(".claude/settings.json"), "PostToolUse")
codex_post = matchers(pathlib.Path(".codex/hooks.json"), "PostToolUse")
for literal in ["Write", "Edit", "MultiEdit", "apply_patch", "ApplyPatch"]:
    if literal not in claude_post:
        failures.append(f".claude/settings.json: PostToolUse matcher must cover {literal!r}")
    if literal not in codex_post:
        failures.append(f".codex/hooks.json: PostToolUse matcher must cover {literal!r}")

for path in [
    pathlib.Path("docs/00.agent-governance/providers/claude.md"),
    pathlib.Path("docs/00.agent-governance/providers/codex.md"),
    pathlib.Path(".codex/README.md"),
]:
    text = path.read_text(errors="ignore") if path.is_file() else ""
    for literal in ["Hook Parity", "apply_patch", "ApplyPatch"]:
        if literal not in text:
            failures.append(f"{path}: missing hook parity literal: {literal}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Hookify critical-rule metadata"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

try:
    import yaml
except Exception as exc:
    print(f"FAIL: PyYAML is required for Hookify metadata parsing: {exc}", file=sys.stderr)
    sys.exit(1)

failures: list[str] = []
hookify_files = sorted(pathlib.Path(".claude").glob("hookify*.local.md"))
allowed_events = {"bash", "file", "stop"}
allowed_actions = {"block", "warn"}

for path in hookify_files:
    text = path.read_text(errors="ignore")
    match = re.match(r"^---\n(.*?)\n---(?:\n|\Z)", text, re.S)
    if not match:
        failures.append(f"{path}: missing YAML front matter")
        continue

    try:
        metadata = yaml.safe_load(match.group(1))
    except Exception as exc:
        failures.append(f"{path}: YAML front matter parse failed: {exc}")
        continue

    if not isinstance(metadata, dict):
        failures.append(f"{path}: YAML front matter must be a mapping")
        continue

    expected_name = path.name.removeprefix("hookify.").removesuffix(".local.md")
    name = metadata.get("name")
    enabled = metadata.get("enabled")
    event = metadata.get("event")
    action = metadata.get("action")
    pattern = metadata.get("pattern")
    conditions = metadata.get("conditions")

    if name != expected_name:
        failures.append(f"{path}: name must match filename stem {expected_name!r}")
    if enabled is not True:
        failures.append(f"{path}: enabled must be true")
    if event not in allowed_events:
        failures.append(f"{path}: event must be one of {sorted(allowed_events)}")
    if action not in allowed_actions:
        failures.append(f"{path}: action must be one of {sorted(allowed_actions)}")
    elif isinstance(name, str):
        if name.startswith("block-") and action != "block":
            failures.append(f"{path}: block rule must use action: block")
        if name.startswith("require-") and action != "block":
            failures.append(f"{path}: require rule must use action: block")
        if name.startswith("warn-") and action != "warn":
            failures.append(f"{path}: warn rule must use action: warn")

    if event in {"bash", "stop"}:
        if not isinstance(pattern, str) or not pattern.strip():
            failures.append(f"{path}: {event} rule must define a non-empty pattern")
        if conditions is not None:
            failures.append(f"{path}: {event} rule must use pattern, not conditions")
    elif event == "file":
        if not isinstance(conditions, list) or not conditions:
            failures.append(f"{path}: file rule must define non-empty conditions")
            continue
        if pattern is not None:
            failures.append(f"{path}: file rule must use conditions, not top-level pattern")
        for index, condition in enumerate(conditions, start=1):
            if not isinstance(condition, dict):
                failures.append(f"{path}: condition #{index} must be a mapping")
                continue
            field = condition.get("field")
            operator = condition.get("operator")
            condition_pattern = condition.get("pattern")
            if not isinstance(field, str) or not field.strip():
                failures.append(f"{path}: condition #{index} missing field")
            if operator != "regex_match":
                failures.append(f"{path}: condition #{index} operator must be regex_match")
            if not isinstance(condition_pattern, str) or not condition_pattern.strip():
                failures.append(f"{path}: condition #{index} missing pattern")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Runtime agent/function catalog"
if ! python3 - <<'PY'; then
from __future__ import annotations

import json
import pathlib
import re
import sys

failures: list[str] = []

def read(path: pathlib.Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except Exception:
        return ""

def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text, re.M)
    return match.group(1).strip() if match else None

def toml_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}\s*=\s*\"([^\"]*)\"\s*$", text, re.M)
    return match.group(1).strip() if match else None

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
    agent_path = pathlib.Path(f".claude/agents/{agent}.md")
    text = read(agent_path)
    protocol_path = f".claude/agents/{agent}.md"
    model = frontmatter_value(text, "model")
    layer = frontmatter_value(text, "layer")
    expected_model = "opus" if agent == "workflow-supervisor" else "sonnet"
    expected_scope = f"@import docs/00.agent-governance/scopes/{layer}.md" if layer else None

    if protocol_path not in protocol:
        failures.append(f"subagent protocol missing runtime agent: {protocol_path}")
    if model != expected_model:
        failures.append(f"{agent_path}: expected model {expected_model!r}, found {model!r}")
    if not layer:
        failures.append(f"{agent_path}: missing layer front matter")
    elif expected_scope not in text:
        failures.append(f"{agent_path}: missing exact scope import {expected_scope!r}")

# --- Cross-provider parity (Stage 00 Canonical Adapter Model: providers/agents-md.md section 5) ---
codex_agents = sorted(p.stem for p in pathlib.Path(".codex/agents").glob("*.toml"))
codex_functions = sorted(p.parent.name for p in pathlib.Path(".codex/skills").glob("*/skill.md"))
gemini_agents = sorted(p.stem for p in pathlib.Path(".agents/agents").glob("*.md"))
gemini_functions = sorted(p.parent.name for p in pathlib.Path(".agents/skills").glob("*/skill.md"))

# 1. Name-set parity across all three runtimes and governance.
if codex_agents != governance_agents:
    failures.append(f"codex agent catalog mismatch: .codex={codex_agents} governance={governance_agents}")
if codex_functions != governance_functions:
    failures.append(f"codex function catalog mismatch: .codex={codex_functions} governance={governance_functions}")
if gemini_agents != governance_agents:
    failures.append(f"gemini agent catalog mismatch: .agents={gemini_agents} governance={governance_agents}")
if gemini_functions != governance_functions:
    failures.append(f"gemini function catalog mismatch: .agents={gemini_functions} governance={governance_functions}")

# 2. Codex agent TOML adapter policy and skill adapter parity.
for agent in runtime_agents:
    path = pathlib.Path(f".codex/agents/{agent}.toml")
    text = read(path)
    expected_model = "gpt-5.5" if agent == "workflow-supervisor" else "gpt-5.4-mini"
    expected_effort = "xhigh" if agent == "workflow-supervisor" else "medium"
    expected_catalog = f"docs/00.agent-governance/agents/agents/{agent}.md"

    if toml_value(text, "name") != agent:
        failures.append(f"{path}: expected name {agent!r}, found {toml_value(text, 'name')!r}")
    if toml_value(text, "model") != expected_model:
        failures.append(f"{path}: expected model {expected_model!r}, found {toml_value(text, 'model')!r}")
    if toml_value(text, "model_reasoning_effort") != expected_effort:
        failures.append(f"{path}: expected model_reasoning_effort {expected_effort!r}, found {toml_value(text, 'model_reasoning_effort')!r}")
    if toml_value(text, "source_catalog") != expected_catalog:
        failures.append(f"{path}: expected source_catalog {expected_catalog!r}")

codex_markdown_agents = sorted(pathlib.Path(".codex/agents").glob("*.md"))
if codex_markdown_agents:
    failures.append(
        ".codex/agents/*.md compatibility prompts are retired; remove: "
        + ", ".join(str(path) for path in codex_markdown_agents)
    )

for fn in runtime_functions:
    if read(pathlib.Path(f".claude/skills/{fn}/skill.md")) != read(pathlib.Path(f".codex/skills/{fn}/skill.md")):
        failures.append(f".codex/skills/{fn}/skill.md: content drift from .claude/skills/{fn}/skill.md adapter")

# 3. Gemini pointer parity + model policy (reference index, never a full copy).
for agent in gemini_agents:
    path = pathlib.Path(f".agents/agents/{agent}.md")
    text = read(path)
    if f"@docs/00.agent-governance/agents/agents/{agent}.md" not in text:
        failures.append(f"{path}: missing reference-index pointer to governance agent")
    if "Gemini reference index" not in text:
        failures.append(f"{path}: missing Gemini reference-index marker")
    if len(text.splitlines()) > 15:
        failures.append(f"{path}: too long ({len(text.splitlines())} lines); Gemini surface must be a pointer, not a full copy")
    model = frontmatter_value(text, "model")
    expected = "gemini-3.1-pro" if agent == "workflow-supervisor" else "gemini-3.5-flash"
    if model != expected:
        failures.append(f"{path}: expected model {expected!r}, found {model!r}")
for fn in gemini_functions:
    path = pathlib.Path(f".agents/skills/{fn}/skill.md")
    text = read(path)
    if f"@docs/00.agent-governance/agents/functions/{fn}.md" not in text:
        failures.append(f"{path}: missing reference-index pointer to governance function")
    if "Gemini reference index" not in text:
        failures.append(f"{path}: missing Gemini reference-index marker")
    if len(text.splitlines()) > 15:
        failures.append(f"{path}: too long ({len(text.splitlines())} lines); Gemini surface must be a pointer, not a full copy")

codex_readme = pathlib.Path(".codex/README.md")
codex_provider = pathlib.Path("docs/00.agent-governance/providers/codex.md")
for path in [codex_readme, codex_provider]:
    text = read(path)
    if not text:
        failures.append(f"missing Codex runtime/provider document: {path}")
        continue
    for required in [
        "AGENTS.md",
        ".codex/hooks.json",
        "scripts/hooks/agent-event-hook.sh",
        "docs/00.agent-governance/agents/",
        ".claude",
    ]:
        if required not in text:
            failures.append(f"{path}: missing Codex runtime boundary reference: {required}")

event_hook = pathlib.Path("scripts/hooks/agent-event-hook.sh")
if not event_hook.is_file():
    failures.append("missing provider-neutral agent event hook implementation: scripts/hooks/agent-event-hook.sh")
else:
    event_hook_text = read(event_hook)
    for literal in [
        "SessionStart",
        "PreToolUse",
        "PostToolUse",
        "SessionEnd",
        "Stop",
        "PreCompact",
        "scripts/hooks/post-tool-validate.sh",
        "graphify-out",
    ]:
        if literal not in event_hook_text:
            failures.append(f"{event_hook}: missing event hook literal: {literal}")

for wrapper, event in {
    pathlib.Path(".claude/hooks/session-start.sh"): "SessionStart",
    pathlib.Path(".claude/hooks/docker-compose-pre.sh"): "PreToolUse",
    pathlib.Path(".claude/hooks/post-tool-validate.sh"): "PostToolUse",
    pathlib.Path(".claude/hooks/session-end.sh"): "SessionEnd",
    pathlib.Path(".claude/hooks/stop.sh"): "Stop",
    pathlib.Path(".claude/hooks/pre-compact.sh"): "PreCompact",
}.items():
    text = read(wrapper)
    if not text:
        failures.append(f"missing Claude hook wrapper: {wrapper}")
        continue
    if "scripts/hooks/agent-event-hook.sh" not in text or event not in text:
        failures.append(f"{wrapper}: must delegate {event} to scripts/hooks/agent-event-hook.sh")

hook_configs = {
    pathlib.Path(".codex/hooks.json"): "scripts/hooks/agent-event-hook.sh",
    pathlib.Path(".claude/settings.json"): ".claude/hooks/",
}
for path, required_command_literal in hook_configs.items():
    text = read(path)
    if not text:
        failures.append(f"missing hook config: {path}")
        continue
    try:
        data = json.loads(text)
    except Exception as exc:
        failures.append(f"{path}: JSON parse failed for hook contract: {exc}")
        continue
    hooks = data.get("hooks", {}) if isinstance(data, dict) else {}
    for event in ["SessionStart", "PreToolUse", "PostToolUse", "SessionEnd", "Stop", "PreCompact"]:
        if event not in hooks:
            failures.append(f"{path}: missing hook event: {event}")
    if required_command_literal not in text:
        failures.append(f"{path}: missing hook command reference: {required_command_literal}")
    if path == pathlib.Path(".codex/hooks.json"):
        pre_tool_entries = hooks.get("PreToolUse") if isinstance(hooks, dict) else None
        pre_tool_matchers = []
        if isinstance(pre_tool_entries, list):
            pre_tool_matchers = [
                entry.get("matcher", "")
                for entry in pre_tool_entries
                if isinstance(entry, dict)
            ]
        matcher_text = "|".join(pre_tool_matchers)
        for matcher_literal in ["Bash", "Read", "Edit", "Write", "apply_patch"]:
            if matcher_literal not in matcher_text:
                failures.append(f"{path}: PreToolUse matcher must cover {matcher_literal!r}")
    elif path == pathlib.Path(".claude/settings.json"):
        if "[ -f graphify-out/graph.json ]" in text:
            failures.append(f"{path}: Graphify advisory context must route through scripts/hooks/agent-event-hook.sh, not an inline command")
        pre_tool_entries = hooks.get("PreToolUse") if isinstance(hooks, dict) else None
        pre_tool_matchers = []
        pre_tool_commands = []
        if isinstance(pre_tool_entries, list):
            for entry in pre_tool_entries:
                if not isinstance(entry, dict):
                    continue
                pre_tool_matchers.append(entry.get("matcher", ""))
                for hook in entry.get("hooks", []):
                    if isinstance(hook, dict):
                        pre_tool_commands.append(hook.get("command", ""))
        matcher_text = "|".join(pre_tool_matchers)
        command_text = "\n".join(pre_tool_commands)
        for matcher_literal in ["Bash", "Read", "Glob", "Grep", "LS", "Edit", "Write", "MultiEdit", "apply_patch", "ApplyPatch"]:
            if matcher_literal not in matcher_text:
                failures.append(f"{path}: PreToolUse matcher must cover {matcher_literal!r}")
        if ".claude/hooks/docker-compose-pre.sh" not in command_text:
            failures.append(f"{path}: PreToolUse must call .claude/hooks/docker-compose-pre.sh")

claude_settings = read(pathlib.Path(".claude/settings.json"))
if '"Bash(rg:*)"' not in claude_settings:
    failures.append(".claude/settings.json: missing read-only discovery permission Bash(rg:*)")

agents_md = read(pathlib.Path("AGENTS.md"))
if "graphify update ." not in agents_md:
    failures.append("AGENTS.md: missing graphify update command in Graphify contract")
graphify_contract = agents_md.lower()
if "unavailable" not in graphify_contract or "skipped" not in graphify_contract:
    failures.append("AGENTS.md: missing graphify unavailable/skipped fallback in Graphify contract")

stale_patterns = [
    re.compile(r"H100|Harness-100|harness-100|h100_pattern|examples/harness-100"),
    re.compile(r"AGENTS\.md §3 Agent Catalog|AGENTS\.md §4 Orchestration"),
]
scan_roots = [
    pathlib.Path("AGENTS.md"),
    pathlib.Path("CLAUDE.md"),
    pathlib.Path("GEMINI.md"),
    pathlib.Path(".agents"),
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
  failures=$((failures + 1))
fi

section ".agents compatibility surface"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []
agents_root = pathlib.Path(".agents")
claude_skills_root = pathlib.Path(".claude/skills")

if agents_root.exists():
    readme = agents_root / "README.md"
    if not readme.is_file():
        failures.append(".agents/README.md: missing compatibility surface contract")
    else:
        text = readme.read_text(errors="ignore")
        for literal in [
            "compatibility surface",
            "not the source of truth",
            ".claude/agents/",
            ".claude/skills/",
            "docs/00.agent-governance/",
        ]:
            if literal not in text:
                failures.append(f"{readme}: missing compatibility literal: {literal}")

    graphify_rule = agents_root / "rules" / "graphify.md"
    if graphify_rule.is_file():
        text = graphify_rule.read_text(errors="ignore")
        for literal in [
            "report-graphify-health.sh",
            "advisory",
            "corroborate",
            "tracked source files",
            "docs/00.agent-governance/",
        ]:
            if literal not in text:
                failures.append(f"{graphify_rule}: missing advisory Graphify literal: {literal}")

    skills_root = agents_root / "skills"
    if skills_root.exists():
        known_skills = {
            path.parent.name
            for path in claude_skills_root.glob("*/skill.md")
        }
        for skill_file in sorted(skills_root.glob("*/skill.md")):
            skill_name = skill_file.parent.name
            if skill_name not in known_skills:
                failures.append(f"{skill_file}: unknown compatibility skill not present in .claude/skills")
            text = skill_file.read_text(errors="ignore")
            if ".Codex/" in text or ".Codex" in text:
                failures.append(f"{skill_file}: stale .Codex runtime path reference")
            if ".codex/agents" in text or ".codex/skills" in text:
                failures.append(f"{skill_file}: .codex must not be treated as an agent/function catalog")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Provider workspace artifact path parity"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
scan_roots = [
    pathlib.Path(".agents"),
    pathlib.Path(".claude"),
    pathlib.Path(".codex"),
]
scan_files: set[pathlib.Path] = set()
allowed_suffixes = {".md", ".toml", ".json"}
stale_workspace_path = re.compile(
    r"_workspace/(?!(?:repo-support(?:/|[`'\"),.;:\]\}\s]|$)|README\.md))"
)

for root in scan_roots:
    if not root.exists():
        continue
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in allowed_suffixes:
            scan_files.add(path)

workflow_design = pathlib.Path("docs/03.specs/008-workflow/agent-design.md")
if workflow_design.is_file():
    scan_files.add(workflow_design)

for path in sorted(scan_files):
    text = path.read_text(errors="ignore")
    for line_no, line in enumerate(text.splitlines(), start=1):
        if stale_workspace_path.search(line):
            failures.append(
                f"{path}:{line_no}: provider/workflow artifact paths must use _workspace/repo-support/: {line.strip()}"
            )

required_literals = {
    pathlib.Path(".agents/rules/workspace.md"): "_workspace/repo-support/",
    pathlib.Path(".agents/workflows/documentation.md"): "_workspace/repo-support/",
    pathlib.Path(".claude/agents/code-reviewer.md"): "_workspace/repo-support/",
    pathlib.Path(".claude/skills/code-reviewer/skill.md"): "_workspace/repo-support/",
    pathlib.Path(".codex/skills/code-reviewer/skill.md"): "_workspace/repo-support/",
    workflow_design: "_workspace/repo-support/",
}
for path, literal in required_literals.items():
    if not path.is_file():
        failures.append(f"missing provider path parity file: {path}")
        continue
    text = path.read_text(errors="ignore")
    if literal not in text:
        failures.append(f"{path}: missing provider workspace parity literal: {literal}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "_workspace protected surface"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import subprocess
import sys

failures: list[str] = []

allowed_tracked = {
    "_workspace/README.md",
    "_workspace/repo-support/README.md",
}
required_gitignore = [
    "_workspace/**",
    "!_workspace/",
    "!_workspace/README.md",
    "!_workspace/repo-support/",
    "!_workspace/repo-support/README.md",
]
prohibited_segments = {
    "auth",
    "auth-files",
    "credential",
    "credentials",
    "diagnostic",
    "diagnostics",
    "history",
    "key",
    "keys",
    "local-logs",
    "log",
    "logs",
    "private-key",
    "private-keys",
    "raw-logs",
    "secret",
    "secrets",
    "shell-history",
    "token",
    "tokens",
}


def run_git_ls_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "_workspace"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        failures.append(f"git ls-files _workspace failed: {result.stderr.strip()}")
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


tracked = set(run_git_ls_files())
missing = sorted(allowed_tracked - tracked)
if missing:
    failures.append(f"_workspace missing tracked contract files: {', '.join(missing)}")

unexpected = sorted(tracked - allowed_tracked)
if unexpected:
    failures.append(f"_workspace has unapproved tracked files: {', '.join(unexpected)}")

for tracked_path in sorted(tracked):
    parts = [part.lower() for part in pathlib.PurePosixPath(tracked_path).parts]
    for segment in prohibited_segments:
        if segment in parts:
            failures.append(f"{tracked_path}: prohibited _workspace path segment: {segment}")

gitignore = pathlib.Path(".gitignore")
if not gitignore.is_file():
    failures.append("missing .gitignore for _workspace protection")
else:
    text = gitignore.read_text(errors="ignore")
    for literal in required_gitignore:
        if literal not in text:
            failures.append(f".gitignore missing _workspace protection literal: {literal}")

contracts = {
    pathlib.Path("_workspace/README.md"): [
        "repo-support",
        "Prohibited Surface",
        "diagnostics dumps",
        "shell history",
        "secret values",
    ],
    pathlib.Path("_workspace/repo-support/README.md"): [
        "Allowed Artifacts",
        "Prohibited Artifacts",
        "Promotion Rule",
        "docs/04.execution/tasks/",
        "docs/90.references/",
    ],
}
for path, literals in contracts.items():
    if not path.is_file():
        failures.append(f"missing _workspace contract README: {path}")
        continue
    text = path.read_text(errors="ignore")
    for literal in literals:
        if literal not in text:
            failures.append(f"{path}: missing _workspace contract literal: {literal}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Active script ownership globs"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
active_paths = [
    pathlib.Path(".claude/agents/infra-implementer.md"),
    pathlib.Path("docs/00.agent-governance/scopes/infra.md"),
    pathlib.Path("docs/00.agent-governance/scopes/security.md"),
]
patterns = [
    re.compile(r"scripts/validate-\*\.sh"),
    re.compile(r"scripts/check-\*-baseline\.sh"),
]

for path in active_paths:
    if not path.is_file():
        failures.append(f"missing active script ownership document: {path}")
        continue
    text = path.read_text(errors="ignore")
    for pattern in patterns:
        if pattern.search(text):
            failures.append(f"{path}: stale script ownership glob remains: {pattern.pattern}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Related Documents phased coverage"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
for path in sorted(pathlib.Path("docs/99.templates/templates").rglob("*.template.md")):
    text = path.read_text(errors="ignore")
    if not text.startswith("---\nstatus: draft\n---"):
        failures.append(f"{path}: Markdown template frontmatter must start with status: draft")
    if "Target:" not in text:
        failures.append(f"{path}: template missing Target path guidance")
    if "Target-relative" not in text:
        failures.append(f"{path}: template missing target-relative link guidance")
    if "## Related Documents" not in text:
        failures.append(f"{path}: template missing ## Related Documents")
    in_related_documents = False
    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            in_related_documents = line.strip() == "## Related Documents"
            continue
        if in_related_documents:
            for match in re.finditer(r"`([^`]+\.md(?:#[^`]*)?)`", line):
                failures.append(
                    f"{path}:{line_no}: Related Documents path must use a Markdown link: {match.group(1)}"
                )

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Markdown documentation contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
repo_root = pathlib.Path(".").resolve()
template_root = pathlib.Path("docs/99.templates")
generated_llm_index = pathlib.Path("docs/90.references/llm-wiki/llm-wiki-index.md")

markdown_link = re.compile(r"(?<!!)(?<!\\)\[([^\]\n]+)\]\(([^)\n]+)\)")
pseudo_doc_link = re.compile(r"`\[((?:\.{1,2}/|docs/)[^`\]]+?\.md(?:#[^`\]]*)?)\]`")
path_like = re.compile(r"^(?:\.{1,2}/|docs/).+\.md(?:#[^#\s]+)?$")

scoped_label_paths = {
    pathlib.Path(path)
    for path in [
        "docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md",
        "docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md",
        "docs/02.architecture/decisions/0003-vault-as-secrets-manager.md",
        "docs/02.architecture/decisions/0004-postgresql-ha-patroni.md",
        "docs/02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md",
        "docs/02.architecture/decisions/0006-lgtm-stack-selection.md",
        "docs/02.architecture/decisions/0009-tooling-services.md",
        "docs/02.architecture/decisions/0010-communication-services.md",
        "docs/02.architecture/decisions/0011-laboratory-services.md",
        "docs/02.architecture/decisions/0016-open-webui-implementation.md",
        "docs/02.architecture/requirements/0001-gateway-architecture.md",
        "docs/02.architecture/requirements/0002-auth-architecture.md",
        "docs/02.architecture/requirements/0003-security-architecture.md",
        "docs/02.architecture/requirements/0004-data-architecture.md",
        "docs/02.architecture/requirements/0005-messaging-architecture.md",
        "docs/02.architecture/requirements/0006-observability-architecture.md",
        "docs/02.architecture/requirements/0011-laboratory-architecture.md",
        "docs/02.architecture/requirements/0012-data-analytics-architecture.md",
        "docs/02.architecture/requirements/0013-open-webui-architecture.md",
        "docs/04.execution/plans/2026-03-26-01-gateway-standardization.md",
        "docs/04.execution/plans/2026-03-26-02-auth-standardization.md",
        "docs/04.execution/plans/2026-03-26-03-security-standardization.md",
        "docs/04.execution/plans/2026-03-26-04-data-standardization.md",
        "docs/04.execution/plans/2026-03-26-05-messaging-standardization.md",
        "docs/04.execution/plans/2026-03-26-06-observability-standardization.md",
        "docs/04.execution/plans/2026-03-26-07-workflow-standardization.md",
        "docs/04.execution/plans/2026-03-26-08-ai-standardization.md",
        "docs/04.execution/plans/2026-03-26-09-tooling-standardization.md",
        "docs/04.execution/plans/2026-03-26-10-communication-standardization.md",
        "docs/04.execution/plans/2026-03-26-11-laboratory-standardization.md",
        "docs/04.execution/plans/2026-03-27-08-ai-open-webui-plan.md",
        "docs/04.execution/plans/2026-03-29-k8s-migration-strategy.md",
        "docs/04.execution/plans/2026-04-01-standardize-infra-net.md",
        "docs/04.execution/tasks/2026-03-26-01-gateway-tasks.md",
        "docs/04.execution/tasks/2026-03-26-02-auth-tasks.md",
        "docs/04.execution/tasks/2026-03-26-03-security-tasks.md",
        "docs/04.execution/tasks/2026-03-26-04-data-tasks.md",
        "docs/04.execution/tasks/2026-03-26-05-messaging-tasks.md",
        "docs/04.execution/tasks/2026-03-26-06-observability-tasks.md",
        "docs/04.execution/tasks/2026-03-26-07-workflow-tasks.md",
        "docs/04.execution/tasks/2026-03-26-08-ai-tasks.md",
        "docs/04.execution/tasks/2026-03-26-09-tooling-tasks.md",
        "docs/04.execution/tasks/2026-03-26-10-communication-tasks.md",
        "docs/04.execution/tasks/2026-03-26-11-laboratory-tasks.md",
        "docs/04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md",
        "docs/04.execution/tasks/2026-04-01-standardize-infra-net.md",
        "docs/05.operations/runbooks/12-infra-net/standardize-infra-net.md",
        "docs/05.operations/runbooks/04-data/analytics/influxdb.md",
        "docs/05.operations/runbooks/04-data/analytics/ksqldb.md",
        "docs/05.operations/runbooks/04-data/analytics/opensearch.md",
        "docs/05.operations/runbooks/04-data/analytics/warehouses.md",
        "docs/05.operations/runbooks/04-data/operational/supabase.md",
        "docs/05.operations/runbooks/04-data/relational.md",
        "docs/05.operations/runbooks/05-messaging/kafka.md",
        "docs/05.operations/runbooks/05-messaging/rabbitmq.md",
        "docs/05.operations/runbooks/08-ai/ollama.md",
        "docs/05.operations/runbooks/08-ai/open-webui.md",
        "docs/05.operations/runbooks/11-laboratory/dashboard.md",
        "docs/05.operations/runbooks/11-laboratory/dozzle.md",
    ]
}

heading_scope = {
    "ARD": {
        pathlib.Path("docs/02.architecture/requirements/0002-auth-architecture.md"),
        pathlib.Path("docs/02.architecture/requirements/0003-security-architecture.md"),
        pathlib.Path("docs/02.architecture/requirements/0012-data-analytics-architecture.md"),
    },
    "ADR": {
        pathlib.Path("docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md"),
        pathlib.Path("docs/02.architecture/decisions/0003-vault-as-secrets-manager.md"),
        pathlib.Path("docs/02.architecture/decisions/0009-tooling-services.md"),
        pathlib.Path("docs/02.architecture/decisions/0010-communication-services.md"),
        pathlib.Path("docs/02.architecture/decisions/0011-laboratory-services.md"),
    },
    "Plan": {
        pathlib.Path("docs/04.execution/plans/2026-03-26-02-auth-standardization.md"),
        pathlib.Path("docs/04.execution/plans/2026-03-26-03-security-standardization.md"),
        pathlib.Path("docs/04.execution/plans/2026-03-26-07-workflow-standardization.md"),
        pathlib.Path("docs/04.execution/plans/2026-03-26-08-ai-standardization.md"),
        pathlib.Path("docs/04.execution/plans/2026-03-26-09-tooling-standardization.md"),
        pathlib.Path("docs/04.execution/plans/2026-03-26-10-communication-standardization.md"),
        pathlib.Path("docs/04.execution/plans/2026-03-26-11-laboratory-standardization.md"),
        pathlib.Path("docs/04.execution/plans/2026-03-29-k8s-migration-strategy.md"),
    },
    "Task": {
        pathlib.Path("docs/04.execution/tasks/2026-03-26-07-workflow-tasks.md"),
        pathlib.Path("docs/04.execution/tasks/2026-03-26-08-ai-tasks.md"),
        pathlib.Path("docs/04.execution/tasks/2026-03-26-09-tooling-tasks.md"),
        pathlib.Path("docs/04.execution/tasks/2026-03-26-10-communication-tasks.md"),
    },
}


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def is_markdown_template(path: pathlib.Path) -> bool:
    return is_relative_to(path, template_root) and path.name.endswith(".template.md")


def iter_unfenced_lines(path: pathlib.Path) -> list[tuple[int, str]]:
    try:
        lines = path.read_text(errors="ignore").splitlines()
    except Exception:
        return []

    result: list[tuple[int, str]] = []
    in_fence = False
    for line_no, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            result.append((line_no, line))
    return result


def validate_fenced_code_blocks(path: pathlib.Path) -> list[str]:
    try:
        lines = path.read_text(errors="ignore").splitlines()
    except Exception:
        return []

    result: list[str] = []
    in_fence = False
    marker = ""
    open_line = 0
    for line_no, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        prefix = "```" if stripped.startswith("```") else "~~~" if stripped.startswith("~~~") else ""
        if not prefix:
            continue
        if not in_fence:
            in_fence = True
            marker = prefix
            open_line = line_no
            continue
        if prefix != marker:
            continue
        suffix = stripped[len(marker) :]
        if suffix.strip():
            result.append(f"{path}:{line_no}: fenced code closing marker must not include an info string")
        in_fence = False
        marker = ""
        open_line = 0

    if in_fence:
        result.append(f"{path}:{open_line}: fenced code block is not closed")
    return result


def inside_inline_code(line: str, index: int) -> bool:
    return line[:index].count("`") % 2 == 1


def link_path(raw_href: str) -> str:
    href = raw_href.strip()
    if href.startswith("<") and ">" in href:
        return href[1 : href.index(">")]
    return href.split()[0]


def target_exists(path: pathlib.Path, raw_href: str) -> bool:
    href = link_path(raw_href)
    if not href or href.startswith("#"):
        return True
    if re.match(r"^[a-z][a-z0-9+.-]*:", href, flags=re.I):
        return href.startswith(("http://", "https://", "mailto:"))
    target_path = pathlib.Path(href.split("#", 1)[0])
    if target_path.is_absolute():
        return False
    target = (path.parent / target_path).resolve()
    try:
        target.relative_to(repo_root)
    except ValueError:
        return False
    return target.exists()


active_markdown_files = [
    pathlib.Path("README.md"),
    *sorted(pathlib.Path("docs").rglob("*.md")),
]
active_markdown_files = [
    path
    for path in active_markdown_files
    if path.is_file()
    and "graphify-out" not in path.parts
    and "volumes" not in path.parts
    and "node_modules" not in path.parts
    and not is_relative_to(path, template_root)
]

for path in active_markdown_files:
    text = path.read_text(errors="ignore")
    for required in ["## Related Documents"]:
        if required not in text:
            failures.append(f"{path}: missing {required}")
    failures.extend(validate_fenced_code_blocks(path))

    for line_no, line in iter_unfenced_lines(path):
        for match in markdown_link.finditer(line):
            if inside_inline_code(line, match.start()):
                continue
            if not target_exists(path, match.group(2)):
                failures.append(f"{path}:{line_no}: broken or disallowed Markdown link: {match.group(2)}")
        for match in pseudo_doc_link.finditer(line):
            failures.append(f"{path}:{line_no}: use a real Markdown link instead of pseudo-link: {match.group(1)}")

        if path in scoped_label_paths and path != generated_llm_index:
            for match in markdown_link.finditer(line):
                if inside_inline_code(line, match.start()):
                    continue
                label = match.group(1).strip()
                href = link_path(match.group(2))
                if path_like.match(label) and path_like.match(href) and label != href:
                    failures.append(f"{path}:{line_no}: path-like link label and href differ: {label} != {href}")

for path in sorted(template_root.rglob("*.template.md")):
    for line_no, line in iter_unfenced_lines(path):
        for match in pseudo_doc_link.finditer(line):
            failures.append(f"{path}:{line_no}: template Related Documents examples must use Markdown links: {match.group(1)}")

heading_contracts = [
    (
        pathlib.Path("docs/02.architecture/requirements"),
        "ARD",
        [
            ("Overview", ("## Overview",)),
            ("Summary", ("## Summary",)),
            ("Boundaries", ("## Boundaries & Non-goals",)),
            ("Quality Attributes", ("## Quality Attributes",)),
            ("System Overview", ("## System Overview & Context",)),
            ("Data Architecture", ("## Data Architecture", "## Data Models")),
            ("Related Documents", ("## Related Documents",)),
        ],
    ),
    (
        pathlib.Path("docs/02.architecture/decisions"),
        "ADR",
        [
            ("Overview", ("## Overview",)),
            ("Context", ("## Context",)),
            ("Decision", ("## Decision",)),
            ("Explicit Non-goals", ("## Explicit Non-goals",)),
            ("Consequences", ("## Consequences", "## Consequence")),
            ("Alternatives", ("## Alternatives", "## Alternatives Considered")),
            ("Related Documents", ("## Related Documents",)),
        ],
    ),
    (
        pathlib.Path("docs/04.execution/plans"),
        "Plan",
        [
            ("Overview", ("## Overview",)),
            ("Context", ("## Context",)),
            ("Goals", ("## Goals & In-Scope",)),
            ("Non-goals", ("## Non-Goals & Out-of-Scope",)),
            ("Work Breakdown", ("## Work Breakdown", "## Work Breakdown (WBS)")),
            ("Verification Plan", ("## Verification Plan",)),
            ("Completion Criteria", ("## Completion Criteria",)),
            ("Related Documents", ("## Related Documents",)),
        ],
    ),
    (
        pathlib.Path("docs/04.execution/tasks"),
        "Task",
        [
            ("Overview", ("## Overview",)),
            ("Inputs", ("## Inputs",)),
            ("Working Rules", ("## Working Rules",)),
            ("Task Table", ("## Task Table",)),
            ("Verification Summary", ("## Verification Summary",)),
            ("Related Documents", ("## Related Documents",)),
        ],
    ),
]
for root, label, headings in heading_contracts:
    for path in sorted(root.glob("*.md")) if root.exists() else []:
        if path.name == "README.md":
            continue
        if path not in heading_scope[label]:
            continue
        text = path.read_text(errors="ignore")
        for group_name, alternatives in headings:
            if not any(heading in text for heading in alternatives):
                expected = " or ".join(alternatives)
                failures.append(f"{path}: missing {label} contract heading group {group_name}: {expected}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Spec document traceability contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
pseudo_link = re.compile(r"`\[((?:\.\.?/|docs/)[^`\]]+?\.md(?:#[^`\]]*)?)\]`")
related_link = re.compile(
    r"\*\*(Guide|Policy|Operation|Operations|Runbook)\*\*:\s*\[[^\]]+\]\(([^)]+)\)"
)
expected_bucket = {
    "Guide": "05.operations/guides/",
    "Policy": "05.operations/policies/",
    "Operation": "05.operations/policies/",
    "Operations": "05.operations/policies/",
    "Runbook": "05.operations/runbooks/",
}

for path in sorted(pathlib.Path("docs/03.specs").rglob("*.md")):
    text = path.read_text(errors="ignore")
    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in pseudo_link.finditer(line):
            failures.append(
                f"{path}:{line_no}: active spec uses pseudo-link instead of Markdown link: {match.group(1)}"
            )

        for match in related_link.finditer(line):
            label = match.group(1)
            href = match.group(2).strip().split()[0]
            if "05.operations/" not in href:
                continue
            required = expected_bucket[label]
            if required not in href:
                failures.append(
                    f"{path}:{line_no}: {label} link must target {required}: {href}"
                )

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Contract template cross-link ownership"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []
for path in sorted(pathlib.Path("docs/99.templates/templates").rglob("*.template.*")):
    if path.suffix == ".md":
        continue
    text = path.read_text(errors="ignore")
    if "Target:" not in text:
        failures.append(f"{path}: contract template missing Target path guidance")
    if "Cross-links:" not in text:
        failures.append(f"{path}: contract template missing parent Markdown cross-link ownership note")
    if "## Related Documents" in text:
        failures.append(f"{path}: non-Markdown contract template must not include Markdown Related Documents section")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Changed stage document template gate"
if ! python3 - <<'PY'; then
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

failures: list[str] = []
repo_root = pathlib.Path(".").resolve()
stage_roots = tuple(
    pathlib.Path(path)
    for path in [
        "docs/01.requirements",
        "docs/02.architecture",
        "docs/03.specs",
        "docs/04.execution",
        "docs/05.operations",
        "docs/90.references",
        "docs/98.archive",
    ]
)
tracked_suffixes = {".md", ".yaml", ".yml", ".graphql", ".proto"}


def run_git(args: list[str]) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def changed_paths() -> set[pathlib.Path]:
    paths: set[str] = set()
    paths.update(run_git(["diff", "--name-only", "--diff-filter=AM"]))
    paths.update(run_git(["diff", "--cached", "--name-only", "--diff-filter=AM"]))
    paths.update(run_git(["ls-files", "--others", "--exclude-standard"]))

    base_refs: list[str] = []
    explicit_base = os.environ.get("TEMPLATE_GATE_BASE")
    github_base = os.environ.get("GITHUB_BASE_REF")
    if explicit_base:
        base_refs.append(explicit_base)
    if github_base:
        base_refs.extend([f"origin/{github_base}", github_base])

    for ref in base_refs:
        merge_base = run_git(["merge-base", "HEAD", ref])
        if not merge_base:
            continue
        paths.update(run_git(["diff", "--name-only", "--diff-filter=AM", f"{merge_base[0]}...HEAD"]))
        break

    return {pathlib.Path(path) for path in paths}


def target_stage_doc(path: pathlib.Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    if path.suffix.lower() not in tracked_suffixes:
        return False
    return any(is_relative_to(path, root) for root in stage_roots)


def classify(path: pathlib.Path) -> str | None:
    if path.suffix.lower() == ".md" and path.name == "README.md":
        return "README"

    if is_relative_to(path, pathlib.Path("docs/01.requirements")) and path.suffix == ".md":
        return "PRD"

    if is_relative_to(path, pathlib.Path("docs/02.architecture/requirements")) and path.suffix == ".md":
        return "ARD"
    if is_relative_to(path, pathlib.Path("docs/02.architecture/decisions")) and path.suffix == ".md":
        return "ADR"

    specs_root = pathlib.Path("docs/03.specs")
    if is_relative_to(path, specs_root):
        rel = path.relative_to(specs_root)
        if path.suffix == ".md" and len(rel.parts) == 2:
            return {
                "spec.md": "Spec",
                "open-webui.md": "Spec",
                "api-spec.md": "API Spec",
                "agent-design.md": "Agent Design",
                "data-model.md": "Data Model",
                "tests.md": "Tests",
            }.get(rel.parts[1])
        if len(rel.parts) == 3 and rel.parts[1] == "contracts":
            filename = rel.parts[2]
            if filename in {"openapi.yaml", "openapi.yml"}:
                return "OpenAPI Contract"
            if filename == "schema.graphql":
                return "GraphQL Contract"
            if filename == "service.proto":
                return "Protobuf Contract"
        return None

    if is_relative_to(path, pathlib.Path("docs/04.execution/plans")) and path.suffix == ".md":
        return "Plan"
    if is_relative_to(path, pathlib.Path("docs/04.execution/tasks")) and path.suffix == ".md":
        return "Task"

    operations_root = pathlib.Path("docs/05.operations")
    if is_relative_to(path, operations_root) and path.suffix == ".md":
        rel = path.relative_to(operations_root)
        if not rel.parts:
            return None
        if rel.parts[0] == "guides":
            return "Operation Guide"
        if rel.parts[0] == "policies":
            return "Operation Policy"
        if rel.parts[0] == "runbooks":
            return "Operation Runbook"
        if rel.parts[0] == "incidents":
            return "Postmortem" if "postmortem" in path.stem else "Incident"
        return None

    if is_relative_to(path, pathlib.Path("docs/90.references")) and path.suffix == ".md":
        return "Reference"
    if is_relative_to(path, pathlib.Path("docs/98.archive")) and path.suffix == ".md":
        return "Archive Tombstone"

    return None


heading_requirements: dict[str, list[tuple[str, tuple[str, ...]]]] = {
    "README": [
        ("Overview", ("## Overview",)),
        ("Audience", ("## Audience",)),
        ("Scope", ("## Scope",)),
        ("Structure", ("## Structure",)),
        ("How to Work", ("## How to Work in This Area",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "PRD": [
        ("Overview", ("## Overview",)),
        ("Vision", ("## Vision",)),
        ("Problem Statement", ("## Problem Statement",)),
        ("Functional Requirements", ("## Functional Requirements",)),
        ("Success Criteria", ("## Success Criteria",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "ARD": [
        ("Overview", ("## Overview",)),
        ("Summary", ("## Summary",)),
        ("Boundaries", ("## Boundaries & Non-goals",)),
        ("Quality Attributes", ("## Quality Attributes",)),
        ("System Overview", ("## System Overview & Context",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "ADR": [
        ("Overview", ("## Overview",)),
        ("Context", ("## Context",)),
        ("Decision", ("## Decision",)),
        ("Explicit Non-goals", ("## Explicit Non-goals",)),
        ("Consequences", ("## Consequences", "## Consequence")),
        ("Alternatives", ("## Alternatives", "## Alternatives Considered")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Spec": [
        ("Overview", ("## Overview",)),
        ("Boundaries", ("## Strategic Boundaries & Non-goals",)),
        ("Related Inputs", ("## Related Inputs",)),
        ("Contracts", ("## Contracts",)),
        ("Core Design", ("## Core Design",)),
        ("Verification", ("## Verification",)),
        ("Success Criteria", ("## Success Criteria & Verification Plan",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "API Spec": [
        ("Overview", ("## Overview",)),
        ("Parent Spec", ("## Parent Spec",)),
        ("Scope", ("## Scope & Non-goals",)),
        ("API Style", ("## API Style",)),
        ("Operations", ("## Endpoint / Operation Catalog",)),
        ("Verification", ("## Verification",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Agent Design": [
        ("Overview", ("## Overview",)),
        ("Parent Documents", ("## Parent Documents",)),
        ("Agent Role", ("## Agent Role",)),
        ("Inputs / Outputs", ("## Inputs / Outputs",)),
        ("Tools", ("## Tools & Permissions",)),
        ("Evaluation", ("## Evaluation Plan",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Data Model": [
        ("Overview", ("## Overview",)),
        ("Parent Documents", ("## Parent Documents",)),
        ("Entities", ("## Entities / Aggregates",)),
        ("Relationships", ("## Relationships",)),
        ("Validation", ("## Validation & Integrity Rules",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Tests": [
        ("Overview", ("## Overview",)),
        ("Parent Documents", ("## Parent Documents",)),
        ("Verification Goals", ("## Verification Goals",)),
        ("Test Matrix", ("## Test Matrix",)),
        ("How to Run", ("## How to Run",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Plan": [
        ("Overview", ("## Overview",)),
        ("Context", ("## Context",)),
        ("Goals", ("## Goals & In-Scope",)),
        ("Work Breakdown", ("## Work Breakdown", "## Work Breakdown (WBS)")),
        ("Verification Plan", ("## Verification Plan",)),
        ("Completion Criteria", ("## Completion Criteria",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Task": [
        ("Overview", ("## Overview",)),
        ("Inputs", ("## Inputs",)),
        ("Working Rules", ("## Working Rules",)),
        ("Task Table", ("## Task Table",)),
        ("Verification Summary", ("## Verification Summary",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Operation Guide": [
        ("Overview", ("## Overview",)),
        ("Usage", ("## Usage", "### Usage")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Operation Policy": [
        ("Overview", ("## Overview",)),
        ("Policy Scope", ("## Policy Scope", "### Policy Scope")),
        ("Controls", ("## Controls", "### Controls")),
        ("Verification", ("## Verification", "### Verification")),
        ("Review Cadence", ("## Review Cadence", "### Review Cadence")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Operation Runbook": [
        ("Overview", ("## Overview",)),
        ("When to Use", ("## When to Use", "### When to Use")),
        ("Procedure", ("## Procedure", "### Procedure", "#### Procedure")),
        ("Evidence", ("## Evidence", "### Evidence", "#### Evidence")),
        ("Rollback or Recovery", ("## Rollback or Recovery", "### Rollback or Recovery", "#### Rollback or Recovery")),
        ("Escalation", ("## Escalation", "### Escalation", "#### Escalation")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Incident": [
        ("Overview", ("## Overview",)),
        ("Incident Metadata", ("## Incident Metadata",)),
        ("Incident Summary", ("## Incident Summary",)),
        ("Impact", ("## Impact",)),
        ("Timeline", ("## Timeline",)),
        ("Evidence", ("## Evidence",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Postmortem": [
        ("Overview", ("## Overview",)),
        ("Incident Summary", ("## Incident Summary",)),
        ("Impact", ("## Impact",)),
        ("Timeline", ("## Timeline",)),
        ("Root Cause", ("## Root Cause Analysis",)),
        ("Action Items", ("## Action Items",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Reference": [
        ("Overview", ("## Overview",)),
        ("Purpose", ("## Purpose",)),
        ("Repository Role", ("## Repository Role",)),
        ("Scope", ("## Scope",)),
        ("Definitions / Facts", ("## Definitions / Facts",)),
        ("Sources", ("## Sources",)),
        ("Maintenance", ("## Maintenance",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Archive Tombstone": [
        ("Overview", ("## Overview",)),
        ("Archive Metadata", ("## Archive Metadata",)),
        ("Current Replacement", ("## Current Replacement",)),
        ("Archive Ledger", ("## Archive Ledger",)),
        ("Related Documents", ("## Related Documents",)),
    ],
}

contract_requirements = {
    "OpenAPI Contract": ("# Target:", "# Cross-links:", "openapi:", "info:", "paths:"),
    "GraphQL Contract": ("# Target:", "# Cross-links:", "schema {", "type Query"),
    "Protobuf Contract": ("// Target:", "// Cross-links:", 'syntax = "proto3";', "service "),
}

operation_forbidden = {
    "Operation Guide": ["## Policy Scope", "## Controls", "## Review Cadence", "### When to Use", "#### Procedure"],
    "Operation Policy": ["## Usage", "## Runbook Handoff", "### When to Use", "#### Procedure"],
    "Operation Runbook": ["## Usage", "## Policy Scope", "## Controls", "## Exceptions", "## Review Cadence"],
}

placeholder_patterns = [
    re.compile(r"YYYY-MM-DD-<[^>\n]+>"),
    re.compile(r"####-<[^>\n]+>"),
    re.compile(r"<(?:feature-id|feature|topic|item|category|system-or-domain|system-or-domain-name|short-title|bucket|domain|subdomain|incident-title)>"),
    re.compile(r"\[(?:Feature|System|State|What|Why|Requirement|Metric|Risk|Role|Need|Source|Owner|Update|Item|How this|Scope)[^\]\n]*\](?!\()"),
]
placeholder_literals = [
    "{Topic Name}",
    "{Guide | Policy | Runbook}",
    "{One-line",
    "{Explain",
    "{Describe",
    "{List",
    "{Owner}",
    "{Review Cadence}",
    "{Update Trigger}",
    "{What this source supports}",
    "{Current",
    "{Last",
    "{Recovery",
    "{Escalation",
    "{Expected",
]


def validate_text(path: pathlib.Path, doc_type: str, text: str) -> None:
    if doc_type in heading_requirements:
        if "Target:" not in text:
            failures.append(f"{path}: changed {doc_type} document missing template Target guidance")
        for group_name, alternatives in heading_requirements[doc_type]:
            if not any(heading in text for heading in alternatives):
                expected = " or ".join(alternatives)
                failures.append(f"{path}: changed {doc_type} document missing template heading {group_name}: {expected}")
        for literal in operation_forbidden.get(doc_type, []):
            if literal in text:
                failures.append(f"{path}: changed {doc_type} document contains wrong operation profile heading: {literal}")

    elif doc_type in contract_requirements:
        for literal in contract_requirements[doc_type]:
            if literal not in text:
                failures.append(f"{path}: changed {doc_type} missing contract template literal: {literal}")

    for pattern in placeholder_patterns:
        match = pattern.search(text)
        if match:
            failures.append(f"{path}: unresolved template placeholder remains: {match.group(0)}")
    for literal in placeholder_literals:
        if literal in text:
            failures.append(f"{path}: unresolved template placeholder remains: {literal}")


def normalized_target_doc(doc_type: str, text: str) -> bool:
    if doc_type in contract_requirements:
        return True
    headings = heading_requirements.get(doc_type, ())
    if not headings:
        return False
    if not all(any(heading in text for heading in alternatives) for _, alternatives in headings):
        return False
    if any(pattern.search(text) for pattern in placeholder_patterns):
        return False
    return not any(literal in text for literal in placeholder_literals)


changed_stage_docs = sorted(path for path in changed_paths() if target_stage_doc(path))
normalized_changed_docs = 0
legacy_changed_docs = 0
print(f"changed_template_docs_total={len(changed_stage_docs)}")

for path in changed_stage_docs:
    doc_type = classify(path)
    if doc_type is None:
        failures.append(f"{path}: unknown target-stage document type; add a docs/99.templates mapping before editing")
        continue
    text = path.read_text(errors="ignore")
    if not normalized_target_doc(doc_type, text):
        legacy_changed_docs += 1
        continue
    normalized_changed_docs += 1
    validate_text(path, doc_type, text)

print(f"normalized_changed_template_docs_total={normalized_changed_docs}")
print(f"legacy_changed_template_docs_skipped={legacy_changed_docs}")

if legacy_changed_docs:
    failures.append(
        f"changed target-stage documents must be normalized; legacy_changed_template_docs_skipped={legacy_changed_docs}"
    )

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Normalized target-stage document template contracts"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
stage_roots = tuple(
    pathlib.Path(path)
    for path in [
        "docs/01.requirements",
        "docs/02.architecture",
        "docs/03.specs",
        "docs/04.execution",
        "docs/05.operations",
        "docs/90.references",
        "docs/98.archive",
    ]
)
tracked_suffixes = {".md", ".yaml", ".yml", ".graphql", ".proto"}


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def target_stage_doc(path: pathlib.Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    if path.suffix.lower() not in tracked_suffixes:
        return False
    return any(is_relative_to(path, root) for root in stage_roots)


def classify(path: pathlib.Path) -> str | None:
    if path.suffix.lower() == ".md" and path.name == "README.md":
        return "Folder Index README"

    if is_relative_to(path, pathlib.Path("docs/01.requirements")) and path.suffix == ".md":
        return "PRD"

    if is_relative_to(path, pathlib.Path("docs/02.architecture/requirements")) and path.suffix == ".md":
        return "ARD"
    if is_relative_to(path, pathlib.Path("docs/02.architecture/decisions")) and path.suffix == ".md":
        return "ADR"

    specs_root = pathlib.Path("docs/03.specs")
    if is_relative_to(path, specs_root):
        rel = path.relative_to(specs_root)
        if path.suffix == ".md" and len(rel.parts) == 2:
            return {
                "spec.md": "Spec",
                "open-webui.md": "Spec",
                "api-spec.md": "API Spec",
                "agent-design.md": "Agent Design",
                "data-model.md": "Data Model",
                "tests.md": "Tests",
            }.get(rel.parts[1])
        if len(rel.parts) == 3 and rel.parts[1] == "contracts":
            filename = rel.parts[2]
            if filename in {"openapi.yaml", "openapi.yml"}:
                return "OpenAPI Contract"
            if filename == "schema.graphql":
                return "GraphQL Contract"
            if filename == "service.proto":
                return "Protobuf Contract"
        return None

    if is_relative_to(path, pathlib.Path("docs/04.execution/plans")) and path.suffix == ".md":
        return "Plan"
    if is_relative_to(path, pathlib.Path("docs/04.execution/tasks")) and path.suffix == ".md":
        return "Task"

    operations_root = pathlib.Path("docs/05.operations")
    if is_relative_to(path, operations_root) and path.suffix == ".md":
        rel = path.relative_to(operations_root)
        if not rel.parts:
            return None
        if rel.parts[0] == "guides":
            return "Operation Guide"
        if rel.parts[0] == "policies":
            return "Operation Policy"
        if rel.parts[0] == "runbooks":
            return "Operation Runbook"
        if rel.parts[0] == "incidents":
            return "Postmortem" if "postmortem" in path.stem else "Incident"
        return None

    if is_relative_to(path, pathlib.Path("docs/90.references")) and path.suffix == ".md":
        return "Reference"
    if is_relative_to(path, pathlib.Path("docs/98.archive")) and path.suffix == ".md":
        return "Archive Tombstone"

    return None


heading_requirements: dict[str, list[tuple[str, tuple[str, ...]]]] = {
    "Folder Index README": [
        ("Overview", ("## Overview", "## Purpose", "## Context and Objective", "## 목적")),
        ("Audience", ("## Audience",)),
        ("Scope", ("## Scope",)),
        ("Structure", ("## Structure", "## Directory Structure", "## 템플릿-폴더 매핑")),
        ("How to Work", ("## How to Work in This Area",)),
        ("Related Documents", ("## Related Documents", "## Related References", "## 관련 문서")),
    ],
    "PRD": [
        ("Overview", ("## Overview",)),
        ("Vision", ("## Vision",)),
        ("Problem Statement", ("## Problem Statement",)),
        ("Functional Requirements", ("## Functional Requirements",)),
        ("Success Criteria", ("## Success Criteria",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "ARD": [
        ("Overview", ("## Overview",)),
        ("Summary", ("## Summary",)),
        ("Boundaries", ("## Boundaries & Non-goals",)),
        ("Quality Attributes", ("## Quality Attributes",)),
        ("System Overview", ("## System Overview & Context",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "ADR": [
        ("Overview", ("## Overview",)),
        ("Context", ("## Context",)),
        ("Decision", ("## Decision",)),
        ("Explicit Non-goals", ("## Explicit Non-goals",)),
        ("Consequences", ("## Consequences", "## Consequence")),
        ("Alternatives", ("## Alternatives", "## Alternatives Considered")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Spec": [
        ("Overview", ("## Overview",)),
        ("Boundaries", ("## Strategic Boundaries & Non-goals",)),
        ("Related Inputs", ("## Related Inputs",)),
        ("Contracts", ("## Contracts",)),
        ("Core Design", ("## Core Design",)),
        ("Verification", ("## Verification",)),
        ("Success Criteria", ("## Success Criteria & Verification Plan",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "API Spec": [
        ("Overview", ("## Overview",)),
        ("Parent Spec", ("## Parent Spec",)),
        ("Scope", ("## Scope & Non-goals",)),
        ("API Style", ("## API Style",)),
        ("Operations", ("## Endpoint / Operation Catalog",)),
        ("Verification", ("## Verification",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Agent Design": [
        ("Overview", ("## Overview",)),
        ("Parent Documents", ("## Parent Documents",)),
        ("Agent Role", ("## Agent Role",)),
        ("Inputs / Outputs", ("## Inputs / Outputs",)),
        ("Tools", ("## Tools & Permissions",)),
        ("Evaluation", ("## Evaluation Plan",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Data Model": [
        ("Overview", ("## Overview",)),
        ("Parent Documents", ("## Parent Documents",)),
        ("Entities", ("## Entities / Aggregates",)),
        ("Relationships", ("## Relationships",)),
        ("Validation", ("## Validation & Integrity Rules",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Tests": [
        ("Overview", ("## Overview",)),
        ("Parent Documents", ("## Parent Documents",)),
        ("Verification Goals", ("## Verification Goals",)),
        ("Test Matrix", ("## Test Matrix",)),
        ("How to Run", ("## How to Run",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Plan": [
        ("Overview", ("## Overview",)),
        ("Context", ("## Context",)),
        ("Goals", ("## Goals & In-Scope",)),
        ("Work Breakdown", ("## Work Breakdown", "## Work Breakdown (WBS)")),
        ("Verification Plan", ("## Verification Plan",)),
        ("Completion Criteria", ("## Completion Criteria",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Task": [
        ("Overview", ("## Overview",)),
        ("Inputs", ("## Inputs",)),
        ("Working Rules", ("## Working Rules",)),
        ("Task Table", ("## Task Table",)),
        ("Verification Summary", ("## Verification Summary",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Operation Guide": [
        ("Overview", ("## Overview",)),
        ("Usage", ("## Usage", "### Usage")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Operation Policy": [
        ("Overview", ("## Overview",)),
        ("Policy Scope", ("## Policy Scope", "### Policy Scope")),
        ("Controls", ("## Controls", "### Controls")),
        ("Verification", ("## Verification", "### Verification")),
        ("Review Cadence", ("## Review Cadence", "### Review Cadence")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Operation Runbook": [
        ("Overview", ("## Overview",)),
        ("When to Use", ("## When to Use", "### When to Use")),
        ("Procedure", ("## Procedure", "### Procedure", "#### Procedure")),
        ("Evidence", ("## Evidence", "### Evidence", "#### Evidence")),
        ("Rollback or Recovery", ("## Rollback or Recovery", "### Rollback or Recovery", "#### Rollback or Recovery")),
        ("Escalation", ("## Escalation", "### Escalation", "#### Escalation")),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Incident": [
        ("Overview", ("## Overview",)),
        ("Incident Metadata", ("## Incident Metadata",)),
        ("Incident Summary", ("## Incident Summary",)),
        ("Impact", ("## Impact",)),
        ("Timeline", ("## Timeline",)),
        ("Evidence", ("## Evidence",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Postmortem": [
        ("Overview", ("## Overview",)),
        ("Incident Summary", ("## Incident Summary",)),
        ("Impact", ("## Impact",)),
        ("Timeline", ("## Timeline",)),
        ("Root Cause", ("## Root Cause Analysis",)),
        ("Action Items", ("## Action Items",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Reference": [
        ("Overview", ("## Overview",)),
        ("Purpose", ("## Purpose",)),
        ("Repository Role", ("## Repository Role",)),
        ("Scope", ("## Scope",)),
        ("Definitions / Facts", ("## Definitions / Facts",)),
        ("Sources", ("## Sources",)),
        ("Maintenance", ("## Maintenance",)),
        ("Related Documents", ("## Related Documents",)),
    ],
    "Archive Tombstone": [
        ("Overview", ("## Overview",)),
        ("Archive Metadata", ("## Archive Metadata",)),
        ("Current Replacement", ("## Current Replacement",)),
        ("Archive Ledger", ("## Archive Ledger",)),
        ("Related Documents", ("## Related Documents",)),
    ],
}

contract_requirements = {
    "OpenAPI Contract": ("# Target:", "# Cross-links:", "openapi:", "info:", "paths:"),
    "GraphQL Contract": ("# Target:", "# Cross-links:", "schema {", "type Query"),
    "Protobuf Contract": ("// Target:", "// Cross-links:", 'syntax = "proto3";', "service "),
}

operation_forbidden = {
    "Operation Guide": ["## Policy Scope", "## Controls", "## Review Cadence", "## When to Use", "## Procedure"],
    "Operation Policy": ["## Usage", "## Runbook Handoff", "## When to Use", "## Procedure"],
    "Operation Runbook": ["## Usage", "## Policy Scope", "## Controls", "## Exceptions", "## Review Cadence"],
}

placeholder_patterns = [
    re.compile(r"YYYY-MM-DD-<[^>\n]+>"),
    re.compile(r"####-<[^>\n]+>"),
    re.compile(r"<(?:feature-id|feature|topic|item|category|system-or-domain|system-or-domain-name|short-title|bucket|domain|subdomain|incident-title)>"),
]
placeholder_literals = [
    "{Topic Name}",
    "{Guide | Policy | Runbook}",
    "{One-line",
    "{Explain",
    "{Describe",
    "{List",
    "{Owner}",
    "{Review Cadence}",
    "{Update Trigger}",
    "{What this source supports}",
    "{Current",
    "{Last",
    "{Recovery",
    "{Escalation",
    "{Expected",
    "{Verified",
]


def validate_text(path: pathlib.Path, doc_type: str, text: str) -> None:
    if doc_type in heading_requirements:
        for group_name, alternatives in heading_requirements[doc_type]:
            if not any(heading in text for heading in alternatives):
                expected = " or ".join(alternatives)
                failures.append(f"{path}: {doc_type} missing template heading {group_name}: {expected}")
        for literal in operation_forbidden.get(doc_type, []):
            if literal in text:
                failures.append(f"{path}: {doc_type} contains wrong operation profile heading: {literal}")
    elif doc_type in contract_requirements:
        for literal in contract_requirements[doc_type]:
            if literal not in text:
                failures.append(f"{path}: {doc_type} missing contract template literal: {literal}")

    for pattern in placeholder_patterns:
        match = pattern.search(text)
        if match:
            failures.append(f"{path}: unresolved template placeholder remains: {match.group(0)}")
    for literal in placeholder_literals:
        if literal in text:
            failures.append(f"{path}: unresolved template placeholder remains: {literal}")


def normalized_target_doc(doc_type: str, text: str) -> bool:
    if doc_type in contract_requirements:
        return True
    headings = heading_requirements.get(doc_type, ())
    if not headings:
        return False
    if not all(any(heading in text for heading in alternatives) for _, alternatives in headings):
        return False
    if any(pattern.search(text) for pattern in placeholder_patterns):
        return False
    return not any(literal in text for literal in placeholder_literals)


target_docs = sorted(path for path in pathlib.Path("docs").rglob("*") if target_stage_doc(path))
unknown_docs: list[pathlib.Path] = []
normalized_docs = 0
legacy_docs = 0
print(f"target_stage_docs_total={len(target_docs)}")

for path in target_docs:
    doc_type = classify(path)
    if doc_type is None:
        unknown_docs.append(path)
        continue
    text = path.read_text(errors="ignore")
    if not normalized_target_doc(doc_type, text):
        legacy_docs += 1
        continue
    normalized_docs += 1
    validate_text(path, doc_type, text)

print(f"normalized_target_stage_docs_total={normalized_docs}")
print(f"legacy_target_stage_docs_skipped={legacy_docs}")

if legacy_docs:
    failures.append(
        f"all target-stage documents must be normalized; legacy_target_stage_docs_skipped={legacy_docs}"
    )

for path in unknown_docs:
    failures.append(f"{path}: unknown target-stage document type; add a docs/99.templates mapping")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Infra README rubric advisory"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []
required_template_literals = [
    "SNIPPET: INFRA SERVICE READINESS",
    "Folder index README",
    "Service leaf README",
    "Secret refs",
    "Troubleshooting",
    "scripts/validation/",
    "root-level `scripts/*.sh` wrappers",
]
for path in [pathlib.Path("docs/99.templates/templates/common/readme.template.md"), pathlib.Path("infra/README.md")]:
    if not path.is_file():
        failures.append(f"missing rubric source: {path}")
        continue
    text = path.read_text(errors="ignore")
    required = ["Secret refs", "Troubleshooting"] if path.parts[0] == "infra" else required_template_literals
    for literal in required:
        if literal not in text:
            failures.append(f"{path}: missing rubric/lifecycle literal: {literal}")

required_fields = [
    "Purpose",
    "Config files",
    "Config values",
    "Compose linkage",
    "Networks",
    "Volumes",
    "Ports",
    "Labels",
    "Secret refs",
    "Healthcheck",
    "Operations",
    "Validation",
    "Troubleshooting",
]
readmes = sorted(pathlib.Path("infra").rglob("README.md"))


def has_service_marker(directory: pathlib.Path) -> bool:
    marker_names = {
        "compose.yml",
        "compose.yaml",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Dockerfile",
    }
    return any((directory / name).exists() for name in marker_names)


def has_child_readme(directory: pathlib.Path) -> bool:
    return any(
        child.is_dir() and (child / "README.md").is_file()
        for child in directory.iterdir()
        if child.is_dir()
    )


def readme_kind(path: pathlib.Path) -> str:
    directory = path.parent
    if path == pathlib.Path("infra/README.md"):
        return "folder-index"
    if has_service_marker(directory):
        return "service-leaf"
    if has_child_readme(directory):
        return "folder-index"
    return "support"


missing_by_file: dict[str, list[str]] = {}
kind_counts = {"folder-index": 0, "service-leaf": 0, "support": 0}
for path in readmes:
    kind = readme_kind(path)
    kind_counts[kind] += 1
    if kind != "service-leaf":
        continue
    text = path.read_text(errors="ignore")
    missing = [field for field in required_fields if field not in text]
    if missing:
        missing_by_file[str(path)] = missing

print(f"infra_readmes_total={len(readmes)}")
print(f"infra_readmes_folder_index={kind_counts['folder-index']}")
print(f"infra_readmes_service_leaf={kind_counts['service-leaf']}")
print(f"infra_readmes_support={kind_counts['support']}")
print(f"infra_service_readmes_rubric_partial={len(missing_by_file)}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Governance memory contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []

required_files = [
    pathlib.Path("docs/00.agent-governance/memory/README.md"),
    pathlib.Path("docs/00.agent-governance/memory/template.md"),
    pathlib.Path("docs/00.agent-governance/memory/progress.md"),
    pathlib.Path("docs/99.templates/templates/governance/memory.template.md"),
    pathlib.Path("docs/99.templates/templates/governance/progress.template.md"),
]

for path in required_files:
    if not path.is_file():
        failures.append(f"missing governance memory file: {path}")

checks = {
    pathlib.Path("AGENTS.md"): [
        "[LOAD:MEMORY]",
        "docs/00.agent-governance/memory/",
        "update `progress.md` during repository work",
    ],
    pathlib.Path("docs/00.agent-governance/README.md"): [
        "[LOAD:MEMORY]",
        "memory/README.md",
        "mandatory work progress log",
    ],
    pathlib.Path("docs/00.agent-governance/rules/bootstrap.md"): [
        "[LOAD:MEMORY]",
        "Memory is advisory",
        "memory/progress.md",
        "progress logging",
        "docs/99.templates/templates/governance/memory.template.md",
    ],
    pathlib.Path("docs/00.agent-governance/rules/agentic.md"): [
        "advisory retrieval context",
        "Memory notes must not",
        "running work log",
        "docs/99.templates/templates/governance/memory.template.md",
    ],
    pathlib.Path("docs/00.agent-governance/rules/task-checklists.md"): [
        "progress.md",
        "durable finding report",
        "material task progress",
        "final status",
    ],
    pathlib.Path("docs/00.agent-governance/rules/stage-authoring-matrix.md"): [
        "docs/99.templates/templates/governance/memory.template.md",
        "docs/99.templates/templates/governance/progress.template.md",
        "progress log updated",
    ],
    pathlib.Path("docs/00.agent-governance/memory/README.md"): [
        "advisory retrieval context",
        "do not define active policy",
        "Retrieve relevant notes",
        "docs/99.templates/templates/governance/memory.template.md",
        "mandatory agent progress log",
        "docs/99.templates/templates/governance/progress.template.md",
    ],
    pathlib.Path("docs/00.agent-governance/memory/template.md"): [
        "docs/99.templates/templates/governance/memory.template.md",
        "Retrieval Keywords",
        "Last Verified",
        "Evidence",
    ],
    pathlib.Path("docs/99.templates/templates/governance/memory.template.md"): [
        "Memory notes are advisory retrieval context",
        "Retrieval Keywords",
        "Last Verified",
        "## Evidence",
    ],
    pathlib.Path("docs/00.agent-governance/memory/progress.md"): [
        "docs/99.templates/templates/governance/progress.template.md",
        "## Usage Contract",
        "## Current Work Log",
    ],
    pathlib.Path("docs/99.templates/templates/governance/progress.template.md"): [
        "AI agents must update",
        "## Current Work Log",
        "## Phase Tracker",
        "## Related Documents",
    ],
}

for path, literals in checks.items():
    if not path.is_file():
        failures.append(f"missing file for memory contract check: {path}")
        continue
    text = path.read_text(errors="ignore")
    for literal in literals:
        if literal not in text:
            failures.append(f"{path}: missing memory contract literal: {literal}")

memory_note_required = [
    "- Date:",
    "- Layer:",
    "- Status:",
    "- Applies To:",
    "- Tags:",
    "- Retrieval Keywords:",
    "- Last Verified:",
    "## Problem",
    "## Context",
    "## Resolution",
    "## Prevention",
    "## Evidence",
]
memory_dir = pathlib.Path("docs/00.agent-governance/memory")
for path in sorted(memory_dir.glob("*.md")) if memory_dir.exists() else []:
    if path.name in {"README.md", "progress.md", "template.md"}:
        continue
    text = path.read_text(errors="ignore")
    for literal in memory_note_required:
        if literal not in text:
            failures.append(f"{path}: missing memory note template literal: {literal}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Reference stage contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []
root = pathlib.Path("docs/90.references")
template = pathlib.Path("docs/99.templates/templates/common/reference.template.md")

if not root.is_dir():
    failures.append("missing reference stage folder: docs/90.references")

allowed_top_level = {"README.md", "audits", "data", "research", "learning", "llm-wiki"}
required_top_level = {"audits", "data", "research", "learning", "llm-wiki"}
if root.exists():
    present_top_level = {child.name for child in root.iterdir()}
    for required_name in sorted(required_top_level):
        if required_name not in present_top_level:
            failures.append(f"missing reference top-level folder: docs/90.references/{required_name}")
    for child in sorted(root.iterdir()):
        if child.name not in allowed_top_level:
            failures.append(
                f"{child}: unsupported reference top-level entry; expected one of audits, data, research, learning, llm-wiki, README.md"
            )

template_required = [
    "Reference docs provide stable context",
    "## Overview",
    "## Purpose",
    "## Repository Role",
    "## Scope",
    "## Definitions / Facts",
    "## Source Rules",
    "## Sources",
    "## Maintenance",
    "## Related Documents",
    "do not define active policy",
    "secret values",
]
if not template.is_file():
    failures.append(f"missing reference template: {template}")
else:
    text = template.read_text(errors="ignore")
    for literal in template_required:
        if literal not in text:
            failures.append(f"{template}: missing reference-template literal: {literal}")

readme_required = [
    "## Overview",
    "## Audience",
    "## Scope",
    "## Structure",
    "## How to Work in This Area",
    "## Related Documents",
]
for path in sorted(root.rglob("README.md")) if root.exists() else []:
    text = path.read_text(errors="ignore")
    for heading in readme_required:
        if heading not in text:
            failures.append(f"{path}: missing reference README heading: {heading}")
    if path == root / "README.md":
        for heading in [
            "## Repository Role",
            "## Required Format",
            "## Naming and Lifecycle Rules",
            "## Placement Rules",
        ]:
            if heading not in text:
                failures.append(f"{path}: missing reference root README heading: {heading}")
    elif "## Category Role" not in text:
        failures.append(f"{path}: missing reference category README heading: ## Category Role")

reference_required = [
    "## Overview",
    "## Purpose",
    "## Repository Role",
    "## Scope",
    "## Definitions / Facts",
    "## Sources",
    "## Maintenance",
    "## Related Documents",
]
placeholder_markers = [
    "[Item Name]",
    "[Why this reference exists",
    "[How this reference supports",
    "[What is covered]",
    "[What is not covered]",
    "[Source 1]",
    "<category>",
    "<item>",
    "<topic>",
]
for path in sorted(root.rglob("*.md")) if root.exists() else []:
    if path.name == "README.md":
        continue
    text = path.read_text(errors="ignore")
    lines = text.splitlines()
    has_status = (
        len(lines) >= 3
        and lines[0].strip() == "---"
        and any(line.startswith("status:") and line.split(":", 1)[1].strip() for line in lines[1:12])
    )
    if not has_status:
        failures.append(f"{path}: missing frontmatter status")
    for heading in reference_required:
        if heading not in text:
            failures.append(f"{path}: missing reference heading: {heading}")
    for marker in placeholder_markers:
        if marker in text:
            failures.append(f"{path}: unresolved reference-template marker: {marker}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "LLM Wiki contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

failures: list[str] = []

required_files = [
    pathlib.Path("llms.txt"),
    pathlib.Path("scripts/knowledge/generate-llm-wiki-index.sh"),
    pathlib.Path("docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md"),
    pathlib.Path("docs/90.references/llm-wiki/README.md"),
    pathlib.Path("docs/90.references/llm-wiki/llm-wiki-index.md"),
    pathlib.Path("docs/90.references/llm-wiki/repository-map.md"),
    pathlib.Path(".claude/agents/wiki-curator.md"),
    pathlib.Path("docs/00.agent-governance/agents/agents/wiki-curator.md"),
    pathlib.Path("docs/03.specs/096-llm-wiki-agent-first-completion/spec.md"),
    pathlib.Path("docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md"),
    pathlib.Path("docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md"),
]

for path in required_files:
    if not path.is_file():
        failures.append(f"missing LLM Wiki file: {path}")

llms_path = pathlib.Path("llms.txt")
if llms_path.is_file():
    text = llms_path.read_text(errors="ignore")
    required_literals = [
        "docs/90.references/llm-wiki/llm-wiki-index.md",
        "docs/90.references/llm-wiki/repository-map.md",
        "generated tracked repo-local path index",
        "tracked source files",
        "Runtime truth",
        "secrets/",
        "volumes/",
        "graphify-out/",
        "advisory",
        "not authoritative source material",
        "llms-full.txt",
        "public website",
    ]
    for literal in required_literals:
        if literal not in text:
            failures.append(f"{llms_path}: missing LLM Wiki boundary literal: {literal}")

readme_checks = {
    pathlib.Path("README.md"): [
        "llms.txt",
        "docs/90.references/llm-wiki/",
        "docs/90.references/llm-wiki/llm-wiki-index.md",
    ],
    pathlib.Path("docs/README.md"): [
        "90.references/llm-wiki/",
        "LLM Wiki contract",
        "generated index freshness",
    ],
    pathlib.Path("docs/90.references/README.md"): [
        "llm-wiki/README.md",
        "llm-wiki/llm-wiki-index.md",
    ],
    pathlib.Path("docs/05.operations/guides/README.md"): [
        "00-workspace/README.md",
    ],
    pathlib.Path("docs/05.operations/guides/00-workspace/README.md"): [
        "llm-wiki-maintenance.md",
    ],
    pathlib.Path("scripts/README.md"): [
        "generate-llm-wiki-index.sh",
        "--check",
    ],
    pathlib.Path("docs/00.agent-governance/agents/README.md"): [
        "wiki-curator",
    ],
    pathlib.Path("docs/00.agent-governance/subagent-protocol.md"): [
        ".claude/agents/wiki-curator.md",
        "wiki-curator",
    ],
    pathlib.Path(".claude/CLAUDE.md"): [
        "14 workers",
    ],
}
for path, literals in readme_checks.items():
    if not path.is_file():
        failures.append(f"missing file for LLM Wiki README registration: {path}")
        continue
    text = path.read_text(errors="ignore")
    for literal in literals:
        if literal not in text:
            failures.append(f"{path}: missing LLM Wiki registration literal: {literal}")

wiki_files = [path for path in pathlib.Path("docs/90.references/llm-wiki").glob("*.md")]
safety_files = [
    llms_path,
    pathlib.Path("docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md"),
    *wiki_files,
]
for path in safety_files:
    if not path.is_file():
        continue
    text = path.read_text(errors="ignore")
    lower_text = text.lower()
    if "file://" in text:
        failures.append(f"{path}: file:// links are not allowed in LLM Wiki")
    unsafe_phrases = [
        "read secret values",
        "quote secret values",
        "dump secrets",
        "print secrets",
        "graphify-out/ is authoritative",
        "graphify-out is authoritative",
        "graphify-out/ as authoritative",
        "graphify-out as authoritative",
    ]
    for phrase in unsafe_phrases:
        if phrase in lower_text:
            failures.append(f"{path}: unsafe LLM Wiki wording: {phrase}")
    if (
        re.search(r"(?i)\bpublic\s+(site|website|wiki)\b", text)
        and "Out of Scope" not in text
        and "Disallowed" not in text
        and "does not define a public website" not in text
    ):
        failures.append(f"{path}: public wiki/site wording must be explicitly out of scope")

map_path = pathlib.Path("docs/90.references/llm-wiki/repository-map.md")
if map_path.is_file():
    text = map_path.read_text(errors="ignore")
    for literal in [
        "tracked source files",
        "Runtime truth",
        "secrets/",
        "volumes/",
        "graphify-out/",
        "authoritative source",
        "## Repository Map",
    ]:
        if literal not in text:
            failures.append(f"{map_path}: missing repository map boundary literal: {literal}")

index_path = pathlib.Path("docs/90.references/llm-wiki/llm-wiki-index.md")
if index_path.is_file():
    text = index_path.read_text(errors="ignore")
    for literal in [
        "generated_by: scripts/knowledge/generate-llm-wiki-index.sh",
        "Generated tracked repo-local index",
        "## Generated Index",
        "scripts/knowledge/generate-llm-wiki-index.sh --check",
        "wiki-curator",
    ]:
        if literal not in text:
            failures.append(f"{index_path}: missing generated index literal: {literal}")

    generated_section = text.split("## Generated Index", 1)[-1].split("## Sources", 1)[0]
    for forbidden in [
        "volumes/",
        "graphify-out/",
        "node_modules/",
        ".min.js",
        ".min.css",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
    ]:
        if forbidden in generated_section:
            failures.append(f"{index_path}: generated index includes excluded path marker: {forbidden}")
    for match in re.finditer(r"\[([^\]]+)\]\(", generated_section):
        linked_path = match.group(1)
        if linked_path.startswith("secrets/") and linked_path != "secrets/README.md":
            failures.append(f"{index_path}: generated index includes secret content path: {linked_path}")

generator = pathlib.Path("scripts/knowledge/generate-llm-wiki-index.sh")
if generator.is_file() and index_path.is_file():
    result = subprocess.run(
        ["bash", "scripts/knowledge/generate-llm-wiki-index.sh", "--check"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        failures.append("generated LLM Wiki index is stale or generator check failed")
        for line in (result.stderr or result.stdout).splitlines():
            failures.append(f"generate-llm-wiki-index.sh --check: {line}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "HADS reference profile"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

failures: list[str] = []
root = pathlib.Path("docs/90.references/data/hads")

if root.exists():
    for path in sorted(root.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(errors="ignore")
        lines = text.splitlines()
        first_20 = "\n".join(lines[:20])
        if not re.search(r"(?m)^# .+", text):
            failures.append(f"{path}: HADS document missing H1 title")
        if not re.search(r"\*\*Version [0-9]+\.[0-9]+\.[0-9]+\*\*", first_20):
            failures.append(f"{path}: HADS document missing **Version X.Y.Z** in first 20 lines")
        manifest_match = re.search(r"(?m)^## AI READING INSTRUCTION\s*$", text)
        if not manifest_match:
            failures.append(f"{path}: HADS document missing AI READING INSTRUCTION")
        first_content = re.search(r"(?m)^## (?!AI READING INSTRUCTION\b).+", text)
        if manifest_match and first_content and manifest_match.start() > first_content.start():
            failures.append(f"{path}: AI READING INSTRUCTION must appear before first content section")
        if "**[SPEC]**" not in text:
            failures.append(f"{path}: HADS document missing **[SPEC]** block")
        bad_tags = re.findall(r"(?m)^(?<!\*)\[(SPEC|NOTE|BUG|\?)\](?!\*)", text)
        if bad_tags:
            failures.append(f"{path}: HADS block tags must be bold, found plain tags {bad_tags}")
        for bug_match in re.finditer(r"(?ms)^\*\*\[BUG\][^\n]*\*\*\n(.*?)(?=^\*\*\[(?:SPEC|NOTE|BUG|\?)\]|^## |\Z)", text):
            block = bug_match.group(1).lower()
            if "symptom" not in block or "fix" not in block:
                failures.append(f"{path}: HADS BUG block must include symptom and fix")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Infrastructure hardening hard gate"
if ! bash scripts/hardening/check-all-hardening.sh >/tmp/check-repo-contracts-hardening.txt 2>&1; then
  fail "infrastructure hardening hard gate failed"
  cat /tmp/check-repo-contracts-hardening.txt >&2
fi
rm -f /tmp/check-repo-contracts-hardening.txt

section "Script reference integrity"
if ! python3 - <<'PY'; then
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
deleted_entrypoints = {
    "scripts/hardening/check-ai-hardening.sh",
    "scripts/hardening/check-auth-hardening.sh",
    "scripts/hardening/check-data-hardening.sh",
    "scripts/hardening/check-gateway-hardening.sh",
    "scripts/hardening/check-laboratory-hardening.sh",
    "scripts/hardening/check-messaging-hardening.sh",
    "scripts/hardening/check-observability-hardening.sh",
    "scripts/hardening/check-security-hardening.sh",
    "scripts/hardening/check-tooling-hardening.sh",
    "scripts/hardening/check-workflow-hardening.sh",
    "scripts/operations/bootstrap-vault-approle.sh",
    "scripts/operations/generate-local-certs.sh",
    "scripts/validation/preflight-compose.sh",
}

historical_reference_roots = (
    pathlib.Path("docs/00.agent-governance/memory"),
)

reference_artifact_roots = ()

def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True

def allows_deleted_entrypoint_reference(path: pathlib.Path, ref: str) -> bool:
    if ref not in deleted_entrypoints:
        return False
    return any(is_relative_to(path, root) for root in (*historical_reference_roots, *reference_artifact_roots))

for root in roots:
    files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file() and "graphify-out" not in p.parts]
    for path in files:
        if path == pathlib.Path("scripts/validation/check-repo-contracts.sh"):
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
            if allows_deleted_entrypoint_reference(path, ref):
                continue
            failures.append(f"{path}: missing script reference {match.group(0)}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Service documentation coverage"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

stages = ["05.operations/guides"]

# Implementation path names sometimes differ from product names. Keep those
# differences explicit so missing docs do not get hidden by ad-hoc conventions.
document_path_overrides = {
    pathlib.Path("04-data/analytics/ksql"): pathlib.Path("04-data/analytics/ksqldb.md"),
}

# Aggregate compose files are documented by component-level docs in the same
# stage folder, not by a single service markdown file.
aggregate_compose_dirs = {
    pathlib.Path("06-observability"),
}

service_dirs = sorted(
    {
        path.parent.relative_to("infra")
        for path in pathlib.Path("infra").rglob("docker-compose*.yml")
        if path.is_file()
    }
)

failures: list[str] = []

for service_dir in service_dirs:
    if service_dir in aggregate_compose_dirs:
        continue

    doc_rel = document_path_overrides.get(service_dir, pathlib.Path(f"{service_dir}.md"))
    for stage in stages:
        doc_path = pathlib.Path("docs") / stage / doc_rel
        if not doc_path.is_file():
            failures.append(f"missing {stage} service documentation for infra/{service_dir}: expected {doc_path}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Script usage contract"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

readme = pathlib.Path("scripts/README.md")
if not readme.is_file():
    print("FAIL: missing scripts/README.md", file=sys.stderr)
    sys.exit(1)

readme_text = readme.read_text()
failures: list[str] = []
required_readme_fragments = [
    "## Purpose Folder Implementation",
    "scripts/validation/",
    "scripts/hardening/",
    "scripts/hooks/",
    "scripts/knowledge/",
    "scripts/operations/",
    "scripts/lib/",
    "canonical purpose-folder paths",
    "## Active Surface Retention Rules",
    "Historical references under completed requirements",
    "`--check` for readiness checks",
    "`--dry-run` for ID/path-only action previews",
]
for fragment in required_readme_fragments:
    if fragment not in readme_text:
        failures.append(f"scripts/README.md missing script purpose-folder fragment: {fragment}")

root_scripts = sorted(path for path in pathlib.Path("scripts").glob("*.sh") if path.is_file())
lib_scripts = sorted(path for path in pathlib.Path("scripts/lib").glob("*.sh") if path.is_file())
expected_implementations = {
    pathlib.Path("scripts/validation/validate-docker-compose.sh"),
    pathlib.Path("scripts/validation/validate-harness.sh"),
    pathlib.Path("scripts/validation/check-repo-contracts.sh"),
    pathlib.Path("scripts/validation/check-doc-implementation-alignment.sh"),
    pathlib.Path("scripts/validation/check-storybook-contract.sh"),
    pathlib.Path("scripts/validation/check-doc-traceability.sh"),
    pathlib.Path("scripts/validation/check-quickwin-baseline.sh"),
    pathlib.Path("scripts/validation/check-template-security-baseline.sh"),
    pathlib.Path("scripts/validation/recommend-qa-gates.sh"),
    pathlib.Path("scripts/validation/run-local-qa-gates.sh"),
    pathlib.Path("scripts/hardening/check-all-hardening.sh"),
    pathlib.Path("scripts/hooks/agent-event-hook.sh"),
    pathlib.Path("scripts/hooks/patch-graphify-post-commit.sh"),
    pathlib.Path("scripts/hooks/post-tool-validate.sh"),
    pathlib.Path("scripts/knowledge/generate-llm-wiki-index.sh"),
    pathlib.Path("scripts/knowledge/report-graphify-health.sh"),
    pathlib.Path("scripts/operations/gen-secrets.sh"),
    pathlib.Path("scripts/operations/use-qa-ci-tools.sh"),
    pathlib.Path("scripts/operations/sync-provider-surfaces.sh"),
    pathlib.Path("scripts/operations/sync-tech-stack-versions.sh"),
}
implementation_scripts = sorted(
    path
    for folder in ["validation", "hardening", "hooks", "knowledge", "operations"]
    for path in pathlib.Path("scripts", folder).glob("*.sh")
    if path.is_file()
)

for path in root_scripts:
    failures.append(f"root duplicate script remains after purpose-folder migration: {path}")

if set(implementation_scripts) != expected_implementations:
    missing = sorted(expected_implementations - set(implementation_scripts))
    extra = sorted(set(implementation_scripts) - expected_implementations)
    for path in missing:
        failures.append(f"missing purpose-folder implementation: {path}")
    for path in extra:
        failures.append(f"unexpected purpose-folder implementation not inventoried in scripts/README.md: {path}")

for path in sorted(expected_implementations):
    if str(path) not in readme_text:
        failures.append(f"scripts/README.md missing purpose-folder inventory entry: {path}")

scan_roots = [
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
        ".pre-commit-config.yaml",
        "docker-compose.yml",
    ]
    if pathlib.Path(p).exists()
]

def iter_files(root: pathlib.Path) -> list[pathlib.Path]:
    if root.is_file():
        return [root]
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and "graphify-out" not in path.parts
    ]

scanned_files: list[tuple[pathlib.Path, str]] = []
for root in scan_roots:
    for path in iter_files(root):
        try:
            scanned_files.append((path, path.read_text(errors="ignore")))
        except Exception:
            continue

script_texts: list[tuple[pathlib.Path, str]] = []
for script in implementation_scripts:
    try:
        script_texts.append((script, script.read_text(errors="ignore")))
    except Exception:
        continue

for lib_script in lib_scripts:
    candidates = {str(lib_script), f"./{lib_script}", str(lib_script.relative_to("scripts")), lib_script.name}
    referenced = any(
        any(candidate in text for candidate in candidates)
        for _script, text in script_texts
    )
    if not referenced:
        failures.append(f"library script is not referenced by any script implementation: {lib_script}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Floating image tag policy"
if ! python3 - <<'PY'; then
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
  failures=$((failures + 1))
fi

section "Tech-stack version drift"
if ! python3 - <<'PY'; then
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
  failures=$((failures + 1))
fi

section "Documentation runtime version drift"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

stage_roots = [
    pathlib.Path("docs/01.requirements"),
    pathlib.Path("docs/02.architecture"),
    pathlib.Path("docs/03.specs"),
    pathlib.Path("docs/04.execution"),
    pathlib.Path("docs/05.operations"),
]

stale_literals = {
    "v3.6.8": "Traefik is declared as traefik:v3.7.6",
    "v3.6.12": "Traefik is declared as traefik:v3.7.6",
    "26.5.4": "Keycloak is declared as quay.io/keycloak/keycloak:26.6.4-1",
    "7.14.2": "OAuth2 Proxy Dockerfile uses quay.io/oauth2-proxy/oauth2-proxy:v7.15.3",
    "hashicorp/vault:1.21.4": "Vault is declared as hashicorp/vault:2.0.3",
    "Confluent CP 8.1.1": "Kafka is declared as confluentinc/cp-kafka:8.3.0",
    "RabbitMQ 4.2": "RabbitMQ is declared as rabbitmq:4.3.1-management-alpine",
    "kafbat/kafka-ui:v1.4.2": "Kafbat UI is declared as kafbat/kafka-ui:v1.5.0",
    "v0.20.0": "Ollama is declared as ollama/ollama:0.31.1",
    "v0.8.5-cuda": "Open WebUI is declared as ghcr.io/open-webui/open-webui:v0.10.2-cuda",
    "OLLAMA_WEB_UI_PORT": "Open WebUI compose uses OLLAMA_WEBUI_PORT",
    "docker compose -f infra/08-ai/ollama/docker-compose.yml config": "08-ai service-local compose files depend on root infra_net context; use the AI hardening check and root profile validator",
    "docker compose -f infra/08-ai/open-webui/docker-compose.yml config": "08-ai service-local compose files depend on root infra_net context; use the AI hardening check and root profile validator",
    "v10.7.0": "SonarQube is declared as sonarqube:26.5.0.122743-community",
    "v2.0.13": "Syncthing is declared as syncthing/syncthing:2.1.1",
    "hashicorp/terraform:1.14.4": "Terraform helper is declared as hashicorp/terraform:1.15.5",
    "Terrakube 2.29.0": "Terrakube services are declared as 2.31.2 images",
    "azbuilder/api-server:2.29.0": "Terrakube API is declared as azbuilder/api-server:2.31.2",
    "azbuilder/terrakube-ui:2.29.0": "Terrakube UI is declared as azbuilder/terrakube-ui:2.31.2",
    "azbuilder/executor:2.29.0": "Terrakube executor is declared as azbuilder/executor:2.31.2",
    "infra/0Tooling/k6": "k6 leaf path is infra/09-tooling/k6",
    "k6-worker": "Current k6 leaf declares only k6-master; use locust-worker for the Locust leaf",
    "https://k6.${DEFAULT_URL}": "Current k6 leaf has no Traefik route; use the approved host port runtime boundary",
    "https://locust.${DEFAULT_URL}": "Current Locust leaf has no Traefik route; use the approved host port runtime boundary",
    "for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f \"$f\" config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "docker compose -f infra/09-tooling/registry/docker-compose.yml config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "docker compose -f infra/09-tooling/sonarqube/docker-compose.yml config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "docker compose -f infra/09-tooling/terrakube/docker-compose.yml config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "docker compose -f infra/09-tooling/syncthing/docker-compose.yml config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "docker compose -f infra/09-tooling/locust/docker-compose.yml config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "docker compose -f infra/09-tooling/k6/docker-compose.yml config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "docker compose -f infra/09-tooling/terraform/docker-compose.yml config": "09-tooling service-local compose files need root network/secret/dependency context; use the hardening check and approved root+leaf overlay",
    "172.19.0.260": "Stalwart static IP is 172.19.0.228",
    "172.19.0.261": "MailHog static IP is 172.19.0.229",
    "172.19.0.260-261": "10-communication infra_net allocation is 172.19.0.228-229",
    "MailHog HTTP | 8025 | 18025": "MailHog UI is exposed through the Traefik route, not a documented 18025 host port",
    "docker compose -f infra/10-communication/mail/docker-compose.yml config": "10-communication service-local compose depends on root network/secret/template context; use the communication hardening check and approved root-context render",
    "docker-compose --profile communication": "Use Docker Compose v2 spelling and the communication hardening/root-context boundary",
    "for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f \"$f\" config": "11-laboratory service-local compose files depend on root infra_net context; use the laboratory hardening check and root admin profile validator",
    "docker compose -f infra/11-laboratory/open-notebook/docker-compose.yml config": "11-laboratory service-local compose files depend on root infra_net context; use the laboratory hardening check and root admin profile validator",
    "docker compose --profile admin up -d open_notebook surrealdb": "Open Notebook runtime start requires approved root context; use root admin profile validation first",
    "docker compose --profile admin config": "Use HYHOME_COMPOSE_PROFILES=admin with scripts/validation/validate-docker-compose.sh for root-context validation",
    "redis/redisinsight:3.2.0": "RedisInsight is declared as redis/redisinsight:3.6.0",
    "HOMER_HOST_PORT": "Homer has no host port in the current optional compose; Traefik targets HOMER_PORT through expose",
    "docker logs dashboard": "Homer container name is homer",
    "portainer_data": "Portainer volume is portainer-data",
    "redisinsight_data": "RedisInsight volume is redisinsight-data",
    "traefik.http.routers.portainer.middlewares: sso-auth@file": "Portainer route uses the full gateway+allowlist+SSO chain",
    "traefik.http.routers.redisinsight.middlewares: sso-auth@file": "RedisInsight route uses the full gateway+allowlist+SSO chain",
    "v12.3.3": "Grafana is declared as grafana/grafana:13.1.0",
    "v2.10.x": "Airflow is declared as apache/airflow:3.2.2",
    "airflow-webserver": "Airflow 3 uses airflow-apiserver in current workflow docs",
    "Apache n8n": "n8n is not an Apache project in current workflow docs",
    "infra/07-workflow/airflow/dags": "Airflow DAGs are bind-mounted from ${DEFAULT_WORKFLOW_DIR}/airflow/dags",
    "v1.11.2": "Pushgateway is declared as prom/pushgateway:v1.11.3",
    "Pyroscope (v1.18.1)": "Pyroscope is declared as grafana/pyroscope:2.1.0",
    "v1.17-unprivileged": "Qdrant is declared as qdrant/qdrant:v1.18.1-unprivileged",
    "neo4j:5.26.23-community": "Neo4j is declared as neo4j:5.26.26-community",
    "v10.2.0": "Dozzle is declared as amir20/dozzle:v10.6.6",
    "PostgreSQL (v16+)": "PostgreSQL services are currently PostgreSQL 17/18 family images",
    "InfluxDB 2.x 채택": "InfluxDB 3.x Core is the primary compose; InfluxDB 2.x is legacy compose only",
    "OpenSearch 2.x 채택": "OpenSearch 3.x is the current analytics implementation family",
    "StarRocks 3.x 채택": "StarRocks 4.x is the current analytics implementation family",
    "Primary Tech Stack: InfluxDB 2.x, ksqlDB 0.29+, OpenSearch 2.x, StarRocks 3.x": "analytics ARD must describe the current compose-backed version families",
    "Tech Stack**: Docker, InfluxDB 2.x, ksqlDB, OpenSearch 2.x, StarRocks.": "analytics spec must describe the current compose-backed version families",
}

failures: list[str] = []
for root in stage_roots:
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for stale, replacement in stale_literals.items():
                if stale in line:
                    failures.append(f"{path}:{line_no}: stale runtime version {stale!r}; {replacement}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "02-auth current-truth drift"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

auth_stage_files: list[pathlib.Path] = []
for root in [
    pathlib.Path("docs/01.requirements"),
    pathlib.Path("docs/02.architecture"),
    pathlib.Path("docs/03.specs"),
    pathlib.Path("docs/04.execution"),
    pathlib.Path("docs/05.operations"),
]:
    if not root.exists():
        continue
    for path in sorted(root.rglob("*.md")):
        normalized = path.as_posix()
        if "/02-auth/" in normalized or "02-auth" in path.name or "auth-" in path.name:
            auth_stage_files.append(path)

auth_files = auth_stage_files + sorted(pathlib.Path("infra/02-auth").rglob("*"))
allowed_suffixes = {".md", ".yml", ".yaml", ".sh", ".cfg", ".Dockerfile", ""}
auth_files = [path for path in auth_files if path.is_file() and path.suffix in allowed_suffixes]

stale_literals = {
    "26.5.4": "Keycloak current image is quay.io/keycloak/keycloak:26.6.4-1",
    "v26.5.4": "Keycloak current image is quay.io/keycloak/keycloak:26.6.4-1",
    "7.14.2": "OAuth2 Proxy source image is quay.io/oauth2-proxy/oauth2-proxy:v7.15.3",
    "v7.14.2": "OAuth2 Proxy source image is quay.io/oauth2-proxy/oauth2-proxy:v7.15.3",
    "Keycloak: `template-infra-med`": "Keycloak current compose extends template-infra-high",
    "Keycloak은 `template-infra-med`": "Keycloak current compose extends template-infra-high",
    "`service: template-infra-med` 적용 여부": "Keycloak current guide must check template-infra-high",
    "docker compose -f infra/02-auth/keycloak/docker-compose.yml config": "02-auth validation must use root profile validator",
    "docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config": "02-auth validation must use root profile validator",
    "docker compose -f infra/02-auth/keycloak/docker-compose.yml up -d keycloak": "runtime starts must use root compose context",
    "docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml up -d oauth2-proxy": "runtime starts must use root compose context",
    "docker exec keycloak": "runtime checks must use root compose exec context",
    "docker exec oauth2-proxy": "runtime checks must use root compose exec context",
    "docker logs keycloak": "log checks must use root compose logs context",
    "docker logs oauth2-proxy": "log checks must use root compose logs context",
}

failures: list[str] = []
for path in auth_files:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for literal, guidance in stale_literals.items():
        if literal in text:
            failures.append(f"{path}: stale 02-auth literal {literal!r}; {guidance}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "03-security current-truth drift"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

security_stage_files: list[pathlib.Path] = []
for root in [
    pathlib.Path("docs/01.requirements"),
    pathlib.Path("docs/02.architecture"),
    pathlib.Path("docs/03.specs"),
    pathlib.Path("docs/04.execution"),
    pathlib.Path("docs/05.operations"),
]:
    if not root.exists():
        continue
    for path in sorted(root.rglob("*.md")):
        normalized = path.as_posix()
        if "/03-security/" in normalized or "03-security" in path.name or "security-" in path.name or "vault" in path.name:
            security_stage_files.append(path)

security_files = security_stage_files + sorted(pathlib.Path("infra/03-security").rglob("*"))
allowed_suffixes = {".md", ".yml", ".yaml", ".sh", ".hcl", ".ctmpl", ""}
security_files = [path for path in security_files if path.is_file() and path.suffix in allowed_suffixes]

stale_literals = {
    "hashicorp/vault:1.21.4": "Vault current image is hashicorp/vault:2.0.3",
    "v1.21.4": "Vault current image is hashicorp/vault:2.0.3",
    "docs/05.operations/guides/03-security/01.setup.md": "Security setup guidance is consolidated into the Vault guide",
    "guides/03-security/01.setup.md": "Security setup guidance is consolidated into the Vault guide",
    "docker compose -f infra/03-security/vault/docker-compose.yml config": "03-security validation must use root profile validator",
    "docker compose -f infra/03-security/vault/docker-compose.yml up -d vault vault-agent": "runtime starts must use root compose context",
    "cd infra/03-security/vault": "03-security docs must not require service-local working-directory compose context",
    "docker exec vault": "runtime checks must use root compose exec context",
    "docker exec vault-agent": "runtime checks must use root compose exec context",
    "docker logs vault": "log checks must use root compose logs context",
    "docker logs vault-agent": "log checks must use root compose logs context",
    "01~09": "Active documentation scope is Stage 01-05",
    "고가용성 클러스터": "Current Vault implementation is single-node Raft with planned HA expansion",
}

failures: list[str] = []
for path in security_files:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for literal, guidance in stale_literals.items():
        if literal in text:
            failures.append(f"{path}: stale 03-security literal {literal!r}; {guidance}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Gateway current-truth drift"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

roots = [
    pathlib.Path("docs/01.requirements"),
    pathlib.Path("docs/02.architecture"),
    pathlib.Path("docs/03.specs"),
    pathlib.Path("docs/04.execution"),
    pathlib.Path("docs/05.operations"),
    pathlib.Path("infra/01-gateway"),
]

stale_literals = {
    "Traefik v3.6.12": "Traefik is declared as traefik:v3.7.6",
    "Port 80, 443, 7687": "Traefik static entrypoints are web(80), websecure(443), and metrics(8082)",
    "| `7687` | `7687` | TCP | Neo4j Bolt": "Current gateway docs must not claim a public Neo4j Bolt gateway entrypoint",
    "cd infra/01-gateway": "Use root profile validation instead of a nonexistent tier-level compose stack",
    "docker compose up -d traefik": "Traefik runtime actions must use an approved root compose context",
    "docker compose up -d nginx": "Nginx is profile-only and needs an explicit approved runtime context",
    "docker compose -f infra/01-gateway/traefik/docker-compose.yml config": "Use HYHOME_COMPOSE_PROFILES=core with validate-docker-compose.sh for root-context validation",
    "docker compose -f infra/01-gateway/nginx/docker-compose.yml config": "Nginx standalone compose rendering lacks root infra_net/backend context",
    "docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t": "Nginx lint is runtime-only evidence in an approved Nginx context",
    "docker compose -f infra/01-gateway/traefik/docker-compose.yml exec traefik traefik healthcheck --ping": "Traefik healthcheck is runtime-only evidence in the approved root context",
    "average: 1000": "Gateway req-rate-limit average is 100",
    "burst: 300": "Gateway req-rate-limit burst is 50",
}

failures: list[str] = []
for root in roots:
    for path in sorted(root.rglob("*.md")) + sorted(root.rglob("*.yml")) + sorted(root.rglob("*.yaml")):
        text = path.read_text(errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for stale, replacement in stale_literals.items():
                if stale in line:
                    failures.append(f"{path}:{line_no}: stale gateway reference {stale!r}; {replacement}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Harness surface contracts"
harness_map="docs/00.agent-governance/harness-implementation-map.md"
approval_boundaries="docs/00.agent-governance/rules/approval-boundaries.md"
[[ -f "$harness_map" ]] || fail "missing harness implementation map: $harness_map"
[[ -f "$approval_boundaries" ]] || fail "missing approval boundaries rule: $approval_boundaries"
[[ -f "docs/99.templates/templates/governance/harness-task-contract.template.md" ]] || fail "missing harness task contract template"
[[ -f "scripts/validation/validate-harness.sh" ]] || fail "missing harness validation wrapper: scripts/validation/validate-harness.sh"
if ! grep -q -- "--harness" scripts/validation/run-local-qa-gates.sh; then
  fail "run-local-qa-gates.sh missing --harness mode"
fi
if ! grep -q "run-local-qa-gates.sh --harness" scripts/validation/validate-harness.sh; then
  fail "validate-harness.sh must delegate to run-local-qa-gates.sh --harness"
fi
if ! grep -q "validate-harness.sh" scripts/README.md; then
  fail "scripts/README.md missing reference to validate-harness.sh"
fi
if ! grep -q "run-local-qa-gates.sh --harness" scripts/README.md; then
  fail "scripts/README.md missing reference to the harness gate (run-local-qa-gates.sh --harness)"
fi
if ! grep -q "## Harness Impact" .github/PULL_REQUEST_TEMPLATE.md; then
  fail "PR template missing Harness Impact section"
fi
if ! grep -q "validate-harness.sh" .github/PULL_REQUEST_TEMPLATE.md; then
  fail "PR template missing validate-harness.sh evidence command"
fi
if ! grep -q "harness-implementation-map.md" docs/00.agent-governance/README.md; then
  fail "governance README missing harness implementation map reference"
fi

echo
echo "Repo contract check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: repository Docker/docs contracts are synchronized"
