## Запуск приложения

**1. Клонируем репозиторий:**

    git clone <ссылка с git-hub>

**2. Переходим в папку /menu_app_FastApi**

**3. Поднимаем docker comopose**

    docker compose up

**4. Устанавливаем poetry и зависимости**

    pip install poetry

    poetry install --no-root

**5. Проводим миграции**

    alembic upgrade head

**6. Запускаем main.py**

    python main.py