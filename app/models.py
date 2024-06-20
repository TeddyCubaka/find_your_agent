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

    def find_many (self):
        # users_collection = db['users']
        agents_collection = db['agents']

        join_pipeline = [
            {
                '$lookup': {
                    'from': 'users',  # Join with the 'users' collection
                    'localField': 'as_user',  # Assuming 'agents' have an 'as_user' field
                    'foreignField': '_id',  # '_id' field of users collection
                    'as': 'as_user'  # Name the joined user data as 'user_details'
                }
            },
            {
                '$unwind': '$as_user'  # Unwind the array to access each user document
            },
            {
                '$match': {
                    'as_user': {'$exists': True}  # Filter for agents with an associated user
                }
            },
            {
                '$project': {
                    '_id': 1,  # Include the agent's '_id'
                    'firstname' : 1,
                    'grade' : 1,
                    'lastname' : 1,
                    'poste' : 1,
                    'as_user': 1  # Include the user details
                }
            }
        ]
        agents = list(agents_collection.aggregate(join_pipeline))
        for agent in agents:
            del agent['as_user']['pwd']
        
        return agents
        



class Localisation(ModelInterface):
    collection = db['localisation']

    def __init__(self, validated_data=None):
        super().__init__(validated_data)


class Schedule(ModelInterface):
    collection = db['Schedule']

    def __init__(self, validated_data=None):
        super().__init__(validated_data)
