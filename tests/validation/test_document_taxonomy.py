import unittest
from pathlib import PurePosixPath

from scripts.lib.document_governance.taxonomy import (
    find_dated_identity_parts,
    validate_stable_identity,
)


class StableDocumentTaxonomyTests(unittest.TestCase):
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
        findings = validate_stable_identity(
            PurePosixPath(
                "docs/02.architecture/descriptions/ad-0001-gateway.md"
            ),
            {
                "artifact_id": "ad-0001",
                "artifact_type": "architecture-description",
            },
            {
                "architecture-description": {
                    "id_pattern": r"ad-[0-9]{4}",
                }
            },
        )
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
