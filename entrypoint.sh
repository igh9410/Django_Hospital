#!/bin/bash

# Run database migrations
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Start your application
#exec "$@"
