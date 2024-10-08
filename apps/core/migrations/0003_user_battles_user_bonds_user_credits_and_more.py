# Generated by Django 5.0 on 2024-02-16 21:57

import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_access_token'),
        ('directory', '0009_alter_map_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='battles',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='bonds',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='credits',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='damage_dealt',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='damage_received',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='draws',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='dropped_capture_points',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='frags',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='free_xp',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gold',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='hits',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='losses',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='max_damage',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='max_damage_tank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='max_damage_users', to='directory.tank'),
        ),
        migrations.AddField(
            model_name='user',
            name='max_frags',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='max_frags_tank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='max_frags_users', to='directory.tank'),
        ),
        migrations.AddField(
            model_name='user',
            name='max_xp',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='max_xp_tank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='max_xp_users', to='directory.tank'),
        ),
        migrations.AddField(
            model_name='user',
            name='shots',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='spotted',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='wins',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='wins_percent',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('wins'), '*', models.Value(100)), '/', models.F('battles')), output_field=models.FloatField()),
        ),
        migrations.AddField(
            model_name='user',
            name='hits_percent',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('shots'), '*', models.Value(100)), '/', models.F('hits')), output_field=models.FloatField()),
        ),
    ]
