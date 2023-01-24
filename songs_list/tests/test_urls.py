from django.test import TestCase
from django.urls import reverse, resolve
from songs_list.views import *

class TestUrls(TestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, AllSongsView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_add_user_url(self):
        url = reverse('add_user')
        self.assertEqual(resolve(url).func.view_class, AddUserView)

    def test_all_users_url(self):
        url = reverse('all_users')
        self.assertEqual(resolve(url).func.view_class, AllUsersView)

    def test_user_url(self):
        url = reverse('user', args=[5])
        self.assertEqual(resolve(url).func.view_class, UserView)

    def test_change_user_url(self):
        url = reverse('change_user_details', args=[3])
        self.assertEqual(resolve(url).func.view_class, UserDetailsChangeView)

    def test_reset_password_url(self):
        url = reverse('reset_password', args=[6])
        self.assertEqual(resolve(url).func.view_class, ResetPasswordView)

    def test_add_song_url(self):
        url = reverse('add_song')
        self.assertEqual(resolve(url).func.view_class, AddSongView)

    def test_all_songs_url(self):
        url = reverse('all_songs')
        self.assertEqual(resolve(url).func.view_class, AllSongsView)

    def test_songs_with_tag_url(self):
        url = reverse('songs_with_tag', args=["some-tag"])
        self.assertEqual(resolve(url).func.view_class, SongsWithTagView)

    def test_song_url(self):
        url = reverse('song', args=[4,5])
        self.assertEqual(resolve(url).func.view_class, SongView)

    def test_song_declaration_url(self):
        url = reverse('song_declaration', args=[6,11])
        self.assertEqual(resolve(url).func.view_class, SongDeclarationView)

    def test_set_voices_in_song_url(self):
        url = reverse('set_voices', args=[4, 66])
        self.assertEqual(resolve(url).func.view_class, SongSetVoicesView)

    def test_edit_song_url(self):
        url = reverse('edit_song', args=[1, 123])
        self.assertEqual(resolve(url).func.view_class, EditSongView)

    def test_add_file_to_song_url(self):
        url = reverse('add_file_to_song', args=[2])
        self.assertEqual(resolve(url).func.view_class, SongAddFileView)

    def test_delete_song_url(self):
        url = reverse('delete_song', args=[44])
        self.assertEqual(resolve(url).func.view_class, SongDeleteView)

    def test_backup_url(self):
        url = reverse('backup')
        self.assertEqual(resolve(url).func.view_class, BackupView)

    def test_test_url(self):
        url = reverse('test')
        self.assertEqual(resolve(url).func.view_class, LittleHelperView)
