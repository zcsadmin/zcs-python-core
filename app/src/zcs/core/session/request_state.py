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
            qa_info: Optional[QaInfo] = None,
            doc_type: Optional[str] = None,
            size: Optional[int] = None,
            total_pages: Optional[int] = None,
            job_id: Optional[str] = None,
            file_id: Optional[str] = None,
            attempts: Optional[int] = 0
            ):

        self.__request_id = request_id if request_id else RequestState.generate_op_code(prefix=prefix)
        self.__op_code = op_code if op_code else self.__request_id
        self.__request_start_ns = time.perf_counter_ns()
        self.__checkpoint_ns = self.__request_start_ns
        self.__auth_info = auth_info
        self.__follia_module = follia_module
        self.__qa_info = qa_info
        self.__doc_type = doc_type
        self.__size = size
        self.__total_pages = total_pages
        self.__job_id = job_id
        self.__file_id = file_id
        self.__attempts = attempts

    def setAttempts(self, attempts: int):
        """
        Set number of attempts.
        """

        self.__attempts = attempts

    def getAttempts(self) -> int:
        """
        Get number of attempts.
        """

        return self.__attempts

    def setFileId(self, file_id: str):
        """
        Set file id.
        """

        self.__file_id = file_id

    def getFileId(self) -> Optional[str]:
        """
        Get file id.
        """

        return self.__file_id
    
    def setJobId(self, job_id: str):
        """
        Set job id.
        """

        self.__job_id = job_id

    def getJobId(self) -> Optional[str]:
        """
        Get job id.
        """

        return self.__job_id

    def setTotalPages(self, total_pages: int):
        """
        Set total pages.
        """

        self.__total_pages = total_pages

    def getTotalPages(self) -> Optional[int]:
        """
        Get total pages.
        """

        return self.__total_pages

    def getSize(self) -> Optional[int]:
        """
        Get size.
        """

        return self.__size

    def setSize(self, size: int):
        """
        Set size.
        """

        self.__size = size
    
    def getDocType(self) -> Optional[str]:
        """
        Get document type.
        """

        return self.__doc_type
    
    def setDocType(self, doc_type: str):
        """
        Set document type.
        """

        self.__doc_type = doc_type

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
