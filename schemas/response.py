from typing import Optional, List
from pydantic import BaseModel


# =========================
# DATA
# =========================
class AffiliateLink(BaseModel):
    platform: str
    url: str

class ProductRecommendation(BaseModel):
    name: str
    product_id: int
    category: str
    reason: str
    priority: int
    affiliate: Optional[AffiliateLink]

# class ProductRecommendation(BaseModel):
#     name: str
#     category: str
#     reason: str
#     priority: int

class PredictionData(BaseModel):
    class_index: int
    class_name: str
    slug: str
    confidence: float
    advice: List[str]
    recommendations: List[ProductRecommendation]
    disclaimer: str


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
