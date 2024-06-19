from pymongo import MongoClient


def get_db():
    uri = ""
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        return client.find_agent
    except Exception as e:
        print("Error connecting to MongoDB:", e, "\n")
        return None
