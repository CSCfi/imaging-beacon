from flask import request


def index():
    """Display beacon info."""
    beacon_info = {
        "id": ".".join(reversed(request.host.split("."))),
        "name": "Imaging beacon",
        "type": {"group": "test", "artifact": "beacon", "version": "0.0.0"},
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


def getSearchTerms(db):
    """Get all search terms."""
    searchTerms = []
    searchTerms.append(
        {
            "anatomicalSite": list(
                db.sample.find(
                    {"specimen.attributes.attribute.tag": "anatomical_site"},
                    {"specimen.attributes.attribute": 1, "_id": 0},
                )
            )
        }
    )
    searchTerms.append(
        {
            "biologicalBeing": list(
                db.sample.find(
                    {"biologicalBeing.attributes.attribute.tag": "animal_species"},
                    {"biologicalBeing": 1, "_id": 0},
                )
            )
        }
    )
    return searchTerms


def searchQuery(request, db):
    """Search query."""
    # Get sample info
    dbSamples = __getSamples(request, db)
    if not dbSamples[0]:
        return "No results found."
    images = __getImages(dbSamples, db)
    
    return __response(len(images))


def __getSamples(request, db):
    dbSamples = []
    requestBiological = request.get_json().get("biologicalBeing")
    requestAnatomical = request.get_json().get("anatomicalSite")
    requestSex = request.get_json().get("sex")
    requestAge = request.get_json().get("age")
    if request.get_json().get("ageOption") == "<":
        # Age less than
        dbSamples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.attribute.tag": "age_at_extraction"},
                            {"specimen.attributes.attribute.value": {"$lt": int(requestAge)}},
                            {"specimen.attributes.attribute.value": requestAnatomical},
                        ]
                    }
                )
            )
        )
    elif request.get_json().get("ageOption") == ">":
        # Age more than
        dbSamples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.attribute.tag": "age_at_extraction"},
                            {"specimen.attributes.attribute.value": {"$gt": int(requestAge)}},
                            {"specimen.attributes.attribute.value": requestAnatomical},
                        ]
                    }
                )
            )
        )
    elif request.get_json().get("ageOption") == "-":
        # Ages between
        dbSamples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.attribute.tag": "age_at_extraction"},
                            {
                                "specimen.attributes.attribute.value": {
                                    "$gt": int(request.get_json().get("ageStart")),
                                    "$lt": int(request.get_json().get("ageEnd")),
                                }
                            },
                            {"specimen.attributes.attribute.value": requestAnatomical},
                        ]
                    }
                )
            )
        )

    elif requestBiological != "":
        dbSamples.append(
            list(
                db.sample.find(
                    {
                        "biologicalBeing.attributes.attribute.value": requestBiological,
                        "biologicalBeing.attributes.attribute.value": requestSex,
                    }
                )
            )
        )
    elif requestAge != "":
        dbSamples.append(list(db.sample.find({"specimen.attributes.attribute.value": requestAnatomical})))
    return dbSamples


def __getImages(dbSamples, db):

    images = []
    for sample in dbSamples:
        keys = sample[0].keys()
        for key in keys:
            if key == "biologicalBeing":
                images.append(__getImageByBiologicalBeing(sample[0].get("biologicalBeing"), db))
            elif key == "specimen":
                images.append(__getImageBySpecimen(sample[0].get("specimen"), db))
    return images


def __getImageByBiologicalBeing(biologicalBeing, db):

    specimenOfBiologicalBeing = db.sample.find({"specimen.extractedFrom.refname": biologicalBeing.get("alias")})

    blockOfSpecimen = db.sample.find({"block.sampledFrom.refname": specimenOfBiologicalBeing[0].get("specimen").get("alias")})

    slideOfBlock = db.sample.find({"slide.createdFrom.refname": blockOfSpecimen[0].get("block").get("alias")})

    return db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")})


def __getImageBySpecimen(specimen, db):
    blockOfSpecimen = db.sample.find({"block.sampledFrom.refname": specimen.get("alias")})

    slideOfBlock = db.sample.find({"slide.createdFrom.refname": blockOfSpecimen[0].get("block").get("alias")})

    return db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")})


def __response(images):

    beacon_response = {
        "beaconId": ".".join(reversed(request.host.split("."))),
        "apiVersion": "0.0.0",
        "exists": True,
        "images": images,
    }

    return beacon_response
