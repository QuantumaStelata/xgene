from apps.directory.services.tanks import TankService
from cluster import celery_app


@celery_app.task
def update_tanks():
    TankService.update_tanks()
