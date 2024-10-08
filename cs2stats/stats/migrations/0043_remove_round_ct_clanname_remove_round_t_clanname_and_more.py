# Generated by Django 5.0.7 on 2024-09-19 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0042_round_ct_clanname_round_t_clanname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='ct_clanName',
        ),
        migrations.RemoveField(
            model_name='round',
            name='t_clanName',
        ),
        migrations.AddField(
            model_name='round',
            name='ct_side',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ct_side_lineup', to='stats.lineup'),
        ),
        migrations.AddField(
            model_name='round',
            name='t_side',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='t_side_lineup', to='stats.lineup'),
        ),
    ]
