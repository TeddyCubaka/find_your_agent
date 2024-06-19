from pymongo.mongo_client import MongoClient
from env import mongo_uri

def get_db():
    try:
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        return client.find_agent
    except Exception as e:
        print("Error connecting to MongoDB:", e, "\n")
        return None
