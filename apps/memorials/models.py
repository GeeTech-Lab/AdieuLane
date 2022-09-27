import logging
import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from adieulane.validators import MaxSizeValidator
from apps.notifications.models import Notification
from .util import RELATIONSHIP, BANKS
from adieulane.utils import unique_slug_generator


logger = logging.getLogger(__name__)


def upload_dir(instance, filename):
    return "{}/{}".format(instance.username, filename)


class BurialMemory(models.Model):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others")
    )
    user = models.ForeignKey("accounts.User", related_name="memories", on_delete=models.CASCADE)  # user.memories.all()
    title = models.CharField(help_text="Mr, Mrs, Miss, Sir....", max_length=100)
    first_name = models.CharField(help_text="John", max_length=100)
    last_name = models.CharField(help_text="Ezeh", max_length=100)
    other_names = models.CharField(help_text="Other titled names...", max_length=100, null=True, blank=True)
    gender = models.CharField(help_text="Male/Female", max_length=100, default="Others", choices=GENDER, null=True, blank=True)
    slug = models.SlugField(unique=True)
    image = CloudinaryField(
        folder='Nwaben_Burial_Images',
        blank=True,
        null=True,
        help_text="The deceased image",
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    date_of_birth = models.DateField()
    date_of_death = models.DateField()
    place_of_birth = models.CharField(help_text="City, State, Country", max_length=220, null=True, blank=True)
    place_of_death = models.CharField(help_text="City, State, Country", max_length=220, null=True, blank=True)
    cause_of_death = models.CharField(help_text="Sickness, Accident...", max_length=200, null=True, blank=True)
    brief_biography = models.TextField(help_text="Brief biography...", null=True, blank=True)
    education = models.TextField(help_text="Education...", null=True, blank=True)
    work_life = models.TextField(help_text="Work life...", null=True, blank=True)
    family_biography = models.TextField(help_text="Family's origin/history...", null=True, blank=True)
    burial_ceremony_address = models.CharField(help_text="Street, Town, City, State, Country", max_length=220,
                                               null=True, blank=True)
    accept_donations = models.BooleanField(help_text="Accept burial levy donation for the deceased?...", default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.title} {self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "BurialMemories"
        ordering = ("-created",)

    @property
    def get_name(self):
        return f"{self.title}-{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.title}-{self.first_name}{self.last_name}-{self.other_names}"

    @property
    def calculated_age(self):
        return self.date_of_death.year - self.date_of_birth.year - (
                    (self.date_of_death.month, self.date_of_death.day) < (
            self.date_of_birth.month, self.date_of_birth.day))

    @property
    def image_url(self):
        if self.image:
            return f"{self.image.url}"
        return "https://res.cloudinary.com/geetechlab-com/image/upload/v1659898818/nwaben.com/daddy_heaven_3_m0xhos.jpg"


@receiver(pre_save, sender=BurialMemory)
def blog_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_delete, sender=BurialMemory)
def burial_memory_image_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


class MemoryGallery(models.Model):
    by = models.ForeignKey("accounts.User", related_name="galleries", on_delete=models.CASCADE,
                           blank=True)  # user.galleries.all()
    burial_memory = models.ForeignKey(BurialMemory, related_name="galleries", on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, help_text="What was the event and where was it taken?...")
    image = CloudinaryField(
        folder='AdieuLane_Burial_Images_Gallery',
        blank=True,
        null=True,
        help_text="The deceased memory image",
        transformation={"quality": "auto:eco"},
        resource_type="image",
        validators=[MaxSizeValidator(5)],
    )
    # video = CloudinaryField(
    #     folder='AdieuLane_Burial_Video_Gallery',
    #     blank=True,
    #     null=True,
    #     help_text="The deceased memory video",
    #     transformation={"quality": "auto:eco"},
    #     resource_type="video",
    #     format="raw",
    # )
    video = models.URLField(max_length=200, blank=True, null=True, help_text="video youtube link")
    audio = CloudinaryField(
        folder='AdieuLane_Burial_Audio_Gallery',
        blank=True,
        null=True,
        help_text="The deceased memory audio",
        transformation={"quality": "auto:eco"},
        resource_type="auto",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.burial_memory.slug

    class Meta:
        verbose_name_plural = "MemoryGalleries"
        ordering = ("-created",)

    @property
    def image_url(self):
        return f"{self.image.url}"

    # @property
    # def video_url(self):
    #     return f"{self.video.url}"

    @property
    def audio_url(self):
        return f"{self.audio.url}"


@receiver(pre_delete, sender=MemoryGallery)
def memory_gallery_image_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


@receiver(post_save, sender=MemoryGallery)
def user_add_gallery_notification(sender, instance, *args, **kwargs):
    gallery = instance
    sender = gallery.user
    message = f"{sender.username} just uploaded a media for {gallery.burial_memory.get_name}"
    notify = Notification(
        memorial_gallery=gallery,
        from_user=sender,
        to_user=gallery.burial_memory.user,
        notification_type=3,
        message=message,
    )
    notify.save()


class FamilyTree(models.Model):
    burial_memory = models.OneToOneField(BurialMemory, related_name="family_trees", on_delete=models.CASCADE)
    title = models.CharField(help_text="Mr, Mrs, Miss, Sir....", max_length=100)
    guest_full_name = models.CharField(help_text="full name(John Ezeh)...", max_length=100)
    user_full_name = models.ForeignKey("accounts.User", related_name="family_trees", on_delete=models.CASCADE,
                                       blank=True)
    image = CloudinaryField(
        folder='Nwaben_Family_Tree_Images',
        blank=True,
        null=True,
        help_text="The deceased memory image",
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    relationship = models.CharField(help_text="Relationship with the deceased...", max_length=200, choices=RELATIONSHIP)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.full_name}"

    class Meta:
        verbose_name_plural = "FamilyTrees"
        ordering = ("-created",)

    def image_url(self):
        if self.image:
            return f"{self.image.url}"
        return "https://res.cloudinary.com/dptrfsirm/image/upload/v1658601579/bg_logos/logo_dygcg3.png"


@receiver(pre_delete, sender=FamilyTree)
def family_tree_image_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


class MemoryTribute(models.Model):
    CATEGORY = (
        ("candle", "candle"),
        ("flower", "flower"),
        ("note", "note"),
    )
    burial_memory = models.ForeignKey(BurialMemory, related_name="memory_tributes", on_delete=models.CASCADE)
    tribute_text = models.TextField()
    category = models.CharField(max_length=200, choices=CATEGORY, default="candle")
    by = models.ForeignKey("accounts.User", related_name="tributes", on_delete=models.CASCADE)
    on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.burial_memory.user.username} {self.tribute_text[:10]}"


@receiver(post_save, sender=MemoryTribute)
def user_add_tribute_notification(sender, instance, *args, **kwargs):
    tribute = instance
    sender = tribute.by
    message = f"{sender.username.title()} just added a tribute for {tribute.burial_memory.get_name}"
    notify = Notification(
        memorial_tribute=tribute,
        from_user=sender,
        to_user=tribute.burial_memory.user,
        notification_type=2,
        message=message,
    )
    notify.save()
