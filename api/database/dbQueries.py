from typing import List
from aiohttp.web import Request
from pymongo import MongoClient


def getAll(request: Request, db: MongoClient) -> List:
    return list(db.sample.find({"specimen": {"$exists": "true"}}))


def getBiological(db: MongoClient, biological, sex) -> List:
    return list(
        db.sample.find(
            {
                "$and": [
                    {"biologicalBeing.attributes.value": biological},
                    {"biologicalBeing.attributes.value": sex},
                ]
            }
        )
    )

def getBiologicalsBySex(db: MongoClient, sex) -> List:
    return list(db.sample.find({"biologicalBeing.attributes.value": sex}))

def getBiologicalBySamples(db: MongoClient, request_age, ageOption, ageStart, ageEnd, request_anatomical, biological_list: List) -> List:
    alias_list = []
    samples = []
    for biological in biological_list:
        alias_list.append(biological[0]["biologicalBeing"]["alias"])
        if ageOption == "<":
            # Age less than
            samples.append(
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

        elif ageOption == ">":
            # Age more than
            samples.append(
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

        elif ageOption == "-":
            # Ages between
            samples.append(
                list(
                    db.sample.find(
                        {
                            "$and": [
                                {"specimen.attributes.tag": "age_at_extraction"},
                                {
                                    "specimen.attributes.value": {
                                        "$gt": int(ageStart),
                                        "$lt": int(ageEnd),
                                    }
                                },
                                {"specimen.attributes.value": request_anatomical},
                                {"specimen.extractedFrom.refname": biological[0]["biologicalBeing"]["alias"]},
                            ]
                        }
                    )
                )
            )
    return samples[0]


def getSampleByAge(db: MongoClient, request_age, ageOption, ageStart, ageEnd, request_anatomical) -> List:
    db_samples = []
    if ageOption == "<":
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
    elif ageOption == ">":
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
    elif ageOption == "-":
        # Ages between
        db_samples.append(
            list(
                db.sample.find(
                    {
                        "$and": [
                            {"specimen.attributes.tag": "age_at_extraction"},
                            {
                                "specimen.attributes.value": {
                                    "$gt": int(ageStart),
                                    "$lt": int(ageEnd),
                                }
                            },
                            {"specimen.attributes.value": request_anatomical},
                        ]
                    }
                )
            )
        )
    return db_samples[0]
