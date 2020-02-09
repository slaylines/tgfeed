from pymongo import MongoClient

class MongoDatabase:
  def __init__(self, config):
    self.client = MongoClient(config['uri'])
    self.instance = self.client[config['name']]
