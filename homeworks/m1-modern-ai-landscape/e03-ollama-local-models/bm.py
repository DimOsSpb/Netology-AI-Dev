import time

import ollama

# models = ["qwen2:1.5b", "gemma3:1b", "gemma2:2b", "bench-gemma3:1b"]
models = ["gemma3:1b", "bench-gemma3:1b"]

tasks = {
    "О себе": {
        "prompt": "Ты LLM, Раскажи кратко что ты такое",
        "keys": [
            "я",
            "модель",
            "разраб",
            "интелект",
            "данны",
            "искуст",
            "понима",
            "генер",
            "текст",
            "отве",
            "вопросы",
            "переводить",
            "алгоритм",
            "программ",
        ],
    },
    "Математика": {
        "prompt": "Сколько будет 2+12*2-3?",
        "keys": ["23"],
    },
    "Краски": {
        "prompt": "Смешаем красную и желтую краску - какой цвет получим?",
        "keys": ["оранж"],
    },
}

results = []

for model in models:
    print(f"\n{'*' * 6} Модель: {model} {'*' * 6}")
    times = []
    qualities = []
    grades = []
    for task_name, task_data in tasks.items():
        prompt = task_data["prompt"]
        keywords = task_data["keys"]
        print(f"\nЗадача: {task_name}")
        print(f"Промт: {prompt}")

        start = time.perf_counter()

        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            options={"num_ctx": 2048, "num_predict": 200, "temperature": 0.1},
        )

        answer = response["message"]["content"]
        answer_lower = answer.lower()
        found = sum(1 for kw in keywords if kw.lower() in answer_lower)
        quality = found / len(keywords)
        # length_bonus = min(0.3, len(answer) / 300)
        # quality = min(1.0, score * 0.7 + length_bonus)

        elapsed = time.perf_counter() - start

        times.append(elapsed)
        qualities.append(quality)

        print(f"Время: {elapsed:.2f} сек")
        print(f"Ответ: {response['message']['content']}")
        print(f"Качество: {quality:.1%}")
        print(f"{'-' * 40}")

    avg_time = sum(times) / len(times)
    avg_quality = sum(qualities) / len(qualities)
    if avg_quality >= 0.9:
        grade = "Отлично"
    elif avg_quality >= 0.6:
        grade = "Хорошо"
    elif avg_quality >= 0.3:
        grade = "Средне"
    else:
        grade = "Плохо"

    results.append(
        {"model": model, "time": avg_time, "quality": avg_quality, "grade": grade}
    )

print("\nУсредненные Итоги:")
print("*" * 40)


def mySF(e):
    return e["quality"]


results.sort(key=mySF)
for res in results:
    print(
        f"{res['model']:13} - {res['time']:.2f} сек, качество: {res['quality']:.1%}, оценка: {res['grade']}"
    )
