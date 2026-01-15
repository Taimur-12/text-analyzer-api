from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from app.schemas import TextRequest, TextResponse
from app.services import analyze_text
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import TextAnalysis, APIKey
from app.auth import verify_api
from app.security import hash_api_key, generate_api_key
import time, logging, uuid
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def rate_limit_exceeded():
    raise HTTPException(
        status_code=429,
        detail="too many requests"
    )

app = FastAPI(title="Text Analyzer API")

@app.on_event("startup")
def on_startup():
    from app.database import engine
    from app.models import Base
    retries = 5
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connection successful!")
            break
        except OperationalError:
            retries -= 1
            print(f"Waiting for database... ({retries} retries left)")
            time.sleep(2)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request);
    response.headers["X-Request-ID"] = request_id
    return response

@app.post("/api/v1/analyze", response_model = TextResponse)
def analyze(
    body : TextRequest, 
    request: Request,
    db:Session = Depends(get_db), 
    api_key = Depends(verify_api),
):
    return analyze_text(body.text, db, body.use_llm, api_key, request.state.request_id)

@app.get("/api/v1/history")
def history(
    limit: int = 10, 
    offset: int =0, 
    db:Session = Depends(get_db),
    api_key = Depends(verify_api)
):
    records = (db.query(TextAnalysis)
    .order_by(TextAnalysis.created_at.desc())
    .offset(offset)
    .limit(limit)
    .all()
    )
    return records

@app.post("/api/v1/keys")
def keys(db:Session = Depends(get_db)):
    raw_key = generate_api_key()
    hashed = hash_api_key(raw_key)

    api_key = APIKey(key_hash = hashed)
    db.add(api_key)
    db.commit()

    return {
        "api_key" : raw_key,
        "warning" : "Store this key securely. It will not be shown again."
    }

@app.get("/health")
def health():
    return {"status" : "ok"}
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    if isinstance(exc, HTTPException):
        raise exc
    
    logger.exception("Unhandled exception occured")

    return JSONResponse(
        status_code = 500,
        content={
            "detail": "Internal server error"
        }
    )
