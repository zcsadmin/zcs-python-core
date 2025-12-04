
from enum import StrEnum

class FolliaModule(StrEnum):
    """
    Data class to hold Follia module information for a user request.
    """
    VIRTUAL_ASSISTANT = "virtual_assistant"
    DATA_EXTRACTION = "data_extraction"