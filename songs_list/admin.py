from django.contrib import admin
from .models import *
# Register your models here.


class SongAdmin(admin.ModelAdmin):
    list_display = ['name']

# class EventAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'date']
#     search_fields = ['name']

admin.site.register(Song, SongAdmin)
# admin.site.register(Event, EventAdmin)
# admin.site.register(EventSongs)
admin.site.register(UserExt)
admin.site.register(AllTags)
admin.site.register(UserSong)
