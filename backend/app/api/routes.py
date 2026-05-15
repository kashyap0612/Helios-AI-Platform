import hashlib
import time
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import PlainTextResponse, StreamingResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.cache.redis_cache import RedisCache
from app.routing.model_router import ModelRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.retrieval.pipeline import RetrievalPipeline
from app.services.inference import InferenceService
from app.streaming.sse import sse_event
from app.observability.metrics import CACHE_HIT, CACHE_MISS, ROUTING_DIST, STREAM_DURATION, TOKENS_STREAMED

router = APIRouter()
cache = RedisCache()
model_router = ModelRouter()
retrieval = RetrievalPipeline()
inference = InferenceService()


@router.get('/health')
async def health():
    return {'status': 'ok'}


@router.get('/ready')
async def ready():
    return {'ready': True}


@router.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):
    cache_key = 'resp:' + hashlib.sha256(req.query.encode()).hexdigest()
    cached = await cache.get_json(cache_key)
    if cached:
        CACHE_HIT.labels(cache='response').inc()
        return ChatResponse(**cached)
    CACHE_MISS.labels(cache='response').inc()

    decision = model_router.route(req.query, req.model_hint)
    ROUTING_DIST.labels(model=decision.model).inc()
    chunks, retrieval_latency = await retrieval.retrieve(req.query) if req.use_rag else ([], 0.0)
    prompt = req.query + '\n\n' + '\n'.join([c.text for c in chunks])
    answer = await inference.complete(decision.model, prompt)
    payload = ChatResponse(answer=answer, model=decision.model, cached=False, retrieval_latency_ms=retrieval_latency, chunks=chunks, routing_reason=decision.reason)
    await cache.set_json(cache_key, payload.model_dump())
    return payload


@router.post('/stream')
async def stream(req: ChatRequest):
    decision = model_router.route(req.query, req.model_hint)
    async def gen():
        start = time.perf_counter()
        yield sse_event('routing', {'model': decision.model, 'reason': decision.reason, 'confidence': decision.confidence})
        async for token in inference.stream(decision.model, req.query):
            TOKENS_STREAMED.labels(model=decision.model).inc()
            yield sse_event('token', {'token': token})
        STREAM_DURATION.labels(model=decision.model).observe(time.perf_counter() - start)
        yield sse_event('done', {'ok': True})
    return StreamingResponse(gen(), media_type='text/event-stream')


@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, 'Only PDF files are supported')
    return {'ingested': file.filename, 'status': 'queued'}


@router.post('/retrieve')
async def retrieve(req: ChatRequest):
    chunks, latency = await retrieval.retrieve(req.query)
    return {'chunks': [c.model_dump() for c in chunks], 'latency_ms': latency}


@router.get('/routing-debug')
async def routing_debug(query: str):
    d = model_router.route(query)
    return d.__dict__


@router.post('/failure-simulate')
async def failure_simulate(kind: str):
    if kind not in {'model_crash', 'redis_outage', 'timeout', 'retrieval_failure'}:
        raise HTTPException(400, 'Unsupported failure kind')
    return {'simulated': kind, 'fallback_activated': True}


@router.get('/metrics')
async def metrics():
    return PlainTextResponse(generate_latest().decode(), media_type=CONTENT_TYPE_LATEST)
