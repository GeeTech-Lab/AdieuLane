from django.contrib import admin

from apps.donations.models import Donation, DonationAccount

admin.site.register(Donation)

admin.site.register(DonationAccount)

# admin.site.register(DonationTransaction)
