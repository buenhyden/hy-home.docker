from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import stat
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
HELPER_PATH = ROOT / "scripts/validation/grype_db_seed.py"
HARNESS_PATH = ROOT / "scripts/security/seed-grype-db-cache.sh"
OUTPUT_RELATIVE = pathlib.Path(
    "_workspace/repo-support/"
    "task-2026-07-23-security-supply-chain-runtime-closure/grype-db-seed"
)
PACKAGE_SHA256 = "7" * 64
GRYPE_TOOL = {
    "image_ref": (
        "anchore/grype:v0.116.0@"
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
    ),
    "repo_digest": (
        "anchore/grype@"
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
    ),
    "config_id": (
        "sha256:4d4127e08c9eaafe6fa1eb2fcc05c83b2608562541949ffb33ef32eb4b1b25c0"
    ),
    "target_descriptor_digest": (
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
    ),
}
SEEDED_AT = "2026-07-23T00:00:00Z"


def load_helper():
    spec = importlib.util.spec_from_file_location("grype_db_seed", HELPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Grype DB seed helper is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_status(path: pathlib.Path, *, checksum: str = PACKAGE_SHA256) -> None:
    path.write_text(
        "Schema: v6.1.9\n"
        "Built: 2026-07-23T00:00:00Z\n"
        "Status: valid\n"
        "From: https://toolbox-data.anchore.io/grype/databases/v6/"
        "vulnerability-db_v6.1.9_2026-07-23T00:00:00Z.tar.zst?"
        f"checksum=sha256%3A{checksum}\n",
        encoding="utf-8",
    )
    path.chmod(0o600)


class GrypeDbSeedHarnessContractTests(unittest.TestCase):
    def run_harness_library(
        self,
        body: str,
        *,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        source = HARNESS_PATH.read_text(encoding="utf-8")
        library = source.split('\ncase "$MODE" in\n', maxsplit=1)[0]
        self.assertNotEqual(source, library, "seed harness dispatch boundary is missing")
        with tempfile.TemporaryDirectory(
            prefix="grype-seed-library-", dir="/tmp"
        ) as raw:
            library_path = pathlib.Path(raw) / "seed-grype-db-cache.lib.sh"
            library_path.write_text(library + "\n", encoding="utf-8")
            environment = os.environ.copy()
            if env:
                environment.update(env)
            return subprocess.run(
                ["bash", "-c", f"source {library_path!s}\n{body}"],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_harness_is_narrowly_networked_and_keeps_advisory_offline(self) -> None:
        self.assertTrue(HARNESS_PATH.is_file(), "dedicated seed harness is missing")
        text = HARNESS_PATH.read_text(encoding="utf-8")
        self.assertIn("--preflight|--seed", text)
        self.assertIn("Grype DB network approval: confirmed", text)
        self.assertIn("GRYPE_CHECK_FOR_APP_UPDATE=false", text)
        self.assertIn("GRYPE_DB_AUTO_UPDATE=false", text)
        self.assertIn("--network bridge", text)
        self.assertIn(" db update", text)
        self.assertIn("--network none", text)
        self.assertIn(" db status", text)
        self.assertIn("--pull=never", text)
        self.assertNotIn("curl ", text)
        self.assertNotIn("wget ", text)
        self.assertNotIn("docker pull", text)
        self.assertNotIn("pre-commit", text)

        advisory = (
            ROOT / "scripts/security/verify-sample-service-supply-chain.sh"
        ).read_text(encoding="utf-8")
        self.assertIn("--network none", advisory)
        self.assertNotIn("db update", advisory)

    def test_harness_has_private_runtime_and_bounded_cleanup(self) -> None:
        self.assertTrue(HARNESS_PATH.is_file(), "dedicated seed harness is missing")
        text = HARNESS_PATH.read_text(encoding="utf-8")
        self.assertIn("mktemp -d /tmp/hyhome-grype-db-seed.XXXXXX", text)
        self.assertIn("chmod 700", text)
        self.assertIn("umask 077", text)
        self.assertIn("trap cleanup EXIT", text)
        self.assertNotIn("docker system prune", text)
        self.assertNotIn("docker volume prune", text)
        self.assertNotIn("docker network prune", text)

    def test_harness_separates_target_descriptor_from_config_digest(self) -> None:
        text = HARNESS_PATH.read_text(encoding="utf-8")
        self.assertIn(
            f'readonly GRYPE_TARGET_DESCRIPTOR_DIGEST="{GRYPE_TOOL["target_descriptor_digest"]}"',
            text,
        )
        self.assertIn(
            f'readonly GRYPE_CONFIG_ID="{GRYPE_TOOL["config_id"]}"',
            text,
        )
        self.assertNotEqual(
            GRYPE_TOOL["target_descriptor_digest"],
            GRYPE_TOOL["config_id"],
        )

    def test_local_image_identity_accepts_target_descriptor_runtime_id(self) -> None:
        inspection = json.dumps(
            {
                "RepoDigests": [GRYPE_TOOL["repo_digest"]],
                "Id": GRYPE_TOOL["target_descriptor_digest"],
                "Descriptor": {
                    "digest": GRYPE_TOOL["target_descriptor_digest"],
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        result = self.run_harness_library(
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_grype_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            "assert_local_grype_identity\n",
            env={
                "TEST_INSPECTION": inspection,
                "TEST_CONFIG_ID": GRYPE_TOOL["config_id"],
            },
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_local_image_identity_accepts_config_digest_runtime_id(self) -> None:
        inspection = json.dumps(
            {
                "RepoDigests": [GRYPE_TOOL["repo_digest"]],
                "Id": GRYPE_TOOL["config_id"],
                "Descriptor": {
                    "digest": GRYPE_TOOL["target_descriptor_digest"],
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        result = self.run_harness_library(
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_grype_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            "assert_local_grype_identity\n",
            env={
                "TEST_INSPECTION": inspection,
                "TEST_CONFIG_ID": GRYPE_TOOL["config_id"],
            },
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_local_image_identity_rejects_unrelated_runtime_id(self) -> None:
        inspection = json.dumps(
            {
                "RepoDigests": [GRYPE_TOOL["repo_digest"]],
                "Id": "sha256:" + ("e" * 64),
                "Descriptor": {
                    "digest": GRYPE_TOOL["target_descriptor_digest"],
                    "mediaType": "application/vnd.oci.image.index.v1+json",
                },
            }
        )
        result = self.run_harness_library(
            "docker() { printf '%s\\n' \"$TEST_INSPECTION\"; }\n"
            "observe_local_grype_config_digest() { "
            "printf '%s\\n' \"$TEST_CONFIG_ID\"; }\n"
            "assert_local_grype_identity\n",
            env={
                "TEST_INSPECTION": inspection,
                "TEST_CONFIG_ID": GRYPE_TOOL["config_id"],
            },
        )
        self.assertEqual(10, result.returncode)
        self.assertIn("pinned-grype-manifest-mismatch", result.stderr)


class GrypeDbSeedPublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.helper = load_helper()

    def prepare(self, base: pathlib.Path):
        base.mkdir(mode=0o700)
        output_identity, stage_identity, stage = self.helper.prepare_seed_stage(
            base, OUTPUT_RELATIVE
        )
        cache = stage / "cache"
        schema = cache / "6"
        schema.mkdir(parents=True, mode=0o700)
        (schema / "vulnerability.db").write_bytes(b"current database\n")
        (schema / "metadata.json").write_text('{"schema":"v6.1.9"}\n', encoding="utf-8")
        status_path = stage / "db-status.txt"
        write_status(status_path)
        return output_identity, stage_identity, stage, status_path

    def finalize(
        self,
        base: pathlib.Path,
        output_identity: str,
        stage_identity: str,
        stage: pathlib.Path,
        status_path: pathlib.Path,
    ):
        return self.helper.finalize_seed_generation(
            base,
            OUTPUT_RELATIVE,
            output_identity,
            stage_identity,
            stage,
            status_path,
            GRYPE_TOOL,
            SEEDED_AT,
        )

    def test_publish_creates_private_generation_and_atomic_minimized_pointer(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            payload = self.finalize(
                base, output_identity, stage_identity, stage, status_path
            )

            output = base / OUTPUT_RELATIVE
            pointer = output / "current.json"
            generation = output / payload["generation_path"]
            self.assertEqual(0o700, stat.S_IMODE(output.stat().st_mode))
            self.assertEqual(0o600, stat.S_IMODE(pointer.stat().st_mode))
            self.assertEqual(0o700, stat.S_IMODE(generation.stat().st_mode))
            self.assertEqual(0o700, stat.S_IMODE((generation / "cache").stat().st_mode))
            self.assertEqual(
                0o600,
                stat.S_IMODE((generation / "identity.json").stat().st_mode),
            )
            for path in (generation / "cache").rglob("*"):
                expected = 0o700 if path.is_dir() else 0o600
                self.assertEqual(expected, stat.S_IMODE(path.stat().st_mode), path)

            self.assertEqual(payload, json.loads(pointer.read_text(encoding="utf-8")))
            self.assertEqual(
                payload,
                json.loads((generation / "identity.json").read_text(encoding="utf-8")),
            )
            self.assertEqual(
                {
                    "cache",
                    "database",
                    "generation",
                    "generation_path",
                    "redaction_status",
                    "schema_version",
                    "seeded_at",
                    "tool",
                },
                set(payload),
            )
            self.assertEqual("hyhome-grype-db-seed-v1", payload["generation"])
            self.assertEqual(PACKAGE_SHA256, payload["database"]["package_sha256"])
            self.assertRegex(payload["cache"]["tree_sha256"], r"^sha256:[0-9a-f]{64}$")
            self.assertEqual(2, payload["cache"]["file_count"])
            self.assertGreater(payload["cache"]["byte_count"], 0)
            self.assertEqual(
                generation / "cache",
                self.helper.resolve_seed_generation(base, OUTPUT_RELATIVE),
            )
            self.assertFalse(any(output.glob(".current.json.*.tmp")))

    def test_failed_new_seed_preserves_last_valid_pointer_and_generation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            first = self.finalize(
                base, output_identity, stage_identity, stage, status_path
            )
            output = base / OUTPUT_RELATIVE
            pointer = output / "current.json"
            before = pointer.read_bytes()
            old_generation = output / first["generation_path"]

            output_identity, stage_identity, stage = self.helper.prepare_seed_stage(
                base, OUTPUT_RELATIVE
            )
            schema = stage / "cache/6"
            schema.mkdir(parents=True)
            (schema / "vulnerability.db").write_bytes(b"untrusted\n")
            status_path = stage / "db-status.txt"
            write_status(status_path, checksum="not-a-checksum")
            with self.assertRaises(self.helper.SeedContractError):
                self.finalize(base, output_identity, stage_identity, stage, status_path)

            self.assertEqual(before, pointer.read_bytes())
            self.assertTrue(old_generation.is_dir())
            self.assertEqual(
                old_generation / "cache",
                self.helper.resolve_seed_generation(base, OUTPUT_RELATIVE),
            )

    def test_symlinked_cache_member_is_rejected_without_pointer_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            first = self.finalize(
                base, output_identity, stage_identity, stage, status_path
            )
            output = base / OUTPUT_RELATIVE
            before = (output / "current.json").read_bytes()

            output_identity, stage_identity, stage = self.helper.prepare_seed_stage(
                base, OUTPUT_RELATIVE
            )
            schema = stage / "cache/6"
            schema.mkdir(parents=True)
            outside = pathlib.Path(temporary) / "outside.db"
            outside.write_bytes(b"preserve\n")
            (schema / "vulnerability.db").symlink_to(outside)
            status_path = stage / "db-status.txt"
            write_status(status_path)
            with self.assertRaises(self.helper.SeedContractError):
                self.finalize(base, output_identity, stage_identity, stage, status_path)

            self.assertEqual(b"preserve\n", outside.read_bytes())
            self.assertEqual(before, (output / "current.json").read_bytes())
            self.assertTrue((output / first["generation_path"]).is_dir())

    def test_resolver_rejects_cache_tamper_and_pointer_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            payload = self.finalize(
                base, output_identity, stage_identity, stage, status_path
            )
            output = base / OUTPUT_RELATIVE
            generation = output / payload["generation_path"]
            (generation / "cache/6/vulnerability.db").write_bytes(b"tampered\n")
            with self.assertRaises(self.helper.SeedContractError):
                self.helper.resolve_seed_generation(base, OUTPUT_RELATIVE)

        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            payload = self.finalize(
                base, output_identity, stage_identity, stage, status_path
            )
            pointer = base / OUTPUT_RELATIVE / "current.json"
            payload["generation_path"] = "../../outside"
            pointer.write_text(
                json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8"
            )
            pointer.chmod(0o600)
            with self.assertRaises(self.helper.SeedContractError):
                self.helper.resolve_seed_generation(base, OUTPUT_RELATIVE)

    def test_output_and_stage_identity_swaps_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            displaced = stage.with_name(stage.name + ".displaced")
            stage.rename(displaced)
            stage.mkdir(mode=0o700)
            with self.assertRaises(self.helper.SeedContractError):
                self.finalize(base, output_identity, stage_identity, stage, status_path)

        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            output = base / OUTPUT_RELATIVE
            displaced = output.with_name(output.name + ".displaced")
            output.rename(displaced)
            output.mkdir(mode=0o700)
            with self.assertRaises(self.helper.SeedContractError):
                self.finalize(base, output_identity, stage_identity, stage, status_path)

    def test_cli_check_current_emits_only_minimized_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "repo"
            output_identity, stage_identity, stage, status_path = self.prepare(base)
            payload = self.finalize(
                base, output_identity, stage_identity, stage, status_path
            )
            result = subprocess.run(
                [
                    "python3",
                    str(HELPER_PATH),
                    "--check-current",
                    str(base),
                    str(OUTPUT_RELATIVE),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(payload, json.loads(result.stdout))
            self.assertNotIn("vulnerability.db", result.stdout)
            self.assertNotIn("toolbox-data", result.stdout)


if __name__ == "__main__":
    unittest.main()
