from dotenv import load_dotenv
load_dotenv()

import os

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

if not API_KEY_SECRET:
    raise RuntimeError("API_KEY_SECRET is not set")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

