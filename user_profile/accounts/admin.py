from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'first_name', 'last_name']

    list_display =['first_name', 'last_name', 'email', 'is_active', 'is_staff']

    list_filter = ['is_active', 'is_staff', 'date_joined']

    inlines = (UserProfileInline,)


admin.site.register(models.User, UserAdmin)
