from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
import textwrap
import time
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/rehearse-postgres-logical-upgrade.sh"
FIXTURE = ROOT / "tests/fixtures/postgres-logical-upgrade"
COMPOSE = FIXTURE / "docker-compose.yml"
SEED_SQL = FIXTURE / "sql/001_schema_and_seed.sql"
ORACLE_SQL = FIXTURE / "sql/010_integrity_oracle.sql"
PARTIAL_SQL = FIXTURE / "sql/020_negative_partial_state.sql"
ALIGNMENT_CHECK = ROOT / "scripts/validation/check-doc-implementation-alignment.sh"
REPO_CONTRACTS = ROOT / "scripts/validation/check-repo-contracts.sh"

SOURCE_IMAGE = (
    "postgres:17.6-alpine@sha256:"
    "ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94"
)
TARGET_IMAGE = (
    "postgres:18.4-alpine@sha256:"
    "9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15"
)
CLIENT_IMAGE = TARGET_IMAGE
SOURCE_IMAGE_ID = "sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94"
TARGET_IMAGE_ID = "sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15"
CLIENT_IMAGE_ID = TARGET_IMAGE_ID
EXPECTED_VERDICT_KEYS = {
    "schema_version",
    "producer_spec",
    "scope",
    "source_image",
    "target_image",
    "fixture_sha256",
    "dump_sha256",
    "integrity_status",
    "backup_seconds",
    "restore_seconds",
    "cleanup_status",
    "redaction_status",
}


def valid_rendered_topology_json(
    project: str = "fixture", password: str = "synthetic"
) -> str:
    return json.dumps(
        {
            "name": project,
            "networks": {
                "default": {
                    "name": f"{project}_default",
                    "ipam": {},
                }
            },
            "services": {
                "source": {
                    "command": None,
                    "entrypoint": None,
                    "environment": {
                        "POSTGRES_DB": "rehearsal",
                        "POSTGRES_PASSWORD": password,
                        "POSTGRES_USER": "rehearsal",
                    },
                    "healthcheck": {
                        "test": [
                            "CMD-SHELL",
                            "pg_isready -U rehearsal -d rehearsal",
                        ],
                        "timeout": "2s",
                        "interval": "2s",
                        "retries": 30,
                    },
                    "image": SOURCE_IMAGE,
                    "networks": {"default": None},
                    "pull_policy": "never",
                    "volumes": [
                        {
                            "type": "volume",
                            "target": "/var/lib/postgresql/data",
                            "volume": {},
                        }
                    ],
                },
                "target": {
                    "command": None,
                    "entrypoint": None,
                    "environment": {
                        "POSTGRES_DB": "rehearsal",
                        "POSTGRES_PASSWORD": password,
                        "POSTGRES_USER": "rehearsal",
                    },
                    "healthcheck": {
                        "test": [
                            "CMD-SHELL",
                            "pg_isready -U rehearsal -d rehearsal",
                        ],
                        "timeout": "2s",
                        "interval": "2s",
                        "retries": 30,
                    },
                    "image": TARGET_IMAGE,
                    "networks": {"default": None},
                    "pull_policy": "never",
                    "volumes": [
                        {
                            "type": "volume",
                            "target": "/var/lib/postgresql",
                            "volume": {},
                        }
                    ],
                },
            },
        },
        separators=(",", ":"),
    )


class PostgresLogicalUpgradeRehearsalTests(unittest.TestCase):
    maxDiff = None

    def run_script(
        self, *args: str, extra_env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="ior-direct-run-", dir="/tmp") as tmp:
            root = Path(tmp) / "repo"
            script = root / "scripts/validation/rehearse-postgres-logical-upgrade.sh"
            script.parent.mkdir(parents=True)
            shutil.copy2(SCRIPT, script)
            shutil.copytree(
                FIXTURE,
                root / "tests/fixtures/postgres-logical-upgrade",
            )
            (root / "_workspace/repo-support").mkdir(parents=True, mode=0o700)
            env = os.environ.copy()
            if extra_env:
                env.update(extra_env)
            return subprocess.run(
                ["bash", str(script), *args],
                cwd=root,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

    def run_sourced(
        self, body: str, *, extra_env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        command = (
            "IOR_SOURCE_ONLY=1 "
            "IOR_TEST_SOURCE_ONLY=postgres-logical-upgrade-rehearsal-tests "
            f"source {SCRIPT!s}\n{body}"
        )
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["bash", "-c", command],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_evidence_directory_is_exclusively_owned_and_identity_bound(self) -> None:
        run_id = str(time.time_ns())
        evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
        result = self.run_sourced(
            textwrap.dedent(
                f"""\
                RUN_ID={run_id}
                EVIDENCE_DIR={evidence!s}
                CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                DUMP_PATH={evidence!s}/rehearsal.dump
                SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                RUNTIME_LOG={evidence!s}/runtime.log
                IOR_TEST_MODE=1
                IOR_TEST_TOTAL_TIMEOUT=10
                IOR_TEST_CLEANUP_RESERVE=3
                initialize_runtime_state
                test "$EVIDENCE_OWNED" = true
                test -n "$EVIDENCE_DEVICE_INODE"
                verify_evidence_ownership
                cleanup_owned_evidence_dir
                """
            )
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(evidence.exists())

    def test_preexisting_evidence_directory_is_never_mutated(self) -> None:
        run_id = str(time.time_ns())
        evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
        evidence.mkdir(mode=0o700)
        sentinel = evidence / "runtime.log"
        sentinel.write_text("foreign-sentinel\n", encoding="utf-8")
        try:
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    RUN_ID={run_id}
                    EVIDENCE_DIR={evidence!s}
                    RUNTIME_LOG={sentinel!s}
                    create_owned_evidence_dir
                    """
                )
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(
                sentinel.read_text(encoding="utf-8"), "foreign-sentinel\n"
            )
        finally:
            sentinel.unlink(missing_ok=True)
            evidence.rmdir()

    def test_evidence_directory_symlink_is_never_followed_or_mutated(self) -> None:
        run_id = str(time.time_ns())
        evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
        with tempfile.TemporaryDirectory(prefix="ior-foreign-", dir="/tmp") as tmp:
            foreign = Path(tmp)
            sentinel = foreign / "runtime.log"
            sentinel.write_text("foreign-sentinel\n", encoding="utf-8")
            evidence.symlink_to(foreign, target_is_directory=True)
            try:
                result = self.run_sourced(
                    textwrap.dedent(
                        f"""\
                        RUN_ID={run_id}
                        EVIDENCE_DIR={evidence!s}
                        RUNTIME_LOG={evidence!s}/runtime.log
                        create_owned_evidence_dir
                        """
                    )
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(evidence.is_symlink())
                self.assertEqual(
                    sentinel.read_text(encoding="utf-8"), "foreign-sentinel\n"
                )
            finally:
                evidence.unlink(missing_ok=True)

    def test_canonical_symlink_and_directory_are_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-canonical-", dir="/tmp") as tmp:
            root = Path(tmp)
            foreign = root / "foreign.json"
            foreign.write_text('{"foreign":true}\n', encoding="utf-8")
            symlink = root / "symlink.json"
            symlink.symlink_to(foreign)
            directory = root / "directory.json"
            directory.mkdir()
            for unsafe in (symlink, directory):
                result = self.run_sourced(
                    textwrap.dedent(
                        f"""\
                        HANDOFF_DIR={root!s}
                        HANDOFF_PATH={unsafe!s}
                        invalidate_canonical_handoff
                        """
                    )
                )
                self.assertNotEqual(result.returncode, 0)
            self.assertTrue(symlink.is_symlink())
            self.assertTrue(directory.is_dir())
            self.assertEqual(
                foreign.read_text(encoding="utf-8"), '{"foreign":true}\n'
            )

    def test_canonical_parent_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-parent-", dir="/tmp") as tmp:
            root = Path(tmp)
            real_parent = root / "real"
            real_parent.mkdir()
            handoff = real_parent / "recovery-verdict.json"
            handoff.write_text('{"stale":true}\n', encoding="utf-8")
            linked_parent = root / "linked"
            linked_parent.symlink_to(real_parent, target_is_directory=True)
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    HANDOFF_DIR={linked_parent!s}
                    HANDOFF_PATH={linked_parent!s}/recovery-verdict.json
                    invalidate_canonical_handoff
                    """
                )
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(handoff.exists())

    def test_cleanup_accumulates_failures_and_attempts_every_owner(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-cleanup-all-", dir="/tmp") as tmp:
            root = Path(tmp)
            calls = root / "calls"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    HANDOFF_DIR={root!s}
                    HANDOFF_PATH={root!s}/recovery-verdict.json
                    SOURCE_OWNED=true
                    TARGET_OWNED=true
                    DUMP_CLIENT_MAY_EXIST=true
                    cleanup_labeled_dump_clients() {{ echo client >> {calls!s}; return 60; }}
                    cleanup_one_owned_project() {{ echo "$1" >> {calls!s}; return 60; }}
                    cleanup_owned_evidence_dir() {{ echo evidence >> {calls!s}; return 60; }}
                    cleanup_owned_projects_and_tmp
                    """
                )
            )
            call_text = calls.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 60, result.stdout + result.stderr)
        self.assertIn("client", call_text)
        self.assertIn("target", call_text)
        self.assertIn("source", call_text)
        self.assertIn("evidence", call_text)

    def test_candidate_is_memory_only_and_publication_requires_complete_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-state-machine-", dir="/tmp") as tmp:
            root = Path(tmp)
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            handoff = root / "recovery-verdict.json"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    HANDOFF_DIR={root!s}
                    HANDOFF_PATH={handoff!s}
                    EVIDENCE_DIR={evidence!s}
                    SOURCE_IMAGE={SOURCE_IMAGE!r}
                    TARGET_IMAGE={TARGET_IMAGE!r}
                    FIXTURE_SHA256={'a' * 64!r}
                    DUMP_SHA256={'b' * 64!r}
                    BACKUP_SECONDS=1
                    RESTORE_SECONDS=2
                    write_recovery_verdict
                    test "$CANDIDATE_WRITTEN" = true
                    test ! -e "$CANDIDATE_PATH"
                    ! publish_canonical_after_cleanup
                    test ! -e "$HANDOFF_PATH"
                    """
                )
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_deadline_precedes_every_docker_call_and_reserves_cleanup(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        main = text[text.index("main() {") :]
        self.assertLess(main.index("initialize_runtime_state"), main.index("assert_safe"))
        self.assertIn("CLEANUP_RESERVE_SECONDS", text)
        self.assertIn("OPERATION_DEADLINE", text)
        self.assertIn("run_cleanup_bounded", text)
        direct_docker_lines = [
            line.strip()
            for line in text.splitlines()
            if re.match(r"^\s*docker(?:\s|$)", line)
        ]
        self.assertEqual(direct_docker_lines, [])
        self.assertRegex(text, r'"\$runner" docker (?:ps|network|volume)')
        self.assertEqual(text.count("run_bounded sleep 1"), 2)
        self.assertNotRegex(text, re.compile(r"^\s+sleep 1$", re.MULTILINE))

    def test_readiness_pause_cannot_cross_operation_deadline(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-pause-", dir="/tmp") as tmp:
            calls = Path(tmp) / "calls"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    RUNTIME_LOG=/dev/null
                    SOURCE_PROJECT=source-boundary
                    verify_evidence_ownership() {{ return 0; }}
                    database_readiness_stable() {{ return 1; }}
                    service_has_terminal_state() {{ return 1; }}
                    run_bounded() {{
                      printf '%s\n' "$*" >> {calls!s}
                      if [ "$1" = sleep ]; then return 124; fi
                      return 0
                    }}
                    OPERATION_DEADLINE=$((SECONDS + 2))
                    start_source_and_wait
                    """
                )
            )
            call_text = calls.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 20, result.stdout + result.stderr)
        self.assertIn("failure_class=readiness", result.stdout)
        self.assertIn("sleep 1", call_text)

    def test_direct_execution_rejects_every_test_control_before_docker(self) -> None:
        controls = {
            "IOR_RUN_ID": "424242",
            "IOR_EVIDENCE_DIR": "/tmp/hyhome-ior-evidence.424242",
            "IOR_PROJECT_PREFIX": "hyhome-ior-20260719",
            "IOR_TEST_MODE": "1",
            "IOR_TEST_TOTAL_TIMEOUT": "3",
            "IOR_TEST_CLEANUP_RESERVE": "1",
            "IOR_SOURCE_ONLY": "1",
            "IOR_TEST_SOURCE_ONLY": "postgres-logical-upgrade-rehearsal-tests",
        }
        for variable, value in controls.items():
            with self.subTest(variable=variable):
                with tempfile.TemporaryDirectory(
                    prefix="ior-direct-control-", dir="/tmp"
                ) as tmp:
                    root = Path(tmp) / "repo"
                    isolated_script = (
                        root
                        / "scripts/validation/rehearse-postgres-logical-upgrade.sh"
                    )
                    isolated_script.parent.mkdir(parents=True)
                    shutil.copy2(SCRIPT, isolated_script)
                    handoff_dir = (
                        root
                        / "_workspace"
                        / "repo-support"
                        / "task-2026-07-19-infrastructure-operations-readiness-remediation"
                        / "postgres"
                    )
                    handoff_dir.mkdir(parents=True, mode=0o700)
                    handoff = handoff_dir / "recovery-verdict.json"
                    handoff.write_text('{"stale":true}\n', encoding="utf-8")
                    handoff.chmod(0o600)
                    fake_bin = Path(tmp) / "bin"
                    fake_bin.mkdir()
                    calls = Path(tmp) / "calls"
                    docker = fake_bin / "docker"
                    docker.write_text(
                        "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$IOR_TEST_DOCKER_CALLS\"\n",
                        encoding="utf-8",
                    )
                    docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
                    env = os.environ.copy()
                    env.update(
                        {
                            "PATH": f"{fake_bin}:{os.environ['PATH']}",
                            "IOR_TEST_DOCKER_CALLS": str(calls),
                            variable: value,
                        }
                    )
                    result = subprocess.run(
                        ["bash", str(isolated_script), "--check"],
                        cwd=root,
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertEqual(
                        result.returncode, 10, result.stdout + result.stderr
                    )
                    self.assertIn("reason=test-control-forbidden", result.stdout)
                    self.assertIn("cleanup_status=passed", result.stdout)
                    self.assertFalse(handoff.exists())
                    self.assertFalse(calls.exists())

    def test_direct_control_failure_invalidates_isolated_stale_canonical(self) -> None:
        controls = {
            "IOR_RUN_ID": "424242",
            "IOR_EVIDENCE_DIR": "/tmp/hyhome-ior-evidence.424242",
            "IOR_PROJECT_PREFIX": "hyhome-ior-20260719",
            "IOR_TEST_MODE": "1",
            "IOR_TEST_TOTAL_TIMEOUT": "3",
            "IOR_TEST_CLEANUP_RESERVE": "1",
            "IOR_SOURCE_ONLY": "1",
            "IOR_TEST_SOURCE_ONLY": "postgres-logical-upgrade-rehearsal-tests",
        }
        unset_controls = " ".join(controls)
        for variable, value in controls.items():
            with self.subTest(variable=variable):
                with tempfile.TemporaryDirectory(
                    prefix="ior-direct-stale-", dir="/tmp"
                ) as tmp:
                    root = Path(tmp) / "repo"
                    handoff_dir = (
                        root
                        / "_workspace"
                        / "repo-support"
                        / "task-2026-07-19-infrastructure-operations-readiness-remediation"
                        / "postgres"
                    )
                    handoff_dir.mkdir(parents=True, mode=0o700)
                    handoff = handoff_dir / "recovery-verdict.json"
                    handoff.write_text('{"stale":true}\n', encoding="utf-8")
                    fake_bin = Path(tmp) / "bin"
                    fake_bin.mkdir()
                    calls = Path(tmp) / "calls"
                    docker = fake_bin / "docker"
                    docker.write_text(
                        "#!/bin/sh\n"
                        "printf '%s\\n' \"$*\" >> \"$IOR_TEST_DOCKER_CALLS\"\n"
                        "exit 99\n",
                        encoding="utf-8",
                    )
                    docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
                    result = self.run_sourced(
                        textwrap.dedent(
                            f"""\
                            unset {unset_controls}
                            SCRIPT_IS_SOURCED=false
                            ROOT_DIR={root!s}
                            HANDOFF_DIR={handoff_dir!s}
                            HANDOFF_PATH={handoff!s}
                            PATH={fake_bin!s}:$PATH
                            IOR_TEST_DOCKER_CALLS={calls!s}
                            {variable}={value}
                            export PATH IOR_TEST_DOCKER_CALLS {variable}
                            main --check
                            """
                        )
                    )
                    self.assertEqual(
                        result.returncode, 10, result.stdout + result.stderr
                    )
                    self.assertIn("reason=test-control-forbidden", result.stdout)
                    self.assertIn("cleanup_status=passed", result.stdout)
                    self.assertFalse(calls.exists())
                    self.assertFalse(handoff.exists())

    def test_direct_run_id_is_process_pid_and_check_reports_active_budget(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('RUN_ID="$$"', text)
        self.assertEqual(text.count('RUN_ID="${IOR_RUN_ID:-$$}"'), 1)
        self.assertRegex(
            text,
            re.compile(
                r'if \[ "\$TEST_SOURCE_BOUNDARY" = true \]; then[\s\S]+?'
                r'RUN_ID="\$\{IOR_RUN_ID:-\$\$\}"[\s\S]+?fi'
            ),
        )
        self.assertIn(
            "printf 'total_timeout_seconds=%s\\n' \"$ACTIVE_TOTAL_TIMEOUT\"",
            text,
        )
        self.assertIn(
            "printf 'cleanup_reserve_seconds=%s\\n' \"$ACTIVE_CLEANUP_RESERVE\"",
            text,
        )

    def test_rendered_topology_mutations_fail_closed(self) -> None:
        topology_dir = FIXTURE / "topology"
        for name, reason in (
            ("long-form-bind.json", "unsafe-volume"),
            ("privileged-host.json", "unsafe-service-option"),
            ("bad-target-major.json", "bad-target-major"),
            ("fixed-network.json", "unsafe-network"),
            ("removed-healthcheck.json", "unsafe-healthcheck"),
            ("wrong-password.json", "unsafe-environment"),
        ):
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    IOR_POSTGRES_PASSWORD=synthetic
                    export IOR_POSTGRES_PASSWORD
                    validate_rendered_topology_file {topology_dir / name!s} fixture
                    """
                )
            )
            self.assertNotEqual(result.returncode, 0, name)
            self.assertIn(reason, result.stdout + result.stderr)
            self.assertNotIn("wrong-secret-value", result.stdout + result.stderr)

    def test_render_validates_both_exact_project_names(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn(
            '"$SOURCE_PROJECT" "$RENDERED_TOPOLOGY_PATH" false', text
        )
        self.assertIn(
            '"$TARGET_PROJECT" "$TARGET_RENDERED_TOPOLOGY_PATH"', text
        )
        self.assertIn('docker compose -p "$project"', text)

    def test_compose_render_command_error_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-render-error-", dir="/tmp") as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    f"""\
                    #!/bin/sh
                    case "$*" in
                      "image inspect --format {{{{.Id}}}} {SOURCE_IMAGE}")
                        printf '%s\n' {SOURCE_IMAGE_ID!r}
                        ;;
                      "image inspect --format {{{{.Id}}}} {TARGET_IMAGE}")
                        printf '%s\n' {TARGET_IMAGE_ID!r}
                        ;;
                      "compose version") exit 0 ;;
                      *) exit 71 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    RUN_ID={run_id}
                    EVIDENCE_DIR={evidence!s}
                    SOURCE_PROJECT="${{PROJECT_PREFIX}}-${{RUN_ID}}-source"
                    TARGET_PROJECT="${{PROJECT_PREFIX}}-${{RUN_ID}}-target"
                    CANDIDATE_PATH="${{EVIDENCE_DIR}}/recovery-verdict.candidate.json"
                    DUMP_PATH="${{EVIDENCE_DIR}}/rehearsal.dump"
                    SOURCE_ORACLE_PATH="${{EVIDENCE_DIR}}/source-oracle.json"
                    TARGET_ORACLE_PATH="${{EVIDENCE_DIR}}/target-oracle.json"
                    RUNTIME_LOG="${{EVIDENCE_DIR}}/runtime.log"
                    initialize_runtime_state || exit $?
                    assert_safe_images_paths_and_project
                    status=$?
                    cleanup_owned_evidence_dir || exit 60
                    exit "$status"
                    """
                ),
                extra_env={"PATH": f"{fake_bin}:{os.environ['PATH']}"},
            )
        self.assertEqual(result.returncode, 10, result.stdout + result.stderr)
        self.assertIn("reason=compose-render-failed", result.stdout)
        self.assertFalse(evidence.exists())

    def test_required_wrapper_symbols_follow_contract_order(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        symbols = [
            "parse_args",
            "assert_safe_images_paths_and_project",
            "start_source_and_wait",
            "apply_seed_sql",
            "capture_source_oracle",
            "dump_custom_format_with_pg18_client",
            "start_target_and_wait",
            "restore_without_owner_or_acl",
            "capture_target_oracle",
            "compare_oracles",
            "run_selected_negative_case",
            "write_recovery_verdict",
            "cleanup_owned_projects_and_tmp",
        ]
        offsets = []
        for symbol in symbols:
            match = re.search(rf"^{symbol}\(\) \{{", text, flags=re.MULTILINE)
            self.assertIsNotNone(match, symbol)
            offsets.append(match.start())
        self.assertEqual(offsets, sorted(offsets))

    def test_fixture_uses_only_pinned_source_and_target(self) -> None:
        text = COMPOSE.read_text(encoding="utf-8")
        self.assertEqual(text.count(SOURCE_IMAGE), 1)
        self.assertEqual(text.count(TARGET_IMAGE), 1)
        self.assertEqual(
            re.findall(r"^  ([a-z][a-z0-9_-]+):$", text, flags=re.MULTILINE),
            ["source", "target"],
        )
        for forbidden in (
            "container_name:",
            "ports:",
            "external:",
            "restart:",
            "${DEFAULT_DATA_DIR}",
            "./:",
        ):
            self.assertNotIn(forbidden, text)
        self.assertEqual(text.count("- /var/lib/postgresql/data"), 1)
        self.assertEqual(
            len(re.findall(r"^\s+- /var/lib/postgresql$", text, re.MULTILINE)),
            1,
        )
        self.assertEqual(text.count("pg_isready -U rehearsal -d rehearsal"), 2)

    def test_source_target_and_client_have_explicit_digest_and_local_id_pins(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        expected_assignments = (
            f"SOURCE_IMAGE='{SOURCE_IMAGE}'",
            f"TARGET_IMAGE='{TARGET_IMAGE}'",
            f"DUMP_CLIENT_IMAGE='{CLIENT_IMAGE}'",
            f"SOURCE_IMAGE_ID='{SOURCE_IMAGE_ID}'",
            f"TARGET_IMAGE_ID='{TARGET_IMAGE_ID}'",
            f"DUMP_CLIENT_IMAGE_ID='{CLIENT_IMAGE_ID}'",
        )
        for assignment in expected_assignments:
            self.assertIn(assignment, text)

    def test_exact_local_image_ids_are_checked_before_compose_or_runtime(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-image-ids-", dir="/tmp") as tmp:
            calls = Path(tmp) / "calls"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    OPERATION_DEADLINE=$((SECONDS + 30))
                    run_bounded() {{
                      printf '%s\n' "$*" >> {calls!s}
                      case "${{@: -1}}" in
                        "$SOURCE_IMAGE") printf '%s\n' "$SOURCE_IMAGE_ID" ;;
                        "$TARGET_IMAGE"|"$DUMP_CLIENT_IMAGE") printf '%s\n' "$TARGET_IMAGE_ID" ;;
                        *) return 99 ;;
                      esac
                    }}
                    assert_exact_local_image_identities
                    """
                )
            )
            observed = calls.read_text(encoding="utf-8").splitlines() if calls.exists() else []
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            [
                f"docker image inspect --format {{{{.Id}}}} {SOURCE_IMAGE}",
                f"docker image inspect --format {{{{.Id}}}} {TARGET_IMAGE}",
                f"docker image inspect --format {{{{.Id}}}} {CLIENT_IMAGE}",
            ],
            observed,
        )

        text = SCRIPT.read_text(encoding="utf-8")
        preflight = text.split("assert_safe_images_paths_and_project() {", 1)[1].split(
            "\n}\n\nservice_has_terminal_state", 1
        )[0]
        self.assertLess(
            preflight.index("assert_exact_local_image_identities"),
            preflight.index("docker compose version"),
        )

    def test_missing_or_replaced_local_image_fails_before_other_runtime_calls(self) -> None:
        for name, response in (
            ("missing", "return 1"),
            ("replaced", "printf '%s\\n' sha256:" + "f" * 64),
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="ior-image-gate-", dir="/tmp"
            ) as tmp:
                calls = Path(tmp) / "calls"
                result = self.run_sourced(
                    textwrap.dedent(
                        f"""\
                        OPERATION_DEADLINE=$((SECONDS + 30))
                        run_bounded() {{
                          printf '%s\n' "$*" >> {calls!s}
                          {response}
                        }}
                        assert_exact_local_image_identities
                        """
                    )
                )
                observed = calls.read_text(encoding="utf-8").splitlines() if calls.exists() else []
            self.assertEqual(10, result.returncode, result.stdout + result.stderr)
            self.assertEqual(1, len(observed))
            self.assertTrue(observed[0].startswith("docker image inspect "))
            self.assertNotIn("compose", observed[0])
            self.assertNotIn("create", observed[0])
            self.assertNotIn("run", observed[0])

    def test_all_start_and_create_paths_disable_pull_and_build(self) -> None:
        compose = COMPOSE.read_text(encoding="utf-8")
        self.assertEqual(2, compose.count("pull_policy: never"))

        text = SCRIPT.read_text(encoding="utf-8")
        up_lines = [line.strip() for line in text.splitlines() if " compose " in line and " up " in line]
        self.assertEqual(2, len(up_lines))
        for command in up_lines:
            self.assertIn("--pull never", command)
            self.assertIn("--no-build", command)

        client = text.split("create_owned_dump_client() {", 1)[1].split(
            "\n}\n\ndump_custom_format_with_pg18_client", 1
        )[0]
        self.assertIn("run_bounded docker create", client)
        self.assertIn("--pull=never", client)
        self.assertIn('"$DUMP_CLIENT_IMAGE"', client)
        self.assertNotRegex(text, r"run_bounded docker run(?:\s|$)")

    def test_seed_schema_is_deterministic(self) -> None:
        text = SEED_SQL.read_text(encoding="utf-8")
        self.assertIn("rehearsal_schema_version", text)
        self.assertIn("accounts", text)
        self.assertIn("orders", text)
        self.assertRegex(text, r"INSERT INTO accounts[\s\S]+?\(3,")
        self.assertRegex(text, r"INSERT INTO orders[\s\S]+?\(4,")
        self.assertIn("balance >= 0", text)
        self.assertIn("amount > 0", text)
        self.assertIn("state IN ('open', 'paid')", text)

    def test_rehearsal_runbook_is_not_classified_as_an_infra_service(self) -> None:
        text = ALIGNMENT_CHECK.read_text(encoding="utf-8")
        self.assertEqual(
            text.count('"postgresql-logical-upgrade-restore-rehearsal"'), 1
        )
        self.assertRegex(
            text,
            re.compile(
                r"NON_SERVICE_STEMS\s*=\s*\{[\s\S]+?"
                r'"postgresql-logical-upgrade-restore-rehearsal"[\s\S]+?\}',
            ),
        )

    def test_wrapper_is_in_the_exact_script_inventory(self) -> None:
        text = REPO_CONTRACTS.read_text(encoding="utf-8")
        self.assertEqual(
            text.count(
                'pathlib.Path("scripts/validation/'
                'rehearse-postgres-logical-upgrade.sh")'
            ),
            1,
        )

    def test_direct_evidence_override_is_forbidden(self) -> None:
        result = self.run_script(
            "--check", extra_env={"IOR_EVIDENCE_DIR": "/var/tmp/ior-unsafe"}
        )
        self.assertEqual(result.returncode, 10, result.stdout + result.stderr)
        self.assertIn("failure_class=preflight", result.stdout)
        self.assertIn("reason=test-control-forbidden", result.stdout)

    def test_rejects_project_collision(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-fake-docker-", dir="/tmp") as tmp:
            fake_bin = Path(tmp)
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    f"""\
                    #!/bin/sh
                    case "$*" in
                      "image inspect --format {{{{.Id}}}} {SOURCE_IMAGE}")
                        printf '%s\n' {SOURCE_IMAGE_ID!r}
                        ;;
                      "image inspect --format {{{{.Id}}}} {TARGET_IMAGE}")
                        printf '%s\n' {TARGET_IMAGE_ID!r}
                        ;;
                      "compose version") exit 0 ;;
                      *"config --format json")
                        printf '%s\\n' {valid_rendered_topology_json()!r}
                        exit 0
                        ;;
                      *"ps -aq --filter label=com.docker.compose.project="*)
                        printf '%s\\n' collision-container
                        exit 0
                        ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            env = {
                "PATH": f"{fake_bin}:{os.environ['PATH']}",
                "IOR_RUN_ID": "424242",
                "IOR_EVIDENCE_DIR": "/tmp/hyhome-ior-evidence.424242",
            }
            result = self.run_sourced(
                textwrap.dedent(
                    """\
                    render_and_validate_topology() { return 0; }
                    initialize_runtime_state || exit $?
                    assert_safe_images_paths_and_project
                    status=$?
                    cleanup_owned_evidence_dir || exit 60
                    exit "$status"
                    """
                ),
                extra_env=env,
            )
        self.assertEqual(result.returncode, 10, result.stdout + result.stderr)
        self.assertIn("reason=project-collision", result.stdout)

    def test_oracle_contains_no_row_payload(self) -> None:
        text = ORACLE_SQL.read_text(encoding="utf-8")
        self.assertIn("json_build_object", text)
        self.assertIn("server_version_num", text)
        self.assertIn("md5", text.lower())
        self.assertNotIn("\\pset", text)
        self.assertIn("contype IN ('p', 'u', 'f', 'c')", text)
        self.assertNotRegex(text.lower(), r"json_agg|jsonb_agg|row_to_json")
        self.assertNotRegex(text, re.compile(r"SELECT\s+\*", re.IGNORECASE))
        seed = SEED_SQL.read_text(encoding="utf-8")
        row_codes = re.findall(r"\(\d+,\s*'([^']+)'", seed)
        self.assertGreaterEqual(len(row_codes), 3)
        for value in row_codes:
            self.assertNotIn(value, text)

    def test_bad_target_major_fails_preflight(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-bad-major-", dir="/tmp") as tmp:
            fake_bin = Path(tmp)
            docker = fake_bin / "docker"
            rendered = valid_rendered_topology_json("__PROJECT__", "__PASSWORD__")
            docker.write_text(
                textwrap.dedent(
                    f"""\
                    #!/bin/sh
                    case "$*" in
                      "image inspect --format {{{{.Id}}}} {SOURCE_IMAGE}")
                        printf '%s\n' {SOURCE_IMAGE_ID!r}
                        ;;
                      "image inspect --format {{{{.Id}}}} {TARGET_IMAGE}")
                        printf '%s\n' {TARGET_IMAGE_ID!r}
                        ;;
                      "compose version") exit 0 ;;
                      *"config --format json")
                        printf '%s\n' {rendered!r} | sed \
                          -e "s/__PROJECT__/$3/g" \
                          -e "s/__PASSWORD__/$IOR_POSTGRES_PASSWORD/g"
                        ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            result = self.run_script(
                "--negative-case",
                "bad-target-major",
                extra_env={"PATH": f"{fake_bin}:{os.environ['PATH']}"},
            )
        self.assertEqual(result.returncode, 10, result.stdout + result.stderr)
        self.assertIn("failure_class=preflight", result.stdout)
        self.assertIn("reason=bad-target-major", result.stdout)

    def test_checksum_mismatch_is_nonzero(self) -> None:
        captured = hashlib.sha256(b"before-corruption").hexdigest()
        run_id = str(time.time_ns())
        evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
        result = self.run_sourced(
            textwrap.dedent(
                f"""\
                RUN_ID={run_id}
                EVIDENCE_DIR={evidence!s}
                CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                DUMP_PATH={evidence!s}/rehearsal.dump
                SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                RUNTIME_LOG={evidence!s}/runtime.log
                IOR_TEST_MODE=1
                IOR_TEST_TOTAL_TIMEOUT=10
                IOR_TEST_CLEANUP_RESERVE=3
                initialize_runtime_state
                printf synthetic-dump > "$DUMP_PATH"
                NEGATIVE_CASE=checksum-mismatch
                DUMP_SHA256={captured}
                run_selected_negative_case
                status=$?
                cleanup_owned_evidence_dir || exit 60
                exit "$status"
                """
            )
        )
        self.assertEqual(result.returncode, 50, result.stdout + result.stderr)
        self.assertIn("failure_class=integrity", result.stdout)
        self.assertIn("reason=checksum-mismatch", result.stdout)

    def test_partial_state_is_nonzero(self) -> None:
        result = self.run_sourced(
            textwrap.dedent(
                """\
                NEGATIVE_CASE=partial-state
                run_partial_state_sql() { return 1; }
                partial_state_marker_exists() { return 0; }
                run_selected_negative_case
                """
            )
        )
        self.assertEqual(result.returncode, 50, result.stdout + result.stderr)
        self.assertIn("failure_class=integrity", result.stdout)
        self.assertIn("reason=partial-state-detected", result.stdout)

    def test_timeout_still_cleans(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-fake-docker-", dir="/tmp") as tmp:
            fake_bin = Path(tmp)
            calls = fake_bin / "calls"
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    f"""\
                    #!/bin/sh
                    printf '%s\\n' "$*" >> "$IOR_TEST_DOCKER_CALLS"
                    case "$*" in
                      "image inspect --format {{{{.Id}}}} {SOURCE_IMAGE}")
                        printf '%s\\n' {SOURCE_IMAGE_ID!r}
                        ;;
                      "image inspect --format {{{{.Id}}}} {TARGET_IMAGE}")
                        printf '%s\\n' {TARGET_IMAGE_ID!r}
                        ;;
                      "compose version") exit 0 ;;
                      *"config --format json") printf '%s\\n' {valid_rendered_topology_json()!r}; exit 0 ;;
                      *"ps -aq"*) exit 0 ;;
                      *"network ls"*) exit 0 ;;
                      *"volume ls"*) exit 0 ;;
                      *"config --services"*) printf 'source\\ntarget\\n'; exit 0 ;;
                      *" up -d "*) exit 0 ;;
                      *" exec -T source sh -ec "*) exit 1 ;;
                      *" ps -q --status "*) exit 0 ;;
                      *" down --volumes --remove-orphans"*) exit 0 ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            run_id = str(time.time_ns())
            evidence = f"/tmp/hyhome-ior-evidence.{run_id}"
            env = {
                "PATH": f"{fake_bin}:{os.environ['PATH']}",
                "IOR_RUN_ID": run_id,
                "IOR_EVIDENCE_DIR": evidence,
                "IOR_TEST_DOCKER_CALLS": str(calls),
                "IOR_TEST_MODE": "1",
                "IOR_TEST_TOTAL_TIMEOUT": "5",
                "IOR_TEST_CLEANUP_RESERVE": "2",
            }
            result = self.run_sourced(
                textwrap.dedent(
                    """\
                    prepare_default_handoff_dir() { return 0; }
                    invalidate_canonical_handoff() { return 0; }
                    render_and_validate_topology() { return 0; }
                    main --negative-case timeout
                    """
                ),
                extra_env=env,
            )
            call_text = calls.read_text(encoding="utf-8") if calls.exists() else ""
        self.assertEqual(result.returncode, 20, result.stdout + result.stderr)
        self.assertIn("failure_class=readiness", result.stdout)
        self.assertIn("reason=timeout", result.stdout)
        self.assertIn("down --volumes --remove-orphans", call_text)
        self.assertFalse(Path(evidence).exists())

    def test_partial_state_fixture_creates_marker_before_error(self) -> None:
        text = PARTIAL_SQL.read_text(encoding="utf-8")
        create_at = text.index("CREATE TABLE rehearsal_partial_state_marker")
        raise_at = text.index("RAISE EXCEPTION")
        self.assertLess(create_at, raise_at)

    def test_backup_restore_commands_and_cleanup_are_mandatory(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("pg_dump -Fc --no-owner --no-acl", text)
        self.assertIn(
            "pg_restore --clean --if-exists --no-owner --no-acl", text
        )
        self.assertIn("trap on_exit EXIT", text)
        self.assertIn("down --volumes --remove-orphans", text)
        self.assertIn("run_bounded docker compose", text)
        self.assertIn("run_cleanup_bounded docker compose", text)
        self.assertIn('timeout --signal=KILL "${remaining}s"', text)
        self.assertIn('timeout --signal=KILL "${cap}s"', text)
        self.assertIn("run_bounded docker create", text)
        self.assertIn("run_bounded docker wait", text)
        self.assertIn("run_bounded docker cp", text)
        self.assertIn("docker rm -f -v", text)
        self.assertIn("database_readiness_stable()", text)
        self.assertEqual(
            text.count('database_readiness_stable "$SOURCE_PROJECT" source'), 2
        )
        self.assertEqual(
            text.count('database_readiness_stable "$TARGET_PROJECT" target'), 1
        )
        self.assertIn('PGCONNECT_TIMEOUT=1', text)
        self.assertIn('-c "SELECT pg_postmaster_start_time()"', text)
        self.assertIn("run_bounded sleep 2", text)
        self.assertIn("service_is_running_and_healthy", text)
        self.assertNotIn("run --rm --no-deps", text)
        self.assertNotIn("docker logs", text)
        self.assertNotIn('-e PGPASSWORD="$IOR_POSTGRES_PASSWORD"', text)
        self.assertNotIn("docker system prune", text)

    def test_readiness_rejects_changed_postmaster_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-readiness-", dir="/tmp") as tmp:
            counter = Path(tmp) / "counter"
            counter.write_text("0\n", encoding="utf-8")
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    IDENTITY_COUNTER={counter!s}
                    read_database_identity() {{
                      count=$(cat "$IDENTITY_COUNTER")
                      count=$((count + 1))
                      printf '%s\n' "$count" >"$IDENTITY_COUNTER"
                      printf '2026-07-22 00:00:0%s+00\n' "$count"
                    }}
                    run_bounded() {{ return 0; }}
                    service_is_running_and_healthy() {{ return 0; }}
                    if database_readiness_stable source-project source 5432; then
                      exit 70
                    fi
                    read_database_identity() {{
                      printf '2026-07-22 00:00:03+00\n'
                    }}
                    database_readiness_stable source-project source 5432
                    """
                )
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_socket_only_temp_postmaster_never_satisfies_readiness(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-socket-only-", dir="/tmp") as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            calls = root / "calls"
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    printf '%s\n' "$*" >> "$IOR_TEST_DOCKER_CALLS"
                    case "$*" in
                      *" up -d --no-deps source") exit 0 ;;
                      *" exec -T source sh -ec "*" -h 127.0.0.1 -p 5432 "*) exit 1 ;;
                      *" exec -T source sh -ec "*) printf 'socket-temp-identity\n'; exit 0 ;;
                      *" ps -q --status running source") printf '%064d\n' 0; exit 0 ;;
                      *"inspect --format "*) printf 'healthy\n'; exit 0 ;;
                      *" ps -q --status exited source") printf '%064d\n' 0; exit 0 ;;
                      *" down --volumes --remove-orphans") exit 0 ;;
                      *"ps -aq"*|*"network ls"*|*"volume ls"*) exit 0 ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            handoff = root / "recovery-verdict.json"
            handoff.write_text('{"stale":true}\n', encoding="utf-8")
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    PATH={fake_bin!s}:$PATH
                    export PATH
                    IOR_TEST_DOCKER_CALLS={calls!s}
                    export IOR_TEST_DOCKER_CALLS
                    RUN_ID={run_id}
                    SOURCE_PROJECT=source-socket-only
                    TARGET_PROJECT=target-socket-only
                    EVIDENCE_DIR={evidence!s}
                    CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                    DUMP_PATH={evidence!s}/rehearsal.dump
                    SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                    TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                    RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                    RUNTIME_LOG={evidence!s}/runtime.log
                    HANDOFF_DIR={root!s}
                    HANDOFF_PATH={handoff!s}
                    IOR_TEST_MODE=1
                    IOR_TEST_TOTAL_TIMEOUT=10
                    IOR_TEST_CLEANUP_RESERVE=4
                    initialize_runtime_state
                    invalidate_canonical_handoff
                    start_source_and_wait
                    status=$?
                    PUBLISH_ALLOWED=false
                    cleanup_owned_projects_and_tmp || exit 60
                    exit "$status"
                    """
                )
            )
            call_text = calls.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 20, result.stdout + result.stderr)
        self.assertIn("failure_class=readiness", result.stdout)
        self.assertIn("-h 127.0.0.1 -p 5432", call_text)
        self.assertNotIn("seed-apply", call_text)
        self.assertFalse(evidence.exists())
        self.assertFalse(handoff.exists())

    def test_recovery_verdict_schema(self) -> None:
        result = self.run_sourced(
            textwrap.dedent(
                f"""\
                SOURCE_IMAGE={SOURCE_IMAGE!r}
                TARGET_IMAGE={TARGET_IMAGE!r}
                FIXTURE_SHA256={'a' * 64!r}
                DUMP_SHA256={'b' * 64!r}
                BACKUP_SECONDS=1
                RESTORE_SECONDS=2
                build_recovery_verdict_json
                """
            )
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), EXPECTED_VERDICT_KEYS)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            payload["producer_spec"],
            "spec:125-infrastructure-operations-readiness-remediation",
        )
        self.assertEqual(payload["scope"], "synthetic-local")
        self.assertEqual(payload["integrity_status"], "passed")
        self.assertEqual(payload["cleanup_status"], "passed")
        self.assertEqual(payload["redaction_status"], "passed")
        self.assertRegex(payload["fixture_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(payload["dump_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertIsInstance(payload["backup_seconds"], int)
        self.assertIsInstance(payload["restore_seconds"], int)

    def test_stale_canonical_is_invalidated_before_a_run(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-handoff-", dir="/tmp") as tmp:
            handoff = Path(tmp) / "recovery-verdict.json"
            handoff.write_text('{"stale":true}\n', encoding="utf-8")
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    HANDOFF_DIR={Path(tmp)!s}
                    HANDOFF_PATH={handoff!s}
                    invalidate_canonical_handoff
                    test ! -e {handoff!s}
                    """
                )
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cleanup_failure_does_not_publish_canonical(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-cleanup-", dir="/tmp") as tmp:
            root = Path(tmp)
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            handoff = root / "recovery-verdict.json"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    RUN_ID={run_id}
                    EVIDENCE_DIR={evidence!s}
                    CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                    DUMP_PATH={evidence!s}/rehearsal.dump
                    SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                    TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                    RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                    RUNTIME_LOG={evidence!s}/runtime.log
                    HANDOFF_DIR={root!s}
                    HANDOFF_PATH={handoff!s}
                    IOR_TEST_MODE=1
                    IOR_TEST_TOTAL_TIMEOUT=10
                    IOR_TEST_CLEANUP_RESERVE=3
                    initialize_runtime_state
                    PUBLISH_ALLOWED=true
                    CANDIDATE_WRITTEN=true
                    SOURCE_OWNED=true
                    cleanup_one_owned_project() {{ return 60; }}
                    cleanup_owned_projects_and_tmp
                    """
                )
            )
            self.assertFalse(handoff.exists())
            self.assertFalse(evidence.exists())
        self.assertEqual(result.returncode, 60, result.stdout + result.stderr)
        self.assertIn("failure_class=cleanup", result.stdout)

    def test_signal_path_cleans_owned_state_and_leaves_canonical_absent(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-signal-", dir="/tmp") as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            calls = root / "calls"
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    printf '%s\n' "$*" >> "$IOR_TEST_DOCKER_CALLS"
                    case "$*" in
                      *"down --volumes --remove-orphans"*) exit 0 ;;
                      *"ps -aq"*|*"network ls"*|*"volume ls"*) exit 0 ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            handoff = root / "recovery-verdict.json"
            handoff.write_text('{"stale":true}\n', encoding="utf-8")
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    PATH={fake_bin!s}:$PATH
                    export PATH
                    IOR_TEST_DOCKER_CALLS={calls!s}
                    export IOR_TEST_DOCKER_CALLS
                    RUN_ID={run_id}
                    SOURCE_PROJECT=source-signal
                    TARGET_PROJECT=target-signal
                    EVIDENCE_DIR={evidence!s}
                    CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                    DUMP_PATH={evidence!s}/rehearsal.dump
                    SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                    TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                    RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                    RUNTIME_LOG={evidence!s}/runtime.log
                    HANDOFF_DIR={root!s}
                    HANDOFF_PATH={handoff!s}
                    IOR_TEST_MODE=1
                    IOR_TEST_TOTAL_TIMEOUT=10
                    IOR_TEST_CLEANUP_RESERVE=4
                    initialize_runtime_state
                    SOURCE_OWNED=true
                    trap on_exit EXIT
                    on_signal
                    """
                )
            )
            call_text = calls.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 20, result.stdout + result.stderr)
        self.assertIn("down --volumes --remove-orphans", call_text)
        self.assertFalse(evidence.exists())
        self.assertFalse(handoff.exists())

    def test_cleanup_retry_is_idempotent_after_temp_removal(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-retry-", dir="/tmp") as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            calls = root / "calls"
            down_count = root / "down-count"
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    printf '%s\n' "$*" >> "$IOR_TEST_DOCKER_CALLS"
                    case "$*" in
                      *"down --volumes --remove-orphans"*)
                        count=0
                        [ ! -f "$IOR_TEST_DOWN_COUNT" ] || count=$(cat "$IOR_TEST_DOWN_COUNT")
                        count=$((count + 1))
                        printf '%s\n' "$count" > "$IOR_TEST_DOWN_COUNT"
                        [ "$count" -gt 1 ]
                        ;;
                      *"ps -aq"*|*"network ls"*|*"volume ls"*) exit 0 ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            handoff = root / "recovery-verdict.json"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    PATH={fake_bin!s}:$PATH
                    export PATH
                    IOR_TEST_DOCKER_CALLS={calls!s}
                    IOR_TEST_DOWN_COUNT={down_count!s}
                    export IOR_TEST_DOCKER_CALLS IOR_TEST_DOWN_COUNT
                    RUN_ID={run_id}
                    SOURCE_PROJECT=source-retry
                    TARGET_PROJECT=target-retry
                    EVIDENCE_DIR={evidence!s}
                    CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                    DUMP_PATH={evidence!s}/rehearsal.dump
                    SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                    TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                    RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                    RUNTIME_LOG={evidence!s}/runtime.log
                    HANDOFF_DIR={root!s}
                    HANDOFF_PATH={handoff!s}
                    IOR_TEST_MODE=1
                    IOR_TEST_TOTAL_TIMEOUT=10
                    IOR_TEST_CLEANUP_RESERVE=5
                    initialize_runtime_state
                    SOURCE_OWNED=true
                    cleanup_owned_projects_and_tmp
                    first_status=$?
                    test "$first_status" -eq 60
                    test "$EVIDENCE_REMOVED" = true
                    cleanup_owned_projects_and_tmp
                    test "$CLEANUP_COMPLETE" = true
                    test "$SOURCE_OWNED" = false
                    """
                )
            )
            call_text = calls.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(call_text.count("down --volumes --remove-orphans"), 2)
        self.assertGreaterEqual(call_text.count("network ls"), 2)
        self.assertGreaterEqual(call_text.count("volume ls"), 2)
        self.assertFalse(evidence.exists())
        self.assertFalse(handoff.exists())

    def test_docker_query_error_is_not_treated_as_absence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-query-error-", dir="/tmp") as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            calls = root / "calls"
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    printf '%s\n' "$*" >> "$IOR_TEST_DOCKER_CALLS"
                    case "$*" in
                      *"ps -aq"*) exit 71 ;;
                      *"network ls"*|*"volume ls"*) exit 0 ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    PATH={fake_bin!s}:$PATH
                    export PATH
                    IOR_TEST_DOCKER_CALLS={calls!s}
                    export IOR_TEST_DOCKER_CALLS
                    IOR_TEST_MODE=1
                    IOR_TEST_TOTAL_TIMEOUT=10
                    IOR_TEST_CLEANUP_RESERVE=3
                    initialize_deadline_budget
                    query_project_resource_state synthetic operation
                    test "$?" -eq 2
                    """
                )
            )
            call_text = calls.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ps -aq", call_text)
        self.assertIn("network ls", call_text)
        self.assertIn("volume ls", call_text)

    def test_post_cleanup_prepublication_window_has_no_canonical(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-publish-window-", dir="/tmp") as tmp:
            root = Path(tmp)
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            handoff = root / "recovery-verdict.json"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    RUN_ID={run_id}
                    EVIDENCE_DIR={evidence!s}
                    CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                    DUMP_PATH={evidence!s}/rehearsal.dump
                    SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                    TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                    RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                    RUNTIME_LOG={evidence!s}/runtime.log
                    HANDOFF_DIR={root!s}
                    HANDOFF_PATH={handoff!s}
                    IOR_TEST_MODE=1
                    IOR_TEST_TOTAL_TIMEOUT=10
                    IOR_TEST_CLEANUP_RESERVE=3
                    initialize_runtime_state
                    FIXTURE_SHA256={'a' * 64!r}
                    DUMP_SHA256={'b' * 64!r}
                    BACKUP_SECONDS=1
                    RESTORE_SECONDS=2
                    write_recovery_verdict
                    cleanup_owned_projects_and_tmp
                    test "$CLEANUP_COMPLETE" = true
                    test "$EVIDENCE_REMOVED" = true
                    test ! -e "$HANDOFF_PATH"
                    """
                )
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(evidence.exists())
        self.assertFalse(handoff.exists())

    def test_detached_dump_client_nonzero_is_removed(self) -> None:
        result, calls = self._run_dump_client_case("nonzero")
        self.assertEqual(result.returncode, 30, result.stdout + result.stderr)
        self.assertIn("reason=dump-client-nonzero", result.stdout)
        self.assertIn("rm -f -v", calls)

    def test_detached_dump_client_timeout_is_removed(self) -> None:
        result, calls = self._run_dump_client_case("timeout")
        self.assertEqual(result.returncode, 30, result.stdout + result.stderr)
        self.assertIn("reason=dump-client-timeout", result.stdout)
        self.assertIn("rm -f -v", calls)

    def test_target_terminal_state_is_readiness_failure_and_cleans(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ior-target-exit-", dir="/tmp") as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            calls = root / "calls"
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    printf '%s\\n' "$*" >> "$IOR_TEST_DOCKER_CALLS"
                    case "$*" in
                      *" up -d --no-deps target") exit 0 ;;
                      *" exec -T target sh -ec "*) exit 1 ;;
                      *" ps -q --status exited target") printf '%064d\\n' 0; exit 0 ;;
                      *" down --volumes --remove-orphans") exit 0 ;;
                      *"ps -aq"*|*"network ls"*|*"volume ls"*) exit 0 ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            handoff = root / "recovery-verdict.json"
            handoff.write_text('{"stale":true}\n', encoding="utf-8")
            body = textwrap.dedent(
                f"""\
                PATH={fake_bin!s}:$PATH
                export PATH
                IOR_TEST_DOCKER_CALLS={calls!s}
                export IOR_TEST_DOCKER_CALLS
                RUN_ID={run_id}
                SOURCE_PROJECT=source-terminal
                TARGET_PROJECT=target-terminal
                EVIDENCE_DIR={evidence!s}
                CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                DUMP_PATH={evidence!s}/rehearsal.dump
                SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                RUNTIME_LOG={evidence!s}/runtime.log
                HANDOFF_DIR={root!s}
                HANDOFF_PATH={handoff!s}
                IOR_TEST_MODE=1
                IOR_TEST_TOTAL_TIMEOUT=10
                IOR_TEST_CLEANUP_RESERVE=4
                initialize_runtime_state
                invalidate_canonical_handoff
                start_target_and_wait
                status=$?
                PUBLISH_ALLOWED=false
                cleanup_owned_projects_and_tmp || exit 60
                exit "$status"
                """
            )
            result = self.run_sourced(body)
            call_text = calls.read_text(encoding="utf-8")
            self.assertFalse(evidence.exists())
            self.assertFalse(handoff.exists())
        self.assertEqual(result.returncode, 20, result.stdout + result.stderr)
        self.assertIn("failure_class=readiness", result.stdout)
        self.assertIn("reason=target-exited", result.stdout)
        self.assertIn("down --volumes --remove-orphans", call_text)

    def _run_dump_client_case(
        self, case: str
    ) -> tuple[subprocess.CompletedProcess[str], str]:
        with tempfile.TemporaryDirectory(prefix="ior-client-", dir="/tmp") as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            calls = root / "calls"
            run_id = str(time.time_ns())
            evidence = Path(f"/tmp/hyhome-ior-evidence.{run_id}")
            docker = fake_bin / "docker"
            docker.write_text(
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    printf '%s\\n' "$*" >> "$IOR_TEST_DOCKER_CALLS"
                    case "$1" in
                      create) printf '%064d\\n' 0; exit 0 ;;
                      start) exit 0 ;;
                      wait) printf '1\\n'; exit 0 ;;
                      rm) exit 0 ;;
                      *) exit 0 ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
            timeout_override = ""
            if case == "timeout":
                timeout_override = textwrap.dedent(
                    """\
                    run_bounded() {
                      if [ "$1 $2" = "docker wait" ]; then return 124; fi
                      command "$@"
                    }
                    """
                )
            body = textwrap.dedent(
                f"""\
                PATH={fake_bin!s}:$PATH
                export PATH
                IOR_TEST_DOCKER_CALLS={calls!s}
                export IOR_TEST_DOCKER_CALLS
                RUN_ID={run_id}
                EVIDENCE_DIR={evidence!s}
                CANDIDATE_PATH={evidence!s}/recovery-verdict.candidate.json
                DUMP_PATH={evidence!s}/rehearsal.dump
                SOURCE_ORACLE_PATH={evidence!s}/source-oracle.json
                TARGET_ORACLE_PATH={evidence!s}/target-oracle.json
                RENDERED_TOPOLOGY_PATH={evidence!s}/compose-rendered.json
                RUNTIME_LOG={evidence!s}/runtime.log
                IOR_TEST_MODE=1
                IOR_TEST_TOTAL_TIMEOUT=10
                IOR_TEST_CLEANUP_RESERVE=4
                initialize_runtime_state
                {timeout_override}
                dump_custom_format_with_pg18_client
                status=$?
                cleanup_owned_evidence_dir || exit 60
                exit "$status"
                """
            )
            result = self.run_sourced(body)
            call_text = calls.read_text(encoding="utf-8")
        return result, call_text


if __name__ == "__main__":
    unittest.main()
