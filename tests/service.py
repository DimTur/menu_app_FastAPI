from typing import Callable

from main import app


def get_routes() -> dict[str, str]:
    """Получение словаря с маршрутами приложений"""
    routes = {}
    for route in app.routes:
        routes[route.endpoint.__name__] = route.path
    return routes


def reverse(foo: Callable, routes: dict[str, str] = get_routes(), **kwargs) -> str:
    """Получение url адресу"""
    path = routes[foo.__name__]
    print(path.format(**kwargs))
    return path.format(**kwargs)
