# Generated by Django 2.1.4 on 2022-02-14 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs_list', '0013_sessionhosts'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersong',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]