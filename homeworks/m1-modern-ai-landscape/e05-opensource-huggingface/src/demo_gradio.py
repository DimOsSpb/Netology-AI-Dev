import time

import gradio as gr
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = "cointegrated/rut5-base-absum"

print("Загрузка модели...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()
print(f"Модель загружена на {device}")


def summarize(text):

    if not text or len(text.strip()) < 10:
        return "Введите текст длиной не менее 10 символов"

    # ограничиваем входной текст
    if len(text) > 2000:
        text = text[:2000]

    prompt = f"Кратко: {text}"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(
        device
    )

    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            # max_new_tokens=max_length,
            # min_new_tokens=min_length,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary


# Создаём интерфейс
demo = gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(
        label="Текст для анализа", placeholder="Опишите ситуацию...", lines=3
    ),
    outputs=gr.Textbox(label="Результат"),
    title="Суммаризация текстов",
    description="Введите текст описывающий ситуацию или скопируйте запись из журнала — модель сформирует краткое описание",
    examples=[
        ["Проверка readiness probe провалилась: HTTP 503, сервис не принимает трафик"],
        [
            "kubectl не может подключиться к API серверу: connection refused после обновления сертификатов. Это произошло из-за того, что сертификаты истекли и их нужно обновить вручную или автоматически через cert-manager."
        ],
    ],
)
demo.launch(share=True)
