from __future__ import annotations

import os
import contextlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
import unittest
import json
from unittest import mock

import yaml

from scripts.lib.document_governance import operations_catalog
from scripts.lib.document_governance.operations_catalog import (
    REGISTRY_PATH,
    OperationsAuthorityError,
    _run_git_bounded,
    read_bounded_regular,
    validate_active_operations_references,
    validate_current_operations,
)


ROOT = pathlib.Path(__file__).resolve().parents[3]


def current_role_paths(root: pathlib.Path = ROOT) -> tuple[pathlib.PurePosixPath, ...]:
    return tuple(
        pathlib.PurePosixPath(path.relative_to(root).as_posix())
        for path in sorted(
            (root / "docs/05.operations/catalog").glob(
                "*/[0-9][0-9][0-9][0-9]-*/*.md"
            )
        )
        if path.name in {"guide.md", "policy.md", "runbook.md"}
    )


def finding_codes(root: pathlib.Path = ROOT) -> set[str]:
    return {finding.code for finding in validate_current_operations(root)}


class OperationsCatalogTopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.role_paths = current_role_paths()

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        for source in (
            "docs/05.operations",
            "docs/99.templates/templates/operations",
        ):
            shutil.copytree(ROOT / source, root / source)
        for source in ("docs/99.templates/registry.json",):
            target = root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, target)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(
            ["git", "add", "docs/05.operations", "docs/99.templates"],
            cwd=root,
            check=True,
        )
        context = contextlib.ExitStack()
        context.enter_context(directory)
        self.addCleanup(context.close)
        return context, root

    def test_current_operations_tree_is_self_authoritative_and_archive_free(self) -> None:
        self.assertEqual(set(), finding_codes())
        context, root = self._fixture()
        with context:
            self.assertFalse((root / "docs/98.archive").exists())
            self.assertEqual(set(), finding_codes(root))

    def test_prefixed_subject_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            subject = next((root / "docs/05.operations/catalog/00-workspace").glob("0001-*"))
            subject.rename(subject.with_name(f"ops-{subject.name}"))
            self.assertIn("subject-path-invalid", finding_codes(root))

    def test_invalid_domain_route_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            subject = next((root / "docs/05.operations/catalog/00-workspace").glob("0001-*"))
            invalid_domain = root / "docs/05.operations/catalog/workspace"
            invalid_domain.mkdir()
            (invalid_domain / "README.md").write_text("invalid\n", encoding="utf-8")
            subject.rename(invalid_domain / subject.name)
            self.assertIn("domain-path-invalid", finding_codes(root))

    def test_changed_or_duplicate_role_identity_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            first, second = self.role_paths[:2]
            first_text = (root / first).read_text(encoding="utf-8")
            first_id = yaml.safe_load(first_text.split("---\n", 2)[1])["artifact_id"]
            second_path = root / second
            second_id = yaml.safe_load(
                second_path.read_text(encoding="utf-8").split("---\n", 2)[1]
            )["artifact_id"]
            second_path.write_text(
                second_path.read_text(encoding="utf-8").replace(
                    f"artifact_id: {second_id}",
                    f"artifact_id: {first_id}",
                    1,
                ),
                encoding="utf-8",
            )
            codes = finding_codes(root)
            self.assertTrue({"role-identity-invalid", "role-identity-duplicate"} <= codes)

    def test_release_and_parallel_role_roots_are_rejected(self) -> None:
        for retired in ("releases", "guides"):
            with self.subTest(retired=retired):
                context, root = self._fixture()
                with context:
                    (root / "docs/05.operations" / retired).mkdir(exist_ok=True)
                    self.assertIn("retired-root-present", finding_codes(root))

    def test_release_profile_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / "docs/99.templates/registry.json"
            registry = registry_path.read_text(encoding="utf-8")
            registry_path.write_text(
                registry.replace(
                    '"profiles": [',
                    '"profiles": [{"profile_id":"release","path_pattern":"docs/05.operations/releases/{slug}.md"},',
                    1,
                ),
                encoding="utf-8",
            )
            self.assertIn("release-authority-present", finding_codes(root))

    def test_registry_operations_profiles_and_template_roles_are_present(self) -> None:
        mutations = (
            ("profile_id", "guide-copy"),
            ("template_id", "operations/policy"),
        )
        for key, value in mutations:
            with self.subTest(key=key):
                context, root = self._fixture()
                with context:
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    guide = next(item for item in registry["profiles"] if item["profile_id"] == "guide")
                    guide[key] = value
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    self.assertIn("registry-operations-profile-invalid", finding_codes(root))

        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["profile_id"] == "guide")
            registry["profiles"].append(dict(guide))
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-profile-duplicate", finding_codes(root))

    def test_registry_lifecycle_and_required_sections_are_consumed(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            living = registry["lifecycles"]["living"]
            living["statuses"].remove("active")
            living["transitions"].pop("active")
            for targets in living["transitions"].values():
                if "active" in targets:
                    targets.remove("active")
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("role-status-invalid", finding_codes(root))

        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["profile_id"] == "guide")
            guide["required_sections"].append("New Contract")
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("role-sections-invalid", finding_codes(root))

    def test_registry_schema_valid_optional_changes_do_not_require_a_python_mirror(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["profile_id"] == "guide")
            guide["optional_frontmatter"].append("generated_by")
            guide["optional_sections"].append("Operator Notes")
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            codes = finding_codes(root)
            self.assertNotIn("registry-operations-profile-invalid", codes)
            self.assertNotIn("registry-operations-lifecycle-invalid", codes)

    def test_malformed_registry_returns_findings_without_traceback(self) -> None:
        for mutation in (
            "missing-artifact-pattern",
            "object-frontmatter-member",
            "object-profile-id",
            "object-lifecycle-id",
        ):
            with self.subTest(mutation=mutation):
                context, root = self._fixture()
                with context:
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    guide = next(
                        item
                        for item in registry["profiles"]
                        if item["profile_id"] == "guide"
                    )
                    if mutation == "missing-artifact-pattern":
                        del guide["artifact_id_pattern"]
                    elif mutation == "object-frontmatter-member":
                        guide["required_frontmatter"] = [{"bad": "shape"}]
                    elif mutation == "object-profile-id":
                        guide["profile_id"] = {"bad": "shape"}
                    else:
                        guide["lifecycle_id"] = {"bad": "shape"}
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    codes = finding_codes(root)
                    self.assertIn("registry-canonical-invalid", codes)

    def test_registry_loader_rejects_excessive_depth_without_traceback(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            cursor = registry
            for _ in range(70):
                child: dict[str, object] = {}
                cursor["too_deep"] = child
                cursor = child
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-invalid", finding_codes(root))

    def test_registry_loader_rejects_symlinked_parent_directory(self) -> None:
        context, root = self._fixture()
        with context:
            registry_root = root / "docs/99.templates"
            external_root = root / "external-templates"
            registry_root.rename(external_root)
            registry_root.symlink_to(external_root, target_is_directory=True)
            self.assertIn("registry-invalid", finding_codes(root))

    def test_registry_route_and_identity_relation_govern_catalog_leaves(self) -> None:
        mutations = (
            (
                "path_pattern",
                "docs/05.operations/guides/{number:4}-{slug}.md",
                "role-path-profile-mismatch",
            ),
            ("identity_relation", "direct", "role-identity-relation-invalid"),
        )
        for key, value, expected in mutations:
            with self.subTest(key=key):
                context, root = self._fixture()
                with context:
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    guide = next(
                        item for item in registry["profiles"] if item["profile_id"] == "guide"
                    )
                    guide[key] = value
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    self.assertIn(expected, finding_codes(root))

    def test_registry_route_and_identity_relation_govern_incident_leaves(self) -> None:
        mutations = (
            (
                "path_pattern",
                "docs/05.operations/incidents/{year:4}/incident-{number:4}-{slug}.md",
                "incident-path-profile-mismatch",
            ),
            ("identity_relation", "subject-member", "incident-identity-relation-invalid"),
        )
        for key, value, expected in mutations:
            with self.subTest(key=key):
                context, root = self._fixture()
                with context:
                    self._write_incident_packet(root)
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    incident = next(
                        item for item in registry["profiles"] if item["profile_id"] == "incident"
                    )
                    incident[key] = value
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    self.assertIn(expected, finding_codes(root))

    def test_registry_required_sections_keep_operations_roles_distinct(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            profiles = {item["profile_id"]: item for item in registry["profiles"]}
            profiles["policy"]["required_sections"] = list(profiles["guide"]["required_sections"])
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-role-purpose-duplicate", finding_codes(root))

    def test_role_profile_and_registry_grounded_sections_are_required(self) -> None:
        context, root = self._fixture()
        with context:
            role = root / next(
                path for path in self.role_paths
            )
            text = role.read_text(encoding="utf-8")
            role.write_text(text.split("---\n", 2)[0] + "---\n" + text.split("---\n", 2)[1] + "---\n# Arbitrary\n", encoding="utf-8")
            self.assertIn("role-sections-invalid", finding_codes(root))

    def test_role_profile_id_is_required_even_when_all_other_metadata_is_valid(self) -> None:
        context, root = self._fixture()
        with context:
            role = root / next(
                path for path in self.role_paths
            )
            text = role.read_text(encoding="utf-8")
            role_name = role.stem
            role.write_text(
                text.replace(f"profile_id: {role_name}\n", "", 1),
                encoding="utf-8",
            )
            self.assertIn("role-profile-invalid", finding_codes(root))

    def test_role_frontmatter_rejects_duplicate_same_value_profile_id(self) -> None:
        context, root = self._fixture()
        with context:
            role = root / next(
                path for path in self.role_paths
            )
            role_name = role.stem
            text = role.read_text(encoding="utf-8")
            role.write_text(
                text.replace(
                    f"profile_id: {role_name}\n",
                    f"profile_id: {role_name}\nprofile_id: {role_name}\n",
                    1,
                ),
                encoding="utf-8",
            )
            self.assertIn("frontmatter-invalid", finding_codes(root))

    def _write_incident_packet(
        self,
        root: pathlib.Path,
        *,
        year: str = "2026",
        artifact_id: str = "inc-0001",
        status: str = "open",
        occurred_at: str = "2026-08-23T01:00:00Z",
        resolved_at: str = "2026-08-23T02:00:00Z",
        body: str | None = None,
    ) -> pathlib.Path:
        registry = json.loads((root / REGISTRY_PATH).read_text(encoding="utf-8"))
        profile = next(item for item in registry["profiles"] if item["profile_id"] == "incident")
        packet = root / f"docs/05.operations/incidents/{year}/inc-0001-fixture"
        packet.mkdir(parents=True)
        metadata = (
            f"---\nprofile_id: incident\nstatus: {status}\n"
            f"artifact_id: {artifact_id}\nartifact_type: incident\nparent_ids: []\n"
            "created: 2026-08-23\nupdated: 2026-08-23\n"
            f"occurred_at: {occurred_at}\nresolved_at: {resolved_at}\n---\n"
        )
        sections = body or "\n".join(f"## {section}\nEvidence." for section in profile["required_sections"])
        path = packet / "incident.md"
        path.write_text(metadata + "# Fixture Incident\n\n" + sections + "\n", encoding="utf-8")
        return path

    def test_incident_body_identity_year_and_date_relations_are_validated(self) -> None:
        mutations = (
            ({"body": "Arbitrary body."}, "incident-sections-invalid"),
            ({"year": "2025"}, "incident-year-date-invalid"),
            ({"artifact_id": "inc-0002"}, "incident-identity-invalid"),
            (
                {"occurred_at": "2026-08-23T02:00:00Z", "resolved_at": "2026-08-23T01:00:00Z"},
                "incident-date-order-invalid",
            ),
            ({"status": "active"}, "incident-status-invalid"),
        )
        for kwargs, expected in mutations:
            with self.subTest(expected=expected):
                context, root = self._fixture()
                with context:
                    self._write_incident_packet(root, **kwargs)
                    self.assertIn(expected, finding_codes(root))

    def test_incident_year_packet_and_roles_are_exact(self) -> None:
        mutations = (
            "docs/05.operations/incidents/current/inc-0001-bad/incident.md",
            "docs/05.operations/incidents/2026/incident-0001-bad/incident.md",
            "docs/05.operations/incidents/2026/inc-0001-bad/notes.md",
        )
        for relative in mutations:
            with self.subTest(relative=relative):
                context, root = self._fixture()
                with context:
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("invalid", encoding="utf-8")
                    codes = finding_codes(root)
                    self.assertTrue(
                        codes & {"incident-year-invalid", "incident-packet-invalid", "incident-roles-invalid"}
                    )

    def test_role_symlink_and_nonregular_inputs_are_rejected(self) -> None:
        target = self.role_paths[0]
        for mutation in ("symlink", "directory"):
            with self.subTest(mutation=mutation):
                context, root = self._fixture()
                with context:
                    path = root / target
                    path.unlink()
                    if mutation == "symlink":
                        path.symlink_to(ROOT / target)
                    else:
                        path.mkdir()
                    self.assertIn("role-file-invalid", finding_codes(root))

    def test_untracked_valid_subject_is_not_current_membership(self) -> None:
        context, root = self._fixture()
        with context:
            source = root / "docs/05.operations/catalog/01-gateway/0011-nginx"
            target = source.with_name("0999-untracked")
            shutil.copytree(source, target)
            for role in ("guide", "policy", "runbook"):
                path = target / f"{role}.md"
                path.write_text(
                    re.sub(
                        rf"^artifact_id: {role}-[0-9]{{4}}$",
                        f"artifact_id: {role}-9999",
                        path.read_text(encoding="utf-8"),
                        count=1,
                        flags=re.MULTILINE,
                    ),
                    encoding="utf-8",
                )
            self.assertIn("untracked-operations-path", finding_codes(root))

    def test_structural_indexes_must_be_regular_and_symlink_free(self) -> None:
        for relative, expected in (
            ("docs/05.operations/README.md", "operations-root-index-invalid"),
            ("docs/05.operations/incidents/README.md", "incident-index-invalid"),
        ):
            for mutation in ("symlink", "directory", "fifo"):
                with self.subTest(relative=relative, mutation=mutation):
                    context, root = self._fixture()
                    with context:
                        path = root / relative
                        path.unlink()
                        if mutation == "symlink":
                            path.symlink_to(ROOT / relative)
                        elif mutation == "directory":
                            path.mkdir()
                        else:
                            os.mkfifo(path)
                        self.assertIn(expected, finding_codes(root))

    def test_catalog_enumeration_is_bounded(self) -> None:
        with mock.patch(
            "scripts.lib.document_governance.operations_catalog.MAX_CATALOG_ENTRIES", 1
        ):
            self.assertIn("catalog-bounds", finding_codes())

    def test_operations_root_domain_and_subject_enumeration_are_independently_bounded(self) -> None:
        mutations = (
            ("MAX_OPERATIONS_ROOT_ENTRIES", "operations-root-bounds"),
            ("MAX_DOMAIN_ENTRIES", "domain-bounds"),
            ("MAX_SUBJECT_ENTRIES", "subject-bounds"),
        )
        for constant, expected in mutations:
            with self.subTest(constant=constant), mock.patch.object(
                operations_catalog, constant, 1
            ):
                self.assertIn(expected, finding_codes())

    def test_incident_enumeration_is_bounded(self) -> None:
        context, root = self._fixture()
        with context:
            self._write_incident_packet(root)
            with mock.patch.object(operations_catalog, "MAX_INCIDENT_ENTRIES", 1):
                self.assertIn("incident-bounds", finding_codes(root))


class BoundedRegularReaderTests(unittest.TestCase):
    def test_reader_rejects_service_readme_regular_to_fifo_race_without_blocking(
        self,
    ) -> None:
        source = """
import os
import pathlib
import sys
from unittest import mock

from scripts.lib.document_governance import operations_catalog

root = pathlib.Path(sys.argv[1])
target = root / "infra/service/README.md"
real_stat = os.stat
swapped = False

def racing_stat(path, *args, **kwargs):
    global swapped
    result = real_stat(path, *args, **kwargs)
    if path == "README.md" and kwargs.get("dir_fd") is not None and not swapped:
        swapped = True
        target.unlink()
        os.mkfifo(target)
    return result

with mock.patch.object(operations_catalog.os, "stat", side_effect=racing_stat):
    try:
        operations_catalog.read_bounded_regular(
            root, pathlib.PurePosixPath("infra/service/README.md")
        )
    except operations_catalog.OperationsAuthorityError:
        sys.exit(0)
sys.exit(1)
"""
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "infra/service/README.md"
            target.parent.mkdir(parents=True)
            target.write_text("content\n", encoding="utf-8")
            environment = os.environ.copy()
            python_path = environment.get("PYTHONPATH")
            environment["PYTHONPATH"] = (
                str(ROOT) if not python_path else f"{ROOT}{os.pathsep}{python_path}"
            )
            try:
                result = subprocess.run(
                    [sys.executable, "-c", source, str(root)],
                    capture_output=True,
                    text=True,
                    check=False,
                    env=environment,
                    timeout=1.0,
                )
            except subprocess.TimeoutExpired:
                self.fail("regular-to-FIFO reader race blocked during open")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_reader_rejects_symlink_and_byte_overflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "real").write_text("content", encoding="utf-8")
            (root / "link").symlink_to(root / "real")
            with self.assertRaisesRegex(OperationsAuthorityError, "symlink"):
                read_bounded_regular(root, pathlib.PurePosixPath("link"))
            with self.assertRaisesRegex(OperationsAuthorityError, "bound"):
                read_bounded_regular(root, pathlib.PurePosixPath("real"), max_bytes=2)

    def test_reader_rejects_an_in_read_identity_race(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "input"
            target.write_text("content", encoding="utf-8")
            real = os.stat(target)
            changed = types.SimpleNamespace(
                st_dev=real.st_dev,
                st_ino=real.st_ino,
                st_size=real.st_size,
                st_mtime_ns=real.st_mtime_ns + 1,
            )
            with mock.patch(
                "scripts.lib.document_governance.operations_catalog.os.fstat",
                side_effect=(real, changed),
            ):
                with self.assertRaisesRegex(OperationsAuthorityError, "during read"):
                    read_bounded_regular(root, pathlib.PurePosixPath("input"))

    def test_reader_clamps_caller_limit_to_hard_maximum(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "input").write_text("content", encoding="utf-8")
            with mock.patch.object(operations_catalog, "MAX_FILE_BYTES", 2):
                with self.assertRaisesRegex(OperationsAuthorityError, "bound"):
                    read_bounded_regular(
                        root,
                        pathlib.PurePosixPath("input"),
                        max_bytes=1_000_000,
                    )


class BoundedDirectoryEnumerationTests(unittest.TestCase):
    def test_directory_path_identity_swap_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "entry").write_text("content", encoding="utf-8")
            before = os.stat(target)
            swapped = types.SimpleNamespace(
                st_mode=before.st_mode,
                st_dev=before.st_dev,
                st_ino=before.st_ino + 1,
                st_mtime_ns=before.st_mtime_ns,
            )
            with mock.patch(
                "scripts.lib.document_governance.operations_catalog.os.stat",
                side_effect=(before, swapped),
            ):
                with self.assertRaisesRegex(OperationsAuthorityError, "changed"):
                    operations_catalog._directory_entries_bounded(
                        root,
                        pathlib.PurePosixPath("target"),
                        max_entries=8,
                    )

    def test_directory_in_enumeration_metadata_race_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "entry").write_text("content", encoding="utf-8")
            before = os.stat(target)
            changed = types.SimpleNamespace(
                st_mode=before.st_mode,
                st_dev=before.st_dev,
                st_ino=before.st_ino,
                st_mtime_ns=before.st_mtime_ns + 1,
            )
            with mock.patch(
                "scripts.lib.document_governance.operations_catalog.os.fstat",
                side_effect=(before, changed),
            ):
                with self.assertRaisesRegex(OperationsAuthorityError, "changed"):
                    operations_catalog._directory_entries_bounded(
                        root,
                        pathlib.PurePosixPath("target"),
                        max_entries=8,
                    )


class BoundedGitAndTrackedInputTests(unittest.TestCase):
    def _repo(self) -> tempfile.TemporaryDirectory[str]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        return directory

    def test_git_helper_drains_stdout_and_stderr_without_deadlock(self) -> None:
        with self._repo() as directory:
            root = pathlib.Path(directory)
            alias = (
                "alias.noisy=!python3 -c 'import sys;"
                "sys.stdout.write(\"o\"*65536);sys.stdout.flush();"
                "sys.stderr.write(\"e\"*65536);sys.stderr.flush()'"
            )
            result = _run_git_bounded(
                root,
                ["-c", alias, "noisy"],
                timeout_seconds=2,
                max_stdout=100_000,
                max_stderr=100_000,
            )
            self.assertEqual(0, result.returncode)
            self.assertEqual(65_536, len(result.stdout))
            self.assertEqual(65_536, len(result.stderr))

    def test_git_helper_enforces_deadline_and_reaps_process_group(self) -> None:
        with self._repo() as directory:
            root = pathlib.Path(directory)
            started = time.monotonic()
            with self.assertRaisesRegex(OperationsAuthorityError, "deadline"):
                _run_git_bounded(
                    root,
                    ["-c", "alias.wait=!sleep 2", "wait"],
                    timeout_seconds=0.05,
                )
            self.assertLess(time.monotonic() - started, 1.0)

    def test_git_helper_enforces_stdout_and_stderr_caps(self) -> None:
        with self._repo() as directory:
            root = pathlib.Path(directory)
            (root / "blob").write_text("x" * 512, encoding="utf-8")
            subprocess.run(["git", "add", "blob"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            with self.assertRaisesRegex(OperationsAuthorityError, "stdout"):
                _run_git_bounded(root, ["show", "HEAD:blob"], max_stdout=32)
            with self.assertRaisesRegex(OperationsAuthorityError, "stderr"):
                _run_git_bounded(root, ["show", "HEAD:missing"], max_stderr=8)

    def test_active_scan_allows_deletion_but_rejects_nonregular_tracked_paths(self) -> None:
        mutations = ("broken-symlink", "directory")
        for mutation in mutations:
            with self.subTest(mutation=mutation), self._repo() as directory:
                root = pathlib.Path(directory)
                path = root / "tracked.md"
                path.write_text("tracked", encoding="utf-8")
                subprocess.run(["git", "add", "tracked.md"], cwd=root, check=True)
                subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
                path.unlink()
                if mutation == "broken-symlink":
                    path.symlink_to("missing.md")
                elif mutation == "directory":
                    path.mkdir()
                with self.assertRaises(OperationsAuthorityError):
                    validate_active_operations_references(root)

        with self._repo() as directory:
            root = pathlib.Path(directory)
            path = root / "tracked.md"
            path.write_text("tracked", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            path.unlink()
            self.assertEqual((), validate_active_operations_references(root))


if __name__ == "__main__":
    unittest.main()
