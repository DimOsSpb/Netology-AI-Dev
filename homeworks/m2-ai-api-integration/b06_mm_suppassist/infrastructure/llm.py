"""Клиент LLM с retry (tenacity) и fallback.

Все провайдеры работают через OpenAI-совместимый API.
Цепочка: primary → fallback → эскалация на оператора.
"""

from __future__ import annotations

from collections.abc import Iterator

from config import Settings
from core.classification import heuristic_classify
from loguru import logger
from models import Category, LLMResult
from openai import APIStatusError, OpenAI, RateLimitError
from openai.types.chat import ChatCompletionMessageParam
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

# Ответ-заглушка, когда ни один провайдер не дал полезный ответ
FALLBACK_ANSWER = "Передаю вопрос специалисту."


def _build_client(api_key: str | None, base_url: str | None) -> OpenAI | None:
    """Создаёт OpenAI-совместимый клиент, если есть ключ."""
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=base_url)


class RobustLLMClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.primary = _build_client(settings.api_key, settings.base_url)
        self.fallback = _build_client(
            settings.fallback_api_key, settings.fallback_base_url
        )

    # ── Цепочка провайдеров ───────────────────────────────────────────

    def _provider_chain(self) -> Iterator[tuple[OpenAI, str, bool]]:
        """Отдаёт (client, model, used_fallback) для каждого доступного провайдера."""
        if self.primary is not None:
            yield self.primary, self.settings.primary_model, False
        if self.fallback is not None and self.settings.fallback_model:
            yield self.fallback, self.settings.fallback_model, True

    # ── Публичные методы ──────────────────────────────────────────────

    def classify(self, messages: list[ChatCompletionMessageParam]) -> Category:
        """Классифицирует запрос: primary → fallback → эвристика."""
        for client, model, _ in self._provider_chain():
            try:
                raw = self._call(client, model, messages, temperature=0, max_tokens=64)
                return Category(raw.strip().lower())
            except Exception as e:
                logger.warning("[classify] - Провайдер {} недоступен: {}", model, e)  # noqa: S112
                continue

        # Безопасно извлекаем контент последнего сообщения
        last_content = messages[-1].get("content") if messages else ""
        text_content = ""

        if isinstance(last_content, str):
            text_content = last_content
        elif isinstance(last_content, list):
            # Если это мультимодальный контент (список), собираем все текстовые части
            text_parts = []
            for part in last_content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    text_parts.append(part)
            text_content = " ".join(text_parts)

        # Теперь text_content гарантированно имеет тип str
        return heuristic_classify(text_content)

    def answer(self, messages: list[ChatCompletionMessageParam]) -> LLMResult:
        """Получает ответ: primary → fallback → эскалация."""
        for client, model, used_fallback in self._provider_chain():
            try:
                if used_fallback:
                    logger.info("Переключаюсь на fallback: {}", model)
                text, tokens = self._answer_from(client, model, messages)
                return LLMResult(
                    text,
                    tokens,
                    "fallback" if used_fallback else "primary",
                    model,
                    used_fallback,
                )
            except Exception as e:
                logger.warning("[answer] Провайдер {} недоступен: {}", model, e)

        # Все провайдеры недоступны — переводим на оператора
        return LLMResult(FALLBACK_ANSWER, 0, "escalation", "none", True)

    def transcribe(self, audio_path: str, stt_model: str) -> str:
        """STT: аудиофайл → текст через audio.transcriptions."""
        client = self.primary or self.fallback
        if client is None:
            return ""
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model=stt_model,
                file=f,
                language="ru",
                response_format="text",
            )
        return transcript

    # ── Внутренние методы ─────────────────────────────────────────────

    def _answer_from(
        self,
        client: OpenAI,
        model: str,
        messages: list[ChatCompletionMessageParam],
    ) -> tuple[str, int]:
        """Один ответ от провайдера. Возвращает (текст, токены)."""
        text = self._call(client, model, messages)
        return (text or FALLBACK_ANSWER), 0

    def _call(
        self,
        client: OpenAI,
        model: str,
        messages: list[ChatCompletionMessageParam],
        temperature: float = 0.2,
        max_tokens: int = 250,
    ) -> str:
        """Вызов LLM с retry через tenacity (экспоненциальная задержка)."""

        def should_retry(error: BaseException) -> bool:
            if isinstance(error, RateLimitError):
                return True
            if isinstance(error, APIStatusError) and error.status_code >= 500:
                return True
            return False

        @retry(
            wait=wait_exponential(multiplier=1, min=1, max=60),
            stop=stop_after_attempt(5),
            retry=retry_if_exception(should_retry),
            reraise=True,
        )
        def _do() -> str:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=self.settings.request_timeout_seconds,
            )
            return (response.choices[0].message.content or "").strip()

        return _do()
