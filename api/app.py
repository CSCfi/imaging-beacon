import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

application = Flask(__name__)
application.config["MONGO_URI"] = ("mongodb://"
    + os.environ["MONGO_INITDB_ROOT_USERNAME"]
    + ":"
    + os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    + "@"
    + "localhost"
    + ":27017/"
    + "beacondb?authSource=admin")

mongo = PyMongo(application)
db = mongo.db


@application.route("/")
@application.route("/service-info")
def index():
    """Display beacon info."""
    beacon_info = {
        "id": ".".join(reversed(request.host.split("."))),
        "name": "Imaging beacon",
        "type": "",
        "description": "",
        "organization": {
            "name": "",
            "url": "",
        },
        "contactUrl": "",
        "documentationUrl": "",
        "createdAt": "",
        "updatedAt": "",
        "environment": "",
        "version": "",
    }
    return jsonify(beacon_info)


@application.route("/db")
def getItem():
    """List all db items."""
    dbImages = db.images.find()
    dbDataset = db.dataset.find()
    dbSamples = db.sample.find()

    datasets = []
    for set in dbDataset:
        setdata = {"id": str(set["_id"]), "alias": set["alias"], "attributes": set["attributes"], "title": set["title"], "description": set["description"], "datasetType": set["datasetType"], "policyRef": set["policyRef"], "imageRef": ["imageRef"]}
        datasets.append(setdata)

    images = []
    
    for i in dbImages:
        image = {"id": str(i["_id"]), "alias": i["alias"], "attributes": i["attributes"], "studyRef": i["studyRef"], "imageOf": i["imageOf"], "imageType": i["imageType"], "files": i["files"]}
        images.append(image)

    samples = []
    
    for sample in dbSamples:
        sampleData = {"id": str(sample["_id"]), "biologicalBeing": sample["biologicalBeing"], "specimen": sample["specimen"], "block": sample["block"], "slide": sample["slide"]}
        samples.append(sampleData)

    data = [] 
    data.append({"datasets": datasets})   
    data.append({"images": images})
    data.append({"samples": samples})


    return jsonify(status=True, data=data)


@application.route("/query", methods=["POST"])
def searchQueary():
    """Search query."""
    return jsonify(), 201


if __name__ == "__main__":
    application.config.from_prefixed_env()
    application.config["APP_PORT"]
    application.config["APP_DEBUG"]
    application.run()
