import pymongo
import json
import sys
import os

client = pymongo.MongoClient(
    "mongodb://"
    + os.environ["MONGO_INITDB_ROOT_USERNAME"]
    + ":"
    + os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    + "@"
    + "localhost"
    + ":27017/"
    + "mongodb?authSource=admin"
)

db = client["beacondb"]


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
