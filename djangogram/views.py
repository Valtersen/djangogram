from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import generic
from django.contrib.auth.forms import *
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib import messages


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            author__in=request.user.following.all()).order_by('-created_at').all()
        context = {'posts': posts}
        return render(request, 'home.html', context)
    else:
        return redirect('account_login')


@login_required
def edit_user(request):
    if request.method == 'POST':
        form = DUserChangeForm(
            request.POST,
            request.FILES,
            instance=request.user)
        if form.is_valid():
            request.user.save()
            messages.success(request, "Profile was updated successfully")
            return redirect('home')
    else:
        form = DUserChangeForm(instance=request.user)

    return render(request, 'edituser.html', {'form': form, })


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
            form.save_m2m()

            for i in images:
                image = PostImage(image=i, post=post)
                image.save()
            return redirect('home')
    else:
        form = PostForm()
        image_form = PostImageForm()

    return render(
        request, 'create_post.html', {
            'form': form, 'image_form': image_form})


@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.author:
        return redirect('home')
    if request.method == 'POST':

        form = PostForm(request.POST, instance=post)
        image_form = PostChangeImageForm(request.POST, request.FILES,)
        images = request.FILES.getlist('image')
        if form.is_valid() and image_form.is_valid():
            form.save()
            for i in images:
                image = PostImage(image=i, post=post)
                image.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
        image_form = PostChangeImageForm

    return render(request,
                  'create_post.html',
                  {'form': form,
                   'image_form': image_form,
                   'edit': True,
                   'post_id': post_id})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    already_liked = True if request.user.id in post.likes.values_list(
        'user', flat=True) else False
    tags_post = list(post.tags.all())
    context = {
        'post': post,
        'liked': already_liked,
        'total': post.likes.count(),
        'tags_post': tags_post
    }
    return render(request, 'post_detail.html', context)


@login_required()
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        return redirect('post_detail', post_id=post_id)
    if Likes.objects.filter(user=request.user.id, post=post.id).exists():
        like = Likes.objects.get(user=request.user.id, post=post.id)
        like.delete()
    else:
        like = Likes(user=request.user, post=post)
        like.save()
    return redirect('post_detail', post_id=post_id)


@login_required()
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('home')
    post.delete()
    return redirect('home')


@login_required
def profile(request, username):
    owner = get_object_or_404(DUser, username=username)
    posts = owner.posts.all().order_by('-created_at')

    followers = owner.followers.count()
    following = owner.following.count()

    context = {
        'posts': posts,
        'owner': owner,
        'followers': followers,
        'following': following}

    if request.user == owner:
        return render(request, 'userprofile.html', context)
    else:
        followed = True if request.user in owner.followers.all() else False
        follows = True if request.user in owner.following.all() else False
        context['followed'] = followed
        context['follows'] = follows
        return render(request, 'profile.html', context)


@login_required()
def follow(request, username):
    owner = get_object_or_404(DUser, username=username)
    followed = True if request.user in owner.followers.all() else False
    if followed:
        request.user.following.remove(owner)
        request.user.save()
    else:
        request.user.following.add(owner)
        request.user.save()
    return redirect('profile', username=owner.username)


@login_required()
def search_user(request):
    context = {}
    if request.GET.get('query'):
        query = request.GET.get('query')
        result = DUser.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query)).all()
        context = {'result': result}
    return render(request, 'search.html', context)


@login_required()
def posts_with_tag(request, tag):
    posts = Post.objects.filter(tags__name__icontains=tag).all()
    context = {'posts': posts, 'tag': tag}
    return render(request, 'posts_tag.html', context)
