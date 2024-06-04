from pymongo import MongoClient


def get_db():
    uri = "mongodb+srv://teddy:birh-cub_04@woubou.gzzbgka.mongodb.net/?retryWrites=true&w=majority&appName=woubou"
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        return client.find_agent
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return None
