
# Домашнее задание
https://u.netology.ru/backend/uploads/lms/content_assets/file/15197/homeworks_part05.pdf
---
# Решение

# Support Assistant CLI

Простое CLI-приложение для практики блока 2.5. Помощник отвечает только по теме сервиса `InfraAssist`, умеет классифицировать обращения, кешировать FAQ в Redis, делать retry (tenacity) и fallback, логировать диалог (loguru) и поддерживает базовые команды.

## Структура

```text
support_assistant_cli/
  cli.py                  # точка входа
  models.py               # все dataclass-ы и type alias-ы
  core/
    assistant.py          # сценарий диалога и команды CLI
    classification.py     # категории и правила эскалации
  infrastructure/
    cache.py              # Redis-кеш
    llm.py                # retry (tenacity) + fallback для LLM
  prompts/
    loader.py             # загрузка prompt-файлов
    system_prompt.txt
    classifier_system_prompt.txt
    classifier_few_shots.json
    service_facts.txt
```

## Возможности

- `System prompt` в формате РРФО: роль, правила, факты, ограничения
- `Few-shot` в классификаторе: 4 примера
- `Retry`: tenacity с экспоненциальной задержкой (RateLimitError, APIStatusError)
- `Fallback`: primary → fallback → эскалация на оператора
- `Кеширование`: Redis-кеш (TTL по умолчанию 1 час)
- `CLI`: `/clear`, `/clear_cache`, `/reset_redis_stats`, `/stats`, `/quit`
- `Логирование`: loguru (файл + консоль)
- `Все провайдеры` через OpenAI-совместимый API (OpenAI, Groq, OpenRouter, Ollama)
- `История`: последние 10 сообщений для контекста
- `Классификация`: `faq`, `technical`, `complaint`, `escalation`
- `Эскалация`: ответ `Передаю вопрос специалисту`

## Запуск

Из папки:

```bash
python __main__.py
```

Предварительно должен быть запущен Redis:

```bash
redis-server
# или через Docker:
docker run -d --name redis:latest -p 6379:6379 redis:alpine
```

Для сохранения кеша после перезапуска Redis включите RDB или AOF (`appendonly yes` в `redis.conf`).

## Переменные окружения

### Основной провайдер
- `API_KEY` — API-ключ (OpenAI, Groq, OpenRouter и т.д.)
- `BASE_URL` — base URL (по умолчанию OpenAI; для Groq: `https://api.groq.com/openai/v1`)

### Fallback-провайдер
- `FALLBACK_API_KEY` — API-ключ fallback (по умолчанию `ollama`)
- `FALLBACK_BASE_URL` — base URL fallback (по умолчанию `http://localhost:11434/v1`)
- `FALLBACK_MODEL` — модель fallback (по умолчанию `qwen3:8b`)

### Redis
- `REDIS_HOST` — хост Redis, по умолчанию `localhost`
- `REDIS_PORT` — порт Redis, по умолчанию `6379`
- `REDIS_TTL` — время жизни кеша в секундах, по умолчанию `3600`

### Прочее
- `SUPPORT_SERVICE_NAME` — имя сервиса, по умолчанию `InfraAssist`

Без ключей приложение тоже работает: классификация работает эвристикой, при недоступности обоих провайдеров — эскалация на оператора.

## Быстрый сценарий проверки

1. `Сколько стоит тариф Pro?`
2. Повторите тот же вопрос и проверьте `cache` в строке статуса.
3. `Не могу загрузить файл, ошибка 413`
4. `Позовите менеджера`
5. `/stats`
6. `/clear_cache`
7. `/reset_redis_stats`

### Пример работы программы
```bash
(netology-ai-dev) odv@matebook16s:~/project/MY/Netology-AI-Dev/homeworks/m2-ai-api-integration/b05_suppassist$ python __main__.py
=== InfraAssist Support CLI ===
Команды: /clear, /clear_cache, /reset_redis_stats, /stats, /quit

Вы: hello
[technical | primary | 16.80с]
Здравствуйте! Как я могу вам помочь по сервису InfraAssist?

Вы: Hello
[technical | cache | 2.29с]
Здравствуйте! Как я могу вам помочь по сервису InfraAssist?

Вы: Сколько стоит тариф Pro?
[faq | primary | 15.58с]
Тариф Pro стоит 299 ₽ в месяц.

Вы: Сколько стоит тариф Pro?
[faq | cache | 1.30с]
Тариф Pro стоит 299 ₽ в месяц.

Вы: Позовите менеджера
[escalation | primary | 13.84с]
Передаю вопросспециалисту.

Вы: Позовите менеджера
[escalation | cache | 1.03с]
Передаю вопросспециалисту.

Вы: /stats
Запросов: 6 | LLM вызовов: 3 | Токенов: 0 | Эскалаций: 0 | Redis: 4 ключей, hit rate: 46.7% (7/15)

Вы: Позовите менеджера
[escalation | cache | 6.95с]
Передаю вопросспециалисту.

Вы: Позовите менеджера
[escalation | router | 1.10с]
Передаю вопрос специалисту. Номер обращения: BC9F9E74.

Вы: /stats
Запросов: 8 | LLM вызовов: 3 | Токенов: 0 | Эскалаций: 1 | Redis: 4 ключей, hit rate: 50.0% (8/16)
```
