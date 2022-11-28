"""Database functions."""
from aiohttp.web import Request
from pymongo import MongoClient
from typing import List, Dict
from .dbQueries import getAll, getBiological, getBiologicalBySamples, getSampleByAge, getBiologicalsBySex


def db_samples(request: Request, db: MongoClient) -> List:
    """Query for samples collection."""
    db_samples = []
    request_biological = request.get("biologicalSpecies")
    request_anatomical = request.get("anatomicalSite")
    request_sex = request.get("sex")
    request_age = request.get("age", "0")
    if request_biological == "All" and request_anatomical == "All" and request_sex == "All" and request_age == "All":
        db_samples.append(getAll(request, db))
    elif request_biological != "All" and request_anatomical != "All" and request_sex != "All" and request_age != "All":
        # first search biological ids and add those to sample search
        biological_list = []
        biological_list.append(getBiological(db, request_biological, request_sex))

        db_samples.append(
            getBiologicalBySamples(
                db, request_age, request.get("ageOption"), request.get("ageStart", "0"), request.get("ageEnd", "0"), request_anatomical, biological_list
            )
        )
    elif request.get("ageOption") != "Any":
        # Age less than
        db_samples.append(
            getSampleByAge(db, request_age, request.get("ageOption"), request.get("ageStart", "0"), request.get("ageEnd", "0"), request_anatomical)
        )

    elif request_biological != "All" and request_sex != "All":
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
    elif request_anatomical != "All" and request_sex != "All":
        biological_list = getBiologicalsBySex(db, request_sex)
        print("\x1b[6;30;42m" + str(type(biological_list)) + "\x1b[0m")
        samples = []
        for biological in biological_list:
            being = biological.get("biologicalBeing")
            samples.append(
                list(
                    db.sample.find(
                        {
                            "$and": [
                                {"specimen.attributes.value": request_anatomical},
                                {"specimen.extractedFrom.refname": being["alias"]},
                            ]
                        }
                    )
                )
            )
        db_samples.append(samples[0])
    elif request_biological != "All":
        db_samples.append(list(db.sample.find({"biologicalBeing.attributes.value": request_biological})))
    elif request_sex != "All":
        db_samples.append(getBiologicalsBySex(db, request_sex))
    elif request_anatomical != "All":
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
