from __future__ import annotations

import os
import pathlib
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
    EXPECTED_DOMAINS,
    EXPECTED_ROLE_COUNTS,
    MIGRATION_PATH,
    REGISTRY_PATH,
    OperationsAuthorityError,
    Task8Migration,
    _run_git_bounded,
    extract_task8_consumers,
    load_task8_migration,
    read_bounded_regular,
    validate_current_operations,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def finding_codes(root: pathlib.Path = ROOT) -> set[str]:
    return {finding.code for finding in validate_current_operations(root, include_semantic_witnesses=False)}


class OperationsCatalogTopologyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.migration = load_task8_migration(ROOT)

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        for source in (
            "docs/05.operations",
            "docs/99.templates/templates/operations",
        ):
            shutil.copytree(ROOT / source, root / source)
        for source in (
            "docs/99.templates/registry.json",
            str(MIGRATION_PATH),
            "docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md",
        ):
            target = root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, target)
        return directory, root

    def test_current_operations_has_exact_final_topology(self) -> None:
        self.assertEqual(set(), finding_codes())
        targets = [row.target_path for row in self.migration.rows if row.action == "rename"]
        self.assertEqual(75, len({path.parent for path in targets if path is not None}))
        self.assertEqual(
            EXPECTED_ROLE_COUNTS,
            {
                role: sum(path is not None and path.name == f"{role}.md" for path in targets)
                for role in EXPECTED_ROLE_COUNTS
            },
        )
        self.assertEqual(
            set(EXPECTED_DOMAINS),
            {path.parts[3] for path in targets if path is not None},
        )

    def test_current_operations_preserves_registered_role_ids(self) -> None:
        for row in self.migration.rows:
            if row.target_path is None:
                continue
            current = ROOT / row.target_path
            if not current.is_file():
                current = ROOT / row.source_path
            text = current.read_text(encoding="utf-8")
            metadata = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(path=row.target_path):
                self.assertEqual(row.artifact_id, metadata["artifact_id"])

    def test_prefixed_subject_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            subject = next((root / "docs/05.operations/catalog/00-workspace").glob("0001-*"))
            subject.rename(subject.with_name(f"ops-{subject.name}"))
            self.assertIn("subject-path-invalid", finding_codes(root))

    def test_domain_subject_ownership_change_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            subject = next((root / "docs/05.operations/catalog/00-workspace").glob("0001-*"))
            subject.rename(root / "docs/05.operations/catalog/01-gateway" / subject.name)
            self.assertIn("domain-ownership-invalid", finding_codes(root))

    def test_changed_or_duplicate_role_identity_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            targets = [row.target_path for row in self.migration.rows if row.target_path is not None]
            first, second = targets[:2]
            first_text = (root / first).read_text(encoding="utf-8")
            first_id = yaml.safe_load(first_text.split("---\n", 2)[1])["artifact_id"]
            second_path = root / second
            second_path.write_text(
                second_path.read_text(encoding="utf-8").replace(
                    f"artifact_id: {self.migration.rows[1].artifact_id}",
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

    def test_registry_operations_profiles_are_duplicate_safe_and_exact(self) -> None:
        mutations = (
            ("profile_id", "guide-copy"),
            ("identity_relation", "direct"),
            ("template_id", "operations/policy"),
            ("lifecycle_id", "incident"),
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

    def test_registry_operations_frontmatter_traceability_and_lifecycle_are_exact(self) -> None:
        mutations = (
            ("required_frontmatter", ["status", "artifact_id"]),
            (
                "traceability",
                {
                    "allowed_parent_profiles": ["spec", "policy", "runbook"],
                    "membership_authority": "stale-migration",
                },
            ),
            (
                "traceability",
                {
                    "allowed_parent_profiles": ["spec"],
                    "membership_authority": "operations-migration-manifest",
                },
            ),
        )
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                context, root = self._fixture()
                with context:
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    guide = next(
                        item for item in registry["profiles"] if item["profile_id"] == "guide"
                    )
                    guide[key] = value
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    self.assertIn("registry-operations-profile-invalid", finding_codes(root))

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
            self.assertIn("registry-operations-lifecycle-invalid", finding_codes(root))

    def test_registry_operations_optional_projection_and_transitions_are_exact(self) -> None:
        profile_mutations = (
            ("optional_frontmatter", ["reviewed_at", "task8-extra"]),
            ("optional_sections", ["Examples", "Task 8 Extra"]),
        )
        for key, value in profile_mutations:
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
                    self.assertIn("registry-operations-profile-invalid", finding_codes(root))

        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["lifecycles"]["living"]["transitions"]["active"].append("draft")
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-operations-lifecycle-invalid", finding_codes(root))

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
                row.target_path for row in self.migration.rows if row.target_path is not None
            )
            text = role.read_text(encoding="utf-8")
            role.write_text(text.split("---\n", 2)[0] + "---\n" + text.split("---\n", 2)[1] + "---\n# Arbitrary\n", encoding="utf-8")
            self.assertIn("role-sections-invalid", finding_codes(root))

    def test_role_profile_id_is_required_even_when_all_other_metadata_is_valid(self) -> None:
        context, root = self._fixture()
        with context:
            role = root / next(
                row.target_path for row in self.migration.rows if row.target_path is not None
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
                row.target_path for row in self.migration.rows if row.target_path is not None
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
        target = next(row.target_path for row in self.migration.rows if row.target_path is not None)
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


class Migration0003ContractTests(unittest.TestCase):
    def _mutated_migration(self, old: str, new: str) -> tempfile.TemporaryDirectory[str]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        target = root / MIGRATION_PATH
        target.parent.mkdir(parents=True)
        text = (ROOT / MIGRATION_PATH).read_text(encoding="utf-8")
        self.assertIn(old, text)
        target.write_text(text.replace(old, new, 1), encoding="utf-8")
        return directory

    def test_duplicate_yaml_key_is_rejected(self) -> None:
        old = "row_id: mig-0003-r0257, source_path:"
        replacement = "row_id: mig-0003-r0257, row_id: mig-0003-r0257, source_path:"
        with self._mutated_migration(old, replacement) as directory:
            with self.assertRaisesRegex(OperationsAuthorityError, "duplicate YAML key"):
                load_task8_migration(pathlib.Path(directory))

    def test_task8_owner_source_status_and_recovery_contract_is_exact(self) -> None:
        mutations = (
            ("owner_task: 8", "owner_task: 9", "owner_task"),
            ("owner_task: 8", "owner_task: '8'", "owner_task"),
            ("source_kind: tracked, source_owner_task: null", "source_kind: planned-output, source_owner_task: null", "source_kind"),
            ("source_kind: tracked, source_owner_task: null", "source_kind: tracked, source_owner_task: 7", "source_owner_task"),
            ("recovery_commit: null, status: planned", "recovery_commit: deadbeef, status: planned", "recovery"),
            ("recovery_commit: null, status: planned", "recovery_commit: null, status: completed", "status"),
        )
        for old, new, message in mutations:
            with self.subTest(message=message), self._mutated_migration(old, new) as directory:
                with self.assertRaisesRegex(OperationsAuthorityError, message):
                    load_task8_migration(pathlib.Path(directory))

    def test_full_row_order_uniqueness_and_frozen_digest_are_enforced(self) -> None:
        row257_source = (
            "docs/05.operations/catalog/00-workspace/"
            "ops-0001-common-optimizations-template-exceptions/policy.md"
        )
        row258_source = "docs/05.operations/catalog/00-workspace/ops-0002-developer-environment/guide.md"
        mutations = (
            ("row_id: mig-0003-r0257", "row_id: mig-0003-r0258", "row"),
            (row258_source, row257_source, "source_path"),
            ("artifact_id: policy-0001", "artifact_id: policy-review-mutation", "digest"),
        )
        for old, new, message in mutations:
            with self.subTest(message=message), self._mutated_migration(old, new) as directory:
                with self.assertRaisesRegex(OperationsAuthorityError, message):
                    load_task8_migration(pathlib.Path(directory))


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

    def test_consumer_scan_rejects_absent_broken_symlink_and_nonregular_tracked_paths(self) -> None:
        mutations = ("absent", "broken-symlink", "directory")
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
                    extract_task8_consumers(
                        root,
                        Task8Migration(rows=(), all_rows=()),
                    )


if __name__ == "__main__":
    unittest.main()
