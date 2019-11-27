import sys
import toml
import socks

from pathlib import Path
from fastapi import FastAPI
from pymongo import MongoClient
from telethon import TelegramClient
from telethon.tl.functions.channels import GetChannelsRequest, GetMessagesRequest

##################
# INITIALIZATION #
##################

# Load configurations.
config_path = Path('./config.toml')
config = toml.load(config_path)

tgconfig = config['telegram']
dbconfig = config['database']
pconfig = config['proxy']

# Initialize Telegram client.
proxy = (socks.SOCKS5, pconfig['host'], pconfig['port']) if tgconfig['proxy'] else None
tg_client = TelegramClient(tgconfig['session'], tgconfig['api_id'], tgconfig['api_hash'], proxy=proxy)

# Start the app.
app = FastAPI()

################
# TELEGRAM API #
################

async def get_channels():
  result = await tg_client(GetChannelsRequest(id=['winecookies']))
  return result

##############
# API ROUTES #
##############

@app.on_event('startup')
async def startup_event():
  # Start Telegram client session.
  await tg_client.start(bot_token=tgconfig['bot_token'])

  # Establish database connection.
  db_client = MongoClient(dbconfig['uri'])
  db = db_client[dbconfig['name']]

@app.get("/")
async def read_root():
  result = await get_channels()
  return result
