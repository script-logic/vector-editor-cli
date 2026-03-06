DC := docker-compose
APP := vector-editor

.PHONY: run test fix lint clean docker-build docker-run docker-stop

run:
	uv run python main.py

test:
	uv run pytest

fix:
	uv run ruff check --fix

lint:
	uv run ruff check .
	uv run ty check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

docker-run:
	$(DC) run --rm $(APP)

docker-down:
	$(DC) down

docker-build:
	$(DC) build

docker-rebuild:
	$(MAKE) docker-down
	$(MAKE) docker-build
	$(MAKE) docker-run
