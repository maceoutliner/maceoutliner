web: gunicorn config.wsgi:application
worker: celery worker --app=maceoutliner.taskapp --loglevel=info
