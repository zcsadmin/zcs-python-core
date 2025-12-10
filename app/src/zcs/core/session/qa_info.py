from dataclasses import dataclass

@dataclass
class QaInfo:
    """
    Data class to hold QA information.
    """
    agent_id: str = None
    session_id: str = None
    datasource_id: str = None
    interaction_id: str = None
