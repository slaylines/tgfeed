import json
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from .tglib.config import dbconfig, stconfig, tgconfig
from .tglib.database import Database
from .tglib.storage import Storage
from .tglib.telegram import Telegram

db = Database(dbconfig)
st = Storage(stconfig)
tg = Telegram(tgconfig)
app = FastAPI()

# Initialize Telegram client on the app startup.
@app.on_event('startup')
async def startup_event():
  await tg.client.connect()

@app.get("/")
async def read_root():
  channel = await tg.get_channel('winecookies')
  # history = await tg.get_messages(channel)

  # NOTE: https://t.me/winecookies/9?embed=1
  history = []
  count = 0
  async for message in tg.client.iter_messages(channel):
    history.append(message.id)

  # history = await tg.get_messages(channel)
  # history = await tg_client(GetHistoryRequest(
  #   peer=result,
  #   limit=100,
  #   offset_date=None,
  #   offset_id=0,
  #   max_id=0,
  #   min_id=0,
  #   add_offset=0,
  #   hash=0
  # ))
  # return str(history[-165].id)
  return history
