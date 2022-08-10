import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json

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
    dbSamples = list(db.sample.find())
    for coll in db.list_collection_names():
        print(coll)
    datasets = []
    for set in dbDataset:
        setdata = {"id": str(set["_id"]), "alias": set["alias"], "attributes": set["attributes"], "title": set["title"], "description": set["description"], "datasetType": set["datasetType"], "policyRef": set["policyRef"], "imageRef": ["imageRef"]}
        datasets.append(setdata)

    images = []
    
    for i in dbImages:
        image = {"id": str(i["_id"]), "alias": i["alias"], "attributes": i["attributes"], "studyRef": i["studyRef"], "imageOf": i["imageOf"], "imageType": i["imageType"], "files": i["files"]}
        images.append(image)

    samples = []
    print()
    for sample in dbSamples:
        samples.append(json.loads(json.dumps(sample, default=str)))
        
    data = [] 
    data.append({"datasets": datasets})   
    data.append({"images": images})
    data.append({"samples": samples})
    return jsonify(status=True, data=data)

@application.route("/getSearchTerms")
def getSearchTerms():
    searchTerms = []
    anatomicalSite = []
    biologicalBeing = []
    anatomicalSite.append(list(db.sample.find({"specimen.attributes.attribute.tag": "anatomical_site"},{"specimen.attributes.attribute": 1, "_id": 0})))
    biologicalBeing.append(list(db.sample.find({"biologicalBeing.attributes.attribute.tag": "animal_species"}, {"biologicalBeing": 1, "_id": 0})))
    searchTerms.append({"anatomicalSite": anatomicalSite})
    searchTerms.append({"biologicalBeing": biologicalBeing})
    return jsonify(results=searchTerms), 201

@application.route("/query", methods=["POST"])
def searchQueary():

    """Search query."""
    # Get sample info  
    dbSamples = getSamples(request)
    if not dbSamples:
        return jsonify(error="No results found.")
    images = getImages(dbSamples)
    return jsonify(results=str(images)), 201

def getSamples(request):
    dbSamples = []
    requestBiological = request.get_json().get('biologicalBeing')
    requestAnatomical = request.get_json().get('anatomicalSite')
    requestSex = request.get_json().get('sex')
    requestAge = request.get_json().get('age')
    if(request.get_json().get("ageCondition") == "<"):
        # Age less than
        dbSamples.append(list(db.sample.find({'specimen.attributes.attribute': {"$elemMatch": 
        { "tag": "age_at_extraction", "value": { "$lt": requestAge}, "tag": "anatomical_site", "value": requestAnatomical}}})))

    elif(request.get_json().get("ageCondition") == ">"):
        # Age more than
        dbSamples.append(list(db.sample.find({'specimen.attributes.attribute': {"$elemMatch": 
        { "tag": "age_at_extraction", "value": { "$gt": requestAge}, "tag": "anatomical_site", "value": requestAnatomical}}})))
    elif(request.get_json().get("ageCondition") == "-"):
        # Ages between       
        dbSamples.append(list(db.sample.find({'specimen.attributes.attribute': {"$elemMatch": 
        { "tag": "age_at_extraction", "value": { "$gte": request.form.get('ageStart'), "$lt": request.form.get('ageEnd')},
         "tag": "anatomical_site", "value": requestAnatomical}}})))
    else:
        # No age
        dbSamples.append(list(db.sample.find({"biologicalBeing.alias": requestBiological, 'biologicalBeing.attributes.attribute.value': requestSex})))
        dbSamples.append(list(db.sample.find({"specimen.attributes.attribute.value": requestAnatomical})))

    return dbSamples
def getImages(dbSamples):
    images= []
    for sample in dbSamples:
        keys = sample[0].keys()
        for key in keys:
            if(key == "biologicalBeing"):
                images.append(getImageByBiologicalBeing(sample[0].get("biologicalBeing")))
            elif (key == "specimen"):
                images.append(getImageBySpecimen(sample[0].get("specimen")))
    return images

def getImageByBiologicalBeing(biologicalBeing):

    specimenOfBiologicalBeing = list(db.sample.find({"specimen.extractedFrom.refname": biologicalBeing.get("alias")}))

    blockOfSpecimen =  list(db.sample.find({'block.sampledFrom.refname': specimenOfBiologicalBeing[0].get("specimen").get("alias")}))

    slideOfBlock = list(db.sample.find({'slide.createdFrom.refname': blockOfSpecimen[0].get("block").get("alias")}))

    return list(db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")}))

def getImageBySpecimen(specimen):
    blockOfSpecimen =  list(db.sample.find({'block.sampledFrom.refname': specimen.get("alias")}))

    slideOfBlock = list(db.sample.find({'slide.createdFrom.refname': blockOfSpecimen[0].get("block").get("alias")}))

    return list(db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")}))

    
if __name__ == "__main__":
    application.config.from_prefixed_env()
    application.config["APP_PORT"]
    application.config["APP_DEBUG"]
    application.run()
