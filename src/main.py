import uvicorn

import config
from src.app.app import app
from src.app_logger import get_logger

import logging

logger = get_logger()
# Specific logger for multipart
logging.getLogger('multipart.multipart').setLevel(logging.INFO)


def run_server():
    logger.info("Starting ML Service on Port {}".format(config.BASE_CONFIG["MLServer"]["port"]))
    uvicorn.run(
        app,
        host=config.BASE_CONFIG["MLServer"]["host"],
        port=int(config.BASE_CONFIG["MLServer"]["port"])
    )


if __name__ == "__main__":
    run_server()
