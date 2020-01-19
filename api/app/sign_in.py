from .tglib.telegram import Telegram
from .tglib.config import tgconfig

tg = Telegram(tgconfig)
tg.client.loop.run_until_complete(tg.sign_in())
