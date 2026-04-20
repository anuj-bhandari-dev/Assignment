from arq.connections import RedisSettings
from assignment.background_jobs import send_email
from assignment.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB


class WorkerSettings:
    functions = [send_email]
    redis_settings = RedisSettings(host=REDIS_HOST, port=REDIS_PORT, database=REDIS_DB)
