"""Crawl4AI egress gateway and network contract (SPEC-0220)."""

from __future__ import annotations

import asyncio
import importlib.util
import pathlib
import socket
import struct
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
