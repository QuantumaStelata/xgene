from apps.clan.services.stronghold import StrongholdService
from cluster import celery_app


@celery_app.task
def update_stronghold():
    StrongholdService.update_stronghold()
