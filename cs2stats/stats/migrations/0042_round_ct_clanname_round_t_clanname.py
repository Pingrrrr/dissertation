# Generated by Django 5.0.7 on 2024-09-19 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0041_strategy_created_strategy_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='ct_clanName',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='round',
            name='t_clanName',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
