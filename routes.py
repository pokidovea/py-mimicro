from typing import Dict

from aiohttp import web

from views import add_override, list_requests, get_handler


def setup_service_routes(app: web.Application):
    app.router.add_post('/__service/override', add_override)
    app.router.add_get('/__service/list-requests', list_requests)


def setup_dynamic_routes(app: web.Application, config: Dict):
    for domain_settings in config:
        domain_app = web.Application()

        for resource in domain_settings['resources']:
            for response in resource['responses']:
                domain_app.router.add_route(
                    response['method'], resource['path'], get_handler(resource, response)
                )

        app.add_domain(domain_settings['domain'], domain_app)
