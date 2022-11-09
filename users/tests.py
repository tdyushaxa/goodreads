from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register.html"),
            data={
                "username": "shaxa",
                "first_name": "maxmudov",
                "last_name": "shaxzod",
                "email": "smaxmudov015@@gmail.com",
                "password": "anybbody"
            }
        )

        user = CustomUser.objects.get(username="shaxa")
        self.assertEqual(user.first_name, "maxmudov")
        self.assertEqual(user.last_name, "shaxzod")
        self.assertEqual(user.email, "smaxmudov015@@gmail.com")
        self.assertNotEqual(user.password, "anybbody")
        self.assertTrue(user.check_password("anybbody"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register.html"),
            data={
                "first_name": "shaxa",
                "email": "smaxmudov015@@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register.html"),
            data={
                "username": "shaxa",
                "first_name": "maxmudov",
                "last_name": "shaxzod",
                "email": "smaxmudov015@@gmail.com",
                "password": "anybbody"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="shaxa", first_name="maxmudov")
        user.set_password("somepass")
        user.save()

        response = self.client.post(
            reverse("users:register.html"),
            data={
                "username": "shaxa",
                "first_name": "maxmudov",
                "last_name": "shaxzod",
                "email": "smaxmudov015@@gmail.com",
                "password": "anybbody"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        # DRY - Dont repeat yourself
        self.db_user = CustomUser.objects.create(username="shaxa", first_name="maxmudov")
        self.db_user.set_password("somepass")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "shaxa",
                "password": "somepass"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-user",
                "password": "somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "shaxa",
                "password": "wrong-password"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="shaxa", password="somepass")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="shaxa", first_name="maxmudov", last_name="shaxzod", email="smaxmudov015@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="shaxa", password="somepass")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="jakhongir", first_name="shaxa", last_name="maxmudov", email="smaxmuodv015@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="shaxa", password="somepass")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "shaxa",
                "first_name": "maxmudov",
                "last_name": "shaxzod",
                "email": "smaxmudov015@@gmail.com",
                "password": "anybbody"
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "smaxmudov015@@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))