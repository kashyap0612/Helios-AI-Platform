import time
from app.schemas.chat import RetrievedChunk
from app.observability.metrics import RETRIEVAL_LATENCY


class RetrievalPipeline:
    async def retrieve(self, query: str) -> tuple[list[RetrievedChunk], float]:
        start = time.perf_counter()
        # Placeholder retrieval logic; production uses embeddings + Qdrant similarity search + reranking.
        chunks = [
            RetrievedChunk(id='chunk-1', text=f'Contextual info for: {query[:80]}', score=0.91, source='demo.pdf'),
            RetrievedChunk(id='chunk-2', text='Fallback chunk for robustness and recall.', score=0.73, source='demo.pdf'),
        ]
        latency_ms = (time.perf_counter() - start) * 1000
        RETRIEVAL_LATENCY.observe(latency_ms / 1000)
        return chunks, latency_ms
