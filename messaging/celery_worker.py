from messaging.celery_app import celery_app_conf
import messaging.tasks

if __name__ == "__main__":
    celery_app_conf.worker_main()
