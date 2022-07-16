from django.test import TestCase
from django.test import Client
from allauth.utils import get_user_model
from allauth.account.models import EmailAddress
from django.urls import reverse

from social import settings


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'john'
        self.email = 'smith@mail.com'
        self.password = "password1"
        self.user = get_user_model().objects.create(username=self.username, email=self.email)
        self.user.set_password(self.password)
        EmailAddress.objects.create(
            user=self.user,
            email=self.email,
            primary=True,
            verified=True
        )

    def test_login(self):
        response = self.client.post('/login/',
                                    {"Username": self.username, "Password": self.password})
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False)




