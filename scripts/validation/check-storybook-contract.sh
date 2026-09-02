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

root = pathlib.Path.cwd()
sys.path.insert(0, str(root))
from scripts.lib.document_governance.suite_registry import SuiteRegistryError, load as load_suites
from scripts.lib.gate.ci_gate_contract import load_contract_document, parse_public_gate_contract
from scripts.lib.gate.github_workflow_contract import (
    GateContractError, WorkflowContractError, expand_gate_ids,
    load_workflow_contract, validate_workflows,
)

failures: list[str] = []
package_path = pathlib.Path("projects/storybook/nextjs/package.json")
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

# The npm invocations moved out of inline workflow shell into typed gate argv
# declarations executed through scripts/lib/gate/ci_gate_adapters.py. Assert
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

try:
    contract = load_workflow_contract(root)
    failures.extend(
        f"{finding.path}: {finding.code}: {finding.message}"
        for finding in validate_workflows(root, contract)
    )
    public = parse_public_gate_contract(
        load_contract_document(root), load_suites(root / "scripts/manifest.yaml")
    )
    roots = next(route.root_gate_ids for route in public.suites if route.name == "repository-integrity")
    reachable: set[str] = set()
    for gate in ("ci.frontend-quality", "ci.storybook-coverage"):
        if gate not in roots:
            failures.append(f"{contract_path}: full public profile omits {gate}")
        reachable.update(expand_gate_ids(contract.gate_registry, "ci", gate, False))
    declared = {node.gate_id: list(node.argv) for node in contract.gate_registry.nodes}
    for gate_id, expected_argv in sorted(required_gate_argv.items()):
        if gate_id not in reachable:
            failures.append(f"{contract_path}: unreachable Storybook coverage gate: {gate_id}")
        elif declared[gate_id] != expected_argv:
            failures.append(
                f"{contract_path}: gate {gate_id} argv mismatch: "
                f"expected {expected_argv}, found {declared[gate_id]}"
            )
except (GateContractError, WorkflowContractError, SuiteRegistryError) as error:
    failures.append(f"{contract_path}: {error}")

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
