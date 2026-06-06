# Добавим мультимодальные возможности к помощнику из Б2.5

- Я выбрал - вариант Б: Голосовой пайплайн (Whisper + TTS)  
- В идеале цель - VoiceAssistant loop (STT→LLM→TTS в реальном времени)

1. Приём пути к аудиофайлу / потоковый режим (реалтайм)
2. Транскрипция через локальный Whisper API (меньше задержка, нет зависимости стоимости и доступности провайдера - на данном этапе я не хочу использовать платные модели)
3. Дополнительный class RobustSTTClient архитектурно по аналогии с RobustLLMClient, но со своей логикой
4. Voice(потоковый режим / file) -> RobustSTTClient -> Получаем Текст |-> далее стандартная логика на RobustLLMClient -> ответ
5. Озвучка через TTS API -> файл
6. Демо: голосовой вопрос -> полный пайплайн

## Порядок действий
- Установка зависимостей
  ### STT - faster-whisper
  - Добавим в /pyproject.toml 
    - uv add faster-whisper & uv sync | (pip install faster-whisper)
    - uv add sounddevice soundfile & uv sync
    - sudo apt install portaudio19-dev
  ### TTS - piper
  - wget -O - https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz | tar -xz -C ./infrastructure/tts/piper/bin
  - wget -P ./infrastructure/tts/piper/models https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx
  - wget -P ./infrastructure/tts/piper/models https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json
## Доработки и оптимизации
- В assistant оптимизирована работа с командами - стало удобней, убраны повторы логики и текста
- Настройка логирования вынесена в начало программы (устранен шум в консоль)
- RobustSTTClient
- RobustTTSClient
- Запись и озвучивание речи

## Пример вывода STT→LLM→TTS в реальном времени
```bash
(netology-ai-dev) odv@matebook16s:~/project/MY/Netology-AI-Dev/homeworks/m2-ai-api-integration/b06_mm_suppassist$ python __main__.py
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


Вы: /v
Говорите...
Распознаю речь...
Распознано: ошибка 413 что она значит
[technical | primary | 6.55с]
Озвучиваю...
response.mp3
```
- INPUT - [input.wav](input.wav)
- OUTPUT - [response.mp3](response.mp3)
