"""Library behavior tests for the isolated Compose core-readiness harness."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.lib.ops._support import (
    EXPECTED_CONFIG_DIGESTS,
    EXPECTED_IMAGES,
    EXPECTED_SERVICES,
    ROOT,
)


LIBRARY = ROOT / "scripts/lib/ops/compose-core-readiness.sh"


class ComposeCoreReadinessHarness:
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


class ComposeCoreReadinessLibraryTests(ComposeCoreReadinessHarness, unittest.TestCase):
    maxDiff = None

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
            "non-loopback binding": lambda model: model["services"]["traefik"]["ports"][
                0
            ].update({"host_ip": "0.0.0.0"}),
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

    def test_cleanup_includes_stopped_containers_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            marker = Path(raw) / "down-called"
            body = (
                "docker() { "
                'if [ "$1" = container ] && [ "$2" = ls ]; then '
                'case " $* " in *" -aq "*) printf stopped-id;; *) return 91;; esac; '
                'elif [ "$2" = inspect ]; then printf wrong-owner; '
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
                    docker_body + compose_body + "cleanup_owned_project "
                    "hyhome-crr-20260719-12345-abcd1234"
                )
                self.assertEqual(50, result.returncode)
                self.assertNotIn("true", result.stdout)

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
                "RepoDigests": ["example.invalid/readiness@sha256:" + "3" * 64],
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
            'docker() { if [ "${1-}" = compose ]; then return 0; fi; return 55; }; '
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
            degraded = self.run_library(f"classify_readiness_status {services!s} false")
            self.assertEqual(0, degraded.returncode, degraded.stderr)
            self.assertEqual("degraded", degraded.stdout.strip())

            payload = json.loads(services.read_text(encoding="utf-8"))
            payload["vault"]["container"] = "exited"
            services.write_text(json.dumps(payload), encoding="utf-8")
            failed = self.run_library(f"classify_readiness_status {services!s} false")
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
            self.assertEqual(
                "local-linked-worktree-docker-engine", payload["target_class"]
            )
            self.assertEqual("ready", payload["observed_state"])
            self.assertEqual("not_applicable", payload["recovery_status"])
            self.assertEqual("passed", payload["teardown_status"])
            self.assertEqual(EXPECTED_SERVICES, set(payload["services"]))

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


if __name__ == "__main__":
    unittest.main()
