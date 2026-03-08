.PHONY: install install-dev run fmt fmt-check test

install:
	poetry install

install-dev:
	poetry install --with dev

run:
	poetry run google-workspace-mcp

fmt:
	poetry run ruff format .
	poetry run ruff check --fix .

fmt-check:
	poetry run ruff format --check .
	poetry run ruff check .

test:
	poetry run pytest tests/ --cov --cov-branch --cov-report=html
