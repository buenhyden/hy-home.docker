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


ROOT = pathlib.Path(__file__).resolve().parents[3]
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


class SupplyChainPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_checker()

    def load_fixture(self, name: str):
        return self.checker.load_json(FIXTURES / name)

    def test_tool_manifest_pins_are_exact(self) -> None:
        registry = self.checker.load_json(TOOL_REGISTRY)
        self.assertEqual([], self.checker.validate_tool_registry(registry))
        by_name = {row["name"]: row for row in registry["tools"]}
        for name, (target_digest, config_digest) in OBSERVED_TOOL_IDENTITIES.items():
            with self.subTest(name=name):
                self.assertEqual(
                    target_digest,
                    by_name[name]["target_descriptor_digest"],
                )
                self.assertEqual(config_digest, by_name[name]["config_id"])
                self.assertNotEqual(
                    by_name[name]["target_descriptor_digest"],
                    by_name[name]["config_id"],
                )

        digestless = copy.deepcopy(registry)
        digestless["tools"][0]["digest"] = ""
        self.assertIn(
            "tool-digest-invalid",
            self.checker.validate_tool_registry(digestless),
        )

        configless = copy.deepcopy(registry)
        configless["tools"][0]["config_id"] = ""
        self.assertIn(
            "tool-config-id-invalid",
            self.checker.validate_tool_registry(configless),
        )

    def test_private_docker_save_config_body_is_hashed_independently(self) -> None:
        config_body = b'{"architecture":"amd64","os":"linux","rootfs":{"type":"layers","diff_ids":[]}}'
        config_digest = "sha256:" + hashlib.sha256(config_body).hexdigest()
        with tempfile.TemporaryDirectory(
            prefix="docker-save-config-", dir="/tmp"
        ) as raw:
            directory = pathlib.Path(raw)
            directory.chmod(0o700)
            archive_path = directory / "image.tar"
            manifest_body = json.dumps(
                [
                    {
                        "Config": f"{config_digest.removeprefix('sha256:')}.json",
                        "Layers": [],
                        "RepoTags": [],
                    }
                ],
                separators=(",", ":"),
            ).encode("utf-8")
            with tarfile.open(
                archive_path, "w", format=tarfile.USTAR_FORMAT
            ) as archive:
                for name, body in (
                    ("manifest.json", manifest_body),
                    (f"{config_digest.removeprefix('sha256:')}.json", config_body),
                ):
                    member = tarfile.TarInfo(name)
                    member.size = len(body)
                    archive.addfile(member, io.BytesIO(body))
            archive_path.chmod(0o600)
            self.assertEqual(
                config_digest,
                self.checker.inspect_docker_save_archive_config_digest(archive_path),
            )

    def test_policy_and_exception_registry_are_fail_closed(self) -> None:
        policy = self.checker.load_json(POLICY)
        exceptions = self.checker.load_json(EXCEPTIONS)
        self.assertEqual([], self.checker.validate_policy(policy))
        self.assertEqual(
            [],
            self.checker.validate_exceptions(
                exceptions,
                policy,
                CANDIDATE_SUBJECT["image_config_digest"],
            ),
        )

        unowned = copy.deepcopy(exceptions)
        unowned["exceptions"][0]["owner_role"] = ""
        self.assertIn(
            "exception-owner-invalid",
            self.checker.validate_exceptions(
                unowned,
                policy,
                CANDIDATE_SUBJECT["image_config_digest"],
            ),
        )

    def test_roles_have_distinct_subjects(self) -> None:
        self.assertEqual(
            [],
            self.checker.validate_subject_tuples([BASELINE_SUBJECT, CANDIDATE_SUBJECT]),
        )

        duplicate = copy.deepcopy(BASELINE_SUBJECT)
        duplicate["role"] = "candidate"
        self.assertIn(
            "subject-tuples-not-distinct",
            self.checker.validate_subject_tuples([BASELINE_SUBJECT, duplicate]),
        )

    def test_sample_service_sbom_valid_cdx_json(self) -> None:
        self.assertEqual(
            [],
            self.checker.validate_sbom_subject(
                self.load_fixture("sample-service-sbom.valid.cdx.json"),
                CANDIDATE_SUBJECT,
            ),
        )

    def test_sample_service_sbom_subject_mismatch_cdx_json(self) -> None:
        self.assertIn(
            "sbom-image-config-subject-mismatch",
            self.checker.validate_sbom_subject(
                cyclonedx_report(image_config_digest="sha256:" + "a" * 64),
                CANDIDATE_SUBJECT,
            ),
        )

    def _write_oci_archive(
        self, path: pathlib.Path, *, tamper_config: bool = False
    ) -> str:
        config = json.dumps(
            {
                "architecture": "amd64",
                "os": "linux",
                "rootfs": {"diff_ids": [], "type": "layers"},
            },
            sort_keys=True,
        ).encode()
        config_digest = hashlib.sha256(config).hexdigest()
        manifest = json.dumps(
            {
                "config": {
                    "digest": f"sha256:{config_digest}",
                    "mediaType": "application/vnd.oci.image.config.v1+json",
                    "size": len(config),
                },
                "layers": [],
                "mediaType": "application/vnd.oci.image.manifest.v1+json",
                "schemaVersion": 2,
            },
            sort_keys=True,
        ).encode()
        manifest_digest = hashlib.sha256(manifest).hexdigest()
        index = json.dumps(
            {
                "manifests": [
                    {
                        "digest": f"sha256:{manifest_digest}",
                        "mediaType": "application/vnd.oci.image.manifest.v1+json",
                        "size": len(manifest),
                    }
                ],
                "mediaType": "application/vnd.oci.image.index.v1+json",
                "schemaVersion": 2,
            },
            sort_keys=True,
        ).encode()
        with tarfile.open(path, "w") as archive:
            for name, content in (
                ("oci-layout", b'{"imageLayoutVersion":"1.0.0"}'),
                ("index.json", index),
                (f"blobs/sha256/{manifest_digest}", manifest),
                (
                    f"blobs/sha256/{config_digest}",
                    b"x" * len(config) if tamper_config else config,
                ),
            ):
                entry = tarfile.TarInfo(name)
                entry.size = len(content)
                archive.addfile(entry, fileobj=io.BytesIO(content))
        path.chmod(0o600)
        return f"sha256:{config_digest}"

    def _write_portable_oci_archive(
        self,
        path: pathlib.Path,
        *,
        mutation: str | None = None,
    ) -> dict[str, str | int]:
        layer_payload = (
            b"x" * 16384 if mutation == "oversized-layer" else b"deterministic-layer\n"
        )
        layer_buffer = io.BytesIO()
        with tarfile.open(
            fileobj=layer_buffer, mode="w", format=tarfile.USTAR_FORMAT
        ) as layer_archive:
            layer_entry = tarfile.TarInfo("layer.txt")
            layer_entry.mode = 0o644
            layer_entry.uid = 0
            layer_entry.gid = 0
            layer_entry.uname = ""
            layer_entry.gname = ""
            layer_entry.mtime = 0
            layer_entry.size = len(layer_payload)
            layer_archive.addfile(layer_entry, io.BytesIO(layer_payload))
        layer_diff = layer_buffer.getvalue()
        if mutation == "corrupt-gzip":
            layer = b"not-a-gzip-stream"
        else:
            layer = gzip.compress(layer_diff, mtime=0)
            if mutation == "gzip-trailing-data":
                layer += b"trailing-data"
        layer_digest = hashlib.sha256(layer).hexdigest()
        layer_diff_id = hashlib.sha256(layer_diff).hexdigest()
        diff_ids = (
            []
            if mutation == "rootfs-cardinality"
            else [
                "sha256:" + "0" * 64
                if mutation == "diff-id-mismatch"
                else f"sha256:{layer_diff_id}"
            ]
        )
        config = json.dumps(
            {
                "architecture": "amd64",
                "config": {
                    "Labels": {"org.hyhome.delivery.rehearsal.role": "baseline"}
                },
                "os": "linux",
                "rootfs": {
                    "diff_ids": diff_ids,
                    "type": "invalid" if mutation == "rootfs-schema" else "layers",
                },
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        config_digest = hashlib.sha256(config).hexdigest()
        manifest = json.dumps(
            {
                "config": {
                    "digest": f"sha256:{config_digest}",
                    "mediaType": (
                        "application/octet-stream"
                        if mutation == "config-media"
                        else "application/vnd.oci.image.config.v1+json"
                    ),
                    "size": len(config) + (1 if mutation == "config-size" else 0),
                },
                "layers": [
                    {
                        "digest": f"sha256:{layer_digest}",
                        "mediaType": (
                            "application/vnd.oci.image.layer.v1.tar"
                            if mutation == "layer-media"
                            else "application/vnd.oci.image.layer.v1.tar+gzip"
                        ),
                        "size": len(layer) + (1 if mutation == "layer-size" else 0),
                    }
                ],
                "mediaType": (
                    "application/octet-stream"
                    if mutation == "manifest-media"
                    else "application/vnd.oci.image.manifest.v1+json"
                ),
                "schemaVersion": 2,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        manifest_digest = hashlib.sha256(manifest).hexdigest()
        index = json.dumps(
            {
                "manifests": [
                    {
                        "digest": f"sha256:{manifest_digest}",
                        "mediaType": (
                            "application/octet-stream"
                            if mutation == "index-manifest-media"
                            else "application/vnd.oci.image.manifest.v1+json"
                        ),
                        "size": len(manifest)
                        + (1 if mutation == "manifest-size" else 0),
                    }
                ],
                "mediaType": (
                    "application/octet-stream"
                    if mutation == "index-media"
                    else "application/vnd.oci.image.index.v1+json"
                ),
                "schemaVersion": 2,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        entries: list[tuple[tarfile.TarInfo, bytes | None]] = []
        for name, content in (
            ("oci-layout", b'{"imageLayoutVersion":"1.0.0"}'),
            ("index.json", index),
            (f"blobs/sha256/{manifest_digest}", manifest),
            (f"blobs/sha256/{config_digest}", config),
            (
                f"blobs/sha256/{layer_digest}",
                b"x" * len(layer) if mutation == "layer-digest" else layer,
            ),
        ):
            entry = tarfile.TarInfo(name)
            entry.size = len(content)
            entries.append((entry, content))
        if mutation == "duplicate-index":
            duplicate = tarfile.TarInfo("index.json")
            duplicate.size = len(index)
            entries.append((duplicate, index))
        elif mutation == "path-traversal":
            traversal = tarfile.TarInfo("../escape")
            traversal.size = 1
            entries.append((traversal, b"x"))
        elif mutation == "symlink":
            link = tarfile.TarInfo("unsafe-link")
            link.type = tarfile.SYMTYPE
            link.linkname = "index.json"
            entries.append((link, None))
        elif mutation == "special":
            fifo = tarfile.TarInfo("unsafe-fifo")
            fifo.type = tarfile.FIFOTYPE
            entries.append((fifo, None))
        with tarfile.open(path, "w", format=tarfile.USTAR_FORMAT) as archive:
            for entry, content in entries:
                archive.addfile(
                    entry,
                    fileobj=None if content is None else io.BytesIO(content),
                )
        raw_tar_mutations = {
            "gnu-longlink",
            "gnu-longname",
            "gnu-sparse",
            "invalid-padding",
            "malformed-header",
            "malformed-pax-record",
            "missing-termination",
            "oversized-base256-member",
            "oversized-logical-member",
            "pax-size-override",
            "pax-sparse-key",
            "trailing-data",
            "truncated-member",
        }
        if mutation in raw_tar_mutations:
            logical_end = sum(
                512 + (((entry.size + 511) // 512) * 512 if entry.isfile() else 0)
                for entry, _ in entries
            )
            body = bytearray(path.read_bytes())
            if mutation in {
                "oversized-base256-member",
                "oversized-logical-member",
            }:
                oversized = tarfile.TarInfo(f"{mutation}.bin")
                oversized.mode = 0o600
                oversized.size = (
                    1 << 40
                    if mutation == "oversized-base256-member"
                    else self.checker.OCI_ARCHIVE_MAX_BYTES + 1
                )
                header_format = (
                    tarfile.GNU_FORMAT
                    if mutation == "oversized-base256-member"
                    else tarfile.USTAR_FORMAT
                )
                header = oversized.tobuf(format=header_format)
                if mutation == "oversized-base256-member":
                    self.assertTrue(header[124] & 0x80)
                body[logical_end : logical_end + 512] = header
            elif mutation == "malformed-header":
                body[0] ^= 1
            elif mutation == "invalid-padding":
                first_entry = entries[0][0]
                self.assertNotEqual(0, first_entry.size % 512)
                body[512 + first_entry.size] = 1
            elif mutation == "truncated-member":
                truncated = tarfile.TarInfo("truncated-member.bin")
                truncated.mode = 0o600
                truncated.size = 1024
                body[logical_end : logical_end + 512] = truncated.tobuf(
                    format=tarfile.USTAR_FORMAT
                )
                body = body[: logical_end + 1024]
            elif mutation == "missing-termination":
                body = body[:logical_end]
            elif mutation == "trailing-data":
                body[logical_end + 1024] = 1
            elif mutation in {"gnu-longlink", "gnu-longname"}:
                long_metadata = tarfile.TarInfo("././@LongLink")
                long_metadata.type = (
                    tarfile.GNUTYPE_LONGLINK
                    if mutation == "gnu-longlink"
                    else tarfile.GNUTYPE_LONGNAME
                )
                long_metadata.size = 4
                body[logical_end : logical_end + 512] = long_metadata.tobuf(
                    format=tarfile.GNU_FORMAT
                )
            elif mutation == "gnu-sparse":
                sparse = tarfile.TarInfo("gnu-sparse.bin")
                sparse.type = tarfile.GNUTYPE_SPARSE
                sparse.size = 0
                body[logical_end : logical_end + 512] = sparse.tobuf(
                    format=tarfile.GNU_FORMAT
                )
            elif mutation in {
                "malformed-pax-record",
                "pax-size-override",
                "pax-sparse-key",
            }:
                pax_member = tarfile.TarInfo(f"{mutation}.bin")
                pax_member.mode = 0o600
                pax_member.size = 0
                if mutation == "pax-size-override":
                    pax_member.pax_headers = {
                        "size": str(self.checker.OCI_ARCHIVE_MAX_BYTES + 1)
                    }
                elif mutation == "pax-sparse-key":
                    pax_member.pax_headers = {"GNU.sparse.realsize": "0"}
                else:
                    pax_member.pax_headers = {"comment": "malformed"}
                pax_sequence = bytearray(pax_member.tobuf(format=tarfile.PAX_FORMAT))
                if mutation == "malformed-pax-record":
                    pax_sequence[512] = ord("x")
                body[logical_end : logical_end + len(pax_sequence)] = pax_sequence
            path.write_bytes(body)
        path.chmod(0o600)
        return {
            "image_config_digest": f"sha256:{config_digest}",
            "oci_manifest_digest": f"sha256:{manifest_digest}",
            "layer_digest": f"sha256:{layer_digest}",
            "layer_diff_id": f"sha256:{layer_diff_id}",
            "layer_uncompressed_size": len(layer_diff),
        }

    def test_oci_archive_config_digest_is_bound_to_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = pathlib.Path(temporary) / "image.oci.tar"
            expected = self._write_oci_archive(archive)
            self.assertEqual(
                expected, self.checker.inspect_oci_archive_config_digest(archive)
            )

    def test_oci_archive_config_digest_rejects_tampered_blob(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = pathlib.Path(temporary) / "image.oci.tar"
            self._write_oci_archive(archive, tamper_config=True)
            with self.assertRaisesRegex(ValueError, "config-blob-digest-mismatch"):
                self.checker.inspect_oci_archive_config_digest(archive)

    def test_oci_archive_config_digest_rejects_oversized_input_before_read(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            archive = root / "oversized.oci.tar"
            archive.touch(mode=0o600)
            with archive.open("r+b") as handle:
                handle.truncate(self.checker.OCI_ARCHIVE_MAX_BYTES + 1)
            with mock.patch.object(
                pathlib.Path,
                "read_bytes",
                side_effect=AssertionError("unbounded archive read attempted"),
            ):
                with self.assertRaisesRegex(
                    ValueError, "oci-archive-size-limit-exceeded"
                ):
                    self.checker.inspect_oci_archive_config_digest(archive)

    def test_oci_archive_config_digest_rejects_symlink_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            target = root / "image.oci.tar"
            self._write_oci_archive(target)
            archive = root / "image.link.oci.tar"
            archive.symlink_to(target.name)
            with self.assertRaisesRegex(
                ValueError, "oci-archive-private-input-invalid"
            ):
                self.checker.inspect_oci_archive_config_digest(archive)

    def test_portable_docker_load_archive_is_deterministic_and_minimal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            source = root / "image.oci.tar"
            expected = self._write_portable_oci_archive(source)
            first = root / "image.first.docker.tar"
            second = root / "image.second.docker.tar"

            first_result = self.checker.convert_oci_archive_to_docker_load_archive(
                source, first, "baseline"
            )
            second_result = self.checker.convert_oci_archive_to_docker_load_archive(
                source, second, "baseline"
            )

            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(0o600, stat.S_IMODE(first.stat().st_mode))
            self.assertEqual(
                expected["image_config_digest"], first_result["image_config_digest"]
            )
            self.assertEqual(
                expected["oci_manifest_digest"], first_result["oci_manifest_digest"]
            )
            self.assertEqual(
                "hyhome.local/sample-web-service:baseline-"
                + expected["image_config_digest"].removeprefix("sha256:"),
                first_result["local_image_ref"],
            )
            self.assertEqual(first_result, second_result)
            self.assertEqual(
                "sha256:" + hashlib.sha256(first.read_bytes()).hexdigest(),
                first_result["docker_archive_sha256"],
            )
            with tarfile.open(first, "r:") as archive:
                names = archive.getnames()
                self.assertEqual(len(names), len(set(names)))
                self.assertEqual(
                    sorted(
                        (
                            expected["image_config_digest"].removeprefix("sha256:")
                            + ".json",
                            expected["layer_digest"].removeprefix("sha256:") + ".tar",
                            "manifest.json",
                        )
                    ),
                    names,
                )
                self.assertNotIn("index.json", names)
                self.assertNotIn("oci-layout", names)
                manifest = json.load(archive.extractfile("manifest.json"))
            self.assertEqual([first_result["local_image_ref"]], manifest[0]["RepoTags"])

    def test_portable_converter_rejects_unsafe_or_unbound_oci_members(self) -> None:
        cases = {
            "duplicate-index": "oci-archive-member-duplicate",
            "path-traversal": "oci-archive-member-path-invalid",
            "symlink": "oci-archive-member-type-invalid",
            "special": "oci-archive-member-type-invalid",
            "manifest-size": "oci-manifest-blob-size-mismatch",
            "config-size": "oci-config-blob-size-mismatch",
            "layer-size": "oci-layer-blob-size-mismatch",
            "layer-digest": "oci-layer-blob-digest-mismatch",
            "index-media": "oci-index-schema-or-media-type-invalid",
            "index-manifest-media": "oci-index-manifest-media-type-invalid",
            "manifest-media": "oci-manifest-schema-or-media-type-invalid",
            "config-media": "oci-config-media-type-invalid",
            "layer-media": "oci-layer-media-type-not-portable",
            "rootfs-cardinality": "oci-rootfs-layer-cardinality-mismatch",
            "rootfs-schema": "oci-config-rootfs-invalid",
            "diff-id-mismatch": "oci-layer-diff-id-mismatch",
            "corrupt-gzip": "oci-layer-gzip-invalid",
            "gzip-trailing-data": "oci-layer-gzip-trailing-data",
            "gnu-longlink": "oci-archive-longname-type-invalid",
            "gnu-longname": "oci-archive-longname-type-invalid",
            "gnu-sparse": "oci-archive-sparse-type-invalid",
            "invalid-padding": "oci-archive-padding-invalid",
            "malformed-header": "oci-archive-header-invalid",
            "malformed-pax-record": "oci-archive-pax-header-invalid",
            "missing-termination": "oci-archive-termination-invalid",
            "oversized-base256-member": "oci-archive-member-size-limit-exceeded",
            "oversized-logical-member": "oci-archive-member-size-limit-exceeded",
            "pax-sparse-key": "oci-archive-sparse-type-invalid",
            "trailing-data": "oci-archive-trailing-data-invalid",
            "truncated-member": "oci-archive-truncated",
        }
        for mutation, reason in cases.items():
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = pathlib.Path(temporary)
                root.chmod(0o700)
                source = root / "image.oci.tar"
                target = root / "image.docker.tar"
                self._write_portable_oci_archive(source, mutation=mutation)
                with self.assertRaisesRegex(ValueError, reason):
                    self.checker.convert_oci_archive_to_docker_load_archive(
                        source, target, "baseline"
                    )
                self.assertFalse(target.exists())

    def test_portable_converter_bounds_uncompressed_layer_size(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            source = root / "image.oci.tar"
            target = root / "image.docker.tar"
            expected = self._write_portable_oci_archive(
                source, mutation="oversized-layer"
            )
            original = getattr(self.checker, "OCI_LAYER_MAX_UNCOMPRESSED_BYTES", None)
            setattr(
                self.checker,
                "OCI_LAYER_MAX_UNCOMPRESSED_BYTES",
                int(expected["layer_uncompressed_size"]) - 1,
            )
            try:
                with self.assertRaisesRegex(
                    ValueError, "oci-layer-uncompressed-size-limit-exceeded"
                ):
                    self.checker.convert_oci_archive_to_docker_load_archive(
                        source, target, "baseline"
                    )
            finally:
                if original is None:
                    delattr(self.checker, "OCI_LAYER_MAX_UNCOMPRESSED_BYTES")
                else:
                    self.checker.OCI_LAYER_MAX_UNCOMPRESSED_BYTES = original
            self.assertFalse(target.exists())

    def test_portable_converter_rejects_outer_compressed_oci_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            source = root / "image.oci.tar.gz"
            target = root / "image.docker.tar"
            self._write_portable_oci_archive(source)
            source.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            source.chmod(0o600)
            with self.assertRaisesRegex(
                ValueError, "oci-archive-outer-compression-invalid"
            ):
                self.checker.convert_oci_archive_to_docker_load_archive(
                    source, target, "baseline"
                )
            self.assertFalse(target.exists())

    def test_portable_converter_accepts_uncompressed_pax_oci_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            ustar_source = root / "image.ustar.oci.tar"
            pax_source = root / "image.pax.oci.tar"
            first_target = root / "image.first.docker.tar"
            second_target = root / "image.second.docker.tar"
            expected = self._write_portable_oci_archive(ustar_source)
            with tarfile.open(ustar_source, "r:") as source_archive:
                with tarfile.open(
                    pax_source,
                    "w",
                    format=tarfile.PAX_FORMAT,
                    pax_headers={"comment": "global-build-metadata"},
                ) as pax_archive:
                    for member in source_archive:
                        copied = copy.copy(member)
                        if copied.name == "index.json":
                            copied.pax_headers = {
                                "comment": (
                                    "buildx-compatible-oci-layout without "
                                    "GNU.sparse extensions"
                                ),
                                "size": str(copied.size),
                            }
                        handle = (
                            source_archive.extractfile(member)
                            if member.isfile()
                            else None
                        )
                        pax_archive.addfile(copied, handle)
            pax_source.chmod(0o600)
            first_result = self.checker.convert_oci_archive_to_docker_load_archive(
                pax_source, first_target, "baseline"
            )
            second_result = self.checker.convert_oci_archive_to_docker_load_archive(
                pax_source, second_target, "baseline"
            )
            self.assertEqual(
                expected["image_config_digest"],
                first_result["image_config_digest"],
            )
            self.assertEqual(first_result, second_result)
            self.assertEqual(first_target.read_bytes(), second_target.read_bytes())

    def test_oci_tar_preflight_rejects_oversized_pax_size_override(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            source = root / "image.pax-size-override.oci.tar"
            self._write_portable_oci_archive(source, mutation="pax-size-override")
            with self.assertRaisesRegex(
                ValueError, "oci-archive-member-size-limit-exceeded"
            ):
                self.checker._preflight_uncompressed_oci_tar(source.read_bytes())

    def test_portable_converter_rejects_oversized_hidden_pax_metadata(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            ustar_source = root / "image.ustar.oci.tar"
            self._write_portable_oci_archive(ustar_source)
            original_limit = self.checker.OCI_METADATA_MAX_BYTES
            self.checker.OCI_METADATA_MAX_BYTES = 512
            try:
                for scope in ("extended", "global", "cumulative"):
                    with self.subTest(scope=scope):
                        pax_source = root / f"image.{scope}.pax.oci.tar"
                        target = root / f"image.{scope}.docker.tar"
                        global_headers = (
                            {"comment": "g" * 2048} if scope == "global" else None
                        )
                        with tarfile.open(ustar_source, "r:") as source_archive:
                            with tarfile.open(
                                pax_source,
                                "w",
                                format=tarfile.PAX_FORMAT,
                                pax_headers=global_headers,
                            ) as pax_archive:
                                cumulative_headers = 0
                                for member in source_archive:
                                    copied = copy.copy(member)
                                    if (
                                        scope == "extended"
                                        and copied.name == "index.json"
                                    ):
                                        copied.pax_headers = {"comment": "x" * 2048}
                                    elif (
                                        scope == "cumulative"
                                        and copied.isfile()
                                        and cumulative_headers < 2
                                    ):
                                        copied.pax_headers = {"comment": "c" * 300}
                                        cumulative_headers += 1
                                    handle = (
                                        source_archive.extractfile(member)
                                        if member.isfile()
                                        else None
                                    )
                                    pax_archive.addfile(copied, handle)
                        pax_source.chmod(0o600)
                        with self.assertRaisesRegex(
                            ValueError,
                            "oci-archive-pax-metadata-size-limit-exceeded",
                        ):
                            self.checker.convert_oci_archive_to_docker_load_archive(
                                pax_source, target, "baseline"
                            )
                        self.assertFalse(target.exists())
            finally:
                self.checker.OCI_METADATA_MAX_BYTES = original_limit

    def test_portable_converter_rejects_non_role_local_reference_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            root.chmod(0o700)
            source = root / "image.oci.tar"
            self._write_portable_oci_archive(source)
            with self.assertRaisesRegex(ValueError, "local-image-role-invalid"):
                self.checker.convert_oci_archive_to_docker_load_archive(
                    source, root / "image.docker.tar", "canary"
                )

    def test_grype_clean_json(self) -> None:
        result = self.checker.evaluate_grype_fixture(
            self.load_fixture("grype.clean.json"),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("accepted", result["verdict"])
        self.assertIsNone(result["exception_id"])

    def test_grype_high_without_exception_json(self) -> None:
        result = self.checker.evaluate_grype_fixture(
            grype_report(matches=[grype_match()]),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("review-finding-without-exception", result["reason"])

    def test_grype_high_with_valid_exception_json(self) -> None:
        result = self.checker.evaluate_grype_fixture(
            grype_report(matches=[grype_match()], exception_id="EXC-SSC-0001"),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("accepted", result["verdict"])
        self.assertEqual("EXC-SSC-0001", result["exception_id"])

    def test_grype_valid_exception_cannot_short_circuit_later_critical(self) -> None:
        result = self.checker.evaluate_grype_fixture(
            grype_report(
                matches=[
                    grype_match(),
                    grype_match(
                        vulnerability_id="CVE-2099-0002",
                        severity="Critical",
                        package="critical-runtime-package",
                    ),
                ],
                exception_id="EXC-SSC-0001",
            ),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("blocking-finding-without-exception", result["reason"])
        self.assertIsNone(result["exception_id"])

    def test_embedded_exception_is_bound_to_each_match(self) -> None:
        fixture = grype_report(
            matches=[
                grype_match(),
                grype_match(
                    vulnerability_id="CVE-2099-0002",
                    severity="Critical",
                    package="critical-runtime-package",
                ),
            ],
            exception=self.checker.load_json(EXCEPTIONS)["exceptions"][0],
        )
        result = self.checker.evaluate_grype_fixture(
            fixture,
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("blocking-finding-without-exception", result["reason"])

    def test_grype_wrong_subject_exception_is_rejected(self) -> None:
        exceptions = self.checker.load_json(EXCEPTIONS)
        exceptions["exceptions"][0]["subject_digest"] = BASELINE_SUBJECT[
            "image_config_digest"
        ]
        result = self.checker.evaluate_grype_fixture(
            grype_report(matches=[grype_match()], exception_id="EXC-SSC-0001"),
            self.checker.load_json(POLICY),
            exceptions,
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("review-finding-without-exception", result["reason"])

    def test_grype_expired_exception_json(self) -> None:
        exception = self.checker.load_json(EXCEPTIONS)["exceptions"][0]
        exception["expires_on"] = "1970-01-01"
        result = self.checker.evaluate_grype_fixture(
            grype_report(matches=[grype_match()], exception=exception),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("exception-expired", result["reason"])

    def test_grype_raw_finding_leakage_is_rejected(self) -> None:
        fixture = grype_report(matches=[grype_match()])
        fixture["matches"][0]["vulnerability"]["description"] = "raw finding"
        result = self.checker.evaluate_grype_fixture(
            fixture,
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("raw-finding-leakage", result["reason"])

    def test_provenance_valid_intoto_json(self) -> None:
        self.assertEqual(
            [],
            self.checker.validate_provenance_subject(
                self.load_fixture("provenance.valid.intoto.json"),
                CANDIDATE_SUBJECT,
            ),
        )

    def test_provenance_subject_mismatch_intoto_json(self) -> None:
        self.assertIn(
            "provenance-archive-subject-mismatch",
            self.checker.validate_provenance_subject(
                provenance_statement(archive_digest="sha256:" + "b" * 64),
                CANDIDATE_SUBJECT,
            ),
        )

    def test_provenance_binds_full_build_context_digest(self) -> None:
        provenance = self.load_fixture("provenance.valid.intoto.json")
        self.assertEqual(
            [], self.checker.validate_provenance_subject(provenance, CANDIDATE_SUBJECT)
        )
        wrong_context = copy.deepcopy(CANDIDATE_SUBJECT)
        wrong_context["build_context_sha256"] = "sha256:" + ("f" * 64)
        self.assertIn(
            "provenance-build-context-mismatch",
            self.checker.validate_provenance_subject(provenance, wrong_context),
        )

    def test_cosign_verify_valid_json(self) -> None:
        self.assertEqual(
            [],
            self.checker.validate_signature_fixture(
                self.load_fixture("cosign.verify.valid.json"), CANDIDATE_SUBJECT
            ),
        )

    def test_cosign_verify_tampered_json(self) -> None:
        self.assertIn(
            "signature-verification-rejected",
            self.checker.validate_signature_fixture(
                cosign_verification(verified=False), CANDIDATE_SUBJECT
            ),
        )

    def test_cosign_verify_wrong_subject_json(self) -> None:
        self.assertIn(
            "signature-subject-mismatch",
            self.checker.validate_signature_fixture(
                cosign_verification(archive_digest="sha256:" + "b" * 64),
                CANDIDATE_SUBJECT,
            ),
        )

    def test_scorecard_advisory_json(self) -> None:
        self.assertEqual(
            [],
            self.checker.validate_scorecard_advisory(
                self.load_fixture("scorecard.advisory.json")
            ),
        )

        wrong_repository = scorecard_report(
            repository="hy-home-docker/hy-home.docker"
        )
        self.assertIn(
            "scorecard-repository-invalid",
            self.checker.validate_scorecard_advisory(wrong_repository),
        )

    def test_live_score_cannot_be_a_blocking_decision(self) -> None:
        scorecard = scorecard_report(ci_enforcement="blocking")
        self.assertIn(
            "scorecard-blocking-forbidden",
            self.checker.validate_scorecard_advisory(scorecard),
        )
