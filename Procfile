release: utility/post_build_steps.sh
web: waitress-serve --port=$PORT config.wsgi:application
worker: python manage.py qcluster 
