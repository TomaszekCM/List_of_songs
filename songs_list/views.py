from datetime import datetime, timedelta, time

import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, SuperuserMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404
from django.shortcuts import get_object_or_404

from songs_list.forms import *
from songs_list.models import *

# FUNCTIONS


# This function returns just part of the yt address, which allows to display correctly
def yt_link_cutter(link):
    if link.startswith("https://m.youtube.com/watch?v="):
        clean_link = link[30:]
    elif link.startswith("https://www.youtube.com/watch?v="):
        clean_link = link[32:]
        if link.endswith("&app=desktop"):
            clean_link = link[:-12]
    else:
        return None

    return clean_link


def previous_next_songs(song_id, event_id):
    song = Song.objects.get(pk=song_id)
    all_songs = Song.objects.all().order_by("name")
    list_of_all_songs = [i for i in all_songs]

    song_index = list_of_all_songs.index(song)
    lower_index = song_index - 1
    if lower_index < 0:
        lower_index = len(list_of_all_songs) - 1
    higher_index = song_index + 1
    if higher_index >= len(list_of_all_songs):
        higher_index = 0

    previous_song_id = list_of_all_songs[lower_index].id
    next_song_id = list_of_all_songs[higher_index].id

    return previous_song_id, next_song_id


# VIEWS


class LoginView(View):
    """First page, available for all - login into the app"""

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            failed = "Zły login lub hasło!"
            return render(request, "login.html", {"form": form, "failed": failed})

        return render(request, "login.html", {"form": form})


def logout_view(request):
    """Simple log out address, with no html assigned"""
    logout(request)
    return redirect('login')


# ALL USER RELATED VIEWS


class AddUserView(SuperuserMixin, View):
    """Formular - available only to admins - allowing to create user/superuser"""

    def get(self, request):
        user = request.user

        form = AddUserForm(False, user=user, specific_user="")
        return render(request, "add_user.html", {"form": form})

    def post(self, request):
        user = request.user
        form = AddUserForm(False, request.POST, user=user, specific_user="")
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            name = form['name'].value()
            surname = form['surname'].value()
            email = form['email'].value()
            superuser = form['superuser'].value()
            phone = form['phone'].value()
            singer = form['singer'].value()

            user = User.objects.create_user(username, password=password,
                                            first_name=name,
                                            last_name=surname,
                                            email=email)
            user.is_superuser = superuser
            user.save()

            UserExt.objects.create(user=user, phone=phone, singer=singer)

            return redirect('home')

        else:
            return render(request, "add_user.html", {"form": form})


class AllUsersView(LoginRequiredMixin, View):
    """List of all users"""
    login_url = 'login'

    def get(self, request):
        all_active_users = User.objects.filter(is_active=True).order_by("last_name")
        all_inactive_users = User.objects.filter(is_active=False).order_by("last_name")
        return render(request, "all_users.html", {"users": all_active_users, "inactive_users": all_inactive_users})


class UserView(LoginRequiredMixin, View):
    """Specific user's details. Logged user and admin can see links to change details"""
    login_url = 'login'

    def get(self, request, user_id):
        specific_user = get_object_or_404(User, pk=user_id)
        try:
            specific_user_ext = UserExt.objects.get(user=specific_user)
        except:
            specific_user_ext = UserExt.objects.create(user=specific_user)

        return render(request, "user_view.html",
                      {"specific_user": specific_user,
                       "specific_user_ext": specific_user_ext})


class UserDetailsChangeView(LoginRequiredMixin, View):
    """Changing user's details"""
    login_url = 'login'

    def get(self, request, user_id):
        user = request.user
        if user.is_superuser or int(user.id) == int(user_id):
            specific_user = get_object_or_404(User, pk=user_id)
            specific_user_ext = UserExt.objects.get(user=specific_user)
            form = EditUserForm(True, user=user, specific_user=specific_user,
                                initial={'username': specific_user.username,
                                            "name": specific_user.first_name,
                                            "surname": specific_user.last_name,
                                            "email": specific_user.email,
                                            "phone": specific_user_ext.phone,
                                            "superuser": specific_user.is_superuser,
                                            "singer": specific_user_ext.singer,
                                            "active": specific_user.is_active
                                         })

            return render(request, "change_user_details.html",
                          {"form": form, "specific_user": specific_user, "specific_user_ext": specific_user_ext})
        else:
            return HttpResponse("Nie twoje - nie dotykaj!")

    def post(self, request, user_id):
        user = request.user
        edited_user = get_object_or_404(User, pk=user_id)
        edited_user_ext = UserExt.objects.get(user=edited_user)

        form = EditUserForm(True, request.POST, user=user, specific_user=edited_user)
        if form.is_valid():
            edited_user.username = form['username'].value()
            edited_user.first_name = form['name'].value()
            edited_user.last_name = form['surname'].value()
            edited_user.email = form['email'].value()
            edited_user_ext.phone = form['phone'].value()

            if 'superuser' in request.POST:
                edited_user.is_superuser = True
            else:
                if edited_user.is_superuser:
                    edited_user.is_superuser = False

            if 'singer' in request.POST:
                edited_user_ext.singer = True
            else:
                if edited_user_ext.singer:
                    edited_user_ext.singer = False

            if 'active' in request.POST:
                edited_user.is_active = True
            else:
                if edited_user.is_active:
                    edited_user.is_active = False

            edited_user.save()
            edited_user_ext.save()

            return redirect('all_users')

        else:
            return render(request, "change_user_details.html",
                          {"form": form, "specific_user": edited_user})


class ResetPasswordView(LoginRequiredMixin, View):
    """User can change user's password"""
    login_url = 'login'

    def get(self, request, user_id):
        if int(request.user.id) == int(user_id):
            form = PasswordChangeForm()
            user = get_object_or_404(User, pk=user_id)
            return render(request, "change_passwd.html", {"form": form, "user": user})
        else:
            return HttpResponse("Nie twoje - nie dotykaj!")

    def post(self, request, user_id):
        if int(request.user.id) == int(user_id):
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user = User.objects.get(pk=user_id)
                user.set_password(password)
                user.save()
                user = authenticate(request, username=user.username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "change_passwd.html", {"form": form})
        else:
            return HttpResponse("Nie twoje - nie dotykaj!")


# ALL SONG RELATED VIEWS

class AddSongView(SuperuserMixin, View):
    """Formular that allows to add song to the choirs resources"""

    def get(self, request):
        form = AddSongForm()
        all_tags = AllTags.objects.all().order_by("name")
        tags = []
        for tag in all_tags:
            tags.append(tag.name)
        add = True
        return render(request, "add_song.html", {"form": form, "add": add, "all_tags": tags})

    def post(self, request):
        form = AddSongForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            composer = form.cleaned_data['composer']
            description = form.cleaned_data['description']
            link = form.cleaned_data['yt_link']
            scores = form.cleaned_data['scores']
            duration = form.cleaned_data['duration']
            voices = request.POST.getlist('newVoice')
            clear_voices = []
            for i in voices:
                if i != '':
                    clear_voices.append(i)

            new_link = yt_link_cutter(link)
            if voices == ['']:
                voices = ["unisono"]
                new_song = Song.objects.create(name=name, composer=composer, description=description,
                                               voices=["unisono"], yt_link=new_link, duration=duration)
            else:
                new_song = Song.objects.create(name=name, composer=composer, description=description,
                                               voices=clear_voices, yt_link=new_link, duration=duration)

            if len(voices) == 1:
                all_users = User.objects.filter(is_active=True)
                # in such case we can set unisono voice for all users, even not singing,
                # as otherwise when they start to sing, they would have to -manually- set his unisono voice
                # all_hosts = [i.host for i in SessionHosts.objects.all()]
                for user in all_users:
                    UserSong.objects.create(user=user, voice=voices[0], song=new_song)

            if scores:
                SongFiles.objects.create(song=new_song, file=scores)

            # TAGS RELATED UTILITIES
            new_tags = request.POST.getlist('tag')
            new_tags = [i for i in new_tags if i != '']

            if new_tags != []:
                new_song.tags = new_tags
                new_song.save()

                for tag in new_tags:
                    try:
                        current_tag = AllTags.objects.get(name=tag)
                        list_of_songs = current_tag.songs_tagged
                        list_of_songs.append(new_song.id)
                        current_tag.songs_tagged = list_of_songs
                        current_tag.save()
                    except:
                        AllTags.objects.create(name=tag, songs_tagged=[new_song.id])

            return redirect('song/%s/0' % new_song.id)

        # If form is invalid, we need the above to get the form with available tags
        all_tags = AllTags.objects.all()
        tags = []
        for tag in all_tags:
            tags.append(tag.name)
        add = True
        return render(request, "add_song.html", {"form": form, "add": add, "all_tags": tags})
        # return render(request, "add_song.html", {"form": form})


class AllSongsView(LoginRequiredMixin, View):
    """Shows list of all available songs"""
    login_url = 'login'

    def get(self, request):
        all_songs = Song.objects.all().order_by("name")
        all_tags = AllTags.objects.all().order_by("name")
        tags = {}
        songs_tags = {}

        for tag in all_tags:
            tag_name = tag.name
            if " " in tag_name:
                tag_withouth_space = tag_name.replace(" ", "")
                tags[tag] = (tag_withouth_space)
            else:
                tags[tag] = (tag_name)

        for song in all_songs:
            tags_string = ""
            if song.tags:
                for tag in song.tags:
                    clear_tag = tag.replace(" ", "")
                    tags_string += clear_tag + " "
            songs_tags[song] = tags_string

        return render(request, "all_songs.html", {"tags": tags, "all_tags": all_tags, "songs_tags": songs_tags})


class SongsWithTagView(LoginRequiredMixin, View):
    """Shows all songs with the specific tag"""
    login_url = 'login'

    def get(self, request, tag_name):
        try:
            tag = AllTags.objects.get(name=tag_name)
        except:
            raise Http404
        songs_with_tag = [Song.objects.get(pk=i) for i in tag.songs_tagged]
        return render(request, "songs_with_tag.html", {"all_songs": songs_with_tag, "tag": tag})


class SongView(LoginRequiredMixin, View):
    """Each song's details with user information about his one's and link to change his declaration"""
    login_url = 'login'

    def get(self, request, song_id, event_id):
        try:
            song = Song.objects.get(pk=song_id)
        except:
            raise Http404
        user = request.user
        all_users = UserSong.objects.filter(song=song).filter(user__userext__singer=True)
        files = SongFiles.objects.filter(song=song)

        if len(song.voices) > 1:
            more_voices = True
        else:
            more_voices = False

        # This is for 'previous/next song' buttons. If someone gets to the song from event,
        # this shows next one within such event. Otherwise, the next song globally
        ids_of_surrounding_songs = previous_next_songs(song_id, event_id)
        previous_song_id = ids_of_surrounding_songs[0]
        next_song_id = ids_of_surrounding_songs[1]

        # create string with duration without unnecessary zeroes on the beginning
        duration = song.duration
        if duration:
            string_duration = str(duration)
            while string_duration[0] == "0" or string_duration[0] == ":":
                string_duration = string_duration[1:]

            if len(string_duration) <= 2:
                string_duration += " sek"
            duration = string_duration

        ctx = {"duration": duration,
               "song": song,
               "all_users": all_users,
               "files": files,
               "event": int(event_id),
               "more_voices": more_voices,
               "previous_song": previous_song_id,
               "next_song": next_song_id}

        try:
            user_voice = UserSong.objects.filter(song_id=song_id).get(user=user)
            ctx["user_voice"] = user_voice
            return render(request, "song_view.html", ctx)

        except:
            ctx["alert"] = "Zadeklaruj jakim głosem śpiewasz!"
            return render(request, "song_view.html", ctx)

    # Needed to delete file
    def post(self, request, song_id, event_id):
        if request.user.is_superuser:
            # if "change" in request.POST:
            try:
                song = Song.objects.get(pk=song_id)
            except:
                raise Http404
            file_id = request.POST['name']
            file = SongFiles.objects.get(pk=file_id)
            try:
                if len(file.file) > 0:
                    os.remove(file.file.path)
                    file.delete()
            except:
                file.delete()
            return HttpResponseRedirect("/song/%s/%s" % (song_id, event_id))

        else:
            return HttpResponse("Nice try!")


class SongDeclarationView(LoginRequiredMixin, View):
    """As currently there is 'no front', it is easier to make such view"""
    login_url = 'login'

    def get(self, request, song_id, event_id):
        try:
            song = Song.objects.get(pk=song_id)
        except:
            raise Http404
        user = request.user
        return render(request, "song_declaration.html", {"song": song, "user": user})

    def post(self, request, song_id, event_id):
        try:
            song = Song.objects.get(pk=song_id)
        except:
            raise Http404
        user = request.user
        voice = request.POST['voice']

        try:
            user_voice = UserSong.objects.filter(song_id=song_id).get(user=user)
            user_voice.voice = voice
            user_voice.save()

        except:
            UserSong.objects.create(song=song, user=user, voice=voice)

        return HttpResponseRedirect("/song/%s/%s" % (song_id, event_id))


class SongSetVoicesView(SuperuserMixin, View):
    """Admin can set users' voices to the song without their permission"""

    def get(self, request, song_id, event_id):
        try:
            song = Song.objects.get(pk=song_id)
        except:
            raise Http404
        all_active_users = User.objects.filter(is_active=True).filter(userext__singer=True).order_by("last_name")

        current_voices = {}
        for user in all_active_users:
            try:
                user_voice = UserSong.objects.filter(song=song).get(user=user)
                current_voices[user] = user_voice.voice

            except:
                current_voices[user] = ""

        return render(request, "song_set_voices.html",
                      {"song": song, "all_users": all_active_users, "current_voices": current_voices})

    def post(self, request, song_id, event_id):
        try:
            song = Song.objects.get(pk=song_id)
        except:
            raise Http404
        users_voices = request.POST
        all_voice_declarations = UserSong.objects.filter(song=song)
        for i in users_voices:
            if i != "csrfmiddlewaretoken":
                user = User.objects.get(username=i)
                voice = users_voices[i]
                if voice != "":
                    try:
                        voice_declaration = all_voice_declarations.get(user=user)
                        voice_declaration.voice = voice
                        voice_declaration.save()
                    except:
                        UserSong.objects.create(user=user, song=song, voice=voice)
        return HttpResponseRedirect("/song/%s/%s" % (song_id, event_id))


class EditSongView(SuperuserMixin, View):

    def get(self, request, song_id, event_id):
        try:
            song = Song.objects.get(id=song_id)
        except:
            raise Http404
        tags = []

        try:
            all_tags = AllTags.objects.all()
            for tag in all_tags:
                tags.append(tag.name)
        except:
            pass

        try:
            yt_extension = "https://www.youtube.com/watch?v=" + song.yt_link
            form = EditSongForm(initial={'duration': song.duration, 'name': song.name, "composer": song.composer,
                                         "yt_link": yt_extension,
                                         "description": song.description, "voices": song.voices, "scores": song.scores})
        except:
            form = EditSongForm(initial={'duration': song.duration, 'name': song.name, "composer": song.composer,
                                         "description": song.description, "voices": song.voices, "scores": song.scores})

        return render(request, "add_song.html", {"form": form, "song": song, "all_tags": tags})

    def post(self, request, song_id, event_id):
        form = EditSongForm(request.POST)
        if form.is_valid():
            try:
                song = Song.objects.get(pk=song_id)
            except:
                raise Http404
            old_voices = song.voices
            song.name = request.POST['name']
            song.composer = request.POST['composer']
            song.description = request.POST['description']
            duration = request.POST['duration']
            if duration:
                song.duration = duration
            else:
                song.duration = None
            song.yt_link = yt_link_cutter(request.POST['yt_link'])

            # VOICES RELATED UTILITIES
            if "change" in request.POST:
                new_voices = request.POST.getlist('newVoice')

                # if no voice is set, it means that song is unisono
                if new_voices == ['']:
                    new_voices = ["unisono"]

                #  if among voices there are empty spaces, such a voice is being skipped
                clear_voices = []
                for i in new_voices:
                    if i != '':
                        clear_voices.append(i)

                song.voices = clear_voices

                # if new set of voices is different than the old one, all old voice declarations are deleted
                if old_voices != clear_voices:
                    all_declared_voices = UserSong.objects.filter(song=song)
                    for declaration in all_declared_voices:
                        declaration.delete()

                #  if there is only one voice, all members are moved to sing this specific voice
                if len(clear_voices) == 1:
                    all_users = User.objects.filter(is_active=True)
                    for user in all_users:
                        # we want to make sure that there are no doubled records left...
                        try:
                            user_song = UserSong.objects.filter(song=song).filter(user=user)
                            # so we delete all existing
                            user_song.delete()
                        except:
                            pass

                        UserSong.objects.create(user=user, voice=clear_voices[0], song=song)

            # TAGS RELATED UTILITIES
            if "change_tags" in request.POST:
                new_tags = request.POST.getlist('tag')
                new_tags = [i for i in new_tags if i != '']
                # print("lista nowych tagów: ", new_tags)
                # print("stare tagi: ", song.tags)

                if new_tags != song.tags:
                    # print("przeszło")
                    if song.tags is not None:
                        old_tags = song.tags

                        # first of all, old tags have to be managed, so for each old tag we have to get an existing recorg
                        # if such exists and to remove song index from the list of tagged songs
                        for tag in old_tags:
                            try:
                                tag_to_remove_from_song = AllTags.objects.get(name=tag)
                                if song.id in tag_to_remove_from_song.songs_tagged:
                                    tag_to_remove_from_song.songs_tagged.remove(song.id)
                                    tag_to_remove_from_song.save()
                                #     if no song is tagged with such tag, tag has to be deleted
                                if len(tag_to_remove_from_song.songs_tagged) == 0:
                                    tag_to_remove_from_song.delete()
                            except:
                                pass

                    if new_tags == ['']:
                        song.tags.clear()
                    else:
                        song.tags = new_tags
                        # now we have to add song intex to the list of the tagged songs in each tag
                        for tag in new_tags:
                            try:
                                current_tag = AllTags.objects.get(name=tag)
                                if song.id not in current_tag.songs_tagged:
                                    current_tag.songs_tagged.append(song.id)
                                    current_tag.save()
                            except:
                                AllTags.objects.create(name=tag, songs_tagged=[song.id])
            song.save()

            return HttpResponseRedirect("/song/%s/%s" % (song_id, event_id))

        # WHEN FORM IS INVALID, WE HAVE TO DISPLAY EVERYTHING ONCE AGAIN - TO BE REWRITTEN TO AVOID HAVING THE ABOWE TWICE IN ONE VIEW
        try:
            song = Song.objects.get(id=song_id)
        except:
            raise Http404
        tags = []
        try:
            all_tags = AllTags.objects.all()
            for tag in all_tags:
                tags.append(tag.name)
        except:
            pass
        # print(tags)
        try:
            yt_extension = "https://www.youtube.com/watch?v=" + song.yt_link
            form = EditSongForm(request.POST,
                                initial={'name': song.name, "composer": song.composer, "yt_link": yt_extension,
                                         "description": song.description, "voices": song.voices, "scores": song.scores})
        except:
            form = EditSongForm(request.POST,
                                initial={'name': song.name, "composer": song.composer, "description": song.description,
                                         "voices": song.voices, "scores": song.scores})

        return render(request, "add_song.html", {"form": form, "song": song, "all_tags": tags})


class SongAddFileView(SuperuserMixin, View):

    def get(self, request, song_id):
        try:
            song = Song.objects.get(pk=song_id)
        except:
            raise Http404
        return render(request, "add_song_file.html", {"song": song})

    def post(self, request, song_id):
        if "add" in request.POST:
            try:
                song = Song.objects.get(pk=song_id)
            except:
                raise Http404

            try:
                new_file = request.FILES['file']
                SongFiles.objects.create(song=song, file=new_file)
                return HttpResponseRedirect("../%s/0" % song_id)
            except:
                return HttpResponseRedirect("../%s" % song_id)

        else:
            return HttpResponseRedirect("../%s/0" % song_id)


class SongDeleteView(SuperuserMixin, View):
    """Admin can delete the song"""

    def get(self, request, song_id):
        if request.user.is_superuser:
            try:
                song = Song.objects.get(pk=song_id)
            except:
                raise Http404

            return render(request, "delete_song.html", {"song": song})

        else:
            HttpResponse("NAWET NIE PRÓBUJ!!!")

    def post(self, request, song_id):
        if request.user.is_superuser:

            if "Usuń" in request.POST:
                try:
                    song = Song.objects.get(pk=song_id)
                except:
                    raise Http404

                # first of all, we have to manage tags related issues
                if song.tags is not None:
                    # first of all, old tags have to be managed, so for each old tag we have to get an existing recorg
                    # if such exists and to remove song index from the list of tagged songs
                    for tag in song.tags:
                        try:
                            tag_to_remove_from_song = AllTags.objects.get(name=tag)
                            if song.id in tag_to_remove_from_song.songs_tagged:
                                tag_to_remove_from_song.songs_tagged.remove(song.id)
                                tag_to_remove_from_song.save()
                            #     if no song is tagged with such tag, tag has to be deleted
                            if len(tag_to_remove_from_song.songs_tagged) == 0:
                                tag_to_remove_from_song.delete()
                        except:
                            pass

                # then we can remove song itself
                try:
                    all_files = SongFiles.objects.filter(song=song_id)
                    for file in all_files:
                        try:
                            if len(file.file) > 0:
                                os.remove(file.file.path)
                            file.delete()
                        except:
                            file.delete()
                    song.delete()
                except:
                    song.delete()
                return redirect('all_songs')

            else:
                return HttpResponseRedirect("../%s/0" % song_id)

        else:
            HttpResponse("NAWET NIE PRÓBUJ!!!")


class BackupView(SuperuserMixin, View):
    """Admin can check presence for the past events"""

    def get(self, request):
        now = datetime.now()
        full_time = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + ":" + str(
            now.minute)
        command = "python3 manage.py dumpdata --format json -e contenttypes -e auth.permission > backups/" + full_time + ".json"
        os.system(command)
        return redirect("/home")


class LittleHelperView(SuperuserMixin, View):
    """To be used when needed"""

    def get(self, request):
        return HttpResponse("git")
