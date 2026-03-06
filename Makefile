DC_FILE := docker-compose.yml
DC := docker-compose -f $(DC_FILE)

.PHONY: run up down build rebuild test lint clean

run:
	uv run python main.py

test:
	uv run pytest

up:
	$(DC) up

up-detached:
	$(DC) up -d

down:
	$(DC) down

build:
	$(DC) build

rebuild:
	$(MAKE) down
	$(MAKE) build
	$(MAKE) up

fix:
	uv run ruff check --fix

lint:
	uv run ruff check .
	uv run ty check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
