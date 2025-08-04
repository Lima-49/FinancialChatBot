from fastapi import HTTPException, Header

from app.core.config import get_env_variable

API_KEY_CREDITS = {get_env_variable("API_KEY"): 5}

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=403, detail="API key is invalid or has no credits left")
    return x_api_key