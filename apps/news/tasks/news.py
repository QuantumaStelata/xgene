from apps.core.models import User
from apps.news.models import New
from apps.news.services.news import NewService
from cluster import celery_app


@celery_app.task
def update_news():
    NewService.update_news()


@celery_app.task
def add_new_viewer(new: New | int, user: User | int):
    NewService.add_new_viewer(new=new, user=user)
