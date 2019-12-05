.PHONY: deps test dev

deps:
	pip install -r requirements-dev.txt

test:
	pytest

dev:
	uvicorn tictactoe.main:app --reload
