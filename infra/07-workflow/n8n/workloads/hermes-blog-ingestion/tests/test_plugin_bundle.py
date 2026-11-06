"""The Hermes plugin release is explicit, self-contained, and fail closed."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
PLUGIN = WORKLOAD / "hermes-plugin"
PUBLISHER = WORKLOAD / "publisher"
UPDATE = WORKLOAD / "deploy/update-hermes-plugin.sh"
PLUGIN_FILES = ("__init__.py", "plugin.yaml", "tools.py", "webhook_transport.py")
SHARED_FILES = (
    "gateway_receipt.py",
    "private_records.py",
    "source_check.py",
    "source_collection.py",
    "source_fetch.py",
)


def copy_bundle(root, *, missing=None):
    package = root / "research_report"
    package.mkdir(parents=True)
    for name in PLUGIN_FILES:
        if name != missing:
            shutil.copyfile(PLUGIN / name, package / name)
    for name in SHARED_FILES:
        if name != missing:
            shutil.copyfile(PUBLISHER / name, package / name)
    return package


class PluginBundleTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def run_isolated(self, code):
        return subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                f"import sys; sys.path.insert(0, {str(self.root)!r}); {code}",
            ],
            capture_output=True,
            check=False,
            text=True,
        )

    def test_nine_file_bundle_imports_and_registers_both_tools(self):
        package = copy_bundle(self.root)
        expected = {
            name: hashlib.sha256(
                ((PLUGIN if name in PLUGIN_FILES else PUBLISHER) / name).read_bytes()
            ).hexdigest()
            for name in (*PLUGIN_FILES, *SHARED_FILES)
        }
        actual = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in package.iterdir()
        }
        self.assertEqual(actual, expected)
        code = (
            "import research_report as plugin; "
            "C=type('C',(),{'register_tool':lambda s,**k: print(k['name'])}); "
            "plugin.register(C())"
        )
        result = self.run_isolated(code)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            ["collect_research_source", "submit_research_report"],
        )

    def test_missing_shared_module_is_rejected_in_isolated_bundle(self):
        copy_bundle(self.root, missing="source_collection.py")
        result = self.run_isolated(
            "import research_report.tools as tools; tools._modules()"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source_collection", result.stderr)

    def test_update_script_allowlists_exact_bundle(self):
        source = UPDATE.read_text()
        files = re.search(r"^FILES=\(([^)]*)\)$", source, re.MULTILINE)[1]
        shared = re.search(r"^SHARED=\(([^)]*)\)$", source, re.MULTILINE)[1]
        self.assertEqual(tuple(files.split()), PLUGIN_FILES)
        self.assertEqual(tuple(shared.split()), SHARED_FILES)
        self.assertIn('[[ ! -L "$PLUGIN" ]]', source)
        self.assertIn("unexpected installed plugin file", source)


class UpdateScriptRefusalTests(unittest.TestCase):
    def setUp(self):
        # Fixture modes must not depend on the host umask (0002 makes 0775 homes).
        self.addCleanup(os.umask, os.umask(0o022))
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "repo"
        self.home = self.root / "home"
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        for name, body in (
            ("hermes", "#!/bin/sh\nprintf 'doctor ok\\n'\n"),
            ("systemctl", "#!/bin/sh\nexit 0\n"),
        ):
            executable = self.fake_bin / name
            executable.write_text(body, encoding="utf-8")
            executable.chmod(0o700)
        destination = (
            self.repo / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion"
        )
        (destination / "deploy").mkdir(parents=True)
        shutil.copyfile(UPDATE, destination / "deploy/update-hermes-plugin.sh")
        copy = destination / "hermes-plugin"
        copy.mkdir()
        for name in PLUGIN_FILES:
            shutil.copyfile(PLUGIN / name, copy / name)
        publisher = destination / "publisher"
        publisher.mkdir()
        for name in SHARED_FILES:
            shutil.copyfile(PUBLISHER / name, publisher / name)
        self.git("init", "-q", "-b", "main")
        self.git("add", ".")
        self.git(
            "-c",
            "user.name=fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "fixture",
        )
        self.git("remote", "add", "origin", str(self.repo))

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            capture_output=True,
            check=True,
        )

    def run_update(self):
        script = (
            self.repo
            / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/deploy/update-hermes-plugin.sh"
        )
        return subprocess.run(
            ["bash", str(script)],
            env={
                **os.environ,
                "HOME": str(self.home),
                "PATH": f"{self.fake_bin}:{os.environ['PATH']}",
            },
            capture_output=True,
            check=False,
            text=True,
        )

    def test_symlink_plugin_directory_is_rejected_before_install(self):
        plugins = self.home / ".hermes/plugins"
        plugins.mkdir(parents=True)
        target = self.root / "outside"
        target.mkdir()
        (plugins / "research-report").symlink_to(target, target_is_directory=True)
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugin directory is a symlink", result.stderr)
        self.assertEqual(list(target.iterdir()), [])

    def test_unexpected_installed_file_is_rejected_before_install(self):
        plugin = self.home / ".hermes/plugins/research-report"
        plugin.mkdir(parents=True)
        marker = plugin / "extra.py"
        marker.write_text("untouched", encoding="utf-8")
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexpected installed plugin file", result.stderr)
        self.assertEqual(marker.read_text(), "untouched")

    def test_group_writable_plugin_parent_is_rejected_before_fetch(self):
        plugins = self.home / ".hermes/plugins"
        plugins.mkdir(parents=True)
        plugins.chmod(0o770)
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"unsafe plugin ancestor: {plugins} (mode 0770", result.stderr)
        self.assertFalse((plugins / "research-report").exists())

    def test_group_writable_plugin_directory_is_rejected_before_install(self):
        plugin = self.home / ".hermes/plugins/research-report"
        plugin.mkdir(parents=True)
        plugin.chmod(0o770)
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"unsafe plugin directory: {plugin} (mode 0770", result.stderr)
        self.assertEqual(list(plugin.iterdir()), [])

    def test_group_writable_installed_file_is_rejected_before_install(self):
        plugin = self.home / ".hermes/plugins/research-report"
        plugin.mkdir(parents=True)
        installed = plugin / "tools.py"
        installed.write_text("untouched", encoding="utf-8")
        installed.chmod(0o660)
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            f"unsafe installed plugin file: {installed} (mode 0660", result.stderr
        )
        self.assertEqual(installed.read_text(encoding="utf-8"), "untouched")

    def test_hardlinked_installed_file_is_rejected_before_install(self):
        plugin = self.home / ".hermes/plugins/research-report"
        plugin.mkdir(parents=True)
        installed = plugin / "tools.py"
        installed.write_text("untouched", encoding="utf-8")
        other_link = self.root / "outside-tools.py"
        os.link(installed, other_link)
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe installed plugin file", result.stderr)
        self.assertEqual(other_link.read_text(encoding="utf-8"), "untouched")

    def test_unsafe_bytecode_cache_is_rejected_before_install(self):
        cache = self.home / ".hermes/plugins/research-report/__pycache__"
        cache.mkdir(parents=True)
        cache.chmod(0o770)
        cached = cache / "tools.cpython-313.pyc"
        cached.write_bytes(b"synthetic-bytecode")
        cached.chmod(0o600)
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe plugin bytecode directory", result.stderr)
        self.assertEqual(cached.read_bytes(), b"synthetic-bytecode")

    def test_safe_cache_is_removed_and_excluded_from_source_only_backup(self):
        plugin = self.home / ".hermes/plugins/research-report"
        cache = plugin / "__pycache__"
        cache.mkdir(parents=True, mode=0o700)
        cache.chmod(0o700)
        cached = cache / "tools.cpython-313.pyc"
        cached.write_bytes(b"synthetic-bytecode")
        cached.chmod(0o600)
        installed = plugin / "tools.py"
        installed.write_text("previous-reviewed-source", encoding="utf-8")
        installed.chmod(0o600)

        result = self.run_update()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(cache.exists())
        backups = list(
            (self.home / ".hermes/plugins").glob(".research-report-backup-*")
        )
        self.assertEqual(len(backups), 1)
        backup = backups[0]
        self.assertEqual(backup.stat().st_mode & 0o777, 0o700)
        self.assertFalse((backup / "__pycache__").exists())
        self.assertEqual({path.name for path in backup.iterdir()}, {"tools.py"})
        self.assertEqual(
            (backup / "tools.py").read_text(encoding="utf-8"),
            "previous-reviewed-source",
        )
        self.assertEqual((backup / "tools.py").stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
