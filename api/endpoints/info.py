"""Info endpoint provides useful information and documentation on the service."""
from aiohttp.web import Request
from typing import Dict, List
from ..config import APP


async def service_info(request: Request) -> Dict:
    """Display beacon info."""
    service_info = APP["info"]
    service_info["id"] = ".".join(reversed(request.host.split(".")))
    return service_info


def get_search_terms(request: Request) -> List:
    """Get all search terms."""
    db = request.app["db_client"]
    search_terms = []
    search_terms.append(
        {
            "anatomicalSite": list(
                db.sample.find(
                    {"specimen.attributes.tag": "anatomical_site"},
                    {"specimen.attributes": 1, "_id": 0},
                )
            )
        }
    )
    search_terms.append(
        {
            "biologicalBeing": list(
                db.sample.find(
                    {"biologicalBeing.attributes.tag": "animal_species"},
                    {"biologicalBeing": 1, "_id": 0},
                )
            )
        }
    )

    return search_terms
