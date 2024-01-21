from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from core.config import settings
from api_v1 import router as router_v1
from dishes.views import router as dishes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(dishes_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
