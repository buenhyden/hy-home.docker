"""Opt-in OAuth2 Proxy OIDC verification against a controlled local issuer."""

from __future__ import annotations

import base64
import hashlib
import http.cookiejar
import http.server
import json
import os
import re
import socket
import subprocess
import tarfile
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OPENSSL = "/usr/bin/openssl"


def _test_environment(home: Path) -> dict[str, str]:
    return {
        "HOME": str(home),
        "NO_PROXY": "127.0.0.1,localhost",
        "PATH": "/usr/bin:/bin",
        "TMPDIR": str(home),
    }


def _b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: object, **kwargs: object) -> None:
        return None


class _Issuer:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.key = root / "issuer.pem"
        subprocess.run(
            [
                OPENSSL,
                "genpkey",
                "-quiet",
                "-algorithm",
                "RSA",
                "-pkeyopt",
                "rsa_keygen_bits:2048",
                "-out",
                str(self.key),
            ],
            check=True,
            capture_output=True,
            env=_test_environment(root),
        )
        public = subprocess.run(
            [
                OPENSSL,
                "pkey",
                "-in",
                str(self.key),
                "-pubout",
                "-text_pub",
                "-noout",
            ],
            check=True,
            capture_output=True,
            text=True,
            env=_test_environment(root),
        ).stdout
        modulus = re.search(r"Modulus:\n(.*?)\nExponent:", public, re.S)
        exponent = re.search(r"Exponent: (\d+)", public)
        if modulus is None or exponent is None:
            raise RuntimeError("could not parse synthetic RSA public key")
        hex_modulus = re.sub(r"[^0-9a-f]", "", modulus.group(1).lower())
        if hex_modulus.startswith("00"):
            hex_modulus = hex_modulus[2:]
        self.jwk = {
            "kty": "RSA",
            "use": "sig",
            "alg": "RS256",
            "kid": "p02-synthetic",
            "n": _b64(bytes.fromhex(hex_modulus)),
            "e": _b64(int(exponent.group(1)).to_bytes(3, "big")),
        }
        self.case = "valid"
        self.nonces: dict[str, str | None] = {}
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), self.handler())
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def token(self, code: str) -> str:
        now = int(time.time())
        claims: dict[str, object] = {
            "iss": self.base,
            "sub": "p02-user",
            "aud": "p02-client",
            "iat": now,
            "exp": now + 300,
            "email": "p02@example.test",
            "email_verified": True,
        }
        if self.nonces[code] is not None:
            claims["nonce"] = self.nonces[code]
        if code.startswith("wrong-issuer"):
            claims["iss"] = self.base + "/wrong"
        elif code.startswith("wrong-audience"):
            claims["aud"] = "other-client"
        elif code.startswith("expired"):
            claims["exp"] = now - 300
        header = {"alg": "RS256", "typ": "JWT", "kid": "p02-synthetic"}
        signing_input = ".".join(
            _b64(json.dumps(item, separators=(",", ":")).encode("ascii"))
            for item in (header, claims)
        )
        signed = subprocess.run(
            [OPENSSL, "dgst", "-sha256", "-sign", str(self.key)],
            input=signing_input.encode("ascii"),
            check=True,
            capture_output=True,
            env=_test_environment(self.root),
        ).stdout
        return signing_input + "." + _b64(signed)

    def handler(self) -> type[http.server.BaseHTTPRequestHandler]:
        issuer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def reply(self, value: object, status: int = 200) -> None:
                body = json.dumps(value).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:
                parsed = urllib.parse.urlsplit(self.path)
                query = dict(urllib.parse.parse_qsl(parsed.query))
                if parsed.path == "/.well-known/openid-configuration":
                    self.reply(
                        {
                            "issuer": issuer.base,
                            "authorization_endpoint": issuer.base + "/authorize",
                            "token_endpoint": issuer.base + "/token",
                            "jwks_uri": issuer.base + "/jwks",
                            "response_types_supported": ["code"],
                            "subject_types_supported": ["public"],
                            "id_token_signing_alg_values_supported": ["RS256"],
                        }
                    )
                elif parsed.path == "/jwks":
                    self.reply({"keys": [issuer.jwk]})
                elif parsed.path == "/authorize":
                    code = f"{issuer.case}-{time.time_ns()}"
                    issuer.nonces[code] = query.get("nonce")
                    location = (
                        query["redirect_uri"]
                        + "?"
                        + urllib.parse.urlencode(
                            {"code": code, "state": query["state"]}
                        )
                    )
                    self.send_response(302)
                    self.send_header("Location", location)
                    self.end_headers()
                else:
                    self.reply({"error": "not found"}, 404)

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                form = dict(
                    urllib.parse.parse_qsl(self.rfile.read(length).decode("ascii"))
                )
                code = form["code"]
                self.reply(
                    {
                        "access_token": "synthetic-access-token",
                        "token_type": "Bearer",
                        "expires_in": 300,
                        "id_token": issuer.token(code),
                    }
                )

            def log_message(self, *args: object) -> None:
                pass

        return Handler


@unittest.skipUnless(
    os.environ.get("HYHOME_P02_OAUTH_NATIVE") == "1",
    "set HYHOME_P02_OAUTH_NATIVE=1 with verified v7.15.5 asset paths",
)
class OAuth2ProxyOidcNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.binary = Path(os.environ["HYHOME_P02_OAUTH_BINARY"])
        archive = Path(os.environ["HYHOME_P02_OAUTH_ARCHIVE"])
        checksum = Path(os.environ["HYHOME_P02_OAUTH_CHECKSUM"])
        cls.temporary = tempfile.TemporaryDirectory(prefix="hy-p02-oidc-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.environment = _test_environment(Path(cls.temporary.name))
        expected = checksum.read_text(encoding="ascii").split()[0]
        actual = hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError("OAuth2 Proxy release archive checksum mismatch")
        with tarfile.open(archive, "r:gz") as release:
            members = release.getmembers()
            if len(members) != 2:
                raise RuntimeError("unexpected OAuth2 Proxy archive member count")
            for member in members:
                path = Path(member.name)
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or member.issym()
                    or member.islnk()
                ):
                    raise RuntimeError("unsafe OAuth2 Proxy release archive member")
            candidates = [
                member
                for member in members
                if member.isfile() and Path(member.name).name == "oauth2-proxy"
            ]
            if (
                len(candidates) != 1
                or not 1_000_000 <= candidates[0].size <= 200_000_000
            ):
                raise RuntimeError("unexpected OAuth2 Proxy binary member")
            extracted = release.extractfile(candidates[0])
            if extracted is None:
                raise RuntimeError("OAuth2 Proxy binary member could not be read")
            archive_binary_digest = hashlib.sha256(extracted.read()).hexdigest()
        binary_digest = hashlib.sha256(cls.binary.read_bytes()).hexdigest()
        if binary_digest != archive_binary_digest:
            raise RuntimeError("OAuth2 Proxy binary is not from verified archive")
        version = subprocess.run(
            [str(cls.binary), "--version"],
            check=True,
            capture_output=True,
            text=True,
            env=cls.environment,
        ).stdout
        if "oauth2-proxy v7.15.5" not in version:
            raise RuntimeError("native test requires OAuth2 Proxy v7.15.5")

        cls.issuer = _Issuer(Path(cls.temporary.name))
        cls.addClassCleanup(cls.issuer.close)
        cls.port = _free_port()
        cookie_secret = _b64(os.urandom(32))
        cls.proxy = subprocess.Popen(
            [
                str(cls.binary),
                "--provider=oidc",
                f"--oidc-issuer-url={cls.issuer.base}",
                "--client-id=p02-client",
                "--client-secret=p02-secret",
                f"--cookie-secret={cookie_secret}",
                "--cookie-secure=false",
                "--email-domain=*",
                f"--http-address=127.0.0.1:{cls.port}",
                f"--redirect-url=http://127.0.0.1:{cls.port}/oauth2/callback",
                "--upstream=static://200",
                "--skip-provider-button=true",
                "--scope=openid email profile",
                "--code-challenge-method=S256",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=cls.environment,
        )
        cls.addClassCleanup(cls.stop_proxy)
        direct = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        for _ in range(100):
            try:
                with direct.open(
                    f"http://127.0.0.1:{cls.port}/ping", timeout=0.2
                ) as response:
                    response.read()
                break
            except (OSError, urllib.error.URLError):
                if cls.proxy.poll() is not None:
                    _, stderr = cls.proxy.communicate(timeout=2)
                    raise RuntimeError(
                        "oauth2-proxy failed to start: " + stderr[-2000:]
                    ) from None
                time.sleep(0.05)
        else:
            raise RuntimeError("oauth2-proxy did not become ready")

    @classmethod
    def stop_proxy(cls) -> None:
        if cls.proxy.poll() is None:
            cls.proxy.terminate()
            try:
                cls.proxy.wait(timeout=5)
            except subprocess.TimeoutExpired:
                cls.proxy.kill()
                cls.proxy.wait(timeout=5)

    def callback_status(self, case: str) -> tuple[int, list[str]]:
        self.issuer.case = case
        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPCookieProcessor(jar),
            _NoRedirect(),
        )

        def request(url: str) -> urllib.response.addinfourl:
            try:
                return opener.open(url, timeout=3)
            except urllib.error.HTTPError as error:
                return error

        start = request(f"http://127.0.0.1:{self.port}/oauth2/start?rd=%2F")
        authorize_url = start.headers["Location"]
        start.close()
        authorize = request(authorize_url)
        callback_url = authorize.headers["Location"]
        authorize.close()
        callback = request(callback_url)
        status = callback.status
        callback.close()
        return status, [cookie.name for cookie in jar]

    def test_valid_id_token_establishes_session_control(self) -> None:
        status, cookies = self.callback_status("valid")
        self.assertEqual(302, status)
        self.assertIn("_oauth2_proxy", cookies)

    def test_wrong_issuer_audience_and_expiry_are_rejected(self) -> None:
        for case in ("wrong-issuer", "wrong-audience", "expired"):
            with self.subTest(case=case):
                status, cookies = self.callback_status(case)
                self.assertIn(status, (400, 401, 403, 500))
                self.assertFalse(
                    any(name == "_oauth2_proxy" for name in cookies), cookies
                )


if __name__ == "__main__":
    unittest.main()
