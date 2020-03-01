import io
from uuid import uuid3, NAMESPACE_URL
from telethon.extensions.html import unparse as unparse_html
from telethon.utils import get_extension
from .logger import logger

class MessageProcessor:
  def __init__(self, database, storage):
    self.database = database
    self.storage = storage

  async def process_message(self, channel, message):
    message_type = self._get_message_type(message)
    method_name = '_process_' + message_type
    method = getattr(self, method_name, self._process_text)

    return await method(channel, message)

  async def _process_photo(self, channel, message):
    name = self._get_media_name(message.photo, channel.id, message.id, 'photo')
    media = await message.download_media(io.BytesIO())
    upload = self.storage.upload_fileobj(media, name)
    html = self._message_to_html(message)

    return {'html': html, 'upload': upload}

  async def _process_video(self, channel, message):
    logger.warning('Can not process message #%s of video type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_document(self, channel, message):
    logger.warning('Can not process message #%s of document type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_gif(self, channel, message):
    logger.warning('Can not process message #%s of gif type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_sticker(self, channel, message):
    logger.warning('Can not process message #%s of sticker type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_audio(self, channel, message):
    logger.warning('Can not process message #%s of audio type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_poll(self, channel, message):
    logger.warning('Can not process message #%s of poll type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_geo(self, channel, message):
    logger.warning('Can not process message #%s of geo type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_venue(self, channel, message):
    logger.warning('Can not process message #%s of venue type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_voice(self, channel, message):
    logger.warning('Can not process message #%s of voice type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_video_note(self, channel, message):
    logger.warning('Can not process message #%s of video_note type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_contact(self, channel, message):
    logger.warning('Can not process message #%s of contact type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_invoice(self, channel, message):
    logger.warning('Can not process message #%s of invoice type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  async def _process_game(self, channel, message):
    logger.warning('Can not process message #%s of game type from %s' % (message.id, channel.title))
    return await self._process_text(channel, message)

  # List of all possible entities:
  # https://tl.telethon.dev/?q=MessageEntity
  #
  # Some of these methods can be useful:
  # https://docs.telethon.dev/en/latest/modules/utils.html
  #
  # Example of HTML parsing in tests:
  # https://github.com/LonamiWebs/Telethon/blob/master/tests/telethon/extensions/test_html.py
  async def _process_text(self, channel, message):
    html = self._message_to_html(message)

    return {'html': html}

  def _message_to_html(self, message):
    return unparse_html(message.raw_text, message.entities).replace('\n', '<br>')

  def _get_media_name(self, media, *parts):
    key = '/'.join(map(str, parts))
    name = str(uuid3(NAMESPACE_URL, key))
    ext = str(get_extension(media))

    return name + ext

  def _get_message_type(self, message):
    if message.photo is not None:
      return 'photo'
    elif message.video is not None:
      return 'video'
    elif message.document is not None:
      return 'document'
    elif message.gif is not None:
      return 'gif'
    elif message.sticker is not None:
      return 'sticker'
    elif message.audio is not None:
      return 'audio'
    elif message.poll is not None:
      return 'poll'
    elif message.geo is not None:
      return 'geo'
    elif message.venue is not None:
      return 'venue'
    elif message.voice is not None:
      return 'voice'
    elif message.video_note is not None:
      return 'video_note'
    elif message.contact is not None:
      return 'contact'
    elif message.invoice is not None:
      return 'invoice'
    elif message.game is not None:
      return 'game'
    else:
      return 'text'
