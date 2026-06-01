
# Домашнее задание
https://u.netology.ru/backend/uploads/lms/content_assets/file/15196/homeworks_part04.pdf
---
# [Решение](caching.py)
```bach
odv@matebook16s:~/Downloads$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                                       NAMES
2049036283a3   redis:latest   "docker-entrypoint.s…"   12 seconds ago   Up 10 seconds   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   redis-cache
-----------------------------

(netology-ai-dev) odv@matebook16s:~/project/MY/Netology-AI-Dev/homeworks/m2-ai-api-integration/e04-caching$ python caching.py
Выберите провайдера:
  1. Ollama (локальный) (модель: qwen2:1.5b)
  2. OpenAI (модель: openai/gpt-oss-120b:free)
  3. OpenAI (модель: anthropic/claude-opus-4.8-fast)
Номер провайдера: 2
2026-06-01 16:57:21.733 | INFO     | __main__:main:288 - Fallback: Ollama (локальный) (qwen2:1.5b)
2026-06-01 16:57:21.733 | INFO     | __main__:main:292 - Провайдер: OpenAI, модель: openai/gpt-oss-120b:free
2026-06-01 16:57:21.747 | INFO     | __main__:build_cache:84 - Кеш: Redis (TTL=3600s)
Введите сообщение. Для выхода используйте exit или quit

Вы: Hello
2026-06-01 16:57:26.404 | DEBUG    | redis_cache:get:43 - Cache miss: llm:ea49856478099b751fdc13df8e9659e8791db9099e349b42dc79aee8c16bdb64
2026-06-01 16:57:33.478 | INFO     | __main__:chat_with_cache:263 - API ответ за 6.88s
2026-06-01 16:57:33.480 | DEBUG    | redis_cache:set:55 - Cached with TTL=3600s: llm:ea49856478099b751fdc13df8e9659e8791db9099e349b42dc79aee8c16bdb64
Ассистент: Hello! How can I help you today? What are you looking to purchase?
  [Токены: 92+50 | Стоимость: $0.000000 | За сессию: $0.000000]

Вы: Hello
2026-06-01 16:57:43.674 | DEBUG    | redis_cache:get:41 - Cache hit: llm:ea49856478099b751fdc13df8e9659e8791db9099e349b42dc79aee8c16bdb64
2026-06-01 16:57:43.674 | INFO     | __main__:chat_with_cache:237 - Из кеша за 0.0014s
Ассистент: Hello! How can I help you today? What are you looking to purchase?

Вы: Привет
2026-06-01 16:57:53.929 | DEBUG    | redis_cache:get:43 - Cache miss: llm:79c2c93c8eb11b64d6c427f9c3c699b9bb6fe3f70a5cb9a619f7baab114b5f85
2026-06-01 16:57:56.105 | INFO     | __main__:chat_with_cache:263 - API ответ за 1.71s
2026-06-01 16:57:56.107 | DEBUG    | redis_cache:set:55 - Cached with TTL=3600s: llm:79c2c93c8eb11b64d6c427f9c3c699b9bb6fe3f70a5cb9a619f7baab114b5f85
Ассистент: Привет! Чем могу помочь? Что бы вы хотели приобрести?
  [Токены: 147+35 | Стоимость: $0.000000 | За сессию: $0.000000]

----------------------------------
odv@matebook16s:~/Downloads$ docker rm 2049036283a3 -f
2049036283a3
odv@matebook16s:~/Downloads$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
odv@matebook16s:~/Downloads$ 
----------------------------------
(netology-ai-dev) odv@matebook16s:~/project/MY/Netology-AI-Dev/homeworks/m2-ai-api-integration/e04-caching$ python caching.py
Выберите провайдера:
  1. Ollama (локальный) (модель: qwen2:1.5b)
  2. OpenAI (модель: openai/gpt-oss-120b:free)
  3. OpenAI (модель: anthropic/claude-opus-4.8-fast)
Номер провайдера: 2
2026-06-01 17:03:01.161 | INFO     | __main__:main:288 - Fallback: Ollama (локальный) (qwen2:1.5b)
2026-06-01 17:03:01.161 | INFO     | __main__:main:292 - Провайдер: OpenAI, модель: openai/gpt-oss-120b:free
2026-06-01 17:03:05.224 | WARNING  | __main__:build_cache:87 - Redis недоступен, используется SimpleCache (in-memory)
Введите сообщение. Для выхода используйте exit или quit

Вы: Hello
2026-06-01 17:03:19.092 | INFO     | __main__:chat_with_cache:263 - API ответ за 6.79s
Ассистент: Добрый день! Чем могу помочь? Что вы ищете?
  [Токены: 92+49 | Стоимость: $0.000000 | За сессию: $0.000000]

Вы: Hello
2026-06-01 17:03:26.873 | INFO     | __main__:chat_with_cache:237 - Из кеша за 0.0002s
Ассистент: Добрый день! Чем могу помочь? Что вы ищете?

Вы: Привет
2026-06-01 17:04:24.943 | INFO     | __main__:chat_with_cache:263 - API ответ за 48.68s
Ассистент: Здравствуйте! Чем могу помочь? Ищете какой‑то конкретный товар или хотите узнать о наших акциях?
  [Токены: 141+49 | Стоимость: $0.000000 | За сессию: $0.000000]
```
