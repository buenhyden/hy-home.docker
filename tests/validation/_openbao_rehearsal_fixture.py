#!/usr/bin/env python3
"""Owned synthetic resources and verified API for the opt-in P01 rehearsal.

Run only after reviewing the isolated boundary:
    HYHOME_OPENBAO_REHEARSAL=1 python3 -m unittest discover \
        -s tests/validation -p test_openbao_rehearsal.py -v

Requires the exact cached image; never pulls. Secret values stay in memory or
invocation-owned mode-0600 files. Subprocess output, HTTP payloads and audit
content are captured privately and never become assertion messages.
"""

import http.client
import json
import shutil
import socket
import ssl
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao"
IMAGE = "sha256:11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641"
PORT = 8240
CLUSTER_PORT = 8241


class RehearsalFailure(RuntimeError):
    """Sanitized failure: never include captured output or credential values."""


def captured(argv, *, data=None, allow_failure=False):
    """Do not expose output/arguments through CalledProcessError or logging."""
    try:
        result = subprocess.run(
            argv,
            input=data,
            capture_output=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise RehearsalFailure(
            "isolated fixture command unavailable or timed out"
        ) from None
    if result.returncode and not allow_failure:
        raise RehearsalFailure("isolated fixture command failed (output withheld)")
    return result


class OwnedFixture:
    """Ownership list is the cleanup boundary; no Docker discovery/pruning."""

    def __init__(self):
        self.owner = "p01-" + uuid.uuid4().hex
        self.directory = Path(tempfile.mkdtemp(prefix=self.owner + "-"))
        self.directory.chmod(0o750)
        self.network = self.owner + "-net"
        self.containers = []
        self.volumes = []
        self.network_created = False
        self.tls = self.directory / "tls"
        self.tls.mkdir(mode=0o750)
        self.auth = self.directory / "auth"
        self.auth.mkdir(mode=0o770)
        self.out = self.directory / "out"
        self.out.mkdir(mode=0o770)

    def docker(self, *args, data=None, allow_failure=False):
        return captured(["docker", *args], data=data, allow_failure=allow_failure)

    def prepare(self):
        inspected = self.docker("image", "inspect", IMAGE)
        try:
            image = json.loads(inspected.stdout)[0]
        except (ValueError, IndexError, KeyError):
            raise RehearsalFailure("cached image identity unavailable") from None
        if image.get("Id") != IMAGE or image.get("Architecture") != "amd64":
            raise RehearsalFailure(
                "cached image identity does not match reviewed fixture"
            )
        version = self.docker("version", "--format", "{{.Server.Version}}")
        if version.stdout.strip() != b"29.8.2":
            raise RehearsalFailure("Docker server differs from reviewed 29.8.2 input")
        self.certificates()
        self.docker(
            "network", "create", "--internal", "--label", self.owner, self.network
        )
        self.network_created = True
        self.auth_volume = self.volume("agent-auth")
        tagged = self.docker(
            "image", "inspect", "openbao/openbao:2.6.2", "--format", "{{.Id}}"
        )
        if tagged.stdout.strip().decode() != IMAGE:
            raise RehearsalFailure(
                "issuer helper cached tag differs from reviewed image"
            )

    def certificates(self):
        """CA private key is never mounted into a container."""
        issuer = self.directory / "issuer"
        issuer.mkdir(mode=0o700)
        ca_key, ca = issuer / "ca-key.pem", self.tls / "ca.pem"
        key, csr, cert = (
            self.tls / "server-key.pem",
            issuer / "server.csr",
            self.tls / "server.pem",
        )
        wrong_key, wrong_ca = issuer / "wrong-key.pem", issuer / "wrong-ca.pem"
        for private, public, name in (
            (ca_key, ca, "P01 Synthetic CA"),
            (wrong_key, wrong_ca, "P01 Untrusted CA"),
        ):
            captured(
                [
                    "openssl",
                    "req",
                    "-x509",
                    "-newkey",
                    "rsa:2048",
                    "-nodes",
                    "-keyout",
                    str(private),
                    "-out",
                    str(public),
                    "-days",
                    "1",
                    "-subj",
                    "/CN=" + name,
                ]
            )
            private.chmod(0o600)
        captured(
            [
                "openssl",
                "req",
                "-new",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(key),
                "-out",
                str(csr),
                "-subj",
                "/CN=openbao",
            ]
        )
        key.chmod(0o640)
        extension = issuer / "server.ext"
        extension.write_text(
            "subjectAltName=DNS:openbao,IP:127.0.0.1\nextendedKeyUsage=serverAuth\n"
        )
        captured(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                str(csr),
                "-CA",
                str(ca),
                "-CAkey",
                str(ca_key),
                "-CAcreateserial",
                "-out",
                str(cert),
                "-days",
                "1",
                "-extfile",
                str(extension),
            ]
        )
        self.wrong_ca = wrong_ca

    def volume(self, suffix):
        name = self.owner + "-" + suffix
        self.docker("volume", "create", "--label", self.owner, name)
        self.volumes.append(name)
        helper = self.container(
            suffix + "-prepare",
            [
                "--user",
                "0:0",
                "--cap-add",
                "CHOWN",
                "--entrypoint",
                "/bin/sh",
                "--mount",
                f"type=volume,src={name},dst=/openbao/data",
            ],
            ["-ec", "chown 100:1000 /openbao/data"],
        )
        self.docker("wait", helper)
        return name

    def container(
        self, suffix, args, command, *, image=IMAGE, start=True, network=None
    ):
        name = self.owner + "-" + suffix
        self.docker(
            "create",
            "--name",
            name,
            "--label",
            self.owner,
            "--network",
            network or self.network,
            "--log-driver",
            "none",
            "--user",
            "100:1000",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--memory",
            "384m",
            "--cpus",
            "1",
            "--pids-limit",
            "128",
            *args,
            image,
            *command,
        )
        self.containers.append(name)
        if start:
            self.docker("start", name)
        return name

    def server(self, suffix, *, active=False, tls=None, ready=True):
        tls = tls or self.tls
        compose = yaml.safe_load((SOURCE / "docker-compose.yml").read_text())
        config_text = compose["services"]["openbao"]["environment"]["BAO_LOCAL_CONFIG"]
        config_text = config_text.replace("${OPENBAO_PORT:-8200}", str(PORT))
        config_text = config_text.replace(
            "${OPENBAO_CLUSTER_PORT:-8201}", str(CLUSTER_PORT)
        )
        try:
            config = json.loads(config_text)
        except ValueError:
            raise RehearsalFailure(
                "tracked listener configuration is not JSON"
            ) from None
        tcp = config["listener"][0]["tcp"]
        if tcp.get("tls_disable") is not False:
            raise RehearsalFailure("tracked listener is not native verified TLS")
        if not config.get("audit"):
            raise RehearsalFailure("tracked listener has no declarative audit device")
        config_path = self.directory / (suffix + "-config")
        config_path.mkdir(mode=0o770)
        args = [
            "--mount",
            f"type=volume,src={self.volume(suffix)},dst=/openbao/data",
            "--mount",
            f"type=bind,src={tls},dst=/openbao/tls,readonly",
            "--mount",
            f"type=bind,src={config_path},dst=/openbao/config",
            "--mount",
            f"type=bind,src={SOURCE / 'scripts'},dst=/openbao/scripts,readonly",
            "--mount",
            f"type=volume,src={self.auth_volume},dst=/openbao/agent",
            "--tmpfs",
            "/openbao/audit:rw,size=4m,mode=0770,uid=100,gid=1000",
            "--env",
            "BAO_LOCAL_CONFIG=" + json.dumps(config),
            "--env",
            "SKIP_CHOWN=1",
            "--env",
            f"OPENBAO_PORT={PORT}",
            "--env",
            f"OPENBAO_CLUSTER_PORT={CLUSTER_PORT}",
            "--entrypoint",
            "/bin/sh",
            "--env",
            f"BAO_ADDR=https://127.0.0.1:{PORT}",
            "--env",
            "BAO_CACERT=/openbao/tls/ca.pem",
        ]
        if active:
            args += ["--network-alias", "openbao"]
        name = self.container(
            suffix, args, ["/openbao/scripts/start-server.sh", "server"]
        )
        target = (
            self.docker(
                "inspect",
                "--format",
                '{{(index .NetworkSettings.Networks "'
                + self.network
                + '").IPAddress}}',
                name,
            )
            .stdout.decode()
            .strip()
        )
        if not target:
            raise RehearsalFailure("owned internal fixture address unavailable")
        client = Client(target, tls / "ca.pem")
        if not ready:
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                try:
                    with socket.create_connection((target, PORT), timeout=1):
                        return name, client
                except OSError:
                    time.sleep(0.25)
            raise RehearsalFailure("expired-certificate fixture did not accept TCP")
        version = self.docker("exec", name, "bao", "version").stdout
        if b"OpenBao v2.6.2" not in version:
            raise RehearsalFailure("native image version is not 2.6.2")
        deadline = time.monotonic() + 40
        while time.monotonic() < deadline:
            try:
                if client.api("GET", "sys/health")[0] in (501, 503):
                    return name, client
            except RehearsalFailure:
                pass
            time.sleep(0.25)
        raise RehearsalFailure(
            "isolated server did not reach uninitialized/sealed health"
        )

    def agent(self, suffix, *, start=True):
        args = [
            "--mount",
            f"type=bind,src={SOURCE / 'config'},dst=/openbao/config,readonly",
            "--mount",
            f"type=bind,src={SOURCE / 'scripts'},dst=/openbao/scripts,readonly",
            "--mount",
            f"type=bind,src={self.tls},dst=/openbao/tls,readonly",
            "--mount",
            f"type=volume,src={self.auth_volume},dst=/openbao/agent",
            "--mount",
            f"type=bind,src={self.out},dst=/openbao/out",
            "--env",
            f"BAO_ADDR=https://openbao:{PORT}",
            "--env",
            f"VAULT_ADDR=https://openbao:{PORT}",
            "--env",
            "BAO_CACERT=/openbao/tls/ca.pem",
            "--env",
            "VAULT_CACERT=/openbao/tls/ca.pem",
            "--env",
            f"OPENBAO_PORT={PORT}",
            "--entrypoint",
            "/bin/sh",
        ]
        return self.container(
            suffix, args, ["/openbao/scripts/start-agent.sh"], start=start
        )

    def stop(self, name):
        self.docker("stop", "--time", "5", name)

    def _cleanup_command(self, *args, expected_stdout=None):
        try:
            result = self.docker(*args, allow_failure=True)
        except RehearsalFailure:
            return False
        return result.returncode == 0 and (
            expected_stdout is None or result.stdout.strip() == expected_stdout
        )

    def cleanup(self):
        failures = False
        for name in self.containers:
            failures |= not self._cleanup_command("stop", "--time", "2", name)
        if self.containers and self.network_created:
            try:
                cleanup = self.container(
                    "cleanup",
                    [
                        "--user",
                        "0:0",
                        "--cap-add",
                        "DAC_OVERRIDE",
                        "--entrypoint",
                        "/bin/sh",
                        "--mount",
                        f"type=bind,src={self.directory},dst=/p01-owned",
                    ],
                    ["-ec", "rm -rf /p01-owned/*"],
                )
                failures |= not self._cleanup_command(
                    "wait", cleanup, expected_stdout=b"0"
                )
            except RehearsalFailure:
                failures = True
        for name in reversed(self.containers):
            failures |= not self._cleanup_command("rm", "--force", name)
        for name in reversed(self.volumes):
            failures |= not self._cleanup_command("volume", "rm", name)
        if self.network_created:
            failures |= not self._cleanup_command("network", "rm", self.network)
        try:
            shutil.rmtree(self.directory)
        except OSError:
            failures = True
        if failures:
            raise RehearsalFailure(
                "owned fixture cleanup failed; owned names require review"
            )


class VerifiedConnection(http.client.HTTPSConnection):
    def __init__(self, target, hostname, context):
        super().__init__(hostname, PORT, timeout=30, context=context)
        self.target = target

    def connect(self):
        raw = socket.create_connection((self.target, PORT), timeout=self.timeout)
        self.sock = self._context.wrap_socket(raw, server_hostname=self.host)


class Client:
    def __init__(self, target, ca, *, hostname="openbao"):
        self.target = target
        self.hostname = hostname
        self.context = ssl.create_default_context(cafile=str(ca))
        self.token = None

    def api(
        self, method, path, payload=None, *, token=None, headers=None, binary=False
    ):
        data = (
            payload
            if binary
            else (json.dumps(payload).encode() if payload is not None else None)
        )
        request_headers = {
            "Content-Type": "application/octet-stream" if binary else "application/json"
        }
        credential = self.token if token is None else token
        if credential:
            request_headers["X-Vault-Token"] = credential
        request_headers.update(headers or {})
        connection = VerifiedConnection(self.target, self.hostname, self.context)
        try:
            connection.request(method, "/v1/" + path, data, request_headers)
            response = connection.getresponse()
            status, body = response.status, response.read()
        except (OSError, http.client.HTTPException) as error:
            raise RehearsalFailure(
                "verified TLS request failed: " + type(error).__name__
            ) from None
        finally:
            connection.close()
        if binary:
            return status, body
        if not body:
            return status, {}
        try:
            return status, json.loads(body)
        except ValueError:
            return status, {}

    def initialize(self):
        status, result = self.api(
            "POST", "sys/init", {"secret_shares": 3, "secret_threshold": 2}
        )
        if status != 200:
            raise RehearsalFailure("synthetic initialization failed")
        self.token = result["root_token"]
        shares = result["keys_base64"]
        self.unseal(shares)
        self.wait_open()
        return shares

    def wait_open(self):
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if self.api("GET", "sys/health")[0] == 200:
                return
            time.sleep(0.25)
        raise RehearsalFailure("unsealed Raft fixture did not elect a healthy leader")

    def unseal(self, shares):
        for share in shares[:2]:
            status, result = self.api("POST", "sys/unseal", {"key": share})
            if status != 200:
                raise RehearsalFailure("synthetic unseal failed")
        if result.get("sealed") is not False:
            raise RehearsalFailure("synthetic unseal did not open the server")
