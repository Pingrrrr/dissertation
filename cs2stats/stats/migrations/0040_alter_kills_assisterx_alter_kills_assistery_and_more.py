# Generated by Django 5.0.7 on 2024-09-19 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0039_comment_acknowledgements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kills',
            name='assisterX',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='assisterY',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='assisterZ',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='attackerX',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='attackerY',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='attackerZ',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='victimX',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='victimY',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='kills',
            name='victimZ',
            field=models.FloatField(null=True),
        ),
    ]
