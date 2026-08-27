import os
import re
import subprocess
import unittest
from pathlib import Path, PurePosixPath

import yaml

from scripts.lib.document_governance.taxonomy import (
    architecture_identity,
    find_dated_identity_parts,
    validate_stable_identity,
)


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md"

# These surfaces preserve migration provenance or time-bounded evidence; they do
# not publish active document-routing contracts. Active Stage 00, Stage 01–03,
# Stage 05, root/provider, template, and infrastructure surfaces remain scanned.
LEGACY_PATH_EVIDENCE_ALLOWLIST = (
    "docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md",
    "docs/04.execution/",
    "docs/90.references/audits/",
    "docs/90.references/data/0068-target-surface-convergence-summary/README.md",
    # Widened 2026-08-19 from the retiring research pack's own directory to the
    # whole research namespace, under the user-approved resolution of a Spec 137
    # gate 4 finding. An independent seat ruled that the narrower entry was
    # admitted under no admission route: route 3 covers literals the retirement
    # machinery needs in order to function, and this file is document-taxonomy
    # validation that the retiring pack merely contaminates. Naming the pack
    # directly here is therefore not permissible, while dropping the exemption
    # outright is not either, because six legacy Stage 01/02 paths across three
    # of that pack's files fail the scan below.
    #
    # Removal condition, and it is a narrowing rather than a deletion: when the
    # Spec 137 retirement completes and its post-deletion literal scan is
    # recorded, narrow this back to the successor pack's own directory. Until
    # then the successor pack is exempt too, which is the cost of the widening
    # and is the reason it is time-bounded rather than permanent.
    "docs/90.references/research/",
    "docs/98.archive/",
    "graphify-out/",
)

AD_TO_REQUIREMENT_PACKAGE = {
    "AD-0001": "REQ-0001",
    "AD-0002": "REQ-0002",
    "AD-0003": "REQ-0003",
    "AD-0004": "REQ-0004",
    "AD-0005": "REQ-0006",
    "AD-0006": "REQ-0007",
    "AD-0007": "REQ-0008",
    "AD-0008": "REQ-0009",
    "AD-0009": "REQ-0010",
    "AD-0010": "REQ-0011",
    "AD-0011": "REQ-0012",
    "AD-0012": "REQ-0005",
    "AD-0013": "REQ-0013",
    "AD-0014": "REQ-0014",
    "AD-0018": "REQ-0015",
    "AD-0019": "REQ-0016",
    "AD-0020": "REQ-0017",
    "AD-0021": "REQ-0018",
    "AD-0022": "REQ-0019",
    "AD-0023": "REQ-0020",
    "AD-0024": "REQ-0021",
    "AD-0025": "REQ-0022",
    "AD-0026": "REQ-0023",
    "AD-0027": "REQ-0024",
    "AD-0028": "REQ-0025",
}

ADR_TO_AD = {
    "ADR-0001": "AD-0001",
    "ADR-0002": "AD-0002",
    "ADR-0003": "AD-0003",
    "ADR-0004": "AD-0004",
    "ADR-0005": "AD-0005",
    "ADR-0006": "AD-0006",
    "ADR-0007": "AD-0007",
    "ADR-0008": "AD-0008",
    "ADR-0009": "AD-0009",
    "ADR-0010": "AD-0010",
    "ADR-0011": "AD-0011",
    "ADR-0015": "AD-0012",
    "ADR-0016": "AD-0013",
    "ADR-0017": "AD-0014",
    "ADR-0018": "AD-0018",
    "ADR-0019": "AD-0019",
    "ADR-0020": "AD-0020",
    "ADR-0021": "AD-0021",
    "ADR-0022": "AD-0022",
    "ADR-0023": "AD-0023",
    "ADR-0024": "AD-0024",
    "ADR-0025": "AD-0025",
    "ADR-0026": "AD-0026",
    "ADR-0027": "AD-0027",
    "ADR-0028": "AD-0028",
    "ADR-0029": "AD-0027",
}


def tracked_paths(pathspec: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--", pathspec],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def metadata_for(relative_path: str) -> dict[str, object]:
    text = (ROOT / relative_path).read_text()
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S)
    if match is None:
        raise AssertionError(f"missing frontmatter: {relative_path}")
    return yaml.safe_load(match.group(1))


def ledger_records() -> list[dict[str, object]]:
    match = re.search(r"```yaml\n(.*?)\n```", LEDGER.read_text(), flags=re.S)
    if match is None:
        raise AssertionError("migration ledger YAML block is missing")
    return yaml.safe_load(match.group(1))["records"]


def resolved_repo_path(source: str, destination: str) -> str | None:
    if destination.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
    base = re.split(r"[#?]", destination, maxsplit=1)[0]
    if not base:
        return None
    if base.startswith("/"):
        candidate = base.lstrip("/")
    elif base.startswith("docs/"):
        candidate = base
    else:
        candidate = str(PurePosixPath(source).parent / base)
    return os.path.normpath(candidate).replace(os.sep, "/")


class StableDocumentTaxonomyTests(unittest.TestCase):
    def test_stage_01_has_no_unprefixed_three_digit_documents(self):
        legacy_paths = [
            path
            for path in tracked_paths("docs/01.requirements")
            if re.fullmatch(
                r"docs/01\.requirements/[0-9]{3}-[^/]+\.md",
                path,
            )
        ]
        self.assertEqual([], legacy_paths)

    def test_stage_02_has_no_architecture_requirements_directory(self):
        self.assertEqual(
            [],
            tracked_paths("docs/02.architecture/requirements"),
        )

    def test_stage_01_requirement_package_filename_and_metadata_agree_exactly(self):
        paths = [
            path
            for path in tracked_paths("docs/01.requirements")
            if re.fullmatch(
                r"docs/01\.requirements/[0-9]{4}-[a-z0-9-]+\.md",
                path,
            )
        ]
        self.assertEqual(25, len(paths))
        self.assertEqual(
            {f"REQ-{number:04d}" for number in range(1, 26)},
            {metadata_for(path)["artifact_id"] for path in paths},
        )
        for path in paths:
            with self.subTest(path=path):
                match = re.fullmatch(
                    r"docs/01\.requirements/(?P<number>[0-9]{4})-[a-z0-9-]+\.md",
                    path,
                )
                self.assertIsNotNone(match)
                metadata = metadata_for(path)
                self.assertEqual(
                    f"REQ-{match.group('number')}", metadata["artifact_id"]
                )
                self.assertEqual("requirements-package", metadata["profile_id"])
                self.assertEqual(
                    "requirements-package", metadata["artifact_type"]
                )
                self.assertEqual([], metadata["parent_ids"])
                self.assertRegex(str(metadata["created"]), r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
                self.assertRegex(str(metadata["updated"]), r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

    def test_stage_02_description_filename_metadata_and_parent_agree_exactly(self):
        paths = [
            path
            for path in tracked_paths("docs/02.architecture/descriptions")
            if re.fullmatch(
                r"docs/02\.architecture/descriptions/[0-9]{4}-[a-z0-9-]+\.md",
                path,
            )
        ]
        self.assertEqual(25, len(paths))
        self.assertEqual(
            set(AD_TO_REQUIREMENT_PACKAGE),
            {metadata_for(path)["artifact_id"] for path in paths},
        )
        for path in paths:
            with self.subTest(path=path):
                match = re.fullmatch(
                    r"docs/02\.architecture/descriptions/(?P<number>[0-9]{4})-[a-z0-9-]+\.md",
                    path,
                )
                self.assertIsNotNone(match)
                metadata = metadata_for(path)
                artifact_id = f"AD-{match.group('number')}"
                self.assertEqual(artifact_id, metadata["artifact_id"])
                self.assertEqual("architecture-description", metadata["profile_id"])
                self.assertEqual("architecture-description", metadata["artifact_type"])
                self.assertEqual(
                    [AD_TO_REQUIREMENT_PACKAGE[artifact_id]], metadata["parent_ids"]
                )
                self.assertRegex(str(metadata["created"]), r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
                self.assertRegex(str(metadata["updated"]), r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

    def test_stage_02_adr_filename_metadata_and_parent_agree_exactly(self):
        paths = [
            path
            for path in tracked_paths("docs/02.architecture/decisions")
            if re.fullmatch(
                r"docs/02\.architecture/decisions/[0-9]{4}-[a-z0-9-]+\.md",
                path,
            )
        ]
        self.assertEqual(26, len(paths))
        self.assertEqual(set(ADR_TO_AD), {metadata_for(path)["artifact_id"] for path in paths})
        for path in paths:
            with self.subTest(path=path):
                match = re.fullmatch(
                    r"docs/02\.architecture/decisions/(?P<number>[0-9]{4})-[a-z0-9-]+\.md",
                    path,
                )
                self.assertIsNotNone(match)
                metadata = metadata_for(path)
                artifact_id = f"ADR-{match.group('number')}"
                self.assertEqual(artifact_id, metadata["artifact_id"])
                self.assertEqual("adr", metadata["profile_id"])
                self.assertEqual("adr", metadata["artifact_type"])
                self.assertEqual([ADR_TO_AD[artifact_id]], metadata["parent_ids"])
                self.assertRegex(str(metadata["created"]), r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
                self.assertRegex(str(metadata["updated"]), r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

    def test_description_readme_ledger_row_is_a_move_to_descriptions(self):
        rows = {
            row["legacy_path"]: row
            for row in ledger_records()
        }
        row = rows["docs/02.architecture/requirements/README.md"]
        self.assertEqual("docs/02.architecture/descriptions/README.md", row["stable_path"])
        self.assertEqual("move", row["action"])
        self.assertIsNone(row["artifact_id"])

    def test_tracked_markdown_has_no_inbound_link_to_moved_stage_01_or_02_path(self):
        legacy_paths = {
            str(row["legacy_path"])
            for row in ledger_records()
            if row["action"] == "move"
            and (
                str(row["legacy_path"]).startswith("docs/01.requirements/")
                or str(row["legacy_path"]).startswith("docs/02.architecture/")
            )
            and architecture_identity(PurePosixPath(str(row["legacy_path"])))
            is None
        }
        destinations = re.compile(
            r"!?\[[^\]\n]*\]\(([^\s)]+)|"
            r"^\[[^\]\n]+\]:\s*(\S+)|"
            r"\b(?:href|src)=[\"']([^\"']+)",
            flags=re.M,
        )
        violations: list[str] = []
        for source in tracked_paths("*.md"):
            if source == str(LEDGER.relative_to(ROOT)):
                continue
            source_path = ROOT / source
            if not source_path.is_file():
                continue
            for match in destinations.finditer(source_path.read_text()):
                destination = next(group for group in match.groups() if group is not None)
                resolved = resolved_repo_path(source, destination)
                if resolved in legacy_paths:
                    violations.append(f"{source}: {destination} -> {resolved}")
        self.assertEqual([], violations)

    def test_active_markdown_publishes_no_legacy_stage_01_or_02_path(self):
        forbidden = re.compile(
            r"01\.requirements/[0-9]{3}-[a-z0-9-]+\.md|"
            r"02\.architecture/requirements/|"
            r"02\.architecture/descriptions/ad-[0-9]{4}-[a-z0-9-]+\.md|"
            r"02\.architecture/decisions/adr-[0-9]{4}-[a-z0-9-]+\.md"
        )
        violations: list[str] = []
        for relative in tracked_paths("*.md"):
            if any(
                relative == prefix or relative.startswith(prefix)
                for prefix in LEGACY_PATH_EVIDENCE_ALLOWLIST
            ):
                continue
            for line_number, line in enumerate(
                (ROOT / relative).read_text().splitlines(),
                start=1,
            ):
                if forbidden.search(line):
                    violations.append(f"{relative}:{line_number}: {line.strip()}")
        self.assertEqual([], violations)

    def test_stage_01_and_02_publish_no_legacy_architecture_vocabulary(self):
        forbidden = re.compile(
            r"Architecture (?:Requirements|Reference) Document|"
            r"architecture-requirements|"
            r"docs/02\.architecture/requirements|"
            r"\bARD\b|"
            r"artifact_type:\s*ard|"
            r"\bard:",
            flags=re.I,
        )
        violations: list[str] = []
        for pathspec in ("docs/01.requirements", "docs/02.architecture"):
            for relative in tracked_paths(pathspec):
                path = ROOT / relative
                if path.suffix != ".md":
                    continue
                if forbidden.search(path.read_text()):
                    violations.append(relative)
        self.assertEqual([], violations)

    def test_rejects_date_prefix_and_year_partition(self):
        self.assertEqual(
            ("2026", "2026-08-09-audit.md"),
            find_dated_identity_parts(
                PurePosixPath(
                    "docs/90.references/research/2026/2026-08-09-audit.md"
                )
            ),
        )

    def test_accepts_architecture_description_identity(self):
        path = PurePosixPath(
            "docs/02.architecture/descriptions/0001-gateway.md"
        )
        self.assertEqual(
            ("architecture-description", "AD-0001"),
            architecture_identity(path),
        )
        findings = validate_stable_identity(
            path,
            {
                "artifact_id": "AD-0001",
                "artifact_type": "architecture-description",
            },
            {
                "architecture-description": {
                    "path_pattern": "docs/02.architecture/descriptions/{number:4}-{slug}.md",
                    "artifact_id_pattern": "AD-{number:4}",
                    "identity_relation": "direct",
                }
            },
        )
        self.assertEqual([], findings)

    def test_accepts_inherited_task_role_identity(self):
        findings = validate_stable_identity(
            PurePosixPath(
                "docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md"
            ),
            {
                "artifact_id": "task-0136-01",
                "artifact_type": "task",
            },
            {
                "task": {
                    "id_pattern": r"task-[0-9]{4}-[0-9]{2}",
                    "path_identity": "inherited",
                    "parent_id_pattern": (
                        r"spec-(?P<identity>[0-9]{4})-[a-z0-9-]+"
                    ),
                    "artifact_id_identity_pattern": (
                        r"task-(?P<identity>[0-9]{4})-[0-9]{2}"
                    ),
                    "identity_capture": "identity",
                }
            },
        )
        self.assertEqual([], findings)

    def test_rejects_inherited_task_role_with_mismatched_identity(self):
        findings = validate_stable_identity(
            PurePosixPath(
                "docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md"
            ),
            {
                "artifact_id": "task-9999-01",
                "artifact_type": "task",
            },
            {
                "task": {
                    "id_pattern": r"task-[0-9]{4}-[0-9]{2}",
                    "path_identity": "inherited",
                    "parent_id_pattern": (
                        r"spec-(?P<identity>[0-9]{4})-[a-z0-9-]+"
                    ),
                    "artifact_id_identity_pattern": (
                        r"task-(?P<identity>[0-9]{4})-[0-9]{2}"
                    ),
                    "identity_capture": "identity",
                }
            },
        )
        self.assertEqual(
            ["path-id-mismatch"],
            [finding.code for finding in findings],
        )

    def test_rejects_inherited_task_role_without_stable_parent(self):
        findings = validate_stable_identity(
            PurePosixPath("docs/03.specs/temporary-task/task.md"),
            {
                "artifact_id": "task-0136-01",
                "artifact_type": "task",
            },
            {
                "task": {
                    "id_pattern": r"task-[0-9]{4}-[0-9]{2}",
                    "path_identity": "inherited",
                    "parent_id_pattern": (
                        r"spec-(?P<identity>[0-9]{4})-[a-z0-9-]+"
                    ),
                    "artifact_id_identity_pattern": (
                        r"task-(?P<identity>[0-9]{4})-[0-9]{2}"
                    ),
                    "identity_capture": "identity",
                }
            },
        )
        self.assertEqual(
            [
                "path-id-mismatch",
            ],
            [finding.code for finding in findings],
        )


if __name__ == "__main__":
    unittest.main()
