"""Query endpoint is used to query the database."""
from ..database.services import db_samples, db_images

from aiohttp.web import Request

async def search_query(request: Request):
    """Search query."""
    req = await request.json()
    # Get sample info

    db = request.app["db"]
    dbSamples = db_samples(req, db)
    if not dbSamples[0]:
        return "No results found."
    images = db_images(dbSamples[0], db)
    amountOfImages = len(list(db.images.find({})))

    return __response(req,[len(images[0]), amountOfImages])


def __response(params, images):

    beacon_response = {
        "beaconId": "localhost:5000",
        "apiVersion": "0.0.0",
        "exists": True,
        "images": images,
    }

    return beacon_response
