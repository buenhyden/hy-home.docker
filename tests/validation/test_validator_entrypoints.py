"""Behavioral smoke coverage for registered validation entrypoints."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from tests.lib.gate.subprocess_support import gate_root_pass_fds

ROOT = Path(__file__).resolve().parents[2]
PYTHON_ENTRYPOINTS = (
    "scripts/operations/provider_surface_renderer.py",
    "scripts/lib/agent_governance/agent_governance_contract.py",
    "scripts/validation/check-agent-governance-contract.py",
    "scripts/validation/check-document-corpus-lifecycle.py",
    "scripts/validation/check-document-metadata.py",
    "scripts/validation/check-github-workflow-contract.py",
    "scripts/validation/check-operations-catalog.py",
    "scripts/validation/check-supply-chain-policy.py",
    "scripts/lib/gate/ci_gate_contract.py",
    "scripts/validation/ci_gate_runner.py",
    "scripts/lib/gate/github_workflow_contract.py",
    "scripts/validation/run-ci-gate.py",
)
SHELL_ENTRYPOINTS = (
    "scripts/hardening/check-all-hardening.sh",
    "scripts/hooks/agent-event-hook.sh",
    "scripts/hooks/post-tool-validate.sh",
    "scripts/knowledge/report-graphify-health.sh",
    "scripts/operations/check-compose-core-readiness.sh",
    "scripts/operations/gen-secrets.sh",
    "scripts/operations/sync-tech-stack-versions.sh",
    "scripts/operations/use-qa-ci-tools.sh",
    "scripts/validation/check-candidate-preflight.sh",
    "scripts/validation/run-agent-precommit-all-files.sh",
    "scripts/validation/validate-docker-compose.sh",
)


class ValidatorEntrypointTests(unittest.TestCase):
    def test_ci_routing_explain_needs_no_site_packages(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-ES",
                "scripts/validation/run-ci-gate.py",
                "--profile",
                "changed",
                "--explain",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            pass_fds=gate_root_pass_fds(ROOT),
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("leaf.", completed.stdout)

    def test_python_entrypoints_expose_closed_cli_help(self) -> None:
        for entrypoint in PYTHON_ENTRYPOINTS:
            with self.subTest(entrypoint=entrypoint):
                completed = subprocess.run(
                    [sys.executable, entrypoint, "--help"],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    pass_fds=gate_root_pass_fds(ROOT),
                )
                self.assertEqual(0, completed.returncode, completed.stderr)

    def test_agent_descriptions_carry_role_routing_text(self) -> None:
        from scripts.operations import provider_surface_renderer as renderer

        for role in sorted((ROOT / ".agents/roles").glob("*.md")):
            with self.subTest(role=role.stem):
                source = renderer.compact_payload(role.read_text(encoding="utf-8"))
                overview = source.split("## Overview\n\n", 1)[1].split("\n\n", 1)[0]
                use_when = source.split("### Use When\n\n", 1)[1].split("\n\n", 1)[0]
                claude = (ROOT / ".claude/agents" / role.name).read_text(
                    encoding="utf-8"
                )
                codex = (ROOT / ".codex/agents" / f"{role.stem}.toml").read_text(
                    encoding="utf-8"
                )
                descriptions = (
                    json.loads(claude.split("\ndescription: ", 1)[1].split("\n", 1)[0]),
                    tomllib.loads(codex)["description"],
                )
                for description in descriptions:
                    self.assertIn(" ".join(overview.split()), description)
                    for case in use_when.split("\n- "):
                        case = " ".join(case.removeprefix("- ").split()).rstrip(".")
                        self.assertIn(case, description)

    def test_agent_description_keeps_wrapped_use_when_bullets(self) -> None:
        from scripts.operations import provider_surface_renderer as renderer

        text = (
            "# r\n\n## Overview\n\nDo the work.\n\n### Use When\n\n"
            "- First case wraps\n  onto a second line.\n- Second case.\n\n## Next\n"
        )
        role = renderer.RoleRecord(
            agent_id="r",
            scope="common",
            tier="worker",
            work_profile="adversarial-review",
            permission_profile="read-only",
            tool_profile="inspection",
            skill_ids=(),
            source_path=pathlib.PurePosixPath(".agents/roles/r.md"),
            source_text=text,
        )
        self.assertEqual(
            "Do the work. Use when: First case wraps onto a second line; Second case.",
            renderer._description(role),
        )

    def test_ci_gate_adapter_rejects_unadmitted_commands(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/lib/gate/ci_gate_adapters.py", "unadmitted"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
            pass_fds=gate_root_pass_fds(ROOT),
        )
        self.assertEqual(2, completed.returncode, completed.stderr)

    def test_shell_entrypoints_parse_without_execution(self) -> None:
        for entrypoint in SHELL_ENTRYPOINTS:
            with self.subTest(entrypoint=entrypoint):
                completed = subprocess.run(
                    ["bash", "-n", entrypoint],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    pass_fds=gate_root_pass_fds(ROOT),
                )
                self.assertEqual(0, completed.returncode, completed.stderr)

    def test_candidate_preflight_compares_against_the_origin_main_merge_base(
        self,
    ) -> None:
        """SPEC-0221: the local preflight runs both candidate checks or fails closed."""
        stub = '#!/usr/bin/env bash\necho "$0 $*" >> "$(dirname "$0")/../../calls"\nexit ${STUB_EXIT:-0}\n'

        def git(repo, *args):
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True,
                           env={"PATH": "/usr/bin:/bin", "GIT_CONFIG_GLOBAL": "/dev/null",
                                "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@invalid",
                                "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@invalid"})  # fmt: skip

        def run(repo, *args, metadata_exit=0, drift_exit=0):
            for name, code in (("validation/check-document-metadata.py", metadata_exit),
                               ("operations/sync-tech-stack-versions.sh", drift_exit)):  # fmt: skip
                path = repo / "scripts" / name
                path.write_text(stub.replace("${STUB_EXIT:-0}", str(code)))
                path.chmod(0o755)
            (repo / "calls").unlink(missing_ok=True)
            return subprocess.run(
                ["bash", str(repo / "scripts/validation/check-candidate-preflight.sh"), *args],
                cwd=repo, capture_output=True, text=True, timeout=30, check=False,
                env={"PATH": f"{repo}/bin:/usr/bin:/bin", "GIT_CONFIG_GLOBAL": "/dev/null"},
            )  # fmt: skip

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            for folder in ("scripts/validation", "scripts/operations", "bin"):
                (repo / folder).mkdir(parents=True)
            shutil.copy(ROOT / "scripts/validation/check-candidate-preflight.sh",
                        repo / "scripts/validation/check-candidate-preflight.sh")  # fmt: skip
            # python3 resolves to a shell stub so the fake validator runs as is.
            (repo / "bin/python3").write_text('#!/usr/bin/env bash\nexec bash "$@"\n')
            (repo / "bin/python3").chmod(0o755)
            git(repo, "init", "-q")
            git(repo, "add", ".")
            git(repo, "commit", "-qm", "base")

            missing = run(repo)
            self.assertEqual(2, missing.returncode)
            self.assertIn("no merge-base with origin/main", missing.stderr)

            git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
            refused = run(repo, "--skip")
            self.assertEqual(2, refused.returncode)
            self.assertIn("no arguments are accepted", refused.stderr)
            base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                                  capture_output=True, text=True).stdout.strip()  # fmt: skip
            passed = run(repo)
            self.assertEqual(0, passed.returncode, passed.stderr)
            calls = (repo / "calls").read_text()
            self.assertIn(f"--mode check-changed --base-ref {base}", calls)
            self.assertIn("sync-tech-stack-versions.sh --check", calls)
            self.assertEqual(1, run(repo, metadata_exit=1).returncode)
            self.assertEqual(1, run(repo, drift_exit=1).returncode)


class NativeTemplateProducerTests(unittest.TestCase):
    """P04: the real producer reads native payload, not a common wrapper."""

    def setUp(self) -> None:
        from scripts.lib.agent_governance.agent_governance_contract import (
            ProviderRecord,
        )
        from scripts.operations import provider_surface_renderer as renderer

        self.renderer = renderer
        self.role = renderer.RoleRecord(
            agent_id="fixture-reviewer",
            scope="common",
            tier="worker",
            work_profile="review",
            permission_profile="read-only",
            tool_profile="inspection",
            skill_ids=("fixture-procedure",),
            source_path=pathlib.PurePosixPath(".agents/roles/fixture-reviewer.md"),
            source_text=(
                '# fixture-reviewer\n\n## Overview\n\nReview "quoted" input.\n\n'
                "### Use When\n\n- A bounded review is needed.\n\n"
                "## Responsibilities\n\nKeep the source read-only.\n"
            ),
        )
        providers = tuple(
            ProviderRecord(
                provider_id=provider,
                capability_status="supported",
                adoption_status="adopted",
                runtime_acceptance="unobserved",
                adapter_path=pathlib.PurePosixPath(f".{provider}/provider.md"),
                agent_pattern=f".{provider}/agents/{{agent_id}}.{suffix}",
                skill_pattern=None,
                canonical_skill_pattern=".agents/skills/{skill_id}/SKILL.md",
                config_path=pathlib.PurePosixPath(f".{provider}/hooks.json"),
            )
            for provider, suffix in (("claude", "md"), ("codex", "toml"))
        )
        skill = renderer.SkillRecord(
            skill_id="fixture-procedure",
            scope="common",
            owner_agent="fixture-reviewer",
            description="A bounded fixture procedure.",
            source_path=pathlib.PurePosixPath(
                ".agents/skills/fixture-procedure/SKILL.md"
            ),
            source_text="# Fixture\n",
        )
        self.state = renderer.AgentGovernanceState(
            providers=("claude", "codex"),
            provider_records=providers,
            root_entries=(),
            provider_entries=(),
            roles=(self.role,),
            skills=(skill,),
            registry={
                "work_profiles": {
                    "review": {
                        "claude": {"model": "sonnet", "value": "high"},
                        "codex": {"model": "fixture-model", "value": "high"},
                    }
                },
                "permissions": {"read-only": {"claude": "plan", "codex": "read-only"}},
                "tool_profiles": {"inspection": ["Read", "Glob"]},
                "projections": [],
            },
        )
        folder = ROOT / "docs/99.templates/02.templates/92.runtime"
        self.claude = (folder / "claude-agent.template.md").read_text()
        self.codex = (folder / "codex-agent.template.toml").read_text()

    def test_claude_output_consumes_native_template_and_keeps_typed_fields(
        self,
    ) -> None:
        from scripts.lib.document_governance.frontmatter import parse_frontmatter_text

        source = self.claude + "\nNative fixture payload.\n"
        self.assertIn(
            "<!-- markdownlint-disable-next-line MD041 -->\n{{AGENT_BODY}}", source
        )
        content = self.renderer._claude_agent(
            self.state,
            self.role,
            pathlib.PurePosixPath(".claude/agents/fixture-reviewer.md"),
            template=source,
        ).decode()
        metadata = parse_frontmatter_text(content)
        self.assertEqual(
            {
                "name",
                "description",
                "tools",
                "model",
                "effort",
                "permissionMode",
                "skills",
            },
            set(metadata),
        )
        self.assertEqual(["Read", "Glob"], metadata["tools"])
        self.assertEqual(["fixture-procedure"], metadata["skills"])
        self.assertEqual("plan", metadata["permissionMode"])
        self.assertIn('Review "quoted" input.', metadata["description"])
        self.assertIn("Native fixture payload.", content)
        self.assertNotIn("## 문서 개요", content)
        self.assertNotIn("markdownlint-disable", content)
        self.assertIn(
            self.renderer._marker(self.role.source_path) + "\n\n# fixture-reviewer\n",
            content,
        )
        self.assertEqual(1, content.splitlines().count("# fixture-reviewer"))

    def test_optional_claude_effort_and_empty_skills_remain_native_values(self) -> None:
        from dataclasses import replace

        from scripts.lib.document_governance.frontmatter import parse_frontmatter_text

        state = replace(
            self.state,
            registry={
                **self.state.registry,
                "work_profiles": {
                    "review": {"claude": {"model": "sonnet", "value": None}}
                },
            },
        )
        role = replace(self.role, skill_ids=())
        content = self.renderer._claude_agent(
            state,
            role,
            pathlib.PurePosixPath(".claude/agents/fixture-reviewer.md"),
            template=self.claude,
        ).decode()
        metadata = parse_frontmatter_text(content)
        self.assertNotIn("effort", metadata)
        self.assertEqual([], metadata["skills"])

    def test_codex_output_consumes_native_template_and_escapes_instructions(
        self,
    ) -> None:
        source = self.codex.replace(
            "__AGENT_BODY__", "__AGENT_BODY__\\nNative fixture payload."
        )
        content = self.renderer._codex_agent(
            self.state,
            self.role,
            pathlib.PurePosixPath(".codex/agents/fixture-reviewer.toml"),
            template=source,
        ).decode()
        metadata = tomllib.loads(content)
        self.assertEqual(
            {
                "name",
                "description",
                "developer_instructions",
                "model",
                "model_reasoning_effort",
                "sandbox_mode",
            },
            set(metadata),
        )
        self.assertEqual("read-only", metadata["sandbox_mode"])
        self.assertIn('Review "quoted" input.', metadata["developer_instructions"])
        self.assertIn("Native fixture payload.", metadata["developer_instructions"])
        self.assertIn("## Required Procedures", metadata["developer_instructions"])
        self.assertNotIn("## 문서 개요", metadata["developer_instructions"])

    def test_native_templates_reject_unknown_keys_and_permission_overrides(
        self,
    ) -> None:
        cases = (
            ("claude", self.claude.replace("\n---\n", '\nowner: "intruder"\n---\n', 1)),
            (
                "claude",
                self.claude.replace('"{{PERMISSION_MODE}}"', '"bypassPermissions"'),
            ),
            ("codex", self.codex + 'permissionMode = "plan"\n'),
            ("codex", self.codex.replace('"__SANDBOX_MODE__"', '"danger-full-access"')),
        )
        for provider, source in cases:
            with self.subTest(provider=provider, source=source):
                render = getattr(self.renderer, f"_{provider}_agent")
                with self.assertRaises(ValueError):
                    render(
                        self.state,
                        self.role,
                        pathlib.PurePosixPath(f".{provider}/agents/fixture"),
                        template=source,
                    )

    def test_native_templates_require_one_active_standalone_role_payload(self) -> None:
        for provider, template, token, newline in (
            ("claude", self.claude, "{{AGENT_BODY}}", "\n"),
            ("codex", self.codex, "__AGENT_BODY__", "\\n"),
        ):
            for replacement in (
                "",
                token + newline + token,
                "```markdown" + newline + token + newline + "```",
                "~~~" + newline + token + newline + "~~~",
                "<!--" + newline + token + newline + "-->",
                "prefix " + token,
                "    " + token,
            ):
                with self.subTest(provider=provider, replacement=replacement):
                    render = getattr(self.renderer, f"_{provider}_agent")
                    with self.assertRaisesRegex(ValueError, "payload slot"):
                        render(
                            self.state,
                            self.role,
                            pathlib.PurePosixPath(f".{provider}/agents/fixture"),
                            template=template.replace(token, replacement),
                        )

    def test_render_all_reads_registered_payloads_once_per_native_kind(self) -> None:
        templates = {
            "governance/claude-agent": self.claude + "\nNative fixture payload.\n",
            "governance/codex-agent": self.codex.replace(
                "__AGENT_BODY__", "__AGENT_BODY__\\nNative fixture payload."
            ),
        }
        registry = object()
        with (
            mock.patch.object(
                self.renderer, "load_agent_governance", return_value=self.state
            ),
            mock.patch.object(
                self.renderer, "validate_contract_bundle", return_value=()
            ),
            mock.patch.object(self.renderer, "_folder_guides", return_value=()),
            mock.patch.object(self.renderer, "load_registry", return_value=registry),
            mock.patch.object(
                self.renderer,
                "template_payload",
                side_effect=lambda _registry, kind, *, root: templates[kind],
            ) as payload,
        ):
            records = self.renderer.render_all(Path("/fixture"))
        self.assertEqual(
            [
                mock.call(registry, "governance/claude-agent", root=Path("/fixture")),
                mock.call(registry, "governance/codex-agent", root=Path("/fixture")),
            ],
            payload.call_args_list,
        )
        self.assertTrue(
            all(b"Native fixture payload." in item.content for item in records)
        )
        self.assertTrue(
            all(item.path.parts[0] in {".claude", ".codex"} for item in records)
        )

    def test_wrapped_role_and_readme_keep_native_and_owned_boundaries(self) -> None:
        from dataclasses import replace

        from scripts.lib.document_governance.frontmatter import parse_frontmatter_text

        role = replace(
            self.role,
            source_text=self.renderer.wrap_document(self.role.source_text, kind="role"),
        )
        self.assertEqual(
            self.renderer._description(self.role), self.renderer._description(role)
        )
        native = self.renderer._codex_agent(
            self.state,
            role,
            pathlib.PurePosixPath(".codex/agents/fixture-reviewer.toml"),
            template=self.codex,
        )
        self.assertNotIn(
            "## 문서 개요", tomllib.loads(native.decode())["developer_instructions"]
        )
        pointer = self.renderer._pointer(
            "Codex Runtime Route",
            pathlib.PurePosixPath(".codex/provider.md"),
            pathlib.PurePosixPath(".codex/README.md"),
        )
        self.assertIn("## 문서 개요", pointer.decode())
        self.assertNotIn("\n\n\n", pointer.decode())
        self.assertEqual(
            "provider",
            parse_frontmatter_text(pointer.decode())["document_scope"]["layer"],
        )
        self.assertTrue(self.renderer._is_generated(pointer))


class FolderGuideShimTests(unittest.TestCase):
    """The renderer owns one `@AGENTS.md` import shim per tracked folder guide."""

    def setUp(self) -> None:
        from scripts.operations import provider_surface_renderer as renderer

        self.renderer = renderer
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for name in (
            ".agents",
            ".claude",
            ".codex",
            "docs/00.workspace",
            "docs/99.templates",
            "scripts/hooks",
        ):
            ignored = ["worktrees", "settings.local.json", "__pycache__"]
            if name == "docs/99.templates":
                # The real template dependencies are needed; unrelated folder
                # guide fixtures would add extra shims to these focused tests.
                ignored.extend(("AGENTS.md", "CLAUDE.md"))
            shutil.copytree(
                ROOT / name,
                self.root / name,
                ignore=shutil.ignore_patterns(*ignored),
            )
        (self.root / "AGENTS.md").write_text("# root\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("add", "-A")
        # Copied adapters may belong to the previous checked-in generation.
        # Establish current native output before introducing the tested guide.
        self.renderer.write_native_projection(self.root)
        (self.root / "docs/03.specs").mkdir(parents=True)
        (self.root / "docs/03.specs/AGENTS.md").write_text("# s\n", encoding="utf-8")
        self.git("add", "-A")

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.root, check=True, timeout=30)

    def findings(self) -> list[tuple[str, str]]:
        return [
            (item.path.as_posix(), item.kind)
            for item in self.renderer.find_native_projection_drift(self.root)
        ]

    def test_write_creates_checks_and_retires_the_shim(self) -> None:
        shim = self.root / "docs/03.specs/CLAUDE.md"
        self.assertEqual([("docs/03.specs/CLAUDE.md", "missing")], self.findings())
        self.renderer.write_native_projection(self.root)
        self.assertEqual(
            "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
            "source: docs/03.specs/AGENTS.md -->\n\n"
            "# docs/03.specs Folder Guide\n\n@AGENTS.md\n",
            shim.read_text(encoding="utf-8"),
        )
        self.assertFalse((self.root / "CLAUDE.md").exists())
        self.assertEqual([], self.findings())

        shim.write_text(shim.read_text(encoding="utf-8") + "extra\n", encoding="utf-8")
        self.assertEqual([("docs/03.specs/CLAUDE.md", "drift")], self.findings())
        self.renderer.write_native_projection(self.root)
        self.assertEqual([], self.findings())

        self.git("add", "-A")
        (self.root / "docs/03.specs/AGENTS.md").unlink()
        self.assertEqual(
            [("docs/03.specs/CLAUDE.md", "stale-generated")], self.findings()
        )
        with self.assertRaisesRegex(ValueError, "stale generated projections"):
            self.renderer.write_native_projection(self.root)
        self.assertFalse(shim.exists())

    def test_write_never_overwrites_a_hand_written_folder_claude_file(self) -> None:
        shim = self.root / "docs/03.specs/CLAUDE.md"
        shim.write_text("# Hand written\n", encoding="utf-8")
        self.assertEqual([("docs/03.specs/CLAUDE.md", "drift")], self.findings())
        with self.assertRaisesRegex(ValueError, "not a generated shim"):
            self.renderer.write_native_projection(self.root)
        self.assertEqual("# Hand written\n", shim.read_text(encoding="utf-8"))

    def test_only_tracked_regular_guides_outside_provider_homes_get_shims(
        self,
    ) -> None:
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        (Path(outside.name) / "AGENTS.md").write_text("# o\n", encoding="utf-8")
        for name in (".agents/x", ".claude/x", ".codex/x", "lab", "infra"):
            (self.root / name).mkdir(parents=True, exist_ok=True)
        for name in (".agents/x", ".claude/x", ".codex/x"):
            (self.root / name / "AGENTS.md").write_text("# p\n", encoding="utf-8")
        (self.root / "lab/AGENTS.md").symlink_to(Path(outside.name) / "AGENTS.md")
        self.git("add", "-A")
        (self.root / "infra/AGENTS.md").write_text("# untracked\n", encoding="utf-8")
        self.assertEqual(
            (pathlib.PurePosixPath("docs/03.specs/AGENTS.md"),),
            self.renderer._folder_guides(self.root),
        )

    def test_a_nested_folder_guide_gets_its_own_shim(self) -> None:
        nested = self.root / "docs/03.specs/0264-x"
        nested.mkdir()
        (nested / "AGENTS.md").write_text("# n\n", encoding="utf-8")
        self.git("add", "-A")
        self.assertIn(("docs/03.specs/0264-x/CLAUDE.md", "missing"), self.findings())
        self.renderer.write_native_projection(self.root)
        self.assertIn(
            "# docs/03.specs/0264-x Folder Guide\n\n@AGENTS.md\n",
            (nested / "CLAUDE.md").read_text(encoding="utf-8"),
        )
        self.assertEqual([], self.findings())
