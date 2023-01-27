"""Query endpoint is used to query the database."""
from aiohttp.web import Request

import ujson

from ..config import DB
from ..database.db_service import DBService


async def search_query(request: Request) -> str:
    """Search query.
    
    :param request:  POST request with query parameters as json
    :returns: 
    """
    db_client = request.app["db_client"]
    db_name = DB["name"]
    db_service = DBService(db_name, db_client)

    # Generate mongodb query from requests from json content
    samples, images, datasets = [], [], []
    body = await request.json()

    biobeing_filter = {
        "$and": [
            # Based on species
            {
                "biologicalBeing.attributes.meaning": {
                    "$regex": body["biologicalSpecies"], 
                    "$options": "i"
                }
            },
            # Based on sex
            {
                "biologicalBeing.attributes.value": body["sex"]
            }
        ]
    }

    if isinstance(body["age"], list) and len(body["age"]) == 2:
        age_filter = {
            "specimen.attributes": {
                "$elemMatch": {
                    "tag": "age_at_extraction",
                    "value": {
                        "$gt": body["age"][0],
                        "$lt": body["age"][1]
                    }
                }
            }
        }
    elif isinstance(body["age"], int) and body["ageOption"] == ">":
        age_filter = {
            "specimen.attributes": {
                "$elemMatch": {
                    "tag": "age_at_extraction",
                    "value": {
                        "$gt": body["age"]
                    }
                }
            }
        }
    elif isinstance(body["age"], int) and body["ageOption"] == "<":
        age_filter = {
            "specimen.attributes": {
                "$elemMatch": {
                    "tag": "age_at_extraction",
                    "value": {
                        "$lt": body["age"]
                    }
                }
            }
        }
    else:
        raise Exception("Age parameters cannot be parsed from request")

    specimen_filter = {
        "$and": [
            # Based on anatomical site
            {
                "specimen.attributes.meaning": {
                    "$regex": body["anatomicalSite"], 
                    "$options": "i"
                }
            },
            # Based on age
            age_filter
        ]
    }

    # Combine sample queries and query all the samples
    sample_filter = {
        "$or": [
            biobeing_filter,
            specimen_filter,
        ]
    }
    sample_cursor = db_service.query("samples", sample_filter)
    samples = [item async for item in sample_cursor]

    # Query datasets if search parameters were given
    if "searchTerm" in body.keys():
        search_terms = "|".join(body["searchTerm"])
        dataset_filter = {
            "$or": [
                {
                    "title": {
                        "$regex": search_terms, 
                        "$options": "i"
                    }
                },
                {
                    "description": {
                        "$regex": search_terms, 
                        "$options": "i"
                    }
                },
            ]
        }
        dataset_cursor = db_service.query("datasets", dataset_filter)
        datasets = [item async for item in dataset_cursor]

    result = ujson.dumps(samples + images + datasets)

    return result