"""Forward the host-loopback listener to the Crawl4AI API and nothing else (POL-0091)."""

import asyncio

UPSTREAM = ("crawl4ai", 11235)


async def pipe(reader, writer):
    try:
        while data := await reader.read(65536):
            writer.write(data)
            await writer.drain()
    finally:
        writer.close()


async def handle(reader, writer):
    try:
        up_reader, up_writer = await asyncio.open_connection(*UPSTREAM)
    except OSError:
        writer.close()
        return
    await asyncio.gather(
        pipe(reader, up_writer), pipe(up_reader, writer), return_exceptions=True
    )


async def main():
    server = await asyncio.start_server(handle, "0.0.0.0", 11235)
    async with server:
        await server.serve_forever()


asyncio.run(main())
