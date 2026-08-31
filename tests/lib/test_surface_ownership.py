from __future__ import annotations

import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _manifest_rows() -> list[dict]:
    payload = yaml.safe_load(
        (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
    )
    rows = payload["files"]
    if not isinstance(rows, list) or not rows:
        raise AssertionError("scripts/manifest.yaml must carry a non-empty files list")
    return [row for row in rows if isinstance(row, dict)]


class SurfaceOwnershipTests(unittest.TestCase):
    """A directory states what its files are, and no constant restates it."""

    def test_every_library_package_has_a_test_directory(self) -> None:
        packages = {
            path.name
            for path in (ROOT / "scripts/lib").iterdir()
            if path.is_dir() and not path.name.startswith("__")
        }
        missing = sorted(
            name for name in packages if not (ROOT / "tests/lib" / name).is_dir()
        )
        self.assertEqual([], missing)

    def test_no_placeholder_test_directory_remains(self) -> None:
        for name in ("docs", "qa", "setup"):
            self.assertFalse(
                (ROOT / "tests" / name).exists(),
                f"tests/{name} described a structure that was never built",
            )

    def test_library_rows_declare_no_execution_context(self) -> None:
        """A library declares no execution context.

        This replaced a ban on `if __name__ == "__main__"` that would have been
        red eight ways. `ci_gate_adapters.py` carries that guard and is the
        declared entrypoint of thirty-four gate leaves, so the guard is not what
        makes a module a library here. Declaring no execution context is.
        """

        offenders = [
            row["path"]
            for row in _manifest_rows()
            if str(row.get("path", "")).startswith("scripts/lib/")
            and row.get("execution_contexts")
        ]
        self.assertEqual([], offenders)

    def test_every_non_standalone_path_lives_under_scripts_lib(self) -> None:
        """The derivation replacing the constant must be exhaustive.

        Four rows of the earlier move set were wrong in both directions. This
        asserts the property that made the constant deletable, rather than
        trusting that the move covered it.
        """

        offenders = [
            row["path"]
            for row in _manifest_rows()
            if row.get("kind") in {"validator", "library"}
            and row.get("execution_contexts") == []
            and not str(row.get("path", "")).startswith("scripts/lib/")
        ]
        self.assertEqual([], offenders)

    def test_the_non_standalone_list_is_gone(self) -> None:
        from scripts.lib.document_governance import suite_registry

        self.assertFalse(hasattr(suite_registry, "NON_STANDALONE_VALIDATOR_PATHS"))
