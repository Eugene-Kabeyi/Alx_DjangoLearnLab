from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin layout for the CustomUser model.
    """

    model = CustomUser

    # Fields displayed in admin list view
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')

    # Add custom fields to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional Info',
            {'fields': ('date_of_birth', 'profile_photo')}
        ),
    )

    # For add user page
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Additional Info',
            {'fields': ('date_of_birth', 'profile_photo')}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
