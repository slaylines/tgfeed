import toml
from pathlib import Path

config_path = Path('./config.toml')
config = toml.load(config_path)

tgconfig = config['telegram']
dbconfig = config['database']
stconfig = config['storage']
lgconfig = config['logger']
