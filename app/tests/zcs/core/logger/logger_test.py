import pytest
from zcs.core.logger import ZcsLogger


def test_zcs_logger():

    with pytest.raises(Exception) as exc_info:
        ZcsLogger()

    assert exc_info.type == TypeError