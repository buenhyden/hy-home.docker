"""Owner scripts for the RUN-0085 window and the OIDC client secret batch."""

import os
import re
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WINDOW = ROOT / "infra/03-security/openbao/scripts/owner-window.sh"
K8S = ROOT / "infra/03-security/openbao/scripts/k8s-writers.sh"
OIDC = ROOT / "infra/03-security/openbao/consumer-migration/oidc-client-secrets.sh"
RUNBOOK = ROOT / "docs/05.operations/runbooks/04-security-and-secrets/0085-openbao.md"


class OwnerWindowScriptTests(unittest.TestCase):
    def test_runbook_copies_and_calls_every_step(self):
        runbook = RUNBOOK.read_text()
        manifest = runbook.split("<<'P01_SOURCE_MANIFEST'\n", 1)[1]
        self.assertIn(" infra/03-security/openbao/scripts/owner-window.sh\n", manifest)
        self.assertIn(" infra/03-security/openbao/scripts/k8s-writers.sh\n", manifest)
        for script, minimum in ((WINDOW, 20), (K8S, 7)):
            rows = re.findall(r"^(\S+(?: \| \S+)*)\)$", script.read_text(), re.M)
            steps = {
                s
                for row in rows
                for s in row.split(" | ")
                if re.fullmatch(r"[a-z][a-z0-9-]*", s)
            }
            self.assertGreaterEqual(len(steps), minimum)
            for step in steps:
                with self.subTest(script=script.name, step=step):
                    self.assertRegex(
                        runbook, rf'{re.escape(script.name)}"? {re.escape(step)}\b'
                    )

    def test_unknown_step_exits_two_without_touching_state(self):
        with tempfile.TemporaryDirectory() as runtime:
            result = subprocess.run(
                ["bash", str(WINDOW), "nope"],
                env={"PATH": "/usr/bin:/bin", "XDG_RUNTIME_DIR": runtime},
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode)
            self.assertEqual([], os.listdir(runtime))

    def test_cleanup_keeps_root_custody_until_w7_or_explicit_discard(self):
        with tempfile.TemporaryDirectory() as runtime:
            custody = Path(runtime) / "p01-custody.synthetic"
            custody.mkdir()
            root = custody / "root.token"
            root.write_text("synthetic")
            env = {"PATH": "/usr/bin:/bin", "XDG_RUNTIME_DIR": runtime}
            result = subprocess.run(
                ["bash", str(WINDOW), "cleanup"],
                env=env,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertTrue(root.exists())
            # An exported variable is not an option: the guard still holds.
            result = subprocess.run(
                ["bash", str(WINDOW), "cleanup"],
                env={**env, "P01_KEEP_ROOT": "0"},
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            subprocess.run(
                ["bash", str(WINDOW), "cleanup", "--keep-root"], env=env, check=True
            )
            self.assertTrue(root.exists())
            subprocess.run(
                ["bash", str(WINDOW), "cleanup", "--discard-root"], env=env, check=True
            )
            self.assertFalse(custody.exists())


class WindowGateTests(unittest.TestCase):
    """Fail-closed gates that need no OpenBao, Docker or cluster."""

    def runtime(self, directory, **values):
        runtime = Path(directory)
        lines = [f"declare -- {k}={v}" for k, v in values.items()]
        (runtime / "p01-window.vars").write_text("\n".join(lines) + "\n")
        return runtime

    def run_window(self, runtime, *args):
        return subprocess.run(
            ["bash", str(WINDOW), *args],
            env={"PATH": "/usr/bin:/bin", "XDG_RUNTIME_DIR": str(runtime)},
            capture_output=True,
            text=True,
            check=False,
        )

    def test_w3_hands_the_saved_k8s_state_to_the_writer_check(self):
        with tempfile.TemporaryDirectory() as directory:
            scripts = Path(directory) / "scripts"
            scripts.mkdir()
            seen = Path(directory) / "seen"
            (scripts / "k8s-writers.sh").write_text(
                f'printf "%s %s" "$1" "${{P01_K8S_STATE:-}}" >{seen}\nexit 1\n'
            )
            runtime = self.runtime(
                directory,
                P01_SCRIPT_DIR=scripts,
                P01_INPUTS=Path(directory) / "inputs",
                P01_K8S_STATE=Path(directory) / "k8s",
            )
            target = Path(directory) / "snapshot"
            result = self.run_window(runtime, "w3", str(target), "2.6.2")
            self.assertEqual(1, result.returncode)
            self.assertEqual(f"check {Path(directory) / 'k8s'}", seen.read_text())
            self.assertFalse(target.exists())

    def test_w3_without_state_needs_the_attestation(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = self.runtime(directory, P01_INPUTS=Path(directory) / "inputs")
            target = Path(directory) / "snapshot"
            result = self.run_window(runtime, "w3", str(target), "2.6.2")
            self.assertEqual(1, result.returncode)
            self.assertFalse(target.exists())

    def test_w4_needs_w3a_acceptance_and_w3b_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            inputs = Path(directory) / "inputs"
            inputs.mkdir()
            runtime = self.runtime(directory, P01_INPUTS=inputs)
            result = self.run_window(runtime, "w4", "2064/115612005")
            self.assertIn("W3a not accepted", result.stderr)
            (inputs / "w3a-accepted").touch()
            result = self.run_window(runtime, "w4", "2064/115612005")
            self.assertIn("no W3b receipt", result.stderr)
            self.assertEqual(1, result.returncode)

    def test_retire_token_refuses_a_shared_file_and_keeps_it(self):
        with tempfile.TemporaryDirectory() as directory:
            token = Path(directory) / "p01-operator.token"
            token.write_text("synthetic")
            token.chmod(0o644)
            result = self.run_window(Path(directory), "retire-token", str(token))
            self.assertEqual(1, result.returncode)
            self.assertTrue(token.exists())

    def test_finish_wait_and_refresh_need_a_restored_finish(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "k8s"
            state.mkdir()
            env = {
                "PATH": "/usr/bin:/bin",
                "P01_K8S_STATE": str(state),
                "P01_FORCE_REFRESH_APPROVAL": "synthetic",
            }
            for args in (["finish-wait"], ["force-refresh", "ns", "name"]):
                with self.subTest(args=args):
                    result = subprocess.run(
                        ["bash", str(K8S), *args],
                        env=env,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(1, result.returncode)
                    self.assertIn("run finish first", result.stderr)


class OidcClientSecretScriptTests(unittest.TestCase):
    def run_script(self, home, *args):
        bin_dir = home / "bin"
        bin_dir.mkdir(exist_ok=True)
        docker = bin_dir / "docker"
        docker.write_text('#!/bin/sh\n[ "$1" = inspect ] && echo true\nexit 0\n')
        docker.chmod(0o755)
        return subprocess.run(
            ["bash", str(OIDC), *args],
            env={
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "OIDC_HOME_ROOT": str(home),
                "VERIFY_HEALTH_TRIES": "1",
            },
            capture_output=True,
            check=False,
            text=True,
        )

    def test_cutover_and_rollback_change_only_that_variable(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            env = home / ".env"
            env.write_text("A=1\nDOZZLE_CLIENT_SECRET_FILE=/old\nB=2\n")
            env.chmod(0o640)
            self.run_script(home, "cutover", "dozzle")
            self.assertEqual(
                "A=1\nB=2\nDOZZLE_CLIENT_SECRET_FILE="
                "/run/openbao/dozzle/dozzle_client_secret.txt\n",
                env.read_text(),
            )
            self.assertEqual(0o640, stat.S_IMODE(env.stat().st_mode))
            self.run_script(home, "rollback", "dozzle")
            self.assertEqual("A=1\nB=2\n", env.read_text())
            self.assertEqual([".env", "bin"], sorted(os.listdir(home)))

    def test_unknown_service_leaves_env_alone(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / ".env").write_text("A=1\n")
            result = self.run_script(home, "cutover", "grafana")
            self.assertEqual(2, result.returncode)
            self.assertEqual("A=1\n", (home / ".env").read_text())


if __name__ == "__main__":
    unittest.main()
