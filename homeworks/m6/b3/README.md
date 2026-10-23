# Блок 6.3 - LangGraph: основы
---

# [Задание](6-3.md)
# Решение
```python
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run python -m scripts.visualize_graph
saved docs/agent-graph-custom.mmd
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ curl -X POST http://localhost:8000/agent/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "Сколько будет 17 умножить на 23?"}'
{"answer":"17 умножить на 23 равно **391**.","tool_results":[{"name":"multiply","args":{"a":17,"b":23},"result":"391"}]}(diploma)
```

## [Репозиторий с работой](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.6.3)
