from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from .models import *


class DUserCreationForm(UserCreationForm):
    class Meta:
        model = DUser
        fields = ('username', 'email', 'avatar', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'avatar': ClearableFileInput(),
        }

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.avatar = self.cleaned_data['avatar']
        user.bio = self.cleaned_data['bio']
        user.save()


class DUserChangeForm(forms.ModelForm):
    class Meta:
        model = DUser
        fields = ('username', 'avatar', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'avatar': ClearableFileInput(),
        }


class DUserAvatarForm(forms.ModelForm):
    class Meta:
        model = DUser
        fields = ('avatar',)
        widgets = {

            'avatar': ClearableFileInput(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'text', 'tags')


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)

        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True})
        }
        labels = {
            'image': 'Select one or multiple images'
        }


class PostChangeImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True})
        }
        labels = {
            'image': 'Add image/s to post'
        }
