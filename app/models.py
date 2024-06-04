from .configs.model import ModelInterface
from app.db import get_db


db = get_db()


class User(ModelInterface):
    collection = db['users']

    def __init__(self, validated_data):
        super().__init__(validated_data)


class Agent(ModelInterface):
    collection = db['agents']

    def __init__(self, username, email):
        super().__init__({
            'username': username,
            'email': email
        })


class Localisation(ModelInterface):
    collection = db['localisation']

    def __init__(self, username, email):
        super().__init__({
            'username': username,
            'email': email
        })


class horraire(ModelInterface):
    collection = db['horraires']

    def __init__(self, username, email):
        super().__init__({
            'username': username,
            'email': email
        })
