# Generated by Django 5.0.7 on 2024-09-10 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0020_strategy_stratcanvas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategy',
            name='description',
            field=models.CharField(max_length=10000),
        ),
    ]
