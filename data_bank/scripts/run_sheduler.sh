#!/bin/bash
export CELERY_TYPE=BEAT
celery -A src.tasks.celery:celery beat