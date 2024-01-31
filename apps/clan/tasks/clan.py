from apps.clan.services.clan import ClanService
from cluster import celery_app


@celery_app.task
def update_clan():
    ClanService.update_clan()
