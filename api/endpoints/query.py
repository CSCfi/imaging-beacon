"""Query endpoint is used to query the database."""
from typing import Dict, List
from aiohttp.web import Request

from ..database.services import db_samples, db_images


async def search_query(request: Request) -> Dict:
    """Search query."""
    req = await request.json()
    # Get sample info

    db = request.app["db"]
    samples = db_samples(req, db)
    if not samples[0]:
        return _response(req, [])
    images = db_images(samples[0], db)
    amount_of_images = len(list(db.images.find({})))

    return _response(request, [len(images[0]), amount_of_images])


def _response(request: Request, images: List) -> Dict:

    beacon_response = {
        "beaconId": ".".join(reversed(request.host.split("."))),
        "apiVersion": "0.0.0",
        "exists": bool(images),
        "images": images,
    }

    return beacon_response
