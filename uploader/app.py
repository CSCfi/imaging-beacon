import pymongo
import json
import sys



client = pymongo.MongoClient("mongodb://"
    + "test"
    + ":"
    + "test"
    + "@"
    + "localhost"
    + ":27017/"
    + "mongodb?authSource=admin")

db = client["beacondb"]
collection = db["imagedb"]

def populate():
   with open(sys.argv[1]) as file:
    file_data = json.load(file)

    if isinstance(file_data, list):
        collection.insert_many(file_data) 
    else:
        collection.insert_one(file_data)


if __name__ == '__main__':
    populate()
