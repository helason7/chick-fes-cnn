import time
import torch
from fastapi import APIRouter

from helpers.clip_gate import is_clip_loaded
from helpers.cnn_predict import is_cnn_loaded
from app import APP_START_TIME

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    uptime = int(time.time() - APP_START_TIME)

    return {
        "status": "ok",
        "service": "Chicken Feces Disease Predictor",
        "version": "v1",
        "uptime_seconds": uptime,
        "models": {
            "clip": "loaded" if is_clip_loaded() else "not_loaded",
            "cnn": "loaded" if is_cnn_loaded() else "not_loaded"
        },
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }
