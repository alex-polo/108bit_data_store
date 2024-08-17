#!/bin/bash
export CELERY_TYPE=WORKER
celery -A src.tasks.celery:celery  worker --hostname=worker@%hostname%