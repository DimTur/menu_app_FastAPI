
<details>
<summary><b>ЗАДАНИЯ со звездочками:</b></summary>

1. Нет заданий со звездочками.
2. Есть. Ниже ссылки

* *Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос. ([ТЫК](https://github.com/DimTur/menu_app_FastApi/blob/db144b55abde82beb301a31c0d04c9836db0dc44/api_v1/menus/crud.py#L24))

* **Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest ([ТЫК](https://github.com/DimTur/menu_app_FastApi/blob/b09c16aada584ac4c81b2a08f68313bad3b578de/tests/counter))

3. Есть. Ниже ссылки

* *Описать ручки API в соответствий c OpenAPI ([ТЫК](http://127.0.0.1:8000/openapi.json))

* **Реализовать в тестах аналог Django reverse() для FastAPI ([ТЫК](https://github.com/DimTur/menu_app_FastApi/blob/b459d207988c9934daf7acba638724d0e336c781/tests/service.py))

4. Есть. Выполнены не до конца. В текущем варианте подтягиваются только меню из файла. Ниже ссылки
* *Обновление меню из google sheets раз в 15 сек. ([ТЫК](https://github.com/DimTur/menu_app_FastApi/blob/dadbcdfdba220aeace86fac59ca091a749b66538/tasks/tasks.py))

* **Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx ([ТЫК](https://github.com/DimTur/menu_app_FastApi/blob/dadbcdfdba220aeace86fac59ca091a749b66538/tasks/tasks.py))

</details>

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

Для прогона тестов необходимо убедиться, что Вы выполнили команду "docker compose down -v" для
корректного запуска тестового сценария. Также очень важно убедиться, что у вас отсутствуют образы и кэш с предыдущих сборок!!!

Чтобы запустить тестовый сценарий, введите команду, представленную ниже. Она создаст нужные контейнеры,
прогонит написанные мной тесты, выведет результаты в консоль, после чего остановит зупущенные сервисы, удалит
контейнеры, тома и образы, которые использовались

    docker compose -f docker-compose-pytest.yml up -d && docker logs --follow menu_app_fastapi_test && docker compose -f docker-compose-pytest.yml down -v

**3-ий пункт ДЗ реализован в api_v1.munus.crud в функциях "get_menus" и  "get_menu_by_id", аналогично в submenus**
