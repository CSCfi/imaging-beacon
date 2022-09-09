import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json

def index():
    """Display beacon info."""
    beacon_info = {
        "id": ".".join(reversed(request.host.split("."))),
        "name": "Imaging beacon",
        "type": {'group': "test",
                    'artifact': "beacon",
                    'version': "0.0.0"},
        "description": "bp test beacon",
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
    return beacon_info

def getItems(db):
    """List all db items."""
    dbImages = db.images.find()
    dbDataset = db.dataset.find()
    dbSamples = list(db.sample.find())
    datasets = []
    for ds in dbDataset:
        setdata = {"id": str(ds["_id"]), "alias": ds["alias"], "attributes": ds["attributes"], "title": ds["title"], "description": ds["description"], "datasetType": ds["datasetType"], "policyRef": ds["policyRef"], "imageRef": ["imageRef"]}
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
    return data

def getSearchTerms(db):
    """Gets all search terms"""
    searchTerms = []
    searchTerms.append({"anatomicalSite": list(db.sample.find({"specimen.attributes.attribute.tag": "anatomical_site"},{"specimen.attributes.attribute": 1, "_id": 0}))})
    searchTerms.append({"biologicalBeing": list(db.sample.find({"biologicalBeing.attributes.attribute.tag": "animal_species"}, {"biologicalBeing": 1, "_id": 0}))})
    return searchTerms

def searchQuery(request, db):
    """Search query."""
    # Get sample info  
    dbSamples = getSamples(request, db)
    if not dbSamples[0]:
        return "No results found."
    images = getImages(dbSamples, db)

    return response(images)

def getSamples(request, db):
    dbSamples = []
    requestBiological = request.get_json().get('biologicalBeing')
    requestAnatomical = request.get_json().get('anatomicalSite')
    requestSex = request.get_json().get('sex')
    requestAge = request.get_json().get('age')
    if(request.get_json().get("ageOption") == "<"):
        # Age less than
        dbSamples.append(list(db.sample.find({ "$and": [
        {"specimen.attributes.attribute.tag": "age_at_extraction"},
        {"specimen.attributes.attribute.value": {"$lt": int(requestAge)}},
        {"specimen.attributes.attribute.value": requestAnatomical}]})))
    elif(request.get_json().get("ageOption") == ">"):
        # Age more than
        dbSamples.append(list(db.sample.find({ "$and": [
        {"specimen.attributes.attribute.tag": "age_at_extraction"},
        {"specimen.attributes.attribute.value": {"$gt": int(requestAge)}},
        {"specimen.attributes.attribute.value": requestAnatomical}]})))
        ## "$and": [{"specimen.attributes.attribute.tag": "age_at_extraction"}, {"$expr":{ "$gt": [{ "$toInt": "$value" }, 59]}}]
    elif(request.get_json().get("ageOption") == "-"):
        # Ages between
        dbSamples.append(list(db.sample.find({ "$and": [
        {"specimen.attributes.attribute.tag": "age_at_extraction"},
        {"specimen.attributes.attribute.value": {"$gt": int(request.get_json().get('ageStart')), "$lt": int(request.get_json().get('ageEnd'))}},
        {"specimen.attributes.attribute.value": requestAnatomical}]})))

    elif(requestBiological != ""):
        dbSamples.append(list(db.sample.find({"biologicalBeing.attributes.attribute.value": requestBiological, 'biologicalBeing.attributes.attribute.value': requestSex})))
    elif(requestAge != ""):
        dbSamples.append(list(db.sample.find({"specimen.attributes.attribute.value": requestAnatomical})))
    return dbSamples

def getImages(dbSamples, db):
    ## tästä tulee dublicate
    images= []
    for sample in dbSamples:
        keys = sample[0].keys()
        for key in keys:
            if(key == "biologicalBeing"):
                images.append(getImageByBiologicalBeing(sample[0].get("biologicalBeing"), db))
            elif (key == "specimen"):
                images.append(getImageBySpecimen(sample[0].get("specimen"), db))
    return images

def getImageByBiologicalBeing(biologicalBeing, db):

    specimenOfBiologicalBeing = db.sample.find({"specimen.extractedFrom.refname": biologicalBeing.get("alias")})

    blockOfSpecimen =  db.sample.find({'block.sampledFrom.refname': specimenOfBiologicalBeing[0].get("specimen").get("alias")})

    slideOfBlock = db.sample.find({'slide.createdFrom.refname': blockOfSpecimen[0].get("block").get("alias")})

    return db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")})

def getImageBySpecimen(specimen, db):
    blockOfSpecimen =  db.sample.find({'block.sampledFrom.refname': specimen.get("alias")})

    slideOfBlock = db.sample.find({'slide.createdFrom.refname': blockOfSpecimen[0].get("block").get("alias")})

    return db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")})

def response(images):
    
    beacon_response = {
        "beaconId": ".".join(reversed(request.host.split("."))),
        "apiVersion": "0.0.0",
        "exists": True,
        "images": images
    }

    return beacon_response