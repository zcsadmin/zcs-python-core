from typing import List
from dataclasses import dataclass

@dataclass
class QaInfo:
    """
    Data class to hold QA information.
    """
    agent_id: str = None
    session_id: str = None
    datasource_ids: List[str] = None
    interaction_id: str = None
