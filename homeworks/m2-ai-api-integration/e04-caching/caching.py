import time
from typing import Any

from config import ProviderSettings, settings
from loguru import logger
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    OpenAI,
    RateLimitError,
    Stream,
)
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageParam
from redis_cache import RedisCache
from simple_cache import SimpleCache
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

# Примерные цены за 1M токенов (для логирования стоимости)
PRICES_PER_1M_TOKENS: dict[str, dict[str, float]] = {
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
    "anthropic/claude-opus-4.8-fast": {"input": 10, "output": 50},
    "qwen2:1.5b": {"input": 0.0, "output": 0.0},
    "openai/gpt-oss-120b:free": {"input": 0.0, "output": 0.0},
}


class SessionCostTracker:
    """Подсчитывает общую стоимость всех запросов за сессию."""

    def __init__(self) -> None:
        self.total_cost = 0.0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.request_count = 0

    def log_usage(self, model: str, prompt_tokens: int, completion_tokens: int) -> None:
        """Записывает usage одного запроса и выводит стоимость."""
        price = PRICES_PER_1M_TOKENS.get(model, {"input": 1.00, "output": 3.00})

        cost_input = prompt_tokens / 1_000_000 * price["input"]
        cost_output = completion_tokens / 1_000_000 * price["output"]
        cost = cost_input + cost_output

        self.total_cost += cost
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.request_count += 1

        print(
            f"  [Токены: {prompt_tokens}+{completion_tokens} | "
            f"Стоимость: ${cost:.6f} | "
            f"За сессию: ${self.total_cost:.6f}]"
        )

    def summary(self) -> None:
        """Выводит итоговую статистику сессии."""
        print(f"\n{'=' * 50}")
        print("Итого за сессию:")
        print(f"  Запросов: {self.request_count}")
        print(
            f"  Токенов: {self.total_prompt_tokens} input + {self.total_completion_tokens} output"
        )
        print(f"  Общая стоимость: ${self.total_cost:.6f}")
        print(f"{'=' * 50}")


# Кеш: Redis с fallback на SimpleCache
# --------------------------------------------------------------------------


def build_cache() -> RedisCache | SimpleCache:
    """Создаёт Redis-кеш, при недоступности — fallback на SimpleCache."""
    try:
        cache = RedisCache(ttl=3600)
        cache.client.ping()
        logger.info("Кеш: Redis (TTL=3600s)")
        return cache
    except Exception:
        logger.warning("Redis недоступен, используется SimpleCache (in-memory)")
        return SimpleCache(ttl_seconds=3600)


def print_cache_stats(cache: RedisCache | SimpleCache) -> None:
    """Выводит статистику кеша."""
    if isinstance(cache, RedisCache):
        stats = cache.stats()
        logger.info(
            "Cache stats: keys={}, hits={}, misses={}, hit_rate={}",
            stats["keys"],
            stats["hits"],
            stats["misses"],
            stats["hit_rate"],
        )
    else:
        logger.info(
            "Cache stats: keys={}, hits={}, misses={}, hit_rate={:.1f}%",
            len(cache._cache),
            cache.hits,
            cache.misses,
            cache.hit_rate,
        )


def clear_cache(cache: RedisCache | SimpleCache) -> None:
    """Очищает кеш."""
    if isinstance(cache, RedisCache):
        deleted = 0
        for key in cache.client.scan_iter("llm:*"):
            cache.client.delete(key)
            deleted += 1
        logger.info("Удалено ключей из Redis: {}", deleted)
    else:
        cache._cache.clear()
        cache.hits = 0
        cache.misses = 0
        logger.info("SimpleCache очищен")


def build_client(provider: ProviderSettings) -> OpenAI:
    if not provider.api_key:
        raise SystemExit(
            f"Не найден {provider.env_key} в переменных окружения или .env"
        )
    if not provider.base_url:
        raise SystemExit(f"Для {provider.name} не определен base_url в конфигурации")
    return OpenAI(api_key=provider.api_key, base_url=provider.base_url)


def choose_provider() -> ProviderSettings:
    if settings.def_provider:
        print("\nАвтовыбор провайдера. ", end="")
        return settings.providers[settings.def_provider]
    print("Выберите провайдера:")
    for key, p in settings.providers.items():
        print(f"  {key}. {p.name} (модель: {p.model})")
    while True:
        choice = input("Номер провайдера: ").strip()
        if choice in settings.providers:
            return settings.providers[choice]
        print(f"Неверный выбор. Введите число от 1 до {len(settings.providers)}.")


def call_llm_with_retry(
    client: OpenAI, model: str, messages: list[ChatCompletionMessageParam]
) -> Any:  # noqa: E501

    # Функция-предикат: проверяет конкретные условия ошибки
    def should_retry(error: BaseException) -> bool:
        # print("- should_retry -")
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
    def _call() -> Stream[ChatCompletionChunk]:
        return client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            stream_options={"include_usage": True},
        )

    return _call()


def call_with_fallback(
    primary_client: OpenAI,
    primary_model: str,
    fallback_client: OpenAI | None,
    fallback_model: str | None,
    messages: list[ChatCompletionMessageParam],
) -> tuple[Any, str]:
    """Пробует основного провайдера, при неудаче — fallback."""
    try:
        return call_llm_with_retry(
            primary_client, primary_model, messages
        ), primary_model
    except (RateLimitError, APIError, APIConnectionError) as e:
        logger.warning("Основной провайдер недоступен: {}", e)

        if fallback_client and fallback_model:
            logger.info("Переключаюсь на fallback: {}", fallback_model)
            try:
                return call_llm_with_retry(
                    fallback_client, fallback_model, messages
                ), fallback_model
            except Exception as fallback_err:
                raise RuntimeError(
                    f"Оба провайдера недоступны. Fallback: {fallback_err}"
                ) from fallback_err
        raise


def chat_with_cache(
    client: OpenAI,
    model: str,
    messages: list[ChatCompletionMessageParam],
    cache: RedisCache | SimpleCache,
    fallback_client: OpenAI | None = None,
    fallback_model: str | None = None,
) -> tuple[str, str, float | None, Any | None]:
    """Запрос к LLM с кешированием.

    Ключ кеша строится по system-промпту + последнему сообщению пользователя,
    а не по всей истории — иначе один и тот же вопрос никогда не попадёт в кеш.

    Возвращает (ответ, использованная_модель, время_с, usage | None).
    """
    start = time.time()
    elapsed = None

    # Для кеша берём только system + последнее сообщение пользователя
    cache_messages: list[ChatCompletionMessageParam] = [
        m for m in messages if m["role"] == "system"
    ]
    cache_messages.append(messages[-1])

    # 1. Проверяем кеш
    cached = cache.get(model, cache_messages, temperature=0)
    if cached:
        elapsed = time.time() - start
        logger.info("Из кеша за {:.4f}s", elapsed)
        return str(cached), model, elapsed, None

    # 2. Запрос к API (передаём полную историю для контекста)
    response, used_model = call_with_fallback(
        client,
        model,
        fallback_client,
        fallback_model,
        messages,
    )

    full_response = ""
    usage = None

    for chunk in response:
        if chunk.choices:
            delta = chunk.choices[0].delta.content or ""
            delta = delta.replace("\ufeff", "")
            if delta:
                if not elapsed:
                    elapsed = time.time() - start
                full_response += delta
        if chunk.usage:
            usage = chunk.usage

    logger.info("API ответ за {:.2f}s", elapsed)

    # 3. Сохраняем в кеш
    cache.set(model, cache_messages, 0, full_response)

    return full_response, used_model, elapsed, usage


def main() -> None:

    # Выбор основного провайдера
    provider = choose_provider()
    primary_client = build_client(provider)
    primary_model = provider.model

    # Настройка fallback-провайдера (Ollama как бесплатный локальный запасной вариант)
    fallback_client: OpenAI | None = None
    fallback_model: str | None = None

    # Если основной провайдер — не Ollama, используем Ollama как fallback
    if provider.name != "Ollama (локальный)":
        try:
            fallback_provider = settings.providers["1"]  # Ollama
            fallback_client = build_client(fallback_provider)
            fallback_model = fallback_provider.model
            logger.info("Fallback: {} ({})", fallback_provider.name, fallback_model)
        except Exception:
            logger.warning("Fallback (Ollama) недоступен, работаем без резерва")

    logger.info("Провайдер: {}, модель: {}", provider.name, primary_model)

    # Кеш
    cache = build_cache()
    # Инициализация трекера стоимости
    tracker = SessionCostTracker()

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": "Ты - продавец. Отвечай только в этом направлении. Больше ничего не говори.",
        }
    ]

    print("Введите сообщение. Для выхода используйте exit или quit")

    while True:
        user_input = input("\nВы: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        if not user_input:
            logger.warning("Пустой ввод пропущен")
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            answer, used_model, elapsed, usage = chat_with_cache(
                client=primary_client,
                model=primary_model,
                messages=messages,
                cache=cache,
                fallback_client=fallback_client,
                fallback_model=fallback_model,
            )
        except RateLimitError:
            logger.error("Превышен лимит запросов. Попробуйте позже")
            messages.pop()
            continue
        except APIConnectionError:
            logger.error("Нет подключения к API. Проверьте интернет")
            messages.pop()
            continue
        except APIError as e:
            logger.error("Ошибка API: {}", e)
            messages.pop()
            continue
        except Exception as e:
            logger.error("Непредвиденная ошибка: {}", e)
            messages.pop()
            continue

        print(f"Ассистент: {answer}")

        if usage:
            tracker.log_usage(used_model, usage.prompt_tokens, usage.completion_tokens)

        messages.append({"role": "assistant", "content": answer})

    tracker.summary()
    logger.info("Диалог завершён")


if __name__ == "__main__":
    main()
