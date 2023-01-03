from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import widgets

from songs_list.models import Song


def login_validator(value):
    try:
        User.objects.get(username=value)
    except ObjectDoesNotExist:
        raise ValidationError("zły login")
# , validators=[login_validator]

class LoginForm(forms.Form):
    username = forms.CharField(label="Użytkownik:", max_length=50)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


def new_login_validator(value):
    try:
        User.objects.get(username=value)
        raise ValidationError("taki login już istnieje!")
    except ObjectDoesNotExist:
        return None


class AddUserForm(forms.Form):
    username = forms.CharField(label="nazwa użytkownika", max_length=50, validators=[new_login_validator])
    password = forms.CharField(label="podaj hasło", max_length=50, widget=forms.PasswordInput)
    passwordRepeat = forms.CharField(label="potwierdź hasło", max_length=50, widget=forms.PasswordInput)
    name = forms.CharField(label="Imię", max_length=50)
    surname = forms.CharField(label="Nazwisko", max_length=50)
    email = forms.EmailField(label="Adres email", required=False)
    phone = forms.CharField(label="Numer telefonu", max_length=20, required=False)
    superuser = forms.BooleanField(label="Użytkownik na prawach administratora?", required=False)
    singer = forms.BooleanField(label="Użytkownik aktywnie śpiewający?", required=False)


class AddSongForm(forms.Form):
    name = forms.CharField(label="Nazwa utworu:", max_length=255)
    composer = forms.CharField(label="Kompozytor:", max_length=255, required=False)
    scores = forms.FileField(label="Nuty:", required=False)
    yt_link = forms.CharField(label="Link do youtybe'a:",required=False)
    description = forms.CharField(label="Opis:", required=False)
    duration = forms.DurationField(label="Czas trwania (gg:mm:ss):", required=False)


class EditSongForm(forms.Form):
    name = forms.CharField(label="Nazwa utworu:", max_length=255)
    composer = forms.CharField(label="Kompozytor:", max_length=255, required=False)
    yt_link = forms.CharField(label="Link do youtybe'a:", required=False)
    description = forms.CharField(label="Opis:", required=False)
    duration = forms.DurationField(label="Czas trwania (gg:mm:ss):", required=False)


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label="podaj hasło", max_length=50, widget=forms.PasswordInput)
    passwordRepeat = forms.CharField(label="potwierdź hasło", max_length=50, widget=forms.PasswordInput)





