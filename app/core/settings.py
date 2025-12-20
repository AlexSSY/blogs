from pathlib import Path
import yaml
import os


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"


def load_yaml(filename: str) -> dict:
    with open(CONFIG_DIR / filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_env() -> str:
    return os.getenv("APP_ENV", "development")


class Settings:
    def __init__(self):
        env = get_env()

        env_config = load_yaml(f"{env}.yml")
        db_config = load_yaml("database.yml")[env]

        self.env = env

        self.debug = env_config["app"]["debug"]
        self.secret_key = env_config["app"]["secret_key"]
        self.host = env_config["app"]["host"]
        self.port = env_config["app"]["port"]

        self.database_url = db_config["url"]
        self.log_level = env_config["logging"]["level"]


settings = Settings()
