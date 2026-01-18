from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    user_context: Optional[str] = None  # e.g., "new employee", "manager"

class PolicySource(BaseModel):
    filename: str
    content_snippet: str
    similarity_score: float

class QueryResponse(BaseModel):
    answer: str
    model_used: str
    sources: List[PolicySource]
    ambiguity_detected: bool = False
    is_sensitive: bool = False
    warning_message: Optional[str] = None
