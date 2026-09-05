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


class SupplyChainSecureOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_checker()

    @staticmethod
    def write_verdict(path: pathlib.Path, role: str) -> None:
        config = "sha256:" + (("a" if role == "baseline" else "c") * 64)
        payload = {
            "build_context_sha256": CANDIDATE_SUBJECT["build_context_sha256"],
            "docker_archive_sha256": "sha256:"
            + (("3" if role == "baseline" else "4") * 64),
            "exception_id": None,
            "image_config_digest": config,
            "local_image_ref": (
                f"hyhome.local/sample-web-service:{role}-"
                f"{config.removeprefix('sha256:')}"
            ),
            "oci_archive_sha256": "sha256:"
            + (("b" if role == "baseline" else "d") * 64),
            "oci_manifest_digest": "sha256:"
            + (("1" if role == "baseline" else "2") * 64),
            "policy_id": "sample-service-local-v1",
            "producer_spec": "contract:sample-service-supply-chain-v2",
            "redaction_status": "passed",
            "role": role,
            "runtime_identity_kind": "config-digest",
            "runtime_image_id": config,
            "schema_version": 2,
            "source_revision": SOURCE_REVISION,
            "verified_at": "2026-07-23T00:00:00Z",
            "verdict": "accepted",
        }
        path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
        path.chmod(0o600)

    def test_secure_pair_publication_is_manifest_committed_and_mode_0600(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            base.mkdir(mode=0o700)
            identity = self.checker.prepare_secure_output_directory(
                base, HANDOFF_RELATIVE
            )
            output = base / HANDOFF_RELATIVE
            self.assertEqual(0o700, stat.S_IMODE(output.stat().st_mode))
            private = pathlib.Path(temporary) / "private"
            private.mkdir(mode=0o700)
            baseline = private / "baseline.json"
            candidate = private / "candidate.json"
            self.write_verdict(baseline, "baseline")
            self.write_verdict(candidate, "candidate")

            manifest = self.checker.publish_verdict_pair(
                base,
                HANDOFF_RELATIVE,
                identity,
                baseline,
                candidate,
                SOURCE_REVISION,
                CANDIDATE_SUBJECT["build_context_sha256"],
            )
            self.assertEqual(3, manifest["schema_version"])
            self.assertEqual(
                "hyhome-verification-verdict-pair-v3", manifest["generation"]
            )
            self.assertEqual({"baseline", "candidate"}, set(manifest["subjects"]))
            self.assertEqual({"baseline", "candidate"}, set(manifest["verdict_sha256"]))
            for name in (
                "verification-verdict.baseline.json",
                "verification-verdict.candidate.json",
                "verification-verdict.pair.json",
            ):
                self.assertEqual(
                    0o600, stat.S_IMODE((output / name).stat().st_mode), name
                )

    def test_pair_v3_binds_complete_distinct_runtime_identity_tuple(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            base.mkdir(mode=0o700)
            identity = self.checker.prepare_secure_output_directory(
                base, HANDOFF_RELATIVE
            )
            private = pathlib.Path(temporary) / "private"
            private.mkdir(mode=0o700)
            paths: dict[str, pathlib.Path] = {}
            for role, digit in (("baseline", "1"), ("candidate", "2")):
                config = "sha256:" + digit * 64
                payload = {
                    "build_context_sha256": CANDIDATE_SUBJECT["build_context_sha256"],
                    "docker_archive_sha256": "sha256:"
                    + ("3" if role == "baseline" else "4") * 64,
                    "exception_id": None,
                    "image_config_digest": config,
                    "local_image_ref": (
                        f"hyhome.local/sample-web-service:{role}-"
                        f"{config.removeprefix('sha256:')}"
                    ),
                    "oci_archive_sha256": "sha256:"
                    + ("5" if role == "baseline" else "6") * 64,
                    "oci_manifest_digest": "sha256:"
                    + ("7" if role == "baseline" else "8") * 64,
                    "policy_id": "sample-service-local-v1",
                    "producer_spec": "contract:sample-service-supply-chain-v2",
                    "redaction_status": "passed",
                    "role": role,
                    "runtime_identity_kind": (
                        "config-digest"
                        if role == "baseline"
                        else "docker-target-digest"
                    ),
                    "runtime_image_id": (
                        config if role == "baseline" else "sha256:" + "a" * 64
                    ),
                    "schema_version": 2,
                    "source_revision": SOURCE_REVISION,
                    "verified_at": "2026-07-23T00:00:00Z",
                    "verdict": "accepted",
                }
                paths[role] = private / f"{role}.json"
                paths[role].write_text(
                    json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8"
                )
                paths[role].chmod(0o600)

            manifest = self.checker.publish_verdict_pair(
                base,
                HANDOFF_RELATIVE,
                identity,
                paths["baseline"],
                paths["candidate"],
                SOURCE_REVISION,
                CANDIDATE_SUBJECT["build_context_sha256"],
            )
            self.assertEqual(3, manifest["schema_version"])
            self.assertEqual(
                "hyhome-verification-verdict-pair-v3", manifest["generation"]
            )
            self.assertEqual(
                {
                    "oci_manifest_digest",
                    "image_config_digest",
                    "oci_archive_sha256",
                    "docker_archive_sha256",
                    "local_image_ref",
                    "runtime_image_id",
                    "runtime_identity_kind",
                },
                set(manifest["subjects"]["baseline"]),
            )
            for field in (
                "oci_manifest_digest",
                "image_config_digest",
                "oci_archive_sha256",
                "docker_archive_sha256",
                "local_image_ref",
                "runtime_image_id",
            ):
                self.assertNotEqual(
                    manifest["subjects"]["baseline"][field],
                    manifest["subjects"]["candidate"][field],
                    field,
                )

    def test_secure_output_rejects_ancestor_and_final_symlinks_or_bad_mode(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            outside = pathlib.Path(temporary) / "outside"
            base.mkdir(mode=0o700)
            outside.mkdir(mode=0o700)
            (base / "_workspace").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(self.checker.SecureOutputError):
                self.checker.prepare_secure_output_directory(base, HANDOFF_RELATIVE)

        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            base.mkdir(mode=0o700)
            identity = self.checker.prepare_secure_output_directory(
                base, HANDOFF_RELATIVE
            )
            output = base / HANDOFF_RELATIVE
            private = pathlib.Path(temporary) / "private"
            private.mkdir(mode=0o700)
            baseline = private / "baseline.json"
            candidate = private / "candidate.json"
            self.write_verdict(baseline, "baseline")
            self.write_verdict(candidate, "candidate")

            output.chmod(0o755)
            with self.assertRaises(self.checker.SecureOutputError):
                self.checker.publish_verdict_pair(
                    base,
                    HANDOFF_RELATIVE,
                    identity,
                    baseline,
                    candidate,
                    SOURCE_REVISION,
                    CANDIDATE_SUBJECT["build_context_sha256"],
                )
            output.chmod(0o700)
            outside = pathlib.Path(temporary) / "outside.json"
            outside.write_text("preserve\n", encoding="utf-8")
            (output / "verification-verdict.baseline.json").symlink_to(outside)
            with self.assertRaises(self.checker.SecureOutputError):
                self.checker.publish_verdict_pair(
                    base,
                    HANDOFF_RELATIVE,
                    identity,
                    baseline,
                    candidate,
                    SOURCE_REVISION,
                    CANDIDATE_SUBJECT["build_context_sha256"],
                )
            self.assertEqual("preserve\n", outside.read_text(encoding="utf-8"))

    def test_secure_output_rejects_path_swap_and_interrupted_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            base.mkdir(mode=0o700)
            identity = self.checker.prepare_secure_output_directory(
                base, HANDOFF_RELATIVE
            )
            output = base / HANDOFF_RELATIVE
            displaced = output.with_name("supply-chain.displaced")
            output.rename(displaced)
            output.mkdir(mode=0o700)
            private = pathlib.Path(temporary) / "private"
            private.mkdir(mode=0o700)
            baseline = private / "baseline.json"
            candidate = private / "candidate.json"
            self.write_verdict(baseline, "baseline")
            self.write_verdict(candidate, "candidate")
            with self.assertRaises(self.checker.SecureOutputError):
                self.checker.publish_verdict_pair(
                    base,
                    HANDOFF_RELATIVE,
                    identity,
                    baseline,
                    candidate,
                    SOURCE_REVISION,
                    CANDIDATE_SUBJECT["build_context_sha256"],
                )
            self.assertEqual([], list(output.iterdir()))

        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            base.mkdir(mode=0o700)
            identity = self.checker.prepare_secure_output_directory(
                base, HANDOFF_RELATIVE
            )
            output = base / HANDOFF_RELATIVE
            private = pathlib.Path(temporary) / "private"
            private.mkdir(mode=0o700)
            baseline = private / "baseline.json"
            candidate = private / "candidate.json"
            self.write_verdict(baseline, "baseline")
            self.write_verdict(candidate, "candidate")
            candidate.chmod(0o644)
            with self.assertRaises(self.checker.SecureOutputError):
                self.checker.publish_verdict_pair(
                    base,
                    HANDOFF_RELATIVE,
                    identity,
                    baseline,
                    candidate,
                    SOURCE_REVISION,
                    CANDIDATE_SUBJECT["build_context_sha256"],
                )
            self.assertFalse((output / "verification-verdict.pair.json").exists())
            self.assertFalse((output / "verification-verdict.baseline.json").exists())
            self.assertFalse((output / "verification-verdict.candidate.json").exists())


if __name__ == "__main__":
    unittest.main()
