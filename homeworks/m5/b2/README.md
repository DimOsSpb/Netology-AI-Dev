# Блок 5.2 - Векторные базы данных
---

# [Задание](https://u.netology.ru/backend/uploads/lms/content_assets/file/16047/self-practice-5-2.pdf)
# Решение
## [Репозиторий с работой](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2)
1. [Qdrant в docker-compose.yml](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/compose.yaml)
2. [Подключение клиента и конфиг](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/app/core/config.py#L74-L80)
3. [Скрипт загрузки 100+ документов в data/kb](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/scripts/embedding/kb-builder/main.py)
  - [100+ документов](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/data/kb)
4. [Скрипт scripts/embedding/loaders/load_to_qdrant.py](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/scripts/generate_report.py)
```bach
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run -m scripts.embedding.loaders.load_to_qdrant
============================================================
load_to_qdrant.py — загрузка документов в Qdrant
============================================================
  ✓ Qdrant доступен
  ✓ Создана коллекция 'documents' (dim=1024)
  ✓ Создан индекс для 'source'
  ✓ Создан индекс для 'created_at'
  ✓ Создан индекс для 'category'
  ✓ Создан индекс для 'tenant_id'
  ✓ Создан индекс для 'department'
  📄 Найдено 114 документов
  ✓ Разбиение и векторизация: 114 документов за 45.0 с (2.53 док./с)
  ✓ Сгенерировано 991 точек
  ⏳ Батч 1/4 (25.8%) — 256 точек
  ⏳ Батч 2/4 (51.7%) — 256 точек
  ⏳ Батч 3/4 (77.5%) — 256 точек
  ⏳ Батч 4/4 (100.0%) — 223 точек

============================================================
📊 Итого в коллекции: 991 точек
============================================================
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run -m scripts.embedding.loaders.load_to_qdrant
============================================================
load_to_qdrant.py — загрузка документов в Qdrant
============================================================
  ✓ Qdrant доступен
  ✓ Коллекция 'documents' существует (dim=1024)
  📄 Найдено 114 документов
  ✓ Разбиение и векторизация: 114 документов за 41.7 с (2.74 док./с)
  ✓ Сгенерировано 991 точек
  ⏳ Батч 1/4 (25.8%) — 256 точек
  ⏳ Батч 2/4 (51.7%) — 256 точек
  ⏳ Батч 3/4 (77.5%) — 256 точек
  ⏳ Батч 4/4 (100.0%) — 223 точек

============================================================
📊 Итого в коллекции: 991 точек
============================================================
```
5. [Модуль app/services/vector_store.py](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/app/services/vector_store.py)
6. [Cosine vs Dot product. На 5 запросах из предметной области](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/scripts/embedding/benchmarks/distance_metric.py)
```bash
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run -m scripts.embedding.benchmarks.distance_metric
Создание тестовых коллекций...
Cosine
  ✓ Коллекция 'documents_cosine' существует (dim=1024)
  ⏳ Батч 1/1 (100.0%) — 256 точек
  ⏳ Батч 1/1 (100.0%) — 256 точек
  ⏳ Батч 1/1 (100.0%) — 256 точек
  ⏳ Батч 1/1 (100.0%) — 223 точек
Dot
  ✓ Коллекция 'documents_dot' существует (dim=1024)
  ⏳ Батч 1/1 (100.0%) — 256 точек
  ⏳ Батч 1/1 (100.0%) — 256 точек
  ⏳ Батч 1/1 (100.0%) — 256 точек
  ⏳ Батч 1/1 (100.0%) — 223 точек

====================================================================================================
Cosine vs Dot Product
====================================================================================================

❓ Почему pod постоянно перезапускается?
   COSINE : d2d336ee → 325d7498 → b9e371df → 578de017 → 1bb99966
   DOT    : d2d336ee → 325d7498 → b9e371df → 578de017 → 1bb99966
   Match  : ✓ Yes

❓ Почему PVC не монтируется?
   COSINE : 6f529c47 → 957d04d9 → c47388a6 → 148a81fa → 9a9a7876
   DOT    : 6f529c47 → 957d04d9 → c47388a6 → 148a81fa → 9a9a7876
   Match  : ✓ Yes

❓ Какая нагрузка на worker node?
   COSINE : 446f24d8 → c47388a6 → 55a8a804 → b397ed18 → 40460a4a
   DOT    : 446f24d8 → c47388a6 → 55a8a804 → b397ed18 → 40460a4a
   Match  : ✓ Yes

❓ Почему nginx возвращает 502 Bad Gateway?
   COSINE : b95236b2 → 55a8a804 → 40460a4a → ababf8eb → b2362162
   DOT    : b95236b2 → 55a8a804 → 40460a4a → ababf8eb → b2362162
   Match  : ✓ Yes

❓ Есть ли ошибки подключения к Redis?
   COSINE : c47388a6 → 6eddf9d0 → fadd8346 → ce13e69c → 6e4af7b1
   DOT    : c47388a6 → 6eddf9d0 → fadd8346 → ce13e69c → 6e4af7b1
   Match  : ✓ Yes

====================================================================================================
Summary
====================================================================================================
Queries checked   : 5
Identical ranking : 5/5 (100%)
Conclusion        : COSINE and DOT produce identical ranking.
Production metric : COSINE
```
7. [Фильтрация по metadata](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.5.2/scripts/embedding/benchmarks/metadata_filter.py)
- Range по дате не делал, т.к. документы все одной даты
```bash
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ uv run -m scripts.embedding.benchmarks.metadata_filter

====================================================================================================
Match по строке
====================================================================================================
Query: 'Что такое Kube-proxy?'
Filter: key: 'category' value 'networking'
Top 3:
   bf5dce51: k8s-00048: kube-proxy — сетевой прокси, работающий на каждом в кластере и реализующий часть концепции Kubernetes. <!--more--> [kube-proxy](/docs/reference/comman
   4d57a8d0: k8s-00091: <!-- overview --> На этой странице рассказывается о различных типах прокси-серверов, которые используются в Kubernetes. <!-- body --> ## Прокси-сервер
   c511e8ab: k8s-00040: Абстрактный способ представления приложения, запущенного в наборе , в виде сетевого сервиса. <!--more--> Набор подов, из которых состоит сервис, опред

====================================================================================================
Композитный must + must_not
====================================================================================================
Query: 'Что такое Kube-proxy?'
Filter: key: 'category' value 'networking'
Filter: not_key: 'id' not_value 'k8s-00091'
Top 3 composi:
   bf5dce51: k8s-00048: kube-proxy — сетевой прокси, работающий на каждом в кластере и реализующий часть концепции Kubernetes. <!--more--> [kube-proxy](/docs/reference/comman
   c511e8ab: k8s-00040: Абстрактный способ представления приложения, запущенного в наборе , в виде сетевого сервиса. <!--more--> Набор подов, из которых состоит сервис, опред
   e0abaf09: k8s-00081: <!-- overview --> Этот документ описывает связь между API-сервером и кластером Kubernetes. Цель состоит в том, чтобы позволить пользователям настраива
```
