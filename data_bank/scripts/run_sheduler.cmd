cd ..
set CELERY_TYPE=BEAT
venv\Scripts\celery.exe -A src.tasks.celery:celery beat