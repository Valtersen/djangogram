from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import *
from .models import *
from django.contrib import messages


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            author__in=request.user.following.all()).order_by('-created_at').all()[:10]
        context = {'posts': posts}
        if not posts:
            recommended_users = DUser.objects.annotate(count=Count('followers')).order_by(
                '-count').exclude(id=request.user.id).all()[:5]
            context['recommended_users'] = recommended_users
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
            return redirect('profile', request.user.username)
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

            for i in images:
                image = PostImage(image=i, post=post)
                image.save()
            form.save_m2m()
            return redirect(reverse('post_detail', args=(post.id,)))
            # return redirect('profile', request.user.username) #HERE
            # #like = Like.objects.filter(post=post, user=request.user).latest('id')
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
            return redirect('post_detail', post.id)
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
    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)


@login_required()
def like(request):
    post_id = request.POST.get('post_id')

    try:
        post = Post.objects.get(pk=post_id)
    except ObjectDoesNotExist:
        return HttpResponse('Could not find post')

    if request.user == post.author:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        if post.liked(request.user.id):
            like = Likes.objects.get(user=request.user.id, post=post.id)
            like.delete()
        else:
            like = Likes(user=request.user, post=post)
            like.save()
        html = render_to_string('like_section.html', {'post': post}, request=request)
        return JsonResponse({'form': html})


@login_required()
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    post.delete()
    return redirect('profile', request.user.username)


@login_required
def profile(request, username):
    profile = get_object_or_404(DUser, username=username)
    posts = profile.posts.all().order_by('-created_at')

    followers = profile.followers.count()
    following = profile.following.count()

    context = {
        'posts': posts,
        'profile': profile,
        'followers': followers,
        'following': following}

    if request.user == profile:
        return render(request, 'userprofile.html', context)
    else:
        return render(request, 'profile.html', context)


@login_required()
def follow(request):

    profile_id = request.POST.get('profile_id')
    try:
        profile = DUser.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        return HttpResponse('Could not find user')

    if profile == request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        followed = True if request.user in profile.followers.all() else False
        if followed:
            request.user.following.remove(profile)
            request.user.save()
        else:
            request.user.following.add(profile)
            request.user.save()

        html = render_to_string('follow_section.html', {'profile': profile}, request=request)
        return JsonResponse({'form': html})


@login_required()
def search_user(request):
    context = {}
    if request.GET.get('query'):
        query = request.GET.get('query')
        result = DUser.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query)).all()
        context = {'result': result, 'search': query}
    return render(request, 'search.html', context)


@login_required()
def posts_with_tag(request, tag):
    posts = Post.objects.filter(tags__name__icontains=tag).all()
    context = {'posts': posts, 'tag': tag}
    return render(request, 'posts_tag.html', context)


@login_required()
def users_liked(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_list =  DUser.objects.filter(liked__post=post)
    return render(request, 'user_list.html', {'user_list': user_list, 'page_name': f"Likes on post '{post.caption}'"})

