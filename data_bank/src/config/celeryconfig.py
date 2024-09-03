from kombu import Queue

worker_hijack_root_logger = False

broker_connection_retry_on_startup = True
task_remote_tracebacks = True
database_engine_options = {'echo': True}
timezone = 'Europe/Moscow'

task_queues = (
    Queue('default', routing_key='task_default', max_priority=100),
    Queue('periodic_tasks', routing_key='periodic_tasks', max_priority=100),
    Queue('news_tasks', routing_key='news_tasks', max_priority=100),
    Queue('catalogs_tasks', routing_key='catalogs_tasks', max_priority=100),
)

task_default_queue = 'default'

task_routes = {
    'task_default': {'queue': 'task_default'},
    # 'news_task_scheduler': {'queue': 'periodic_tasks'},
    'sheduler_news_task': {'queue': 'periodic_tasks'},
    'news_site_task': {'queue': 'news_tasks'},

    'catalogs_tasks': {'queue': 'catalogs_tasks'},
}

worker_deduplicate_successful_tasks = True
worker_concurrency = 4
