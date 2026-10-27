"""Public schema and offline CLI contracts, with synthetic stdin only."""

import json
import re
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


KC_VERIFIER = PACKAGE / "verify-keycloak-consumption.sh"
FAKE_KC_DOCKER = r"""#!/usr/bin/env python3
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
    print(os.environ.get("FAKE_KC_FILE", "/run/secrets/keycloak_admin_password"))
elif args[0] == "cat":
    sys.stdout.buffer.write(open(local(args[1]), "rb").read())
elif args[:2] == ["sh", "-c"]:
    env.update(PATH="/usr/bin:/bin", KC_BOOTSTRAP_ADMIN_USERNAME="admin",
               MOUNTED=local(env["MOUNTED"]), FAKE_ROOT=os.environ["FAKE_ROOT"],
               FAKE_KC_NO_RESPONSE=os.environ.get("FAKE_KC_NO_RESPONSE", "0"))
    script = args[2].replace("/opt/keycloak/bin/", os.environ["FAKE_BIN"] + "/")
    sys.exit(subprocess.run(["sh", "-c", script], env=env).returncode)
"""
FAKE_KCADM = r"""#!/usr/bin/env python3
import os, sys
root = os.environ["FAKE_ROOT"]
open(os.path.join(root, "kcadm-argv"), "a").write(" ".join(sys.argv) + "\n")
config = sys.argv[sys.argv.index("--config") + 1]
open(os.path.join(root, "kcadm-config"), "a").write(config + "\n")
counter = os.path.join(root, "kcadm-calls")
calls = int(open(counter).read()) + 1 if os.path.exists(counter) else 1
open(counter, "w").write(str(calls))
if calls <= int(os.environ["FAKE_KC_NO_RESPONSE"]):
    sys.stderr.write("Failed to send request - Connection refused\n")
    sys.exit(1)
expected = open(os.path.join(root, "expected-password")).read()
if os.environ.get("KC_CLI_PASSWORD") != expected or sys.argv[-1] != "admin":
    sys.stderr.write("Invalid user credentials [invalid_grant]\n")
    sys.exit(1)
"""


class KeycloakConsumptionVerifierTests(unittest.TestCase):
    def run_verifier(
        self,
        rendered,
        mounted,
        version=b"2",
        login=None,
        port=None,
        kc_file=None,
        misses=0,
        health=None,
    ):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "openbao-agent/openbao/out/auth"
            out.mkdir(parents=True)
            (out / "keycloak_admin_password.txt").write_bytes(rendered)
            (out / "keycloak_admin_password.version").write_bytes(version)
            for path in (
                "keycloak/run/secrets/keycloak_admin_password",
                "keycloak/run/openbao/auth/keycloak_admin_password.txt",
            ):
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(mounted)
            login = (
                mounted.replace(b"\r", b"").replace(b"\n", b"")
                if login is None
                else login
            )
            (root / "expected-password").write_bytes(login)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name, body in (("docker", FAKE_KC_DOCKER), ("kcadm.sh", FAKE_KCADM)):
                (bin_dir / name).write_text(body)
                (bin_dir / name).chmod(0o755)
            result = subprocess.run(
                ["bash", str(KC_VERIFIER)],
                capture_output=True,
                env={
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "FAKE_ROOT": str(root),
                    "FAKE_BIN": str(bin_dir),
                    **({"KEYCLOAK_PORT": port} if port else {}),
                    **({"FAKE_KC_FILE": kc_file} if kc_file else {}),
                    "VERIFY_RETRY_SLEEP": "0",
                    "VERIFY_HEALTH_SLEEP": "0",
                    "VERIFY_HEALTH_TRIES": "3",
                    **({"FAKE_HEALTH": health} if health else {}),
                    **({"FAKE_KC_NO_RESPONSE": str(misses)} if misses else {}),
                },
                timeout=30,
                check=False,
            )

            def read(name):
                path = root / name
                return path.read_bytes() if path.exists() else b""

            argv = read("kcadm-argv")
            self.calls = int(read("kcadm-calls") or 0)
            # kcadm's token file must be gone once the verifier returns.
            self.leftover = [
                p for p in read("kcadm-config").decode().split() if Path(p).exists()
            ]
        return result, argv

    def test_equal_bytes_and_login_pass_without_printing_the_value(self):
        marker = b"Synth'etic\"marker-1"
        result, argv = self.run_verifier(marker, marker + b"\n")
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual(
            b"PASS keycloak_healthy\n"
            b"PASS consumed_file path=/run/secrets/keycloak_admin_password\n"
            b"PASS rendered_version version=2\nPASS mounted_equals_rendered\n"
            b"PASS admin_login kcadm=ok\n",
            result.stdout,
        )
        for stream in (result.stdout, result.stderr, argv):
            self.assertNotIn(b"Synth", stream)
        self.assertIn(b"--realm master --user admin", argv)
        self.assertEqual([], self.leftover)

    def test_mismatch_wrong_login_bad_version_and_empty_fail(self):
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-b")
        self.assertEqual(1, result.returncode)
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", login=b"other")
        self.assertIn(b"FAIL admin_login kcadm=invalid\n", result.stdout)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", version=b"x1")
        self.assertIn(b"FAIL rendered_version\n", result.stdout)
        result, _ = self.run_verifier(b"\r\n", b"")
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        self.assertEqual(1, result.returncode)

    def test_cr_and_newlines_are_dropped_as_the_entrypoint_does(self):
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a\r\n")
        self.assertEqual(0, result.returncode, result.stdout)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-b\n")
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)

    def test_port_injection_is_rejected_before_any_docker_call(self):
        result, argv = self.run_verifier(
            b"synthetic-a", b"synthetic-a", port="8080@evil.example"
        )
        self.assertEqual(2, result.returncode)
        self.assertEqual(b"", result.stdout)
        self.assertEqual(b"", argv)

    def test_follows_the_agent_directory_file_and_rejects_other_paths(self):
        path = "/run/openbao/auth/keycloak_admin_password.txt"
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", kc_file=path)
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn(f"PASS consumed_file path={path}\n".encode(), result.stdout)
        result, _ = self.run_verifier(
            b"synthetic-a", b"synthetic-a", kc_file="/etc/passwd"
        )
        self.assertEqual(1, result.returncode)
        self.assertEqual(b"PASS keycloak_healthy\nFAIL consumed_file\n", result.stdout)
        self.assertEqual(0, self.calls)

    def test_login_retries_only_when_the_server_gave_no_answer(self):
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", misses=1)
        self.assertIn(b"PASS admin_login kcadm=ok\n", result.stdout)
        self.assertEqual(2, self.calls)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", misses=3)
        self.assertIn(b"FAIL admin_login kcadm=error\n", result.stdout)
        self.assertEqual(3, self.calls)
        # A rejection is final: a wrong password is tried exactly once.
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", login=b"other")
        self.assertEqual(1, self.calls)
        self.assertEqual([], self.leftover)

    def test_waits_for_keycloak_health_before_any_check(self):
        result, _ = self.run_verifier(
            b"synthetic-a", b"synthetic-a", health="starting,starting,healthy"
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertTrue(
            result.stdout.startswith(b"WAIT keycloak_healthy\nPASS keycloak_healthy\n")
        )
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", health="starting")
        self.assertEqual(1, result.returncode)
        self.assertEqual(
            b"WAIT keycloak_healthy\nFAIL keycloak_healthy state=starting\n",
            result.stdout,
        )
        self.assertEqual(0, self.calls)

    def test_keycloak_binds_the_agent_directory_and_keeps_the_db_secret(self):
        import yaml

        compose = yaml.safe_load(
            (ROOT / "infra/02-auth/keycloak/docker-compose.yml").read_text()
        )
        keycloak = compose["services"]["keycloak"]
        binds = [
            v
            for v in keycloak["volumes"]
            if isinstance(v, dict) and v["target"] == "/run/openbao/auth"
        ]
        self.assertEqual(1, len(binds))
        self.assertEqual("${DEFAULT_SECURITY_DIR}/openbao/out/auth", binds[0]["source"])
        self.assertIs(True, binds[0]["read_only"])
        self.assertIs(False, binds[0]["bind"]["create_host_path"])
        self.assertEqual(
            "${KEYCLOAK_ADMIN_PASSWORD_FILE:-/run/secrets/keycloak_admin_password}",
            keycloak["environment"]["KEYCLOAK_ADMIN_PASSWORD_FILE"],
        )
        script = keycloak["entrypoint"][-1]
        self.assertIn('<"$$KEYCLOAK_ADMIN_PASSWORD_FILE"', script)
        self.assertIn("</run/secrets/keycloak_db_password", script)
        self.assertIn("keycloak_db_password", keycloak["secrets"])
        example = (ROOT / ".env.example").read_text()
        self.assertIn('\nKEYCLOAK_ADMIN_PASSWORD_FILE=""\n', example)


CS_VERIFIER = PACKAGE / "verify-grafana-client-secret.sh"
FAKE_CS_DOCKER = r"""#!/usr/bin/env python3
import os, subprocess, sys
args, env = sys.argv[1:], {}
if args[0] == "inspect":
    print(os.environ.get("FAKE_HEALTH", "healthy"))
    sys.exit(0)
assert args.pop(0) == "exec"
while args[0] in ("-e", "-i"):
    if args[0] == "-i":
        args = args[1:]
        continue
    key, _, value = args[1].partition("=")
    env[key] = value
    args = args[2:]
name = args.pop(0)
root = os.path.join(os.environ["FAKE_ROOT"], name)
if args[0] == "printenv":
    print({"GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE": os.environ.get(
               "FAKE_CS_FILE", "/run/secrets/grafana_client_secret"),
           "GF_AUTH_GENERIC_OAUTH_CLIENT_ID": os.environ.get("FAKE_CLIENT", "home-grafana")}[args[1]])
elif args[0] == "cat":
    sys.stdout.buffer.write(open(root + args[1], "rb").read())
elif args[:2] == ["sh", "-c"]:
    env.update(PATH=os.environ["FAKE_BIN"] + ":/usr/bin:/bin", KC_BOOTSTRAP_ADMIN_USERNAME="admin",
               KEYCLOAK_ADMIN_PASSWORD_FILE=root + "/run/secrets/keycloak_admin_password",
               FAKE_ROOT=os.environ["FAKE_ROOT"])
    script = args[2].replace("/opt/keycloak/bin/", os.environ["FAKE_BIN"] + "/")
    sys.exit(subprocess.run(["sh", "-c", script], env=env).returncode)
"""
FAKE_CS_KCADM = r"""#!/usr/bin/env python3
import os, sys
root = os.environ["FAKE_ROOT"]
open(os.path.join(root, "kcadm-argv"), "a").write(" ".join(sys.argv) + "\n")
args = sys.argv[1:]
if args[:2] == ["config", "credentials"]:
    if os.environ.get("KC_CLI_PASSWORD") == "synthetic-admin":
        sys.exit(0)
    sys.stderr.write("Invalid user credentials [invalid_grant]\n")
    sys.exit(1)
if args[:2] == ["get", "clients"]:
    assert "clientId=home-grafana" in args and "hy-home.realm" in args
    print("0f1e2d3c-aaaa-bbbb-cccc-000000000001")
    sys.exit(0)
if args[:2] == ["get", "clients/0f1e2d3c-aaaa-bbbb-cccc-000000000001/client-secret"]:
    sys.stdout.buffer.write(open(os.path.join(root, "keycloak-secret"), "rb").read() + b"\n")
    sys.exit(0)
sys.exit(1)
"""


class GrafanaClientSecretVerifierTests(unittest.TestCase):
    def run_verifier(self, rendered, mounted, keycloak=None, version=b"2",
                     cs_file=None, admin=b"synthetic-admin", client=None, health=None):  # fmt: skip
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "openbao-agent/openbao/out/observability"
            out.mkdir(parents=True)
            (out / "grafana_client_secret.txt").write_bytes(rendered)
            (out / "grafana_admin_password.version").write_bytes(version)
            for path in (
                "grafana/run/secrets/grafana_client_secret",
                "grafana/run/openbao/observability/grafana_client_secret.txt",
            ):
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(mounted)
            admin_file = root / "keycloak/run/secrets/keycloak_admin_password"
            admin_file.parent.mkdir(parents=True)
            admin_file.write_bytes(admin)
            (root / "keycloak-secret").write_bytes(
                mounted.rstrip(b"\n") if keycloak is None else keycloak
            )
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name, body in (("docker", FAKE_CS_DOCKER), ("kcadm.sh", FAKE_CS_KCADM)):
                (bin_dir / name).write_text(body)
                (bin_dir / name).chmod(0o755)
            result = subprocess.run(
                ["bash", str(CS_VERIFIER)],
                capture_output=True,
                env={
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "FAKE_ROOT": str(root),
                    "FAKE_BIN": str(bin_dir),
                    "VERIFY_HEALTH_SLEEP": "0",
                    "VERIFY_HEALTH_TRIES": "2",
                    **({"FAKE_CS_FILE": cs_file} if cs_file else {}),
                    **({"FAKE_CLIENT": client} if client else {}),
                    **({"FAKE_HEALTH": health} if health else {}),
                },
                timeout=30,
                check=False,
            )
            path = root / "kcadm-argv"
            argv = path.read_bytes() if path.exists() else b""
        return result, argv

    def test_all_three_copies_equal_pass_without_printing_values(self):
        marker = b"Synth-client-marker"
        result, argv = self.run_verifier(marker, marker + b"\n")
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual(
            b"PASS grafana_healthy\n"
            b"PASS consumed_file path=/run/secrets/grafana_client_secret\n"
            b"PASS rendered_version version=2\nPASS mounted_equals_rendered\n"
            b"PASS keycloak_client_matches client=home-grafana kcadm=match\n",
            result.stdout,
        )
        for stream in (result.stdout, result.stderr, argv):
            self.assertNotIn(b"Synth", stream)
            self.assertNotIn(b"synthetic-admin", stream)

    def test_each_mismatch_fails_its_own_check(self):
        result, _ = self.run_verifier(
            b"synthetic-a", b"synthetic-b", keycloak=b"synthetic-b"
        )
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        self.assertIn(b"PASS keycloak_client_matches", result.stdout)
        result, _ = self.run_verifier(
            b"synthetic-a", b"synthetic-a", keycloak=b"synthetic-k"
        )
        self.assertIn(b"PASS mounted_equals_rendered\n", result.stdout)
        self.assertIn(b"kcadm=mismatch\n", result.stdout)
        self.assertEqual(1, result.returncode)
        result, argv = self.run_verifier(b"synthetic-a", b"synthetic-a", admin=b"wrong")
        self.assertIn(
            b"FAIL keycloak_client_matches client=home-grafana kcadm=invalid\n",
            result.stdout,
        )
        self.assertEqual(1, argv.count(b"\n"))  # one login, no retry
        # An empty Grafana file is never compared, even when Keycloak is empty too.
        result, argv = self.run_verifier(b"synthetic-a", b"", keycloak=b"")
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        self.assertIn(b"kcadm=empty\n", result.stdout)
        self.assertEqual(b"", argv)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", keycloak=b"")
        self.assertIn(
            b"FAIL keycloak_client_matches client=home-grafana kcadm=empty\n",
            result.stdout,
        )
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", version=b"0")
        self.assertIn(b"FAIL rendered_version\n", result.stdout)

    def test_follows_the_agent_file_and_rejects_other_paths_or_ids(self):
        path = "/run/openbao/observability/grafana_client_secret.txt"
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", cs_file=path)
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn(f"PASS consumed_file path={path}\n".encode(), result.stdout)
        result, argv = self.run_verifier(
            b"synthetic-a", b"synthetic-a", cs_file="/etc/passwd"
        )
        self.assertEqual(b"PASS grafana_healthy\nFAIL consumed_file\n", result.stdout)
        self.assertEqual(b"", argv)
        result, argv = self.run_verifier(b"synthetic-a", b"synthetic-a", client="x;id")
        self.assertIn(b"FAIL client_id\n", result.stdout)
        self.assertEqual(b"", argv)
        result, _ = self.run_verifier(b"synthetic-a", b"synthetic-a", health="starting")
        self.assertEqual(
            b"WAIT grafana_healthy\nFAIL grafana_healthy state=starting\n",
            result.stdout,
        )

    def test_grafana_selects_the_client_secret_file_by_variable(self):
        import yaml

        compose = yaml.safe_load(
            (ROOT / "infra/06-observability/docker-compose.yml").read_text()
        )
        self.assertEqual(
            "${GRAFANA_CLIENT_SECRET_FILE:-/run/secrets/grafana_client_secret}",
            compose["services"]["grafana"]["environment"][
                "GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE"
            ],
        )
        self.assertIn(
            '\nGRAFANA_CLIENT_SECRET_FILE=""\n', (ROOT / ".env.example").read_text()
        )


OIDC_VERIFIER = PACKAGE / "verify-oidc-client-secret.sh"
FAKE_OIDC_DOCKER = r"""#!/usr/bin/env python3
import io, json, os, subprocess, sys, tarfile
root = os.environ["FAKE_ROOT"]
args = sys.argv[1:]
open(os.path.join(root, "docker-argv"), "a").write(" ".join(args) + "\n")
if args[0] == "inspect":
    if "Config.Env" in args[2]:
        for key, value in json.loads(os.environ["FAKE_ENV"]).items():
            print(key + "=" + value)
    else:
        print(os.environ.get("FAKE_HEALTH", "healthy"))
    sys.exit(0)
if args[0] == "cp":
    name, _, path = args[1].partition(":")
    data = open(os.path.join(root, name) + path, "rb").read()
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        info = tarfile.TarInfo(os.path.basename(path))
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))
    sys.stdout.buffer.write(buffer.getvalue())
    sys.exit(0)
assert args.pop(0) == "exec"
env = {}
while args[0] in ("-e", "-i"):
    if args[0] == "-i":
        args = args[1:]
        continue
    key, _, value = args[1].partition("=")
    env[key] = value
    args = args[2:]
name = args.pop(0)
if args[0] == "cat":
    sys.stdout.buffer.write(open(os.path.join(root, name) + args[1], "rb").read())
    sys.exit(0)
assert name == "keycloak" and args[:2] == ["sh", "-c"]
env.update(PATH=os.environ["FAKE_BIN"] + ":/usr/bin:/bin", KC_BOOTSTRAP_ADMIN_USERNAME="admin",
           KEYCLOAK_ADMIN_PASSWORD_FILE=os.path.join(root, "admin-password"), FAKE_ROOT=root)
script = args[2].replace("/opt/keycloak/bin/", os.environ["FAKE_BIN"] + "/")
sys.exit(subprocess.run(["sh", "-c", script], env=env).returncode)
"""
FAKE_OIDC_KCADM = r"""#!/usr/bin/env python3
import os, sys
root = os.environ["FAKE_ROOT"]
open(os.path.join(root, "kcadm-argv"), "a").write(" ".join(sys.argv) + "\n")
args = sys.argv[1:]
if args[:2] == ["config", "credentials"]:
    if os.environ.get("KC_CLI_PASSWORD") == "synthetic-admin":
        sys.exit(0)
    sys.stderr.write("Invalid user credentials [invalid_grant]\n")
    sys.exit(1)
if args[:2] == ["get", "clients"]:
    if "clientId=" + open(os.path.join(root, "expected-client")).read() not in args:
        sys.exit(0)
    print("0f1e2d3c-aaaa-bbbb-cccc-000000000001")
    sys.exit(0)
if args[:2] == ["get", "clients/0f1e2d3c-aaaa-bbbb-cccc-000000000001/client-secret"]:
    sys.stdout.buffer.write(open(os.path.join(root, "keycloak-secret"), "rb").read() + b"\n")
    sys.exit(0)
sys.exit(1)
"""
OIDC_SERVICES = {
    # service: (Agent dir, stem, Compose secret, path variable)
    "oauth2-proxy": ("oauth2-proxy", "oauth2_proxy_client_secret", "oauth2_proxy_client_secret",
                     "OAUTH2_PROXY_CLIENT_SECRET_FILE"),
    "opensearch-dashboards": ("oauth2-proxy", "oauth2_proxy_client_secret", "oauth2_proxy_client_secret",
                              "OPENSEARCH_OIDC_CLIENT_SECRET_FILE"),
    "kafbat-ui": ("kafbat", "kafbat_client_secret", "kafbat_client_secret",
                  "KAFBAT_CLIENT_SECRET_FILE"),
    "dozzle": ("dozzle", "dozzle_client_secret", "dozzle_client_secret",
               "DOZZLE_AUTH_OIDC_CLIENT_SECRET_FILE"),
    "gatus": ("gatus", "gatus_oidc_client_secret", "gatus_oidc_client_secret",
              "GATUS_OIDC_CLIENT_SECRET_FILE"),
    "airflow-apiserver": ("airflow", "airflow_client_secret", "airflow_keycloak_client_secret",
                          "AIRFLOW__KEYCLOAK_AUTH_MANAGER__CLIENT_SECRET_CMD"),
    "open-webui": ("open-webui", "openwebui_oidc_client_secret", "openwebui_oidc_client_secret",
                   "OPENWEBUI_OIDC_CLIENT_SECRET_FILE"),
    "superset": ("superset", "superset_oidc_client_secret", "superset_oidc_client_secret",
                 "SUPERSET_OIDC_CLIENT_SECRET_FILE"),
}  # fmt: skip
# Keycloak clientId per service, kept apart from the secret names.
KEYCLOAK_CLIENTS = {
    "oauth2-proxy": "home-proxy-client",
    "opensearch-dashboards": "realm-home-client",
    "kafbat-ui": "home-kafbat",
    "dozzle": "home-dozzle",
    "gatus": "home-gatus",
    "airflow-apiserver": "home-airflow",
    "open-webui": "home-openwebui",
    "superset": "home-superset",
}
OIDC_CLIENT_ENV = {
    "oauth2-proxy": "OAUTH2_PROXY_CLIENT_ID",
    "kafbat-ui": "KAFBAT_OAUTH_CLIENT_ID",
    "dozzle": "DOZZLE_AUTH_OIDC_CLIENT_ID",
    "airflow-apiserver": "AIRFLOW__KEYCLOAK_AUTH_MANAGER__CLIENT_ID",
    "open-webui": "OAUTH_CLIENT_ID",
    "superset": "SUPERSET_OIDC_CLIENT_ID",
}


class OidcClientSecretVerifierTests(unittest.TestCase):
    def run_verifier(self, service, rendered=b"synthetic-a", mounted=None,
                     keycloak=None, agent_path=False, path=None, env=None,
                     health=None, args=None):  # fmt: skip
        import os
        import tempfile

        known = service if service in OIDC_SERVICES else "oauth2-proxy"
        directory, stem, secret, path_env = OIDC_SERVICES[known]
        client = KEYCLOAK_CLIENTS[known]
        mounted = rendered if mounted is None else mounted
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / f"openbao-agent/openbao/out/{directory}"
            out.mkdir(parents=True)
            (out / f"{stem}.txt").write_bytes(rendered)
            (out / f"{stem}.version").write_bytes(b"1")
            chosen = path or (
                f"/run/openbao/{directory}/{stem}.txt"
                if agent_path
                else f"/run/secrets/{secret}"
            )
            target = root / service / chosen.lstrip("/")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(mounted)
            (root / "admin-password").write_bytes(b"synthetic-admin\n")
            (root / "expected-client").write_text(client)
            (root / "keycloak-secret").write_bytes(
                mounted.rstrip(b"\n") if keycloak is None else keycloak
            )
            settings = {path_env: ("cat " if "_CMD" in path_env else "") + chosen}
            if service in OIDC_CLIENT_ENV:
                settings[OIDC_CLIENT_ENV[service]] = client
            settings.update(env or {})
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name, body in (
                ("docker", FAKE_OIDC_DOCKER),
                ("kcadm.sh", FAKE_OIDC_KCADM),
            ):
                (bin_dir / name).write_text(body)
                (bin_dir / name).chmod(0o755)
            result = subprocess.run(
                ["bash", str(OIDC_VERIFIER), *([service] if args is None else args)],
                capture_output=True,
                env={
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "FAKE_ROOT": str(root),
                    "FAKE_BIN": str(bin_dir),
                    "FAKE_ENV": json.dumps(settings),
                    "VERIFY_HEALTH_SLEEP": "0",
                    "VERIFY_HEALTH_TRIES": "2",
                    **({"FAKE_HEALTH": health} if health else {}),
                },
                timeout=30,
                check=False,
            )
            traces = b"".join(
                (root / name).read_bytes()
                for name in ("docker-argv", "kcadm-argv")
                if (root / name).exists()
            )
        return result, traces

    def test_every_service_passes_on_both_paths_without_printing_values(self):
        for service, (directory, stem, secret, _) in OIDC_SERVICES.items():
            client = KEYCLOAK_CLIENTS[service]
            for agent_path in (False, True):
                with self.subTest(service=service, agent_path=agent_path):
                    marker = b"Synth-oidc-marker"
                    result, traces = self.run_verifier(
                        service, marker, marker + b"\n", agent_path=agent_path
                    )
                    self.assertEqual(0, result.returncode, result.stdout)
                    path = (
                        f"/run/openbao/{directory}/{stem}.txt"
                        if agent_path
                        else f"/run/secrets/{secret}"
                    )
                    self.assertEqual(
                        f"PASS healthy service={service}\n"
                        f"PASS consumed_file path={path}\n"
                        "PASS rendered_version version=1\n"
                        "PASS mounted_equals_rendered\n"
                        f"PASS keycloak_client_matches client={client} kcadm=match\n".encode(),
                        result.stdout,
                    )
                    for stream in (result.stdout, result.stderr, traces):
                        self.assertNotIn(b"Synth", stream)
                        self.assertNotIn(b"synthetic-admin", stream)

    def test_mismatches_paths_ids_and_usage_fail(self):
        result, _ = self.run_verifier("dozzle", b"synthetic-a", b"synthetic-b")
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        result, _ = self.run_verifier("dozzle", keycloak=b"synthetic-k")
        self.assertIn(b"kcadm=mismatch\n", result.stdout)
        self.assertEqual(1, result.returncode)
        result, traces = self.run_verifier("gatus", path="/etc/passwd")
        self.assertEqual(
            b"PASS healthy service=gatus\nFAIL consumed_file\n", result.stdout
        )
        self.assertNotIn(b"kcadm", traces)
        # Another service's Agent file is not this service's path.
        result, _ = self.run_verifier(
            "dozzle", path="/run/openbao/gatus/gatus_oidc_client_secret.txt"
        )
        self.assertIn(b"FAIL consumed_file\n", result.stdout)
        result, _ = self.run_verifier(
            "kafbat-ui", env={"KAFBAT_OAUTH_CLIENT_ID": "x;id"}
        )
        self.assertIn(b"FAIL client_id\n", result.stdout)
        result, _ = self.run_verifier(
            "superset", rendered=b"", mounted=b"", keycloak=b""
        )
        self.assertIn(b"FAIL mounted_equals_rendered\n", result.stdout)
        self.assertIn(b"kcadm=empty\n", result.stdout)
        result, _ = self.run_verifier("open-webui", health="unhealthy")
        self.assertEqual(b"WAIT healthy\nFAIL healthy state=unhealthy\n", result.stdout)
        result, _ = self.run_verifier("superset", health="running")
        self.assertEqual(0, result.returncode, result.stdout)
        for args in ([], ["grafana"], ["oauth2-proxy", "extra"]):
            result, traces = self.run_verifier("oauth2-proxy", args=args)
            self.assertEqual(2, result.returncode)
            self.assertEqual(b"", result.stdout)
            self.assertEqual(b"", traces)

    def test_each_consumer_binds_only_its_agent_directory_and_defaults_to_secrets(self):
        import yaml

        files = {
            "oauth2-proxy": "infra/02-auth/oauth2-proxy/docker-compose.yml",
            "opensearch-dashboards": "infra/04-data/opensearch/docker-compose.yml",
            "kafbat-ui": "infra/05-messaging/kafka/docker-compose.yml",
            "dozzle": "infra/06-observability/dozzle/docker-compose.yml",
            "gatus": "infra/06-observability/docker-compose.yml",
            "airflow-apiserver": "infra/07-workflow/airflow/docker-compose.yml",
            "open-webui": "infra/08-ai/open-webui/docker-compose.yml",
            "superset": "infra/12-analytics/superset/docker-compose.yml",
        }
        example = (ROOT / ".env.example").read_text()
        for service, path in files.items():
            with self.subTest(service=service):
                directory, _, secret, _ = OIDC_SERVICES[service]
                spec = yaml.safe_load((ROOT / path).read_text())["services"][service]
                binds = [
                    v for v in spec["volumes"]
                    if isinstance(v, dict) and v["target"].startswith("/run/openbao/")
                ]  # fmt: skip
                self.assertEqual(1, len(binds))
                self.assertEqual(f"/run/openbao/{directory}", binds[0]["target"])
                self.assertEqual(
                    "${DEFAULT_SECURITY_DIR}/openbao/out/" + directory,
                    binds[0]["source"],
                )
                self.assertIs(True, binds[0]["read_only"])
                self.assertIs(False, binds[0]["bind"]["create_host_path"])
                text = (ROOT / path).read_text()
                self.assertIn(f":-/run/secrets/{secret}}}", text)
                variable = re.search(r"\$\{(\w+):-/run/secrets/" + secret + r"\}", text)
                self.assertIsNotNone(variable)
                self.assertIn(f'\n{variable.group(1)}=""\n', example)
