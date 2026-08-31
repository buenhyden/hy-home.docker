from __future__ import annotations

import pathlib
import unittest
from unittest import mock

import yaml

from scripts.lib.gate import ci_gate_contract as gate_contract
from scripts.validation import ci_gate_runner as gate_runner

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _manifest_rows() -> list[dict]:
    payload = yaml.safe_load(
        (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
    )
    rows = payload["files"]
    if not isinstance(rows, list) or not rows:
        raise AssertionError("scripts/manifest.yaml must carry a non-empty files list")
    return [row for row in rows if isinstance(row, dict)]


def _full_profile_unittest_modules() -> set[str]:
    document = gate_contract.load_contract_document(ROOT)
    registry = gate_contract.parse_gate_registry(
        document, ".github/workflow-contract.yml"
    )
    suites = gate_contract.load_public_suite_registry(ROOT / "scripts/manifest.yaml")
    public_gate = gate_contract.parse_public_gate_contract(document, suites)
    selected = gate_contract.select_public_suites(public_gate, "full", ())
    plan = gate_runner.build_public_validation_plan(
        registry,
        gate_contract.public_root_gate_ids(public_gate, selected),
        suites,
        selected,
        gate_runner.ExecutionContext.LOCAL,
        profile="full",
    )
    return {
        module
        for invocation in plan
        if invocation.entrypoint == gate_runner._INTERNAL_ADAPTER_PATH
        and invocation.argv[:1] == ("run-unittest",)
        and invocation.argv[-1:] == ("-v",)
        for module in invocation.argv[1:-1]
    }


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

    def test_every_test_module_is_reachable_from_the_full_profile(self) -> None:
        on_disk = {
            str(path.relative_to(ROOT).with_suffix("")).replace("/", ".")
            for path in (ROOT / "tests").rglob("test_*.py")
        }
        self.assertEqual(on_disk, _full_profile_unittest_modules())

    def test_document_contract_tests_do_not_read_fixed_workspace_history(self) -> None:
        """Current contracts never depend on a deleted taxonomy or pinned clone history."""

        contract_tests = (
            ROOT / "tests/validation/test_document_metadata.py",
            ROOT / "tests/validation/test_document_corpus_lifecycle.py",
            ROOT / "tests/lib/target_surface/test_target_surface_contracts.py",
            ROOT / "tests/lib/document_governance/test_spec_packages.py",
        )
        forbidden = (
            "HISTORICAL_COMMIT",
            "LEGACY_CONTRACT_FIXTURE_COMMIT",
            "docs/99.templates/support/",
        )
        offenders = [
            f"{path.relative_to(ROOT)}: {token}"
            for path in contract_tests
            for token in forbidden
            if token in path.read_text(encoding="utf-8")
        ]
        self.assertEqual([], offenders)

    def test_adapter_admission_alone_is_not_test_registration(self) -> None:
        module = "tests.lib.unreachable.test_admission_only"
        argv = ("run-unittest", module, "-v")
        with mock.patch.dict(
            gate_runner._INTERNAL_ADAPTER_CONTEXTS,
            {argv: gate_runner._ALL_EXECUTION_CONTEXTS},
        ):
            self.assertNotIn(module, _full_profile_unittest_modules())
