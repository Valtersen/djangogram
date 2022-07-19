import os
from django.test import TestCase
from django.test import Client
from allauth.utils import get_user_model
from allauth.account.models import EmailAddress
from django.urls import reverse
from social import settings
from django.test.utils import override_settings
from dotenv import load_dotenv

load_dotenv()


@override_settings(
    DATABASES={
        'service': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'djangogram',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },  #f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    DATABASE_URL='postgresql://postgres:password@localhost:5432/djangogram'
)
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

    def test_create_post(self):
        url = reverse('create_post')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')
