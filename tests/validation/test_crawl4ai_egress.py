"""Crawl4AI egress gateway and network contract (SPEC-0220)."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import pathlib
import secrets
import socket
import struct
import subprocess
import sys
import tempfile
import time
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "egress_gateway", ROOT / "infra/08-ai/crawl4ai/egress_gateway.py"
)
gateway = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gateway)
COMPOSE = ROOT / "infra/08-ai/crawl4ai/docker-compose.yml"
EGRESS_IP = "10.250.200.2"


def dns_query(name: str, qtype: int, ident: int = 0x1234) -> bytes:
    labels = b"".join(bytes([len(p)]) + p.encode() for p in name.split("."))
    header = struct.pack("!HHHHHH", ident, 0x0100, 1, 0, 0, 0)
    return header + labels + b"\0" + struct.pack("!HH", qtype, 1)


class AddressRuleTests(unittest.TestCase):
    def test_only_global_unicast_ipv4_passes(self):
        for address in ("93.184.216.34", "8.8.8.8", "11.200.0.10"):
            with self.subTest(address):
                self.assertTrue(gateway.allowed_address(address))
        for address in (
            "127.0.0.1", "10.0.0.1", "172.16.0.1", "192.168.0.13", "169.254.169.254",
            "100.64.0.1", "0.0.0.0", "224.0.0.251", "240.0.0.1", "255.255.255.255",
            "192.0.2.1", "198.18.0.1", "10.250.200.2",
            "2001:4860:4860::8888", "::1", "::ffff:127.0.0.1", "::ffff:8.8.8.8",
            "64:ff9b::a00:1", "2002:a00:1::", "2001:0:4136:e378:8000:63bf:f5ff:fffe",
            "fe80::1", "fd00::1", "not-an-address",
        ):  # fmt: skip
            with self.subTest(address):
                self.assertFalse(gateway.allowed_address(address))

    def test_pin_refuses_ports_literals_mixed_answers_and_integer_forms(self):
        answers = {
            "mixed.test": ["93.184.216.34", "10.0.0.1"],
            "ok.test": ["93.184.216.34"],
        }

        async def resolve(host, port):
            return answers[host]

        async def run():
            self.assertEqual(
                "93.184.216.34", await gateway.pin("ok.test", 443, resolve)
            )
            for host, port in (
                ("ok.test", 22), ("ok.test", 8080), ("mixed.test", 443),
                ("169.254.169.254", 80), ("[::1]", 443), ("[::ffff:7f00:1]", 80),
            ):  # fmt: skip
                with self.subTest(host=host, port=port):
                    with self.assertRaises(gateway.Refused):
                        await gateway.pin(host, port, resolve)
            # The system resolver turns integer and hex forms into loopback.
            for host in ("2130706433", "0x7f000001", "localhost"):
                with self.subTest(host), self.assertRaises(gateway.Refused):
                    await gateway.pin(host, 80, gateway.system_resolve)

        asyncio.run(run())


class ProxyTests(unittest.TestCase):
    """The proxy against a local origin; the dialer records the checked address."""

    def setUp(self):
        self.dialed = []
        self.resolved = []
        self.answers = {
            "allowed.test": [["93.184.216.34"]],
            "private.test": [["10.0.0.5"]],
        }

    async def _resolve(self, host, port):
        self.resolved.append(host)
        queue = self.answers[host]
        return queue.pop(0) if len(queue) > 1 else queue[0]

    async def _exchange(self, request: bytes, origin_reply: bytes = b""):
        received = bytearray()

        async def origin(reader, writer):
            received.extend(await reader.read(65536))
            writer.write(origin_reply)
            await writer.drain()
            writer.close()

        origin_server = await asyncio.start_server(origin, "127.0.0.1", 0)
        origin_port = origin_server.sockets[0].getsockname()[1]

        async def dial(ip, port):
            self.dialed.append((ip, port))
            return await asyncio.open_connection("127.0.0.1", origin_port)

        proxy = gateway.Proxy(resolve=self._resolve, dial=dial)
        server = await asyncio.start_server(
            proxy.handle, "127.0.0.1", 0, limit=gateway.MAX_HEAD
        )
        reader, writer = await asyncio.open_connection(
            "127.0.0.1", server.sockets[0].getsockname()[1]
        )
        writer.write(request)
        await writer.drain()
        if request.startswith(b"CONNECT"):
            reply = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 5)
            if b" 200 " in reply:
                writer.write(b"tunneled-bytes")
                await writer.drain()
                await asyncio.sleep(0.2)
        else:
            reply = await asyncio.wait_for(reader.read(), 5)
        writer.close()
        server.close()
        origin_server.close()
        return reply, bytes(received)

    def test_connect_tunnels_to_the_checked_address(self):
        reply, received = asyncio.run(
            self._exchange(b"CONNECT allowed.test:443 HTTP/1.1\r\n\r\n")
        )
        self.assertIn(b"200 Connection established", reply)
        self.assertEqual([("93.184.216.34", 443)], self.dialed)
        self.assertEqual(b"tunneled-bytes", received)

    def test_refusals_never_dial(self):
        for request in (
            b"CONNECT private.test:443 HTTP/1.1\r\n\r\n",
            b"CONNECT allowed.test:22 HTTP/1.1\r\n\r\n",
            b"CONNECT 169.254.169.254:80 HTTP/1.1\r\n\r\n",
            b"CONNECT [::1]:443 HTTP/1.1\r\n\r\n",
            b"GET http://private.test/ HTTP/1.1\r\nHost: private.test\r\n\r\n",
            b"GET https://allowed.test/ HTTP/1.1\r\n\r\n",
            b"GET /relative HTTP/1.1\r\nHost: allowed.test\r\n\r\n",
        ):
            with self.subTest(request):
                self.dialed.clear()
                reply, _ = asyncio.run(self._exchange(request))
                self.assertTrue(reply.startswith(b"HTTP/1.1 403"), reply)
                self.assertEqual([], self.dialed)

    def test_malformed_request_is_a_bad_request(self):
        reply, _ = asyncio.run(self._exchange(b"NONSENSE\r\n\r\n"))
        self.assertTrue(reply.startswith(b"HTTP/1.1 400"), reply)

    def test_plain_http_keeps_host_drops_proxy_headers_and_closes(self):
        reply, received = asyncio.run(
            self._exchange(
                b"GET http://93.184.216.34:80/page?q=1 HTTP/1.1\r\nHost: allowed.test\r\n"
                b"Proxy-Authorization: Basic eDp5\r\nConnection: keep-alive\r\n\r\n",
                origin_reply=b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok",
            )
        )
        self.assertTrue(received.startswith(b"GET /page?q=1 HTTP/1.1\r\n"), received)
        self.assertIn(b"Host: allowed.test\r\n", received)
        self.assertIn(b"Connection: close\r\n", received)
        self.assertNotIn(b"Proxy-Authorization", received)
        self.assertNotIn(b"keep-alive", received)
        self.assertTrue(reply.endswith(b"ok"))

    def test_a_changed_dns_answer_cannot_redirect_the_connection(self):
        # Rebinding: the first answer is public, a later one loopback. The
        # proxy resolves once and dials the address it checked.
        self.answers["allowed.test"] = [["93.184.216.34"], ["127.0.0.1"]]
        asyncio.run(self._exchange(b"CONNECT allowed.test:443 HTTP/1.1\r\n\r\n"))
        self.assertEqual(["allowed.test"], self.resolved)
        self.assertEqual([("93.184.216.34", 443)], self.dialed)


class DnsRelayTests(unittest.TestCase):
    def test_aaaa_gets_an_empty_answer(self):
        query = dns_query("example.com", gateway.AAAA)
        reply = gateway.empty_answer(query, gateway.question_end(query))
        ident, flags, qd, an, ns, ar = struct.unpack_from("!HHHHHH", reply)
        self.assertEqual((0x1234, 1, 0, 0, 0), (ident, qd, an, ns, ar))
        self.assertTrue(flags & 0x8000)  # a response
        self.assertEqual(0, flags & 0x000F)  # NOERROR
        self.assertEqual(query[12:], reply[12:])

    def test_relay_forwards_a_and_answers_aaaa_locally(self):
        async def run():
            loop = asyncio.get_running_loop()
            upstream_seen = []

            class Upstream(asyncio.DatagramProtocol):
                def connection_made(self, transport):
                    self.transport = transport

                def datagram_received(self, data, addr):
                    upstream_seen.append(data)
                    self.transport.sendto(data[:2] + b"upstream-reply", addr)

            up, _ = await loop.create_datagram_endpoint(
                Upstream, local_addr=("127.0.0.1", 0)
            )
            relay, _ = await loop.create_datagram_endpoint(
                lambda: gateway.DnsRelay(up.get_extra_info("sockname")),
                local_addr=("127.0.0.1", 0),
            )
            address = relay.get_extra_info("sockname")
            replies = []
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
                client.setblocking(False)
                for qtype in (gateway.AAAA, 1):
                    await loop.sock_sendto(
                        client, dns_query("example.com", qtype), address
                    )
                    replies.append(
                        await asyncio.wait_for(loop.sock_recv(client, 4096), 3)
                    )
                await loop.sock_sendto(client, b"\x00\x01short", address)
                await asyncio.sleep(0.1)
            up.close()
            relay.close()
            return upstream_seen, replies

        upstream_seen, replies = asyncio.run(run())
        self.assertEqual(1, len(upstream_seen))  # only the A query left the relay
        self.assertEqual(0, struct.unpack_from("!H", replies[0], 6)[0])
        self.assertTrue(replies[1].endswith(b"upstream-reply"))


class ComposeContractTests(unittest.TestCase):
    def setUp(self):
        self.data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
        self.services = self.data["services"]

    def test_crawler_has_no_route_but_the_gateway(self):
        crawler = self.services["crawl4ai"]
        self.assertRegex(
            crawler["image"], r"^unclecode/crawl4ai:0\.9\.4@sha256:9021b3cb5c6f1257"
        )
        self.assertEqual(["crawl4ai_net", "crawl4ai_egress_net"], crawler["networks"])
        for name in crawler["networks"]:
            self.assertIs(True, self.data["networks"][name]["internal"], name)
        self.assertEqual([EGRESS_IP], crawler["dns"])
        self.assertEqual(
            f"http://{EGRESS_IP}:3128",
            crawler["environment"]["CRAWL4AI_UPSTREAM_PROXY"],
        )
        for absent in ("ports", "extra_hosts", "volumes"):
            self.assertNotIn(absent, crawler)
        self.assertEqual(["crawl4ai_api_token"], crawler["secrets"])
        self.assertEqual(
            "service_healthy", crawler["depends_on"]["crawl4ai-egress"]["condition"]
        )

    def test_gateway_is_unprivileged_and_the_only_bridge_to_outside(self):
        egress = self.services["crawl4ai-egress"]
        self.assertEqual(["crawl4ai"], egress["profiles"])
        self.assertEqual("template-infra-readonly-low", egress["extends"]["service"])
        self.assertEqual("65534:65534", egress["user"])
        self.assertEqual(
            ["./egress_gateway.py:/app/egress_gateway.py:ro"], egress["volumes"]
        )
        self.assertEqual(
            {
                "crawl4ai_egress_net": {"ipv4_address": EGRESS_IP},
                "crawl4ai_outbound_net": {},
            },
            egress["networks"],
        )
        self.assertNotIn("internal", self.data["networks"]["crawl4ai_outbound_net"])
        for absent in ("secrets", "ports", "environment"):
            self.assertNotIn(absent, egress)
        outside = [
            name
            for name, service in self.services.items()
            if "crawl4ai_outbound_net" in (service.get("networks") or {})
        ]
        self.assertEqual(["crawl4ai-egress"], outside)


if __name__ == "__main__":
    unittest.main()


IMAGE = "unclecode/crawl4ai@sha256:9021b3cb5c6f12570bbcd5395638495e0a06969b3148e377b953d174af2ebc9b"
PYTHON = "python:3.13.15-alpine"
PUBLIC_IP = "11.200.0.10"  # globally routable form, on an internal network only
FIXTURE = r"""
import http.server, sys
PAGES = {
    "/ok.html": (200, {}, b"<html><head><title>OK</title></head><body><p>public-ok</p>"
                 b"<img src='http://lan.fixture/pixel.png'></body></html>"),
    "/redirect-lan": (302, {"Location": "http://lan.fixture/secret"}, b""),
    "/redirect-meta": (302, {"Location": "http://169.254.169.254/latest/meta-data/"}, b""),
    "/loopback.html": (200, {}, b"<html><head><meta http-equiv='refresh' "
                       b"content='0;url=http://127.0.0.1:11235/health'></head><body>start</body></html>"),
    "/robots.txt": (200, {}, b"User-agent: *\nAllow: /\n"),
    "/secret": (200, {}, b"lan-secret"),
    "/pixel.png": (200, {}, b"lan-pixel"),
}
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("hit", self.path, flush=True)
        code, headers, body = PAGES.get(self.path, (404, {}, b"missing"))
        self.send_response(code)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass
http.server.ThreadingHTTPServer(("0.0.0.0", 80), Handler).serve_forever()
"""
PROBE = r"""
import json, os, urllib.error, urllib.request
TOKEN = os.environ["TOKEN"]
def call(path, body=None, token=True):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + TOKEN
    request = urllib.request.Request("http://crawl4ai:11235" + path, method="POST" if body else "GET",
                                     data=json.dumps(body).encode() if body else None, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", "replace")
def crawl(url, **extra):
    return call("/crawl", {"urls": [url], **extra})
cases = {
    "health": call("/health", token=False),
    "no-token": call("/crawl", {"urls": ["http://public.fixture/ok.html"]}, token=False),
    "allowed": crawl("http://public.fixture/ok.html",
                     crawler_config={"type": "CrawlerRunConfig", "params": {"check_robots_txt": True}}),
    "private": crawl("http://lan.fixture/secret"),
    "metadata": crawl("http://169.254.169.254/latest/meta-data/"),
    "redirect-lan": crawl("http://public.fixture/redirect-lan"),
    "redirect-meta": crawl("http://public.fixture/redirect-meta"),
    "loopback-refresh": crawl("http://public.fixture/loopback.html"),
    "caller-proxy": crawl("http://public.fixture/ok.html", browser_config={
        "type": "BrowserConfig", "params": {"proxy_config": {"server": "http://lan.fixture:80"}}}),
    "extra-args": crawl("http://public.fixture/ok.html", browser_config={
        "type": "BrowserConfig", "params": {"extra_args": ["--proxy-server=http://lan.fixture:80"]}}),
}
print(json.dumps({name: [status, body[:4000]] for name, (status, body) in cases.items()}))
"""
DIRECT = r"""
import json, socket
def attempt(command):
    try:
        with socket.create_connection(("10.250.201.2", 3128), 5) as s:
            s.sendall(command)
            return s.recv(200).split(b"\r\n")[0].decode()
    except OSError as error:
        return "error " + type(error).__name__
def direct(address):
    try:
        socket.create_connection((address, 80), 3).close()
        return "connected"
    except OSError as error:
        return "error " + type(error).__name__
print(json.dumps({
    "direct-public": direct("11.200.0.10"),
    "direct-gateway-lan": direct("10.250.202.10"),
    "gateway-public": attempt(b"CONNECT 11.200.0.10:80 HTTP/1.1\r\n\r\n"),
    "gateway-lan": attempt(b"CONNECT lan.fixture:80 HTTP/1.1\r\n\r\n"),
    "gateway-port": attempt(b"CONNECT 11.200.0.10:22 HTTP/1.1\r\n\r\n"),
}))
"""


def docker(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["docker", *args], capture_output=True, text=True, timeout=300, check=False
    )
    if check and result.returncode != 0:
        raise AssertionError(f"docker {args[0]} failed: {result.stderr.strip()[:300]}")
    return result.stdout


@unittest.skipUnless(
    os.environ.get("HYHOME_CRAWL4AI_REHEARSAL") == "1",
    "set HYHOME_CRAWL4AI_REHEARSAL=1 to run the disposable Crawl4AI egress rehearsal (needs Docker and the pinned image)",
)
class Crawl4AIEgressRehearsalTests(unittest.TestCase):
    """The real image behind the gateway, with every network internal and local."""

    @classmethod
    def setUpClass(cls):
        if not docker("image", "ls", "-q", IMAGE, check=False).strip():
            raise AssertionError(f"missing image {IMAGE}; pull it by digest first")
        run = f"c4a-rehearsal-{secrets.token_hex(3)}"
        cls.prefix, cls.names, cls.networks = run, [], []
        cls.tmp = tempfile.TemporaryDirectory(prefix=run)
        token = secrets.token_urlsafe(24)
        cls.token = token
        secret = pathlib.Path(cls.tmp.name) / "token"
        secret.write_text(token)
        secret.chmod(0o444)
        try:
            for name, subnet in (("api", None), ("egress", "10.250.201.0/29"),
                                 ("world", "11.200.0.0/24"), ("lan", "10.250.202.0/24")):  # fmt: skip
                docker("network", "create", "--internal", *(["--subnet", subnet] if subnet else []),
                       f"{run}-{name}")  # fmt: skip
                cls.networks.append(f"{run}-{name}")
            hardened = ["--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges:true",
                        "--user", "65534:65534"]  # fmt: skip
            for name, network, ip in (
                ("public", "world", PUBLIC_IP),
                ("lan", "lan", "10.250.202.10"),
            ):
                docker("run", "-d", "--name", f"{run}-{name}", *hardened, "--network", f"{run}-{network}",
                       "--ip", ip, "--network-alias", f"{name}.fixture",
                       "--sysctl", "net.ipv4.ip_unprivileged_port_start=80",
                       PYTHON, "python", "-c", FIXTURE)  # fmt: skip
                cls.names.append(f"{run}-{name}")
            gateway_source = ROOT / "infra/08-ai/crawl4ai/egress_gateway.py"
            docker("create", "--name", f"{run}-egress", *hardened, "--network", f"{run}-egress",
                   "--ip", "10.250.201.2", "--sysctl", "net.ipv4.ip_unprivileged_port_start=53",
                   "-v", f"{gateway_source}:/app/egress_gateway.py:ro",
                   PYTHON, "python", "/app/egress_gateway.py")  # fmt: skip
            cls.names.append(f"{run}-egress")
            for network in ("world", "lan"):
                docker("network", "connect", f"{run}-{network}", f"{run}-egress")
            docker("start", f"{run}-egress")
            crawler = COMPOSE_SERVICES()["crawl4ai"]
            tmpfs = [arg for mount in crawler["tmpfs"] for arg in ("--tmpfs", mount)]
            docker("create", "--name", f"{run}-crawl4ai", "--network", f"{run}-api",
                   "--network-alias", "crawl4ai", "--user", crawler["user"], "--read-only", *tmpfs,
                   "--cap-drop", "ALL", "--security-opt", "no-new-privileges:true",
                   "--memory", "4g", "--pids-limit", "512", "--shm-size", "1g",
                   "--dns", "10.250.201.2", "-e", "CRAWL4AI_UPSTREAM_PROXY=http://10.250.201.2:3128",
                   "-v", f"{secret}:/run/secrets/crawl4ai_api_token:ro",
                   IMAGE, *(part.replace("$$", "$") for part in crawler["command"]))  # fmt: skip
            cls.names.append(f"{run}-crawl4ai")
            docker(
                "network",
                "connect",
                "--ip",
                "10.250.201.3",
                f"{run}-egress",
                f"{run}-crawl4ai",
            )
            docker("start", f"{run}-crawl4ai")
            deadline = time.monotonic() + 180
            while docker("exec", f"{run}-crawl4ai", "curl", "-fsS", "http://127.0.0.1:11235/health",
                         check=False).find("ok") < 0:  # fmt: skip
                if time.monotonic() > deadline:
                    tail = subprocess.run(
                        ["docker", "logs", "--tail", "25", f"{run}-crawl4ai"],
                        capture_output=True,
                        text=True,
                        check=False,
                    ).stderr
                    raise AssertionError(f"crawl4ai did not become healthy:\n{tail}")
                time.sleep(3)
            probe = docker("run", "--rm", "--network", f"{run}-api", "-e", f"TOKEN={token}",
                           *hardened, PYTHON, "python", "-c", PROBE)  # fmt: skip
            cls.cases = json.loads(probe)
            cls.direct = json.loads(
                docker("exec", f"{run}-crawl4ai", "python3", "-c", DIRECT)
            )
            cls.lan_hits = docker("logs", f"{run}-lan")
            cls.gateway_log = docker("logs", f"{run}-egress")
            cls.inspect = json.loads(docker("inspect", f"{run}-crawl4ai"))[0]
            # A safe summary for the Task: statuses and whether a marker leaked.
            print(
                json.dumps(
                    {
                        name: [status, "public-ok" in body, "lan-secret" in body]
                        for name, (status, body) in cls.cases.items()
                    }
                ),
                file=sys.stderr,
            )
            print(json.dumps(cls.direct), file=sys.stderr)
        except BaseException:
            cls.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        for name in getattr(cls, "names", []):
            docker("rm", "-f", "-v", name, check=False)
        for network in getattr(cls, "networks", []):
            docker("network", "rm", network, check=False)
        if getattr(cls, "tmp", None):
            cls.tmp.cleanup()

    def result(self, name):
        status, body = self.cases[name]
        return status, body

    def test_token_guards_everything_but_health(self):
        self.assertEqual(200, self.result("health")[0])
        self.assertEqual(401, self.result("no-token")[0])

    def test_an_allowed_page_is_fetched_through_the_gateway(self):
        status, body = self.result("allowed")
        self.assertEqual(200, status, body[:300])
        self.assertIn("public-ok", body)
        # The in-image broker sends the address it pinned, not the name.
        self.assertIn(
            f"egress allowed GET {PUBLIC_IP} {PUBLIC_IP}:80", self.gateway_log
        )

    def test_private_metadata_and_redirect_targets_are_refused(self):
        for name in (
            "private",
            "metadata",
            "redirect-lan",
            "redirect-meta",
            "loopback-refresh",
        ):
            with self.subTest(name):
                _, body = self.result(name)
                self.assertNotIn("lan-secret", body)
                self.assertNotIn('"status":"ok"', body.replace(" ", ""))
        self.assertNotIn("hit /secret", self.lan_hits)
        self.assertNotIn("hit /pixel.png", self.lan_hits)  # the private subresource

    def test_caller_proxy_and_browser_arguments_are_refused(self):
        for name in ("caller-proxy", "extra-args"):
            with self.subTest(name):
                status, body = self.result(name)
                self.assertNotEqual(200, status, body[:300])
        self.assertEqual("", self.lan_hits.strip())

    def test_the_crawler_has_no_route_except_the_gateway(self):
        self.assertTrue(self.direct["direct-public"].startswith("error"), self.direct)
        self.assertTrue(
            self.direct["direct-gateway-lan"].startswith("error"), self.direct
        )
        self.assertIn(" 200 ", self.direct["gateway-public"])
        self.assertIn(" 403 ", self.direct["gateway-lan"])
        self.assertIn(" 403 ", self.direct["gateway-port"])

    def test_resource_limits_hold(self):
        host = self.inspect["HostConfig"]
        self.assertEqual(4 * 1024**3, host["Memory"])
        self.assertEqual(512, host["PidsLimit"])
        self.assertEqual(1024**3, host["ShmSize"])
        self.assertIs(True, host["ReadonlyRootfs"])
        self.assertEqual(["ALL"], host["CapDrop"])
        self.assertEqual("appuser", self.inspect["Config"]["User"])


def COMPOSE_SERVICES():
    return yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))["services"]
