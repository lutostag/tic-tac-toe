.PHONY: deps

deps:
	pip install -r requirements-dev.txt

test:
	pytest
