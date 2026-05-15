import json
from redis.asyncio import Redis
from app.config.settings import settings


class RedisCache:
    def __init__(self) -> None:
        self.client = Redis.from_url(settings.redis_url, encoding='utf-8', decode_responses=True)

    async def get_json(self, key: str):
        data = await self.client.get(key)
        return json.loads(data) if data else None

    async def set_json(self, key: str, value: dict, ttl: int | None = None):
        await self.client.set(key, json.dumps(value), ex=ttl or settings.cache_ttl_sec)
