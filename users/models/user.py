import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(_("ID"), primary_key=True)
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        auto_created=True,
    )
    first_name = models.CharField(_("First Name"), max_length=50, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=50, blank=True, null=True)
    contact = models.CharField(_("Contact"), max_length=15, null=True, blank=True)
    email = models.EmailField(_("Email Address"), unique=True, max_length=254)
    is_admin = models.BooleanField(_("Admin"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)
    archive = models.BooleanField(_("Archive"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    objects = CustomUserManager()


    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} || {self.email} || {self.contact}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def soft_delete(self, archive=False):
        self.archive = True if archive else False
        self.save()