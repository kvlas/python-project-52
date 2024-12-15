install: 
	poetry install

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

build: install migrate

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

test:
	poetry run python3 manage.py test

run:
	poetry run python3 manage.py runserver 0:$(PORT)

lint:
	poetry run flake8 task_manager