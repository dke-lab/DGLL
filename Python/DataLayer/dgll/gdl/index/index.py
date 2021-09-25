import json
import urllib

from pymongo import MongoClient


class Index:
    def __init__(self, index):
        self.db_name = 'gdbms'
        self.index_name = index
        self.user_name = '' # Your MongoDB Username
        self.password = ''  # Your MongoDB Password
        self.client = MongoClient('')   # MongoDB URL
        self.db = self.client[self.db_name]
        self.collection = self.db[self.index_name]

    def insert(self, vertex_id, data):
        arr = {}
        arr['id'] = vertex_id
        arr['data'] = data
        self.collection.insert_one(arr)

    def get(self, vertex_id):
        return self.collection.find_one({'id': vertex_id})['data']

    def remove(self, vertex_id):
        return self.collection.delete_one({'id': vertex_id})