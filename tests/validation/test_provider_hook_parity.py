from __future__ import annotations

import json
import os
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
    def test_explicit_fixture_root_works_from_non_git_cwd_with_closed_argv(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            command = ["bash", str(SCRIPT), "--validate-only", "--root", str(root)]
            result = subprocess.run(
                command, cwd=root, capture_output=True, text=True, check=False
            )
            self.assertEqual(0, result.returncode, result.stderr)
            for extra in (("--unknown",), ("--root", str(root)), ("--write",)):
                with self.subTest(extra=extra):
                    rejected = subprocess.run(
                        command + list(extra),
                        cwd=root,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(2, rejected.returncode)

    def test_held_script_uses_git_root_without_fixture_override(self) -> None:
        output = (
            ROOT / "docs/90.references/data/0072-provider-hook-parity-matrix/README.md"
        )
        before = output.read_bytes()
        env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        env["PYTHONSAFEPATH"] = "1"
        with SCRIPT.open("rb") as held:
            for path in (str(SCRIPT), f"/proc/self/fd/{held.fileno()}"):
                with self.subTest(path=path):
                    result = subprocess.run(
                        ["bash", path, "--check"],
                        cwd=ROOT,
                        env=env,
                        pass_fds=(held.fileno(),),
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, output.read_bytes())

    def run_validation(self, root: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), "--validate-only", "--root", str(root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_current_dispatchers_wrappers_timeouts_and_events_are_exact(self) -> None:
        self.assertEqual(0, self.run_validation(ROOT).returncode)

    def test_changed_aggregate_is_owned_only_by_completion_dispatch(self) -> None:
        post_tool = (ROOT / "scripts/hooks/post-tool-validate.sh").read_text(
            encoding="utf-8"
        )
        dispatcher = (ROOT / "scripts/hooks/agent-event-hook.sh").read_text(
            encoding="utf-8"
        )
        invocation = "python3 scripts/validation/run-ci-gate.py --profile changed"

        self.assertNotIn(invocation, post_tool)
        self.assertIn("changed_profile_stop_gate", dispatcher)
        self.assertIn(f'output="$({invocation} 2>&1)"', dispatcher)

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

    def test_executable_mode_and_registry_binding_mutations_fail_closed(self) -> None:
        for case in ("mode", "duplicate-event", "missing-contract"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                registry_path = (
                    root / "docs/00.agent-governance/providers/registry.yaml"
                )
                registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
                if case == "mode":
                    executable = (
                        root / registry["hook_contracts"]["codex"]["Stop"]["executable"]
                    )
                    executable.chmod(0o644)
                elif case == "duplicate-event":
                    registry["semantic_events"]["codex"].append("Stop")
                    registry_path.write_text(
                        yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
                    )
                else:
                    registry["hook_contracts"]["codex"].pop("Stop")
                    registry_path.write_text(
                        yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
                    )
                self.assertNotEqual(0, self.run_validation(root).returncode)

    def test_synchronized_command_prefix_mutation_fails_immutable_template(
        self,
    ) -> None:
        for provider, event in (("claude", "PostToolUse"), ("codex", "Stop")):
            with (
                self.subTest(provider=provider),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                copy_fixture(root)
                registry_path = (
                    root / "docs/00.agent-governance/providers/registry.yaml"
                )
                registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
                command = registry["hook_contracts"][provider][event]["command"]
                mutated = f"true; {command}"
                registry["hook_contracts"][provider][event]["command"] = mutated
                registry_path.write_text(
                    yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
                )
                native_path = root / (
                    ".claude/settings.json"
                    if provider == "claude"
                    else ".codex/hooks.json"
                )
                native = json.loads(native_path.read_text(encoding="utf-8"))
                native["hooks"][event][0]["hooks"][0]["command"] = mutated
                native_path.write_text(json.dumps(native), encoding="utf-8")
                self.assertNotEqual(0, self.run_validation(root).returncode)

    def test_synchronized_unsafe_event_name_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            unsafe = "Stop;echo"
            registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["semantic_events"]["codex"] = [
                unsafe if event == "Stop" else event
                for event in registry["semantic_events"]["codex"]
            ]
            registry["hook_contracts"]["codex"] = {
                (unsafe if event == "Stop" else event): (
                    {
                        **binding,
                        "command": binding["command"].removesuffix(" Stop")
                        + f" {unsafe}",
                    }
                    if event == "Stop"
                    else binding
                )
                for event, binding in registry["hook_contracts"]["codex"].items()
            }
            registry_path.write_text(
                yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
            )

            native_path = root / ".codex/hooks.json"
            native = json.loads(native_path.read_text(encoding="utf-8"))
            native["hooks"][unsafe] = native["hooks"].pop("Stop")
            native["hooks"][unsafe][0]["hooks"][0]["command"] = registry[
                "hook_contracts"
            ]["codex"][unsafe]["command"]
            native_path.write_text(json.dumps(native), encoding="utf-8")

            self.assertNotEqual(0, self.run_validation(root).returncode)

    def test_synchronized_unsafe_executable_path_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            binding = registry["hook_contracts"]["codex"]["Stop"]
            original = binding["executable"]
            unsafe = "scripts/hooks/$(id).sh"
            target = root / unsafe
            shutil.copy2(root / original, target)
            binding["executable"] = unsafe
            binding["command"] = binding["command"].replace(original, unsafe)
            registry_path.write_text(
                yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
            )

            native_path = root / ".codex/hooks.json"
            native = json.loads(native_path.read_text(encoding="utf-8"))
            native["hooks"]["Stop"][0]["hooks"][0]["command"] = binding["command"]
            native_path.write_text(json.dumps(native), encoding="utf-8")

            self.assertNotEqual(0, self.run_validation(root).returncode)

    def test_parity_scope_excludes_neutral_workflow_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry.update(
                {
                    "workflow_states": "not-provider-parity-data",
                    "harness_layers": "not-provider-parity-data",
                    "harness_loops": "not-provider-parity-data",
                }
            )
            registry_path.write_text(
                yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
            )
            self.assertEqual(0, self.run_validation(root).returncode)


if __name__ == "__main__":
    unittest.main()
