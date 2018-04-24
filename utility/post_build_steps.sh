#! /usr/bin/env bash

echo "Running post build django management commands..."
python manage.py migrate
echo "Done!"
