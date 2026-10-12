"""Synthetic subprocess lock ownership; never executes the secret generator."""

import importlib.util
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from scripts.lib.ops import retire_materials

ROOT = Path(__file__).resolve().parents[2]


class LockInheritanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="smtp-held-lock-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in (
            "scripts",
            "scripts/lib",
            "scripts/lib/ops",
            "scripts/operations",
            "secrets",
        ):
            (self.root / directory).mkdir(exist_ok=True)
        for directory in ("scripts", "scripts/lib", "scripts/lib/ops"):
            (self.root / directory / "__init__.py").write_text("")
        helper = self.root / "scripts/lib/ops/smtp_contract.py"
        helper.write_bytes((ROOT / "scripts/lib/ops/smtp_contract.py").read_bytes())
        retire_helper = self.root / "scripts/lib/ops/retire_materials.py"
        retire_helper.write_bytes((ROOT / "scripts/lib/ops/retire_materials.py").read_bytes())
        spec = importlib.util.spec_from_file_location("synthetic_lock", helper)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        source = (ROOT / "scripts/operations/gen-secrets.sh").read_text()
        self.wrapper = re.search(r"<<'PY_LOCK'\n(.*?)\nPY_LOCK", source, re.S).group(1)
        self.stub = self.root / "scripts/operations/gen-secrets.sh"
        self.stub.write_text(
            'REPO_ROOT="${HYHOME_GENERATOR_HELD_ROOT:?}"\n'
            'dispatch() { printf "%s" "$BASHPID" > "$REPO_ROOT/mutator.pid"; while [[ ! -f "$REPO_ROOT/release" ]]; do sleep 0.02; done; printf continued > "$REPO_ROOT/continued"; }\n'
        )
        self.holder = None
        self.addCleanup(self.stop_holder)

    def stop_holder(self):
        if self.holder is None:
            return
        try:
            os.killpg(self.holder.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        self.holder.wait(timeout=5)

    def wait_for(self, predicate):
        deadline = time.monotonic() + 5
        while not predicate():
            if time.monotonic() >= deadline:
                self.fail("synthetic child deadline")
            time.sleep(0.01)

    def smtp_busy(self):
        try:
            with self.module.retirement_lock(self.root):
                return False
        except self.module.ContractError as error:
            self.assertEqual("retirement_lock_busy", str(error))
            return True

    def cln_busy(self):
        try:
            with retire_materials.retirement_lock(self.root):
                return False
        except OSError:
            return True

    def busy(self):
        return self.smtp_busy() and self.cln_busy()

    def start_holder(self):
        self.holder = subprocess.Popen(
            [
                sys.executable,
                "-c",
                self.wrapper,
                str(self.stub),
                str(self.root),
                str(self.root),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        self.wait_for(lambda: (self.root / "mutator.pid").exists())
        self.assertTrue(self.busy())
        return int((self.root / "mutator.pid").read_text())

    def test_parent_death_keeps_actual_mutator_lock_until_exit(self):
        mutator = self.start_holder()
        self.holder.kill()
        self.assertEqual(-signal.SIGKILL, self.holder.wait(timeout=5))
        os.kill(mutator, 0)
        self.assertTrue(
            self.busy(), "second writer acquired while actual mutator remains live"
        )
        (self.root / "release").touch()
        self.wait_for(lambda: (self.root / "continued").exists())
        self.wait_for(lambda: not self.busy())

    def test_parent_death_after_root_replacement_keeps_mutator_on_held_inode(self):
        mutator = self.start_holder()
        displaced = self.root.with_name(self.root.name + "-displaced")
        self.root.rename(displaced)
        self.root.mkdir()
        (self.root / "secrets").mkdir()
        with retire_materials.retirement_lock(self.root):
            pass
        self.holder.kill()
        self.assertEqual(-signal.SIGKILL, self.holder.wait(timeout=5))
        os.kill(mutator, 0)
        self.assertTrue((displaced / "mutator.pid").exists())
        self.assertFalse((self.root / "mutator.pid").exists())
        (displaced / "release").touch()
        self.wait_for(lambda: (displaced / "continued").exists())
        self.assertFalse((self.root / "continued").exists())

    def test_normal_child_exit_releases_lock(self):
        self.start_holder()
        (self.root / "release").touch()
        self.assertEqual(0, self.holder.wait(timeout=5))
        self.assertFalse(self.busy())

    def test_default_identity_contract_and_exception_release(self):
        expected = self.module.root_identity(self.root)
        with self.assertRaisesRegex(RuntimeError, "synthetic"):
            with self.module.retirement_lock(self.root, expected) as result:
                self.assertEqual(expected, result)
                self.assertTrue(self.busy())
                raise RuntimeError("synthetic")
        self.assertFalse(self.busy())

    def test_opt_in_fd_is_same_lock_identity_and_closed_on_exit(self):
        with self.module.retirement_lock(self.root, with_fd=True) as (identity, fd):
            self.assertEqual(self.module.root_identity(self.root), identity)
            held = os.fstat(fd)
            named = (self.root / self.module.LOCK_PATH).stat()
            self.assertEqual((held.st_dev, held.st_ino), (named.st_dev, named.st_ino))
            self.assertFalse(os.get_inheritable(fd))
            self.assertTrue(self.smtp_busy())
        with self.assertRaises(OSError):
            os.fstat(fd)
        self.assertFalse(self.smtp_busy())

    def test_opt_in_fds_include_root_and_smtp_and_close_on_exit(self):
        with self.module.retirement_lock(self.root, with_fds=True) as (identity, fds):
            self.assertEqual(self.module.root_identity(self.root), identity)
            self.assertEqual(2, len(fds))
            for fd in fds:
                os.fstat(fd)
                self.assertFalse(os.get_inheritable(fd))
            self.assertTrue(self.smtp_busy())
            self.assertTrue(self.cln_busy())
        for fd in fds:
            with self.assertRaises(OSError):
                os.fstat(fd)
        self.assertFalse(self.smtp_busy())
        self.assertFalse(self.cln_busy())

    def test_opt_in_exception_closes_fd_and_releases(self):
        fd = None
        with self.assertRaisesRegex(RuntimeError, "synthetic"):
            with self.module.retirement_lock(self.root, with_fd=True) as (_, fd):
                raise RuntimeError("synthetic")
        with self.assertRaises(OSError):
            os.fstat(fd)
        self.assertFalse(self.busy())

    def test_opt_in_rejects_symlink_shared_and_wrong_mode_lock(self):
        target = self.root / self.module.LOCK_PATH
        other = self.root / "synthetic-lock"
        other.write_text("")
        other.chmod(0o600)
        for kind in ("symlink", "shared", "mode"):
            with self.subTest(kind=kind):
                if kind == "symlink":
                    target.symlink_to(other)
                elif kind == "shared":
                    os.link(other, target)
                else:
                    target.write_text("")
                    target.chmod(0o644)
                with self.assertRaises((OSError, self.module.ContractError)):
                    with self.module.retirement_lock(self.root, with_fd=True):
                        self.fail("unsafe lock accepted")
                target.unlink()

    def test_invalid_fd_option_rejects_before_creating_lock(self):
        for value in (1, "true", None):
            with self.subTest(value=value):
                with self.assertRaisesRegex(
                    self.module.ContractError, "invalid_lock_fd_option"
                ):
                    with self.module.retirement_lock(self.root, with_fd=value):
                        self.fail("invalid opt-in accepted")
                self.assertFalse((self.root / self.module.LOCK_PATH).exists())

    def test_opt_in_rejects_changed_root_identity(self):
        wrong = {**self.module.root_identity(self.root), "st_ino": -1}
        with self.assertRaisesRegex(
            self.module.ContractError, "root_identity_mismatch"
        ):
            with self.module.retirement_lock(self.root, wrong, with_fd=True):
                self.fail("wrong root accepted")


if __name__ == "__main__":
    unittest.main()
