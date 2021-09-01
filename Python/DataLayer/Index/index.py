import json
import urllib

from pymongo import MongoClient


class MongoIndex:
    def __init__(self):
        self.db_name = 'gdbms'
        self.index_name = 'index'
        self.user_name = '' # Your MongoDB Username
        self.password = ''  # Your MongoDB Password
        self.client = MongoClient('')   # MongoDB URL
        self.db = self.client[self.db_name]
        self.collection = self.db[self.index_name]

    def db_list(self):
        print(self.client.list_database_names())

    def index(self, data):
        self.collection.insert_one(data)

    def bulk_index(self, json_file):
        data = json.load(open(json_file))

        print('Records (Nodes) in JSON: ' + str(len(data)))
        print('Bulk Insert JSON into MongoDB...')
        self.collection.insert_many(data)
        print('Bulk Insert Successful...')

        print('Documents (Nodes) in MongoDB: ' + str(self.collection.estimated_document_count()))

    def drop_index(self):
        self.collection.drop()

    def drop_db(self):
        self.client.drop_database(self.index_name)

    def drop_index_and_db(self):
        self.drop_index()
        self.drop_db()

    def get(self, node_id, hop):
        return self.collection.find_one({'node_id': node_id, 'hop': hop})


if __name__ == "__main__":
    mongo = MongoIndex()

    mongo.db_list()
    mongo.bulk_index('') # Data to be indexed
    node = mongo.get(node_id=31353, hop=10)
    print(node)
