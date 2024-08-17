cd ..
set CELERY_TYPE=FLOWER
venv\Scripts\celery.exe -A src.tasks.celery:celery flower