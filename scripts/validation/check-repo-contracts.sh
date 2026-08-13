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

section "Operations catalog approval manifest"
if ! python3 scripts/validation/check-operations-catalog.py --mode manifest; then
  fail "Operations catalog approval manifest is invalid"
fi

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
fi

section "Typed repository gate wiring"
if ! python3 - <<'PY'; then
from __future__ import annotations

import json
import pathlib
import sys

contract_path = pathlib.Path(".github/workflow-contract.yml")
try:
    document = json.loads(contract_path.read_text(encoding="utf-8"))
except (OSError, UnicodeError, json.JSONDecodeError):
    print("FAIL: typed repository gate wiring is unavailable", file=sys.stderr)
    sys.exit(1)

nodes = {
    node.get("gate_id"): node
    for node in document.get("gate_nodes", [])
    if isinstance(node, dict)
}
repo_leaf = nodes.get("leaf.repo-contracts")
repo_root = nodes.get("ci.repo-contracts")
if (
    repo_leaf != {
        "gate_id": "leaf.repo-contracts",
        "kind": "leaf",
        "entrypoint": "scripts/validation/check-repo-contracts.sh",
        "argv": [],
        "cwd": ".",
        "allowed_env_keys": [],
        "timeout_minutes": 10,
        "profiles": [
            "ci",
            "local-script-backed",
            "local-harness",
            "local-all-profiles",
        ],
        "opaque": True,
        "suite_key": "repo-contracts",
    }
    or not isinstance(repo_root, dict)
    or repo_root.get("kind") != "aggregate"
    or repo_root.get("children", [])[-1:] != ["leaf.repo-contracts"]
):
    print("FAIL: typed repository gate wiring differs from the exact contract", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
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

section "Template inventory routing"
# Exact source inventory and template body semantics are owned by the Python
# checker and its canonical registry. This shell keeps only placement routing.

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
import subprocess
import sys

import yaml

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
profiles = yaml.safe_load(
    pathlib.Path("docs/99.templates/support/document-metadata-profiles.yaml").read_text()
)
registered_markdown_sources = {
    pathlib.Path(role["source"])
    for role in profiles["template_roles"].values()
    if role["source"].endswith(".md")
}
governance_markdown_sources = {
    pathlib.Path(profiles["template_roles"][role_name]["source"])
    for role_name in ("memory", "progress")
}


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
    frontmatter = top_frontmatter(text)
    frontmatter_values = [value for _, value in frontmatter]
    if path in governance_markdown_sources:
        if frontmatter_values != ["layer: agentic", "status: draft"]:
            failures.append(
                f"{path}: governance template frontmatter must be exactly layer: agentic and status: draft"
            )
    elif not frontmatter or frontmatter[0][1] != "status: draft":
        failures.append(
            f"{path}: Markdown template frontmatter must start with status: draft"
        )
    if path not in registered_markdown_sources:
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

section "Approval evidence template"
if ! grep -q "^## Approval Evidence" docs/99.templates/templates/sdlc/task.template.md; then
  echo "FAIL: docs/99.templates/templates/sdlc/task.template.md must include conditional Approval Evidence" >&2
  failures=$((failures + 1))
fi
if ! grep -q "policy, runtime, CI, templates, secrets, remote GitHub" docs/00.agent-governance/rules/task-checklists.md; then
  echo "FAIL: Stage 00 task checklist must retain high-risk surface classes" >&2
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

import yaml

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
profiles = yaml.safe_load(
    pathlib.Path("docs/99.templates/support/document-metadata-profiles.yaml").read_text()
)
generated_outputs = {
    pathlib.Path(path) for path in profiles["common"]["generated_outputs"]
}


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


for path in sorted(pathlib.Path("docs").rglob("*.md")):
    if path.name == "README.md" or path in generated_outputs:
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
  --glob '!docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md' >/tmp/check-repo-contracts-english-only-surfaces.txt; then
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
scan_roots = [
    pathlib.Path("docs/99.templates"),
    pathlib.Path("docs/00.agent-governance/rules"),
    pathlib.Path("docs/00.agent-governance/scopes"),
    pathlib.Path(".github/ISSUE_TEMPLATE"),
]
scan_files = {
    pathlib.Path("docs/01.requirements/README.md"),
    pathlib.Path("docs/03.specs/README.md"),
}
for root in scan_roots:
    if root.exists():
        scan_files.update(path for path in root.rglob("*") if path.is_file())

for path in sorted(scan_files):
    if path.suffix.lower() not in {".md", ".yaml", ".yml", ".graphql", ".proto"}:
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
    "policies": ["## Controls", "## Verification", "## Review Cadence"],
    "runbooks": ["## When to Use", "## Procedure", "## Evidence", "## Escalation"],
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
            scope_count = sum(
                1 for line in text.splitlines() if line.strip() == "## Policy Scope"
            )
            if scope_count != 1:
                failures.append(
                    f"{path}: policy document must contain exactly one ## Policy Scope heading; found {scope_count}"
                )
        heading_lines = {line.strip() for line in text.splitlines()}
        for literal in required[bucket]:
            if literal not in heading_lines:
                failures.append(f"{path}: missing {bucket} profile heading: {literal}")
        for literal in forbidden[bucket]:
            if literal in heading_lines:
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
year_re = re.compile(r"^[0-9]{4}$")
packet_re = re.compile(r"^inc-[0-9]{4}-[a-z0-9][a-z0-9-]*$")

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
                failures.append(f"{packet}: incident year folders may contain only inc-####-<slug> packet folders")
                continue
            expected_incident = packet / "incident.md"
            expected_postmortem = packet / "postmortem.md"
            markdown_files = sorted(path for path in packet.glob("*.md"))
            allowed_files = {expected_incident, expected_postmortem}
            for path in markdown_files:
                if path not in allowed_files:
                    failures.append(
                        f"{path}: incident packet markdown files must be incident.md or postmortem.md"
                    )
            if not expected_incident.is_file():
                failures.append(f"{packet}: incident packet is missing {expected_incident.name}")
            if expected_postmortem.is_file() and not expected_incident.is_file():
                failures.append(f"{expected_postmortem}: postmortem requires paired incident file {expected_incident.name}")
    for stale in sorted(incidents_root.rglob("*postmortem*.md")):
        if stale.name != "postmortem.md":
            failures.append(f"{stale}: postmortem file must be named postmortem.md inside the incident packet")

literal_requirements = {
    pathlib.Path("docs/05.operations/incidents/README.md"): [
        "YYYY/inc-####-incident-title/",
        "incident.md",
        "postmortem.md",
    ],
    pathlib.Path("docs/99.templates/support/template-selection.md"): [
        "docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md",
        "docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md",
    ],
    pathlib.Path("docs/00.agent-governance/rules/documentation-protocol.md"): [
        "docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md",
    ],
    pathlib.Path(".claude/skills/ops-runbook-agent/SKILL.md"): [
        "incidents/<year>/inc-####-<slug>/",
        "Filename: `postmortem.md`",
    ],
    pathlib.Path(".claude/skills/incident-response/SKILL.md"): [
        "docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md",
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
    pathlib.Path(".claude/skills/ops-runbook-agent/SKILL.md"),
    pathlib.Path(".claude/skills/incident-response/SKILL.md"),
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

section "Stage 00 GitHub routing contracts"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path("scripts/validation").resolve()))
from github_workflow_contract import (
    WorkflowContractError,
    load_workflow_contract,
    load_workflows,
)

failures: list[str] = []
try:
    workflow_contract = load_workflow_contract(pathlib.Path.cwd())
except WorkflowContractError as error:
    failures.append(
        f".github/workflow-contract.yml: typed workflow contract is invalid ({error.code})"
    )
    required_jobs: set[str] = set()
    required_job_order: tuple[str, ...] = ()
else:
    required_workflows = [
        workflow
        for workflow in workflow_contract.workflows
        if workflow.classification == "required-quality"
    ]
    if len(required_workflows) != 1:
        failures.append(
            ".github/workflow-contract.yml: exactly one required-quality workflow is required"
        )
        required_jobs = set()
        required_job_order: tuple[str, ...] = ()
    else:
        required_job_order = tuple(required_workflows[0].jobs)
        required_jobs = set(required_job_order)
        if len(required_jobs) != 16:
            failures.append(
                ".github/workflow-contract.yml: required-quality workflow must own exactly 16 jobs"
            )

ci_path = ".github/workflows/ci-quality.yml"
try:
    workflow_documents = load_workflows(pathlib.Path.cwd())
except WorkflowContractError as error:
    failures.append(
        f"{ci_path}: workflow document is invalid ({error.code})"
    )
    ci_jobs: set[str] = set()
else:
    matching_ci = [
        document for document in workflow_documents if document.path == ci_path
    ]
    if len(matching_ci) != 1:
        failures.append(f"{ci_path}: required workflow document is unavailable")
        ci_jobs = set()
    else:
        raw_jobs = matching_ci[0].data.get("jobs")
        if not isinstance(raw_jobs, dict) or any(
            not isinstance(job_id, str) for job_id in raw_jobs
        ):
            failures.append(f"{ci_path}: required workflow jobs are invalid")
            ci_jobs = set()
        else:
            ci_jobs = set(raw_jobs)
if ci_jobs != required_jobs:
    failures.append(
        f"{ci_path}: required job IDs differ from the typed workflow contract"
    )

class DuplicateKeyError(yaml.YAMLError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "mapping key must be a hashable scalar",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise DuplicateKeyError("duplicate mapping key")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)
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

governance_path = pathlib.Path(
    "docs/00.agent-governance/rules/github-governance.md"
)
if not governance_path.is_file():
    failures.append(f"missing active GitHub governance surface: {governance_path}")
else:
    governance_text = governance_path.read_text(encoding="utf-8")
    governance_section = re.search(
        r"(?ms)^### Required Quality Gates\s*(.*?)(?:\n### |\Z)",
        governance_text,
    )
    governance_jobs = (
        tuple(
            re.findall(
                r"(?m)^\|\s*`([^`]+)`\s*\|",
                governance_section.group(1),
            )
        )
        if governance_section is not None
        else ()
    )
    if governance_jobs != required_job_order:
        failures.append(
            f"{governance_path}: required quality gate table differs from typed workflow contract"
        )

github_index = pathlib.Path(".github/INDEX.md")
github_readme = pathlib.Path(".github/README.md")
required_index_sections = (
    "Purpose",
    "Surface Map",
    "Authority and Change Routes",
    "Verification",
    "Related Documents",
)
required_index_links = (
    "./workflows/ci-quality.yml",
    "./rulesets/main-protection.md",
    "../docs/00.agent-governance/rules/github-governance.md",
    "../scripts/validation/run-local-qa-gates.sh",
    "../docs/90.references/data/governance/ref-0071-github-actions-control-plane-observation.yaml",
)
if github_readme.exists():
    failures.append(f"{github_readme}: GitHub navigation README is forbidden")
if not github_index.is_file():
    failures.append(f"missing GitHub navigation index: {github_index}")
else:
    index_text = github_index.read_text(encoding="utf-8")
    if index_text.startswith("---"):
        failures.append(f"{github_index}: frontmatter is forbidden")
    index_sections = tuple(re.findall(r"(?m)^## (.+?)\s*$", index_text))
    if index_sections != required_index_sections:
        failures.append(f"{github_index}: section envelope must match navigation contract")
    for link in required_index_links:
        if f"]({link})" not in index_text:
            failures.append(f"{github_index}: missing canonical navigation link")
    if any(f"`{job_id}`" in index_text for job_id in required_jobs):
        failures.append(f"{github_index}: CI job identity duplication is forbidden")
    index_forbidden_patterns = (
        r"(?i)\b(?:must|shall)\b",
        r"(?i)\b16[- ]job\b",
        r"(?i)\b(?:secrets?|vars?|variables?)\.",
        r"\bGITHUB_TOKEN\b",
        r"(?i)\bremote\b.{0,40}\b(?:active|enforced)\b",
        r"(?i)\b(?:active|enforced)\b.{0,40}\bremote\b",
    )
    if any(re.search(pattern, index_text) for pattern in index_forbidden_patterns):
        failures.append(f"{github_index}: navigation-only authority was exceeded")

artifact_contract = pathlib.Path(
    "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml"
)
if not artifact_contract.is_file():
    failures.append(f"missing agent-governance artifact contract: {artifact_contract}")
else:
    try:
        artifact_data = yaml.load(
            artifact_contract.read_text(encoding="utf-8"),
            Loader=UniqueKeyLoader,
        )
    except DuplicateKeyError:
        failures.append(f"{artifact_contract}: duplicate YAML mapping key")
        artifact_data = None
    except yaml.YAMLError:
        failures.append(f"{artifact_contract}: invalid artifact contract YAML")
        artifact_data = None
    expected_index_profile = {
        "profile_id": "github-navigation-index",
        "artifact_type": "github-navigation-index",
        "path_pattern": ".github/INDEX.md",
        "repository_section": "harness",
        "canonical": False,
        "required_keys": [],
        "key_order": [],
        "required_sections": list(required_index_sections),
        "expected_values": {},
    }
    profiles = (
        artifact_data.get("artifacts") or []
        if isinstance(artifact_data, dict)
        else []
    )
    matching_profiles = [
        profile
        for profile in profiles
        if isinstance(profile, dict)
        and profile.get("profile_id") == "github-navigation-index"
    ]
    if matching_profiles != [expected_index_profile]:
        failures.append(
            f"{artifact_contract}: GitHub navigation profile must match the approved non-canonical contract"
        )
    if "github-ci-contract-audit" in artifact_contract.read_text(encoding="utf-8"):
        failures.append(
            f"{artifact_contract}: deleted GitHub CI memo remains an active artifact consumer"
        )

observation_path = pathlib.Path(
    "docs/90.references/data/governance/"
    "github-actions-control-plane-observation.yaml"
)
observation: dict[object, object] | None = None
if not observation_path.is_file():
    failures.append(f"missing remote GitHub observation: {observation_path}")
else:
    observation_text = observation_path.read_text(encoding="utf-8")
    try:
        loaded_observation = yaml.load(observation_text, Loader=UniqueKeyLoader)
    except DuplicateKeyError:
        failures.append(f"{observation_path}: duplicate YAML mapping key")
    except yaml.YAMLError:
        failures.append(f"{observation_path}: invalid remote observation field")
    else:
        if isinstance(loaded_observation, dict):
            observation = loaded_observation
        else:
            failures.append(f"{observation_path}: invalid remote observation field")
    sensitive_observation_re = re.compile(
        r"(?i)(?:\$\{\{\s*secrets\.|github_pat_|ghp_[A-Za-z0-9]|"
        r"authorization\s*:|bearer\s+[A-Za-z0-9])"
    )
    if sensitive_observation_re.search(observation_text):
        failures.append(f"{observation_path}: invalid remote observation field")

if observation is not None:
    expected_observation_keys = {
        "schema_version",
        "observed_at",
        "repository",
        "authority",
        "source_visibility",
        "remote_default_commit",
        "remote_default_source_url",
        "local_base_commit",
        "latest_ci_run_id",
        "latest_ci_source_url",
        "latest_ci_conclusion",
        "observed_ci_jobs",
        "root_cause",
        "managed_workflows",
        "control_plane_verification",
        "public_sources",
        "limitations",
    }
    expected_observation_values = {
        "schema_version": 1,
        "observed_at": "2026-07-26T18:22:32+09:00",
        "repository": "buenhyden/hy-home.docker",
        "authority": "non-authoritative-observation",
        "source_visibility": "public-metadata-only",
        "remote_default_commit": "a897978f",
        "remote_default_source_url": (
            "https://github.com/buenhyden/hy-home.docker/commit/a897978f"
        ),
        "local_base_commit": "e65bb18fa2f6e3fb6235725750c7c57cbe0227ee",
        "latest_ci_run_id": 29777690571,
        "latest_ci_source_url": (
            "https://github.com/buenhyden/hy-home.docker/actions/runs/29777690571"
        ),
        "latest_ci_conclusion": "failure",
        "observed_ci_jobs": 15,
        "root_cause": "unverified",
        "control_plane_verification": "unverified",
    }
    if set(observation) != expected_observation_keys or any(
        observation.get(key) != value
        for key, value in expected_observation_values.items()
    ):
        failures.append(f"{observation_path}: invalid remote observation field")

    expected_managed_workflows = (
        (222509952, "Dependabot Updates"),
        (223086017, "CodeQL"),
        (282786058, "Dependency Graph"),
    )
    expected_managed_keys = {
        "id",
        "name",
        "management_class",
        "observed_state",
        "last_run",
        "source_visibility",
        "review_owner",
        "retrieved_at",
        "source_url",
    }
    managed_workflows = observation.get("managed_workflows")
    managed_valid = (
        isinstance(managed_workflows, list)
        and len(managed_workflows) == len(expected_managed_workflows)
    )
    if managed_valid:
        for record, expected_identity in zip(
            managed_workflows,
            expected_managed_workflows,
            strict=True,
        ):
            if not isinstance(record, dict):
                managed_valid = False
                break
            workflow_id, workflow_name = expected_identity
            expected_record = {
                "id": workflow_id,
                "name": workflow_name,
                "management_class": "github-managed",
                "observed_state": "active",
                "last_run": "unverified",
                "source_visibility": "public-metadata-only",
                "review_owner": "ci-cd-engineer",
                "retrieved_at": "2026-07-26T18:22:32+09:00",
                "source_url": (
                    "https://api.github.com/repos/buenhyden/hy-home.docker/"
                    f"actions/workflows/{workflow_id}"
                ),
            }
            if set(record) != expected_managed_keys or record != expected_record:
                managed_valid = False
                break
    if not managed_valid:
        failures.append(f"{observation_path}: invalid remote observation field")

    expected_public_sources = {
        "repository": "https://github.com/buenhyden/hy-home.docker",
        "actions_secure_use": (
            "https://docs.github.com/en/actions/reference/security/secure-use"
        ),
        "workflow_monitoring": (
            "https://docs.github.com/en/actions/how-tos/monitor-workflows"
        ),
        "rulesets": (
            "https://docs.github.com/en/enterprise-cloud@latest/repositories/"
            "configuring-branches-and-merges-in-your-repository/"
            "managing-rulesets/about-rulesets"
        ),
        "zizmor_v1_28_0": (
            "https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0"
        ),
    }
    expected_limitations = [
        "Authenticated control-plane readback was unavailable, so no enforcement state is inferred.",
        "Public run metadata does not establish a failure root cause.",
        "No raw payload or authenticated workflow log is retained.",
    ]
    if (
        observation.get("public_sources") != expected_public_sources
        or observation.get("limitations") != expected_limitations
    ):
        failures.append(f"{observation_path}: invalid remote observation field")

stale_remote_patterns = (
    r"2026-07-04",
    r"12 remote contexts",
    r"classic branch protection (?:is )?active",
    r"Repository rulesets API returned `0`",
    r"enforce_admins=false",
)
for active_path in (
    pathlib.Path("docs/00.agent-governance/rules/github-governance.md"),
    ruleset,
):
    if not active_path.is_file():
        failures.append(f"missing active GitHub governance surface: {active_path}")
        continue
    active_text = active_path.read_text(encoding="utf-8")
    if (
        "github-actions-control-plane-observation.yaml" not in active_text
        or not re.search(
            r"(?is)(?:control[- ]plane.{0,120}unverified|"
            r"unverified.{0,120}control[- ]plane)",
            active_text,
        )
        or any(
            re.search(pattern, active_text, re.IGNORECASE)
            for pattern in stale_remote_patterns
        )
    ):
        failures.append(f"{active_path}: stale active remote-state claim")

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
    pathlib.Path(".gemini"),
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

import yaml

failures: list[str] = []
profiles = yaml.safe_load(
    pathlib.Path("docs/99.templates/support/document-metadata-profiles.yaml").read_text()
)
registered_markdown_sources = {
    pathlib.Path(role["source"])
    for role in profiles["template_roles"].values()
    if role["source"].endswith(".md")
}
governance_markdown_sources = {
    pathlib.Path(profiles["template_roles"][role_name]["source"])
    for role_name in ("memory", "progress")
}
for path in sorted(pathlib.Path("docs/99.templates/templates").rglob("*.template.md")):
    text = path.read_text(errors="ignore")
    lines = text.splitlines()
    if path in governance_markdown_sources:
        valid_frontmatter = len(lines) >= 4 and lines[:4] == [
            "---",
            "layer: agentic",
            "status: draft",
            "---",
        ]
    else:
        valid_frontmatter = len(lines) >= 3 and lines[:2] == ["---", "status: draft"] and "---" in lines[2:]
    if not valid_frontmatter:
        failures.append(f"{path}: Markdown template frontmatter must start with status: draft")
    if path not in registered_markdown_sources:
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

import yaml

failures: list[str] = []
repo_root = pathlib.Path(".").resolve()
template_root = pathlib.Path("docs/99.templates")
generated_llm_index = pathlib.Path("docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md")
profiles = yaml.safe_load(
    pathlib.Path("docs/99.templates/support/document-metadata-profiles.yaml").read_text()
)
generated_outputs = {
    pathlib.Path(path) for path in profiles["common"]["generated_outputs"]
}
artifact_contract = yaml.safe_load(
    pathlib.Path(
        "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml"
    ).read_text()
)
current_memory_path = pathlib.Path(
    "docs/00.agent-governance/memory/current.md"
)
current_memory_profiles = [
    profile
    for profile in artifact_contract.get("artifacts", [])
    if isinstance(profile, dict)
    and profile.get("profile_id") == "governance-current-memory"
]
if (
    len(current_memory_profiles) != 1
    or current_memory_profiles[0].get("path_pattern")
    != current_memory_path.as_posix()
):
    failures.append("governance current-memory profile path mismatch")
    related_documents_exemptions: set[pathlib.Path] = set()
else:
    related_documents_exemptions = {current_memory_path}

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
        "docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md",
        "docs/05.operations/runbooks/04-data/analytics/influxdb.md",
        "docs/05.operations/runbooks/04-data/analytics/ksqldb.md",
        "docs/05.operations/runbooks/04-data/analytics/opensearch.md",
        "docs/05.operations/runbooks/04-data/analytics/warehouses.md",
        "docs/05.operations/runbooks/04-data/operational/supabase.md",
        "docs/05.operations/runbooks/04-data/relational.md",
        "docs/05.operations/runbooks/05-messaging/kafka.md",
        "docs/05.operations/runbooks/05-messaging/rabbitmq.md",
        "docs/05.operations/08-ai/ops-0056-ollama/runbook.md",
        "docs/05.operations/08-ai/ops-0057-open-webui/runbook.md",
        "docs/05.operations/11-laboratory/ops-0071-dashboard/runbook.md",
        "docs/05.operations/11-laboratory/ops-0072-dozzle/runbook.md",
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
    and path not in generated_outputs
]

for path in active_markdown_files:
    text = path.read_text(errors="ignore")
    if path not in related_documents_exemptions:
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

section "Infra README rubric advisory"
if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []
rubric_sources = {
    pathlib.Path("docs/99.templates/support/readme-profile-contract.md"): [
        "Folder index README",
        "Service leaf README",
        "Secret refs",
        "Troubleshooting",
        "scripts/validation/",
        "root-level `scripts/*.sh` duplicates",
    ],
    pathlib.Path("infra/README.md"): ["Secret refs", "Troubleshooting"],
    pathlib.Path("scripts/README.md"): [
        "scripts/validation/",
        "root-level `scripts/*.sh` duplicates",
    ],
}
for path, required in rubric_sources.items():
    if not path.is_file():
        failures.append(f"missing rubric source: {path}")
        continue
    text = path.read_text(errors="ignore")
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

sys.path.insert(0, str(pathlib.Path("scripts/validation").resolve()))
import agent_governance_contract as governance_contract

failures: list[str] = []

required_files = [
    pathlib.Path("docs/00.agent-governance/memory/README.md"),
    pathlib.Path("docs/00.agent-governance/memory/current.md"),
    pathlib.Path("docs/00.agent-governance/memory/progress.md"),
    pathlib.Path("docs/99.templates/templates/governance/memory.template.md"),
    pathlib.Path("docs/99.templates/templates/governance/progress.template.md"),
]

for path in required_files:
    if not path.is_file():
        failures.append(f"missing governance memory file: {path}")

route_checks = {
    pathlib.Path("docs/00.agent-governance/README.md"): [
        "[LOAD:MEMORY]",
        "memory/current.md",
        "memory/README.md",
        "applicable Stage 04 Task",
    ],
    pathlib.Path("docs/00.agent-governance/rules/bootstrap.md"): [
        "[LOAD:MEMORY]",
        "Memory is advisory",
        "memory/current.md",
        "applicable Stage 04 Task",
    ],
    pathlib.Path("docs/00.agent-governance/rules/agentic.md"): [
        "memory/current.md",
        "applicable Stage 04 Task",
    ],
    pathlib.Path("docs/00.agent-governance/rules/task-checklists.md"): [
        "memory/current.md",
        "applicable Stage 04 Task",
    ],
    pathlib.Path("docs/00.agent-governance/rules/stage-authoring-matrix.md"): [
        "memory/current.md",
        "Stage 04 Task evidence recorded",
    ],
    pathlib.Path("docs/00.agent-governance/memory/README.md"): [
        "current.md",
        "Stage 04 Task",
        "progress.md",
    ],
}

for path, literals in route_checks.items():
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
    if path.name in {"README.md", "current.md", "progress.md", "template.md"}:
        continue
    text = path.read_text(errors="ignore")
    for literal in memory_note_required:
        if literal not in text:
            failures.append(f"{path}: missing memory note template literal: {literal}")

try:
    contract_bundle = governance_contract.load_contract_bundle(
        pathlib.Path(".").resolve()
    )
except governance_contract.ContractLoadError as error:
    failures.append(
        f"{error.code} path={error.path} location={error.location}"
    )
except (OSError, UnicodeError, ValueError, TypeError):
    failures.append("governance current-memory contract unavailable")
else:
    current_memory_findings = governance_contract._validate_current_memory(
        pathlib.Path(".").resolve(),
        contract_bundle,
    )
    if current_memory_findings:
        failures.extend(
            governance_contract.render_findings([finding])
            for finding in current_memory_findings
        )

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
import re
import sys

import yaml

failures: list[str] = []
root = pathlib.Path("docs/90.references")
template = pathlib.Path("docs/99.templates/templates/common/reference.template.md")
profiles = yaml.safe_load(
    pathlib.Path("docs/99.templates/support/document-metadata-profiles.yaml").read_text()
)
generated_outputs = {
    pathlib.Path(path) for path in profiles["common"]["generated_outputs"]
}

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
    "# {{title}}",
    "## Overview",
    "## Purpose",
    "## Scope",
    "## Definitions / Facts",
    "## Sources",
    "## Maintenance",
    "## Related Documents",
]
if not template.is_file():
    failures.append(f"missing reference template: {template}")
else:
    text = template.read_text(errors="ignore")
    for literal in template_required:
        if literal not in text:
            failures.append(f"{template}: missing reference-template literal: {literal}")

common_contract = pathlib.Path("docs/99.templates/support/common-document-contract.md")
common_contract_required = [
    "stable, source-backed facts",
    "current policy",
]
source_discipline_required = [
    "Reference, Audit, generated output, and Repo-support",
    "secret values",
    "credentials or tokens",
    "private keys",
    "shell history",
    "raw secret-bearing logs",
]
if not common_contract.is_file():
    failures.append(f"missing common document contract: {common_contract}")
else:
    text = common_contract.read_text(errors="ignore")
    for literal in common_contract_required:
        if literal not in text:
            failures.append(f"{common_contract}: missing Reference support literal: {literal}")
    section_heading = "## Source and Evidence Discipline"
    if section_heading not in text:
        failures.append(f"{common_contract}: missing Common evidence-discipline section")
    else:
        section = text.split(section_heading, 1)[1]
        next_heading = re.search(r"^## ", section, flags=re.MULTILINE)
        if next_heading:
            section = section[: next_heading.start()]
        for literal in source_discipline_required:
            if literal not in section:
                failures.append(
                    f"{common_contract}: missing Source and Evidence Discipline literal: {literal}"
                )

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
    if path.name == "README.md" or path in generated_outputs:
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
    pathlib.Path("scripts/knowledge/generate-llm-wiki.py"),
    pathlib.Path("docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md"),
    pathlib.Path("docs/90.references/llm-wiki/README.md"),
    pathlib.Path("docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md"),
    pathlib.Path("docs/90.references/llm-wiki/ref-0083-repository-map.md"),
    pathlib.Path("docs/90.references/data/knowledge/README.md"),
    pathlib.Path("docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md"),
    pathlib.Path(".claude/agents/doc-writer.md"),
    pathlib.Path("docs/00.agent-governance/agents/agents/doc-writer.md"),
    pathlib.Path("docs/00.agent-governance/agents/functions/knowledge-map-agent.md"),
    pathlib.Path("docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md"),
]

for path in required_files:
    if not path.is_file():
        failures.append(f"missing LLM Wiki file: {path}")

llms_path = pathlib.Path("llms.txt")
if llms_path.is_file():
    text = llms_path.read_text(errors="ignore")
    required_literals = [
        "docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md",
        "docs/90.references/llm-wiki/ref-0083-repository-map.md",
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
        "docs/90.references/llm-wiki/ref-0083-repository-map.md",
    ],
    pathlib.Path("docs/README.md"): [
        "90.references/llm-wiki/",
        "LLM Wiki contract",
        "generated index freshness",
    ],
    pathlib.Path("docs/90.references/README.md"): [
        "llm-wiki/README.md",
        "llm-wiki/ref-0082-llm-wiki-index.md",
    ],
    pathlib.Path("scripts/README.md"): [
        "generate-llm-wiki.py",
        "check-script-manifest.py",
        "--check",
    ],
    pathlib.Path("docs/90.references/data/README.md"): [
        "knowledge/README.md",
        "knowledge/ref-0076-llm-wiki-stage-category-coverage.md",
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
    pathlib.Path("docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md"),
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

map_path = pathlib.Path("docs/90.references/llm-wiki/ref-0083-repository-map.md")
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

index_path = pathlib.Path("docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md")
if index_path.is_file():
    text = index_path.read_text(errors="ignore")
    for literal in [
        "generated_by: scripts/knowledge/generate-llm-wiki.py",
        "Generated tracked repo-local index",
        "## Generated Index",
        "scripts/knowledge/generate-llm-wiki.py --check",
        "doc-writer",
        "knowledge-map-agent",
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

coverage_path = pathlib.Path("docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md")
if coverage_path.is_file():
    text = coverage_path.read_text(errors="ignore")
    for literal in [
        "generated_by: scripts/knowledge/generate-llm-wiki.py",
        "## Source Bucket Coverage",
        "## LLM Wiki Category Coverage",
        "## Path Role Coverage",
        "scripts/knowledge/generate-llm-wiki.py --check",
        "graphify-out/",
        "secrets/README.md",
    ]:
        if literal not in text:
            failures.append(f"{coverage_path}: missing generated coverage literal: {literal}")

    coverage_tables = text.split("## Source Bucket Coverage", 1)[-1].split("## Sources", 1)[0]
    for forbidden in [
        "volumes/",
        "node_modules/",
        ".min.js",
        ".min.css",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
    ]:
        if forbidden in coverage_tables:
            failures.append(f"{coverage_path}: generated coverage includes excluded path marker: {forbidden}")
    for match in re.finditer(r"\[([^\]]+)\]\(", coverage_tables):
        linked_path = match.group(1)
        if linked_path.startswith("secrets/") and linked_path != "secrets/README.md":
            failures.append(f"{coverage_path}: generated coverage includes secret content path: {linked_path}")

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

section "Gap routing recommender"
if ! bash scripts/validation/recommend-gap-routing.sh --text "runbook recovery procedure is missing rollback evidence" >/tmp/check-repo-contracts-gap-routing-ops.txt 2>&1; then
  fail "gap routing recommender failed for operations text"
  cat /tmp/check-repo-contracts-gap-routing-ops.txt >&2
elif ! grep -q "suggested_owner=\`docs/05.operations/\`" /tmp/check-repo-contracts-gap-routing-ops.txt; then
  fail "gap routing recommender did not route operations text to docs/05.operations"
  cat /tmp/check-repo-contracts-gap-routing-ops.txt >&2
fi
rm -f /tmp/check-repo-contracts-gap-routing-ops.txt

if ! bash scripts/validation/recommend-gap-routing.sh --files docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md >/tmp/check-repo-contracts-gap-routing-spec.txt 2>&1; then
  fail "gap routing recommender failed for spec path"
  cat /tmp/check-repo-contracts-gap-routing-spec.txt >&2
elif ! grep -q "suggested_owner=\`docs/03.specs/\`" /tmp/check-repo-contracts-gap-routing-spec.txt; then
  fail "gap routing recommender did not route spec path to docs/03.specs"
  cat /tmp/check-repo-contracts-gap-routing-spec.txt >&2
fi
rm -f /tmp/check-repo-contracts-gap-routing-spec.txt

if ! bash scripts/validation/recommend-gap-routing.sh --text "token=example-redacted" >/tmp/check-repo-contracts-gap-routing-redaction.txt 2>&1; then
  fail "gap routing recommender failed for redaction fixture"
  cat /tmp/check-repo-contracts-gap-routing-redaction.txt >&2
elif ! grep -q 'suggested_owner=Stage 04 task/audit gap first' /tmp/check-repo-contracts-gap-routing-redaction.txt; then
  fail "gap routing recommender did not route protected text to Stage 04 task/audit gap first"
  cat /tmp/check-repo-contracts-gap-routing-redaction.txt >&2
elif ! grep -q 'input=\[redacted-sensitive-input\]' /tmp/check-repo-contracts-gap-routing-redaction.txt; then
  fail "gap routing recommender did not redact sensitive-looking text input"
  cat /tmp/check-repo-contracts-gap-routing-redaction.txt >&2
fi
rm -f /tmp/check-repo-contracts-gap-routing-redaction.txt

section "Audit pack coverage report"
if ! bash scripts/validation/report-audit-pack-coverage.sh --check >/tmp/check-repo-contracts-audit-pack-coverage.txt 2>&1; then
  fail "agentic engineering audit-pack coverage report failed"
  cat /tmp/check-repo-contracts-audit-pack-coverage.txt >&2
elif ! grep -q 'coverage_check=pass' /tmp/check-repo-contracts-audit-pack-coverage.txt; then
  fail "agentic engineering audit-pack coverage report did not print a pass marker"
  cat /tmp/check-repo-contracts-audit-pack-coverage.txt >&2
fi
rm -f /tmp/check-repo-contracts-audit-pack-coverage.txt

section "Agentic audit semantic freshness"
semantic_audit_output="$(mktemp "${TMPDIR:-/tmp}/check-repo-contracts-agentic-audit-semantic.XXXXXX")"
cleanup_semantic_audit_output() {
  rm -f -- "$semantic_audit_output"
}
handle_semantic_audit_signal() {
  local exit_code="$1"
  cleanup_semantic_audit_output
  trap - EXIT HUP INT TERM
  exit "$exit_code"
}
trap cleanup_semantic_audit_output EXIT
trap 'handle_semantic_audit_signal 129' HUP
trap 'handle_semantic_audit_signal 130' INT
trap 'handle_semantic_audit_signal 143' TERM
if ! python3 scripts/validation/check-agentic-audit-semantic-freshness.py >"$semantic_audit_output" 2>&1; then
  fail "agentic audit semantic freshness failed"
  cat "$semantic_audit_output" >&2
elif ! grep -Fxq 'audit_semantic_freshness: PASS assertions=11 failures=0' "$semantic_audit_output"; then
  fail "agentic audit semantic validator did not print the exact pass marker"
  cat "$semantic_audit_output" >&2
fi
cleanup_semantic_audit_output
trap - EXIT HUP INT TERM

section "Controlled agent pre-commit wrapper contract"
wrapper_script="scripts/validation/run-agent-precommit-all-files.sh"
wrapper_tests="tests/validation/test_run_agent_precommit_all_files.sh"
[[ -x "$wrapper_script" ]] || fail "controlled agent pre-commit wrapper is missing or not executable: $wrapper_script"
[[ -x "$wrapper_tests" ]] || fail "controlled agent pre-commit wrapper tests are missing or not executable: $wrapper_tests"
if [[ -x "$wrapper_script" && -x "$wrapper_tests" ]]; then
  if ! bash -n "$wrapper_script" "$wrapper_tests"; then
    fail "controlled agent pre-commit wrapper or tests failed Bash syntax validation"
  fi
  wrapper_test_output="$(mktemp "${TMPDIR:-/tmp}/check-repo-contracts-agent-precommit.XXXXXX")"
  if ! bash "$wrapper_tests" >"$wrapper_test_output" 2>&1; then
    fail "controlled agent pre-commit wrapper tests failed"
    cat "$wrapper_test_output" >&2
  elif ! grep -Eq '^passed=[1-9][0-9]* failed=0$' "$wrapper_test_output"; then
    fail "controlled agent pre-commit wrapper tests did not print the expected pass marker"
    cat "$wrapper_test_output" >&2
  else
    critical_wrapper_cases=(
      "clean linked worktree runs the exact command"
      "fake pre-commit exit status is propagated"
      "after snapshot Git failure fails closed and reports hook exit"
      "unexpected-path status remains distinct from hook failure"
      "registered files-modified failure emits one bounded tuple"
      "unsafe or incomplete failure metadata emits unavailable"
      "duplicate registered metadata fails closed"
      "raw-output spoof fails closed without leaking values"
    )
    for critical_wrapper_case in "${critical_wrapper_cases[@]}"; do
      if ! grep -Fxq "ok - $critical_wrapper_case" "$wrapper_test_output"; then
        fail "controlled agent pre-commit wrapper tests omitted a critical case: $critical_wrapper_case"
        cat "$wrapper_test_output" >&2
        break
      fi
    done
  fi
  rm -f "$wrapper_test_output"
fi

if ! python3 - <<'PY'; then
from __future__ import annotations

import pathlib
import sys

wrapper = pathlib.Path("scripts/validation/run-agent-precommit-all-files.sh")
required_wrapper_fragments = [
    "pre-commit run --all-files --show-diff-on-failure",
    "git rev-parse --absolute-git-dir",
    "git rev-parse --path-format=absolute --git-common-dir",
    "git status --porcelain=v1 -z --untracked-files=all",
    "path_has_symlink_component",
    "TASK_INDEX_MODE",
    "EXIT_SNAPSHOT=6",
    "EXIT_UNEXPECTED_PATHS=20",
    "handle_signal HUP 129",
    "handle_signal INT 130",
    "handle_signal TERM 143",
]

required_surface_fragments = {
    pathlib.Path("scripts/README.md"): [
        "scripts/validation/run-agent-precommit-all-files.sh",
        "Direct all-files execution is prohibited",
        "never writes task evidence",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/00.agent-governance/rules/environment-constraints.md"): [
        "Direct `pre-commit run` execution by agents is prohibited",
        "scripts/validation/run-agent-precommit-all-files.sh",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/00.agent-governance/rules/postflight-checklist.md"): [
        "Direct `pre-commit run` was not used",
        "Controlled wrapper reports exit 20",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/00.agent-governance/rules/task-checklists.md"): [
        "Never run `pre-commit run` directly",
        "scripts/validation/run-agent-precommit-all-files.sh",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/00.agent-governance/rules/github-governance.md"): [
        "must not invoke `pre-commit run` directly",
        "scripts/validation/run-agent-precommit-all-files.sh",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/00.agent-governance/rules/workflows.md"): [
        "run all-files pre-commit only through",
        "scripts/validation/run-agent-precommit-all-files.sh",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/00.agent-governance/scopes/common.md"): [
        "direct `pre-commit run`",
        "scripts/validation/run-agent-precommit-all-files.sh",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/00.agent-governance/scopes/qa.md"): [
        "must not invoke `pre-commit run` directly",
        "scripts/validation/run-agent-precommit-all-files.sh",
        "unexpected-path exit",
        "Git-visible, non-ignored repository",
    ],
    pathlib.Path("docs/99.templates/templates/sdlc/task.template.md"): [
        "## Controlled Agent Pre-commit Evidence",
        "{{controlled_wrapper_command}}",
        "{{controlled_wrapper_allowed_prefixes}}",
        "{{controlled_wrapper_exit_status}}",
        "{{controlled_wrapper_snapshot_result}}",
        "{{controlled_wrapper_observation_boundary}}",
        "{{controlled_wrapper_path_sets}}",
        "{{controlled_wrapper_disposition}}",
    ],
}

forbidden_ambiguous_fragments = [
    "do not run `pre-commit` manually",
    "hooks will pass (never run manually)",
    "`pre-commit` for formatting/linting",
]

failures: list[str] = []
wrapper_text = wrapper.read_text(encoding="utf-8") if wrapper.is_file() else ""
for fragment in required_wrapper_fragments:
    if fragment not in wrapper_text:
        failures.append(f"{wrapper}: missing controlled-wrapper fragment: {fragment}")

for path, fragments in required_surface_fragments.items():
    if not path.is_file():
        failures.append(f"missing controlled-wrapper contract surface: {path}")
        continue
    text = path.read_text(encoding="utf-8")
    for fragment in fragments:
        if fragment not in text:
            failures.append(f"{path}: missing controlled-wrapper contract fragment: {fragment}")
    for fragment in forbidden_ambiguous_fragments:
        if fragment in text:
            failures.append(f"{path}: retains ambiguous direct-agent pre-commit instruction: {fragment}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
  failures=$((failures + 1))
fi

section "Script reference integrity"
if ! python3 - <<'PY'; then
from __future__ import annotations

import os
import pathlib
import re
import stat
import subprocess
import sys
from typing import Final


# Baseline 2026-07-16: 1,338 surfaces, 23,602,312 aggregate bytes, and a
# 9,242,745-byte largest tracked artifact. These immutable ceilings leave
# measured repository growth headroom while keeping every scan deterministic.
MAX_REFERENCE_SURFACES: Final = 4_096
MAX_REFERENCE_FILE_BYTES: Final = 16 * 1_048_576
MAX_REFERENCE_TOTAL_BYTES: Final = 64 * 1_048_576
MAX_REFERENCE_DISCOVERY_ENTRIES: Final = 8_192
MAX_REFERENCE_GIT_OUTPUT_BYTES: Final = 1_048_576
MAX_REFERENCE_PATH_BYTES: Final = 4_096
MAX_REFERENCE_CONTEXT_CHARS: Final = 4_096
MAX_REFERENCE_CONTEXT_BYTES: Final = 4_096
MAX_REFERENCE_MATCHES: Final = 16_384
MAX_REFERENCE_UNIQUE_TARGETS: Final = 8_192
MAX_REFERENCE_FAILURES: Final = 4_096
MAX_REFERENCE_FAILURE_BYTES: Final = 1_048_576


class UnsafeScriptReferenceSurface(Exception):
    pass

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
    if os.path.lexists(p)
]

failures: list[str] = []
approved_reference_prefix = (
    r"(?:\./|\$BASE_DIR/|\$\{ROOT\}/|"
    r"\$\(git rev-parse --show-toplevel\)/)?"
)
pattern = re.compile(
    r"(?<![\w./$({-])" + approved_reference_prefix
    + r"(?P<ref>scripts/[A-Za-z0-9._/-]+\.sh)"
)
uri_scheme_boundary = re.compile(
    r"(?:^|[=(\[<{\x27\x22])[A-Za-z][A-Za-z0-9+.-]*:"
)
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

# Paths that never existed in this tree but are cited by evidence documents
# precisely to record their absence. Stage 04 execution evidence and Stage 90
# references must be able to state "this path is absent and no substitute was
# invented" without that honest record counting as a broken reference. Keep the
# set explicit so a genuinely broken link still fails.
absent_documented_entrypoints = {
    "scripts/governance/validate-cross-links.sh",
}

absence_record_roots = (
    pathlib.Path("docs/04.execution"),
    pathlib.Path("docs/90.references"),
)

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

def allows_absence_record_reference(path: pathlib.Path, ref: str) -> bool:
    if ref not in absent_documented_entrypoints:
        return False
    return any(is_relative_to(path, root) for root in absence_record_roots)

def git_paths(*arguments: str) -> tuple[pathlib.Path, ...] | None:
    try:
        process = subprocess.Popen(
            [
                "git",
                "ls-files",
                "-z",
                *arguments,
                "--",
                *(root.as_posix() for root in roots),
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    if process.stdout is None:
        process.kill()
        process.wait()
        return None

    paths: list[pathlib.Path] = []
    pending = bytearray()
    output_bytes = 0
    try:
        while True:
            chunk = process.stdout.read(
                min(64 * 1_024, MAX_REFERENCE_GIT_OUTPUT_BYTES - output_bytes + 1)
            )
            if not chunk:
                break
            output_bytes += len(chunk)
            if output_bytes > MAX_REFERENCE_GIT_OUTPUT_BYTES:
                raise ValueError
            for byte in chunk:
                if byte == 0:
                    if pending:
                        paths.append(
                            pathlib.Path(pending.decode("utf-8", errors="strict"))
                        )
                        if len(paths) > MAX_REFERENCE_SURFACES:
                            raise ValueError
                        pending.clear()
                    continue
                if len(pending) >= MAX_REFERENCE_PATH_BYTES:
                    raise ValueError
                pending.append(byte)
        if pending:
            raise ValueError
    except (OSError, UnicodeError, ValueError):
        try:
            process.kill()
        except OSError:
            pass
        process.wait()
        return None
    if process.wait() != 0:
        return None
    return tuple(paths)


tracked = git_paths("--cached")
untracked = git_paths("--others", "--exclude-standard")
if tracked is None or untracked is None:
    print("FAIL: unsafe script-reference surface", file=sys.stderr)
    sys.exit(1)

tracked_set = set(tracked)


def is_untracked_python_cache(path: pathlib.Path) -> bool:
    return path.suffix == ".pyc" and "__pycache__" in path.parts


def is_ignored(path: pathlib.Path) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path.as_posix()],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def untracked_special_paths() -> set[pathlib.Path] | None:
    """Find non-regular surfaces Git cannot represent in an untracked listing."""

    discovered: set[pathlib.Path] = set()
    tracked_prefixes: set[pathlib.Path] = set()
    for tracked_path in tracked_set:
        for parent in tracked_path.parents:
            if parent == pathlib.Path(".") or parent in tracked_prefixes:
                continue
            if len(tracked_prefixes) >= MAX_REFERENCE_DISCOVERY_ENTRIES:
                return None
            tracked_prefixes.add(parent)
    pending = list(reversed(roots))
    discovery_count = len(pending)
    if discovery_count > MAX_REFERENCE_DISCOVERY_ENTRIES:
        return None
    while pending:
        path = pending.pop()
        try:
            metadata = os.lstat(path)
        except OSError:
            continue
        if stat.S_ISDIR(metadata.st_mode):
            if path not in tracked_prefixes and is_ignored(path):
                continue
            try:
                with os.scandir(path) as entries:
                    for entry in entries:
                        discovery_count += 1
                        if discovery_count > MAX_REFERENCE_DISCOVERY_ENTRIES:
                            return None
                        child = path / entry.name
                        if len(os.fsencode(child.as_posix())) > MAX_REFERENCE_PATH_BYTES:
                            return None
                        pending.append(child)
            except OSError:
                discovered.add(path)
                continue
            continue
        if (
            path not in tracked_set
            and not stat.S_ISREG(metadata.st_mode)
            and not is_ignored(path)
        ):
            discovered.add(path)
    return discovered


special_paths = untracked_special_paths()
if special_paths is None:
    print("FAIL: unsafe script-reference surface", file=sys.stderr)
    sys.exit(1)

file_set: set[pathlib.Path] = set()


def add_surface(path: pathlib.Path) -> None:
    if path in file_set:
        return
    if len(file_set) >= MAX_REFERENCE_SURFACES:
        raise UnsafeScriptReferenceSurface
    file_set.add(path)


try:
    for path in tracked_set:
        add_surface(path)
    for path in untracked:
        if path not in tracked_set and not is_untracked_python_cache(path):
            add_surface(path)
    for path in special_paths:
        add_surface(path)
except UnsafeScriptReferenceSurface:
    print("FAIL: unsafe script-reference surface", file=sys.stderr)
    sys.exit(1)

files = sorted(file_set)


def safe_parts(path: pathlib.Path) -> tuple[str, ...]:
    pure = pathlib.PurePosixPath(path.as_posix())
    if pure.is_absolute() or not pure.parts or any(
        part in {"", ".", ".."} for part in pure.parts
    ):
        raise UnsafeScriptReferenceSurface
    return pure.parts


total_reference_bytes = 0


def metadata_tuple(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    """Return the immutable identity and mutation tuple for one descriptor."""

    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def open_confined_regular(
    path: pathlib.Path, *, size_limit: int | None = None
) -> tuple[list[int], int, os.stat_result]:
    """lstat then read the same root-confined, non-symlink regular file."""

    parts = safe_parts(path)
    try:
        initial = os.lstat(path)
    except OSError as error:
        raise UnsafeScriptReferenceSurface from error
    if not stat.S_ISREG(initial.st_mode) or (
        size_limit is not None and initial.st_size > size_limit
    ):
        raise UnsafeScriptReferenceSurface
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
    descriptors: list[int] = []
    try:
        current = os.open(".", directory_flags)
        descriptors.append(current)
        for part in parts[:-1]:
            current = os.open(part, directory_flags, dir_fd=current)
            descriptors.append(current)
        file_descriptor = os.open(parts[-1], file_flags, dir_fd=current)
        descriptors.append(file_descriptor)
        opened = os.fstat(file_descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or (size_limit is not None and opened.st_size > size_limit)
            or metadata_tuple(opened) != metadata_tuple(initial)
        ):
            raise UnsafeScriptReferenceSurface
        return descriptors, file_descriptor, opened
    except (OSError, UnsafeScriptReferenceSurface) as error:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass
        raise UnsafeScriptReferenceSurface from error


def read_confined_regular(path: pathlib.Path) -> str:
    """Read at most the immutable per-file and aggregate reference budgets."""

    global total_reference_bytes
    aggregate_remaining = MAX_REFERENCE_TOTAL_BYTES - total_reference_bytes
    if aggregate_remaining < 0:
        raise UnsafeScriptReferenceSurface
    read_limit = min(MAX_REFERENCE_FILE_BYTES, aggregate_remaining)
    descriptors, file_descriptor, opened = open_confined_regular(
        path, size_limit=read_limit
    )
    try:
        if opened.st_size > read_limit:
            raise UnsafeScriptReferenceSurface
        chunks: list[bytes] = []
        remaining = read_limit + 1
        while remaining > 0:
            chunk = os.read(file_descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > read_limit:
            raise UnsafeScriptReferenceSurface
        final = os.fstat(file_descriptor)
        if metadata_tuple(final) != metadata_tuple(opened):
            raise UnsafeScriptReferenceSurface
        total_reference_bytes += len(payload)
        return payload.decode("utf-8", errors="ignore")
    except OSError as error:
        raise UnsafeScriptReferenceSurface from error
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


regular_cache: dict[pathlib.Path, bool] = {}


def confined_regular_exists(path: pathlib.Path) -> bool:
    if path not in regular_cache:
        if len(regular_cache) >= MAX_REFERENCE_UNIQUE_TARGETS:
            raise UnsafeScriptReferenceSurface
        try:
            descriptors, _file_descriptor, _opened = open_confined_regular(path)
        except UnsafeScriptReferenceSurface:
            regular_cache[path] = False
        else:
            regular_cache[path] = True
            for descriptor in reversed(descriptors):
                try:
                    os.close(descriptor)
                except OSError:
                    pass
    return regular_cache[path]


failure_bytes = 0
match_count = 0


def bounded_backward_context(text: str, start: int) -> str:
    """Return one bounded non-whitespace token preceding a reference."""

    context_start = start
    context_chars = 0
    context_bytes = 0
    while context_start > 0:
        character = text[context_start - 1]
        if character.isspace():
            break
        context_chars += 1
        context_bytes += len(character.encode("utf-8", errors="strict"))
        if (
            context_chars > MAX_REFERENCE_CONTEXT_CHARS
            or context_bytes > MAX_REFERENCE_CONTEXT_BYTES
        ):
            raise UnsafeScriptReferenceSurface
        context_start -= 1
    return text[context_start:start]


def record_missing_failure(path: pathlib.Path, ref: str) -> None:
    global failure_bytes
    if len(failures) >= MAX_REFERENCE_FAILURES:
        raise UnsafeScriptReferenceSurface
    path_text = path.as_posix()
    message_prefix = f"{path_text}: missing script reference "
    rendered_bytes = (
        len("FAIL: \n".encode("ascii"))
        + len(message_prefix.encode("utf-8", errors="strict"))
        + len(ref.encode("ascii", errors="strict"))
    )
    if failure_bytes + rendered_bytes > MAX_REFERENCE_FAILURE_BYTES:
        raise UnsafeScriptReferenceSurface
    message = message_prefix + ref
    failures.append(message)
    failure_bytes += rendered_bytes


try:
    for path in files:
        if path == pathlib.Path("scripts/validation/check-repo-contracts.sh"):
            continue
        text = read_confined_regular(path)
        for match in pattern.finditer(text):
            match_count += 1
            if match_count > MAX_REFERENCE_MATCHES:
                raise UnsafeScriptReferenceSurface
            if match.end("ref") - match.start("ref") > MAX_REFERENCE_PATH_BYTES:
                raise UnsafeScriptReferenceSurface
            context = bounded_backward_context(text, match.start("ref"))
            if uri_scheme_boundary.search(context):
                continue
            ref = match.group("ref")
            local_target = path.parent / ref
            root_target = pathlib.Path(ref)
            if confined_regular_exists(local_target) or confined_regular_exists(root_target):
                continue
            if allows_deleted_entrypoint_reference(path, ref):
                continue
            if allows_absence_record_reference(path, ref):
                continue
            record_missing_failure(path, ref)
except (UnicodeError, UnsafeScriptReferenceSurface):
    print("FAIL: unsafe script-reference surface", file=sys.stderr)
    sys.exit(1)

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
    pathlib.Path("scripts/validation/compose-core-readiness.lib.sh"),
    pathlib.Path("scripts/validation/run-compose-core-readiness.sh"),
    pathlib.Path("scripts/validation/check-repo-contracts.sh"),
    pathlib.Path("scripts/validation/check-document-links.py"),
    pathlib.Path("scripts/validation/check-storybook-contract.sh"),
    pathlib.Path("scripts/validation/check-quickwin-baseline.sh"),
    pathlib.Path("scripts/validation/check-template-security-baseline.sh"),
    pathlib.Path("scripts/validation/generate-audit-implementation-matrix.sh"),
    pathlib.Path("scripts/validation/generate-security-automation-readiness.sh"),
    pathlib.Path("scripts/validation/recommend-gap-routing.sh"),
    pathlib.Path("scripts/validation/recommend-qa-gates.sh"),
    pathlib.Path("scripts/validation/report-audit-pack-coverage.sh"),
    pathlib.Path("scripts/validation/report-provider-hook-parity.sh"),
    pathlib.Path("scripts/validation/run-agent-output-eval-fixtures.sh"),
    pathlib.Path("scripts/validation/run-agent-precommit-all-files.sh"),
    pathlib.Path("scripts/validation/run-ci-precommit.sh"),
    pathlib.Path("scripts/validation/run-local-qa-gates.sh"),
    pathlib.Path("scripts/validation/rehearse-postgres-logical-upgrade.sh"),
    pathlib.Path("scripts/security/generate-supply-chain-sample-service-summary.sh"),
    pathlib.Path("scripts/security/seed-grype-db-cache.sh"),
    pathlib.Path("scripts/security/verify-sample-service-supply-chain.sh"),
    pathlib.Path("scripts/hardening/check-all-hardening.sh"),
    pathlib.Path("scripts/hooks/agent-event-hook.sh"),
    pathlib.Path("scripts/hooks/patch-graphify-post-commit.sh"),
    pathlib.Path("scripts/hooks/post-tool-validate.sh"),
    pathlib.Path("scripts/knowledge/generate-llm-wiki.py"),
    pathlib.Path("scripts/knowledge/report-graphify-health.sh"),
    pathlib.Path("scripts/operations/gen-secrets.sh"),
    pathlib.Path("scripts/operations/rehearse-sample-service-delivery.sh"),
    pathlib.Path("scripts/operations/generate-compose-profile-service-coverage.sh"),
    pathlib.Path("scripts/operations/generate-tech-stack-version-provenance.sh"),
    pathlib.Path("scripts/operations/use-qa-ci-tools.sh"),
    pathlib.Path("scripts/operations/sync-provider-surfaces.sh"),
    pathlib.Path("scripts/operations/sync-tech-stack-versions.sh"),
}
implementation_scripts = sorted(
    path
    for folder in ["validation", "hardening", "hooks", "knowledge", "operations", "security"]
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
    "v3.6.8": "Traefik is declared as traefik:v3.7.8",
    "v3.6.12": "Traefik is declared as traefik:v3.7.8",
    "26.5.4": "Keycloak is declared as quay.io/keycloak/keycloak:26.7.0-0",
    "7.14.2": "OAuth2 Proxy Dockerfile uses quay.io/oauth2-proxy/oauth2-proxy:v7.15.3",
    "hashicorp/vault:1.21.4": "Vault is declared as hashicorp/vault:2.0.3",
    "Confluent CP 8.1.1": "Kafka is declared as confluentinc/cp-kafka:8.3.0",
    "RabbitMQ 4.2": "RabbitMQ is declared as rabbitmq:4.3.1-management-alpine",
    "kafbat/kafka-ui:v1.4.2": "Kafbat UI is declared as kafbat/kafka-ui:v1.5.0",
    "v0.20.0": "Ollama is declared as ollama/ollama:0.32.1",
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
    "v10.2.0": "Dozzle is declared as amir20/dozzle:v10.6.11",
    "PostgreSQL (v16+)": "PostgreSQL services are currently PostgreSQL 17/18 family images",
    "InfluxDB 2.x 채택": "InfluxDB 3 Core is the sole current analytics time-series compose",
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
    "26.5.4": "Keycloak current image is quay.io/keycloak/keycloak:26.7.0-0",
    "v26.5.4": "Keycloak current image is quay.io/keycloak/keycloak:26.7.0-0",
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
    "Traefik v3.6.12": "Traefik is declared as traefik:v3.7.8",
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

echo
echo "Repo contract check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: repository Docker/docs contracts are synchronized"
