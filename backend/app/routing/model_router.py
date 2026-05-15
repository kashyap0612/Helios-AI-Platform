from dataclasses import dataclass
from app.config.settings import settings


@dataclass
class RoutingDecision:
    model: str
    reason: str
    confidence: float


class ModelRouter:
    def route(self, query: str, hint: str = 'auto') -> RoutingDecision:
        if hint == 'small':
            return RoutingDecision(settings.vllm_small_model, 'User override to small model', 1.0)
        if hint == 'large':
            return RoutingDecision(settings.vllm_large_model, 'User override to large model', 1.0)

        complexity = len(query.split()) + query.count('?') * 2
        if complexity < 18:
            return RoutingDecision(settings.vllm_small_model, 'Low complexity query routed to low-latency model', 0.82)
        return RoutingDecision(settings.vllm_large_model, 'Higher complexity query routed to higher-quality model', 0.79)
