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
                "    runtime_acceptance: rejected\n    runtime_acceptance: rejected\n",
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

    def test_model_observation_separates_cutoff_status_and_reasoning_policy(
        self,
    ) -> None:
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
        self.assertEqual(["high", "medium"], gemini["repository_reasoning_controls"])
        self.assertNotIn("model-selected", json.dumps(values, sort_keys=True))

        fable = models[("claude", "claude-fable-5")]
        mythos = models[("claude", "claude-mythos-5")]
        haiku = models[("claude", "claude-haiku-4-5-20251001")]
        opus = models[("claude", "claude-opus-4-8")]
        sonnet = models[("claude", "claude-sonnet-5")]
        self.assertEqual("adaptive-always-on", fable["thinking_control_kind"])
        self.assertEqual(["always-on-adaptive"], fable["supported_thinking_controls"])
        self.assertEqual("adaptive-always-on", mythos["thinking_control_kind"])
        self.assertEqual(["always-on-adaptive"], mythos["supported_thinking_controls"])
        self.assertEqual("extended-thinking", haiku["thinking_control_kind"])
        self.assertEqual(["extended-thinking"], haiku["supported_thinking_controls"])
        self.assertEqual("adaptive", opus["thinking_control_kind"])
        self.assertEqual(
            ["high", "low", "max", "medium", "xhigh"],
            opus["supported_effort_controls"],
        )
        self.assertEqual("adaptive-default", sonnet["thinking_control_kind"])
        self.assertEqual(
            ["adaptive", "disabled"], sonnet["supported_thinking_controls"]
        )

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
            self.assertIn(
                item["fallback_policy"], {"same-profile", "approved-degraded"}
            )
            if item["fallback_policy"] == "approved-degraded":
                self.assertEqual(
                    f"fallback:{item['provider']}:"
                    f"{item['model_id']}-to-{item['fallback']}",
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
                if item["provider"] == "claude" and item["model_id"] == "claude-fable-5"
            )
            fable["fallback_policy"] = "same-profile"
            fable["fallback_approval"] = None
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            observed = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertIn("AGC-MODEL-FALLBACK-POLICY", observed)

    def test_claude_controls_fallback_and_cutoff_evidence_are_typed(self) -> None:
        values = load_provider_contract()
        models = {
            (item["provider"], item["model_id"]): item for item in values["models"]
        }
        for model in values["models"]:
            self.assertIn("cutoff_evidence_id", model)
            self.assertNotIn("cutoff_evidence_url", model)
            self.assertNotIn("cutoff_evidence_observed_at", model)

        for model_id in ("claude-opus-4-8", "claude-sonnet-5"):
            model = models[("claude", model_id)]
            self.assertIn("thinking_control_kind", model)
            self.assertIn("supported_thinking_controls", model)
            self.assertEqual(
                ["high", "low", "max", "medium", "xhigh"],
                model["supported_effort_controls"],
            )
            self.assertNotIn("reasoning_control_kind", model)

        sonnet = models[("claude", "claude-sonnet-5")]
        self.assertEqual("claude-opus-4-8", sonnet["fallback"])
        self.assertEqual(
            "fallback:claude:claude-sonnet-5-to-claude-opus-4-8",
            sonnet["fallback_approval"],
        )

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

    def test_fallback_approval_registry_resolves_anchor_and_exact_edge(self) -> None:
        values = load_provider_contract()
        approvals = {item["approval_id"]: item for item in values["fallback_approvals"]}
        for model in values["models"]:
            if model["fallback_policy"] != "approved-degraded":
                self.assertIsNone(model["fallback_approval"])
                continue
            approval = approvals[model["fallback_approval"]]
            self.assertEqual(model["provider"], approval["provider"])
            self.assertEqual(model["model_id"], approval["source_model_id"])
            self.assertEqual(model["fallback"], approval["target_model_id"])
            self.assertEqual(model["work_profiles"], approval["work_profiles"])
            reference_path, anchor = approval["reference"].split("#", 1)
            self.assertTrue((ROOT / reference_path).is_file())
            self.assertEqual("approved-fallback-edges", anchor)

        mutations = {
            "missing": lambda document, model, approval: document[
                "fallback_approvals"
            ].remove(approval),
            "wrong-anchor": lambda document, model, approval: approval.__setitem__(
                "reference",
                "docs/03.specs/132-agent-governance-harness-convergence/spec.md#missing-edge-authority",
            ),
            "wrong-edge": lambda document, model, approval: approval.__setitem__(
                "target_model_id", model["model_id"]
            ),
        }
        expected_codes = {
            "missing": "AGC-MODEL-FALLBACK-APPROVAL-REFERENCE",
            "wrong-anchor": "AGC-MODEL-FALLBACK-APPROVAL-REFERENCE",
            "wrong-edge": "AGC-MODEL-FALLBACK-APPROVAL-EDGE",
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                shutil.copytree(
                    ROOT / "docs/00.agent-governance",
                    root / "docs/00.agent-governance",
                )
                spec_source = (
                    ROOT
                    / "docs/03.specs/132-agent-governance-harness-convergence/spec.md"
                )
                spec_target = root / spec_source.relative_to(ROOT)
                spec_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(spec_source, spec_target)
                path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
                document = yaml.safe_load(path.read_text(encoding="utf-8"))
                model = next(
                    item
                    for item in document["models"]
                    if item["fallback_policy"] == "approved-degraded"
                )
                approval = next(
                    item
                    for item in document["fallback_approvals"]
                    if item["approval_id"] == model["fallback_approval"]
                )
                mutate(document, model, approval)
                path.write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                bundle = contract.load_contract_bundle(root)
                codes = {
                    item.code
                    for item in contract.validate_contract_bundle(root, bundle)
                }
                self.assertIn(expected_codes[name], codes)

    def test_cutoff_evidence_registry_rejects_unofficial_or_backdated_claims(
        self,
    ) -> None:
        values = load_provider_contract()
        self.assertIn("cutoff_evidence", values)
        self.assertEqual([], values["cutoff_evidence"])
        for model in values["models"]:
            self.assertEqual(
                "historical-state-unverified", model["cutoff_evidence_status"]
            )
            self.assertIsNone(model["cutoff_evidence_id"])
            self.assertNotIn("cutoff_evidence_url", model)
            self.assertNotIn("cutoff_evidence_observed_at", model)
        gpt_56 = next(
            item
            for item in values["models"]
            if item["provider"] == "codex" and item["model_id"] == "gpt-5.6"
        )
        self.assertIsNone(gpt_56["cutoff_evidence_id"])

        mutations = {
            "unofficial-source": {
                "source_url": "https://example.com/provider-model-history",
                "published_at": "2026-07-09T10:00:00+09:00",
                "observed_at": values["retrieved_at"],
                "code": "AGC-MODEL-CUTOFF-EVIDENCE-SOURCE",
            },
            "backdated-observation": {
                "source_url": "https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions",
                "published_at": "2026-07-09T10:00:00+09:00",
                "observed_at": "2026-07-09T10:00:00+09:00",
                "code": "AGC-MODEL-CUTOFF-EVIDENCE-DATE",
            },
            "post-cutoff-publication": {
                "source_url": "https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions",
                "published_at": "2026-07-11T10:00:00+09:00",
                "observed_at": values["retrieved_at"],
                "code": "AGC-MODEL-CUTOFF-EVIDENCE-DATE",
            },
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                shutil.copytree(
                    ROOT / "docs/00.agent-governance",
                    root / "docs/00.agent-governance",
                )
                path = root / "docs/00.agent-governance/contracts/provider-models.yaml"
                document = yaml.safe_load(path.read_text(encoding="utf-8"))
                model = next(
                    item
                    for item in document["models"]
                    if item["provider"] == "claude"
                    and item["model_id"] == "claude-sonnet-5"
                )
                evidence_id = "evidence:claude-sonnet-5-before-cutoff"
                model["cutoff_evidence_status"] = "verified-before-cutoff"
                model["cutoff_evidence_id"] = evidence_id
                document["cutoff_evidence"].append(
                    {
                        "evidence_id": evidence_id,
                        "provider": "claude",
                        "source_url": mutation["source_url"],
                        "published_at": mutation["published_at"],
                        "observed_at": mutation["observed_at"],
                    }
                )
                path.write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                bundle = contract.load_contract_bundle(root)
                codes = {
                    item.code
                    for item in contract.validate_contract_bundle(root, bundle)
                }
                self.assertIn(mutation["code"], codes)

    def test_cutoff_evidence_registry_accepts_official_dated_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
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
            evidence_id = "evidence:claude:sonnet-5-before-cutoff"
            sonnet["cutoff_evidence_status"] = "verified-before-cutoff"
            sonnet["cutoff_evidence_id"] = evidence_id
            values["cutoff_evidence"].append(
                {
                    "evidence_id": evidence_id,
                    "provider": "claude",
                    "source_url": "https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions",
                    "published_at": "2026-07-09T10:00:00+09:00",
                    "observed_at": values["retrieved_at"],
                }
            )
            path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

            bundle = contract.load_contract_bundle(root)
            codes = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertFalse(
                {
                    "AGC-MODEL-CUTOFF-EVIDENCE-DATE",
                    "AGC-MODEL-CUTOFF-EVIDENCE-REFERENCE",
                    "AGC-MODEL-CUTOFF-EVIDENCE-SOURCE",
                }.intersection(codes)
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
            if agent.work_profile in {"complex-implementation", "supervision"}:
                claude_allowed.add("effort")
                self.assertEqual("high", claude_meta["effort"])
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

    def test_contract_rejects_unbound_fallback_approval_and_cutoff_evidence(
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
            codes = {
                item.code for item in contract.validate_contract_bundle(root, bundle)
            }
            self.assertTrue(
                {
                    "AGC-MODEL-CUTOFF-EVIDENCE-REFERENCE",
                    "AGC-MODEL-FALLBACK-APPROVAL-REFERENCE",
                }.issubset(codes)
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
