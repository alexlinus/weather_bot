#!/bin/bash

echo "Running alembic migrations"
# sleep to give postgres time to start accepting connections
sleep 15
poetry run alembic upgrade head
