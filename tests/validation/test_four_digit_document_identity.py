from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

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


ROOT = pathlib.Path(__file__).resolve().parents[2]
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

    def test_srs_and_interface_templates_publish_internal_id_patterns(self) -> None:
        expectations = {
            "docs/99.templates/templates/sdlc/srs.template.md": "SRS-####-R####",
            "docs/99.templates/templates/sdlc/interface-requirement.template.md": "IFR-####-R####",
        }
        for relative, pattern in expectations.items():
            with self.subTest(path=relative):
                self.assertIn(pattern, (ROOT / relative).read_text(encoding="utf-8"))

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

    def test_repo_contract_rejects_empty_incident_packet(self) -> None:
        checker = (
            ROOT / "scripts/validation/check-repo-contracts.sh"
        ).read_text(encoding="utf-8")
        section = checker.split(
            'section "Operations postmortem routing contract"', 1
        )[1]
        body = section.split("from __future__ import annotations", 1)[1]
        topology = (
            "from __future__ import annotations\n"
            + body.split("literal_requirements =", 1)[0]
            + "\n"
            + "for failure in failures:\n"
            + "    print(failure, file=sys.stderr)\n"
            + "raise SystemExit(1 if failures else 0)\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            packet = (
                root
                / "docs/05.operations/incidents/2026/inc-0001-empty-packet"
            )
            packet.mkdir(parents=True)
            result = subprocess.run(
                [sys.executable, "-c", topology],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("incident packet is missing incident.md", result.stderr)

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
            "docs/00.agent-governance/policies/stage-authoring-matrix.md",
            "docs/05.operations/incidents/README.md",
            "docs/99.templates/support/template-selection.md",
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
