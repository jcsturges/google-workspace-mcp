.PHONY: fmt fmt-check

fmt:
	ruff format .
	ruff check --fix .

fmt-check:
	ruff format --check .
	ruff check .
