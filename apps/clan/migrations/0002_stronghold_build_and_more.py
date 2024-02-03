# Generated by Django 5.0 on 2024-02-02 22:46

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0001_initial'),
        ('directory', '0008_auto_20240203_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stronghold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('level', models.PositiveSmallIntegerField()),
                ('clan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stronghold', to='clan.clan')),
                ('map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='directory.map')),
            ],
            options={
                'ordering': ['-created_at', '-modified_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(choices=[('Financial Unit', 'Финансовая часть'), ('Tankodrome', 'Танкодром'), ('Military School', 'Военное училище'), ('Training Unit', 'Учебная часть'), ('Transportation Unit', 'Автотранспортная часть'), ('Trophy Brigade', 'Трофейная бригата'), ('Artillery Battalion', 'Артиллерийский дивизион'), ('Logistical Service', 'Служба тыла')], max_length=32)),
                ('direction', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=32)),
                ('position', models.PositiveSmallIntegerField(choices=[(1, 'P1'), (2, 'P2')])),
                ('level', models.PositiveSmallIntegerField()),
                ('map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='directory.map')),
                ('reserve_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='build', to='directory.reservetype')),
                ('stronghold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='clan.stronghold')),
            ],
            options={
                'ordering': ['direction', 'position'],
            },
        ),
        migrations.AddConstraint(
            model_name='build',
            constraint=models.UniqueConstraint(fields=('stronghold', 'direction', 'position'), name='stronghold, direction and position unique constraint'),
        ),
        migrations.AddConstraint(
            model_name='build',
            constraint=models.UniqueConstraint(fields=('stronghold', 'title'), name='stronghold and title unique constraint'),
        ),
        migrations.AddConstraint(
            model_name='build',
            constraint=models.UniqueConstraint(fields=('stronghold', 'reserve_type'), name='stronghold and reserve_type unique constraint'),
        ),
    ]