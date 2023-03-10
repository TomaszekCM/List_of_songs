# Generated by Django 2.1.4 on 2022-01-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs_list', '0009_alltags_songs_tagged'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='declaration',
            field=models.FloatField(choices=[(-2, 'nieusprawiedliwiony występ'), (-1, 'nieusprawiedliwione'), (0, 'nie będzie'), (0.75, 'spóźni się'), (1, 'będzie'), (7, 'jeszcze nie wie')], default=1),
        ),
        migrations.AlterField(
            model_name='usersong',
            name='voice',
            field=models.CharField(max_length=255),
        ),
    ]
