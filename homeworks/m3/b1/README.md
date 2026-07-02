# Блок 3.1 — Function Calling и продвинутый промпт-инжиниринг

[В дипломный репозиторий](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/main) добавляется 1-3 инструмента, релевантный предметной области
проекта, и прогоняется полный цикл Function Calling: JSON Schema → запрос → парсинг
tool_calls → выполнение функции → возврат результата → финальный ответ.  

## Выбран tools:

Техподдержка (SaaS): pve_status() - получить текущее состояние кластера Proxmox VE.

## Задачи
- [Описать tool через JSON Schema](https://github.com/DimOsSpb/AI-Dev-Diploma/blob/9c2be24513686ece494946acebd9918ad2f3af31/packages/infraassist/src/infraassist/tools/schemas.py)
- [Реализовать функцию-обработчик](https://github.com/DimOsSpb/AI-Dev-Diploma/blob/9c2be24513686ece494946acebd9918ad2f3af31/packages/infraassist/src/infraassist/tools/handlers.py)
- [Вынести промпты в отдельные файлы](https://github.com/DimOsSpb/AI-Dev-Diploma/blob/9c2be24513686ece494946acebd9918ad2f3af31/packages/infraassist/src/infraassist/prompts/system_prompt.txt)
- Реализовать полный цикл tool_call на одном из SDK. Прогнать на трёх запросах.
```bash
=== InfraAssist Support CLI ===
Доступные команды:
/clear                       (/c)   - Очисттка истории
/clear_cache                 (/cc)  - Очистка кеш
/reset_redis_stats           (/rrs) - Сброс статистики Redis
/stats                       (/s)   - Вывод статистики
/quit                        (/q)   - Выход из приложения
/transcribe <file> [вопрос]  (/t)   - Распознать речь из файла
/speak                       (/sp)  - Голосовой вывод последнего ответа модели
/voice                       (/v)   - Полностью голосовой pipeline (STT→LLM→TTS в реальном времени)


Вы: Состояние pve?
[faq | primary | 26.94с]
Кластер Proxmox в состоянии **quorate** (доступен кворум). Все 4 узла онлайн:

- pve0 (IP 192.168.0.218)
- pve1 (IP 192.168.0.217) – локальный узел
- pve10 (IP 192.168.0.211)
- pve11 (IP 192.168.0.212)

Если нужен более детальный статус конкретного узла, уточните его имя.

Вы: pve1?
[faq | primary | 16.49с]
Узел **pve1** (IP 192.168.0.217) находится в онлайн‑режиме, локальный для текущего подключения. Кворум кластера достигнут, остальные узлы также онлайн. Если требуется выполнить действия на этом узле — дайте знать.

Вы: Ошибка 401 что значит?
[faq | primary | 17.58с]
Ошибка **401 Unauthorized** означает, что запрос был отклонён из‑за отсутствия или неверных учётных данных. Проверьте, что вы передаёте корректный токен/логин‑пароль и что у вашей учётной записи есть необходимые права доступа к API Proxmox. При необходимости обновите токен или выполните повторный вход.

Вы: Перечисли виртуалки на pve0
[faq | primary | 245.34с]
На узле **pve0** в текущем ответе нет данных о виртуальных машинах. Чтобы получить список VM, выполните запрос к API Proxmox /​nodes/pve0/qemu. Если нужна помощь с формированием запроса — дайте знать.
```
- [Добавить логирование каждого шага](https://github.com/DimOsSpb/AI-Dev-Diploma/blob/9c2be24513686ece494946acebd9918ad2f3af31/packages/infraassist/src/infraassist/infrastructure/assistant.log)
```bash
2026-06-12T13:40:31.961140+0300 Function call: 'pve_status' args: {'check_quorum_only': False, 'include_nodes': True, 'specific_node': 'pve1'}
2026-06-12T13:40:32.029782+0300 Function result: '[{'name': 'pm1', 'nodes': 4, 'type': 'cluster', 'id': 'cluster', 'quorate': 1, 'version': 10}, {'online': 1, 'level': '', 'type': 'node', 'id': 'node/pve0', 'name': 'pve0', 'nodeid': 1, 'local': 0, 'ip': '192.168.0.218'}, {'local': 0, 'nodeid': 3, 'ip': '192.168.0.211', 'name': 'pve10', 'id': 'node/pve10', 'type': 'node', 'online': 1, 'level': ''}, {'id': 'node/pve1', 'type': 'node', 'online': 1, 'level': '', 'nodeid': 2, 'local': 1, 'ip': '192.168.0.217', 'name': 'pve1'}, {'id': 'node/pve11', 'type': 'node', 'online': 1, 'level': '', 'local': 0, 'nodeid': 4, 'ip': '192.168.0.212', 'name': 'pve11'}]'
2026-06-12T13:40:37.941474+0300 faq | primary/openai/gpt-oss-120b:free | 1518 tok | 16.494s | cache=False | Q: pve1? | A: Узел **pve1** (IP 192.168.0.217) находится в онлайн‑режиме, локальный для текущего подключения. Квор
2026-06-12T13:41:29.271879+0300 faq | primary/openai/gpt-oss-120b:free | 797 tok | 17.579s | cache=False | Q: Ошибка 401 что значит? | A: Ошибка **401 Unauthorized** означает, что запрос был отклонён из‑за отсутствия или неверных учётных 
2026-06-12T13:44:10.026961+0300 Function call: 'pve_status' args: {'check_quorum_only': False, 'include_nodes': True, 'specific_node': 'pve0'}
2026-06-12T13:44:46.884620+0300 Function result: '[{'name': 'pm1', 'nodes': 4, 'id': 'cluster', 'type': 'cluster', 'quorate': 1, 'version': 10}, {'id': 'node/pve10', 'type': 'node', 'online': 1, 'level': '', 'local': 0, 'nodeid': 3, 'ip': '192.168.0.211', 'name': 'pve10'}, {'level': '', 'online': 1, 'type': 'node', 'id': 'node/pve0', 'name': 'pve0', 'ip': '192.168.0.218', 'local': 0, 'nodeid': 1}, {'ip': '192.168.0.212', 'local': 0, 'nodeid': 4, 'name': 'pve11', 'id': 'node/pve11', 'type': 'node', 'level': '', 'online': 1}, {'ip': '192.168.0.217', 'nodeid': 2, 'local': 1, 'name': 'pve1', 'id': 'node/pve1', 'type': 'node', 'level': '', 'online': 1}]'
2026-06-12T13:47:53.891313+0300 faq | primary/openai/gpt-oss-120b:free | 1941 tok | 245.339s | cache=False | Q: Перечисли виртуалки на pve0 | A: На узле **pve0** в текущем ответе нет данных о виртуальных машинах. Чтобы получить список VM, выполн
```

## Вывод
- По всем вопросам относительно кластера PVE модель вызвала функцию и адекватно обработала данные из функции, сформировав правильный ответ
- Если функция не предоставила нужной информации, модель это отметила и предложила добавить функционал
- На вопрос не связаный с кластером (Ошибка 401 что значит?), модель не вызывала функцию
