cd ..
set CELERY_TYPE=WORKER
venv\Scripts\celery.exe -A src.tasks.celery:celery worker --pool=solo --hostname=logika-server@%hostname%