#!/bin/bash

echo "Running alembic migrations"
poetry run alembic upgrade head
