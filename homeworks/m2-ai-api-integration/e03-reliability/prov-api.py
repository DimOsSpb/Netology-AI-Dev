from typing import Any

from config import ProviderSettings, settings
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    OpenAI,
    RateLimitError,
    Stream,
)
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageParam
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
    """Вызов LLM с автоматическим retry через tenacity.

    Повторяет запрос при:
    - RateLimitError (429) — до 5 раз с экспоненциальной задержкой
    - APIStatusError с кодом 5xx — серверные ошибки
    """

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
) -> Any:
    """Пробует основного провайдера, при неудаче — fallback.

    Возвращает stream от первого успешного провайдера.
    """
    from openai import APIConnectionError, APIError, RateLimitError

    try:
        return call_llm_with_retry(
            primary_client, primary_model, messages
        ), primary_model
    except (RateLimitError, APIError, APIConnectionError) as e:
        print(f"  [Основной провайдер недоступен: {e}]")

        if fallback_client and fallback_model:
            print(f"  [Переключаюсь на fallback: {fallback_model}]")
            try:
                return call_llm_with_retry(
                    fallback_client, fallback_model, messages
                ), fallback_model
            except Exception as fallback_err:
                raise RuntimeError(
                    f"Сервис временно недоступен: {fallback_err}"
                ) from fallback_err
        raise


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
            print(f"Fallback: {fallback_provider.name} ({fallback_model})")
        except Exception:
            print("Fallback (Ollama) недоступен, работаем без резерва.")

    print(f"\nПровайдер: {provider.name}, модель: {primary_model}")

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
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            stream, used_model = call_with_fallback(
                primary_client,
                primary_model,
                fallback_client,
                fallback_model,
                messages,
            )
        except RateLimitError:
            print("  [ERROR] Превышен лимит запросов. Попробуйте позже.")
            messages.pop()  # убираем неотправленное сообщение
            continue
        except APIConnectionError:
            print("  [ERROR] Нет подключения к API. Проверьте интернет.")
            messages.pop()
            continue
        except APIError as e:
            print(f"  [ERROR] Ошибка API: {e}")
            messages.pop()
            continue
        except Exception as e:
            print(f"  [ERROR] {e}")
            messages.pop()
            continue

        print("Ассистент: ", end="")
        full_response = ""
        usage = None

        for chunk in stream:
            if chunk.choices:
                delta = chunk.choices[0].delta.content or ""
                delta = delta.replace("\ufeff", "")
                if delta:
                    print(delta, end="", flush=True)
                    full_response += delta
            if chunk.usage:
                usage = chunk.usage
        print()

        # Логируем usage и стоимость
        if usage:
            tracker.log_usage(used_model, usage.prompt_tokens, usage.completion_tokens)

        messages.append({"role": "assistant", "content": full_response})

    # Итоговая статистика при выходе
    tracker.summary()
    print("Диалог завершён.")


if __name__ == "__main__":
    main()
