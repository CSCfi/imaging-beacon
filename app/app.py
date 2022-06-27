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
        # TO DO implement some fallback mechanism for ID
        "id": ".".join(reversed(request.host.split("."))),
        "name": "Imaging beacon",
        "type": "service_type",
        "description": "description",
        "organization": {
            "name": "org_name",
            "url": "org_welcomeUrl__",
        },
        "contactUrl": "__org_contactUrl__",
        "documentationUrl": "__docs_url__",
        "createdAt": "__createtime__",
        "updatedAt": "__updatetime__",
        "environment": "__service_env__",
        "version": "__version__",
    }
    return jsonify(
        beacon_info
    )

@application.route('/db')
def getItems():
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

@application.route('/submit', methods=['POST'])
def submit():
    data = request.get_json(force=True)
    
    item = {
        'todo': data['todo']
    }
    db.todo.insert_one(item)

    return jsonify(
        status=True,
        message='Saved successfully!'
    ), 201

@application.route('/query', methods=['POST'])
def searchQueary():
    return jsonify(
       
    ),201

@application.route('/remove', methods=['POST'])
def remove():
    data = request.get_json(force=True)
    return jsonify(
        message='Removed successfully'   
    ),201

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)