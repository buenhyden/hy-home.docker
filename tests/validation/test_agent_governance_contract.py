from __future__ import annotations

import importlib.util
import os
import pathlib
import shutil
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
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
    shutil.copytree(ROOT / "docs/00.agent-governance", root / "docs/00.agent-governance")
    registry = root / "docs/99.templates/registry.json"
    registry.parent.mkdir(parents=True)
    shutil.copy2(ROOT / "docs/99.templates/registry.json", registry)
    for path in ("AGENTS.md", "CLAUDE.md"):
        shutil.copy2(ROOT / path, root / path)
    for directory in (".agents", ".claude", ".codex"):
        shutil.copytree(ROOT / directory, root / directory)
    hook = root / "scripts/hooks/agent-event-hook.sh"
    hook.parent.mkdir(parents=True)
    shutil.copy2(ROOT / "scripts/hooks/agent-event-hook.sh", hook)


class AgentGovernanceContractTests(unittest.TestCase):
    def test_supported_providers_and_governance_roots_are_exact(self) -> None:
        state = contract.load_agent_governance(ROOT)
        self.assertEqual(("claude", "codex"), state.providers)
        self.assertEqual(
            ("README.md", "policies", "providers", "roles", "sdlc.md", "skills"),
            state.root_entries,
        )
        self.assertEqual(
            ("README.md", "claude.md", "codex.md", "registry.yaml"),
            state.provider_entries,
        )
        self.assertEqual(14, len(state.roles))
        self.assertEqual(23, len(state.skills))
        self.assertFalse((ROOT / "docs/00.agent-governance/memory").exists())
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
            policy = root / "docs/00.agent-governance/policies/agentic.md"
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
            generated = root / ".agents/agents/code-reviewer.md"
            generated.write_text(
                generated.read_text() + "\nThis generated file is the policy source of truth.\n"
            )
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "harness"
            )
            self.assertIn("AGC-GENERATED-AUTHORITY", {item.code for item in findings})

    def test_orphan_compatibility_skill_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_governance_fixture(root)
            orphan = root / ".agents/skills/orphan/SKILL.md"
            orphan.parent.mkdir(parents=True)
            orphan.write_text("# orphan\n")
            findings = contract.validate_repository(
                root, contract.load_contract_bundle(root), "catalog"
            )
            self.assertIn("AGC-ORPHAN-SKILL", {item.code for item in findings})

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
                "docs/01.requirements/prd-0001-example.md",
                "docs/01.requirements/prd-{0001..0025}-*.md",
            )
        )

    def test_provider_registry_is_strict_typed_and_cross_referenced(self) -> None:
        state = contract.load_agent_governance(ROOT)
        self.assertEqual(("claude", "codex"), tuple(item.provider_id for item in state.provider_records))
        self.assertEqual(".claude/agents/{agent_id}.md", state.provider_records[0].agent_pattern)
        mutations = {
            "top-level-key": lambda data: data.update({"unknown": True}),
            "provider-key": lambda data: data["providers"][0].update({"unknown": True}),
            "adapter-cross-reference": lambda data: data["providers"][0].update(
                {"adapter_path": "docs/00.agent-governance/providers/codex.md"}
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
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                path = root / "docs/00.agent-governance/providers/registry.yaml"
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutation(data)
                path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                with self.assertRaises(contract.ContractLoadError):
                    contract.load_agent_governance(root)

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
                self.assertIn("AGC-ACTIVE-TEXT-UNSAFE", {item.code for item in findings})

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
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("Gemini is active authority here.\n", encoding="utf-8")
                scanned = {path.as_posix() for path in contract._active_text_paths(root)}
                self.assertIn(relative, scanned)
                findings = contract.validate_repository(
                    root, contract.load_contract_bundle(root), "harness"
                )
                self.assertIn("AGC-UNSUPPORTED-TOKEN", {item.code for item in findings})

    def test_stage03_token_evidence_is_exact_and_new_active_specs_are_scanned(self) -> None:
        historical = "docs/03.specs/0094-harness-agent-first-engineering/spec.md"
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
                    shutil.copy2(ROOT / historical, target)
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
                    item.path for item in findings if item.code == "AGC-UNSUPPORTED-TOKEN"
                }
                if case == "exact-evidence":
                    self.assertNotIn(historical, unsupported)
                else:
                    self.assertIn(target.relative_to(root).as_posix(), unsupported)

    def test_explicit_history_quote_does_not_hide_adjacent_current_authority(self) -> None:
        path = "docs/03.specs/9999-example/spec.md"
        quote = contract.HISTORICAL_QUOTE_MARKER + "\n> July baseline used Gemini.\n"
        self.assertFalse(contract._has_unsupported_active_token(path, quote))
        for token in ("Gemini is active authority.", "Load memory/current.md."):
            for text in (token + "\n" + quote, quote + "\n" + token,
                         "## Historical evidence\n" + token,
                         quote.replace("not current authority", "current authority") + token,
                         quote + token):
                with self.subTest(text=text):
                    self.assertTrue(contract._has_unsupported_active_token(path, text))
        self.assertTrue(contract._has_unsupported_active_token("scripts/current.py", quote))

    def test_active_reader_retains_finite_four_mebibyte_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "evidence.md"
            target.write_bytes(b"x" * (2241242))
            self.assertEqual(2241242, len(contract.read_repository_text(root, "evidence.md")))
            target.write_bytes(b"x" * (contract.MAX_TEXT_BYTES + 1))
            with self.assertRaisesRegex(contract.ContractLoadError, "TOO-LARGE"):
                contract.read_repository_text(root, "evidence.md")

    def test_removal_statements_do_not_authorize_mixed_positive_adoption(self) -> None:
        path = "docs/03.specs/9999-example/spec.md"
        for text in ("Gemini and Antigravity are removed.", "Delete: `.gemini/`.",
                     "No bootstrap loads memory/current.md.", "self.assertFalse(Path(\".gemini\").exists())"):
            with self.subTest(text=text):
                self.assertFalse(contract._has_unsupported_active_token(path, text))
        for text in ("Remove Gemini. Use Gemini for new work.",
                     "Remove old memory and use Gemini.", "Do not remove Gemini.",
                     "Gemini must remain active despite removal of old memory.",
                     "Gemini is the default provider when Codex fails.",
                     "No secrets are stored; Gemini is supported.",
                     "Remove Gemini, but Antigravity is active.",
                     "Add mutation cases for Gemini. Use memory/current.md.",
                     "## Historical\nUse memory/current.md."):
            with self.subTest(text=text):
                self.assertTrue(contract._has_unsupported_active_token(path, text))

    def test_historical_table_requires_exact_marker_header_and_separator(self) -> None:
        path = "docs/03.specs/9999-example/tasks/tsk-0001-evidence.md"
        table = contract.HISTORICAL_TABLE_MARKER + "\n| Command | Result |\n| --- | --- |\n| Gemini probe | July measurement |\n"
        self.assertFalse(contract._has_unsupported_active_token(path, table))
        for candidate in (table + "\nUse Gemini now.", table + "\n| Current | State |\n| --- | --- |\n| Load memory/current.md | required |\n", table.replace("| --- | --- |", "bad separator"), table.replace("| --- | --- |", "| - | - |"), table.replace("| Command | Result |", "| Command |"), table.replace("| Command | Result |", "| | Result |"), table.replace("not current authority", "current authority")):
            self.assertTrue(contract._has_unsupported_active_token(path, candidate))

    def test_mutable_task_token_evidence_is_statement_bounded(self) -> None:
        task = (
            "docs/03.specs/0153-workspace-governance-simplification/"
            "tasks/tsk-0004-stage00.md"
        )
        cases = ("evidence-only-edit", "new-active-authority", "altered-statement")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                target = root / task
                target.parent.mkdir(parents=True)
                shutil.copy2(ROOT / task, target)
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
                    item.path for item in findings if item.code == "AGC-UNSUPPORTED-TOKEN"
                }
                if case == "evidence-only-edit":
                    self.assertNotIn(task, unsupported)
                else:
                    self.assertIn(task, unsupported)

    def test_loops_states_and_harness_layers_are_strict_and_cross_referenced(self) -> None:
        mutations = {
            "loop-owner": lambda data: data["harness_loops"]["context-bootstrap"].update(
                {"owner_agent": "not-a-role"}
            ),
            "loop-reviewer": lambda data: data["harness_loops"]["context-bootstrap"].update(
                {"reviewer_agent": "not-a-role"}
            ),
            "loop-stop": lambda data: data["harness_loops"]["context-bootstrap"].update(
                {"stop_condition": ""}
            ),
            "loop-failure": lambda data: data["harness_loops"]["context-bootstrap"].update(
                {"on_failure": []}
            ),
            "state-owner": lambda data: data["workflow_states"][0].update(
                {"owner_agent": "not-a-role"}
            ),
            "state-return": lambda data: data["workflow_states"][0].update(
                {"failure_return": "invented-state"}
            ),
            "layer-owner": lambda data: data["harness_layers"][0].update(
                {"owner_agent": "not-a-role"}
            ),
            "layer-gate": lambda data: data["harness_layers"][0].update({"gate": ""}),
            "layer-return": lambda data: data["harness_layers"][0].update(
                {"failure_return": "invented-state"}
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_governance_fixture(root)
                path = root / "docs/00.agent-governance/providers/registry.yaml"
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutation(data)
                path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                with self.assertRaises(contract.ContractLoadError):
                    contract.load_agent_governance(root)

    def test_dirty_state_and_scratch_safeguards_are_durable(self) -> None:
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in (
                "docs/00.agent-governance/policies/agentic.md",
                "docs/00.agent-governance/policies/approval-boundaries.md",
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
