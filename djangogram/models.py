from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from taggit.managers import TaggableManager
from io import BytesIO


class DUser(AbstractUser):
    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField(max_length=254)
    avatar = models.ImageField(default='default_hdqd19.png', null=True, upload_to='avatars')
    bio = models.CharField(max_length=200, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.avatar)

        if image.height > 200 or image.width > 200:
            size = 200, 200

            # Create a buffer to hold the bytes
            imageBuffer = BytesIO()

            # Resize
            image.thumbnail(size, Image.ANTIALIAS)

            # Save the image as jpeg to the buffer
            image.save(imageBuffer, image.format)

            # # CloudinaryImage("turtles.jpg").image(width=70, height=53, crop="scale")
            # new_img = CloudinaryImage(img).image(width=200, height=200, crop="scale")
            #img.thumbnail((200, 200))
            # new_img.save(self.avatar) cv2.resize(img, (300,300))
            #img.save(self.avatar, img.format)

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
    # image = models.ImageField(upload_to='posts/%Y/%m/%d', null=True)
    image = models.ImageField(null=True, blank=True, upload_to='posts/%Y/%m/%d')

    # resizing images
    # CloudinaryImage("turtles.jpg").image(width=70, height=53, crop="scale")
    # def save(self, *args, **kwargs):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 500 or img.width > 500:
    #         new_img = (500, 500)
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)

    def __str__(self):
        return self.post


class Likes(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(DUser, null=True, on_delete=models.CASCADE, related_name='liked')

    def __str__(self):
        return f"post: {self.post}, user: {self.user}"


