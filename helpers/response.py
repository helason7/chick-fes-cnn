def api_response(status, message, data=None, meta=None):
    return {
        "status": status,
        "message": message,
        "data": data,
        "meta": meta
    }
