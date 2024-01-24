FROM python:3.11

WORKDIR /menu_app_FastApi

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml .
RUN poetry install --no-dev

COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--loop=uvloop", "--port=80"]