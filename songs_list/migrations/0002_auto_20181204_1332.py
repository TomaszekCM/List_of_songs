# Generated by Django 2.1.4 on 2018-12-04 13:32

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='voices',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('soprano1', 'soprano1'), ('soprano2', 'soprano2'), ('soprano3', 'soprano3'), ('soprano4', 'soprano4'), ('alto1', 'alto1'), ('alto2', 'alto2'), ('alto3', 'alto3'), ('alto4', 'alto4'), ('tenor1', 'tenor1'), ('tenor2', 'tenor2'), ('tenor3', 'tenor3'), ('tenor4', 'tenor4'), ('bas1', 'bas1'), ('bas2', 'bas2'), ('bas3', 'bas3'), ('bas4', 'bas4')], max_length=255), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='song',
            name='yt_link',
            field=models.TextField(null=True),
        ),
    ]
