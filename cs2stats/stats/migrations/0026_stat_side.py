# Generated by Django 5.0.7 on 2024-09-11 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0025_remove_uploadeddemo_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='side',
            field=models.CharField(max_length=24, null=True),
        ),
    ]
