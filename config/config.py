import os
from dotenv import load_dotenv
import torch

load_dotenv()

FECES_PROMPTS = [
    "chicken feces",
    "chicken droppings",
    "chicken poop"
]

# Environment
APP_ENV = os.getenv("APP_ENV", "development")

# Thresholds
CLIP_THRESHOLD = float(os.getenv("CLIP_THRESHOLD", 0.25))
CNN_MIN_CONFIDENCE = float(os.getenv("CNN_MIN_CONFIDENCE", 0.6))

# Device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# CNN
CNN_INPUT_SIZE = (150, 150)

# Upload limit
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 5))
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# Allowed image types
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png"]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# Rate limit
RATE_LIMIT_PREDICT = os.getenv("RATE_LIMIT_PREDICT", "10/minute")

# Class labels (multi language)
CLASS_MAP = {
    0: {"id": "Koksidiosis", "en": "Coccidiosis"},
    1: {"id": "Sehat", "en": "Healthy"},
    2: {"id": "Tetelo", "en": "New Castle Disease"},
    3: {"id": "Salmonella", "en": "Salmonella"}
}

SLUG_MAP = {
    0: "coccidiosis",
    1: "healthy",
    2: "tetelo",
    3: "salmonella"
}

# Advice per disease
DISEASE_ADVICE = {
    0: {
        "id": {
            "advice": [
                "Pisahkan ayam yang terinfeksi",
                "Jaga kebersihan kandang",
                "Berikan obat antikoksidia sesuai anjuran"
            ]
        },
        "en": {
            "advice": [
                "Isolate infected chickens",
                "Maintain coop hygiene",
                "Administer anticoccidial treatment as recommended"
            ]
        }
    },
    1: {
        "id": {
            "advice": [
                "Lanjutkan perawatan rutin",
                "Pastikan pakan dan air bersih",
                "Pantau kondisi ayam secara berkala"
            ]
        },
        "en": {
            "advice": [
                "Continue routine care",
                "Ensure clean feed and water",
                "Monitor chickens regularly"
            ]
        }
    },
    2: {
        "id": {
            "advice": [
                "Segera isolasi ayam yang sakit",
                "Batasi kontak dengan ayam lain",
                "Hubungi dokter hewan setempat"
            ]
        },
        "en": {
            "advice": [
                "Immediately isolate sick chickens",
                "Limit contact with other poultry",
                "Consult a veterinarian immediately"
            ]
        }
    },
    3: {
        "id": {
            "advice": [
                "Gunakan sarung tangan saat menangani ayam",
                "Bersihkan kandang secara menyeluruh",
                "Konsultasikan pengobatan dengan dokter hewan"
            ]
        },
        "en": {
            "advice": [
                "Wear gloves when handling chickens",
                "Thoroughly disinfect the coop",
                "Consult a veterinarian for treatment"
            ]
        }
    }
}
# ===============================
# Messages (i18n)
# ===============================

MESSAGES = {
    "prediction_success": {
        "id": "Prediksi berhasil",
        "en": "Prediction successful"
    },
    "not_feces": {
        "id": "Gambar yang diunggah bukan feses ayam",
        "en": "Uploaded image is not chicken feces"
    },
    "low_confidence": {
        "id": "Model tidak cukup yakin dengan hasil prediksi",
        "en": "Model confidence is too low"
    },
    "file_too_large": {
        "id": "Ukuran file terlalu besar. Maksimal 5 MB",
        "en": "File size is too large. Maximum allowed size is 5 MB"
    },
    "invalid_file_type": {
        "id": "Format file tidak didukung. Gunakan JPG atau PNG",
        "en": "Invalid file format. Only JPG or PNG are allowed"
    },
    "internal_error": {
        "id": "Terjadi kesalahan pada sistem",
        "en": "Internal server error"
    }
}

# ===============================
# Suggestions (i18n)
# ===============================

SUGGESTIONS = {
    "retake_photo": {
        "id": "Silakan ambil ulang foto dengan pencahayaan dan fokus yang lebih baik",
        "en": "Please retake the photo with better lighting and focus"
    }
}
