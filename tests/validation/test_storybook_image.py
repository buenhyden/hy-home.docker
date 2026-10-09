"""Storybook image, design token, design export and MCP client contracts (SPEC-0219)."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "storybook_image", ROOT / "scripts/operations/storybook_image.py"
)
storybook_image = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(storybook_image)
EXPORT_SPEC = importlib.util.spec_from_file_location(
    "storybook_design_export", ROOT / "scripts/operations/storybook_design_export.py"
)
design_export = importlib.util.module_from_spec(EXPORT_SPEC)
EXPORT_SPEC.loader.exec_module(design_export)

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


class DesignTokenTests(unittest.TestCase):
    """Root DESIGN.md and the package CSS name the same token values."""

    def test_design_tokens_match_the_package_css(self):
        import re

        import yaml

        design = yaml.safe_load(
            (ROOT / "DESIGN.md").read_text(encoding="utf-8").split("---")[1]
        )
        css = (ROOT / storybook_image.SOURCE / "packages/ui/src/styles.css").read_text()
        declared = dict(re.findall(r"--hy-([a-z0-9-]+):\s*([^;]+);", css))
        expected = {f"color-{k}": v for k, v in design["colors"].items()}
        expected |= {f"rounded-{k}": v for k, v in design["rounded"].items()}
        expected |= {f"spacing-{k}": v for k, v in design["spacing"].items()}
        for name in ("body-md", "heading-md"):
            style = design["typography"][name]
            expected[f"font-size-{name}"] = style["fontSize"]
            expected[f"line-height-{name}"] = str(style["lineHeight"])
        expected["font-family"] = design["typography"]["body-md"]["fontFamily"]
        self.assertEqual(expected, {k: declared.get(k) for k in expected})
        ui = json.loads(
            (ROOT / storybook_image.SOURCE / "packages/ui/package.json").read_text()
        )
        self.assertEqual(ui["version"], design["version"])


class DesignExportTests(unittest.TestCase):
    """Only allowlisted, committed files leave for Claude Design."""

    def test_bundle_holds_exactly_the_allowlist(self):
        import tempfile

        allowlist = json.loads((ROOT / design_export.ALLOWLIST).read_text())["files"]
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp) / "bundle"
            manifest = design_export.export(out, "HEAD")
            exported = {
                p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()
            }
            self.assertEqual(set(allowlist) | {"export-manifest.json"}, exported)
            self.assertEqual(set(allowlist), set(manifest["files"]))
            for target, source in allowlist.items():
                text = (out / target).read_text()
                committed = subprocess.run(
                    ["git", "show", f"HEAD:{source}"],
                    cwd=ROOT, check=True, capture_output=True, text=True,
                ).stdout  # fmt: skip
                if target.startswith("stories/"):
                    self.assertNotIn("packages/ui", text)
                    committed = committed.replace(design_export.STORY_IMPORT, "../src/")
                self.assertEqual(committed, text, target)
            with self.assertRaises(SystemExit):
                design_export.export(out, "HEAD")  # never into a non-empty directory

    def test_unsafe_paths_and_secret_shaped_content_are_refused(self):
        for path in ("../secrets/a", "src/*.ts", "/etc/passwd", ".env",
                     "x/.env.local", "secrets/key", "certs/tls.pem"):  # fmt: skip
            with self.subTest(path):
                self.assertTrue(design_export.check_allowlist({"a": path}))
        self.assertEqual([], design_export.check_allowlist({"src/a.ts": "src/a.ts"}))
        for text in ("-----BEGIN RSA PRIVATE KEY-----", "password: 'longenough1'",
                     "Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
                     "Cookie: __Secure-sso-cookie=abc"):  # fmt: skip
            with self.subTest(text):
                self.assertTrue(design_export.scan("f", text))
        self.assertEqual(
            [], design_export.scan("f", "label: 'Save', retryLabel = 'Try'")
        )


if __name__ == "__main__":
    unittest.main()
