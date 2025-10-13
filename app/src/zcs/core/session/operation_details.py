import time
import logging
from typing import Literal, Optional
import uuid
from dataclasses import dataclass


@dataclass
class OperationDetailsConfig:
    time_threshold_ms: int


@dataclass
class OperationDetails:
    """
    Class used to record and manage detailed data about a specific operation.
    """

    def __init__(self, operation_code: str, logger: Optional[logging.Logger] = None):
        self.__operation_code = operation_code
        self.__logger = logger if logger else logging.getLogger()
        self.__start_time_ns = time.perf_counter_ns()
        self.__last_time_ns = self.__start_time_ns

    def getStartTimeNs(self) -> int:
        return self.__start_time_ns

    def getOpCode(self) -> str:
        return self.__operation_code

    def logCheckpoint(self, message: Optional[str] = None, level: Literal[20] = logging.INFO):
        time_ns = time.perf_counter_ns()
        self.__logger.log(
            level,
            "[{}] {} ({:.2f}s delta - {:.2f}s total)".format(
                self.__operation_code,
                message,
                (time_ns - self.__last_time_ns) / 1e9,
                (time_ns - self.__start_time_ns) / 1e9
            )
        )
        self.__last_time_ns = time_ns

    @staticmethod
    def create(op_code: Optional[str] = None, prefix: Optional[str] = None, logger=None) -> "OperationDetails":

        # Use passed operation code if present, otherwise generate a new one
        operation_code = op_code if op_code else OperationDetails.generate_op_code(prefix)

        operation_details = OperationDetails(operation_code, logger)

        return operation_details

    @staticmethod
    def generate_op_code(prefix: Optional[str] = None) -> str:
        """
        Generate a new unique operation code.
        If prefix is provided, prepend it to the generated code.
        """
        op_code = str(uuid.uuid4())
        if prefix:
            return f"{prefix}_{op_code}"
        return op_code
