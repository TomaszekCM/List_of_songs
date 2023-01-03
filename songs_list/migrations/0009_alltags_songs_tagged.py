# Generated by Django 2.1.4 on 2021-11-26 12:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs_list', '0008_auto_20211026_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltags',
            name='songs_tagged',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[], size=None),
            preserve_default=False,
        ),
    ]