from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User

class ViewsTests(TestCase):

    def setUp(self):
        test_user = User.objects.create(username="First", email="email.first@ema.il")
        test_user_pw = "First_password_123"
        self.test_user_pw = test_user_pw
        test_user.is_staff = True
        test_user.is_superuser = True
        test_user.save()
        test_user.set_password(test_user_pw)
        self.test_user = test_user

    def test_new_user_exists(self):
        users_number = User.objects.all().count()
        self.assertEqual(users_number, 1)
        self.assertNotEqual(users_number, 0)


    def test_user_password(self):
        # user_qs = User.objects.filter(username__iexact="Pierwszy")
        # user_exists = user_qs.exists() and user_qs.count() == 1
        # self.assertTrue(user_exists)
        # test_user = user_qs.first()
        self.assertTrue(self.test_user.check_password("First_password_123"))


    def test_login_url(self):
        # login_url = '/login'
        # self.assertEqual(settings.LOGIN_URL, login_url)
        login_url = settings.LOGIN_URL
        # response = self.client.post(url, {}, follow=True)
        data = {"username": "First", "password": self.test_user_pw}
        response = self.client.post(login_url, data, follow=True)
        print(dir(response))
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        print("kontrolnie:")
        # print(response.templates)
        print("i dalej:")
        print(redirect_path)
        print(status_code)

        # self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(status_code, 200)
