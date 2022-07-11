import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin'

mongo = PyMongo(application)
db = mongo.db

@application.route('/')
@application.route('/service-info')
def index():
    beacon_info = {
        "id": ".".join(reversed(request.host.split("."))),
        "name": "Imaging beacon",
        "type": "",
        "description": "",
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
    return jsonify(
        beacon_info
    )

@application.route('/db')
# lists all db items
def getItem():
    _db = db.todo.find()

    item = {}
    data = []
    for i in _db:
        item = {
            'id': str(i['_id']),
            'item': i['todo']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )


@application.route('/query', methods=['POST'])
def searchQueary():
    return jsonify(
       
    ),201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)