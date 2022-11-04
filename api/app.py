"""Web app."""
from aiohttp import web
import aiohttp_cors
import uvloop
import asyncio
import ujson

from .config import APP, DB
from .database import create_db_client
from .endpoints.info import service_info, get_search_terms
from .endpoints.query import search_query

routes = web.RouteTableDef()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@routes.get("/")
@routes.get("/service-info")
async def beacon_get(request: web.Request) -> web.Response:
    """Return service info."""
    response = await service_info(request)
    return web.json_response(response)


@routes.get("/getSearchTerms")
async def returnearchTerms(request: web.Request) -> web.Response:
    """Return db search terms."""
    response = get_search_terms(request)
    return web.json_response(
        response,
        content_type="application/json",
        dumps=ujson.dumps,
    )


@routes.post("/query")
async def query(request: web.Request) -> web.Response:
    """Search query."""
    result = await search_query(request)
    return web.json_response(
        result,
        content_type="application/json",
        dumps=ujson.dumps,
    )


def set_cors(server: web.Application) -> None:
    """Set CORS rules."""
    # Configure CORS settings
    cors = aiohttp_cors.setup(
        server,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods=["GET", "POST", "OPTIONS"],
                max_age=86400,
            )
        },
    )
    # Apply CORS to endpoints
    for route in list(server.router.routes()):
        cors.add(route)


async def init() -> web.Application:
    """Initialise server."""
    app = web.Application()
    app.router.add_routes(routes)
    if APP["cors"]:
        set_cors(app)

    client = create_db_client(DB["uri"])
    app["db"] = client[DB["name"]]

    return app


def main():
    """Start web application as a python process.

    For development purposes only, for production use gunicorn instead.
    """
    # TO DO make it HTTPS and request certificate
    # sslcontext.load_cert_chain(ssl_certfile, ssl_keyfile)
    # sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # sslcontext.check_hostname = False
    app = init()

    web.run_app(
        app,
        host=APP["host"],
        port=APP["port"],
        shutdown_timeout=0,
        ssl_context=None,
    )


if __name__ == "__main__":
    main()
