import os
from configparser import ConfigParser
from dotenv import load_dotenv
import logging
import sys

CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), os.pardir, "config"))

BASE_CONFIG = ConfigParser()
BASE_CONFIG.read(os.path.join(CONFIG_PATH, "config.ini"))

ML_ENV = os.environ["ML_ENV"] if "ML_ENV" in os.environ else BASE_CONFIG["Default"]["ML_ENV_DEV"]

try:
    load_dotenv(os.path.join(CONFIG_PATH, "environments", ".env.{}".format(ML_ENV)))
    print('Loaded variables from {} environment file'.format(ML_ENV))
except FileNotFoundError as e:
    logging.error('Required files not present in config folder')
    raise e

if "debug" in os.environ and os.environ["debug"].lower() == "true":
    BASE_CONFIG["Logging"]["LOG_LEVEL"] = "DEBUG"

if "ML_DATA_DIR" not in os.environ:
    logging.error('Environment Variable "ML_DATA" has not been set. Point it to an empty directory')
    sys.exit(2)
