# Generated by Django 5.0 on 2024-07-13 13:26

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('-created_at', '-modified_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('external_id', models.CharField(max_length=128, unique=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('link', models.URLField()),
                ('pub_date', models.DateTimeField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.newcategory')),
            ],
            options={
                'ordering': ('-created_at', '-modified_at'),
                'abstract': False,
            },
        ),
    ]
