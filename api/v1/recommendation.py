from fastapi import APIRouter, HTTPException
from supabase_client import supabase

router = APIRouter(prefix="/v1", tags=["Recommendation v1"])

CONFIDENCE_THRESHOLD = 0.7

@router.post("/recommendation")
def recommend(payload: dict):
    disease_slug = payload.get("disease_slug")
    confidence = payload.get("confidence", 0)

    if confidence < CONFIDENCE_THRESHOLD:
        raise HTTPException(
            status_code=400,
            detail="Confidence terlalu rendah untuk rekomendasi"
        )

    if disease_slug == "healthy":
        return {
            "disease": "Healthy",
            "severity": "low",
            "recommendations": []
        }

    # Ambil problem
    problem = (
        supabase.table("problems")
        .select("id, name, severity")
        .eq("slug", disease_slug)
        .single()
        .execute()
    )

    if not problem.data:
        raise HTTPException(status_code=404, detail="Penyakit tidak ditemukan")

    problem_id = problem.data["id"]

    # Ambil rekomendasi produk
    rules = (
        supabase.table("product_rules")
        .select(
            "priority, reason, products(name, category)"
        )
        .eq("problem_id", problem_id)
        .order("priority", desc=True)
        .execute()
    )

    recommendations = [
        {
            "name": r["products"]["name"],
            "category": r["products"]["category"],
            "reason": r["reason"],
            "priority": r["priority"]
        }
        for r in rules.data
    ]

    return {
        "disease": problem.data["name"],
        "severity": problem.data["severity"],
        "recommendations": recommendations
    }

def get_recommendation(disease_slug: str, confidence: float):
    # Rule confidence
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "severity": None,
            "recommendations": []
        }

    # Rule healthy
    if disease_slug == "healthy":
        return {
            "severity": "low",
            "recommendations": []
        }

    # Ambil problem
    problem = (
        supabase.table("problems")
        .select("id, name, severity")
        .eq("slug", disease_slug)
        .single()
        .execute()
    )

    if not problem.data:
        return {
            "severity": None,
            "recommendations": []
        }

    problem_id = problem.data["id"]
    severity = problem.data["severity"]

    # Ambil rules
    rules = (
        supabase.table("product_rules")
        .select("""
            priority,
            reason,
            product_id,
            products(
                name,
                category,
                product_affiliates(
                    platform,
                    url,
                    is_active
                )
            )
        """)
        .eq("problem_id", problem_id)
        .order("priority", desc=True)
        .execute()
    )


    # Dedup produk (ambil priority tertinggi)
    unique = {}

    for r in rules.data:
        product = r["products"]
        product_name = product["name"]

        if product_name not in unique:
            affiliates = product.get("product_affiliates", [])
            active_affiliate = next(
                (a for a in affiliates if a["is_active"]),
                None
            )

            unique[product_name] = {
                "name": product_name,
                "product_id": r["product_id"],
                "category": product["category"],
                "reason": r["reason"],
                "priority": r["priority"],
                "affiliate": active_affiliate
            }

    recommendations = list(unique.values())

    return {
        "severity": severity,
        "recommendations": recommendations
    }