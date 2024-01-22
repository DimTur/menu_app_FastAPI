## Запуск приложения

**1. Клонируем репозиторий:**

    git clone <ссылка с git-hub>

**2. Переходим в папку /menu_app_FastApi**

***2.1. Убедитесь что у Вас установлено виртуально окружение, если нет, то:***

    python3 -m venv venv
    
    source venv/bin/activate

**3. Устанавливаем poetry и зависимости**

    pip install poetry

    poetry install --no-root

**4. Проводим миграции**

    alembic upgrade head

**5. Поднимаем docker comopose в соседнем терминале**

    docker compose up

**6. Запускаем main.py**

    python main.py