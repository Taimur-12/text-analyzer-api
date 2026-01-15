from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import TextAnalysis, APIKey
from app.quota import DAILY_REQUEST_LIMIT, reset_llm_quota
from app.llm.service import analyze_with_llm
import logging
import time

logging.basicConfig(
    level = logging.INFO
)

logger = logging.getLogger(__name__)

sia = SentimentIntensityAnalyzer()

def classical_analysis(text: str) -> dict:
    tokens = word_tokenize(text)
    scores = sia.polarity_scores(text)
    compound = scores["compound"]

    if compound > 0.05:
        label = "positive"
    elif compound < -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {"word_count" : len(tokens),
                "char_count" : len(text),
                "sentiment" :{
                    "label" : label,
                    "score" : compound
                }
            }

def analyze_text(text: str, db: Session, use_llm: bool, api_key: APIKey, request_id: str) -> dict:
    logger.info(
        f"[request_id={request_id}] Analysis started | use_llm={use_llm}"
    )
    try:
        base_result = classical_analysis(text)
        llm_result = None
        llm_latency_ms = None

        if use_llm:
            api_key = db.merge(api_key)
            reset_llm_quota(api_key)

            if api_key.llm_requests_today >= DAILY_REQUEST_LIMIT:
                raise HTTPException(
                    status_code=429,
                    detail="Daily LLM quota exceeded"
                )

            start = time.perf_counter()
            llm_result = analyze_with_llm(text)
            llm_latency_ms = int((time.perf_counter() - start) * 1000)
            llm_result["latency_ms"] = llm_latency_ms

            api_key.llm_requests_today += 1
            db.commit()

        result = {
            "request_id": request_id,
            **base_result,
            "llm": llm_result,
            "model": {
                "type": "openai" if use_llm else "classical",
                "name": "gpt-4o-mini" if use_llm else "vader",
                "version": "1.0"
            }
        }

        record = TextAnalysis(text=text, result=result)
        db.add(record)
        db.commit()
        db.refresh(record)

        return result

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        logger.exception("Text analysis failed")
        raise HTTPException(
            status_code=500,
            detail="Text Analysis Failed"
        )
