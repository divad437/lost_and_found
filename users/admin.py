from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import forms as admin_forms
from django.contrib.auth.models import Group
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from users.models import City, User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("phone_number",)
        field_classes = {"email": EmailField}
        error_messages = {
            "phone_number": {"unique": _("This phone number has already been taken.")},
        }


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "location")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["phone_number", "first_name", "last_name", "email", "is_superuser"]
    list_display_links = ["email", "phone_number"]
    search_fields = ["first_name", "last_name", "email", "phone_number"]
    list_filter = ["is_staff", "is_active"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "email",
                    "location",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["id"]
    fields = ["name"]
    list_display_links = ["name"]
    list_filter = ["name"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name",),
            },
        ),
    )


admin.site.unregister(Group)
