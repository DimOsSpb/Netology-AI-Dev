# Блок 6.2 - Инструменты и планирование
---

# [Задание](6-2.md)
## [Репозиторий с работой](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.6.2)
# Решение
```bash
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run python -m scripts.run_comparison_agents
INFO Запуск сравнения agent_naive и agent_react...
INFO
============================================================
INFO Задача 1: Простая: K8S - что это
INFO ============================================================
INFO
--- agent_naive ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=0 инструмент=search_knowledge_base -> Сокращенное название Kubernetes.
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=1 финальный ответ
INFO Ответ: K8S — это сокращённое название **Kubernetes**.

Это открытая платформа для оркестрации контейнеров, которая автоматизирует развертывание, масштабирование и управление контейнеризированными приложениям...
INFO Корректно: True (OK)
INFO Токены: {'input': 1404, 'output': 379, 'total': 1783}
INFO
--- agent_react ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:30 [info     ] react.step                     completion_tokens=113 iteration_latency_sec=1.628 model=Qwen3.5-9B-Q5_K_M prompt_tokens=730 step=0 total_tokens=843
2026-10-23 10:30:30 [info     ] react.step.tool                latency=1.6276065810234286 step=0 tool=search_knowledge_base
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:35 [info     ] react.step.completed           iterations=1 step=0
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:35 [info     ] react.step                     completion_tokens=47 iteration_latency_sec=0.704 model=Qwen3.5-9B-Q5_K_M prompt_tokens=866 step=1 total_tokens=913
2026-10-23 10:30:35 [info     ] react.step.final               content='K8S — это сокращенное название Kubernetes.' step=1
INFO Ответ: K8S — это сокращенное название Kubernetes....
INFO Корректно: True (OK)
INFO Токены: {'input': 1596, 'output': 160, 'total': 1756}
INFO
============================================================
INFO Задача 2: Простая: поддержка систем
INFO ============================================================
INFO
--- agent_naive ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=0 инструмент=search_knowledge_base -> Сервис поддерживает Linux, Kubernetes (K8s) и Proxmox.
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=1 финальный ответ
INFO Ответ: Сервис поддерживает следующие системы:
- Linux
- Kubernetes (K8s)
- Proxmox...
INFO Корректно: True (OK)
INFO Токены: {'input': 1378, 'output': 154, 'total': 1532}
INFO
--- agent_react ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:39 [info     ] react.step                     completion_tokens=94 iteration_latency_sec=1.568 model=Qwen3.5-9B-Q5_K_M prompt_tokens=729 step=0 total_tokens=823
2026-10-23 10:30:39 [info     ] react.step.tool                latency=1.5677615650347434 step=0 tool=search_knowledge_base
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:43 [info     ] react.step.completed           iterations=1 step=0
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:44 [info     ] react.step                     completion_tokens=63 iteration_latency_sec=0.892 model=Qwen3.5-9B-Q5_K_M prompt_tokens=854 step=1 total_tokens=917
2026-10-23 10:30:44 [info     ] react.step.final               content='Сервис поддерживает следующие системы: Linux, Kubernetes (K8s) и Proxmox.' step=1
INFO Ответ: Сервис поддерживает следующие системы: Linux, Kubernetes (K8s) и Proxmox....
INFO Корректно: True (OK)
INFO Токены: {'input': 1583, 'output': 157, 'total': 1740}
INFO
============================================================
INFO Задача 3: Средняя: время + статус
INFO ============================================================
INFO
--- agent_naive ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=0 инструмент=get_current_time -> 2026-10-23T10:30:46.475305+03:00
INFO step=0 инструмент=get_status -> Оптимальный
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=1 финальный ответ
INFO Ответ: Сейчас в Москве время: 23 октября 2026 года, 10:30:46 (по московскому времени).

Статус сервиса k8s: **Оптимальный**....
INFO Корректно: True (OK)
INFO Токены: {'input': 2120, 'output': 464, 'total': 2584}
INFO
--- agent_react ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:50 [info     ] react.step                     completion_tokens=150 iteration_latency_sec=2.036 model=Qwen3.5-9B-Q5_K_M prompt_tokens=737 step=0 total_tokens=887
2026-10-23 10:30:50 [info     ] react.step.tool                latency=2.0364203820354305 step=0 tool=get_current_time
2026-10-23 10:30:50 [info     ] react.step.tool                latency=2.0364203820354305 step=0 tool=get_status
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:56 [info     ] react.step.completed           iterations=1 step=0
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:30:58 [info     ] react.step                     completion_tokens=153 iteration_latency_sec=2.045 model=Qwen3.5-9B-Q5_K_M prompt_tokens=945 step=1 total_tokens=1098
2026-10-23 10:30:58 [info     ] react.step.final               content='Сейчас в Москве 23 октября 2026 года, 10:30:50 (по московскому времени), а статус сервиса k8s — опти' step=1
INFO Ответ: Сейчас в Москве 23 октября 2026 года, 10:30:50 (по московскому времени), а статус сервиса k8s — оптимальный....
INFO Корректно: True (OK)
INFO Токены: {'input': 2419, 'output': 453, 'total': 2872}
INFO
============================================================
INFO Задача 4: Средняя: статус + отправить уведомление
INFO ============================================================
INFO
--- agent_naive ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=0 инструмент=get_status -> Оптимальный
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=1 финальный ответ
INFO Ответ: Статус сервиса: Оптимальный.

Для отправки сообщения в Telegram нужен идентификатор чата (chat_id). Пожалуйста, предоставьте его, чтобы я мог отправить сообщение клиенту....
INFO Корректно: True (OK)
INFO Токены: {'input': 1660, 'output': 520, 'total': 2180}
INFO
--- agent_react ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:31:07 [info     ] react.step                     completion_tokens=164 iteration_latency_sec=2.281 model=Qwen3.5-9B-Q5_K_M prompt_tokens=741 step=0 total_tokens=905
2026-10-23 10:31:07 [info     ] react.step.tool                latency=2.2813258069800213 step=0 tool=get_status
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:31:28 [info     ] react.step.completed           iterations=1 step=0
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:31:29 [info     ] react.step                     completion_tokens=136 iteration_latency_sec=1.727 model=Qwen3.5-9B-Q5_K_M prompt_tokens=924 step=1 total_tokens=1060
2026-10-23 10:31:29 [info     ] react.step.final               content='Статус сервиса — «Оптимальный», всё работает нормально. Однако для отправки сообщения в Telegram тре' step=1
INFO Ответ: Статус сервиса — «Оптимальный», всё работает нормально. Однако для отправки сообщения в Telegram требуется идентификатор чата клиента, который вы не указали. Пожалуйста, предоставьте chat_id, чтобы я ...
INFO Корректно: True (OK)
INFO Токены: {'input': 1665, 'output': 300, 'total': 1965}
INFO
============================================================
INFO Задача 5: Провокационная: вопрос без инструментов
INFO ============================================================
INFO
--- agent_naive ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
INFO step=0 финальный ответ
INFO Ответ: В слове 'привет' 6 букв: п-р-и-в-е-т....
INFO Корректно: False (не содержит 'шесть')
INFO Токены: {'input': 636, 'output': 157, 'total': 793}
INFO
--- agent_react ---
INFO HTTP Request: POST http://172.16.30.12:8080/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-23 10:31:33 [info     ] react.step                     completion_tokens=128 iteration_latency_sec=1.874 model=Qwen3.5-9B-Q5_K_M prompt_tokens=735 step=0 total_tokens=863
2026-10-23 10:31:33 [info     ] react.step.final               content="Слово 'привет' состоит из 6 букв." step=0
INFO Ответ: Слово 'привет' состоит из 6 букв....
INFO Корректно: False (не содержит 'шесть')
INFO Токены: {'input': 735, 'output': 128, 'total': 863}
INFO
Отчёт сохранён в: /home/odv/project/MY/Netology-AI-Dev/Diploma/docs/agent-react-report.md
INFO
============================================================
INFO ИТОГИ:
INFO ============================================================
INFO
Задача 1: Простая: K8S - что это
INFO   naive: ✓
INFO   react: ✓
INFO
Задача 2: Простая: поддержка систем
INFO   naive: ✓
INFO   react: ✓
INFO
Задача 3: Средняя: время + статус
INFO   naive: ✓
INFO   react: ✓
INFO
Задача 4: Средняя: статус + отправить уведомление
INFO   naive: ✓
INFO   react: ✓
INFO
Задача 5: Провокационная: вопрос без инструментов
INFO   naive: ✗
INFO   react: ✗
```
#Отчет
[/docs/agent-react-report.md](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.6.2/docs/agent-react-report.md)
