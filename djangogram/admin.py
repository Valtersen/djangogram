from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *


class DUserAdmin(UserAdmin):
    add_form = DUserCreationForm
    form = DUserChangeForm
    model = DUser
    list_display = ["username", 'is_superuser', 'date_joined', 'last_login', 'email']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'avatar', 'bio', 'password')}),
        ('Time related', {'fields': ('last_login', 'date_joined')}),
        ('Other', {'fields': ('is_active', 'is_superuser', 'is_staff', 'user_permissions')}),
        ('Follow', {'fields': ('following',)})

    )
    filter_horizontal = ('following',)


admin.site.register(DUser, DUserAdmin)
admin.site.unregister(Group)

admin.site.register(Post)
admin.site.register(PostImage)

admin.site.register(Likes)

