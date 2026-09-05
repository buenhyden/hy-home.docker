"""Wrapper, scenario, and example contracts for Compose core readiness."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.lib.ops._support import (
    EXPECTED_IMAGES,
    EXPECTED_PORTS,
    EXPECTED_SERVICES,
    LIBRARY,
    OVERRIDE,
    ROOT,
    RUNNER,
)
from tests.lib.ops.test_compose_core_readiness import ComposeCoreReadinessHarness


class ComposeCoreReadinessContractTests(ComposeCoreReadinessHarness, unittest.TestCase):
    maxDiff = None

    def run_stubbed_scenario(
        self,
        scenario: str,
        evidence_dir: Path,
        *,
        fail_at: str = "",
        service_state: str = "healthy",
    ) -> subprocess.CompletedProcess[str]:
        runtime_dir = evidence_dir.parent / "runtime"
        shell = f"""
source {RUNNER!s}
assert_linked_worktree() {{ CRR_ROOT={evidence_dir.parent!s}; }}
allocate_runtime_identity() {{
  CRR_PROJECT_NAME=hyhome-crr-20260719-12345-abcd1234
  CRR_RUNTIME_DIR={runtime_dir!s}
  mkdir -p "$CRR_RUNTIME_DIR"
}}
prepare_owned_paths() {{
  CRR_TASK_ROOT={evidence_dir.parent!s}
  CRR_EVIDENCE_DIR={evidence_dir!s}
  CRR_SECRET_DIR="$CRR_RUNTIME_DIR/secrets"
  CRR_CONFIG_DIR="$CRR_RUNTIME_DIR/config"
  CRR_SERVICES_JSON="$CRR_RUNTIME_DIR/services.json"
  CRR_ENDPOINTS_JSON="$CRR_RUNTIME_DIR/endpoints.json"
  CRR_VERDICT_PATH="$CRR_EVIDENCE_DIR/readiness-verdict.json"
  mkdir -p "$CRR_EVIDENCE_DIR" "$CRR_SECRET_DIR" "$CRR_CONFIG_DIR"
}}
fail_positive_precheck() {{
  [ ! -e "$CRR_VERDICT_PATH" ] || return 99
  return 10
}}
assert_docker_compose() {{
  [ {fail_at!r} != dependency ] || fail_positive_precheck
}}
prepare_synthetic_secrets() {{ [ {fail_at!r} != secrets ] || return 10; }}
render_core_model() {{
  if [ {fail_at!r} = render ]; then
    fail_positive_precheck
  fi
}}
assert_docker_daemon() {{
  [ {fail_at!r} != daemon ] || fail_positive_precheck
}}
assert_local_image_identities() {{
  [ {fail_at!r} != images ] || fail_positive_precheck
}}
assert_target_capacity() {{
  [ {fail_at!r} != capacity ] || fail_positive_precheck
}}
start_vault() {{ [ {fail_at!r} != startup ] || return 20; }}
initialize_unseal_and_configure_synthetic_vault() {{ :; }}
prepare_vault_agent_output_volume() {{ :; }}
start_remaining_services() {{ :; }}
collect_service_states() {{
  printf '%s\n' '{{
    "keycloak": {{"container": "{service_state}"}},
    "oauth2-proxy": {{"container": "healthy"}},
    "traefik": {{"container": "healthy"}},
    "vault": {{"container": "healthy"}},
    "vault-agent": {{"container": "healthy"}}
  }}' >"$CRR_SERVICES_JSON"
}}
probe_all_service_endpoints() {{
  printf '%s\n' '{{"all-endpoints": "passed"}}' >"$CRR_ENDPOINTS_JSON"
}}
probe_service_endpoint() {{ return 1; }}
recover_vault_after_restart() {{ [ {fail_at!r} != recovery ] || return 40; }}
cleanup_owned_project() {{ CRR_CLEANUP_DONE=true; return 0; }}
cleanup_runtime_material() {{ :; }}
main --scenario {scenario}
"""
        return subprocess.run(
            ["bash", "-c", shell],
            cwd=ROOT,
            env=os.environ.copy(),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_successful_endpoints_cannot_publish_ready_with_unhealthy_service(
        self,
    ) -> None:
        expected_exit = {
            "startup-readiness": 30,
            "vault-restart-recovery": 40,
        }
        for scenario, exit_code in expected_exit.items():
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as raw:
                evidence = Path(raw) / "evidence"
                result = self.run_stubbed_scenario(
                    scenario,
                    evidence,
                    service_state="unhealthy",
                )
                self.assertEqual(
                    exit_code,
                    result.returncode,
                    result.stdout + result.stderr,
                )
                self.assertFalse((evidence / "readiness-verdict.json").exists())
                verdict = json.loads(
                    (evidence / f"readiness-verdict.{scenario}.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual("failed", verdict["overall_status"])

    def test_runtime_identity_is_collision_resistant_and_symlink_safe(self) -> None:
        wrapper = (
            ROOT / "scripts/operations/check-compose-core-readiness.sh"
        ).read_text(encoding="utf-8")
        self.assertIn("allocate_runtime_identity", wrapper)
        self.assertNotIn('CRR_PROJECT_NAME="${CRR_PROJECT_PREFIX}$$"', wrapper)

        with tempfile.TemporaryDirectory() as fake_root_raw:
            fake_root = Path(fake_root_raw)
            task_root = (
                fake_root / "_workspace/repo-support/"
                "task-2026-07-19-compose-runtime-readiness-remediation"
            )
            task_root.mkdir(parents=True)
            outside = fake_root / "outside"
            outside.mkdir()
            project = f"hyhome-crr-20260719-{os.getpid()}-symlink1"
            runtime = Path("/tmp") / project
            shutil.rmtree(runtime, ignore_errors=True)
            runtime.mkdir(mode=0o700)
            (runtime / "secrets").symlink_to(outside, target_is_directory=True)
            try:
                result = self.run_library(
                    "prepare_owned_paths",
                    env={"CRR_ROOT": str(fake_root), "CRR_PROJECT_NAME": project},
                )
                self.assertEqual(10, result.returncode)
                self.assertIn("symbolic link", result.stderr)
            finally:
                (runtime / "secrets").unlink(missing_ok=True)
                shutil.rmtree(runtime, ignore_errors=True)

    def test_positive_invalidates_old_canonical_before_early_failure(self) -> None:
        for failure in ("dependency", "render", "daemon", "images", "capacity"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as raw:
                evidence = Path(raw) / "evidence"
                evidence.mkdir()
                canonical = evidence / "readiness-verdict.json"
                canonical.write_bytes(b"stale-ready-canonical\n")

                result = self.run_stubbed_scenario(
                    "startup-readiness", evidence, fail_at=failure
                )

                self.assertEqual(10, result.returncode, result.stderr)
                self.assertFalse(canonical.exists())
                scenario = evidence / "readiness-verdict.startup-readiness.json"
                self.assertTrue(scenario.exists())
                self.assertEqual(
                    "failed", json.loads(scenario.read_text())["overall_status"]
                )

    def test_successful_ready_positive_publishes_canonical_from_scenario_record(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            evidence = Path(raw) / "evidence"
            result = self.run_stubbed_scenario("vault-restart-recovery", evidence)

            self.assertEqual(0, result.returncode, result.stderr)
            scenario = evidence / "readiness-verdict.vault-restart-recovery.json"
            canonical = evidence / "readiness-verdict.json"
            self.assertEqual(scenario.read_bytes(), canonical.read_bytes())
            payload = json.loads(canonical.read_text(encoding="utf-8"))
            self.assertEqual("vault-restart-recovery", payload["scenario"])
            self.assertEqual("ready", payload["overall_status"])
            self.assertEqual("passed", payload["recovery_status"])
            self.assertEqual(EXPECTED_SERVICES, set(payload["services"]))

    def test_negative_writes_scenario_evidence_and_preserves_canonical_bytes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            evidence = Path(raw) / "evidence"
            evidence.mkdir()
            canonical = evidence / "readiness-verdict.json"
            original = b'{"overall_status":"ready","sentinel":"unchanged"}\n'
            canonical.write_bytes(original)

            result = self.run_stubbed_scenario("negative-timeout", evidence)

            self.assertEqual(30, result.returncode, result.stderr)
            self.assertEqual(original, canonical.read_bytes())
            scenario = evidence / "readiness-verdict.negative-timeout.json"
            payload = json.loads(scenario.read_text(encoding="utf-8"))
            self.assertEqual("negative-timeout", payload["scenario"])
            self.assertEqual("timed_out", payload["overall_status"])

    def test_scenario_stdout_names_evidence_and_canonical_paths(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            evidence = Path(raw) / "evidence"
            result = self.run_stubbed_scenario("startup-readiness", evidence)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn(
                f"evidence_path={evidence / 'readiness-verdict.startup-readiness.json'}",
                result.stdout,
            )
            self.assertIn(
                f"readiness_handoff={evidence / 'readiness-verdict.json'}",
                result.stdout,
            )

    def test_every_scenario_writes_evidence_on_early_failure(self) -> None:
        for scenario in (
            "startup-readiness",
            "vault-restart-recovery",
            "negative-timeout",
        ):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as raw:
                evidence = Path(raw) / "evidence"
                result = self.run_stubbed_scenario(scenario, evidence, fail_at="daemon")
                self.assertEqual(10, result.returncode, result.stderr)
                verdict = evidence / f"readiness-verdict.{scenario}.json"
                self.assertTrue(verdict.exists())
                payload = json.loads(verdict.read_text(encoding="utf-8"))
                self.assertEqual(scenario, payload["scenario"])
                self.assertEqual("failed", payload["overall_status"])

    def test_startup_and_recovery_failure_evidence_preserves_exit_classes(
        self,
    ) -> None:
        cases = (
            ("startup-readiness", "startup", 20),
            ("vault-restart-recovery", "recovery", 40),
        )
        for scenario, failure, exit_class in cases:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as raw:
                evidence = Path(raw) / "evidence"
                result = self.run_stubbed_scenario(scenario, evidence, fail_at=failure)
                self.assertEqual(exit_class, result.returncode, result.stderr)
                payload = json.loads(
                    (evidence / f"readiness-verdict.{scenario}.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual("failed", payload["overall_status"])
                self.assertEqual("passed", payload["cleanup_status"])
                self.assertEqual("passed", payload["redaction_status"])
                expected_recovery = (
                    "failed"
                    if scenario == "vault-restart-recovery"
                    else "not_applicable"
                )
                self.assertEqual(expected_recovery, payload["recovery_status"])

    def test_exit_cleanup_honors_runtime_marker_before_parent_flag(self) -> None:
        cases = (
            ("marker-present", True, True, True, 0, 37, True),
            ("marker-absent", True, True, False, 0, 37, False),
            ("marker-invalid-runtime", False, True, True, 0, 37, False),
            ("marker-project-mismatch", True, False, True, 0, 37, False),
            ("marker-cleanup-failure", True, True, True, 50, 50, True),
        )
        for (
            label,
            owned_runtime,
            matching_project,
            marker_present,
            cleanup_exit,
            expected_exit,
            cleanup_called,
        ) in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as raw:
                directory = Path(raw)
                runtime = (
                    Path("/tmp") / f"hyhome-crr-20260719-{os.getpid()}-marker01"
                    if owned_runtime
                    else directory / "runtime"
                )
                runtime_project = runtime.name
                project_name = (
                    runtime_project
                    if matching_project
                    else "hyhome-crr-20260719-12345-abcd1234"
                )
                shutil.rmtree(runtime, ignore_errors=True)
                runtime.mkdir()
                try:
                    if marker_present:
                        (runtime / "cleanup-required").touch()
                    cleanup_record = directory / "cleanup-called"
                    shell = f"""
source {RUNNER!s}
CRR_RUNTIME_DIR={runtime!s}
CRR_PROJECT_NAME={project_name}
CRR_CLEANUP_REQUIRED=false
CRR_CLEANUP_DONE=false
cleanup_owned_project() {{
  printf '%s\n' "$1" >{cleanup_record!s}
  return {cleanup_exit}
}}
cleanup_runtime_material() {{ :; }}
set +e
(exit 37)
on_exit
"""
                    result = subprocess.run(
                        ["bash", "-c", shell],
                        cwd=ROOT,
                        env=os.environ.copy(),
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(expected_exit, result.returncode, result.stderr)
                    self.assertEqual(cleanup_called, cleanup_record.exists())
                    if cleanup_called:
                        self.assertEqual(
                            runtime_project,
                            cleanup_record.read_text(encoding="utf-8").strip(),
                        )
                finally:
                    shutil.rmtree(runtime, ignore_errors=True)

    def test_traefik_uses_task_owned_file_provider_without_engine_socket(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        traefik_section = text.split("\n  traefik:\n", maxsplit=1)[1].split(
            "\n  vault:\n", maxsplit=1
        )[0]
        self.assertIn("--providers.file.filename=", traefik_section)
        self.assertIn("--providers.file.watch=false", traefik_section)
        self.assertNotIn("--providers.docker", traefik_section)
        self.assertNotIn("docker" + ".sock", text)
        self.assertIn("traefik-readiness.yml", traefik_section)

    def test_runtime_images_are_exact_digest_pins(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        for service, image in EXPECTED_IMAGES.items():
            with self.subTest(service=service):
                section = text.split(f"\n  {service}:\n", maxsplit=1)[1]
                self.assertIn(f"    image: {image}\n", section)

    def test_local_image_identity_gate_accepts_target_descriptor_runtime_id(
        self,
    ) -> None:
        runner = RUNNER.read_text(encoding="utf-8")
        runtime_body = runner.split("execute_runtime_scenario() {", maxsplit=1)[
            1
        ].split("\n}\n\nmain()", maxsplit=1)[0]
        self.assertLess(
            runtime_body.index("assert_local_image_identities"),
            runtime_body.index('>"${CRR_RUNTIME_DIR}/cleanup-required"'),
        )
        self.assertLess(
            runtime_body.index("assert_local_image_identities"),
            runtime_body.index("start_vault"),
        )
        manifest_digest = "sha256:" + "1" * 64
        config_id = "sha256:" + "2" * 64
        image_ref = f"example.invalid/readiness@{manifest_digest}"
        expected_repo_digest = f"example.invalid/readiness@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [expected_repo_digest],
                "Id": manifest_digest,
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        valid = self.run_library(
            "docker() { printf '%s\\n' \"$CRR_TEST_INSPECTION\"; }; "
            "observe_docker_image_config_digest() { "
            "printf '%s\\n' \"$CRR_TEST_CONFIG_ID\"; }; "
            "assert_local_image_identity "
            f"{image_ref} {expected_repo_digest} {manifest_digest} {config_id}",
            env={
                "CRR_TEST_INSPECTION": inspection,
                "CRR_TEST_CONFIG_ID": config_id,
            },
        )
        self.assertEqual(0, valid.returncode, valid.stderr)

    def test_oauth_manual_endpoints_include_internal_issuer(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        oauth_section = text.split("\n  oauth2-proxy:\n", maxsplit=1)[1].split(
            "\n  traefik:\n", maxsplit=1
        )[0]
        self.assertIn("--skip-oidc-discovery=true", oauth_section)
        self.assertIn(
            "--oidc-issuer-url=http://keycloak:8080/realms/master",
            oauth_section,
        )
        for endpoint in ("--login-url=", "--redeem-url=", "--oidc-jwks-url="):
            self.assertIn(endpoint, oauth_section)

    def test_override_declares_resource_limits(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        expected = {
            "keycloak": ('cpus: "1.00"', "mem_limit: 768m"),
            "oauth2-proxy": ('cpus: "0.50"', "mem_limit: 256m"),
            "traefik": ('cpus: "0.50"', "mem_limit: 256m"),
            "vault": ('cpus: "0.50"', "mem_limit: 256m"),
            "vault-agent": ('cpus: "0.25"', "mem_limit: 128m"),
        }
        service_order = list(expected)
        for index, service in enumerate(service_order):
            start = text.index(f"\n  {service}:\n")
            end = (
                text.index(f"\n  {service_order[index + 1]}:\n", start)
                if index + 1 < len(service_order)
                else len(text)
            )
            section = text[start:end]
            for declaration in expected[service]:
                self.assertIn(declaration, section, service)

    def test_override_declares_closed_service_and_port_contract(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        declared_services = {
            line.strip()[:-1]
            for line in text.splitlines()
            if line.startswith("  ")
            and not line.startswith("    ")
            and line.strip().endswith(":")
            and line.strip()[:-1] in EXPECTED_SERVICES
        }
        self.assertEqual(EXPECTED_SERVICES, declared_services)
        published_ports = {
            port for port in EXPECTED_PORTS if f"127.0.0.1:{port}:" in text
        }
        self.assertEqual(EXPECTED_PORTS, published_ports)

    def test_task_bridge_is_dedicated_and_publish_capable(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        network_section = text.split("networks: !override\n", maxsplit=1)[1].split(
            "\nvolumes: !override", maxsplit=1
        )[0]
        self.assertIn("  crr_net:", network_section)
        self.assertIn("    driver: bridge", network_section)
        self.assertNotIn("    external: true", network_section)
        self.assertNotIn("    internal: true", network_section)

    def test_traefik_healthcheck_ping_matches_published_target(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        traefik_section = text.split("\n  traefik:\n", maxsplit=1)[1].split(
            "\n  vault:\n", maxsplit=1
        )[0]
        self.assertIn("--entryPoints.ping.address=:8080", traefik_section)
        self.assertIn('"127.0.0.1:18082:8080"', traefik_section)
        self.assertIn("test: [CMD, traefik, healthcheck, --ping]", traefik_section)

    def test_vault_agent_output_preparation_order_and_identity(self) -> None:
        wrapper = (
            ROOT / "scripts/operations/check-compose-core-readiness.sh"
        ).read_text(encoding="utf-8")
        self.assertLess(
            wrapper.index("initialize_unseal_and_configure_synthetic_vault"),
            wrapper.index("prepare_vault_agent_output_volume"),
        )
        self.assertLess(
            wrapper.index("prepare_vault_agent_output_volume"),
            wrapper.index("start_remaining_services"),
        )

        override = OVERRIDE.read_text(encoding="utf-8")
        vault_agent_section = override.split("\n  vault-agent:\n", maxsplit=1)[1]
        self.assertNotIn("    user: 0:0", vault_agent_section)
        self.assertNotIn("chmod 0777", LIBRARY.read_text(encoding="utf-8"))

    def test_vault_commands_respect_image_entrypoint(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        self.assertIn("    command: !override\n      - server\n", text)
        self.assertIn(
            "      - agent\n      - -config=/vault/config/vault-agent-readiness.hcl",
            text,
        )
        self.assertNotIn("      - vault\n      - server", text)
        self.assertNotIn("      - vault\n      - agent", text)

    def test_vault_server_loads_entrypoint_config_directory_once(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        vault_section = text.split("\n  vault:\n", maxsplit=1)[1].split(
            "\n  vault-agent:\n", maxsplit=1
        )[0]
        self.assertIn("    command: !override\n      - server\n", vault_section)
        self.assertNotIn("-config=/vault/config/", vault_section)

    def test_vault_sensitive_commands_use_mounted_secret_flow(self) -> None:
        library = LIBRARY.read_text(encoding="utf-8")
        override = OVERRIDE.read_text(encoding="utf-8")
        self.assertIn("crr-vault-unseal-key", override)
        self.assertIn("crr-vault-root-token", override)
        self.assertIn("vault_exec_with_mounted_root_token", library)
        self.assertIn("unseal_vault_from_mounted_secret", library)
        self.assertNotIn("-e VAULT_TOKEN", library)
        self.assertNotIn(
            'unseal_key="$(<"${CRR_SECRET_DIR}/vault_unseal_key")"', library
        )


if __name__ == "__main__":
    unittest.main()
