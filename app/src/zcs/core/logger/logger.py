import json
import logging
#from google.cloud import logging as gcloud_logging

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt)
        }
        return json.dumps(log_record)





class ZcsLogger:

    def __init__(self, environment: str, log_level: str = logging.INFO):
        self.__logger = logging
        self.__log_level = log_level
        
        if environment == "local":
            # TODO verificare che questa Google Cloud Logging serva
            # Configura il client di Google Cloud Logging
            #gcloud_logging_client = gcloud_logging.Client()
            #gcloud_logging_client.setup_logging()

            # Configura il logger root
            root_logger = self.__logger.getLogger()
            root_logger.setLevel(self.__log_level)
            self.clear_handlers(root_logger)

            # Configura i logger di Uvicorn

            
            uvicorn_logger = self.__logger.getLogger("uvicorn")
            uvicorn_logger.setLevel(self.__log_level)
            self.clear_handlers(uvicorn_logger)

            #uvicorn_error_logger = self.__logger.getLogger("uvicorn.error")
            # uvicorn_error_logger.setLevel(self.__logger.ERROR)
            #self.clear_handlers(uvicorn_error_logger)

            uvicorn_access_logger = self.__logger.getLogger("uvicorn.access")
            # uvicorn_access_logger.setLevel(self.__log_level)
            self.clear_handlers(uvicorn_access_logger)

            # Crea un handler personalizzato per Google Cloud Logging
            handler = self.__logger.StreamHandler()
            formatter = JsonFormatter()
            handler.setFormatter(formatter)

            # Aggiungi l'handler a tutti i logger
            #loggers = [root_logger, uvicorn_logger, uvicorn_access_logger, uvicorn_error_logger]
            loggers = [root_logger, uvicorn_logger, uvicorn_access_logger]
            for logger in loggers:
                logger.addHandler(handler)

        else:
            log_handlers = []
            log_handlers.append(logging.StreamHandler())

            # logging config
            logging.basicConfig(
                level=self.__log_level,
                format="%(asctime)s [%(levelname)s] %(message)s",
                handlers=log_handlers
            )

    def clear_handlers(self, logger):
        while logger.handlers:
            logger.handlers.pop()

    def get_logger(self):
        return self.__logger
