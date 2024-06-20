from bson import json_util, ObjectId
from datetime import datetime
import json
from flask_pymongo import pymongo


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


class ModelInterface:
    collection = None
    error = None

    def __init__(self, data):
        self.data = data

    def save(self):
        try:
            if "_id" in self.data:
                self.collection.update_one(
                    {"_id": self.data["_id"]}, {"$set": self.data}
                )
            else:
                result = self.collection.insert_one(self.data)
                self.data["_id"] = result.inserted_id
        except pymongo.errors.PyMongoError as e:
            self.error = e

    def delete(self, id):
        if "_id" != None:
            self.collection.delete_one({"_id": ObjectId(id)})
        else:
            raise ValueError("Document must have an '_id' field to be deleted")

    @classmethod
    def find_by_id(cls, id):
        data = cls.collection.find_one({"_id": ObjectId(id)})
        if data:
            return cls(data)
        return None

    @classmethod
    def find(cls, query=None):
        documents = list(cls.collection.find(query))
        return documents
        # return json.dumps(documents, cls=EnhancedJSONEncoder)
