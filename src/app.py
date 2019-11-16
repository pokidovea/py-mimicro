import argparse

import yaml
from aiohttp import web

from routes import setup_service_routes, setup_dynamic_routes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start MOCK server')
    parser.add_argument('-c', '--config', dest='config', required=True, help='path to config')
    parser.add_argument('--host', dest='host', type=str, default='localhost', help='server host')
    parser.add_argument('-p', '--port', dest='port', type=int, default=8080, help='server port')

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    app = web.Application()

    setup_service_routes(app)
    setup_dynamic_routes(app, config)

    web.run_app(app, host=args.host, port=args.port)
