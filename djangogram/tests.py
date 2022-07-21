from django.test import TestCase
from django.test import Client
from allauth.utils import get_user_model
from allauth.account.models import EmailAddress
from dotenv import load_dotenv
from djangogram.models import *

load_dotenv()


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'john'
        self.email = 'smith@mail.com'
        self.password = "password1"
        self.bio = 'just a dude'
        self.user = get_user_model().objects.create(username=self.username, email=self.email, bio=self.bio)
        self.user.set_password(self.password)
        EmailAddress.objects.create(
            user=self.user,
            email=self.email,
            primary=True,
            verified=True
        )
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        post = Post(author=self.user, caption='first post', text='hi')
        post.save()
        post.tags.add('new', 'first post')
        post.save()

    def test_home_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/djangogram/', fetch_redirect_response=False)

    def test_profile(self):
        response = self.client.get('/djangogram/profile/john/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile.html')

    def test_create_post_get(self):
        response = self.client.get('/djangogram/create_post/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')

    def test_create_post_post(self):
        data = {
            'caption': 'second post',
            'text': 'hello',
            'tags': 'hi new tag',
        }
        response = self.client.post('/djangogram/create_post/', data)
        self.assertRedirects(response, '/djangogram/', fetch_redirect_response=False)
        post = Post.objects.get(caption='second post')
        self.assertEqual(post.text, 'hello')
        self.assertEqual(post.author.username, 'john')

        # test post in tags
        response = self.client.get('/djangogram/tag/new')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'first post' in response.content)
        self.assertTrue(b'second post' in response.content)

        # test post detail view
        response = self.client.get(f'/djangogram/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'second post' in response.content)
        self.assertTrue(b'Likes: 0' in response.content)

    def test_followers(self):
        response = self.client.get('/djangogram/profile/john/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'just a dude' in response.content)
        self.assertTemplateUsed(response, 'userprofile.html')
        self.assertTrue(b'0 followers' in response.content)

        # create user to follow
        follower = get_user_model().objects.create(username='follower', email='example@mail.com')
        follower.following.add(self.user)
        response = self.client.get('/djangogram/profile/john/')
        self.assertTrue(b'1 follower' in response.content)
        response = self.client.get('/djangogram/profile/follower/')
        self.assertTemplateUsed(response, 'profile.html')

    def test_search(self):
        response = self.client.get('/djangogram/search/?query=dude')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'john' and b'just a dude' in response.content)

    def test_edit(self):
        post = Post.objects.get(caption='first post')
        data = {
            'caption': '1st post',
            'text': 'hi',
            'tags': 'new, first post'
        }
        response = self.client.post(f'/djangogram/edit_post/{post.id}', data)
        self.assertRedirects(response, '/djangogram/', fetch_redirect_response=False)
        response = self.client.get(f'/djangogram/post/{post.id}')
        self.assertTrue(b'1st post' in response.content)

    def test_feed_and_likes(self):
        post_creator = get_user_model().objects.create(username='poster', email='example@email.com')
        post_creator.save()
        post = Post(author=post_creator, caption='example post', text='text.')
        post.save()
        self.user.following.add(post_creator)
        response = self.client.get('/djangogram/')
        self.assertTrue(b'example post' in response.content)

        like = Likes(user=self.user, post=post)
        like.save()
        response = self.client.get(f'/djangogram/post/{post.id}')
        self.assertTrue(b'1' in response.content)
