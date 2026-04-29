# Домашнее задание
## [Задача: провести полный цикл выбора модели для вашего проекта.](https://u.netology.ru/backend/uploads/lms/content_assets/file/14978/1-block-04-comparison-cost-homework.pdf)
Шаг 1. Создайте eval-набор (20+ задач)
• Задачи должны отражать реальные сценарии вашего бота/приложения
• Каждая задача — промпт + проверочная функция
Шаг 2. Прогоните бенчмарк на 3+ моделях
• Минимум: 2 локальные (через Ollama) + 1 облачная (через OpenRouter бесплатно)
• Измерьте: TTFT, throughput, accuracy на вашем eval
Шаг 3. Рассчитайте стоимость
• Определите: сколько запросов/день, средний input/output в токенах
• Посчитайте стоимость для каждой модели (без кэша и с кэшем)
Шаг 4. Подготовьте рекомендацию
• Какую модель выбрали и почему (1 абзац)
• Сравнительная таблица: модель, accuracy, TTFT, стоимость/месяц

---
## Решение
1. [eval-набор (20+ задач) - Системные events K8s]
Проект: K8s Infra Dispatcher  
Роль LLM: Автоматический анализатор событий инфраструктуры Kubernetes. Получает на вход JSON-событие от кластера, классифицирует его и принимает решение на реакцию дальнейших действий. 
Вход: структурированное событие (JSON)  
Выход: JSON с полями severity, category, action, suggested_commands, summary  
Мы проверяем как модель подходит к задаче. К каждому событию — проверочная функция, оценивающая корректность классификации и диагностики.  
2. [Сам скрипт - bm.py](bm.py)
benchmark_model - функция оценки моделей из массива MODELS
3. Расчет стоимости
- Выполнен для локальных моделей на своем оборудовании
- Для облачных аналогов
- Произведена оценка точки безубыточности
```bash
(venv) odv@matebook16s:~/project/MY/Netology-AI-Dev/homeworks/m1-modern-ai-landscape/e04-comparison-cost$ python3 bm.py
Benchmark моделей под проект - K8s Infra Dispatcher
Total tasks: 20

Testing: phi3:mini
========================================
  E01: False (ttft=8.65 sek)
  E02: Ok (ttft=2.98 sek)
  E03: False (ttft=3.49 sek)
  E04: False (ttft=2.55 sek)
  E05: False (ttft=3.16 sek)
  E06: False (ttft=2.52 sek)
  E07: False (ttft=2.00 sek)
  E08: False (ttft=2.39 sek)
  E09: False (ttft=2.42 sek)
  E10: Ok (ttft=2.81 sek)
  E11: False (ttft=2.64 sek)
  E12: False (ttft=2.10 sek)
  E13: False (ttft=2.54 sek)
  E14: False (ttft=2.88 sek)
  E15: False (ttft=2.22 sek)
  E16: False (ttft=2.16 sek)
  E17: False (ttft=2.48 sek)
  E18: Ok (ttft=2.29 sek)
  E19: False (ttft=2.12 sek)
  E20: False (ttft=2.71 sek)

  Results for phi3:mini
------------------------------
  Accuracy: 15.00%
  Avg TTFT: 2.86s
  Throughput: 0.35 req/s
  Avg tokens: 63

Testing: qwen2:1.5b
========================================
  E01: False (ttft=2.80 sek)
  E02: Ok (ttft=0.94 sek)
  E03: False (ttft=1.07 sek)
  E04: Ok (ttft=1.23 sek)
  E05: False (ttft=0.96 sek)
  E06: False (ttft=0.87 sek)
  E07: False (ttft=0.64 sek)
  E08: False (ttft=0.78 sek)
  E09: False (ttft=0.81 sek)
  E10: Ok (ttft=0.92 sek)
  E11: False (ttft=0.85 sek)
  E12: False (ttft=0.69 sek)
  E13: False (ttft=0.76 sek)
  E14: False (ttft=0.83 sek)
  E15: False (ttft=0.75 sek)
  E16: False (ttft=0.67 sek)
  E17: Ok (ttft=0.80 sek)
  E18: Ok (ttft=0.77 sek)
  E19: False (ttft=0.75 sek)
  E20: False (ttft=0.79 sek)

  Results for qwen2:1.5b
------------------------------
  Accuracy: 25.00%
  Avg TTFT: 0.93s
  Throughput: 1.07 req/s
  Avg tokens: 26

Testing: gemma2:2b
========================================
  E01: Ok (ttft=5.62 sek)
  E02: Ok (ttft=1.53 sek)
  E03: False (ttft=1.80 sek)
  E04: False (ttft=1.45 sek)
  E05: False (ttft=1.64 sek)
  E06: False (ttft=1.41 sek)
  E07: False (ttft=1.08 sek)
  E08: Ok (ttft=1.24 sek)
  E09: False (ttft=1.40 sek)
  E10: Ok (ttft=1.68 sek)
  E11: Ok (ttft=1.35 sek)
  E12: False (ttft=1.16 sek)
  E13: False (ttft=1.40 sek)
  E14: Ok (ttft=1.39 sek)
  E15: False (ttft=1.21 sek)
  E16: False (ttft=1.14 sek)
  E17: Ok (ttft=1.37 sek)
  E18: False (ttft=1.32 sek)
  E19: False (ttft=1.22 sek)
  E20: False (ttft=1.40 sek)

  Results for gemma2:2b
------------------------------
  Accuracy: 35.00%
  Avg TTFT: 1.59s
  Throughput: 0.63 req/s
  Avg tokens: 27

Testing: openai/gpt-oss-120b:free
========================================
  E01: Ok (ttft=3.30 sek)
  E02: Ok (ttft=3.39 sek)
  E03: Ok (ttft=3.82 sek)
  E04: Ok (ttft=10.61 sek)
  E05: Ok (ttft=9.42 sek)
  E06: Ok (ttft=4.70 sek)
  E07: Ok (ttft=4.80 sek)
  E08: Ok (ttft=5.35 sek)
  E09: False (ttft=7.26 sek)
  E10: Ok (ttft=2.64 sek)
  E11: False (ttft=9.93 sek)
  E12: False (ttft=4.71 sek)
  E13: Ok (ttft=4.06 sek)
  E14: Ok (ttft=1.98 sek)
  E15: False (ttft=4.12 sek)
  E16: Ok (ttft=9.19 sek)
  E17: False (ttft=10.54 sek)
  E18: Ok (ttft=5.18 sek)
  E19: Ok (ttft=4.18 sek)
on-primes  E20: False (ttft=3.54 sek)

  Results for openai/gpt-oss-120b:free
------------------------------
  Accuracy: 70.00%
  Avg TTFT: 5.64s
  Throughput: 0.18 req/s
  Avg tokens: 64

  РЕЗУЛЬТАТЫ БЕНЧМАРКА
==========================================================================================
Модель                                        Точность     Ср. TTFT (с)    req/sec
------------------------------------------------------------------------------------------
openai/gpt-oss-120b:free                      70.00%       5.64             0.18
gemma2:2b                                     35.00%       1.59             0.63
qwen2:1.5b                                    25.00%       0.93             1.07
phi3:mini                                     15.00%       2.86             0.35


 РАСЧЁТ СТОИМОСТИ
 500 000 запросов в день  за период 90 дней
==========================================================================================

ЛОКАЛЬНЫЙ GPU СЕРВЕР (TCO руб)
------------------------------------------------------------------------------------------
Модель                    Размер     Мощность (кВт)   Электричество          TCO                руб/req
------------------------------------------------------------------------------------------
qwen2:1.5b                1.5B          0.09                        1 335                300 335        0.006674
gemma2:2b                 2.0B          0.10                        1 506                300 506        0.006678
phi3:mini                 3.8B          0.21                        3 241                302 241        0.006716

ОБЛАЧНЫЕ МОДЕЛИ (за 90 дней, курс 80 руб/$)
------------------------------------------------------------------------------------------------------------------------
Модель                                        Вход ($/1M)    Выход ($/1M)    Всего (руб)      С кэшем (руб)
------------------------------------------------------------------------------------------------------------------------
mistralai/mistral-7b-instruct                 $0.07/M        $0.07/M                  176 400          128 772
google/gemini-2.0-flash-exp                   $0.1/M         $0.4/M                   468 000          341 640
openai/gpt-4o-mini                            $0.15/M        $0.6/M                   702 000          512 460
anthropic/claude-3-haiku                      $0.25/M        $1.25/M                1 350 000          985 500

СРАВНЕНИЕ (ЗА 90 ДНЕЙ) — ТОЛЬКО ПЛАТНЫЕ ОБЛАЧНЫЕ МОДЕЛИ
====================================================================================================

Локальный сервер (за 90 дней): 302 241 руб
Стоимость одного запроса: 0.006716 руб

Сравнение с платными облачными моделями (за 90 дней):
----------------------------------------------------------------------------------------------------
Модель                                        Облачно (руб)        Локально (руб)       Разница (%)
----------------------------------------------------------------------------------------------------
mistralai/mistral-7b-instruct                         176 400                  302 241           -41.6%
google/gemini-2.0-flash-exp                           468 000                  302 241           +54.8%
openai/gpt-4o-mini                                    702 000                  302 241          +132.3%
anthropic/claude-3-haiku                            1 350 000                  302 241          +346.7%

ТОЧКА БЕЗУБЫТОЧНОСТИ (окупаемость железа):
----------------------------------------------------------------------------------------------------
Стоимость железа: 260 000 руб
  - openai/gpt-4o-mini: 2.0 месяцев
  - google/gemini-2.0-flash-exp: 4.7 месяцев
  - anthropic/claude-3-haiku: 0.7 месяцев
  - mistralai/mistral-7b-instruct: облако дешевле на 41 947 руб/мес. Локальный сервер НЕ ОКУПАЕТСЯ
```
4. Выводы
- По результатам тестирования моделей для данной задачи, маленькие локальные модели быстрее отвечают но результат неудовлетворительный. Т.о. для on-premise развертывания такого проекта нужно рассматривать более продвинутые LLM и учитывать необходимость GPU ресурса.
- Облачные большие LLM дают по тестам заметно лучший результат (openrouter openai/gpt-oss-120b:free точность = 70.00% vs локальной gemma2:2b = 35.00%)
- Расчет стоимости Локального развертывания в сравнении с облачным решением показал, что при большом количестве запросов локальное решение окупится достаточно быстро и у него есть в таком случае преимущество по сравнению с оплатой облачным провайдерам.
  
Т.О. Все решает количество и сложность (специфичность) запросов. Для такого рода проекта я вижу целесообразным использовать более тяжелые локальные модели наподобие openai/gpt-oss-120b из теста. Даже учитывая что затраты на локальное оборудование окупится преблизительно через пару месяцев. Но на начальном этапе, пока (если) трафик событий не превышает 10000 запросов в день - полностью облачные вычисления заметно дешевле. В таком случае с приобретением оборудования стоит подождать.

---
## Ресурсы для углублённого изучения
1. [Примеры из лекции](https://github.com/abat-voix/ai-tools-and-links/blob/main/m1_b4)
2. Рейтинги и сравнения моделей:
- Artificial Analysis — сравнение моделей по качеству, скорости и цене (artificialanalysis.ai)
- Chatbot Arena / LMArena — рейтинг на основе голосов пользователей (lmarena.ai)
- LLM Stats — агрегатор лидербордов (llm-stats.com)
3. Цены провайдеров (актуальные):
- OpenAI: openai.com/api/pricing
- Anthropic: platform.claude.com/docs/en/about-claude/pricing
- Google: ai.google.dev/gemini-api/docs/pricing
- DeepSeek: api-docs.deepseek.com/quick_start/pricing
4. Инструменты:
- OpenRouter — единый API ко всем провайдерам (openrouter.ai)
- tiktoken — подсчёт токенов офлайн (github.com/openai/tiktoken)
- PricePerToken — калькулятор стоимости (pricepertoken.com)
5. Документация:
- OpenAI Batch API: platform.openai.com/docs/guides/batch
- Anthropic Prompt Caching: docs.anthropic.com/en/docs/build-with-claude/prompt-caching
