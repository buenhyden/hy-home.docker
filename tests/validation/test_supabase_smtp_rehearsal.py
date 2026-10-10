"""Opt-in isolated GoTrue SMTP rehearsal using only synthetic credentials.

Run with HYHOME_SUPABASE_SMTP_REHEARSAL=1 and this unittest module.

Requires cached pins, Docker, openssl, local Go, and PyYAML. Owns only a unique
network, named containers, and a temporary directory. Never reads HOME credentials
or logs; captured output is excluded. This is ISOLATED evidence, not HOME.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from tests.validation._supabase_smtp_fixture_storage import (
    PUBLIC_SYNTHETIC_DB_PASSWORD,
    PUBLIC_SYNTHETIC_JWT,
    PUBLIC_SYNTHETIC_SIGNUP_EMAILS,
    PUBLIC_SYNTHETIC_SIGNUP_PASSWORD,
    PUBLIC_SYNTHETIC_SMTP_PASSWORD,
    PUBLIC_SYNTHETIC_WRONG_SMTP_PASSWORD,
    write_exclusive,
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/04-data/supabase/docker-compose.yml"
AUTH = "supabase/gotrue:v2.197.0@sha256:1736a63078f5922b198c4cbe50f80ab9a2d3b54fe8b7b6cfb2e9dc5dbbc12c6b"
MAIL = "axllent/mailpit:v1.31.2@sha256:74d609a42ec279aa63c6b4622a6fa9b5408d1ad5b1d76a1c4be40a265ce0863d"
POSTGRES = "postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873"


class RehearsalFailure(AssertionError):
    """Safe status-only exception; never attach command output."""


def captured(args, *, check=True, timeout=180, input_=None, env=None):
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            timeout=timeout,
            check=False,
            input=input_,
            env=env,
        )
    except (subprocess.TimeoutExpired, OSError):
        raise RehearsalFailure(
            "isolated fixture command timeout/unavailable (output withheld)"
        ) from None
    if check and result.returncode:
        raise RehearsalFailure("isolated fixture command failed (output withheld)")
    return result


class SMTPFixture:
    def __init__(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="smtp01-synthetic-")
        self.directory = Path(self.scratch.name)
        self.prefix = "smtp01-" + secrets.token_hex(6)
        self.network = self.prefix + "-network"
        self.containers = []
        self.network_created = False
        self.smtp_password = PUBLIC_SYNTHETIC_SMTP_PASSWORD
        self.db_password = PUBLIC_SYNTHETIC_DB_PASSWORD
        self.jwt = PUBLIC_SYNTHETIC_JWT
        self.signup_count = 0

    def docker(self, *args, check=True, timeout=180, input_=None):
        return captured(["docker", *args], check=check, timeout=timeout, input_=input_)

    def write(self, name, content, mode=0o600):
        return write_exclusive(self.directory, name, content, mode)

    def create(self, suffix, image, *args, command=(), network=None):
        name = self.prefix + "-" + suffix
        # A CLI timeout may follow daemon creation. Register the exact owned
        # name before mutation so cleanup can still remove that resource.
        self.containers.append(name)
        self.docker(
            "create",
            "--name",
            name,
            "--network",
            network or self.network,
            "--log-driver",
            "none",
            *args,
            image,
            *command,
        )
        self.docker("start", name)
        return name

    def build_http_peer(self):
        # Standard-library-only HTTP client keeps request contexts alive while
        # GoTrue performs DB writes. It emits no response body, tokens or logs.
        source = self.write(
            "http-peer.go",
            r"""package main
import (
 "bytes"; "encoding/json"; "io"; "net/http"; "os"; "strings"; "time"
)
func main() {
 summary := struct { Status int `json:"status"`; SMTPFailure bool `json:"smtp_failure"`; Total int `json:"total"` }{Total:-1}
 defer func(){json.NewEncoder(os.Stdout).Encode(summary)}()
 if len(os.Args)!=3 {return}
 data,err:=io.ReadAll(io.LimitReader(os.Stdin,1048576)); if err!=nil {return}
 req,err:=http.NewRequest(os.Args[1],os.Args[2],bytes.NewReader(data)); if err!=nil {return}
 req.Header.Set("Content-Type","application/json")
 client:=http.Client{Timeout:8*time.Second,Transport:&http.Transport{Proxy:nil}}
 response,err:=client.Do(req); if err!=nil {return}; defer response.Body.Close()
 body,err:=io.ReadAll(io.LimitReader(response.Body,1048576)); if err!=nil {return}
 summary.Status=response.StatusCode
 var parsed struct { Total *int `json:"total"`; Msg string `json:"msg"`; ErrorCode string `json:"error_code"` }
 if json.Unmarshal(body,&parsed)==nil {
  if parsed.Total!=nil {summary.Total=*parsed.Total}
  summary.SMTPFailure=parsed.ErrorCode=="email_send_error" || strings.Contains(parsed.Msg,"Error sending confirmation email")
 }
}
""",
        )
        compiler_env = {
            "PATH": os.environ.get("PATH", ""),
            "CGO_ENABLED": "0",
            "GOOS": "linux",
            "GOARCH": "amd64",
            "GO111MODULE": "off",
            "GOTOOLCHAIN": "local",
            "GOCACHE": str(self.directory / "go-cache"),
            "GOPATH": str(self.directory / "go-path"),
        }
        captured(
            ["go", "build", "-o", str(self.directory / "http-peer"), str(source)],
            env=compiler_env,
        )
        (self.directory / "http-peer").chmod(0o755)

    def owned_ip(self, name):
        result = self.docker(
            "inspect",
            "--format",
            "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
            name,
        )
        address = result.stdout.decode().strip()
        if not re.fullmatch(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", address):
            raise RehearsalFailure("owned peer IP resolution failed")
        return address

    def http(self, url, payload=None):
        # Request payload goes via stdin to the owned DB peer. Only a safe
        # status/category/count summary comes back, never the response body.
        result = self.docker(
            "exec",
            "-i",
            self.prefix + "-db",
            "/fixture/http-peer",
            "POST" if payload is not None else "GET",
            url,
            check=False,
            timeout=15,
            input_=json.dumps(payload).encode() if payload is not None else b"",
        )
        try:
            summary = json.loads(result.stdout)
            return summary["status"], summary["smtp_failure"], summary["total"]
        except (ValueError, KeyError, TypeError):
            raise RehearsalFailure(
                "owned HTTP peer returned invalid status summary"
            ) from None

    def wait_http(self, url):
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            if self.http(url)[0] == 200:
                return
            time.sleep(0.25)
        raise RehearsalFailure("isolated service did not become healthy")

    def _verify_images(self):
        for image in (AUTH, MAIL, POSTGRES):
            metadata = json.loads(self.docker("image", "inspect", image).stdout)[0]
            if metadata.get("Os") != "linux" or metadata.get("Architecture") != "amd64":
                raise RehearsalFailure("fixture requires observed linux/amd64 platform")
            if not any(
                item.endswith("@" + image.split("@", 1)[1])
                for item in metadata.get("RepoDigests", [])
            ):
                raise RehearsalFailure(
                    "fixture image digest differs from fixed contract"
                )
            if image == AUTH and (
                metadata["Config"].get("User") != "supabase"
                or metadata["Config"].get("Entrypoint") is not None
                or metadata["Config"].get("Cmd") != ["auth"]
            ):
                raise RehearsalFailure(
                    "upstream auth startup contract differs; revalidate wrapper"
                )

    def _prepare_fixture_files(self):
        self.build_http_peer()
        # Track creation intent before the CLI; daemon success can precede a
        # client timeout and must not escape the bounded cleanup path.
        self.network_created = True
        self.docker("network", "create", "--internal", self.network)
        self.write("smtp-password", self.smtp_password + "\n", 0o640)
        self.write("wrong-password", PUBLIC_SYNTHETIC_WRONG_SMTP_PASSWORD + "\n", 0o640)
        self.write("empty-password", "", 0o640)
        self.write("unreadable-password", self.smtp_password + "\n", 0o000)
        self.write("db-password", self.db_password, 0o644)
        self.write("smtp-auth", "fixture:" + self.smtp_password + "\n", 0o644)
        self.certificates()

    def _set_secret_file_ownership(self):
        # Exact synthetic files only: force supplemental group access. The
        # image's UID1000 cannot rely on owner/world read permissions.
        owner_helper = self.create(
            "file-owner",
            AUTH,
            "--user",
            "0:0",
            "--mount",
            f"type=bind,src={self.directory / 'smtp-password'},dst=/fixture/smtp-password",
            "--mount",
            f"type=bind,src={self.directory / 'wrong-password'},dst=/fixture/wrong-password",
            "--mount",
            f"type=bind,src={self.directory / 'empty-password'},dst=/fixture/empty-password",
            "--mount",
            f"type=bind,src={self.directory / 'unreadable-password'},dst=/fixture/unreadable-password",
            "--entrypoint",
            "/bin/sh",
            command=(
                "-c",
                "chown 0:23456 /fixture/smtp-password /fixture/wrong-password "
                "/fixture/empty-password /fixture/unreadable-password",
            ),
            network="none",
        )
        if self.docker("wait", owner_helper, timeout=15).stdout.strip() != b"0":
            raise RehearsalFailure("synthetic file ownership setup failed")

    def _start_database(self):
        self.create(
            "db",
            POSTGRES,
            "--network-alias",
            "db",
            "--tmpfs",
            "/var/lib/postgresql:rw",
            "--mount",
            f"type=bind,src={self.directory / 'http-peer'},dst=/fixture/http-peer,readonly",
            "--mount",
            f"type=bind,src={self.directory / 'db-password'},dst=/run/secrets/db-password,readonly",
            "-e",
            "POSTGRES_PASSWORD_FILE=/run/secrets/db-password",
        )
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            if (
                self.docker(
                    "exec",
                    self.prefix + "-db",
                    "pg_isready",
                    "-h",
                    "127.0.0.1",
                    "-U",
                    "postgres",
                    check=False,
                ).returncode
                == 0
            ):
                break
            time.sleep(0.25)
        else:
            raise RehearsalFailure("isolated database did not become ready")

    def _initialize_database(self):
        # Upstream auth migrations expect these platform roles even in a
        # standalone synthetic database; no HOME/platform service is started.
        self.docker(
            "exec",
            self.prefix + "-db",
            "psql",
            "-U",
            "postgres",
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            "CREATE ROLE supabase_auth_admin NOLOGIN; CREATE ROLE anon NOLOGIN; "
            "CREATE ROLE authenticated NOLOGIN; CREATE ROLE service_role NOLOGIN; "
            'CREATE EXTENSION "uuid-ossp"; CREATE EXTENSION pgcrypto; '
            "CREATE SCHEMA auth AUTHORIZATION supabase_auth_admin; "
            "CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql STABLE AS "
            "$$ SELECT NULLIF(current_setting('request.jwt.claim.sub', true), '')::uuid $$; "
            "CREATE FUNCTION auth.role() RETURNS text LANGUAGE sql STABLE AS "
            "$$ SELECT NULLIF(current_setting('request.jwt.claim.role', true), '') $$; "
            "CREATE FUNCTION auth.email() RETURNS text LANGUAGE sql STABLE AS "
            "$$ SELECT NULLIF(current_setting('request.jwt.claim.email', true), '') $$;",
        )

    def _start_mail(self):
        self.mail = self.create(
            "mail",
            MAIL,
            "--network-alias",
            "smtp",
            "--mount",
            f"type=bind,src={self.directory / 'smtp-auth'},dst=/fixture/smtp-auth,readonly",
            "--mount",
            f"type=bind,src={self.directory / 'server.pem'},dst=/fixture/server.pem,readonly",
            "--mount",
            f"type=bind,src={self.directory / 'server.key'},dst=/fixture/server.key,readonly",
            command=(
                "--smtp-auth-file",
                "/fixture/smtp-auth",
                "--smtp-tls-cert",
                "/fixture/server.pem",
                "--smtp-tls-key",
                "/fixture/server.key",
                "--smtp-require-starttls",
                "--smtp-auth-accept-any=false",
                "--smtp-auth-allow-insecure=false",
                "--smtp-disable-rdns",
                "--disable-version-check",
                "--quiet",
            ),
        )
        self.mail_url = "http://" + self.owned_ip(self.mail) + ":8025"
        self.wait_http(self.mail_url + "/readyz")

    def setup(self):
        self._verify_images()
        self._prepare_fixture_files()
        self._set_secret_file_ownership()
        self._start_database()
        self._initialize_database()
        self._start_mail()

    def _create_ca(self, ca, key):
        captured(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-days",
                "1",
                "-subj",
                "/CN=SMTP01 Synthetic CA",
                "-keyout",
                str(key),
                "-out",
                str(ca),
            ]
        )

    def _create_server_certificate(self, ca, key, server, server_key, csr, extensions):
        captured(
            [
                "openssl",
                "req",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-subj",
                "/CN=smtp",
                "-keyout",
                str(server_key),
                "-out",
                str(csr),
            ]
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
                str(key),
                "-CAcreateserial",
                "-days",
                "1",
                "-extfile",
                str(extensions),
                "-out",
                str(server),
            ]
        )

    def certificates(self):
        ca = self.directory / "ca.pem"
        key = self.directory / "ca.key"
        server = self.directory / "server.pem"
        server_key = self.directory / "server.key"
        csr = self.directory / "server.csr"
        extensions = self.write(
            "extensions", "subjectAltName=DNS:smtp\nextendedKeyUsage=serverAuth\n"
        )
        self._create_ca(ca, key)
        self._create_server_certificate(ca, key, server, server_key, csr, extensions)
        ca.chmod(0o644)
        server.chmod(0o644)
        server_key.chmod(0o600)

    def _auth_peers(self):
        # Docker embedded DNS is unavailable to this image's unprivileged
        # Go resolver on the isolated host. Resolve only our owned peers once,
        # then keep stable names for PostgreSQL and certificate verification.
        peers = {}
        for alias, container in (("db", self.prefix + "-db"), ("smtp", self.mail)):
            peers[alias] = (
                self.docker(
                    "inspect",
                    "--format",
                    "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
                    container,
                )
                .stdout.decode()
                .strip()
            )
            if not re.fullmatch(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", peers[alias]):
                raise RehearsalFailure("owned peer IP resolution failed")
        return peers

    def _auth_environment(self):
        environment = {
            "GOTRUE_API_HOST": "0.0.0.0",
            "PORT": "9999",
            "GOTRUE_API_PORT": "9999",
            "API_EXTERNAL_URL": "http://example.invalid",
            "GOTRUE_SITE_URL": "http://example.invalid",
            "GOTRUE_DB_DRIVER": "postgres",
            "GOTRUE_DB_DATABASE_URL": "postgres://postgres:"
            + self.db_password
            + "@db:5432/postgres?sslmode=disable&search_path=auth,public",
            "GOTRUE_JWT_SECRET": self.jwt,
            "GOTRUE_JWT_AUD": "authenticated",
            "GOTRUE_JWT_DEFAULT_GROUP_NAME": "authenticated",
            "GOTRUE_SMTP_HOST": "smtp",
            "GOTRUE_SMTP_PORT": "1025",
            "GOTRUE_SMTP_USER": "fixture",
            "GOTRUE_SMTP_ADMIN_EMAIL": "noreply@example.com",
            "GOTRUE_SMTP_PASS_FILE": "/run/secrets/supabase_smtp_password",
            "GOTRUE_MAILER_AUTOCONFIRM": "false",
            "GOTRUE_RATE_LIMIT_EMAIL_SENT": "1000",
            "GOTRUE_LOG_LEVEL": "fatal",
            "GOTRUE_DISABLE_SIGNUP": "false",
        }
        environment["DATABASE_URL"] = environment["GOTRUE_DB_DATABASE_URL"]
        return environment

    def _auth_create_args(self, suffix, smtp_value, trusted, group_granted):
        args = ["--network-alias", suffix, "--init"]
        for alias, address in self._auth_peers().items():
            args.extend(("--add-host", alias + ":" + address))
        if group_granted:
            args.extend(("--group-add", "23456"))
        environment = self._auth_environment()
        if trusted:
            environment["SSL_CERT_FILE"] = "/fixture/ca.pem"
        envfile = self.write(
            suffix + ".env",
            "".join(key + "=" + value + "\n" for key, value in environment.items()),
        )
        args.extend(
            (
                "--env-file",
                str(envfile),
                "--mount",
                f"type=bind,src={self.directory / 'ca.pem'},dst=/fixture/ca.pem,readonly",
            )
        )
        if smtp_value != "missing":
            args.extend(
                (
                    "--mount",
                    f"type=bind,src={self.directory / smtp_value},dst=/run/secrets/supabase_smtp_password,readonly",
                )
            )
        return args

    def _auth_command(self, auth, args, wrapped):
        if wrapped:
            entrypoint = auth.get("entrypoint", [])
            if len(entrypoint) != 4 or entrypoint[:2] != ["/bin/sh", "-ec"]:
                raise RehearsalFailure(
                    "production SMTP wrapper has not been implemented"
                )
            args.extend(("--entrypoint", entrypoint[0]))
            # Compose unescapes doubled dollar signs before executing shells.
            command = (
                entrypoint[1],
                entrypoint[2].replace("$$", "$"),
                entrypoint[3],
                *auth["command"],
            )
        else:
            command = ()
        return command

    def start_auth(
        self,
        suffix,
        *,
        wrapped=True,
        smtp_value="smtp-password",
        trusted=True,
        group_granted=True,
    ):
        model = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
        auth = model["services"]["auth"]
        args = self._auth_create_args(suffix, smtp_value, trusted, group_granted)
        command = self._auth_command(auth, args, wrapped)
        name = self.create(suffix, AUTH, *args, command=command)
        # Rejected startup cases intentionally exit before an IP is assigned;
        # their verdict is the exit status, not an HTTP/network assertion.
        if (
            smtp_value in ("missing", "empty-password", "unreadable-password")
            or not group_granted
        ):
            return name, None
        return name, "http://" + self.owned_ip(name) + ":9999"

    def signup(self, url):
        # Reject a broken synthetic DB as a fixture error, never SMTP evidence.
        database_ready = self.docker(
            "exec",
            self.prefix + "-db",
            "psql",
            "-Atq",
            "-U",
            "postgres",
            "-c",
            "SELECT to_regclass('auth.users') IS NOT NULL AND "
            "has_table_privilege('postgres', 'auth.users', 'SELECT,INSERT');",
        ).stdout.strip()
        if database_ready != b"t":
            raise RehearsalFailure("synthetic auth schema/role is not ready")
        try:
            email = PUBLIC_SYNTHETIC_SIGNUP_EMAILS[self.signup_count]
        except IndexError:
            raise RehearsalFailure(
                "synthetic signup fixture inputs exhausted"
            ) from None
        self.signup_count += 1
        return self.http(
            url + "/signup",
            {
                "email": email,
                "password": PUBLIC_SYNTHETIC_SIGNUP_PASSWORD,
            },
        )

    def captures(self):
        status, _, total = self.http(self.mail_url + "/api/v1/messages")
        if status != 200:
            raise RehearsalFailure("capture API failed")
        if total < 0:
            raise RehearsalFailure("capture API omitted count")
        return total

    def cleanup(self):
        failed = False
        for name in reversed(self.containers):
            try:
                failed |= (
                    self.docker(
                        "rm", "--force", name, check=False, timeout=30
                    ).returncode
                    != 0
                )
            except (subprocess.TimeoutExpired, RehearsalFailure):
                failed = True
        if self.network_created:
            failed |= (
                self.docker(
                    "network", "rm", self.network, check=False, timeout=30
                ).returncode
                != 0
            )
        self.scratch.cleanup()
        if failed:
            raise RehearsalFailure("owned fixture cleanup incomplete")


class CapturedOutputSafetyTests(unittest.TestCase):
    def test_timeout_discards_captured_output(self):
        marker = b"synthetic-sensitive-output"
        exception = subprocess.TimeoutExpired(
            "fixture", 1, output=marker, stderr=marker
        )
        with patch("subprocess.run", side_effect=exception):
            with self.assertRaises(RehearsalFailure) as caught:
                captured(["fixture"], timeout=1)
        self.assertNotIn(marker.decode(), str(caught.exception))
        self.assertTrue(caught.exception.__suppress_context__)

    def test_os_failure_discards_detail(self):
        with patch("subprocess.run", side_effect=OSError("synthetic-sensitive-output")):
            with self.assertRaises(RehearsalFailure) as caught:
                captured(["fixture"])
        self.assertNotIn("synthetic-sensitive-output", str(caught.exception))
        self.assertTrue(caught.exception.__suppress_context__)


class FixtureCleanupTimeoutTests(unittest.TestCase):
    def test_container_created_before_cli_timeout_is_removed(self):
        fixture = SMTPFixture()
        daemon_containers = set()

        def daemon(args, **kwargs):
            if args[1] == "create":
                daemon_containers.add(args[args.index("--name") + 1])
                raise subprocess.TimeoutExpired(
                    args, 1, output=b"withheld-fixture-output"
                )
            if args[1:3] == ["rm", "--force"]:
                daemon_containers.remove(args[-1])
            return subprocess.CompletedProcess(args, 0, stdout=b"", stderr=b"")

        try:
            with patch("subprocess.run", side_effect=daemon):
                with self.assertRaises(RehearsalFailure):
                    fixture.create("timed-out", AUTH)
                fixture.cleanup()
            self.assertEqual(
                set(), daemon_containers, "created container escaped timeout cleanup"
            )
        finally:
            fixture.scratch.cleanup()

    def test_network_created_before_cli_timeout_is_removed(self):
        fixture = SMTPFixture()
        daemon_networks = set()

        def daemon(args, **kwargs):
            if args[1:3] == ["image", "inspect"]:
                metadata = {
                    "Os": "linux",
                    "Architecture": "amd64",
                    "RepoDigests": [args[-1]],
                    "Config": {"User": "supabase", "Entrypoint": None, "Cmd": ["auth"]},
                }
                return subprocess.CompletedProcess(
                    args, 0, stdout=json.dumps([metadata]).encode(), stderr=b""
                )
            if args[1:3] == ["network", "create"]:
                daemon_networks.add(args[-1])
                raise subprocess.TimeoutExpired(
                    args, 1, output=b"withheld-fixture-output"
                )
            if args[1:3] == ["network", "rm"]:
                daemon_networks.remove(args[-1])
            return subprocess.CompletedProcess(args, 0, stdout=b"", stderr=b"")

        try:
            with (
                patch("subprocess.run", side_effect=daemon),
                patch.object(fixture, "build_http_peer"),
            ):
                with self.assertRaises(RehearsalFailure):
                    fixture.setup()
                fixture.cleanup()
            self.assertEqual(
                set(), daemon_networks, "created network escaped timeout cleanup"
            )
        finally:
            fixture.scratch.cleanup()


@unittest.skipUnless(
    os.environ.get("HYHOME_SUPABASE_SMTP_REHEARSAL") == "1",
    "isolated native rehearsal requires opt-in",
)
class SupabaseSMTPRehearsalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = SMTPFixture()
        try:
            cls.fixture.setup()
        except BaseException:
            cls.fixture.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def test_01_unwrapped_file_variable_cannot_authenticate(self):
        fixture = self.fixture
        name, url = fixture.start_auth("baseline", wrapped=False)
        fixture.wait_http(url + "/health")
        before = fixture.captures()
        status, smtp_failure, _ = fixture.signup(url)
        self.assertEqual(
            500, status, "unwrapped _FILE unexpectedly sent authenticated SMTP"
        )
        self.assertTrue(smtp_failure, "baseline failed before reaching SMTP")
        self.assertEqual(before, fixture.captures(), "unwrapped auth captured email")
        fixture.docker("stop", "--time", "3", name)

    def test_02_production_wrapper_reads_as_image_user_and_delivers(self):
        fixture = self.fixture
        name, url = fixture.start_auth("correct")
        self.assertEqual(
            b"1000", fixture.docker("exec", name, "id", "-u").stdout.strip()
        )
        self.assertEqual(
            b"1000", fixture.docker("exec", name, "id", "-g").stdout.strip()
        )
        self.assertIn(b"23456", fixture.docker("exec", name, "id", "-G").stdout.split())
        fixture.wait_http(url + "/health")
        before = fixture.captures()
        self.assertEqual(
            200, fixture.signup(url)[0], "production wrapper SMTP signup failed"
        )
        self.assertEqual(
            before + 1, fixture.captures(), "signup did not capture exactly one email"
        )
        self.assertEqual(
            b"auth",
            fixture.docker(
                "exec", name, "/bin/sh", "-c", "cat /proc/$(pgrep -x auth)/comm"
            ).stdout.strip(),
        )
        fixture.docker("kill", "--signal", "TERM", name)
        code = fixture.docker("wait", name, timeout=15).stdout.strip()
        self.assertIn(
            code, (b"0", b"143"), "auth child did not terminate after forwarded SIGTERM"
        )

    def test_03_wrong_password_fails_without_capture(self):
        fixture = self.fixture
        name, url = fixture.start_auth("wrong", smtp_value="wrong-password")
        fixture.wait_http(url + "/health")
        before = fixture.captures()
        status, smtp_failure, _ = fixture.signup(url)
        self.assertEqual(500, status, "wrong SMTP password accepted")
        self.assertTrue(smtp_failure, "wrong-password case failed before reaching SMTP")
        self.assertEqual(before, fixture.captures(), "wrong password captured email")
        fixture.docker("stop", "--time", "3", name)

    def test_04_untrusted_tls_fails_without_capture(self):
        fixture = self.fixture
        name, url = fixture.start_auth("untrusted", trusted=False)
        fixture.wait_http(url + "/health")
        before = fixture.captures()
        status, smtp_failure, _ = fixture.signup(url)
        self.assertEqual(500, status, "untrusted SMTP TLS accepted")
        self.assertTrue(smtp_failure, "untrusted-TLS case failed before reaching SMTP")
        self.assertEqual(before, fixture.captures(), "untrusted TLS captured email")
        fixture.docker("stop", "--time", "3", name)

    def test_05_missing_empty_unreadable_files_reject_before_auth(self):
        fixture = self.fixture
        for suffix, smtp_value in (
            ("missing", "missing"),
            ("empty", "empty-password"),
            ("unreadable", "unreadable-password"),
        ):
            with self.subTest(case=suffix):
                name, _ = fixture.start_auth(suffix, smtp_value=smtp_value)
                result = fixture.docker("wait", name, timeout=15)
                self.assertNotEqual(
                    b"0",
                    result.stdout.strip(),
                    "invalid SMTP secret did not fail startup",
                )

    def test_06_supplemental_group_is_required_for_secret_read(self):
        fixture = self.fixture
        name, _ = fixture.start_auth("no-group", group_granted=False)
        result = fixture.docker("wait", name, timeout=15)
        self.assertNotEqual(
            b"0",
            result.stdout.strip(),
            "secret readable without required supplemental group",
        )


if __name__ == "__main__":
    unittest.main()
