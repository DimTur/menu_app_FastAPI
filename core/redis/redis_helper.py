import os
from typing import cast

import redis.asyncio as redis
from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class GlobalConfig(BaseConfig):
    """Конфигурация для подключения к redis"""

    redis_server: str = cast(str, os.environ.get("REDIS_HOST"))
    redis_port: int = cast(int, os.environ.get("REDIS_PORT"))


settings = GlobalConfig()

REDIS_URL = f"redis://{GlobalConfig.redis_server}:{GlobalConfig.redis_port}"


async def cache():
    """Подключение к redis"""
    async with redis.from_url(REDIS_URL) as client:
        try:
            yield client
        finally:
            await client.aclose()
