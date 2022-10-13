import pymongo
import json
import sys
import os

client = pymongo.MongoClient(
    "mongodb://"
    + os.environ["DB_USERNAME"]
    + ":"
    + os.environ["DB_PASSWORD"]
    + "@"
    + os.environ["DB_HOST"]
    + ":27017/"
    + os.environ["DB_NAME"]+ "?authSource=admin"
)

db = client[os.environ["DB_NAME"]]


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
