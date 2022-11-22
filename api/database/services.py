"""Database functions."""
from aiohttp.web import Request
from pymongo import MongoClient
from typing import List, Dict


def db_samples(request: Request, db: MongoClient) -> List:
    """Query for samples collection."""
    db_samples = []
    request_biological = request.get("biologicalSpecies")
    request_anatomical = request.get("anatomicalSite")
    request_sex = request.get("sex")
    request_age = request.get("age", "0")
    if request_biological is not None and request_anatomical is not None and request_sex is not None and request_age is not None:
        # first search biological ids and add those to sample search
        
        biological_list = []
        alias_list = []
        biological_list.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"biologicalBeing.attributes.value": request_biological},
                            {"biologicalBeing.attributes.value": request_sex},
                        ]
                    }
                )
            )
        )
        for biological in biological_list:
            alias_list.append(biological[0]["biologicalBeing"]["alias"])
            if request.get("ageOption") == "<":
                # Age less than
                db_samples.append(
                    list(
                        db.sample.find(
                            {
                                "$and": [
                                    {"specimen.attributes.tag": "age_at_extraction"},
                                    {"specimen.attributes.value": {"$lt": int(request_age)}},
                                    {"specimen.attributes.value": request_anatomical},
                                    {"specimen.extractedFrom.refname": biological[0]["biologicalBeing"]["alias"]},
                                ]
                            }
                        )
                    )
                )
            elif request.get("ageOption") == ">":
                # Age more than
                db_samples.append(
                    list(
                        db.sample.find(
                            {
                                "$and": [
                                    {"specimen.attributes.tag": "age_at_extraction"},
                                    {"specimen.attributes.value": {"$gt": int(request_age)}},
                                    {"specimen.attributes.value": request_anatomical},
                                    {"specimen.extractedFrom.refname": biological[0]["biologicalBeing"]["alias"]},
                                ]
                            }
                        )
                    )
                )
            elif request.get("ageOption") == "-":
                # Ages between
                db_samples.append(
                    list(
                        db.sample.find(
                            {
                                "$and": [
                                    {"specimen.attributes.tag": "age_at_extraction"},
                                    {
                                        "specimen.attributes.value": {
                                            "$gt": int(request.get("ageStart", "0")),
                                            "$lt": int(request.get("ageEnd", "0")),
                                        }
                                    },
                                    {"specimen.attributes.value": request_anatomical},
                                    {"specimen.extractedFrom.refname": biological[0]["biologicalBeing"]["alias"]},
                                ]
                            }
                        )
                    )
                )

    elif request.get("ageOption") == "<":
        # Age less than
        db_samples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.tag": "age_at_extraction"},
                            {"specimen.attributes.value": {"$lt": int(request_age)}},
                            {"specimen.attributes.value": request_anatomical},
                        ]
                    }
                )
            )
        )
    elif request.get("ageOption") == ">":
        # Age more than
        db_samples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.tag": "age_at_extraction"},
                            {"specimen.attributes.value": {"$gt": int(request_age)}},
                            {"specimen.attributes.value": request_anatomical},
                        ]
                    }
                )
            )
        )
    elif request.get("ageOption") == "-":
        # Ages between
        db_samples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.tag": "age_at_extraction"},
                            {
                                "specimen.attributes.value": {
                                    "$gt": int(request.get("ageStart", "0")),
                                    "$lt": int(request.get("ageEnd", "0")),
                                }
                            },
                            {"specimen.attributes.value": request_anatomical},
                        ]
                    }
                )
            )
        )

    elif request_biological != "":
        db_samples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"biologicalBeing.attributes.value": request_biological},
                            {"biologicalBeing.attributes.value": request_sex},
                        ]
                    }
                )
            )
        )
    elif request_age != "":
        db_samples.append(list(db.sample.find({"specimen.attributes.value": request_anatomical})))
    return db_samples


def db_images(db_samples: List, db: MongoClient) -> List:
    """Query for images collection."""
    images = []
    for sample in db_samples:
        keys = sample.keys()
        for key in keys:
            if key == "biologicalBeing":
                images.append(get_image_by_biological_being(sample.get("biologicalBeing"), db))
            elif key == "specimen":
                images.append(get_image_by_specimen(sample.get("specimen"), db))

    return images


def get_image_by_biological_being(biological_being: Dict, db: MongoClient):
    """."""
    specimen_of_biological_being = list(db.sample.find({"specimen.extractedFrom.refname": biological_being.get("alias")}))

    block_of_specimen = list(db.sample.find({"block.sampledFrom.refname": specimen_of_biological_being[0].get("specimen").get("alias")}))

    slide_of_block = list(db.sample.find({"slide.createdFrom.refname": block_of_specimen[0].get("block").get("alias")}))

    return list(db.images.find({"imageOf.refname": slide_of_block[0].get("slide").get("alias")}))


def get_image_by_specimen(specimen: Dict, db: MongoClient):
    """."""
    block_of_specimen = list(db.sample.find({"block.sampledFrom.refname": specimen.get("alias")}))

    slide_of_block = list(db.sample.find({"slide.createdFrom.refname": block_of_specimen[0].get("block").get("alias")}))

    return list(db.images.find({"imageOf.refname": slide_of_block[0].get("slide").get("alias")}))
