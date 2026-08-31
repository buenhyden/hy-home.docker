from __future__ import annotations

import contextlib
import dataclasses
import io
import pathlib
import re
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts.lib.document_governance import metadata_contract
from scripts.lib.document_governance.metadata_validator import (
    _write_or_check_output,
    validate_repository_contracts,
    validate_prd_internal_id_contract,
    validate_requirement_internal_id_contract,
)
from scripts.lib.document_governance.taxonomy import (
    is_valid_incident_path,
    is_valid_internal_requirement_id,
    requirement_package_identity,
    validate_stable_identity,
)
from scripts.lib.gate.ci_gate_contract import (
    load_contract_document,
    load_public_suite_registry,
    parse_public_gate_contract,
    select_public_suites,
)


ROOT = pathlib.Path(__file__).resolve().parents[3]
PROFILES = ROOT / "docs/99.templates/registry.json"
INCIDENT_ROUTE = "docs/05.operations/incidents/<year>/inc-####-<slug>/"
THREE_DIGIT_COMPONENT = re.compile(
    r"^(?:prd|srs|interface|ad|adr|spec|ops|inc|rel|chg|mig|ref|audit)-[0-9]{3}-"
)
THREE_DIGIT_ARTIFACT_ID = re.compile(
    r"^artifact_id:\s*(?:prd|srs|interface|ad|adr|spec|ops|inc|rel|chg|mig|ref|audit)-[0-9]{3}\s*$",
    re.MULTILINE,
)
class FourDigitDocumentIdentityTests(unittest.TestCase):
    def test_native_migration_compaction_requires_both_exact_provenance_states(self) -> None:
        from scripts.lib.document_governance import archive, metadata_validator as metadata

        path = pathlib.Path("docs/98.archive/migrations/0003-workspace-governance-simplification.md")
        profiles = metadata.build_registry_profiles(self.registry)
        base = next(
            row["recovery_commit"] for row in archive._migration_document(ROOT)["rows"]
            if row["source_path"] == "docs/03.specs/0153-workspace-governance-simplification/spec.md"
            and row["action"] == "delete"
        )
        record = metadata._record_from_text(
            path, (ROOT / path).read_text(), profiles=profiles, previous_status="archived"
        )
        witness = metadata._native_migration_compaction_witness(ROOT, record, base)
        self.assertEqual(record, witness)
        # `archived` is not a status any lifecycle defines, so moving to a
        # defined status is a repair and no longer needs this witness to
        # suppress `invalid-transition`. The witness stays exercised below for
        # the provenance binding it verifies; its transition role is subsumed
        # and its removal belongs to the provenance narrowing in SPEC-0155.
        self.assertNotIn("invalid-transition", {
            finding.code for finding in metadata.validate_record(record, profiles, {})
        })
        self.assertNotIn("invalid-transition", {
            finding.code for finding in metadata.validate_record(
                record, profiles, {}, migration_compaction_witness=witness
            )
        })
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
                self.assertIsNone(metadata._native_migration_compaction_witness(ROOT, other, base))
                codes = {
                    finding.code for finding in metadata.validate_record(
                        other, profiles, {}, migration_compaction_witness=witness
                    )
                }
                # Whether a near miss also reports `invalid-transition` now
                # depends on its statuses, not on the witness. The `historical`
                # lifecycle defines draft, completed, and superseded. Leaving
                # `archived`, which it does not define, for `completed`, which
                # it does, is a repair. Leaving `superseded` for `completed` is
                # a forbidden move between two defined statuses, and moving to
                # `active` lands on a status this lifecycle never defined.
                repair = (
                    other.previous_status == "archived"
                    and other.metadata.get("status") == "completed"
                )
                if repair:
                    self.assertNotIn("invalid-transition", codes)
                else:
                    self.assertIn("invalid-transition", codes)
        for invalid_base in (None, "0" * 40):
            with self.subTest(base=invalid_base):
                self.assertIsNone(metadata._native_migration_compaction_witness(ROOT, record, invalid_base))
        with mock.patch.object(archive.HistoricalDocument, "read_bytes", return_value=b"unproved history"):
            self.assertIsNone(metadata._native_migration_compaction_witness(ROOT, record, base))
        current = (ROOT / path).read_bytes()
        malformed_states = {
            "schema": current.replace(b"schema_version: 3", b"schema_version: 4", 1),
            "mapping": current.replace(
                b"source_path: docs/03.specs/spec-0153-workspace-governance-simplification/spec.md",
                b"source_path: docs/03.specs/spec-0153-unproved/spec.md", 1,
            ),
            "recovery": current.replace(
                b"recovery_commit: 889d3868ecd0913cddac79a718584a54a8453525",
                b"recovery_commit: " + b"0" * 40, 1,
            ),
            "envelope": current.replace(b"parent_ids: [ADR-0029]", b"parent_ids: []", 1),
        }
        for failure, malformed in malformed_states.items():
            self.assertNotEqual(current, malformed)
            with self.subTest(failure=failure), mock.patch.object(archive, "_read_regular", return_value=malformed):
                self.assertIsNone(metadata._native_migration_compaction_witness(ROOT, record, base))
        with mock.patch.object(archive, "_migration_document", return_value={"schema_version": 2}):
            self.assertIsNone(metadata._native_migration_compaction_witness(ROOT, record, base))

    def test_retired_spec_lineage_is_relation_only_and_requires_real_recovery(self) -> None:
        from scripts.lib.document_governance import metadata_validator as metadata

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = "docs/03.specs/0153-example/spec.md"
            path = root / source
            path.parent.mkdir(parents=True)
            path.write_text("---\nartifact_id: SPEC-0153\nartifact_type: spec\nstatus: completed\nsupersedes: [SPEC-0136]\n---\n# Recovered\n", encoding="utf-8")
            for args in (("init", "-q"), ("add", "."), ("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "recoverable spec")):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            path.unlink()
            migration_path = root / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
            migration_path.parent.mkdir(parents=True)
            migration_path.write_text("fixture boundary", encoding="utf-8")
            row = {"source_path": source, "artifact_id": "SPEC-0153", "action": "delete", "target_path": None, "recovery_commit": commit}
            record = metadata.Record(pathlib.Path("docs/03.specs/0136-original/spec.md"), {"artifact_id": "SPEC-0136", "superseded_by": "SPEC-0153"}, "spec")
            # Native compact selection has its own real-905 integration test;
            # this injects only that parsed boundary, not Git/blob recovery.
            with mock.patch("scripts.lib.document_governance.archive._migration_document", return_value={"schema_version": 3, "rows": [row]}):
                manifest = metadata.build_current_manifest(root, [record])
                self.assertNotIn("SPEC-0153", manifest)
                self.assertEqual("retired", manifest.relation_records_by_id["SPEC-0153"].metadata["status"])
                self.assertEqual(["SPEC-0136"], manifest.relation_records_by_id["SPEC-0153"].metadata["supersedes"])
                row["recovery_commit"] = "0" * 40
                with self.assertRaises(metadata.ProfileError):
                    metadata.build_current_manifest(root, [record])
                stderr = io.StringIO()
                with mock.patch.object(metadata, "collect_records", return_value=[record]), contextlib.redirect_stderr(stderr):
                    result = metadata.main(["--root", str(root), "--registry", str(PROFILES), "--mode", "check-active"])
                self.assertEqual(2, result)
                self.assertIn("configuration-error: retired Spec lineage recovery is invalid", stderr.getvalue())
                self.assertNotIn("Traceback", stderr.getvalue())
                row.update(recovery_commit=commit, artifact_id="SPEC-0152")
                record.metadata["superseded_by"] = "SPEC-0152"
                with self.assertRaises(metadata.ProfileError):
                    metadata.build_current_manifest(root, [record])
            with mock.patch("scripts.lib.document_governance.archive._migration_document", return_value={"schema_version": 3, "rows": []}):
                self.assertNotIn("SPEC-0152", metadata.build_current_manifest(root, [record]).relation_records_by_id)

    def test_full_repository_contracts_reaches_active_record_validation(self) -> None:
        from scripts.lib.document_governance import metadata_validator as metadata

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(PROFILES.read_bytes())
            document = root / "docs/03.specs/0104-example/spec.md"
            document.parent.mkdir(parents=True)
            document.write_text("---\nstatus: active\nartifact_id: SPEC-0104\n---\n# Invalid\n", encoding="utf-8")
            for args in (("init", "-q"), ("add", "."), ("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "baseline")):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            findings = validate_repository_contracts(root, metadata.build_registry_profiles(self.registry))
            self.assertIn("profile-id-mismatch", {item.code for item in findings})

    def test_current_profile_envelope_never_loads_legacy_authority(self) -> None:
        from scripts.lib.document_governance import metadata_validator

        profiles = metadata_validator.build_registry_profiles(self.registry)
        self.assertEqual(set(self.registry.profiles), set(profiles["profiles"]))
        self.assertNotIn("_legacy_profiles", profiles)
        self.assertEqual("unsupported", metadata_validator.infer_artifact_type(
            pathlib.Path("docs/90.references/ref-9999-legacy.md"), profiles
        ))

    def test_metadata_contract_uses_the_canonical_registry(self) -> None:
        self.assertEqual(
            PROFILES,
            metadata_contract.DEFAULT_REGISTRY,
        )

    @classmethod
    def setUpClass(cls) -> None:
        from scripts.lib.document_governance.registry import load_registry

        cls.registry = load_registry(PROFILES)
        cls.profiles = cls.registry.profiles

    def test_every_tracked_typed_document_path_uses_four_digits(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files", "docs"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()
        invalid = sorted(
            path
            for path in tracked
            if path.startswith(
                (
                    "docs/01.requirements/",
                    "docs/02.architecture/",
                    "docs/03.specs/",
                    "docs/05.operations/",
                    "docs/90.references/",
                    "docs/98.archive/",
                )
            )
            if any(THREE_DIGIT_COMPONENT.match(part) for part in path.split("/"))
        )
        self.assertEqual([], invalid)

    def test_every_tracked_typed_document_frontmatter_uses_four_digits(self) -> None:
        invalid: list[str] = []
        for path in sorted((ROOT / "docs").rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if THREE_DIGIT_ARTIFACT_ID.search(text):
                invalid.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], invalid)

    def test_profiles_parse_and_publish_exact_incident_selector(self) -> None:
        incident = self.profiles["incident"]
        postmortem = self.profiles["postmortem"]
        self.assertEqual("inc-{number:4}", incident["artifact_id_pattern"])
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
            "incident": {
                "id_pattern": r"inc-[0-9]{4}",
                "path_identity": "direct",
            }
        }
        metadata = {"artifact_type": "incident", "artifact_id": "inc-0001"}
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
            "incident": {
                "id_pattern": r"inc-[0-9]{4}",
                "path_identity": "direct",
            },
            "postmortem": {
                "id_pattern": r"postmortem-[0-9]{4}",
                "path_identity": "inherited",
                "parent_id_pattern": r"inc-(?P<identity>[0-9]{4})-[a-z0-9-]+",
                "artifact_id_identity_pattern": r"postmortem-(?P<identity>[0-9]{4})",
                "identity_capture": "identity",
            },
        }
        packet = "docs/05.operations/incidents/2026/inc-0001-outage"
        swaps = (
            (
                pathlib.PurePosixPath(f"{packet}/postmortem.md"),
                {"artifact_type": "incident", "artifact_id": "inc-0001"},
            ),
            (
                pathlib.PurePosixPath(f"{packet}/incident.md"),
                {
                    "artifact_type": "postmortem",
                    "artifact_id": "postmortem-0001",
                },
            ),
        )
        for path, metadata in swaps:
            with self.subTest(path=path, artifact_type=metadata["artifact_type"]):
                self.assertIn(
                    "incident-path-invalid",
                    {
                        finding.code
                        for finding in validate_stable_identity(
                            path, metadata, profiles
                        )
                    },
                )

    def test_current_requirement_package_paths_own_their_ids(self) -> None:
        paths = sorted((ROOT / "docs/01.requirements").glob("[0-9][0-9][0-9][0-9]-*.md"))
        identities = tuple(
            requirement_package_identity(path.relative_to(ROOT)) for path in paths
        )
        self.assertEqual(25, len(paths))
        self.assertTrue(all(identity is not None for identity in identities))
        self.assertEqual(25, len(set(identities)))
        self.assertIsNone(
            requirement_package_identity(
                pathlib.PurePosixPath("docs/01.requirements/prd-0001-legacy.md")
            )
        )

    def test_prd_internal_id_validator_fails_closed(self) -> None:
        path = pathlib.Path("docs/01.requirements/prd-0001-example.md")
        valid = """## Requirements

- **PRD-0001-R0001**: requirement

## Non-functional Requirements

- **PRD-0001-R0002 — Quality**: requirement

## Acceptance and Verification

- **PRD-0001-AC0001**: acceptance
"""
        self.assertEqual([], validate_prd_internal_id_contract(path, valid))

        invalid = valid.replace("PRD-0001-R0001", "REQ-PRD-FUN-01").replace(
            "- **PRD-0001-AC0001**: acceptance",
            "- acceptance without an ID",
        )
        self.assertEqual(
            {"internal-id-invalid", "internal-id-legacy", "internal-id-missing"},
            {
                finding.code
                for finding in validate_prd_internal_id_contract(path, invalid)
            },
        )

    def test_prd_internal_id_validator_rejects_ids_in_adversarial_contexts(self) -> None:
        path = pathlib.Path("docs/01.requirements/prd-0001-example.md")
        canonical = """## Requirements

- **PRD-0001-R0001**: requirement

## Acceptance and Verification

- **PRD-0001-AC0001**: acceptance
"""
        adversarial = {
            "numbered-legacy": canonical + "\n1. REQ-PRD-FUN-01: hidden legacy ID\n",
            "lowercase-bypass": canonical + "\nprd-001-r001: malformed ID\n",
            "unsupported-kind": canonical + "\n1. PRD-0001-X0001: invalid kind\n",
            "indented-extra": canonical + "\n   - PRD-0001-R0002: undeclared ID\n",
            "blockquote-owner": canonical + "\n> PRD-9999-R0001: wrong owner\n",
            "list-acceptance": canonical + "\n* PRD-0001-AC0002: undeclared ID\n",
            "table-legacy": canonical + "\n| VAL-ORC-001 | hidden legacy ID |\n",
        }
        for context, document in adversarial.items():
            with self.subTest(context=context):
                self.assertTrue(
                    validate_prd_internal_id_contract(path, document),
                    context,
                )

    def test_requirement_sections_reject_idless_list_entries(self) -> None:
        path = pathlib.Path("docs/01.requirements/prd-0001-example.md")
        document = """## Requirements

- **PRD-0001-R0001**: requirement
1. missing typed id

## Acceptance and Verification

- **PRD-0001-AC0001**: acceptance
* another missing typed id
"""
        missing = [
            finding
            for finding in validate_prd_internal_id_contract(path, document)
            if finding.code == "internal-id-missing"
        ]
        self.assertEqual(2, len(missing))

    def test_requirement_sections_allow_ordinary_prose(self) -> None:
        path = pathlib.Path("docs/01.requirements/prd-0001-example.md")
        document = """## Requirements

This paragraph explains the requirement scope without declaring an entry.

- **PRD-0001-R0001**: requirement

## Acceptance and Verification

This paragraph explains how verification evidence will be interpreted.

- **PRD-0001-AC0001**: acceptance
"""
        self.assertEqual([], validate_prd_internal_id_contract(path, document))

    def test_prd_internal_id_validator_allows_declared_id_references(self) -> None:
        path = pathlib.Path("docs/01.requirements/prd-0001-example.md")
        document = """## Requirements

- **PRD-0001-R0001**: requirement

## Acceptance and Verification

- **PRD-0001-AC0001**: acceptance

## Traceability

`PRD-0001-R0001` is verified by PRD-0001-AC0001.
"""
        self.assertEqual([], validate_prd_internal_id_contract(path, document))

    def test_prd_internal_id_validator_enforces_owner_and_uniqueness(self) -> None:
        path = pathlib.Path("docs/01.requirements/prd-0001-example.md")
        wrong_owner = """## Requirements

- **PRD-0002-R0001**: requirement

## Acceptance and Verification

- **PRD-0001-AC0001**: acceptance
"""
        duplicate = """## Requirements

- **PRD-0001-R0001**: requirement
- **PRD-0001-R0001**: duplicate requirement

## Acceptance and Verification

- **PRD-0001-AC0001**: acceptance
"""
        self.assertIn(
            "internal-id-invalid",
            {
                finding.code
                for finding in validate_prd_internal_id_contract(path, wrong_owner)
            },
        )
        self.assertIn(
            "internal-id-duplicate",
            {
                finding.code
                for finding in validate_prd_internal_id_contract(path, duplicate)
            },
        )

    def test_srs_and_interface_internal_ids_are_repository_contracts(self) -> None:
        fixtures = {
            pathlib.Path("docs/01.requirements/srs-0001-example.md"): (
                """## System Behavior

- **SRS-0001-R0001**: behavior

## Quality Requirements

- **SRS-0001-R0002**: quality
""",
                "SRS-0001-R0001",
            ),
            pathlib.Path("docs/01.requirements/interface-0001-example.md"): (
                """## Information Semantics

- **IFR-0001-R0001**: semantics

## Constraints and Compatibility

- **IFR-0001-R0002**: compatibility
""",
                "IFR-0001-R0001",
            ),
        }
        for path, (valid, first_identity) in fixtures.items():
            with self.subTest(path=path, state="valid"):
                self.assertEqual(
                    [], validate_requirement_internal_id_contract(path, valid)
                )
            adversarial = valid + (
                f"\n> {first_identity.lower()}: lowercase bypass\n"
                "1. REQ-LEGACY-01: legacy namespace\n"
                "- **SRS-9999-R0001**: foreign owner\n"
            )
            with self.subTest(path=path, state="adversarial"):
                self.assertTrue(
                    validate_requirement_internal_id_contract(path, adversarial)
                )

    def test_requirement_template_publishes_all_owned_child_id_patterns(self) -> None:
        text = (ROOT / "docs/99.templates/templates/requirements/requirement-package.template.md").read_text(encoding="utf-8")
        for kind in ("FR", "NFR", "IF"):
            with self.subTest(kind=kind):
                self.assertIn(f"REQ-####-{kind}-####", text)

    def test_requirement_repository_contract_rejects_symlink_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            requirement_root = root / "docs/01.requirements"
            requirement_root.mkdir(parents=True)
            outside = root.parent / f"{root.name}-outside-prd.md"
            outside.write_text(
                """## Requirements

- **PRD-0001-R0001**: external requirement

## Acceptance and Verification

- **PRD-0001-AC0001**: external acceptance
""",
                encoding="utf-8",
            )
            linked = requirement_root / "prd-0001-linked.md"
            linked.symlink_to(outside)
            subprocess.run(["git", "add", "docs"], cwd=root, check=True)
            try:
                findings = validate_repository_contracts(root, {})
            finally:
                outside.unlink(missing_ok=True)
        self.assertIn(
            "requirement-source-symlink",
            {finding.code for finding in findings},
        )

    def test_metadata_validator_write_and_check_modes_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = pathlib.Path(directory) / "inventory.md"
            self.assertTrue(_write_or_check_output(output, "current\n", False))
            self.assertEqual("current\n", output.read_text(encoding="utf-8"))
            self.assertTrue(_write_or_check_output(output, "current\n", True))
            self.assertFalse(_write_or_check_output(output, "stale\n", True))
            self.assertEqual("current\n", output.read_text(encoding="utf-8"))

    def test_public_gate_routes_incident_packets_through_operations(self) -> None:
        suite_registry = load_public_suite_registry(ROOT / "scripts/manifest.yaml")
        operations = next(
            suite for suite in suite_registry.suites if suite.name == "operations"
        )
        self.assertEqual(
            1,
            operations.validators.count(
                pathlib.PurePosixPath(
                    "scripts/validation/check-operations-catalog.py"
                )
            ),
        )
        contract = parse_public_gate_contract(
            load_contract_document(ROOT), suite_registry
        )
        self.assertEqual(
            (
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "operations",
                "repository-integrity",
            ),
            select_public_suites(
                contract,
                "changed",
                (
                    "docs/05.operations/incidents/2026/"
                    "inc-0001-empty-packet/incident.md",
                ),
            ),
        )

    def test_active_contracts_publish_no_ambiguous_typed_id_routes(self) -> None:
        tracked = subprocess.run(
            [
                "git",
                "ls-files",
                "docs/00.agent-governance",
                "docs/99.templates",
                ".agents/skills",
                ".claude/skills",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()
        ambiguous = re.compile(
            r"\b(?:prd|srs|interface|ad|adr|spec|ops|inc|rel|chg|mig|ref|audit|plan|task)-<id>"
        )
        violations: list[str] = []
        for relative in tracked:
            if relative.startswith("docs/00.agent-governance/memory/"):
                continue
            path = ROOT / relative
            if path.suffix not in {".md", ".yaml", ".yml", ".graphql", ".proto"}:
                continue
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                if ambiguous.search(line):
                    violations.append(f"{relative}:{line_number}:{line.strip()}")
        self.assertEqual([], violations)

    def test_active_human_contracts_publish_only_the_canonical_incident_route(self) -> None:
        contracts = (
            "docs/00.agent-governance/skills/ops-runbook-agent.md",
            "docs/00.agent-governance/skills/incident-response.md",
            "docs/00.agent-governance/policies/documentation-protocol.md",
            "docs/05.operations/incidents/README.md",
        )
        missing: list[str] = []
        stale: list[str] = []
        for relative in contracts:
            text = (ROOT / relative).read_text(encoding="utf-8")
            if INCIDENT_ROUTE not in text:
                missing.append(relative)
            if "INC-###" in text or "inc-<id>" in text:
                stale.append(relative)
        self.assertEqual([], missing)
        self.assertEqual([], stale)


if __name__ == "__main__":
    unittest.main()
