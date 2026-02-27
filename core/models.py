from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.constants import StatusChoice
from core.middleware import CuserMiddleware
from core.utils.common import unique_slugify


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(
                f"Only one instance of {self.__class__.__name__} is allowed."
            )
        return super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance


class UpdatedByModel(models.Model):
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_modified",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if user and user.is_authenticated:
            self.updated_by = user
        return super().save(*args, **kwargs)


class CuserModel(UpdatedByModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if user and user.is_authenticated:
            if self._state.adding:
                self.created_by = user
            self.updated_by = user
        return super().save(*args, **kwargs)


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        abstract = True

    def _get_slug_text(self):
        assert any([hasattr(self, "name"), hasattr(self, "title")])
        slug_text = ""
        if hasattr(self, "name"):
            slug_text = self.name.lower()
        elif hasattr(self, "title"):
            slug_text = self.title.lower()
        return slug_text

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = self._get_slug_text()
            unique_slugify(self, slug_text)
        return super().save(*args, **kwargs)


class Status(models.Model):
    status = models.CharField(
        max_length=20,
        choices=StatusChoice.CHOICES,
        default=StatusChoice.PENDING,
    )

    class Meta:
        abstract = True


class Disabled(models.Model):
    """
    Abstract model for tracking the disabled state of other models.
    """

    disabled = models.BooleanField(_("disabled"), default=False)
    disabled_date = models.DateTimeField(null=True, blank=True)
    disabled_by = models.ForeignKey(
        "users.CustomUser", on_delete=models.SET_NULL, null=True, blank=True
    )
    disabled_reason = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        abstract = True
