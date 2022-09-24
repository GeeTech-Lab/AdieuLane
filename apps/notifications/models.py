from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Transaction_Message'),
        (2, 'Tribute_Message'),
        (3, 'Gallery_Message'),
        (4, 'Donation_message'),
    )
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    to_user = models.ForeignKey('accounts.User', related_name='notification_to', on_delete=models.CASCADE, blank=True, null=True)
    from_user = models.ForeignKey('accounts.User', related_name='notification_from', on_delete=models.CASCADE, blank=True, null=True)
    from_admin = models.CharField(max_length=100, blank=True, null=True, default="System Notification")
    memorial_tribute = models.ForeignKey('memorials.MemoryTribute', related_name='tribute_notifications', on_delete=models.CASCADE, blank=True, null=True)
    memorial_gallery = models.ForeignKey('memorials.MemoryGallery', related_name='gallery_notifications', on_delete=models.CASCADE, blank=True, null=True)
    memorial_donation = models.ForeignKey('donations.Donation', related_name='donation_notifications', on_delete=models.CASCADE, blank=True, null=True)
    donation_by = models.CharField(max_length=50, blank=True, null=True)
    wallet_transaction = models.ForeignKey('wallets.WalletTransaction', related_name='wallet_transaction_notifications', on_delete=models.CASCADE, blank=True, null=True)
    text_preview = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=225, blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.notification_type} -> {self.to_user.username}"
