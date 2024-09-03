import logging.config
import os
import traceback

from celery import Celery
from celery.schedules import crontab

from .mics import get_news_site_processing_timeout
from ..config import (get_celery_config,
                      CeleryConfig,
                      get_database_config,
                      DatabaseConfig)

# Получаем базы данных брокера и бекэнда для celery из .env
celery_config: CeleryConfig = get_celery_config()
database_config: DatabaseConfig = get_database_config()

# Конфигурация логгера
# logging.config.fileConfig(celery_config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Инициализируем celery
celery = Celery(__name__, broker=celery_config.BROKER, backend=celery_config.BACKEND)
celery.config_from_object('src.config.celeryconfig')


@celery.task
def send_verification_code(email: str, code: int):
    print('send_verification_code')
    print(email, code)
    pass


# Автопоиск задач
celery.autodiscover_tasks()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    celery_type = os.environ.get('CELERY_TYPE')
    logger.info(f'Celery {celery_type.title()} configuration')
    if celery_type == 'BEAT':
        try:
            sender.conf.beat_schedule = {
                'task_scheduler': {
                    'task': 'sheduler_news_task',
                    # 'schedule': crontab(minute=f'*/{celery_config.SCHEDULER_TIME}'),
                    'schedule': crontab(minute=f'*/{get_news_site_processing_timeout()}'),
                    'options': {
                        'routing_key': 'periodic_tasks',
                        'priority': 100
                    },
                },
            }

            logger.info(f'Celery {celery_type.title()} configuration completed')
        except Exception as error:
            logger.error(error)
            logger.error(traceback.format_exc(limit=None, chain=True))
            logger.warning('Configuration completed with errors')
