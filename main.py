from contextlib import asynccontextmanager

import aioredis
from fastapi import FastAPI

import uvicorn

from core.config import settings
from api_v1 import router as router_v1

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.redis_settings.redis_url)
    yield
    redis.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
