"""
Pydantic models for API requests.
"""
from pydantic import BaseModel

class MatchRequest(BaseModel):
    cv_text: str
    jd_text: str
