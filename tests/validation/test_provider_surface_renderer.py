from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
import unittest
from dataclasses import replace
from types import SimpleNamespace
from unittest import mock

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
RENDERER = ROOT / "scripts/operations/provider_surface_renderer.py"


def _child_env() -> dict[str, str]:
    """Return an environment for a non-gate subprocess owned by this test."""

    environment = dict(os.environ)
    environment.pop("HYHOME_CI_GATE_ROOT", None)
    return environment


def load_renderer():
    spec = importlib.util.spec_from_file_location("provider_surface_renderer", RENDERER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {RENDERER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _copy_registered_file(
    source_root: pathlib.Path, root: pathlib.Path, name: str
) -> None:
    """Read only a bounded regular registered fixture, without following links."""
    relative = pathlib.PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe fixture path: {name}")
    descriptor = os.open(source_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        parts = pathlib.PurePosixPath(name).parts
        for part in parts[:-1]:
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor
            )
            os.close(descriptor)
            descriptor = child
        source = os.open(
            parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor
        )
        with os.fdopen(source, "rb") as handle:
            before = os.fstat(handle.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise ValueError(f"unsafe fixture input: {name}")
            payload = handle.read(8 * 1024 * 1024 + 1)
            after = os.fstat(handle.fileno())
            if len(payload) > 8 * 1024 * 1024 or (
                before.st_size,
                before.st_mtime_ns,
                before.st_ctime_ns,
            ) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise ValueError(f"unstable or oversized fixture input: {name}")
    finally:
        os.close(descriptor)
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    target.chmod(stat.S_IMODE(before.st_mode))


def copy_fixture(root: pathlib.Path) -> None:
    from scripts.lib.agent_governance.agent_governance_contract import (
        canonical_source_paths,
        validate_canonical_agent_home,
    )

    findings = validate_canonical_agent_home(ROOT)
    if findings:
        raise ValueError(f"invalid canonical fixture inventory: {findings}")
    native_paths = (
        subprocess.run(
            ["git", "ls-files", "-z", "--", ".claude", ".codex"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .split("\0")
    )
    native_pattern = re.compile(
        r"(?:[.]claude/agents/[a-z0-9-]+[.]md|[.]codex/agents/[a-z0-9-]+[.]toml|"
        r"[.]claude/skills/[a-z0-9-]+/SKILL[.]md|[.]claude/hooks/[a-z0-9-]+[.]sh|"
        r"[.]claude/output-styles/hy-home[.]md|"
        r"[.]claude/(?:README[.]md|CLAUDE[.]md|settings[.]json)|"
        r"[.]codex/(?:README[.]md|hooks[.]json))"
    )
    names = {name for name in native_paths if native_pattern.fullmatch(name)}
    names.update(
        {
            ".agents/README.md",
            ".agents/governance/providers/README.md",
            ".agents/governance/providers/registry.yaml",
            ".claude/provider.md",
            ".codex/provider.md",
            "scripts/hooks/agent-event-hook.sh",
        }
    )
    names.update(path.as_posix() for path in canonical_source_paths(ROOT))
    for name in sorted(names):
        _copy_registered_file(ROOT, root, name)


def mutate_registry(root: pathlib.Path, mutation) -> None:
    path = root / ".agents/governance/providers/registry.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutation(data)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def clear_generated_quarantine(test_case, renderer, root: pathlib.Path) -> None:
    quarantine = root / renderer.QUARANTINE_ROOT
    quarantined = tuple(quarantine.iterdir())
    test_case.assertTrue(quarantined)
    for path in quarantined:
        test_case.assertTrue(renderer._is_generated(path.read_bytes()))
        path.unlink()
    quarantine.rmdir()


def parse_frontmatter(payload: bytes) -> dict[str, object]:
    text = payload.decode("utf-8")
    _prefix, frontmatter, _body = text.split("---", 2)
    parsed = yaml.safe_load(frontmatter)
    if not isinstance(parsed, dict):
        raise AssertionError("generated frontmatter is not a mapping")
    return parsed


class ProviderSurfaceRendererTests(unittest.TestCase):
    def test_role_tools_come_from_the_registry_not_the_renderer(self) -> None:
        """A role owns which tools it may use.

        The renderer used to infer the list from the two-value permission enum,
        which made this generated projection the owner of role intent and gave
        every workspace-write role the same tools whatever it does. Each role
        declares a `tool_profile`; the registry maps it; the renderer only
        looks it up.
        """

        import yaml

        root = pathlib.Path(__file__).resolve().parents[2]
        registry = yaml.safe_load(
            (root / ".agents/governance/providers/registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        profiles = registry["tool_profiles"]
        self.assertTrue(profiles, "the registry must own at least one tool profile")

        # No two profiles may carry the same tool list: a distinction that
        # changes nothing is a distinction that will drift.
        rendered = {name: tuple(tools) for name, tools in profiles.items()}
        self.assertEqual(
            len(set(rendered.values())), len(rendered), "tool profiles must differ"
        )

        for role_path in sorted((root / ".agents/roles").glob("*.md")):
            text = role_path.read_text(encoding="utf-8")
            match = re.search(r'^tool_profile: "([^"]+)"', text, re.M)
            with self.subTest(role=role_path.stem):
                self.assertIsNotNone(match, "every role declares a tool profile")
                assert match is not None
                profile = match.group(1)
                self.assertIn(profile, profiles)
                agent = (root / ".claude/agents" / f"{role_path.stem}.md").read_text(
                    encoding="utf-8"
                )
                declared = re.findall(r'^- "([A-Za-z]+)"$', agent, re.M)
                self.assertEqual(
                    list(profiles[profile]),
                    declared[: len(profiles[profile])],
                    "the rendered adapter must carry exactly the profile's tools",
                )

    def test_an_observation_role_can_reach_runtime_a_reviewer_cannot(self) -> None:
        """`drift-detector` compares declared configuration with observed state.

        With the inspection tool set it could read files and nothing else, so it
        could not observe the runtime its own definition is about. It is the one
        read-only role that needs to run a non-mutating command, and separating
        `observation` from `inspection` is what lets it say so without also
        gaining write access.
        """

        import yaml

        root = pathlib.Path(__file__).resolve().parents[2]
        registry = yaml.safe_load(
            (root / ".agents/governance/providers/registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("Bash", registry["tool_profiles"]["observation"])
        self.assertNotIn("Bash", registry["tool_profiles"]["inspection"])
        self.assertNotIn("Write", registry["tool_profiles"]["observation"])

        agent = (root / ".claude/agents/drift-detector.md").read_text(encoding="utf-8")
        self.assertIn('- "Bash"', agent)
        # Read-only permission still gates every mutation.
        self.assertIn('permissionMode: "plan"', agent)

    def test_empty_agent_home_is_not_a_valid_canonical_source(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / ".agents").mkdir()
            self.assertTrue(renderer.validate_canonical_agent_home(root))

    def test_claude_skill_is_explicit_thin_adapter(self) -> None:
        renderer = load_renderer()
        skill = renderer.SkillRecord(
            skill_id="sample",
            scope="common",
            owner_agent="code-reviewer",
            description="Use when explicitly reviewing the sample.",
            source_path=pathlib.PurePosixPath(".agents/skills/sample/SKILL.md"),
            source_text="---\nname: sample\n---\n\nSecret canonical procedure body.\n",
        )
        payload = renderer._skill(
            skill, pathlib.PurePosixPath(".claude/skills/sample/SKILL.md")
        )
        metadata = parse_frontmatter(payload)
        body = payload.decode("utf-8").split("---", 2)[2]
        visible_body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).lstrip()
        self.assertTrue(visible_body.startswith("# sample\n"))
        self.assertIs(metadata.get("disable-model-invocation"), True)
        self.assertNotIn("allowed-tools", metadata)
        self.assertNotIn(b"Secret canonical procedure body", payload)
        self.assertIn(b"../../../.agents/skills/sample/SKILL.md", payload)

    def test_cli_preserves_read_only_canonical_agent_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            canonical = root / ".agents"
            before = {
                path.relative_to(root): path.read_bytes()
                for path in canonical.rglob("*")
                if path.is_file()
            }
            canonical.chmod(0o555)
            for mode in ("--check", "--write", "--write"):
                with self.subTest(mode=mode):
                    result = subprocess.run(
                        [sys.executable, str(RENDERER), mode, "--root", str(root)],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=15,
                        env=_child_env(),
                    )
                    self.assertEqual(
                        0, result.returncode, result.stdout + result.stderr
                    )
                    self.assertEqual(
                        before,
                        {
                            path.relative_to(root): path.read_bytes()
                            for path in canonical.rglob("*")
                            if path.is_file()
                        },
                    )
                    self.assertEqual(0o555, canonical.stat().st_mode & 0o777)
                    self.assertFalse((root / ".codex/skills").exists())

    def test_cli_rejects_unknown_canonical_input_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            unowned = root / ".agents/unowned.md"
            unowned.write_bytes(b"user-owned content\n")
            projection = root / ".codex/agents/code-reviewer.toml"
            original = projection.read_bytes() + b"\n# local drift\n"
            projection.write_bytes(original)
            for mode in ("--check", "--write"):
                with self.subTest(mode=mode):
                    result = subprocess.run(
                        [sys.executable, str(RENDERER), mode, "--root", str(root)],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=15,
                        env=_child_env(),
                    )
                    self.assertEqual(
                        1, result.returncode, result.stdout + result.stderr
                    )
                    self.assertIn("AGC-CANONICAL-HOME", result.stderr)
                    self.assertEqual(b"user-owned content\n", unowned.read_bytes())
                    self.assertEqual(original, projection.read_bytes())
                    self.assertFalse((root / ".provider-surface-quarantine").exists())

    def test_write_fixedpoint_preserves_sources_and_native_controls(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            protected = [
                *list((root / ".agents").rglob("*")),
                root / ".claude/provider.md",
                root / ".codex/provider.md",
                root / ".claude/settings.json",
                root / ".codex/hooks.json",
            ]
            before = {path: path.read_bytes() for path in protected if path.is_file()}
            renderer.write_native_projection(root)
            expected = renderer.expected_native_projection(root)
            first = {path: (root / path).read_bytes() for path in expected}
            renderer.write_native_projection(root)
            self.assertEqual(
                first, {path: (root / path).read_bytes() for path in expected}
            )
            self.assertEqual(before, {path: path.read_bytes() for path in before})
            self.assertEqual([], renderer.find_native_projection_drift(root))
            self.assertFalse((root / ".codex/config.toml").exists())
            self.assertFalse((root / ".provider-surface-quarantine").exists())

    def test_renderer_independently_rejects_canonical_outputs(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            state = renderer.load_agent_governance(root)
            for kind in ("role", "skill", "static", "managed-root"):
                with self.subTest(kind=kind):
                    registry = dict(state.registry)
                    providers = list(state.provider_records)
                    if kind == "role":
                        providers[0] = replace(
                            providers[0], agent_pattern=".agents/roles/{agent_id}.md"
                        )
                    elif kind == "skill":
                        providers[0] = replace(
                            providers[0],
                            skill_pattern=".agents/skills/{skill_id}/SKILL.md",
                        )
                    elif kind == "static":
                        registry["projections"] = [
                            {
                                "provider_id": "claude",
                                "path": ".agents/README.md",
                                "source": ".claude/provider.md",
                            }
                        ]
                    else:
                        registry["generated_roots"] = [".agents/skills"]
                    changed = replace(
                        state, registry=registry, provider_records=tuple(providers)
                    )
                    if kind == "managed-root":
                        with self.assertRaises(ValueError):
                            renderer._managed_roots(changed)
                    else:
                        with mock.patch.object(
                            renderer, "load_agent_governance", return_value=changed
                        ):
                            with self.assertRaisesRegex(ValueError, "native output"):
                                renderer.render_all(root)

    def test_native_provider_source_output_cycles_are_rejected(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            before = (root / ".claude/provider.md").read_bytes()
            mutate_registry(
                root,
                lambda data: data["projections"][0].update(
                    {"path": ".claude/provider.md"}
                ),
            )
            with self.assertRaises(renderer.ContractLoadError):
                renderer.write_native_projection(root)
            self.assertEqual(before, (root / ".claude/provider.md").read_bytes())

    def test_rebased_links_preserve_targets_queries_and_fragments(self) -> None:
        renderer = load_renderer()
        source = pathlib.PurePosixPath(".agents/roles/code-reviewer.md")
        output = pathlib.PurePosixPath(".codex/agents/code-reviewer.toml")
        text = (
            '[Policy](../governance/agentic.md?q=1#scope "title")\n'
            "[reference]: <../skills/code-review-dimensions/SKILL.md#inputs>\n"
            "[external](https://example.com/read?q=1#part) [local](#inputs)\n"
        )
        rendered = renderer._rebase_links(text, source, output)
        self.assertIn('../../.agents/governance/agentic.md?q=1#scope "title"', rendered)
        self.assertIn(
            "<../../.agents/skills/code-review-dimensions/SKILL.md#inputs>", rendered
        )
        self.assertIn(
            "[external](https://example.com/read?q=1#part) [local](#inputs)", rendered
        )
        with self.assertRaisesRegex(ValueError, "escapes"):
            renderer._rebase_links("[escape](../../../outside.md)", source, output)

    def test_tracked_static_inventory_is_path_metadata_only(self) -> None:
        renderer = load_renderer()
        result = subprocess.CompletedProcess(
            [],
            0,
            stdout=(
                b".claude/README.md\0.codex/README.md\0.claude/settings.local.json\0"
                b".claude/agents/reviewer.md\0.codex/provider.md\0.agents/README.md\0"
            ),
        )
        with mock.patch.object(renderer, "run_bounded_git", return_value=result):
            paths = renderer._tracked_static_paths(ROOT)
        self.assertEqual(
            (
                pathlib.PurePosixPath(".claude/README.md"),
                pathlib.PurePosixPath(".codex/README.md"),
            ),
            paths,
        )

    def test_tracked_static_inventory_rejects_unterminated_or_excessive_paths(
        self,
    ) -> None:
        renderer = load_renderer()
        for payload in (b".codex/README.md", b".codex/README.md\0\0", b"x\0" * 4097):
            with self.subTest(payload_size=len(payload)):
                result = subprocess.CompletedProcess([], 0, stdout=payload)
                with mock.patch.object(
                    renderer, "run_bounded_git", return_value=result
                ):
                    with self.assertRaises(ValueError):
                        renderer._tracked_static_paths(ROOT)

    def test_tracked_static_reader_bounds_noisy_and_stalled_children(self) -> None:
        from scripts.lib.document_governance import git_provenance

        renderer = load_renderer()
        real_popen = subprocess.Popen
        programs = (
            "import os\nwhile True: os.write(1, b'x' * 65536)",
            "import time; time.sleep(60)",
        )
        for program in programs:
            with (
                self.subTest(program=program),
                tempfile.TemporaryDirectory() as directory,
            ):
                children = []

                def spawn(_argv, **kwargs):
                    child = real_popen([sys.executable, "-c", program], **kwargs)
                    children.append(child)
                    return child

                with (
                    mock.patch.object(
                        git_provenance.subprocess, "Popen", side_effect=spawn
                    ),
                    mock.patch.object(git_provenance, "_GIT_TIMEOUT_SECONDS", 0.5),
                ):
                    with self.assertRaisesRegex(ValueError, "inventory is unavailable"):
                        renderer._tracked_static_paths(pathlib.Path(directory))
                self.assertEqual(1, len(children))
                self.assertIsNotNone(children[0].poll())

    def test_static_scan_never_reads_untracked_native_payloads(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for name in (
                ".claude/settings.local.json",
                ".claude/RESUME.md",
                ".codex/private.md",
            ):
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(b"private synthetic input")
            state = SimpleNamespace(
                provider_records=tuple(
                    SimpleNamespace(
                        agent_pattern=f".{provider}/agents/{{agent_id}}.md",
                        skill_pattern=None,
                    )
                    for provider in ("claude", "codex")
                ),
                registry={"projections": []},
            )
            with (
                mock.patch.object(
                    renderer,
                    "_owned_projection_identity_at",
                    wraps=renderer._owned_projection_identity_at,
                ) as owned,
                mock.patch.object(
                    renderer,
                    "_read_projection_prefix_at",
                    wraps=renderer._read_projection_prefix_at,
                ) as prefix,
            ):
                self.assertEqual(
                    (), renderer._current_static_generated_files(root, state)
                )
            self.assertEqual([], owned.call_args_list)
            self.assertEqual([], prefix.call_args_list)

    def test_fixture_reader_rejects_links_and_nonregular_inputs(self) -> None:
        for kind in ("symlink", "parent-symlink", "fifo", "oversized"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                source = pathlib.Path(directory) / "source"
                target = pathlib.Path(directory) / "target"
                source.mkdir()
                (source / "real").mkdir()
                (source / "real/input").write_bytes(b"fixture")
                if kind == "symlink":
                    (source / "input").symlink_to(source / "real/input")
                    name = "input"
                elif kind == "parent-symlink":
                    (source / "alias").symlink_to(
                        source / "real", target_is_directory=True
                    )
                    name = "alias/input"
                elif kind == "fifo":
                    os.mkfifo(source / "input")
                    name = "input"
                else:
                    (source / "input").write_bytes(b"x" * (8 * 1024 * 1024 + 1))
                    name = "input"
                with self.assertRaises((OSError, ValueError)):
                    _copy_registered_file(source, target, name)
                self.assertFalse(target.exists())

    def test_static_projection_routes_follow_registry_data(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            registry_path = root / ".agents/governance/providers/registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            self.assertIn("projections", registry)
            registry["projections"][2]["path"] = ".codex/ROUTE.md"
            registry_path.write_text(
                yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
            )

            projection = renderer.expected_native_projection(root)

            self.assertIn(pathlib.Path(".codex/ROUTE.md"), projection)
            self.assertNotIn(pathlib.Path(".codex/README.md"), projection)

    def test_dynamic_yaml_scalars_are_quoted_in_role_and_skill_projections(
        self,
    ) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            for relative, original in (
                ("roles/code-reviewer.md", 'scope: "common"'),
                ("skills/adr-writing/SKILL.md", None),
            ):
                path = root / ".agents" / relative
                text = path.read_text(encoding="utf-8")
                if original is None:
                    _prefix, frontmatter, body = text.split("---", 2)
                    values = yaml.safe_load(frontmatter)
                    values["description"] = "Canonical x: injected procedure"
                    text = (
                        "---\n" + yaml.safe_dump(values, sort_keys=False) + "---" + body
                    )
                else:
                    self.assertIn(original, text)
                    text = text.replace(original, "scope: 'x: injected'", 1)
                path.write_text(text, encoding="utf-8")

            def unsafe_but_valid_scalars(data):
                model = data["models"].pop("claude-opus-5")
                model["supported_values"] = [
                    "high: injected" if value == "high" else value
                    for value in model["supported_values"]
                ]
                data["models"]["evil: true"] = model
                for profile in data["work_profiles"].values():
                    selection = profile["claude"]
                    if selection["model"] == "claude-opus-5":
                        selection["model"] = "evil: true"
                    if (
                        selection["model"] == "evil: true"
                        and selection["value"] == "high"
                    ):
                        selection["value"] = "high: injected"

            mutate_registry(root, unsafe_but_valid_scalars)
            projection = renderer.expected_native_projection(root)
            claude_role = parse_frontmatter(
                projection[pathlib.Path(".claude/agents/code-reviewer.md")]
            )
            claude_skill = parse_frontmatter(
                projection[pathlib.Path(".claude/skills/adr-writing/SKILL.md")]
            )

            self.assertIn("Canonical x: injected role", claude_role["description"])
            self.assertEqual("evil: true", claude_role["model"])
            self.assertEqual("high: injected", claude_role["effort"])
            self.assertIn(
                "Canonical x: injected procedure", claude_skill["description"]
            )

    def test_write_rejects_static_projection_over_native_config(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            settings = root / ".claude/settings.json"
            before = settings.read_bytes()
            mutate_registry(
                root,
                lambda data: data["projections"][1].update(
                    {"path": ".claude/settings.json"}
                ),
            )

            with self.assertRaises(renderer.ContractLoadError):
                renderer.write_native_projection(root)

            self.assertEqual(before, settings.read_bytes())

    def test_static_projection_route_change_or_removal_converges_without_legacy_copy(
        self,
    ) -> None:
        renderer = load_renderer()
        renderer._tracked_static_paths = mock.Mock(
            return_value=(pathlib.PurePosixPath(".codex/README.md"),)
        )
        for case in ("change", "remove"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                old_path = root / ".codex/README.md"
                if case == "change":
                    mutate_registry(
                        root,
                        lambda data: data["projections"][2].update(
                            {"path": ".codex/ROUTE.md"}
                        ),
                    )
                else:
                    mutate_registry(root, lambda data: data["projections"].pop(2))

                self.assertIn(
                    renderer.Finding(
                        pathlib.PurePosixPath(".codex/README.md"),
                        "stale-generated",
                    ),
                    renderer.find_native_projection_drift(root),
                )
                with self.assertRaisesRegex(ValueError, "manual cleanup required"):
                    renderer.write_native_projection(root)
                self.assertFalse(old_path.exists())
                clear_generated_quarantine(self, renderer, root)
                renderer.write_native_projection(root)
                self.assertEqual([], renderer.find_native_projection_drift(root))
                if case == "change":
                    self.assertTrue((root / ".codex/ROUTE.md").is_file())

    def test_removed_codex_role_projection_converges(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            retired = pathlib.PurePosixPath(".codex/agents/retired-role.toml")
            (root / retired).write_bytes(
                (root / ".codex/agents/code-reviewer.toml").read_bytes()
            )

            self.assertIn(
                renderer.Finding(retired, "stale-generated"),
                renderer.find_native_projection_drift(root),
            )
            with self.assertRaisesRegex(ValueError, "manual cleanup required"):
                renderer.write_native_projection(root)
            self.assertFalse((root / retired).exists())
            clear_generated_quarantine(self, renderer, root)
            renderer.write_native_projection(root)
            self.assertEqual([], renderer.find_native_projection_drift(root))

    def test_removed_large_codex_role_projection_converges(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            retired = pathlib.PurePosixPath(".codex/agents/retired-large-role.toml")
            values = {
                "name": "retired-large-role",
                "description": (
                    "Canonical common role for retired-large-role; owned by canonical agent governance."
                ),
                "developer_instructions": (
                    "# Generated by scripts/operations/provider_surface_renderer.py; "
                    "source: .agents/roles/retired-large-role.md\n\n" + "x" * 9_000
                ),
                "model": "gpt-5.6-sol",
                "model_reasoning_effort": "high",
                "sandbox_mode": "read-only",
            }
            (root / retired).write_bytes(
                "".join(
                    f"{key} = {json.dumps(value)}\n" for key, value in values.items()
                ).encode()
            )

            self.assertIn(
                renderer.Finding(retired, "stale-generated"),
                renderer.find_native_projection_drift(root),
            )
            with self.assertRaisesRegex(ValueError, "manual cleanup required"):
                renderer.write_native_projection(root)
            self.assertFalse((root / retired).exists())
            clear_generated_quarantine(self, renderer, root)
            renderer.write_native_projection(root)
            self.assertEqual([], renderer.find_native_projection_drift(root))

    def test_check_rejects_expected_static_projection_symlink(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            target = root / ".codex/README.md"
            outside = root / "outside-generated.md"
            outside.write_bytes(target.read_bytes())
            target.unlink()
            target.symlink_to(outside)

            self.assertIn(
                renderer.Finding(pathlib.PurePosixPath(".codex/README.md"), "unsafe"),
                renderer.find_native_projection_drift(root),
            )

    def test_check_does_not_hash_oversized_unowned_namespace_file(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            oversized = pathlib.PurePosixPath(".codex/unowned-large.bin")
            (root / oversized).write_bytes(b"x" * 16_384)
            real_identity = renderer._owned_projection_identity_at

            def guarded_identity(parent_descriptor, relative):
                if relative == oversized:
                    self.fail("oversized unowned namespace file was hashed")
                return real_identity(parent_descriptor, relative)

            with mock.patch.object(
                renderer,
                "_owned_projection_identity_at",
                side_effect=guarded_identity,
            ):
                findings = renderer.find_native_projection_drift(root)

            self.assertNotIn(oversized, {finding.path for finding in findings})

    def test_owned_projection_identity_opens_fifo_nonblocking(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            fifo = root / "candidate"
            os.mkfifo(fifo)
            parent = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            real_open = renderer.os.open

            def require_nonblocking(path, flags, *args, **kwargs):
                if path == fifo.name:
                    self.assertTrue(flags & os.O_NONBLOCK)
                return real_open(path, flags, *args, **kwargs)

            try:
                with mock.patch.object(
                    renderer.os,
                    "open",
                    side_effect=require_nonblocking,
                ):
                    with self.assertRaisesRegex(ValueError, "unowned"):
                        renderer._owned_projection_identity_at(
                            parent, pathlib.PurePosixPath(fifo.name)
                        )
            finally:
                os.close(parent)

    def test_oversized_static_generated_pointer_is_detected_and_quarantined(
        self,
    ) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            stale = pathlib.PurePosixPath(".codex/STALE.md")
            renderer._tracked_static_paths = mock.Mock(return_value=(stale,))
            (root / stale).write_bytes(
                b"<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                b"source: .claude/provider.md -->\n" + b"x" * 8_193
            )
            real_identity = renderer._owned_projection_identity_at

            def guarded_identity(parent_descriptor, relative):
                if relative == stale:
                    self.fail(
                        "oversized static candidate was fully hashed during check"
                    )
                return real_identity(parent_descriptor, relative)

            with mock.patch.object(
                renderer,
                "_owned_projection_identity_at",
                side_effect=guarded_identity,
            ):
                findings = renderer.find_native_projection_drift(root)

            self.assertIn(renderer.Finding(stale, "stale-generated"), findings)
            with self.assertRaisesRegex(ValueError, "manual cleanup required"):
                renderer.write_native_projection(root)
            self.assertFalse((root / stale).exists())
            clear_generated_quarantine(self, renderer, root)
            renderer.write_native_projection(root)
            self.assertEqual([], renderer.find_native_projection_drift(root))

    def test_corrupted_oversized_generated_pointer_cannot_hide_its_marker(
        self,
    ) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            stale = pathlib.PurePosixPath(".codex/CORRUPTED.md")
            renderer._tracked_static_paths = mock.Mock(return_value=(stale,))
            (root / stale).write_bytes(
                b"<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                b"source: .claude/provider.md -->\n" + b"\xff" + b"x" * 9_000
            )

            self.assertIn(
                renderer.Finding(stale, "stale-generated"),
                renderer.find_native_projection_drift(root),
            )
            with self.assertRaisesRegex(ValueError, "manual cleanup required"):
                renderer.write_native_projection(root)
            self.assertFalse((root / stale).exists())
            clear_generated_quarantine(self, renderer, root)
            renderer.write_native_projection(root)
            self.assertEqual([], renderer.find_native_projection_drift(root))

    def test_renderer_does_not_require_stage99_registry(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            self.assertFalse((root / "docs/99.templates").exists())
            try:
                records = renderer.render_all(root)
            except renderer.ContractLoadError as error:
                self.fail(f"renderer loaded a non-Stage-00 dependency: {error}")
            self.assertTrue(records)

    def test_managed_root_order_is_registry_data_not_a_parallel_tuple(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            mutate_registry(root, lambda data: data["generated_roots"].reverse())
            try:
                roots = renderer._managed_roots(renderer.load_agent_governance(root))
            except renderer.ContractLoadError as error:
                self.fail(f"managed roots were compared with a parallel tuple: {error}")
            self.assertEqual(
                set(
                    yaml.safe_load(
                        (root / ".agents/governance/providers/registry.yaml").read_text(
                            encoding="utf-8"
                        )
                    )["generated_roots"]
                ),
                {path.as_posix() for path in roots},
            )

    def test_repository_projection_is_exact(self) -> None:
        renderer = load_renderer()
        self.assertEqual([], renderer.find_native_projection_drift(ROOT))

    def test_all_generated_structured_surfaces_parse(self) -> None:
        renderer = load_renderer()
        projection = renderer.expected_native_projection(ROOT)
        for path, payload in projection.items():
            relative = path.as_posix()
            with self.subTest(path=relative):
                if relative.startswith(".codex/agents/"):
                    parsed = tomllib.loads(payload.decode("utf-8"))
                    self.assertIsInstance(parsed, dict)
                elif relative.startswith(
                    (
                        ".claude/agents/",
                        ".claude/skills/",
                    )
                ):
                    self.assertIsInstance(parse_frontmatter(payload), dict)
                elif relative in {
                    ".claude/README.md",
                    ".codex/README.md",
                }:
                    metadata = parse_frontmatter(payload)
                    self.assertEqual(
                        ["title", "version", "type", "status", "owner", "updated"],
                        list(metadata)[:6],
                    )
                    self.assertEqual("active", metadata["status"])

    def test_write_repairs_registered_projection_drift(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            target = root / ".claude/agents/code-reviewer.md"
            target.write_text("drift\n")
            self.assertTrue(renderer.find_native_projection_drift(root))
            renderer.write_native_projection(root)
            self.assertEqual([], renderer.find_native_projection_drift(root))

    def test_write_hands_off_revalidated_stale_projection_cleanup(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            stale = root / ".claude/skills/stale/SKILL.md"
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "---\nname: stale\n---\n\n"
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: .agents/skills/stale/SKILL.md -->\n"
            )
            with self.assertRaisesRegex(ValueError, "manual cleanup required"):
                renderer.write_native_projection(root)
            self.assertFalse(stale.exists())
            pending = renderer._pending_quarantine_paths(root)
            self.assertTrue(pending)
            self.assertIn(
                renderer.Finding(pending[0], "pending-cleanup"),
                renderer.find_native_projection_drift(root),
            )
            clear_generated_quarantine(self, renderer, root)
            renderer.write_native_projection(root)
            self.assertEqual([], renderer.find_native_projection_drift(root))

    def test_write_preserves_unowned_projection_file(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            unowned = root / ".claude/skills/local/SKILL.md"
            unowned.parent.mkdir(parents=True)
            unowned.write_text("# local\n")
            with self.assertRaisesRegex(ValueError, "unowned"):
                renderer.write_native_projection(root)
            self.assertTrue(unowned.exists())

    def test_managed_roots_reject_escape_and_unregistered_values(self) -> None:
        renderer = load_renderer()
        mutations = {
            "absolute": lambda data: data.update({"generated_roots": ["/tmp"]}),
            "parent": lambda data: data.update({"generated_roots": ["../outside"]}),
            "unexpected": lambda data: data["generated_roots"].append(".codex/other"),
            "missing": lambda data: data.update(
                {"generated_roots": data["generated_roots"][:-1]}
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                mutate_registry(root, mutation)
                with self.assertRaises((ValueError, renderer.ContractLoadError)):
                    renderer.write_native_projection(root)

    def test_managed_root_symlink_is_rejected(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            managed = root / ".claude/agents"
            outside = root / "outside"
            shutil.rmtree(managed)
            outside.mkdir()
            managed.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                renderer.write_native_projection(root)

    def test_marker_inside_unowned_file_is_not_ownership_proof(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            unowned = root / ".claude/skills/local/SKILL.md"
            unowned.parent.mkdir(parents=True)
            unowned.write_text(
                "# local file\n\n"
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: .agents/skills/local/SKILL.md -->\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "unowned"):
                renderer.write_native_projection(root)
            self.assertTrue(unowned.exists())

    def test_replacement_race_preserves_new_unowned_file(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            relative = pathlib.PurePosixPath(".claude/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: .agents/skills/stale/SKILL.md -->\n",
                encoding="utf-8",
            )
            identity = renderer._owned_projection_identity(root, relative)
            stale.unlink()
            stale.write_text("# replacement owned by user\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed"):
                renderer._quarantine_owned_projection(root, relative, identity)
            self.assertEqual("# replacement owned by user\n", stale.read_text())

    def test_validation_to_unlink_replacement_race_preserves_user_file(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            relative = pathlib.PurePosixPath(".claude/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: .agents/skills/stale/SKILL.md -->\n",
                encoding="utf-8",
            )
            identity = renderer._owned_projection_identity(root, relative)
            real_stat = os.stat
            replaced = False

            def replace_after_stat(path, *args, **kwargs):
                nonlocal replaced
                metadata = real_stat(path, *args, **kwargs)
                if (
                    not replaced
                    and path == relative.name
                    and kwargs.get("dir_fd") is not None
                    and kwargs.get("follow_symlinks") is False
                ):
                    replaced = True
                    os.unlink(stale)
                    descriptor = os.open(
                        stale, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
                    )
                    try:
                        os.write(descriptor, b"# replacement owned by user\n")
                    finally:
                        os.close(descriptor)
                return metadata

            with mock.patch.object(renderer.os, "stat", side_effect=replace_after_stat):
                with self.assertRaisesRegex(ValueError, "changed"):
                    renderer._quarantine_owned_projection(root, relative, identity)
            self.assertTrue(replaced)
            self.assertEqual("# replacement owned by user\n", stale.read_text())

    def test_post_validation_quarantine_replacement_is_retained(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            relative = pathlib.PurePosixPath(".claude/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: .agents/skills/stale/SKILL.md -->\n",
                encoding="utf-8",
            )
            identity = renderer._owned_projection_identity(root, relative)
            replacement = b"# post-validation user replacement\n"
            real_identity_at = renderer._owned_projection_identity_at
            replaced = False

            def replace_after_quarantine_validation(descriptor, candidate):
                nonlocal replaced
                actual = real_identity_at(descriptor, candidate)
                if not replaced and ".delete-" in candidate.name:
                    replaced = True
                    os.unlink(candidate.name, dir_fd=descriptor)
                    handle = os.open(
                        candidate.name,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                        dir_fd=descriptor,
                    )
                    try:
                        os.write(handle, replacement)
                    finally:
                        os.close(handle)
                return actual

            with mock.patch.object(
                renderer,
                "_owned_projection_identity_at",
                side_effect=replace_after_quarantine_validation,
            ):
                with self.assertRaisesRegex(ValueError, "retained.*quarantine|changed"):
                    renderer._quarantine_owned_projection(root, relative, identity)
            self.assertTrue(replaced)
            survivors = [
                path
                for path in root.rglob("*")
                if path.is_file() and path.read_bytes() == replacement
            ]
            self.assertTrue(survivors)

    def test_post_final_validation_quarantine_replacement_is_not_deleted(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            relative = pathlib.PurePosixPath(".claude/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: .agents/skills/stale/SKILL.md -->\n",
                encoding="utf-8",
            )
            identity = renderer._owned_projection_identity(root, relative)
            replacement = b"# replacement after final validation\n"
            real_identity_at = renderer._owned_projection_identity_at
            quarantine_validations = 0
            replaced = False

            def replace_after_final_validation(descriptor, candidate):
                nonlocal quarantine_validations, replaced
                actual = real_identity_at(descriptor, candidate)
                if ".delete-" in candidate.name:
                    quarantine_validations += 1
                    if quarantine_validations == 2:
                        os.unlink(candidate.name, dir_fd=descriptor)
                        handle = os.open(
                            candidate.name,
                            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                            0o600,
                            dir_fd=descriptor,
                        )
                        try:
                            os.write(handle, replacement)
                        finally:
                            os.close(handle)
                        replaced = True
                return actual

            with mock.patch.object(
                renderer,
                "_owned_projection_identity_at",
                side_effect=replace_after_final_validation,
            ):
                renderer._quarantine_owned_projection(root, relative, identity)

            self.assertTrue(replaced)
            survivors = [
                path
                for path in root.rglob("*")
                if path.is_file() and path.read_bytes() == replacement
            ]
            self.assertTrue(survivors)

    def test_post_write_managed_root_symlink_race_preserves_outside_directory(
        self,
    ) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            managed = root / ".claude/skills"
            displaced = root / "displaced-skills"
            outside = root / "outside"
            outside_child = outside / "must-survive"
            outside_child.mkdir(parents=True)
            expected_write_count = len(renderer.expected_native_projection(root))
            real_atomic_write = renderer._atomic_write
            writes = 0

            def replace_after_last_write(source_root, relative, content):
                nonlocal writes
                real_atomic_write(source_root, relative, content)
                writes += 1
                if writes == expected_write_count:
                    managed.rename(displaced)
                    managed.symlink_to(outside, target_is_directory=True)

            with mock.patch.object(
                renderer, "_atomic_write", side_effect=replace_after_last_write
            ):
                with self.assertRaisesRegex(
                    ValueError, "managed root.*symlink|changed"
                ):
                    renderer.write_native_projection(root)
            self.assertEqual(expected_write_count, writes)
            self.assertTrue(outside_child.is_dir())

    def test_parent_replacement_race_preserves_outside_projection(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            relative = pathlib.PurePosixPath(".claude/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: .agents/skills/stale/SKILL.md -->\n",
                encoding="utf-8",
            )
            identity = renderer._owned_projection_identity(root, relative)
            outside = root / "outside"
            outside.mkdir()
            outside_file = outside / "SKILL.md"
            outside_file.write_text("# outside user file\n", encoding="utf-8")
            shutil.rmtree(stale.parent)
            stale.parent.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "changed"):
                renderer._quarantine_owned_projection(root, relative, identity)
            self.assertEqual("# outside user file\n", outside_file.read_text())


if __name__ == "__main__":
    unittest.main()
