## Запуск приложения

**1. Клонируем репозиторий:**

    git clone https://github.com/DimTur/menu_app_FastApi.git

**2. Перейти в папку /menu_app_FastApi**

**3. Поднимаем docker comopose в фоновом режиме**

    docker compose up -d

**4. Пользуемся приложением по адресу http://127.0.0.1:8000/docs**

**5. Чтобы остановить работу контейнеров вводим команду:**

    docker compose down

**Однако, рекомендуется прекращать работу контейнеров с удалением томов, команда:**

    docker compose down -v

## Запуск приложения с прохождением тестов

**Для прогона тестов необходимо убедиться, что Вы выполнили команду "docker compose down -v" для 
корректного запуска тестового сценария**

**Чтобы запустить тестовый сценарий, введите команду, представленную ниже. Она создаст нужные контейнеры, 
прогонит написанные мной тесты, выведет результаты в консоль, после чего остановит зупущенные сервисы, удалит 
контейнеры, тома и образы, которые использовались**

    docker compose -f docker-compose-pytest.yml up -d && docker logs --follow menu_app_fastapi_test && docker compose -f docker-compose-pytest.yml down -v
