from prometheus_client import Counter, Gauge, Histogram

REQUEST_LATENCY = Histogram('helios_request_latency_seconds', 'End-to-end request latency', ['endpoint'])
RETRIEVAL_LATENCY = Histogram('helios_retrieval_latency_seconds', 'Retrieval latency seconds')
STREAM_DURATION = Histogram('helios_stream_duration_seconds', 'Streaming duration seconds', ['model'])
REQUEST_COUNT = Counter('helios_requests_total', 'Total request count', ['endpoint', 'status'])
CACHE_HIT = Counter('helios_cache_hits_total', 'Cache hits', ['cache'])
CACHE_MISS = Counter('helios_cache_miss_total', 'Cache misses', ['cache'])
TOKENS_STREAMED = Counter('helios_tokens_streamed_total', 'Total streamed tokens', ['model'])
ACTIVE_REQUESTS = Gauge('helios_active_requests', 'Number of active requests')
ROUTING_DIST = Counter('helios_routing_decisions_total', 'Routing model distribution', ['model'])
