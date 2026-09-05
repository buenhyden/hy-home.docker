from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest import mock

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
RENDERER = ROOT / "scripts/operations/provider_surface_renderer.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("provider_surface_renderer", RENDERER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {RENDERER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def copy_fixture(root: pathlib.Path) -> None:
    shutil.copytree(
        ROOT / "docs/00.agent-governance", root / "docs/00.agent-governance"
    )
    for directory in (".agents", ".claude", ".codex"):
        shutil.copytree(ROOT / directory, root / directory)
    hook = root / "scripts/hooks/agent-event-hook.sh"
    hook.parent.mkdir(parents=True)
    shutil.copy2(ROOT / "scripts/hooks/agent-event-hook.sh", hook)


def mutate_registry(root: pathlib.Path, mutation) -> None:
    path = root / "docs/00.agent-governance/providers/registry.yaml"
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
    def test_cli_rejects_retired_agent_projection_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            retired = root / ".agents/agents/code-reviewer.md"
            retired.parent.mkdir()
            retired.write_bytes(b"unowned role content\n")
            projection = root / ".agents/README.md"
            original = projection.read_bytes() + b"\nlocal drift\n"
            projection.write_bytes(original)

            for mode in ("--check", "--write"):
                with self.subTest(mode=mode):
                    result = subprocess.run(
                        [sys.executable, str(RENDERER), mode, "--root", str(root)],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=15,
                    )
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn("AGC-RETIRED-AGENT-PROJECTION", result.stderr)
                    self.assertEqual(b"unowned role content\n", retired.read_bytes())
                    self.assertEqual(original, projection.read_bytes())
                    self.assertFalse((root / ".provider-surface-quarantine").exists())

    def test_projection_omits_provider_neutral_agent_compatibility_root(
        self,
    ) -> None:
        projection = load_renderer().expected_native_projection(ROOT)

        self.assertFalse(
            any(
                path.is_relative_to(pathlib.PurePosixPath(".agents/agents"))
                for path in projection
            )
        )
        self.assertTrue(
            any(
                path.is_relative_to(pathlib.PurePosixPath(".agents/skills"))
                for path in projection
            )
        )
        self.assertTrue(
            any(
                path.is_relative_to(pathlib.PurePosixPath(".claude"))
                for path in projection
            )
        )
        self.assertTrue(
            any(
                path.is_relative_to(pathlib.PurePosixPath(".codex"))
                for path in projection
            )
        )

    def test_static_projection_routes_follow_registry_data(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            self.assertIn("projections", registry)
            registry["projections"][0]["path"] = ".agents/ROUTE.md"
            registry_path.write_text(
                yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
            )

            projection = renderer.expected_native_projection(root)

            self.assertIn(pathlib.Path(".agents/ROUTE.md"), projection)
            self.assertNotIn(pathlib.Path(".agents/README.md"), projection)

    def test_dynamic_yaml_scalars_are_quoted_in_role_and_skill_projections(
        self,
    ) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            for relative, original in (
                ("roles/code-reviewer.md", 'scope: "common"'),
                ("skills/adr-writing.md", 'scope: "architecture"'),
            ):
                path = root / "docs/00.agent-governance" / relative
                text = path.read_text(encoding="utf-8")
                self.assertIn(original, text)
                path.write_text(
                    text.replace(original, "scope: 'x: injected'", 1),
                    encoding="utf-8",
                )

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
            shared_skill = parse_frontmatter(
                projection[pathlib.Path(".agents/skills/adr-writing/SKILL.md")]
            )
            claude_skill = parse_frontmatter(
                projection[pathlib.Path(".claude/skills/adr-writing/SKILL.md")]
            )

            self.assertIn("Canonical x: injected role", claude_role["description"])
            self.assertEqual("evil: true", claude_role["model"])
            self.assertEqual("high: injected", claude_role["effort"])
            self.assertIn(
                "Canonical x: injected procedure", shared_skill["description"]
            )
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
        for case in ("change", "remove"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_fixture(root)
                old_path = root / ".agents/README.md"
                if case == "change":
                    mutate_registry(
                        root,
                        lambda data: data["projections"][0].update(
                            {"path": ".agents/ROUTE.md"}
                        ),
                    )
                else:
                    mutate_registry(root, lambda data: data["projections"].pop(0))

                self.assertIn(
                    renderer.Finding(
                        pathlib.PurePosixPath(".agents/README.md"),
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
                    self.assertTrue((root / ".agents/ROUTE.md").is_file())

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
                    "Canonical common role for retired-large-role; owned by Stage 00."
                ),
                "developer_instructions": (
                    "# Generated by scripts/operations/provider_surface_renderer.py; "
                    "source: docs/00.agent-governance/roles/retired-large-role.md\n\n"
                    + "x"
                    * 9_000
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
            target = root / ".agents/README.md"
            outside = root / "outside-generated.md"
            outside.write_bytes(target.read_bytes())
            target.unlink()
            target.symlink_to(outside)

            self.assertIn(
                renderer.Finding(pathlib.PurePosixPath(".agents/README.md"), "unsafe"),
                renderer.find_native_projection_drift(root),
            )

    def test_check_does_not_hash_oversized_unowned_namespace_file(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_fixture(root)
            oversized = pathlib.PurePosixPath(".agents/unowned-large.bin")
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
            stale = pathlib.PurePosixPath(".agents/STALE.md")
            (root / stale).write_bytes(
                b"<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                b"source: docs/00.agent-governance/providers/claude.md -->\n"
                + b"x"
                * 8_193
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
            stale = pathlib.PurePosixPath(".agents/CORRUPTED.md")
            (root / stale).write_bytes(
                b"<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                b"source: docs/00.agent-governance/providers/claude.md -->\n"
                + b"\xff"
                + b"x" * 9_000
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
                        (
                            root / "docs/00.agent-governance/providers/registry.yaml"
                        ).read_text(encoding="utf-8")
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
                        ".agents/skills/",
                        ".claude/agents/",
                        ".claude/skills/",
                    )
                ):
                    self.assertIsInstance(parse_frontmatter(payload), dict)
                elif relative in {
                    ".agents/README.md",
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
            stale = root / ".agents/skills/stale/SKILL.md"
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "---\nname: stale\n---\n\n"
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: docs/00.agent-governance/skills/stale.md -->\n"
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
            unowned = root / ".agents/skills/local/SKILL.md"
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
            "unexpected": lambda data: data["generated_roots"].append(".agents/other"),
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
            unowned = root / ".agents/skills/local/SKILL.md"
            unowned.parent.mkdir(parents=True)
            unowned.write_text(
                "# local file\n\n"
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: docs/00.agent-governance/skills/local.md -->\n",
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
            relative = pathlib.PurePosixPath(".agents/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: docs/00.agent-governance/skills/stale.md -->\n",
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
            relative = pathlib.PurePosixPath(".agents/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: docs/00.agent-governance/skills/stale.md -->\n",
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
            relative = pathlib.PurePosixPath(".agents/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: docs/00.agent-governance/skills/stale.md -->\n",
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
            relative = pathlib.PurePosixPath(".agents/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: docs/00.agent-governance/skills/stale.md -->\n",
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
            managed = root / ".agents/skills"
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
            relative = pathlib.PurePosixPath(".agents/skills/stale/SKILL.md")
            stale = root / relative
            stale.parent.mkdir(parents=True)
            stale.write_text(
                "<!-- Generated by scripts/operations/provider_surface_renderer.py; "
                "source: docs/00.agent-governance/skills/stale.md -->\n",
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
