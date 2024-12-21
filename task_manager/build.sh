#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install poetry
poetry install

# run migrations
python manage.py migrate