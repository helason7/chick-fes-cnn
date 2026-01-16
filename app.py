import time

APP_START_TIME = time.time()
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app_logging.logger import setup_logger

from helpers.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    rate_limit_exception_handler
)

from helpers.clip_gate import load_clip
from helpers.cnn_predict import load_cnn
from api.v1.predict import router as predict_v1_router
from api.health import router as health_v1_router

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from helpers.limiter import limiter

@asynccontextmanager
async def lifespan(app):
    # ===== STARTUP =====

    load_clip()
    load_cnn()
    print("✅ Models loaded")

    yield  # aplikasi berjalan di sini

    # ===== SHUTDOWN =====
    print("🛑 Application shutting down")


app = FastAPI(
    title="Chicken Feces Disease Predictor API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

logger = setup_logger()

# Register API v1
app.include_router(predict_v1_router)
app.include_router(health_v1_router)


@app.get("/")
def root():
    return {
        "message": "Chicken Feces Disease Predictor API",
        "available_versions": ["v1"]
    }
