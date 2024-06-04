from flask import Blueprint, request, jsonify
from app.db import get_db
from flask_pymongo import pymongo
from bson import json_util, ObjectId
from datetime import datetime
import json

db = get_db()

users_router = Blueprint(
    'users_router', 'users_router', url_prefix='/api/v1/user')


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


@users_router.route('/', methods=["GET", "POST"])
def get_all_users():
    try:
        documents = list(db.users.find())

        return JSONEncoder().encode({
            "code": 200,
            "users": documents
        }), 400

    except pymongo.errors.PyMongoError as e:
        print(e)
        return jsonify({
            'error': 'An error occurred while retrieving users.',
            'details': str(e)
        }), 500
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'An error occurred while retrieving users.',
            'details': str(e)
        }), 500


@users_router.route('/save', methods=['POST'])
def save_user():
    try:
        data = request.get_json()
        result = db.users.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return JSONEncoder().encode({
            "code": 200,
            "data": result
        })
    except pymongo.errors.PyMongoError as e:
        print(e)
        return jsonify({
            'error': 'user not created',
            'details': str(e)
        }), 500
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'user not created',
            'details': str(e)
        }), 500
