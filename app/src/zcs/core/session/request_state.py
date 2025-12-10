import time
import uuid
from typing import Optional

from zcs.core.session.auth_info import AuthInfo
from zcs.core.session.follia_module import FolliaModule
from zcs.core.session.qa_info import QaInfo


class RequestState():

    def __init__(
            self,
            request_id: Optional[str] = None,
            prefix: Optional[str] = None,
            op_code: Optional[str] = None,
            auth_info: Optional[AuthInfo] = None,
            follia_module: Optional[FolliaModule] = None,
            qa_info: Optional[QaInfo] = None):

        self.__request_id = request_id if request_id else RequestState.generate_op_code(prefix=prefix)
        self.__op_code = op_code if op_code else self.__request_id
        self.__request_start_ns = time.perf_counter_ns()
        self.__checkpoint_ns = self.__request_start_ns
        self.__auth_info = auth_info
        self.__follia_module = follia_module
        self.__qa_info = qa_info

    def getQaInfo(self) -> Optional[QaInfo]:
        """
        Get QA information.
        """

        return self.__qa_info

    def setQaInfo(self, qa_info: QaInfo):
        """
        Set QA information.
        """

        self.__qa_info = qa_info

    def getFolliaModule(self) -> Optional[FolliaModule]:
        """
        Get Follia module information.
        """

        return self.__follia_module
    
    def setFolliaModule(self, follia_module: FolliaModule):
        """
        Set Follia module information.
        """

        self.__follia_module = follia_module

    def getAuthInfo(self) -> Optional[AuthInfo]:
        """
        Get authentication information.
        """

        return self.__auth_info
    
    def setAuthInfo(self, auth_info: AuthInfo):
        """
        Set authentication information.
        """

        self.__auth_info = auth_info

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
