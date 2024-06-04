from ..models.model import ModelInterface
from app.db import get_db


db = get_db()


class User(ModelInterface):
    collection = db['users']

    def __init__(self, username, email):
        super().__init__({
            'username': username,
            'email': email
        })
