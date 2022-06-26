from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *
# valter django2022
# anotherUser Userloh123
# valtersen DUser1234
# miha miha4321
# dusa ddd321321
# loh pass4321
# last_user nosense123
# felt cute cute123456
# anotherOne ohugh4321
# labaza fgdzzhzhFDVVZ
# EWANXNGFHX dsVVSBfSBfbe

class DUserAdmin(UserAdmin):
    add_form = DUserCreationForm
    form = DUserChangeForm
    model = DUser
    list_display = ["username", 'is_superuser', 'date_joined', 'last_login']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'avatar', 'bio', 'password')}),
        ('Time related', {'fields': ('last_login', 'date_joined')}),
        ('Other', {'fields': ('is_active', 'is_superuser', 'is_staff', 'user_permissions')})
    )


admin.site.register(DUser, DUserAdmin)
admin.site.unregister(Group)

admin.site.register(Post)
admin.site.register(PostImage)

