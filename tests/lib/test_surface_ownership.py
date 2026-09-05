from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.gate import ci_gate_adapters
from scripts.lib.gate import ci_gate_contract as gate_contract
from scripts.validation import ci_gate_runner as gate_runner

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _missing_test_domains(root: pathlib.Path, tracked: set[str]) -> list[str]:
    paths = {pathlib.PurePosixPath(path) for path in tracked if path}
    packages = {
        path.parts[2]
        for path in paths
        if path.parts[:2] == ("scripts", "lib") and len(path.parts) >= 4
    }
    tested = {
        path.parts[2]
        for path in paths
        if path.parts[:2] == ("tests", "lib")
        and len(path.parts) >= 4
        and path.name.startswith("test_")
        and path.suffix == ".py"
        and not any(
            root.joinpath(*path.parts[:index]).is_symlink()
            for index in range(1, len(path.parts) + 1)
        )
        and (root / path).is_file()
    }
    return sorted(packages - tested)


def _manifest_rows() -> list[dict]:
    payload = yaml.safe_load(
        (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
    )
    rows = payload["files"]
    if not isinstance(rows, list) or not rows:
        raise AssertionError("scripts/manifest.yaml must carry a non-empty files list")
    return [row for row in rows if isinstance(row, dict)]


def _full_profile_unittest_modules() -> list[str]:
    document = gate_contract.load_contract_document(ROOT)
    registry = gate_contract.parse_gate_registry(
        document, ".github/workflow-contract.yml"
    )
    public_gate = gate_contract.parse_public_gate_contract(document)
    selected = gate_contract.select_public_suites(public_gate, "full", ())
    plan = gate_runner.build_public_validation_plan(
        registry,
        gate_contract.public_root_gate_ids(public_gate, selected),
        public_gate,
        selected,
        gate_runner.ExecutionContext.LOCAL,
        profile="full",
    )
    return [
        module
        for invocation in plan
        if invocation.entrypoint == gate_runner._INTERNAL_ADAPTER_PATH
        and invocation.argv[:1] == ("run-unittest",)
        and invocation.argv[-1:] == ("-v",)
        for module in invocation.argv[1:-1]
    ]


class SurfaceOwnershipTests(unittest.TestCase):
    """A directory states what its files are, and no constant restates it."""

    def test_every_library_package_has_a_tracked_test(self) -> None:
        tracked = set(
            subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT, timeout=10)
            .decode()
            .split("\0")
        )
        self.assertEqual([], _missing_test_domains(ROOT, tracked))

    def test_library_mirror_requires_a_tracked_behavior_test(self) -> None:
        for shape in (
            "empty",
            "cache",
            "placeholder",
            "untracked",
            "symlink",
            "tracked",
        ):
            with self.subTest(shape=shape), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                (root / "scripts/lib/sample").mkdir(parents=True)
                mirror = root / "tests/lib/sample"
                mirror.mkdir(parents=True)
                tracked = {"scripts/lib/sample/module.py"}
                if shape == "cache":
                    (mirror / "__pycache__").mkdir()
                elif shape == "placeholder":
                    (mirror / ".gitkeep").touch()
                    tracked.add("tests/lib/sample/.gitkeep")
                elif shape in {"untracked", "tracked"}:
                    (mirror / "test_module.py").write_text(
                        "def test_behavior():\n    assert True\n", encoding="utf-8"
                    )
                    if shape == "tracked":
                        tracked.add("tests/lib/sample/test_module.py")
                elif shape == "symlink":
                    target = root / "test_outside.py"
                    target.write_text("def test_behavior():\n    assert True\n")
                    (mirror / "test_module.py").symlink_to(target)
                    tracked.add("tests/lib/sample/test_module.py")
                expected = [] if shape == "tracked" else ["sample"]
                self.assertEqual(expected, _missing_test_domains(root, tracked))

    def test_no_placeholder_test_directory_remains(self) -> None:
        for name in ("docs", "qa", "setup"):
            self.assertFalse(
                (ROOT / "tests" / name).exists(),
                f"tests/{name} described a structure that was never built",
            )

    def test_manifest_rows_declare_no_executable_composition(self) -> None:
        forbidden = {"public_suites", "execution_argv", "execution_contexts"}
        offenders = [
            row["path"] for row in _manifest_rows() if forbidden.intersection(row)
        ]
        self.assertEqual([], offenders)

    def test_retired_manifest_suite_registry_is_gone(self) -> None:
        self.assertFalse(
            (ROOT / "scripts/lib/document_governance/suite_registry.py").exists()
        )

    def test_every_test_module_is_reachable_from_the_full_profile(self) -> None:
        on_disk = {
            str(path.relative_to(ROOT).with_suffix("")).replace("/", ".")
            for path in (ROOT / "tests").rglob("test_*.py")
        }
        planned = _full_profile_unittest_modules()
        self.assertEqual(on_disk, set(planned))
        # Exactly once. The adapter grammar admits any well-shaped module, so
        # this is the only thing stopping the full profile from running one
        # module twice while another is silently dropped.
        duplicates = sorted(
            module for module in set(planned) if planned.count(module) > 1
        )
        self.assertEqual([], duplicates)

    def test_document_contract_tests_do_not_read_fixed_workspace_history(self) -> None:
        """Current contracts never depend on a deleted taxonomy or pinned clone history."""

        contract_tests = (
            *sorted((ROOT / "tests/lib/document_governance/metadata").glob("*.py")),
            *sorted((ROOT / "tests/validation/lifecycle").glob("*.py")),
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
        # The grammar admits any well-shaped module, so admission alone cannot
        # register a test. Only the workflow contract route puts it in the plan.
        self.assertTrue(
            ci_gate_adapters.admits_adapter_invocation(argv, "local"),
            "the grammar admits this shape",
        )
        self.assertNotIn(module, _full_profile_unittest_modules())
