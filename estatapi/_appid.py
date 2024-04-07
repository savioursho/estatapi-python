_APPID = None

def set_appid(appid:str | None = None):
    global _APPID
    _APPID = appid

def get_appid():
    return _APPID
