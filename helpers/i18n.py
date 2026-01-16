from config.config import MESSAGES, SUGGESTIONS


def get_message(key: str, lang: str | None = "id"):
    print("DEBUG i18n key:", repr(key))
    print("DEBUG available keys:", list(MESSAGES.keys()))

    msg = MESSAGES.get(key)

    if not msg:
        return f"Unknown message key: {key}"

    if not lang:
        lang = "id"

    return msg.get(lang) or msg.get("en")

def get_suggestion(key: str, lang: str = "id"):
    sug = SUGGESTIONS.get(key, {})
    return sug.get(lang, sug.get("en", ""))

def assert_message_key_exists(key: str):
    if key not in MESSAGES:
        raise RuntimeError(f"Message key not defined: {key}")
