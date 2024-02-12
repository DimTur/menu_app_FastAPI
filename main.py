from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import settings
from tasks.tasks import CELERY_STATUS, update_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    if CELERY_STATUS:
        update_db.delay()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
