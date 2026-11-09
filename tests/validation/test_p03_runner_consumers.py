"""Public n8n Code-node consumers covered by the P03 runner policy."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKLOADS = ROOT / "infra/07-workflow/n8n/workloads"
CODE_TYPE = "n8n-nodes-base.code"


def contains_environment_reference(value: object) -> bool:
    if isinstance(value, str):
        return bool(re.search(r"\$env\b|process\.env\b", value))
    if isinstance(value, list):
        return any(contains_environment_reference(item) for item in value)
    if isinstance(value, dict):
        return any(contains_environment_reference(item) for item in value.values())
    return False


def public_workflows_and_code_nodes() -> tuple[list[tuple[Path, dict]], list[Path]]:
    code_nodes = []
    workflows = []
    for path in sorted(WORKLOADS.rglob("*.json")):
        source = path.read_text(encoding="utf-8")
        if '"nodes"' not in source:
            continue
        value = json.loads(source)
        if not isinstance(value, dict) or not isinstance(value.get("nodes"), list):
            continue
        workflows.append(path)
        if contains_environment_reference(value):
            raise AssertionError(f"public workflow uses environment expression: {path}")
        for node in value.get("nodes", []):
            if isinstance(node, dict) and node.get("type") == CODE_TYPE:
                code_nodes.append((path, node))
    return code_nodes, workflows


class P03RunnerConsumerTests(unittest.TestCase):
    def test_every_public_code_node_uses_no_environment_or_module_import(self):
        rows, workflows = public_workflows_and_code_nodes()
        self.assertGreater(len(workflows), 0, "no public workflow was reviewed")
        self.assertGreater(len(rows), 0, "no public Code-node consumer was reviewed")
        reviewed_paths = {path.relative_to(ROOT).as_posix() for path, _ in rows}
        self.assertEqual(
            {
                "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/workflow.json",
                "infra/07-workflow/n8n/workloads/manifest-outbox-notifier/"
                "workflows/manifest-outbox-mailpit.json",
                "infra/07-workflow/n8n/workloads/task-runner-warmup/workflow.json",
            },
            reviewed_paths,
        )
        for path, node in rows:
            parameters = node.get("parameters")
            self.assertIsInstance(parameters, dict, path)
            code = parameters.get("jsCode", parameters.get("pythonCode", ""))
            self.assertIsInstance(code, str, path)
            self.assertNotRegex(code, r"\$env\b|process\.env\b|\brequire\s*\(", path)
            self.assertIsNone(
                re.search(r"(?m)^\s*(?:from\s+\S+\s+import|import\s+\S+)", code),
                path,
            )

    def test_environment_reference_scan_covers_non_code_expressions(self):
        self.assertTrue(
            contains_environment_reference(
                {"nodes": [{"type": "set", "parameters": {"value": "={{$env.KEY}}"}}]}
            )
        )
        self.assertFalse(
            contains_environment_reference(
                {"nodes": [{"type": "set", "parameters": {"value": "literal"}}]}
            )
        )


if __name__ == "__main__":
    unittest.main()
