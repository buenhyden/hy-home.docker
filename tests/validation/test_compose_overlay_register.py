"""The overlay register, the POL-0078 table and the overlay files must agree."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY = (
    ROOT / "docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md"
)
MARKER = re.compile(r"^x-hyhome-overlay:", re.M)


def overlay_files():
    return {
        path.relative_to(ROOT).as_posix()
        for suffix in ("yml", "yaml")
        for path in (ROOT / "infra").rglob(f"*.{suffix}")
        if path.is_file() and MARKER.search(path.read_text(encoding="utf-8"))
    }


class OverlayRegisterTests(unittest.TestCase):
    def test_register_matches_overlay_files_and_policy_table(self):
        register = json.loads((ROOT / "infra/compose-overlays.json").read_text())
        files = {item["file"] for item in register["overlays"]}
        self.assertEqual(overlay_files(), files)
        table = set(
            re.findall(r"^\| `(infra/[^`]+\.ya?ml)` \|", POLICY.read_text(), re.M)
        )
        self.assertEqual(files, table)
        for item in register["overlays"]:
            self.assertTrue((ROOT / item["owner_doc"]).is_file(), item["owner_doc"])


if __name__ == "__main__":
    unittest.main()
