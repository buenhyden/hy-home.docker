from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.lib.supply_chain import ledger_rebind
from scripts.lib.supply_chain.latest_version_gate import expected_from_root

REVISION = "a" * 40
STAMP = "2026-11-09T00:00:00+00:00"
LEAF = "infra/svc/docker-compose.yml"


def write_compose(root: Path, image: str, comment: str = "") -> None:
    (root / "docker-compose.yml").write_text(f"include:\n  - {LEAF}\n")
    leaf = root / LEAF
    leaf.parent.mkdir(parents=True, exist_ok=True)
    leaf.write_text(f"{comment}services:\n  app:\n    image: {image}\n")


def build_ledger(root: Path) -> None:
    _, inventory = expected_from_root(root)
    row = {
        "service": "app",
        "compose_file": LEAF,
        "current_declared": "app:1",
        "build_source": None,
        "disposition": "BLOCKED",
        "sbom_scan": "NOT_RUN",
        "source_refreshed_at": "2026-01-01T00:00:00+00:00",
        "source_input_sha256": hashlib.sha256((root / LEAF).read_bytes()).hexdigest(),
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


class LedgerRebindTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
