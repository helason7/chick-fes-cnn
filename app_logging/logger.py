import logging
import json
import uuid
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "event": getattr(record, "event", record.msg),
            "message": record.getMessage(),
        }

        # Optional extra fields
        for field in [
            "request_id",
            "status",
            "clip_similarity",
            "class_index",
            "confidence",
            "language",
            "error_code",
        ]:
            if hasattr(record, field):
                log_record[field] = getattr(record, field)

        return json.dumps(log_record)


def setup_logger():
    logger = logging.getLogger("chick-fes")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.handlers = []
    logger.addHandler(handler)

    return logger


def generate_request_id():
    return str(uuid.uuid4())
