from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_repo_root(start_path: Path) -> Path:
    for parent in [start_path] + list(start_path.parents):
        if (parent / ".git").exists():
            return parent
    return start_path


APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = find_repo_root(APP_DIR)


# 1. Описываем схему одного провайдера
class ProviderSettings(BaseModel):
    name: str
    api_key: str | None = None
    base_url: str | None = None
    model: str
    env_key: str | None = None  # Ключ API или Файл с ключем

    # Валидатор, который проверяет api_key.
    # Если там указан путь к файлу (начинается с ~ или /), он прочитает файл.
    @field_validator("api_key", mode="before")
    @classmethod
    def resolve_secret_path(cls, v: str | None) -> str | None:
        res: str = str(v)
        if isinstance(v, str) and (v.startswith("~") or v.startswith("/") or "./" in v):
            path = Path(v).expanduser()
            if path.is_file():
                res = path.read_text(encoding="utf-8").strip()
            else:
                raise FileNotFoundError(f"Файл ключа не найден по пути: {path}")
        return res.replace("\ufeff", "")


# 2. Главный класс настроек
class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", APP_DIR / ".env"),
        extra="allow",
        case_sensitive=True,
    )
    # Провайдер по умолчанию (autoselect). На старте содержит имя ключа .env
    def_provider: str | None = "LLM_PROVIDER"
    # Базовая структура провайдеров
    providers: dict[str, ProviderSettings] = Field(
        default={
            "1": ProviderSettings(
                name="Ollama (локальный)",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                model="qwen2:1.5b",
            ),
            "2": ProviderSettings(
                name="OpenAI",
                model="openai/gpt-oss-120b:free",
                base_url="https://openrouter.ai/api/v1",
                env_key="OPENROUTER_API_KEY",
            ),
            "3": ProviderSettings(
                name="OpenAI",
                model="anthropic/claude-opus-4.8-fast",
                base_url="https://openrouter.ai/api/v1",
                env_key="OPENROUTER_API_KEY",
            ),
        }
    )

    # валидатор объекта, выполняющийся после чтения .env
    @model_validator(mode="after")
    def populate_provider_keys(self) -> "Settings":
        # Извлекаем прочитанные переменные из .env
        env_vars = self.model_extra or {}

        # Провайдер по умолчанию из .env
        if self.def_provider in env_vars:
            def_value = str(env_vars.get(self.def_provider)).lower().strip()
        else:
            def_value = None
        keep_def_key = self.def_provider
        self.def_provider = None

        for key, provider in self.providers.items():
            # Проверяем, задан ли вообще env_key у этого провайдера
            if provider.env_key:
                raw_value = env_vars.get(provider.env_key)
                if isinstance(raw_value, str):
                    provider.api_key = ProviderSettings.resolve_secret_path(raw_value)
            if def_value and def_value in provider.name.lower():
                self.def_provider = key
        if def_value and not self.def_provider:
            print(
                f"Провайдер по умолчанию (.env key={keep_def_key}): {def_value} не найден в config"
            )
        return self


# Инициализируем объект настроек
settings = Settings()
