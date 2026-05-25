#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

python3 - <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

failures: list[str] = []
package_path = pathlib.Path("projects/storybook/nextjs/package.json")
workflow_path = pathlib.Path(".github/workflows/ci-quality.yml")
vitest_config_path = pathlib.Path("projects/storybook/nextjs/vitest.config.ts")

if not package_path.is_file():
    failures.append(f"missing package file: {package_path}")
else:
    data = json.loads(package_path.read_text())
    scripts = data.get("scripts", {})
    for name in ["test", "coverage"]:
        value = scripts.get(name)
        if not value or "vitest run --project storybook" not in value:
            failures.append(f"{package_path}: script {name!r} must run the Storybook Vitest project")
    if "--coverage" not in str(scripts.get("coverage", "")):
        failures.append(f"{package_path}: coverage script must enable coverage")
    if scripts.get("typecheck") != "tsc --noEmit":
        failures.append(f"{package_path}: script 'typecheck' must run TypeScript without emitting files")

if not workflow_path.is_file():
    failures.append(f"missing workflow file: {workflow_path}")
else:
    text = workflow_path.read_text(errors="ignore")
    for literal in [
        "frontend-quality:",
        "npm run lint --prefix projects/storybook/nextjs",
        "npm run typecheck --prefix projects/storybook/nextjs",
        "npm run build --prefix projects/storybook/nextjs",
        "npm run build-storybook --prefix projects/storybook/nextjs",
        "storybook-coverage:",
        "npm ci --prefix projects/storybook/nextjs",
        "npm run coverage --prefix projects/storybook/nextjs",
    ]:
        if literal not in text:
            failures.append(f"{workflow_path}: missing Storybook coverage workflow literal: {literal}")

if not vitest_config_path.is_file():
    failures.append(f"missing Vitest config: {vitest_config_path}")
else:
    text = vitest_config_path.read_text(errors="ignore")
    for metric in ["statements", "branches", "functions", "lines"]:
        if not re.search(rf"\b{metric}\s*:\s*90\b", text):
            failures.append(f"{vitest_config_path}: missing 90% coverage threshold for {metric}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
