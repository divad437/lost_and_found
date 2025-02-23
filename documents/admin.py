from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from documents.models import (
    DepositPoint,
    Document,
    DocumentImage,
    DocumentType,
    FounderInformation,
    Quarter,
)


class DocumentImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        images_count = sum(
            1
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )

        if images_count < settings.MINIMUM_IMAGES_REQUIRED:
            raise ValidationError(
                _("A document must have at least 2 images to be saved.")
            )


class DocumentImageInline(admin.TabularInline):
    model = DocumentImage
    extra = 2
    fields = ["image"]
    formset = DocumentImageInlineFormSet


@admin.register(DocumentImage)
class DocumentImageAdmin(admin.ModelAdmin):
    list_display = ["id", "document", "image"]
    list_display_links = ["document"]
    search_fields = ["document__name"]
    ordering = ["id"]
    fields = ["document", "image"]
    list_filter = ["document"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("document", "image"),
            },
        ),
    )


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["id"]
    fields = ["name", "slug"]
    list_display_links = ["name"]
    list_filter = ["name"]


@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_display = ["name", "city"]
    search_fields = ["name", "city__name"]
    ordering = ["id"]
    fields = ["name", "city"]
    list_display_links = ["name"]
    list_filter = ["city"]


@admin.register(FounderInformation)
class FounderInformationAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone_number"]
    search_fields = ["first_name", "last_name", "phone_number"]
    ordering = ["last_name", "first_name"]
    fields = ["first_name", "last_name", "phone_number"]
    list_display_links = ["first_name"]
    list_filter = ["last_name", "first_name"]


@admin.register(DepositPoint)
class DepositPointAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "quarter"]
    search_fields = ["name", "city__name", "quarter__name"]
    ordering = ["id"]
    fields = ["name", "city", "quarter", "address", "phone_number", "working_hours"]
    list_display_links = ["name"]
    list_filter = ["city", "quarter"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["name", "document_type", "founder", "deposit_point"]
    search_fields = [
        "name",
        "document_type__name",
        "founder__first_name",
        "founder__last_name",
        "deposit_point__name",
    ]
    ordering = ["id"]
    list_display_links = ["name"]
    list_filter = ["document_type", "deposit_point"]
    inlines = [DocumentImageInline]
    readonly_fields = ["added_by", "created_at", "updated_at"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return (
                (
                    None,
                    {
                        "fields": (
                            "name",
                            "document_type",
                            "found_city",
                            "found_quarter",
                            "date_found",
                            "status",
                            "founder",
                            "deposit_point",
                            "description",
                        )
                    },
                ),
            )
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
