import json
import logging

from zcs.core.exception import ZcsException 

old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    
    record.error_code = None
    if args[4] and isinstance(args[4], ZcsException):
        record.error_code = args[4].get_error_code()

    # Set original exception value if needed
    record.original_exception = None
    if args[6] is not None:
        for arg in args[6]:
            if isinstance(arg, Exception):
                record.original_exception = arg
                if isinstance(arg, ZcsException):
                    record.error_code = arg.get_error_code()
    
    return record

logging.setLogRecordFactory(record_factory)

class CloudJsonFormatter(logging.Formatter):
    def format(self, record):

        message = record.getMessage()
        if record.exc_info and record.original_exception:
            message = str(record.original_exception)

        log_record = {
            "severity": record.levelname,
            "message": message,
            "time": self.formatTime(record, self.datefmt),
            "logging.googleapis.com/sourceLocation": {
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
                "pathname": record.pathname,
                "traceback": self.formatException(record.exc_info) if record.exc_info else ""
            },
            "logging.googleapis.com/labels": {
                "logger_name": record.name,
                "error_code": record.error_code,
            },
        }
        return json.dumps(log_record)

class ConsoleCustomFormatter(logging.Formatter):

    def __init__(self, verbose = False):
        super().__init__()
        
        set_grey = "\x1b[38;20m"
        set_green = "\x1b[32;20m"
        set_yellow = "\x1b[33;20m"
        set_red = "\x1b[31;20m"
        set_bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        base_format = "%(levelname)-8s %(asctime)s - %(message)s"
        if verbose:
            base_format += " (%(filename)s:%(lineno)d)"

        self.FORMATTERS = {
            logging.DEBUG: logging.Formatter(set_grey + base_format + reset),
            logging.INFO: logging.Formatter(base_format),
            logging.WARNING: logging.Formatter(set_yellow + base_format + reset),
            logging.ERROR: logging.Formatter(set_red + base_format + reset),
            logging.CRITICAL: logging.Formatter(set_bold_red + base_format + reset)
        }

    def format(self, record):
        formatter = self.FORMATTERS.get(record.levelno)
        return formatter.format(record)

class ZcsLogging:

    def __init__(self, enable_cloud_logging: bool = True, log_level: str = logging.INFO):

        self.__log_level = log_level

        # Create a custom logger for ZCS application
        self.__logger = logging.getLogger('zcsapp')

        # Create a custom handler for logging
        custom_handler = logging.StreamHandler()
        if enable_cloud_logging:
            custom_handler.setFormatter(CloudJsonFormatter())
        else:
            custom_handler.setFormatter(ConsoleCustomFormatter())

        # Apply custom handler to all configured loggers
        configured_loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        for p_logger in configured_loggers:
            p_logger.setLevel(self.__log_level)
            if len(p_logger.handlers) == 0:
                continue
            p_logger.handlers = [ custom_handler ]
        
        zcs_handler = logging.StreamHandler()
        if enable_cloud_logging:
            zcs_handler.setFormatter(CloudJsonFormatter())
        else:
            zcs_handler.setFormatter(ConsoleCustomFormatter(True))

        # Set log level and handler for the root logger
        logging.basicConfig(
            level=self.__log_level,
            handlers=[ zcs_handler ]
        )

    def get_logger(self):
        return self.__logger
