# Generated by Django 5.0 on 2024-05-07 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0017_auto_20240507_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('external_id', models.CharField(choices=[('commander', 'Commander'), ('executive_officer', 'Executive Officer'), ('personnel_officer', 'Personnel Officer'), ('recruitment_officer', 'Recruitment Officer'), ('combat_officer', 'Combat Officer'), ('intelligence_officer', 'Intelligence Officer'), ('quartermaster', 'Quartermaster'), ('junior_officer', 'Junior Officer'), ('private', 'Private'), ('recruit', 'Recruit'), ('reservist', 'Reservist')], max_length=32, unique=True)),
            ],
        ),
    ]