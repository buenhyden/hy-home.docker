"""Storybook image revision contract (SPEC-0219)."""

from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "storybook_image", ROOT / "scripts/operations/storybook_image.py"
)
storybook_image = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(storybook_image)

REVISION = "a" * 40
EXPECTED = {
    "lockfileSha256": "1" * 64,
    "uiPackage": {"name": "@hy-home/storybook-ui", "version": "0.2.0"},
}
MANIFESTS = {"components.json": "2" * 64, "docs.json": "3" * 64}


def record(**change):
    return {
        "sourceRevision": REVISION,
        **EXPECTED,
        "manifestSha256": dict(MANIFESTS),
        **change,
    }


class StaticOutputTests(unittest.TestCase):
    def check(self, value=None, files=("index.html", "iframe.html"), manifests=None):
        return storybook_image.check_static(
            value or record(),
            REVISION,
            EXPECTED,
            list(files),
            manifests or dict(MANIFESTS),
        )

    def test_matching_image_passes(self):
        self.assertEqual([], self.check())

    def test_every_mismatch_is_reported(self):
        cases = {
            "sourceRevision": record(sourceRevision="uncommitted"),
            "lockfileSha256": record(lockfileSha256="0" * 64),
            "uiPackage": record(
                uiPackage={"name": "@hy-home/storybook-ui", "version": "0.1.0"}
            ),
        }
        for field, value in cases.items():
            with self.subTest(field):
                self.assertTrue(any(field in f for f in self.check(value)))
        drifted = {**MANIFESTS, "docs.json": "4" * 64}
        self.assertTrue(any("manifest" in f for f in self.check(manifests=drifted)))

    def test_environment_key_and_map_files_are_forbidden(self):
        for name in (".env", "assets/.env.local", "certs/tls.pem", "x.key",
                     "assets/main.js.map", "node_modules/a/index.js"):  # fmt: skip
            with self.subTest(name):
                self.assertEqual([f"forbidden file {name}"], self.check(files=[name]))
        self.assertEqual(
            [], self.check(files=["assets/keyboard.js", "environment.html"])
        )


class RevisionTests(unittest.TestCase):
    def test_default_revision_is_the_last_source_commit(self):
        expected = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", storybook_image.SOURCE],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()  # fmt: skip
        self.assertEqual(expected, storybook_image.resolve_revision(None))

    def test_dockerfile_refuses_a_build_without_a_commit(self):
        dockerfile = (ROOT / storybook_image.SOURCE / "Dockerfile").read_text()
        self.assertIn("ARG STORYBOOK_SOURCE_REVISION\n", dockerfile)
        self.assertNotIn("STORYBOOK_SOURCE_REVISION=uncommitted", dockerfile)
        self.assertIn("*[!0-9a-f]*) false", dockerfile)
        self.assertIn('[ "${#STORYBOOK_SOURCE_REVISION}" -eq 40 ]', dockerfile)


if __name__ == "__main__":
    unittest.main()
