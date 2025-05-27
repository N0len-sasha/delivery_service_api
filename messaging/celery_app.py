from celery import Celery

celery_app = Celery(
    "delivery_service",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {
    "messaging.worker.recalculate_delivery_price": {"queue": "delivery_queue"},
}
