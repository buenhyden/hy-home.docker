from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/operations/rehearse-sample-service-delivery.sh"
FIXTURES = ROOT / "tests/fixtures/sample-service-delivery"
BASELINE = FIXTURES / "spec126-verdict.baseline.accepted.json"
CANDIDATE = FIXTURES / "spec126-verdict.candidate.accepted.json"
REJECTED = FIXTURES / "spec126-verdict.candidate.rejected.json"
DIGEST_MISMATCH = FIXTURES / "spec126-verdict.candidate.digest-mismatch.json"
COMPOSE = ROOT / "examples/sample-web-service/docker-compose.yml"
OVERRIDE = FIXTURES / "compose.delivery.override.yml"
POLICY = ROOT / "infra/supply-chain.sample-service-policy.json"
READINESS = ROOT / "_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/compose/readiness-verdict.json"
RECOVERY = ROOT / "_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/postgres/recovery-verdict.json"
REAL_BASELINE = ROOT / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json"
REAL_CANDIDATE = ROOT / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json"
REAL_RECORD = ROOT / "_workspace/repo-support/task-2026-07-19-deployment-release-engineering-remediation/delivery/rehearsal-record.json"

VERDICT_KEYS = {
    "schema_version",
    "producer_spec",
    "role",
    "source_revision",
    "image_config_digest",
    "oci_archive_sha256",
    "policy_id",
    "verdict",
    "exception_id",
    "verified_at",
    "redaction_status",
}
RECORD_KEYS = {
    "schema_version",
    "producer_spec",
    "release_rehearsal_id",
    "source_revision",
    "baseline_verdict_ref",
    "candidate_verdict_ref",
    "readiness_verdict_ref",
    "baseline_project",
    "canary_project",
    "promotion_decision",
    "rollback_decision",
    "post_rollback_health",
    "data_impact",
    "recovery_boundary_ref",
    "cleanup_status",
    "remote_non_goals_confirmed",
    "build_context_sha256",
    "policy_id",
    "policy_sha256",
    "baseline_image_config_digest",
    "candidate_image_config_digest",
    "baseline_oci_archive_sha256",
    "candidate_oci_archive_sha256",
    "baseline_verdict_sha256",
    "candidate_verdict_sha256",
    "readiness_verdict_sha256",
    "recovery_boundary_sha256",
    "approval_ref",
    "started_at",
    "completed_at",
    "baseline_result",
    "canary_result",
    "rehearsal_result",
}


class DeliveryRehearsalContractTests(unittest.TestCase):
    maxDiff = None

    def run_cli(
        self,
        *args: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        merged = os.environ.copy()
        if env:
            merged.update(env)
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            cwd=ROOT,
            env=merged,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_sourced(
        self,
        body: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        merged = os.environ.copy()
        merged["DRE_SOURCE_TEST_BOUNDARY"] = "1"
        if env:
            merged.update(env)
        return subprocess.run(
            [
                "bash",
                "-c",
                f"source {SCRIPT!s}\n{body}",
            ],
            cwd=ROOT,
            env=merged,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_payload(self, directory: Path, name: str, mutate) -> Path:
        payload = json.loads(BASELINE.read_text(encoding="utf-8"))
        mutate(payload)
        path = directory / name
        path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def snapshot_path(self, path: Path) -> tuple[object, ...]:
        try:
            info = path.lstat()
        except FileNotFoundError:
            return ("absent",)
        mode = stat.S_IMODE(info.st_mode)
        if stat.S_ISREG(info.st_mode):
            payload = path.read_bytes()
            return ("file", mode, len(payload), hashlib.sha256(payload).hexdigest())
        if stat.S_ISDIR(info.st_mode):
            return ("directory", mode, tuple(sorted(item.name for item in path.iterdir())))
        if stat.S_ISLNK(info.st_mode):
            return ("symlink", mode, os.readlink(path))
        return ("other", mode)

    def render_delivery_compose(
        self, role: str, digest: str, port: int
    ) -> dict[str, object]:
        env = os.environ.copy()
        env.update(
            {
                "DRE_TASK_ID": "2026-07-19-dre",
                "DRE_ROLE": role,
                "DRE_HOST_PORT": str(port),
                "DRE_IMAGE_CONFIG_DIGEST": digest,
            }
        )
        result = subprocess.run(
            [
                "docker",
                "compose",
                "--project-name",
                f"hyhome-dre-20260719-12345-{role}",
                "--file",
                str(COMPOSE),
                "--file",
                str(OVERRIDE),
                "config",
                "--format",
                "json",
            ],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def cleanup_stub_body(
        self,
        call_log: Path,
        *,
        container: str = "",
        network: str = "",
        volume: str = "",
        failure: str = "none",
    ) -> str:
        setup = (
            "TASK_ID=2026-07-19-dre\n"
            "BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline\n"
            "CANARY_PROJECT=hyhome-dre-20260719-12345-canary\n"
            f"DRE_STUB_LOG={call_log!s}\n"
            f"DRE_STUB_CONTAINER={container}\n"
            f"DRE_STUB_NETWORK={network}\n"
            f"DRE_STUB_VOLUME={volume}\n"
            f"DRE_STUB_FAILURE={failure}\n"
        )
        return setup + textwrap.dedent(
            r"""
            dre_cleanup_bounded() {
              local requested="$1"
              shift
              local rendered="$*"
              printf '%s\n' "$rendered" >>"$DRE_STUB_LOG"
              case "$rendered" in
                docker\ ps\ --all*)
                  [[ "$DRE_STUB_FAILURE" != container-query ]] || return 1
                  printf '%s' "$DRE_STUB_CONTAINER"
                  ;;
                docker\ network\ ls*)
                  [[ "$DRE_STUB_FAILURE" != network-query ]] || return 1
                  printf '%s' "$DRE_STUB_NETWORK"
                  ;;
                docker\ volume\ ls*)
                  [[ "$DRE_STUB_FAILURE" != volume-query ]] || return 1
                  printf '%s' "$DRE_STUB_VOLUME"
                  ;;
                docker\ rm\ --force*)
                  [[ "$DRE_STUB_FAILURE" != container-remove ]] || return 1
                  ;;
                docker\ network\ rm*)
                  [[ "$DRE_STUB_FAILURE" != network-remove ]] || return 1
                  ;;
                *) return 99 ;;
              esac
            }
            """
        )

    def run_cleanup_cli_with_inventory(
        self, container_lines: str, network_lines: str
    ) -> tuple[subprocess.CompletedProcess[str], list[str]]:
        with tempfile.TemporaryDirectory() as raw:
            mock = Path(raw)
            call_log = mock / "calls.log"
            docker = mock / "docker"
            docker.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env bash
                    printf '%s\n' "$*" >>"$CLEANUP_CALL_LOG"
                    if [[ "$1 $2" == "ps --all" ]]; then
                      printf '%s' "$CLEANUP_CONTAINER_LINES"
                    elif [[ "$1 $2" == "network ls" ]]; then
                      printf '%s' "$CLEANUP_NETWORK_LINES"
                    elif [[ "$1 $2" == "volume ls" ]]; then
                      exit 0
                    elif [[ "$1 $2" == "rm --force" || "$1 $2" == "network rm" ]]; then
                      exit 0
                    else
                      exit 99
                    fi
                    """
                ),
                encoding="utf-8",
            )
            docker.chmod(0o755)
            result = self.run_cli(
                "cleanup",
                "--task-id",
                "2026-07-19-dre",
                env={
                    "PATH": f"{mock}:{os.environ['PATH']}",
                    "CLEANUP_CALL_LOG": str(call_log),
                    "CLEANUP_CONTAINER_LINES": container_lines,
                    "CLEANUP_NETWORK_LINES": network_lines,
                },
            )
            calls = (
                call_log.read_text(encoding="utf-8").splitlines()
                if call_log.exists()
                else []
            )
        return result, calls

    def test_fixture_verdicts_have_exact_schema(self) -> None:
        for path in (BASELINE, CANDIDATE, REJECTED, DIGEST_MISMATCH):
            with self.subTest(path=path.name):
                self.assertEqual(VERDICT_KEYS, set(json.loads(path.read_text())))

    def test_rejects_fixed_compose_identity(self) -> None:
        compose = COMPOSE.read_text(encoding="utf-8")
        self.assertNotRegex(compose, r"(?m)^name\s*:")
        self.assertNotRegex(compose, r"(?m)^\s+container_name\s*:")
        with tempfile.TemporaryDirectory() as raw:
            fixed = Path(raw) / "docker-compose.yml"
            fixed.write_text(
                "name: fixed-sample-service\n"
                + compose.replace(
                    "  web:\n", "  web:\n    container_name: fixed-sample-service\n"
                ),
                encoding="utf-8",
            )
            result = self.run_sourced(f"validate_compose_contract {fixed!s} {OVERRIDE!s}")
        self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_accepts_project_scopable_compose_contract(self) -> None:
        result = self.run_sourced(
            f"validate_compose_contract {COMPOSE!s} {OVERRIDE!s}"
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_delivery_override_labels_service_and_network_exactly(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        self.assertEqual(1, text.count("build: !reset null"))
        self.assertEqual(1, text.count("pull_policy: never"))
        self.assertEqual(1, text.count("127.0.0.1:${DRE_HOST_PORT"))
        for label in (
            "org.hyhome.delivery.owner:",
            "org.hyhome.delivery.task-id:",
            "org.hyhome.delivery.role:",
        ):
            self.assertEqual(2, text.count(label), label)

    def test_rendered_delivery_topology_is_exact_and_cannot_build_or_pull(self) -> None:
        owner = "task:2026-07-19-deployment-release-engineering-remediation"
        cases = (
            ("baseline", "sha256:" + "1" * 64, 18080),
            ("canary", "sha256:" + "2" * 64, 18081),
        )
        for role, digest, port in cases:
            with self.subTest(role=role):
                rendered = self.render_delivery_compose(role, digest, port)
                service = rendered["services"]["web"]
                network = rendered["networks"]["sample-internal"]
                labels = {
                    "org.hyhome.delivery.owner": owner,
                    "org.hyhome.delivery.task-id": "2026-07-19-dre",
                    "org.hyhome.delivery.role": role,
                }
                self.assertNotIn("build", service)
                self.assertEqual(digest, service["image"])
                self.assertEqual("never", service["pull_policy"])
                self.assertEqual(labels, service["labels"])
                self.assertEqual(labels, network["labels"])
                self.assertEqual({"sample-internal": None}, service["networks"])
                self.assertEqual(
                    [
                        {
                            "mode": "ingress",
                            "host_ip": "127.0.0.1",
                            "target": 8080,
                            "published": str(port),
                            "protocol": "tcp",
                        }
                    ],
                    service["ports"],
                )

    def test_rejects_missing_rejected_or_mismatched_verdict(self) -> None:
        cases = (
            (FIXTURES / "missing.json", "candidate"),
            (REJECTED, "candidate"),
            (DIGEST_MISMATCH, "candidate"),
        )
        for path, role in cases:
            with self.subTest(path=path.name):
                result = self.run_sourced(
                    f"load_and_validate_verdict {role} {path!s}"
                )
                self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_rejects_extra_unknown_verdict_field(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = self.write_payload(Path(raw), "extra.json", lambda p: p.update(extra=True))
            result = self.run_sourced(f"load_and_validate_verdict baseline {path!s}")
        self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_rejects_equal_baseline_candidate_subjects(self) -> None:
        result = self.run_sourced(
            f"load_and_validate_verdict baseline {BASELINE!s}\n"
            f"load_and_validate_verdict candidate {BASELINE!s}\n"
            "VERDICT_ROLE[candidate]=candidate\n"
            "assert_distinct_subjects_and_same_revision"
        )
        self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_requires_same_source_revision(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
            candidate["source_revision"] = "f" * 40
            path = Path(raw) / "candidate.json"
            path.write_text(json.dumps(candidate, sort_keys=True) + "\n", encoding="utf-8")
            result = self.run_sourced(
                f"load_and_validate_verdict baseline {BASELINE!s}\n"
                f"load_and_validate_verdict candidate {path!s}\n"
                "assert_distinct_subjects_and_same_revision"
            )
        self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_requires_distinct_archive_subjects(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
            candidate["oci_archive_sha256"] = json.loads(
                BASELINE.read_text(encoding="utf-8")
            )["oci_archive_sha256"]
            path = Path(raw) / "candidate.json"
            path.write_text(json.dumps(candidate, sort_keys=True) + "\n", encoding="utf-8")
            result = self.run_sourced(
                f"load_and_validate_verdict baseline {BASELINE!s}\n"
                f"load_and_validate_verdict candidate {path!s}\n"
                "assert_distinct_subjects_and_same_revision"
            )
        self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_rejects_wrong_verdict_scalar_types(self) -> None:
        for field, value in (
            ("schema_version", True),
            ("exception_id", ""),
            ("redaction_status", True),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as raw:
                path = self.write_payload(
                    Path(raw), "wrong-type.json", lambda p: p.update({field: value})
                )
                result = self.run_sourced(
                    f"load_and_validate_verdict baseline {path!s}"
                )
                self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_accepts_current_spec126_verdict_schema_and_binds_pair_context(self) -> None:
        build_context = "sha256:" + "e" * 64
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            paths: dict[str, Path] = {}
            for role, source in (("baseline", BASELINE), ("candidate", CANDIDATE)):
                payload = json.loads(source.read_text(encoding="utf-8"))
                payload["build_context_sha256"] = build_context
                paths[role] = root / f"{role}.json"
                paths[role].write_text(
                    json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8"
                )
            result = self.run_sourced(
                f"load_and_validate_verdict baseline {paths['baseline']!s} || exit $?\n"
                f"load_and_validate_verdict candidate {paths['candidate']!s} || exit $?\n"
                "assert_distinct_subjects_and_same_revision || exit $?\n"
                "printf '%s|%s\\n' \"$BUILD_CONTEXT_SHA256\" \"$POLICY_ID\""
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            f"{build_context}|sample-service-local-v1\n", result.stdout
        )

    def test_snapshot_revalidation_rejects_content_and_identity_drift(self) -> None:
        for mutation, command, expected_code in (
            (
                "content",
                'printf "\\n" >>"$CANDIDATE_VERDICT_PATH"',
                "input-snapshot-drift",
            ),
            (
                "identity",
                'cp -- "$DRE_READINESS_PATH" "$DRE_READINESS_PATH.replacement"\n'
                'mv -- "$DRE_READINESS_PATH.replacement" "$DRE_READINESS_PATH"',
                "input-snapshot-identity-drift",
            ),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                inputs = {
                    "baseline.json": BASELINE,
                    "candidate.json": CANDIDATE,
                    "readiness.json": READINESS,
                    "recovery.json": RECOVERY,
                    "policy.json": POLICY,
                    "compose.yml": COMPOSE,
                    "override.yml": OVERRIDE,
                }
                for name, source in inputs.items():
                    shutil.copy2(source, root / name)
                result = self.run_sourced(
                    textwrap.dedent(
                        f"""\
                        BASELINE_VERDICT_PATH={root / 'baseline.json'!s}
                        CANDIDATE_VERDICT_PATH={root / 'candidate.json'!s}
                        DRE_READINESS_PATH={root / 'readiness.json'!s}
                        DRE_RECOVERY_PATH={root / 'recovery.json'!s}
                        DRE_POLICY_PATH={root / 'policy.json'!s}
                        DRE_COMPOSE_PATH={root / 'compose.yml'!s}
                        DRE_OVERRIDE_PATH={root / 'override.yml'!s}
                        capture_delivery_input_snapshots || exit $?
                        {command}
                        revalidate_delivery_input_snapshots 40
                        """
                    )
                )
            self.assertEqual(40, result.returncode, result.stdout + result.stderr)
            self.assertIn(expected_code, result.stderr)

    def test_publication_revalidates_inputs_immediately_before_schema_and_write(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        publication = text.split("publish_rehearsal_record() {", 1)[1].split(
            "\ndre_operation_bounded()", 1
        )[0]
        self.assertIn("revalidate_delivery_input_snapshots", publication)
        revalidate = publication.index("revalidate_delivery_input_snapshots")
        validate_schema = publication.index('dre_python_json "${CANDIDATE_JSON:-}"')
        write_record = publication.index('record_dir="$(dirname -- "$record_path")"')
        self.assertLess(revalidate, validate_schema)
        self.assertLess(revalidate, write_record)

    def test_rejects_remote_image_reference(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = self.write_payload(
                Path(raw),
                "remote.json",
                lambda p: p.update(
                    image_config_digest="ghcr.io/example/service@sha256:" + "1" * 64
                ),
            )
            result = self.run_sourced(f"load_and_validate_verdict baseline {path!s}")
        self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_local_image_objects_are_exactly_inspected_before_start(self) -> None:
        baseline_digest = "sha256:" + "1" * 64
        candidate_digest = "sha256:" + "2" * 64
        with tempfile.TemporaryDirectory() as raw:
            call_log = Path(raw) / "calls.log"
            result = self.run_sourced(
                textwrap.dedent(
                    f"""\
                    VERDICT_IMAGE_CONFIG_DIGEST[baseline]={baseline_digest}
                    VERDICT_IMAGE_CONFIG_DIGEST[candidate]={candidate_digest}
                    DRE_OPERATION_DEADLINE=$((SECONDS + 30))
                    dre_operation_bounded() {{
                      local requested="$1"
                      shift
                      printf '%s\n' "$*" >>{call_log!s}
                      printf '%s\n' "${{@: -1}}"
                    }}
                    validate_local_image_objects
                    """
                )
            )
            calls = (
                call_log.read_text(encoding="utf-8").splitlines()
                if call_log.exists()
                else []
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(2, len(calls))
        for digest, call in zip((baseline_digest, candidate_digest), calls):
            self.assertEqual(
                f"docker image inspect --format {{{{.Id}}}} {digest}", call
            )

        script = SCRIPT.read_text(encoding="utf-8")
        rehearsal = script.split("dre_rehearse() {", 1)[1].split(
            "\ndre_cleanup_command()", 1
        )[0]
        self.assertLess(
            rehearsal.index("validate_local_image_objects"),
            rehearsal.index("start_baseline"),
        )

    def test_local_image_object_rejects_missing_mismatch_or_multiple_ids(self) -> None:
        digest = "sha256:" + "1" * 64
        cases = {
            "missing": "return 1",
            "mismatch": "printf '%s\\n' 'sha256:" + "2" * 64 + "'",
            "multiple": f"printf '%s\\n%s\\n' '{digest}' '{digest}'",
        }
        for name, response in cases.items():
            with self.subTest(name=name):
                result = self.run_sourced(
                    textwrap.dedent(
                        f"""\
                        DRE_OPERATION_DEADLINE=$((SECONDS + 30))
                        dre_operation_bounded() {{ {response}; }}
                        validate_local_image_object baseline {digest}
                        """
                    )
                )
                self.assertEqual(10, result.returncode, result.stdout + result.stderr)

    def test_start_commands_deny_pull_and_build(self) -> None:
        digest = "sha256:" + "1" * 64
        result = self.run_sourced(
            textwrap.dedent(
                f"""\
                TASK_ID=2026-07-19-dre
                BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline
                CANARY_PROJECT=hyhome-dre-20260719-12345-canary
                VERDICT_IMAGE_CONFIG_DIGEST[baseline]={digest}
                dre_timeout() {{ printf '%s\n' "$*"; }}
                start_baseline
                """
            )
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(" up -d --pull never --no-build --remove-orphans", result.stdout)

    def test_health_requires_container_and_http_marker(self) -> None:
        accepted = self.run_sourced("health_observation_is_accepted healthy 200 present")
        self.assertEqual(0, accepted.returncode, accepted.stdout + accepted.stderr)
        for values in (
            "starting 200 present",
            "healthy 503 present",
            "healthy 200 absent",
        ):
            with self.subTest(values=values):
                rejected = self.run_sourced(f"health_observation_is_accepted {values}")
                self.assertNotEqual(0, rejected.returncode)

    def test_promotion_record_requires_all_gates(self) -> None:
        result = self.run_sourced(
            "PROMOTION_GATES_COMPLETE=false\nrecord_promotion_decision"
        )
        self.assertEqual(40, result.returncode, result.stdout + result.stderr)

    def test_failure_mode_rolls_back_previous_digest(self) -> None:
        forced = self.run_sourced(
            "FAILURE_MODE=canary-health-timeout\n"
            "inject_canary_timeout_when_requested\n"
            '[[ "$CANARY_HEALTH_FORCED_TIMEOUT" == true ]]'
        )
        self.assertEqual(0, forced.returncode, forced.stdout + forced.stderr)
        normal = self.run_sourced(
            "FAILURE_MODE=none\n"
            "inject_canary_timeout_when_requested\n"
            '[[ "$CANARY_HEALTH_FORCED_TIMEOUT" == false ]]'
        )
        self.assertEqual(0, normal.returncode, normal.stdout + normal.stderr)
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("CANARY_HEALTH_FORCED_TIMEOUT", text)
        negative = text.index("inject_canary_timeout_when_requested")
        rollback = text.index("rollback_to_baseline_digest", negative)
        post_health = text.index("verify_post_rollback_health", rollback)
        cleanup = text.index("cleanup_owned_projects", post_health)
        self.assertLess(negative, rollback)
        self.assertLess(rollback, post_health)
        self.assertLess(post_health, cleanup)

    def test_cleanup_accepts_only_owned_projects(self) -> None:
        good = self.run_sourced(
            "BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline\n"
            "CANARY_PROJECT=hyhome-dre-20260719-12345-canary\n"
            "assert_owned_project_names"
        )
        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        bad = self.run_sourced(
            "BASELINE_PROJECT=sample-web-service\n"
            "CANARY_PROJECT=hyhome-dre-20260719-12345-canary\n"
            "assert_owned_project_names"
        )
        self.assertEqual(10, bad.returncode, bad.stdout + bad.stderr)

        wrong_date = self.run_sourced(
            "BASELINE_PROJECT=hyhome-dre-20260720-12345-baseline\n"
            "CANARY_PROJECT=hyhome-dre-20260720-12345-canary\n"
            "assert_owned_project_names"
        )
        self.assertEqual(10, wrong_date.returncode, wrong_date.stdout + wrong_date.stderr)

    def test_in_process_cleanup_handles_exact_partial_owned_states(self) -> None:
        cases = (
            ("container", {"container": "container-id"}, ["docker rm --force container-id"]),
            ("network", {"network": "network-id"}, ["docker network rm network-id"]),
        )
        for name, resources, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as raw:
                call_log = Path(raw) / "calls.log"
                body = self.cleanup_stub_body(call_log, **resources)
                result = self.run_sourced(
                    body + 'dre_cleanup_one_project "$BASELINE_PROJECT"\n'
                )
                calls = call_log.read_text(encoding="utf-8").splitlines()
                destructive = [
                    call
                    for call in calls
                    if call.startswith(("docker rm ", "docker network rm "))
                    or "docker compose" in call
                ]
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(expected, destructive)

    def test_cleanup_query_and_remove_errors_are_stable_class60(self) -> None:
        cases = (
            ("container-query", {}, []),
            ("network-query", {}, []),
            ("volume-query", {}, []),
            (
                "container-remove",
                {"container": "container-id"},
                ["docker rm --force container-id"],
            ),
            (
                "network-remove",
                {"network": "network-id"},
                ["docker network rm network-id"],
            ),
        )
        for failure, resources, expected in cases:
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as raw:
                call_log = Path(raw) / "calls.log"
                body = self.cleanup_stub_body(call_log, failure=failure, **resources)
                result = self.run_sourced(
                    body + 'dre_cleanup_one_project "$BASELINE_PROJECT"\n'
                )
                calls = call_log.read_text(encoding="utf-8").splitlines()
                destructive = [
                    call
                    for call in calls
                    if call.startswith(("docker rm ", "docker network rm "))
                    or "docker compose" in call
                ]
            self.assertEqual(60, result.returncode, result.stdout + result.stderr)
            self.assertEqual(expected, destructive)

    def test_rollback_cleanup_error_is_stable_class50(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            call_log = Path(raw) / "calls.log"
            body = self.cleanup_stub_body(
                call_log,
                container="container-id",
                failure="container-remove",
            )
            result = self.run_sourced(body + "rollback_to_baseline_digest\n")
            calls = call_log.read_text(encoding="utf-8").splitlines()
        self.assertEqual(50, result.returncode, result.stdout + result.stderr)
        self.assertIn("docker rm --force container-id", calls)

    def test_standalone_cleanup_rejects_absent_or_invalid_project_pairs(self) -> None:
        cases = (
            ("absent", "", ""),
            (
                "incomplete",
                "hyhome-dre-20260719-12345-baseline|baseline",
                "",
            ),
            (
                "additional",
                "hyhome-dre-20260719-12345-baseline|baseline\n"
                "hyhome-dre-20260719-54321-baseline|baseline",
                "hyhome-dre-20260719-12345-canary|canary",
            ),
            (
                "nonmatching",
                "hyhome-dre-20260719-12345-baseline|baseline",
                "hyhome-dre-20260719-54321-canary|canary",
            ),
        )
        for name, container_lines, network_lines in cases:
            with self.subTest(name=name):
                result, calls = self.run_cleanup_cli_with_inventory(
                    container_lines, network_lines
                )
                destructive = [
                    call
                    for call in calls
                    if call.startswith(("rm ", "network rm ", "compose "))
                ]
                self.assertEqual(60, result.returncode, result.stdout + result.stderr)
                self.assertEqual([], destructive)

    def test_runtime_stage_failures_use_stable_classes(self) -> None:
        baseline = self.run_sourced(
            "TASK_ID=2026-07-19-dre\n"
            "BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline\n"
            "CANARY_PROJECT=hyhome-dre-20260719-12345-canary\n"
            "VERDICT_IMAGE_CONFIG_DIGEST[baseline]=sha256:" + "1" * 64 + "\n"
            "dre_compose() { return 99; }\n"
            "start_baseline"
        )
        self.assertEqual(20, baseline.returncode, baseline.stdout + baseline.stderr)

        rollback = self.run_sourced(
            "BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline\n"
            "CANARY_PROJECT=hyhome-dre-20260719-12345-canary\n"
            "dre_compose() { return 99; }\n"
            "rollback_to_baseline_digest"
        )
        self.assertEqual(50, rollback.returncode, rollback.stdout + rollback.stderr)

        cleanup = self.run_sourced(
            "BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline\n"
            "CANARY_PROJECT=hyhome-dre-20260719-12345-canary\n"
            "dre_cleanup_one_project() { return 99; }\n"
            "cleanup_owned_projects"
        )
        self.assertEqual(60, cleanup.returncode, cleanup.stdout + cleanup.stderr)

    def test_rehearsal_record_schema(self) -> None:
        result = self.run_sourced(
            textwrap.dedent(
                """\
                SOURCE_REVISION=0123456789abcdef0123456789abcdef01234567
                BASELINE_VERDICT_PATH=/tmp/verification-verdict.baseline.json
                CANDIDATE_VERDICT_PATH=/tmp/verification-verdict.candidate.json
                BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline
                CANARY_PROJECT=hyhome-dre-20260719-12345-canary
                PROMOTION_DECISION=promoted
                ROLLBACK_DECISION=not_required
                POST_ROLLBACK_HEALTH=not_applicable
                CLEANUP_COMPLETE=true
                build_rehearsal_record_json
                """
            )
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(RECORD_KEYS, set(payload))
        self.assertEqual(1, payload["schema_version"])
        self.assertEqual(
            "spec:127-deployment-release-engineering-remediation",
            payload["producer_spec"],
        )
        self.assertEqual("none", payload["data_impact"])
        self.assertTrue(payload["remote_non_goals_confirmed"])
        self.assertEqual(
            "local-rehearsal-20260719-0123456789ab",
            payload["release_rehearsal_id"],
        )
        self.assertEqual(
            "verification-verdict.baseline.json", payload["baseline_verdict_ref"]
        )
        self.assertEqual(
            "verification-verdict.candidate.json", payload["candidate_verdict_ref"]
        )
        self.assertEqual("readiness-verdict.json", payload["readiness_verdict_ref"])
        self.assertEqual("recovery-verdict.json", payload["recovery_boundary_ref"])

    def test_publication_is_atomic_mode_0600_and_only_after_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as raw:
            root = Path(raw)
            record = root / "rehearsal-record.json"
            invalid_body = textwrap.dedent(
                f"""\
                REHEARSAL_RECORD_PATH={record!s}
                CANDIDATE_JSON='{{"schema_version":1}}'
                CLEANUP_COMPLETE=true
                publish_rehearsal_record
                """
            )
            failed = self.run_sourced(invalid_body)
            self.assertEqual(40, failed.returncode, failed.stdout + failed.stderr)
            self.assertFalse(record.exists())
            body = textwrap.dedent(
                f"""\
                REHEARSAL_RECORD_PATH={record!s}
                SOURCE_REVISION=0123456789abcdef0123456789abcdef01234567
                BASELINE_VERDICT_PATH=/tmp/verification-verdict.baseline.json
                CANDIDATE_VERDICT_PATH=/tmp/verification-verdict.candidate.json
                BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline
                CANARY_PROJECT=hyhome-dre-20260719-12345-canary
                PROMOTION_DECISION=promoted
                ROLLBACK_DECISION=not_required
                POST_ROLLBACK_HEALTH=not_applicable
                CLEANUP_COMPLETE=true
                CANDIDATE_JSON="$(build_rehearsal_record_json)"
                publish_rehearsal_record
                """
            )
            passed = self.run_sourced(body)
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
            self.assertEqual(0o600, stat.S_IMODE(record.stat().st_mode))
            self.assertFalse(any(root.glob(".rehearsal-record.*")))

    def test_publication_uses_stable_nofollow_parent_directory_fd(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")
        publication = script.split("publish_rehearsal_record() {", 1)[1].split(
            "\ndre_operation_bounded()", 1
        )[0]
        self.assertIn("parent_fd = os.open(parent, flags)", publication)
        self.assertIn("dir_fd=parent_fd", publication)
        self.assertIn("src_dir_fd=parent_fd", publication)
        self.assertIn("dst_dir_fd=parent_fd", publication)
        self.assertIn("os.O_NOFOLLOW", publication)
        self.assertNotIn("os.replace(temporary, target)", publication)

    def test_readiness_requires_exact_passing_schema_and_cleanup(self) -> None:
        canonical = ROOT / "_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/compose/readiness-verdict.json"
        result = self.run_sourced(f"validate_readiness_verdict {canonical!s}")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        with tempfile.TemporaryDirectory() as raw:
            payload = json.loads(canonical.read_text(encoding="utf-8"))
            payload["cleanup_status"] = "failed"
            path = Path(raw) / "readiness.json"
            path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
            os.chmod(path, 0o600)
            rejected = self.run_sourced(f"validate_readiness_verdict {path!s}")
        self.assertEqual(10, rejected.returncode, rejected.stdout + rejected.stderr)

    def test_recovery_requires_exact_synthetic_boundary_schema(self) -> None:
        canonical = ROOT / "_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/postgres/recovery-verdict.json"
        result = self.run_sourced(f"validate_recovery_boundary {canonical!s}")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        with tempfile.TemporaryDirectory() as raw:
            payload = json.loads(canonical.read_text(encoding="utf-8"))
            payload["scope"] = "production"
            path = Path(raw) / "recovery.json"
            path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
            os.chmod(path, 0o600)
            rejected = self.run_sourced(f"validate_recovery_boundary {path!s}")
        self.assertEqual(10, rejected.returncode, rejected.stdout + rejected.stderr)

    def test_strict_cli_and_failure_modes(self) -> None:
        for args, expected in (
            ((), 2),
            (("unknown",), 2),
            (("cleanup", "--task-id", "../bad"), 2),
            (("rehearse", "--task-id", "ok", "--failure-mode", "other"), 2),
            (
                (
                    "preflight",
                    "--baseline-verdict",
                    str(BASELINE.relative_to(ROOT)),
                    "--task-id",
                    "2026-07-19-dre",
                    "--candidate-verdict",
                    str(CANDIDATE.relative_to(ROOT)),
                ),
                2,
            ),
            (
                (
                    "rehearse",
                    "--task-id",
                    "2026-07-19-dre",
                    "--baseline-verdict",
                    str(BASELINE.relative_to(ROOT)),
                    "--candidate-verdict",
                    str(CANDIDATE.relative_to(ROOT)),
                    "--failure-mode",
                    "none",
                ),
                2,
            ),
        ):
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(expected, result.returncode, result.stdout + result.stderr)

    def test_fixture_preflight_is_contract_only_and_never_calls_docker(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            mock = Path(raw)
            call_log = mock / "calls.log"
            docker = mock / "docker"
            docker.write_text(
                "#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >>\"$DRE_CALL_LOG\"\nexit 99\n",
                encoding="utf-8",
            )
            docker.chmod(0o755)
            result = self.run_cli(
                "preflight",
                "--task-id",
                "2026-07-19-dre",
                "--baseline-verdict",
                str(BASELINE.relative_to(ROOT)),
                "--candidate-verdict",
                str(CANDIDATE.relative_to(ROOT)),
                env={"PATH": f"{mock}:{os.environ['PATH']}", "DRE_CALL_LOG": str(call_log)},
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("evidence=fixture-contract-only", result.stdout)
            self.assertIn("readiness=passed", result.stdout)
            self.assertIn("recovery_boundary=passed", result.stdout)
            self.assertIn("compose=passed", result.stdout)
            self.assertIn("ports=18080,18081", result.stdout)
            self.assertFalse(call_log.exists())

    def test_canonical_absence_fails_class10_before_docker_or_evidence(self) -> None:
        self.assertFalse(REAL_BASELINE.exists())
        self.assertFalse(REAL_CANDIDATE.exists())
        directory_before = self.snapshot_path(REAL_RECORD.parent)
        record_before = self.snapshot_path(REAL_RECORD)
        with tempfile.TemporaryDirectory() as raw:
            mock = Path(raw)
            call_log = mock / "calls.log"
            docker = mock / "docker"
            docker.write_text(
                "#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >>\"$DRE_CALL_LOG\"\nexit 99\n",
                encoding="utf-8",
            )
            docker.chmod(0o755)
            result = self.run_cli(
                "rehearse",
                "--task-id",
                "2026-07-19-dre",
                "--baseline-verdict",
                str(REAL_BASELINE.relative_to(ROOT)),
                "--candidate-verdict",
                str(REAL_CANDIDATE.relative_to(ROOT)),
                "--failure-mode",
                "none",
                env={"PATH": f"{mock}:{os.environ['PATH']}", "DRE_CALL_LOG": str(call_log)},
            )
            self.assertEqual(10, result.returncode, result.stdout + result.stderr)
            self.assertIn("class=10", result.stderr)
            self.assertFalse(call_log.exists())
        self.assertEqual(record_before, self.snapshot_path(REAL_RECORD))
        self.assertEqual(directory_before, self.snapshot_path(REAL_RECORD.parent))

    def test_test_suite_has_no_real_canonical_mutator(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        self.assertNotIn("REAL_RECORD." + "unlink()", source)
        self.assertNotIn("REAL_RECORD.parent." + "rmdir()", source)

    def test_direct_execution_rejects_test_controls_before_docker(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            mock = Path(raw)
            call_log = mock / "calls.log"
            docker = mock / "docker"
            docker.write_text(
                "#!/usr/bin/env bash\nprintf called >>\"$DRE_TEST_DOCKER_CALL_LOG\"\nexit 99\n",
                encoding="utf-8",
            )
            docker.chmod(0o755)
            result = self.run_cli(
                "preflight",
                "--task-id",
                "2026-07-19-dre",
                "--baseline-verdict",
                str(BASELINE.relative_to(ROOT)),
                "--candidate-verdict",
                str(CANDIDATE.relative_to(ROOT)),
                env={
                    "PATH": f"{mock}:{os.environ['PATH']}",
                    "DRE_TEST_DOCKER_CALL_LOG": str(call_log),
                },
            )
            self.assertEqual(10, result.returncode, result.stdout + result.stderr)
            self.assertFalse(call_log.exists())

            redirected = self.run_cli(
                "preflight",
                "--task-id",
                "2026-07-19-dre",
                "--baseline-verdict",
                str(BASELINE.relative_to(ROOT)),
                "--candidate-verdict",
                str(CANDIDATE.relative_to(ROOT)),
                env={"REHEARSAL_RECORD_PATH": str(mock / "redirected-record.json")},
            )
            self.assertEqual(
                10, redirected.returncode, redirected.stdout + redirected.stderr
            )
            self.assertIn("direct-test-control-rejected", redirected.stderr)
            self.assertFalse((mock / "redirected-record.json").exists())

    def test_required_wrapper_symbols_and_order_are_present(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        symbols = (
            "parse_subcommand",
            "load_and_validate_verdict",
            "assert_distinct_subjects_and_same_revision",
            "validate_local_image_object",
            "validate_local_image_objects",
            "assert_ports_and_owned_project_names",
            "start_baseline",
            "wait_container_and_http_health",
            "start_canary",
            "record_promotion_decision",
            "inject_canary_timeout_when_requested",
            "rollback_to_baseline_digest",
            "verify_post_rollback_health",
            "write_rehearsal_record",
            "cleanup_owned_projects",
        )
        missing = [symbol for symbol in symbols if f"{symbol}()" not in text]
        self.assertEqual([], missing)
        positions = [text.index(f"{symbol}()") for symbol in symbols]
        self.assertEqual(sorted(positions), positions)

    def test_rollback_verifies_previous_digest_and_exact_marker(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("verify_baseline_previous_digest", text)
        self.assertIn("<h1>sample-web-service</h1>", text)

    def test_record_contains_no_raw_body_log_or_secret_fields(self) -> None:
        result = self.run_sourced(
            textwrap.dedent(
                """\
                SOURCE_REVISION=0123456789abcdef0123456789abcdef01234567
                BASELINE_VERDICT_PATH=/tmp/verification-verdict.baseline.json
                CANDIDATE_VERDICT_PATH=/tmp/verification-verdict.candidate.json
                BASELINE_PROJECT=hyhome-dre-20260719-12345-baseline
                CANARY_PROJECT=hyhome-dre-20260719-12345-canary
                PROMOTION_DECISION=not_promoted
                ROLLBACK_DECISION=rolled_back_to_baseline
                POST_ROLLBACK_HEALTH=passed
                CLEANUP_COMPLETE=true
                build_rehearsal_record_json
                """
            )
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        serialized = result.stdout.lower()
        for forbidden in ("body", "log", "secret", "credential", "token"):
            self.assertNotIn(forbidden, serialized)

    def test_docker_http_and_sleep_calls_are_bounded(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("DRE_TOTAL_TIMEOUT_SECONDS=180", text)
        self.assertIn("DRE_CLEANUP_RESERVE_SECONDS=30", text)
        self.assertIn("dre_operation_bounded()", text)
        self.assertIn("dre_cleanup_bounded()", text)
        self.assertIn("DRE_RUN_DEADLINE", text)
        self.assertIn("DRE_OPERATION_DEADLINE", text)
        self.assertNotIn("docker system prune", text)
        self.assertNotIn("docker container prune", text)
        self.assertNotIn("curl http", text)
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("docker ", "curl ", "sleep ")):
                self.fail(f"unbounded external call: {stripped}")


if __name__ == "__main__":
    unittest.main()
