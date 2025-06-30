from celery import Celery

celery_app_conf = Celery(
    "delivery_service",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app_conf.conf.beat_schedule = {
    'recalculate-every-300-seconds': {
        'task': 'messaging.tasks.recalculate_prices',
        'schedule': 30.0,
    },
}

celery_app_conf.conf.timezone = 'Europe/Moscow'

celery_app_conf.conf.task_routes = {
    "messaging.tasks.recalculate_prices": {"queue": "delivery_queue"},
}

