import mimetypes
from datetime import datetime

import pytz
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from rss_parser import RSSParser

from apps.core.models import User
from apps.news.models import Category, New


class NewService:
    @staticmethod
    def get_rss_url(language: str | None = None):
        if not language:
            language = settings.MODELTRANSLATION_DEFAULT_LANGUAGE

        return f'{settings.WG_HOST}{language}/rss/news/'

    @classmethod
    def get_data(cls, url: str) -> str | None:
        response = requests.get(url)
        if not response.ok:
            return
        return response.content.decode('utf-8')

    @classmethod
    def update_news(cls, with_translations: bool = True):
        url = cls.get_rss_url()
        data = cls.get_data(url)
        if not data:
            return

        news = []
        rss = RSSParser.parse(data)
        for item in rss.channel.items:
            external_id = item.link.content[:-1].split('/')[-1]
            if not external_id:
                continue

            category, _ = Category.objects.get_or_create(name=item.category.content)
            image_url = item.content.enclosure.attributes['url']
            image_response = requests.get(image_url)
            content_type = image_response.headers['Content-Type']
            extension = mimetypes.guess_extension(content_type)
            filename = external_id + extension
            image = ContentFile(image_response.content, name=filename)

            news.append(
                New(
                    external_id=external_id,
                    category=category,
                    title=item.title.content,
                    description=item.description.content,
                    image=image,
                    link=item.link.content,
                    publicated_at=datetime.strptime(
                        item.pub_date.content, '%a, %d %b %Y %H:%M:%S %Z',
                    ).replace(tzinfo=pytz.utc),
                ),
            )

        New.objects.bulk_create(
            news,
            update_conflicts=True,
            update_fields=['category', 'title', 'description', 'image', 'link', 'publicated_at'],
            unique_fields=['external_id'],
        )

        if with_translations:
            cls.update_news_translation()

    @classmethod
    def update_news_translation(cls):
        new_id_map = dict(New.objects.values_list('external_id', 'id'))
        category_id_map = dict(New.objects.values_list('external_id', 'category_id'))

        for language in settings.MODELTRANSLATION_LANGUAGES:
            url = cls.get_rss_url(language=language)
            data = cls.get_data(url)
            if not data:
                continue

            news = []
            categories = []
            rss = RSSParser.parse(data)
            for item in rss.channel.items:
                external_id = item.link.content[:-1].split('/')[-1]
                if not external_id:
                    continue

                new_id = new_id_map.get(external_id)
                if not new_id:
                    continue

                category_id = category_id_map.get(external_id)
                if not category_id:
                    continue

                new_data = {
                    f'title_{language}': item.title.content,
                    f'description_{language}': item.description.content,
                    f'link_{language}': item.link.content,
                }
                category_data = {
                    f'name_{language}': item.category.content,
                }

                news.append(New(id=new_id, **new_data))
                categories.append(Category(id=category_id, **category_data))

            New.objects.bulk_update(news, fields=new_data.keys())
            Category.objects.bulk_update(categories, fields=category_data.keys())

    @classmethod
    def add_new_viewer(cls, new: New | int, user: User | int):
        if not isinstance(new, New):
            try:
                new = New.objects.get(id=new)
            except New.DoesNotExist:
                return
        if not isinstance(user, User):
            try:
                user = User.objects.get(id=user)
            except User.DoesNotExist:
                return

        new.viewers.add(user)
