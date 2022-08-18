import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json

application = Flask(__name__)
application.config["MONGO_URI"] = ("mongodb://"
    + os.environ["MONGO_INITDB_ROOT_USERNAME"]
    + ":"
    + os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    + "@"
    + "localhost"
    + ":27017/"
    + "beacondb?authSource=admin")

mongo = PyMongo(application)
db = mongo.db

from database.services import index, getItems, getSearchTerms, searchQuery

@application.route("/")
@application.route("/service-info")
def root():
    return jsonify(index())


@application.route("/db")
def getItem():
    return jsonify(response=getItems(db)), 200

@application.route("/getSearchTerms")
def getSearchTerms():
   return jsonify(response=getSearchTerms(db)), 200

@application.route("/query", methods=["POST"])
def query():
    """Search query.""" 
    result = searchQuery(request, db)
    return jsonify(response=str(result)), 200
    
if __name__ == "__main__":
    application.config.from_prefixed_env()
    application.config["APP_PORT"]
    application.config["APP_DEBUG"]
    application.run()
