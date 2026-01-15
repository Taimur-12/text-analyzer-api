import hmac
import hashlib
import os
import secrets
from app.config import API_KEY_SECRET

def generate_api_key() -> str:
    return "sk_" + secrets.token_urlsafe(32)

def hash_api_key(api_key: str) -> str:
    return hmac.new(
        API_KEY_SECRET.encode(),
        api_key.encode(),
        hashlib.sha256
    ).hexdigest()