from __future__ import annotations

import contextlib
import dataclasses
import io
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

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


class FourDigitDocumentIdentityTests(unittest.TestCase):
    def test_native_migration_compaction_requires_both_exact_provenance_states(
        self,
    ) -> None:
        from scripts.lib.document_governance import (
            archive,
        )
        from scripts.lib.document_governance import (
            metadata_validator as metadata,
        )

        path = pathlib.Path(
            "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        )
        profiles = metadata.build_registry_profiles(self.registry)
        base = next(
            row["recovery_commit"]
            for row in archive._migration_document(ROOT)["rows"]
            if row["source_path"]
            == "docs/03.specs/0153-workspace-governance-simplification/spec.md"
            and row["action"] == "delete"
        )
        record = metadata._record_from_text(
            path,
            (ROOT / path).read_text(),
            profiles=profiles,
            previous_status="archived",
        )
        witness = metadata._native_migration_compaction_witness(ROOT, record, base)
        self.assertEqual(record, witness)
        # The current lifecycle requires sealed records, but this exact ledger
        # is frozen with its legacy completed status. Registry owns that narrow
        # status exception and the witness still binds its historical transition
        # to the verified native compact state.
        self.assertNotIn(
            "invalid-status",
            {
                finding.code
                for finding in metadata.validate_record(record, profiles, {})
            },
        )
        self.assertNotIn(
            "frontmatter-order",
            {
                finding.code
                for finding in metadata.validate_record(record, profiles, {})
            },
        )
        self.assertIn(
            "invalid-transition",
            {
                finding.code
                for finding in metadata.validate_record(record, profiles, {})
            },
        )
        self.assertNotIn(
            "invalid-transition",
            {
                finding.code
                for finding in metadata.validate_record(
                    record, profiles, {}, migration_compaction_witness=witness
                )
            },
        )
        for changed in (
            {"path": path.with_name("0004-other.md")},
            {"metadata": {**record.metadata, "artifact_id": "mig-0004"}},
            {"metadata": {**record.metadata, "status": "active"}},
            {"previous_status": "superseded"},
        ):
            with self.subTest(changed=changed):
                other = dataclasses.replace(record, **changed)
                # The witness is exact: any near miss fails to bind. This is
                # the property under test, and it is unchanged.
                self.assertIsNone(
                    metadata._native_migration_compaction_witness(ROOT, other, base)
                )
                codes = {
                    finding.code
                    for finding in metadata.validate_record(
                        other, profiles, {}, migration_compaction_witness=witness
                    )
                }
                self.assertIn("invalid-transition", codes)
                if "path" in changed:
                    self.assertIn("frontmatter-order", codes)
        for invalid_base in (None, "0" * 40):
            with self.subTest(base=invalid_base):
                self.assertIsNone(
                    metadata._native_migration_compaction_witness(
                        ROOT, record, invalid_base
                    )
                )
        with mock.patch.object(
            archive.HistoricalDocument, "read_bytes", return_value=b"unproved history"
        ):
            self.assertIsNone(
                metadata._native_migration_compaction_witness(ROOT, record, base)
            )
        current = (ROOT / path).read_bytes()
        malformed_states = {
            "schema": current.replace(b"schema_version: 3", b"schema_version: 4", 1),
            "mapping": current.replace(
                b"source_path: docs/03.specs/spec-0153-workspace-governance-simplification/spec.md",
                b"source_path: docs/03.specs/spec-0153-unproved/spec.md",
                1,
            ),
            "recovery": current.replace(
                b"recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525",
                b"recovery_commit: " + b"0" * 40,
                1,
            ),
            "envelope": current.replace(
                b"parent_ids: [ADR-0029]", b"parent_ids: []", 1
            ),
        }
        for failure, malformed in malformed_states.items():
            self.assertNotEqual(current, malformed)
            with (
                self.subTest(failure=failure),
                mock.patch.object(archive, "_read_regular", return_value=malformed),
            ):
                self.assertIsNone(
                    metadata._native_migration_compaction_witness(ROOT, record, base)
                )
        with mock.patch.object(
            archive, "_migration_document", return_value={"schema_version": 2}
        ):
            self.assertIsNone(
                metadata._native_migration_compaction_witness(ROOT, record, base)
            )

    def test_retired_spec_lineage_is_relation_only_and_requires_real_recovery(
        self,
    ) -> None:
        from scripts.lib.document_governance import metadata_validator as metadata
        from scripts.lib.document_governance.metadata import reference

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = "docs/03.specs/0153-example/spec.md"
            path = root / source
            path.parent.mkdir(parents=True)
            path.write_text(
                "---\nartifact_id: SPEC-0153\nartifact_type: spec\nstatus: completed\nsupersedes: [SPEC-0136]\n---\n# Recovered\n",
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
                    "recoverable spec",
                ),
            ):
                subprocess.run(
                    ["git", *args], cwd=root, check=True, capture_output=True
                )
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            path.unlink()
            migration_path = (
                root
                / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
            )
            migration_path.parent.mkdir(parents=True)
            migration_path.write_text("fixture boundary", encoding="utf-8")
            row = {
                "source_path": source,
                "artifact_id": "SPEC-0153",
                "action": "delete",
                "target_path": None,
                "recovery_commit": commit,
            }
            record = metadata.Record(
                pathlib.Path("docs/03.specs/0136-original/spec.md"),
                {"artifact_id": "SPEC-0136", "superseded_by": "SPEC-0153"},
                "spec",
            )
            # Native compact selection has its own real-905 integration test;
            # this injects only that parsed boundary, not Git/blob recovery.
            with mock.patch(
                "scripts.lib.document_governance.archive._migration_document",
                return_value={"schema_version": 3, "rows": [row]},
            ):
                manifest = metadata.build_current_manifest(root, [record])
                self.assertNotIn("SPEC-0153", manifest)
                self.assertEqual(
                    "retired",
                    manifest.relation_records_by_id["SPEC-0153"].metadata["status"],
                )
                self.assertEqual(
                    ["SPEC-0136"],
                    manifest.relation_records_by_id["SPEC-0153"].metadata["supersedes"],
                )
                row["recovery_commit"] = "0" * 40
                with self.assertRaises(metadata.ProfileError):
                    metadata.build_current_manifest(root, [record])
                stderr = io.StringIO()
                with (
                    mock.patch.object(
                        reference, "collect_records", return_value=[record]
                    ),
                    contextlib.redirect_stderr(stderr),
                ):
                    result = metadata.main(
                        [
                            "--root",
                            str(root),
                            "--registry",
                            str(PROFILES),
                            "--mode",
                            "check-active",
                        ]
                    )
                self.assertEqual(2, result)
                self.assertIn(
                    "configuration-error: retired Spec lineage recovery is invalid",
                    stderr.getvalue(),
                )
                self.assertNotIn("Traceback", stderr.getvalue())
                row.update(recovery_commit=commit, artifact_id="SPEC-0152")
                record.metadata["superseded_by"] = "SPEC-0152"
                with self.assertRaises(metadata.ProfileError):
                    metadata.build_current_manifest(root, [record])
            with mock.patch(
                "scripts.lib.document_governance.archive._migration_document",
                return_value={"schema_version": 3, "rows": []},
            ):
                self.assertNotIn(
                    "SPEC-0152",
                    metadata.build_current_manifest(
                        root, [record]
                    ).relation_records_by_id,
                )

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
