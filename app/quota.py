from datetime import datetime, timedelta
from app.models import APIKey

DAILY_REQUEST_LIMIT = 10

def reset_llm_quota(api_key: APIKey):
    if datetime.utcnow() - api_key.llm_last_reset >= timedelta(days=1):
        api_key.llm_last_reset = datetime.utcnow()
        api_key.llm_requests_today = 0
