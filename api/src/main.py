import json
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from .tglib.config import dbconfig, stconfig, tgconfig
from .tglib.database import MongoDatabase
from .tglib.storage import S3Storage
from .tglib.telegram import Telegram
from .tglib.processor import MessageProcessor

db = MongoDatabase(dbconfig)
st = S3Storage(stconfig)
tg = Telegram(tgconfig)
proc = MessageProcessor(db, st)
app = FastAPI()

# Initialize Telegram client on the app startup.
@app.on_event('startup')
async def startup_event():
  await tg.client.connect()

@app.get("/")
async def read_root():
  channel = await tg.get_channel('tgfeed_test')
  history = []
  count = 0

  async for message in tg.client.iter_messages(channel):
    history.append(message)

  await proc.process_message(channel, history[1])

  return True
