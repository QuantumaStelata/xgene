from apps.core.services.users import UserService
from cluster import celery_app


@celery_app.task
def update_users_stats():
    UserService.update_users_stats()
