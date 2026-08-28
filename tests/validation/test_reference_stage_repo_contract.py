from __future__ import annotations

import pathlib
import tempfile
import unittest

from scripts.lib.document_governance.references import (
    CATEGORIES,
    ReferenceCorpusError,
    load_reference_packages,
)
from scripts.validation.ci_gate_contract import (
    load_contract_document,
    load_public_suite_registry,
    parse_public_gate_contract,
    select_public_suites,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


class ReferenceStageRepoContractTests(unittest.TestCase):
    def _fixture(self, directory: str) -> pathlib.Path:
        root = pathlib.Path(directory)
        stage = root / "docs/90.references"
        for category in ("audits", "data", "research"):
            (stage / category).mkdir(parents=True, exist_ok=True)
            (stage / category / "README.md").write_text(
                f"# {category.title()}\n", encoding="utf-8"
            )
        (stage / "README.md").write_text("# References\n", encoding="utf-8")
        return root

    def test_exact_three_category_topology_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = load_reference_packages(
                self._fixture(directory) / "docs/90.references"
            )
        self.assertEqual(CATEGORIES, corpus.category_names)

    def test_retired_reference_roots_fail_closed(self) -> None:
        for retired in ("learning", "llm-wiki"):
            with self.subTest(retired=retired), tempfile.TemporaryDirectory() as directory:
                root = self._fixture(directory)
                (root / "docs/90.references" / retired).mkdir()
                corpus = load_reference_packages(root / "docs/90.references")
                self.assertNotEqual(
                    CATEGORIES,
                    corpus.category_names,
                )
                self.assertIn(retired, corpus.category_names)

    def test_root_readme_and_category_directories_are_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._fixture(directory)
            (root / "docs/90.references/README.md").unlink()
            with self.assertRaisesRegex(
                ReferenceCorpusError,
                "docs/90.references is missing README.md",
            ):
                load_reference_packages(root / "docs/90.references")

        with tempfile.TemporaryDirectory() as directory:
            root = self._fixture(directory)
            category = root / "docs/90.references/data"
            (category / "README.md").unlink()
            category.rmdir()
            category.write_text("not a directory\n", encoding="utf-8")
            with self.assertRaisesRegex(
                ReferenceCorpusError,
                "docs/90.references/data must be a category directory",
            ):
                load_reference_packages(root / "docs/90.references")

    def test_public_changed_profile_selects_reference_validators(self) -> None:
        suite_registry = load_public_suite_registry(ROOT / "scripts/manifest.yaml")
        contract = parse_public_gate_contract(
            load_contract_document(ROOT), suite_registry
        )
        selected = select_public_suites(
            contract,
            "changed",
            ("docs/90.references/data/0082-llm-wiki-index/README.md",),
        )
        self.assertEqual(
            (
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "repository-integrity",
            ),
            selected,
        )


if __name__ == "__main__":
    unittest.main()
