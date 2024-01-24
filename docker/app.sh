#!/bin/bash

alembic upgrade head

uvicorn main:app --host=0.0.0.0 --loop=uvloop --port=80