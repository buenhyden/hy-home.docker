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
IMAGE = "openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf"
MANIFEST = "sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005"


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
        (self.agent / "token").write_text(self.token)
        (self.agent / "token").chmod(0o600)
        self.rendered = [
            self.out / "auth/keycloak_admin_password.txt",
            self.out / "observability/grafana_admin_password.txt",
        ]
        for path, value in zip(self.rendered, self.values, strict=True):
            path.write_text(value)
            path.chmod(0o600)
        self.versions = [path.with_suffix(".version") for path in self.rendered]
        for path, version in zip(self.versions, ("7", "11"), strict=True):
            path.write_text(version)
            path.chmod(0o600)
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
if os.environ.get("BAO_TOKEN") not in (os.environ["STUB_TOKEN"], os.environ["STUB_CLEANUP_TOKEN"]):
    sys.exit(1)
if args[:2] == ["read", "-format=json"]:
    role = "renderer-issuer" if os.environ["BAO_TOKEN"] == os.environ["STUB_TOKEN"] else "renderer-cleanup"
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
    if payload.split("\\n",1)[0] not in (os.environ["STUB_TOKEN"],os.environ["STUB_CLEANUP_TOKEN"]):
        sys.exit(1)
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
                            for p in (fixture, self.root / "renderer-issuance.py")
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
                    for value in [self.token, self.cleanup_token, *self.values]
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

    def test_rendered_passwords_require_private_mode(self):
        for index in (0, 1):
            self.rendered[index].chmod(0o644)
            self.assertNotEqual(self.run_script("health-agent.sh").returncode, 0)
            self.rendered[index].chmod(0o600)

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

    def test_issue_and_delivery_failures_are_redacted(self):
        for failure in ("issue", "deliver", "volume"):
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


if __name__ == "__main__":
    unittest.main()
