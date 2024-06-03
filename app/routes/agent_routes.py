from flask import Blueprint, jsonify, request

agent_router = Blueprint('agent_router', __name__, url_prefix='/api/v1/agent')


@agent_router.route('/', methods=['GET'])
def get_agents():
    users = {
        "agent": "teddy"
    }
    return jsonify(users)
