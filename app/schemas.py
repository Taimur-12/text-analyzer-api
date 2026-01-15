from pydantic import BaseModel, Field
from typing import Optional

class Sentiment(BaseModel):
    label: str
    score: float

class LLMResult(BaseModel):
    sentiment: str
    tone: str
    explanation: str

class ModelMeta(BaseModel):
    type: str
    name: str
    version: str

class TextRequest(BaseModel):
    text: str = Field(...,
        min_length = 1,
        max_length = 1500,
        description = "Input non-empty text (max 1500 characters)"
    )
    use_llm : bool = False

class TextResponse(BaseModel):
    word_count: int
    char_count: int
    sentiment: Sentiment
    llm: Optional[LLMResult] = None
    model: ModelMeta

