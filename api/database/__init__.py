"""Database initialisation and services."""
from ..config import DB

from motor.motor_asyncio import AsyncIOMotorClient

def create_db_client() -> AsyncIOMotorClient:
    """Initialize database client for AioHTTP App.

    :returns: Coroutine-based Motor client for Mongo operations
    """
    # LOG.debug("initialised DB client")
    return AsyncIOMotorClient(DB["uri"], connectTimeoutMS=15000, serverSelectionTimeoutMS=15000)
