from typing import Optional, List
from pydantic import BaseModel


# =========================
# DATA
# =========================

class PredictionData(BaseModel):
    class_index: int
    class_name: str
    confidence: float
    advice: List[str]


class UncertainData(BaseModel):
    predicted_class_index: int
    predicted_class_name: str
    confidence: float


# =========================
# META
# =========================

class MetaData(BaseModel):
    language: Optional[str] = None
    clip_similarity: Optional[float] = None
    suggestion: Optional[str] = None


# =========================
# RESPONSES
# =========================

class AcceptedResponse(BaseModel):
    status: str
    message: str
    data: PredictionData
    meta: MetaData


class UncertainResponse(BaseModel):
    status: str
    message: str
    data: UncertainData
    meta: MetaData


class RejectedResponse(BaseModel):
    status: str
    message: str
    data: None = None
    meta: MetaData
