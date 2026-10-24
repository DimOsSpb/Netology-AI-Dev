# Блок 6.4 - LangGraph: продвинутые паттерны
---

## [Репозиторий с работой](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.6.4)

## Решение
```python
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ curl -X POST localhost:8000/agent/chat -H 'Content-Type: application/json' \
  -d '{"message":"Вызови send_email: to=client@example.com, subject=Счёт, body=Ваш счёт","thread_id":"t1"}'
{"status":"interrupted","thread_id":"t1","answer":null,"tool_results":[],"interrupt":{"type":"approve_email","preview":{"to":"client@example.com","subject":"Счёт","body":"Ваш счёт","tool_call_id":"JoASZ9fSYUljHtPLvb2IOGdT7VZoBGum"}}}
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ curl -X POST localhost:8000/agent/resume -H 'Content-Type: application/json' \
  -d '{"thread_id":"t1","decision":true}'
{"status":"done","thread_id":"t1","answer":"Письмо успешно отправлено клиенту на адрес client@example.com с темой «Счёт».","tool_results":[{"name":"send_email","args":{"to":"client@example.com","subject":"Счёт","body":"Ваш счёт","tool_call_id":"JoASZ9fSYUljHtPLvb2IOGdT7VZoBGum"},"result":"письмо отправлено: Счёт"}],"interrupt":null}
```
