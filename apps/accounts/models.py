from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from adieulane.utils import unique_slug_generator
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


def upload_dir(instance, filename):
    return f"{instance.username}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    # pkid = models.BigAutoField(primary_key=True, editable=False)
    # id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=40, unique=True)
    slug = models.SlugField(unique=True, )
    full_name = models.CharField(verbose_name=_("First&Last Name"), max_length=20, blank=True, null=True)
    phone = PhoneNumberField(verbose_name=_("Phone Number"), max_length=14, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone']

    class Meta:
        verbose_name_plural = _("Users")
        verbose_name = _("User")

    def __str__(self):
        return f"{self.username}"

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return f"{self.username}"

    @property
    def name(self):
        return self.username

    @property
    def get_user_initials(self):
        return f"{self.first_name.title()[0:1]}{self.last_name.title()[0:1]}"


@receiver(pre_save, sender=User)
def user_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

