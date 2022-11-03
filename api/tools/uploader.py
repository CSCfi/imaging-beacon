import pymongo
import json
import sys
import os

from ..config import DB

mongo_uri = f"mongodb://{DB['username']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['name']}?authSource={DB['auth']}"
client =  pymongo.MongoClient(mongo_uri)
db = client[DB["name"]]


def populate():
    """Populate database function."""
    if sys.argv[2] != "":
        collection = db[sys.argv[2]]
    else:
        collection = db["dataset"]
    with open(sys.argv[1]) as file:
        file_data = json.load(file)

        if isinstance(file_data, list):
            collection.insert_many(file_data)
        else:
            collection.insert_one(file_data)


if __name__ == "__main__":
    populate()
