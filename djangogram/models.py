from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


class DUser(AbstractUser):
    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField(max_length=254)
    avatar = models.ImageField(default='default_hdqd19.png', null=True, upload_to='avatars')
    bio = models.CharField(max_length=200, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(DUser, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=200)
    text = models.CharField(max_length=2200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.caption


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=True, blank=True, upload_to='posts/%Y/%m/%d')

    def __str__(self):
        return self.post


class Likes(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(DUser, null=True, on_delete=models.CASCADE, related_name='liked')

    def __str__(self):
        return f"post: {self.post}, user: {self.user}"
