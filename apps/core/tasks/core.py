from apps.core.services.core import CoreService
from cluster import celery_app


@celery_app.task
def update_users():
    CoreService.update_users()


@celery_app.task
def update_users_access_tokens():
    CoreService.update_users_access_tokens()
