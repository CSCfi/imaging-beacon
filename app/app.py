import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo


application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin'

mongo = PyMongo(application)
db = mongo.db

@application.route('/')
def index():
    print('\x1b[6;30;42m' + str(application.config["MONGO_URI"]) + '\x1b[0m')
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app!'
    )

@application.route('/todo')
def todo():
    _todos = db.todo.find()

    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )

@application.route('/todo', methods=['POST'])
def createTodo():
    data = request.get_json(force=True)
    print('\x1b[6;30;42m' + str(data) + '\x1b[0m')
    item = {
        'todo': data['todo']
    }
    db.todo.insert_one(item)

    return jsonify(
        status=True,
        message='To-do saved successfully!'
    ), 201

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)