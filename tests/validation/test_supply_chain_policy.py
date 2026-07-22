from __future__ import annotations

import copy
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
WRAPPER = ROOT / "scripts/security/verify-sample-service-supply-chain.sh"

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
BASELINE_SUBJECT["build_context_sha256"] = CANDIDATE_SUBJECT[
    "build_context_sha256"
]

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

    def _write_oci_archive(self, path: pathlib.Path, *, tamper_config: bool = False) -> str:
        config = json.dumps({"architecture": "amd64", "os": "linux"}, sort_keys=True).encode()
        config_digest = hashlib.sha256(config).hexdigest()
        manifest = json.dumps(
            {
                "config": {
                    "digest": f"sha256:{config_digest}",
                    "mediaType": "application/vnd.oci.image.config.v1+json",
                    "size": len(config),
                },
                "layers": [],
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
                "schemaVersion": 2,
            },
            sort_keys=True,
        ).encode()
        with tarfile.open(path, "w") as archive:
            for name, content in (
                ("oci-layout", b'{"imageLayoutVersion":"1.0.0"}'),
                ("index.json", index),
                (f"blobs/sha256/{manifest_digest}", manifest),
                (f"blobs/sha256/{config_digest}", b"tampered-config" if tamper_config else config),
            ):
                entry = tarfile.TarInfo(name)
                entry.size = len(content)
                archive.addfile(entry, fileobj=io.BytesIO(content))
        return f"sha256:{config_digest}"

    def test_oci_archive_config_digest_is_bound_to_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = pathlib.Path(temporary) / "image.oci.tar"
            expected = self._write_oci_archive(archive)
            self.assertEqual(expected, self.checker.inspect_oci_archive_config_digest(archive))

    def test_oci_archive_config_digest_rejects_tampered_blob(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = pathlib.Path(temporary) / "image.oci.tar"
            self._write_oci_archive(archive, tamper_config=True)
            with self.assertRaisesRegex(ValueError, "config-blob-digest-mismatch"):
                self.checker.inspect_oci_archive_config_digest(archive)

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

    def test_exact_local_image_gate_precedes_build_or_tool_start(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        advisory = text.split("run_advisory() {", maxsplit=1)[1].split(
            "\n}\n\nrun_scorecard_advisory", maxsplit=1
        )[0]
        self.assertLess(
            advisory.index("assert_local_image_identities"),
            advisory.index("build_role_image baseline"),
        )
        expected_id = "sha256:" + ("a" * 64)
        valid = self.run_wrapper_library(
            f"source {shlex.quote(str(WRAPPER))}\n"
            f"TEST_IMAGE_ID={expected_id}\n"
            "docker() { printf '%s\\n' \"$TEST_IMAGE_ID\"; }\n"
            f"assert_local_image_identity example.invalid/tool@{expected_id} {expected_id}\n"
        )
        self.assertEqual(0, valid.returncode, valid.stderr)
        for image_id in ("", "sha256:" + ("b" * 64)):
            with self.subTest(image_id=image_id or "missing"):
                result = self.run_wrapper_library(
                    f"source {shlex.quote(str(WRAPPER))}\n"
                    f"TEST_IMAGE_ID={shlex.quote(image_id)}\n"
                    "docker() { [ -n \"$TEST_IMAGE_ID\" ] || return 1; "
                    "printf '%s\\n' \"$TEST_IMAGE_ID\"; }\n"
                    f"assert_local_image_identity example.invalid/tool@{expected_id} {expected_id}\n"
                )
                self.assertEqual(10, result.returncode)

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
                "test \"$(stat -c %a \"$runtime_dir\")\" = 700\n"
                "test \"$(stat -c %a \"$grype_db_dir\")\" = 700\n"
                "test \"$(stat -c %a \"$private_key_dir\")\" = 700\n"
                "touch \"$runtime_dir/raw-artifact\"\n"
                "saved_runtime_dir=$runtime_dir\n"
                "cleanup_transient_state\n"
                "test ! -e \"$saved_runtime_dir\"\n"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual([], list(output.iterdir()))

    def test_legacy_runtime_cleanup_uses_the_gated_offline_root_container(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")
        cleanup = text.split(
            "remove_legacy_runtime_artifacts() {", maxsplit=1
        )[1].split("\n}\n\nbuild_role_image", maxsplit=1)[0]
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
            if "docker run " in line
            and '--user "$(id -u):$(id -g)"' in line
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
            output = pathlib.Path(temporary) / "supply-chain"
            output.mkdir(mode=0o700)
            docker_marker = pathlib.Path(temporary) / "docker-called"
            result = self.run_wrapper_library(
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"OUTPUT_DIR={shlex.quote(str(output))}\n"
                f"docker() {{ touch {shlex.quote(str(docker_marker))}; }}\n"
                "assert_grype_db_seed_available\n"
            )
            self.assertEqual(10, result.returncode, result.stderr)
            self.assertFalse(docker_marker.exists())

        text = WRAPPER.read_text(encoding="utf-8")
        advisory = text.split("run_advisory() {", maxsplit=1)[1].split(
            "\n}\n\nrun_scorecard_advisory", maxsplit=1
        )[0]
        self.assertLess(
            advisory.index("assert_grype_db_seed_available"),
            advisory.index("seed_private_grype_db_cache"),
        )
        self.assertLess(
            advisory.index("assert_grype_db_seed_available"),
            advisory.index("build_role_image baseline"),
        )

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
            common = (
                f"source {shlex.quote(str(WRAPPER))}\n"
                f"BASE_DIR={shlex.quote(str(repo))}\n"
                f"SERVICE_DIR={shlex.quote(str(service))}\n"
                f"CHECKER={shlex.quote(str(CHECKER_PATH))}\n"
                f"SOURCE_REVISION={source_revision}\n"
                f"build_context_snapshot={shlex.quote(str(snapshot))}\n"
            )

            (service / "site/untracked.html").write_text("new\n", encoding="utf-8")
            dirty = self.run_wrapper_library(common + "capture_build_context_snapshot\n")
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

            clean = self.run_wrapper_library(common + "capture_build_context_snapshot\n")
            self.assertEqual(0, clean.returncode, clean.stderr)
            (service / "site/index.html").write_text("tampered\n", encoding="utf-8")
            tampered = self.run_wrapper_library(common + "assert_build_context_unchanged\n")
            self.assertEqual(50, tampered.returncode, tampered.stderr)

    def test_invalidate_consumer_verdicts_removes_only_exact_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            output = base / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
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
            output = base / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
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

    def test_accepted_grype_exception_cannot_publish_consumer_verdict_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary) / "base"
            output = base / "_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
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
                "  mkdir -p \"$OUTPUT_DIR/grype-db-cache\"\n"
                "  grype_db_dir=\"$OUTPUT_DIR/grype-db-cache\"\n"
                "  run_verdict_dir=$(mktemp -d \"$OUTPUT_DIR/.verification-verdicts.XXXXXX\")\n"
                "}\n"
                "capture_build_context_snapshot() { BUILD_CONTEXT_SHA256=sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee; }\n"
                "ensure_advisory_prerequisites() { :; }\n"
                "assert_grype_db_seed_available() { :; }\n"
                "assert_local_image_identities() { :; }\n"
                "seed_private_grype_db_cache() { :; }\n"
                "remove_legacy_runtime_artifacts() { :; }\n"
                "record_grype_db_identity() { :; }\n"
                "build_role_image() { mkdir -p \"$OUTPUT_DIR/$1\"; }\n"
                "export_oci_archive() { :; }\n"
                "derive_subject_tuple() {\n"
                "  if [[ $1 == baseline ]]; then\n"
                "    IMAGE_CONFIG_DIGEST[$1]=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
                "    OCI_ARCHIVE_SHA256[$1]=sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n"
                "  else\n"
                "    IMAGE_CONFIG_DIGEST[$1]=sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\n"
                "    OCI_ARCHIVE_SHA256[$1]=sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
                "  fi\n"
                "}\n"
                "generate_cyclonedx_and_grype_verdict() {\n"
                "  mkdir -p \"$OUTPUT_DIR/$1\"\n"
                "  if [[ $1 == baseline ]]; then\n"
                "    printf '%s\\n' '{\"exception_id\":\"EXC-SSC-0001\",\"verdict\":\"accepted\"}' >\"$OUTPUT_DIR/$1/vulnerability-verdict.json\"\n"
                "  else\n"
                "    printf '%s\\n' '{\"exception_id\":null,\"verdict\":\"accepted\"}' >\"$OUTPUT_DIR/$1/vulnerability-verdict.json\"\n"
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
                "mkdir -p \"$private_key_dir\"\n"
                "docker() {\n"
                f"  printf '%s\\n' \"$*\" >> {shlex.quote(str(command_log))}\n"
                "  case \" $* \" in\n"
                "    *\" /workspace/tampered.oci.tar\"*|*\" /other/image.oci.tar\"*) return 1 ;;\n"
                "  esac\n"
                "  return 0\n"
                "}\n"
                "sign_and_verify_archive baseline\n"
                f"grep -Fq -- {shlex.quote(f'source={output}/candidate,target=/other,readonly')} {shlex.quote(str(command_log))}\n"
            )
            self.assertEqual(0, result.returncode, result.stderr)

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
                "mkdir -p \"$private_key_dir\"\n"
                "docker() {\n"
                "  case \" $* \" in\n"
                "    *\" /workspace/tampered.oci.tar\"*) return 1 ;;\n"
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
        payload = {
            "exception_id": None,
            "image_config_digest": "sha256:" + (("a" if role == "baseline" else "c") * 64),
            "oci_archive_sha256": "sha256:" + (("b" if role == "baseline" else "d") * 64),
            "policy_id": "sample-service-local-v1",
            "producer_spec": "spec:126-security-supply-chain-remediation",
            "redaction_status": "passed",
            "role": role,
            "schema_version": 1,
            "source_revision": SOURCE_REVISION,
            "build_context_sha256": CANDIDATE_SUBJECT["build_context_sha256"],
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
            self.assertEqual(1, manifest["schema_version"])
            self.assertEqual(
                {"baseline", "candidate"}, set(manifest["verdict_sha256"])
            )
            for name in (
                "verification-verdict.baseline.json",
                "verification-verdict.candidate.json",
                "verification-verdict.pair.json",
            ):
                self.assertEqual(
                    0o600, stat.S_IMODE((output / name).stat().st_mode), name
                )

    def test_secure_output_rejects_ancestor_and_final_symlinks_or_bad_mode(self) -> None:
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
