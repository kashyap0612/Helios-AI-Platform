from pydantic import BaseModel, Field
from typing import Literal


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=8000)
    use_rag: bool = True
    model_hint: Literal['auto', 'small', 'large'] = 'auto'


class RetrievedChunk(BaseModel):
    id: str
    text: str
    score: float
    source: str


class ChatResponse(BaseModel):
    answer: str
    model: str
    cached: bool
    retrieval_latency_ms: float
    chunks: list[RetrievedChunk]
    routing_reason: str
