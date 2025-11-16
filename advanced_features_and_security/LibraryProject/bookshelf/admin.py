from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('author', 'publication_year')

admin.site.register(Book, BookAdmin)
# ----------------------------------------
# CUSTOM USER ADMIN
# ----------------------------------------
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add custom fields to admin form
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )

# ----------------------------------------
# REGISTER MODELS
# ----------------------------------------
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)