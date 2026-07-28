from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
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


def copy_provider_contract_root(root: pathlib.Path) -> None:
    shutil.copytree(
        ROOT / "docs/00.agent-governance",
        root / "docs/00.agent-governance",
    )
    ledger_source = (
        ROOT
        / "docs/90.references/data/governance/"
        "agent-governance-retirement-ledger.yaml"
    )
    ledger_target = root / ledger_source.relative_to(ROOT)
    ledger_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ledger_source, ledger_target)
    spec_source = (
        ROOT / "docs/03.specs/132-agent-governance-harness-convergence/spec.md"
    )
    spec_target = root / spec_source.relative_to(ROOT)
    spec_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(spec_source, spec_target)


def expected_native_projection(test: unittest.TestCase, renderer, root: pathlib.Path):
    render = getattr(renderer, "expected_native_projection", None)
    test.assertIsNotNone(render, "renderer must expose expected_native_projection")
    return render(root)


def write_native_projection(
    test: unittest.TestCase, renderer, root: pathlib.Path
) -> None:
    write = getattr(renderer, "write_native_projection", None)
    test.assertIsNotNone(write, "renderer must expose write_native_projection")
    write(root)


class ProviderNativeSurfaceTests(unittest.TestCase):
    def test_gemini_reasoning_uses_scoped_model_configs_without_sampling_parameters(
        self,
    ) -> None:
        renderer = load_renderer()
        projection = expected_native_projection(self, renderer, ROOT)
        catalog = renderer.load_catalog(ROOT)
        values = load_provider_contract()
        selections = renderer._provider_selections(values)
        settings = json.loads(projection[pathlib.Path(".gemini/settings.json")])
        expected_overrides = [
            {
                "match": {"overrideScope": agent.agent_id},
                "modelConfig": {
                    "generateContentConfig": {
                        "thinkingConfig": {
                            "thinkingLevel": selections[
                                (agent.work_profile, "gemini")
                            ].control_value.upper()
                        }
                    }
                },
            }
            for agent in catalog.agents
        ]

        self.assertEqual(
            expected_overrides,
            settings["modelConfigs"]["overrides"],
        )
        serialized = json.dumps(settings, sort_keys=True)
        for forbidden in ("temperature", "top_p", "top_k", "topP", "topK"):
            self.assertNotIn(forbidden, serialized)
        for agent in catalog.agents:
            metadata = yaml.safe_load(
                projection[
                    pathlib.Path(f".gemini/agents/{agent.agent_id}.md")
                ]
                .decode()
                .split("---\n", 2)[1]
            )
            self.assertEqual(
                selections[(agent.work_profile, "gemini")].model_id,
                metadata["model"],
            )

    def test_contract_loader_rejects_duplicate_provider_model_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            text = path.read_text(encoding="utf-8")
            active_model_key = "    model_id: claude-fable-5\n"
            self.assertEqual(1, text.count(active_model_key))
            text = text.replace(
                active_model_key,
                active_model_key * 2,
                1,
            )
            self.assertEqual(2, text.count(active_model_key))
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
                if item["provider"] == "codex"
                and item["model_id"] == "gpt-5.6-sol"
            )
            sol["repository_reasoning_controls"] = [
                "high",
                "medium",
                "ultra",
                "xhigh",
            ]
            sol["runtime_activation_eligible"] = True
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            observed = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertTrue(
                {
                    "AGC-MODEL-ACTIVATION-ELIGIBILITY",
                    "AGC-MODEL-REASONING-POLICY",
                    "AGC-SOURCE-OBSERVATION-ORDER",
                }.issubset(observed)
            )

    def test_model_observation_separates_lifecycle_runtime_and_reasoning_policy(
        self,
    ) -> None:
        values = load_provider_contract()
        retrieved_at = "2026-07-26T20:08:18+09:00"
        self.assertEqual(retrieved_at, values.get("cutoff_at"))
        self.assertEqual(retrieved_at, values.get("retrieved_at"))

        models = {
            (item["provider"], item["model_id"]): item for item in values["models"]
        }
        sol = models[("codex", "gpt-5.6-sol")]
        self.assertEqual("stable", sol["provider_lifecycle"])
        self.assertEqual("default", sol["repository_disposition"])
        self.assertEqual("needs_revalidation", sol["runtime_acceptance"])
        self.assertEqual("needs_revalidation", sol["entitlement"])
        self.assertTrue(sol["repository_default_eligible"])
        self.assertFalse(sol["runtime_activation_eligible"])
        self.assertEqual(
            ["high", "low", "max", "medium", "none", "xhigh"],
            sol["supported_reasoning_controls"],
        )
        self.assertEqual(["high", "xhigh"], sol["repository_reasoning_controls"])

        gemini = models[("gemini", "gemini-3.6-flash")]
        self.assertEqual(
            ["high", "low", "medium", "minimal"],
            gemini["supported_reasoning_controls"],
        )
        self.assertEqual(["high"], gemini["repository_reasoning_controls"])
        self.assertNotIn("model-selected", json.dumps(values, sort_keys=True))

        fable = models[("claude", "claude-fable-5")]
        mythos = models[("claude", "claude-mythos-5")]
        haiku = models[("claude", "claude-haiku-4-5-20251001")]
        opus = models[("claude", "claude-opus-5")]
        sonnet = models[("claude", "claude-sonnet-5")]
        self.assertEqual("effort", fable["reasoning_control_kind"])
        self.assertEqual("effort", mythos["reasoning_control_kind"])
        self.assertEqual("unsupported", haiku["reasoning_control_kind"])
        self.assertEqual([], haiku["supported_reasoning_controls"])
        self.assertEqual("effort", opus["reasoning_control_kind"])
        self.assertEqual(
            ["high", "low", "max", "medium", "xhigh"],
            opus["supported_reasoning_controls"],
        )
        self.assertEqual(
            ["high", "low", "max", "medium", "xhigh"],
            sonnet["supported_reasoning_controls"],
        )

        self.assertEqual(
            {"limited_availability", "preview", "stable"},
            {item["provider_lifecycle"] for item in values["models"]},
        )
        retired_model_ids = {
            "claude-opus-4-1-20250805",
            "claude-opus-4-8",
            "gemini-3.1-flash-lite",
            "gemini-3.1-flash-lite-preview",
            "gemini-3.1-pro-preview",
            "gemini-3.5-flash",
            "gpt-5.2-codex",
            "gpt-5.6",
        }
        self.assertTrue(
            retired_model_ids.isdisjoint(
                {item["model_id"] for item in values["models"]}
            )
        )
        removed_fields = {
            "canonical_model_id",
            "cutoff_evidence_id",
            "cutoff_evidence_status",
            "fallback",
            "fallback_approval",
            "fallback_policy",
            "normalized_status",
            "provider_status",
            "supported_effort_controls",
            "supported_thinking_controls",
            "thinking_control_kind",
        }
        for item in values["models"]:
            self.assertTrue(removed_fields.isdisjoint(item))
            self.assertEqual(retrieved_at, item["source_retrieved_at"])

    def test_contract_rejects_automatic_fallback_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            values = yaml.safe_load(path.read_text(encoding="utf-8"))
            values["models"][0]["fallback"] = values["models"][1]["model_id"]
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            observed = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertIn("AGC-SCHEMA-UNKNOWN-FIELD", observed)

    def test_claude_controls_use_unified_reasoning_schema_without_fallbacks(
        self,
    ) -> None:
        values = load_provider_contract()
        models = {
            (item["provider"], item["model_id"]): item for item in values["models"]
        }
        removed_fields = {
            "cutoff_evidence_id",
            "cutoff_evidence_observed_at",
            "cutoff_evidence_status",
            "cutoff_evidence_url",
            "fallback",
            "fallback_approval",
            "fallback_policy",
            "supported_effort_controls",
            "supported_thinking_controls",
            "thinking_control_kind",
        }
        for model in values["models"]:
            self.assertTrue(removed_fields.isdisjoint(model))

        for model_id in ("claude-opus-5", "claude-sonnet-5"):
            model = models[("claude", model_id)]
            self.assertEqual("effort", model["reasoning_control_kind"])
            self.assertEqual(
                ["high", "low", "max", "medium", "xhigh"],
                model["supported_reasoning_controls"],
            )
            self.assertEqual("effort", model["native_reasoning_field"])

        haiku = models[("claude", "claude-haiku-4-5-20251001")]
        self.assertEqual("unsupported", haiku["reasoning_control_kind"])
        self.assertEqual([], haiku["supported_reasoning_controls"])
        self.assertIsNone(haiku["native_reasoning_field"])

    def test_claude_native_subagents_use_effort_without_per_agent_thinking(
        self,
    ) -> None:
        values = load_provider_contract()
        claude_defaults = {
            profile["profile_id"]: next(
                item for item in profile["defaults"] if item["provider"] == "claude"
            )
            for profile in values["work_profiles"]
        }
        for default in claude_defaults.values():
            self.assertEqual({"provider", "model_id", "effort"}, set(default))
            self.assertNotIn("thinking", default)

        renderer = load_renderer()
        projection = expected_native_projection(self, renderer, ROOT)
        catalog = renderer.load_catalog(ROOT)
        for agent in catalog.agents:
            relative = pathlib.Path(f".claude/agents/{agent.agent_id}.md")
            metadata = yaml.safe_load(
                projection[relative].decode().split("---\n", 2)[1]
            )
            self.assertNotIn("thinking", metadata)
            expected_effort = claude_defaults[agent.work_profile]["effort"]
            if expected_effort is None:
                self.assertNotIn("effort", metadata)
            else:
                self.assertEqual(expected_effort, metadata["effort"])

    def test_claude_native_effort_contract_rejects_schema_and_policy_drift(
        self,
    ) -> None:
        mutations = {
            "per-agent-thinking": (
                lambda default: default.__setitem__("thinking", "adaptive"),
                "AGC-SCHEMA-UNKNOWN-FIELD",
            ),
            "missing-effort": (
                lambda default: default.pop("effort"),
                "AGC-SCHEMA-MISSING-FIELD",
            ),
            "unapproved-effort": (
                lambda default: default.__setitem__("effort", "max"),
                "AGC-MODEL-REASONING-MISMATCH",
            ),
        }
        for name, (mutate, expected_code) in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_provider_contract_root(root)
                path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
                values = yaml.safe_load(path.read_text(encoding="utf-8"))
                profile = next(
                    item
                    for item in values["work_profiles"]
                    if item["profile_id"] == "complex-implementation"
                )
                default = next(
                    item for item in profile["defaults"] if item["provider"] == "claude"
                )
                mutate(default)
                path.write_text(
                    yaml.safe_dump(values, sort_keys=False), encoding="utf-8"
                )
                bundle = contract.load_contract_bundle(root)
                codes = {
                    item.code
                    for item in contract.validate_contract_bundle(root, bundle)
                }
                self.assertIn(expected_code, codes)

    def test_active_contract_rejects_legacy_fallback_registry(self) -> None:
        mutations = {
            "registry": lambda document: document.__setitem__(
                "fallback_approvals", []
            ),
            "model-edge": lambda document: document["models"][0].__setitem__(
                "fallback", document["models"][1]["model_id"]
            ),
            "approval-reference": lambda document: document["models"][
                0
            ].__setitem__("fallback_approval", "fallback:claude:legacy"),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                shutil.copytree(
                    ROOT / "docs/00.agent-governance",
                    root / "docs/00.agent-governance",
                )
                path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
                document = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(document)
                path.write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                bundle = contract.load_contract_bundle(root)
                codes = {
                    item.code
                    for item in contract.validate_contract_bundle(root, bundle)
                }
                self.assertIn("AGC-SCHEMA-UNKNOWN-FIELD", codes)

    def test_model_sources_are_per_record_and_bound_to_retrieval_time(self) -> None:
        values = load_provider_contract()
        self.assertNotIn("cutoff_evidence", values)
        for model in values["models"]:
            with self.subTest(model=model["model_id"]):
                self.assertEqual(
                    values["retrieved_at"], model["source_retrieved_at"]
                )
                for field in (
                    "source_url",
                    "task_fit_source_url",
                    "reasoning_source_url",
                    "native_schema_source_url",
                ):
                    self.assertTrue(str(model[field]).startswith("https://"))

        mutations = {
            "observation-time": (
                lambda document: document["models"][0].__setitem__(
                    "source_retrieved_at", "2026-07-26T20:08:17+09:00"
                ),
                "AGC-SOURCE-OBSERVATION-ORDER",
            ),
            "invalid-source": (
                lambda document: document["models"][0].__setitem__(
                    "source_url", "not-a-url"
                ),
                "AGC-SOURCE-INVALID-URL",
            ),
            "legacy-registry": (
                lambda document: document.__setitem__("cutoff_evidence", []),
                "AGC-SCHEMA-UNKNOWN-FIELD",
            ),
        }
        for name, (mutate, expected_code) in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                shutil.copytree(
                    ROOT / "docs/00.agent-governance",
                    root / "docs/00.agent-governance",
                )
                path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
                document = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(document)
                path.write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                bundle = contract.load_contract_bundle(root)
                codes = {
                    item.code
                    for item in contract.validate_contract_bundle(root, bundle)
                }
                self.assertIn(expected_code, codes)

    def test_runtime_activation_requires_acceptance_and_entitlement(self) -> None:
        mutations = {
            "unverified-activation": (
                lambda model: model.__setitem__(
                    "runtime_activation_eligible", True
                ),
                True,
            ),
            "verified-activation": (
                lambda model: model.update(
                    {
                        "runtime_acceptance": "accepted",
                        "entitlement": "available",
                        "runtime_activation_eligible": True,
                    }
                ),
                False,
            ),
        }
        for name, (mutate, expect_finding) in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_provider_contract_root(root)
                path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
                values = yaml.safe_load(path.read_text(encoding="utf-8"))
                sonnet = next(
                    item
                    for item in values["models"]
                    if item["provider"] == "claude"
                    and item["model_id"] == "claude-sonnet-5"
                )
                mutate(sonnet)
                path.write_text(
                    yaml.safe_dump(values, sort_keys=False), encoding="utf-8"
                )

                bundle = contract.load_contract_bundle(root)
                codes = {
                    item.code
                    for item in contract.validate_contract_bundle(root, bundle)
                }
                self.assertIs(
                    expect_finding,
                    "AGC-MODEL-ACTIVATION-ELIGIBILITY" in codes,
                )

    def test_native_projection_contains_every_exact_owned_path(self) -> None:
        renderer = load_renderer()
        projection = expected_native_projection(self, renderer, ROOT)
        catalog = renderer.load_catalog(ROOT)
        expected = {
            *(
                pathlib.Path(".claude/agents") / f"{item.agent_id}.md"
                for item in catalog.agents
            ),
            *(
                pathlib.Path(".codex/agents") / f"{item.agent_id}.toml"
                for item in catalog.agents
            ),
            *(
                pathlib.Path(".gemini/agents") / f"{item.agent_id}.md"
                for item in catalog.agents
            ),
            *(
                pathlib.Path(".agents/agents") / f"{item.agent_id}.md"
                for item in catalog.agents
            ),
            *(
                pathlib.Path(".claude/skills") / item.function_id / "SKILL.md"
                for item in catalog.functions
            ),
            *(
                pathlib.Path(".agents/skills") / item.function_id / "SKILL.md"
                for item in catalog.functions
            ),
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
        selections = renderer._provider_selections(load_provider_contract())

        claude_base = {
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
            claude_text = projection[
                pathlib.Path(f".claude/agents/{agent.agent_id}.md")
            ].decode()
            claude_meta = yaml.safe_load(claude_text.split("---\n", 2)[1])
            claude_allowed = set(claude_base)
            selection = selections[(agent.work_profile, "claude")]
            if selection.control_value is not None:
                claude_allowed.add("effort")
                self.assertEqual(selection.control_value, claude_meta["effort"])
            self.assertEqual(claude_allowed, set(claude_meta))
            self.assertNotIn("thinking", claude_meta)
            self.assertEqual(agent.agent_id, claude_meta["name"])
            if agent.agent_id in read_only_ids:
                self.assertEqual("plan", claude_meta["permissionMode"])
                self.assertNotIn("Write", claude_meta["tools"])
                self.assertNotIn("Edit", claude_meta["tools"])

            codex = tomllib.loads(
                projection[
                    pathlib.Path(f".codex/agents/{agent.agent_id}.toml")
                ].decode()
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

            gemini_text = projection[
                pathlib.Path(f".gemini/agents/{agent.agent_id}.md")
            ].decode()
            gemini_meta = yaml.safe_load(gemini_text.split("---\n", 2)[1])
            self.assertEqual(gemini_allowed, set(gemini_meta))
            self.assertNotIn("sandbox", gemini_meta)
            if agent.agent_id in read_only_ids:
                self.assertNotIn("*", gemini_meta["tools"])
                self.assertNotIn("write_file", gemini_meta["tools"])
                self.assertNotIn("replace", gemini_meta["tools"])

    def test_every_generated_agent_local_link_resolves_from_its_projection(
        self,
    ) -> None:
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
                    resolved = (
                        ROOT / relative.parent / target.split("#", 1)[0]
                    ).resolve()
                    self.assertTrue(
                        resolved.is_relative_to(repository), relative.as_posix()
                    )
                    self.assertTrue(resolved.is_file(), f"{relative}: {target}")
                    checked_links += 1

            relative = pathlib.Path(f".codex/agents/{agent.agent_id}.toml")
            body = tomllib.loads(projection[relative].decode())[
                "developer_instructions"
            ]
            checked_agents += 1
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
                if target.startswith(("#", "/", "http://", "https://", "mailto:")):
                    continue
                resolved = (ROOT / relative.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(
                    resolved.is_relative_to(repository), relative.as_posix()
                )
                self.assertTrue(resolved.is_file(), f"{relative}: {target}")
                checked_links += 1

        self.assertEqual(56, checked_agents)
        self.assertEqual(224, checked_links)

    def test_native_hook_projection_preserves_event_semantics_and_time_units(
        self,
    ) -> None:
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
            self.assertIn(
                "${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}", command
            )
        for event in gemini["hooks"].values():
            command = event[0]["hooks"][0]["command"]
            self.assertIn(
                "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}", command
            )

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
        self.assertEqual(
            ".agents/skills/**/SKILL.md", providers["codex"]["native_skill_pattern"]
        )
        self.assertEqual(
            ".agents/skills/**/SKILL.md", providers["gemini"]["native_skill_pattern"]
        )
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
            self.assertIn(
                "Generated by scripts/operations/provider_surface_renderer.py", hook
            )
            self.assertIn("scripts/hooks/agent-event-hook.sh", hook)
        for event in values["semantic_events"]:
            for binding in event["provider_bindings"]:
                self.assertNotIn("blocking", binding)
                self.assertIn("provider_can_block", binding)
                self.assertIn(
                    binding["repository_hook_mode"],
                    {"advisory", "blocking", "deny-retry", "retry", "unsupported"},
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
            copy_provider_contract_root(root)
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
            self.assertEqual(
                [], contract.validate_repository(root, bundle, "providers")
            )

            codex_path = root / ".codex/agents/code-reviewer.toml"
            codex_path.write_text(
                codex_path.read_text(encoding="utf-8") + 'canonical_scope = "common"\n',
                encoding="utf-8",
            )
            findings = contract.validate_repository(root, bundle, "providers")
            self.assertIn(
                "AGC-PROVIDER-NATIVE-SCHEMA", {item.code for item in findings}
            )

    def test_repository_provider_section_blocks_exact_renderer_and_json_drift(
        self,
    ) -> None:
        renderer = load_renderer()
        mutations = (
            "unknown-json-key",
            "mutated-command",
            "rogue-agent",
            "mutated-agent-body",
            "scalar-handler",
        )
        for mutation in mutations:
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                copy_provider_contract_root(root)
                write_native_projection(self, renderer, root)
                if mutation == "unknown-json-key":
                    path = root / ".gemini/settings.json"
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["unknown"] = True
                    path.write_text(
                        json.dumps(value, indent=2) + "\n", encoding="utf-8"
                    )
                elif mutation == "mutated-command":
                    path = root / ".codex/hooks.json"
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["hooks"]["Stop"][0]["hooks"][0]["command"] = "true"
                    path.write_text(
                        json.dumps(value, indent=2) + "\n", encoding="utf-8"
                    )
                elif mutation == "rogue-agent":
                    path = root / ".claude/agents/rogue.md"
                    path.write_text("unowned role\n", encoding="utf-8")
                elif mutation == "mutated-agent-body":
                    path = root / ".claude/agents/code-reviewer.md"
                    path.write_text(
                        path.read_text(encoding="utf-8")
                        + "\nUnapproved instruction mutation.\n",
                        encoding="utf-8",
                    )
                else:
                    path = root / ".gemini/settings.json"
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["hooks"]["BeforeAgent"][0]["hooks"][0] = "invalid"
                    path.write_text(
                        json.dumps(value, indent=2) + "\n", encoding="utf-8"
                    )

                bundle = contract.load_contract_bundle(root)
                findings = contract.validate_repository(root, bundle, "providers")
                self.assertIn(
                    "AGC-PROVIDER-PROJECTION-DRIFT",
                    {item.code for item in findings},
                )

    def test_contract_rejects_removed_historical_model_fields(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            values = yaml.safe_load(path.read_text(encoding="utf-8"))
            sonnet = next(
                item
                for item in values["models"]
                if item["provider"] == "claude"
                and item["model_id"] == "claude-sonnet-5"
            )
            sonnet["fallback_approval"] = "fallback:claude:missing-edge"
            sonnet["cutoff_evidence_status"] = "verified-before-cutoff"
            sonnet["cutoff_evidence_id"] = "evidence:claude:missing"
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            findings = contract.validate_contract_bundle(root, bundle)
            unknown_locations = {
                item.location
                for item in findings
                if item.code == "AGC-SCHEMA-UNKNOWN-FIELD"
            }
            model_index = values["models"].index(sonnet)
            self.assertEqual(
                {
                    f"models[{model_index}].cutoff_evidence_id",
                    f"models[{model_index}].cutoff_evidence_status",
                    f"models[{model_index}].fallback_approval",
                },
                unknown_locations,
            )

    def test_gemini_adapter_translates_all_seven_native_event_outputs(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            adapter = pathlib.Path(directory) / "agent-event-hook.sh"
            adapter.write_bytes(renderer._render_gemini_hook())
            adapter.chmod(0o755)
            cases = {
                "SessionStart": ({}, {"systemMessage"}),
                "BeforeTool": ({"tool_name": "read_file", "tool_input": {}}, None),
                "AfterTool": ({"tool_name": "read_file", "tool_input": {}}, None),
                "SessionEnd": ({}, {"systemMessage"}),
                "AfterAgent": ({}, {"systemMessage"}),
                "BeforeAgent": ({"prompt": "prepare a PRD"}, {"hookSpecificOutput"}),
                "PreCompress": ({"trigger": "manual"}, {"systemMessage"}),
            }
            environment = dict(os.environ)
            environment["GEMINI_PROJECT_DIR"] = str(ROOT)
            environment["AGENT_ALLOW_UNCOMMITTED_STOP"] = "1"
            for event, (payload, required) in cases.items():
                with self.subTest(event=event):
                    result = subprocess.run(
                        ["bash", str(adapter), event],
                        input=json.dumps(payload),
                        capture_output=True,
                        text=True,
                        env=environment,
                        check=False,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)
                    output = json.loads(result.stdout or "{}")
                    if required is not None:
                        self.assertTrue(required.issubset(output))
                    if "hookSpecificOutput" in output:
                        self.assertEqual(
                            event, output["hookSpecificOutput"]["hookEventName"]
                        )
                    if event == "PreCompress":
                        self.assertTrue(
                            set(output).issubset({"systemMessage", "suppressOutput"})
                        )

    def test_codex_stop_denial_uses_native_retry_decision_and_reason(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "uncommitted.txt").write_text("dirty\n", encoding="utf-8")
            environment = dict(os.environ)
            environment["CODEX_PROJECT_DIR"] = str(root)
            environment["HY_HOME_HOOK_PROVIDER"] = "codex"
            result = subprocess.run(
                ["bash", str(ROOT / "scripts/hooks/agent-event-hook.sh"), "Stop"],
                input=json.dumps({"stop_hook_active": False}),
                capture_output=True,
                text=True,
                env=environment,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual("block", output["decision"])
            self.assertIsInstance(output["reason"], str)
            self.assertNotIn("continue", output)
            self.assertNotIn("stopReason", output)

    def test_codex_stop_retry_is_bounded_by_stop_hook_active(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "uncommitted.txt").write_text("dirty\n", encoding="utf-8")
            environment = dict(os.environ)
            environment["CODEX_PROJECT_DIR"] = str(root)
            environment["HY_HOME_HOOK_PROVIDER"] = "codex"
            result = subprocess.run(
                ["bash", str(ROOT / "scripts/hooks/agent-event-hook.sh"), "Stop"],
                input=json.dumps({"stop_hook_active": True}),
                capture_output=True,
                text=True,
                env=environment,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(False, output["continue"])
            self.assertIsInstance(output["stopReason"], str)
            self.assertNotIn("decision", output)

    def test_codex_stop_repository_mode_is_bound_to_retry_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(
                ROOT / "docs/00.agent-governance",
                root / "docs/00.agent-governance",
            )
            path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
            values = yaml.safe_load(path.read_text(encoding="utf-8"))
            stop = next(
                event
                for event in values["semantic_events"]
                if event["event_id"] == "stop"
            )
            codex = next(
                item
                for item in stop["provider_bindings"]
                if item["provider"] == "codex"
            )
            self.assertEqual("retry", codex["repository_hook_mode"])
            codex["repository_hook_mode"] = "advisory"
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            codes = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertIn("AGC-EVENT-SEMANTICS", codes)


if __name__ == "__main__":
    unittest.main()
