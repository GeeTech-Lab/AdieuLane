import logging
import cloudinary
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from adieulane.settings import AUTH_USER_MODEL
from adieulane.utils import get_phone_country
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    phone = get_phone_country(instance.phone)
    if created:
        Profile.objects.create(user=instance, country=phone)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    logger.info(f"{instance}'s profile created")


@receiver(pre_delete, sender=Profile)
def profile_image_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)
