# Generated by Django 5.0 on 2023-12-30 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=5)),
                ('name', models.TextField()),
                ('motto', models.TextField()),
                ('color', models.CharField(max_length=7)),
                ('emblem', models.URLField()),
                ('clan_id', models.IntegerField(unique=True)),
            ],
        ),
    ]
