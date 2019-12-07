.PHONY: deps fmt test dev

deps:
	pip install -Ur requirements-dev.txt

fmt:
	black .

lint:
	black --check .
	#pylint tictactoe

test: lint
	pytest

dev:
	uvicorn tictactoe.backend.main:app --reload

up:
	docker-compose up --build
