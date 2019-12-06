.PHONY: deps fmt test dev

deps:
	pip install -r requirements-dev.txt

fmt:
	black .

test:
	python -m doctest -o NORMALIZE_WHITESPACE -o ELLIPSIS **/*.py
	pytest

dev:
	uvicorn tictactoe.main:app --reload
