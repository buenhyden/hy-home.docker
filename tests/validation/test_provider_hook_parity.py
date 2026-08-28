from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/report-provider-hook-parity.sh"


def copy_fixture(root: pathlib.Path) -> None:
    for source in (
        "docs/00.agent-governance/providers/registry.yaml",
        ".claude/settings.json",
        ".codex/hooks.json",
    ):
        target = root / source
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / source, target)
    shutil.copytree(
        ROOT / "docs/00.agent-governance/roles",
        root / "docs/00.agent-governance/roles",
    )
    registry = yaml.safe_load(
        (root / "docs/00.agent-governance/providers/registry.yaml").read_text(
            encoding="utf-8"
        )
    )
    for contracts in registry["hook_contracts"].values():
        for contract in contracts.values():
            source = ROOT / contract["executable"]
            target = root / contract["executable"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


class ProviderHookParityTests(unittest.TestCase):
    def run_validation(self, root: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), "--validate-only", "--root", str(root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_current_dispatchers_wrappers_timeouts_events_and_loops_are_exact(self) -> None:
        self.assertEqual(0, self.run_validation(ROOT).returncode)

    def test_generated_data_is_fresh(self) -> None:
        result = subprocess.run(
            ["bash", str(SCRIPT), "--check", "--root", str(ROOT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_command_timeout_and_event_mutations_fail_closed(self) -> None:
        for case in ("command", "timeout", "event"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                path = root / ".codex/hooks.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                if case == "event":
                    data["hooks"].pop("PreCompact")
                else:
                    hook = data["hooks"]["Stop"][0]["hooks"][0]
                    hook[case] = "false" if case == "command" else 999
                path.write_text(json.dumps(data), encoding="utf-8")
                self.assertNotEqual(0, self.run_validation(root).returncode)

    def test_executable_mode_and_loop_contract_mutations_fail_closed(self) -> None:
        for case in ("mode", "loop-field", "workflow-state"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
                registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
                if case == "mode":
                    executable = root / registry["hook_contracts"]["codex"]["Stop"][
                        "executable"
                    ]
                    executable.chmod(0o644)
                elif case == "loop-field":
                    registry["harness_loops"]["bounded-implementation"].pop(
                        "max_attempts"
                    )
                    registry_path.write_text(
                        yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
                    )
                else:
                    registry["workflow_states"][0]["state_id"] = "invented"
                    registry_path.write_text(
                        yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
                    )
                self.assertNotEqual(0, self.run_validation(root).returncode)

    def test_synchronized_command_prefix_mutation_fails_immutable_template(self) -> None:
        for provider, event in (("claude", "PostToolUse"), ("codex", "Stop")):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
                registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
                command = registry["hook_contracts"][provider][event]["command"]
                mutated = f"true; {command}"
                registry["hook_contracts"][provider][event]["command"] = mutated
                registry_path.write_text(
                    yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
                )
                native_path = root / (
                    ".claude/settings.json" if provider == "claude" else ".codex/hooks.json"
                )
                native = json.loads(native_path.read_text(encoding="utf-8"))
                native["hooks"][event][0]["hooks"][0]["command"] = mutated
                native_path.write_text(json.dumps(native), encoding="utf-8")
                self.assertNotEqual(0, self.run_validation(root).returncode)

    def test_parity_rejects_corrupt_loop_state_and_harness_values(self) -> None:
        mutations = {
            "loop-owner": lambda data: data["harness_loops"]["context-bootstrap"].update(
                {"owner_agent": "not-a-role"}
            ),
            "loop-stop": lambda data: data["harness_loops"]["context-bootstrap"].update(
                {"stop_condition": ""}
            ),
            "state-owner": lambda data: data["workflow_states"][0].update(
                {"owner_agent": "not-a-role"}
            ),
            "state-return": lambda data: data["workflow_states"][0].update(
                {"failure_return": "invented-state"}
            ),
            "layer-gate": lambda data: data["harness_layers"][0].update({"gate": ""}),
            "layer-return": lambda data: data["harness_layers"][0].update(
                {"failure_return": "invented-state"}
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
                registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
                mutation(registry)
                registry_path.write_text(
                    yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
                )
                self.assertNotEqual(0, self.run_validation(root).returncode)


if __name__ == "__main__":
    unittest.main()
