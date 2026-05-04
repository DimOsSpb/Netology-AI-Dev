import logging
import time
import warnings

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# --- ОТКЛЮЧАЕМ ШУМ ---
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

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


def benchmark_model(model_name, test_data):
    print(f"Загрузка модели {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    total_time = 0
    results = []

    for text in test_data:
        prompt = f"Кратко: {text}"
        inputs = tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=512
        ).to(device)

        start = time.time()
        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_new_tokens=40,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3,
            )
        inference_time = time.time() - start

        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        results.append(summary)
        total_time += inference_time

    avg_time = total_time / len(test_data)
    return avg_time, total_time, results


models = [
    "cointegrated/rut5-base-absum",
    "IlyaGusev/rut5_base_headline_gen_telegram",
    "RussianNLP/FRED-T5-Summarizer",
]
results = []

for model in models:
    print(f"\n{model}")
    print("-" * 40)
    avg_time, total_time, outputs = benchmark_model(model, test_texts)
    results.append({
        "id": model,
        "avg_time": avg_time,
        "total_time": total_time,
    })
    for inp, out in zip(test_texts, outputs):
        print(f"IN: {inp}...")
        print(f"OUT: {out}")

print(f"\n\n{'N':<2} | {'ID модели':<45} | {'avg_time':<10} | {'total_time':<10} |")
print("-" * 80)

for idx, res in enumerate(results, start=1):
    print(
        f"{idx:<2} | {res['id']:<45} | {res['avg_time']:<10.2f} | {res['total_time']:<10.2f} |"
    )
