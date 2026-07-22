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


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "scripts/validation/check-supply-chain-policy.py"
FIXTURES = ROOT / "tests/fixtures/supply-chain"
TOOL_REGISTRY = ROOT / "infra/supply-chain.tool-images.json"
POLICY = ROOT / "infra/supply-chain.sample-service-policy.json"
EXCEPTIONS = ROOT / "infra/supply-chain.vulnerability-exceptions.json"
COSIGN_OFFLINE_SIGNING_CONFIG = (
    ROOT / "infra/supply-chain.cosign-offline-signing-config.json"
)
COSIGN_OFFLINE_TRUSTED_ROOT = ROOT / "infra/supply-chain.cosign-offline-trusted-root.json"
WRAPPER = ROOT / "scripts/security/verify-sample-service-supply-chain.sh"
SEED_HELPER = ROOT / "scripts/validation/grype_db_seed.py"
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
    "sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5"
)
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
                self.load_fixture("sample-service-sbom.subject-mismatch.cdx.json"),
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
        return f"sha256:{config_digest}"

    def _write_portable_oci_archive(
        self,
        path: pathlib.Path,
        *,
        mutation: str | None = None,
    ) -> dict[str, str | int]:
        layer_payload = (
            b"x" * 16384
            if mutation == "oversized-layer"
            else b"deterministic-layer\n"
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
                    "Labels": {
                        "org.hyhome.delivery.rehearsal.role": "baseline"
                    }
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
        if mutation == "oversized-logical-member":
            logical_end = sum(
                512
                + (
                    ((entry.size + 511) // 512) * 512
                    if entry.isfile()
                    else 0
                )
                for entry, _ in entries
            )
            oversized = tarfile.TarInfo("oversized-logical-member.bin")
            oversized.mode = 0o600
            oversized.size = self.checker.OCI_ARCHIVE_MAX_BYTES + 1
            body = bytearray(path.read_bytes())
            body[logical_end : logical_end + 512] = oversized.tobuf(
                format=tarfile.USTAR_FORMAT
            )
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
            self.assertEqual(expected["image_config_digest"], first_result["image_config_digest"])
            self.assertEqual(expected["oci_manifest_digest"], first_result["oci_manifest_digest"])
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
                            expected["layer_digest"].removeprefix("sha256:")
                            + ".tar",
                            "manifest.json",
                        )
                    ),
                    names,
                )
                self.assertNotIn("index.json", names)
                self.assertNotIn("oci-layout", names)
                manifest = json.load(archive.extractfile("manifest.json"))
            self.assertEqual(
                [first_result["local_image_ref"]], manifest[0]["RepoTags"]
            )

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
            "oversized-logical-member": "oci-archive-member-size-limit-exceeded",
        }
        for mutation, reason in cases.items():
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
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
            original = getattr(
                self.checker, "OCI_LAYER_MAX_UNCOMPRESSED_BYTES", None
            )
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
                    delattr(
                        self.checker, "OCI_LAYER_MAX_UNCOMPRESSED_BYTES"
                    )
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
            self.load_fixture("grype.high-without-exception.json"),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("review-finding-without-exception", result["reason"])

    def test_grype_high_with_valid_exception_json(self) -> None:
        result = self.checker.evaluate_grype_fixture(
            self.load_fixture("grype.high-with-valid-exception.json"),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("accepted", result["verdict"])
        self.assertEqual("EXC-SSC-0001", result["exception_id"])

    def test_grype_valid_exception_cannot_short_circuit_later_critical(self) -> None:
        result = self.checker.evaluate_grype_fixture(
            self.load_fixture("grype.valid-exception-then-critical.json"),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("blocking-finding-without-exception", result["reason"])
        self.assertIsNone(result["exception_id"])

    def test_embedded_exception_is_bound_to_each_match(self) -> None:
        fixture = self.load_fixture("grype.valid-exception-then-critical.json")
        fixture.pop("exception_id")
        fixture["exception"] = self.checker.load_json(EXCEPTIONS)["exceptions"][0]
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
            self.load_fixture("grype.high-with-valid-exception.json"),
            self.checker.load_json(POLICY),
            exceptions,
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("review-finding-without-exception", result["reason"])

    def test_grype_expired_exception_json(self) -> None:
        result = self.checker.evaluate_grype_fixture(
            self.load_fixture("grype.expired-exception.json"),
            self.checker.load_json(POLICY),
            self.checker.load_json(EXCEPTIONS),
            CANDIDATE_SUBJECT,
        )
        self.assertEqual("rejected", result["verdict"])
        self.assertEqual("exception-expired", result["reason"])

    def test_grype_raw_finding_leakage_is_rejected(self) -> None:
        fixture = self.load_fixture("grype.high-without-exception.json")
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
                self.load_fixture("provenance.subject-mismatch.intoto.json"),
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
                self.load_fixture("cosign.verify.tampered.json"), CANDIDATE_SUBJECT
            ),
        )

    def test_cosign_verify_wrong_subject_json(self) -> None:
        self.assertIn(
            "signature-subject-mismatch",
            self.checker.validate_signature_fixture(
                self.load_fixture("cosign.verify.wrong-subject.json"), CANDIDATE_SUBJECT
            ),
        )

    def test_scorecard_advisory_json(self) -> None:
        self.assertEqual(
            [],
            self.checker.validate_scorecard_advisory(
                self.load_fixture("scorecard.advisory.json")
            ),
        )

        wrong_repository = self.load_fixture("scorecard.advisory.json")
        wrong_repository["repository"] = "hy-home-docker/hy-home.docker"
        self.assertIn(
            "scorecard-repository-invalid",
            self.checker.validate_scorecard_advisory(wrong_repository),
        )

    def test_live_score_cannot_be_a_blocking_decision(self) -> None:
        scorecard = self.load_fixture("scorecard.advisory.json")
        scorecard["ci_enforcement"] = "blocking"
        self.assertIn(
            "scorecard-blocking-forbidden",
            self.checker.validate_scorecard_advisory(scorecard),
        )


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

    def test_local_image_identity_accepts_independent_manifest_and_config(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        valid = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_REPO_DIGESTS={shlex.quote(json.dumps([reference]))}\n"
            f"TEST_CONFIG_ID={config_id}\n"
            "docker() { printf '%s|%s\\n' \"$TEST_REPO_DIGESTS\" "
            '"$TEST_CONFIG_ID"; }\n'
            f"assert_local_image_identity {reference} {reference} {config_id}\n"
        )
        self.assertEqual(0, valid.returncode, valid.stderr)

    def test_local_image_identity_rejects_manifest_mismatch(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        wrong_reference = "example.invalid/tool@sha256:" + ("c" * 64)
        result = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_REPO_DIGESTS={shlex.quote(json.dumps([wrong_reference]))}\n"
            f"TEST_CONFIG_ID={config_id}\n"
            "docker() { printf '%s|%s\\n' \"$TEST_REPO_DIGESTS\" "
            '"$TEST_CONFIG_ID"; }\n'
            f"assert_local_image_identity {reference} {reference} {config_id}\n"
        )
        self.assertEqual(10, result.returncode)
        self.assertIn("pinned-image-manifest-mismatch", result.stderr)

    def test_local_image_identity_rejects_config_id_mismatch(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        result = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_REPO_DIGESTS={shlex.quote(json.dumps([reference]))}\n"
            f"TEST_CONFIG_ID=sha256:{'d' * 64}\n"
            "docker() { printf '%s|%s\\n' \"$TEST_REPO_DIGESTS\" "
            '"$TEST_CONFIG_ID"; }\n'
            f"assert_local_image_identity {reference} {reference} {config_id}\n"
        )
        self.assertEqual(10, result.returncode)
        self.assertIn("pinned-image-config-id-mismatch", result.stderr)

    def test_local_image_identity_rejects_missing_image(self) -> None:
        manifest_digest = "sha256:" + ("a" * 64)
        config_id = "sha256:" + ("b" * 64)
        reference = f"example.invalid/tool@{manifest_digest}"
        result = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            "docker() { return 1; }\n"
            f"assert_local_image_identity {reference} {reference} {config_id}\n"
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
            "producer_spec": "spec:126-security-supply-chain-remediation",
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
                    "build_context_sha256": CANDIDATE_SUBJECT[
                        "build_context_sha256"
                    ],
                    "docker_archive_sha256": "sha256:" + ("3" if role == "baseline" else "4") * 64,
                    "exception_id": None,
                    "image_config_digest": config,
                    "local_image_ref": (
                        f"hyhome.local/sample-web-service:{role}-"
                        f"{config.removeprefix('sha256:')}"
                    ),
                    "oci_archive_sha256": "sha256:" + ("5" if role == "baseline" else "6") * 64,
                    "oci_manifest_digest": "sha256:" + ("7" if role == "baseline" else "8") * 64,
                    "policy_id": "sample-service-local-v1",
                    "producer_spec": "spec:126-security-supply-chain-remediation",
                    "redaction_status": "passed",
                    "role": role,
                    "runtime_identity_kind": (
                        "config-digest" if role == "baseline" else "docker-target-digest"
                    ),
                    "runtime_image_id": (
                        config
                        if role == "baseline"
                        else "sha256:" + "a" * 64
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
