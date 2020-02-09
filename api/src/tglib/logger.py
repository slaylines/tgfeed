import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import lgconfig

# Make sure that log directory exists.
filename = Path(lgconfig.pop('filename'))
filename.parent.mkdir(parents=True, exist_ok=True)

# Rotate logs.
max_bytes = lgconfig.pop('max_bytes')
backup_count = lgconfig.pop('backup_count')
handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)

# Setup the logger.
logging.basicConfig(**{ 'handlers': [handler], **lgconfig })
logger = logging.getLogger('tgfeed')
