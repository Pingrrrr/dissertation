# Generated by Django 5.0.7 on 2024-09-15 18:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0032_uploadeddemofile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_time']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created_at',
            new_name='created_time',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='round',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='comment',
            name='last_updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='stats.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stats.post'),
            preserve_default=False,
        ),
    ]
