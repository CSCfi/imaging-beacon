from aiohttp import web
import os
import sys
import aiohttp_cors
import pymongo
import json
import bson.json_util as json_util
import uvloop
import asyncio
import ujson
from .database.services import index, getSearchTerms, searchQuery

routes = web.RouteTableDef()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
db =  pymongo.MongoClient(
    "mongodb://"
    + os.environ["DB_USERNAME"]
    + ":"
    + os.environ["DB_PASSWORD"]
    + "@"
    + os.environ["DB_HOST"]
    + ":27017/"
    + os.environ["DB_NAME"]
    )
@routes.get("/")  # For Beacon API Specification
@routes.get("/service-info") 
async def beacon_get(request: web.Request) -> web.Response:
    """Return service info."""
    response = await index(request.host)
    return web.json_response(response)


@routes.get("/getSearchTerms")
async def returnearchTerms(request: web.Request) -> web.Response:
    """Return db search terms."""
    response = getSearchTerms(db)
    return web.json_response(response, content_type="application/json", dumps=ujson.dumps)


@routes.post("/query")
async def query(request: web.Request) -> web.Response:
    """Search query."""
    result = await searchQuery(request, db)
    if result == "No results found.":
        return web.json_response(result, content_type="application/json", dumps=ujson.dumps)
    return web.json_response(result, content_type="application/json", dumps=ujson.dumps)

def set_cors(server):
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

async def destroy(app: web.Application) -> None:
    """Upon server close, close the DB connection pool."""
    # will defer this to asyncpg
    await app["pool"].close()  # pragma: no cover

async def initialize(app: web.Application) -> None:
    """Spin up DB a connection pool with the HTTP server."""
    
    app["pool"] 
    
    set_cors(app)

async def init() -> web.Application:
    """Initialise server."""
    beacon = web.Application()
    beacon.router.add_routes(routes)
    return beacon

def main():
    """Run the beacon API.
    At start also initialize a PostgreSQL connection pool.
    """
    # TO DO make it HTTPS and request certificate
    # sslcontext.load_cert_chain(ssl_certfile, ssl_keyfile)
    # sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # sslcontext.check_hostname = False
    app = init()
   
    web.run_app(
        app,
        host=os.environ.get("HOST", "0.0.0.0"),  # nosec
        port=os.environ.get("PORT", "8080"),
        shutdown_timeout=0,
        ssl_context=None,
    )


if __name__ == "__main__":
    if sys.version_info < (3, 8):
        LOG.error("beacon-python requires python 3.8")
        sys.exit(1)
    main()

