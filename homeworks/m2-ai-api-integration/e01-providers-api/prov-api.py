import time

from config import ProviderSettings, settings
from openai import APIConnectionError, APIError, OpenAI, RateLimitError
from openai.types.chat import ChatCompletionMessageParam


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


def main() -> None:

    provider = choose_provider()
    client = build_client(provider)
    model = provider.model

    print(f"\nПровайдер: {provider.name}, модель: {model}")

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
            print("Диалог завершён.")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        temperatures = [0.0, 0.7, 1.5]
        print(f"Загруженный список температур: {temperatures}")
        for temp in temperatures:
            try:
                start_time = time.perf_counter()
                stream = client.chat.completions.create(
                    messages=messages,
                    model=model,
                    stream=True,
                    # stream_options={"include_usage": True},
                    temperature=temp,
                    max_tokens=200,
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

            full_response = ""

            ttft = None
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                delta = delta.replace("\ufeff", "")
                if delta:
                    if ttft is None:
                        end_time = time.perf_counter()
                        ttft = end_time - start_time
                        print(f"\nTTFT (Время до первого токена): {ttft:.4f} сек.")
                        print(f"Ассистент (температура = {temp}): ", end="")

                    print(delta, end="", flush=True)
                    full_response += delta

            print()


if __name__ == "__main__":
    main()
