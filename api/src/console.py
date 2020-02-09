from tglib.config import dbconfig, stconfig, tgconfig
from tglib.database import MongoDatabase
from tglib.storage import S3Storage
from tglib.telegram import Telegram
from tglib.processor import MessageProcessor

db = MongoDatabase(dbconfig)
st = S3Storage(stconfig)
tg = Telegram(tgconfig)
proc = MessageProcessor(db, st)

def connect():
  return tg.client.loop.run_until_complete(tg.client.connect())

def get_channel(name):
  return tg.client.loop.run_until_complete(tg.get_channel(name))

def get_messages(channel):
  return tg.client.loop.run_until_complete(tg.client.get_messages(entity=channel))
