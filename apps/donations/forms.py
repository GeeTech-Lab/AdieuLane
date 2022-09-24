from django import forms
from apps.donations.models import Donation


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = (
            "donor_fullname",
            "amount",
        )