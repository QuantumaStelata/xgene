# Generated by Django 5.0 on 2024-07-13 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_reaction_reaction_new_and_author_unique_constraint'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewCategory',
            new_name='Category',
        ),
    ]
