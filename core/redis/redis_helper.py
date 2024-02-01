import os

import redis.asyncio as redis
from dotenv import load_dotenv
from pydantic import BaseConfig
from redis.asyncio import ConnectionPool, Redis

load_dotenv()


class GlobalConfig(BaseConfig):
    redis_server: str = os.environ.get("REDIS_HOST")
    redis_port: int = int(os.environ.get("REDIS_PORT"))


settings = GlobalConfig()

REDIS_URL = f"redis://{GlobalConfig.redis_server}:{GlobalConfig.redis_port}"


async def cache():
    async with redis.from_url(REDIS_URL) as client:
        try:
            yield client
        finally:
            await client.aclose()


# REDIS_URL = f"redis://{GlobalConfig.redis_server}:{GlobalConfig.redis_port}/0"
#
#
# def create_redis():
#     return ConnectionPool.from_url(REDIS_URL)
#
#
# pool = create_redis()
#
#
# def cache():
#     return Redis(connection_pool=pool)


# async def cache():
#     return redis.Redis(
#         host=GlobalConfig.redis_server,
#         port=GlobalConfig.redis_port,
#     )
# async def cache():
#     return await redis.from_url(
#         host=GlobalConfig.redis_server,
#         port=GlobalConfig.redis_port,
#     )
