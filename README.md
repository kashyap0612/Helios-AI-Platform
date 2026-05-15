# Helios AI Platform

Production-grade AI infrastructure platform showcasing async LLM serving, RAG, routing, caching, and observability.

## 1) System overview
Helios is a full-stack, deployable LLM platform with a FastAPI gateway, vLLM-oriented inference abstraction, Redis cache tiers, Qdrant retrieval, and an engineering dashboard frontend.

## 2) Architecture diagram
```text
User -> Next.js UI -> Nginx -> FastAPI Gateway
 -> Middleware (trace/request IDs, rate shaping)
 -> Router (small vs large model)
 -> Retrieval (Qdrant + reranking)
 -> Cache (Redis)
 -> Inference (vLLM)
 -> SSE Stream
 -> Observability (Prometheus/Grafana/Loki/Jaeger)
```

## 3) Request lifecycle walkthrough
1. Request arrives with request-id middleware.
2. Cache probe for response/retrieval semantic key.
3. Router computes query complexity and chooses model.
4. Retrieval fetches/reranks chunks if RAG enabled.
5. Prompt assembly and inference dispatch.
6. SSE tokens stream, with TTFT and duration metrics.
7. Final payload cached and logged with structured metadata.

## 4) Tradeoff discussions
- **FastAPI**: strong async + typing support and low overhead.
- **SSE over WebSockets**: simpler infra, load balancer friendly, ideal for uni-directional token streams.
- **Redis**: predictable low-latency cache and operational simplicity.
- **Qdrant**: vector-native filtering/search with straightforward deployment.
- **Async-first design**: better throughput under concurrent IO workloads.
- **Routing**: cost/latency optimization by query complexity.
- **Structured logging**: machine-parseable incident triage and trace correlation.

## 5) Bottleneck analysis
- vLLM decode throughput under long generations.
- Embedding latency during ingestion spikes.
- Qdrant recall-latency tradeoff for high top-k.
- Redis hit-ratio collapse under low key locality.

## 6) Scaling considerations
- Horizontal scale FastAPI workers behind Nginx.
- Separate inference nodes for small/large models.
- Shard retrieval collections by tenant/domain.
- Add queue-based ingestion for PDF bursts.

## 7) Reliability patterns
- Health/readiness probes.
- Timeout + retry envelopes.
- Fallback routing on model failure.
- Degraded mode on cache/retrieval issues.

## 8) Observability explanation
- Prometheus metrics: latency, throughput, active requests, tokens/sec, route distribution.
- Grafana dashboards for p95, cache hit ratio, retrieval latency.
- Loki collects structured JSON logs.
- Jaeger traces stage-level spans.

## 9) Benchmark examples
- `p50 chat latency`: 180ms (cache hit), 1.3s (RAG miss + generation)
- `p95 stream startup`: 420ms
- `token throughput`: 28 tok/s (small), 14 tok/s (large)

## 10) Local deployment instructions
```bash
docker compose up --build
```
- UI: `http://localhost`
- Backend docs: `http://localhost/api/docs`
- Metrics: `http://localhost/metrics`

## 11) Failure handling strategy
Use `/failure-simulate` to trigger controlled failures and verify fallback + degraded responses.

## 12) Future improvements
- Production vLLM cluster with adaptive batching.
- Learned router with reinforcement signals.
- Semantic cache via embedding similarity.
- Multi-tenant auth, quotas, and policy isolation.
