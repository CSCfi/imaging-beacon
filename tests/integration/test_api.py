"""Run integration tests for imaging beacon api endpoints."""
import logging
import os

from aiohttp import ClientSession

# === Global vars ===
FORMAT = "[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s](L:%(lineno)s) %(funcName)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

base_url = os.getenv("BASE_URL", "http://localhost:8080")


async def test_service_info():
    """Test the service info endpoint works."""
    async with ClientSession() as sess:
        async with sess.get(f"{base_url}") as resp:
            assert resp.status == 200, f"Incorrect response status: {resp.status}"
            LOG.debug("Endpoint is functional")
            res = await resp.json()
            assert res["organization"]["name"] == "CSC - IT Center for Science"

async def test_json_schema_validation():
    """Test the query request fails with an incorrect json payload."""
    async with ClientSession() as sess:
        async with sess.post(f"{base_url}/query", json={"wrong key": "wrong value"}) as resp:
            assert resp.status == 400, f"Incorrect response status: {resp.status}"
            res = await resp.text()
            assert res == "Could not validate request body: 'biologicalSpecies' is a required property"

async def test_minimal_json_query():
    """Test the database query works with minimal json info."""
    query_json = {
        "biologicalSpecies": "homo sapiens",
        "anatomicalSite": "lung",
        "sex": "F",
        "age": [60, 80],
        "ageUnit": "Y"
    }
    async with ClientSession() as sess:
        async with sess.post(f"{base_url}/query", json=query_json) as resp:
            assert resp.status == 200, f"Incorrect response status: {resp.status}"
            res = await resp.json()
            biological_beings, specimen, dataset = 0, 0, 0
            for item in res:
                if "biologicalBeing" in item.keys():
                    biological_beings += 1
                if "specimen" in item.keys():
                    specimen += 1
                if "datasetType" in item.keys():
                    dataset += 1
            assert biological_beings == 6, f"Incorrect amount of objects found"
            assert specimen == 9, f"Incorrect amount of objects found"
            assert dataset == 0, f"Incorrect amount of objects found"

async def test_maximal_json_query():
    """Test the database query works with maximal json info."""
    query_json = {
        "biologicalSpecies": "homo sapiens",
        "anatomicalSite": "lung",
        "sex": "M",
        "age": 60,
        "ageOption": "<",
        "ageUnit": "Y",
        "searchTerm": ["mockdataset"]
    }
    async with ClientSession() as sess:
        async with sess.post(f"{base_url}/query", json=query_json) as resp:
            assert resp.status == 200, f"Incorrect response status: {resp.status}"
            res = await resp.json()
            biological_beings, specimen, dataset = 0, 0, 0
            for item in res:
                if "biologicalBeing" in item.keys():
                    biological_beings += 1
                if "specimen" in item.keys():
                    specimen += 1
                if "datasetType" in item.keys():
                    dataset += 1
            assert biological_beings == 5, f"Incorrect amount of objects found"
            assert specimen == 2, f"Incorrect amount of objects found"
            assert dataset == 1, f"Incorrect amount of objects found"


