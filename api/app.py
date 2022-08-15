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


from database.services import index, getItems, getSearchTerms, searchQueary

@application.route("/")
@application.route("/service-info")
def index():
    index


@application.route("/db")
def getItem():
    getItems

@application.route("/getSearchTerms")
def getSearchTerms():
   getSearchTerms

@application.route("/query", methods=["POST"])
def searchQueary():
    """Search query.""" 
    searchQueary(request)
    
if __name__ == "__main__":
    application.config.from_prefixed_env()
    application.config["APP_PORT"]
    application.config["APP_DEBUG"]
    application.run()
