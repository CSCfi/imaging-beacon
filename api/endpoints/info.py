"""Info endpoint provides useful information and documentation on the service."""

from typing import Dict

from aiohttp.web import Request


async def service_info(request: Request) -> Dict:
    """Display beacon info."""
    return {
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


def get_search_terms(request: Request) -> Dict:
    """Get all search terms."""
    db = request.app["db"]
    searchTerms = []
    searchTerms.append(
        {
            "anatomicalSite": list(
                db.sample.find(
                    {"specimen.attributes.tag": "anatomical_site"},
                    {"specimen.attributes": 1, "_id": 0},
                )
            )
        }
    )
    searchTerms.append(
        {
            "biologicalBeing": list(
                db.sample.find(
                    {"biologicalBeing.attributes.tag": "animal_species"},
                    {"biologicalBeing": 1, "_id": 0},
                )
            )
        }
    )
    
    return searchTerms
