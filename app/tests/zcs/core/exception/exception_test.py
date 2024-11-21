import pytest
from zcs.core.exception import ZcsException

def test_zcs_exception():

    with pytest.raises(ZcsException) as exc_info:
        raise ZcsException("Test exception message", "Test error source", 400, "Test internal message")
    
    assert exc_info.value.get_status_code() == 400
    assert exc_info.value.get_error_source() == "Test error source"
    assert exc_info.value.get_user_message() == "Test exception message"
    assert exc_info.value.get_internal_message() == "Test internal message"
    assert exc_info.value.get_error_code() is not None
    