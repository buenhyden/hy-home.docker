"""Crawl4AI egress gateway (SPEC-0220): DNS relay and forward proxy.

crawl4ai joins internal networks only, so this container is its only way out.

DNS: UDP queries are relayed to Docker's resolver; AAAA queries get an empty
answer so the crawler only ever pins IPv4.
Proxy: CONNECT host:port and absolute-form http:// requests. The target is
resolved here, every answer must be a globally routable IPv4 address and the
port 80 or 443, and the connection goes to the address that was checked, so a
second DNS answer cannot change the destination.
"""

from __future__ import annotations

import asyncio
import ipaddress
import socket
import struct
import sys
from collections.abc import Awaitable, Callable

PORTS = frozenset({80, 443})
PROXY_PORT = 3128
DNS_PORT = 53
DOCKER_DNS = ("127.0.0.11", 53)
MAX_HEAD = 64 * 1024
IDLE_SECONDS = 120
MAX_CONNECTIONS = 128
AAAA = 28

Resolver = Callable[[str, int], Awaitable[list[str]]]
Dialer = Callable[
    [str, int], Awaitable[tuple[asyncio.StreamReader, asyncio.StreamWriter]]
]


class Refused(Exception):
    """The destination is not allowed; the reason is logged, never returned."""


def allowed_address(text: str) -> bool:
    """Only globally routable unicast IPv4; every IPv6 form is refused."""
    try:
        address = ipaddress.ip_address(text)
    except ValueError:
        return False
    return (
        address.version == 4
        and address.is_global
        and not (address.is_multicast or address.is_reserved or address.is_unspecified)
    )


async def system_resolve(host: str, port: int) -> list[str]:
    infos = await asyncio.get_running_loop().getaddrinfo(
        host, port, family=socket.AF_INET, type=socket.SOCK_STREAM
    )
    return [info[4][0] for info in infos]


async def system_dial(ip: str, port: int):
    return await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=30)


async def pin(host: str, port: int, resolve: Resolver) -> str:
    """The one address to dial, after every answer passed the rule."""
    if port not in PORTS or not host:
        raise Refused(f"port {port}")
    try:
        answers = [str(ipaddress.ip_address(host.strip("[]")))]
    except ValueError:
        try:
            answers = await resolve(host, port)
        except OSError as exc:
            raise Refused(f"resolve {host}") from exc
    if not answers or not all(allowed_address(answer) for answer in answers):
        raise Refused(f"address {host}")
    return answers[0]


def split_authority(authority: str, default: int) -> tuple[str, int]:
    host, sep, port = authority.rpartition(":")
    if not sep or "]" in port:
        return authority, default
    if not port.isdigit():
        raise Refused("port")
    return host, int(port)


class Proxy:
    def __init__(self, resolve: Resolver = system_resolve, dial: Dialer = system_dial):
        self.resolve = resolve
        self.dial = dial
        self.slots = asyncio.Semaphore(MAX_CONNECTIONS)

    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        if self.slots.locked():
            await self._reply(writer, b"503 Busy")
            writer.close()
            return
        async with self.slots:
            try:
                await self._serve(reader, writer)
            except Refused as exc:
                log("refused", exc)
                await self._reply(writer, b"403 Forbidden")
            except (
                ValueError,
                UnicodeError,
                asyncio.IncompleteReadError,
                asyncio.LimitOverrunError,
            ):
                await self._reply(writer, b"400 Bad Request")
            except (TimeoutError, OSError):
                await self._reply(writer, b"502 Bad Gateway")
            finally:
                writer.close()

    async def _serve(self, reader, writer):
        head = await asyncio.wait_for(
            reader.readuntil(b"\r\n\r\n"), timeout=IDLE_SECONDS
        )
        line, _, rest = head.decode("latin-1").partition("\r\n")
        method, target, version = line.split(" ")
        if not version.startswith("HTTP/1."):
            raise ValueError("version")
        if method == "CONNECT":
            host, port = split_authority(target, 443)
            ip = await pin(host, port, self.resolve)
            up_reader, up_writer = await self.dial(ip, port)
            log("allowed", f"CONNECT {host} {ip}:{port}")
            writer.write(b"HTTP/1.1 200 Connection established\r\n\r\n")
        else:
            if not target.startswith("http://"):
                raise Refused("scheme")
            authority, _, path = target[len("http://") :].partition("/")
            host, port = split_authority(authority, 80)
            ip = await pin(host, port, self.resolve)
            headers = [
                header
                for header in rest.split("\r\n")
                if header
                and not header.lower().startswith(
                    ("proxy-", "connection:", "keep-alive:")
                )
            ]
            if not any(header.lower().startswith("host:") for header in headers):
                headers.append(f"Host: {authority}")
            up_reader, up_writer = await self.dial(ip, port)
            log("allowed", f"{method} {host} {ip}:{port}")
            # One request per connection, so a reused client connection cannot
            # carry an unchecked second request.
            request = f"{method} /{path} {version}\r\n"
            request += "".join(f"{header}\r\n" for header in headers)
            up_writer.write((request + "Connection: close\r\n\r\n").encode("latin-1"))
        await asyncio.gather(_pump(reader, up_writer), _pump(up_reader, writer))

    @staticmethod
    async def _reply(writer, status: bytes):
        try:
            writer.write(
                b"HTTP/1.1 " + status + b"\r\nContent-Length: 0\r\n"
                b"Connection: close\r\n\r\n"
            )
            await writer.drain()
        except OSError:
            pass


async def _pump(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while chunk := await asyncio.wait_for(reader.read(65536), timeout=IDLE_SECONDS):
            writer.write(chunk)
            await writer.drain()
    except (TimeoutError, OSError):
        pass
    finally:
        writer.close()


def question_end(query: bytes) -> int | None:
    """Offset just past the first question's QTYPE and QCLASS, or None."""
    offset = 12
    while offset < len(query):
        length = query[offset]
        if length == 0:
            end = offset + 5
            return end if end <= len(query) else None
        if length & 0xC0:
            return None
        offset += length + 1
    return None


def empty_answer(query: bytes, end: int) -> bytes:
    """NOERROR with no records, echoing the query's id, flags and question."""
    flags = 0x8080 | (struct.unpack_from("!H", query, 2)[0] & 0x7900)
    return query[:2] + struct.pack("!HHHHH", flags, 1, 0, 0, 0) + query[12:end]


class DnsRelay(asyncio.DatagramProtocol):
    def __init__(self, upstream=DOCKER_DNS):
        self.upstream = upstream

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        end = question_end(data) if len(data) > 12 else None
        if end is None:
            return
        if struct.unpack_from("!H", data, end - 4)[0] == AAAA:
            self.transport.sendto(empty_answer(data, end), addr)
            return
        asyncio.get_running_loop().create_task(self._forward(data, addr))

    async def _forward(self, data, addr):
        loop = asyncio.get_running_loop()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as upstream:
            upstream.setblocking(False)
            try:
                await loop.sock_sendto(upstream, data, self.upstream)
                reply = await asyncio.wait_for(
                    loop.sock_recv(upstream, 4096), timeout=3
                )
            except (TimeoutError, OSError):
                return
        self.transport.sendto(reply, addr)


def log(decision: str, detail: object) -> None:
    # Host and address only: paths and queries can carry tokens.
    print(f"egress {decision} {detail}", file=sys.stdout, flush=True)


async def main() -> None:
    loop = asyncio.get_running_loop()
    # ponytail: UDP only; a truncated answer that needs TCP fails closed.
    await loop.create_datagram_endpoint(DnsRelay, local_addr=("0.0.0.0", DNS_PORT))
    server = await asyncio.start_server(
        Proxy().handle, "0.0.0.0", PROXY_PORT, limit=MAX_HEAD
    )
    log("listening", f"proxy :{PROXY_PORT} dns :{DNS_PORT}/udp")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
