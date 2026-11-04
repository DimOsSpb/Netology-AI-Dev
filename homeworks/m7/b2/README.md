# Блок 7.2 - Воспроизводимость изменения в ML-релизе

---

# [Задание](task.txt)

# Решение

## Шаг 1. Зафиксировано изменение параметра

**Изменённый параметр:** `training.threshold` в `params.yaml`

| Параметр | Значение до | Значение после |
|----------|-------------|----------------|
| `training.threshold` | 0.5 | 0.6 |

**Git SHA:** `0259edf`

**Влияние параметра:** Порог классификации используется для определения риска оттока клиента. Изменение с 0.5 на 0.6 повышает порог, что означает, что только клиенты с более высокой вероятностью оттока будут классифицированы как "high risk".

---

## Шаг 2. Воспроизведение pipeline через DVC

### Вывод команды `dvc repro`:

```
Running stage 'generate_data':                                                 
> python scripts/generate_data.py
Updating lock file 'dvc.lock'                                                  

Running stage 'train':                                                         
> python -m src.churn_ml.training
{
  "roc_auc": 0.7693,
  "average_precision": 0.2919,
  "sentiment_accuracy": 1.0,
  "sentiment_f1": 1.0,
  "train_rows": 3200,
  "test_rows": 800,
  "model_version": "bc436dcba6c8431dac9111d42363630a",
  "model_sha256": "ce756f0211ace41d9ca1372c18916aac7a6f8fa0cabfb4046812270dc75162e9"
}
Updating lock file 'dvc.lock'                                                  

Stage 'monitor' didn't change, skipping
```

### Вывод команды `dvc status`:
```
Data and pipelines are up to date.
```

### Вывод команды `dvc metrics show`:
```
Path                           average_precision    roc_auc    sentiment_accuracy    sentiment_f1    test_rows    train_rows
reports/training_metrics.json  0.2919               0.7693     1.0                   1.0             800          3200
```

**Причинная цепочка:**
1. Изменение параметра `training.threshold` в `params.yaml` влияет на этап `train` в `dvc.yaml`
2. DVC обнаруживает изменение зависимости и запускает пересчёт зависимых этапов
3. Этап `generate_data` пересчитывается (так как `params.yaml` — его зависимость)
4. Этап `train` пересчитывается, используя обновлённые данные и новый параметр threshold
5. Этап `monitor` пропускается, так как его входные данные не изменились
6. `dvc.lock` обновляется с новыми хешами зависимостей и результатов

---

## Шаг 3. Запуск модели в MLflow

**MLflow Run ID:** `bc436dcba6c8431dac9111d42363630a`

**Параметры модели:**
- `name`: hybrid-review-churn
- `threshold`: 0.6 (изменено с 0.5)
- `trained_at`: 2026-11-04T10:49:29.902782+00:00

**Метрики:**
- `roc_auc`: 0.7693
- `average_precision`: 0.2919
- `sentiment_accuracy`: 1.0
- `sentiment_f1`: 1.0
- `train_rows`: 3200
- `test_rows`: 800

**Связь с артефактом модели:**
- SHA256 модели: `ce756f0211ace41d9ca1372c18916aac7a6f8fa0cabfb4046812270dc75162e9`
- Эта SHA256 зафиксирована в `models/model_metadata.json` и используется в паспорте релиза

---

## Шаг 4. Паспорт релиза

### Ключевые поля `release_manifest.json`:

```json
{
  "schema_version": "1.0",
  "service": {
    "version": "0.2.0",
    "git_sha": "0259edf"
  },
  "pipeline": {
    "dvc_lock_sha256": "6142900c88321a62fcdf3ab605652c35cd9034813b19c69cc24d8eed131ad545",
    "params_sha256": "b781c05d0f4153517efbd31bc04fa7d2f259abe168eb163978ea8da800ab25dc",
    "requirements_sha256": "3c3dd07785ecb7eb935634fdd30901abd734d5519b0a4c143250a78a3cbaa704",
    "runtime_requirements_sha256": "05e6ea437b9024ebc96036f598647ee0e6c34d033302106ba10737a78f190d52"
  },
  "data": {
    "reference_sha256": "9b5ba37afbf3703467e694451d7f65a1beec5eace79fc672c1a888c724f67b66",
    "current_sha256": "937b4e57a48888f7c060b97fd8e0c97cbd8277c6e03fcbb5d03786042b9c387f"
  },
  "model": {
    "name": "hybrid-review-churn",
    "mlflow_run_id": "bc436dcba6c8431dac9111d42363630a",
    "sha256": "ce756f0211ace41d9ca1372c18916aac7a6f8fa0cabfb4046812270dc75162e9",
    "threshold": 0.6
  },
  "metrics": {
    "roc_auc": 0.7693,
    "average_precision": 0.2919,
    "sentiment_accuracy": 1.0,
    "sentiment_f1": 1.0,
    "train_rows": 3200,
    "test_rows": 800
  },
  "image": {
    "tag": "mlops-student:0.2.0"
  }
}
```

**Изменённые поля вслед за параметром:**
- `model.threshold`: 0.6 (изменено с 0.5)
- `model.sha256`: новый хеш модели из-за изменения параметра
- `model.mlflow_run_id`: новый ID запуска MLflow
- `pipeline.params_sha256`: новый хеш params.yaml
- `pipeline.dvc_lock_sha256`: новый хеш dvc.lock

---

## Шаг 5. Граница CI и CD

### Проверки в workflow GitHub Actions (`.github/workflows/ci.yml`):

1. **Установка зависимостей:** `pip install -r requirements.txt`
2. **Воспроизведение pipeline:** `dvc repro`
3. **Формирование паспорта релиза:** `python scripts/build_release_manifest.py`
4. **Проверка состояния DVC:** `dvc status` и `dvc metrics show`
5. **Запуск тестов:** `python -m pytest -q`
6. **Сборка Docker-образа:** `docker build --build-arg SERVICE_VERSION=ci ...`
7. **Приложение артефактов:** `dvc.lock`, метрики, metadata, monitoring report, release manifest

### Почему это CI, а не CD:

**CI (Continuous Integration)** — это автоматизированная проверка кода и артефактов перед слиянием. Workflow выполняет:
- ✅ Воспроизведение pipeline для проверки корректности изменений
- ✅ Формирование паспорта релиза для верификации поставки
- ✅ Запуск тестов для проверки функциональности
- ✅ Сборку Docker-образа для проверки совместимости
- ✅ Прикрепление evidence для аудита

**CD (Continuous Deployment/Delivery)** — это автоматизированное развёртывание в production. В данном workflow:
- ❌ **Нет публикации Docker-образа** в реестр (Docker Hub, ECR и т.д.)
- ❌ **Нет развёртывания** в production-окружение
- ❌ **Нет approvals** или gate-процедур перед развёртыванием
- ❌ **Нет мониторинга** production-среды после развёртывания

**Вывод:** Workflow является CI, потому что он **проверяет** и **валидирует** поставку, но не **публикует** и не **развёртывает** её. Публикация образа, approvals и deployment появятся на следующем шаге курса как CD.

---

## Цепочка: параметр → DVC → MLflow → паспорт релиза → CI/CD

```
1. Изменение params.yaml (threshold: 0.5 → 0.6)
   ↓
2. DVC repro обнаруживает изменение и пересчитывает этапы:
   - generate_data (пересчёт)
   - train (пересчёт с новым threshold)
   - monitor (пропуск, данные не изменились)
   ↓
3. MLflow создаёт новый run (bc436dcba6c8431dac9111d42363630a)
   с обновлёнными параметрами и метриками
   ↓
4. build_release_manifest.py формирует паспорт релиза
   связывающий Git SHA, dvc.lock, данные, модель и метрики
   ↓
5. CI workflow валидирует всю цепочку:
   - воспроизводит pipeline
   - проверяет паспорт релиза
   - запускает тесты
   - собирает Docker-образ
   (но не развёртывает — это CI, а не CD)
```

---

## Критерии оценки

| Критерий | Статус |
|----------|--------|
| Изменён ровно один релевантный параметр; значения до и после зафиксированы, влияние объяснено | ✅ |
| DVC-след подтверждён: приведены пересчитанные/актуальные этапы и связь params.yaml → dvc.yaml → dvc.lock | ✅ |
| Указан новый MLflow run ID, параметры и метрики; показана связь с артефактом модели | ✅ |
| Паспорт релиза связывает Git, DVC lock, данные, модель/MLflow run и Docker-образ; секреты отсутствуют | ✅ |
| CI и CD различены корректно: указано отсутствие публикации образа и развёртывания | ✅ |
