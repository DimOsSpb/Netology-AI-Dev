# Slide: Redis: production-решение

import hashlib
import json
from typing import Any, final

import redis
from loguru import logger
from openai.types.chat import ChatCompletionMessageParam


@final
class RedisCache:
    """Production-кеш на Redis."""

    def __init__(
        self, host: str = "localhost", port: int = 6379, ttl: int = 3600
    ) -> None:
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.ttl = ttl

    def _make_key(
        self, model: str, messages: list[ChatCompletionMessageParam], temperature: float
    ) -> str:
        data = json.dumps(
            {"model": model, "messages": messages, "temperature": temperature},
            sort_keys=True,
            ensure_ascii=False,
        )
        return f"llm:{hashlib.sha256(data.encode()).hexdigest()}"

    def get(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        temperature: float = 0,
    ) -> bytes | str | None:
        key = self._make_key(model, messages, temperature)
        value = self.client.get(key)
        if value is not None:
            logger.debug("Cache hit: {}", key)
        else:
            logger.debug("Cache miss: {}", key)
        return value

    def set(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        temperature: float,
        response: str,
    ) -> None:
        key = self._make_key(model, messages, temperature)
        _ = self.client.setex(key, self.ttl, response)
        logger.debug("Cached with TTL={}s: {}", self.ttl, key)

    def stats(self) -> dict[str, str | int]:
        info: dict[str, Any] = self.client.info("stats")
        # Принудительно приводим к int, так как Redis возвращает данные в виде строк
        hits = int(info.get("keyspace_hits", 0))
        misses = int(info.get("keyspace_misses", 0))
        total = hits + misses
        return {
            "hits": hits,
            "misses": misses,
            "hit_rate": f"{(hits / total * 100):.1f}%" if total else "N/A",
            "keys": int(self.client.dbsize()),  # На всякий случай приводим dbsize к int
        }
