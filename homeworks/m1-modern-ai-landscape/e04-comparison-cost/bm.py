import json
import time

from eval_set import TASKS
from openai import OpenAI

SYSTEM_PROMPT = """Ты — K8s Infra Dispatcher. Анализируй событие и отвечай ТОЛЬКО JSON:
{
  "severity": "critical|warning|info",
  "category": "compute|network|storage|config|security|unknown",
  "action": "ignore|log_only|diagnose|auto_fix|escalate|diagnose_and_escalate",
  "suggested_commands": ["kubectl ..."],
  "summary": "краткое объяснение на русском"
}
Не добавляй текст до или после JSON."""


def read_api_key(path: str) -> str:
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read().strip()


def benchmark_model(model_cfg: dict) -> dict:

    client = OpenAI(base_url=model_cfg["base_url"], api_key=model_cfg["api_key"])
    name = model_cfg["model"]

    print(f"\nTesting: {name}")
    print(f"{'=' * 40}")

    total_accuracy = 0
    total_ttft = 0.0
    total_tokens = 0
    results = []

    for task in TASKS:
        prompt = f"{SYSTEM_PROMPT}\n\nСобытие:\n{json.dumps(task['event'], indent=2)}"

        start = time.perf_counter()
        stream = client.chat.completions.create(
            model=model_cfg["model"],
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            temperature=0.1,
            max_tokens=500,
        )

        first_token = True
        response_text = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                if first_token:
                    ttft = time.perf_counter() - start
                    first_token = False
                response_text += chunk.choices[0].delta.content

        total_ttft += ttft

        try:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            response_obj = json.loads(response_text[json_start:json_end])
            passed = task["validate"](response_obj)
        except Exception as e:
            passed = False
            response_obj = {"json error": str(e), "raw": response_text[:100]}

        total_tokens += len(response_text.split())

        if passed:
            total_accuracy += 1

        status = "Ok" if passed else "False"
        print(f"  {task['id']}: {status} (ttft={ttft:.2f} sek)")
        results.append({"id": task["id"], "passed": passed, "ttft": ttft})

    accuracy = total_accuracy / len(TASKS)
    avg_ttft = total_ttft / len(TASKS)
    throughput = len(TASKS) / total_ttft if total_ttft > 0 else 0

    print(f"\n  Results for {name}")
    print(f"{'-' * 30}")
    print(f"  Accuracy: {accuracy:.2%}")
    print(f"  Avg TTFT: {avg_ttft:.2f}s")
    print(f"  Throughput: {throughput:.2f} req/s")
    print(f"  Avg tokens: {total_tokens // len(TASKS)}")

    return {
        "model": name,
        "accuracy": accuracy,
        "avg_ttft": avg_ttft,
        "throughput": throughput,
        "avg_output_tokens": total_tokens // len(TASKS),
        "results": results,
    }


def calculate_local_cost(
    model_cfg: dict, requests_per_day: int, days: int = 90
) -> dict:
    """С учетом стоимости инфраструктуры и владения"""

    # Реалистичные цены (2025 год, б.у. оборудование)
    # 4x NVIDIA V100 16GB SXM2 (сейчас б.у. 15000) + плата NVLink (50000)
    gpu_cost_rub = 4 * 15000 + 50000  # 110 000 руб
    server_hardware_rub = 150000  # CPU, RAM, БП, корпус, SSD
    hardware_cost_rub = gpu_cost_rub + server_hardware_rub

    # Администрирование
    monthly_admin_hours = 8
    admin_hourly_rate_rub = 1000
    admin_cost_rub = monthly_admin_hours * admin_hourly_rate_rub * (days / 30)

    # Охлаждение, интернет, резервирование
    misc_cost_rub = 5000 * (days / 30)  # 5000 руб/мес

    # Электроэнергия - простой
    base_power_kw = 0.08  # 80W

    # Мощность зависит от размера модели
    size_b = model_cfg.get("size_b", 7.0)
    gpu_utilization = min(1.0, size_b / 7.0)
    power_gpu_w = size_b * 30 * gpu_utilization
    power_load_kw = (power_gpu_w * 4 * gpu_utilization) / 1000

    total_power_kw = base_power_kw + power_load_kw

    hours = days * 24
    kwh = total_power_kw * hours
    electricity_rate_rub = 7  # руб/kWh
    electricity_cost_rub = kwh * electricity_rate_rub

    total_cost_rub = (
        hardware_cost_rub + electricity_cost_rub + admin_cost_rub + misc_cost_rub
    )

    total_requests = requests_per_day * days
    cost_per_request_rub = total_cost_rub / total_requests if total_requests > 0 else 0

    return {
        "model": model_cfg["model"],
        "type": "local",
        "size_b": size_b,
        "hardware_cost_rub": hardware_cost_rub,
        "gpu_cost_rub": gpu_cost_rub,
        "server_cost_rub": server_hardware_rub,
        "electricity_cost_rub": electricity_cost_rub,
        "admin_cost_rub": admin_cost_rub,
        "misc_cost_rub": misc_cost_rub,
        "total_cost_rub": total_cost_rub,
        "period_days": days,
        "total_requests": total_requests,
        "cost_per_request_rub": cost_per_request_rub,
        "base_power_kw": base_power_kw,
        "power_gpu_w": power_gpu_w,
        "total_power_kw": total_power_kw,
    }


def calculate_cloud_cost(
    model_cfg: dict,
    avg_input_tokens: int,
    avg_output_tokens: int,
    requests_per_day: int,
    days: int = 90,
) -> dict:
    """Рассчитывает стоимость облачной модели за указанный период"""

    price = model_cfg.get("price", {"input": 0, "output": 0})
    cache_reduction = model_cfg.get("cache_reduction", 0.1)  # кэш дешевле в 10 раз
    cache_hit_rate = model_cfg.get("cache_hit_rate", 0.3)
    exchange_rate = 80  # курс рубль/доллар

    total_requests = requests_per_day * days

    total_input_tokens = avg_input_tokens * total_requests
    total_output_tokens = avg_output_tokens * total_requests

    cost_input_usd = total_input_tokens / 1_000_000 * price["input"]
    cost_output_usd = total_output_tokens / 1_000_000 * price["output"]
    total_cost_usd = cost_input_usd + cost_output_usd
    total_cost_rub = total_cost_usd * exchange_rate

    # С кэшированием
    cached_requests = total_requests * cache_hit_rate
    non_cached_requests = total_requests - cached_requests

    cost_with_cache_usd = (
        total_cost_usd * (non_cached_requests / total_requests)
        + total_cost_usd * (cached_requests / total_requests) * cache_reduction
    )
    cost_with_cache_rub = cost_with_cache_usd * exchange_rate

    return {
        "model": model_cfg["model"],
        "type": "cloud",
        "input_price_usd": price["input"],
        "output_price_usd": price["output"],
        "avg_input_tokens": avg_input_tokens,
        "avg_output_tokens": avg_output_tokens,
        "requests_per_day": requests_per_day,
        "period_days": days,
        "total_requests": total_requests,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "cost_input_rub": cost_input_usd * exchange_rate,
        "cost_output_rub": cost_output_usd * exchange_rate,
        "cost_total_rub": total_cost_rub,
        "cache_hit_rate": cache_hit_rate,
        "cache_reduction": cache_reduction,
        "cost_with_cache_rub": cost_with_cache_rub,
        "savings_percent": (1 - cost_with_cache_usd / total_cost_usd) * 100
        if total_cost_usd > 0
        else 0,
    }


OPENROUTER_KEY = read_api_key("/home/odv/.secret/openrouter-netology-key")

MODELS = [
    # ЛОКАЛЬНЫЕ
    {
        "type": "local",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
        "model": "phi3:mini",
        "bench": True,
        "cost": True,
        "size_b": 3.8,
    },
    {
        "type": "local",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
        "model": "qwen2:1.5b",
        "bench": True,
        "cost": True,
        "size_b": 1.5,
    },
    {
        "type": "local",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
        "model": "gemma2:2b",
        "bench": True,
        "cost": True,
        "size_b": 2.0,
    },
    # ОБЛАЧНЫЕ
    {
        "type": "cloud",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": OPENROUTER_KEY,
        "model": "openai/gpt-oss-120b:free",
        "price": {"input": 0, "output": 0},
        "bench": True,
        "cost": False,
        "cache_reduction": 0.1,
        "cache_hit_rate": 0.3,
    },
    {
        "type": "cloud",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": OPENROUTER_KEY,
        "model": "openai/gpt-4o-mini",
        "price": {"input": 0.15, "output": 0.60},
        "bench": False,
        "cost": True,
        "cache_reduction": 0.1,
        "cache_hit_rate": 0.3,
    },
    {
        "type": "cloud",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": OPENROUTER_KEY,
        "model": "google/gemini-2.0-flash-exp",
        "price": {"input": 0.10, "output": 0.40},
        "bench": False,
        "cost": True,
        "cache_reduction": 0.1,
        "cache_hit_rate": 0.3,
    },
    {
        "type": "cloud",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": OPENROUTER_KEY,
        "model": "anthropic/claude-3-haiku",
        "price": {"input": 0.25, "output": 1.25},
        "bench": False,
        "cost": True,
        "cache_reduction": 0.1,
        "cache_hit_rate": 0.3,
    },
    {
        "type": "cloud",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": OPENROUTER_KEY,
        "model": "mistralai/mistral-7b-instruct",
        "price": {"input": 0.07, "output": 0.07},
        "bench": False,
        "cost": True,
        "cache_reduction": 0.1,
        "cache_hit_rate": 0.3,
    },
]


def format_number(num):
    return f"{num:,.0f}".replace(",", " ")


if __name__ == "__main__":
    print("Benchmark моделей под проект - K8s Infra Dispatcher")
    print(f"Total tasks: {len(TASKS)}")

    # Бенчмарк
    benchmark_results = []
    for cfg in MODELS:
        if cfg.get("bench", False):
            try:
                result = benchmark_model(cfg)
                benchmark_results.append(result)
            except Exception as e:
                print(f"\nFailed to test {cfg['model']}: {e}")

    # Итоговая таблица бенчмарка
    if benchmark_results:
        print("\n  РЕЗУЛЬТАТЫ БЕНЧМАРКА")
        print("=" * 90)
        print(f"{'Модель':<45} {'Точность':<12} {'Ср. TTFT (с)':<15} {'req/sec':<18}")
        print("-" * 90)
        for r in sorted(benchmark_results, key=lambda x: x["accuracy"], reverse=True):
            print(
                f"{r['model']:<45} {r['accuracy']:3.2%}       {r['avg_ttft']:.2f}             {r['throughput']:.2f}"
            )

    # Расчёт стоимости
    REQUESTS_PER_DAY = 500_000  # Прикинул логи в кластерах за день +-
    AVG_INPUT_TOKENS = 500
    PERIOD_DAYS = 90

    all_costs = []

    # Локальные модели
    for cfg in MODELS:
        if cfg.get("type") == "local" and cfg.get("cost", False):
            existing_result = next(
                (r for r in benchmark_results if r["model"] == cfg["model"]), None
            )
            avg_output = (
                existing_result["avg_output_tokens"] if existing_result else 200
            )
            cost = calculate_local_cost(cfg, REQUESTS_PER_DAY, days=PERIOD_DAYS)
            cost["avg_output_tokens"] = avg_output
            all_costs.append(cost)

    # Облачные модели
    for cfg in MODELS:
        if cfg.get("type") == "cloud" and cfg.get("cost", False):
            existing_result = next(
                (r for r in benchmark_results if r["model"] == cfg["model"]), None
            )
            avg_output = (
                existing_result["avg_output_tokens"] if existing_result else 200
            )
            cost = calculate_cloud_cost(
                cfg, AVG_INPUT_TOKENS, avg_output, REQUESTS_PER_DAY, days=PERIOD_DAYS
            )
            all_costs.append(cost)

    # Отчёт по стоимости
    if all_costs:
        print("\n\n РАСЧЁТ СТОИМОСТИ")
        print(
            f" {REQUESTS_PER_DAY:,.0f} запросов в день, за период {PERIOD_DAYS} дней".replace(
                ",", " "
            )
        )
        print("=" * 90)

        local_costs = [c for c in all_costs if c["type"] == "local"]
        cloud_costs = [c for c in all_costs if c["type"] == "cloud"]

        # Локальные модели
        if local_costs:
            days_local = local_costs[0]["period_days"]
            print(f"\nЛОКАЛЬНЫЙ GPU СЕРВЕР (TCO руб)")
            print("-" * 90)
            print(
                f"{'Модель':<25} {'Размер':<10} {'Мощность (кВт)':<16} {'Электричество':<22} {'TCO':<18} {'руб/req':<12}"
            )
            print("-" * 90)
            for c in sorted(local_costs, key=lambda x: x["size_b"]):
                elec = format_number(c["electricity_cost_rub"])
                tco = format_number(c["total_cost_rub"])
                print(
                    f"{c['model']:<25} {c['size_b']:.1f}B          {c['total_power_kw']:.2f}              {elec:>15}        {tco:>15}        {c['cost_per_request_rub']:.6f}"
                )

        # Облачные модели
        if cloud_costs:
            days_cloud = cloud_costs[0]["period_days"]
            print(f"\nОБЛАЧНЫЕ МОДЕЛИ (за {days_cloud} дней, курс 80 руб/$)")
            print("-" * 120)
            print(
                f"{'Модель':<45} {'Вход ($/1M)':<14} {'Выход ($/1M)':<15} {'Всего (руб)':<16} {'С кэшем (руб)':<16}"
            )
            print("-" * 120)
            for c in sorted(cloud_costs, key=lambda x: x["cost_total_rub"]):
                total = format_number(c["cost_total_rub"])
                total_cache = format_number(c["cost_with_cache_rub"])
                # Фиксированные отступы
                input_str = f"${c['input_price_usd']}/M"
                output_str = f"${c['output_price_usd']}/M"
                print(
                    f"{c['model']:<45} {input_str:<14} {output_str:<15} {total:>16} {total_cache:>16}"
                )

        # Сравнение
        paid_cloud_costs = [c for c in cloud_costs if c["cost_total_rub"] > 0]

        if local_costs and paid_cloud_costs:
            print("\nСРАВНЕНИЕ (ЗА 90 ДНЕЙ) — ТОЛЬКО ПЛАТНЫЕ ОБЛАЧНЫЕ МОДЕЛИ")
            print("=" * 100)

            avg_local = local_costs[0]
            local_total = avg_local["total_cost_rub"]

            print(f"\nЛокальный сервер (за 90 дней): {format_number(local_total)} руб")
            print(
                f"Стоимость одного запроса: {avg_local['cost_per_request_rub']:.6f} руб"
            )

            print("\nСравнение с платными облачными моделями (за 90 дней):")
            print("-" * 100)
            print(
                f"{'Модель':<45} {'Облачно (руб)':<20} {'Локально (руб)':<20} {'Разница (%)':<15}"
            )
            print("-" * 100)

            for c in sorted(paid_cloud_costs, key=lambda x: x["cost_total_rub"]):
                cloud_total = c["cost_total_rub"]
                diff_pct = (
                    ((cloud_total - local_total) / local_total) * 100
                    if local_total > 0
                    else 0
                )
                cloud_str = format_number(cloud_total)
                local_str = format_number(local_total)
                print(
                    f"{c['model']:<45} {cloud_str:>15}          {local_str:>15}          {diff_pct:>+6.1f}%"
                )

            # Точка безубыточности для платных моделей
            print("\nТОЧКА БЕЗУБЫТОЧНОСТИ (окупаемость железа):")
            print("-" * 100)
            hardware_cost = avg_local["hardware_cost_rub"]
            print(f"Стоимость железа: {format_number(hardware_cost)} руб")

            for c in paid_cloud_costs:
                cloud_total = c["cost_total_rub"]
                diff_90d = cloud_total - local_total

                if diff_90d > 0:
                    saving_per_month = diff_90d / 3
                    months = hardware_cost / saving_per_month
                    if months < 60:
                        print(f"  - {c['model']}: {months:.1f} месяцев")
                    else:
                        print(f"  - {c['model']}: не окупится ({months:.0f} месяцев)")
                elif diff_90d < 0:
                    saving_per_month = -diff_90d / 3
                    print(
                        f"  - {c['model']}: облако дешевле на {format_number(saving_per_month)} руб/мес. Локальный сервер НЕ ОКУПАЕТСЯ"
                    )
                else:
                    print(f"  - {c['model']}: стоимость одинакова")
