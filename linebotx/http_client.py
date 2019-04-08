import asyncio

import aiohttp

from linebot.http_client import HttpClient, HttpResponse


class AioHttpClient(HttpClient):
    """HttpClient implemented by aiohttp."""

    DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=30)

    def __init__(self, timeout=DEFAULT_TIMEOUT, loop=None):
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.session = aiohttp.ClientSession(loop=loop)
        self.timeout = timeout

    async def get(self, url, headers=None, params=None, stream=False, timeout=None):
        if timeout is None:
            timeout = self.timeout

        async with self.session.get(
            url, headers=headers, params=params, stream=stream, timeout=timeout
        ) as response:
            return AioHttpResponse(response)

    async def post(self, url, headers=None, data=None, timeout=None):
        if timeout is None:
            timeout = self.timeout

        async with self.session.post(url, headers=headers, data=data) as response:
            return AioHttpResponse(response)

    async def delete(self, url, headers=None, data=None, timeout=None):
        if timeout is None:
            timeout = self.timeout

        response = await self.session.delete(
            url, headers=headers, data=data, timeout=timeout
        )

        return AioHttpResponse(response)

    async def close(self):
        await self.session.close()


class AioHttpResponse(HttpResponse):
    """HttpResponse implemented by aiohttp lib's response."""

    def __init__(self, response):
        self.response = response

    @property
    def status_code(self):
        return self.response.status

    @property
    def headers(self):
        return self.response.headers

    @property
    async def text(self):
        return await self.response.text()

    @property
    async def content(self):
        return await self.response.read()

    @property
    async def json(self):
        return await self.response.json()

    def iter_content(self, chunk_size=1024):
        return self.response.content.iter_chunked(chunk_size)
