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
RUNBOOKS = ROOT / "docs/05.operations/runbooks/04-security-and-secrets"
RUNBOOK = RUNBOOKS / "0105-openbao-maintenance-window.md"


class OwnerWindowScriptTests(unittest.TestCase):
    def test_runbook_copies_and_calls_every_step(self):
        runbook = "".join(
            (RUNBOOKS / name).read_text()
            for name in (
                "0085-openbao.md",
                "0103-openbao-renderer-delivery.md",
                "0104-openbao-metrics-credential.md",
                "0105-openbao-maintenance-window.md",
            )
        )
        bootstrap = (WINDOW.parent / "p01-bootstrap.sh").read_text()
        manifest = bootstrap.split("<<'P01_SOURCE_MANIFEST'\n", 1)[1]
        # The runbook runs the bootstrap through p01_run, never a pasted copy.
        self.assertNotIn("P01_SOURCE_MANIFEST", runbook)
        self.assertIn("p01-bootstrap.sh", runbook)
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

    def test_p01_run_keeps_its_trust_checks(self):
        runner = (RUNBOOKS / "0085-openbao.md").read_text()
        runner = runner.split("p01_git() {", 1)[1].split("```", 1)[0]
        for token in (
            "GIT_NO_REPLACE_OBJECTS=1",
            "GIT_CONFIG_NOSYSTEM=1",
            "'64512:4338469:1000 64512:4338470:1000'",
            "--no-textconv",
            "hash-object --no-filters",
            "findmnt -n -T",
            '/usr/bin/bash "$f"',
            "BASH_ENV ENV",
        ):
            with self.subTest(token=token):
                self.assertIn(token, runner)

    def test_bootstrap_records_paths_only_after_every_pin(self):
        bootstrap = (WINDOW.parent / "p01-bootstrap.sh").read_text()
        record = bootstrap.index('>>"$XDG_RUNTIME_DIR/p01-window.vars"')
        self.assertGreater(record, bootstrap.index("\nP01_SOURCE_MANIFEST\n"))
        self.assertEqual(1, bootstrap.count('>>"$XDG_RUNTIME_DIR/p01-window.vars"'))
        self.assertNotIn("readonly", bootstrap)

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

    def status(self, directory, *, sealed, expires, alert_state, stopped=True):
        bin_dir = Path(directory) / "bin"
        bin_dir.mkdir()
        docker = bin_dir / "docker"
        docker.write_text(
            "#!/bin/sh\n"
            'case "$*" in\n'
            "  'ps -a --filter name=^openbao$ --filter name=^openbao-agent$'*)"
            " echo 'openbao: Up 1 hour (healthy)'; echo 'openbao-agent: Up 1 hour (healthy)' ;;\n"
            "  'exec openbao bao status -format=json')"
            f' echo \'{{"sealed":{sealed},"ha_enabled":true,"is_self":true,"version":"2.7.1"}}\' ;;\n'
            "  *api/v1/alerts*)"
            f' echo \'{{"data":{{"alerts":[{{"labels":{{"alertname":"OpenBaoMetricsScrapeFailing"}},'
            f'"state":"{alert_state}","activeAt":"2026-10-24T10:04:53Z"}}]}}}}\' ;;\n'
            "  *api/v1/targets*)"
            ' echo \'{"data":{"activeTargets":[{"labels":{"job":"openbao"},'
            '"health":"up","lastError":""}]}}\' ;;\n'
            "  'ps -a --filter label=com.docker.compose.project=hy-home-infra'*)"
            + (
                " echo 'airflow-dag-processor Exited (1) 2 hours ago'"
                if stopped
                else " echo 'seaweedfs-buckets Exited (0) 6 days ago'"
            )
            + " ;;\n"
            "esac\n"
        )
        docker.chmod(0o755)
        journal = Path(directory) / "journal"
        journal.mkdir(mode=0o700)
        (journal / "issuance.anchor").write_text(
            '{"nonce":"synthetic-nonce-value","issuance_id":"synthetic-nonce-value",'
            '"schema_version":2,"state":"complete"}'
        )
        custody = Path(directory) / "metrics.custody"
        custody.write_text(
            f"accessor=synthetic-accessor-value\nexpires={expires}\npolicy=prometheus\n"
        )
        return subprocess.run(
            ["bash", str(WINDOW), "status"],
            env={
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "XDG_RUNTIME_DIR": directory,
                "issuance_journal": str(journal),
                "metrics_custody": str(custody),
            },
            capture_output=True,
            text=True,
            check=False,
        )

    def test_status_reports_health_without_values(self):
        import datetime

        far = (
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=300)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        near = (
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=10)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        with tempfile.TemporaryDirectory() as directory:
            ok = self.status(
                directory, sealed="false", expires=far, alert_state="inactive"
            )
            self.assertIn("server: sealed=false ha=active", ok.stdout)
            self.assertIn("journal: complete schema=2", ok.stdout)
            self.assertIn("metrics token: expires " + far, ok.stdout)
            self.assertIn("stopped: airflow-dag-processor Exited (1)", ok.stdout)
            self.assertNotIn("synthetic-accessor-value", ok.stdout + ok.stderr)
            # A non-zero exit only for problems; the stopped container is one.
            self.assertEqual(1, ok.returncode)
        with tempfile.TemporaryDirectory() as directory:
            clean = self.status(
                directory,
                sealed="false",
                expires=far,
                alert_state="inactive",
                stopped=False,
            )
            self.assertIn("problems: 0", clean.stdout)
            self.assertNotIn("WARN:", clean.stdout)
            self.assertNotIn("synthetic-nonce-value", clean.stdout + clean.stderr)
            self.assertEqual(0, clean.returncode)
        with tempfile.TemporaryDirectory() as directory:
            bad = self.status(
                directory, sealed="true", expires=near, alert_state="firing"
            )
            self.assertIn("WARN: server sealed", bad.stdout)
            self.assertIn("WARN: metrics token expires in", bad.stdout)
            self.assertIn("alert: OpenBaoMetricsScrapeFailing firing", bad.stdout)
            self.assertNotIn("synthetic-accessor-value", bad.stdout + bad.stderr)
            self.assertEqual(1, bad.returncode)

    def test_metrics_rotate_needs_w1_root_and_the_reviewed_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = self.runtime(directory)
            result = self.run_window(runtime, "metrics-rotate")
            self.assertIn("run w1 first", result.stderr)
            self.assertEqual(1, result.returncode)
            custody = Path(directory) / "p01-custody.synthetic"
            custody.mkdir()
            root = custody / "root.token"
            root.write_text("synthetic-root-value")
            root.chmod(0o600)
            runtime = self.runtime(
                directory,
                P01_CUSTODY_DIR=custody,
                P01_CLIENT_DIR=Path(directory) / "client",
            )
            result = self.run_window(runtime, "metrics-rotate")
            self.assertIn("reviewed prometheus.hcl missing", result.stderr)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("synthetic-root-value", result.stdout + result.stderr)
            self.assertEqual(
                [], [p for p in os.listdir(directory) if p.startswith("p01-metrics")]
            )

    def test_cleanup_keeps_an_unrevoked_metrics_token(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory) / "p01-metrics.synthetic"
            work.mkdir()
            (work / "new.token").write_text("synthetic-metrics-value")
            (work / "new.unrevoked").touch()
            runtime = self.runtime(directory)
            result = self.run_window(runtime, "cleanup", "--keep-root")
            self.assertIn("run metrics-revoke", result.stderr)
            self.assertEqual(1, result.returncode)
            self.assertTrue((work / "new.token").exists())
            self.assertNotIn("synthetic-metrics-value", result.stdout + result.stderr)
            result = self.run_window(
                runtime, "cleanup", "--keep-root", "--discard-metrics"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse(work.exists())

    def test_metrics_revoke_without_leftovers_does_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            custody = Path(directory) / "p01-custody.synthetic"
            custody.mkdir()
            root = custody / "root.token"
            root.write_text("synthetic-root-value")
            root.chmod(0o600)
            runtime = self.runtime(
                directory,
                P01_CUSTODY_DIR=custody,
                P01_METRICS_DIR=Path(directory) / "p01-metrics.gone",
            )
            result = self.run_window(runtime, "metrics-revoke")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("nothing to resolve", result.stdout)
            self.assertNotIn("synthetic-root-value", result.stdout + result.stderr)

    def stub(self, bin_dir, name, body):
        path = bin_dir / name
        path.write_text("#!/bin/sh\n" + body)
        path.chmod(0o755)

    def test_renderer_expiry_prints_timestamps_only(self):
        with tempfile.TemporaryDirectory() as directory:
            bin_dir = Path(directory) / "bin"
            bin_dir.mkdir()
            self.stub(
                bin_dir,
                "docker",
                'case "$1" in\n'
                "  logs) echo '2026-10-28T09:32:40.100Z [INFO]  expiration: revoked lease:"
                " lease_id=auth/approle/login/synthetic-lease-value'\n"
                "        echo '2026-10-28T09:33:00.000Z [INFO]  core: other line' ;;\n"
                '  exec) echo \'{"active_time":"2026-10-28T09:32:39Z"}\' ;;\n'
                "esac\n",
            )
            result = subprocess.run(
                ["bash", str(WINDOW), "renderer-expiry", "2026-10-27T07:45:00Z"],
                env={"PATH": f"{bin_dir}:/usr/bin:/bin", "XDG_RUNTIME_DIR": directory},
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                "2026-10-28T09:32:40.100Z\n"
                "revocations: 1\n"
                "log starts: 2026-10-28T09:32:40.100Z\n"
                "server active since: 2026-10-28T09:32:39Z\n",
                result.stdout,
            )
            self.assertNotIn("synthetic-lease-value", result.stdout + result.stderr)

    def test_host_hold_holds_the_runtime_packages(self):
        with tempfile.TemporaryDirectory() as directory:
            bin_dir = Path(directory) / "bin"
            bin_dir.mkdir()
            log = Path(directory) / "sudo.log"
            self.stub(bin_dir, "sudo", f'echo "$*" >>{log}; cat >/dev/null\n')
            self.stub(bin_dir, "dpkg-query", "echo 'install ok installed'\n")
            self.stub(
                bin_dir,
                "apt-mark",
                "printf '%s\\n' containerd.io docker-ce docker-ce-cli vim\n",
            )
            result = subprocess.run(
                ["bash", str(WINDOW), "host-hold"],
                env={"PATH": f"{bin_dir}:/usr/bin:/bin", "XDG_RUNTIME_DIR": directory},
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(
                "apt-mark hold containerd.io docker-ce docker-ce-cli\n"
                "tee /etc/needrestart/conf.d/hy-home.conf\n",
                log.read_text(),
            )
            self.assertIn("needrestart: containerd and docker excluded", result.stdout)
            self.assertNotIn("vim", result.stdout)

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
