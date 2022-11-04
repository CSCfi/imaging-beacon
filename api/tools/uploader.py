"""Database uploader tool."""
import pymongo
import json
import sys

from ..config import DB

client = pymongo.MongoClient(DB["uri"])
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
