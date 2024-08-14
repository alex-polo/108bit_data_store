from kombu import Queue

worker_hijack_root_logger = False

broker_connection_retry_on_startup = True
task_remote_tracebacks = True
database_engine_options = {'echo': True}
timezone = 'Europe/Moscow'

task_queues = (
    Queue('default', routing_key='task_default', max_priority=100),
    Queue('periodic_tasks', routing_key='periodic_tasks', max_priority=100),
    Queue('email_tasks', routing_key='email_tasks_collection', max_priority=100),
    Queue('parsers_tasks', routing_key='parsers_tasks_collection', max_priority=100),
)

task_default_queue = 'default'

task_routes = {
     'task_delete_verify_code': {'queue': 'task_default'},
     'task_get_verification_code': {'queue': 'auth_tasks'},
     'task_delete_garbage_verify_code': {'queue': 'periodic_tasks'},
}

worker_deduplicate_successful_tasks = True
worker_concurrency = 4
