from pathlib import Path
from pydantic import BaseModel
import yaml
import os


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"


def load_yaml(filename: str) -> dict:
    with open(CONFIG_DIR / filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_env() -> str:
    return os.getenv("APP_ENV", "development")


def build_database_url(cfg: dict) -> str:
    adapter = cfg["adapter"]

    if adapter == "sqlite3":
        return f"sqlite+aiosqlite:///{cfg['name']}"

    if adapter == "mysql":
        return (
            f"mysql+pymysql://{cfg['username']}:{cfg['password']}"
            f"@{cfg['host']}:{cfg['port']}/{cfg['name']}"
        )

    raise ValueError(f"Unsupported adapter: {adapter}")


class AppConfig(BaseModel):
    debug: bool
    secret_key: str
    templates_dir: str
    timezone: str
    features: list[str]


class LoggingConfig(BaseModel):
    level: str


class Settings(BaseModel):
    env: str
    app: AppConfig
    logging: LoggingConfig
    database_url: str
    
    @classmethod
    def load(cls) -> "Settings":
        env = get_env()

        env_config = load_yaml(f"{env}.yml")
        db_config = load_yaml("database.yml")[env]

        settings = cls(
            env=env,
            app=env_config["app"],
            logging=env_config["logging"],
            database_url=build_database_url(db_config),
        )

        return settings


settings = Settings.load()
