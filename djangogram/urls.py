from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from social import settings
from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('logged_in/', RedirectView.as_view(pattern_name='home', permanent=False), name='logged_in'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('edit/', views.edit_user, name='edituser'),
    path('create_post/', views.create_post, name='create_post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('search/', views.search_user, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

