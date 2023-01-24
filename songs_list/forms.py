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


class UserForm(forms.Form):

    def __init__(self, edit, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.specific_user = kwargs.pop('specific_user')
        self.edit = edit
        super(UserForm, self).__init__(*args, **kwargs)

        # remove conditional fields
        if self.user.is_superuser:
            pass
        else:
            del self.fields['superuser']

        self.admins = User.objects.filter(is_active=True).filter(is_superuser=True)
        self.active_users = User.objects.filter(is_active=True)

    username = forms.CharField(label="nazwa użytkownika", max_length=50)
    name = forms.CharField(label="Imię", max_length=50)
    surname = forms.CharField(label="Nazwisko", max_length=50)
    email = forms.EmailField(label="Adres email", required=False)
    phone = forms.CharField(label="Numer telefonu", max_length=20, required=False)
    superuser = forms.BooleanField(label="Użytkownik na prawach administratora?", required=False)
    singer = forms.BooleanField(label="Użytkownik aktywnie śpiewający?", required=False)

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        if self.edit:
            if username != self.specific_user.username:
                if len(User.objects.filter(username=username)) > 0:
                    raise ValidationError("Login już zajęty! Spróbuj inny.")
        else:
            if len(User.objects.filter(username=username)) > 0:
                raise ValidationError("Login już zajęty! Spróbuj inny.")

    def clean_superuser(self):
        cleaned_data = super().clean()
        if not cleaned_data['superuser']:
            # if we add new user, specific user (here: "") is not in self.admins, so it would never raise error
            if self.specific_user in self.admins and len(self.admins) <= 2:
                raise ValidationError("Musi być choć dwóch administratorów!")


class AddUserForm(UserForm):
    password = forms.CharField(label="podaj hasło", max_length=50, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="potwierdź hasło", max_length=50, widget=forms.PasswordInput)

    def clean_password_repeat(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_repeat = cleaned_data['password_repeat']
        if password_repeat != password:
            raise ValidationError("Niepoprawnie powtórzone hasło!")


class EditUserForm(UserForm):
    active = forms.BooleanField(label="Aktywny użytkownik?", required=False)

    def clean_active(self):
        cleaned_data = super().clean()
        if not cleaned_data['active']:
            if self.specific_user.is_superuser and len(self.admins) <= 2:
                raise ValidationError("Musisz zostawić co najmniej 2 aktywnych administratorów!")





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





