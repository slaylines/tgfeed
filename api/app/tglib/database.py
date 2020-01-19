from pymongo import MongoClient

class Database:
  def __init__(self, config):
    self.client = MongoClient(config['uri'])
    self.instance = self.client[config['name']]
