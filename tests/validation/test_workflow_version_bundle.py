"""Offline workflow bundle regressions; these do not prove deployment."""

import hashlib
import json
import os
import re
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
AIRFLOW = ROOT / "infra/07-workflow/airflow"
N8N = ROOT / "infra/07-workflow/n8n"
CANDIDATE_MANIFESTS = {
    "hy-home/sec01-airflow:3.3.2-keycloak-candidate": "sha256:c9096805e76159e0b18d55a5e357b1958894c291ebf88e9af2a497de208f227e",
    "hy-home/sec01-n8n-prod:2.42.6-candidate": "sha256:4298977846ed580208c670a87b125ab86873958bc25057a6e9aca1fa8a5f329b",
    "hy-home/sec01-n8n-dev:2.42.6-candidate": "sha256:c32096b2ded1c1c9d6a00c39f32eb3e9ecf3a82a3282910d5d77a9cef8b1c710",
}

CANDIDATE_INDEXES = {
    "hy-home/sec01-airflow:3.3.2-keycloak-candidate": "sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2",
    "hy-home/sec01-n8n-prod:2.42.6-candidate": "sha256:caecb10cce97f48f5131aff8d682ed8b2a24e27f573afac1a58f02cd5efb49d7",
    "hy-home/sec01-n8n-dev:2.42.6-candidate": "sha256:1469f5d7034ba7a7282d061f40135796c8f78e2665f6df0ea72a16a2103ccbff",
}


class WorkflowVersionBundleTests(unittest.TestCase):
    def test_airflow_base_and_args_align(self):
        source = (AIRFLOW / "Dockerfile").read_text()
        compose = yaml.safe_load((AIRFLOW / "docker-compose.yml").read_text())
        args = compose["x-airflow-common"]["build"]["args"]
        for key in (
            "AIRFLOW_VERSION",
            "PYTHON_VERSION",
            "KEYCLOAK_PROVIDER_VERSION",
            "COMMON_COMPAT_PROVIDER_VERSION",
            "CELERY_PROVIDER_VERSION",
        ):
            values = re.findall(rf"^ARG {key}=([^\s]+)$", source, re.M)
            self.assertTrue(values, key)
            self.assertEqual({str(args[key])}, set(values), key)
        self.assertRegex(
            source,
            r"FROM apache/airflow:\$\{AIRFLOW_VERSION\}-python\$\{PYTHON_VERSION\}@sha256:[0-9a-f]{64}",
        )
        self.assertEqual("3.3.2", args["AIRFLOW_VERSION"])
        self.assertEqual("0.11.0", args["KEYCLOAK_PROVIDER_VERSION"])
        self.assertEqual("1.20.0", args["COMMON_COMPAT_PROVIDER_VERSION"])
        self.assertEqual("3.24.1", args["CELERY_PROVIDER_VERSION"])

    def test_airflow_resolution_cannot_silently_drift(self):
        source = (AIRFLOW / "Dockerfile").read_text()
        shell_declaration = re.search(r"^SHELL (\[.+\])$", source, re.M)
        self.assertIsNotNone(
            shell_declaration, "pipeline failures require an explicit shell contract"
        )
        self.assertEqual(
            [
                "/bin/bash",
                "-o",
                "pipefail",
                "-o",
                "errexit",
                "-o",
                "nounset",
                "-o",
                "nolog",
                "-c",
            ],
            json.loads(shell_declaration.group(1)),
        )
        self.assertNotIn("--no-deps", source)
        self.assertNotIn(
            "_PIP_ADDITIONAL_REQUIREMENTS", (AIRFLOW / "docker-compose.yml").read_text()
        )
        self.assertIn("ENV _PIP_ADDITIONAL_REQUIREMENTS=", source)
        self.assertIn("pip check", source)
        self.assertIn('"apache-airflow==${AIRFLOW_VERSION}"', source)
        self.assertIn(
            '"apache-airflow-providers-keycloak==${KEYCLOAK_PROVIDER_VERSION}"', source
        )
        self.assertIn("assert sys.version_info[:2]", source)
        self.assertIn('assert version("apache-airflow")', source)
        upstream = AIRFLOW / "constraints-upstream-3.3.2-python3.13.txt"
        self.assertTrue(upstream.is_file())
        self.assertIn("apache-airflow-providers-keycloak==0.10.0", upstream.read_text())
        self.assertIn(hashlib.sha256(upstream.read_bytes()).hexdigest(), source)
        self.assertIn("constraints-reviewed.txt", source)

    def test_n8n_main_worker_runners_and_both_builds_align(self):
        compose = yaml.safe_load((N8N / "docker-compose.yml").read_text())
        for name in ("n8n", "n8n-worker"):
            service = compose["services"][name]
            self.assertEqual("2.42.6", str(service["build"]["args"]["N8N_VERSION"]))
            self.assertEqual("hyhome/n8n:2.42.6-local", service["image"])
        runners = {
            compose["services"][n]["image"]
            for n in ("n8n-task-runner", "n8n-task-runner-worker")
        }
        self.assertEqual(1, len(runners))
        self.assertRegex(runners.pop(), r"^n8nio/runners:2\.42\.6@sha256:[0-9a-f]{64}$")
        for name in ("Dockerfile", "dev.Dockerfile"):
            source = (N8N / name).read_text()
            self.assertEqual(
                {"2.42.6"}, set(re.findall(r"^ARG N8N_VERSION=(\S+)$", source, re.M))
            )
            self.assertIn('RUN test "$(n8n --version)" = "${N8N_VERSION}"', source)
            self.assertRegex(
                source, r"FROM n8nio/n8n:\$\{N8N_VERSION\}@sha256:[0-9a-f]{64}"
            )
            self.assertRegex(
                source, r"FROM alpine:3\.24\.2@sha256:[0-9a-f]{64} AS font-builder"
            )
            for package in (
                "fontconfig",
                "font-noto",
                "font-noto-cjk",
                "font-dejavu",
                "font-liberation",
                "font-noto-emoji",
            ):
                self.assertRegex(source, rf"{package}=[^\s]+")
            self.assertIn("COPY --from=font-builder /font-builder-packages.txt", source)
            self.assertIn(
                "apk --no-network info -v > /font-builder-packages.txt", source
            )

    def test_candidate_mismatch_blocks_before_container_creation(self):
        image = "hy-home/sec01-airflow:3.3.2-keycloak-candidate"
        digest = (
            "sha256:c9096805e76159e0b18d55a5e357b1958894c291ebf88e9af2a497de208f227e"
        )
        for descriptor in (
            {
                "digest": "sha256:" + "a" * 64,
                "platform": {"os": "linux", "architecture": "amd64"},
            },
            {"digest": digest, "platform": {"os": "linux", "architecture": "arm64"}},
            {"digest": digest, "platform": {"os": "windows", "architecture": "amd64"}},
        ):
            with self.subTest(descriptor=descriptor), patch("subprocess.run") as run:
                run.return_value = subprocess.CompletedProcess(
                    [], 0, json.dumps(descriptor), ""
                )
                rehearsal = WorkflowCandidateRehearsalTests(
                    "test_airflow_actual_versions_dependency_and_imports"
                )
                with self.assertRaises(AssertionError):
                    rehearsal.run_candidate(image, "python", "--version")
                run.assert_called_once()
                self.assertEqual(
                    ["docker", "image", "inspect"], run.call_args.args[0][:3]
                )

    def test_matching_receipt_runs_immutable_index_with_checked_manifest(self):
        image = "hy-home/sec01-airflow:3.3.2-keycloak-candidate"
        digest = (
            "sha256:c9096805e76159e0b18d55a5e357b1958894c291ebf88e9af2a497de208f227e"
        )
        descriptor = {
            "digest": digest,
            "platform": {"os": "linux", "architecture": "amd64"},
        }
        with patch("subprocess.run") as run:
            run.side_effect = [
                subprocess.CompletedProcess([], 0, json.dumps(descriptor), ""),
                subprocess.CompletedProcess([], 0, "synthetic-pass", ""),
            ]
            rehearsal = WorkflowCandidateRehearsalTests(
                "test_airflow_actual_versions_dependency_and_imports"
            )
            self.assertEqual(
                "synthetic-pass", rehearsal.run_candidate(image, "python", "--version")
            )
            self.assertEqual(2, run.call_count)
            command = run.call_args_list[1].args[0]
            self.assertIn(
                "sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2",
                command,
            )
            self.assertNotIn(image, command)
            self.assertIn("linux/amd64", command)


@unittest.skipUnless(
    os.environ.get("HYHOME_WORKFLOW_REHEARSAL") == "1",
    "isolated candidate images must be built explicitly",
)
class WorkflowCandidateRehearsalTests(unittest.TestCase):
    def run_candidate(self, image, entrypoint, *args, script=None):
        expected_digest = CANDIDATE_MANIFESTS[image]
        immutable_index = CANDIDATE_INDEXES[image]
        inspection = subprocess.run(
            [
                "docker",
                "image",
                "inspect",
                "--platform",
                "linux/amd64",
                "--format",
                "{{json .Descriptor}}",
                immutable_index,
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        self.assertEqual(
            0, inspection.returncode, inspection.stdout + inspection.stderr
        )
        descriptor = json.loads(inspection.stdout)
        self.assertIsInstance(descriptor, dict)
        self.assertEqual(expected_digest, descriptor.get("digest"))
        platform = descriptor.get("platform")
        self.assertIsInstance(platform, dict)
        self.assertEqual("linux", platform.get("os"))
        self.assertEqual("amd64", platform.get("architecture"))
        result = subprocess.run(
            [
                "docker",
                "run",
                "--platform",
                "linux/amd64",
                "--rm",
                "--pull",
                "never",
                "-i",
                "--network",
                "none",
                "--read-only",
                "--cpus",
                "1",
                "--memory",
                "1g",
                "--cap-drop",
                "ALL",
                "--security-opt",
                "no-new-privileges",
                "--tmpfs",
                "/tmp:rw,nosuid,nodev",
                "--tmpfs",
                "/opt/airflow/logs:rw,nosuid,nodev",
                "--entrypoint",
                entrypoint,
                immutable_index,
                *args,
            ],
            input=script,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return result.stdout

    def test_airflow_actual_versions_dependency_and_imports(self):
        output = self.run_candidate(
            "hy-home/sec01-airflow:3.3.2-keycloak-candidate",
            "python",
            "-",
            script="""
import sys, subprocess
from importlib.metadata import version
from airflow.providers.keycloak.auth_manager.keycloak_auth_manager import KeycloakAuthManager
from airflow.providers.celery.executors.celery_executor import CeleryExecutor
assert sys.version_info[:2] == (3, 13)
assert version('apache-airflow') == '3.3.2'
assert version('apache-airflow-providers-keycloak') == '0.11.0'
assert version('apache-airflow-providers-common-compat') == '1.20.0'
assert version('apache-airflow-providers-celery') == '3.24.1'
subprocess.run(['pip', 'check'], check=True)
print('installed bundle PASS')
""",
        )
        self.assertIn("installed bundle PASS", output)

    def test_installed_provider_rejects_other_client_before_exchange(self):
        output = self.run_candidate(
            "hy-home/sec01-airflow:3.3.2-keycloak-candidate",
            "python",
            "-",
            script="""
from unittest.mock import patch
from fastapi import HTTPException
from airflow.providers.keycloak.auth_manager.services import token
from airflow.providers.keycloak.auth_manager.keycloak_auth_manager import KeycloakAuthManager
with patch.object(token.conf, 'get', return_value='selected-client'), patch.object(KeycloakAuthManager, 'get_keycloak_client') as exchange:
    try:
        token.create_client_credentials_token('other-client', 'synthetic-unused', expiration_time_in_seconds=60)
    except HTTPException as error:
        assert error.status_code == 403
        assert error.detail == 'Client credentials authentication failed'
    else:
        raise AssertionError('cross-client grant accepted')
    exchange.assert_not_called()
with patch.object(token.conf, 'get', side_effect=lambda section, key, **kwargs: 'selected-client' if key == token.CONF_CLIENT_ID_KEY else '' if key == token.CONF_JWT_FEDERATED_CLIENT_IDS_KEY else 'synthetic'), patch.object(token, '_get_jwks_client'), patch.object(token.jwt, 'decode', return_value={'azp': 'other-client'}), patch.object(KeycloakAuthManager, 'get_keycloak_client') as exchange:
    try:
        token.create_jwt_federated_token('synthetic-unused', expiration_time_in_seconds=60)
    except HTTPException as error:
        assert error.status_code == 403
        assert error.detail == 'Invalid Keycloak assertion'
    else:
        raise AssertionError('unlisted federated client accepted')
    exchange.assert_not_called()
print('cross-client denial PASS; exchange/crypto mocked, no live OIDC claim')
""",
        )
        self.assertIn("cross-client denial PASS", output)

    def test_n8n_both_variants_actual_uid_version_and_font_receipt(self):
        for variant in ("prod", "dev"):
            with self.subTest(variant=variant):
                output = self.run_candidate(
                    f"hy-home/sec01-n8n-{variant}:2.42.6-candidate",
                    "/bin/sh",
                    "-ec",
                    'test "$(id -u)" = 1000; test "$(n8n --version)" = 2.42.6; '
                    'grep -q "fontconfig-2.17.1-r1" /usr/share/hy-home-font-builder-packages.txt; '
                    'grep -q "font-noto-emoji-2.051-r0" /usr/share/hy-home-font-builder-packages.txt; '
                    'echo "installed n8n/font bundle PASS"',
                )
                self.assertIn("installed n8n/font bundle PASS", output)


if __name__ == "__main__":
    unittest.main()
