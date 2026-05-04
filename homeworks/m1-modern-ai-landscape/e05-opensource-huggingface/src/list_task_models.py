from huggingface_hub import HfApi

api = HfApi()

# Поиск 3-х популярных моделей для summarization
#
task = "summarization"
limit = 100
free_licenses = [  # Полностью свободные лицензий для проверки
    "apache-2.0",
    "mit",
    "bsd-3-clause",
    "bsd-2-clause",
    "cc0-1.0",
    "unlicense",
    "mpl-2.0",
]
selected_models = []

print(f"Топ-3 из {limit} моделей для summarization:\n")

models = list(
    api.list_models(
        pipeline_tag=task,
        sort="downloads",  # Сортируем по популярности
        limit=limit,
    )
)

for model in models:
    model_info = api.model_info(repo_id=model.id)
    license = None
    language = None
    size = None

    print(f"\r      {model_info.id:<100}", end="", flush=True)

    if model_info.safetensors and "total" in model_info.safetensors:
        size = model_info.safetensors["total"] / (1024**3)
        if size > 3:
            continue  # Gb
    else:
        continue

    if model_info.cardData and "license" in model_info.cardData:
        license_value = model_info.cardData["license"]
        if isinstance(license_value, list):
            license_value = ", ".join(license_value).lower()
        if not license_value:
            continue
        if license_value.lower() not in free_licenses:
            continue
    else:
        continue

    if model_info.cardData and "language" in model_info.cardData:
        language = model_info.cardData["language"]
        if isinstance(language, list):
            language = ", ".join(language).lower()
        if not language:
            continue
        if "ru" not in language:
            continue
    else:
        continue

    print("\rOK -> ", end="")
    selected_models.append({
        "id": model.id,
        "license": license,
        "downloads": model.downloads,
        "lang": language,
        "likes": model.likes,
        "size": size,
    })

selected_models = sorted(
    selected_models, key=lambda x: (x["likes"], x["downloads"]), reverse=True
)
print(
    f'\rРезультат отбора "Топ-3 из {limit} моделей для summarization"' + " " * 50,
    flush=True,
)
print("=" * 91)
print(
    f"{'N':<2} | {'ID задачи':<45} | {'Загрузок':<10} | {'Лайки':<10} | {'Размер':<10} |"
)
print("=" * 91)

if len(selected_models) > 0:
    for index, selected in enumerate(selected_models[:3], start=1):
        size_display = f"{selected['size']:.2f} GB"
        print(
            f"{index:<2} | {selected['id']:<45} | {selected['downloads']:<10} | {selected['likes']:<10} | {size_display:<10} |"
        )
