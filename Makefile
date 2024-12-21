PORT ?= 8000

lint:
	poetry run flake8 task_manager

dev:
	poetry run python manage.py runserver

install: 
	poetry install

build:
	./build.sh

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

run:
	poetry run python3 manage.py runserver 0:$(PORT)

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

test:
	poetry run python3 manage.py test task_manager.tests

test-cov:
	poetry run coverage run manage.py test
	poetry run coverage xml

dev-cov:
	poetry run coverage run manage.py test
	poetry run coverage report -m