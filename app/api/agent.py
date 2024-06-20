from flask import Blueprint, request, jsonify
from ..models import User, Agent
from .users import Response
from flask_pymongo import pymongo


agents_router = Blueprint(
    'agents_router', 'agents_router', url_prefix='/api/v1/agent')

@agents_router.route('/', methods=["GET"])
def get_all_users():
    try:
        agentModel = Agent()
        # documents = agentModel.find()
        return Response({
            "code": 200,
            "users": agentModel.find_many()
        }), 200

    except pymongo.errors.PyMongoError as e:
        return jsonify({
            'error': 'An error occurred while retrieving users.',
            'details': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while retrieving users.',
            'details': str(e)
        }), 500

@agents_router.route('/arrive', methods=['POST'])
def point_arrive():
    try:
        agentModel = Agent()
        # documents = agentModel.find()
        return Response({
            "code": 200,
            "users": agentModel.find_many()
        }), 200

    except pymongo.errors.PyMongoError as e:
        return jsonify({
            'error': 'An error occurred while retrieving users.',
            'details': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while retrieving users.',
            'details': str(e)
        }), 400