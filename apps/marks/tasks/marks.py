from apps.marks.services.marks import MarkService
from cluster import celery_app


@celery_app.task
def update_gun_marks():
    MarkService.update_gun_marks()


@celery_app.task
def update_mastery():
    MarkService.update_mastery()
