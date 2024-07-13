# Generated by Django 5.0 on 2024-07-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='new',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='new',
            name='link_en',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='new',
            name='link_ru',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='new',
            name='title_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='new',
            name='title_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='newcategory',
            name='name_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='newcategory',
            name='name_ru',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
