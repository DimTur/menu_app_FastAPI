import os

import redis
from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class GlobalConfig(BaseConfig):
    redis_server: str = os.environ.get("REDIS_HOST")
    redis_port: int = int(os.environ.get("REDIS_PORT"))


settings = GlobalConfig()


def cache():
    return redis.Redis(
        host=GlobalConfig.redis_server,
        port=GlobalConfig.redis_port,
    )
