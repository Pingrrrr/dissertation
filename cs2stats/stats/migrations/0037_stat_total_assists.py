# Generated by Django 5.0.7 on 2024-09-18 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0036_alter_round_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='total_assists',
            field=models.IntegerField(default=0),
        ),
    ]
