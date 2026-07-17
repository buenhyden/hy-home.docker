from __future__ import annotations

import contextlib
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
RECOMMENDER = ROOT / "scripts/validation/recommend-qa-gates.sh"
PRE_COMMIT = ROOT / ".pre-commit-config.yaml"
WORKFLOW = ROOT / ".github/workflows/ci-quality.yml"
CODEOWNERS = ROOT / ".github/CODEOWNERS"
LABELER = ROOT / ".github/labeler.yml"
PR_TEMPLATE = ROOT / ".github/PULL_REQUEST_TEMPLATE.md"
HARNESS_WRAPPER = ROOT / "scripts/validation/validate-harness.sh"
LOCAL_QA = ROOT / "scripts/validation/run-local-qa-gates.sh"
REPO_CONTRACT = ROOT / "scripts/validation/check-repo-contracts.sh"

COUPLED_PATHS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".agents/agents/code-reviewer.md",
    ".claude/agents/code-reviewer.md",
    ".codex/agents/code-reviewer.toml",
    ".gemini/agents/code-reviewer.md",
    "docs/00.agent-governance/rules/agentic.md",
    "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml",
    "docs/00.agent-governance/contracts/agent-catalog.yaml",
    "docs/00.agent-governance/contracts/provider-models.yaml",
    "scripts/operations/provider_surface_renderer.py",
    "scripts/validation/agent_governance_contract.py",
    "scripts/validation/agent_output_eval.py",
    "scripts/validation/check-agent-governance-contract.py",
    "scripts/validation/check-repo-contracts.sh",
    "scripts/validation/run-agent-output-eval-fixtures.sh",
    "scripts/validation/run-agent-precommit-all-files.sh",
    "scripts/validation/run-local-qa-gates.sh",
    "scripts/validation/validate-harness.sh",
    "tests/validation/test_agent_governance_contract.py",
    "tests/validation/test_agent_governance_ci_routing.py",
    "tests/validation/test_agent_output_eval_fixtures.py",
    "tests/validation/test_provider_native_surfaces.py",
    "tests/validation/test_provider_surface_renderer.py",
)


class AgentGovernanceRoutingTests(unittest.TestCase):
    def test_recommender_selects_coupled_contract_and_eval_gates(self) -> None:
        for path in COUPLED_PATHS:
            with self.subTest(path=path):
                result = subprocess.run(
                    ["bash", str(RECOMMENDER), "--files", path],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(
                    "bash scripts/validation/check-repo-contracts.sh",
                    result.stdout,
                )
                self.assertIn(
                    "bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
                    result.stdout,
                )

    def test_pre_push_repo_contract_selector_covers_every_coupled_path(self) -> None:
        data = yaml.safe_load(PRE_COMMIT.read_text(encoding="utf-8"))
        hooks = [
            hook
            for repo in data["repos"]
            if repo["repo"] == "local"
            for hook in repo["hooks"]
            if hook["id"] == "check-repo-contracts"
        ]
        self.assertEqual(1, len(hooks))
        selector = re.compile(hooks[0]["files"])
        for path in COUPLED_PATHS:
            with self.subTest(path=path):
                self.assertIsNotNone(selector.fullmatch(path))

    def test_existing_ci_jobs_run_full_contract_and_semantic_eval_markers(self) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        jobs = workflow["jobs"]

        repo_steps = jobs["repo-contracts"]["steps"]
        repo_commands = "\n".join(
            str(step.get("run", "")) for step in repo_steps if isinstance(step, dict)
        )
        self.assertIn(
            "check-agent-governance-contract.py --mode repository --section all",
            repo_commands,
        )

        eval_steps = jobs["agent-output-eval-fixture-gate"]["steps"]
        eval_commands = "\n".join(
            str(step.get("run", "")) for step in eval_steps if isinstance(step, dict)
        )
        self.assertIn(
            "run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
            eval_commands,
        )
        self.assertIn("fixtures_check=pass", eval_commands)
        self.assertIn("regressions_check=pass", eval_commands)
        for module in (
            "tests.validation.test_agent_governance_ci_routing",
            "tests.validation.test_agent_output_eval_fixtures",
        ):
            with self.subTest(ci_module=module):
                self.assertIn(module, repo_commands + eval_commands)
        self.assertEqual({"contents": "read"}, jobs["repo-contracts"]["permissions"])
        self.assertEqual(
            {"contents": "read"},
            jobs["agent-output-eval-fixture-gate"]["permissions"],
        )

    def test_github_review_surfaces_cover_semantic_harness_evidence(self) -> None:
        owners = CODEOWNERS.read_text(encoding="utf-8")
        for path in (
            "scripts/validation/agent_output_eval.py",
            "scripts/validation/run-agent-output-eval-fixtures.sh",
            "scripts/validation/report-provider-hook-parity.sh",
            "tests/validation/test_agent_governance_ci_routing.py",
            "tests/validation/test_agent_output_eval_fixtures.py",
        ):
            with self.subTest(owner=path):
                self.assertIn(path, owners)

        labeler = LABELER.read_text(encoding="utf-8")
        for provider_path in (
            ".agents/**/*",
            ".claude/**/*",
            ".codex/**/*",
            ".gemini/**/*",
        ):
            with self.subTest(labeler=provider_path):
                self.assertIn(provider_path, labeler)

        template = PR_TEMPLATE.read_text(encoding="utf-8")
        for evidence in (
            "--mode repository --section all",
            "run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
            "fixtures_check=pass",
            "regressions_check=pass",
            "command, result, rollback, and skipped-check fields",
        ):
            with self.subTest(evidence=evidence):
                self.assertIn(evidence, template)

        harness = HARNESS_WRAPPER.read_text(encoding="utf-8")
        self.assertIn("run-local-qa-gates.sh --harness", harness)

    def test_local_qa_routes_all_files_through_controlled_wrapper(self) -> None:
        result = subprocess.run(
            ["bash", str(LOCAL_QA), "--list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        for fragment in (
            "scripts/validation/run-agent-precommit-all-files.sh",
            "initially clean linked worktree",
            "tracked Task evidence",
            "--allow-prefix",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, result.stdout)
        self.assertNotIn("locally use pre-commit", result.stdout)
        self.assertNotIn("pre-commit run --all-files", result.stdout)

    def test_semantic_local_qa_bypass_guard_is_selector_coupled(self) -> None:
        for path in (
            "scripts/validation/run-local-qa-gates.sh",
            "scripts/validation/agent_governance_contract.py",
            "scripts/validation/check-repo-contracts.sh",
            "tests/validation/test_agent_governance_contract.py",
            "tests/validation/test_agent_governance_ci_routing.py",
        ):
            with self.subTest(path=path):
                self.assertIn(path, COUPLED_PATHS)

    def test_aggregate_delegates_local_qa_semantics_to_typed_authority(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "required_surface_fragments = {"
        end = "\n}\n\nforbidden_ambiguous_fragments"
        aggregate_fragments = source.split(start, 1)[1].split(end, 1)[0]
        self.assertNotIn(
            'pathlib.Path("scripts/validation/run-local-qa-gates.sh")',
            aggregate_fragments,
        )
        self.assertIn("--mode repository --section all", source)

    def test_script_reference_scan_ignores_only_python_cache_artifacts(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]

        with self.subTest("cache-is-ignored"), self._script_reference_fixture() as root:
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)

        with (
            self.subTest("source-is-still-checked"),
            self._script_reference_fixture() as root,
        ):
            docs = root / "docs"
            docs.mkdir()
            (docs / "active.md").write_text(
                "Run scripts/validation/missing-active.sh\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("missing-active.sh", result.stderr)

        with (
            self.subTest("doc-under-cache-name-is-checked"),
            self._script_reference_fixture() as root,
        ):
            docs = root / "docs/__pycache__"
            docs.mkdir(parents=True)
            (docs / "active.md").write_text(
                "Run scripts/validation/missing-active-cache-name.sh\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "add", "-f", "docs/__pycache__/active.md"],
                cwd=root,
                check=True,
            )
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("missing-active-cache-name.sh", result.stderr)

        with (
            self.subTest("tracked-pyc-is-checked"),
            self._script_reference_fixture(track_cache=True) as root,
        ):
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("missing-cache.sh", result.stderr)

    def test_script_reference_scan_rejects_unsafe_files_without_dereference(
        self,
    ) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]

        with self.subTest("external-symlink"), self._script_reference_fixture() as root:
            docs = root / "docs"
            docs.mkdir()
            sentinel = root / "external-sentinel.md"
            sentinel.write_text(
                "Run scripts/validation/missing-external-sentinel.sh\n",
                encoding="utf-8",
            )
            (docs / "linked.md").symlink_to(sentinel)
            subprocess.run(["git", "add", "docs/linked.md"], cwd=root, check=True)
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            rendered = result.stdout + result.stderr
            self.assertIn("unsafe script-reference surface", rendered)
            self.assertNotIn("missing-external-sentinel.sh", rendered)

        with self.subTest("broken-symlink"), self._script_reference_fixture() as root:
            docs = root / "docs"
            docs.mkdir()
            (docs / "broken.md").symlink_to(root / "missing-sentinel.md")
            subprocess.run(["git", "add", "docs/broken.md"], cwd=root, check=True)
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            rendered = result.stdout + result.stderr
            self.assertIn("unsafe script-reference surface", rendered)
            self.assertNotIn("missing-sentinel.md", rendered)

        with self.subTest("fifo"), self._script_reference_fixture() as root:
            docs = root / "docs"
            docs.mkdir()
            os.mkfifo(docs / "pipe.md")
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("unsafe script-reference surface", result.stderr)

    def test_script_reference_scan_enforces_exact_resource_ceilings(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]
        expected_constants = (
            "MAX_REFERENCE_SURFACES: Final = 4_096",
            "MAX_REFERENCE_FILE_BYTES: Final = 16 * 1_048_576",
            "MAX_REFERENCE_TOTAL_BYTES: Final = 64 * 1_048_576",
            "MAX_REFERENCE_DISCOVERY_ENTRIES: Final = 8_192",
            "MAX_REFERENCE_GIT_OUTPUT_BYTES: Final = 1_048_576",
            "MAX_REFERENCE_PATH_BYTES: Final = 4_096",
        )
        for constant in expected_constants:
            with self.subTest(constant=constant):
                self.assertIn(constant, block)
        existence_check = block.split("def confined_regular_exists", 1)[1].split(
            "\n\nfor path in files:", 1
        )[0]
        self.assertIn("open_confined_regular(path)", existence_check)
        self.assertNotIn("read_confined_regular(path)", existence_check)
        for boundary_fragment in (
            "initial = os.lstat(path)",
            "opened = os.fstat(file_descriptor)",
            "aggregate_remaining = MAX_REFERENCE_TOTAL_BYTES - total_reference_bytes",
            "read_limit = min(MAX_REFERENCE_FILE_BYTES, aggregate_remaining)",
            "opened.st_size > read_limit",
            "remaining = read_limit + 1",
            "metadata.st_ctime_ns",
            "metadata_tuple(opened) != metadata_tuple(initial)",
            "metadata_tuple(final) != metadata_tuple(opened)",
        ):
            with self.subTest(boundary_fragment=boundary_fragment):
                self.assertIn(boundary_fragment, block)

        cases = (
            ("surface-below", 3, 8, 16, 16, 2, (b"a", b"b"), 0),
            ("surface-at", 2, 8, 16, 16, 2, (b"a", b"b"), 0),
            ("surface-above", 1, 8, 16, 16, 2, (b"a", b"b"), 1),
            ("file-below", 2, 5, 16, 16, 2, (b"abcd",), 0),
            ("file-at", 2, 4, 16, 16, 2, (b"abcd",), 0),
            ("file-above", 2, 3, 16, 16, 2, (b"abcd",), 1),
            ("total-below", 2, 8, 9, 16, 2, (b"abcd", b"efgh"), 0),
            ("total-at", 2, 8, 8, 16, 2, (b"abcd", b"efgh"), 0),
            ("total-above", 2, 8, 7, 16, 2, (b"abcd", b"efgh"), 1),
            ("discovery-below", 2, 8, 16, 3, 2, (b"a",), 0),
            ("discovery-at", 2, 8, 16, 2, 2, (b"a",), 0),
            ("discovery-above", 2, 8, 16, 1, 2, (b"a",), 1),
        )
        for (
            label,
            surface_limit,
            file_limit,
            total_limit,
            discovery_limit,
            discovery_entries,
            payloads,
            expected,
        ) in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                subprocess.run(["git", "init", "-q"], cwd=root, check=True)
                docs = root / "docs"
                docs.mkdir()
                for index, payload in enumerate(payloads):
                    (docs / f"surface-{index}.md").write_bytes(payload)
                while len(list(docs.iterdir())) < discovery_entries - 1:
                    index = len(list(docs.iterdir()))
                    (docs / f"discovery-{index}.md").write_bytes(b"")
                mutated = (
                    block.replace(
                        "MAX_REFERENCE_SURFACES: Final = 4_096",
                        f"MAX_REFERENCE_SURFACES: Final = {surface_limit}",
                    )
                    .replace(
                        "MAX_REFERENCE_FILE_BYTES: Final = 16 * 1_048_576",
                        f"MAX_REFERENCE_FILE_BYTES: Final = {file_limit}",
                    )
                    .replace(
                        "MAX_REFERENCE_TOTAL_BYTES: Final = 64 * 1_048_576",
                        f"MAX_REFERENCE_TOTAL_BYTES: Final = {total_limit}",
                    )
                    .replace(
                        "MAX_REFERENCE_DISCOVERY_ENTRIES: Final = 8_192",
                        f"MAX_REFERENCE_DISCOVERY_ENTRIES: Final = {discovery_limit}",
                    )
                )
                result = subprocess.run(
                    [sys.executable, "-c", mutated],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(expected, result.returncode, result.stderr)
                if expected:
                    self.assertIn("unsafe script-reference surface", result.stderr)

    def test_script_reference_discovery_is_bounded_before_allocation(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))", 1
        )[0]
        git_reader = block.split("def git_paths", 1)[1].split("\n\ntracked =", 1)[0]
        discovery = block.split("def untracked_special_paths", 1)[1].split(
            "\n\nspecial_paths =", 1
        )[0]
        for fragment in (
            "subprocess.Popen(",
            "MAX_REFERENCE_GIT_OUTPUT_BYTES - output_bytes + 1",
            "MAX_REFERENCE_PATH_BYTES",
            "len(paths) > MAX_REFERENCE_SURFACES",
            "process.kill()",
            "process.wait()",
        ):
            with self.subTest(scope="git", fragment=fragment):
                self.assertIn(fragment, git_reader)
        self.assertNotIn("capture_output=True", git_reader)
        self.assertNotIn('.split(b"\\0")', git_reader)
        for fragment in (
            "os.scandir(path)",
            "discovery_count += 1",
            "discovery_count > MAX_REFERENCE_DISCOVERY_ENTRIES",
            "tracked_prefixes: set[pathlib.Path] = set()",
            "if len(tracked_prefixes) >= MAX_REFERENCE_DISCOVERY_ENTRIES",
            "tracked_prefixes.add(parent)",
        ):
            with self.subTest(scope="filesystem", fragment=fragment):
                self.assertIn(fragment, discovery)
        self.assertNotIn("os.listdir", discovery)
        self.assertNotIn("sorted(", discovery)
        self.assertNotIn("tracked_prefixes = {", discovery)

    def test_script_reference_scan_rejects_same_inode_metadata_mutation(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]
        mutations = (
            (
                "lstat-to-open",
                "        initial = os.lstat(path)",
                "        initial = os.lstat(path)\n        os.chmod(path, 0o600)",
            ),
            (
                "open-to-final",
                "        final = os.fstat(file_descriptor)",
                "        os.chmod(path, 0o600)\n        final = os.fstat(file_descriptor)",
            ),
        )
        for label, mutation_point, replacement in mutations:
            with self.subTest(label=label):
                self.assertIn(mutation_point, block)
                mutated = block.replace(mutation_point, replacement, 1)
                with self._script_reference_fixture() as root:
                    docs = root / "docs"
                    docs.mkdir()
                    (docs / "active.md").write_text(
                        "ordinary prose\n", encoding="utf-8"
                    )
                    result = subprocess.run(
                        [sys.executable, "-c", mutated],
                        cwd=root,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                self.assertEqual(1, result.returncode)
                self.assertIn("unsafe script-reference surface", result.stderr)
                self.assertNotIn("active.md", result.stderr)

    def test_script_reference_scan_enforces_literal_ceiling_boundaries(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]

        def run(
            root: pathlib.Path, program: str = block
        ) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )

        with (
            self.subTest("surfaces-4096-and-4097"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            for index in range(4_096):
                (docs / f"surface-{index:04d}.md").touch()
            self.assertEqual(0, run(root).returncode)
            (docs / "surface-over.md").touch()
            above = run(root)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with (
            self.subTest("discovery-8192-and-8193"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            for index in range(8_191):
                (docs / f"entry-{index:04d}").mkdir()
            ignore_start = block.index("def is_ignored(path: pathlib.Path) -> bool:")
            ignore_end = block.index("\n\n\ndef untracked_special_paths", ignore_start)
            fast_discovery = (
                block[:ignore_start]
                + "def is_ignored(path: pathlib.Path) -> bool:\n    return False"
                + block[ignore_end:]
            )
            self.assertEqual(0, run(root, fast_discovery).returncode)
            (docs / "entry-over").mkdir()
            above = run(root, fast_discovery)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with (
            self.subTest("file-16mib-and-n-plus-one"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            surface = docs / "surface.md"
            surface.write_bytes(b"\0" * (16 * 1_048_576))
            self.assertEqual(0, run(root).returncode)
            with surface.open("ab") as stream:
                stream.write(b"\0")
            above = run(root)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with (
            self.subTest("aggregate-64mib-and-n-plus-one"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            for index in range(4):
                (docs / f"surface-{index}.md").write_bytes(b"\0" * (16 * 1_048_576))
            self.assertEqual(0, run(root).returncode)
            (docs / "surface-4.md").write_bytes(b"\0")
            above = run(root)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

    def test_typed_harness_replacement_covers_removed_aggregate_routes(self) -> None:
        contract_text = (
            ROOT / "scripts/validation/agent_governance_contract.py"
        ).read_text(encoding="utf-8")
        for relative, fragment in (
            (".github/PULL_REQUEST_TEMPLATE.md", "validate-harness.sh"),
            ("scripts/README.md", "validate-harness.sh"),
            ("scripts/README.md", "run-local-qa-gates.sh --harness"),
            ("docs/00.agent-governance/README.md", "harness-implementation-map.md"),
        ):
            with self.subTest(relative=relative, fragment=fragment):
                self.assertIn(relative, contract_text)
                self.assertIn(fragment, contract_text)
        self.assertNotRegex(
            (ROOT / "scripts/validation/check-repo-contracts.sh").read_text(
                encoding="utf-8"
            ),
            r"grep .*validate-harness",
        )

    @staticmethod
    @contextlib.contextmanager
    def _script_reference_fixture(*, track_cache: bool = False):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            cache = root / "scripts/validation/__pycache__"
            cache.mkdir(parents=True)
            cache_file = cache / "module.cpython-312.pyc"
            cache_file.write_bytes(b"scripts/validation/missing-cache.sh")
            if track_cache:
                subprocess.run(
                    [
                        "git",
                        "add",
                        "-f",
                        "scripts/validation/__pycache__/module.cpython-312.pyc",
                    ],
                    cwd=root,
                    check=True,
                )
            yield root


if __name__ == "__main__":
    unittest.main()
