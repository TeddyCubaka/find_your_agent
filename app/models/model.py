from bson import ObjectId


class ModelInterface:
    collection = None

    def __init__(self, data):
        self.data = data

    def save(self):
        if '_id' in self.data:
            self.collection.update_one(
                {'_id': self.data['_id']}, {'$set': self.data})
        else:
            result = self.collection.insert_one(self.data)
            self.data['_id'] = result.inserted_id

    def delete(self):
        if '_id' in self.data:
            self.collection.delete_one({'_id': self.data['_id']})
        else:
            raise ValueError("Document must have an '_id' field to be deleted")

    @classmethod
    def find_by_id(cls, id):
        data = cls.collection.find_one({'_id': ObjectId(id)})
        if data:
            return cls(data)
        return None

    @classmethod
    def find(cls, query):
        documents = cls.collection.find(query)
        return [cls(doc) for doc in documents]
