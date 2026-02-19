from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class AccountsViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

    def test_signup_view_status_code(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse("accounts:profile")}"
        )

    def test_profile_view_authenticated(self):
        self.client.login(
            username="testuser",
            password="password123"
        )
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "registration/profile.html"
        )
