# Блок 5.4 - Chunking и оптимизация качества
---

# [Задание](homeworks/m5/b4/5-4.md)
# Решение
## [Репозиторий с работой](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.4)
## Модуль оценки качества RAG [evaluate.py](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.4/tests/eval
```bash
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run -m tests.eval.rag.evaluate

========================================================================
Experiment: fixed_size
------------------------------------------------------------------------
chunk_size=512  overlap=64  top_k=10  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.02s)
  Chunks        :  727 (4.00s)
  Collection    : eval_fixed_size_512_64_k10
  Embedding + Qdrant upload...
  ✓ Index ready  (44.12s)
  Documents     :  114
  Retriever     : top_k=10
  Questions     :   22

Result: fixed_size
------------------------------------------------------------------------
Hit@5       : 0.727
MRR@10      : 0.577
Recall@10   : 0.553
Avg docs    : 10.0
Avg latency : 79.2 ms
Total time  : 49.90 s
========================================================================

========================================================================
Experiment: recursive
------------------------------------------------------------------------
chunk_size=512  overlap=64  top_k=10  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.02s)
  Chunks        : 4507 (0.55s)
  Collection    : eval_recursive_512_64_k10
  Embedding + Qdrant upload...
  ✓ Index ready  (114.91s)
  Documents     :  114
  Retriever     : top_k=10
  Questions     :   22

Result: recursive
------------------------------------------------------------------------
Hit@5       : 0.636
MRR@10      : 0.558
Recall@10   : 0.515
Avg docs    : 10.0
Avg latency : 377.0 ms
Total time  : 123.78 s
========================================================================

========================================================================
Experiment: semantic
------------------------------------------------------------------------
chunk_size=512  overlap=64  top_k=10  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.02s)
  Chunks        :  727 (4.89s)
  Collection    : eval_semantic_512_64_k10
  Embedding + Qdrant upload...
  ✓ Index ready  (39.45s)
  Documents     :  114
  Retriever     : top_k=10
  Questions     :   22

Result: semantic
------------------------------------------------------------------------
Hit@5       : 0.682
MRR@10      : 0.556
Recall@10   : 0.530
Avg docs    : 10.0
Avg latency : 83.2 ms
Total time  : 46.20 s
========================================================================

========================================================================
Experiment: fixed_size
------------------------------------------------------------------------
chunk_size=512  overlap=64  top_k=10  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.02s)
  Chunks        :  727 (3.36s)
  Collection    : eval_fixed_size_512_64_k10
  Embedding + Qdrant upload...
  ✓ Index ready  (40.86s)
  Documents     :  114
  Retriever     : top_k=10
  Questions     :   22

Result: fixed_size
------------------------------------------------------------------------
Hit@5       : 0.727
MRR@10      : 0.577
Recall@10   : 0.553
Avg docs    : 10.0
Avg latency : 80.1 ms
Total time  : 46.00 s
========================================================================

========================================================================
Experiment: fixed_size
------------------------------------------------------------------------
chunk_size=256  overlap=32  top_k=10  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.02s)
  Chunks        : 1407 (3.69s)
  Collection    : eval_fixed_size_256_32_k10
  Embedding + Qdrant upload...
  ✓ Index ready  (56.67s)
  Documents     :  114
  Retriever     : top_k=10
  Questions     :   22

Result: fixed_size
------------------------------------------------------------------------
Hit@5       : 0.682
MRR@10      : 0.573
Recall@10   : 0.485
Avg docs    : 10.0
Avg latency : 120.8 ms
Total time  : 63.04 s
========================================================================

========================================================================
Experiment: fixed_size
------------------------------------------------------------------------
chunk_size=256  overlap=64  top_k=10  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.03s)
  Chunks        : 1616 (3.39s)
  Collection    : eval_fixed_size_256_64_k10
  Embedding + Qdrant upload...
  ✓ Index ready  (65.14s)
  Documents     :  114
  Retriever     : top_k=10
  Questions     :   22

Result: fixed_size
------------------------------------------------------------------------
Hit@5       : 0.682
MRR@10      : 0.543
Recall@10   : 0.485
Avg docs    : 10.0
Avg latency : 166.7 ms
Total time  : 72.24 s
========================================================================

========================================================================
Experiment: fixed_size
------------------------------------------------------------------------
chunk_size=512  overlap=32  top_k=20  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.02s)
  Chunks        :  682 (3.36s)
  Collection    : eval_fixed_size_512_32_k20
  Embedding + Qdrant upload...
  ✓ Index ready  (37.95s)
  Documents     :  114
  Retriever     : top_k=20
  Questions     :   22

Result: fixed_size
------------------------------------------------------------------------
Hit@5       : 0.682
MRR@10      : 0.576
Recall@10   : 0.576
Avg docs    : 20.0
Avg latency : 89.9 ms
Total time  : 43.31 s
========================================================================

========================================================================
Experiment: fixed_size
------------------------------------------------------------------------
chunk_size=512  overlap=64  top_k=20  reranker=OFF
========================================================================
  Building index...
  Documents     :  114 (0.03s)
  Chunks        :  727 (3.59s)
  Collection    : eval_fixed_size_512_64_k20
  Embedding + Qdrant upload...
  ✓ Index ready  (40.58s)
  Documents     :  114
  Retriever     : top_k=20
  Questions     :   22

Result: fixed_size
------------------------------------------------------------------------
Hit@5       : 0.727
MRR@10      : 0.577
Recall@10   : 0.553
Avg docs    : 20.0
Avg latency : 88.6 ms
Total time  : 46.16 s
========================================================================

========================================================================
Experiment: fixed_size
------------------------------------------------------------------------
chunk_size=512  overlap=64  top_k=10  reranker=ON
========================================================================
  Building index...
  Documents     :  114 (0.02s)
  Chunks        :  727 (3.27s)
  Collection    : eval_fixed_size_512_64_k10
  Embedding + Qdrant upload...
  ✓ Index ready  (40.66s)
  Documents     :  114
  Initializing reranker...
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 393/393 [00:00<00:00, 3165.37it/s]
  ✓ Reranker ready (15.72s)
  Re-ranker     : BAAI/bge-reranker-v2-m3
  Re-rank top_n : 10
  Retriever     : top_k=20
  Questions     :   22

Result: fixed_size
------------------------------------------------------------------------
Hit@5       : 0.727
MRR@10      : 0.601
Recall@10   : 0.576
Avg docs    : 10.0
Avg latency : 50248.0 ms
Total time  : 1165.13 s
========================================================================
✓ Report: /home/odv/project/MY/Netology-AI-Dev/Diploma/docs/chunking_report.md
```
## Вывод
- Очень большое значение имеет качество Golden dataset для оценки RAG и в самом корпусе документации (его содержательность и релевантность с dataset) [retrieval_dataset.json](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.4/tests/eval/retrieval_dataset.json)
- Отчет [docs/chunking_report.md](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.4/docs/chunking_report.md)
