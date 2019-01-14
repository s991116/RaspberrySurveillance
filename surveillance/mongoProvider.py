import pymongo
import dns.resolver

class MongoProvider:

    def __init__(self, connection):
        self.client = pymongo.MongoClient(connection)
        self.db = self.client.test
        

    def insert_one(self, data):
        return self.db.posts.insert_one(data).inserted_id

