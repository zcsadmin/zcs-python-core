import pytest
from zcs.core.logger import ZcsLogging


def test_zcs_logger():

    zcsLogging = ZcsLogging(enable_cloud_logging=False)

    assert zcsLogging is not None