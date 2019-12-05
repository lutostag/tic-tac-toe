.PHONY: deps fmt test dev

deps:
	pip install -r requirements-dev.txt

fmt:
	black .

test:
	pytest

dev:
	uvicorn tictactoe.main:app --reload
