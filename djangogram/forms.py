from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class DUserCreationForm(UserCreationForm):
    class Meta:
        model = DUser
        fields = ('username', 'email', 'avatar', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'avatar': ClearableFileInput(),
        }


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
        fields = ('caption', 'text')


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
