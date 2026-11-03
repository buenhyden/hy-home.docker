"""Opt-in disposable native rehearsals for P02 service contracts."""

from __future__ import annotations

import os
import secrets
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

import yaml

from tests.validation.test_p02_service_contracts import ROOT, _service


@unittest.skipUnless(
    os.environ.get("HYHOME_P02_NATIVE") == "1",
    "set HYHOME_P02_NATIVE=1 for the disposable cached-image Traefik rehearsal",
)
class GrafanaStaticRouteNativeTests(unittest.TestCase):
    """Exercise the tracked rules through the exact cached Traefik binary."""

    TRAEFIK_IMAGE = (
        "traefik:v3.7.16@sha256:"
        "1336e85aaed293bd63d005086e0dd013b04078b26aaeb1c18b26a2f928af7e65"
    )
    PYTHON_IMAGE = "python:3.13.15-alpine"

    @classmethod
    def docker(cls, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/usr/bin/docker", "--host", "unix:///var/run/docker.sock", *args],
            capture_output=True,
            text=True,
            check=check,
            timeout=90,
            env={"HOME": "/tmp", "PATH": "/usr/bin:/bin"},
        )

    @classmethod
    def setUpClass(cls) -> None:
        if not Path("/usr/bin/docker").is_file():
            raise unittest.SkipTest("/usr/bin/docker is unavailable")
        cls.tag = f"hy-p02-grafana-{os.getpid()}-{secrets.token_hex(3)}"
        cls.network = cls.tag + "-net"
        cls.backend = cls.tag + "-backend"
        cls.proxy = cls.tag + "-proxy"
        cls.client = cls.tag + "-client"
        cls.temporary = tempfile.TemporaryDirectory(prefix="hy-p02-grafana-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.state = cls.root / "state"
        cls.state.mkdir(mode=0o777)
        cls.state.chmod(0o777)
        counter = cls.state / "count"
        counter.write_text("0", encoding="ascii")
        counter.chmod(0o666)

        labels = _service("infra/06-observability/docker-compose.yml", "grafana")[
            "labels"
        ]
        allow_rule = labels["traefik.http.routers.grafana-static.rule"].replace(
            "${DEFAULT_URL}", "p02.test"
        )
        deny_rule = labels["traefik.http.routers.grafana-static-deny.rule"].replace(
            "${DEFAULT_URL}", "p02.test"
        )
        middleware = yaml.safe_load(
            (ROOT / "infra/01-gateway/traefik/dynamic/middleware.yml").read_text(
                encoding="utf-8"
            )
        )
        oauth_template = middleware["http"]["services"]["oauth2-proxy-svc"][
            "loadBalancer"
        ]["servers"][0]["url"]
        dynamic = {
            "http": {
                "routers": {
                    "allow": {
                        "rule": allow_rule,
                        "entryPoints": ["web"],
                        "priority": int(
                            labels["traefik.http.routers.grafana-static.priority"]
                        ),
                        "middlewares": ["standard-chain"],
                        "service": "backend",
                    },
                    "deny": {
                        "rule": deny_rule,
                        "entryPoints": ["web"],
                        "priority": int(
                            labels["traefik.http.routers.grafana-static-deny.priority"]
                        ),
                        "middlewares": ["standard-chain"],
                        "service": "noop@internal",
                    },
                    "authenticated-fallback": {
                        "rule": "Host(`grafana.p02.test`)",
                        "entryPoints": ["web"],
                        "priority": 100,
                        "service": "noop@internal",
                    },
                },
                "middlewares": {
                    "standard-chain": {"chain": {"middlewares": ["peer-limit"]}},
                    "peer-limit": {
                        "rateLimit": {
                            "average": 100,
                            "period": "1s",
                            "burst": 200,
                            "sourceCriterion": {"ipStrategy": {"depth": 0}},
                        }
                    },
                },
                "services": {
                    "backend": {
                        "loadBalancer": {"servers": [{"url": "http://backend:8000"}]}
                    },
                    "oauth-template": {
                        "loadBalancer": {"servers": [{"url": oauth_template}]}
                    },
                },
            }
        }
        (cls.root / "dynamic.yml").write_text(
            yaml.safe_dump(dynamic, sort_keys=False), encoding="utf-8"
        )
        (cls.root / "server.py").write_text(_BACKEND_FIXTURE, encoding="utf-8")

        for image in (cls.TRAEFIK_IMAGE, cls.PYTHON_IMAGE):
            inspected = cls.docker("image", "inspect", image, check=False)
            if inspected.returncode:
                raise unittest.SkipTest(f"required cached image unavailable: {image}")
        cls.docker("network", "create", "--internal", cls.network)
        cls.addClassCleanup(cls.docker, "network", "rm", cls.network, check=False)
        for name in (cls.backend, cls.proxy, cls.client):
            cls.addClassCleanup(cls.docker, "rm", "-f", name, check=False)
        common = [
            "--network",
            cls.network,
            "--cpus",
            "1",
            "--memory",
            "256m",
            "--pids-limit",
            "128",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges:true",
        ]
        cls.docker(
            "run",
            "-d",
            "--name",
            cls.backend,
            *common,
            "--network-alias",
            "backend",
            "--read-only",
            "--mount",
            f"type=bind,src={cls.root / 'server.py'},dst=/fixture/server.py,readonly",
            "--mount",
            f"type=bind,src={cls.state},dst=/state",
            cls.PYTHON_IMAGE,
            "python",
            "/fixture/server.py",
        )
        cls.docker(
            "run",
            "-d",
            "--name",
            cls.proxy,
            *common,
            "--network-alias",
            "grafana.p02.test",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev,size=8m",
            "--env",
            "OAUTH2_PROXY_PORT=14180",
            "--mount",
            f"type=bind,src={cls.root / 'dynamic.yml'},dst=/dynamic/dynamic.yml,readonly",
            cls.TRAEFIK_IMAGE,
            "--entrypoints.web.address=:80",
            "--providers.file.filename=/dynamic/dynamic.yml",
            "--log.level=ERROR",
        )
        cls.docker(
            "run",
            "-d",
            "--name",
            cls.client,
            *common,
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev,size=8m",
            cls.PYTHON_IMAGE,
            "sleep",
            "infinity",
        )
        for _ in range(60):
            if cls.request("GET", "/favicon.ico") == 200:
                (cls.state / "count").write_text("0", encoding="ascii")
                break
            time.sleep(0.1)
        else:
            logs = cls.docker("logs", cls.proxy, check=False)
            raise AssertionError(
                "isolated Traefik did not become ready: " + logs.stderr
            )

    @classmethod
    def request(cls, method: str, path: str, host: str = "grafana.p02.test") -> int:
        script = (
            "import urllib.error,urllib.request;"
            f"r=urllib.request.Request('http://grafana.p02.test{path}',method={method!r},"
            f"headers={{'Host':{host!r}}});"
            "\ntry: x=urllib.request.urlopen(r,timeout=3)\n"
            "except urllib.error.HTTPError as e: x=e\n"
            "print(x.status)"
        )
        result = cls.docker("exec", cls.client, "python", "-c", script, check=False)
        if result.returncode:
            return 0
        return int(result.stdout.strip())

    @classmethod
    def count(cls) -> int:
        return int((cls.state / "count").read_text(encoding="ascii"))

    def test_only_exact_get_and_head_reach_backend(self) -> None:
        self.assertEqual(200, self.request("GET", "/favicon.ico"))
        self.assertEqual(200, self.request("HEAD", "/robots.txt"))
        self.assertEqual(2, self.count())
        for method in ("POST", "PUT", "PATCH", "DELETE", "OPTIONS"):
            for path in ("/favicon.ico", "/robots.txt"):
                with self.subTest(method=method, path=path):
                    self.assertEqual(418, self.request(method, path))
        self.assertEqual(2, self.count())


_BACKEND_FIXTURE = """import http.server
from pathlib import Path

counter = Path('/state/count')
class Handler(http.server.BaseHTTPRequestHandler):
    def hit(self, body):
        counter.write_text(str(int(counter.read_text()) + 1))
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD': self.wfile.write(body)
    def do_GET(self): self.hit(self.path.encode())
    def do_HEAD(self): self.hit(b'')
    def log_message(self, *args): pass
http.server.HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
"""


if __name__ == "__main__":
    unittest.main()
