"""Public schema and offline CLI contracts, with synthetic stdin only."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tests.lib.ops.test_openbao_consumer_migration import receipt, wave

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts/operations/openbao-consumer-migration.py"
PACKAGE = ROOT / "infra/03-security/openbao/consumer-migration"


def run_cli(arguments, raw=b""):
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        input=raw,
        capture_output=True,
        cwd=ROOT,
        timeout=8,
        check=False,
    )


class PublicMigrationContractTests(unittest.TestCase):
    def test_closed_schemas_accept_only_pre_copy_synthetic_receipts(self):
        schemas = {}
        for kind, candidate in (("wave", wave()), ("receipt", receipt())):
            schema = json.loads((PACKAGE / f"{kind}.schema.json").read_bytes())
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            self.assertTrue(validator.is_valid(candidate))
            self.assertFalse(
                validator.is_valid({**candidate, "token": "private-marker"})
            )
            self.assertFalse(
                validator.is_valid({**candidate, "evidence_kind": "native"})
            )
            schemas[kind] = schema
        self.assertEqual(
            schemas["wave"]["$defs"]["catalog"], schemas["receipt"]["$defs"]["catalog"]
        )
        candidate = receipt()
        candidate["items"][0].update(state="recoverable", kv_version=1)
        self.assertFalse(Draft202012Validator(schemas["receipt"]).is_valid(candidate))

    def test_cli_validates_synthetic_documents_without_echoing_them(self):
        for kind, candidate in (("wave", wave()), ("receipt", receipt())):
            result = run_cli(["validate-" + kind], json.dumps(candidate).encode())
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(b"PASS: public contract shape only\n", result.stdout)
            self.assertEqual(b"", result.stderr)
            self.assertNotIn(candidate["consumer"].encode(), result.stdout)

    def test_cli_errors_do_not_echo_argv_json_or_tracebacks(self):
        for arguments, raw in (
            (["--private-marker"], b""),
            (["apply", "private-marker"], b""),
            (["validate-wave", "private-marker"], b""),
            (["validate-wave"], b"private-marker"),
            (["validate-wave"], b'{"token":"private-marker"}'),
            (["validate-receipt"], b'{"a":1,"a":2}'),
            (["validate-wave"], b" " * 131073),
        ):
            result = run_cli(arguments, raw)
            self.assertEqual(2, result.returncode)
            self.assertEqual(b"", result.stdout)
            self.assertNotIn(b"private-marker", result.stderr)
            self.assertNotIn(b"Traceback", result.stderr)
            self.assertTrue(result.stderr.startswith(b"FAIL: "))

    def test_cli_help_has_no_copy_delete_rotation_or_private_inputs(self):
        result = run_cli(["--help"])
        self.assertEqual(0, result.returncode)
        self.assertIn(b"validate-wave", result.stdout)
        self.assertNotIn(b"--token", result.stdout)
        self.assertNotIn(b"--apply", result.stdout)
        self.assertIn(b"stdin", result.stdout)

    def test_cli_stdin_wait_has_a_whole_operation_deadline(self):
        process = subprocess.Popen(
            [sys.executable, str(CLI), "validate-wave"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )
        try:
            process.wait(timeout=8)
            self.assertEqual(2, process.returncode)
            self.assertEqual(b"FAIL: public_input_timeout\n", process.stderr.read())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            for stream in (process.stdin, process.stdout, process.stderr):
                stream.close()

    def test_new_folder_has_korean_navigation(self):
        text = (PACKAGE / "README.md").read_text()
        self.assertIn("wave.schema.json", text)
        self.assertIn("receipt.schema.json", text)
        self.assertTrue(any("\uac00" <= character <= "\ud7a3" for character in text))


VERIFIER = PACKAGE / "verify-grafana-consumption.sh"
FAKE_DOCKER = r"""#!/usr/bin/env python3
import os, subprocess, sys
args, env = sys.argv[1:], {}
if args[0] == "inspect":
    states = os.environ.get("FAKE_HEALTH", "healthy").split(",")
    counter = os.path.join(os.environ["FAKE_ROOT"], "inspect-calls")
    n = int(open(counter).read()) if os.path.exists(counter) else 0
    open(counter, "w").write(str(n + 1))
    print(states[min(n, len(states) - 1)])
    sys.exit(0)
assert args.pop(0) == "exec"
while args[0] == "-e":
    key, _, value = args[1].partition("=")
    env[key] = value
    args = args[2:]
root = os.path.join(os.environ["FAKE_ROOT"], args.pop(0))
local = lambda path: root + path
if args[0] == "printenv":
    print(os.environ.get("FAKE_GF_FILE", "/run/secrets/grafana_admin_password"))
elif args[0] == "cat":
    sys.stdout.buffer.write(open(local(args[1]), "rb").read())
elif args[:2] == ["test", "-s"]:
    sys.exit(0 if os.path.getsize(local(args[2])) else 1)
elif args[:2] == ["sh", "-c"]:
    env.update(PATH=os.environ["FAKE_BIN"] + ":/usr/bin:/bin", GF_SECURITY_ADMIN_USER="admin",
               MOUNTED=local(env["MOUNTED"]), FAKE_ROOT=os.environ["FAKE_ROOT"],
               FAKE_CURL_NO_RESPONSE=os.environ.get("FAKE_CURL_NO_RESPONSE", "0"))
    sys.exit(subprocess.run(["sh", "-c", args[2]], env=env).returncode)
"""
FAKE_CURL = r"""#!/usr/bin/env python3
import os, sys
open(os.path.join(os.environ["FAKE_ROOT"], "curl-argv"), "a").write(" ".join(sys.argv) + "\n")
config = sys.stdin.read()
counter = os.path.join(os.environ["FAKE_ROOT"], "curl-calls")
calls = int(open(counter).read()) + 1 if os.path.exists(counter) else 1
open(counter, "w").write(str(calls))
if calls <= int(os.environ.get("FAKE_CURL_NO_RESPONSE", "0")):
    sys.stdout.write("000")
    sys.exit(28)
expected = open(os.path.join(os.environ["FAKE_ROOT"], "expected-config")).read()
sys.stdout.write("200" if config == expected else "401")
"""


class GrafanaConsumptionVerifierTests(unittest.TestCase):
    def run_verifier(
        self,
        rendered,
        mounted,
        version=b"3",
        login=None,
        port=None,
        gf_file=None,
        misses=0,
        health=None,
    ):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "openbao-agent/openbao/out/observability"
            run = root / "grafana/run/secrets"
            out.mkdir(parents=True)
            run.mkdir(parents=True)
            (out / "grafana_admin_password.txt").write_bytes(rendered)
            (out / "grafana_admin_password.version").write_bytes(version)
            (run / "grafana_admin_password").write_bytes(mounted)
            agent_dir = root / "grafana/run/openbao/observability"
            agent_dir.mkdir(parents=True)
            (agent_dir / "grafana_admin_password.txt").write_bytes(mounted)
            login = mounted.rstrip(b"\n") if login is None else login
            quoted = login.replace(b"\\", b"\\\\").replace(b'"', b'\\"')
            (root / "expected-config").write_bytes(b'user = "admin:' + quoted + b'"\n')
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name, body in (("docker", FAKE_DOCKER), ("curl", FAKE_CURL)):
                (bin_dir / name).write_text(body)
                (bin_dir / name).chmod(0o755)
            result = subprocess.run(
                ["bash", str(VERIFIER)],
                capture_output=True,
                env={
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "FAKE_ROOT": str(root),
                    "FAKE_BIN": str(bin_dir),
                    **({"GRAFANA_PORT": port} if port else {}),
                    **({"FAKE_GF_FILE": gf_file} if gf_file else {}),
                    "VERIFY_RETRY_SLEEP": "0",
                    "VERIFY_HEALTH_SLEEP": "0",
                    "VERIFY_HEALTH_TRIES": "3",
                    **({"FAKE_HEALTH": health} if health else {}),
                    **({"FAKE_CURL_NO_RESPONSE": str(misses)} if misses else {}),
                },
                timeout=30,
                check=False,
            )
            argv = (
                (root / "curl-argv").read_bytes()
                if (root / "curl-argv").exists()
                else b""
            )
            self.calls = (
                int((root / "curl-calls").read_text())
                if (root / "curl-calls").exists()
                else 0
            )
        return result, argv

    def test_equal_bytes_and_login_pass_without_printing_the_value(self):
        marker = b'Synth"etic\\marker-1'
        result, argv = self.run_verifier(marker, marker + b"\n")
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual(
            b"PASS grafana_healthy\n"
            b"PASS consumed_file path=/run/secrets/grafana_admin_password\n"
            b"PASS rendered_version version=3\nPASS mounted_equals_rendered\n"
            b"PASS admin_login http=200\n",
            result.stdout,
        )
        for stream in (result.stdout, result.stderr, argv):
            self.assertNotIn(b"Synth", stream)

    def test_mismatch_wrong_login_bad_version_and_empty_fail(self):
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-b")
        self.assertEqual(1, result.returncode)
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", login=b"other")
        self.assertIn(b"FAIL admin_login http=401\n", result.stdout)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", version=b"x1")
        self.assertIn(b"FAIL rendered_version\n", result.stdout)
        result, _ = self.run_verifier(b"", b"\n")
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        self.assertEqual(1, result.returncode)

    def test_cr_newline_only_and_port_injection_fail(self):
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a\r\n")
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        result, _ = self.run_verifier(b"\n", b"")
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        result, argv = self.run_verifier(
            b"synthetic-a", b"synthetic-a", port="3000@evil.example"
        )
        self.assertEqual(2, result.returncode)
        self.assertEqual(b"", result.stdout)
        self.assertEqual(b"", argv)

    def test_follows_the_agent_directory_file_and_rejects_other_paths(self):
        path = "/run/openbao/observability/grafana_admin_password.txt"
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", gf_file=path)
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn(f"PASS consumed_file path={path}\n".encode(), result.stdout)
        result, _ = self.run_verifier(
            b"synthetic-a", b"synthetic-a", gf_file="/etc/passwd"
        )
        self.assertEqual(1, result.returncode)
        self.assertEqual(b"PASS grafana_healthy\nFAIL consumed_file\n", result.stdout)

    def test_grafana_binds_the_agent_directory_read_only_without_creating_it(self):
        import yaml

        compose = yaml.safe_load(
            (ROOT / "infra/06-observability/docker-compose.yml").read_text()
        )
        grafana = compose["services"]["grafana"]
        binds = [
            v
            for v in grafana["volumes"]
            if isinstance(v, dict) and v["target"] == "/run/openbao/observability"
        ]
        self.assertEqual(1, len(binds))
        self.assertIs(True, binds[0]["read_only"])
        self.assertIs(False, binds[0]["bind"]["create_host_path"])
        self.assertEqual(
            "${GRAFANA_ADMIN_PASSWORD_FILE:-/run/secrets/grafana_admin_password}",
            grafana["environment"]["GF_SECURITY_ADMIN_PASSWORD__FILE"],
        )

    def test_login_retries_only_when_no_http_status_came_back(self):
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", misses=1)
        self.assertIn(b"PASS admin_login http=200\n", result.stdout)
        self.assertEqual(2, self.calls)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", misses=3)
        self.assertIn(b"FAIL admin_login http=000\n", result.stdout)
        self.assertEqual(3, self.calls)
        # A real HTTP status is final: a wrong password is tried exactly once.
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", login=b"other")
        self.assertIn(b"FAIL admin_login http=401\n", result.stdout)
        self.assertEqual(1, self.calls)

    def test_waits_for_grafana_health_before_any_check(self):
        result, _ = self.run_verifier(
            b"synthetic-a", b"synthetic-a", health="starting,starting,healthy"
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertTrue(
            result.stdout.startswith(b"WAIT grafana_healthy\nPASS grafana_healthy\n")
        )
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", health="starting")
        self.assertEqual(1, result.returncode)
        self.assertEqual(
            b"WAIT grafana_healthy\nFAIL grafana_healthy state=starting\n",
            result.stdout,
        )
        self.assertEqual(0, self.calls)
