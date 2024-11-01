import logging
import logging.config
import os

import src.config as config


def get_logger():
    log_file_dir = os.path.join(config.DATA_PATH, "logs")

    # Create logs directory if not exists
    os.makedirs(log_file_dir, exist_ok=True)

    logging.config.fileConfig(os.path.join(config.CONFIG_PATH, "logging.ini"), defaults={
        'logFileName': os.path.join(log_file_dir, config.BASE_CONFIG["Logging"]["LOG_FILE_NAME"]),
        'logLevel': config.BASE_CONFIG["Logging"]["LOG_LEVEL"]
    })

    return logging.getLogger("mlLogger")
