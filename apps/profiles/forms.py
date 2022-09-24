from currencies.models import Currency
from django import forms
from apps.profiles.models import Profile


class ProfileForm(forms.ModelForm):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), required=False, help_text="Your currency")

    class Meta:
        model = Profile
        fields = (
            "image",
            "phone",
            "gender",
            "birth_day",
            "bio",
            "country",
            "city",
            "currency",
        )
