import configparser
import logging
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print(config.sections())
