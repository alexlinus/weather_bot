

## shortcuts

# db-makemigrations message='some_message'
db-makemigrations:
	alembic revision --autogenerate -m $(message)

db-migrate:
	alembic upgrade head

up:
	docker compose up

build:
	docker-compose build --progress=plain --no-cache