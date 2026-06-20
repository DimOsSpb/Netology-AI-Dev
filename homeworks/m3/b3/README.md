# Блок 3.3 — Асинхронная обработка запросов к ИИ
---
## [Репозиторий с работой](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/2ab83c5bf7bef67098caf2b0065e0e30cfefb0a8)
## Результаты
- scripts/benchmark.py - вывод с результатами работы sync/async без сбоев и примером с assync сетевого сбоя в логах и результатах
```bash
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run -m scripts.benchmark
=== Start Sync TEST ===
=== End Sync TEST === 66.20s
=== Start Async TEST c=1 ===
=== End Async TEST c=1 time=90.61s ok=20/20
=== Start Async TEST c=5 ===
=== End Async TEST c=5 time=24.68s ok=20/20
=== Start Async TEST c=10 ===
=== End Async TEST c=10 time=10.74s ok=20/20

===== SUMMARY =====
Sync     : 66.20s
Async x1 : 90.61s
Async x5 : 24.68s
Async x10: 10.74s
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run -m scripts.benchmark
=== Start Async TEST c=1 ===
=== End Async TEST c=1 time=81.60s ok=20/20
=== Start Async TEST c=5 ===
=== End Async TEST c=5 time=33.07s ok=10/20
=== Start Async TEST c=10 ===
=== End Async TEST c=10 time=20.01s ok=19/20

===== SUMMARY =====
Sync     : 0.00s
Async x1 : 81.60s
Async x5 : 33.07s
Async x10: 20.01s
```
```bash
2026-06-20T15:02:52.185670+0300 | INFO | async.llm.call duration_ms=46349.32 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:02:55.668784+0300 | INFO | async.llm.call duration_ms=49832.44 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:02:59.172242+0300 | INFO | async.llm.call duration_ms=53335.90 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:04.680965+0300 | INFO | async.llm.call duration_ms=58844.62 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:14.844689+0300 | INFO | async.llm.call duration_ms=69008.33 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:17.300120+0300 | INFO | async.llm.call duration_ms=71463.76 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:21.992265+0300 | INFO | async.llm.call duration_ms=76155.90 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:24.429928+0300 | INFO | async.llm.call duration_ms=78593.56 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:26.594635+0300 | INFO | async.llm.call duration_ms=80758.26 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:41.607378+0300 | INFO | async.llm.call duration_ms=15011.85 model=openai/gpt-oss-120b:free prompt_chars=47 status=timeout
2026-06-20T15:03:41.608105+0300 | INFO | async.llm.call duration_ms=15010.64 model=openai/gpt-oss-120b:free prompt_chars=47 status=timeout
2026-06-20T15:03:41.608478+0300 | INFO | async.llm.call duration_ms=15009.38 model=openai/gpt-oss-120b:free prompt_chars=47 status=timeout
2026-06-20T15:03:41.608932+0300 | INFO | async.llm.call duration_ms=15007.98 model=openai/gpt-oss-120b:free prompt_chars=47 status=timeout
2026-06-20T15:03:41.609334+0300 | INFO | async.llm.call duration_ms=15006.62 model=openai/gpt-oss-120b:free prompt_chars=47 status=timeout
2026-06-20T15:03:44.615828+0300 | WARNING | Провайдер openai/gpt-oss-120b:free недоступен: Connection error.
2026-06-20T15:03:44.616292+0300 | INFO | async.llm.call duration_ms=18006.44 model=openai/gpt-oss-120b:free prompt_chars=47 status=providers_error
2026-06-20T15:03:44.875877+0300 | WARNING | Провайдер openai/gpt-oss-120b:free недоступен: Connection error.
2026-06-20T15:03:44.876419+0300 | INFO | async.llm.call duration_ms=18266.56 model=openai/gpt-oss-120b:free prompt_chars=47 status=providers_error
2026-06-20T15:03:44.892203+0300 | WARNING | Провайдер openai/gpt-oss-120b:free недоступен: Connection error.
2026-06-20T15:03:44.892579+0300 | INFO | async.llm.call duration_ms=18282.76 model=openai/gpt-oss-120b:free prompt_chars=47 status=providers_error
2026-06-20T15:03:44.932068+0300 | WARNING | Провайдер openai/gpt-oss-120b:free недоступен: Connection error.
2026-06-20T15:03:44.932455+0300 | INFO | async.llm.call duration_ms=18322.61 model=openai/gpt-oss-120b:free prompt_chars=47 status=providers_error
2026-06-20T15:03:44.932786+0300 | WARNING | Провайдер openai/gpt-oss-120b:free недоступен: Connection error.
2026-06-20T15:03:44.933168+0300 | INFO | async.llm.call duration_ms=18323.33 model=openai/gpt-oss-120b:free prompt_chars=47 status=providers_error
2026-06-20T15:03:48.118526+0300 | INFO | async.llm.call duration_ms=21508.66 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
2026-06-20T15:03:48.926970+0300 | INFO | async.llm.call duration_ms=22317.11 model=openai/gpt-oss-120b:free prompt_chars=48 status=success
```
- Проверка SSE
```bash
odv@matebook16s:~$ curl -X POST http://localhost:8000/chat/stream -H "Content-Type: application/json" -d '{"prompt":"Какая команда для просмотра каталогов?"}'
data: Для
data:  просмотра
data:  содерж
data: имого
data:  каталог
...
```
