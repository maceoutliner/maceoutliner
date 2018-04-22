#! /usr/bin/env bash

echo "Running post build django management commands..."
python manage.py collectstatic --no-input --clear
python manage.py compress
python manage.py migrate
echo "Done!"
