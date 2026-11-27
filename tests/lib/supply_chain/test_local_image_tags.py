from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.lib.supply_chain import ledger_rebind, local_image_tags
from scripts.lib.supply_chain.latest_version_gate import expected_from_root

LEAF = "infra/svc/docker-compose.yml"
ROOT = Path(__file__).resolve().parents[3]
DIGEST = "@sha256:" + "a" * 64


def make(root: Path, image: str, base: str) -> None:
    (root / "docker-compose.yml").write_text(f"include:\n  - {LEAF}\n")
    leaf = root / LEAF
    (leaf.parent / "loki").mkdir(parents=True, exist_ok=True)
    leaf.write_text(
        f"services:\n  loki:\n    image: {image}\n    build:\n      context: ./loki\n"
    )
    (leaf.parent / "loki/Dockerfile").write_text(
        f"ARG ALPINE=alpine:3.24\nFROM {base}{DIGEST} AS upstream\nFROM ${{ALPINE}}\n"
    )


def ledger(root: Path, declared: str) -> Path:
    _, inventory = expected_from_root(root)
    row = {
        "service": "loki",
        "compose_file": LEAF,
        "current_declared": declared,
        "build_source": {"context": "./loki"},
        "disposition": "NO_CHANGE_VERSION",
        "source_refreshed_at": "2026-01-01T00:00:00+00:00",
        "source_input_sha256": hashlib.sha256((root / LEAF).read_bytes()).hexdigest(),
    }
    path = root / "infra/09-platform-ops/security-updates/update-ledger.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "expected_services": ["loki"],
        "include_inputs": inventory["input_files"],
        "entries": [row],
        "source_refreshes": [],
    }
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    return path


def run(main, *argv: str) -> tuple[int, str]:
    output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        code = main(list(argv))
    return code, output.getvalue()


class LocalImageTagTests(unittest.TestCase):
    def test_stale_tag_is_reported_then_rewritten_to_the_base_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make(root, "hy/loki:3.7.8-seaweedfs", "grafana/loki:v3.7.10")
            ledger(root, "hy/loki:3.7.8-seaweedfs")
            check = ("--check", "--repo-root", directory)

            code, output = run(local_image_tags.main, *check)
            self.assertEqual(1, code)
            self.assertIn("hy/loki:3.7.8-seaweedfs -> hy/loki:3.7.10-seaweedfs", output)

            write = ("--write", "--repo-root", directory)
            self.assertEqual(0, run(local_image_tags.main, *write)[0])
            self.assertIn(
                "image: hy/loki:3.7.10-seaweedfs\n", (root / LEAF).read_text()
            )
            # The lagging ledger row is ledger_rebind's drift, not a stale tag.
            self.assertEqual(0, run(local_image_tags.main, *check)[0])

    def test_unversioned_tag_gains_the_version_and_unrelated_base_is_not_covered(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make(root, "hy/loki:local", "grafana/loki:3.7.10")
            row = json.loads(ledger(root, "hy/loki:local").read_text())["entries"][0]
            self.assertEqual(
                "hy/loki:3.7.10-local", local_image_tags.expected_image(root, row)
            )
            make(root, "hy/loki:3.7.8", "grafana/other:3.9.0")
            row["current_declared"] = "hy/loki:3.7.8"
            self.assertIsNone(local_image_tags.expected_image(root, row))

    def test_source_build_takes_its_version_from_the_named_arg(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make(root, "hy/gatus:local", "golang:1.26.4")
            dockerfile = root / "infra/svc/loki/Dockerfile"
            dockerfile.write_text("ARG GATUS_VERSION=5.38.0\n" + dockerfile.read_text())
            row = json.loads(ledger(root, "hy/gatus:local").read_text())["entries"][0]
            self.assertEqual(
                "hy/gatus:5.38.0-local", local_image_tags.expected_image(root, row)
            )

    def test_ledger_accepts_only_the_base_version_rename_as_unverified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make(root, "hy/loki:3.7.8-seaweedfs", "grafana/loki:3.7.10")
            path = ledger(root, "hy/loki:3.7.8-seaweedfs")
            write = (
                "--repo-root",
                directory,
                "--ledger",
                str(path),
                "--accept-image-updates",
                "--write",
                "--source-revision",
                "a" * 40,
            )

            make(root, "hy/loki:3.9.0-seaweedfs", "grafana/loki:3.7.10")
            code, output = run(ledger_rebind.main, *write)
            self.assertEqual(2, code, "a rename the base does not name stays refused")
            self.assertIn("image changed", output)

            make(root, "hy/loki:3.7.10-seaweedfs", "grafana/loki:3.7.10")
            self.assertEqual(0, run(ledger_rebind.main, *write)[0])
            row = json.loads(path.read_text())["entries"][0]
            self.assertEqual("hy/loki:3.7.10-seaweedfs", row["current_declared"])
            self.assertEqual("3.7.10", row["target_version"])
            self.assertEqual("BLOCKED", row["disposition"])
            self.assertEqual("NOT_RUN", row["signature"])
            self.assertIn("Local tag renamed", row["blocker"]["reason"])
            self.assertTrue(row["target_declared_digest"].startswith("UNKNOWN: "))

    def test_repository_tags_follow_their_dockerfile_base(self):
        code, output = run(local_image_tags.main, "--check", "--repo-root", str(ROOT))
        self.assertEqual(0, code, output)


if __name__ == "__main__":
    unittest.main()
