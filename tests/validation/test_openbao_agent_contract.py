"""Renderer readiness and wrapped reissue contracts using private safe stubs."""

import hashlib
import json
import os
import secrets
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "infra/03-security/openbao/scripts"
IMAGE = "hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8"
MANIFEST = "sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8"


class AgentContractTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.agent = self.root / "openbao/agent"
        self.agent.mkdir(parents=True)
        self.out = self.root / "openbao/out"
        for directory in ("auth", "observability"):
            (self.out / directory).mkdir(parents=True)
        self.journal = self.root / "journal"
        self.journal.mkdir(mode=0o700)
        self.cleanup_token = secrets.token_hex(24)
        self.token = secrets.token_hex(24)
        self.values = [secrets.token_hex(24), secrets.token_hex(24)]
        self.client_secret = secrets.token_hex(24)
        (self.agent / "token").write_text(self.token)
        (self.agent / "token").chmod(0o600)
        self.rendered = [
            self.out / "auth/keycloak_admin_password.txt",
            self.out / "observability/grafana_admin_password.txt",
        ]
        # Both consumed passwords are group-readable (P06 W49 Grafana, Keycloak).
        self.rendered_modes = (0o640, 0o640)
        for path, value, mode in zip(
            self.rendered, self.values, self.rendered_modes, strict=True
        ):
            path.write_text(value)
            path.chmod(mode)
        self.client = self.out / "observability/grafana_client_secret.txt"
        self.client.write_text(self.client_secret)
        self.client.chmod(0o640)
        self.versions = [path.with_suffix(".version") for path in self.rendered]
        for path, version in zip(self.versions, ("7", "11"), strict=True):
            path.write_text(version)
            path.chmod(0o600)
        config = self.root / "openbao/config"
        config.mkdir()
        (config / "agent.hcl").write_text(
            (SCRIPTS.parent / "config/agent.hcl")
            .read_text()
            .replace("/openbao/", str(self.root / "openbao") + "/")
        )
        self.ca = self.root / "ca.pem"
        self.ca.write_text("synthetic CA stub\n")
        self.log = self.root / "arguments.jsonl"
        self.env = {
            **os.environ,
            "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
            "VAULT_ADDR": "https://openbao:8200",
            "VAULT_CACERT": str(self.ca),
            "BAO_ADDR": "https://openbao:8200",
            "BAO_CACERT": str(self.ca),
            "STUB_ROOT": str(self.root),
            "STUB_TOKEN": self.token,
            "STUB_CLEANUP_TOKEN": self.cleanup_token,
            "STUB_MANIFEST": MANIFEST,
            "STUB_VALUE_1": self.values[0],
            "STUB_VALUE_2": self.values[1],
            "STUB_VALUE_3": self.client_secret,
        }
        for name in (
            "BAO_SKIP_VERIFY",
            "VAULT_SKIP_VERIFY",
            "BAO_TOKEN",
            "VAULT_TOKEN",
        ):
            self.env.pop(name, None)
        self.stub(
            "bao",
            """import json, os, pathlib, sys
args = sys.argv[1:]
root = pathlib.Path(os.environ["STUB_ROOT"])
with (root / "arguments.jsonl").open("a") as log:
    log.write(json.dumps(args) + "\\n")
mode = os.environ.get("STUB_FAILURE", "")
if args[0] == "agent":
    sys.stderr.write("agent: authentication pending\\n")
    sys.exit(0 if not (root / "openbao/agent/token").exists() else 1)
token = os.environ.get("BAO_TOKEN")
if os.environ.get("BAO_TOKEN_PATH"):
    source = pathlib.Path(os.environ["BAO_TOKEN_PATH"])
    if source.stat().st_mode & 0o777 != 0o600 or source.stat().st_nlink != 1:
        sys.exit(1)
    token = source.read_text().removesuffix("\\n")
if token not in (os.environ["STUB_TOKEN"], os.environ["STUB_CLEANUP_TOKEN"]):
    sys.exit(1)
if args[:2] == ["read", "-format=json"]:
    role = "renderer-issuer" if token == os.environ["STUB_TOKEN"] else "renderer-cleanup"
    print(json.dumps({"data":{"policies":[role],"renewable":False,"ttl":299,
                             "explicit_max_ttl":300,"type":"service",
                             "path":"auth/token/create/"+role}}))
    sys.exit(0)
if args[0] == "list":
    data = json.loads((root / "accessors.json").read_text()) if (root / "accessors.json").exists() else {}
    print(json.dumps({"data":{"keys":list(data)}}))
    sys.exit(0)
if args[0] == "status":
    sys.exit(2 if mode == "sealed" else 0)
if args[:2] == ["token", "lookup"]:
    sys.exit(1 if mode in ("expired", "forbidden") else 0)
if args[0] == "write":
    from datetime import datetime,timezone
    payload = json.load(sys.stdin)
    state = root / "accessors.json"
    data = json.loads(state.read_text()) if state.exists() else {}
    if "secret-id-accessor/lookup" in args[-2]:
        print(json.dumps({"data":data[payload["secret_id_accessor"]]}))
    elif "secret-id-accessor/destroy" in args[-2]:
        data.pop(payload["secret_id_accessor"])
        state.write_text(json.dumps(data))
    else:
        data["synthetic-accessor"] = {"metadata":json.loads(payload["metadata"]),
                                      "creation_time":datetime.now(timezone.utc).isoformat()}
        state.write_text(json.dumps(data))
        if mode == "issue":
            sys.stderr.write(os.environ["STUB_VALUE_1"])
            sys.exit(1)
        print(json.dumps({"wrap_info":{"token":os.environ["STUB_VALUE_1"]}}))
    sys.exit(0)
if args[:2] == ["kv", "get"]:
    output = os.readlink("/proc/self/fd/1")
    if output != "/dev/null" and not output.startswith("pipe:["):
        sys.exit(1)
    if mode == "fetch":
        sys.stderr.write(os.environ["STUB_VALUE_1"])
        sys.exit(1)
    index = "1" if args[-1].endswith("keycloak") else "2"
    if "-field=grafana_client_secret" in args:
        index = "3"
    sys.stdout.write(os.environ["STUB_VALUE_" + index])
    sys.exit(0)
if args[:2] == ["read", "-field=current_version"]:
    if mode == "metadata":
        sys.exit(1)
    sys.stdout.write("7" if args[-1].endswith("keycloak") else "11")
    sys.exit(0)
sys.exit(1)
""",
        )
        self.stub(
            "timeout",
            """import os, sys
if os.environ.get("STUB_FAILURE") == "timeout":
    sys.exit(124)
os.execvp(sys.argv[2], sys.argv[2:])
""",
        )
        self.stub(
            "docker",
            """import json, os, pathlib, subprocess, sys
args = sys.argv[1:]
root = pathlib.Path(os.environ["STUB_ROOT"])
with (root / "arguments.jsonl").open("a") as log:
    log.write(json.dumps(args) + "\\n")
image_id = os.environ["STUB_MANIFEST"]
mode = os.environ.get("STUB_FAILURE", "")
if args[:2] == ["volume", "inspect"]:
    if mode == "volume":sys.exit(1)
    sys.stdout.write(str(root / "openbao/agent"))
    sys.exit(0)
if args[:2] == ["image", "inspect"]:
    sys.stdout.write(image_id)
    sys.exit(0)
if args[0] == "inspect":
    query = args[args.index("--format") + 1]
    if args[-1] == "openbao":
        if mode == "server-image":image_id = "sha256:" + "b" * 64
        sys.stdout.write(image_id + (" false" if mode == "server-stopped" else " true"))
    elif query == "{{.State.StartedAt}}":
        sys.stdout.write("2026-10-10T07:00:01Z")
    elif query == "{{.State.Running}}":
        sys.stdout.write("true" if mode == "agent-running" or (root / "started").exists() else "false")
    elif query.startswith('{"entrypoint":'):
        sys.stdout.write(json.dumps({"entrypoint":["/bin/sh",str(root / "openbao/scripts/start-agent.sh")],"cmd":None}))
    else:
        if mode == "agent-image":image_id = "sha256:" + "b" * 64
        mount = {"agent-volume":"volume different-volume","agent-bind":"bind p01-agent",
                 "agent-mount":""}.get(mode,"volume p01-agent")
        sys.stdout.write(image_id + " " + mount)
    sys.exit(0)
if args[0] == "start":
    (root / "started").touch()
    (root / "accessors.json").write_text("{}")
    (root / "openbao/agent/token").write_text(os.environ["STUB_TOKEN"])
    (root / "openbao/agent/token").chmod(0o600)
    sys.exit(0)
payload = sys.stdin.read()
if args[0] == "exec":
    if args[-1].endswith("health-agent.sh"):
        result = subprocess.run(["sh", args[-1]], check=False)
        sys.exit(result.returncode)
    token, body = payload.split("\\n", 1)
    if token not in (os.environ["STUB_TOKEN"],os.environ["STUB_CLEANUP_TOKEN"]):
        sys.exit(1)
    script_index = args.index("-c") + 1
    if args[script_index + 1] != "renderer-request" or not 0 < int(args[script_index + 2]) < 20:
        sys.exit(1)
    # shortcut: emulate the container token file; native peer custody has its own suite.
    import tempfile
    with tempfile.TemporaryDirectory(dir=root) as temporary:
        token_file = pathlib.Path(temporary) / "token"
        token_file.touch(mode=0o600)
        token_file.write_text(token)
        environment = {**os.environ, "BAO_TOKEN_PATH": str(token_file)}
        environment.pop("BAO_TOKEN", None)
        result = subprocess.run(["bao", *args[script_index + 3:]], input=body,
                                text=True, env=environment, check=False)
        sys.exit(result.returncode)
elif args[0] == "run":
    if mode == "deliver":
        sys.stderr.write(payload)
        sys.exit(1)
    if payload.rstrip("\\n") != os.environ["STUB_VALUE_1"]:
        sys.exit(1)
else:
    sys.exit(1)
result = subprocess.run(["sh", "-c", args[-1]], input=payload, text=True, check=False)
sys.exit(result.returncode)
""",
        )

    def stub(self, name, body):
        path = self.bin / name
        path.write_text("#!/usr/bin/env python3\n" + body)
        path.chmod(0o700)

    def run_script(self, name, *args, stdin=None):
        if name == "issue-renderer-secret-id.sh":
            helper = self.root / "renderer-issuance.py"
            helper.write_text(
                (SCRIPTS / "renderer-issuance.py")
                .read_text()
                .replace("/openbao/", str(self.root / "openbao") + "/")
            )
            helper.chmod(0o600)
            request = self.root / "renderer-request.sh"
            request.write_bytes((SCRIPTS / "renderer-request.sh").read_bytes())
            request.chmod(0o600)
            health = self.root / "openbao/scripts/health-agent.sh"
            health.parent.mkdir(exist_ok=True)
            health.write_text(
                (SCRIPTS / "health-agent.sh")
                .read_text()
                .replace("/openbao/", str(self.root / "openbao") + "/")
            )
            if len(args) == 4:
                args = (*args, str(self.journal), "a" * 40)
            stdin = self.token + "\n" + self.cleanup_token + "\n"
        source = SCRIPTS / name
        self.assertTrue(source.is_file(), f"Missing contract script: {name}")
        fixture = self.root / name
        fixture.write_text(
            source.read_text().replace("/openbao/", str(self.root / "openbao") + "/")
        )
        fixture.chmod(0o600)
        if name == "issue-renderer-secret-id.sh":
            receipt = self.root / "source-receipt.json"
            if receipt.exists():
                receipt.chmod(0o600)
            receipt.write_text(
                json.dumps(
                    {
                        "source_revision": "a" * 40,
                        "sha256": {
                            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in (
                                fixture,
                                self.root / "renderer-issuance.py",
                                self.root / "renderer-request.sh",
                            )
                        },
                    }
                )
            )
            receipt.chmod(0o400)
        result = subprocess.run(
            ["sh", str(fixture), *args],
            env=self.env,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        # Never use assertions whose failure formatter can print synthetic secrets.
        self.assertTrue(result.stdout == "", "Unexpected public stdout")
        self.assertTrue(
            result.stderr in ("", "agent: authentication pending\n")
            if name == "start-agent.sh"
            else result.stderr == "",
            "Unexpected public stderr",
        )
        if self.log.exists():
            public = self.log.read_text()
            self.assertTrue(
                all(
                    value not in public
                    for value in [
                        self.token,
                        self.cleanup_token,
                        self.client_secret,
                        *self.values,
                    ]
                ),
                "Secret-bearing argv",
            )
        return result

    def test_readiness_fetches_two_restricted_paths_and_version_sentinels(self):
        self.assertEqual(self.run_script("health-agent.sh").returncode, 0)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual(calls[0], ["status"])
        self.assertEqual(calls[1], ["token", "lookup", "-format=json"])
        self.assertEqual(
            calls[2:],
            [
                [
                    "kv",
                    "get",
                    "-field=admin_password",
                    "secret/hy-home/02-auth/keycloak",
                ],
                [
                    "kv",
                    "get",
                    "-field=admin_password",
                    "secret/hy-home/06-observability/grafana",
                ],
                [
                    "kv",
                    "get",
                    "-field=grafana_client_secret",
                    "secret/hy-home/06-observability/grafana",
                ],
                [
                    "kv",
                    "get",
                    "-field=admin_password",
                    "secret/hy-home/02-auth/keycloak",
                ],
                [
                    "kv",
                    "get",
                    "-field=admin_password",
                    "secret/hy-home/06-observability/grafana",
                ],
                [
                    "kv",
                    "get",
                    "-field=grafana_client_secret",
                    "secret/hy-home/06-observability/grafana",
                ],
                [
                    "read",
                    "-field=current_version",
                    "secret/metadata/hy-home/02-auth/keycloak",
                ],
                [
                    "read",
                    "-field=current_version",
                    "secret/metadata/hy-home/06-observability/grafana",
                ],
            ],
        )

    def test_sink_presence_does_not_accept_sealed_expired_or_forbidden(self):
        for failure in (
            "sealed",
            "expired",
            "forbidden",
            "fetch",
            "metadata",
            "timeout",
        ):
            with self.subTest(failure=failure):
                self.env["STUB_FAILURE"] = failure
                self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_missing_or_stale_render_fails(self):
        self.versions[0].write_text("6")
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
        self.versions[0].write_text("7")
        self.rendered[0].unlink()
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_multiline_and_trailing_newline_secret_bytes_are_preserved(self):
        self.env["STUB_VALUE_1"] = self.values[0] + "\nsecond line\n"
        self.rendered[0].write_text(self.env["STUB_VALUE_1"])
        self.assertEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_keycloak_payload_mismatch_fails_even_with_current_version(self):
        self.rendered[0].write_text(secrets.token_hex(24))
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_client_secret_is_checked_like_the_passwords(self):
        self.client.write_text(secrets.token_hex(24))
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
        self.client.write_text(self.client_secret)
        for mode in (0o600, 0o644):
            self.client.chmod(mode)
            self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
        self.client.chmod(0o640)
        self.assertEqual(self.run_script("health-agent.sh").returncode, 0)
        self.client.unlink()
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_grafana_payload_mismatch_fails_even_with_current_version(self):
        self.rendered[1].write_text(secrets.token_hex(24))
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_missing_token_or_symlink_fails(self):
        (self.agent / "token").unlink()
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
        target = self.root / "private-token"
        target.write_text(self.token)
        (self.agent / "token").symlink_to(target)
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_token_requires_private_mode(self):
        (self.agent / "token").chmod(0o644)
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_rendered_passwords_require_their_exact_mode(self):
        # World-readable and owner-only must both fail.
        for index, wrong in ((0, 0o644), (1, 0o644), (0, 0o600), (1, 0o600)):
            self.rendered[index].chmod(wrong)
            self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
            self.rendered[index].chmod(self.rendered_modes[index])

    def test_no_other_group_readable_file_beside_consumed_passwords(self):
        for directory in ("observability", "auth"):
            with self.subTest(directory=directory):
                stray = self.out / directory / "other.txt"
                stray.write_text("synthetic")
                stray.chmod(0o640)
                self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
                stray.chmod(0o600)
                self.assertEqual(self.run_script("health-agent.sh").returncode, 0)
        # Each directory admits only its own consumer's file.
        stray = self.out / "auth/grafana_admin_password.txt"
        stray.write_text("synthetic")
        stray.chmod(0o640)
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)

    def test_only_the_consumed_password_templates_are_group_readable(self):
        import re

        hcl = (SCRIPTS.parent / "config/agent.hcl").read_text()
        modes = dict(
            re.findall(r'destination = "([^"]+)"\n(?:.*\n)??\s*perms\s*= (\d+)', hcl)
        )
        for consumed in (
            "/openbao/out/observability/grafana_admin_password.txt",
            "/openbao/out/observability/grafana_client_secret.txt",
            "/openbao/out/auth/keycloak_admin_password.txt",
        ):
            self.assertEqual("0640", modes.pop(consumed))
        self.assertEqual({"0600"}, set(modes.values()))
        self.assertEqual(2, len(modes))

    def test_version_sentinels_require_private_mode(self):
        for index in (0, 1):
            self.versions[index].chmod(0o644)
            self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
            self.versions[index].chmod(0o600)

    def test_start_clears_previous_sink(self):
        result = self.run_script("start-agent.sh")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stderr == "agent: authentication pending\n")
        self.assertFalse((self.agent / "token").exists())

    def test_start_applies_template_perms_to_existing_files(self):
        # An unchanged render keeps its old mode; start must fix it from agent.hcl.
        self.rendered[0].chmod(0o600)
        self.versions[1].chmod(0o640)
        self.versions[0].unlink()
        self.assertEqual(self.run_script("start-agent.sh").returncode, 0)
        self.assertEqual(0o640, self.rendered[0].stat().st_mode & 0o777)
        self.assertEqual(0o640, self.rendered[1].stat().st_mode & 0o777)
        self.assertEqual(0o600, self.versions[1].stat().st_mode & 0o777)
        # A missing destination is left for the Agent to render.
        self.assertFalse(self.versions[0].exists())

    def test_start_refuses_symlinked_destination_before_the_agent(self):
        target = self.root / "elsewhere"
        target.write_text("synthetic")
        target.chmod(0o600)
        self.rendered[0].unlink()
        self.rendered[0].symlink_to(target)
        self.assertNotEqual(self.run_script("start-agent.sh").returncode, 0)
        self.assertEqual(0o600, target.stat().st_mode & 0o777)
        self.assertFalse(self.log.exists())

    def test_start_rejects_unsafe_template_perms_or_destination(self):
        hcl = self.root / "openbao/config/agent.hcl"
        original = hcl.read_text()
        prefix = str(self.root / "openbao") + "/"
        for old, new in (
            ("perms       = 0640", "perms       = 640"),
            ("perms       = 0640", "perms       = 06400"),
            (prefix + "out/auth/", prefix + "agent/"),
            (prefix + "out/auth/", prefix + "out/auth/../../agent/"),
            # A template whose perms the parser cannot read must not pass silently.
            ("perms       = 0640", "perms=0640"),
        ):
            with self.subTest(new=new):
                hcl.write_text(original.replace(old, new, 1))
                self.assertNotEqual(self.run_script("start-agent.sh").returncode, 0)
                self.assertFalse(self.log.exists())
        hcl.unlink()
        self.assertNotEqual(self.run_script("start-agent.sh").returncode, 0)

    def test_http_missing_ca_and_skip_verify_are_rejected(self):
        for name in ("health-agent.sh", "start-agent.sh"):
            self.env["VAULT_ADDR"] = "http://openbao:8200"
            self.assertNotEqual(self.run_script(name).returncode, 0)
            self.env["VAULT_ADDR"] = "https://openbao:8200"
            self.env["VAULT_CACERT"] = str(self.root / "absent.pem")
            self.assertNotEqual(self.run_script(name).returncode, 0)
            self.env["VAULT_CACERT"] = str(self.ca)
            self.env["VAULT_SKIP_VERIFY"] = "true"
            self.assertNotEqual(self.run_script(name).returncode, 0)
            self.env.pop("VAULT_SKIP_VERIFY")

    def test_wrapped_reissue_delivers_only_through_stdin(self):
        result = self.run_script(
            "issue-renderer-secret-id.sh",
            "openbao",
            "p01-agent",
            IMAGE,
            "openbao-agent",
            stdin=self.token + "\n",
        )
        self.assertEqual(result.returncode, 0)
        target = self.agent / "secret_id"
        self.assertTrue(
            target.read_text() == self.values[0], "Unexpected private payload"
        )
        self.assertEqual(target.stat().st_mode & 0o777, 0o600)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        delivery = next(call for call in calls if call[0] == "run")
        self.assertIn("--network=none", delivery)
        self.assertIn("--pull=never", delivery)
        self.assertIn("--user=100:1000", delivery)
        self.assertIn("--cap-drop=ALL", delivery)
        self.assertIn("--read-only", delivery)
        self.assertEqual(
            calls[0],
            [
                "image",
                "inspect",
                "--platform=linux/amd64",
                "--format",
                "{{.Id}}",
                IMAGE,
            ],
        )
        self.assertTrue(any(call[:2] == ["volume", "inspect"] for call in calls))
        issue = next(call for call in calls if "-wrap-ttl=60s" in " ".join(call))
        self.assertIn("auth/approle/role/hy-home-renderer/secret-id", " ".join(issue))
        self.assertEqual(calls[1][-1], "openbao")
        self.assertEqual(calls[2][-1], "openbao-agent")
        self.assertFalse((self.journal / "issuance.json").exists())
        self.assertEqual(
            "complete",
            json.loads((self.journal / "issuance.anchor").read_text())["state"],
        )

    def test_issue_failure_is_redacted(self):
        self.check_issuance_failure("issue")

    def test_delivery_failure_is_redacted(self):
        self.check_issuance_failure("deliver")

    def test_volume_failure_is_redacted(self):
        self.check_issuance_failure("volume")

    def check_issuance_failure(self, failure):
        self.env["STUB_FAILURE"] = failure
        result = self.run_script(
            "issue-renderer-secret-id.sh",
            "openbao",
            "p01-agent",
            IMAGE,
            "openbao-agent",
            stdin=self.token + "\n",
        )
        self.assertNotEqual(result.returncode, 0)

    def test_wrong_server_image_is_rejected_before_credential_delivery(self):
        self.check_rejected_image("server-image")

    def test_wrong_agent_image_is_rejected_before_credential_delivery(self):
        self.check_rejected_image("agent-image")

    def check_rejected_image(self, failure):
        self.env["STUB_FAILURE"] = failure
        result = self.run_script(
            "issue-renderer-secret-id.sh",
            "openbao",
            "p01-agent",
            IMAGE,
            "openbao-agent",
            stdin=self.token + "\n",
        )
        self.assertNotEqual(result.returncode, 0)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertFalse(any(call[0] in ("exec", "run") for call in calls))

    def test_delivery_refuses_symlink_and_leaves_no_partial(self):
        target = self.root / "owner-private-file"
        target.write_text(self.values[1])
        (self.agent / "secret_id").symlink_to(target)
        result = self.run_script(
            "issue-renderer-secret-id.sh",
            "openbao",
            "p01-agent",
            IMAGE,
            "openbao-agent",
            stdin=self.token + "\n",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(target.read_text() == self.values[1], "Target was modified")
        self.assertEqual(list(self.agent.glob(".wrapped-secret-id.*")), [])

    def test_unsafe_target_or_other_image_rejected(self):
        for args in (
            ("--privileged", "p01-agent", IMAGE),
            ("openbao", "../data", IMAGE),
            ("openbao", "p01-agent", "other:latest"),
        ):
            self.assertNotEqual(
                self.run_script(
                    "issue-renderer-secret-id.sh",
                    *args,
                    "openbao-agent",
                    stdin=self.token + "\n",
                ).returncode,
                0,
            )
        self.assertFalse(self.log.exists())

    def test_health_creates_no_plaintext_scratch(self):
        self.env["TMPDIR"] = str(self.root)
        self.assertEqual(self.run_script("health-agent.sh").returncode, 0)
        self.assertEqual(list(self.root.glob("openbao-health.*")), [])
        self.env["STUB_FAILURE"] = "fetch"
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
        self.assertEqual(list(self.root.glob("openbao-health.*")), [])

    def test_issuer_requires_stopped_agent_and_exact_volume_binding(self):
        for failure in ("agent-running", "agent-volume", "agent-bind", "agent-mount"):
            self.log.unlink(missing_ok=True)
            self.env["STUB_FAILURE"] = failure
            result = self.run_script(
                "issue-renderer-secret-id.sh",
                "openbao",
                "p01-agent",
                IMAGE,
                "openbao-agent",
                stdin=self.token + "\n",
            )
            self.assertNotEqual(result.returncode, 0)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertFalse(any(call[0] in ("exec", "run") for call in calls))

    def test_version_sentinel_is_required_and_symlink_rejected(self):
        self.versions[0].unlink()
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
        self.versions[0].symlink_to(self.versions[1])
        self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)


PROMTOOL = "sha256:5ce7540c3c00ef4ab0c9d2c995c6a5b9c421f44b4a115d97a2c7af3b1c21cbb0"


class AgentMetricsTests(unittest.TestCase):
    """SPEC-0239: the Agent's metrics_only listener, its scrape job and alerts."""

    def test_agent_serves_metrics_only_without_tls_on_obs_net(self):
        import re

        import yaml

        hcl = (SCRIPTS.parent / "config/agent.hcl").read_text()
        listener = re.search(r'listener "tcp" \{(.*?)\}', hcl, re.S).group(1)
        self.assertIn('role        = "metrics_only"', listener)
        self.assertIn('address     = "0.0.0.0:8100"', listener)
        self.assertIn("tls_disable = true", listener)
        self.assertEqual(1, len(re.findall(r"^listener ", hcl, re.M)))
        self.assertNotIn("api_proxy", hcl)
        self.assertNotIn("cache {", hcl)
        self.assertIn('prometheus_retention_time = "24h"', hcl)
        compose = yaml.safe_load((SCRIPTS.parent / "docker-compose.yml").read_text())
        agent = compose["services"]["openbao-agent"]
        self.assertEqual({"secrets_net", "obs_net"}, set(agent["networks"]))
        self.assertNotIn("ports", agent)

    def test_prometheus_scrapes_the_agent_listener(self):
        import yaml

        config = ROOT / "infra/06-observability/prometheus/config"
        for name in ("prometheus.yml", "prometheus.dev.yml"):
            jobs = yaml.safe_load((config / name).read_text())["scrape_configs"]
            job = next(j for j in jobs if j["job_name"] == "openbao-agent")
            self.assertEqual("/agent/v1/metrics", job["metrics_path"], name)
            self.assertEqual({"format": ["prometheus"]}, job["params"], name)
            self.assertEqual(
                ["openbao-agent:8100"], job["static_configs"][0]["targets"], name
            )
            self.assertNotIn("bearer_token_file", job, name)


class AgentMetricsNativeTests(unittest.TestCase):
    """Cached promtool execution; listener and scrape contracts stay required."""

    def test_agent_alert_rules_pass_their_promtool_cases(self):
        try:
            present = (
                subprocess.run(
                    ["docker", "image", "inspect", PROMTOOL],
                    capture_output=True,
                    check=False,
                ).returncode
                == 0
            )
        except OSError:
            present = False
        if not present:
            self.skipTest("cached promtool image is not available")
        rules = (
            ROOT
            / "infra/06-observability/prometheus/config/alert_rules/alert_rules.openbao.yml"
        )
        cases = ROOT / "tests/validation/fixtures/openbao-agent-alerts.test.yml"
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                "none",
                "--read-only",
                "--tmpfs",
                "/tmp:size=32m",
                "--entrypoint",
                "/bin/promtool",
                "--mount",
                f"type=bind,src={rules},dst=/rules/alert_rules.openbao.yml,readonly",
                "--mount",
                f"type=bind,src={cases},dst=/p/cases.yml,readonly",
                "--workdir",
                "/p",
                PROMTOOL,
                "test",
                "rules",
                "/p/cases.yml",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
