from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.lib.supply_chain import ledger_rebind
from scripts.lib.supply_chain.latest_version_gate import expected_from_root

REVISION = "a" * 40
OLD = "app:1.0@sha256:" + "1" * 64
NEW = "app:1.1@sha256:" + "2" * 64
VERIFIED = {
    "target_version": "1.0",
    "target_index_digest": "sha256:" + "1" * 64,
    "target_manifest_digest": "sha256:" + "3" * 64,
    "target_config_digest": "sha256:" + "4" * 64,
    "target_declared_digest": "sha256:" + "1" * 64,
    "signature": "PASS: cosign",
    "sbom_scan": "PASS: grype",
    "native_test": "PASS",
    "disposition": "NO_CHANGE_VERSION",
    "blocker": {"owner": "SEC01", "reason": "old"},
    "candidate_workflow_receipt": {"status": "PASS"},
}
STAMP = "2026-11-09T00:00:00+00:00"
LEAF = "infra/svc/docker-compose.yml"
ROOT = Path(__file__).resolve().parents[3]
WRAPPER = "scripts/operations/sync-update-ledger.sh"


def write_compose(root: Path, image: str, comment: str = "") -> None:
    (root / "docker-compose.yml").write_text(f"include:\n  - {LEAF}\n")
    leaf = root / LEAF
    leaf.parent.mkdir(parents=True, exist_ok=True)
    leaf.write_text(f"{comment}services:\n  app:\n    image: {image}\n")


def build_ledger(root: Path, declared: str = "app:1", **fields) -> None:
    _, inventory = expected_from_root(root)
    row = {
        "service": "app",
        "compose_file": LEAF,
        "current_declared": declared,
        "build_source": None,
        "disposition": "BLOCKED",
        "sbom_scan": "NOT_RUN",
        "source_refreshed_at": "2026-01-01T00:00:00+00:00",
        "source_input_sha256": hashlib.sha256((root / LEAF).read_bytes()).hexdigest(),
        **fields,
    }
    ledger = {
        "expected_services": ["app"],
        "include_inputs": inventory["input_files"],
        "entries": [row],
        "source_refreshes": [],
    }
    (root / "ledger.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"
    )


class CliCase(unittest.TestCase):
    def run_cli(self, root: Path, *extra: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = ledger_rebind.main(
                [
                    "--repo-root",
                    str(root),
                    "--ledger",
                    str(root / "ledger.json"),
                    *extra,
                ]
            )
        return code, output.getvalue()

    def read(self, root: Path) -> dict:
        return json.loads((root / "ledger.json").read_text())


class LedgerRebindTests(CliCase):
    def test_hash_only_drift_rebinds_once_and_second_write_is_a_noop(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_compose(root, "app:1")
            build_ledger(root)
            before = self.read(root)
            write_compose(root, "app:1", "# edited\n")
            write = ("--write", "--source-revision", REVISION, "--refreshed-at", STAMP)

            self.assertEqual(0, self.run_cli(root)[0])
            self.assertEqual(before, self.read(root), "dry run must not write")

            self.assertEqual(0, self.run_cli(root, *write)[0])
            after = self.read(root)
            new_hash = hashlib.sha256((root / LEAF).read_bytes()).hexdigest()
            self.assertEqual(new_hash, after["entries"][0]["source_input_sha256"])
            row = {**after["entries"][0], "source_input_sha256": None}
            old = {**before["entries"][0], "source_input_sha256": None}
            self.assertEqual(old, row)
            refresh = after["source_refreshes"][0]
            self.assertEqual(
                before["include_inputs"], refresh["previous_include_inputs"]
            )
            self.assertEqual([LEAF], refresh["changed_inputs"])
            self.assertEqual(
                [
                    {
                        "service": "app",
                        "source_input_sha256": before["entries"][0][
                            "source_input_sha256"
                        ],
                        "source_refreshed_at": "2026-01-01T00:00:00+00:00",
                    }
                ],
                refresh["previous_service_source_bindings"],
            )

            text = (root / "ledger.json").read_text()
            self.assertEqual(0, self.run_cli(root, *write)[0])
            self.assertEqual(text, (root / "ledger.json").read_text())

    def test_changed_image_is_refused_and_nothing_is_written(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_compose(root, "app:1")
            build_ledger(root)
            text = (root / "ledger.json").read_text()
            write_compose(root, "app:2")
            code, output = self.run_cli(root, "--write", "--source-revision", REVISION)
            self.assertEqual(2, code)
            self.assertIn("image changed", output)
            self.assertEqual(text, (root / "ledger.json").read_text())

    def test_added_service_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_compose(root, "app:1")
            build_ledger(root)
            (root / LEAF).write_text(
                "services:\n  app:\n    image: app:1\n  extra:\n    image: x:1\n"
            )
            code, output = self.run_cli(root)
            self.assertEqual(2, code)
            self.assertIn("service without a ledger row: extra", output)


class RenovateImageUpdateTests(CliCase):
    """The post-upgrade mode: accept a Renovate pin bump, claim nothing verified."""

    WRITE = (
        "--write",
        "--accept-image-updates",
        "--source-revision",
        REVISION,
        "--refreshed-at",
        STAMP,
    )

    def bumped(self, root: Path, image: str = NEW) -> str:
        write_compose(root, OLD)
        build_ledger(root, OLD, **VERIFIED)
        text = (root / "ledger.json").read_text()
        write_compose(root, image)
        return text

    def test_full_digest_pin_of_the_same_repository_is_accepted_unverified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.bumped(root)
            code, output = self.run_cli(root, *self.WRITE)
            self.assertEqual(0, code, output)
            row = self.read(root)["entries"][0]
            self.assertEqual(NEW, row["current_declared"])
            self.assertEqual(
                hashlib.sha256((root / LEAF).read_bytes()).hexdigest(),
                row["source_input_sha256"],
            )
            for field in (
                "target_index_digest",
                "target_manifest_digest",
                "target_config_digest",
                "target_declared_digest",
            ):
                self.assertEqual("UNKNOWN", row[field], field)
            for field in ("signature", "sbom_scan", "native_test"):
                self.assertEqual("NOT_RUN", row[field], field)
            self.assertEqual("BLOCKED", row["disposition"])
            self.assertEqual("SEC01", row["blocker"]["owner"])
            self.assertEqual("1.1", row["target_version"])
            self.assertEqual(
                {
                    "source_version": "1.1",
                    "source_image": NEW,
                    "status": "UNBOUND_CURRENT_TARGET",
                    "reason": row["current_target_artifact_binding"]["reason"],
                },
                row["current_target_artifact_binding"],
            )
            self.assertIn("Renovate", row["current_target_artifact_binding"]["reason"])
            refresh = self.read(root)["source_refreshes"][-1]
            self.assertEqual(["app"], refresh["updated_services"])
            self.assertEqual(REVISION, refresh["source_revision"])
            for words in (
                "Renovate-proposed",
                "signature",
                "provenance",
                "not verified",
            ):
                self.assertIn(words, refresh["meaning"])
            self.assertEqual(
                OLD, refresh["previous_service_images"][0]["current_declared"]
            )
            kept = refresh["previous_service_images"][0]["previous_fields"]
            for field, value in VERIFIED.items():
                self.assertEqual(value, kept[field], field)
            self.assertNotIn("PASS", json.dumps(row))
            self.assertNotIn("candidate_workflow_receipt", row)

    def test_second_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.bumped(root)
            self.assertEqual(0, self.run_cli(root, *self.WRITE)[0])
            text = (root / "ledger.json").read_text()
            code, output = self.run_cli(root, *self.WRITE)
            self.assertEqual(0, code)
            self.assertIn("up to date", output)
            self.assertEqual(text, (root / "ledger.json").read_text())

    def test_refused_changes_write_nothing(self):
        cases = {
            "no digest": ("app:1.1", "image changed"),
            "digest without tag": ("app@sha256:" + "2" * 64, "image changed"),
            "short digest": ("app:1.1@sha256:" + "2" * 63, "image changed"),
            "repository change": ("other:1.1@sha256:" + "2" * 64, "repository"),
            "registry change": ("evil.test/app:1.1@sha256:" + "2" * 64, "repository"),
            "interpolated": ("${APP_IMAGE:-app:1.1}", "image changed"),
        }
        for label, (image, expect) in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                text = self.bumped(root, image)
                code, output = self.run_cli(root, *self.WRITE)
                self.assertEqual(2, code, output)
                self.assertIn(expect, output)
                self.assertEqual(text, (root / "ledger.json").read_text())

    def test_new_or_removed_service_is_refused_even_with_a_valid_pin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text = self.bumped(root)
            (root / LEAF).write_text(
                f"services:\n  app:\n    image: {NEW}\n  extra:\n    image: {NEW}\n"
            )
            code, output = self.run_cli(root, *self.WRITE)
            self.assertEqual(2, code)
            self.assertIn("service without a ledger row: extra", output)
            (root / LEAF).write_text(f"services:\n  other:\n    image: {NEW}\n")
            code, output = self.run_cli(root, *self.WRITE)
            self.assertEqual(2, code)
            self.assertIn("ledger row without a Compose service: app", output)
            self.assertEqual(text, (root / "ledger.json").read_text())

    def test_build_change_is_refused_even_with_a_valid_pin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text = self.bumped(root)
            (root / LEAF).write_text(
                f"services:\n  app:\n    image: {NEW}\n    build: .\n"
            )
            code, output = self.run_cli(root, *self.WRITE)
            self.assertEqual(2, code)
            self.assertIn("build changed", output)
            self.assertEqual(text, (root / "ledger.json").read_text())

    def test_mode_is_needed_to_accept_an_image_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text = self.bumped(root)
            code, output = self.run_cli(root, "--write", "--source-revision", REVISION)
            self.assertEqual(2, code)
            self.assertIn("image changed", output)
            self.assertEqual(text, (root / "ledger.json").read_text())


class PostUpgradeWrapperTests(unittest.TestCase):
    def test_only_the_allowlisted_write_mode_runs(self):
        for arguments in ([], ["--check"], ["--write", "--write"], ["--dry-run"]):
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    ["bash", WRAPPER, *arguments],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(2, result.returncode)
                self.assertIn("Usage:", result.stderr)

    def test_dependencies_come_from_the_hash_locked_renovate_file(self):
        text = (ROOT / WRAPPER).read_text()
        self.assertIn("--require-hashes", text)
        self.assertIn("scripts/requirements-renovate.lock", text)
        self.assertNotIn("curl", text)


N8N_INPUT = "infra/svc/n8n-input.txt"


def n8n_binding(root: Path) -> dict:
    data = (root / N8N_INPUT).read_bytes()
    return {
        "checked_at": "2026-01-01T00:00:00Z",
        "source_revision": "b" * 40,
        "source_state": "SOURCE_REVIEW_ONLY",
        "input_sha256": hashlib.sha256(N8N_INPUT.encode() + b"\0" + data).hexdigest(),
        "algorithm": "SHA256 of sorted relative path UTF-8 bytes + NUL + file bytes",
        "input_files": [
            {"path": N8N_INPUT, "sha256": hashlib.sha256(data).hexdigest()}
        ],
        "native_test": "NOT_RUN",
    }


class N8nSourceBindingTests(CliCase):
    def prepare(self, root: Path) -> dict:
        write_compose(root, "app:1")
        (root / N8N_INPUT).write_text("FROM alpine:3.24.2\n")
        build_ledger(root)
        binding = n8n_binding(root)
        ledger = self.read(root)
        section = {"source_binding": binding, "historical_source_bindings": []}
        ledger["n8n_source_preparation"] = section
        (root / "ledger.json").write_text(ledger_rebind._dump(ledger))
        (root / "build-inputs.json").write_text(
            ledger_rebind._dump({"n8n_source_preparation": copy.deepcopy(section)})
        )
        return binding

    def bindings(self, root: Path) -> tuple[dict, dict]:
        ledger = self.read(root)["n8n_source_preparation"]
        build = json.loads((root / "build-inputs.json").read_text())
        return ledger, build["n8n_source_preparation"]

    def test_changed_input_rebinds_both_documents_identically_and_keeps_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = self.prepare(root)
            (root / N8N_INPUT).write_text("FROM alpine:3.24.3\n")
            write = ("--write", "--source-revision", REVISION, "--refreshed-at", STAMP)

            self.assertEqual(0, self.run_cli(root)[0])
            self.assertEqual(old, self.bindings(root)[0]["source_binding"], "dry run")

            code, output = self.run_cli(root, *write)
            self.assertEqual(0, code, output)
            ledger, build = self.bindings(root)
            self.assertEqual(ledger["source_binding"], build["source_binding"])
            self.assertEqual(
                n8n_binding(root)["input_sha256"],
                ledger["source_binding"]["input_sha256"],
            )
            self.assertNotEqual(
                old["input_sha256"], ledger["source_binding"]["input_sha256"]
            )
            for section in (ledger, build):
                self.assertEqual(
                    [{**old, "archived_at": STAMP}],
                    section["historical_source_bindings"],
                )
            self.assertEqual("NOT_RUN", ledger["source_binding"]["native_test"])
            self.assertEqual(REVISION, ledger["source_binding"]["source_revision"])

            texts = [
                (root / n).read_text() for n in ("ledger.json", "build-inputs.json")
            ]
            self.assertEqual(0, self.run_cli(root, *write)[0])
            self.assertEqual(
                texts,
                [(root / n).read_text() for n in ("ledger.json", "build-inputs.json")],
            )

    def test_bindings_that_already_differ_are_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.prepare(root)
            build = json.loads((root / "build-inputs.json").read_text())
            build["n8n_source_preparation"]["source_binding"]["checked_at"] = "other"
            (root / "build-inputs.json").write_text(ledger_rebind._dump(build))
            (root / N8N_INPUT).write_text("changed\n")
            code, output = self.run_cli(root, "--write", "--source-revision", REVISION)
            self.assertEqual(2, code)
            self.assertIn("n8n source bindings differ", output)

    def test_a_removed_input_file_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.prepare(root)
            (root / N8N_INPUT).unlink()
            code, output = self.run_cli(root, "--write", "--source-revision", REVISION)
            self.assertEqual(2, code)
            self.assertIn("n8n source input missing", output)


if __name__ == "__main__":
    unittest.main()
