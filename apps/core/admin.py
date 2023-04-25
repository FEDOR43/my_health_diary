from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.core.models import User
from apps.core.models import UserProfile


@admin.register(User)
class CoreUserAdmin(UserAdmin):
    list_display = (
        "email",
        "is_email_confirmed",
        "get_short_name",
        "phone",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = (
        "is_email_confirmed",
        "is_phone_confirmed",
        "is_active",
        "groups",
    )
    ordering = ()
    search_fields = ("first_name", "last_name", "middle_name", "email", "phone")

    readonly_fields = ("last_login", "joined")
    fieldsets = (
        (
            "Контакты",
            {"fields": ("email", "is_email_confirmed", "phone", "is_phone_confirmed")},
        ),
        (
            "Персональная информация",
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "timezone",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Группы, права и безопасность",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "password",
                ),
                "classes": ("collapse", "wide"),
            },
        ),
        ("Важные даты", {"fields": ("last_login", "joined")}),
    )


@admin.register(UserProfile)
class CoreUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "birthday", "age")
    list_filter = ("age",)
    ordering = ()
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__middle_name",
        "user__email",
        "user__phone",
    )
