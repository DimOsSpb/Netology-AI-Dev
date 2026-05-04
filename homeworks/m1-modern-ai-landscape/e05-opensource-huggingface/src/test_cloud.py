import os
import time

from openai import OpenAI

with open("/home/odv/.secret/openrouter-netology-key", "r", encoding="utf-8-sig") as f:
    OPENROUTER_API_KEY = f.read().strip()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# тот-же набор
test_texts = [
    "kubectl не может подключиться к API серверу: connection refused после обновления сертификатов",
    "Под под управлением node exporter падает с ошибкой OOMKilled: memory limit 256Mi",
    "kube-scheduler не назначает поды на узел из-за taint Effect=NoSchedule",
    "Развертывание приложения остановлено: ImagePullBackOff, образ не найден в registry",
    "Проверка readiness probe провалилась: HTTP 503, сервис не принимает трафик",
    "PV не смонтировался: mount error: permission denied на NFS экспорте",
    "Helm чарт не устанавливается: template failed: missing required value .Values.db.password",
    "kubectl logs возвращает ошибку: container is not running (state=CrashLoopBackOff)",
    "Аргумент --request-timeout превышен: etcd не отвечает на запросы лидера",
    "Сертификат ingress истек: certificate has expired or is not yet valid",
]


def test_openrouter_model(model_name, prompts):
    times = []

    print(f"\n{model_name}")
    print("=" * 30)

    for prompt in prompts:
        start = time.time()

        response = None
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "Кратко перескажи суть одним предложением на русском языке, максимум 10 слов.",
                    },
                    {"role": "user", "content": f"Кратко: {prompt}"},
                ],
                max_tokens=100,
                temperature=0.3,
            )
            elapsed = time.time() - start
            times.append(elapsed)
            response = completion.choices[0].message.content
            print(f"+ {len(times)}/{len(prompts)} - {elapsed:.2f}s")
            print(f"IN: {prompt}")
            print(f"OUT: {response}")
            print("-" * 30)
        except Exception as e:
            print(f"- Ошибка: {e}")
            times.append(None)

    valid_times = [t for t in times if t is not None]
    avg_time = sum(valid_times) / len(valid_times) if valid_times else 0
    total_time = sum(valid_times) if valid_times else 0

    return {
        "id": model_name,
        "avg_time": avg_time,
        "total_time": total_time,
    }


results = []
models = ["openai/gpt-oss-120b:free", "openai/gpt-4o-mini"]
for model in models:
    result = test_openrouter_model(model, test_texts)
    results.append(result)

print(f"\n\n{'N':<2} | {'ID модели':<45} | {'avg_time':<10} | {'total_time':<10} |")
print("-" * 80)

for result in results:
    print(
        f"{1:<2} | {result['id']:<45} | {result['avg_time']:<10.2f} | {result['total_time']:<10.2f} |"
    )
