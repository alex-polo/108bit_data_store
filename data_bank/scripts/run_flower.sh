#!/bin/bash
export CELERY_TYPE=FLOWER
celery -A src.tasks.celery:celery flower