from datetime import datetime, timedelta
from bson import json_util, ObjectId
import os
from json import JSONEncoder

from flask import Flask, jsonify, request
from app.db import get_db
from flask_pymongo import pymongo

from app.api.users import users_router
from app.api.agent import agents_router
from app.api.dashboard import dashboard_router

db = get_db()


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app():

    if db == None:
        return {
            "code": 500,
            "details": "échec de la connexion à la bd"
        }
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'build')

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER)

    app.json_encoder = MongoJsonEncoder
    app.register_blueprint(users_router)
    app.register_blueprint(dashboard_router)
    app.register_blueprint(agents_router)

    @app.route('/', methods=['GET', 'POST'])
    def serve():
        if request.method == 'GET':
            return jsonify({
                "code": 200,
                "message": "Hello world!"
            })

    return app


def register_error_handlers(app):
    @app.errorhandler(pymongo.errors.PyMongoError)
    def handle_mongo_error(error):
        print(f"MongoDB error: {error}")
        return jsonify({'error': 'An error occurred with the database.'}), 500
