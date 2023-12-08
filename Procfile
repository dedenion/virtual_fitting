web: gunicorn background_removal.wsgi --log-file -
worker: celery worker -A background_removal.celery -l INFO