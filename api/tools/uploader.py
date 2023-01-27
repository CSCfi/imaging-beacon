"""Database uploader tool."""
import json
import sys
from os import getenv
from typing import Dict

from motor.motor_asyncio import AsyncIOMotorClient


DB: Dict = {
    "host": getenv("DB_HOST", "localhost"),
    "port": getenv("DB_PORT", 27017),
    "name": getenv("DB_NAME", "beacon"),
    "auth": getenv("DB_AUTH", "admin"),
    "username": getenv("DB_USERNAME", "username"),
    "password": getenv("DB_PASSWORD", "password"),
}
DB["uri"] = f"mongodb://{DB['username']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['name']}?authSource={DB['auth']}"

db_client = AsyncIOMotorClient(DB["uri"], connectTimeoutMS=15000, serverSelectionTimeoutMS=15000)
db_name = DB["name"]
db_service = db_client[db_name]

def populate():
    """Populate database function."""
    if sys.argv[2] != "":
        collection = db_service[sys.argv[2]]
    else:
        collection = db_service["dataset"]
    with open(sys.argv[1]) as file:
        file_data = json.load(file)

        if isinstance(file_data, list):
            collection.insert_many(file_data)
        else:
            collection.insert_one(file_data)


if __name__ == "__main__":
    populate()
