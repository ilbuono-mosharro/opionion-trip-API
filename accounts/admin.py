from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff', 'is_active', 'first_name', 'last_name',)
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'avatar', 'first_name', 'last_name', 'gender', 'email', 'email_confirmation', 'city', 'contry', 'age',
            'terms_and_privacy',)
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email',)


admin.site.register(User, UserAdmin)