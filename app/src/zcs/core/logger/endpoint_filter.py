"""
Define a custom logging filter that can be used to ignore endpoint access logs.
"""
import logging
from typing import List


class EndpointFilter(logging.Filter):
    """Custom filter class to ignore endpoint access logs"""

    def __init__(self, endpoints: List[str] = ["/health", "/metrics", "/info"]):
        self.__endpoints = endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine if a message should be ignored.

        Returns:
            bool - False if the message should be ignored, True if not
        """

        for endpoint in self.__endpoints:
            if record.getMessage().find(f"GET {endpoint}") != -1:
                return False

        return True
