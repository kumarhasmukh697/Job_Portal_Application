from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Application, Job, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Job portal", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Job portal", {"fields": ("role", "email")}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "category", "employer", "is_active")
    list_filter = ("is_active", "category", "location")
    search_fields = ("title", "company", "location", "description")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "applicant", "status", "submitted_at")
    list_filter = ("status", "submitted_at")
    search_fields = ("job__title", "applicant__username", "applicant__email")
