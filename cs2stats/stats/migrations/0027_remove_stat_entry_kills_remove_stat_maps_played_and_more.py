# Generated by Django 5.0.7 on 2024-09-11 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0026_stat_side'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stat',
            name='entry_kills',
        ),
        migrations.RemoveField(
            model_name='stat',
            name='maps_played',
        ),
        migrations.RemoveField(
            model_name='stat',
            name='win_percentage',
        ),
    ]
