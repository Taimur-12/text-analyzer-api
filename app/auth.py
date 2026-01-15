from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import APIKey
from app.security import hash_api_key

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_api(
        x_api_key: str = Header(...), 
        db: Session = Depends(get_db)
):
    hashed_key = hash_api_key(x_api_key)

    api_key = (
        db.query(APIKey)
        .filter(APIKey.key_hash == hashed_key, APIKey.is_active == True)
        .first()
    )

    if not api_key:
        raise HTTPException(
            status_code = 401,
            detail="Invalid or missing API key"
        )
    
    api_key.usage_count += 1
    db.commit()

    return api_key