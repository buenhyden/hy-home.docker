from __future__ import annotations

import unittest
from pathlib import PurePosixPath as P
from typing import ClassVar

from scripts.lib.document_governance.numbered_folders import (
    numbered_path,
    pre_numbered_path,
)


class NumberedFoldersTests(unittest.TestCase):
    CASES: ClassVar[dict[str, str]] = {
        "docs/00.workspace/02.process/sdlc.md": "docs/00.workspace/03.process/sdlc.md",
        "docs/00.workspace/02.process/approval-boundaries.md": (
            "docs/00.workspace/04.quality/approval-boundaries.md"
        ),
        ".agents/knowledge/glossary.md": "docs/00.workspace/01.project/glossary.md",
        "docs/05.operations/guides/01-common/0004-x.md": (
            "docs/05.operations/01.guides/01.common/0004-x.md"
        ),
        "docs/05.operations/incidents/2026/inc-0002-a/incident.md": (
            "docs/05.operations/04.incidents/2026/inc-0002-a/incident.md"
        ),
        "docs/99.templates/templates/specs/contracts/openapi.template.yaml": (
            "docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml"
        ),
        "docs/03.specs/0212-x/tasks/tsk-0001-y.md": "docs/03.specs/0212-x/01.tasks/tsk-0001-y.md",
        "docs/90.references/research/0002-p/m0001-a.md": (
            "docs/90.references/01.research/0002-p/m0001-a.md"
        ),
    }

    def test_routes_round_trip(self) -> None:
        for old, new in self.CASES.items():
            with self.subTest(old=old):
                self.assertEqual(P(new), numbered_path(P(old)))
                self.assertEqual(P(old), pre_numbered_path(P(new)))

    def test_unrelated_paths_are_unchanged_both_ways(self) -> None:
        for path in (
            "docs/01.requirements/0001-a.md",
            "infra/01-gateway/README.md",
            "docs/03.specs/README.md",
            "docs/05.operations/README.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(P(path), numbered_path(P(path)))
                self.assertEqual(P(path), pre_numbered_path(P(path)))

    def test_incident_year_partition_keeps_its_name(self) -> None:
        self.assertEqual(
            P("docs/05.operations/04.incidents/2026/README.md"),
            numbered_path(P("docs/05.operations/incidents/2026/README.md")),
        )


if __name__ == "__main__":
    unittest.main()
