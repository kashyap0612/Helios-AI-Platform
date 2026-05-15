import asyncio
from collections.abc import AsyncIterator


class InferenceService:
    async def complete(self, model: str, prompt: str) -> str:
        await asyncio.sleep(0.05)
        return f'[{model}] Generated answer for: {prompt[:200]}'

    async def stream(self, model: str, prompt: str) -> AsyncIterator[str]:
        tokens = (f'[{model}]', ' streaming', ' response', ' for ', prompt[:40])
        for tok in tokens:
            await asyncio.sleep(0.04)
            yield tok
