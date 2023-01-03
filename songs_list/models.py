from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models



class UserExt(models.Model):
    """additional user information"""
    phone = models.CharField(max_length=20, null=True)
    picture = models.ImageField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    singer = models.BooleanField(default=True)


class Song(models.Model):
    """each song on choir's repertoire"""
    name = models.CharField(max_length=255)
    composer = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=255, null=True)
    scores = models.FileField(null=True)
    yt_link = models.TextField(null=True)
    voices = ArrayField(models.CharField(max_length=255), null=True)  # list of voices avaliable for the specific song
    tags = ArrayField(models.CharField(max_length=255), null=True)
    duration = models.DurationField(null=True)

    def __str__(self):
        return self.name + "  (" + self.composer + ")"


class UserSong(models.Model):
    """model capturing each singer's choice for the specific song"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    voice = models.CharField(max_length=255, null=True)   # user will be allowed to use only one of the voices. Form will contain only choices from the Song model.


class SongFiles(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    file = models.FileField()


class AllTags(models.Model):
    name = models.CharField(max_length=255, null=False)
    songs_tagged = ArrayField(models.IntegerField())

    def __str__(self):
        return self.name