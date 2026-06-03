from pathlib import Path
from typing import ClassVar

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_repo_root(start_path: Path) -> Path:
    for parent in [start_path] + list(start_path.parents):
        if (parent / ".git").exists():
            return parent
    return start_path


app_dir = Path(__file__).resolve().parent
root_dir = find_repo_root(app_dir)


# 2. Главный класс настроек
class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=(app_dir / ".env"),
        extra="ignore",
    )
    service_name: str = Field(default="SupportAssistent")
    # Основной провайдер (OpenAI-совместимый API)
    api_key: str | None
    base_url: str
    primary_model: str

    # Fallback-провайдер (OpenAI-совместимый API)
    fallback_api_key: str | None = Field(default="")
    fallback_base_url: str = Field(default="")
    fallback_model: str = Field(default="")
    # Общие настройки
    request_timeout_seconds: float = Field(default=30)
    retry_attempts: int = Field(default=3)
    history_limit: int = Field(default=10)
    log_path: Path = Field(default=app_dir / "assistant.log")
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_ttl: int = Field(default=3600)

    # API KEY валидатор
    @staticmethod
    def resolve_secret_path(v: object | None) -> str | None:
        if isinstance(v, str) and (v.startswith("~") or v.startswith("/") or "./" in v):
            path = Path(v).expanduser()
            if path.is_file():
                res = path.read_text(encoding="utf-8").strip()
                return res.replace("\ufeff", "")
            else:
                raise FileNotFoundError(f"Файл ключа не найден по пути: {path}")
        return None

    # валидатор объекта, выполняющийся после чтения .env
    @model_validator(mode="after")
    def check_env_vars(self) -> "Settings":
        # Извлекаем прочитанные переменные из .env
        self.api_key = self.resolve_secret_path(self.api_key)
        self.fallback_api_key = self.resolve_secret_path(self.fallback_api_key)
        return self
