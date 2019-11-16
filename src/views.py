from typing import Dict, Callable

from aiohttp import web

from store import overrides_storage, requests_storage


async def add_override(request):
    data = await request.json()

    await overrides_storage.add(**data)

    return web.json_response('OK')


async def remove_override(request):
    data = await request.json()

    await overrides_storage.remove(**data)

    return web.json_response('OK')


async def get_requests(request):
    requests = [item.as_dict for item in requests_storage]

    return web.json_response(requests)


def get_handler(resource: Dict, response: Dict) -> Callable:
    async def handler(request):

        params = {
            **request.match_info,
            **request.query,
        }

        override = await overrides_storage.get(request.host, resource['name'], response['method'])
        if override:
            content = override.content.format(**params)
            status = override.status
        else:
            content = response['content'].format(**params)
            status = response['status']

        await requests_storage.add(
            domain=request.host,
            resource=resource['name'],
            method=response['method'],
            path=request.path,
            payload=await request.text(),
            request_headers=request.headers,
            request_params=request.query,
            response=content,
            status=status,
        )

        return web.Response(text=content, status=status)

    return handler
