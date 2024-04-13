_APPID = None


def set_appid(appid: str | None = None):
    global _APPID
    _APPID = appid


def get_appid():
    return _APPID


def _check_appid():
    """Check if APP ID is not None."""
    if _APPID is None:
        raise ValueError("APP ID is not set.")
