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
}

CANDIDATE_INDEXES = {
    "hy-home/sec01-airflow:3.3.2-keycloak-candidate": "sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2",
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
            self.assertEqual("2.43.6", str(service["build"]["args"]["N8N_VERSION"]))
            self.assertEqual("hyhome/n8n:2.43.6-local", service["image"])
        runners = {
            compose["services"][n]["image"]
            for n in ("n8n-task-runner", "n8n-task-runner-worker")
        }
        self.assertEqual(1, len(runners))
        self.assertEqual(
            "n8nio/runners:2.43.6@sha256:3168a82b29b3a8ec9acbe876d9e654b3333dfd630b257f6cc2bc81fc5f93b2bf",
            runners.pop(),
        )
        for name in ("Dockerfile", "dev.Dockerfile"):
            source = (N8N / name).read_text()
            self.assertEqual(
                {"2.43.6"}, set(re.findall(r"^ARG N8N_VERSION=(\S+)$", source, re.M))
            )
            self.assertIn('RUN test "$(n8n --version)" = "${N8N_VERSION}"', source)
            self.assertIn(
                "FROM n8nio/n8n:${N8N_VERSION}@sha256:dd580fe1ab6e99e85bc66f2acf8bc8c5e9409fbe61b2e2803c5024403ef52833",
                source,
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

    def test_pruned_custom_node_uses_pinned_base_framework_and_loads_at_build(self):
        for name in ("Dockerfile", "dev.Dockerfile"):
            with self.subTest(name=name):
                source = (N8N / name).read_text()
                self.assertIn(
                    "ENV NODE_PATH=/usr/local/lib/node_modules/n8n/node_modules",
                    source,
                )
                self.assertIn("npm prune --omit=dev", source)
                self.assertIn(
                    "require('/opt/hyhome/n8n-custom/opsflow/dist/OpsflowSmtp.node.js')",
                    source,
                )
                self.assertIn("node.description.name === 'opsflowSmtp'", source)
                self.assertIn(
                    "node.description.inputs[0] === workflow.NodeConnectionTypes.Main",
                    source,
                )

    def test_opsflow_package_matches_upstream_workflow_api(self):
        package_root = N8N / "workloads/manifest-outbox-notifier/nodes/OpsflowSmtp"
        package = json.loads((package_root / "package.json").read_text())
        lock = json.loads((package_root / "package-lock.json").read_text())
        for section in ("peerDependencies", "devDependencies"):
            self.assertEqual("2.43.4", package[section]["n8n-workflow"])
            self.assertEqual(package[section], lock["packages"][""][section])
        self.assertEqual(
            "2.43.4", lock["packages"]["node_modules/n8n-workflow"]["version"]
        )

    def test_n8n_source_receipt_does_not_reuse_previous_native_acceptance(self):
        evidence = ROOT / "infra/09-platform-ops/security-updates"
        ledger = json.loads((evidence / "update-ledger.json").read_text())
        self.assertTrue(ledger["historical_n8n_source_preparations"])
        for row in ledger["entries"]:
            if row["service"] not in {
                "n8n",
                "n8n-worker",
                "n8n-task-runner",
                "n8n-task-runner-worker",
            }:
                continue
            for field in ("signature", "sbom_scan", "native_test", "deployment"):
                self.assertEqual("NOT_RUN", row[field])
            self.assertNotIn("candidate_workflow_receipt", row)
            if row["service"] in {"n8n", "n8n-worker"}:
                self.assertEqual("UNKNOWN", row["target_index_digest"])
        binding = ledger["n8n_source_preparation"]["source_binding"]
        aggregate = hashlib.sha256()
        for item in sorted(binding["input_files"], key=lambda item: item["path"]):
            data = (ROOT / item["path"]).read_bytes()
            self.assertEqual(item["sha256"], hashlib.sha256(data).hexdigest())
            aggregate.update(item["path"].encode() + b"\0" + data)
        self.assertEqual(binding["input_sha256"], aggregate.hexdigest())
        build_inputs = json.loads(
            (
                ROOT / "infra/09-platform-ops/security-updates/build-inputs.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            binding, build_inputs["n8n_source_preparation"]["source_binding"]
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


if __name__ == "__main__":
    unittest.main()
