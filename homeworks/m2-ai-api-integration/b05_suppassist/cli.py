"""Интерактивный CLI (REPL) для общения с ассистентом поддержки.

Принимает пользовательский ввод, обрабатывает команды CLI
и выводит ответ ассистента с метаданными (категория, источник, задержка).
"""

from __future__ import annotations

from config import Settings
from core.assistant import SupportAssistantApp
from pydantic import ValidationError
from redis.exceptions import ConnectionError, TimeoutError


def main():
    try:
        settings = Settings()  # pyright: ignore[reportCallIssue]
        assistant = SupportAssistantApp(settings)
        assistant.cache.client.ping()
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])

            if err["type"] == "missing":
                print(f"! Не задана переменная ENV: {field.upper()}")
            else:
                print(f"! {field.upper()}: {err['msg']}")
        raise SystemExit(1)
    except (ConnectionError, TimeoutError) as e:
        print(f"! Redis недоступен: {e}")
        raise SystemExit(1)

    print(f"=== {settings.service_name} Support CLI ===")
    print("Команды: /clear, /clear_cache, /reset_redis_stats, /stats, /quit")

    while True:
        try:
            user_input = input("\nВы: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо свидания!")
            return None

        if not user_input:
            continue

        if user_input.startswith("/"):
            command_result = assistant.handle_command(user_input)
            if command_result is None:
                print("До свидания!")
                return None
            print(command_result)
            continue

        response = assistant.respond(user_input)
        source = "cache" if response.from_cache else response.provider
        print(f"[{response.category} | {source} | {response.latency_seconds:.2f}с]")
        print(response.text)
