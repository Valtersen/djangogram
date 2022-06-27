from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class DUser(AbstractUser):
    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField(max_length=254)
    avatar = models.ImageField(default='default.png', null=True, upload_to='avatars')
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(DUser, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=200)
    text = models.CharField(max_length=2200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    # image = models.ImageField(upload_to='posts/%Y/%m/%d', null=True)
    image = models.ImageField(null=True, blank=True, upload_to='posts/%Y/%m/%d')

    def __str__(self):
        return self.post
