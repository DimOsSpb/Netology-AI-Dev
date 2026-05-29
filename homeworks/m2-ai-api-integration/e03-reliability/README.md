
# Домашнее задание
https://u.netology.ru/backend/uploads/lms/content_assets/file/15195/homeworks_part03.pdf
---
# [Решение](rel.py)
1. Класс `RobustLLMClient`: обёртка над OpenAI SDK, перехват ошибок 429, 500, таймаутов
2. Retry: exponential backoff (1s → 2s → 4s → 8s → 16s) + jitter, до 5 попыток. Библиотека tenacity или своя реализация
3. Fallback-цепочка: OpenAI → OpenRouter → сообщение «Сервис временно недоступен»
4. Логирование: timestamp, код ошибки, номер попытки
5. Трекинг usage: prompt_tokens, completion_tokens, стоимость
```bach
odv@matebook16s:~/project/MY/Netology-AI-Dev/homeworks/m2-ai-api-integration/e03-reliability$ uv run python prov-api.py
Выберите провайдера:
  1. Ollama (локальный) (модель: qwen2:1.5b)
  2. OpenAI (модель: openai/gpt-oss-120b:free)
  3. OpenAI (модель: anthropic/claude-opus-4.8-fast)
Номер провайдера: 3
Fallback: Ollama (локальный) (qwen2:1.5b)

Провайдер: OpenAI, модель: anthropic/claude-opus-4.8-fast
Введите сообщение. Для выхода используйте exit или quit

Вы: Ghbdtn
  [Основной провайдер недоступен: Error code: 402 - {'error': {'message': 'This request requires more credits, or fewer max_tokens. You requested up to 65536 tokens, but can only afford 706. To increase, visit https://openrouter.ai/settings/credits and upgrade to a paid account', 'code': 402, 'metadata': {'provider_name': None}}, 'user_id': 'user_38pvuT2oyQOaAcxHIJsB5zj999J'}]
  [Переключаюсь на fallback: qwen2:1.5b]
Ассистент: Sorry, I didn't quite catch that. Could you please provide more details or clarify your request?
  [Токены: 41+21 | Стоимость: $0.000000 | За сессию: $0.000000]

Вы: Привет
  [Основной провайдер недоступен: Error code: 402 - {'error': {'message': 'This request requires more credits, or fewer max_tokens. You requested up to 65536 tokens, but can only afford 706. To increase, visit https://openrouter.ai/settings/credits and upgrade to a paid account', 'code': 402, 'metadata': {'provider_name': None}}, 'user_id': 'user_38pvuT2oyQOaAcxHIJsB5zj999J'}]
  [Переключаюсь на fallback: qwen2:1.5b]
Ассистент: Привет! Как я могу помочь вам сегодня?
  [Токены: 74+14 | Стоимость: $0.000000 | За сессию: $0.000000]
```
