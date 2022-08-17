import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json

application = Flask(__name__)
application.config["MONGO_URI"] = (
    "mongodb://"
    + os.environ["MONGODB_USERNAME"]
    + ":"
    + os.environ["MONGODB_PASSWORD"]
    + "@"
    + os.environ["MONGODB_HOSTNAME"]
    + ":27017/"
    + os.environ["MONGODB_DATABASE"]
    + "?authSource=admin"
)

mongo = PyMongo(application)
db = mongo.db


from database.services import index, getItems, getSearchTerms, searchQuery

@application.route("/")
@application.route("/service-info")
def root():
    return jsonify(index())


@application.route("/db")
def getItem():
    return jsonify(status=True, data=getItems(db))

@application.route("/getSearchTerms")
def getSearchTerms():
   return jsonify(results=getSearchTerms(db)), 201

@application.route("/query", methods=["POST"])
def query():
    """Search query.""" 
    result = searchQuery(request, db)
    return jsonify(results=str(result)), 200
    
if __name__ == "__main__":
    application.config.from_prefixed_env()
    application.config["APP_PORT"]
    application.config["APP_DEBUG"]
    application.run()
