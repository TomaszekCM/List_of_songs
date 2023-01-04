"""choir_assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from songs_list.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home$', AllSongsView.as_view(), name="home"),
    url(r'^$', LoginView.as_view(), name="login"),
    url(r'^logout$', logout_view, name="logout"),
    url(r'^add_user$', AddUserView.as_view(), name="add_user"),
    url(r'^all_users$', AllUsersView.as_view(), name="all_users"),
    url(r'^user/(?P<user_id>(\d)+)$', UserView.as_view(), name="user"),
    url(r'^user/(?P<user_id>(\d)+)/change$', UserDetailsChangeView.as_view(), name="change_user_details"),
    url(r'^user/(?P<user_id>(\d)+)/change_password$', ResetPasswordView.as_view(), name="reset_password"),
    url(r'^add_song$', AddSongView.as_view(), name="add_song"),
    url(r'^all_songs$', AllSongsView.as_view(), name="all_songs"),
    url(r'^songs/tag/(?P<tag_name>(.*?))$', SongsWithTagView.as_view(), name="songs_with_tag"),
    url(r'^song/(?P<song_id>(\d)+)/(?P<event_id>(\d+))$', SongView.as_view(), name="song"),
    url(r'^song/(?P<song_id>(\d)+)/(?P<event_id>(\d+))/declare$', SongDeclarationView.as_view(),
        name="song_declaration"),
    url(r'^song/(?P<song_id>(\d)+)/(?P<event_id>(\d)+)/set_voices$', SongSetVoicesView.as_view(), name="set_voices"),
    url(r'^song/(?P<song_id>(\d)+)/(?P<event_id>(\d)+)/edit$', EditSongView.as_view(), name="edit_song"),
    url(r'^song/(?P<song_id>(\d)+)/add_file$', SongAddFileView.as_view(), name="add_file_to_song"),
    url(r'^song/(?P<song_id>(\d)+)/delete$', SongDeleteView.as_view(), name="delete_song"),
    url('hand_backup/', BackupView.as_view(), name="backup"),
    url('test/', TestView.as_view(), name="test"),

]

admin.site.site_header = "Choir Assistant - panel administracyjny"

# required to upload files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
