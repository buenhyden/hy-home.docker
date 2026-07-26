"""Focused contract tests for the isolated Compose core-readiness harness."""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "scripts/validation/compose-core-readiness.lib.sh"
RUNNER = ROOT / "scripts/validation/run-compose-core-readiness.sh"
OVERRIDE = (
    ROOT
    / "tests/fixtures/compose-core-readiness/compose.core-runtime.override.yml"
)

EXPECTED_SERVICES = {
    "keycloak",
    "oauth2-proxy",
    "traefik",
    "vault",
    "vault-agent",
}
EXPECTED_PORTS = {"18000", "18443", "18082", "18083", "18200"}
EXPECTED_IMAGES = {
    "keycloak": (
        "quay.io/keycloak/keycloak@"
        "sha256:0aae0de7fca85525f727d3354df17896092de8bb26ae4c12d89c77e5df8cbce4"
    ),
    "oauth2-proxy": (
        "quay.io/oauth2-proxy/oauth2-proxy@"
        "sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561"
    ),
    "traefik": (
        "traefik@"
        "sha256:21a3d83696379bac6434bb32e1dde0aff0e84ef2abd053ed3db87d3f45e749b2"
    ),
    "vault": (
        "hashicorp/vault@"
        "sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54"
    ),
    "vault-agent": (
        "hashicorp/vault@"
        "sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54"
    ),
}
EXPECTED_CONFIG_DIGESTS = {
    "quay.io/keycloak/keycloak": (
        "sha256:1361d6e492058a69d979ab735cfc19e73e5f1e0a707e8fa5cfb610c00bc3cff2"
    ),
    "quay.io/oauth2-proxy/oauth2-proxy": (
        "sha256:cf3a5d50849b1799260d6aca62367c333b33472f208cbbdaab243a831b1a622f"
    ),
    "traefik": (
        "sha256:7982c57cc89de38c6ca9e3f17caa0569890d2043f6f5271c78ad75a2cff50f32"
    ),
    "hashicorp/vault": (
        "sha256:1747a4ab1e1bea8938269b23827165c5d80eecbdb5c115fd58e6380569537c84"
    ),
}


class ComposeCoreReadinessContractTests(unittest.TestCase):
    maxDiff = None

    def run_library(
        self,
        body: str,
        *,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = f"set -euo pipefail; source {LIBRARY!s}; {body}"
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            ["bash", "-c", command],
            cwd=ROOT,
            env=merged_env,
            text=True,
            capture_output=True,
            check=False,
        )

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
                    (
                        evidence / f"readiness-verdict.{scenario}.json"
                    ).read_text(encoding="utf-8")
                )
                self.assertEqual("failed", verdict["overall_status"])

    @staticmethod
    def isolated_model(*, services: set[str] | None = None) -> dict[str, object]:
        names = services or EXPECTED_SERVICES
        published = {
            "traefik": ["18000", "18443", "18082"],
            "keycloak": ["18083"],
            "vault": ["18200"],
        }
        limits = {
            "keycloak": (1.0, 805306368),
            "oauth2-proxy": (0.5, 268435456),
            "traefik": (0.5, 268435456),
            "vault": (0.5, 268435456),
            "vault-agent": (0.25, 134217728),
        }
        return {
            "name": "hyhome-crr-20260719-12345-abcd1234",
            "services": {
                name: {
                    "container_name": None,
                    "image": EXPECTED_IMAGES.get(
                        name, "example.invalid/extra@sha256:" + ("0" * 64)
                    ),
                    "cpus": limits.get(name, (0, 0))[0],
                    "mem_limit": limits.get(name, (0, 0))[1],
                    "networks": {"crr_net": None},
                    "ports": [
                        {
                            "host_ip": "127.0.0.1",
                            "published": port,
                            "target": 1,
                            "protocol": "tcp",
                        }
                        for port in published.get(name, [])
                    ],
                    "volumes": [
                        {
                            "type": "volume",
                            "source": f"{name}-data",
                            "target": f"/var/lib/{name}",
                        }
                    ],
                }
                for name in sorted(names)
            },
            "networks": {"crr_net": {"external": False}},
        }

    def write_model(self, directory: Path, model: dict[str, object]) -> Path:
        path = directory / "model.json"
        path.write_text(json.dumps(model), encoding="utf-8")
        return path

    def test_exact_five_service_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            valid = self.write_model(directory, self.isolated_model())
            result = self.run_library(f"assert_exact_service_set {valid!s}")
            self.assertEqual(0, result.returncode, result.stderr)

            invalid_model = self.isolated_model(services=EXPECTED_SERVICES | {"redis"})
            invalid = self.write_model(directory, invalid_model)
            result = self.run_library(f"assert_exact_service_set {invalid!s}")
            self.assertEqual(10, result.returncode)
            self.assertIn("exact service set", result.stderr)

    def test_rejects_shared_paths_ports_networks(self) -> None:
        mutations = {
            "host port": lambda model: model["services"]["traefik"]["ports"][0].update(
                {"published": "80"}
            ),
            "non-loopback binding": lambda model: model["services"]["traefik"][
                "ports"
            ][0].update({"host_ip": "0.0.0.0"}),
            "external network": lambda model: model["networks"].update(
                {"mng-pg": {"external": True}}
            ),
            "repository bind": lambda model: model["services"]["vault"][
                "volumes"
            ].append(
                {
                    "type": "bind",
                    "source": str(ROOT / "volumes/security/vault"),
                    "target": "/vault/file",
                }
            ),
            "fixed container name": lambda model: model["services"]["keycloak"].update(
                {"container_name": "keycloak"}
            ),
            "resource limit drift": lambda model: model["services"]["vault"].update(
                {"cpus": 2.0}
            ),
        }
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            for label, mutate in mutations.items():
                with self.subTest(label=label):
                    model = self.isolated_model()
                    mutate(model)
                    path = self.write_model(directory, model)
                    result = self.run_library(
                        f"assert_isolated_paths_ports_networks {path!s}"
                    )
                    self.assertEqual(10, result.returncode)
                    self.assertIn("isolated model", result.stderr)

    def test_synthetic_secret_bodies_never_reach_summary(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            secret_dir = directory / "secrets"
            secret_dir.mkdir()
            marker = "CRR-DO-NOT-PROMOTE-7d0a84"
            (secret_dir / "cookie").write_text(marker, encoding="utf-8")
            output = directory / "readiness-verdict.json"
            services = directory / "services.json"
            endpoints = directory / "endpoints.json"
            services.write_text(json.dumps({"vault": marker}), encoding="utf-8")
            endpoints.write_text("{}", encoding="utf-8")

            result = self.run_library(
                "write_readiness_verdict "
                f"{output!s} hyhome-crr-20260719-12345-abcd1234 "
                "startup-readiness ready 1 passed passed "
                f"{services!s} {endpoints!s} "
                "2026-07-19T01:00:00Z 2026-07-19T01:00:01Z",
                env={"CRR_SECRET_DIR": str(secret_dir)},
            )
            self.assertNotEqual(0, result.returncode)
            self.assertFalse(output.exists())

            services.write_text(
                json.dumps({"vault": {"container": "healthy"}}), encoding="utf-8"
            )
            result = self.run_library(
                "write_readiness_verdict "
                f"{output!s} hyhome-crr-20260719-12345-abcd1234 "
                "startup-readiness ready 1 passed passed "
                f"{services!s} {endpoints!s} "
                "2026-07-19T01:00:00Z 2026-07-19T01:00:01Z",
                env={"CRR_SECRET_DIR": str(secret_dir)},
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn(marker, output.read_text(encoding="utf-8"))

    def test_cleanup_accepts_only_owned_project_name(self) -> None:
        accepted = self.run_library(
            "is_owned_project_name hyhome-crr-20260719-12345-abcd1234"
        )
        self.assertEqual(0, accepted.returncode, accepted.stderr)

        for rejected in (
            "hy-home-infra",
            "hyhome-crr-20260719-",
            "hyhome-crr-20260719-12345",
            "hyhome-crr-20260719-12x",
            "hyhome-crr-20260719-12345-AbCd1234",
            "hyhome-crr-20260719-12345-bad_token",
            "hyhome-crr-20260718-12345",
        ):
            with self.subTest(project=rejected):
                result = self.run_library(f"is_owned_project_name {rejected}")
                self.assertNotEqual(0, result.returncode)

    def test_runtime_identity_is_collision_resistant_and_symlink_safe(self) -> None:
        wrapper = (
            ROOT / "scripts/validation/run-compose-core-readiness.sh"
        ).read_text(encoding="utf-8")
        self.assertIn("allocate_runtime_identity", wrapper)
        self.assertNotIn('CRR_PROJECT_NAME="${CRR_PROJECT_PREFIX}$$"', wrapper)

        with tempfile.TemporaryDirectory() as fake_root_raw:
            fake_root = Path(fake_root_raw)
            task_root = (
                fake_root
                / "_workspace/repo-support/"
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

    def test_cleanup_includes_stopped_containers_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            marker = Path(raw) / "down-called"
            body = (
                "docker() { "
                'if [ "$1" = container ] && [ "$2" = ls ]; then '
                'case " $* " in *" -aq "*) printf stopped-id;; *) return 91;; esac; '
                "elif [ \"$2\" = inspect ]; then printf wrong-owner; "
                "else return 0; fi; }; "
                f"crr_compose() {{ : >{marker!s}; }}; "
                "cleanup_owned_project hyhome-crr-20260719-12345-abcd1234"
            )
            result = self.run_library(body)
            self.assertEqual(50, result.returncode)
            self.assertFalse(marker.exists())

        for label, docker_body, compose_body in (
            (
                "list failure",
                "docker() { return 91; }; ",
                "crr_compose() { return 0; }; ",
            ),
            (
                "down failure",
                'docker() { if [ "$2" = ls ]; then return 0; fi; return 0; }; ',
                "crr_compose() { return 91; }; ",
            ),
        ):
            with self.subTest(label=label):
                result = self.run_library(
                    docker_body
                    + compose_body
                    + "cleanup_owned_project "
                    "hyhome-crr-20260719-12345-abcd1234"
                )
                self.assertEqual(50, result.returncode)
                self.assertNotIn("true", result.stdout)

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
            result = self.run_stubbed_scenario(
                "vault-restart-recovery", evidence
            )

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
                result = self.run_stubbed_scenario(
                    scenario, evidence, fail_at="daemon"
                )
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
                result = self.run_stubbed_scenario(
                    scenario, evidence, fail_at=failure
                )
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
                    Path("/tmp")
                    / f"hyhome-crr-20260719-{os.getpid()}-marker01"
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

    def test_bind_guard_is_scoped_to_current_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            runtime = Path("/tmp/hyhome-crr-20260719-12345-abcd1234")
            valid = self.isolated_model()
            valid["services"]["vault"]["volumes"].append(
                {
                    "type": "bind",
                    "source": str(runtime / "config/vault.hcl"),
                    "target": "/vault/config/vault.hcl",
                    "read_only": True,
                }
            )
            valid_path = self.write_model(directory, valid)
            result = self.run_library(
                f"assert_isolated_paths_ports_networks {valid_path!s}",
                env={"CRR_RUNTIME_DIR": str(runtime)},
            )
            self.assertEqual(0, result.returncode, result.stderr)

            mutations = {
                "raw engine socket": lambda model: model["services"]["traefik"][
                    "volumes"
                ].append(
                    {
                        "type": "bind",
                        "source": "/var/run/docker" + ".sock",
                        "target": "/var/run/docker" + ".sock",
                        "read_only": True,
                    }
                ),
                "sibling runtime": lambda model: model["services"]["vault"][
                    "volumes"
                ].append(
                    {
                        "type": "bind",
                        "source": "/tmp/hyhome-crr-20260719-99999-Evil1234/config",
                        "target": "/vault/config",
                        "read_only": True,
                    }
                ),
                "writable bind": lambda model: model["services"]["vault"][
                    "volumes"
                ].append(
                    {
                        "type": "bind",
                        "source": str(runtime / "config/vault.hcl"),
                        "target": "/vault/config/vault.hcl",
                        "read_only": False,
                    }
                ),
            }
            for label, mutate in mutations.items():
                with self.subTest(label=label):
                    model = self.isolated_model()
                    mutate(model)
                    path = self.write_model(directory, model)
                    result = self.run_library(
                        f"assert_isolated_paths_ports_networks {path!s}",
                        env={"CRR_RUNTIME_DIR": str(runtime)},
                    )
                    self.assertEqual(10, result.returncode)

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
        runtime_body = runner.split("execute_runtime_scenario() {", maxsplit=1)[1].split(
            "\n}\n\nmain()", maxsplit=1
        )[0]
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

    def test_local_image_identity_gate_accepts_config_digest_runtime_id(
        self,
    ) -> None:
        manifest_digest = "sha256:" + "1" * 64
        config_id = "sha256:" + "2" * 64
        image_ref = f"example.invalid/readiness@{manifest_digest}"
        expected_repo_digest = f"example.invalid/readiness@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [expected_repo_digest],
                "Id": config_id,
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

    def test_production_image_tuples_type_target_and_config_independently(
        self,
    ) -> None:
        result = self.run_library(
            "printf '%s\\n' \"${CRR_EXPECTED_IMAGE_IDENTITIES[@]}\""
        )
        self.assertEqual(0, result.returncode, result.stderr)
        rows = [row.split("|") for row in result.stdout.splitlines()]
        self.assertEqual(4, len(rows))
        for image_ref, repo_digest, target_digest, config_digest in rows:
            image_name = image_ref.split("@", maxsplit=1)[0]
            self.assertEqual(repo_digest.split("@", maxsplit=1)[1], target_digest)
            self.assertEqual(EXPECTED_CONFIG_DIGESTS[image_name], config_digest)
            self.assertNotEqual(target_digest, config_digest)

    def test_local_image_identity_gate_rejects_manifest_mismatch(self) -> None:
        manifest_digest = "sha256:" + "1" * 64
        config_id = "sha256:" + "2" * 64
        image_ref = f"example.invalid/readiness@{manifest_digest}"
        expected_repo_digest = f"example.invalid/readiness@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [
                    "example.invalid/readiness@sha256:" + "3" * 64
                ],
                "Id": manifest_digest,
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        rejected = self.run_library(
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
        self.assertEqual(10, rejected.returncode)
        self.assertIn("repository manifest", rejected.stderr)

    def test_local_image_identity_gate_rejects_config_id_mismatch(self) -> None:
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
        rejected = self.run_library(
            "docker() { printf '%s\\n' \"$CRR_TEST_INSPECTION\"; }; "
            "observe_docker_image_config_digest() { "
            "printf '%s\\n' \"$CRR_TEST_CONFIG_ID\"; }; "
            "assert_local_image_identity "
            f"{image_ref} {expected_repo_digest} {manifest_digest} {config_id}",
            env={
                "CRR_TEST_INSPECTION": inspection,
                "CRR_TEST_CONFIG_ID": "sha256:" + "4" * 64,
            },
        )
        self.assertEqual(10, rejected.returncode)
        self.assertIn("configuration ID", rejected.stderr)

    def test_local_image_identity_gate_rejects_unrelated_runtime_id(self) -> None:
        manifest_digest = "sha256:" + "1" * 64
        config_id = "sha256:" + "2" * 64
        image_ref = f"example.invalid/readiness@{manifest_digest}"
        expected_repo_digest = f"example.invalid/readiness@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [expected_repo_digest],
                "Id": "sha256:" + "5" * 64,
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        rejected = self.run_library(
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
        self.assertEqual(10, rejected.returncode)
        self.assertIn("repository manifest", rejected.stderr)

    def test_local_image_identity_gate_rejects_missing_image(self) -> None:
        manifest_digest = "sha256:" + "1" * 64
        config_id = "sha256:" + "2" * 64
        image_ref = f"example.invalid/readiness@{manifest_digest}"
        expected_repo_digest = f"example.invalid/readiness@{manifest_digest}"
        rejected = self.run_library(
            "docker() { return 1; }; assert_local_image_identity "
            f"{image_ref} {expected_repo_digest} {manifest_digest} {config_id}"
        )
        self.assertEqual(10, rejected.returncode)
        self.assertIn("unavailable", rejected.stderr)

    def test_start_commands_disable_pull_and_build(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            capture = Path(raw) / "commands"
            result = self.run_library(
                "crr_compose() { printf '%s\\n' \"$*\" >>"
                f"{capture!s}; }}; "
                "wait_container_health() { :; }; "
                "start_vault; start_remaining_services"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            commands = capture.read_text(encoding="utf-8").splitlines()
            self.assertIn("up -d --pull never --no-build vault", commands)
            self.assertTrue(
                any(
                    command.startswith(
                        "up -d --pull never --no-build --wait --wait-timeout "
                    )
                    for command in commands
                )
            )

    def test_preflight_dependency_check_does_not_require_daemon(self) -> None:
        docker_stub = (
            "docker() { "
            'if [ "${1-}" = compose ]; then return 0; fi; '
            "return 55; }; "
        )
        preflight = self.run_library(docker_stub + "assert_docker_compose")
        self.assertEqual(0, preflight.returncode, preflight.stderr)

        runtime = self.run_library(docker_stub + "assert_docker_daemon")
        self.assertEqual(10, runtime.returncode)
        self.assertIn("Docker daemon is unavailable", runtime.stderr)

    def test_runtime_capacity_gate_fails_closed(self) -> None:
        insufficient = self.run_library(
            "docker() { printf '2 2147483648 /tmp\\n'; }; "
            "df() { printf '%s\\n' "
            "'Filesystem 1024-blocks Used Available Capacity Mounted' "
            "'/dev/test 10000000 1 9000000 1% /tmp'; }; "
            "assert_target_capacity"
        )
        self.assertEqual(10, insufficient.returncode)
        self.assertIn("target capacity", insufficient.stderr)

        sufficient = self.run_library(
            "docker() { printf '4 4294967296 /tmp\\n'; }; "
            "df() { printf '%s\\n' "
            "'Filesystem 1024-blocks Used Available Capacity Mounted' "
            "'/dev/test 10000000 1 8388608 1% /tmp'; }; "
            "assert_target_capacity"
        )
        self.assertEqual(0, sufficient.returncode, sufficient.stderr)

    def test_endpoint_observations_are_complete_and_classified(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            endpoint_path = Path(raw) / "endpoints.json"
            result = self.run_library(
                "probe_service_endpoint() { "
                'case "$1" in *127.0.0.1:18000*) return 1;; *) return 0;; esac; '
                "}; crr_compose() { return 0; }; "
                f"CRR_ENDPOINTS_JSON={endpoint_path!s}; "
                "set +e; probe_all_service_endpoints; status=$?; set -e; "
                "exit $status"
            )
            self.assertEqual(1, result.returncode)
            self.assertEqual(
                {
                    "keycloak-ready": "passed",
                    "oauth2-proxy-ping": "failed",
                    "traefik-ping": "passed",
                    "vault-health": "passed",
                    "vault-agent-sentinel": "passed",
                },
                json.loads(endpoint_path.read_text(encoding="utf-8")),
            )

        with tempfile.TemporaryDirectory() as raw:
            services = Path(raw) / "services.json"
            services.write_text(
                json.dumps(
                    {
                        name: {"container": "healthy"}
                        for name in sorted(EXPECTED_SERVICES)
                    }
                ),
                encoding="utf-8",
            )
            degraded = self.run_library(
                f"classify_readiness_status {services!s} false"
            )
            self.assertEqual(0, degraded.returncode, degraded.stderr)
            self.assertEqual("degraded", degraded.stdout.strip())

            payload = json.loads(services.read_text(encoding="utf-8"))
            payload["vault"]["container"] = "exited"
            services.write_text(json.dumps(payload), encoding="utf-8")
            failed = self.run_library(
                f"classify_readiness_status {services!s} false"
            )
            self.assertEqual(0, failed.returncode, failed.stderr)
            self.assertEqual("failed", failed.stdout.strip())

    def test_runtime_material_permissions_allow_non_root_consumers(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            runtime_dir = Path(raw) / "runtime"
            secret_dir = runtime_dir / "secrets"
            config_dir = runtime_dir / "config"
            secret_dir.mkdir(parents=True, mode=0o700)
            config_dir.mkdir(mode=0o700)
            runtime_dir.chmod(0o700)
            secret_dir.chmod(0o700)
            config_dir.chmod(0o700)

            result = self.run_library(
                "prepare_synthetic_secrets",
                env={
                    "CRR_SECRET_DIR": str(secret_dir),
                    "CRR_CONFIG_DIR": str(config_dir),
                },
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(0o700, stat.S_IMODE(runtime_dir.stat().st_mode))
            self.assertEqual(0o700, stat.S_IMODE(secret_dir.stat().st_mode))
            self.assertEqual(0o700, stat.S_IMODE(config_dir.stat().st_mode))
            self.assertEqual(
                {
                    "keycloak_admin_password",
                    "oauth2_proxy_client_secret",
                    "oauth2_proxy_cookie_secret",
                    "vault_agent_role_id",
                    "vault_agent_secret_id",
                    "vault_root_token",
                    "vault_unseal_key",
                },
                {path.name for path in secret_dir.iterdir()},
            )
            self.assertTrue(
                all(
                    stat.S_IMODE(path.stat().st_mode) == 0o444
                    for path in secret_dir.iterdir()
                )
            )
            self.assertEqual(
                {
                    "vault-readiness.hcl",
                    "vault-agent-readiness.hcl",
                    "traefik-readiness.yml",
                },
                {path.name for path in config_dir.iterdir()},
            )
            self.assertTrue(
                all(
                    stat.S_IMODE(path.stat().st_mode) == 0o644
                    for path in config_dir.iterdir()
                )
            )

    def test_oauth_cookie_secret_has_supported_byte_length(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            runtime_dir = Path(raw) / "runtime"
            secret_dir = runtime_dir / "secrets"
            config_dir = runtime_dir / "config"
            secret_dir.mkdir(parents=True)
            config_dir.mkdir()

            result = self.run_library(
                "prepare_synthetic_secrets",
                env={
                    "CRR_SECRET_DIR": str(secret_dir),
                    "CRR_CONFIG_DIR": str(config_dir),
                },
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(
                32,
                (secret_dir / "oauth2_proxy_cookie_secret").stat().st_size,
            )

    def test_synthetic_secret_preparation_is_exact_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            runtime_dir = Path(raw) / "runtime"
            secret_dir = runtime_dir / "secrets"
            config_dir = runtime_dir / "config"
            secret_dir.mkdir(parents=True)
            config_dir.mkdir()
            runtime_dir.chmod(0o700)
            secret_dir.chmod(0o700)
            config_dir.chmod(0o700)
            env = {
                "CRR_SECRET_DIR": str(secret_dir),
                "CRR_CONFIG_DIR": str(config_dir),
            }

            first = self.run_library("prepare_synthetic_secrets", env=env)
            self.assertEqual(0, first.returncode, first.stderr)
            sentinel = secret_dir / "unrelated-sentinel"
            sentinel.touch(mode=0o400)

            second = self.run_library("prepare_synthetic_secrets", env=env)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertTrue(sentinel.exists())
            self.assertEqual(
                {
                    "keycloak_admin_password",
                    "oauth2_proxy_client_secret",
                    "oauth2_proxy_cookie_secret",
                    "vault_agent_role_id",
                    "vault_agent_secret_id",
                    "vault_root_token",
                    "vault_unseal_key",
                    "unrelated-sentinel",
                },
                {path.name for path in secret_dir.iterdir()},
            )

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

    def test_timeout_has_stable_exit_and_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            cleanup_marker = directory / "cleaned"
            verdict = directory / "readiness-verdict.json"
            services = directory / "services.json"
            endpoints = directory / "endpoints.json"
            services.write_text(
                json.dumps(
                    {
                        name: {"container": "timed_out"}
                        for name in sorted(EXPECTED_SERVICES)
                    }
                ),
                encoding="utf-8",
            )
            endpoints.write_text("{}", encoding="utf-8")
            result = self.run_library(
                "cleanup_owned_project() { printf cleaned >"
                f"{cleanup_marker!s}; }}; "
                "finish_scenario negative-timeout timed_out "
                f"{verdict!s} hyhome-crr-20260719-12345-abcd1234 0 "
                f"{services!s} {endpoints!s} "
                "2026-07-19T01:00:00Z 2026-07-19T01:00:01Z"
            )
            self.assertEqual(30, result.returncode, result.stderr)
            self.assertEqual("cleaned", cleanup_marker.read_text(encoding="utf-8"))
            payload = json.loads(verdict.read_text(encoding="utf-8"))
            self.assertEqual("timed_out", payload["overall_status"])
            self.assertEqual("passed", payload["cleanup_status"])

    def test_readiness_verdict_schema(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            output = directory / "readiness-verdict.json"
            services = directory / "services.json"
            endpoints = directory / "endpoints.json"
            services.write_text(
                json.dumps(
                    {
                        name: {"container": "healthy"}
                        for name in sorted(EXPECTED_SERVICES)
                    }
                ),
                encoding="utf-8",
            )
            endpoints.write_text(
                json.dumps({"traefik-ping": "passed"}), encoding="utf-8"
            )
            result = self.run_library(
                "write_readiness_verdict "
                f"{output!s} hyhome-crr-20260719-12345-abcd1234 "
                "startup-readiness ready 3 passed passed "
                f"{services!s} {endpoints!s} "
                "2026-07-19T01:00:00Z 2026-07-19T01:00:03Z"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                {
                    "schema_version",
                    "producer_spec",
                    "producer_task",
                    "approval_ref",
                    "scenario",
                    "target_class",
                    "project_name",
                    "started_at",
                    "completed_at",
                    "services",
                    "endpoint_verdicts",
                    "observed_state",
                    "recovery_status",
                    "teardown_status",
                    "overall_status",
                    "elapsed_seconds",
                    "cleanup_status",
                    "redaction_status",
                },
                set(payload),
            )
            self.assertEqual(2, payload["schema_version"])
            self.assertEqual(
                "spec:124-compose-runtime-readiness-remediation",
                payload["producer_spec"],
            )
            self.assertEqual(
                "task:2026-07-19-compose-runtime-readiness-remediation",
                payload["producer_task"],
            )
            self.assertEqual("startup-readiness", payload["scenario"])
            self.assertEqual("local-linked-worktree-docker-engine", payload["target_class"])
            self.assertEqual("ready", payload["observed_state"])
            self.assertEqual("not_applicable", payload["recovery_status"])
            self.assertEqual("passed", payload["teardown_status"])
            self.assertEqual(EXPECTED_SERVICES, set(payload["services"]))

    def test_override_and_approval_contract_declare_resource_limits(self) -> None:
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

        for relative in (
            "docs/04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md",
            "docs/04.execution/tasks/2026-07-19-compose-runtime-readiness-remediation.md",
        ):
            document = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("Target host class:", document, relative)
            self.assertIn("Resource limits:", document, relative)

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
            port
            for port in EXPECTED_PORTS
            if f"127.0.0.1:{port}:" in text
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

    def test_vault_agent_output_volume_preparation_is_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            capture = Path(raw) / "argv"
            result = self.run_library(
                "crr_compose() { printf '%s\\n' \"$*\" >"
                f"{capture!s}; }}; prepare_vault_agent_output_volume"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(
                "run --rm --no-deps --pull never --user 0:0 --cap-add CHOWN "
                "--entrypoint sh vault-agent -ec "
                "chmod 0750 /vault/out && chown vault:vault /vault/out",
                capture.read_text(encoding="utf-8").strip(),
            )

        failed = self.run_library(
            "crr_compose() { return 1; }; prepare_vault_agent_output_volume"
        )
        self.assertEqual(20, failed.returncode)
        self.assertIn("Vault Agent output volume preparation failed", failed.stderr)

    def test_vault_agent_output_mode_is_set_before_chown(self) -> None:
        library = LIBRARY.read_text(encoding="utf-8")
        self.assertIn(
            "chmod 0750 /vault/out && chown vault:vault /vault/out",
            library,
        )
        self.assertNotIn(
            "chown vault:vault /vault/out && chmod 0750 /vault/out",
            library,
        )

    def test_vault_agent_output_preparation_order_and_identity(self) -> None:
        wrapper = (
            ROOT / "scripts/validation/run-compose-core-readiness.sh"
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
        vault_agent_section = override.split(
            "\n  vault-agent:\n", maxsplit=1
        )[1]
        self.assertNotIn("    user: 0:0", vault_agent_section)
        self.assertNotIn("chmod 0777", LIBRARY.read_text(encoding="utf-8"))

    def test_vault_recovery_requires_fresh_agent_sentinel_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            capture = Path(raw) / "sequence"
            result = self.run_library(
                "crr_compose() { printf 'compose:%s\\n' \"$*\" >>"
                f"{capture!s}; }}; "
                "wait_container_health() { printf 'wait:%s\\n' \"$1\" >>"
                f"{capture!s}; }}; "
                "unseal_vault_from_mounted_secret() { printf 'unseal\\n' >>"
                f"{capture!s}; }}; recover_vault_after_restart"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(
                [
                    "compose:stop vault-agent",
                    "compose:run --rm --no-deps --entrypoint sh vault-agent "
                    "-ec rm -f /vault/out/readiness.sentinel",
                    "compose:stop vault",
                    "compose:start vault",
                    "wait:vault",
                    "unseal",
                    "compose:start vault-agent",
                    "wait:vault-agent",
                ],
                capture.read_text(encoding="utf-8").splitlines(),
            )

    def test_vault_recovery_steps_fail_closed_as_class_40(self) -> None:
        body = (
            "CRR_STEP=0; "
            "crr_step() { CRR_STEP=$((CRR_STEP + 1)); "
            '[ "$CRR_STEP" -ne "$CRR_FAIL_AT" ]; }; '
            "crr_compose() { crr_step; }; "
            "wait_container_health() { crr_step; }; "
            "unseal_vault_from_mounted_secret() { crr_step; }; "
            "recover_vault_after_restart"
        )
        for failure_step in range(1, 9):
            with self.subTest(failure_step=failure_step):
                result = self.run_library(
                    body,
                    env={"CRR_FAIL_AT": str(failure_step)},
                )
                self.assertEqual(40, result.returncode)
                self.assertIn("compose-core-readiness:", result.stderr)

    def test_vault_commands_respect_image_entrypoint(self) -> None:
        text = OVERRIDE.read_text(encoding="utf-8")
        self.assertIn("    command: !override\n      - server\n", text)
        self.assertIn("      - agent\n      - -config=/vault/config/vault-agent-readiness.hcl", text)
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
        self.assertNotIn('unseal_key="$(<"${CRR_SECRET_DIR}/vault_unseal_key")"', library)


if __name__ == "__main__":
    unittest.main()
