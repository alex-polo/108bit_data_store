from .celery import celery


@celery.task(name='task_scheduler')
def task_scheduler():
    print('print_task_scheduler')
