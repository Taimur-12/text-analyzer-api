from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from datetime import datetime
from app.database import Base


class TextAnalysis(Base):
    __tablename__ = "text_analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash= Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)

    usage_count = Column(Integer, default=0)
    llm_requests_today = Column(Integer, default=0)
    llm_last_reset = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)