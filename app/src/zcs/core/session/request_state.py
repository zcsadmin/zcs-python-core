import time
import uuid
from typing import Optional


class RequestState():

    def __init__(
            self,
            request_id: Optional[str] = None,
            prefix: Optional[str] = None,
            op_code: Optional[str] = None):

        self.__request_id = request_id if request_id else RequestState.generate_op_code(prefix=prefix)
        self.__op_code = op_code if op_code else self.__request_id
        self.__request_start_ns = time.perf_counter_ns()
        self.__checkpoint_ns = self.__request_start_ns

    def getOpCode(self) -> str:
        """
        Get operation code value.
        """

        return self.__op_code

    def getRequestId(self) -> str:
        """
        Get request id value.
        """

        return self.__request_id

    def getRequestStartNs(self) -> int:
        """
        Get request start time in nanoseconds.
        """

        return self.__request_start_ns

    def getCheckpointNs(self) -> int:
        """
        Get checkpoint time in nanoseconds.
        """

        return self.__checkpoint_ns

    def setCheckpointNs(self, time_ns: int):
        """
        Set checkpoint time in nanoseconds.
        """

        self.__checkpoint_ns = time_ns

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
