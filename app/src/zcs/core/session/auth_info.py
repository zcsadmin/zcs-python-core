from dataclasses import dataclass


@dataclass
class AuthInfo:
    """
    Data class to hold authentication information for a user request.
    """
    client_id: str = None
    tenant_id: str = None
    company_id: str = None
    user_id: str = None
    user_email: str = None
