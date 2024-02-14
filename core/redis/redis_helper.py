import os
from typing import cast

import redis.asyncio as redis
from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class GlobalConfig(BaseConfig):
    redis_server: str = cast(str, os.environ.get("REDIS_HOST"))
    redis_port: int = cast(int, os.environ.get("REDIS_PORT"))


settings = GlobalConfig()

REDIS_URL = f"redis://{GlobalConfig.redis_server}:{GlobalConfig.redis_port}"


async def cache():
    async with redis.from_url(REDIS_URL) as client:
        try:
            yield client
        finally:
            await client.aclose()


async def get_async_redis_client():
    return redis.Redis(
        host=f"{GlobalConfig.redis_server}", port=int(f"{GlobalConfig.redis_port}")
    )
