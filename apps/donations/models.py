import logging
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.common.models import TimeStampedUUIDModel
from apps.memorials.models import BurialMemory
from apps.notifications.models import Notification
from django.utils.translation import gettext_lazy as _
from adieulane.flutterwave import FLUTTERWAVE_SECRET_KEY

logger = logging.getLogger(__name__)


class Donation(models.Model):
    burial_memory = models.ForeignKey(BurialMemory, related_name="donations", on_delete=models.CASCADE)
    donor_fullname = models.CharField(help_text="Your fullname", max_length=200, blank=True, null=True)
    donor_email = models.CharField(help_text="Your email", max_length=200, blank=True, null=True)
    currency = models.CharField(help_text="currency type", max_length=200, default="NGN", blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    trans_ref = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.burial_memory_id} -> {self.donor_fullname} {self.amount}"


@receiver(post_save, sender=Donation)
def user_add_donation_notification(sender, instance, *args, **kwargs):
    donation = instance
    donor = donation.donor_fullname
    message = f"{donor.title()} just donated the sum of {donation.currency}{donation.amount} burial levy for {donation.burial_memory.get_name}"
    Notification.objects.create(
        memorial_donation=donation,
        donation_by=donor,
        to_user=donation.burial_memory.by,
        notification_type=4,
        message=message,
    )


class DonationAccount(TimeStampedUUIDModel):
    SPLIT_TYPE = (
        ("percentage", "percentage"),
        ("flat", "flat"),
    )
    burial_memory = models.OneToOneField(BurialMemory, related_name="donation_account", on_delete=models.CASCADE)
    account_name = models.CharField(_("account name"), max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(_("account number"), max_length=11, blank=True, null=True)
    bank_code = models.CharField(_("account reference id"), max_length=100, blank=True, null=True)
    bank_name = models.CharField(_("bank name"), max_length=100, blank=True, null=True)
    sub_account_id = models.CharField(_("subaccount id"), max_length=200, blank=True, null=True)
    split_type = models.CharField(_("percentage or flat"), max_length=100, choices=SPLIT_TYPE, blank=True, null=True)
    split_value = models.FloatField(_("split value"), max_length=100, blank=True, null=True)
    balance = models.DecimalField(_("balance"), max_digits=100, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.burial_memory.get_name}-{self.id}-{self.balance}"


@receiver(post_save, sender=BurialMemory)
def create_memorial_donation_account(sender, instance, created, **kwargs):
    if created:
        DonationAccount.objects.create(burial_memory=instance)


@receiver(post_save, sender=BurialMemory)
def save_memorial_donation_account(sender, instance, **kwargs):
    instance.donation_account.save()
    logger.info(f"{instance}'s donation account created")


@receiver(pre_delete, sender=DonationAccount)
def delete_memorial_donation_account(sender, instance, **kwargs):
    try:
        import requests
        url = f"https://api.flutterwave.com/v3/subaccounts/{instance.sub_account_id}"
        payload = {}
        headers = {
            'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        print(response.text)
    except Exception as e:
        print(e)

