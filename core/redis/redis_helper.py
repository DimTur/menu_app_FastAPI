import os

import redis.asyncio as redis
from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class GlobalConfig(BaseConfig):
    redis_server: str = os.environ.get("REDIS_HOST")
    redis_port: int = int(os.environ.get("REDIS_PORT"))


settings = GlobalConfig()

REDIS_URL = f"redis://{GlobalConfig.redis_server}:{GlobalConfig.redis_port}"


async def cache() -> redis:
    async with redis.from_url(REDIS_URL) as client:
        try:
            yield client
        finally:
            await client.aclose()
