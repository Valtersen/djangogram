from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.contrib.auth.forms import *
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib import messages


def index(request):
    # Question.objects.filter(pub_date__lte=timezone.localtime(timezone.now())).order_by('-pub_date')[:7]
    posts = Post.objects.all().order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'home.html', context)


class SignUp(generic.CreateView):
    form_class = DUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def edit_user(request):
    if request.method == 'POST':
        form = DUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            request.user.save()
            messages.success(request, "Profile was updated successfully")
            return redirect('home')
    else:
        avatar_form = DUserAvatarForm(request.POST, instance=request.user)
        form = DUserChangeForm(instance=request.user)

    return render(request, 'registration/edituser.html', {'form': form, 'avatar_form': avatar_form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        image_form = PostImageForm(request.POST)
        images = request.FILES.getlist('image')
        if form.is_valid() and image_form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for i in images:
                image = PostImage(image=i, post=post)
                image.save()
            return redirect('home')
    else:
        form = PostForm()
        image_form = PostImageForm()

    return render(request, 'create_post.html', {'form': form, 'image_form': image_form})

# in your template.html <form> tag must include enctype="multipart/form-data"