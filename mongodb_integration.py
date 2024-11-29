from pymongo import MongoClient, UpdateOne

class MongoDBHandler:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')  # Adjust connection string as necessary
        self.db = self.client['nailib']
        self.collection = self.db['samples']

    def upsert_data(self, data):
        query = {"title": data["title"]}
        update = {"$set": data}
        
        self.collection.update_one(query, update, upsert=True)

    def close_connection(self):
        self.client.close()