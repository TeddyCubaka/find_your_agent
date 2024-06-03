from app import mongo
from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/v1/users')


@user_bp.route('/', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    users = UserService.get_all_users()
    return jsonify(users)


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    return jsonify(user)


@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()  # Récupérer les données JSON du corps de la requête
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    user = UserService.create_user(data)
    return jsonify(user), 201
