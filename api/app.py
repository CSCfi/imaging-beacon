import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
import bson.json_util as json_util
from database.services import index, getItems, getSearchTerms, searchQuery

application = Flask(__name__)
application.config["MONGO_URI"] = (
    "mongodb://"
    + os.environ["MONGO_INITDB_ROOT_USERNAME"]
    + ":"
    + os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    + "@"
    + "localhost"
    + ":27017/"
    + "beacondb?authSource=admin"
)

mongo = PyMongo(application)
db = mongo.db


@application.route("/")
@application.route("/service-info")
def root():
    """Return service info."""
    return jsonify(index())


@application.route("/db")
def getItem():
    """Return db items."""
    return jsonify(response=getItems(db)), 200


@application.route("/getSearchTerms")
def returnearchTerms():
    """Return db search terms."""
    return jsonify(response=getSearchTerms(db)), 200


@application.route("/query", methods=["POST"])
def query():
    """Search query."""
    result = searchQuery(request, db)
    if result == "No results found.":
        return json.loads(json_util.dumps(result)), 400
    return json.loads(json_util.dumps(result)), 200


if __name__ == "__main__":
    application.config.from_prefixed_env()
    application.config["APP_PORT"]
    application.config["APP_DEBUG"]
    application.run()
