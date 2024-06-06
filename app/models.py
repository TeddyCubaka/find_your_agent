from .configs.model import ModelInterface
from app.db import get_db


db = get_db()


class User(ModelInterface):
    collection = db['users']

    def __init__(self, validated_data=None):
        super().__init__(validated_data)


class Agent(ModelInterface):
    collection = db['agents']

    def __init__(self, validated_data=None):
        super().__init__(validated_data)


class Localisation(ModelInterface):
    collection = db['localisation']

    def __init__(self, validated_data=None):
        super().__init__(validated_data)


class horraire(ModelInterface):
    collection = db['horraires']

    def __init__(self, validated_data=None):
        super().__init__(validated_data)
