export:
	export FLASK_APP=microblog.py

install:
	poetry install

lint:
	poetry run flake8

build: lint
	poetry build