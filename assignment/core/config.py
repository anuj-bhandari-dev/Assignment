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
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", cast=str)
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET", cast=str)
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI", cast=str)
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
