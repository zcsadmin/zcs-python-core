import json
import logging
from google.cloud import logging as gcloud_logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt)
        }
        return json.dumps(log_record)


def clear_handlers(logger):
    while logger.handlers:
        logger.handlers.pop()


class ZcsLogger:

    def __init__(self, logging: logging, environment: str):
        self.logging = logging
        if environment == "develop":
            # Configura il client di Google Cloud Logging
            gcloud_logging_client = gcloud_logging.Client()
            gcloud_logging_client.setup_logging()

            # Configura il logger root
            root_logger = self.logging.getLogger()
            root_logger.setLevel(self.logging.INFO)
            clear_handlers(root_logger)

            # Configura i logger di Uvicorn
            uvicorn_logger = self.logging.getLogger("uvicorn")
            uvicorn_logger.setLevel(self.logging.INFO)
            clear_handlers(uvicorn_logger)

            uvicorn_error_logger = self.logging.getLogger("uvicorn.error")
            uvicorn_error_logger.setLevel(self.logging.INFO)
            clear_handlers(uvicorn_error_logger)

            uvicorn_access_logger = self.logging.getLogger("uvicorn.access")
            uvicorn_access_logger.setLevel(self.logging.INFO)
            clear_handlers(uvicorn_access_logger)

            # Crea un handler personalizzato per Google Cloud Logging
            handler = self.logging.StreamHandler()
            formatter = JsonFormatter()
            handler.setFormatter(formatter)

            # Aggiungi l'handler a tutti i logger
            loggers = [root_logger, uvicorn_logger, uvicorn_access_logger, uvicorn_error_logger]
            for logger in loggers:
                logger.addHandler(handler)

        else:
            handler = self.logging.StreamHandler()
            formatter = JsonFormatter()
            handler.setFormatter(formatter)