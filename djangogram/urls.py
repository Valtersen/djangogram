from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from social import settings
from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('logged_in/', RedirectView.as_view(pattern_name='home', permanent=False), name='logged_in'),
    path('edit/', views.edit_user, name='edituser'),
    path('create_post/', views.create_post, name='create_post'),
    path('profile/<username>/', views.profile, name='profile'),
    path('follow/profile/', views.follow, name='follow'),
    path('edit_post/<post_id>/', views.edit_post, name='edit_post'),
    path('post/<post_id>/', views.post_detail, name='post_detail'),
    path('post/<post_id>/delete/', views.delete_post, name='delete_post'),
    path('search/', views.search_user, name='search'),
    path('tag/<tag>', views.posts_with_tag, name='posts_with_tag'),
    path('like/post/', views.like, name='like'),
    path('liked/<post_id>/', views.users_liked, name='users_liked'),
    path('post/<post_id>/remove_image/<image_id>/', views.remove_image, name='remove_image')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
