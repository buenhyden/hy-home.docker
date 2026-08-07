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
    for literal in ["frontend-quality:", "storybook-coverage:"]:
        if literal not in text:
            failures.append(f"{workflow_path}: missing Storybook coverage workflow job: {literal}")

# The npm invocations moved out of inline workflow shell into typed gate argv
# declarations executed through scripts/validation/ci_gate_adapters.py. Assert
# the declarations, not the retired inline literals.
contract_path = pathlib.Path(".github/workflow-contract.yml")
required_gate_argv = {
    "leaf.frontend-lint": ["run-npm", "run", "lint", "--prefix", "projects/storybook/nextjs"],
    "leaf.frontend-typecheck": ["run-npm", "run", "typecheck", "--prefix", "projects/storybook/nextjs"],
    "leaf.frontend-build": ["run-npm", "run", "build", "--prefix", "projects/storybook/nextjs"],
    "leaf.frontend-quality": ["run-npm", "run", "build-storybook", "--prefix", "projects/storybook/nextjs"],
    "leaf.storybook-coverage": ["run-npm", "run", "coverage", "--prefix", "projects/storybook/nextjs"],
    "setup.storybook-node-dependencies": ["run-npm", "ci", "--prefix", "projects/storybook/nextjs"],
}

if not contract_path.is_file():
    failures.append(f"missing workflow contract: {contract_path}")
else:
    contract_text = contract_path.read_text(errors="ignore")
    try:
        contract = json.loads(contract_text)
    except json.JSONDecodeError:
        try:
            import yaml
        except Exception as exc:  # pragma: no cover - dependency guard
            contract = None
            failures.append(f"{contract_path}: PyYAML is required to parse the workflow contract: {exc}")
        else:
            contract = yaml.safe_load(contract_text)

    def iter_gates(node):
        if isinstance(node, dict):
            if "gate_id" in node:
                yield node
            for value in node.values():
                yield from iter_gates(value)
        elif isinstance(node, list):
            for value in node:
                yield from iter_gates(value)

    if contract is not None:
        declared = {gate["gate_id"]: list(gate.get("argv") or []) for gate in iter_gates(contract)}
        for gate_id, expected_argv in sorted(required_gate_argv.items()):
            if gate_id not in declared:
                failures.append(f"{contract_path}: missing Storybook coverage gate: {gate_id}")
            elif declared[gate_id] != expected_argv:
                failures.append(
                    f"{contract_path}: gate {gate_id} argv mismatch: "
                    f"expected {expected_argv}, found {declared[gate_id]}"
                )

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
