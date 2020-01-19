import socks
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Message:
# id - the ID of this message.
# date - the UTC+0 datetime object indicating when this message was sent.
# message - the string text of the message without formatting.
# action - the message action object, we want to ignore these.
# media - the media sent with this message if any (photos, videos, documents, gifs, stickers, etc.).
# entities - the list of markup entities in this message, such as bold, italics, code, hyperlinks, etc.
# edit_date - the date when this message was last edited.
# post_author - the display name of the message sender to show in messages sent to broadcast channels.
# grouped_id - the group ID of the message (photo albums or video albums).
# audio() - audio.
# document() - document.
# download_media() - downloads the media contained in the message, if any.
# file() - returns a File wrapping the photo or document in this message.
# get_entities_text() - returns a list of (markup entity, inner text).
# gif() - gif.
# photo() - photo.
# poll() - poll.
# raw_text() - the string text of the message without formatting.
# sticker() - sticker.
# text() - the message text, formatted using the client’s default parse mode.
# video() - video.
# web_preview() - the web page in this message.
class Telegram:
  def __init__(self, config):
    self.__dict__.update(config)
    self.client = TelegramClient(config['session'], config['api_id'], config['api_hash'],
                                 proxy=self.__proxy())

  async def sign_in(self):
    await self.client.connect()

    if not await self.client.is_user_authorized():
      await self.client.start(self.phone)
    else:
      print('Already signed in with %s phone number and "%s" session.' % (self.phone, self.session))

  async def get_channel(self, name):
    return await self.client.get_entity(name)

  async def get_messages(self, channel):
    request = GetHistoryRequest(
      peer=channel,
      limit=100,
      offset_date=None,
      offset_id=1000,
      max_id=0,
      min_id=0,
      add_offset=0,
      hash=0
    )

    return await self.client(request)

  def __proxy(self):
    if hasattr(self, 'proxy'):
      return (socks.SOCKS5, self.proxy['host'], self.proxy['port'])
