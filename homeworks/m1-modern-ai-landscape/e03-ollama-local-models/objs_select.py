import time

import ollama

print("\n" + "-" * 40)
print("Извлечение сущностей из текста ")
print("-" * 40)

text = "Василий Иванович сменил профессию. С 12 мая 2025 года он работает в Банке ПСБ."

print(f"\nТекст: {text}")

start = time.perf_counter()

response = ollama.chat(
    model="objsel-gemma2:2b",
    messages=[
        {
            "role": "user",
            "content": f"Извлеки сущности из текста: {text}. Верни JSON с полями persons, organizations, dates",
        }
    ],
    stream=False,
    options={"num_ctx": 2048, "num_predict": 200, "temperature": 0.1},
)

elapsed = time.perf_counter() - start

answer = response["message"]["content"]
print(f"Время: {elapsed:.2f} сек")
print(f"Ответ: {answer}")
