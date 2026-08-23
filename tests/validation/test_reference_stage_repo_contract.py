from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


def _topology_contract_source() -> str:
    source = (ROOT / "scripts/validation/check-repo-contracts.sh").read_text(
        encoding="utf-8"
    )
    section = source.split('section "Reference stage contract"', 1)[1]
    embedded = section.split("if ! python3 - <<'PY'; then\n", 1)[1].split(
        "\nPY\n", 1
    )[0]
    prefix = embedded.split("template_required = [", 1)[0]
    return (
        prefix
        + "\nif failures:\n"
        + "    print('\\n'.join(failures), file=sys.stderr)\n"
        + "    raise SystemExit(1)\n"
    )


def _run_topology_contract(root: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", _topology_contract_source()],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


class ReferenceStageRepoContractTests(unittest.TestCase):
    def _fixture(self, directory: str) -> pathlib.Path:
        root = pathlib.Path(directory)
        stage = root / "docs/90.references"
        for category in ("audits", "data", "research"):
            (stage / category).mkdir(parents=True, exist_ok=True)
        (stage / "README.md").write_text("# References\n", encoding="utf-8")
        registry = root / "docs/99.templates/registry.json"
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(json.dumps({"profiles": []}), encoding="utf-8")
        return root

    def test_exact_three_category_topology_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = _run_topology_contract(self._fixture(directory))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_retired_reference_roots_fail_closed(self) -> None:
        for retired in ("learning", "llm-wiki"):
            with self.subTest(retired=retired), tempfile.TemporaryDirectory() as directory:
                root = self._fixture(directory)
                (root / "docs/90.references" / retired).mkdir()
                result = _run_topology_contract(root)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    f"unsupported reference top-level entry: docs/90.references/{retired}",
                    result.stderr,
                )

    def test_root_readme_and_category_directories_are_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._fixture(directory)
            (root / "docs/90.references/README.md").unlink()
            result = _run_topology_contract(root)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "missing reference top-level file: docs/90.references/README.md",
                result.stderr,
            )

        with tempfile.TemporaryDirectory() as directory:
            root = self._fixture(directory)
            category = root / "docs/90.references/data"
            category.rmdir()
            category.write_text("not a directory\n", encoding="utf-8")
            result = _run_topology_contract(root)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "reference category is not a directory: docs/90.references/data",
                result.stderr,
            )


if __name__ == "__main__":
    unittest.main()
