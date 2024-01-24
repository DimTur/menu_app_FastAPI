FROM python:3.11

WORKDIR /menu_app_FastApi

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml .
RUN poetry install --no-dev

COPY . .

RUN chmod a+x docker/*.sh