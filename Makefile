.PHONY: fmt fmt-check test

fmt:
	ruff format .
	ruff check --fix .

fmt-check:
	ruff format --check .
	ruff check .

test:
	pytest tests/ --cov --cov-branch --cov-report=html
