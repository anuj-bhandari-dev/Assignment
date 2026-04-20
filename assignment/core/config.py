from pathlib import Path

from starlette.config import Config

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"
config = Config(str(ENV_FILE))

DATABASE_URL = config("DATABASE_URL", cast=str)
PORT = config("PORT", cast=int, default=8000)
DEBUG = config("DEBUG", cast=bool, default=False)
APP_NAME = config("APP_NAME", cast=str, default="Book's API")
REDIS_HOST = config("REDIS_HOST", cast=str, default="redis")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_DB = config("REDIS_DB", cast=int, default=0)
