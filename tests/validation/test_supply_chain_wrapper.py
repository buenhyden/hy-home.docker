from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shlex
import stat
import subprocess
import tarfile
import tempfile
import unittest
from unittest import mock

from tests.lib.gate.subprocess_support import gate_root_pass_fds
from tests.lib.supply_chain._fixtures import (
    cosign_verification,
    cyclonedx_report,
    grype_match,
    grype_report,
    provenance_statement,
    scorecard_report,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "scripts/validation/check-supply-chain-policy.py"
FIXTURES = ROOT / "examples/operations/supply-chain"
TOOL_REGISTRY = ROOT / "infra/supply-chain.tool-images.json"
POLICY = ROOT / "infra/supply-chain.sample-service-policy.json"
EXCEPTIONS = ROOT / "infra/supply-chain.vulnerability-exceptions.json"
COSIGN_OFFLINE_SIGNING_CONFIG = (
    ROOT / "infra/supply-chain.cosign-offline-signing-config.json"
)
COSIGN_OFFLINE_TRUSTED_ROOT = (
    ROOT / "infra/supply-chain.cosign-offline-trusted-root.json"
)
WRAPPER = ROOT / "scripts/security/verify-sample-service-supply-chain.sh"
SEED_HELPER = ROOT / "scripts/lib/supply_chain/grype_db_seed.py"
SAMPLE_DOCKERFILE = ROOT / "examples/sample-web-service/Dockerfile"

RUNTIME_MATERIAL_REF = (
    "nginxinc/nginx-unprivileged:1.31.3-alpine3.24-slim@"
    "sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5"
)
RUNTIME_MATERIAL_REPO_DIGEST = (
    "nginxinc/nginx-unprivileged@"
    "sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5"
)
RUNTIME_MATERIAL_CONFIG_ID = (
    "sha256:9c57576567614e37b77581f70984d5fbb8595b1409882bd08ae31a38a4f4b071"
)
RUNTIME_MATERIAL_TARGET_DESCRIPTOR_DIGEST = (
    "sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5"
)
BUILD_MATERIAL_CONFIG_ID = (
    "sha256:2607caa9805847fac4de202017bb1b830deb09f4c07dc9964a0157abbc604577"
)
BUILD_MATERIAL_TARGET_DESCRIPTOR_DIGEST = (
    "sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d"
)
OBSERVED_TOOL_IDENTITIES = {
    "syft": (
        "sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c",
        "sha256:3567af297260e786440f30d149c2846302fd1df0823ee769d8b167d068f7d181",
    ),
    "grype": (
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821",
        "sha256:4d4127e08c9eaafe6fa1eb2fcc05c83b2608562541949ffb33ef32eb4b1b25c0",
    ),
    "cosign": (
        "sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00",
        "sha256:4221e0d9d429afa26a9f1b8bc8f0ba2c9af470f7b495d845c31ac982a5d1182b",
    ),
    "scorecard": (
        "sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795",
        "sha256:6b05eb0cfef8a6df4f78dae40cbbe8b18da1ec881c4c70a14796201a122a3491",
    ),
}
STALE_RUNTIME_MATERIAL = "nginxinc/nginx-unprivileged:1.27.3-alpine"

SOURCE_REVISION = "0123456789abcdef0123456789abcdef01234567"
BASELINE_SUBJECT = {
    "role": "baseline",
    "source_revision": SOURCE_REVISION,
    "image_config_digest": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "oci_archive_sha256": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
}
CANDIDATE_SUBJECT = {
    "role": "candidate",
    "source_revision": SOURCE_REVISION,
    "image_config_digest": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    "oci_archive_sha256": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
    "build_context_sha256": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
}
BASELINE_SUBJECT["build_context_sha256"] = CANDIDATE_SUBJECT["build_context_sha256"]

HANDOFF_RELATIVE = pathlib.Path(
    "_workspace/repo-support/"
    "task-2026-07-19-security-supply-chain-remediation/supply-chain"
)


def load_checker():
    spec = importlib.util.spec_from_file_location("supply_chain_policy", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("supply-chain policy checker cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SupplyChainWrapperContractTests(unittest.TestCase):
    def run_wrapper_library(self, script: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ | {"HYHOME_SUPPLY_CHAIN_LIBRARY_ONLY": "1"}
        return subprocess.run(
            ["bash", "-c", script],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            pass_fds=gate_root_pass_fds(ROOT),
        )

    def test_all_runtime_invocations_are_offline_and_pull_disabled(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        docker_runs = [
            line.strip()
            for line in text.splitlines()
            if line.strip().startswith("docker run ")
        ]
        self.assertGreaterEqual(len(docker_runs), 8)
        for command in docker_runs:
            self.assertIn("--pull=never", command)
        build_command = next(
            line.strip()
            for line in text.splitlines()
            if line.strip().startswith("docker buildx build ")
        )
        self.assertIn("--builder default", build_command)
        self.assertIn("--network=none", build_command)
        self.assertIn("--pull=false", build_command)
        self.assertIn('--file Dockerfile - <"$build_context_archive"', build_command)
        self.assertNotIn('"$SERVICE_DIR"', build_command)

    def test_sample_context_has_closed_dockerignore_contract(self) -> None:
        dockerignore = ROOT / "examples/sample-web-service/.dockerignore"
        self.assertEqual(
            [
                "**",
                "!Dockerfile",
                "!.dockerignore",
                "!nginx.conf",
                "!site/",
                "!site/**",
            ],
            dockerignore.read_text(encoding="utf-8").splitlines(),
        )

    def test_runtime_material_is_exact_current_official_pin(self) -> None:
        wrapper = WRAPPER.read_text(encoding="utf-8")
        dockerfile = SAMPLE_DOCKERFILE.read_text(encoding="utf-8")

        self.assertIn(
            f'readonly RUNTIME_MATERIAL_REF="{RUNTIME_MATERIAL_REF}"',
            wrapper,
        )
        self.assertIn(
            f'readonly RUNTIME_MATERIAL_REPO_DIGEST="{RUNTIME_MATERIAL_REPO_DIGEST}"',
            wrapper,
        )
        self.assertIn(
            f'readonly RUNTIME_MATERIAL_CONFIG_ID="{RUNTIME_MATERIAL_CONFIG_ID}"',
            wrapper,
        )
        self.assertIn(
            "readonly RUNTIME_MATERIAL_TARGET_DESCRIPTOR_DIGEST="
            f'"{RUNTIME_MATERIAL_TARGET_DESCRIPTOR_DIGEST}"',
            wrapper,
        )
        self.assertIn(
            f'readonly BUILD_MATERIAL_CONFIG_ID="{BUILD_MATERIAL_CONFIG_ID}"',
            wrapper,
        )
        self.assertIn(
            "readonly BUILD_MATERIAL_TARGET_DESCRIPTOR_DIGEST="
            f'"{BUILD_MATERIAL_TARGET_DESCRIPTOR_DIGEST}"',
            wrapper,
        )
        self.assertNotEqual(
            RUNTIME_MATERIAL_TARGET_DESCRIPTOR_DIGEST,
            RUNTIME_MATERIAL_CONFIG_ID,
        )
        self.assertNotEqual(
            BUILD_MATERIAL_TARGET_DESCRIPTOR_DIGEST,
            BUILD_MATERIAL_CONFIG_ID,
        )
        self.assertIn(f"FROM {RUNTIME_MATERIAL_REF} AS runtime", dockerfile)
        self.assertNotIn(STALE_RUNTIME_MATERIAL, wrapper)
        self.assertNotIn(STALE_RUNTIME_MATERIAL, dockerfile)

    def test_exact_local_image_gate_precedes_build_or_tool_start(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        advisory = text.split("run_advisory() {", maxsplit=1)[1].split(
            "\n}\n\nrun_scorecard_advisory", maxsplit=1
        )[0]
        self.assertLess(
            advisory.index("assert_local_image_identities"),
            advisory.index("build_role_image baseline"),
        )

    def test_local_image_identity_accepts_target_descriptor_runtime_id(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [reference],
                "Id": manifest_digest,
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        valid = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_INSPECTION={shlex.quote(inspection)}\n"
            f"TEST_CONFIG_ID={config_id}\n"
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_image_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            f"assert_local_image_identity {reference} {reference} "
            f"{manifest_digest} {config_id}\n"
        )
        self.assertEqual(0, valid.returncode, valid.stderr)

    def test_local_image_identity_accepts_config_digest_runtime_id(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [reference],
                "Id": config_id,
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        valid = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_INSPECTION={shlex.quote(inspection)}\n"
            f"TEST_CONFIG_ID={config_id}\n"
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_image_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            f"assert_local_image_identity {reference} {reference} "
            f"{manifest_digest} {config_id}\n"
        )
        self.assertEqual(0, valid.returncode, valid.stderr)

    def test_local_image_identity_rejects_manifest_mismatch(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        wrong_reference = "example.invalid/tool@sha256:" + ("c" * 64)
        inspection = json.dumps(
            {
                "RepoDigests": [wrong_reference],
                "Id": manifest_digest,
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        result = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_INSPECTION={shlex.quote(inspection)}\n"
            f"TEST_CONFIG_ID={config_id}\n"
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_image_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            f"assert_local_image_identity {reference} {reference} "
            f"{manifest_digest} {config_id}\n"
        )
        self.assertEqual(10, result.returncode)
        self.assertIn("pinned-image-manifest-mismatch", result.stderr)

    def test_local_image_identity_rejects_config_id_mismatch(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [reference],
                "Id": manifest_digest,
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        result = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_INSPECTION={shlex.quote(inspection)}\n"
            f"TEST_CONFIG_ID=sha256:{'d' * 64}\n"
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_image_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            f"assert_local_image_identity {reference} {reference} "
            f"{manifest_digest} {config_id}\n"
        )
        self.assertEqual(10, result.returncode)
        self.assertIn("pinned-image-config-id-mismatch", result.stderr)

    def test_local_image_identity_rejects_unrelated_runtime_id(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        inspection = json.dumps(
            {
                "RepoDigests": [reference],
                "Id": "sha256:" + ("e" * 64),
                "Descriptor": {
                    "digest": manifest_digest,
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        result = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_INSPECTION={shlex.quote(inspection)}\n"
            f"TEST_CONFIG_ID={config_id}\n"
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_image_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            f"assert_local_image_identity {reference} {reference} "
            f"{manifest_digest} {config_id}\n"
        )
        self.assertEqual(10, result.returncode)
        self.assertIn("pinned-image-manifest-mismatch", result.stderr)

    def test_local_image_identity_rejects_missing_image(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        result = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            "docker() { return 1; }\n"
            f"assert_local_image_identity {reference} {reference} "
            f"{manifest_digest} {config_id}\n"
        )
        self.assertEqual(10, result.returncode)
        self.assertIn("pinned-image-missing", result.stderr)

    def test_runtime_artifacts_use_one_private_tmp_tree_and_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            output = base / HANDOFF_RELATIVE
            output.mkdir(parents=True)
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(base))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                "prepare_transient_directory\n"
                "case $runtime_dir in /tmp/hyhome-supply-chain.*) ;; *) exit 91 ;; esac\n"
                'test "$(stat -c %a "$runtime_dir")" = 700\n'
                'test "$(stat -c %a "$grype_db_dir")" = 700\n'
                'test "$(stat -c %a "$private_key_dir")" = 700\n'
                'touch "$runtime_dir/raw-artifact"\n'
                "saved_runtime_dir=$runtime_dir\n"
                "cleanup_transient_state\n"
                'test ! -e "$saved_runtime_dir"\n'
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual([], list(output.iterdir()))

    def test_legacy_runtime_cleanup_uses_the_gated_offline_root_container(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        cleanup = text.split("remove_legacy_runtime_artifacts() {", maxsplit=1)[
            1
        ].split("\n}\n\nbuild_role_image", maxsplit=1)[0]
        self.assertIn(
            "docker run --pull=never --rm --network none --user 0:0",
            cleanup,
        )
        self.assertIn('"$BUILD_MATERIAL_REF"', cleanup)
        self.assertNotIn('rm -rf -- "$OUTPUT_DIR', cleanup)

    def test_nonroot_tools_receive_a_private_writable_tmp_mount(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        nonroot_runs = [
            line.strip()
            for line in text.splitlines()
            if "docker run " in line and '--user "$(id -u):$(id -g)"' in line
        ]
        self.assertGreaterEqual(len(nonroot_runs), 8)
        for command in nonroot_runs:
            self.assertIn(
                '--mount "type=bind,source=$tool_tmp_dir,target=/tmp"',
                command,
            )
            self.assertIn("--env HOME=/tmp", command)

    def test_missing_db_seed_fails_before_any_runtime_container(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            base.mkdir(mode=0o700)
            helper = pathlib.Path(temporary) / "resolve-seed"
            helper.write_text("#!/usr/bin/env bash\nexit 1\n", encoding="utf-8")
            helper.chmod(0o755)
            docker_marker = pathlib.Path(temporary) / "docker-called"
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(base))}\n"
                f"GRYPE_DB_SEED_HELPER={shlex.quote(str(helper))}\n"
                "GRYPE_DB_SEED_RELATIVE=_workspace/repo-support/task/grype-db-seed\n"
                f"docker() {{ touch {shlex.quote(str(docker_marker))}; }}\n"
                "assert_grype_db_seed_available\n"
            )
            self.assertEqual(10, result.returncode, result.stderr)
            self.assertIn("grype-db-seed-unavailable-advisory-blocked", result.stderr)
            self.assertFalse(docker_marker.exists())

        text = WRAPPER.read_text(encoding="utf-8")
        advisory = text.split("run_advisory() {", maxsplit=1)[1].split(
            "\n}\n\nrun_scorecard_advisory", maxsplit=1
        )[0]
        self.assertLess(
            advisory.index("assert_grype_db_seed_available"),
            advisory.index("ensure_advisory_prerequisites"),
        )
        self.assertLess(
            advisory.index("assert_grype_db_seed_available"),
            advisory.index("seed_private_grype_db_cache"),
        )
        self.assertLess(
            advisory.index("assert_grype_db_seed_available"),
            advisory.index("build_role_image baseline"),
        )

    def test_advisory_resolves_and_revalidates_only_the_task7_seed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            seed_relative = pathlib.Path("_workspace/repo-support/task/grype-db-seed")
            cache = base / seed_relative / "generations" / ("a" * 64) / "cache"
            (cache / "6").mkdir(parents=True, mode=0o700)
            helper_log = pathlib.Path(temporary) / "helper.log"
            helper = pathlib.Path(temporary) / "resolve-seed"
            helper.write_text(
                "#!/usr/bin/env bash\n"
                f"printf '%s\\n' \"$*\" >> {shlex.quote(str(helper_log))}\n"
                '[[ "$1" == --resolve-current ]] || exit 91\n'
                f"printf '%s\\n' {shlex.quote(str(cache))}\n",
                encoding="utf-8",
            )
            helper.chmod(0o755)
            private_copy = pathlib.Path(temporary) / "private-copy"
            private_copy.mkdir(mode=0o700)
            docker_log = pathlib.Path(temporary) / "docker.log"
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(base))}\n"
                f"GRYPE_DB_SEED_HELPER={shlex.quote(str(helper))}\n"
                f"GRYPE_DB_SEED_RELATIVE={seed_relative}\n"
                f"grype_db_dir={shlex.quote(str(private_copy))}\n"
                "docker() {\n"
                f"  printf '%s\\n' \"$*\" >> {shlex.quote(str(docker_log))}\n"
                "}\n"
                "assert_grype_db_seed_available\n"
                f'test "$grype_db_seed_source" = {shlex.quote(str(cache))}\n'
                "seed_private_grype_db_cache\n"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            helper_calls = helper_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(helper_calls))
            self.assertTrue(
                all(
                    call == f"--resolve-current {base} {seed_relative}"
                    for call in helper_calls
                )
            )
            docker_call = docker_log.read_text(encoding="utf-8")
            self.assertIn("--network none", docker_call)
            self.assertIn(f"source={cache},target=/seed,readonly", docker_call)

        text = WRAPPER.read_text(encoding="utf-8")
        self.assertIn(
            f'GRYPE_DB_SEED_HELPER="$BASE_DIR/{SEED_HELPER.relative_to(ROOT)}"', text
        )
        self.assertIn("task-2026-07-23-security-supply-chain-runtime-closure", text)
        self.assertGreaterEqual(text.count("--resolve-current"), 2)

    def test_git_context_rejection_maps_to_class_10_and_tamper_to_50(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = pathlib.Path(temporary) / "repo"
            service = repo / "examples/sample-web-service"
            (service / "site").mkdir(parents=True)
            (service / ".dockerignore").write_text(
                "**\n!Dockerfile\n!.dockerignore\n!nginx.conf\n!site/\n!site/**\n",
                encoding="utf-8",
            )
            (service / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
            (service / "nginx.conf").write_text("server {}\n", encoding="utf-8")
            (service / "site/index.html").write_text("ok\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "-c",
                    "user.name=Task Test",
                    "-c",
                    "user.email=task@example.invalid",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                check=True,
            )
            source_revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            runtime = pathlib.Path(temporary) / "runtime"
            runtime.mkdir(mode=0o700)
            snapshot = runtime / "context.json"
            archive = runtime / "context.tar"
            common = (
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(repo))}\n"
                f"SERVICE_DIR={shlex.quote(str(service))}\n"
                f"CHECKER={shlex.quote(str(CHECKER_PATH))}\n"
                f"SOURCE_REVISION={source_revision}\n"
                f"build_context_snapshot={shlex.quote(str(snapshot))}\n"
                f"build_context_archive={shlex.quote(str(archive))}\n"
            )

            (service / "site/untracked.html").write_text("new\n", encoding="utf-8")
            dirty = self.run_wrapper_library(
                common + "capture_build_context_snapshot\n"
            )
            self.assertEqual(10, dirty.returncode, dirty.stderr)
            (service / "site/untracked.html").unlink()

            (repo / ".git/info/exclude").write_text(
                "examples/sample-web-service/site/ignored.html\n",
                encoding="utf-8",
            )
            (service / "site/ignored.html").write_text("ignored but effective\n")
            ignored = self.run_wrapper_library(
                common + "capture_build_context_snapshot\n"
            )
            self.assertEqual(10, ignored.returncode, ignored.stderr)
            (service / "site/ignored.html").unlink()

            clean = self.run_wrapper_library(
                common + "capture_build_context_snapshot\n"
            )
            self.assertEqual(0, clean.returncode, clean.stderr)
            self.assertEqual(0o600, stat.S_IMODE(archive.stat().st_mode))
            with tarfile.open(archive, "r:") as bundle:
                names = {member.name.rstrip("/") for member in bundle.getmembers()}
            self.assertEqual(
                {
                    ".dockerignore",
                    "Dockerfile",
                    "nginx.conf",
                    "site",
                    "site/index.html",
                },
                names,
            )
            snapshot_payload = json.loads(snapshot.read_text(encoding="utf-8"))
            self.assertEqual(2, snapshot_payload["schema_version"])
            for material in snapshot_payload["materials"]:
                self.assertTrue(
                    {
                        "device",
                        "inode",
                        "size",
                        "mtime_ns",
                        "ctime_ns",
                        "mode",
                        "uid",
                        "sha256",
                    }.issubset(material)
                )
            (service / "site/index.html").write_text("tampered\n", encoding="utf-8")
            tampered = self.run_wrapper_library(
                common + "assert_build_context_unchanged\n"
            )
            self.assertEqual(50, tampered.returncode, tampered.stderr)

    def test_mutate_and_restore_during_build_fails_class_50_without_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = pathlib.Path(temporary) / "repo"
            service = repo / "examples/sample-web-service"
            (service / "site").mkdir(parents=True)
            (service / ".dockerignore").write_text(
                "**\n!Dockerfile\n!.dockerignore\n!nginx.conf\n!site/\n!site/**\n",
                encoding="utf-8",
            )
            (service / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
            (service / "nginx.conf").write_text("server {}\n", encoding="utf-8")
            material = service / "site/index.html"
            material.write_text("original\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "-c",
                    "user.name=Task Test",
                    "-c",
                    "user.email=task@example.invalid",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                check=True,
            )
            source_revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            runtime = pathlib.Path(temporary) / "runtime"
            runtime.mkdir(mode=0o700)
            output = pathlib.Path(temporary) / "output"
            output.mkdir(mode=0o700)
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(repo))}\n"
                f"SERVICE_DIR={shlex.quote(str(service))}\n"
                f"CHECKER={shlex.quote(str(CHECKER_PATH))}\n"
                f"SOURCE_REVISION={source_revision}\n"
                f"build_context_snapshot={shlex.quote(str(runtime / 'context.json'))}\n"
                f"build_context_archive={shlex.quote(str(runtime / 'context.tar'))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                "capture_build_context_snapshot\n"
                "build_role_image() {\n"
                f"  printf 'mutated\\n' > {shlex.quote(str(material))}\n"
                f"  printf 'original\\n' > {shlex.quote(str(material))}\n"
                "}\n"
                "build_role_image baseline\n"
                "assert_build_context_unchanged\n"
            )
            self.assertEqual(50, result.returncode, result.stderr)
            self.assertIn("build-context-changed", result.stderr)
            self.assertFalse((output / "verification-verdict.pair.json").exists())

        text = WRAPPER.read_text(encoding="utf-8")
        advisory = text.split("run_advisory() {", maxsplit=1)[1].split(
            "\n}\n\nrun_scorecard_advisory", maxsplit=1
        )[0]
        self.assertIn(
            "build_role_image baseline\n  assert_build_context_unchanged\n"
            "  build_role_image candidate\n  assert_build_context_unchanged",
            advisory,
        )

    def test_invalidate_consumer_verdicts_removes_only_exact_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            output = (
                base
                / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
            )
            output.mkdir(parents=True)
            for role in ("baseline", "candidate"):
                (output / f"verification-verdict.{role}.json").write_text("stale\n")
            unrelated = output / "unrelated.json"
            unrelated.write_text("preserve\n")
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(base))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                "invalidate_consumer_verdicts\n"
                f"test ! -e {shlex.quote(str(output / 'verification-verdict.baseline.json'))}\n"
                f"test ! -e {shlex.quote(str(output / 'verification-verdict.candidate.json'))}\n"
                f"test -f {shlex.quote(str(unrelated))}\n"
            )
            self.assertEqual(0, result.returncode, result.stderr)

    def test_failed_advisory_leaves_no_stale_consumer_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            output = (
                base
                / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
            )
            output.mkdir(parents=True)
            for role in ("baseline", "candidate"):
                (output / f"verification-verdict.{role}.json").write_text("stale\n")
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(base))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                "run_preflight() { return 1; }\n"
                "run_advisory\n"
            )
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((output / "verification-verdict.baseline.json").exists())
            self.assertFalse((output / "verification-verdict.candidate.json").exists())

    def test_accepted_grype_exception_cannot_publish_consumer_verdict_pair(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            output = (
                base
                / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
            )
            output.mkdir(parents=True)
            for role in ("baseline", "candidate"):
                (output / f"verification-verdict.{role}.json").write_text("stale\n")
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(base))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                "SOURCE_REVISION=0123456789abcdef0123456789abcdef01234567\n"
                "run_preflight() { :; }\n"
                "prepare_transient_directory() {\n"
                '  mkdir -p "$OUTPUT_DIR/grype-db-cache"\n'
                '  grype_db_dir="$OUTPUT_DIR/grype-db-cache"\n'
                '  run_verdict_dir=$(mktemp -d "$OUTPUT_DIR/.verification-verdicts.XXXXXX")\n'
                "}\n"
                "capture_build_context_snapshot() { BUILD_CONTEXT_SHA256=sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee; }\n"
                "assert_build_context_unchanged() { :; }\n"
                "ensure_advisory_prerequisites() { :; }\n"
                "assert_grype_db_seed_available() { :; }\n"
                "assert_local_image_identities() { :; }\n"
                "seed_private_grype_db_cache() { :; }\n"
                "remove_legacy_runtime_artifacts() { :; }\n"
                "record_grype_db_identity() { :; }\n"
                'build_role_image() { mkdir -p "$OUTPUT_DIR/$1"; }\n'
                "export_oci_archive() { :; }\n"
                "derive_subject_tuple() {\n"
                "  if [[ $1 == baseline ]]; then\n"
                "    OCI_MANIFEST_DIGEST[$1]=sha256:1111111111111111111111111111111111111111111111111111111111111111\n"
                "    IMAGE_CONFIG_DIGEST[$1]=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
                "    OCI_ARCHIVE_SHA256[$1]=sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n"
                "    DOCKER_ARCHIVE_SHA256[$1]=sha256:3333333333333333333333333333333333333333333333333333333333333333\n"
                "    LOCAL_IMAGE_REF[$1]=hyhome.local/sample-web-service:baseline-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
                "  else\n"
                "    OCI_MANIFEST_DIGEST[$1]=sha256:2222222222222222222222222222222222222222222222222222222222222222\n"
                "    IMAGE_CONFIG_DIGEST[$1]=sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\n"
                "    OCI_ARCHIVE_SHA256[$1]=sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
                "    DOCKER_ARCHIVE_SHA256[$1]=sha256:4444444444444444444444444444444444444444444444444444444444444444\n"
                "    LOCAL_IMAGE_REF[$1]=hyhome.local/sample-web-service:candidate-cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\n"
                "  fi\n"
                "}\n"
                "generate_cyclonedx_and_grype_verdict() {\n"
                '  mkdir -p "$OUTPUT_DIR/$1"\n'
                "  if [[ $1 == baseline ]]; then\n"
                '    printf \'%s\\n\' \'{"exception_id":"EXC-SSC-0001","verdict":"accepted"}\' >"$OUTPUT_DIR/$1/vulnerability-verdict.json"\n'
                "  else\n"
                '    printf \'%s\\n\' \'{"exception_id":null,"verdict":"accepted"}\' >"$OUTPUT_DIR/$1/vulnerability-verdict.json"\n'
                "  fi\n"
                "}\n"
                "publish_role_advisory_summary() { :; }\n"
                "generate_slsa_provenance() { :; }\n"
                "sign_and_verify_archive() { :; }\n"
                "run_advisory\n"
            )
            self.assertEqual(40, result.returncode, result.stderr)
            self.assertIn("grype-exception-requires-manual-review", result.stderr)
            self.assertFalse((output / "verification-verdict.baseline.json").exists())
            self.assertFalse((output / "verification-verdict.candidate.json").exists())
            vulnerability_verdict = json.loads(
                (output / "baseline/vulnerability-verdict.json").read_text()
            )
            self.assertEqual("EXC-SSC-0001", vulnerability_verdict["exception_id"])

    def test_baseline_wrong_subject_check_targets_candidate_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "supply-chain"
            (output / "baseline").mkdir(parents=True)
            (output / "candidate").mkdir()
            for role in ("baseline", "candidate"):
                (output / role / "image.oci.tar").write_bytes(b"archive")
            command_log = pathlib.Path(temporary) / "docker-commands.txt"
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                f"private_key_dir={shlex.quote(str(pathlib.Path(temporary) / 'keys'))}\n"
                'mkdir -p "$private_key_dir"\n'
                "docker() {\n"
                f"  printf '%s\\n' \"$*\" >> {shlex.quote(str(command_log))}\n"
                '  case " $* " in\n'
                '    *" sign-blob "*) printf \'%s\\n\' \'{"messageSignature":{"signature":"MEUCIQCanG6y2JAiaAAEk4eI3d9LcCJgmDNKU2ZnRzhJJSySXgIgZh4ClriJ/vjNcMAq3ylRHMlHMHg4tGCO9Cf5EfHR4kw="}}\' >"$OUTPUT_DIR/baseline/cosign.bundle.json" ;;\n'
                "  esac\n"
                '  case " $* " in\n'
                '    *" /workspace/tampered.oci.tar"*|*" /other/image.oci.tar"*) return 1 ;;\n'
                "  esac\n"
                "  return 0\n"
                "}\n"
                "sign_and_verify_archive baseline\n"
                f"grep -Fq -- {shlex.quote(f'source={output}/candidate,target=/other,readonly')} {shlex.quote(str(command_log))}\n"
            )
            self.assertEqual(0, result.returncode, result.stderr)

    def test_cosign_v3_offline_signing_drops_deprecated_tlog_upload_flag(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        signing = text.split("sign_and_verify_archive() {", maxsplit=1)[1].split(
            "\n}\n\nwrite_verification_verdict", maxsplit=1
        )[0]
        self.assertNotIn("--tlog-upload", signing)

    def test_advisory_loads_verified_local_images_for_delivery_consumer(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        self.assertIn("load_role_image_object baseline", text)
        self.assertIn("load_role_image_object candidate", text)
        loader = text.split("load_role_image_object() {", maxsplit=1)[1].split(
            "\n}\n\nvalidate_live_sbom", maxsplit=1
        )[0]
        self.assertIn("docker image load --input", loader)
        self.assertIn("docker image inspect --format", loader)
        self.assertIn("{{.Id}}|{{index .Config.Labels", loader)
        self.assertIn('"${LOCAL_IMAGE_REF[$role]}"', loader)
        self.assertIn("role-image-load-identity-mismatch", loader)

    def test_advisory_converts_once_and_loads_only_portable_docker_archives(
        self,
    ) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        derive = text.split("derive_subject_tuple() {", maxsplit=1)[1].split(
            "\n}\n\nload_role_image_object", maxsplit=1
        )[0]
        loader = text.split("load_role_image_object() {", maxsplit=1)[1].split(
            "\n}\n\nvalidate_live_sbom", maxsplit=1
        )[0]
        self.assertIn("--convert-oci-to-docker-load", derive)
        self.assertIn("image.docker.tar", derive)
        self.assertIn("OCI_MANIFEST_DIGEST", derive)
        self.assertIn("DOCKER_ARCHIVE_SHA256", derive)
        self.assertIn("LOCAL_IMAGE_REF", derive)
        self.assertIn('docker image load --input "$role_dir/image.docker.tar"', loader)
        self.assertNotIn('docker image load --input "$role_dir/image.oci.tar"', loader)
        self.assertIn('"${LOCAL_IMAGE_REF[$role]}"', loader)
        self.assertIn("RUNTIME_IMAGE_ID", loader)
        self.assertIn("RUNTIME_IDENTITY_KIND", loader)

    def test_verdict_v2_and_pair_v3_bind_complete_runtime_identity(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        verdict = text.split("write_verification_verdict() {", maxsplit=1)[1].split(
            "\n}\n\npublish_verification_verdicts", maxsplit=1
        )[0]
        for field in (
            "oci_manifest_digest",
            "image_config_digest",
            "oci_archive_sha256",
            "docker_archive_sha256",
            "local_image_ref",
            "runtime_image_id",
            "runtime_identity_kind",
        ):
            self.assertIn(field, verdict)
        self.assertIn('"schema_version": 2', verdict)
        checker = CHECKER_PATH.read_text(encoding="utf-8")
        self.assertIn('"hyhome-verification-verdict-pair-v3"', checker)
        self.assertIn('"schema_version": 3', checker)

    def test_cosign_v3_offline_signing_uses_explicit_empty_service_config(self) -> None:
        config = json.loads(COSIGN_OFFLINE_SIGNING_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(
            {
                "mediaType": "application/vnd.dev.sigstore.signingconfig.v0.2+json",
                "rekorTlogConfig": {},
                "tsaConfig": {},
            },
            config,
        )

        text = WRAPPER.read_text(encoding="utf-8")
        signing = text.split("sign_and_verify_archive() {", maxsplit=1)[1].split(
            "\n}\n\nwrite_verification_verdict", maxsplit=1
        )[0]
        sign_commands = [
            line.strip()
            for line in signing.splitlines()
            if line.strip().startswith("docker run ") and " sign-blob " in line
        ]
        self.assertEqual(1, len(sign_commands))
        self.assertIn("--network none", sign_commands[0])
        self.assertIn(
            "--signing-config /policy/cosign-offline-signing-config.json",
            sign_commands[0],
        )
        self.assertNotIn("--use-signing-config", sign_commands[0])
        self.assertIn(
            "target=/policy/cosign-offline-signing-config.json,readonly",
            sign_commands[0],
        )

    def test_cosign_v3_offline_signing_uses_bundle_and_explicit_trusted_root(
        self,
    ) -> None:
        trusted_root = json.loads(
            COSIGN_OFFLINE_TRUSTED_ROOT.read_text(encoding="utf-8")
        )
        self.assertEqual(
            {"mediaType": "application/vnd.dev.sigstore.trustedroot+json;version=0.1"},
            trusted_root,
        )

        text = WRAPPER.read_text(encoding="utf-8")
        signing = text.split("sign_and_verify_archive() {", maxsplit=1)[1].split(
            "\n}\n\nwrite_verification_verdict", maxsplit=1
        )[0]
        sign_commands = [
            line.strip()
            for line in signing.splitlines()
            if line.strip().startswith("docker run ") and " sign-blob " in line
        ]
        verify_commands = [
            line.strip()
            for line in signing.splitlines()
            if line.strip().startswith(("docker run ", "if docker run "))
            and " verify-blob " in line
        ]
        self.assertEqual(1, len(sign_commands))
        self.assertEqual(3, len(verify_commands))
        self.assertNotIn("--new-bundle-format=false", sign_commands[0])
        self.assertIn(
            "--trusted-root /policy/cosign-offline-trusted-root.json",
            sign_commands[0],
        )
        self.assertIn(
            "target=/policy/cosign-offline-trusted-root.json,readonly",
            sign_commands[0],
        )
        self.assertNotIn('bundle.get("messageSignature", {}).get("signature")', signing)
        self.assertNotIn("cosign.signature", signing)
        for command in verify_commands:
            self.assertIn("--network none", command)
            self.assertIn("--insecure-ignore-tlog=true", command)
            self.assertIn(
                "--trusted-root /policy/cosign-offline-trusted-root.json", command
            )
            self.assertIn(
                "target=/policy/cosign-offline-trusted-root.json,readonly", command
            )
            self.assertIn("--bundle /workspace/cosign.bundle.json", command)
            self.assertNotIn("--signature", command)

    def test_cross_role_signature_acceptance_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "supply-chain"
            (output / "baseline").mkdir(parents=True)
            (output / "candidate").mkdir()
            for role in ("baseline", "candidate"):
                (output / role / "image.oci.tar").write_bytes(b"archive")
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                f"private_key_dir={shlex.quote(str(pathlib.Path(temporary) / 'keys'))}\n"
                'mkdir -p "$private_key_dir"\n'
                "docker() {\n"
                '  case " $* " in\n'
                '    *" sign-blob "*) printf \'%s\\n\' \'{"messageSignature":{"signature":"MEUCIQCanG6y2JAiaAAEk4eI3d9LcCJgmDNKU2ZnRzhJJSySXgIgZh4ClriJ/vjNcMAq3ylRHMlHMHg4tGCO9Cf5EfHR4kw="}}\' >"$OUTPUT_DIR/baseline/cosign.bundle.json" ;;\n'
                "  esac\n"
                '  case " $* " in\n'
                '    *" /workspace/tampered.oci.tar"*) return 1 ;;\n'
                "  esac\n"
                "  return 0\n"
                "}\n"
                "sign_and_verify_archive baseline\n"
            )
            self.assertEqual(60, result.returncode)
            self.assertIn("wrong-subject-archive-accepted", result.stderr)
