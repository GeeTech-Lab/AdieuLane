from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='user', unique=True, always_update=True)
    gender = models.CharField(verbose_name=_("Gender"), max_length=20, choices=Gender.choices, default=Gender.OTHER)
    bio = models.TextField(verbose_name=_("About me"), default="Say something about yourself")
    image = CloudinaryField(
        verbose_name=_("Image"),
        folder='AdieuLane_UserProfile_Image',
        blank=True,
        null=True,
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    country = CountryField(verbose_name=_("Country"), default="US", blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=100, default="Lagos", blank=True, null=True)
    birth_day = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('profiles:profile_detail', kwargs={'slug': self.slug})

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return 'https://res.cloudinary.com/geetechlab-com/image/upload/v1583147406/nwaben.com/user_azjdde_sd2oje.jpg '


# class UserPreference(models.Model):
#     pass
