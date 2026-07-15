from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import shutil
import sys
import tempfile
import tomllib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
RENDERER = ROOT / "scripts/operations/provider_surface_renderer.py"
VALIDATION_DIR = ROOT / "scripts/validation"
if str(VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATION_DIR))

import agent_governance_contract as contract  # noqa: E402


def load_renderer():
    spec = importlib.util.spec_from_file_location("provider_native_renderer", RENDERER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load renderer: {RENDERER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_provider_contract(root: pathlib.Path = ROOT) -> dict[str, object]:
    return yaml.safe_load(
        (root / "docs/00.agent-governance/contracts/provider-models.yaml").read_text(
            encoding="utf-8"
        )
    )


def expected_native_projection(test: unittest.TestCase, renderer, root: pathlib.Path):
    render = getattr(renderer, "expected_native_projection", None)
    test.assertIsNotNone(render, "renderer must expose expected_native_projection")
    return render(root)


def write_native_projection(test: unittest.TestCase, renderer, root: pathlib.Path) -> None:
    write = getattr(renderer, "write_native_projection", None)
    test.assertIsNotNone(write, "renderer must expose write_native_projection")
    write(root)


class ProviderNativeSurfaceTests(unittest.TestCase):
    def test_contract_loader_rejects_duplicate_provider_model_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            text = path.read_text(encoding="utf-8").replace(
                "    runtime_acceptance: rejected\n",
                "    runtime_acceptance: rejected\n"
                "    runtime_acceptance: rejected\n",
                1,
            )
            path.write_text(text, encoding="utf-8")

            with self.assertRaises(contract.ContractLoadError) as raised:
                contract.load_contract_bundle(root)
            self.assertEqual("AGC-YAML-DUPLICATE-KEY", raised.exception.code)

    def test_contract_rejects_backdated_retrieval_and_policy_conflation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            values = yaml.safe_load(path.read_text(encoding="utf-8"))
            values["retrieved_at"] = "2026-07-09T10:00:00+09:00"
            sol = next(
                item
                for item in values["models"]
                if item["provider"] == "codex" and item["model_id"] == "gpt-5.6"
            )
            sol["normalized_status"] = "stable"
            sol["repository_reasoning_controls"] = [
                "high",
                "medium",
                "ultra",
                "xhigh",
            ]
            sol["fallback_policy"] = "same-profile"
            sol["fallback_approval"] = None
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            observed = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertTrue(
                {
                    "AGC-MODEL-FALLBACK-POLICY",
                    "AGC-MODEL-REASONING-POLICY",
                    "AGC-MODEL-STATUS-NORMALIZATION",
                    "AGC-SOURCE-OBSERVATION-ORDER",
                }.issubset(observed)
            )

    def test_model_observation_separates_cutoff_status_and_reasoning_policy(self) -> None:
        values = load_provider_contract()
        self.assertEqual("2026-07-10T10:00:00+09:00", values.get("cutoff_at"))
        self.assertTrue(str(values.get("retrieved_at", "")).startswith("2026-07-16T"))

        models = {
            (item["provider"], item["model_id"]): item for item in values["models"]
        }
        sol = models[("codex", "gpt-5.6")]
        self.assertEqual("gpt-5.6-sol", sol["canonical_model_id"])
        self.assertEqual("listed", sol["provider_status"])
        self.assertEqual("unclassified-listed", sol["normalized_status"])
        self.assertEqual("historical-state-unverified", sol["cutoff_evidence_status"])
        self.assertEqual(
            ["high", "low", "max", "medium", "none", "xhigh"],
            sol["supported_reasoning_controls"],
        )
        self.assertEqual(
            ["high", "medium", "xhigh"], sol["repository_reasoning_controls"]
        )
        self.assertNotIn("reasoning_controls", sol)

        gemini = models[("gemini", "gemini-3.5-flash")]
        self.assertEqual(
            ["high", "low", "medium", "minimal"],
            gemini["supported_reasoning_controls"],
        )
        self.assertEqual(
            ["high", "medium"], gemini["repository_reasoning_controls"]
        )
        self.assertNotIn("model-selected", json.dumps(values, sort_keys=True))

        fable = models[("claude", "claude-fable-5")]
        mythos = models[("claude", "claude-mythos-5")]
        haiku = models[("claude", "claude-haiku-4-5-20251001")]
        opus = models[("claude", "claude-opus-4-8")]
        sonnet = models[("claude", "claude-sonnet-5")]
        self.assertEqual("adaptive-always-on", fable["reasoning_control_kind"])
        self.assertEqual(
            ["always-on-adaptive"], fable["supported_reasoning_controls"]
        )
        self.assertEqual("adaptive-always-on", mythos["reasoning_control_kind"])
        self.assertEqual(
            ["always-on-adaptive"], mythos["supported_reasoning_controls"]
        )
        self.assertEqual("extended-thinking", haiku["reasoning_control_kind"])
        self.assertEqual(
            ["extended-thinking"], haiku["supported_reasoning_controls"]
        )
        self.assertEqual("effort", opus["reasoning_control_kind"])
        self.assertEqual(["high"], opus["supported_reasoning_controls"])
        self.assertEqual("adaptive", sonnet["reasoning_control_kind"])
        self.assertEqual(["adaptive"], sonnet["supported_reasoning_controls"])

        self.assertEqual(
            {
                "deprecated",
                "limited",
                "preview",
                "stable",
                "unclassified-listed",
            },
            {item["normalized_status"] for item in values["models"]},
        )
        for item in values["models"]:
            self.assertIn(item["fallback_policy"], {"same-profile", "approved-degraded"})
            if item["fallback_policy"] == "approved-degraded":
                self.assertEqual(
                    "spec:132-agent-governance-harness-convergence",
                    item["fallback_approval"],
                )

    def test_contract_requires_fallback_to_cover_every_declared_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            values = yaml.safe_load(path.read_text(encoding="utf-8"))
            fable = next(
                item
                for item in values["models"]
                if item["provider"] == "claude"
                and item["model_id"] == "claude-fable-5"
            )
            fable["fallback_policy"] = "same-profile"
            fable["fallback_approval"] = None
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            observed = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertIn("AGC-MODEL-FALLBACK-POLICY", observed)

    def test_native_projection_contains_every_exact_owned_path(self) -> None:
        renderer = load_renderer()
        projection = expected_native_projection(self, renderer, ROOT)
        catalog = renderer.load_catalog(ROOT)
        expected = {
            *(pathlib.Path(".claude/agents") / f"{item.agent_id}.md" for item in catalog.agents),
            *(pathlib.Path(".codex/agents") / f"{item.agent_id}.toml" for item in catalog.agents),
            *(pathlib.Path(".gemini/agents") / f"{item.agent_id}.md" for item in catalog.agents),
            *(pathlib.Path(".agents/agents") / f"{item.agent_id}.md" for item in catalog.agents),
            *(pathlib.Path(".claude/skills") / item.function_id / "SKILL.md" for item in catalog.functions),
            *(pathlib.Path(".agents/skills") / item.function_id / "SKILL.md" for item in catalog.functions),
            pathlib.Path(".claude/CLAUDE.md"),
            pathlib.Path(".claude/settings.json"),
            pathlib.Path(".claude/hooks/docker-compose-pre.sh"),
            pathlib.Path(".claude/hooks/post-tool-validate.sh"),
            pathlib.Path(".claude/hooks/pre-compact.sh"),
            pathlib.Path(".claude/hooks/session-end.sh"),
            pathlib.Path(".claude/hooks/session-start.sh"),
            pathlib.Path(".claude/hooks/stop.sh"),
            pathlib.Path(".claude/hooks/user-prompt-submit.sh"),
            pathlib.Path(".codex/README.md"),
            pathlib.Path(".codex/hooks.json"),
            pathlib.Path(".gemini/README.md"),
            pathlib.Path(".gemini/settings.json"),
            pathlib.Path(".gemini/hooks/agent-event-hook.sh"),
            pathlib.Path(".agents/README.md"),
            pathlib.Path(".agents/rules/workspace.md"),
            pathlib.Path(".agents/workflows/documentation.md"),
        }
        self.assertEqual(expected, set(projection))
        self.assertFalse((ROOT / ".codex/skills").exists())

    def test_native_agent_schemas_are_strict_and_least_privilege(self) -> None:
        renderer = load_renderer()
        projection = expected_native_projection(self, renderer, ROOT)
        catalog = renderer.load_catalog(ROOT)

        claude_allowed = {
            "name",
            "description",
            "tools",
            "model",
            "permissionMode",
            "skills",
        }
        gemini_allowed = {
            "name",
            "description",
            "kind",
            "tools",
            "model",
            "max_turns",
            "timeout_mins",
        }
        read_only_ids = {
            item.agent_id
            for item in catalog.agents
            if item.permission_profile == "read-only"
        }
        for agent in catalog.agents:
            claude_text = projection[pathlib.Path(f".claude/agents/{agent.agent_id}.md")].decode()
            claude_meta = yaml.safe_load(claude_text.split("---\n", 2)[1])
            self.assertEqual(claude_allowed, set(claude_meta))
            self.assertEqual(agent.agent_id, claude_meta["name"])
            if agent.agent_id in read_only_ids:
                self.assertEqual("plan", claude_meta["permissionMode"])
                self.assertNotIn("Write", claude_meta["tools"])
                self.assertNotIn("Edit", claude_meta["tools"])

            codex = tomllib.loads(
                projection[pathlib.Path(f".codex/agents/{agent.agent_id}.toml")].decode()
            )
            self.assertEqual(
                {
                    "name",
                    "description",
                    "developer_instructions",
                    "model",
                    "model_reasoning_effort",
                    "sandbox_mode",
                },
                set(codex),
            )
            self.assertEqual(
                "read-only" if agent.agent_id in read_only_ids else "workspace-write",
                codex["sandbox_mode"],
            )

            gemini_text = projection[pathlib.Path(f".gemini/agents/{agent.agent_id}.md")].decode()
            gemini_meta = yaml.safe_load(gemini_text.split("---\n", 2)[1])
            self.assertEqual(gemini_allowed, set(gemini_meta))
            self.assertNotIn("sandbox", gemini_meta)
            if agent.agent_id in read_only_ids:
                self.assertNotIn("*", gemini_meta["tools"])
                self.assertNotIn("write_file", gemini_meta["tools"])
                self.assertNotIn("replace", gemini_meta["tools"])

    def test_every_generated_agent_local_link_resolves_from_its_projection(self) -> None:
        renderer = load_renderer()
        projection = expected_native_projection(self, renderer, ROOT)
        catalog = renderer.load_catalog(ROOT)
        repository = ROOT.resolve()
        checked_agents = 0
        checked_links = 0

        for agent in catalog.agents:
            for relative in (
                pathlib.Path(f".claude/agents/{agent.agent_id}.md"),
                pathlib.Path(f".gemini/agents/{agent.agent_id}.md"),
                pathlib.Path(f".agents/agents/{agent.agent_id}.md"),
            ):
                body = projection[relative].decode()
                checked_agents += 1
                for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
                    if target.startswith(("#", "/", "http://", "https://", "mailto:")):
                        continue
                    resolved = (ROOT / relative.parent / target.split("#", 1)[0]).resolve()
                    self.assertTrue(resolved.is_relative_to(repository), relative.as_posix())
                    self.assertTrue(resolved.is_file(), f"{relative}: {target}")
                    checked_links += 1

            relative = pathlib.Path(f".codex/agents/{agent.agent_id}.toml")
            body = tomllib.loads(projection[relative].decode())["developer_instructions"]
            checked_agents += 1
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
                if target.startswith(("#", "/", "http://", "https://", "mailto:")):
                    continue
                resolved = (ROOT / relative.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.is_relative_to(repository), relative.as_posix())
                self.assertTrue(resolved.is_file(), f"{relative}: {target}")
                checked_links += 1

        self.assertEqual(56, checked_agents)
        self.assertEqual(224, checked_links)

    def test_native_hook_projection_preserves_event_semantics_and_time_units(self) -> None:
        renderer = load_renderer()
        projection = expected_native_projection(self, renderer, ROOT)
        codex = json.loads(projection[pathlib.Path(".codex/hooks.json")])
        claude = json.loads(projection[pathlib.Path(".claude/settings.json")])
        gemini = json.loads(projection[pathlib.Path(".gemini/settings.json")])

        self.assertNotIn("SessionEnd", codex["hooks"])
        self.assertIn("PreCompact", codex["hooks"])
        self.assertIn("PreCompact", claude["hooks"])
        self.assertIn("PreCompress", gemini["hooks"])
        self.assertNotIn("matcher", codex["hooks"]["UserPromptSubmit"][0])
        self.assertNotIn("matcher", codex["hooks"]["Stop"][0])

        self.assertEqual(600, codex["hooks"]["PreCompact"][0]["hooks"][0]["timeout"])
        self.assertEqual(
            60000, gemini["hooks"]["PreCompress"][0]["hooks"][0]["timeout"]
        )
        gemini_handler = gemini["hooks"]["PreCompress"][0]["hooks"][0]
        self.assertEqual({"type", "command", "timeout"}, set(gemini_handler))
        self.assertNotIn("async", gemini_handler)
        for event in (
            "SessionStart",
            "SessionEnd",
            "BeforeAgent",
            "AfterAgent",
            "PreCompress",
        ):
            self.assertNotIn("matcher", gemini["hooks"][event][0])

        for event in claude["hooks"].values():
            command = event[0]["hooks"][0]["command"]
            self.assertIn('bash "$CLAUDE_PROJECT_DIR/', command)
        for event in codex["hooks"].values():
            command = event[0]["hooks"][0]["command"]
            self.assertIn('${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}', command)
        for event in gemini["hooks"].values():
            command = event[0]["hooks"][0]["command"]
            self.assertIn('${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}', command)

        gemini_stop = next(
            binding
            for event in load_provider_contract()["semantic_events"]
            if event["event_id"] == "stop"
            for binding in event["provider_bindings"]
            if binding["provider"] == "gemini"
        )
        self.assertTrue(gemini_stop["provider_can_block"])
        self.assertEqual("deny-retry", gemini_stop["repository_hook_mode"])
        gemini_precompress = next(
            binding
            for event in load_provider_contract()["semantic_events"]
            if event["event_id"] == "pre-compaction"
            for binding in event["provider_bindings"]
            if binding["provider"] == "gemini"
        )
        self.assertFalse(gemini_precompress["provider_can_block"])
        self.assertEqual("advisory", gemini_precompress["repository_hook_mode"])

        values = load_provider_contract()
        providers = {item["provider_id"]: item for item in values["providers"]}
        self.assertEqual(".agents/skills/**/SKILL.md", providers["codex"]["native_skill_pattern"])
        self.assertEqual(".agents/skills/**/SKILL.md", providers["gemini"]["native_skill_pattern"])
        for path in (
            ".claude/hooks/docker-compose-pre.sh",
            ".claude/hooks/post-tool-validate.sh",
            ".claude/hooks/pre-compact.sh",
            ".claude/hooks/session-end.sh",
            ".claude/hooks/session-start.sh",
            ".claude/hooks/stop.sh",
            ".claude/hooks/user-prompt-submit.sh",
        ):
            hook = projection[pathlib.Path(path)].decode()
            self.assertIn("Generated by scripts/operations/provider_surface_renderer.py", hook)
            self.assertIn("scripts/hooks/agent-event-hook.sh", hook)
        for event in values["semantic_events"]:
            for binding in event["provider_bindings"]:
                self.assertNotIn("blocking", binding)
                self.assertIn("provider_can_block", binding)
                self.assertIn(
                    binding["repository_hook_mode"],
                    {"advisory", "blocking", "deny-retry", "unsupported"},
                )
                self.assertEqual(
                    "milliseconds" if binding["provider"] == "gemini" else "seconds",
                    binding["timeout_unit"],
                )

    def test_contract_rejects_underreported_gemini_after_agent_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            values = yaml.safe_load(path.read_text(encoding="utf-8"))
            gemini_stop = next(
                binding
                for event in values["semantic_events"]
                if event["event_id"] == "stop"
                for binding in event["provider_bindings"]
                if binding["provider"] == "gemini"
            )
            gemini_stop["provider_can_block"] = False
            gemini_stop["repository_hook_mode"] = "advisory"
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            observed = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertIn("AGC-EVENT-SEMANTICS", observed)

    def test_repository_provider_section_checks_native_schema_and_drift(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(ROOT / "docs/00.agent-governance", root / "docs/00.agent-governance")
            write_native_projection(self, renderer, root)
            executable = {
                pathlib.Path(".claude/hooks/docker-compose-pre.sh"),
                pathlib.Path(".claude/hooks/post-tool-validate.sh"),
                pathlib.Path(".claude/hooks/pre-compact.sh"),
                pathlib.Path(".claude/hooks/session-end.sh"),
                pathlib.Path(".claude/hooks/session-start.sh"),
                pathlib.Path(".claude/hooks/stop.sh"),
                pathlib.Path(".claude/hooks/user-prompt-submit.sh"),
                pathlib.Path(".gemini/hooks/agent-event-hook.sh"),
            }
            for relative in expected_native_projection(self, renderer, root):
                mode = (root / relative).stat().st_mode & 0o777
                self.assertEqual(
                    0o755 if relative in executable else 0o644,
                    mode,
                    relative.as_posix(),
                )
            bundle = contract.load_contract_bundle(root)
            self.assertEqual([], contract.validate_repository(root, bundle, "providers"))

            codex_path = root / ".codex/agents/code-reviewer.toml"
            codex_path.write_text(
                codex_path.read_text(encoding="utf-8") + 'canonical_scope = "common"\n',
                encoding="utf-8",
            )
            findings = contract.validate_repository(root, bundle, "providers")
            self.assertIn("AGC-PROVIDER-NATIVE-SCHEMA", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()
