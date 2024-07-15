# Generated by Django 5.0 on 2024-07-14 10:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import cluster.middlewares


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_rename_newcategory_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=1024)),
                ('author', models.ForeignKey(default=cluster.middlewares.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.new')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]