from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app_logging.logger import generate_request_id, setup_logger
import os, io
from PIL import Image, UnidentifiedImageError

from config.config import (
    CLASS_MAP, DISEASE_ADVICE, CNN_MIN_CONFIDENCE, 
    MAX_UPLOAD_SIZE_BYTES, ALLOWED_MIME_TYPES, ALLOWED_EXTENSIONS
)
from helpers.clip_gate import is_chicken_feces
from helpers.cnn_predict import predict_disease
from helpers.response import api_response
from helpers.i18n import get_message, get_suggestion
from helpers.limiter import limiter
from config.config import RATE_LIMIT_PREDICT


from schemas.response import (
    AcceptedResponse,
    UncertainResponse,
    RejectedResponse
)
from typing import Union

logger = setup_logger()

router = APIRouter(prefix="/v1", tags=["Prediction v1"])

@router.post(
    "/predict",
    response_model=Union[
        AcceptedResponse,
        UncertainResponse,
        RejectedResponse
    ]
)
@limiter.limit(RATE_LIMIT_PREDICT)
async def predict(
    request: Request,  
    file: UploadFile = File(...),
    lang: str = "id"
):
    request_id = generate_request_id()

    # 1️⃣ MIME type validation
    if file.content_type not in ALLOWED_MIME_TYPES:
        logger.warning(
            "invalid_file_type",
            extra={
                "event": "invalid_file_type",
                "request_id": request_id,
                "status": "rejected",
                "content_type": file.content_type
            }
        )
        return api_response(
            status="error",
            message=get_message("invalid_file_type", lang),
            meta={
                "error_code": "INVALID_FILE_TYPE",
                "allowed_types": ALLOWED_MIME_TYPES
            }
        )
    
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        logger.warning(
            "invalid_file_extension",
            extra={
                "event": "invalid_file_extension",
                "request_id": request_id,
                "status": "rejected",
                "filename": file.filename
            }
        )
        return api_response(
            status="error",
            message=get_message("invalid_file_type", lang),
            meta={
                "error_code": "INVALID_FILE_EXTENSION",
                "allowed_extensions": ALLOWED_EXTENSIONS
            }
        )

    # Header-based size check (jika ada)
    content_length = file.headers.get("content-length")
    if content_length and int(content_length) > MAX_UPLOAD_SIZE_BYTES:
        logger.warning(
            "file_size_exceeded",
            extra={
                "event": "file_size_exceeded",
                "request_id": request_id,
                "status": "rejected",
                "content_length": int(content_length)
            }
        )
        return api_response(
            status="error",
            message=get_message("file_too_large", lang),
            meta={
                "error_code": "FILE_TOO_LARGE",
                "max_size_mb": MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)
            }
        )

    logger.info(
    "prediction_request_received",
    extra={
            "event": "prediction_request_received",
            "request_id": request_id,
            "language": lang
        }
    )

    image_bytes = await file.read()

    if len(image_bytes) > MAX_UPLOAD_SIZE_BYTES:
        logger.warning(
            "file_size_exceeded",
            extra={
                "event": "file_size_exceeded",
                "request_id": request_id,
                "status": "rejected",
                "actual_size": len(image_bytes)
            }
        )
        return api_response(
            status="error",
            message=get_message("file_too_large", lang),
            meta={
                "error_code": "FILE_TOO_LARGE",
                "max_size_mb": MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)
            }
        )
    
    # 3️⃣ Validate image integrity
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()  # validasi struktur file
    except UnidentifiedImageError:
        logger.warning(
            "invalid_image_content",
            extra={
                "event": "invalid_image_content",
                "request_id": request_id,
                "status": "rejected"
            }
        )
        return api_response(
            status="error",
            message=get_message("invalid_file_type", lang),
            meta={"error_code": "INVALID_IMAGE_CONTENT"}
        )

    # 1️⃣ CLIP gate
    is_feces, clip_score = is_chicken_feces(image_bytes)

    if not is_feces:
    
        logger.warning(
            "clip_rejected",
            extra={
                "event": "clip_rejected",
                "request_id": request_id,
                "clip_similarity": round(clip_score, 4),
                "status": "rejected"
            }
        )


        return api_response(
            status="rejected",
            message=get_message("not_feces", lang),
            data=None,
            meta={
                "language": lang,   # ← JANGAN NULL
                "clip_similarity": round(clip_score, 4)
            }
        )

    # 2️⃣ CNN prediction
    class_idx, confidence = predict_disease(image_bytes)
    label_info = CLASS_MAP.get(class_idx, {})
    class_name = label_info.get(lang, label_info.get("en", "Unknown"))

    # 3️⃣ Confidence check
    if confidence < CNN_MIN_CONFIDENCE:

        logger.warning(
            "low_cnn_confidence",
            extra={
                "event": "low_cnn_confidence",
                "request_id": request_id,
                "class_index": class_idx,
                "confidence": round(confidence, 4),
                "status": "uncertain"
            }
        )

        return api_response(
            status="uncertain",
            message=get_message("low_confidence", lang),
            data={
                "predicted_class_index": class_idx,
                "predicted_class_name": class_name,
                "confidence": round(confidence, 4)
            },
            meta={
                "language": lang,
                "clip_similarity": round(clip_score, 4),
                "suggestion": get_suggestion("retake_photo", lang)
            }
        )

    # 4️⃣ Advice
    advice_info = DISEASE_ADVICE.get(class_idx, {})
    advice = advice_info.get(lang, advice_info.get("en", {})).get("advice", [])
    
    logger.info(
        "prediction_success",
        extra={
            "event": "prediction_success",
            "request_id": request_id,
            "class_index": class_idx,
            "confidence": round(confidence, 4),
            "status": "accepted"
        }
    )

    return api_response(
        status="accepted",
        message=get_message("prediction_success", lang),
        data={
            "class_index": class_idx,
            "class_name": class_name,
            "confidence": round(confidence, 4),
            "advice": advice
        },
        meta={
            "language": lang,
            "clip_similarity": round(clip_score, 4)
        }
    )
