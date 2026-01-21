from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter(prefix="/v1", tags=["Track v1"])

@router.post("/track/affiliate-click")
def track_affiliate_click(payload: dict):
    """
    payload:
    {
      product_id: 1,
      disease_slug: "tetelo",
      platform: "shopee",
      confidence: 0.994
    }
    """
    supabase.table("affiliate_click_logs").insert({
        "product_id": payload.get("product_id"),
        "disease_slug": payload.get("disease_slug"),
        "platform": payload.get("platform"),
        "confidence": payload.get("confidence")
    }).execute()

    # ⚡ jangan return data berat
    return {"status": "ok"}
