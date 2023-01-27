"""DB Service that handles MongoDB database connections."""
from typing import Dict, List

from motor.motor_asyncio import AsyncIOMotorClient


class DBService:
    """Create service used for database communication."""

    def __init__(self, database_name: str, db_client: AsyncIOMotorClient) -> None:
        """Create service for given database.
        
        Service will have read-write access to given database. Database will be
        created during first read-write operation if not already present.
        
        :param database_name: Name of database to be used
        """
        self.db_client = db_client
        self.database = db_client[database_name]

    def query(self, collection: str, query: Dict, custom_projection: Dict = {}) -> List:
        """Query database with given query.
        
        :param collection: Collection where document should be searched from
        :param query: query to be used
        :param custom_projection: overwrites default projection
        :returns: query result list
        """
        # LOG.debug(f"DB doc query performed in {collection}.")
        projection = {"_id": False}
        if custom_projection:
            projection = custom_projection
        query = self.database[collection].find(query, projection)
        return query

    async def do_aggregate(self, collection: str, query: List) -> List:
        """Peform aggregate query.
        
        :param collection: Collection where document should be searched from
        :param query: query to be used
        :returns: aggregated query result list
        """
        # LOG.debug(f"DB aggregate performed in {collection}.")
        aggregate = self.database[collection].aggregate(query)
        return [doc async for doc in aggregate]