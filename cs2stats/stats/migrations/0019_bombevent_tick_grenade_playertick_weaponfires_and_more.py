# Generated by Django 5.0.7 on 2024-08-31 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0018_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bombevent',
            name='tick',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Grenade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thrower_name', models.CharField(max_length=250)),
                ('grenade_type', models.CharField(max_length=25)),
                ('tick', models.IntegerField(default=0)),
                ('x', models.FloatField(default=0.0)),
                ('y', models.FloatField(default=0.0)),
                ('z', models.FloatField(default=0.0)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.round')),
                ('thrower', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stats.player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerTick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('side', models.CharField(max_length=25)),
                ('tick', models.IntegerField()),
                ('health', models.FloatField()),
                ('armor_value', models.FloatField(default=0.0, null=True)),
                ('x', models.FloatField(default=0.0)),
                ('y', models.FloatField(default=0.0)),
                ('z', models.FloatField(default=0.0)),
                ('yaw', models.FloatField(default=0.0)),
                ('inventory', models.CharField(max_length=500)),
                ('current_equip_value', models.FloatField(default=0.0)),
                ('flash_duration', models.FloatField(default=0.0)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stats.player')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.round')),
            ],
        ),
        migrations.CreateModel(
            name='WeaponFires',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('side', models.CharField(max_length=25)),
                ('tick', models.IntegerField(default=0)),
                ('x', models.FloatField(default=0.0)),
                ('y', models.FloatField(default=0.0)),
                ('z', models.FloatField(default=0.0)),
                ('yaw', models.FloatField(default=0.0)),
                ('weapon', models.CharField(max_length=250)),
                ('zoom_level', models.FloatField(default=0.0)),
                ('accuracy_penalty', models.FloatField(default=0.0)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stats.player')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.round')),
            ],
        ),
        migrations.DeleteModel(
            name='ToDo',
        ),
    ]
