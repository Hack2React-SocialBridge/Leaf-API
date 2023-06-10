#!/bin/sh
alembic upgrade head

exec uvicorn leaf.main:app --reload --host 0.0.0.0