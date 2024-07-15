from unittest.mock import patch

import pytest
import pytz
from faker import Faker

from apps.news.models import New
from apps.news.services.news import NewService

faker = Faker()


@pytest.mark.django_db
def test_new_service():
    news_count = faker.random_int(2, 4)
    return_value = f'''<?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl"  media="screen"?>
    <rss version="2.0">
    <channel>
    {
        ''.join(
            f"""
                <item>
                    <link>{faker.image_url(placeholder_url='https://dummyimage.com/{width}x{height}')}</link>
                    <category>{faker.text()[:128]}</category>
                    <enclosure url="{faker.image_url(placeholder_url='https://dummyimage.com/{width}x{height}')}"/>
                    <title>{faker.text()}</title>
                    <description>{faker.text()}</description>
                    <pubDate>
                        {faker.date_time().replace(tzinfo=pytz.utc).strftime('%a, %d %b %Y %H:%M:%S %Z')}
                    </pubDate>
                </item>
            """ for _ in range(news_count)
        )
    }
    </channel>
    </rss>
    '''

    with patch('apps.news.services.news.NewService.get_data', return_value=return_value):
        NewService.update_news()

    assert news_count == New.objects.all().count()
