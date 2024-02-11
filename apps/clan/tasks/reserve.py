from apps.clan.services.reserve import ReserveService
from cluster import celery_app


@celery_app.task
def update_reserves():
    ReserveService.update_reserves()
