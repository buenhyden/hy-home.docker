from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance.metadata_validator import (
    _write_or_check_output,
    validate_repository_contracts,
)
from scripts.lib.document_governance.taxonomy import (
    is_valid_incident_path,
    is_valid_internal_requirement_id,
    validate_stable_identity,
)

ROOT = pathlib.Path(__file__).resolve().parents[3]
PROFILES = ROOT / "docs/99.templates/registry.json"


class LabDocumentSelectionTests(unittest.TestCase):
    def test_registered_lab_documents_are_collected_before_and_after_staging(self):
        from scripts.lib.document_governance.metadata.lifecycle import collect_records
        from scripts.lib.document_governance.metadata.profile import (
            build_registry_profiles,
        )
        from scripts.lib.document_governance.registry import load_registry

        profiles = build_registry_profiles(load_registry(PROFILES))
        routes = ("labs/locust/README.md", "labs/postgresql-ha.md")
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            for route in routes:
                path = root / route
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '---\ntitle: "LAB fixture"\ntype: "common/readme"\n'
                    'status: "active"\nowner: "@fixture"\n---\n# LAB fixture\n',
                    encoding="utf-8",
                )
            for staged in (False, True):
                with self.subTest(staged=staged):
                    if staged:
                        subprocess.run(
                            ["git", "-C", str(root), "add", "--", *routes], check=True
                        )
                    records = collect_records(root, profiles, selected_paths=routes)
                    self.assertEqual(set(routes), {r.path.as_posix() for r in records})
                    self.assertEqual(
                        {"package-readme"}, {r.artifact_type for r in records}
                    )

    def test_lab_selection_does_not_accept_parent_traversal(self):
        from scripts.lib.document_governance.metadata.profile import (
            _normalized_target_path,
        )

        for path in (
            "../labs/README.md",
            "labs/../README.md",
            "/labs/README.md",
            "labs\\README.md",
        ):
            with self.subTest(path=path):
                self.assertIsNone(_normalized_target_path(path))


class FourDigitDocumentIdentityTests(unittest.TestCase):
    def test_full_repository_contracts_reaches_active_record_validation(self) -> None:
        from scripts.lib.document_governance import metadata_validator as metadata

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(PROFILES.read_bytes())
            document = root / "docs/03.specs/0104-example/spec.md"
            document.parent.mkdir(parents=True)
            document.write_text(
                "---\nstatus: active\ntype: sdlc/plan\nartifact_id: SPEC-0104\n---\n# Invalid\n",
                encoding="utf-8",
            )
            for args in (
                ("init", "-q"),
                ("add", "."),
                (
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "baseline",
                ),
            ):
                subprocess.run(
                    ["git", *args], cwd=root, check=True, capture_output=True
                )
            findings = validate_repository_contracts(
                root, metadata.build_registry_profiles(self.registry)
            )
            self.assertIn("type-mismatch", {item.code for item in findings})

    def test_current_profile_envelope_never_loads_legacy_authority(self) -> None:
        from scripts.lib.document_governance import metadata_validator

        profiles = metadata_validator.build_registry_profiles(self.registry)
        self.assertEqual(set(self.registry.profiles), set(profiles["profiles"]))
        self.assertNotIn("_legacy_profiles", profiles)
        self.assertEqual(
            "unsupported",
            metadata_validator.infer_artifact_type(
                pathlib.Path("docs/90.references/ref-9999-legacy.md"), profiles
            ),
        )

    @classmethod
    def setUpClass(cls) -> None:
        from scripts.lib.document_governance.registry import load_registry

        cls.registry = load_registry(PROFILES)
        cls.profiles = cls.registry.profiles

    def test_profiles_parse_and_publish_exact_incident_selector(self) -> None:
        incident = self.profiles["incident"]
        postmortem = self.profiles["postmortem"]
        self.assertEqual("inc-{year:4}-{number:4}", incident["artifact_id_pattern"])
        self.assertEqual(
            "docs/05.operations/incidents/{year:4}/inc-{number:4}-{slug}/incident.md",
            incident["path_pattern"],
        )
        self.assertEqual(
            "docs/05.operations/incidents/{year:4}/inc-{number:4}-{slug}/postmortem.md",
            postmortem["path_pattern"],
        )

    def test_profile_loader_accepts_only_bounded_digit_classes(self) -> None:
        from scripts.lib.document_governance.metadata_validator import (
            ProfileError,
            load_profiles,
        )

        loaded = load_profiles(PROFILES)
        self.assertEqual(self.profiles["incident"], loaded["incident"])
        unsafe = PROFILES.read_text(encoding="utf-8").replace(
            "{year:4}/inc-{number:4}", "{year:3}/inc-{number:4}", 1
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = pathlib.Path(directory) / "registry.json"
            temporary.write_text(unsafe, encoding="utf-8")
            with self.assertRaises(ProfileError):
                load_profiles(temporary)

    def test_internal_requirement_ids_are_four_digits(self) -> None:
        self.assertFalse(is_valid_internal_requirement_id("PRD-001-R001"))
        self.assertTrue(is_valid_internal_requirement_id("REQ-0001-FR-0001"))
        self.assertTrue(is_valid_internal_requirement_id("REQ-0001-NFR-0001"))
        self.assertTrue(is_valid_internal_requirement_id("REQ-0001-IF-0001"))
        self.assertFalse(is_valid_internal_requirement_id("FR-0001"))

    def test_incident_route_requires_year_and_four_digit_id(self) -> None:
        self.assertTrue(
            is_valid_incident_path(
                pathlib.PurePosixPath(
                    "docs/05.operations/incidents/2026/"
                    "inc-0001-control-plane-outage/incident.md"
                )
            )
        )
        self.assertTrue(
            is_valid_incident_path(
                pathlib.PurePosixPath(
                    "docs/05.operations/incidents/2026/"
                    "inc-0001-control-plane-outage/postmortem.md"
                )
            )
        )
        self.assertFalse(
            is_valid_incident_path(
                pathlib.PurePosixPath(
                    "docs/05.operations/incidents/inc-0001-control-plane-outage/"
                    "incident.md"
                )
            )
        )

    def test_stable_identity_allows_only_the_exact_incident_year_route(self) -> None:
        profiles = {
            "operation/incident": {
                "id_pattern": r"inc-[0-9]{4}-[0-9]{4}",
                "path_identity": "direct",
            }
        }
        metadata = {"type": "operation/incident", "artifact_id": "inc-2026-0001"}
        accepted = validate_stable_identity(
            pathlib.PurePosixPath(
                "docs/05.operations/incidents/2026/"
                "inc-0001-control-plane-outage/incident.md"
            ),
            metadata,
            profiles,
        )
        rejected = validate_stable_identity(
            pathlib.PurePosixPath(
                "docs/05.operations/incidents/inc-0001-control-plane-outage/incident.md"
            ),
            metadata,
            profiles,
        )
        self.assertEqual([], accepted)
        self.assertIn("incident-path-invalid", {finding.code for finding in rejected})
        self.assertFalse(
            is_valid_incident_path(
                pathlib.PurePosixPath(
                    "docs/05.operations/incidents/2026/"
                    "inc-001-control-plane-outage/incident.md"
                )
            )
        )

    def test_stable_identity_rejects_incident_role_file_swaps(self) -> None:
        profiles = {
            "operation/incident": {
                "id_pattern": r"inc-[0-9]{4}-[0-9]{4}",
                "path_identity": "direct",
            },
            "operation/postmortem": {
                "id_pattern": r"inc-[0-9]{4}-[0-9]{4}-PM",
                "path_identity": "inherited",
                "parent_id_pattern": r"inc-(?P<identity>[0-9]{4})-[a-z0-9-]+",
                "artifact_id_identity_pattern": r"inc-[0-9]{4}-(?P<identity>[0-9]{4})-PM",
                "identity_capture": "identity",
            },
        }
        packet = "docs/05.operations/incidents/2026/inc-0001-outage"
        swaps = (
            (
                pathlib.PurePosixPath(f"{packet}/postmortem.md"),
                {"type": "operation/incident", "artifact_id": "inc-2026-0001"},
            ),
            (
                pathlib.PurePosixPath(f"{packet}/incident.md"),
                {
                    "type": "operation/postmortem",
                    "artifact_id": "inc-2026-0001-PM",
                },
            ),
        )
        for path, metadata in swaps:
            with self.subTest(path=path, document_type=metadata["type"]):
                self.assertIn(
                    "incident-path-invalid",
                    {
                        finding.code
                        for finding in validate_stable_identity(
                            path, metadata, profiles
                        )
                    },
                )

    def test_metadata_validator_write_and_check_modes_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = pathlib.Path(directory) / "inventory.md"
            self.assertTrue(_write_or_check_output(output, "current\n", False))
            self.assertEqual("current\n", output.read_text(encoding="utf-8"))
            self.assertTrue(_write_or_check_output(output, "current\n", True))
            self.assertFalse(_write_or_check_output(output, "stale\n", True))
            self.assertEqual("current\n", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
