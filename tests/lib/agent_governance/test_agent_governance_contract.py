from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[3]
MODULE = ROOT / "scripts/lib/agent_governance/agent_governance_contract.py"


def load_contract_module():
    spec = importlib.util.spec_from_file_location("agent_governance_contract", MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {MODULE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


contract = load_contract_module()


def copy_governance_fixture(root: pathlib.Path) -> None:
    from tests.validation.test_provider_surface_renderer import (
        _copy_registered_file,
        copy_fixture,
    )

    copy_fixture(root)
    for path in (
        "docs/99.templates/registry.json",
        "AGENTS.md",
        "CLAUDE.md",
        "_workspace/README.md",
        "_workspace/repo-support/README.md",
    ):
        _copy_registered_file(ROOT, root, path)


class AgentGovernanceContractTests(unittest.TestCase):
    def test_read_only_canonical_directory_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            canonical = root / ".agents"
            canonical.chmod(0o555)
            self.assertEqual([], contract.validate_canonical_agent_home(root))
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "providers"
            )
            self.assertFalse(
                any(item.path.startswith(".agents") for item in findings), findings
            )

    def test_provider_registry_does_not_restate_neutral_workflow_policy(self) -> None:
        registry = yaml.safe_load(
            (ROOT / ".agents/governance/providers/registry.yaml").read_text()
        )
        neutral_keys = {
            "workflow_states",
            "harness_layers",
            "harness_loops",
            "evidence_fields",
            "prohibited_evidence",
        }
        self.assertEqual(set(), neutral_keys & set(registry))

    def test_unsafe_canonical_home_is_rejected_and_preserved(self) -> None:
        for kind in (
            "missing",
            "empty",
            "unknown",
            "file",
            "symlink",
            "broken-symlink",
            "fifo",
        ):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                home = root / ".agents"
                if kind in {"empty", "unknown"}:
                    home.mkdir()
                    if kind == "unknown":
                        (home / "unowned.md").write_text("user-owned content\n")
                elif kind == "file":
                    home.write_text("user-owned content\n")
                elif kind == "fifo":
                    os.mkfifo(home)
                elif kind in {"symlink", "broken-symlink"}:
                    outside = root / "outside"
                    if kind == "symlink":
                        outside.mkdir()
                    home.symlink_to(outside, target_is_directory=True)
                findings = contract.validate_canonical_agent_home(root)
                self.assertEqual(
                    ["AGC-CANONICAL-HOME"], [item.code for item in findings]
                )
                self.assertEqual(kind != "missing", os.path.lexists(home))
                if kind == "unknown":
                    self.assertEqual(
                        "user-owned content\n", (home / "unowned.md").read_text()
                    )

    def test_canonical_directory_enumeration_failure_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / ".agents").mkdir()
            with mock.patch.object(contract.os, "scandir", side_effect=PermissionError):
                findings = contract.validate_canonical_agent_home(root)
            self.assertEqual(["AGC-CANONICAL-HOME"], [item.code for item in findings])
            self.assertTrue((root / ".agents").is_dir())

    def test_skill_envelope_and_invocation_controls_are_closed(self) -> None:
        mutations = {
            "name-mismatch": lambda data: data.update(name="other"),
            "description-missing": lambda data: data.pop("description"),
            "description-blank": lambda data: data.update(description="  "),
            "legacy-top-level": lambda data: data.update(scope="common"),
            "tool-grant": lambda data: data.update({"allowed-tools": "Bash"}),
            "metadata-shape": lambda data: data.update(metadata=[]),
            "id-mismatch": lambda data: data["metadata"].update(function_id="other"),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                source = root / ".agents/skills/adr-writing/SKILL.md"
                _, raw, body = source.read_text().split("---", 2)
                data = yaml.safe_load(raw)
                mutation(data)
                source.write_text(
                    "---\n" + yaml.safe_dump(data, sort_keys=False) + "---" + body
                )
                with self.assertRaises(contract.ContractLoadError):
                    contract.load_agent_governance(root)
        for controls in (
            {"policy": {"allow_implicit_invocation": True}},
            {"policy": {"allow_implicit_invocation": 0}},
            {"policy": {"allow_implicit_invocation": False, "unknown": False}},
            {
                "policy": {"allow_implicit_invocation": False},
                "dependencies": {"tools": []},
            },
        ):
            with (
                self.subTest(controls=controls),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                source = root / ".agents/skills/adr-writing/agents/openai.yaml"
                source.write_text(yaml.safe_dump(controls))
                with self.assertRaises(contract.ContractLoadError):
                    contract.load_agent_governance(root)

    def test_plausible_unregistered_policy_is_rejected_without_reading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            bundle = contract.load_contract_bundle(root)
            private = root / ".agents/governance/private.md"
            private.write_bytes(b"synthetic private input")
            with mock.patch.object(
                contract, "_read_text", wraps=contract._read_text
            ) as read:
                findings = contract.validate_repository(root, bundle, "harness")
                with self.assertRaisesRegex(
                    contract.ContractLoadError, "CANONICAL-HOME"
                ):
                    contract.load_contract_bundle(root)
            self.assertIn("AGC-CANONICAL-HOME", {item.code for item in findings})
            self.assertNotIn(
                ".agents/governance/private.md",
                {str(call.args[1]) for call in read.call_args_list},
            )
            self.assertEqual(b"synthetic private input", private.read_bytes())

    def test_registered_inventory_can_be_read_without_other_payloads(self) -> None:
        from tests.validation.test_provider_surface_renderer import (
            _copy_registered_file,
        )

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            _copy_registered_file(
                ROOT, root, ".agents/governance/providers/registry.yaml"
            )
            sources = contract.canonical_source_paths(root)
            declared = yaml.safe_load(
                (root / ".agents/governance/providers/registry.yaml").read_text(
                    encoding="utf-8"
                )
            )["canonical_sources"]
            # The whole declared inventory is returned, in order and without
            # duplicates. A pinned count would only record how many sources
            # existed when the test was written.
            self.assertEqual([str(source) for source in sources], declared)
            self.assertIn(
                pathlib.PurePosixPath(".agents/skills/adr-writing/SKILL.md"), sources
            )
            self.assertFalse((root / ".agents/skills").exists())

    def test_canonical_child_boundaries_preserve_unknown_inputs(self) -> None:
        for kind in ("unknown", "symlink", "fifo"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                source = root / ".agents/skills/adr-writing/SKILL.md"
                if kind == "unknown":
                    source = source.parent / "unknown.txt"
                    source.write_bytes(b"user-owned")
                else:
                    source.unlink()
                    if kind == "fifo":
                        os.mkfifo(source)
                    else:
                        outside = root / "outside"
                        outside.write_bytes(b"user-owned")
                        source.symlink_to(outside)
                with self.assertRaisesRegex(
                    contract.ContractLoadError, "CANONICAL-HOME"
                ):
                    contract.load_agent_governance(root)
                self.assertTrue(os.path.lexists(source))
                if kind == "unknown":
                    self.assertEqual(b"user-owned", source.read_bytes())

    def test_read_only_review_roles_remain_read_only(self) -> None:
        state = contract.load_agent_governance(ROOT)
        permissions = {role.agent_id: role.permission_profile for role in state.roles}
        for role_id in (
            "workflow-supervisor",
            "eval-engineer",
            "rules-engineer",
            "code-reviewer",
        ):
            self.assertEqual("read-only", permissions[role_id])

    def test_knowledge_and_prompt_profiles_are_registered(self) -> None:
        """Stage 99 owns the document shape of every canonical category."""
        registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        profiles = {profile["id"]: profile for profile in registry["profiles"]}
        expected = {
            "governance-knowledge": ".agents/knowledge/{slug}.md",
            "governance-knowledge-index": ".agents/knowledge/README.md",
            "governance-prompt": ".agents/prompts/{slug}.md",
            "governance-prompt-index": ".agents/prompts/README.md",
        }
        for profile_id, path_pattern in sorted(expected.items()):
            with self.subTest(profile=profile_id):
                self.assertIn(profile_id, profiles)
                profile = profiles[profile_id]
                self.assertEqual(path_pattern, profile["path_pattern"])
                self.assertEqual("living", profile["lifecycle_id"])
                self.assertEqual("living", registry["transitions"][profile_id])
                # A canonical category routes and declares; it never carries a
                # traceable artifact identity of its own.
                self.assertIsNone(profile["artifact_id_pattern"])
                self.assertEqual("none", profile["identity_relation"])
        for role in ("governance/knowledge", "governance/prompt"):
            with self.subTest(template_role=role):
                source = registry["template_roles"][role]["source"]
                self.assertTrue((ROOT / source).is_file())

    def test_canonical_category_roots_are_admitted_and_populated(self) -> None:
        """Each new canonical root is admitted, registered, and non-empty."""
        for directory in (".agents/knowledge", ".agents/prompts"):
            with self.subTest(directory=directory):
                root = ROOT / directory
                self.assertTrue(root.is_dir())
                self.assertIn("README.md", {path.name for path in root.glob("*.md")})
        # The contract requires an exact bijection between the files on disk
        # under the canonical home and the registered source inventory, so a
        # member that is not declared fails the home scan rather than passing
        # quietly.
        declared = set(
            yaml.safe_load(
                (ROOT / ".agents/governance/providers/registry.yaml").read_text(
                    encoding="utf-8"
                )
            )["canonical_sources"]
        )
        for directory in (".agents/knowledge", ".agents/prompts"):
            for path in sorted((ROOT / directory).glob("*.md")):
                with self.subTest(path=f"{directory}/{path.name}"):
                    self.assertIn(f"{directory}/{path.name}", declared)
        self.assertLessEqual(
            {
                "governance-knowledge",
                "governance-knowledge-index",
                "governance-prompt",
                "governance-prompt-index",
            },
            contract.GOVERNANCE_PROFILES,
        )

    def test_supported_providers_and_governance_roots_are_exact(self) -> None:
        state = contract.load_agent_governance(ROOT)
        self.assertEqual(("claude", "codex"), state.providers)
        self.assertEqual(
            ("README.md", "governance", "knowledge", "prompts", "roles", "skills"),
            state.root_entries,
        )
        self.assertEqual(
            ("README.md", "registry.yaml"),
            state.provider_entries,
        )
        self.assertEqual(
            {path.stem for path in (ROOT / ".agents/roles").glob("*.md")},
            {role.agent_id for role in state.roles},
        )
        self.assertEqual(
            {path.parent.name for path in (ROOT / ".agents/skills").glob("*/SKILL.md")},
            {skill.skill_id for skill in state.skills},
        )
        self.assertFalse((ROOT / ".agents/memory").exists())
        retired_provider = "ge" + "mini"
        self.assertFalse((ROOT / ("." + retired_provider)).exists())
        self.assertFalse((ROOT / (retired_provider.upper() + ".md")).exists())

    def test_contract_and_repository_are_clean(self) -> None:
        bundle = contract.load_contract_bundle(ROOT)
        self.assertEqual([], contract.validate_contract_bundle(ROOT, bundle))
        self.assertEqual([], contract.validate_repository(ROOT, bundle, "all"))

    def test_retired_experiment_token_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            policy = root / ".agents/governance/agentic.md"
            retired_experiment = "Anti" + "gravity"
            policy.write_text(policy.read_text() + f"\n{retired_experiment} adapter\n")
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "harness"
            )
            self.assertIn("AGC-UNSUPPORTED-TOKEN", {item.code for item in findings})

    def test_generated_surface_cannot_own_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            generated = root / ".claude/agents/code-reviewer.md"
            generated.write_text(
                generated.read_text()
                + "\nThis generated file is the policy source of truth.\n"
            )
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "harness"
            )
            self.assertIn("AGC-GENERATED-AUTHORITY", {item.code for item in findings})

    def test_orphan_native_skill_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            orphan = root / ".claude/skills/orphan/SKILL.md"
            orphan.parent.mkdir(parents=True)
            orphan.write_text("# orphan\n")
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "catalog"
            )
            self.assertIn("AGC-SKILL-PROJECTION", {item.code for item in findings})

    def test_bootstrap_reference_to_removed_handoff_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            shim = root / "AGENTS.md"
            retired_handoff = "memory" + "/current.md"
            shim.write_text(shim.read_text() + f"\nLoad {retired_handoff}.\n")
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "harness"
            )
            self.assertIn("AGC-UNSUPPORTED-TOKEN", {item.code for item in findings})

    def test_repository_path_helpers_remain_compatible(self) -> None:
        self.assertEqual(
            ".claude/agents/code-reviewer.md",
            contract.normalize_repo_relative_path("./.claude/agents/code-reviewer.md"),
        )
        self.assertTrue(
            contract.path_matches_artifact_pattern(
                "docs/01.requirements/0001-example.md",
                "docs/01.requirements/{0001..0025}-*.md",
            )
        )

    def test_provider_registry_is_strict_typed_and_cross_referenced(self) -> None:
        state = contract.load_agent_governance(ROOT)
        self.assertEqual(
            ("claude", "codex"),
            tuple(item.provider_id for item in state.provider_records),
        )
        self.assertEqual(
            ".claude/agents/{agent_id}.md", state.provider_records[0].agent_pattern
        )

        def inject_unsafe_event(data) -> None:
            unsafe = "Stop;echo"
            data["semantic_events"]["codex"] = [
                unsafe if event == "Stop" else event
                for event in data["semantic_events"]["codex"]
            ]
            data["hook_contracts"]["codex"] = {
                (unsafe if event == "Stop" else event): (
                    {
                        **binding,
                        "command": binding["command"].removesuffix(" Stop")
                        + f" {unsafe}",
                    }
                    if event == "Stop"
                    else binding
                )
                for event, binding in data["hook_contracts"]["codex"].items()
            }

        def make_codex_effort_unsupported(data) -> None:
            model = data["models"]["gpt-5.6-sol"]
            model["control"] = "unsupported"
            model.pop("supported_values")
            for profile in data["work_profiles"].values():
                selection = profile["codex"]
                if selection["model"] == "gpt-5.6-sol":
                    selection["control"] = "effort"
                    selection["value"] = None

        mutations = {
            "top-level-key": lambda data: data.update({"unknown": True}),
            "provider-key": lambda data: data["providers"][0].update({"unknown": True}),
            "adapter-cross-reference": lambda data: data["providers"][0].update(
                {"adapter_path": ".codex/provider.md"}
            ),
            "unsafe-projection": lambda data: data["providers"][0].update(
                {"native_agent_pattern": "../outside/{agent_id}.md"}
            ),
            "status": lambda data: data["providers"][0].update(
                {"capability_status": "unknown"}
            ),
            "permission-provider": lambda data: data["permissions"]["read-only"].update(
                {"other": "read-only"}
            ),
            "model-provider": lambda data: data["models"]["gpt-5.6-sol"].update(
                {"provider": "claude"}
            ),
            "codex-null-effort": make_codex_effort_unsupported,
            "unsafe-event": inject_unsafe_event,
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                path = root / ".agents/governance/providers/registry.yaml"
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutation(data)
                path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                with self.assertRaises(contract.ContractLoadError):
                    contract.load_agent_governance(root)

    def test_hook_executable_rejects_shell_metacharacters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            registry_path = root / ".agents/governance/providers/registry.yaml"
            data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            binding = data["hook_contracts"]["codex"]["Stop"]
            original = binding["executable"]
            unsafe = "scripts/hooks/$(id).sh"
            target = root / unsafe
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / original, target)
            binding["executable"] = unsafe
            binding["command"] = binding["command"].replace(original, unsafe)
            registry_path.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )

            with self.assertRaises(contract.ContractLoadError):
                contract.load_agent_governance(root)

    def test_canonical_role_and_skill_identifiers_are_safe_slugs(self) -> None:
        cases = {
            "role-id": (
                ".agents/roles/code-reviewer.md",
                ".agents/roles/evil: true.md",
                'agent_id: "code-reviewer"',
                'agent_id: "evil: true"',
            ),
            "skill-id": (
                ".agents/skills/code-review-dimensions/SKILL.md",
                ".agents/skills/evil: true/SKILL.md",
                'function_id: "code-review-dimensions"',
                'function_id: "evil: true"',
            ),
            "owner-id": (
                ".agents/skills/code-review-dimensions/SKILL.md",
                ".agents/skills/code-review-dimensions/SKILL.md",
                'owner_agent: "code-reviewer"',
                'owner_agent: "evil: true"',
            ),
            "skill-reference": (
                ".agents/roles/code-reviewer.md",
                ".agents/roles/code-reviewer.md",
                '- "code-review-dimensions"',
                '- "evil: true"',
            ),
        }
        for name, (source_name, target_name, before, after) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                source = root / source_name
                target = root / target_name
                original = source.read_text(encoding="utf-8")
                text = original.replace(before, after, 1)
                self.assertNotEqual(original, text)
                if target != source:
                    source.unlink()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")

                with self.assertRaises(contract.ContractLoadError):
                    contract.load_agent_governance(root)

    def test_workspace_active_scan_does_not_read_ignored_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            private = root / "_workspace/repo-support/private-state.json"
            private.parent.mkdir(parents=True, exist_ok=True)
            private.write_bytes(b"private synthetic scratch state")
            bundle = contract.load_contract_bundle(root)
            with mock.patch.object(
                contract, "_read_text", wraps=contract._read_text
            ) as read:
                contract.validate_repository(root, bundle, "harness")
            self.assertNotIn(
                "_workspace/repo-support/private-state.json",
                {str(call.args[1]) for call in read.call_args_list},
            )
            self.assertEqual(b"private synthetic scratch state", private.read_bytes())

    def test_adopted_output_style_is_current_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            settings = json.loads((root / ".claude/settings.json").read_text())
            self.assertEqual("hy-home", settings["outputStyle"])
            relative = ".claude/output-styles/hy-home.md"
            style = root / relative
            style.write_text(
                style.read_text()
                + "\nLoad docs/00.agent-governance/policies/bootstrap.md.\n"
            )
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "harness"
            )
            self.assertIn(
                relative,
                {
                    item.path
                    for item in findings
                    if item.code == "AGC-UNSUPPORTED-TOKEN"
                },
            )

    def test_unregistered_output_style_is_preserved_without_reading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            relative = ".claude/output-styles/private-local.md"
            private = root / relative
            private.write_bytes(b"private synthetic style input")
            bundle = contract.load_contract_bundle(root)
            with mock.patch.object(
                contract, "_read_text", wraps=contract._read_text
            ) as read:
                contract.validate_repository(root, bundle, "harness")
            self.assertNotIn(
                relative, {str(call.args[1]) for call in read.call_args_list}
            )
            self.assertEqual(b"private synthetic style input", private.read_bytes())

    def test_native_active_scan_does_not_read_local_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            private = root / ".claude/settings.local.json"
            private.write_bytes(b"private fixture payload")
            bundle = contract.load_contract_bundle(root)
            with mock.patch.object(
                contract, "_read_text", wraps=contract._read_text
            ) as read:
                contract.validate_repository(root, bundle, "harness")
            self.assertNotIn(
                ".claude/settings.local.json",
                {str(call.args[1]) for call in read.call_args_list},
            )
            self.assertEqual(b"private fixture payload", private.read_bytes())

    def test_active_text_scan_fails_closed_on_invalid_inputs(self) -> None:
        cases = ("invalid-utf8", "unreadable", "symlink", "fifo")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                target = root / "docs/99.templates" / f"active-{case}.yaml"
                target.parent.mkdir(parents=True, exist_ok=True)
                if case == "invalid-utf8":
                    target.write_bytes(b"\xff\xfe")
                elif case == "unreadable":
                    target.write_text("active but unreadable\n", encoding="utf-8")
                    target.chmod(0)
                elif case == "symlink":
                    outside = root / "outside.txt"
                    outside.write_text("retired provider token\n")
                    target.symlink_to(outside)
                else:
                    os.mkfifo(target)
                findings = contract.validate_repository(
                    root, contract.load_contract_bundle(root), "harness"
                )
                self.assertIn(
                    "AGC-ACTIVE-TEXT-UNSAFE", {item.code for item in findings}
                )

    def test_all_registered_active_roots_reject_retired_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            (root / "README.md").write_text(
                "Load docs/00.agent-governance/contracts/legacy.yaml.\n",
                encoding="utf-8",
            )
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "harness"
            )
            self.assertIn("AGC-UNSUPPORTED-TOKEN", {item.code for item in findings})

    def test_active_authority_inventory_covers_stages_and_precommit(self) -> None:
        active_paths = (
            "docs/01.requirements/current.md",
            "docs/02.architecture/current.md",
            "docs/03.specs/current.md",
            "docs/05.operations/current.md",
            ".pre-commit-config.yaml",
        )
        for relative in active_paths:
            with (
                self.subTest(path=relative),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    "Gemini is active authority here.\n", encoding="utf-8"
                )
                scanned = {
                    path.as_posix() for path in contract._active_text_paths(root)
                }
                self.assertIn(relative, scanned)
                findings = contract.validate_repository(
                    root, contract.load_contract_bundle(root), "harness"
                )
                self.assertIn("AGC-UNSUPPORTED-TOKEN", {item.code for item in findings})

    def test_stage03_token_evidence_is_exact_and_new_active_specs_are_scanned(
        self,
    ) -> None:
        # The scanner judges active roots only, and a completed package is now
        # preserved outside them. The case under test is still what happens
        # when that content sits at an active path, so the destination stays in
        # Stage 03 while the source follows the record into the archive.
        historical = "docs/03.specs/0094-harness-agent-first-engineering/spec.md"
        historical_source = (
            "docs/98.archive/completed/03.specs/"
            "0094-harness-agent-first-engineering/spec.md"
        )
        cases = ("exact-evidence", "changed-evidence", "new-active-spec")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                if case == "new-active-spec":
                    target = root / "docs/03.specs/spec-9999-current/spec.md"
                    target.parent.mkdir(parents=True)
                    target.write_text(
                        "---\nstatus: active\n---\n\n# Current Spec\n\n"
                        "Gemini is current active authority.\n",
                        encoding="utf-8",
                    )
                else:
                    target = root / historical
                    target.parent.mkdir(parents=True)
                    shutil.copy2(ROOT / historical_source, target)
                    if case == "changed-evidence":
                        target.write_text(
                            target.read_text(encoding="utf-8")
                            + "\nGemini is current active authority.\n",
                            encoding="utf-8",
                        )
                findings = contract.validate_repository(
                    root, contract.load_contract_bundle(root), "harness"
                )
                unsupported = {
                    item.path
                    for item in findings
                    if item.code == "AGC-UNSUPPORTED-TOKEN"
                }
                if case == "exact-evidence":
                    self.assertNotIn(historical, unsupported)
                else:
                    self.assertIn(target.relative_to(root).as_posix(), unsupported)

    def test_python_retired_inventory_is_syntax_bounded(self) -> None:
        path = "scripts/check_authority.py"
        old = "docs/00.agent-governance"
        inventories = (
            f'RETIRED_PATHS = ("{old}",)\n',
            f'RETIRED_PATHS = (\n    "{old}",\n)\n',
            f'REMOVED_PATHS: tuple[str, ...] = ("{old}",)\n',
        )
        for inventory in inventories:
            with self.subTest(inventory=inventory):
                self.assertFalse(
                    contract._has_unsupported_active_token(path, inventory)
                )
                self.assertTrue(
                    contract._has_unsupported_active_token(
                        path,
                        inventory.rstrip() + f'; load("{old}/policies/bootstrap.md")\n',
                    )
                )
                self.assertTrue(
                    contract._has_unsupported_active_token(
                        path,
                        inventory + f'CURRENT_PATH = "{old}/policies/bootstrap.md"\n',
                    )
                )
        for source in (
            f'CURRENT_PATHS = ("{old}",)\n',
            f'RETIRED_PATHS = tuple(["{old}"])\n',
            f'RETIRED_PATHS = (load("{old}"),)\n',
        ):
            self.assertTrue(contract._has_unsupported_active_token(path, source))

    def test_retired_home_has_no_active_route_or_physical_fallback(self) -> None:
        path = "docs/03.specs/9999-example/spec.md"
        old = "docs/00.agent-governance"
        for route in (
            f"Load {old}/policies/bootstrap.md.",
            f"Use {old}/skills/adr-writing.md.",
        ):
            self.assertTrue(contract._has_unsupported_active_token(path, route))
            historical = contract.HISTORICAL_QUOTE_MARKER + "\n> " + route
            self.assertFalse(contract._has_unsupported_active_token(path, historical))
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            retired = root / old / "unowned.md"
            retired.parent.mkdir(parents=True)
            retired.write_bytes(b"preserved user content")
            bundle = contract.load_contract_bundle(root)
            with mock.patch.object(
                contract, "_read_text", wraps=contract._read_text
            ) as read:
                findings = contract.validate_repository(root, bundle, "harness")
            self.assertIn("AGC-RETIRED-SURFACE", {item.code for item in findings})
            self.assertFalse(
                any(str(call.args[1]).startswith(old) for call in read.call_args_list)
            )
            self.assertEqual(b"preserved user content", retired.read_bytes())

    def test_explicit_history_quote_does_not_hide_adjacent_current_authority(
        self,
    ) -> None:
        path = "docs/03.specs/9999-example/spec.md"
        quote = contract.HISTORICAL_QUOTE_MARKER + "\n> July baseline used Gemini.\n"
        self.assertFalse(contract._has_unsupported_active_token(path, quote))
        for token in ("Gemini is active authority.", "Load memory/current.md."):
            for text in (
                token + "\n" + quote,
                quote + "\n" + token,
                "## Historical evidence\n" + token,
                quote.replace("not current authority", "current authority") + token,
                quote + token,
            ):
                with self.subTest(text=text):
                    self.assertTrue(contract._has_unsupported_active_token(path, text))
        self.assertTrue(
            contract._has_unsupported_active_token("scripts/current.py", quote)
        )

    def test_source_reader_rejects_ancestor_replacement_race(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            inside = root / ".agents/governance/providers/registry.yaml"
            outside = root / "outside/governance/providers/registry.yaml"
            inside.parent.mkdir(parents=True)
            outside.parent.mkdir(parents=True)
            inside.write_bytes(b"registered input")
            outside.write_bytes(b"outside sentinel")
            real_stat = contract.os.stat
            swapped = False

            def swap_after_parent_stat(path, *args, **kwargs):
                nonlocal swapped
                result = real_stat(path, *args, **kwargs)
                if not swapped and str(path) in {str(root / ".agents"), ".agents"}:
                    swapped = True
                    (root / ".agents").rename(root / "original-agents")
                    (root / ".agents").symlink_to(
                        root / "outside", target_is_directory=True
                    )
                return result

            with mock.patch.object(
                contract.os, "stat", side_effect=swap_after_parent_stat
            ):
                with self.assertRaises(contract.ContractLoadError):
                    contract.read_repository_text(
                        root, ".agents/governance/providers/registry.yaml"
                    )
            self.assertTrue(swapped)
            self.assertEqual(b"outside sentinel", outside.read_bytes())

    def test_active_reader_retains_finite_four_mebibyte_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "evidence.md"
            target.write_bytes(b"x" * (2241242))
            self.assertEqual(
                2241242, len(contract.read_repository_text(root, "evidence.md"))
            )
            target.write_bytes(b"x" * (contract.MAX_TEXT_BYTES + 1))
            with self.assertRaisesRegex(contract.ContractLoadError, "TOO-LARGE"):
                contract.read_repository_text(root, "evidence.md")

    def test_removal_statements_do_not_authorize_mixed_positive_adoption(self) -> None:
        path = "docs/03.specs/9999-example/spec.md"
        for text in (
            "Gemini and Antigravity are removed.",
            "Delete: `.gemini/`.",
            "No bootstrap loads memory/current.md.",
            'self.assertFalse(Path(".gemini").exists())',
        ):
            with self.subTest(text=text):
                self.assertFalse(contract._has_unsupported_active_token(path, text))
        for text in (
            "Remove Gemini. Use Gemini for new work.",
            "Remove old memory and use Gemini.",
            "Do not remove Gemini.",
            "Gemini must remain active despite removal of old memory.",
            "Gemini is the default provider when Codex fails.",
            "No secrets are stored; Gemini is supported.",
            "Remove Gemini, but Antigravity is active.",
            "Add mutation cases for Gemini. Use memory/current.md.",
            "## Historical\nUse memory/current.md.",
        ):
            with self.subTest(text=text):
                self.assertTrue(contract._has_unsupported_active_token(path, text))

    def test_historical_table_requires_exact_marker_header_and_separator(self) -> None:
        path = "docs/03.specs/9999-example/tasks/tsk-0001-evidence.md"
        table = (
            contract.HISTORICAL_TABLE_MARKER
            + "\n| Command | Result |\n| --- | --- |\n| Gemini probe | July measurement |\n"
        )
        self.assertFalse(contract._has_unsupported_active_token(path, table))
        for candidate in (
            table + "\nUse Gemini now.",
            table
            + "\n| Current | State |\n| --- | --- |\n| Load memory/current.md | required |\n",
            table.replace("| --- | --- |", "bad separator"),
            table.replace("| --- | --- |", "| - | - |"),
            table.replace("| Command | Result |", "| Command |"),
            table.replace("| Command | Result |", "| | Result |"),
            table.replace("not current authority", "current authority"),
        ):
            self.assertTrue(contract._has_unsupported_active_token(path, candidate))

    def test_mutable_task_token_evidence_is_statement_bounded(self) -> None:
        task = "docs/03.specs/9999-example/tasks/tsk-0001-evidence.md"
        fixture = (
            "# Stage 00 convergence evidence\n\n"
            "The change completed while removing Gemini, Antigravity, "
            "and project memory.\n"
        )
        cases = ("evidence-only-edit", "new-active-authority", "altered-statement")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                target = root / task
                target.parent.mkdir(parents=True)
                target.write_text(fixture, encoding="utf-8")
                text = target.read_text(encoding="utf-8")
                if case == "evidence-only-edit":
                    text += "\nPost-commit evidence: logical commit recorded.\n"
                elif case == "new-active-authority":
                    text += "\nGemini is current active authority.\n"
                else:
                    text = text.replace(
                        "while removing Gemini, Antigravity, and project memory.",
                        "while making Gemini current active authority and retaining "
                        "Antigravity and project memory.",
                        1,
                    )
                target.write_text(text, encoding="utf-8")
                findings = contract.validate_repository(
                    root, contract.load_contract_bundle(root), "harness"
                )
                unsupported = {
                    item.path
                    for item in findings
                    if item.code == "AGC-UNSUPPORTED-TOKEN"
                }
                if case == "evidence-only-edit":
                    self.assertNotIn(task, unsupported)
                else:
                    self.assertIn(task, unsupported)

    def test_projection_routes_and_managed_roots_are_strict(self) -> None:
        mutations = {
            "canonical-native-root": lambda data: data["generated_roots"].append(
                ".agents/skills"
            ),
            "canonical-static-output": lambda data: data["projections"][0].update(
                {"path": ".agents/README.md"}
            ),
            "codex-fake-native-skill": lambda data: data["providers"][1].update(
                {"native_skill_pattern": ".codex/skills/{skill_id}/SKILL.md"}
            ),
            "old-canonical-route": lambda data: data["providers"][1].update(
                {
                    "canonical_skill_pattern": "docs/00.agent-governance/skills/{skill_id}.md"
                }
            ),
            "projection-provider": lambda data: data["projections"][0].update(
                {"provider_id": "unsupported"}
            ),
            "projection-source": lambda data: data["projections"][0].update(
                {"source": "docs/90.references/current.md"}
            ),
            "projection-route": lambda data: data["projections"][0].update(
                {"path": ".codex/README.md"}
            ),
            "projection-duplicate": lambda data: data["projections"].append(
                dict(data["projections"][0])
            ),
            "projection-managed-collision": lambda data: data["projections"][0].update(
                {"path": ".claude/agents/code-reviewer.md"}
            ),
            "projection-native-config": lambda data: data["projections"][1].update(
                {"path": ".claude/settings.json"}
            ),
            "managed-root-extra": lambda data: data["generated_roots"].append(
                ".claude/other"
            ),
            "managed-root-missing": lambda data: data["generated_roots"].pop(),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                path = root / ".agents/governance/providers/registry.yaml"
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutation(data)
                path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                with self.assertRaises(contract.ContractLoadError):
                    contract.load_agent_governance(root)

    def test_dirty_state_and_scratch_safeguards_are_durable(self) -> None:
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in (
                ".agents/governance/agentic.md",
                ".agents/governance/approval-boundaries.md",
            )
        ).lower()
        for literal in (
            "parent ignore probes",
            "inspection and deletion",
            "controller",
            "only after review",
            "reviewer worktree",
            "digest mismatch",
            "reconcile staged paths",
            "concurrency incident",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, text)


if __name__ == "__main__":
    unittest.main()
