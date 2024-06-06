from ..models import User, Agent
from flask import Blueprint, request, jsonify
from app.db import get_db
from flask_pymongo import pymongo
from bson import json_util, ObjectId
from datetime import datetime
import json
from bcrypt import gensalt, hashpw, checkpw
from .utils import Utils


def hash_pwd(pwd):
    salt = gensalt(13)
    pwd = pwd.encode("utf-8")
    bytes_data = hashpw(pwd, salt)
    return bytes_data.decode('utf-8')


users_router = Blueprint(
    'users_router', 'users_router', url_prefix='/api/v1/user')


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)

def Response(data) :
    return json.loads(JSONEncoder().encode(data))


@users_router.route('/', methods=["GET"])
def get_all_users():
    try:
        userModel = User()
        documents = userModel.find()
        return Response({
            "code": 200,
            "users": documents
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


@users_router.route('/save', methods=['GET', 'POST'])
def save_user():
    try:
        utils = Utils()
        data = request.get_json()
        isDataValid = utils.dataValidator(
            data, ['username', 'mobile_no', 'pwd', 'pwd_repeat', "username", "pwd", "is_root", "mobile_no", "pwd_repeat", "firstname", "lastname", "grade", "poste"])

        if isDataValid == False:
            return {
                'code': 400,
                'message': 'certaines données sont manquante. Vérifiez si vous envoyer toutes ces clé : username, mobile_no, pwd, pwd_repeat',
                'error': utils.error
            }, 400
        if utils.passwordVerify(data['pwd'], data['pwd_repeat']) == False:
            return {
                'code': 400,
                'message': utils.error['details'],
                'error': utils.error
            }, 400

        user_data = {
            "username": data['username'],
            "pwd": data['pwd'],
            "is_root": data['is_root'] if data['is_root'] is not None else False,
            "mobile_no": data['mobile_no']
        }

        user_data['pwd'] = hash_pwd(user_data['pwd'])
        userModel = User(user_data)
        existed_user = userModel.find({"username": data['username']})
        if len(existed_user) > 0:
            return {
                "code": 400,
                "message": "l'utilisateur avec ce nom existe déjà. Veuillez choisir un autre nom d'utilisateur",
            }
        existed_user = userModel.find({"mobile_no": data['mobile_no']})
        if len(existed_user) > 0:
            return {
                "code": 400,
                "message": "Ce numéro de téléphone existe déjà dans le système. Veuillez choisir un autre nom d'utilisateur"
            }
        userModel.save()
        if userModel.error is not None:
            return Response({
                'code': 400,
                'message': 'une erreur s\'est produite lors de la création du compte',
                'error': userModel.error
            }), 400

        agentData = {
            "firstname": data['firstname'],
            "lastname": data['lastname'],
            "grade": data['grade'],
            "poste": data['poste'],
            "as_user": user_data['_id']
        }

        agentModel = Agent(agentData)
        agentModel.save()
        if agentModel.error is not None:
            userModel.delete()
            return Response({
                'code': 400,
                'message': 'une erreur s\'est produite lors de la création du compte',
                'error': agentModel.error
            }), 400

        agentData['as_user'] = user_data

        return Response({
            "code": 200,
            "data": agentData
        })
    except pymongo.errors.PyMongoError as e:
        return jsonify({
            'error': 'user not created',
            'details': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'user not created',
            'details': str(e)
        }), 400
    except TypeError as error:
        return jsonify({
            'error': 'user not created',
            'details': str(error)
        }), 400


@users_router.route('/login', methods=["POST"])
def user_login():
    try:
        utils = Utils()
        data = request.get_json()
        isDataValid = utils.dataValidator(data, ['login', 'pwd'])
        if isDataValid == False:
            return {
                'code': 400,
                'message': 'certaines données sont manquante. Vérifiez si vous envoyer toutes ces clé : login, pwd',
                'error': utils.error
            }, 400
        userModel = User()
        if isinstance(data['login'], (int, float, complex)):
            loginStr = "numéro de téléphone"
            users = userModel.find({"mobile_no": data['login']})
        else:
            loginStr = "nom d'utilisateur"
            users = userModel.find({"username": data['login']})

        if users is None or len(users) == 0:
            return {
                "code": 404,
                "message": f"{loginStr} ou mot de passe incorrect"
            }

        user = users[0]
        password = data['pwd'].encode('utf-8')
        hashed_password = user['pwd'].encode('utf-8')
        if checkpw(password=password, hashed_password=hashed_password) is not True:
            return {
                "code": 404,
                "message": f"{loginStr} ou mot de passe incorrect"
            }, 404

        agentModel = Agent()
        agent = agentModel.find({"as_user": user['_id']})
        if agent is None or len(agent) == 0:
            return {
                "code": 404,
                "message": f"{loginStr} ou mot de passe incorrect"
            }

        agent = agent[0]

        agent["as_user"] = user

        return Response({
            "code": 200,
            "message": f"bienvenue {agent['firstname']}",
            "data": agent
        }), 200

    except TypeError as error:
        return jsonify({
            'error': 'échec de connexion',
            'details': str(error),
            'type': "TypeError"
        }), 400
    except pymongo.errors.PyMongoError as e:
        return jsonify({
            'error': 'échec de connexion',
            'details': str(e)
        }), 400
    except Exception as error:
        return jsonify({
            'error': 'échec de connexion',
            'details': str(error),
            'type': "Exception"
        }), 400
