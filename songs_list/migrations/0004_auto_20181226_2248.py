# Generated by Django 2.1.4 on 2018-12-26 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs_list', '0003_auto_20181226_2246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='songs_list',
            new_name='songs',
        ),
    ]
