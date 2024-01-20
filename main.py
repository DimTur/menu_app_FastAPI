from fastapi import FastAPI

import uvicorn

from menu_views import router as menus_router
from dishes.views import router as dishes_router

app = FastAPI()
app.include_router(menus_router)
app.include_router(dishes_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello world!"
    }


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {
        "message": f"Hello {name}!"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
