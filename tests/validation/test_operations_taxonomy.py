from __future__ import annotations

import os
import pathlib
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance.operations_catalog import (
    MIGRATION_PATH,
    SEMANTIC_WITNESS_PATH,
    TASK8_ROW_IDS,
    GitCommandResult,
    OperationsAuthorityError,
    _markdown_body_text,
    _validate_semantic_witnesses,
    extract_task8_consumers,
    load_task8_migration,
    validate_active_operations_references,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def _repo_contract_python_section(name: str) -> str:
    source = (ROOT / "scripts/validation/check-repo-contracts.sh").read_text(
        encoding="utf-8"
    )
    section = source.split(f'section "{name}"', 1)[1]
    return section.split("if ! python3 - <<'PY'; then\n", 1)[1].split(
        "\nPY\n", 1
    )[0]


def _run_repo_contract_python_section(
    name: str,
    root: pathlib.Path,
    *,
    source: str | None = None,
    environment: dict[str, str] | None = None,
    timeout: float = 10.0,
) -> subprocess.CompletedProcess[str]:
    process_environment = os.environ.copy()
    python_path = process_environment.get("PYTHONPATH")
    process_environment["PYTHONPATH"] = (
        str(ROOT) if not python_path else f"{ROOT}{os.pathsep}{python_path}"
    )
    if environment is not None:
        process_environment.update(environment)
    return subprocess.run(
        [sys.executable, "-c", source or _repo_contract_python_section(name)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
        env=process_environment,
        timeout=timeout,
    )


def _initialize_fixture_repository(root: pathlib.Path, *paths: str) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    if paths:
        subprocess.run(["git", "add", *paths], cwd=root, check=True)


def _write_service_fixture(root: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]:
    service = root / "infra/01-gateway/traefik"
    service.mkdir(parents=True)
    (service / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
    guide = root / "docs/05.operations/catalog/01-gateway/0013-traefik/guide.md"
    guide.parent.mkdir(parents=True)
    guide.write_text("# Guide\n", encoding="utf-8")
    readme = service / "README.md"
    readme.write_text(
        "[Guide](../../../docs/05.operations/catalog/01-gateway/"
        "0013-traefik/guide.md)\n",
        encoding="utf-8",
    )
    _initialize_fixture_repository(root, "infra", "docs")
    return service, readme


class OperationsAuthorityTests(unittest.TestCase):
    def test_operations_checker_is_executable_and_publishes_required_mode_usage(self) -> None:
        checker = ROOT / "scripts/validation/check-operations-catalog.py"
        self.assertTrue(checker.stat().st_mode & stat.S_IXUSR)
        result = subprocess.run(
            [str(checker), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("--mode", result.stdout)
        self.assertIn("complete", result.stdout)

    def test_active_corpus_has_no_generic_predecessor_or_release_role_routes(self) -> None:
        self.assertEqual((), validate_active_operations_references(ROOT))

    def test_active_reference_scan_has_explicit_history_and_negative_exclusions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            fixtures = {
                "docs/00.agent-governance/active.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-subject/guide.md.\n"
                ),
                "docs/90.references/history.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-historical/guide.md.\n"
                ),
                "docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-evidence/guide.md.\n"
                ),
                "docs/03.specs/0153-workspace-governance-simplification/plan.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-migration/guide.md.\n"
                ),
                "docs/03.specs/0999-new-active-spec/spec.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-active-spec/guide.md.\n"
                ),
                "tests/fixtures/negative.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-negative/guide.md.\n"
                ),
                "docs/00.agent-governance/negative.md": "No separate Release document role.\n",
            }
            for relative, content in fixtures.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            subprocess.run(["git", "add", *fixtures], cwd=root, check=True)
            findings = validate_active_operations_references(root)
            self.assertEqual(2, len(findings))
            self.assertEqual(
                {
                    "docs/00.agent-governance/active.md",
                    "docs/03.specs/0999-new-active-spec/spec.md",
                },
                {finding.path.split(":", 1)[0] for finding in findings},
            )

    def test_active_reference_scan_covers_scripts_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            fixtures = {
                "scripts/validation/active.sh": (
                    'guide="docs/05.operations/guides/00-workspace/example.md"\n'
                ),
                ".github/operations.yaml": (
                    "policy: docs/05.operations/policies/00-workspace/example.md\n"
                ),
                "tests/fixtures/negative.sh": (
                    'runbook="docs/05.operations/runbooks/00-workspace/example.md"\n'
                ),
                "docs/98.archive/migrations/history.toml": (
                    'route = "docs/05.operations/guides/00-workspace/example.md"\n'
                ),
                "docs/99.templates/support/document-corpus-migration-contract.yaml": (
                    "source: docs/05.operations/policies/00-workspace/example.md\n"
                ),
            }
            for relative, content in fixtures.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            subprocess.run(["git", "add", *fixtures], cwd=root, check=True)
            findings = validate_active_operations_references(root)
            self.assertEqual(
                {
                    ".github/operations.yaml",
                    "scripts/validation/active.sh",
                },
                {finding.path.split(":", 1)[0] for finding in findings},
            )

    def test_repo_contract_drift_guides_use_existing_current_catalog_paths(self) -> None:
        checker = ROOT / "scripts/validation/check-repo-contracts.sh"
        text = checker.read_text(encoding="utf-8")
        expected = (
            "docs/05.operations/catalog/00-workspace/"
            "0003-env-key-comparison/guide.md",
            "docs/05.operations/catalog/00-workspace/"
            "0010-sensitive-env-vars-comparison/guide.md",
        )
        self.assertIn(f'env_comparison_doc="{expected[0]}"', text)
        self.assertIn(f'sensitive_comparison_doc="{expected[1]}"', text)
        self.assertIn('-f "$env_comparison_doc"', text)
        self.assertIn('-f "$sensitive_comparison_doc"', text)
        for relative in expected:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_execution_evidence_status_section_has_its_regex_dependency(self) -> None:
        result = _run_repo_contract_python_section(
            "Execution evidence status wording", ROOT
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_service_documentation_gate_resolves_current_catalog_guide_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            service, readme = _write_service_fixture(root)
            result = _run_repo_contract_python_section(
                "Service documentation coverage", root
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

            legacy = root / "docs/05.operations/guides/01-gateway/traefik.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("# Retired guide\n", encoding="utf-8")
            readme.write_text(
                "[Guide](../../../docs/05.operations/guides/01-gateway/traefik.md)\n",
                encoding="utf-8",
            )
            result = _run_repo_contract_python_section(
                "Service documentation coverage", root
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)

            readme.write_text(
                "[Guide](../../../docs/05.operations/catalog/01-gateway/"
                "0999-missing/guide.md)\n",
                encoding="utf-8",
            )
            result = _run_repo_contract_python_section(
                "Service documentation coverage", root
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_service_documentation_gate_ignores_nonrendered_markdown_links(self) -> None:
        false_links = (
            "```markdown\n[Guide](../../../docs/05.operations/catalog/01-gateway/"
            "0013-traefik/guide.md)\n```\n",
            "<!-- [Guide](../../../docs/05.operations/catalog/01-gateway/"
            "0013-traefik/guide.md) -->\n",
            "`[Guide](../../../docs/05.operations/catalog/01-gateway/"
            "0013-traefik/guide.md)`\n",
            "![Guide](../../../docs/05.operations/catalog/01-gateway/"
            "0013-traefik/guide.md)\n",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            _service, readme = _write_service_fixture(root)
            for text in false_links:
                with self.subTest(text=text.splitlines()[0]):
                    readme.write_text(text, encoding="utf-8")
                    result = _run_repo_contract_python_section(
                        "Service documentation coverage", root
                    )
                    self.assertEqual(
                        1, result.returncode, result.stdout + result.stderr
                    )

    def test_service_documentation_gate_rejects_compose_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            service, _readme = _write_service_fixture(root)
            compose = service / "docker-compose.yml"
            compose.unlink()
            compose.symlink_to("docker-compose.real.yml")
            (service / "docker-compose.real.yml").write_text(
                "services: {}\n", encoding="utf-8"
            )
            result = _run_repo_contract_python_section(
                "Service documentation coverage", root
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_service_documentation_gate_accepts_git_byte_sorted_component_prefixes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            service, _readme = _write_service_fixture(root)
            (service / "config").mkdir()
            (service / "config/value.txt").write_text("value\n", encoding="utf-8")
            sibling = service.parent / "traefik-extra"
            sibling.mkdir()
            (sibling / "value.txt").write_text("value\n", encoding="utf-8")
            subprocess.run(["git", "add", "infra"], cwd=root, check=True)
            result = _run_repo_contract_python_section(
                "Service documentation coverage", root
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_service_documentation_gate_rejects_readme_fifo_without_hanging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            _service, readme = _write_service_fixture(root)
            readme.unlink()
            os.mkfifo(readme)
            result = _run_repo_contract_python_section(
                "Service documentation coverage", root, timeout=2.0
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_service_documentation_gate_enforces_count_file_and_aggregate_bounds(self) -> None:
        mutations = (
            (r"MAX_SERVICE_TRACKED_PATHS: Final = [^\n]+", "MAX_SERVICE_TRACKED_PATHS: Final = 1"),
            (r"MAX_SERVICE_FILE_BYTES: Final = [^\n]+", "MAX_SERVICE_FILE_BYTES: Final = 32"),
            (r"MAX_SERVICE_TOTAL_BYTES: Final = [^\n]+", "MAX_SERVICE_TOTAL_BYTES: Final = 64"),
        )
        for pattern, replacement in mutations:
            with self.subTest(bound=replacement), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                _service, readme = _write_service_fixture(root)
                readme.write_text(
                    "[Guide](../../../docs/05.operations/catalog/01-gateway/"
                    "0013-traefik/guide.md)\n" + "bounded payload\n" * 8,
                    encoding="utf-8",
                )
                section = re.sub(
                    pattern,
                    replacement,
                    _repo_contract_python_section("Service documentation coverage"),
                )
                result = _run_repo_contract_python_section(
                    "Service documentation coverage", root, source=section
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_spec_role_gate_resolves_existing_confined_regular_targets(self) -> None:
        cases = (
            ("regular", "../../05.operations/catalog/01-gateway/0013-traefik/guide.md", 0),
            ("angle-regular", "<../../05.operations/catalog/01-gateway/0013-traefik/guide.md>", 0),
            ("wrong-depth", "../05.operations/catalog/01-gateway/0013-traefik/guide.md", 1),
            ("nonexistent", "../../05.operations/catalog/01-gateway/0999-missing/guide.md", 1),
            ("angle-nonexistent", "<../../05.operations/catalog/01-gateway/0999-missing/guide.md>", 1),
            ("symlink", "../../05.operations/catalog/01-gateway/0013-traefik/guide.md", 1),
            ("nonregular", "../../05.operations/catalog/01-gateway/0013-traefik/guide.md", 1),
        )
        for mutation, href, expected in cases:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                spec = root / "docs/03.specs/0001-example/spec.md"
                spec.parent.mkdir(parents=True)
                spec.write_text(
                    f"- **Guide**: [Guide]({href})\n", encoding="utf-8"
                )
                guide = root / "docs/05.operations/catalog/01-gateway/0013-traefik/guide.md"
                guide.parent.mkdir(parents=True)
                if mutation == "symlink":
                    real = root / "real-guide.md"
                    real.write_text("# Guide\n", encoding="utf-8")
                    guide.symlink_to(real)
                elif mutation == "nonregular":
                    guide.mkdir()
                else:
                    guide.write_text("# Guide\n", encoding="utf-8")
                result = _run_repo_contract_python_section(
                    "Spec document traceability contract", root
                )
                self.assertEqual(expected, result.returncode, result.stdout + result.stderr)

    def test_spec_role_gate_does_not_treat_operations_index_label_as_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            spec = root / "docs/03.specs/README.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "[Operations](../05.operations/README.md)\n", encoding="utf-8"
            )
            operations = root / "docs/05.operations/README.md"
            operations.parent.mkdir(parents=True)
            operations.write_text("# Operations\n", encoding="utf-8")
            result = _run_repo_contract_python_section(
                "Spec document traceability contract", root
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_incident_contract_uses_only_exact_packet_role_paths(self) -> None:
        surfaces = (
            ROOT / "docs/05.operations/incidents/README.md",
            ROOT / "docs/00.agent-governance/policies/documentation-protocol.md",
        )
        exact_paths = (
            "docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md",
            "docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md",
        )
        for surface in surfaces:
            text = surface.read_text(encoding="utf-8")
            with self.subTest(surface=surface):
                self.assertNotIn("incident-title", text)
                for exact_path in exact_paths:
                    self.assertIn(exact_path, text)

        gate = _repo_contract_python_section("Operations postmortem routing contract")
        self.assertNotIn('"YYYY/inc-####-incident-title/"', gate)
        for exact_path in exact_paths:
            self.assertGreaterEqual(gate.count(exact_path), 2)

    def test_selected_spec_role_links_use_exact_current_role_leaves(self) -> None:
        expected = {
            "docs/03.specs/0001-gateway/spec.md": {
                "Guide": "../../05.operations/catalog/01-gateway/0012-edge-routing-stack/guide.md",
                "Policy": "../../05.operations/catalog/01-gateway/0013-traefik/policy.md",
                "Runbook": "../../05.operations/catalog/01-gateway/0013-traefik/runbook.md",
            },
            "docs/03.specs/0002-auth/spec.md": {
                role: f"../../05.operations/catalog/02-auth/0014-keycloak/{role.lower()}.md"
                for role in ("Guide", "Policy", "Runbook")
            },
            "docs/03.specs/0005-data-analytics/spec.md": {
                role: f"../../05.operations/catalog/04-data/0017-influxdb/{role.lower()}.md"
                for role in ("Guide", "Policy", "Runbook")
            },
            "docs/03.specs/0095-infra-secrets-docs-refresh/spec.md": {
                role: f"../../05.operations/catalog/03-security/0016-vault/{role.lower()}.md"
                for role in ("Guide", "Policy", "Runbook")
            },
        }
        for relative, roles in expected.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            for role, href in roles.items():
                with self.subTest(path=relative, role=role):
                    self.assertIn(f"- **{role}**: [{href}]({href})", text)

    def test_script_reference_gate_accepts_exact_tracked_worktree_deletions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            scripts = root / "scripts"
            docs.mkdir()
            scripts.mkdir()
            (docs / "keep.md").write_text("No script references.\n", encoding="utf-8")
            registered = docs / "05.operations/releases/README.md"
            registered.parent.mkdir(parents=True)
            registered.write_text("No script references.\n", encoding="utf-8")
            (scripts / "exists.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
            subprocess.run(["git", "add", "docs", "scripts"], cwd=root, check=True)
            registered.unlink()
            result = _run_repo_contract_python_section("Script reference integrity", root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

            unexpected = docs / "unexpected.md"
            unexpected.write_text("No script references.\n", encoding="utf-8")
            subprocess.run(["git", "add", "docs/unexpected.md"], cwd=root, check=True)
            unexpected.unlink()
            result = _run_repo_contract_python_section("Script reference integrity", root)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_script_reference_gate_rejects_symlink_nonregular_and_race(self) -> None:
        for mutation in ("broken-symlink", "nonregular", "race"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                subprocess.run(["git", "init", "-q"], cwd=root, check=True)
                docs = root / "docs"
                scripts = root / "scripts"
                docs.mkdir()
                scripts.mkdir()
                victim = docs / "victim.md"
                victim.write_text("No script references.\n", encoding="utf-8")
                (scripts / "exists.sh").write_text(
                    "#!/usr/bin/env bash\n", encoding="utf-8"
                )
                subprocess.run(["git", "add", "docs", "scripts"], cwd=root, check=True)

                section = _repo_contract_python_section("Script reference integrity")
                if mutation == "broken-symlink":
                    victim.unlink()
                    victim.symlink_to("missing.md")
                elif mutation == "nonregular":
                    victim.unlink()
                    os.mkfifo(victim)
                else:
                    section = section.replace(
                        "    initial = os.lstat(path)\n",
                        "    initial = os.lstat(path)\n"
                        "    if path == pathlib.Path('docs/victim.md'):\n"
                        "        os.replace(path, path.with_suffix('.saved'))\n"
                        "        path.write_text('replacement\\n', encoding='utf-8')\n",
                        1,
                    )

                result = subprocess.run(
                    [sys.executable, "-c", section],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_script_reference_git_enumeration_deadlines_and_reaps_partial_hang(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            _initialize_fixture_repository(root)
            fake_bin = root / "fake-bin"
            fake_bin.mkdir()
            fake_git = fake_bin / "git"
            fake_git.write_text(
                "#!/usr/bin/env python3\n"
                "import os\n"
                "import time\n"
                "child = os.fork()\n"
                "if child == 0:\n"
                "    open('git-child.pid', 'w', encoding='ascii').write(str(os.getpid()))\n"
                "    while True:\n"
                "        time.sleep(1)\n"
                "open('git-parent.pid', 'w', encoding='ascii').write(str(os.getpid()))\n"
                "os.write(1, b'docs/keep.md\\0')\n"
                "while True:\n"
                "    time.sleep(1)\n",
                encoding="utf-8",
            )
            fake_git.chmod(0o755)
            section = re.sub(
                r"MAX_REFERENCE_GIT_SECONDS: Final = [^\n]+",
                "MAX_REFERENCE_GIT_SECONDS: Final = 0.2",
                _repo_contract_python_section("Script reference integrity"),
            )
            environment = os.environ.copy()
            environment["PATH"] = f"{fake_bin}{os.pathsep}{environment['PATH']}"
            python_path = environment.get("PYTHONPATH")
            environment["PYTHONPATH"] = (
                str(ROOT) if not python_path else f"{ROOT}{os.pathsep}{python_path}"
            )
            process = subprocess.Popen(
                [sys.executable, "-c", section],
                cwd=root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
                start_new_session=True,
            )
            started = time.monotonic()
            try:
                stdout, stderr = process.communicate(timeout=1.5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
                self.fail("script-reference Git read exceeded its deadline after partial output")
            self.assertLess(time.monotonic() - started, 1.0)
            self.assertEqual(1, process.returncode, stdout + stderr)
            child_pid = int((root / "git-child.pid").read_text(encoding="ascii"))
            child_state = pathlib.Path(f"/proc/{child_pid}/stat")
            deadline = time.monotonic() + 1.0
            while child_state.exists() and time.monotonic() < deadline:
                state = child_state.read_text(encoding="ascii").split()[2]
                if state == "Z":
                    break
                time.sleep(0.02)
            self.assertTrue(
                not child_state.exists()
                or child_state.read_text(encoding="ascii").split()[2] == "Z"
            )

    def test_script_reference_ignored_discovery_is_batched(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "docs/ignored").mkdir(parents=True)
            (root / "scripts").mkdir()
            (root / "docs/keep.md").write_text(
                "No script references.\n", encoding="utf-8"
            )
            (root / "scripts/exists.sh").write_text(
                "#!/usr/bin/env bash\n", encoding="utf-8"
            )
            (root / ".gitignore").write_text("docs/ignored/\n", encoding="utf-8")
            os.mkfifo(root / "docs/ignored/pipe")
            _initialize_fixture_repository(root, ".gitignore", "docs/keep.md", "scripts")
            log = root / "git-calls.log"
            real_git = shutil.which("git")
            self.assertIsNotNone(real_git)
            fake_bin = root / "fake-bin"
            fake_bin.mkdir()
            wrapper = fake_bin / "git"
            wrapper.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> {log.as_posix()}\n"
                f"exec {real_git} \"$@\"\n",
                encoding="utf-8",
            )
            wrapper.chmod(0o755)
            result = _run_repo_contract_python_section(
                "Script reference integrity",
                root,
                environment={"PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"},
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            calls = log.read_text(encoding="utf-8").splitlines()
            self.assertEqual([], [call for call in calls if "check-ignore" in call])
            self.assertEqual(
                1,
                sum("--ignored" in call and "--directory" in call for call in calls),
            )

    def test_script_reference_git_output_overflow_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            document = root / "docs/a-deliberately-long-tracked-path.md"
            document.parent.mkdir(parents=True)
            document.write_text("No script references.\n", encoding="utf-8")
            _initialize_fixture_repository(root, "docs")
            section = re.sub(
                r"MAX_REFERENCE_GIT_OUTPUT_BYTES: Final = [^\n]+",
                "MAX_REFERENCE_GIT_OUTPUT_BYTES: Final = 16",
                _repo_contract_python_section("Script reference integrity"),
            )
            result = _run_repo_contract_python_section(
                "Script reference integrity", root, source=section
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("unsafe script-reference surface", result.stderr)

    def test_migration0003_slice_is_exact_and_preconditions_are_resolved(self) -> None:
        migration = load_task8_migration(ROOT)
        self.assertEqual(TASK8_ROW_IDS, tuple(row.row_id for row in migration.rows))
        self.assertEqual(192, sum(row.action == "rename" for row in migration.rows))
        self.assertEqual(1, sum(row.action == "delete" for row in migration.rows))
        for row in migration.rows:
            source_exists = (ROOT / row.source_path).is_file()
            target_exists = row.target_path is not None and (ROOT / row.target_path).is_file()
            with self.subTest(row=row.row_id):
                if row.action == "rename":
                    self.assertNotEqual(source_exists, target_exists)
                else:
                    self.assertIsNone(row.target_path)

    def test_migration0002_is_rejected_as_current_structural_authority(self) -> None:
        with self.assertRaisesRegex(OperationsAuthorityError, "Migration 0003"):
            load_task8_migration(ROOT, SEMANTIC_WITNESS_PATH)

    def test_consumer_extractor_freezes_exact_declared_and_live_union(self) -> None:
        inventory = extract_task8_consumers(ROOT, load_task8_migration(ROOT))
        self.assertEqual(315, len(inventory.declared_raw))
        self.assertEqual(tuple(sorted(set(inventory.union))), inventory.union)
        self.assertTrue(inventory.declared_current)
        self.assertGreater(inventory.tracked_files, 0)
        self.assertLessEqual(inventory.tracked_files, 10_000)
        self.assertLessEqual(inventory.tracked_bytes, 300_000_000)

    def test_consumer_extractor_rejects_unbounded_file_count_and_bytes(self) -> None:
        migration = load_task8_migration(ROOT)
        with self.assertRaisesRegex(OperationsAuthorityError, "file bound"):
            extract_task8_consumers(ROOT, migration, max_files=1)
        with self.assertRaisesRegex(OperationsAuthorityError, "bound"):
            extract_task8_consumers(ROOT, migration, max_bytes=1)

    def test_semantic_merge_witnesses_are_body_derived_and_present(self) -> None:
        self.assertEqual([], _validate_semantic_witnesses(ROOT))
        text = (ROOT / SEMANTIC_WITNESS_PATH).read_text(encoding="utf-8")
        ledger = yaml.safe_load(
            text.split("## Archive Ledger", 1)[1]
            .split("```yaml", 1)[1]
            .split("```", 1)[0]
        )
        rows = [row for row in ledger["files"] if row["semantic_action"] == "merge"]
        self.assertEqual(2, len(rows))
        for row in rows:
            source = subprocess.run(
                ["git", "show", f"{row['source_commit']}:{row['legacy_path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            target_parts = pathlib.PurePosixPath(row["final_path"]).parts
            target = pathlib.PurePosixPath(
                *(target_parts[:4] + (target_parts[4][4:],) + target_parts[5:])
            )
            current_path = ROOT / target
            if not current_path.is_file():
                current_path = ROOT / row["final_path"]
            current = current_path.read_text(encoding="utf-8")
            witnesses = [
                value.split(":", 2)[2]
                for value in row["preserved_semantics"]
                if value.startswith("text:")
            ]
            with self.subTest(target=target):
                self.assertTrue(witnesses)
                self.assertTrue(all(value in source for value in witnesses))
                self.assertTrue(all(value in current for value in witnesses))

    def test_frozen_migration_hash_is_unchanged(self) -> None:
        result = subprocess.run(
            ["sha256sum", str(MIGRATION_PATH)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertTrue(
            result.stdout.startswith(
                "271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9"
            )
        )


class SemanticWitnessBoundaryTests(unittest.TestCase):
    TARGETS = (
        pathlib.PurePosixPath(
            "docs/05.operations/catalog/00-workspace/"
            "0004-harness-agent-first-engineering/runbook.md"
        ),
        pathlib.PurePosixPath(
            "docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md"
        ),
    )

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        migration = root / SEMANTIC_WITNESS_PATH
        migration.parent.mkdir(parents=True)
        shutil.copy2(ROOT / SEMANTIC_WITNESS_PATH, migration)
        for relative in self.TARGETS:
            target = root / relative
            target.parent.mkdir(parents=True)
            shutil.copy2(ROOT / relative, target)
        return directory, root

    @staticmethod
    def _source_result(arguments: object) -> GitCommandResult:
        assert isinstance(arguments, list)
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        return GitCommandResult(result.returncode, result.stdout, result.stderr)

    def _validate(self, root: pathlib.Path) -> list[object]:
        def bounded_git(_root: pathlib.Path, arguments: list[str], **_kwargs: object) -> GitCommandResult:
            return self._source_result(arguments)

        with mock.patch(
            "scripts.lib.document_governance.operations_catalog._run_git_bounded",
            side_effect=bounded_git,
        ):
            return _validate_semantic_witnesses(root)

    def test_markdown_body_excludes_frontmatter_and_headings(self) -> None:
        text = "---\nnote: frontmatter-only\n---\n# heading-only\nbody-only\n"
        body = _markdown_body_text(text)
        self.assertNotIn("frontmatter-only", body)
        self.assertNotIn("heading-only", body)
        self.assertIn("body-only", body)

    def test_exact_merge_row_identity_is_required(self) -> None:
        context, root = self._fixture()
        with context:
            path = root / SEMANTIC_WITNESS_PATH
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "  final_path: docs/05.operations/catalog/00-workspace/"
                    "ops-0004-harness-agent-first-engineering/runbook.md\n"
                    "  semantic_action: merge",
                    "  final_path: docs/05.operations/catalog/00-workspace/"
                    "ops-0006-infrastructure-optimization-governance/runbook.md\n"
                    "  semantic_action: merge",
                    1,
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "semantic-witness-row-invalid",
                {finding.code for finding in self._validate(root)},
            )

    def test_stale_prefixed_target_is_never_a_fallback(self) -> None:
        context, root = self._fixture()
        with context:
            current = root / self.TARGETS[0]
            stale = root / (
                "docs/05.operations/catalog/00-workspace/"
                "ops-0004-harness-agent-first-engineering/runbook.md"
            )
            stale.parent.mkdir(parents=True, exist_ok=True)
            current.rename(stale)
            codes = {finding.code for finding in self._validate(root)}
            self.assertIn("file-unreadable", codes)

    def test_empty_and_oversize_text_witnesses_are_rejected(self) -> None:
        marker = (
            "text:graphify-advisory-corroboration:"
            "bash scripts/knowledge/report-graphify-health.sh"
        )
        for replacement in ("text:graphify-advisory-corroboration:", f"text:oversize:{'x' * 4097}"):
            with self.subTest(length=len(replacement)):
                context, root = self._fixture()
                with context:
                    path = root / SEMANTIC_WITNESS_PATH
                    path.write_text(
                        path.read_text(encoding="utf-8").replace(marker, replacement, 1),
                        encoding="utf-8",
                    )
                    self.assertIn(
                        "semantic-witness-invalid",
                        {finding.code for finding in self._validate(root)},
                    )


if __name__ == "__main__":
    unittest.main()
