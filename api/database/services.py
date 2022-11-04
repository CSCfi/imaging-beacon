

def db_samples(request, db):
    dbSamples = []
    requestBiological = request.get("biologicalSpecies")
    requestAnatomical = request.get("anatomicalSite")
    requestSex = request.get("sex")
    requestAge = request.get("age")
    if requestBiological != None and requestAnatomical != None and requestSex != None and requestAge != None:
        # first search biological ids and add those to sample search
        print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
        biologicalList = []
        aliasList= []
        biologicalList.append(
            list(
                db.sample.find(
                    {
                        "biologicalBeing.attributes.value": requestBiological,
                        "biologicalBeing.attributes.value": requestSex,
                    }
                )
            )
        )
        for biological in biologicalList:
            aliasList.append(biological[0]["biologicalBeing"]["alias"])
            if request.get("ageOption") == "<":
            # Age less than
                dbSamples.append(
                    list(
                        db.sample.find(
                            {
                                "$and": [
                                    {"specimen.attributes.tag": "age_at_extraction"},
                                    {"specimen.attributes.value": {"$lt": int(requestAge)}},
                                    {"specimen.attributes.value": requestAnatomical},
                                    {"specimen.extractedFrom.refname": biological[0]["biologicalBeing"]["alias"]}
                                ]
                            }
                        )
                    )
                )
            elif request.get("ageOption") == ">":
                # Age more than
                dbSamples.append(
                    list(
                        db.sample.find(
                            {
                                "$and": [
                                    {"specimen.attributes.tag": "age_at_extraction"},
                                    {"specimen.attributes.value": {"$gt": int(requestAge)}},
                                    {"specimen.attributes.value": requestAnatomical},
                                    {"specimen.extractedFrom.refname": biological[0]["biologicalBeing"]["alias"]}
                                ]
                            }
                        )
                    )
                )
            elif request.get("ageOption") == "-":
            # Ages between
                dbSamples.append(
                    list(
                        db.sample.find(
                            {
                                "$and": [
                                    {"specimen.attributes.tag": "age_at_extraction"},
                                    {
                                        "specimen.attributes.value": {
                                            "$gt": int(request.get("ageStart")),
                                            "$lt": int(request.get("ageEnd")),
                                        }
                                    },
                                    {"specimen.attributes.value": requestAnatomical},
                                    {"specimen.extractedFrom.refname": biological[0]["biologicalBeing"]["alias"]}
                                ]
                            }
                        )
                    )
                )

    elif request.get("ageOption") == "<":
        # Age less than
        dbSamples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.tag": "age_at_extraction"},
                            {"specimen.attributes.value": {"$lt": int(requestAge)}},
                            {"specimen.attributes.value": requestAnatomical},
                        ]
                    }
                )
            )
        )
    elif request.get("ageOption") == ">":
        # Age more than
        dbSamples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.tag": "age_at_extraction"},
                            {"specimen.attributes.value": {"$gt": int(requestAge)}},
                            {"specimen.attributes.value": requestAnatomical},
                        ]
                    }
                )
            )
        )
    elif request.get("ageOption") == "-":
        # Ages between
        dbSamples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.tag": "age_at_extraction"},
                            {
                                "specimen.attributes.value": {
                                    "$gt": int(request.get("ageStart")),
                                    "$lt": int(request.get("ageEnd")),
                                }
                            },
                            {"specimen.attributes.value": requestAnatomical},
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
                        "biologicalBeing.attributes.value": requestBiological,
                        "biologicalBeing.attributes.value": requestSex,
                    }
                )
            )
        )
    elif requestAge != "":
        dbSamples.append(list(db.sample.find({"specimen.attributes.value": requestAnatomical})))
    return dbSamples


def db_images(dbSamples, db):
    images = []
    for sample in dbSamples:
        keys = sample.keys()
        for key in keys:
            if key == "biologicalBeing":
                images.append(__getImageByBiologicalBeing(sample.get("biologicalBeing"), db))
            elif key == "specimen":
                images.append(__getImageBySpecimen(sample.get("specimen"), db))
                
    return images


def __getImageByBiologicalBeing(biologicalBeing, db):

    specimenOfBiologicalBeing = list(db.sample.find({"specimen.extractedFrom.refname": biologicalBeing.get("alias")}))

    blockOfSpecimen = list(db.sample.find({"block.sampledFrom.refname": specimenOfBiologicalBeing[0].get("specimen").get("alias")}))

    slideOfBlock = list(db.sample.find({"slide.createdFrom.refname": blockOfSpecimen[0].get("block").get("alias")}))

    return list(db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")}))


def __getImageBySpecimen(specimen, db):
    blockOfSpecimen = list(db.sample.find({"block.sampledFrom.refname": specimen.get("alias")}))
  
    slideOfBlock = list(db.sample.find({"slide.createdFrom.refname": blockOfSpecimen[0].get("block").get("alias")}))
    
    return list(db.images.find({"imageOf.refname": slideOfBlock[0].get("slide").get("alias")}))
