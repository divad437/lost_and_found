from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from users.models import City, User


class DocumentImage(models.Model):
    image = models.ImageField(
        upload_to="documents/images/%Y/%m/%d/", verbose_name=_("Image")
    )
    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Document"),
    )

    class Meta:
        verbose_name = _("Document Image")
        verbose_name_plural = _("Document Images")
        order_with_respect_to = "document"

    def __str__(self):
        return _("{document} -- {image}").format(
            document=self.document.name, image=self.image
        )


class DocumentType(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Name"))
    slug = models.SlugField(max_length=30, verbose_name=_("Slug"), blank=True)

    class Meta:
        verbose_name = _("Document Type")
        verbose_name_plural = _("Document Types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Quarter(models.Model):
    name = models.CharField(max_length=40, verbose_name=_("Name"))
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="quarters", verbose_name=_("City")
    )

    class Meta:
        verbose_name = _("Quarter")
        verbose_name_plural = _("Quarters")
        ordering = ["name"]

    def __str__(self):
        return self.name


class FounderInformation(models.Model):
    first_name = models.CharField(max_length=30, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=30, verbose_name=_("Last Name"))
    phone_number = PhoneNumberField(
        null=True, blank=True, verbose_name=_("Phone Number")
    )

    class Meta:
        verbose_name = _("Founder Information")
        verbose_name_plural = _("Founder Informations")
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return _("{first_name} {last_name}").format(
            first_name=self.first_name, last_name=self.last_name
        )


class DepositPoint(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="deposit_points",
        verbose_name=_("City"),
    )
    quarter = models.ForeignKey(
        Quarter,
        on_delete=models.CASCADE,
        related_name="deposit_points",
        verbose_name=_("Quarter"),
    )
    address = models.CharField(max_length=200, verbose_name=_("Address"))
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))
    working_hours = models.CharField(max_length=100, verbose_name=_("Working Hours"))

    class Meta:
        verbose_name = _("Deposit Point")
        verbose_name_plural = _("Deposit Points")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Document(models.Model):
    class Status(models.TextChoices):
        FOUND = "FOUND", _("Found")
        LOST = "LOST", _("Lost")
        ARCHIVED = "ARCHIVED", _("Archived")

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documents",
        verbose_name=_("Document Type"),
    )
    found_city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documents",
        verbose_name=_("City where the document was found"),
    )
    found_quarter = models.ForeignKey(
        Quarter,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documents",
        verbose_name=_("Quarter where the document was found"),
    )
    date_found = models.DateField(null=True, verbose_name=_("Date Found"))
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.LOST,
        verbose_name=_("Status"),
    )
    founder = models.ForeignKey(
        FounderInformation,
        null=True,
        on_delete=models.SET_NULL,
        related_name="documents",
        verbose_name=_("Founder"),
    )
    deposit_point = models.ForeignKey(
        DepositPoint,
        null=True,
        on_delete=models.SET_NULL,
        related_name="documents",
        verbose_name=_("Deposit Point"),
    )
    description = models.TextField(verbose_name=_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name=_("Added By")
    )

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        if self.document_type:
            return _("{name} -- {category}").format(
                name=self.name, category=self.document_type.name
            )
        return self.name
